from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1913-Y5-R2FR-parent-action-object-and-q-functor-construction-or-finite-residual-branch.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1912_doc": ROOT / "1912-Y5-R2FR-neighbourhood-quotient-descent-signature-proof-or-axiom-ledger.md",
    "1912_validation": OUT / "P8_Y5_BRR545_1912_VALIDATION.csv",
    "1912_descent": OUT / "P8_Y5_PARENT_QLOC_1912_NEIGHBOURHOOD_DESCENT_SIGNATURE_ATTEMPT.csv",
    "1912_axiom_ledger": OUT / "P8_Y5_PARENT_QLOC_1912_MINIMAL_AXIOM_DEBT_LEDGER_NONCLAIM.csv",
    "1912_next": OUT / "P8_Y5_PARENT_QLOC_1912_NEXT_TARGET.csv",
    "990_parent_action": OUT / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
    "943_coframe_contract": OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
    "943_derivation": OUT / "P8_Y5_R10_943_DERIVATION_ATTEMPT.csv",
    "1045_matter_functor": OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1055_parent_candidate": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "1055_adoption_gates": OUT / "P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
    "1066_source_scalar": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
    "1087_matter_descent": OUT / "P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
    "1090_synthesis": OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv",
    "1630_ax1090": OUT / "P8_Y5_PARENT_QLOC_1630_AX1090_REDUCTION_STATUS.csv",
}


SOURCE_NEEDLES = {
    "1912_doc": ["NEXT1912_0_primary", "1913-Y5-R2FR-parent-action-object-and-q-functor-construction-or-finite-residual-branch.md"],
    "1912_validation": ["VAL1912_OVERALL,PASS"],
    "1912_descent": ["NQD1912_4_verdict", "DESCENT_PROOF_NOT_CLOSED_AXIOM_LEDGER_BUILT"],
    "1912_axiom_ledger": ["AX1912_0_parent_action_object", "MISSING_AXIOM_NOT_ADOPTED"],
    "1912_next": ["NEXT1912_0_primary", "parent action object and q-functor"],
    "990_parent_action": ["PAC990_0_parent_fields_and_quotient", "closure_visible_not_parent_signed"],
    "943_coframe_contract": ["CFC943_0_parent_quotient_map", "not_parent_signed_currently"],
    "943_derivation": ["DER943_6_verdict", "selected_as_next_derivation_target"],
    "1045_matter_functor": ["MFS1045_6_verdict", "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED"],
    "1055_parent_candidate": ["PAC1055_6_single_parent_action", "SCHEMA_WRITTEN_NOT_DERIVED_FROM_DEEPER_MTS"],
    "1055_adoption_gates": ["ADG1055_0_derivation_not_minimality", "ACTIVE_BLOCK"],
    "1066_source_scalar": ["SSE1066_5_verdict", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED"],
    "1087_matter_descent": ["PMD1087_6_verdict", "PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED"],
    "1090_synthesis": ["SYN1090_8_verdict", "SYNTHESIS_FAILS_MISSING_AXIOMS"],
    "1630_ax1090": ["AX1630_5_verdict", "AX1090_BUNDLE_NOT_REDUCED"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1913_SOURCE_REGISTER.csv",
    "construction_attempt": OUT / "P8_Y5_PARENT_QLOC_1913_PARENT_ACTION_Q_FUNCTOR_CONSTRUCTION_ATTEMPT.csv",
    "typing_matrix": OUT / "P8_Y5_PARENT_QLOC_1913_Q_FUNCTOR_TYPING_MATRIX_NONCLAIM.csv",
    "finite_residual_branch": OUT / "P8_Y5_PARENT_QLOC_1913_FINITE_RESIDUAL_BRANCH_NONCLAIM.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1913_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1913_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1913_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1913_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1913_VALIDATION.csv",
}


BRANCH_COPIES = {
    "construction_attempt": SOURCE_WEIGHT_DOCS / "PARENT_ACTION_Q_FUNCTOR_CONSTRUCTION_1913_NONCLAIM.csv",
    "finite_residual_branch": MICROSCOPE_COEFFS / "MTS_local_GR_finite_residual_branch_1913_nonclaim.csv",
    "typing_matrix": QUEUE / "JR1913_Q_FUNCTOR_TYPING_MATRIX_NONCLAIM.csv",
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_COEFFS, QUEUE, SOURCE_WEIGHT_DOCS]:
        path.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().lower()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing = [needle for needle in SOURCE_NEEDLES[source_id] if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(SOURCE_NEEDLES[source_id]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def construction_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "PAQ1913_0_target",
            "claim_piece": "one parent action object plus q-functor",
            "formal_statement": "Construct S_parent[Phi,A_Q,Psi_A,theta] with q:Phi->Q_obs, Obs_e:Q_obs->Coframe, and ordinary matter depending on Phi only through Obs_e(q(Phi)), A_Q(q), and fixed theta_A.",
            "construction_status": "TARGET_SHARP",
            "what_composes": "990/943/1045/1055 provide a coherent typed composite candidate",
            "what_fails": "candidate is a contract stack, not a parent-derived object/functor",
            "source_anchor": "PAC990_0_parent_fields_and_quotient; PAC1055_6_single_parent_action",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PAQ1913_1_typed_composite",
            "claim_piece": "typed composite action schema",
            "formal_statement": "S_parent = S_geom[Phi]+S_hidden[Phi]+S_EM[q(Phi),A_Q,ell_EM]+sum_A S_A[Psi_A,Obs_e(q(Phi)),omega[Obs_e(q(Phi))],A_Q,theta_A]+S_boundary[q(Phi)]+S_res.",
            "construction_status": "SCHEMA_COMPOSED_FROM_CURRENT_CONTRACTS",
            "what_composes": "all required symbols can be typed without contradiction if S_res retains unproven sectors",
            "what_fails": "S_res is nonempty because no-hidden-hom, measure/current, constants, boundary and readout closures are unsigned",
            "source_anchor": "PAC1055_0_configuration_and_quotient through PAC1055_6_single_parent_action",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PAQ1913_2_q_functor",
            "claim_piece": "q and observed coframe functor",
            "formal_statement": "If q and Obs_e are parent-owned, Dq[V]=0 implies Lie_V Obs_e(q(Phi))=0; this is enough for geometry silence but not yet matter-action descent.",
            "construction_status": "EXACT_CONDITIONAL_CHAIN_RULE_NOT_OWNER_PROOF",
            "what_composes": "943 and 1912 agree on the chain-rule lemma",
            "what_fails": "parent does not yet select q, Obs_e, allowed vertical distribution, or all local sectors",
            "source_anchor": "DER943_0_vertical_blindness; NQD1912_1_chain_rule",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PAQ1913_3_matter_functor",
            "claim_piece": "ordinary matter functor",
            "formal_statement": "Matter descent requires a parent functor A |-> E_A[Obs_e(q),A_Q,theta_A] plus fixed/gauge vertical lifts and fixed representation constants.",
            "construction_status": "MATTER_FUNCTOR_CONTRACT_NOT_CONSTRUCTED",
            "what_composes": "1045/1087 state the exact matter signature needed",
            "what_fails": "matter bundle, vertical lift, constants, source weights, hidden domain/boundary are not signed in one action",
            "source_anchor": "MFS1045_6_verdict; PMD1087_6_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PAQ1913_4_minimality_guard",
            "claim_piece": "no adoption by aesthetic minimality",
            "formal_statement": "Writing no f_X, no w_A, and no m_A(X) into a candidate action does not prove these slots are illegal unless the parent operator domain forbids them.",
            "construction_status": "ADOPTION_GUARD_ACTIVE",
            "what_composes": "1055 and 1066 show the desired syntax",
            "what_fails": "object-language typing and action-scale/current owner are unsigned",
            "source_anchor": "ADG1055_0_derivation_not_minimality; SSE1066_5_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PAQ1913_5_verdict",
            "claim_piece": "1913 parent action/q construction verdict",
            "formal_statement": "Current MTS corpus can write a consistent parent action/q-functor contract with explicit residual sector S_res, but cannot certify it as a parent-derived construction.",
            "construction_status": "CONSTRUCTION_CONTRACT_READY_PARENT_CERTIFICATION_FAILED",
            "what_composes": "typed composite plus exact q-chain-rule core",
            "what_fails": "AX1090 bundle remains unreduced, so local-GR/WEP claim remains blocked and finite residual branch must stay active",
            "source_anchor": "PAQ1913_0_target through PAQ1913_4_minimality_guard; AX1630_5_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def typing_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "typing_id": "QTM1913_0_parent_object",
            "object": "S_parent owner",
            "required_type": "one variational parent object before readout/projection/fitting",
            "candidate_source": "PAC1055_6_single_parent_action; PAC990_0_parent_fields_and_quotient",
            "current_status": "SCHEMA_WRITTEN_NOT_DERIVED",
            "if_missing": "contracts remain closure discipline rather than derivation",
            "valid_for_claim": False,
        },
        {
            "typing_id": "QTM1913_1_q_functor",
            "object": "q: Phi_parent -> Q_obs",
            "required_type": "parent-selected quotient functor with vertical distribution ker(Dq)",
            "candidate_source": "CFC943_0_parent_quotient_map; MFS1045_0_parent_field_quotient",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "observed-frame descent is a chosen representation, not parent law",
            "valid_for_claim": False,
        },
        {
            "typing_id": "QTM1913_2_Obs_e",
            "object": "Obs_e: Q_obs -> coframes",
            "required_type": "observed coframe/metric/connection functor",
            "candidate_source": "CFC943_1_observed_coframe_descent; MFS1045_1_observed_coframe_functor",
            "current_status": "CONDITIONAL_LEMMA_NOT_OWNER_PROOF",
            "if_missing": "chain-rule zero cannot be promoted",
            "valid_for_claim": False,
        },
        {
            "typing_id": "QTM1913_3_matter_bundle",
            "object": "ordinary matter bundle functor",
            "required_type": "Psi_A sections over observed quotient data and fixed representation constants",
            "candidate_source": "MFS1045_2_matter_bundle_functor; PMD1087_2_matter_lift",
            "current_status": "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED",
            "if_missing": "material response can re-enter through matter lift/frame",
            "valid_for_claim": False,
        },
        {
            "typing_id": "QTM1913_4_constants",
            "object": "theta_A constants",
            "required_type": "fixed representation/superselection data or retained finite residual fields",
            "candidate_source": "MFS1045_5_constants_split; PAC1055_2_matter_functor",
            "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "if_missing": "mass/charge/clock constants can become source currents",
            "valid_for_claim": False,
        },
        {
            "typing_id": "QTM1913_5_no_hidden_hom",
            "object": "hidden-to-visible coefficient maps",
            "required_type": "forbidden by parent operator domain or retained explicitly in S_res",
            "candidate_source": "PAC1055_3_no_mixed_coefficients; AX1630_1_no_hidden_visible_hom",
            "current_status": "MISSING_AXIOM_NOT_ADOPTED",
            "if_missing": "f_X F^2, m_A(X), disformal frames and source weights remain live",
            "valid_for_claim": False,
        },
        {
            "typing_id": "QTM1913_6_measure_current",
            "object": "hbar/action measure/current normalization",
            "required_type": "single species-blind owner",
            "candidate_source": "SSE1066_4_quantum_action_scale_obstruction; AX1630_2_common_quantum_measure",
            "current_status": "MISSING_AXIOM_NOT_ADOPTED",
            "if_missing": "relative action/source weights survive classical normalization",
            "valid_for_claim": False,
        },
        {
            "typing_id": "QTM1913_7_readout_boundary",
            "object": "boundary/readout/source-worldtube order",
            "required_type": "variation before readout plus exact/proper/common-mode boundary/domain terms or finite residuals",
            "candidate_source": "CFC943_5_tau_normal_lock; PAC990_5_Ward_Bianchi",
            "current_status": "OPEN_RETAIN_IN_S_RES",
            "if_missing": "post-selector or boundary source tail can fake a local pass",
            "valid_for_claim": False,
        },
        {
            "typing_id": "QTM1913_8_verdict",
            "object": "typed parent/q construction",
            "required_type": "all QTM1913_0 through QTM1913_7 signed",
            "candidate_source": "QTM1913_0_parent_object through QTM1913_7_readout_boundary",
            "current_status": "TYPED_CONTRACT_ONLY_NOT_PARENT_CERTIFIED",
            "if_missing": "move to finite residual branch",
            "valid_for_claim": False,
        },
    ]


def finite_residual_branch_rows() -> list[dict[str, Any]]:
    residuals = [
        ("FR1913_frame", "frame_or_coframe_residual", "hidden conformal/disformal/frame coefficient not proven zero"),
        ("FR1913_constants", "constant_sector_residual", "mass/charge/alpha/clock constants not proven quotient-owned"),
        ("FR1913_source_weight", "source_weight_residual", "w_A/source-label/common-measure-current not proven absent"),
        ("FR1913_matter_lift", "matter_lift_residual", "vertical lift of ordinary matter not parent-assigned"),
        ("FR1913_EM_hidden", "EM_hidden_F2_residual", "unique EM/F_Q^2 owner and radiative closure not signed"),
        ("FR1913_boundary_domain", "boundary_domain_residual", "boundary/domain/source-worldtube terms not proven silent"),
        ("FR1913_readout_tau", "readout_tau_residual", "variation-before-readout and tau/source kernel not sourced"),
    ]
    rows: list[dict[str, Any]] = []
    for residual_id, component, reason in residuals:
        rows.append(
            {
                "residual_id": residual_id,
                "component": component,
                "why_retained": reason,
                "accepted_forms": "DERIVED_ZERO; finite sourced coefficient with units/prior; or explicit nuisance row marked nonclaim",
                "forbidden_forms": "set to zero by minimality; absorb into measured GM/tau; infer from MICROSCOPE bound; cancel against another residual without identity",
                "current_value": "MISSING_OR_UNBOUNDED",
                "units": "dimensionless response or declared source/readout units",
                "source_anchor": "QTM1913 typing matrix; 1912 axiom ledger",
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1913_0_typed_composite",
            "condition": "parent action/q typed composite is internally coherent",
            "current_status": "PASS_CONTRACT_COMPOSED_NONCLAIM",
            "source_anchor": "PAQ1913_1_typed_composite",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1913_1_parent_certification",
            "condition": "S_parent owner, q functor, matter functor and operator domain are parent-derived",
            "current_status": "FAIL_PARENT_CERTIFICATION_MISSING",
            "source_anchor": "PAQ1913_5_verdict; QTM1913_8_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1913_2_finite_residuals",
            "condition": "all retained residual rows have derived zeros or finite sourced values",
            "current_status": "FAIL_FINITE_RESIDUAL_BRANCH_UNFILLED",
            "source_anchor": OUTPUTS["finite_residual_branch"].name,
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1913_3_claim",
            "condition": "1913 supports local-GR/Newton/WEP claim",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG1913_0_typed_composite through CG1913_2_finite_residuals",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1913_0_gain",
            "decision": "keep typed parent/q construction contract",
            "reason": "the composite is coherent and gives a precise parent action target",
            "status": "CONSTRUCTION_TARGET_SHARPENED",
            "next_dependency": "parent certification or finite residual fills",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1913_1_block",
            "decision": "do not certify construction",
            "reason": "q, Obs_e, matter functor, no-hidden-hom, measure/current and readout/boundary ownership are unsigned",
            "status": "PARENT_CERTIFICATION_FAILED",
            "next_dependency": "finite residual branch interface",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1913_2_next",
            "decision": "move to finite residual branch v0",
            "reason": "this preserves testability while the derivation route remains open",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "1914 finite residual branch no-cancellation interface",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1913_0_primary",
            "selection_status": "selected",
            "target_doc": "1914-Y5-R2FR-finite-residual-branch-v0-no-cancellation-interface.md",
            "target_script": "scripts/Y5_R2FR_finite_residual_branch_v0_no_cancellation_interface_1914.py",
            "objective": "turn the retained residual components from 1913 into a no-cancellation finite vector interface for WEP/PPN/R10/local tests, while keeping theorem-zero rows preferred where derivable",
            "success_condition": "finite residual vector contract with units, arenas, no-cancellation policy, and explicit nonclaim status",
            "do_not": "do not treat unfilled residual rows as local-GR pass or hide them in fitted calibration",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT1913_0_gain",
            "area": "parent action target",
            "summary": "a coherent typed S_parent/q/Obs_e/S_matter contract is now assembled in one place",
            "risk_level": "GOOD_STRUCTURE_NONCLAIM",
            "project_meaning": "the local-GR derivation target is no longer scattered across older ledgers",
            "next_action": "fill/certify owner signatures or residuals",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1913_1_block",
            "area": "derivation",
            "summary": "parent certification fails because the composite is not derived from deeper MTS primitives",
            "risk_level": "CENTRAL_OWNER_GAP",
            "project_meaning": "this is not grim, but it is the exact non-negotiable missing theorem",
            "next_action": "finite residual interface while derivation remains open",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1913_2_testability",
            "area": "empirical branch",
            "summary": "finite residual components are now named so they can be bounded without pretending zero",
            "risk_level": "TESTABLE_FALLBACK_READY",
            "project_meaning": "keeps the theory honest and competitive even before full GR reduction is proved",
            "next_action": "1914 no-cancellation vector",
            "valid_for_claim": False,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "construction_attempt": construction_attempt_rows(),
        "typing_matrix": typing_matrix_rows(),
        "finite_residual_branch": finite_residual_branch_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    for key, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def claim_flags_safe(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in ["valid_for_claim", "claim_allowed", "gate_pass", "parent_signed", "score_ready"]:
                if field in row and bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all claim/parent/score flags remain false"


def construction_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    required = {
        "PAQ1913_1_typed_composite": "SCHEMA_COMPOSED_FROM_CURRENT_CONTRACTS",
        "PAQ1913_5_verdict": "CONSTRUCTION_CONTRACT_READY_PARENT_CERTIFICATION_FAILED",
    }
    bad = []
    row_by_id = {row["attempt_id"]: row for row in rows}
    for row_id, status in required.items():
        if row_id not in row_by_id:
            bad.append(f"{row_id}:missing")
        elif row_by_id[row_id]["construction_status"] != status:
            bad.append(f"{row_id}:{row_by_id[row_id]['construction_status']}")
    return not bad, "; ".join(bad) if bad else "typed composite exists and certification fails safely"


def residual_branch_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    required = {"frame_or_coframe_residual", "constant_sector_residual", "source_weight_residual", "matter_lift_residual", "EM_hidden_F2_residual", "boundary_domain_residual", "readout_tau_residual"}
    present = {row["component"] for row in rows}
    bad = []
    missing = required - present
    if missing:
        bad.append(f"missing={sorted(missing)}")
    for row in rows:
        if row["current_value"] != "MISSING_OR_UNBOUNDED":
            bad.append(f"{row['residual_id']}:unexpected_value")
    return not bad, "; ".join(bad) if bad else "finite residual branch components present and unfilled"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1913_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    construction_ok, construction_detail = construction_valid(csv_rows(OUTPUTS["construction_attempt"]))
    checks.append({"validation_id": "VAL1913_01_construction_attempt", "status": "PASS" if construction_ok else "FAIL", "detail": construction_detail, "valid_for_claim": False})
    typing_rows = csv_rows(OUTPUTS["typing_matrix"])
    checks.append({"validation_id": "VAL1913_02_typing_matrix", "status": "PASS" if any(row["typing_id"] == "QTM1913_8_verdict" and row["current_status"] == "TYPED_CONTRACT_ONLY_NOT_PARENT_CERTIFIED" for row in typing_rows) else "FAIL", "detail": "typing matrix verdict blocks certification", "valid_for_claim": False})
    residual_ok, residual_detail = residual_branch_valid(csv_rows(OUTPUTS["finite_residual_branch"]))
    checks.append({"validation_id": "VAL1913_03_finite_residual_branch", "status": "PASS" if residual_ok else "FAIL", "detail": residual_detail, "valid_for_claim": False})
    gates = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1913_04_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1913_3_claim" and row["current_status"] == "CLAIM_BLOCKED" for row in gates) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1913_05_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1913_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1914 finite residual branch route selected", "valid_for_claim": False})
    flags_ok, flags_detail = claim_flags_safe(generated_without_validation)
    checks.append({"validation_id": "VAL1913_06_claim_flags_safe", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1913_07_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1913_08_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1913_09_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1913-Y5-R2FR-parent-action-object",
            "P8_Y5_PARENT_QLOC_1913",
            "Y5_R2FR_parent_action_object_and_q_functor_construction_or_finite_residual_branch_1913",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append({"validation_id": "VAL1913_10_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1913_artifact_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1913_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1913 parent action object and q-functor construction or finite residual branch", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1913 - Parent Action Object And q-Functor Construction Or Finite Residual Branch

## Purpose

This checkpoint tries to construct the one parent action object and `q`-functor needed to make the 1912 descent route derived rather than closure-only. The typed composite can be assembled consistently, but current evidence does not certify it as parent-derived. The honest result is therefore a finite residual branch, not a local-GR claim.

## Result

- Assembled a coherent typed candidate `S_parent/q/Obs_e/S_matter` composite.
- Retained the exact conditional `q`-chain-rule core.
- Refused certification because parent ownership of `q`, `Obs_e`, matter bundle, constants, hidden-hom exclusion, measure/current, and readout/boundary order is unsigned.
- Staged a finite residual branch so unproved zeros become explicit rows instead of hidden closure.
- Next target is a no-cancellation finite residual vector interface.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Construction Attempt

{markdown_table(rows_by_name["construction_attempt"])}

## q-Functor Typing Matrix

{markdown_table(rows_by_name["typing_matrix"])}

## Finite Residual Branch

{markdown_table(rows_by_name["finite_residual_branch"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
