from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3743"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_PHIS_PROJECTOR_OR_ETA_ZERO_THEOREM_3743"
DOC = ROOT / "3743-Y5-R2FR-local-PhiS-projector-or-eta-zero-theorem.md"

DOC_3742 = ROOT / "3742-Y5-R2FR-local-S-budget-gate-etaPhi2-gradK-bound.md"
NEXT_3742 = RESIDUALS / "P8_Y5_R2FR_3742_NEXT_TARGET.csv"
VALIDATION_3742 = RESIDUALS / "P8_Y5_BRR545_3742_VALIDATION.csv"
PHIS_CONDITIONS_3742 = RESIDUALS / "P8_Y5_R2FR_3742_PhiS_ZERO_OR_BOUND_CONDITIONS.csv"
CLAIM_GATES_3742 = RESIDUALS / "P8_Y5_R2FR_3742_CLAIM_GATES.csv"
MTS_GRAVITY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
RED_TEAM = FORMALIZATION / "06-consistency-red-team.md"
SPINE = FORMALIZATION / "07-unification-spine.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def read_lines(path: Path) -> list[str]:
    return read_text(path).splitlines()


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def find_line(path: Path, needle: str) -> tuple[int, str]:
    for line_number, line in enumerate(read_lines(path), start=1):
        if needle in line:
            return line_number, line.strip()
    return 0, ""


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3742", DOC_3742, "Phi_S Zero-or-Bound Routes", "3742 theorem handoff"),
        ("next_3742", NEXT_3742, "3743-Y5-R2FR-local-PhiS-projector-or-eta-zero-theorem.md", "3742 next target"),
        ("validation_3742", VALIDATION_3742, "next_target_3743", "3742 validation"),
        ("phis_conditions_3742", PHIS_CONDITIONS_3742, "P_loc Phi_S=0", "3742 open theorem target"),
        ("claim_gates_3742", CLAIM_GATES_3742, "CG3742_4_phi", "3742 phi gate"),
        ("gravity_phi", MTS_GRAVITY, "Φ  = |∇κ|", "raw Phi_S definition"),
        ("gravity_phi_term", MTS_GRAVITY, "+ η Φ²", "raw eta Phi term"),
        ("gravity_flrw", MTS_GRAVITY, "Φ = 0", "homogeneous branch zero statement"),
        ("redteam_projector_cheat", RED_TEAM, "P_loc, P_gal, and P_cos could become arbitrary sector switches.", "projector anti-cheat warning"),
        ("redteam_projector_definition", RED_TEAM, "P_loc = Pi_B + (1 - Pi_B)(1 - C_cos)(1 - T_gal)", "existing projector toy definition"),
        ("redteam_plateau", RED_TEAM, "Do not hide a new plateau axiom inside the word \"therefore\".", "plateau anti-smuggling warning"),
        ("spine_projector", SPINE, "exact cancellation/projector theorem", "projector theorem route summary"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        line_number, line_text = find_line(path, needle) if exists else (0, "")
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "line_number": line_number,
            "line_text": line_text,
            "role": role,
            "claim_allowed": False,
        })
    return rows


def theorem_attempt_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("ATT3743_0_eta_zero", "eta=0", "Would remove eta*Phi_S^2 from S_epsilon.", "FAIL_CURRENT_CORPUS", "No source-owned eta=0 line or parent variational reason found."),
        ("ATT3743_1_phi_zero", "Phi_S=0 in local weak-field/vacuum", "Would set the curvature-tension morphology contribution to zero.", "FAIL_LOCAL_INHERITANCE", "Corpus has Phi=0 in homogeneous FLRW, not in Solar/local non-homogeneous weak-field branch."),
        ("ATT3743_2_projector_kernel", "P_loc Phi_S=0", "Would project the morphology term out of local PPN observables.", "FAIL_PARENT_PROOF", "Existing projector material is a toy/repair route and red-team warns against arbitrary sector switches."),
        ("ATT3743_3_numeric_bound", "|eta| Phi_S,D^2 below PPN tolerance", "Would keep raw S ansatz but source a finite small morphology term.", "FAIL_NUMERIC_SOURCE", "No eta value, Phi_S local norm, or PPN tolerance/operator constant package is source-owned here."),
        ("ATT3743_4_modified_S", "local-safe S functional with projector/quarantine", "Would replace raw local S by S_loc=K^m+gradK plus a nonlocal/morphology sector projector.", "REPAIR_ROUTE_AVAILABLE_NOT_PARENT_DERIVED", "This is a clean closure repair if explicitly labeled; it is not yet a parent theorem."),
    ]
    return [
        {
            **base(timestamp),
            "attempt_id": attempt_id,
            "route": route,
            "would_do": would_do,
            "verdict": verdict,
            "reason": reason,
            "claim_allowed": False,
        }
        for attempt_id, route, would_do, verdict, reason in specs
    ]


def projector_contract_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("PCON3743_0_universal_selector", "universal selector", "P_loc must be a fixed function of parent invariants, not dataset labels or arena names.", "REQUIRED_NOT_PROVED"),
        ("PCON3743_1_kernel", "kernel condition", "P_loc(Phi_S^2 contribution)=0 or ||P_loc Phi_S|| below tolerance.", "REQUIRED_NOT_PROVED"),
        ("PCON3743_2_covariance", "covariance", "P_loc must commute with the local gauge/covariant derivative structure enough to preserve Bianchi/conservation.", "REQUIRED_NOT_PROVED"),
        ("PCON3743_3_branch_separation", "branch separation", "Projecting Phi_S out locally must not erase the galaxy/cosmology morphology evidence by hand.", "REQUIRED_NOT_PROVED"),
        ("PCON3743_4_boundary", "boundary and transition control", "The projector must not reintroduce boundary/support residuals larger than the killed Phi_S term.", "REQUIRED_NOT_PROVED"),
        ("PCON3743_5_parent_origin", "parent origin", "The projector/quarantine must follow from parent action, quotient, or variational kernel, not from a post-hoc fit.", "REQUIRED_NOT_PROVED"),
    ]
    return [
        {
            **base(timestamp),
            "contract_id": contract_id,
            "clause": clause,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
        }
        for contract_id, clause, requirement, status in specs
    ]


def local_safe_s_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("LS3743_0_raw_S", "raw current S", "S_raw = K^m/(1+K^m) + ell^2(nablaK)^2/(1+K^m) + eta Phi_S^2", "LOCAL_PPN_UNSAFE_UNLESS_PHI_GATE_CLOSED", "This is the actual corpus ansatz and remains blocked locally."),
        ("LS3743_1_projected_S", "projected closure repair", "S_loc = K^m/(1+K^m) + ell^2(nablaK)^2/(1+K^m) + P_nonloc eta Phi_S^2 with P_loc P_nonloc=0", "CLOSURE_REPAIR_CONTRACT", "Viable as explicit closure if projector contract is satisfied."),
        ("LS3743_2_eta_zero_S", "eta-zero repair", "S_loc = K^m/(1+K^m) + ell^2(nablaK)^2/(1+K^m), eta_local=0", "CLOSURE_REPAIR_CONTRACT", "Viable if eta_local=0 is made a theorem or an explicit local closure assumption."),
        ("LS3743_3_numeric_S", "numeric-bound repair", "S_loc = S_raw with |eta|Phi_S,D^2 <= epsilon_tol", "EMPIRICAL_REPAIR_CONTRACT", "Viable only after source-owned eta, Phi_S profile, and tolerance constants exist."),
    ]
    return [
        {
            **base(timestamp),
            "s_id": s_id,
            "route": route,
            "formula": formula,
            "status": status,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for s_id, route, formula, status, meaning in specs
    ]


def demotion_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEM3743_0_raw_local_pass", "raw S local PPN pass", "DEMOTED", "Because eta*Phi_S^2 is retained and not bounded/killed."),
        ("DEM3743_1_Km_only_argument", "K^m-only solar suppression argument", "DEMOTED", "Because it ignores gradK, Phi_S, boundary, and operator constants."),
        ("DEM3743_2_parent_projector_proof", "parent projector proof", "NOT_DERIVED", "Existing projector notes are warnings/contracts, not a parent proof."),
        ("DEM3743_3_closure_branch", "calibrated-GR closure branch", "CONDITIONAL_KEEP", "Still viable if explicitly modified/projected or if eta/Phi_S receives a real bound."),
    ]
    return [
        {
            **base(timestamp),
            "demotion_id": demotion_id,
            "item": item,
            "verdict": verdict,
            "reason": reason,
            "claim_allowed": False,
        }
        for demotion_id, item, verdict, reason in specs
    ]


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("THM3743_0_eta_zero_fail", "FAILED_THEOREM_ATTEMPT", "eta=0 is not derived in the current corpus.", "Do not silently delete the morphology term."),
        ("THM3743_1_projector_fail", "FAILED_PARENT_PROJECTOR_ATTEMPT", "P_loc Phi_S=0 is not parent-derived; existing projector material is a repair contract with cheat warnings.", "Do not treat sector routing as proof."),
        ("THM3743_2_raw_S_unsafe", "LOCAL_PPN_SAFETY_DEMOTION", "The raw S functional is local-PPN unsafe unless eta*Phi_S^2 is killed or bounded.", "This is the honest current state."),
        ("THM3743_3_repair_contract", "REPAIR_CONTRACT_READY", "A local-safe S branch can be pursued only as explicit projected/eta-zero/numeric-bound closure.", "This preserves the route without pretending it is already derived."),
        ("THM3743_4_claim_gate", "ANTI_OVERCLAIM", "No local-GR/Newton/PPN claim follows from 3743.", "The goal stays active."),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "status": status,
            "clause": clause,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for theorem_id, status, clause, meaning in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3743_0_sources", "projector/eta theorem sources registered", True, "all source needles found"),
        ("CG3743_1_eta_zero", "eta=0 proved", False, "no parent/source proof found"),
        ("CG3743_2_phi_zero", "Phi_S=0 local theorem proved", False, "FLRW zero does not imply local weak-field zero"),
        ("CG3743_3_projector", "P_loc Phi_S=0 parent-derived", False, "projector route is not parent-owned"),
        ("CG3743_4_numeric", "eta Phi_S numeric bound sourced", False, "eta/Phi/tolerance inputs missing"),
        ("CG3743_5_repair", "local-safe S repair contract staged", True, "projected/eta-zero/numeric closure alternatives emitted"),
        ("CG3743_6_local_claim", "local GR/Newton/PPN pass claim allowed", False, "raw S remains unsafe and repair is not yet proven"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, rationale in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3743_0_result", "PHIS_THEOREM_ATTEMPT_FAILED_CLEANLY", "eta=0, Phi_S=0, and P_loc Phi_S=0 are not currently derivable from the sourced corpus."),
        ("DEC3743_1_demote", "RAW_S_LOCAL_PPN_BRANCH_DEMOTED", "The raw S ansatz cannot be treated as local-safe until the morphology term is killed or bounded."),
        ("DEC3743_2_keep_route", "CLOSURE_ROUTE_KEPT_AS_EXPLICIT_REPAIR", "A projected or eta-zero local-safe S branch can still be built if marked as closure and then tested."),
        ("DEC3743_3_next", "NEXT_BUILD_EXPLICIT_LOCAL_SAFE_S_CLOSURE_AND_TEST_STUB", "The next useful move is to write the local-safe S closure variant and a tiny symbolic/numeric gate for PPN tolerances."),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "status_id": "STATUS3743_0",
        "status": "RAW_S_LOCAL_PPN_UNSAFE_REPAIR_CONTRACT_REQUIRED",
        "summary": "3743 fails to derive eta=0 or P_loc Phi_S=0; the raw S functional is demoted as local-PPN unsafe unless a projected/eta-zero/numeric-bound local-safe closure is explicitly added and tested.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3743_0",
        "target_doc": "3744-Y5-R2FR-local-safe-S-closure-variant-and-PPN-test-stub.md",
        "target_script": "scripts/Y5_R2FR_3744_local_safe_S_closure_variant_and_PPN_test_stub.py",
        "objective": "construct an explicit nonclaim local-safe S closure variant with projected/eta-zero/numeric-bound branches and a small PPN tolerance test stub, keeping the raw S branch demoted",
        "success_gate": "the closure variant can compute symbolic S_epsilon and refuses local claims unless K, gradK, Phi_S, boundary, and operator constants pass supplied tolerances",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3743 - Local Phi_S Projector or eta-Zero Theorem",
        "",
        "## Status",
        "- `RAW_S_LOCAL_PPN_UNSAFE_REPAIR_CONTRACT_REQUIRED`",
        "- The theorem attempt failed cleanly: no source-owned `eta=0`, local `Phi_S=0`, or parent-derived `P_loc Phi_S=0` exists.",
        "- The raw `S` ansatz is demoted for local PPN until a projected, eta-zero, or numeric-bound local-safe closure is explicitly added.",
        "",
        "## Theorem Attempts",
    ]
    for row in grouped["attempts"]:
        lines.append(f"- `{row['attempt_id']}` `{row['verdict']}`: {row['route']} | {row['reason']}")
    lines.extend(["", "## Projector Contract"])
    for row in grouped["projector_contract"]:
        lines.append(f"- `{row['contract_id']}` `{row['status']}`: {row['clause']} | {row['requirement']}")
    lines.extend(["", "## Local-Safe S Options"])
    for row in grouped["local_safe_s"]:
        lines.append(f"- `{row['s_id']}` `{row['status']}`: {row['formula']} | {row['meaning']}")
    lines.extend(["", "## Demotions"])
    for row in grouped["demotions"]:
        lines.append(f"- `{row['demotion_id']}` `{row['verdict']}`: {row['item']} | {row['reason']}")
    lines.extend(["", "## Theorem Rows"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['clause']} | {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Next Target"])
    next_row = grouped["next_target"][0]
    lines.append(f"- `{next_row['target_doc']}`")
    lines.append(f"- Objective: {next_row['objective']}")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def validation_rows(timestamp: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    attempts = parse_csv(paths["attempts"])
    projector_contract = parse_csv(paths["projector_contract"])
    local_safe_s = parse_csv(paths["local_safe_s"])
    demotions = parse_csv(paths["demotions"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3743*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("attempts", "five theorem attempts recorded", len(attempts) == 5 and all(token in read_text(paths["attempts"]) for token in ["FAIL_CURRENT_CORPUS", "FAIL_PARENT_PROOF", "REPAIR_ROUTE_AVAILABLE_NOT_PARENT_DERIVED"])),
        ("projector_contract", "projector contract clauses present", len(projector_contract) == 6 and all(token in read_text(paths["projector_contract"]) for token in ["universal selector", "kernel condition", "parent origin"])),
        ("local_safe_s", "local-safe S repair options present", len(local_safe_s) == 4 and "P_loc P_nonloc=0" in read_text(paths["local_safe_s"])),
        ("demotions", "raw S local pass demoted", len(demotions) == 4 and any(row["item"] == "raw S local PPN pass" and row["verdict"] == "DEMOTED" for row in demotions)),
        ("claim_gates_block", "local claim remains blocked", any(row["gate_id"] == "CG3743_6_local_claim" and row["passed"] == "False" for row in claim_gates)),
        ("repair_staged", "repair contract staged", any(row["gate_id"] == "CG3743_5_repair" and row["passed"] == "True" for row in claim_gates)),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("next_target_3744", "next target is local-safe S closure test stub", next_target[0]["target_doc"] == "3744-Y5-R2FR-local-safe-S-closure-variant-and-PPN-test-stub.md"),
        ("doc_core_terms", "doc contains unsafe raw S and repair contract", all(token in read_text(paths["doc"]) for token in ["RAW_S_LOCAL_PPN_UNSAFE", "eta=0", "P_loc Phi_S=0", "local-safe closure"])),
        ("no_formalization_leak", "no 3743 files in formalization-workbench", len(formalization_leaks) == 0),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def main() -> None:
    timestamp = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3743_SOURCE_REGISTER.csv",
        "attempts": RESIDUALS / "P8_Y5_R2FR_3743_THEOREM_ATTEMPT_ROWS.csv",
        "projector_contract": RESIDUALS / "P8_Y5_R2FR_3743_PROJECTOR_CONTRACT_ROWS.csv",
        "local_safe_s": RESIDUALS / "P8_Y5_R2FR_3743_LOCAL_SAFE_S_OPTIONS.csv",
        "demotions": RESIDUALS / "P8_Y5_R2FR_3743_DEMOTION_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3743_THEOREM_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3743_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3743_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3743_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3743_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3743_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(timestamp),
        "attempts": theorem_attempt_rows(timestamp),
        "projector_contract": projector_contract_rows(timestamp),
        "local_safe_s": local_safe_s_rows(timestamp),
        "demotions": demotion_rows(timestamp),
        "theorems": theorem_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "status": status_rows(timestamp),
        "next_target": next_target_rows(timestamp),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(timestamp, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3743 validation failed: {failures}")
    print("wrote 3743 checkpoint: raw S local PPN branch demoted; local-safe repair contract staged")


if __name__ == "__main__":
    main()
