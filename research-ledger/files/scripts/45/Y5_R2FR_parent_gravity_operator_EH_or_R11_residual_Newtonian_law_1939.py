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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1939"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1939-Y5-R2FR-parent-gravity-operator-EH-or-R11-residual-Newtonian-law.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1938_doc": ROOT / "1938-Y5-R2FR-Bianchi-Ward-conservation-and-Newtonian-limit-of-candidate-Hilbert-action.md",
    "1938_validation": OUT / "P8_Y5_BRR545_1938_VALIDATION.csv",
    "1938_newtonian": OUT / "P8_Y5_PARENT_QLOC_1938_NEWTONIAN_LIMIT_DERIVATION.csv",
    "1938_blockers": OUT / "P8_Y5_PARENT_QLOC_1938_GRAVITY_OPERATOR_BLOCKERS.csv",
    "1938_claims": OUT / "P8_Y5_PARENT_QLOC_1938_CLAIM_GATE.csv",
    "1938_next": OUT / "P8_Y5_PARENT_QLOC_1938_NEXT_TARGET.csv",
    "1937_action": OUT / "P8_Y5_PARENT_QLOC_1937_MINIMAL_PARENT_MATTER_ACTION_SIGNATURE.csv",
    "1931_signature": OUT / "P8_Y5_PARENT_QLOC_1931_PARENT_SIGNATURE_LEDGER.csv",
}

NEEDLES = {
    "1938_doc": ["NL1938_1_EH_to_Poisson", "GOB1938_0_operator_owner", "VAL1938_OVERALL"],
    "1938_validation": ["VAL1938_OVERALL", "PASS"],
    "1938_newtonian": ["NL1938_1_EH_to_Poisson", "NL1938_4_verdict"],
    "1938_blockers": ["GOB1938_0_operator_owner", "GOB1938_5_PPN_map"],
    "1938_claims": ["CG1938_2_Newtonian_limit", "FAIL_BLOCKED"],
    "1938_next": ["NEXT1938_0_primary", "gravity-operator"],
    "1937_action": ["ACT1937_1_minimal_matter_action", "ACT1937_3_source_definition"],
    "1931_signature": ["SIG1931_1_EH_or_R11_operator", "SIG1931_10_verdict"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1939_SOURCE_REGISTER.csv",
    "gravity_action_candidate": OUT / "P8_Y5_PARENT_QLOC_1939_GRAVITY_ACTION_CANDIDATE.csv",
    "eh_newtonian_theorem": OUT / "P8_Y5_PARENT_QLOC_1939_EH_NEWTONIAN_THEOREM.csv",
    "r11_residual_law": OUT / "P8_Y5_PARENT_QLOC_1939_R11_RESIDUAL_NEWTONIAN_LAW.csv",
    "operator_decision_matrix": OUT / "P8_Y5_PARENT_QLOC_1939_OPERATOR_DECISION_MATRIX.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1939_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1939_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1939_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1939_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1939_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_operator": SOURCE_WEIGHT_DOCS / "GRAVITY_OPERATOR_EH_OR_R11_1939_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1939_CLAIM_GATE_NONCLAIM.csv",
    "operator_queue": QUEUE / "JR1939_EH_ADOPTION_OR_R11_RESIDUAL_PPN_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1939_CLAIM_GATE.csv",
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
                "needed_for": "1939 parent gravity operator EH or R11 residual Newtonian law",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def gravity_action_candidate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GAC1939_0_EH_minimal", "S_grav=(1/2kappa) int sqrt(-g_obs)(R[g_obs]-2Lambda)", "minimal second-order diffeomorphism-invariant GR operator", "CANDIDATE_NOT_PARENT_DERIVED"),
        ("GAC1939_1_kappa", "kappa=8*pi*G/c^4", "normalization required for Poisson equation", "CANDIDATE_NORMALIZATION_NOT_DERIVED"),
        ("GAC1939_2_field_equation", "G_mn + Lambda g_mn = kappa T_mn + R_mn^res", "local observed-frame field equation with explicit residual slot", "CANDIDATE_WITH_RESIDUAL_SLOT"),
        ("GAC1939_3_residual_zero_branch", "R_mn^res=0 in local ordinary weak-field branch", "route to GR/Newton/PPN", "UNSIGNED_ZERO_BRANCH"),
        ("GAC1939_4_residual_retained_branch", "R_mn^res != 0 but divergence-compatible and bounded", "route to testable modification rather than GR claim", "ACTIVE_FALLBACK_BRANCH"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "action_id": action_id,
            "candidate_operator": candidate_operator,
            "role": role,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for action_id, candidate_operator, role, status in rows
    ]


def eh_newtonian_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EH1939_0_variation",
            "statement": "Variation of the EH candidate action gives G_mn+Lambda g_mn=kappa T_mn when residuals vanish.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "formula": "delta(S_EH+S_matter)=0 -> G_mn+Lambda g_mn=kappa T_mn",
            "remaining_debt": "EH candidate is not derived from deeper MTS parent principle",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EH1939_1_bianchi",
            "statement": "Contracted Bianchi identity makes the EH operator compatible with Hilbert-source conservation.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "formula": "nabla_mu(G^{mu nu}+Lambda g^{mu nu})=0 => nabla_mu T^{mu nu}=0",
            "remaining_debt": "residual branch must also be divergence-compatible or vanish",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EH1939_2_Poisson",
            "statement": "With kappa=8*pi*G/c^4, weak static slow-source EH equation gives the Newtonian Poisson law.",
            "proof_status": "EXACT_CONDITIONAL_NEWTONIAN_LIMIT",
            "formula": "nabla^2 Phi=4*pi*G*rho",
            "remaining_debt": "observed-frame weak-field map and residual suppression must be signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EH1939_3_verdict",
            "statement": "MTS now derives EH/kappa as the parent local gravity operator.",
            "proof_status": "NOT_DERIVED_AS_PARENT_CLAIM",
            "formula": "EH is the minimal candidate, not yet a derived MTS theorem",
            "remaining_debt": "derive/adopt operator from parent geometry or keep R11 residual branch explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def r11_residual_law_rows() -> list[dict[str, Any]]:
    rows = [
        ("R111939_0_field_equation", "G_mn+Lambda g_mn+kappa_R R11_mn = kappa T_mn", "define retained residual operator", "MISSING_R11_OPERATOR"),
        ("R111939_1_divergence", "nabla_mu R11^{mu nu}=0 or exchange current J^nu", "Bianchi compatibility", "MISSING_DIVERGENCE_LAW"),
        ("R111939_2_Newtonian_projection", "nabla^2 Phi=4*pi*G*rho + Xi_R11", "weak-field residual source", "MISSING_XI_R11"),
        ("R111939_3_local_bound", "|Xi_R11| << 4*pi*G*rho or explicit test prediction", "local GR/Newton gate", "MISSING_LOCAL_BOUND"),
        ("R111939_4_PPN_projection", "gamma,beta,preferred-frame residual vector", "solar-system gate", "MISSING_PPN_RESIDUALS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "residual_law": residual_law,
            "needed_for": needed_for,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for residual_id, residual_law, needed_for, status in rows
    ]


def operator_decision_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        ("ODM1939_0_EH_adopted", "adopt EH/kappa as local parent operator", "opens clean Newtonian branch", "needs parent-geometry justification and residual-zero proof"),
        ("ODM1939_1_EH_derived", "derive EH/kappa from MTS parent geometry", "best route to serious GR reduction", "not yet done"),
        ("ODM1939_2_R11_retained", "retain R11/residual operator", "keeps novelty explicit/testable", "must derive divergence and weak-field residual law"),
        ("ODM1939_3_operator_unknown", "leave operator unsigned", "no overclaim", "local GR/Newton branch remains blocked"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_case": decision_case,
            "route": route,
            "advantage": advantage,
            "cost_or_blocker": cost_or_blocker,
            "current_selection": "SELECTED_NEXT_DERIVATION_TARGET" if decision_case == "ODM1939_1_EH_derived" else "DEFERRED_OR_FALLBACK",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for decision_case, route, advantage, cost_or_blocker in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1939_0_EH_Newtonian_conditional", "EH/kappa candidate gives Poisson equation", "PASS_NONCLAIM", "conditional Newtonian theorem recorded"),
        ("CG1939_1_parent_EH_derivation", "MTS derives EH/kappa from parent geometry", "FAIL_BLOCKED", "candidate not parent-derived"),
        ("CG1939_2_R11_law", "R11/residual Newtonian law is defined and bounded", "FAIL_BLOCKED", "R11 operator/residual projection missing"),
        ("CG1939_3_local_Newton", "MTS derives local Newtonian gravity", "FAIL_BLOCKED", "operator adoption/derivation and residual control missing"),
        ("CG1939_4_local_GR_PPN", "MTS derives local GR/PPN", "FAIL_BLOCKED", "PPN residual vector missing"),
        ("CG1939_5_public_claim", "1939 is public-ready local-GR proof", "FAIL_BLOCKED", "private operator-candidate checkpoint only"),
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
            "decision_id": "DEC1939_0_operator_status",
            "decision": "EH_KAPPA_IS_MINIMAL_GR_COMPATIBLE_CANDIDATE_NOT_DERIVED",
            "rationale": "It gives Bianchi compatibility and Poisson law cleanly, but this is adoption unless parent geometry forces it.",
            "next_action": "try deriving EH/kappa from parent geometry or explicitly retain R11 residual law",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1939_1_next_best_route",
            "decision": "ATTACK_EH_UNIQUENESS_OR_R11_RESIDUAL_NEXT",
            "rationale": "This is now the sharpest route to local GR/Newton: prove EH uniqueness/normalization or make the residual testable.",
            "next_action": "build Lovelock/EH uniqueness gate in 4D observed frame, with explicit residual branch if assumptions fail",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1939_0_primary",
            "selection_status": "selected",
            "target_doc": "1940-Y5-R2FR-EH-uniqueness-Lovelock-gate-or-R11-residual-operator.md",
            "target_script": "scripts/Y5_R2FR_EH_uniqueness_Lovelock_gate_or_R11_residual_operator_1940.py",
            "objective": "test whether 4D diffeomorphism invariance, second-order metric equations, local observed frame, and conservation force EH/Lovelock gravity; otherwise define the R11 residual operator branch",
            "success_condition": "an explicit EH uniqueness theorem under stated assumptions, or a nonclaim R11 residual operator ledger with Newtonian/PPN claims blocked",
            "do_not": "do not claim EH is derived unless all uniqueness assumptions are signed; do not claim local GR/Newton or modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1939_0_project_position",
            "status": "EH_CANDIDATE_GIVES_NEWTONIAN_LIMIT_OPERATOR_DERIVATION_OPEN",
            "summary": "1939 records the EH/kappa operator as the minimal GR-compatible candidate and derives its conditional Poisson limit, while keeping R11/residual branches explicit.",
            "strongest_result": "EH with kappa=8*pi*G/c^4 gives nabla^2 Phi=4*pi*G*rho conditionally",
            "missing_piece": "parent derivation/adoption of EH or explicit R11 residual divergence and weak-field laws",
            "claim_position": "local-GR/Newton public claims remain blocked",
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
    write_csv(BRANCH_COPIES["source_weight_operator"], rows_by_name["gravity_action_candidate"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["operator_queue"], rows_by_name["operator_decision_matrix"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1939*") if artifact.is_file())


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

    add("VAL1939_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"]), "all local source paths exist and needles found")
    add("VAL1939_01_candidate_operator", len(rows_by_name["gravity_action_candidate"]) == 5 and any(row["action_id"] == "GAC1939_0_EH_minimal" for row in rows_by_name["gravity_action_candidate"]), "EH candidate and residual slot recorded")
    add("VAL1939_02_eh_theorem", any(row["proof_status"] == "EXACT_CONDITIONAL_NEWTONIAN_LIMIT" for row in rows_by_name["eh_newtonian_theorem"]) and any(row["proof_status"] == "NOT_DERIVED_AS_PARENT_CLAIM" for row in rows_by_name["eh_newtonian_theorem"]), "EH Newtonian theorem conditional and not promoted")
    add("VAL1939_03_r11_residual", len(rows_by_name["r11_residual_law"]) == 5 and all(str(row["status"]).startswith("MISSING_") for row in rows_by_name["r11_residual_law"]), "R11 residual blockers explicit")
    add("VAL1939_04_decision_matrix", any(row["current_selection"] == "SELECTED_NEXT_DERIVATION_TARGET" for row in rows_by_name["operator_decision_matrix"]), "EH derivation selected as next target")
    add("VAL1939_05_claim_gates", any(row["status"] == "PASS_NONCLAIM" for row in rows_by_name["claim_gate"]) and all(str(row["claim_allowed"]) == "False" for row in rows_by_name["claim_gate"]), "only nonclaim gates pass; all claim flags false")
    add("VAL1939_06_decision", any(row["decision"] == "ATTACK_EH_UNIQUENESS_OR_R11_RESIDUAL_NEXT" for row in rows_by_name["decision"]), "EH uniqueness/R11 residual selected next")
    add("VAL1939_07_next_target", rows_by_name["next_target"][0]["target_doc"].startswith("1940-Y5-R2FR-EH-uniqueness"), "1940 EH uniqueness target selected")
    add("VAL1939_08_claim_flags_safe", all(str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False" for rows in rows_by_name.values() for row in rows), "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1939_09_csv_parse", csv_ok, "all generated CSVs parse with rows")
    add("VAL1939_10_branch_copies", all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values()), "; ".join(str(path) for path in BRANCH_COPIES.values()))
    add("VAL1939_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent")
    formalization_count = formalization_artifact_count()
    add("VAL1939_12_formalization_untouched", formalization_count == 0, f"formalization_1939_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1939_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1939 parent gravity operator EH or R11 residual Newtonian law",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1939 Y5 R2FR: Parent Gravity Operator EH or R11 Residual Newtonian Law",
        "",
        "## Verdict",
        "",
        "1939 records the minimal GR-compatible gravity operator candidate: Einstein-Hilbert with `kappa=8*pi*G/c^4`, plus an explicit residual slot. Under the EH/no-residual branch, the Newtonian Poisson law follows conditionally. That is a real local Newtonian route, but still not a derived MTS parent claim.",
        "",
        "If MTS keeps an R11/residual operator, the residual must get a divergence law and weak-field projection. Otherwise local GR/Newton remains blocked.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Gravity Action Candidate",
        "",
        markdown_table(rows_by_name["gravity_action_candidate"]),
        "",
        "## EH Newtonian Theorem",
        "",
        markdown_table(rows_by_name["eh_newtonian_theorem"]),
        "",
        "## R11 Residual Newtonian Law",
        "",
        markdown_table(rows_by_name["r11_residual_law"]),
        "",
        "## Operator Decision Matrix",
        "",
        markdown_table(rows_by_name["operator_decision_matrix"]),
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
        "gravity_action_candidate": gravity_action_candidate_rows(),
        "eh_newtonian_theorem": eh_newtonian_theorem_rows(),
        "r11_residual_law": r11_residual_law_rows(),
        "operator_decision_matrix": operator_decision_matrix_rows(),
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
