from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4049-Y5-R2FR-PPC4048-corpus-clause-map-and-conflict-ledger.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4049_SOURCE_REGISTER.csv",
    "corpus_clause_map": SOURCE_DIR / "P8_Y5_R2FR_4049_CORPUS_CLAUSE_MAP.csv",
    "conflict_ledger": SOURCE_DIR / "P8_Y5_R2FR_4049_CONFLICT_LEDGER.csv",
    "adoption_readiness": SOURCE_DIR / "P8_Y5_R2FR_4049_ADOPTION_READINESS_SCORECARD.csv",
    "integration_patch_plan": SOURCE_DIR / "P8_Y5_R2FR_4049_REQUIRED_FORMALIZATION_PATCH_PLAN.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4049_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4049_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4049_CLAIM_GATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4049_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4049_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4049_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4049_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        ("SRC4049_00", SOURCE_DIR / "P8_Y5_R2FR_4048_PARENT_PACKET_CONTRACT.csv", "PPC4048_0_field_space", "new PPC4048 packet clauses"),
        ("SRC4049_01", ROOT / "4048-Y5-R2FR-parent-selected-local-packet-adoption-or-fallback-scorecard.md", "`PPC4048` is now the exact contract", "4048 handoff"),
        ("SRC4049_02", FORMALIZATION / "12-minimal-parent-theory-sketch.md", "This is an ansatz until the induced-gravity step is proven.", "formal parent sketch admits induced-gravity/action gap"),
        ("SRC4049_03", FORMALIZATION / "33-parent-projection-map.md", "the parent theory needs a projection chain:", "formal projection-map evidence"),
        ("SRC4049_04", FORMALIZATION / "35-parent-stress-energy-options.md", "the parent gravitational equation must be written in total-conserved form;", "formal source/stress conservation requirement"),
        ("SRC4049_05", FORMALIZATION / "36-minimal-parent-equations-v0.md", "It does not derive the final `T_MTS,mu_nu` from a closed action.", "formal closed-action gap"),
        ("SRC4049_06", FORMALIZATION / "37-local-switch-off-and-ppn-gate.md", "no MTS correction is allowed to be interesting locally until it is proven PPN-safe.", "formal local PPN safety rule"),
        ("SRC4049_07", FORMALIZATION / "83-parent-equations-v1.md", "not closed-action derived;", "formal v1 open-system scaffold status"),
        ("SRC4049_08", FORMALIZATION / "95-transition-owner-equations-v2.md", "open_Khat_projection_theorem_required = 1", "formal Khat projection theorem gap"),
        ("SRC4049_09", FORMALIZATION / "96-transition-closure-contract.md", "open_parent_derivation_can_supersede_closure = 1", "formal closure can be superseded by derivation"),
        ("SRC4049_10", FORMALIZATION / "120-derivability-promotion-gate.md", "q_loc profile and PPN residual vector are not derived small enough", "formal local gravity blocker"),
        ("SRC4049_11", FORMALIZATION / "121-local-PPN-repair-route.md", "local_claim_safe_now = false", "formal local claim still unsafe"),
        ("SRC4049_12", FORMALIZATION / "144-local-transition-closure-contract.md", "local transition branch = explicit closure-only.", "formal transition branch closure-only status"),
        ("SRC4049_13", FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md", "MTS parent equations -> Einstein/GR local limit -> Newtonian weak-field limit.", "formal GR-limit target"),
        ("SRC4049_14", FORMALIZATION / "29-em-maxwell-gate-audit.md", "Maxwell recovery: not passed.", "formal EM/Maxwell gap"),
        ("SRC4049_15", FORMALIZATION / "32-maxwell-limit-targets.md", "MTS Maxwell electromagnetism: not yet derived.", "formal Maxwell limit status"),
        ("SRC4049_16", FORMALIZATION / "19-proof-obligations.md", "No sector may upgrade itself by good narrative alone.", "formal proof-obligation claim firewall"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def corpus_clause_map_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("PPC4048_0_field_space", "field-space factorization", "12,33,83", "parent objects and projection chain exist, but Q_parent^loc=Q_dyn^loc x K_G x Q_aux is not formalized", "PARTIAL_NEEDS_FORMAL_PRODUCT_MAP"),
        ("PPC4048_1_action_domain", "local <=2PN action domain", "12,36,83,144", "formal corpus explicitly says action/closed derivation and local GR theorem are not done", "CONFLICT_REQUIRES_NEW_LOCAL_ACTION_PACKET"),
        ("PPC4048_2_fixed_coupling", "constant local coupling branch", "35,36,83", "kappa_GR/G coupling is present as calibrated scaffold; K_G superselection/no-Hom branch is not adopted", "PARTIAL_NEEDS_KG_SUPERSELECTION_CLAUSE"),
        ("PPC4048_3_source_functor", "ordinary matter source descent", "35,36,19", "total conserved source spine exists; q-basic matter functor and no source-prefactor grammar are not in formal corpus", "PARTIAL_NEEDS_MATTER_FUNCTOR_INSERTION"),
        ("PPC4048_4_em_owner", "unique EM owner", "29,32,35", "formal EM sector says Maxwell recovery is not passed; PPC4048 can use standard observed EM as local-GR source but does not unify EM", "COMPATIBLE_LOCAL_STANDARD_EM_ONLY_GLOBAL_EM_OPEN"),
        ("PPC4048_5_source_charge", "same source charge", "35,36,37", "stress/source conservation spine exists; Pi_M/H_tau/Hilbert same-charge machinery is post-checkpoint, not formalized", "PARTIAL_NEEDS_SOURCE_CHARGE_MAP"),
        ("PPC4048_6_boundary_support", "proper boundary/support branch", "96,144,37", "formal closure/no-leak language exists but is explicitly closure-only, not a parent theorem", "PARTIAL_NEEDS_BOUNDARY_SUPPORT_DERIVATION"),
        ("PPC4048_7_gamma_khat_qloc", "Gamma/Khat/q_loc projector silence", "95,120,121,144", "formal corpus directly says Khat/q_loc/local PPN theorem remains open", "CONFLICT_PRIMARY_FORMAL_BLOCKER"),
        ("PPC4048_8_memory_reset", "local retarded memory branch", "37,83,96,144", "local no-leak/switch-off route exists but old formal corpus treats it as closure/quarantine, not reset theorem", "PARTIAL_NEEDS_MEMORY_RESET_PROMOTION"),
        ("PPC4048_9_readout_firewall", "readout-after-variation firewall", "19,120,145", "proof obligations and testing map support the firewall posture; exact readout-order action clause not formalized", "MOSTLY_COMPATIBLE_NEEDS_EXPLICIT_READOUT_CLAUSE"),
        ("PPC4048_10_claim_firewall", "claim firewall", "19,120,144,145", "formal corpus strongly supports nonclaim discipline and local GR blockage until theorem is supplied", "SUPPORTED_KEEP"),
    ]
    return [
        {
            "clause_id": clause_id,
            "contract_clause": clause,
            "formal_source_ids": formal_sources,
            "corpus_evidence_summary": summary,
            "adoption_verdict": verdict,
            "actual_corpus_adopts_clause_now": verdict == "SUPPORTED_KEEP",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for clause_id, clause, formal_sources, summary, verdict in rows
    ]


def conflict_ledger_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("CON4049_0_closed_action", "closed local parent action missing", "36/83 state the parent package is not closed-action derived", "PPC4048_1_action_domain", "add a local <=2PN action packet or keep PPC4048 private conditional"),
        ("CON4049_1_q_loc", "q_loc/Khat projector theorem open", "95/120/121/144 identify Khat/q_loc/local PPN as open or closure-only", "PPC4048_7_gamma_khat_qloc", "map post-4023..4030 derivation into formal corpus or score q_loc residuals"),
        ("CON4049_2_KG", "K_G superselection not formalized", "formal corpus uses kappa_GR scaffold but not Q_dyn x K_G with no-Hom labels", "PPC4048_2_fixed_coupling", "write fixed-coupling/superselection clause"),
        ("CON4049_3_source_charge", "Pi_M/H_tau/Hilbert same-charge machinery absent from formal corpus", "formal stress spine exists but not the post-checkpoint charge-lock mechanism", "PPC4048_5_source_charge", "insert same-source charge map or keep orbital/PPN source rows fallback"),
        ("CON4049_4_matter_functor", "q-basic matter functor/no source-prefactor grammar absent", "formal corpus demands conservation but not the exact functor grammar", "PPC4048_3_source_functor", "write matter/source-label-forgetting constructor clause"),
        ("CON4049_5_memory_closure", "local memory/no-leak branch is closure in formal corpus", "96/144 say parent derivation can supersede closure but has not", "PPC4048_8_memory_reset", "promote 4046 reset theorem into corpus or keep memory fallback"),
        ("CON4049_6_boundary_support", "boundary/support no-flux not parent-derived in formal corpus", "96/144 use closure/no-leak contract language", "PPC4048_6_boundary_support", "insert proper boundary/support theorem or bound flux rows"),
        ("CON4049_7_EM", "Maxwell/emergent EM not derived globally", "29/32 explicitly say Maxwell recovery not passed", "PPC4048_4_em_owner", "separate local standard-EM source recovery from global EM unification"),
        ("CON4049_8_claim", "formal corpus forbids upgrade by narrative", "19/120/144/145 require local GR theorem before claims", "PPC4048_10_claim_firewall", "keep nonclaim status until corpus adoption or scorer rows pass"),
    ]
    return [
        {
            "conflict_id": conflict_id,
            "conflict": conflict,
            "formal_evidence": evidence,
            "affected_clause": clause,
            "resolution_route": route,
            "blocks_public_local_GR": True,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for conflict_id, conflict, evidence, clause, route in rows
    ]


def adoption_readiness_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "score_id": "READ4049_0_private_packet",
            "object": "PPC4048 private selected packet",
            "readiness": "strong_private_candidate",
            "reason": "post-checkpoint derivation stack gives a sufficient conditional local-GR packet",
            "public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "score_id": "READ4049_1_formal_corpus_adoption",
            "object": "formalization-workbench corpus adoption",
            "readiness": "not_adopted",
            "reason": "formal corpus still says local PPN/GR and Khat/q_loc are open or closure-only",
            "public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "score_id": "READ4049_2_compatibility",
            "object": "PPC4048 compatibility with formal spine",
            "readiness": "compatible_as_repair_patch",
            "reason": "formal corpus already requests exactly this kind of parent-derived GR-limit theorem",
            "public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "score_id": "READ4049_3_next_action",
            "object": "next adoption route",
            "readiness": "patch_plan_required",
            "reason": "must add a formal local parent packet and update old closure-only docs before claim status can change",
            "public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def integration_patch_plan_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("PATCH4049_0_new_doc", "create formal local parent packet doc", "add a future formalization-workbench doc that states PPC4048 with all assumptions, no public claim until reviewed", "not_applied_in_4049"),
        ("PATCH4049_1_update_120_121", "update local PPN blocker docs", "cross-reference PPC4048 as candidate repair route while keeping local_claim_safe_now=false until adoption verified", "not_applied_in_4049"),
        ("PATCH4049_2_update_144_145", "update closure/GR-limit map", "mark PPC4048 as candidate parent derivation route that could supersede closure-only branch", "not_applied_in_4049"),
        ("PATCH4049_3_update_29_32", "protect EM wording", "separate local standard-EM source owner from the still-open global Maxwell derivation", "not_applied_in_4049"),
        ("PATCH4049_4_append_claims", "claims register update", "add nonclaim private status: conditional local GR packet candidate, not public local-GR derivation", "not_applied_in_4049"),
        ("PATCH4049_5_scored_fallbacks", "fallback score route", "if any PPC4048 clause is not adopted, fill corresponding PPN/R10/WEP/clock/orbital score rows", "not_applied_in_4049"),
    ]
    return [
        {
            "patch_id": patch_id,
            "patch_target": target,
            "required_change": change,
            "status": status,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for patch_id, target, change, status in rows
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4049_0_private_packet",
            "verdict": "PPC4048_STRONG_PRIVATE_REPAIR_PACKET",
            "result": "The post-checkpoint packet is internally coherent and targets the exact formal local-GR gap identified by the corpus.",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4049",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4049_1_actual_corpus",
            "verdict": "FORMAL_CORPUS_DOES_NOT_YET_ADOPT_PPC4048",
            "result": "The formalization-workbench sources still label the local branch, q_loc/Khat route, and Maxwell/global EM route as open or closure-only.",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4049",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4049_2_next",
            "verdict": "FORMAL_PATCH_OR_FALLBACK_SCORE_NEXT",
            "result": "Next step is either a guarded formal packet integration draft or fallback score rows for each rejected clause.",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4049",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4049_0_no_adoption_yet",
            "decision": "do not declare PPC4048 adopted by the actual corpus",
            "reason": "formalization-workbench still contains explicit local-GR/PPN/q_loc/Maxwell open-status statements",
            "next_action": "draft guarded formal integration plan or score fallback rows",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4049_1_best_route",
            "decision": "best route is a formal packet integration draft, not more abstract checkpoints",
            "reason": "the private derivation stack is mature enough to test against the corpus directly",
            "next_action": "4050 guarded formal packet draft in post-checkpoint first",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4049_0_private",
            "claim": "PPC4048 is compatible with the formal spine as a candidate repair patch",
            "allowed": True,
            "public_claim": False,
            "scope": "private compatibility result only",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4049_1_adopted",
            "claim": "the actual formal corpus already adopts PPC4048",
            "allowed": False,
            "public_claim": False,
            "scope": "contradicted by formal open/closure-only status files",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4049_2_public_local_GR",
            "claim": "MTS publicly derives local GR",
            "allowed": False,
            "public_claim": False,
            "scope": "blocked until formal adoption patch is applied and verified or fallback scores pass",
            "timestamp_utc": ts,
        },
    ]


def remaining_residual_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4049_0_formal_patch",
            "symbol": "formal_PPC4048_integration",
            "residual": "a guarded formal local parent packet must be drafted and cross-linked without erasing older caveats",
            "current_route": "4050 guarded formal packet draft in post-checkpoint first",
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4049_1_q_loc",
            "symbol": "q_loc_Khat_formal_blocker",
            "residual": "formal corpus still identifies q_loc/Khat projection theorem as open",
            "current_route": "integrate post-4023..4030 route or score q_loc residuals",
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4049_2_EM",
            "symbol": "Maxwell_global_unification_gap",
            "residual": "formal EM docs still say Maxwell recovery is not derived",
            "current_route": "keep local standard EM source owner separate from future global Maxwell derivation",
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4049_0",
            "next_doc": "4050-Y5-R2FR-guarded-formal-PPC4048-integration-draft.md",
            "next_script": "scripts/Y5_R2FR_4050_guarded_formal_PPC4048_integration_draft.py",
            "reason": "4049 shows PPC4048 is compatible as a repair patch but not yet in the formal corpus; draft the guarded integration before touching formalization-workbench",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4049",
            "status": "PPC4048_COMPATIBLE_REPAIR_PATCH_FORMAL_CORPUS_NOT_YET_ADOPTED",
            "public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def doc_text(ts: str, source_count: int) -> str:
    return f"""# 4049 - PPC4048 Corpus Clause Map And Conflict Ledger

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: read `formalization-workbench`; write only `post-checkpoint-work`.
- Source needles found: `{source_count}/17`.

## What Actually Moved

4049 checks `PPC4048` against the older formal corpus instead of assuming adoption.

Result:

- `PPC4048` is a strong private repair packet.
- The formal corpus is compatible with needing such a packet.
- The formal corpus does **not** yet adopt it.

The strongest conflicts are exactly where expected:

- closed local parent action is not formalized;
- `q_loc/Khat` projector theorem is still marked open;
- local transition/PPN safety is still closure-only in the old formal docs;
- global Maxwell/EM recovery remains open and must not be confused with local standard-EM sourcing.

## Current Verdict

- Current evaluator result: `FORMAL_CORPUS_DOES_NOT_YET_ADOPT_PPC4048`.
- Compatibility result: `PPC4048_STRONG_PRIVATE_REPAIR_PACKET`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4049`.

## Next Target

- `4050-Y5-R2FR-guarded-formal-PPC4048-integration-draft.md`
- `scripts/Y5_R2FR_4050_guarded_formal_PPC4048_integration_draft.py`
"""


def script_compiles() -> bool:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        return True
    except py_compile.PyCompileError:
        return False


def validate_outputs(source_register: List[Dict[str, object]], tables: Dict[str, List[Dict[str, object]]]) -> List[Dict[str, object]]:
    def all_rows_have_false_public(rows: Iterable[Dict[str, object]]) -> bool:
        for row in rows:
            if "valid_for_public_claim" in row and row["valid_for_public_claim"] is not False:
                return False
            if "public_claim" in row and row["public_claim"] is not False:
                return False
        return True

    checks = [
        ("VAL4049_00_sources_exist", all(row["exists"] for row in source_register), "all cited source paths exist"),
        ("VAL4049_01_needles_found", all(row["needle_found"] for row in source_register), "all source needles found"),
        ("VAL4049_02_clause_map_11", len(tables["corpus_clause_map"]) == 11, "all eleven PPC4048 clauses mapped"),
        ("VAL4049_03_conflicts", len(tables["conflict_ledger"]) >= 8, "major conflicts recorded"),
        ("VAL4049_04_primary_q_loc", any(row["affected_clause"] == "PPC4048_7_gamma_khat_qloc" for row in tables["conflict_ledger"]), "q_loc/Khat conflict recorded"),
        ("VAL4049_05_no_adopted_claim", any(row["verdict"] == "FORMAL_CORPUS_DOES_NOT_YET_ADOPT_PPC4048" for row in tables["evaluator"]), "formal non-adoption evaluator present"),
        ("VAL4049_06_compatibility", any(row["readiness"] == "compatible_as_repair_patch" for row in tables["adoption_readiness"]), "compatibility readiness present"),
        ("VAL4049_07_patch_plan", len(tables["integration_patch_plan"]) >= 6, "integration patch plan present"),
        ("VAL4049_08_public_blocked", any(row["claim"] == "MTS publicly derives local GR" and row["allowed"] is False for row in tables["claim_gate"]), "public local-GR claim blocked"),
        ("VAL4049_09_formal_adoption_blocked", any(row["claim"] == "the actual formal corpus already adopts PPC4048" and row["allowed"] is False for row in tables["claim_gate"]), "formal adoption claim blocked"),
        ("VAL4049_10_next_4050", len(tables["next_target"]) == 1 and "4050" in tables["next_target"][0]["next_doc"], "4050 next target present"),
        ("VAL4049_11_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        ("VAL4049_12_no_formalization_output", not any(str(path).startswith(str(FORMALIZATION)) for path in OUTPUTS.values()), "no output targets formalization-workbench"),
        ("VAL4049_13_script_compiles", script_compiles(), "script compiles"),
        ("VAL4049_14_private_guard", all(all_rows_have_false_public(rows) for rows in tables.values()), "public-claim guard retained"),
    ]
    return [
        {"check_id": check_id, "passed": passed, "detail": detail}
        for check_id, passed, detail in checks
    ]


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows(ts)
    source_count = sum(1 for row in sources if row["needle_found"])
    tables: Dict[str, List[Dict[str, object]]] = {
        "corpus_clause_map": corpus_clause_map_rows(ts),
        "conflict_ledger": conflict_ledger_rows(ts),
        "adoption_readiness": adoption_readiness_rows(ts),
        "integration_patch_plan": integration_patch_plan_rows(ts),
        "evaluator": evaluator_rows(ts),
        "decision_gate": decision_gate_rows(ts),
        "claim_gate": claim_gate_rows(ts),
        "remaining_residuals": remaining_residual_rows(ts),
        "next_target": next_target_rows(ts),
        "status": status_rows(ts),
    }

    DOC_PATH.write_text(doc_text(ts, source_count), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    for key, rows in tables.items():
        write_csv(OUTPUTS[key], rows)

    validation_rows = validate_outputs(sources, tables)
    write_csv(OUTPUTS["validation"], validation_rows)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation_rows if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"validation rows: {len(validation_rows)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
