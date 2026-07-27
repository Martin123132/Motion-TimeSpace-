from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2994"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2994-Y5-R2FR-parent-Sextra-line-hunt-or-GK-q-loc-source-pack-extraction-under-AX1090.md"

SRC_2993_DOC = ROOT / "2993-Y5-R2FR-parent-extra-sector-source-normal-form-pack-or-first-epsilon-Qv-extra-numeric-row-under-AX1090.md"
SRC_2993_NEXT = RESIDUALS / "P8_Y5_R2FR_2993_NEXT_TARGET.csv"
SRC_2993_PACK = RESIDUALS / "P8_Y5_R2FR_2993_PARENT_EXTRA_SOURCE_PACK_AUDIT.csv"
SRC_2029_DOC = ROOT / "2029-Y5-R2FR-source-SZ-normal-form-and-local-profile-pack.md"
SRC_2030_DOC = ROOT / "2030-Y5-R2FR-parent-object-language-Z-removal-or-SZ-coefficient-acquisition.md"
SRC_2190_DOC = ROOT / "2190-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md"
SRC_2111_DOC = ROOT / "2111-Y5-R2FR-fixed-L0-Khat-metric-response-match-or-Qcdb-bound.md"
SRC_2112_DOC = ROOT / "2112-Y5-R2FR-CDB-component-zero-or-bound-Kconn-Kdomain-Kboundary.md"
SRC_2113_DOC = ROOT / "2113-Y5-R2FR-metric-coframe-LC-parent-signature-or-affine-P4-bound.md"
SRC_2114_DOC = ROOT / "2114-Y5-R2FR-sector-Gamma-slot-audit-or-affine-CMTS-source-pack.md"
SRC_2115_DOC = ROOT / "2115-Y5-R2FR-spin-coframe-owned-connection-guard-or-axial-CMTS-KRT-bound.md"
SRC_2116_DOC = ROOT / "2116-Y5-R2FR-spin-connection-parent-action-signature-or-axial-CMTS-component-source-values.md"
SRC_2117_DOC = ROOT / "2117-Y5-R2FR-canonical-owned-coframe-action-promotion-or-sector-exceptions-ledger.md"
SRC_2118_DOC = ROOT / "2118-Y5-R2FR-source-readout-Gamma-silence-or-explicit-exception-kernels.md"
SRC_2118_NEXT = RESIDUALS / "P8_Y5_PARENT_QLOC_2118_NEXT_TARGET.csv"
SRC_2118_KERNELS = RESIDUALS / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv"
SRC_2118_ACQ = RESIDUALS / "P8_Y5_PARENT_QLOC_2118_ACQUISITION_PRIORITIES.csv"
SRC_2118_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2118_VALIDATION.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2994_SOURCE_REGISTER.csv",
    "sextra": RESIDUALS / "P8_Y5_R2FR_2994_SEXTRA_LINE_HUNT_AUDIT.csv",
    "frontier": RESIDUALS / "P8_Y5_R2FR_2994_GK_FRONTIER_REBASE_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2994_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2994_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2994_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2994_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2994_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "sextra_copy": PARENT_ACTION / "parent_Sextra_line_hunt_2994_NOT_SIGNED.csv",
    "frontier_copy": LOCAL_BOUNDS / "GK_owned_coframe_frontier_rebase_2994_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2994_PROJECTIVE_OR_MICROSCOPE_NEXT_NONCLAIM.csv",
}

for directory in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def add(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, out_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in out_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2994_00_2993_doc", SRC_2993_DOC, ["Current files provide a coherent ansatz", "explicit parent `S_extra/S_Z` line"], "imports 2993 Sextra/GK fork"),
        ("SRC2994_01_2993_next", SRC_2993_NEXT, ["NEXT2993_0_2994", "Gamma/Khat/q_loc source pack"], "imports selected 2994 target"),
        ("SRC2994_02_2993_pack", SRC_2993_PACK, ["PES2993_10_total", "SOURCE_PACK_NOT_SIGNED"], "imports parent extra source-pack failure"),
        ("SRC2994_03_2029_SZ", SRC_2029_DOC, ["No claim-grade current-state source supplies the full `S_Z` birth certificate", "SZR2029_5_verdict"], "strongest S_Z normal-form search result"),
        ("SRC2994_04_2030_Z_removal", SRC_2030_DOC, ["strong theorem target, not a local-GR claim", "Z removal theorem"], "parent object-language Z removal route"),
        ("SRC2994_05_2190_q_loc", SRC_2190_DOC, ["official local-test residual vector", "QLOC_RESIDUAL_LOCK_SELECTED"], "GK/q_loc residual lock start"),
        ("SRC2994_06_2111_Khat", SRC_2111_DOC, ["The live match `K_hat = K_metric[Gamma_eff]` still fails", "CDB_COMPONENTS_NEXT"], "Khat match split"),
        ("SRC2994_07_2112_CDB", SRC_2112_DOC, ["highest-leverage blocker", "CONNECTION_PARENT_SIGNATURE_FIRST"], "CDB component narrowing"),
        ("SRC2994_08_2113_LC", SRC_2113_DOC, ["The mathematics is clean", "sector Gamma-slot audit"], "LC parent-signature fork"),
        ("SRC2994_09_2114_slots", SRC_2114_DOC, ["spin is the highest P4 risk", "SPIN_GUARD_OR_AXIAL_CMTS"], "sector Gamma-slot audit"),
        ("SRC2994_10_2115_spin", SRC_2115_DOC, ["precise coupling contract", "NEXT2115_0_2116"], "spin guard/KRT map"),
        ("SRC2994_11_2116_spin_zero", SRC_2116_DOC, ["first useful leap through the coupling problem", "SIGNED_INSIDE_1963_CANDIDATE_NOT_GLOBAL_CORPUS"], "spin zero inside owned-coframe candidate"),
        ("SRC2994_12_2117_canonical", SRC_2117_DOC, ["spin is lowered", "source/readout Gamma silence"], "canonical owned-coframe promotion blocked by sector exceptions"),
        ("SRC2994_13_2118_source_readout", SRC_2118_DOC, ["source/readout is the wall", "projective-invariance certificate or MICROSCOPE numeric kernel acquisition"], "current source/readout frontier"),
        ("SRC2994_14_2118_next", SRC_2118_NEXT, ["NEXT2118_0_2119", "projective trace"], "current next target"),
        ("SRC2994_15_2118_kernels", SRC_2118_KERNELS, ["KSR2118_0_source_worldtube_kernel", "KSR2118_6_projective_trace_kernel"], "explicit exception kernels"),
        ("SRC2994_16_2118_acquisition", SRC_2118_ACQ, ["MICROSCOPE", "projective"], "acquisition priorities"),
        ("SRC2994_17_2118_validation", SRC_2118_VALIDATION, ["VAL2118_OVERALL", "next target selects projective certificate"], "latest validated frontier"),
    ]
    return [
        add(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "required_anchors": ";".join(needles),
                "exists": path.exists(),
                "anchors_found": anchors(path, needles),
            }
        )
        for source_id, path, needles, role in specs
    ]


def sextra_rows() -> list[dict[str, Any]]:
    data = [
        (
            "SXH2994_0_2993_parent_pack",
            "global S_extra/S_Z parent source-normal-form pack",
            "NOT_SIGNED",
            "2993 says the corpus has ansatz/theorem scaffolding but not a signed parent package",
            "epsilon_Qv_extra_piece_total_abs remains live",
        ),
        (
            "SXH2994_1_2029_SZ_birth_certificate",
            "physical S_Z finite-field birth certificate",
            "NOT_FOUND_CLAIM_GRADE",
            "2029 states no claim-grade source supplies K0,V0,Vprime0,mZ2,A_Z,Q_Z and no-source-slot",
            "do not use canonical S_Z double-zero as current proof",
        ),
        (
            "SXH2994_2_2030_object_language",
            "Z removed by parent object-language/constraint/auxiliary route",
            "THEOREM_TARGET_NOT_GLOBAL_CLAIM",
            "2030 says the clean route is precise but category principle is not derived",
            "retain as exact route, not current promotion",
        ),
        (
            "SXH2994_3_direct_line_hunt_verdict",
            "explicit parent S_extra/S_Z action line and field normalization",
            "NO_PROMOTABLE_LINE_FOUND_IN_CURRENT_FRONTIER",
            "candidate expressions are nonclaim ansatz/prototype/queue rows",
            "pivot to concrete GK/owned-coframe frontier instead of replaying Sextra search",
        ),
    ]
    return [
        add(
            {
                "hunt_id": hunt_id,
                "target": target,
                "current_status": status,
                "evidence": evidence,
                "consequence": consequence,
                "promotable_now": False,
            }
        )
        for hunt_id, target, status, evidence, consequence in data
    ]


def frontier_rows() -> list[dict[str, Any]]:
    data = [
        (
            "GKF2994_0_q_loc_lock",
            "Gamma/Khat/q_loc residual lock",
            "q_loc made official residual vector instead of silent zero",
            "2190",
            "local-test residual interface exact, theorem-zero not closed",
        ),
        (
            "GKF2994_1_Khat_match",
            "K_hat metric-response split",
            "algebraic fixed-L0 pieces no longer main blocker; CDB/projector/boundary remain",
            "2111",
            "local obstruction became componentized",
        ),
        (
            "GKF2994_2_CDB_components",
            "CDB/projector/boundary decomposition",
            "narrow boundary/postprocess sublemmas import, K_conn becomes highest leverage",
            "2112",
            "connection ontology became the next exact gate",
        ),
        (
            "GKF2994_3_LC_parent_signature",
            "metric/coframe LC branch",
            "LC theorem exact if Gamma_MTS absent or LC[g_obs], but sector slots unsigned",
            "2113",
            "connection zero route becomes parent object-language question",
        ),
        (
            "GKF2994_4_sector_Gamma_slots",
            "all-sector Gamma-slot audit",
            "spin highest risk; ordinary/source/readout/boundary/projective slots remain unsigned",
            "2114",
            "C_MTS/P4 fallback retained",
        ),
        (
            "GKF2994_5_spin_coupling",
            "spin coupling signature",
            "spin has exact coframe-owned zero route but needed parent action signature",
            "2115",
            "coupling wall localized to action arguments",
        ),
        (
            "GKF2994_6_spin_branch_zero",
            "owned-coframe candidate spin closure",
            "inside the 1963 candidate branch xi_A=0 and A_MTS=0 by variable absence",
            "2116",
            "real progress; not global/canonical yet",
        ),
        (
            "GKF2994_7_canonical_promotion",
            "owned-coframe canonicalization",
            "spin lowered; canonical promotion blocked by EM/source/clock/light/orbit/boundary/projective exceptions",
            "2117",
            "do not poke spin again; attack source/readout exceptions",
        ),
        (
            "GKF2994_8_current_frontier",
            "source/readout Gamma silence",
            "source/readout zero clauses are conditional; explicit exception kernels staged",
            "2118",
            "next fork is projective invariance certificate or MICROSCOPE numeric kernel acquisition",
        ),
    ]
    return [
        add(
            {
                "frontier_id": frontier_id,
                "stage": stage,
                "result": result,
                "source_checkpoint": checkpoint,
                "meaning_for_GR_route": meaning,
                "claim_allowed_now": False,
            }
        )
        for frontier_id, stage, result, checkpoint, meaning in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE2994_0_direct_Sextra", "explicit parent S_extra/S_Z source line is promotable", False, "NO_PROMOTABLE_LINE_FOUND"),
        ("GATE2994_1_SZ_birth", "physical finite S_Z birth certificate exists", False, "2029_NONCLAIM"),
        ("GATE2994_2_object_language", "Z/extra field removal theorem is global", False, "2030_CONDITIONAL"),
        ("GATE2994_3_spin_progress", "spin coupling lowered inside owned-coframe candidate", True, "2116_CANDIDATE_BRANCH_PASS"),
        ("GATE2994_4_owned_coframe_global", "1963 owned-coframe branch is canonical/global", False, "2117_SECTOR_EXCEPTIONS"),
        ("GATE2994_5_source_readout_zero", "source/readout Gamma silence closes", False, "2118_CONDITIONAL_ONLY"),
        ("GATE2994_6_exception_kernels_score", "exception kernels are numeric/source-backed", False, "KERNELS_SHAPE_ONLY"),
        ("GATE2994_7_local_GR_Newton", "local GR/Newton reduction follows", False, "NO_PROMOTION_FROM_2994"),
    ]
    return [
        add(
            {
                "gate_id": gate_id,
                "gate": gate,
                "condition_passed": passed,
                "status": status,
                "promotion_allowed_now": False,
            }
        )
        for gate_id, gate, passed, status in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC2994_0_direct_Sextra_result",
            "Do not continue broad S_extra line hunting as the main path.",
            "The strongest current S_Z/S_extra files are nonclaim ansatz/prototype/queue rows, while the GK branch has a much sharper frontier.",
            "use S_extra hunt as a blocker ledger, not an active promotion route",
        ),
        (
            "DEC2994_1_real_progress",
            "Credit the owned-coframe/spin result as real conditional progress.",
            "2116 derives xi_A=0 and A_MTS=0 inside the 1963 owned-coframe candidate branch by variable absence, which is stronger than a small fitted torsion number.",
            "promote nothing globally, but carry this as branch-zero evidence if 1963 becomes canonical",
        ),
        (
            "DEC2994_2_frontier",
            "Rebase the 299x parent-extra route onto the 2118 frontier.",
            "Current blocker is source/readout Gamma silence or explicit numeric exception kernels, not generic double-zero or spin.",
            "next checkpoint should choose projective-invariance certificate first, with MICROSCOPE numeric kernel as empirical fallback",
        ),
    ]
    return [
        add({"decision_id": decision_id, "decision": decision, "because": because, "next_action": next_action})
        for decision_id, decision, because, next_action in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2994_0_2995",
                "priority": "selected_primary",
                "next_doc": "2995-Y5-R2FR-projective-invariance-certificate-first-or-MICROSCOPE-kernel-acquisition-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_projective_invariance_certificate_first_or_MICROSCOPE_kernel_acquisition_under_AX1090_2995.py",
                "objective": "Attempt the lower-scrutiny derivation route first: prove the projective trace is gauge/unobservable across the owned-coframe/source/readout sectors. If it fails, acquire or stage the MICROSCOPE orbit/source numeric kernel inputs needed by the explicit exception-kernel lane.",
                "include": "2118 projective trace kernel;source/readout zero clauses;owned-coframe candidate branch;MICROSCOPE orbit/source kernel;no-cancellation residual queue",
                "exclude": "generic S_extra re-hunt;spin re-litigation;local-GR claim;Newton claim;PPN/WEP pass;using kernel skeleton as data;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_files = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    checks = [
        ("VAL2994_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2994_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2994_2_Sextra_not_promoted", all(not row["promotable_now"] for row in all_rows["sextra"]), "direct S_extra line hunt is not promoted", True),
        ("VAL2994_3_frontier_rebased", any(row["frontier_id"] == "GKF2994_8_current_frontier" and "2118" in row["source_checkpoint"] for row in all_rows["frontier"]), "frontier rebased to 2118 source/readout fork", True),
        ("VAL2994_4_spin_progress_recorded", any(row["frontier_id"] == "GKF2994_6_spin_branch_zero" for row in all_rows["frontier"]), "spin candidate-branch zero progress recorded", True),
        ("VAL2994_5_no_promotion", all(not row["promotion_allowed_now"] for row in all_rows["gates"]), "no local-GR/Newton promotion allowed", True),
        ("VAL2994_6_next_written", len(all_rows["next"]) == 1 and all_rows["next"][0]["next_id"] == "NEXT2994_0_2995", "2995 next target written", True),
        ("VAL2994_7_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2994_8_csvs_parse", all(csv_ok(path) for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"), "all generated CSVs parse", True),
        ("VAL2994_9_outputs_under_post", all(under(path, ROOT) for path in output_files), "all generated outputs under post-checkpoint-work", True),
        ("VAL2994_10_formalization_clean", len(list(FORMALIZATION.rglob("*2994*"))) == 0 if FORMALIZATION.exists() else True, f"no 2994 outputs in formalization-workbench (count={len(list(FORMALIZATION.rglob('*2994*'))) if FORMALIZATION.exists() else 0})", True),
        ("VAL2994_11_doc_written", DOC.exists(), "2994 markdown checkpoint exists", True),
    ]
    out = [
        add({"validation_id": validation_id, "passed": bool(passed), "check": check, "required": required})
        for validation_id, passed, check, required in checks
    ]
    out.append(add({"validation_id": "VAL2994_OVERALL", "passed": all(row["passed"] for row in out), "check": "2994 validation overall", "required": True}))
    return out


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(out_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in out_rows]
    return "\n".join([header, sep, *body])


def output_rows() -> list[dict[str, Any]]:
    return [{"output": key, "path": str(path), "exists": path.exists()} for key, path in OUTPUTS.items() if key != "validation"]


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2994 - Parent Sextra Line Hunt or GK/q_loc Source-Pack Extraction

Status: `Y5_R2FR_2994_direct_Sextra_not_promoted_GK_frontier_rebased_to_source_readout_projective_or_MICROSCOPE_fork_nonclaim`

Claim ceiling: `no_parent_Sextra_claim_no_owned_coframe_global_claim_no_source_readout_zero_claim_no_projective_claim_no_MICROSCOPE_claim_no_local_GR_no_Newton_no_PPN_no_WEP_no_public_claim`

## Summary

- Direct `S_extra/S_Z` hunting still does not produce a promotable parent action line. The strongest `S_Z` files remain nonclaim birth-certificate or object-language routes.
- The concrete GK/q_loc route is better than the broad `S_extra` route now: it has advanced through Khat response, CDB, LC ontology, sector Gamma slots, and spin coupling.
- Real progress exists: inside the 1963 owned-coframe candidate branch, spin/axial coupling is zero by variable absence rather than by small fitted number.
- The current frontier is 2118: source/readout Gamma silence, projective trace, or explicit MICROSCOPE/source-readout exception kernels.

## Generated Outputs

{table(output_rows(), ["output", "path", "exists"])}

## Branch Copies

{table(all_rows["branches"], ["copy", "path", "exists"])}

## Source Register

{table(all_rows["sources"], ["source_id", "role", "exists", "anchors_found"])}

## Sextra Line Hunt Audit

{table(all_rows["sextra"], ["hunt_id", "target", "current_status", "consequence"])}

## GK Frontier Rebase Ledger

{table(all_rows["frontier"], ["frontier_id", "stage", "result", "source_checkpoint", "meaning_for_GR_route"])}

## Promotion Gates

{table(all_rows["gates"], ["gate_id", "gate", "condition_passed", "status", "promotion_allowed_now"])}

## Decision Ledger

{table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
""",
        encoding="utf-8",
    )


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(),
        "sextra": sextra_rows(),
        "frontier": frontier_rows(),
        "gates": gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["sextra"], BRANCH_OUTPUTS["sextra_copy"])
    shutil.copyfile(OUTPUTS["frontier"], BRANCH_OUTPUTS["frontier_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    print(f"2994 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
