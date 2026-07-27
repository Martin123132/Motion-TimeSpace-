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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1937"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1937-Y5-R2FR-parent-Hilbert-source-coupling-signature-or-nonmetric-source-coefficient-ledger.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1936_doc": ROOT / "1936-Y5-R2FR-source-weight-universality-theorem-or-TiPt-material-charge-ledger.md",
    "1936_validation": OUT / "P8_Y5_BRR545_1936_VALIDATION.csv",
    "1936_universality": OUT / "P8_Y5_PARENT_QLOC_1936_SOURCE_WEIGHT_UNIVERSALITY_ATTEMPT.csv",
    "1936_hilbert": OUT / "P8_Y5_PARENT_QLOC_1936_HILBERT_SOURCE_CONTRACT.csv",
    "1936_tipt": OUT / "P8_Y5_PARENT_QLOC_1936_TIPT_MATERIAL_CHARGE_LEDGER.csv",
    "1936_implication": OUT / "P8_Y5_PARENT_QLOC_1936_WEP_ETA_IMPLICATION.csv",
    "1936_claims": OUT / "P8_Y5_PARENT_QLOC_1936_CLAIM_GATE.csv",
    "1936_next": OUT / "P8_Y5_PARENT_QLOC_1936_NEXT_TARGET.csv",
    "1931_signature": OUT / "P8_Y5_PARENT_QLOC_1931_PARENT_SIGNATURE_LEDGER.csv",
    "1933_closure": OUT / "P8_Y5_PARENT_QLOC_1933_MINIMAL_CLOSURE.csv",
}

NEEDLES = {
    "1936_doc": ["UNIV1936_1_hilbert_source_theorem", "HIL1936_0_single_observed_metric", "VAL1936_OVERALL"],
    "1936_validation": ["VAL1936_OVERALL", "PASS"],
    "1936_universality": ["UNIV1936_1_hilbert_source_theorem", "UNIV1936_4_verdict"],
    "1936_hilbert": ["HIL1936_0_single_observed_metric", "HIL1936_5_readout_boundary_preservation"],
    "1936_tipt": ["TIPT1936_0_Ti_weight", "TIPT1936_5_eta_target"],
    "1936_implication": ["IMP1936_0_universality_to_eta_zero", "IMP1936_1_finite_residual_bound"],
    "1936_claims": ["CG1936_1_parent_signature", "FAIL_BLOCKED"],
    "1936_next": ["NEXT1936_0_primary", "Hilbert-source"],
    "1931_signature": ["SIG1931_4_source_weight_exclusion", "SIG1931_10_verdict"],
    "1933_closure": ["CLOS1933_0_minimal_descent_clause", "CLOS1933_1_preservation_clause"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1937_SOURCE_REGISTER.csv",
    "candidate_action": OUT / "P8_Y5_PARENT_QLOC_1937_MINIMAL_PARENT_MATTER_ACTION_SIGNATURE.csv",
    "hilbert_theorem": OUT / "P8_Y5_PARENT_QLOC_1937_HILBERT_SOURCE_THEOREM.csv",
    "nonmetric_ledger": OUT / "P8_Y5_PARENT_QLOC_1937_NONMETRIC_SOURCE_COEFFICIENT_LEDGER.csv",
    "adoption_gate": OUT / "P8_Y5_PARENT_QLOC_1937_ACTION_ADOPTION_GATE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1937_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1937_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1937_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1937_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1937_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_action": SOURCE_WEIGHT_DOCS / "MINIMAL_PARENT_HILBERT_SOURCE_ACTION_1937_NONCLAIM.csv",
    "microscope_nonmetric": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1937_NONMETRIC_SOURCE_COEFFICIENT_LEDGER_NONCLAIM.csv",
    "next_queue": QUEUE / "JR1937_BIANCHI_CONSERVATION_OR_NONMETRIC_SOURCE_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1937_CLAIM_GATE.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_key, source_path in SOURCES.items():
        path_exists = source_path.exists()
        source_text = read_text(source_path) if path_exists else ""
        missing_needles = [needle for needle in NEEDLES[source_key] if needle not in source_text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "needed_for": "1937 parent Hilbert source-coupling signature or nonmetric source coefficient ledger",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def candidate_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "action_id": "ACT1937_0_parent_geometric_domain",
            "candidate_signature": "q: Phi_parent -> (g_obs, e_obs, A_obs, theta_rep)",
            "meaning": "all ordinary visible structures used by matter are quotient-descended observed structures",
            "derivation_status": "CANDIDATE_PARENT_SIGNATURE_NOT_CORPUS_DERIVED",
            "if_adopted": "prevents hidden representatives from becoming source-only weights",
            "if_rejected": "nonmetric coefficient ledger remains active",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "action_id": "ACT1937_1_minimal_matter_action",
            "candidate_signature": "S_matter = sum_A int d^4x sqrt(-g_obs) L_A(psi_A, D(g_obs,A_obs)psi_A, theta_A)",
            "meaning": "ordinary species may have representation/internal parameters theta_A but no independent gravitational source weight w_A",
            "derivation_status": "CANDIDATE_PARENT_SIGNATURE_NOT_CORPUS_DERIVED",
            "if_adopted": "defines one Hilbert stress-energy source for all ordinary sectors",
            "if_rejected": "species/material source weights must be explicit finite coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "action_id": "ACT1937_2_forbidden_source_vertex",
            "candidate_signature": "forbid DeltaS = int sqrt(-g_obs) w_A(X_hid,theta_A) T_A or w_A rho_A as a separate gravitational source multiplier",
            "meaning": "composition labels cannot enter the gravitational source except through the matter action whose variation defines T_mn",
            "derivation_status": "EXPLICIT_CLOSURE_UNLESS_PARENT_OBJECT_LANGUAGE_SIGNED",
            "if_adopted": "DeltaW_AB=0 in the test-body limit",
            "if_rejected": "WEP/local-GR branch requires sourced w_Ti,w_Pt,tau_WEP rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "action_id": "ACT1937_3_source_definition",
            "candidate_signature": "T_obs^{mu nu} = -2/sqrt(-g_obs) delta S_matter/delta g_obs_mu_nu",
            "meaning": "the source appearing in the local gravitational equation is the Hilbert source of the same action",
            "derivation_status": "CANDIDATE_PARENT_SIGNATURE_NOT_CORPUS_DERIVED",
            "if_adopted": "ties inertial/internal energy and gravitational source to one object",
            "if_rejected": "separate source owner must be introduced and bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "action_id": "ACT1937_4_preservation_requirement",
            "candidate_signature": "renormalization/readout/projection maps preserve absence of w_A source vertices",
            "meaning": "loops, boundary reductions, and local maps cannot reintroduce species source weights",
            "derivation_status": "UNSIGNED_PRESERVATION_REQUIREMENT",
            "if_adopted": "protects WEP/source theorem beyond the bare action",
            "if_rejected": "radiative/readout residual coefficients must be carried",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def hilbert_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HST1937_0_variational_source_owner",
            "statement": "If every ordinary matter sector appears only in S_matter[g_obs,fields,theta_A], the gravitational source is the Hilbert variation of that same action.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "Vary S_matter with respect to g_obs; species labels affect T_obs through physical stress-energy, not through a separate gravitational charge.",
            "gives": "single source owner for ordinary matter",
            "does_not_give": "parent proof that the candidate action is mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HST1937_1_no_wA_no_DeltaW",
            "statement": "If no independent source multiplier w_A exists, then the WEP source-weight difference DeltaW_AB is zero by construction.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "There is no species-indexed gravitational charge variable left to differ between A and B; composition enters only the stress-energy being universally sourced.",
            "gives": "DeltaW_TiPt=0 and eta_TiPt=0 under 1935 projection",
            "does_not_give": "finite-size/self-field/readout corrections",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HST1937_2_common_renormalization",
            "statement": "A universal source normalization rescales the common acceleration but cancels from eta_AB.",
            "proof_status": "EXACT_WEP_CANCELLATION",
            "proof_sketch": "1935 gives eta_AB from epsilon_A-epsilon_B; a common epsilon contributes zero to the numerator.",
            "gives": "measured-G/common-mode shifts are separated from WEP violation",
            "does_not_give": "permission to hide composition-dependent weights inside measured G",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HST1937_3_verdict",
            "statement": "The current MTS corpus derives the parent Hilbert source action signature.",
            "proof_status": "NOT_DERIVED",
            "proof_sketch": "1937 constructs the minimal signature that would close WEP/source coupling, but the corpus still lacks a parent derivation forcing this action form.",
            "gives": "a concrete adoption/derivation target rather than a vague coupling gap",
            "does_not_give": "WEP pass, local-GR derivation, or public claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def nonmetric_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("NMC1937_0_species_source_weight", "w_A", "independent gravitational source multiplier", "would make DeltaW_AB live"),
        ("NMC1937_1_hidden_source_scalar", "w_A(X_hid)", "hidden invariant scalar feeding source strength", "breaks coefficient descent/source universality"),
        ("NMC1937_2_binding_source_anomaly", "b_bind,A", "species-dependent binding-energy source anomaly", "can mimic composition WEP residual"),
        ("NMC1937_3_readout_projection_weight", "r_A", "projection/readout map reintroduces species source response", "bulk theorem insufficient"),
        ("NMC1937_4_transfer_factor", "tau_WEP", "arena transfer from source residual to eta", "needed for finite comparison if nonmetric weights survive"),
        ("NMC1937_5_material_difference", "DeltaW_TiPt", "Ti/Pt source-weight difference", "must be zero theorem or numeric bound row"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "meaning": meaning,
            "danger": danger,
            "status": "ACTIVE_IF_PARENT_HILBERT_SIGNATURE_UNSIGNED",
            "numeric_value": "MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for coefficient_id, symbol, meaning, danger in rows
    ]


def adoption_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ADOPT1937_0_scientific_move",
            "question": "May MTS adopt the minimal Hilbert source action as a parent signature?",
            "answer": "YES_AS_PRIVATE_CANDIDATE_NO_AS_DERIVED_CLAIM",
            "reason": "It is mathematically clean and GR-compatible, but not derived from deeper MTS principles yet.",
            "next_requirement": "test Bianchi/Ward conservation and local Newtonian limit of this candidate action",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ADOPT1937_1_if_adopted",
            "question": "What follows if the candidate is adopted?",
            "answer": "SOURCE_UNIVERSALITY_ROUTE_OPENS",
            "reason": "No independent w_A means DeltaW_AB=0 conditionally.",
            "next_requirement": "prove conservation and weak-field GR/Newton compatibility",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ADOPT1937_2_if_rejected",
            "question": "What follows if the candidate is rejected?",
            "answer": "NONMETRIC_LEDGER_REQUIRED",
            "reason": "The theory must carry w_A, DeltaW_TiPt, tau_WEP, and source-environment coefficients as finite test inputs.",
            "next_requirement": "source numeric rows before WEP comparison",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1937_0_candidate_action", "minimal parent Hilbert source action is written", "PASS_NONCLAIM", "candidate action signature recorded"),
        ("CG1937_1_conditional_theorem", "candidate action implies DeltaW_AB=0", "PASS_NONCLAIM", "exact conditional theorem recorded"),
        ("CG1937_2_parent_derivation", "MTS derives the candidate action from deeper parent principles", "FAIL_BLOCKED", "no parent derivation found"),
        ("CG1937_3_WEP_pass", "MTS passes MICROSCOPE WEP", "FAIL_BLOCKED", "candidate is not a derived claim and preservation clauses remain unsigned"),
        ("CG1937_4_local_GR_Newton", "local GR/Newton reduction is derived", "FAIL_BLOCKED", "needs Bianchi/Ward conservation plus weak-field operator limit"),
        ("CG1937_5_public_claim", "1937 is public-ready proof", "FAIL_BLOCKED", "private candidate-action checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1937_0_leap_taken",
            "decision": "MINIMAL_PARENT_HILBERT_SOURCE_ACTION_WRITTEN_AS_CANDIDATE",
            "rationale": "This is the cleanest leap: a single observed metric/coframe matter action removes species source weights and opens the GR-compatible WEP route.",
            "next_action": "test candidate against Bianchi/Ward conservation and weak-field Newtonian limit",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1937_1_claim_discipline",
            "decision": "CANDIDATE_NOT_DERIVED_YET",
            "rationale": "Adopting a parent action is not the same as deriving it from the deeper MTS programme.",
            "next_action": "keep nonmetric ledger active until parent derivation or conservation/limit tests justify promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1937_0_primary",
            "selection_status": "selected",
            "target_doc": "1938-Y5-R2FR-Bianchi-Ward-conservation-and-Newtonian-limit-of-candidate-Hilbert-action.md",
            "target_script": "scripts/Y5_R2FR_Bianchi_Ward_conservation_and_Newtonian_limit_candidate_Hilbert_action_1938.py",
            "objective": "test the 1937 candidate Hilbert source action against diffeomorphism/Ward conservation and derive its local Newtonian source limit, or demote it to a closure/nonmetric ledger",
            "success_condition": "candidate action passes conservation and gives a controlled Newtonian source equation, or explicit failure blockers with WEP/local-GR claims blocked",
            "do_not": "do not claim local GR, WEP pass, or Newtonian limit unless conservation and weak-field source equations are explicit; do not modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1937_0_project_position",
            "status": "LEAP_TAKEN_CANDIDATE_PARENT_ACTION_WRITTEN",
            "summary": "1937 writes the minimal parent Hilbert source action needed to make WEP/source universality a theorem, but keeps it nonclaim because it is not yet derived from deeper MTS principles.",
            "strongest_result": "if S_matter has one observed metric/coframe and no independent w_A source multipliers, then DeltaW_AB=0 conditionally",
            "missing_piece": "Bianchi/Ward conservation, weak-field Newtonian limit, and deeper MTS derivation/adoption justification",
            "fallback": "nonmetric source coefficient ledger remains active",
            "claim_position": "WEP/local-GR/Newton claims remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_action"], rows_by_name["candidate_action"])
    write_csv(BRANCH_COPIES["microscope_nonmetric"], rows_by_name["nonmetric_ledger"])
    write_csv(BRANCH_COPIES["next_queue"], rows_by_name["next_target"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1937*") if artifact.is_file())


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validation_rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        validation_rows.append(
            {
                "validation_id": validation_id,
                "status": "PASS" if status else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    add("VAL1937_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"]), "all local source paths exist and needles found")
    add("VAL1937_01_candidate_action", len(rows_by_name["candidate_action"]) == 5 and any(row["action_id"] == "ACT1937_1_minimal_matter_action" for row in rows_by_name["candidate_action"]), "minimal parent matter action signature written")
    add("VAL1937_02_hilbert_theorem", any(row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_by_name["hilbert_theorem"]) and any(row["proof_status"] == "NOT_DERIVED" for row in rows_by_name["hilbert_theorem"]), "conditional theorem retained without claiming parent derivation")
    add("VAL1937_03_nonmetric_ledger", len(rows_by_name["nonmetric_ledger"]) == 6 and all(row["status"] == "ACTIVE_IF_PARENT_HILBERT_SIGNATURE_UNSIGNED" for row in rows_by_name["nonmetric_ledger"]), "nonmetric source coefficients remain explicit")
    add("VAL1937_04_adoption_gate", any(row["answer"] == "YES_AS_PRIVATE_CANDIDATE_NO_AS_DERIVED_CLAIM" for row in rows_by_name["adoption_gate"]), "candidate-action adoption status is explicit")
    add("VAL1937_05_claim_gates", any(row["status"] == "PASS_NONCLAIM" for row in rows_by_name["claim_gate"]) and all(str(row["claim_allowed"]) == "False" for row in rows_by_name["claim_gate"]), "only nonclaim gates pass; all claim flags false")
    add("VAL1937_06_decision", any(row["decision"] == "MINIMAL_PARENT_HILBERT_SOURCE_ACTION_WRITTEN_AS_CANDIDATE" for row in rows_by_name["decision"]), "leap decision recorded")
    add("VAL1937_07_next_target", rows_by_name["next_target"][0]["target_doc"].startswith("1938-Y5-R2FR-Bianchi-Ward"), "1938 conservation/Newtonian target selected")
    add("VAL1937_08_claim_flags_safe", all(str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False" for rows in rows_by_name.values() for row in rows), "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1937_09_csv_parse", csv_ok, "all generated CSVs parse with rows")
    add("VAL1937_10_branch_copies", all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values()), "; ".join(str(path) for path in BRANCH_COPIES.values()))
    add("VAL1937_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent")
    formalization_count = formalization_artifact_count()
    add("VAL1937_12_formalization_untouched", formalization_count == 0, f"formalization_1937_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1937_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1937 parent Hilbert source-coupling signature or nonmetric source coefficient ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1937 Y5 R2FR: Parent Hilbert Source-Coupling Signature or Nonmetric Source-Coefficient Ledger",
        "",
        "## Verdict",
        "",
        "This is the leap checkpoint. 1937 writes the minimal parent matter action that would make ordinary source coupling universal: all ordinary matter sees one observed metric/coframe and the gravitational source is the Hilbert stress-energy variation of that same matter action. Under that candidate action, no independent species source-weight `w_A` exists, so `DeltaW_AB=0` conditionally.",
        "",
        "This is **not** claimed as derived yet. It is a private candidate parent signature. The next hard test is whether the candidate passes Bianchi/Ward conservation and yields the controlled Newtonian source equation.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Minimal Parent Matter Action Signature",
        "",
        markdown_table(rows_by_name["candidate_action"]),
        "",
        "## Hilbert Source Theorem",
        "",
        markdown_table(rows_by_name["hilbert_theorem"]),
        "",
        "## Nonmetric Source-Coefficient Ledger",
        "",
        markdown_table(rows_by_name["nonmetric_ledger"]),
        "",
        "## Action Adoption Gate",
        "",
        markdown_table(rows_by_name["adoption_gate"]),
        "",
        "## Claim Gate",
        "",
        markdown_table(rows_by_name["claim_gate"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows_by_name["decision"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(rows_by_name["status_snapshot"]),
        "",
        "## Validation",
        "",
        markdown_table(rows_by_name["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_COEFFS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    rows_by_name = {
        "source_register": source_register_rows(),
        "candidate_action": candidate_action_rows(),
        "hilbert_theorem": hilbert_theorem_rows(),
        "nonmetric_ledger": nonmetric_ledger_rows(),
        "adoption_gate": adoption_gate_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "status_snapshot": status_snapshot_rows(),
    }

    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        write_csv(output_path, rows_by_name[output_key])

    copy_branch_artifacts(rows_by_name)
    remove_pycache()
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
