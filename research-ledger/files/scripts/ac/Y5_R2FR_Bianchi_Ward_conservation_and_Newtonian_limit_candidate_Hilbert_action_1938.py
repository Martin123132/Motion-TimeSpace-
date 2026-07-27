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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1938"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1938-Y5-R2FR-Bianchi-Ward-conservation-and-Newtonian-limit-of-candidate-Hilbert-action.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1937_doc": ROOT / "1937-Y5-R2FR-parent-Hilbert-source-coupling-signature-or-nonmetric-source-coefficient-ledger.md",
    "1937_validation": OUT / "P8_Y5_BRR545_1937_VALIDATION.csv",
    "1937_action": OUT / "P8_Y5_PARENT_QLOC_1937_MINIMAL_PARENT_MATTER_ACTION_SIGNATURE.csv",
    "1937_theorem": OUT / "P8_Y5_PARENT_QLOC_1937_HILBERT_SOURCE_THEOREM.csv",
    "1937_nonmetric": OUT / "P8_Y5_PARENT_QLOC_1937_NONMETRIC_SOURCE_COEFFICIENT_LEDGER.csv",
    "1937_claims": OUT / "P8_Y5_PARENT_QLOC_1937_CLAIM_GATE.csv",
    "1937_next": OUT / "P8_Y5_PARENT_QLOC_1937_NEXT_TARGET.csv",
    "1931_signature": OUT / "P8_Y5_PARENT_QLOC_1931_PARENT_SIGNATURE_LEDGER.csv",
    "1931_theorem": OUT / "P8_Y5_PARENT_QLOC_1931_CONDITIONAL_THEOREM.csv",
}

NEEDLES = {
    "1937_doc": ["ACT1937_1_minimal_matter_action", "HST1937_1_no_wA_no_DeltaW", "VAL1937_OVERALL"],
    "1937_validation": ["VAL1937_OVERALL", "PASS"],
    "1937_action": ["ACT1937_1_minimal_matter_action", "ACT1937_4_preservation_requirement"],
    "1937_theorem": ["HST1937_0_variational_source_owner", "HST1937_3_verdict"],
    "1937_nonmetric": ["NMC1937_0_species_source_weight", "NMC1937_5_material_difference"],
    "1937_claims": ["CG1937_4_local_GR_Newton", "FAIL_BLOCKED"],
    "1937_next": ["NEXT1937_0_primary", "Bianchi-Ward"],
    "1931_signature": ["SIG1931_1_EH_or_R11_operator", "SIG1931_9_Ward_Bianchi_conservation"],
    "1931_theorem": ["THM1931_3_GR_reduction_condition", "THM1931_4_verdict"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1938_SOURCE_REGISTER.csv",
    "ward_bianchi_theorem": OUT / "P8_Y5_PARENT_QLOC_1938_WARD_BIANCHI_CONSERVATION_THEOREM.csv",
    "newtonian_limit_derivation": OUT / "P8_Y5_PARENT_QLOC_1938_NEWTONIAN_LIMIT_DERIVATION.csv",
    "candidate_pass_matrix": OUT / "P8_Y5_PARENT_QLOC_1938_CANDIDATE_PASS_MATRIX.csv",
    "gravity_operator_blockers": OUT / "P8_Y5_PARENT_QLOC_1938_GRAVITY_OPERATOR_BLOCKERS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1938_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1938_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1938_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1938_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1938_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_conservation": SOURCE_WEIGHT_DOCS / "CANDIDATE_HILBERT_ACTION_CONSERVATION_1938_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1938_CLAIM_GATE_NONCLAIM.csv",
    "operator_queue": QUEUE / "JR1938_PARENT_GRAVITY_OPERATOR_EH_OR_R11_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1938_CLAIM_GATE.csv",
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
                "needed_for": "1938 Bianchi/Ward conservation and Newtonian limit gate",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def ward_bianchi_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "WB1938_0_matter_ward_identity",
            "claim": "diffeomorphism-invariant Hilbert matter action gives covariant stress-energy conservation on matter shell",
            "formal_statement": "delta_xi S_matter=0 and E_psi=0 imply nabla_mu T^{mu nu}=0",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "Diffeomorphism variation gives a Noether identity; after matter equations of motion, the metric variation term forces covariant conservation.",
            "remaining_debt": "candidate action is not yet parent-derived and preservation clauses remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "WB1938_1_geometric_bianchi_compatibility",
            "claim": "if the gravitational operator is Einstein tensor plus cosmological term, its divergence vanishes identically",
            "formal_statement": "nabla_mu G^{mu nu}=0 and nabla_mu(Lambda g^{mu nu})=0",
            "proof_status": "STANDARD_GEOMETRIC_IDENTITY_CONDITIONAL_ON_EH_OPERATOR",
            "proof_sketch": "Contracted Bianchi identity supplies the consistency condition for E_g=kappa T.",
            "remaining_debt": "EH/GR operator is still unsigned in 1931",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "WB1938_2_R11_residual_condition",
            "claim": "if an R11/residual gravitational operator is retained, its divergence must vanish or be matched by a conserved residual source",
            "formal_statement": "nabla_mu(E_R11^{mu nu}-kappa T^{mu nu})=0",
            "proof_status": "CONSISTENCY_CONTRACT",
            "proof_sketch": "Any non-EH operator must satisfy the same conservation compatibility or carry explicit exchange terms.",
            "remaining_debt": "R11 operator and residual exchange law are not specified",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "WB1938_3_conservation_verdict",
            "claim": "the 1937 candidate matter action is conservation-compatible",
            "formal_statement": "candidate Hilbert matter action passes the source-conservation side condition conditionally",
            "proof_status": "PASSES_AS_CANDIDATE_NONCLAIM",
            "proof_sketch": "The matter side has the right Ward identity if the action is diffeomorphism invariant and no readout/boundary map breaks it.",
            "remaining_debt": "gravity operator, boundary/projection preservation, and parent derivation still open",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def newtonian_limit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "limit_id": "NL1938_0_weak_field_setup",
            "claim": "Newtonian limit uses weak static metric and slow matter",
            "formula": "g_00=-(1+2 Phi/c^2), |Phi|/c^2<<1, T_00 ~= rho c^2",
            "status": "SETUP_RECORDED",
            "derivation_note": "This is the standard local weak-field source limit setup.",
            "remaining_debt": "observed frame g_obs and weak-field gauge must be parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "limit_id": "NL1938_1_EH_to_Poisson",
            "claim": "Einstein-Hilbert field equation gives Poisson source equation in weak slow limit",
            "formula": "G_00 = kappa T_00 -> nabla^2 Phi = 4 pi G rho when kappa=8 pi G/c^4",
            "status": "EXACT_CONDITIONAL_NEWTONIAN_LIMIT",
            "derivation_note": "With the EH operator and standard coupling normalization, the 00 equation reduces to the Newtonian Poisson equation.",
            "remaining_debt": "EH operator and kappa normalization are not parent-signed in current branch",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "limit_id": "NL1938_2_candidate_matter_source",
            "claim": "1937 Hilbert matter action supplies rho as the universal Newtonian mass-energy source",
            "formula": "rho_eff = T_00/c^2 in the slow test-body limit",
            "status": "CONDITIONAL_SOURCE_IDENTIFICATION",
            "derivation_note": "The same Hilbert source that killed w_A supplies the Newtonian density if the EH equation uses T_obs.",
            "remaining_debt": "binding/self-field/finite-size corrections and observed-frame map remain to be bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "limit_id": "NL1938_3_R11_or_residual_branch",
            "claim": "retained R11/residual gravity modifies the Newtonian source equation unless it vanishes or is bounded locally",
            "formula": "nabla^2 Phi = 4 pi G rho + R_Newtonian_residual",
            "status": "RESIDUAL_BRANCH_ACTIVE",
            "derivation_note": "Any non-EH operator needs its own weak-field projection before a Newtonian claim.",
            "remaining_debt": "R_Newtonian_residual is undefined/unbounded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "limit_id": "NL1938_4_verdict",
            "claim": "MTS now derives local Newtonian gravity from the candidate Hilbert matter action",
            "formula": "not yet",
            "status": "NOT_DERIVED_AS_PARENT_CLAIM",
            "derivation_note": "Matter source side is now well-shaped, but the gravitational operator side remains unsigned.",
            "remaining_debt": "derive/sign EH/GR operator or explicit R11 residual weak-field law",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def candidate_pass_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        ("PASS1938_0_matter_source_owner", "single Hilbert matter source", "PASSES_CONDITIONALLY", "1937 candidate action supplies one T_obs"),
        ("PASS1938_1_WEP_source_universality", "DeltaW_AB=0 if no independent w_A", "PASSES_CONDITIONALLY", "exact conditional theorem from 1937"),
        ("PASS1938_2_matter_Ward_conservation", "nabla_mu T^{mu nu}=0", "PASSES_CONDITIONALLY", "diffeomorphism-invariant matter action gives Ward identity"),
        ("PASS1938_3_gravity_Bianchi_match", "nabla_mu E_g^{mu nu}=0 compatible with source", "BLOCKED_ON_GRAVITY_OPERATOR", "EH/R11 operator not signed"),
        ("PASS1938_4_Newtonian_Poisson", "nabla^2 Phi=4 pi G rho", "BLOCKED_ON_EH_KAPPA_LIMIT", "requires EH operator and kappa normalization"),
        ("PASS1938_5_local_GR_PPN", "gamma=beta=1 and local GR residuals vanish", "BLOCKED_DOWNSTREAM", "needs weak-field metric solution, gauge, residual and PPN maps"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "pass_id": pass_id,
            "criterion": criterion,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for pass_id, criterion, status, reason in rows
    ]


def gravity_operator_blocker_rows() -> list[dict[str, Any]]:
    blockers = [
        ("GOB1938_0_operator_owner", "choose/sign EH tensor or explicit R11/residual operator", "MISSING_PARENT_GRAVITY_OPERATOR"),
        ("GOB1938_1_kappa_normalization", "fix kappa=8 pi G/c^4 or derived equivalent", "MISSING_KAPPA_NORMALIZATION"),
        ("GOB1938_2_observed_frame", "define g_obs/coframe weak-field relation to parent variables", "MISSING_OBSERVED_FRAME_MAP"),
        ("GOB1938_3_residual_divergence", "prove residual operator divergence-free or matched by exchange law", "MISSING_BIANCHI_RESIDUAL_LAW"),
        ("GOB1938_4_Newtonian_residual_bound", "derive/bound R_Newtonian_residual in local systems", "MISSING_LOCAL_RESIDUAL_BOUND"),
        ("GOB1938_5_PPN_map", "derive gamma,beta and preferred-frame residuals", "MISSING_PPN_MAP"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "needed_input": needed_input,
            "status": status,
            "if_filled": "candidate Hilbert matter source can be tested as a local GR/Newton branch",
            "if_missing": "local GR/Newton claim remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for blocker_id, needed_input, status in blockers
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1938_0_matter_conservation", "candidate matter action is Ward-conservation compatible", "PASS_NONCLAIM", "conditional theorem recorded"),
        ("CG1938_1_WEP_source_side", "candidate source side supports DeltaW_AB=0", "PASS_NONCLAIM", "conditional Hilbert source route retained"),
        ("CG1938_2_Newtonian_limit", "MTS derives Poisson/Newtonian source equation", "FAIL_BLOCKED", "EH operator and kappa normalization unsigned"),
        ("CG1938_3_Bianchi_full_system", "full MTS field equation is Bianchi-compatible", "FAIL_BLOCKED", "R11/residual operator divergence law missing"),
        ("CG1938_4_local_GR", "local GR/PPN limit is derived", "FAIL_BLOCKED", "PPN map and residual suppression missing"),
        ("CG1938_5_public_claim", "1938 supports public local-GR/WEP claim", "FAIL_BLOCKED", "candidate remains private nonclaim"),
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
            "decision_id": "DEC1938_0_matter_side",
            "decision": "CANDIDATE_HILBERT_MATTER_SIDE_PASSES_CONSERVATION_NONCLAIM",
            "rationale": "The candidate matter action has the right diffeomorphism Ward identity and universal source structure.",
            "next_action": "stop circling WEP source weights; move to gravity operator/EH-R11 choice",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1938_1_gravity_side",
            "decision": "GRAVITY_OPERATOR_IS_NOW_THE_PRIMARY_BLOCKER",
            "rationale": "Newtonian gravity cannot be claimed from matter action alone; EH/R11 operator and kappa normalization are required.",
            "next_action": "derive/sign EH operator or formulate R11 residual weak-field law",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1938_0_primary",
            "selection_status": "selected",
            "target_doc": "1939-Y5-R2FR-parent-gravity-operator-EH-or-R11-residual-Newtonian-law.md",
            "target_script": "scripts/Y5_R2FR_parent_gravity_operator_EH_or_R11_residual_Newtonian_law_1939.py",
            "objective": "derive/sign the local gravitational operator as EH/GR with kappa normalization, or formulate the retained R11/residual weak-field Newtonian law and blockers",
            "success_condition": "an EH/kappa Newtonian source theorem, or an explicit R11 residual Newtonian equation with local-GR claims blocked",
            "do_not": "do not claim local GR/Newton without a signed operator, kappa normalization, Bianchi compatibility, and weak-field residual control; do not modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1938_0_project_position",
            "status": "MATTER_SOURCE_SIDE_PASSES_GRAVITY_OPERATOR_BLOCKS",
            "summary": "1938 shows the candidate Hilbert matter action is conservation-compatible and WEP-source-universal conditionally, but Newtonian/local-GR claims now hinge on the gravitational operator.",
            "strongest_result": "diffeomorphism-invariant Hilbert matter action gives nabla_mu T^{mu nu}=0 and supplies a universal Newtonian source conditionally",
            "missing_piece": "EH/GR or R11 operator signature, kappa normalization, residual divergence law, and weak-field PPN map",
            "claim_position": "local-GR/Newton/WEP public claims remain blocked",
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
    write_csv(BRANCH_COPIES["source_weight_conservation"], rows_by_name["ward_bianchi_theorem"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["operator_queue"], rows_by_name["gravity_operator_blockers"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1938*") if artifact.is_file())


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

    add("VAL1938_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"]), "all local source paths exist and needles found")
    add("VAL1938_01_conservation", any(row["proof_status"] == "PASSES_AS_CANDIDATE_NONCLAIM" for row in rows_by_name["ward_bianchi_theorem"]) and any(row["proof_status"] == "CONSISTENCY_CONTRACT" for row in rows_by_name["ward_bianchi_theorem"]), "matter Ward conservation passes conditionally; residual consistency retained")
    add("VAL1938_02_newtonian_limit", any(row["status"] == "EXACT_CONDITIONAL_NEWTONIAN_LIMIT" for row in rows_by_name["newtonian_limit_derivation"]) and any(row["status"] == "NOT_DERIVED_AS_PARENT_CLAIM" for row in rows_by_name["newtonian_limit_derivation"]), "Newtonian limit is conditional on EH/kappa and not promoted")
    add("VAL1938_03_pass_matrix", len(rows_by_name["candidate_pass_matrix"]) == 6 and any(row["status"] == "BLOCKED_ON_GRAVITY_OPERATOR" for row in rows_by_name["candidate_pass_matrix"]), "candidate pass matrix separates matter-side pass from gravity-side blockers")
    add("VAL1938_04_operator_blockers", len(rows_by_name["gravity_operator_blockers"]) == 6 and all(str(row["status"]).startswith("MISSING_") for row in rows_by_name["gravity_operator_blockers"]), "gravity operator blockers explicitly named")
    add("VAL1938_05_claim_gates", any(row["status"] == "PASS_NONCLAIM" for row in rows_by_name["claim_gate"]) and all(str(row["claim_allowed"]) == "False" for row in rows_by_name["claim_gate"]), "only nonclaim gates pass; all claim flags false")
    add("VAL1938_06_decision", any(row["decision"] == "GRAVITY_OPERATOR_IS_NOW_THE_PRIMARY_BLOCKER" for row in rows_by_name["decision"]), "gravity operator selected as next blocker")
    add("VAL1938_07_next_target", rows_by_name["next_target"][0]["target_doc"].startswith("1939-Y5-R2FR-parent-gravity-operator"), "1939 gravity operator target selected")
    add("VAL1938_08_claim_flags_safe", all(str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False" for rows in rows_by_name.values() for row in rows), "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1938_09_csv_parse", csv_ok, "all generated CSVs parse with rows")
    add("VAL1938_10_branch_copies", all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values()), "; ".join(str(path) for path in BRANCH_COPIES.values()))
    add("VAL1938_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent")
    formalization_count = formalization_artifact_count()
    add("VAL1938_12_formalization_untouched", formalization_count == 0, f"formalization_1938_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1938_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1938 Bianchi/Ward conservation and Newtonian limit of candidate Hilbert action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1938 Y5 R2FR: Bianchi/Ward Conservation and Newtonian Limit of Candidate Hilbert Action",
        "",
        "## Verdict",
        "",
        "1938 is a useful split result. The 1937 candidate Hilbert matter action is conservation-compatible: diffeomorphism invariance gives the matter Ward identity `nabla_mu T^{mu nu}=0` on shell. It also keeps the WEP/source side clean conditionally.",
        "",
        "But the Newtonian/local-GR claim is still blocked. The matter action supplies the right kind of source, but Poisson/Newton requires the gravitational operator to be signed as EH/GR with the correct coupling normalization, or an explicit R11/residual weak-field law.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Ward/Bianchi Conservation Theorem",
        "",
        markdown_table(rows_by_name["ward_bianchi_theorem"]),
        "",
        "## Newtonian Limit Derivation",
        "",
        markdown_table(rows_by_name["newtonian_limit_derivation"]),
        "",
        "## Candidate Pass Matrix",
        "",
        markdown_table(rows_by_name["candidate_pass_matrix"]),
        "",
        "## Gravity Operator Blockers",
        "",
        markdown_table(rows_by_name["gravity_operator_blockers"]),
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
        "ward_bianchi_theorem": ward_bianchi_theorem_rows(),
        "newtonian_limit_derivation": newtonian_limit_rows(),
        "candidate_pass_matrix": candidate_pass_matrix_rows(),
        "gravity_operator_blockers": gravity_operator_blocker_rows(),
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
