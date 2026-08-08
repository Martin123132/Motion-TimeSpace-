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

DOC = ROOT / "1912-Y5-R2FR-neighbourhood-quotient-descent-signature-proof-or-axiom-ledger.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1911_doc": ROOT / "1911-Y5-R2FR-nonuniversal-material-coefficient-zero-theorem-or-finite-CX-contract.md",
    "1911_validation": OUT / "P8_Y5_BRR545_1911_VALIDATION.csv",
    "1911_zero_theorem": OUT / "P8_Y5_PARENT_QLOC_1911_NONUNIVERSAL_COEFFICIENT_ZERO_THEOREM_ATTEMPT.csv",
    "1911_premise_matrix": OUT / "P8_Y5_PARENT_QLOC_1911_ZERO_THEOREM_PREMISE_MATRIX_NONCLAIM.csv",
    "1911_next": OUT / "P8_Y5_PARENT_QLOC_1911_NEXT_TARGET.csv",
    "1088_minimal_signature": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "1090_synthesis": OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv",
    "1090_axioms": OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
    "1486_neighbourhood": MICROSCOPE_COEFFS / "neighbourhood_quotient_descent_attempt_nonclaim_1486.csv",
    "1630_ax1090_status": OUT / "P8_Y5_PARENT_QLOC_1630_AX1090_REDUCTION_STATUS.csv",
    "1760_descent_audit": OUT / "P8_Y5_PARENT_QLOC_1760_DESCENT_PREMISE_AUDIT.csv",
    "1786_boundary_matter": OUT / "P8_Y5_PARENT_QLOC_1786_BOUNDARY_MATTER_CLOSURE_GATE.csv",
    "1787_extra_sector": OUT / "P8_Y5_PARENT_QLOC_1787_EXTRA_SECTOR_SILENCE_MATRIX.csv",
}


SOURCE_NEEDLES = {
    "1911_doc": ["NEXT1911_0_primary", "1912-Y5-R2FR-neighbourhood-quotient-descent-signature-proof-or-axiom-ledger.md"],
    "1911_validation": ["VAL1911_OVERALL,PASS"],
    "1911_zero_theorem": ["CXZ1911_4_verdict", "ZERO_THEOREM_SHARP_NOT_PARENT_SIGNED"],
    "1911_premise_matrix": ["PREM1911_0_neighbourhood_descent", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"],
    "1911_next": ["NEXT1911_0_primary", "neighbourhood quotient descent"],
    "1088_minimal_signature": ["MOMS1088_7_verdict", "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED"],
    "1090_synthesis": ["SYN1090_8_verdict", "SYNTHESIS_FAILS_MISSING_AXIOMS"],
    "1090_axioms": ["AX1090_0_parent_object", "MISSING_AXIOM_NOT_ADOPTED"],
    "1486_neighbourhood": ["NQD1486_5_verdict", "NOT_CLOSED_SOURCE_MAP_BUILT"],
    "1630_ax1090_status": ["AX1630_5_verdict", "AX1090_BUNDLE_NOT_REDUCED"],
    "1760_descent_audit": ["PRE1760_8_verdict", "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED"],
    "1786_boundary_matter": ["BMC1786_5_verdict", "BOUNDARY_MATTER_CLOSURE_NOT_CLOSED"],
    "1787_extra_sector": ["ESM1787_7_matter_frame", "MATTER_NO_SPURION_CERTIFICATE_MISSING"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1912_SOURCE_REGISTER.csv",
    "descent_attempt": OUT / "P8_Y5_PARENT_QLOC_1912_NEIGHBOURHOOD_DESCENT_SIGNATURE_ATTEMPT.csv",
    "axiom_ledger": OUT / "P8_Y5_PARENT_QLOC_1912_MINIMAL_AXIOM_DEBT_LEDGER_NONCLAIM.csv",
    "closure_refusal": OUT / "P8_Y5_PARENT_QLOC_1912_CLOSURE_SHORTCUT_REFUSAL_MATRIX.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1912_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1912_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1912_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1912_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1912_VALIDATION.csv",
}


BRANCH_COPIES = {
    "descent_attempt": SOURCE_WEIGHT_DOCS / "NEIGHBOURHOOD_DESCENT_SIGNATURE_ATTEMPT_1912_NONCLAIM.csv",
    "axiom_ledger": MICROSCOPE_COEFFS / "MTS_local_GR_minimal_axiom_debt_1912_nonclaim.csv",
    "closure_refusal": QUEUE / "JR1912_CLOSURE_SHORTCUT_REFUSAL_MATRIX.csv",
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


def descent_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "descent_id": "NQD1912_0_target",
            "claim_piece": "ordinary-matter neighbourhood quotient descent",
            "formal_statement": "Find an open U around the local branch such that S_ord[Phi,Psi,theta]=Sbar_ord[q(Phi),Psi_q,theta] and all WEP/material vertical flows remain in q-fibres.",
            "result": "TARGET_SHARP",
            "proved_here": "this is the exact missing premise required by 1911 to import C_X=0",
            "not_proved_here": "existence of one parent action object and one parent matter functor",
            "source_anchor": "CXZ1911_1_descent_theorem; NQD1486_0_target",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "descent_id": "NQD1912_1_chain_rule",
            "claim_piece": "vertical blindness of observed geometry",
            "formal_statement": "If e_obs=Obs_e(q(Phi)) and Dq[V]=0, then Lie_V e_obs=0 and Lie_V g_obs=0 by the chain rule.",
            "result": "EXACT_CONDITIONAL_POINTWISE_LEMMA",
            "proved_here": "geometry silence follows once q and Obs_e are parent-owned and V is q-vertical",
            "not_proved_here": "q/Obs_e parent ownership and open-neighbourhood matter descent",
            "source_anchor": "NQD1486_1_chain_rule; SYN1090_2_quotient_pullback",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "descent_id": "NQD1912_2_open_neighbourhood_upgrade",
            "claim_piece": "pointwise silence upgraded to action descent on U",
            "formal_statement": "The pointwise chain-rule lemma must extend to the full ordinary-matter action, fields, constants, boundary class, and source/readout ordering on an open neighbourhood.",
            "result": "UPGRADE_FAILS_PARENT_SIGNATURE_MISSING",
            "proved_here": "the exact upgrade requirements are identified",
            "not_proved_here": "matter bundle functor, constant sector, no species weights, no shadow domain, and variation order",
            "source_anchor": "MOMS1088_0_action_form through MOMS1088_7_verdict; SYN1090_8_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "descent_id": "NQD1912_3_countermodel_retention",
            "claim_piece": "descent countermodels remain live",
            "formal_statement": "A shadow matter frame, hidden-visible coefficient hom, species/source weight, fixed-constant leak, boundary/domain selector, or post-readout source selector can break descent while preserving visible covariance.",
            "result": "COUNTERMODELS_RETAINED",
            "proved_here": "why adopting local GR universality as a shortcut would be closure-only",
            "not_proved_here": "operator-domain theorem excluding those countermodels",
            "source_anchor": "AX1090_1_no_hidden_visible_hom; PRE1760_4_no_shadow_prefactor; ESM1787_7_matter_frame",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "descent_id": "NQD1912_4_verdict",
            "claim_piece": "1912 descent/signature proof verdict",
            "formal_statement": "Current evidence proves the conditional chain-rule route but not the parent ordinary-matter neighbourhood descent theorem.",
            "result": "DESCENT_PROOF_NOT_CLOSED_AXIOM_LEDGER_BUILT",
            "proved_here": "the minimum axiom/proof debt needed to close C_X=0 is explicit",
            "not_proved_here": "local-GR/WEP claim-grade descent",
            "source_anchor": "NQD1912_0_target through NQD1912_3_countermodel_retention",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def axiom_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "axiom_id": "AX1912_0_parent_action_object",
            "minimal_clause": "one parent action object exists before readout/projection/fitting and owns ordinary matter",
            "why_needed": "contracts cannot derive each other without one owner",
            "current_basis": "AX1090_0_parent_object; SYN1090_1_action_object",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "danger_if_adopted": "turns the local branch into inserted minimality rather than MTS derivation",
            "adopted": False,
            "valid_for_claim": False,
        },
        {
            "axiom_id": "AX1912_1_q_functor",
            "minimal_clause": "q: Phi_parent -> Q_obs and observed coframe/connection functor are parent-selected",
            "why_needed": "chain-rule vertical blindness only works after q and Obs_e are owned",
            "current_basis": "PRE1760_0_q_map; PRE1760_1_observed_geometry; NQD1486_1_chain_rule",
            "status": "NOT_PARENT_SIGNED",
            "danger_if_adopted": "could assume the desired observed-frame reduction",
            "adopted": False,
            "valid_for_claim": False,
        },
        {
            "axiom_id": "AX1912_2_matter_bundle_functor",
            "minimal_clause": "ordinary matter fields are sections of bundles over observed quotient data only",
            "why_needed": "forbids independent matter lift along quotient-vertical directions",
            "current_basis": "MOMS1088_2_matter_bundle; SYN1090_3_matter_lift",
            "status": "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR",
            "danger_if_adopted": "could silently impose EEP on matter rather than derive it",
            "adopted": False,
            "valid_for_claim": False,
        },
        {
            "axiom_id": "AX1912_3_fixed_constant_sector",
            "minimal_clause": "ordinary masses, charges, alpha_EM, clocks and representation labels are fixed or retained as explicit residuals",
            "why_needed": "constant-sector leaks become WEP/clock/fine-structure source currents",
            "current_basis": "AX1090_3_fixed_constant_sector; MOMS1088_3_constant_superselection",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "danger_if_adopted": "hides real EM/mass coupling debt",
            "adopted": False,
            "valid_for_claim": False,
        },
        {
            "axiom_id": "AX1912_4_no_species_source_weights",
            "minimal_clause": "no w_A(X)S_A, material marker, source-only multiplier, or species Jacobian exists before variation",
            "why_needed": "otherwise Hilbert source can carry nonuniversal material coefficients",
            "current_basis": "MOMS1088_4_no_species_weights; OG1451_6_verdict; PRE1760_7_hilbert_source_owner",
            "status": "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED",
            "danger_if_adopted": "assumes away the strongest WEP countermodel",
            "adopted": False,
            "valid_for_claim": False,
        },
        {
            "axiom_id": "AX1912_5_common_measure_current",
            "minimal_clause": "one hbar/action measure/current normalization applies to all ordinary sectors",
            "why_needed": "removes measure/current rescalings that survive classical EOM normalization",
            "current_basis": "AX1090_2_common_quantum_measure; SIGN1462_0_common_measure_current",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "danger_if_adopted": "imports quantum/statistical structure not derived from MTS primitives",
            "adopted": False,
            "valid_for_claim": False,
        },
        {
            "axiom_id": "AX1912_6_no_shadow_hidden_hom",
            "minimal_clause": "no hidden/representative variable maps into visible matter coefficients except through q_obs or fixed data",
            "why_needed": "kills conformal/disformal matter frames and f_X F^2 style hidden couplings",
            "current_basis": "AX1090_1_no_hidden_visible_hom; ESM1787_7_matter_frame",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "danger_if_adopted": "too strong unless tied to real quotient/category construction",
            "adopted": False,
            "valid_for_claim": False,
        },
        {
            "axiom_id": "AX1912_7_variation_before_readout",
            "minimal_clause": "all source/current variations occur before readout, material projection, calibration and fitting",
            "why_needed": "prevents post-variation selectors from manufacturing or erasing C_X",
            "current_basis": "AX1090_4_variation_domain_order; SIGN1454_0_readout_order",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "danger_if_adopted": "over-constrains detector/source physics unless tied to a readout model",
            "adopted": False,
            "valid_for_claim": False,
        },
        {
            "axiom_id": "AX1912_8_boundary_domain_silence",
            "minimal_clause": "boundary, domain, worldtube and support terms are exact/proper/common-mode or explicitly bounded",
            "why_needed": "boundary/domain source tails can re-enter local material/source coefficients",
            "current_basis": "BMC1786_0_boundary_representative; BMC1786_1_matter_interface; PRE1760_6_boundary",
            "status": "BOUNDARY_DOMAIN_SILENCE_OPEN",
            "danger_if_adopted": "could hide physical edge/source terms",
            "adopted": False,
            "valid_for_claim": False,
        },
    ]


def closure_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "CR1912_0_EEP_axiom",
            "shortcut": "adopt metric universality/EEP for ordinary matter and call local GR reduction derived",
            "why_refused": "that would insert the desired result instead of deriving descent from MTS parent structure",
            "allowed_use": "private closure label only, never claim-grade derivation",
            "current_status": "REFUSED_AS_DERIVATION",
            "valid_for_claim": False,
        },
        {
            "refusal_id": "CR1912_1_pointwise_to_neighbourhood",
            "shortcut": "use pointwise chain-rule silence as open-neighbourhood action descent",
            "why_refused": "pointwise geometry silence does not sign matter lifts, constants, boundaries, or source/readout order",
            "allowed_use": "conditional lemma only",
            "current_status": "REFUSED_SCOPE_OVERREACH",
            "valid_for_claim": False,
        },
        {
            "refusal_id": "CR1912_2_no_countermodel_by_covariance",
            "shortcut": "claim covariance excludes species weights/shadow frames/source selectors",
            "why_refused": "covariant countermodels remain live in 1911/1090/1760 ledgers",
            "allowed_use": "countermodel target list",
            "current_status": "REFUSED_COVARIANCE_ONLY",
            "valid_for_claim": False,
        },
        {
            "refusal_id": "CR1912_3_public_claim",
            "shortcut": "treat 1912 as local-GR/WEP pass",
            "why_refused": "axiom ledger is unadopted and parent descent is not closed",
            "allowed_use": "internal proof roadmap",
            "current_status": "CLAIM_REFUSED",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1912_0_chain_rule",
            "condition": "observed geometry vertical-blindness chain rule is exact",
            "current_status": "PASS_CONDITIONAL_POINTWISE",
            "source_anchor": "NQD1912_1_chain_rule",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1912_1_neighbourhood_descent",
            "condition": "ordinary matter action descends through q_obs on open U",
            "current_status": "FAIL_DESCENT_PROOF_NOT_CLOSED",
            "source_anchor": "NQD1912_4_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1912_2_axioms",
            "condition": "minimal axiom ledger is reduced or explicitly adopted as closure",
            "current_status": "FAIL_AXIOMS_MISSING_NOT_ADOPTED",
            "source_anchor": OUTPUTS["axiom_ledger"].name,
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1912_3_claim",
            "condition": "1912 supports local-GR/WEP coefficient-zero claim",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG1912_0_chain_rule through CG1912_2_axioms",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1912_0_keep",
            "decision": "keep chain-rule descent lemma",
            "reason": "it is exact and remains the mathematical core of the local-GR route",
            "status": "CONDITIONAL_CORE_RETAINED",
            "next_dependency": "parent action object and q-functor construction",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1912_1_refuse",
            "decision": "do not adopt EEP/metric universality as proof",
            "reason": "the goal is derivability, so closure axioms must stay labelled as debt",
            "status": "CLOSURE_SHORTCUT_REFUSED",
            "next_dependency": "try to reduce AX1912_0 and AX1912_1 first",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1912_2_next",
            "decision": "attack parent action object and q-functor",
            "reason": "without one parent owner and q functor, all other descent clauses float as contracts",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "1913 parent action object and q-functor construction",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1912_0_primary",
            "selection_status": "selected",
            "target_doc": "1913-Y5-R2FR-parent-action-object-and-q-functor-construction-or-finite-residual-branch.md",
            "target_script": "scripts/Y5_R2FR_parent_action_object_and_q_functor_construction_or_finite_residual_branch_1913.py",
            "objective": "try to construct the one parent action object and q-functor that would make ordinary-matter descent derived; if it fails, move to finite residual branch cleanly",
            "success_condition": "parent-owned action/q-functor construction, or exact finite residual branch decision without local-GR claim",
            "do_not": "do not relabel an unadopted axiom ledger as a derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT1912_0_gain",
            "area": "derivation map",
            "summary": "the exact chain-rule spine is isolated: q-vertical directions cannot affect observed geometry if q and Obs_e are parent-owned",
            "risk_level": "USEFUL_CONDITIONAL_CORE",
            "project_meaning": "we know exactly what would make local GR reduction derivable",
            "next_action": "construct parent action object and q-functor",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1912_1_block",
            "area": "axiom debt",
            "summary": "open-neighbourhood matter descent is not proved; adopting it would be EEP/GR universality by closure",
            "risk_level": "CORE_AXIOM_DEBT",
            "project_meaning": "the work is not dead, but the central derivation is still ahead",
            "next_action": "reduce AX1912_0/AX1912_1 or pivot to finite residuals",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1912_2_safety",
            "area": "claim discipline",
            "summary": "all closure shortcuts are refused and formalization-workbench remains untouched",
            "risk_level": "SAFE_NONCLAIM",
            "project_meaning": "we improved rigor without overclaiming",
            "next_action": "1913",
            "valid_for_claim": False,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "descent_attempt": descent_attempt_rows(),
        "axiom_ledger": axiom_ledger_rows(),
        "closure_refusal": closure_refusal_rows(),
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
            for field in ["valid_for_claim", "claim_allowed", "gate_pass", "parent_signed", "adopted"]:
                if field in row and bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all claim/adoption/parent-signed flags remain false"


def descent_attempt_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    required = {
        "NQD1912_1_chain_rule": "EXACT_CONDITIONAL_POINTWISE_LEMMA",
        "NQD1912_4_verdict": "DESCENT_PROOF_NOT_CLOSED_AXIOM_LEDGER_BUILT",
    }
    bad = []
    row_by_id = {row["descent_id"]: row for row in rows}
    for row_id, result in required.items():
        if row_id not in row_by_id:
            bad.append(f"{row_id}:missing")
        elif row_by_id[row_id]["result"] != result:
            bad.append(f"{row_id}:{row_by_id[row_id]['result']}")
    return not bad, "; ".join(bad) if bad else "chain-rule lemma retained and descent verdict blocked"


def axiom_ledger_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    bad = []
    if len(rows) < 9:
        bad.append(f"too_few_rows={len(rows)}")
    if any(bool_string(row["adopted"]) == "true" for row in rows):
        bad.append("adopted_true")
    if not any(row["axiom_id"] == "AX1912_0_parent_action_object" for row in rows):
        bad.append("missing_parent_action_object")
    return not bad, "; ".join(bad) if bad else "minimal axiom/debt ledger present and unadopted"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1912_00_sources",
            "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
        }
    )
    descent_ok, descent_detail = descent_attempt_valid(csv_rows(OUTPUTS["descent_attempt"]))
    checks.append({"validation_id": "VAL1912_01_descent_attempt", "status": "PASS" if descent_ok else "FAIL", "detail": descent_detail, "valid_for_claim": False})
    axiom_ok, axiom_detail = axiom_ledger_valid(csv_rows(OUTPUTS["axiom_ledger"]))
    checks.append({"validation_id": "VAL1912_02_axiom_ledger", "status": "PASS" if axiom_ok else "FAIL", "detail": axiom_detail, "valid_for_claim": False})
    refusals = csv_rows(OUTPUTS["closure_refusal"])
    checks.append(
        {
            "validation_id": "VAL1912_03_closure_refusal",
            "status": "PASS" if len(refusals) >= 4 and all(row["current_status"].startswith(("REFUSED", "CLAIM_REFUSED")) for row in refusals) else "FAIL",
            "detail": "closure shortcuts refused",
            "valid_for_claim": False,
        }
    )
    gates = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1912_04_claim_gate",
            "status": "PASS" if any(row["gate_id"] == "CG1912_3_claim" and row["current_status"] == "CLAIM_BLOCKED" for row in gates) else "FAIL",
            "detail": "claim remains blocked",
            "valid_for_claim": False,
        }
    )
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1912_05_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1912_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "1913 parent action object/q-functor route selected",
            "valid_for_claim": False,
        }
    )
    flags_ok, flags_detail = claim_flags_safe(generated_without_validation)
    checks.append({"validation_id": "VAL1912_06_claim_flags_safe", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1912_07_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1912_08_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1912_09_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1912-Y5-R2FR-neighbourhood-quotient",
            "P8_Y5_PARENT_QLOC_1912",
            "Y5_R2FR_neighbourhood_quotient_descent_signature_proof_or_axiom_ledger_1912",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append({"validation_id": "VAL1912_10_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1912_artifact_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1912_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1912 neighbourhood quotient descent signature proof or axiom ledger", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1912 - Neighbourhood Quotient Descent Signature Proof Or Axiom Ledger

## Purpose

This checkpoint tries to parent-sign the descent premise needed by 1911: ordinary matter must factor through the observed quotient on an open neighbourhood. The pointwise chain-rule lemma is exact, but the full matter-action descent theorem is not closed. The missing clauses are therefore isolated as an unadopted axiom/debt ledger.

## Result

- Retained the exact chain-rule core: if `e_obs=Obs_e(q(Phi))` and `Dq[V]=0`, observed geometry is vertical-blind.
- Rejected the scope jump from pointwise geometry silence to open-neighbourhood ordinary-matter action descent.
- Refused EEP/metric-universality closure as a derivation.
- Built the minimal unadopted axiom/debt ledger needed to close local GR/WEP by derivation.
- Next target is parent action object plus q-functor construction, or a clean finite-residual pivot.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Descent Signature Attempt

{markdown_table(rows_by_name["descent_attempt"])}

## Minimal Axiom Debt Ledger

{markdown_table(rows_by_name["axiom_ledger"])}

## Closure Shortcut Refusal Matrix

{markdown_table(rows_by_name["closure_refusal"])}

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
