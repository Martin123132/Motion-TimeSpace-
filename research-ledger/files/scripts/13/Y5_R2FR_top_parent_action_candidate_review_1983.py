from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1983-Y5-R2FR-top-parent-action-candidate-review.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1983_VALIDATION.csv"

SOURCE_PATHS = {
    "1982_doc": ROOT / "1982-Y5-R2FR-wider-corpus-parent-action-signature-scan.md",
    "1982_validation": MTS_RESIDUALS / "P8_Y5_BRR545_1982_VALIDATION.csv",
    "1982_hits": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1982_WIDER_CORPUS_CANDIDATE_HITS.csv",
    "yang_mills": REPO / "quantum-particle-field" / "yang-mills" / "yang-mills-mass-gap-via-the-motion-theory.md",
    "proof_obligations": FORMALIZATION / "19-proof-obligations.md",
    "equation_register": FORMALIZATION / "05-equation-register.md",
    "unification_spine": FORMALIZATION / "07-unification-spine.md",
    "bmem_boundary": FORMALIZATION / "174-bmem-parent-boundary-law.md",
    "local_suppression": FORMALIZATION / "54-local-branch-suppression-conditions.md",
    "support_powers": FORMALIZATION / "73-support-powers-kperp-lemma.md",
    "projected_source_laws": FORMALIZATION / "75-projected-source-laws.md",
    "projected_source_results": FORMALIZATION / "76-projected-source-laws-first-results.md",
    "source_boundary": FORMALIZATION / "71-source-support-boundary-law.md",
    "galaxy_v10": REPO / "galaxy-work" / "current-drafts" / "mts-galaxy-law-v10.docx",
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1983_SOURCE_REGISTER.csv",
    "review_criteria": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1983_PARENT_SIGNATURE_REVIEW_CRITERIA.csv",
    "candidate_review": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1983_TOP_CANDIDATE_REVIEW.csv",
    "promotion_ledger": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1983_PROMOTION_LEDGER.csv",
    "route_impact": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1983_ROUTE_IMPACT.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1983_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1983_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1983_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1983_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "TOP_PARENT_ACTION_CANDIDATE_REVIEW_1983_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1983_MINIMAL_PARENT_SIGNATURE_CONSTRUCTION_QUEUE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


CREATED_AT = now()


def ensure_dirs() -> None:
    for path in [MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE, DOC_PATH.parent]:
        path.mkdir(parents=True, exist_ok=True)


def row(values: dict[str, object]) -> dict[str, str]:
    defaults = {
        "branch": BRANCH,
        "id": "",
        "valid_for_claim": "false",
        "public_claim": "false",
        "created_at_utc": CREATED_AT,
    }
    merged = {**defaults, **values}
    return {key: str(value) for key, value in merged.items()}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path in SOURCE_PATHS.items():
        rows.append(
            row(
                {
                    "id": f"SRC1983_{len(rows):02d}_{source_id}",
                    "source_id": source_id,
                    "source_path": str(path),
                    "exists": str(path.exists()).lower(),
                    "role": "manual review input for top wider-corpus parent-action candidates",
                }
            )
        )
    return rows


def criteria_rows() -> list[dict[str, str]]:
    return [
        row(
            {
                "id": "CRIT1983_0_parent_object",
                "criterion": "parent memory object identified",
                "required": "source must identify the local memory field/coordinate or canonical fluctuation varied before readout",
                "reject_if": "analogy, empirical fit, unrelated gauge-field mass gap, or post-readout closure",
            }
        ),
        row(
            {
                "id": "CRIT1983_1_action",
                "criterion": "parent action/signature",
                "required": "source must give an action, Lagrangian, second variation, or theorem that owns the sign before local tests",
                "reject_if": "conditional assumption, proof obligation, checklist, or candidate-only action",
            }
        ),
        row(
            {
                "id": "CRIT1983_2_Zm",
                "criterion": "positive kinetic sign",
                "required": "source must sign Z_m>=Z_min>0 or an equivalent canonical positive field metric with units",
                "reject_if": "merely says positive/coercive/elliptic is assumed or required",
            }
        ),
        row(
            {
                "id": "CRIT1983_3_gap",
                "criterion": "strict mass/canonical gap",
                "required": "source must sign V_R''>=M2_min>0 or mu_m^2>0 after zero-mode projection",
                "reject_if": "ordinary extremum, generic stability language, or unrelated spectral gap",
            }
        ),
        row(
            {
                "id": "CRIT1983_4_source_boundary",
                "criterion": "source and boundary closure",
                "required": "source must own J_m/source-zero/boundary/readout silence or provide bounded residual rows",
                "reject_if": "states the source/boundary theorem is still conditional",
            }
        ),
        row(
            {
                "id": "CRIT1983_5_same_branch",
                "criterion": "same-parent branch",
                "required": "Z_m/gap/source/boundary must belong to one branch, with units and arena matching",
                "reject_if": "mixes galaxy/cosmology/local coefficients without a parent coefficient law",
            }
        ),
    ]


def review_rows() -> list[dict[str, str]]:
    return [
        row(
            {
                "id": "REV1983_0_yang_mills_cluster",
                "hit_ids": "HIT1982_000;HIT1982_001;HIT1982_002;HIT1982_003;HIT1982_004",
                "source_path": str(SOURCE_PATHS["yang_mills"]),
                "line_refs": "3;7;417",
                "reviewed_content": "Yang-Mills/QCD mass-gap argument using curvature-resistance modification of gauge dynamics.",
                "parent_signature_test": "fails CRIT1983_0, CRIT1983_2, CRIT1983_3, CRIT1983_5 for the MTS memory branch",
                "verdict": "REJECT_AS_PARENT_MEMORY_SIGNATURE_SOURCE",
                "reason": "unrelated gauge-field/spectral-gap analogy; no MTS memory scalar m, no Z_m(X_B), no V_R'', no local source/boundary package",
            }
        ),
        row(
            {
                "id": "REV1983_1_recombination_memory_saturation",
                "hit_ids": "HIT1982_005",
                "source_path": str(SOURCE_PATHS["proof_obligations"]),
                "line_refs": "4699",
                "reviewed_content": "recombination-era memory saturation / matter-radiation decoupling statement",
                "parent_signature_test": "fails CRIT1983_1 through CRIT1983_5",
                "verdict": "REJECT_AS_PARENT_MEMORY_SIGNATURE_SOURCE",
                "reason": "cosmology decoupling interpretation, not a local parent action signing Z_m or a strict memory Hessian",
            }
        ),
        row(
            {
                "id": "REV1983_2_equation_register_conditionals",
                "hit_ids": "HIT1982_007;HIT1982_008;HIT1982_009;HIT1982_010;HIT1982_011",
                "source_path": str(SOURCE_PATHS["equation_register"]),
                "line_refs": "901;1668;1819;1823;1905",
                "reviewed_content": "equation-register rows for solar/no-jump, relaxation lock, support powers, projected source laws",
                "parent_signature_test": "fails CRIT1983_1 because the entries explicitly list assumptions/limits",
                "verdict": "REJECT_AS_PARENT_MEMORY_SIGNATURE_SOURCE",
                "reason": "useful conditional map, but states source leak, convexity, boundary theorem, powers, or parent origin remain open",
            }
        ),
        row(
            {
                "id": "REV1983_3_spine_and_local_boundary_conditionals",
                "hit_ids": "HIT1982_012;HIT1982_014;HIT1982_015;HIT1982_016;HIT1982_017;HIT1982_021",
                "source_path": "formalization-workbench/07,54,71,73,75,76 grouped",
                "line_refs": "07:655;54:202;71:391;73:285;75:330;76:101",
                "reviewed_content": "conditional source-silence, K_perp, boundary, and elliptic/static local lemmas",
                "parent_signature_test": "fails CRIT1983_2 through CRIT1983_4 for memory m",
                "verdict": "REJECT_AS_PARENT_MEMORY_SIGNATURE_SOURCE",
                "reason": "conditional local machinery, not a signed parent memory kinetic metric or V_R Hessian",
            }
        ),
        row(
            {
                "id": "REV1983_4_bmem_boundary_law",
                "hit_ids": "HIT1982_013",
                "source_path": str(SOURCE_PATHS["bmem_boundary"]),
                "line_refs": "228",
                "reviewed_content": "b_mem positive if parent trace coupling is positive and cosmological memory relaxes",
                "parent_signature_test": "fails CRIT1983_1 and CRIT1983_2 because positivity is an if-clause",
                "verdict": "REJECT_AS_PARENT_MEMORY_SIGNATURE_SOURCE",
                "reason": "explicitly demotes b_mem magnitude to calibrated phenomenological amplitude; not a parent Z_m/V_R signature",
            }
        ),
        row(
            {
                "id": "REV1983_5_galaxy_empirical_hits",
                "hit_ids": "HIT1982_006;HIT1982_018;HIT1982_019;HIT1982_020",
                "source_path": str(SOURCE_PATHS["galaxy_v10"]),
                "line_refs": "docx extracted chunks around 488 and 634",
                "reviewed_content": "galaxy law numerics, radial load, LTG coupling, branch invariants, calibrated Aloc/U*",
                "parent_signature_test": "fails CRIT1983_1 through CRIT1983_5",
                "verdict": "REJECT_AS_PARENT_MEMORY_SIGNATURE_SOURCE",
                "reason": "empirical galaxy branch material; valuable as test pillar, but not local parent action/signature evidence",
            }
        ),
    ]


def build_tables() -> dict[str, list[dict[str, str]]]:
    reviews = review_rows()
    promotion_ledger = [
        row(
            {
                "id": "PROM1983_0_promoted_sources",
                "candidate_count_reviewed": len(reviews),
                "promoted_count": 0,
                "status": "NO_PROMOTION",
                "reason": "no top candidate satisfies the parent object, action, Z_m sign, strict gap, source/boundary, and same-branch criteria",
            }
        ),
        row(
            {
                "id": "PROM1983_1_reopen_condition",
                "candidate_count_reviewed": len(reviews),
                "promoted_count": 0,
                "status": "REOPEN_ONLY_WITH_EXACT_PARENT_SIGNATURE",
                "reason": "need exact equation/source path for memory action or canonical second variation, not analogy or assumption",
            }
        ),
    ]
    route_impact = [
        row(
            {
                "id": "IMP1983_0_memory_route",
                "area": "memory positivity route",
                "status": "CLOSURE_ONLY_IN_CURRENT_AVAILABLE_CORPUS",
                "impact": "1980 theorem remains mathematically useful, but no reviewed source promotes it to a derived local-GR gate.",
            }
        ),
        row(
            {
                "id": "IMP1983_1_not_failure",
                "area": "project status",
                "status": "NOT_DEAD_BUT_ROUTE_DEMOTED",
                "impact": "The work has ruled out a shortcut; next progress requires constructing or finding a parent signature, not rescanning the same hits.",
            }
        ),
        row(
            {
                "id": "IMP1983_2_next_leap",
                "area": "next route",
                "status": "CONSTRUCT_MINIMAL_SIGNATURE_CONTRACT",
                "impact": "Build the minimal parent action/signature that would make the theorem true, then test whether it is compatible with existing cosmology/galaxy/local branches without hidden tuning.",
            }
        ),
    ]
    claim_gate = [
        row(
            {
                "id": "GATE1983_0_promoted_source",
                "gate": "claim-grade parent source promoted",
                "status": "BLOCKED",
                "reason": "zero reviewed candidates promoted",
                "required_to_open": "exact parent memory action/signature source satisfying all review criteria",
            }
        ),
        row(
            {
                "id": "GATE1983_1_local_GR",
                "gate": "derived local GR/Newton route via memory positivity",
                "status": "BLOCKED",
                "reason": "memory positivity route is closure-only in current available corpus",
                "required_to_open": "minimal parent signature construction or new source that signs Z_m/gap/source/boundary",
            }
        ),
    ]
    decision = [
        row(
            {
                "id": "DEC1983_0_review_result",
                "decision": "NO_TOP_HIT_PROMOTED",
                "because": "top wider-corpus hits are analogy, conditional machinery, empirical galaxy material, or explicit assumptions",
                "next_action": "stop rescanning these same hits for Z_m; pivot to constructive parent-signature contract",
            }
        ),
        row(
            {
                "id": "DEC1983_1_route_status",
                "decision": "MEMORY_POSITIVITY_ROUTE_CURRENTLY_CLOSURE_ONLY",
                "because": "the conditional theorem lacks a parent-owned source in current reviewed materials",
                "next_action": "retain residual coefficients and prevent local-GR claims through this route",
            }
        ),
        row(
            {
                "id": "DEC1983_2_best_next",
                "decision": "MINIMAL_PARENT_SIGNATURE_CONSTRUCTION",
                "because": "the non-circular leap is now constructive: write the smallest parent action/signature contract and test whether it introduces unacceptable tuning or conflicts",
                "next_action": "1984-Y5-R2FR-minimal-parent-memory-signature-contract-or-route-demotion.md",
            }
        ),
    ]
    next_rows = [
        row(
            {
                "id": "NEXT1983_0_primary",
                "status": "selected",
                "target_doc": "1984-Y5-R2FR-minimal-parent-memory-signature-contract-or-route-demotion.md",
                "target_script": "scripts/Y5_R2FR_minimal_parent_memory_signature_contract_or_route_demotion_1984.py",
                "task": "construct the minimal same-parent memory action/signature contract that would sign Z_m, canonical gap/M2_min, source-zero/bounds, boundary/readout silence, units, and arena matching; if it is just an inserted closure, demote the route.",
                "success_condition": "a falsifiable parent-signature contract with compatibility gates, or explicit route demotion to retained residual/phenomenology",
            }
        )
    ]
    snapshot = [
        row(
            {
                "id": "SNAP1983_0_position",
                "area": "local GR/Newton",
                "status": "DERIVATION_GATE_BLOCKED",
                "summary": "No reviewed wider-corpus hit signs the parent memory action. The downstream theorem remains conditional.",
            }
        ),
        row(
            {
                "id": "SNAP1983_1_progress",
                "area": "anti-circling",
                "status": "SHORTCUT_REJECTED",
                "summary": "We inspected the best hits and rejected them as parent signatures; the next move must construct/test the missing contract.",
            }
        ),
    ]
    source_weight = [
        row(
            {
                "id": "SW1983_0",
                "doc": DOC_PATH.name,
                "weight": "private_nonclaim_manual_review",
                "claim_safety": "no candidate promoted; all claim flags false",
                "use": "prevents false promotion of wider-corpus analogy/conditional/empirical hits",
            }
        )
    ]
    queue = [
        row(
            {
                "id": "Q1983_0_minimal_signature_contract",
                "quantity": "minimal parent memory signature",
                "priority": "highest",
                "why": "current source hunt did not find it; construction is the next non-circular route",
                "target": "1984 contract or demotion",
            }
        )
    ]
    return {
        "source_register": source_register_rows(),
        "review_criteria": criteria_rows(),
        "candidate_review": reviews,
        "promotion_ledger": promotion_ledger,
        "route_impact": route_impact,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_rows,
        "snapshot": snapshot,
        "source_weight": source_weight,
        "queue": queue,
    }


def all_claim_flags_false(tables: dict[str, list[dict[str, str]]]) -> bool:
    return all(
        item.get("valid_for_claim") == "false" and item.get("public_claim") == "false"
        for rows in tables.values()
        for item in rows
    )


def output_csvs_parse() -> bool:
    for path in OUTPUTS.values():
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return False
    return True


def formalization_1983_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return len([path for path in FORMALIZATION.rglob("*1983*") if path.is_file()])


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sources_ok = all(item["exists"] == "true" for item in tables["source_register"])
    criteria_ok = len(tables["review_criteria"]) >= 6
    reviews_ok = all(item["verdict"] == "REJECT_AS_PARENT_MEMORY_SIGNATURE_SOURCE" for item in tables["candidate_review"])
    promotion_by_id = {item["id"]: item for item in tables["promotion_ledger"]}
    no_promotion = promotion_by_id["PROM1983_0_promoted_sources"]["promoted_count"] == "0"
    gates_blocked = all(item["status"] == "BLOCKED" for item in tables["claim_gate"])
    next_selected = tables["next"][0]["target_doc"] == "1984-Y5-R2FR-minimal-parent-memory-signature-contract-or-route-demotion.md"
    pycache_path = ROOT / "scripts" / "__pycache__"
    formalization_count = formalization_1983_artifact_count()
    specs = [
        ("VAL1983_00_sources", sources_ok, "all reviewed source paths exist"),
        ("VAL1983_01_criteria", criteria_ok, "parent signature review criteria written"),
        ("VAL1983_02_reviews_reject", reviews_ok, "all top candidate groups rejected as parent memory signature sources"),
        ("VAL1983_03_no_promotion", no_promotion, "zero candidates promoted"),
        ("VAL1983_04_claim_gates", gates_blocked, "all claim gates blocked"),
        (
            "VAL1983_05_decision",
            tables["decision"][-1]["decision"] == "MINIMAL_PARENT_SIGNATURE_CONSTRUCTION",
            "decision selects constructive parent-signature route",
        ),
        ("VAL1983_06_next_target", next_selected, "1984 target selected"),
        ("VAL1983_07_claim_flags_safe", all_claim_flags_false(tables), "claim flags all false"),
        ("VAL1983_08_csv_parse", output_csvs_parse(), "all generated CSVs parse with rows"),
        ("VAL1983_09_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"),
        ("VAL1983_10_formalization_untouched", formalization_count == 0, f"formalization_1983_artifact_count={formalization_count}"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
            "public_claim": "false",
        }
        for validation_id, passed, detail in specs
    ]
    rows.append(
        {
            "validation_id": "VAL1983_OVERALL",
            "status": "PASS" if all(item["status"] == "PASS" for item in rows) else "FAIL",
            "detail": "1983 top parent action candidate review",
            "valid_for_claim": "false",
            "public_claim": "false",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]]) -> str:
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for item in rows:
        values = [item.get(header, "").replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Review Criteria", tables["review_criteria"]),
        ("Top Candidate Review", tables["candidate_review"]),
        ("Promotion Ledger", tables["promotion_ledger"]),
        ("Route Impact", tables["route_impact"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1983 Y5 R2FR: Top Parent Action Candidate Review",
        "",
        "Private checkpoint. This manually reviews the top wider-corpus hits from 1982 against strict parent-memory-signature criteria.",
        "",
        "Verdict: no top wider-corpus hit is promoted as a parent memory action/signature source. The Yang-Mills hit is an unrelated spectral-gap analogy, the formalization hits are conditional assumptions/proof obligations, and the galaxy hits are empirical branch material. The memory-positivity route remains closure-only in the currently reviewed corpus.",
        "",
        "No local-GR, Newton, EH, R10, PPN, clock, orbital, or public claim follows from 1983.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1983_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
