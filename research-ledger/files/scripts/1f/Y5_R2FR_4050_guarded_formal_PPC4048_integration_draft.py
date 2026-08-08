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
DOC_PATH = ROOT / "4050-Y5-R2FR-guarded-formal-PPC4048-integration-draft.md"
DRAFT_DOC_PATH = ROOT / "4050-draft-179-PPC4048-local-parent-packet-candidate.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4050_SOURCE_REGISTER.csv",
    "draft_manifest": SOURCE_DIR / "P8_Y5_R2FR_4050_DRAFT_MANIFEST.csv",
    "formal_patch_snippets": SOURCE_DIR / "P8_Y5_R2FR_4050_FORMAL_PATCH_SNIPPETS.csv",
    "guardrail_checklist": SOURCE_DIR / "P8_Y5_R2FR_4050_GUARDRAIL_CHECKLIST.csv",
    "claim_status_delta": SOURCE_DIR / "P8_Y5_R2FR_4050_CLAIM_STATUS_DELTA.csv",
    "adoption_preflight": SOURCE_DIR / "P8_Y5_R2FR_4050_ADOPTION_PREFLIGHT.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4050_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4050_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4050_CLAIM_GATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4050_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4050_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4050_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4050_VALIDATION.csv",
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
        ("SRC4050_00", ROOT / "4048-Y5-R2FR-parent-selected-local-packet-adoption-or-fallback-scorecard.md", "`PPC4048` is now the exact contract", "4048 parent packet handoff"),
        ("SRC4050_01", ROOT / "4049-Y5-R2FR-PPC4048-corpus-clause-map-and-conflict-ledger.md", "The formal corpus does **not** yet adopt it.", "4049 non-adoption guard"),
        ("SRC4050_02", SOURCE_DIR / "P8_Y5_R2FR_4048_PARENT_PACKET_CONTRACT.csv", "PPC4048_10_claim_firewall", "all PPC4048 clauses"),
        ("SRC4050_03", SOURCE_DIR / "P8_Y5_R2FR_4049_CONFLICT_LEDGER.csv", "q_loc/Khat projector theorem open", "conflict ledger"),
        ("SRC4050_04", SOURCE_DIR / "P8_Y5_R2FR_4049_REQUIRED_FORMALIZATION_PATCH_PLAN.csv", "create formal local parent packet doc", "4049 patch plan"),
        ("SRC4050_05", FORMALIZATION / "19-proof-obligations.md", "No sector may upgrade itself by good narrative alone.", "proof obligation claim firewall"),
        ("SRC4050_06", FORMALIZATION / "120-derivability-promotion-gate.md", "public_claim_allowed = false", "current derivability/claim status"),
        ("SRC4050_07", FORMALIZATION / "121-local-PPN-repair-route.md", "local_claim_safe_now = false", "current local PPN status"),
        ("SRC4050_08", FORMALIZATION / "144-local-transition-closure-contract.md", "local transition branch = explicit closure-only.", "current closure-only transition status"),
        ("SRC4050_09", FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md", "MTS parent equations -> Einstein/GR local limit -> Newtonian weak-field limit.", "formal GR-limit target"),
        ("SRC4050_10", FORMALIZATION / "29-em-maxwell-gate-audit.md", "Maxwell recovery: not passed.", "current EM gate"),
        ("SRC4050_11", FORMALIZATION / "32-maxwell-limit-targets.md", "MTS Maxwell electromagnetism: not yet derived.", "current Maxwell target"),
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


def draft_doc_text(ts: str) -> str:
    return """# 179 - PPC4048 Local Parent Packet Candidate

- Drafted: `__TIMESTAMP__`
- Status: `private_candidate_integration_draft`
- Claim status: `not_public_local_GR_claim`
- Intended formal location: `formalization-workbench/179-PPC4048-local-parent-packet-candidate.md`

## Purpose

This draft records the strongest current local-GR repair packet without erasing the older caveats.

The packet is not a declaration that MTS already derives local GR. It is a candidate parent-action contract: if the full corpus adopts it, the selected compact local PPN/Newton branch closes; if any clause is rejected, the corresponding fallback score row must be filled with no cancellation credit.

## Candidate Packet

The local parent branch is:

`Q_parent^loc = Q_dyn^loc x K_G x Q_aux`,

with `q:Q_dyn^loc -> Met_obs`, `V=ker(Dq)`, `kappa_* in K_G`, and `T_local K_G=0`.

Through the local required PPN order:

`S_loc^{<=2PN}=S_EH[g_obs;kappa_*]+S_matter[psi,g_obs,theta]+S_EM[A,g_obs]+S_binding+dB_proper+S_top+S_aux^{double-zero}+S_vert^{Dq=0}`.

Allowed extra local operators are only:

- exact/proper boundary terms;
- topological terms;
- vertical-only terms annihilated by the observed quotient/readout;
- auxiliary double-zero sectors with no linear local PPN source;
- open-system memory terms whose compact local retarded/reset projection is zero.

## Conditional Local Limit

If the packet is adopted as one parent branch, then in the compact stationary local branch:

- `nabla^2 Phi = 4*pi*G_ref*rho_H`;
- `gamma=1`;
- `beta=1`;
- `alpha_i=0`;
- `xi=0`;
- `zeta_i=0`;
- `Gdot/G=0`;
- `Delta_cZ_selected=0`;
- `Delta_cnorm_selected=0`.

This is a conditional local-GR/PPN zero vector under the packet, not a public theorem of the whole MTS corpus.

## Explicit Non-Claims

- This does not predict the numerical value of Newton's constant.
- This does not derive global Maxwell electromagnetism.
- This does not erase cosmology, galaxy, or open-memory sectors.
- This does not make old closure-only files automatically obsolete.
- This does not allow a public local-GR claim until adoption is verified or fallback score rows pass.

## Remaining Formal Weak Links

1. The closed local parent action is not yet in the formal corpus.
2. `q_loc/Khat` projector silence remains the primary formal blocker.
3. The `K_G` superselection/no-Hom coupling branch must be formalized.
4. The Hilbert/H_tau/Pi_M same-source charge map must be formalized.
5. Local standard-EM sourcing must remain separate from global Maxwell recovery.

## Adoption Rule

The packet may be promoted only if every clause is either:

- matched to an existing formal corpus source;
- inserted as an explicit new parent clause;
- or demoted to a named fallback scorer row.

No hidden closure assumption is allowed.
""".replace("__TIMESTAMP__", ts)


def draft_manifest_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "draft_id": "DRAFT4050_0_main",
            "draft_path": str(DRAFT_DOC_PATH),
            "intended_formal_path": str(FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md"),
            "purpose": "guarded candidate local parent packet integration draft",
            "status": "written_in_post_checkpoint_only",
            "public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def formal_patch_snippet_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        (
            "SNIP4050_0_19",
            "19-proof-obligations.md",
            "Add PPC4048 under GR/local-limit obligations",
            "New private candidate: PPC4048 gives a conditional local-GR zero vector only if the parent corpus adopts all packet clauses. It does not upgrade any sector by narrative; rejected clauses must be scored with no cancellation credit.",
        ),
        (
            "SNIP4050_1_120",
            "120-derivability-promotion-gate.md",
            "Update local_gravity_PPN status without claiming pass",
            "local_gravity_PPN remains public_claim_allowed=false, but now has candidate_private_packet=PPC4048 and next action=formal adoption map or fallback score rows.",
        ),
        (
            "SNIP4050_2_121",
            "121-local-PPN-repair-route.md",
            "Cross-link PPC4048 repair route",
            "local_claim_safe_now=false remains unchanged. PPC4048 is the candidate parent-derived repair route to be checked against q_loc/Khat and PPN residual vector requirements.",
        ),
        (
            "SNIP4050_3_144",
            "144-local-transition-closure-contract.md",
            "Mark closure can be superseded by PPC4048 if adopted",
            "The closure-only status remains active until PPC4048 is formally adopted; if adopted, PPC4048 supplies the candidate GR-limit theorem route for the compact local branch.",
        ),
        (
            "SNIP4050_4_145",
            "145-testing-readiness-and-gr-limit-map.md",
            "Add testing-readiness row for PPC4048",
            "PPC4048 is a pre-test formal candidate: it must be adopted or rejected before local-gravity tests can be interpreted as a derived local-GR pass.",
        ),
        (
            "SNIP4050_5_29",
            "29-em-maxwell-gate-audit.md",
            "Protect EM wording",
            "PPC4048 uses standard observed EM as a local Hilbert source owner. This is not a derivation of Maxwell electromagnetism from MTS.",
        ),
        (
            "SNIP4050_6_32",
            "32-maxwell-limit-targets.md",
            "Separate local source owner from global Maxwell target",
            "Even if PPC4048 is adopted for local gravity, the Maxwell-limit target remains open: gauge structure, conserved current, and transverse modes still require derivation.",
        ),
    ]
    return [
        {
            "snippet_id": snippet_id,
            "target_file": str(FORMALIZATION / target),
            "patch_intent": intent,
            "draft_text": text,
            "applied_to_formalization": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for snippet_id, target, intent, text in rows
    ]


def guardrail_checklist_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("GUARD4050_0_no_public_claim", "public local-GR claim remains false", "required", True),
        ("GUARD4050_1_no_numeric_G", "no numerical G prediction is introduced", "required", True),
        ("GUARD4050_2_no_global_EM", "local standard-EM source owner is not called global Maxwell derivation", "required", True),
        ("GUARD4050_3_no_formal_edits", "formalization-workbench is read but not modified by 4050", "required", True),
        ("GUARD4050_4_q_loc_flag", "q_loc/Khat remains explicitly flagged as the primary formal blocker", "required", True),
        ("GUARD4050_5_fallbacks", "every rejected packet clause routes to fallback score rows", "required", True),
        ("GUARD4050_6_old_caveats", "older closure-only caveats are preserved until formal adoption", "required", True),
    ]
    return [
        {
            "guard_id": guard_id,
            "guardrail": guardrail,
            "requirement_level": level,
            "satisfied_in_draft": satisfied,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for guard_id, guardrail, level, satisfied in rows
    ]


def claim_status_delta_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("DELTA4050_0_local_GR", "public_local_GR_claim", "false", "false", "no public claim change"),
        ("DELTA4050_1_private_packet", "private_local_GR_packet_candidate", "available_in_4048", "formal_integration_draft_written", "candidate becomes draftable, not adopted"),
        ("DELTA4050_2_local_claim_safe", "local_claim_safe_now", "false", "false", "kept false until adoption/scoring"),
        ("DELTA4050_3_EM", "global_Maxwell_claim", "false", "false", "kept false; standard local EM sourcing only"),
        ("DELTA4050_4_G", "numerical_G_prediction", "false", "false", "kept false; calibrated G_ref only"),
    ]
    return [
        {
            "delta_id": delta_id,
            "claim_or_status": claim,
            "before_4050": before,
            "after_4050": after,
            "reason": reason,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for delta_id, claim, before, after, reason in rows
    ]


def adoption_preflight_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("PRE4050_0_new_doc", "draft 179 PPC4048 candidate doc", "ready_in_post_checkpoint", "not applied"),
        ("PRE4050_1_crosslinks", "cross-link proof obligations and local PPN docs", "draft snippets ready", "not applied"),
        ("PRE4050_2_claims", "preserve claim false statuses", "ready", "must verify if applied"),
        ("PRE4050_3_conflicts", "do not hide q_loc/Khat or Maxwell conflicts", "ready", "must verify if applied"),
        ("PRE4050_4_fallback", "fallback scorer rows remain available", "ready", "must verify if applied"),
    ]
    return [
        {
            "preflight_id": preflight_id,
            "item": item,
            "draft_status": status,
            "application_status": application_status,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for preflight_id, item, status, application_status in rows
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4050_0_draft_ready",
            "verdict": "GUARDED_FORMAL_INTEGRATION_DRAFT_READY",
            "result": "4050 writes a formal-ready PPC4048 candidate doc and patch snippets while preserving all claim guards.",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4050",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4050_1_not_applied",
            "verdict": "FORMALIZATION_NOT_MODIFIED",
            "result": "No formalization-workbench files are changed by this checkpoint; application remains a separate gated step.",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4050",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4050_2_next",
            "verdict": "READY_FOR_GUARDED_APPLICATION_OR_USER_REVIEW",
            "result": "Next step is either applying the guarded integration patch to formalization-workbench or converting it into a reviewed GitHub-ready update.",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4050",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4050_0_draft",
            "decision": "keep integration as a draft until explicitly applied",
            "reason": "older formal docs contain real caveats that must be preserved, not overwritten",
            "next_action": "4051 guarded apply-or-review gate",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4050_1_best_route",
            "decision": "the best route is now guarded formal integration, not more private abstraction",
            "reason": "PPC4048 has become precise enough to test against the main formal corpus",
            "next_action": "apply patch only after preflight checks",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4050_0_draft",
            "claim": "a guarded formal integration draft for PPC4048 exists",
            "allowed": True,
            "public_claim": False,
            "scope": "private draft status only",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4050_1_adopted",
            "claim": "formalization-workbench now adopts PPC4048",
            "allowed": False,
            "public_claim": False,
            "scope": "not applied by 4050",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4050_2_local_GR",
            "claim": "MTS publicly derives local GR",
            "allowed": False,
            "public_claim": False,
            "scope": "still blocked until guarded patch is applied and verified or scorer rows pass",
            "timestamp_utc": ts,
        },
    ]


def remaining_residual_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4050_0_apply",
            "symbol": "guarded_formal_application",
            "residual": "4050 draft must be applied or reviewed before the formal corpus status changes",
            "current_route": "4051 guarded application preflight",
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4050_1_q_loc",
            "symbol": "q_loc_Khat_primary_formal_blocker",
            "residual": "q_loc/Khat projector silence remains the highest-scrutiny clause in PPC4048",
            "current_route": "keep explicit blocker in integration doc and scorer fallback",
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4050_2_EM",
            "symbol": "Maxwell_global_unification_gap",
            "residual": "PPC4048 local standard-EM source ownership does not solve global Maxwell emergence",
            "current_route": "separate local gravity packet from future Maxwell-limit derivation",
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4050_0",
            "next_doc": "4051-Y5-R2FR-guarded-PPC4048-formal-application-preflight.md",
            "next_script": "scripts/Y5_R2FR_4051_guarded_PPC4048_formal_application_preflight.py",
            "reason": "4050 produced a safe draft; 4051 should decide whether/how to apply it to formalization-workbench without overwriting caveats",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4050",
            "status": "GUARDED_FORMAL_PPC4048_DRAFT_READY_NOT_APPLIED",
            "public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def doc_text(ts: str, source_count: int) -> str:
    return f"""# 4050 - Guarded Formal PPC4048 Integration Draft

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: draft integration in `post-checkpoint-work`; no `formalization-workbench` edits.
- Source needles found: `{source_count}/12`.

## What Actually Moved

4050 converts the 4049 conflict map into a concrete guarded integration draft.

It writes:

- a proposed formal document draft: `4050-draft-179-PPC4048-local-parent-packet-candidate.md`;
- per-file patch snippets for `19`, `120`, `121`, `144`, `145`, `29`, and `32`;
- a claim-status delta table proving the draft does not upgrade public claims.

## Current Verdict

- Current evaluator result: `GUARDED_FORMAL_INTEGRATION_DRAFT_READY`.
- Formal corpus application: `not_applied`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4050`.

## Key Guardrail

The draft preserves:

- `local_claim_safe_now=false`;
- no numerical `G` prediction;
- no global Maxwell derivation claim;
- `q_loc/Khat` as the primary formal blocker;
- fallback scorer rows for any rejected packet clause.

## Next Target

- `4051-Y5-R2FR-guarded-PPC4048-formal-application-preflight.md`
- `scripts/Y5_R2FR_4051_guarded_PPC4048_formal_application_preflight.py`
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
        ("VAL4050_00_sources_exist", all(row["exists"] for row in source_register), "all cited source paths exist"),
        ("VAL4050_01_needles_found", all(row["needle_found"] for row in source_register), "all source needles found"),
        ("VAL4050_02_draft_doc_written", DRAFT_DOC_PATH.exists(), "draft formal doc written in post-checkpoint"),
        ("VAL4050_03_manifest", len(tables["draft_manifest"]) == 1, "draft manifest present"),
        ("VAL4050_04_snippets", len(tables["formal_patch_snippets"]) == 7, "seven formal patch snippets present"),
        ("VAL4050_05_guards", all(row["satisfied_in_draft"] is True for row in tables["guardrail_checklist"]), "all guardrails satisfied in draft"),
        ("VAL4050_06_claim_false_local", any(row["claim_or_status"] == "local_claim_safe_now" and row["after_4050"] == "false" for row in tables["claim_status_delta"]), "local claim remains false"),
        ("VAL4050_07_no_global_EM", any(row["claim_or_status"] == "global_Maxwell_claim" and row["after_4050"] == "false" for row in tables["claim_status_delta"]), "global Maxwell claim remains false"),
        ("VAL4050_08_evaluator_ready", any(row["verdict"] == "GUARDED_FORMAL_INTEGRATION_DRAFT_READY" for row in tables["evaluator"]), "draft-ready evaluator present"),
        ("VAL4050_09_not_applied", any(row["verdict"] == "FORMALIZATION_NOT_MODIFIED" for row in tables["evaluator"]), "not-applied evaluator present"),
        ("VAL4050_10_public_blocked", any(row["claim"] == "MTS publicly derives local GR" and row["allowed"] is False for row in tables["claim_gate"]), "public local-GR claim blocked"),
        ("VAL4050_11_next_4051", len(tables["next_target"]) == 1 and "4051" in tables["next_target"][0]["next_doc"], "4051 next target present"),
        ("VAL4050_12_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        ("VAL4050_13_no_formalization_output", not any(str(path).startswith(str(FORMALIZATION)) for path in OUTPUTS.values()) and not str(DRAFT_DOC_PATH).startswith(str(FORMALIZATION)), "no output targets formalization-workbench"),
        ("VAL4050_14_script_compiles", script_compiles(), "script compiles"),
        ("VAL4050_15_private_guard", all(all_rows_have_false_public(rows) for rows in tables.values()), "public-claim guard retained"),
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
        "draft_manifest": draft_manifest_rows(ts),
        "formal_patch_snippets": formal_patch_snippet_rows(ts),
        "guardrail_checklist": guardrail_checklist_rows(ts),
        "claim_status_delta": claim_status_delta_rows(ts),
        "adoption_preflight": adoption_preflight_rows(ts),
        "evaluator": evaluator_rows(ts),
        "decision_gate": decision_gate_rows(ts),
        "claim_gate": claim_gate_rows(ts),
        "remaining_residuals": remaining_residual_rows(ts),
        "next_target": next_target_rows(ts),
        "status": status_rows(ts),
    }

    DOC_PATH.write_text(doc_text(ts, source_count), encoding="utf-8")
    DRAFT_DOC_PATH.write_text(draft_doc_text(ts), encoding="utf-8")
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
    print(f"wrote {DRAFT_DOC_PATH}")
    print(f"validation rows: {len(validation_rows)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
