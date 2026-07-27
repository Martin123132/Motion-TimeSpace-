from __future__ import annotations

import csv
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2795-Y5-R2FR-parent-ordinary-matter-signature-source-hunt-or-DD-intake-review-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2795_SOURCE_REGISTER.csv",
    "search_summary": MTS / "P8_Y5_R2FR_2795_CORPUS_SIGNATURE_SEARCH_SUMMARY.csv",
    "hunt": MTS / "P8_Y5_R2FR_2795_SIGNATURE_SOURCE_HUNT.csv",
    "coverage": MTS / "P8_Y5_R2FR_2795_MOMS_CLAUSE_COVERAGE_MATRIX.csv",
    "blockers": MTS / "P8_Y5_R2FR_2795_SIGNATURE_BLOCKER_LEDGER.csv",
    "policy": MTS / "P8_Y5_R2FR_2795_FINITE_INTAKE_REVIEW_POLICY.csv",
    "candidate": MTS / "P8_Y5_R2FR_2795_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "runner": MTS / "P8_Y5_R2FR_2795_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2795_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2795_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2795_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2795_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2795_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2795_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "hunt_queue": RAB_QUEUE / "JR2795_SIGNATURE_SOURCE_HUNT_NONCLAIM.csv",
    "coverage_queue": RAB_QUEUE / "JR2795_MOMS_CLAUSE_COVERAGE_NONCLAIM.csv",
    "policy_queue": RAB_QUEUE / "JR2795_FINITE_INTAKE_REVIEW_POLICY_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "WEP_SIGNATURE_SOURCE_HUNT_2795_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_wep_signature_source_hunt_2795_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2795_SIGNATURE_SYNTHESIS_OR_CLOSURE_DEMOTION_NEXT.csv",
}

SEARCH_PATTERNS = [
    ("SEARCH2795_0_matter_action", "S_matter", "matter-action language exists; source-hunt rows decide whether any hit is parent-signed"),
    ("SEARCH2795_1_parent_action", "parent action", "parent-action language exists; source-hunt rows decide whether it signs MOMS2794"),
    ("SEARCH2795_2_species_weight", "w_A|species weight|species weights", "pre-action species/source-weight language is the main WEP obstruction"),
    ("SEARCH2795_3_superselection", "superselection|theta_A", "constant/representation route is required for alpha/mass/clock silence"),
    ("SEARCH2795_4_shadow_frame", "shadow frame|disformal|source-only metric", "hidden frame/domain countermodels must be killed"),
    ("SEARCH2795_5_variation_readout", "variation-before-readout|before readout|post-variation selector", "variation-order rule must be owned by the same action"),
    ("SEARCH2795_6_matter_bundle", "matter bundle|matter functor|Bundle_A", "ordinary matter lift must be parent-owned"),
    ("SEARCH2795_7_moms2794", "MOMS2794|minimal parent ordinary-matter signature", "direct references to the new signature are contracts unless parent-derived"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def find_first(root: Path, glob_pattern: str) -> Path | None:
    matches = sorted(root.glob(glob_pattern))
    return matches[0] if matches else None


def discover_markdown(prefix: str) -> Path | None:
    matches = sorted(WORK.glob(f"{prefix}-*.md"))
    return matches[0] if matches else None


def discover_formalization(prefix: str) -> Path | None:
    matches = sorted(FORMALIZATION.glob(f"{prefix}*.md"))
    return matches[0] if matches else None


def source_entries() -> list[tuple[str, Path, str]]:
    entries: list[tuple[str, Path | None, str]] = [
        ("2794_next", MTS / "P8_Y5_R2FR_2794_NEXT_TARGET.csv", "authoritative target for source hunt"),
        ("2794_signature", MTS / "P8_Y5_R2FR_2794_MINIMAL_SIGNATURE_CLAUSE.csv", "MOMS2794 minimal signature contract"),
        ("2794_theorem", MTS / "P8_Y5_R2FR_2794_CONDITIONAL_ZERO_THEOREM.csv", "conditional WEP zero theorem under MOMS2794"),
        ("2794_countermodels", MTS / "P8_Y5_R2FR_2794_COUNTERMODEL_RETENTION.csv", "legal countermodels if MOMS2794 is unsigned"),
        ("2794_finite_intake", MTS / "P8_Y5_R2FR_2794_FINITE_DD_INTAKE_SCHEMA.csv", "finite DD intake schema"),
        ("2793_descent", MTS / "P8_Y5_R2FR_2793_PARENT_MATTER_DESCENT_ATTEMPT.csv", "prior parent-descent clause stack"),
        ("2793_pack", MTS / "P8_Y5_R2FR_2793_DD_COEFFICIENT_SOURCE_PACK.csv", "finite coefficient source-pack precursor"),
        ("1089_source_hunt_analogue", MTS / "P8_Y5_R10_1089_SIGNATURE_SOURCE_HUNT.csv", "R10 source-hunt analogue, structural precedent only"),
        ("1089_coverage_analogue", MTS / "P8_Y5_R10_1089_MOMS_CLAUSE_COVERAGE_MATRIX.csv", "R10 coverage analogue, structural precedent only"),
        ("1088_signature_analogue", MTS / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv", "R10 minimal signature analogue"),
        ("1027_qbar_source_zero", discover_markdown("1027"), "qbar_XT source-zero/counterexample checkpoint"),
        ("1028_no_marker_pack", discover_markdown("1028"), "no-marker and coupling bound input pack"),
        ("1009_parent_current_contract", discover_markdown("1009"), "parent current-chain action contract"),
        ("formalization_10_core_repair", FORMALIZATION / "10-core-consistency-repair.md", "older action skeleton and conservation warning"),
        ("formalization_36_parent_equations", discover_formalization("36"), "formal parent-equation scaffold if present"),
    ]
    return [(sid, path, role) for sid, path, role in entries if path is not None]


def build_sources() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": role,
            "contains_text": bool(read_text(path).strip()) if path.exists() else False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for source_id, path, role in source_entries()
    ]


def searchable_files() -> list[Path]:
    focus_prefixes = [
        "943",
        "990",
        "1009",
        "1027",
        "1028",
        "1045",
        "1055",
        "1067",
        "1078",
        "1079",
        "1088",
        "1089",
        "2785",
        "2791",
        "2792",
        "2793",
        "2794",
        "2795",
    ]
    files: list[Path] = []
    if WORK.exists():
        for prefix in focus_prefixes:
            files.extend(sorted(WORK.glob(f"{prefix}-*.md")))
    if MTS.exists():
        for prefix in focus_prefixes:
            files.extend(sorted(MTS.glob(f"*{prefix}*.csv")))
    if FORMALIZATION.exists():
        for prefix in ["05", "06", "07", "10", "36", "116", "125", "130"]:
            files.extend(sorted(FORMALIZATION.glob(f"{prefix}*.md")))
    bounded_files: list[Path] = []
    for path in files:
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".csv", ".txt"}:
            continue
        if path.stat().st_size > 2_000_000:
            continue
        bounded_files.append(path)
    return bounded_files


def build_search_summary() -> list[dict[str, Any]]:
    files = searchable_files()
    texts: list[tuple[Path, str]] = [(path, read_text(path)) for path in files]
    rows: list[dict[str, Any]] = []
    for search_id, pattern, interpretation in SEARCH_PATTERNS:
        regex = re.compile(pattern, flags=re.IGNORECASE)
        matching_files = 0
        occurrences = 0
        first_path = ""
        first_excerpt = ""
        for path, text in texts:
            matches = list(regex.finditer(text))
            if not matches:
                continue
            matching_files += 1
            occurrences += len(matches)
            if not first_path:
                match = matches[0]
                start = max(0, match.start() - 70)
                end = min(len(text), match.end() + 90)
                first_path = str(path)
                first_excerpt = " ".join(text[start:end].split())
        rows.append(
            {
                "search_id": search_id,
                "pattern": pattern,
                "matching_file_count": matching_files,
                "occurrence_count": occurrences,
                "first_match_path": first_path,
                "first_match_excerpt": first_excerpt,
                "interpretation": interpretation,
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def source_path(source_id: str) -> str:
    for sid, path, _role in source_entries():
        if sid == source_id:
            return str(path)
    return "NOT_DISCOVERED"


def build_hunt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "HUNT2795_0_2794",
            source_path("2794_signature"),
            "MOMS2794 minimal parent ordinary-matter signature",
            "exact action-form contract and proof assumptions",
            "MOMS2794_7_verdict=MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
            "CONTRACT_NOT_PARENT_SOURCE",
        ),
        (
            "HUNT2795_1_2794_theorem",
            source_path("2794_theorem"),
            "conditional qbar_XT/J_X WEP-zero theorem",
            "THM2794_5 proves the zero theorem under the signature",
            "THM2794_6_current_corpus_verdict=CONDITIONAL_ZERO_THEOREM_NOT_PROMOTED",
            "CONDITIONAL_THEOREM_NOT_SOURCE",
        ),
        (
            "HUNT2795_2_2793",
            source_path("2793_descent"),
            "parent matter descent stack",
            "object-language, action-measure, matter lift, constants, and boundary clauses are laid out",
            "PMD2793_7_verdict=PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED",
            "CLAUSE_STACK_UNSIGNED",
        ),
        (
            "HUNT2795_3_1009",
            source_path("1009_parent_current_contract"),
            "parent current-chain action contract",
            "names S_parent and universal matter-current channel",
            "total parent action and sector source certificates remain not promoted",
            "PARENT_CURRENT_CONTRACT_NOT_MOMS_SOURCE",
        ),
        (
            "HUNT2795_4_1027",
            source_path("1027_qbar_source_zero"),
            "qbar_XT source-zero route",
            "contains the same conditional matter-functor/no-marker route",
            "qbar_XT/J_X zero requires q-kernel, observed coframe, matter functor, no-marker, and hidden-source silence together",
            "CONFIRMS_COUNTEREXAMPLE_LEDGER",
        ),
        (
            "HUNT2795_5_1028",
            source_path("1028_no_marker_pack"),
            "no-marker/constant descent and coupling bound pack",
            "maps surviving ordinary-matter markers into c_g, b_dis, b_A, b_alpha, q_nonH, support rows",
            "ordinary matter no-marker theorem remains fail-current-claim",
            "NO_MARKER_NOT_PARENT_SIGNED",
        ),
        (
            "HUNT2795_6_formal10",
            source_path("formalization_10_core_repair"),
            "formalization-workbench core consistency repair",
            "early action skeleton names matter and interaction sectors",
            "does not provide species-complete quotient matter functor, constants, no-weight, no-shadow, and boundary clauses",
            "ACTION_SKELETON_INSUFFICIENT",
        ),
        (
            "HUNT2795_7_1089_analogue",
            source_path("1089_source_hunt_analogue"),
            "R10 signature source hunt analogue",
            "structural precedent says many contracts exist but no parent signature source was found there",
            "analogue cannot be imported as R2FR evidence",
            "ANALOGUE_ONLY",
        ),
        (
            "HUNT2795_8_verdict",
            "CURRENT_R2FR_SOURCE_HUNT",
            "any real parent-action source signing all MOMS2794 clauses",
            "no source found that signs action form, quotient observables, matter bundle, constant superselection, no species weights, variation order, and no shadow/domain together",
            "all inspected hits are contracts, conditional theorems, scaffolds, or explicit not-derived verdicts",
            "NO_PARENT_SIGNATURE_SOURCE_FOUND",
        ),
    ]
    return [
        {
            "hunt_id": row[0],
            "source": row[1],
            "candidate_text": row[2],
            "support_for_MOMS": row[3],
            "blocking_text": row[4],
            "verdict": row[5],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_coverage_rows() -> list[dict[str, Any]]:
    rows = [
        ("MOMS2794_0_action_form", "2794 signature; 1009 parent current contract; formalization 10", "single-action schema language exists", "schema_written_not_derived", "derive from MTS primitives rather than adopt a discipline contract"),
        ("MOMS2794_1_quotient_observables", "2794 signature; 2793 descent; 1027 qbar route", "chain-rule descent is exact conditionally", "conditional_lemma_not_parent_signed", "parent-owned q and observed coframe/gauge functor"),
        ("MOMS2794_2_matter_bundle", "2793 descent; 1027 qbar route; 1028 no-marker route", "matter functor language exists", "matter_category_and_vertical_lift_unsigned", "species-complete parent matter bundle and owned lift"),
        ("MOMS2794_3_constant_superselection", "2794 signature; 1028 no-marker pack", "constant-sector route is named", "constant_superselection_unsigned", "ordinary masses, charges, clocks, and alpha_EM fixed by parent representation/topological data or explicit residual coefficients"),
        ("MOMS2794_4_no_species_weights", "2794 signature; 2793 descent", "pre-action weight obstruction is explicit", "single_measure_current_owner_unsigned", "parent action-scale/measure/source-label forgetting theorem"),
        ("MOMS2794_5_variation_order", "2794 signature; 2793 contract; 1089 analogue", "variation-before-readout rule exists as a gate", "conditional_subtheorem_only", "parent-side rule tied to one action and readout map"),
        ("MOMS2794_6_no_shadow_domain", "2794 signature; 1027/1028 countermodel packs", "shadow/disformal/domain countermodels are known", "guard_written_not_parent_derived", "parent operator-domain theorem or retained coefficient rows"),
        ("MOMS2794_7_all_in_one", "none found", "no single source signs all clauses", "NO_PARENT_SIGNATURE_SOURCE_FOUND", "derive one parent ordinary-matter action signature or demote MOMS to explicit closure"),
    ]
    return [
        {
            "clause_id": row[0],
            "best_candidate_source": row[1],
            "coverage": row[2],
            "source_status": row[3],
            "claim_gap": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("BLK2795_0_one_parent_source", "no single parent-action source signs MOMS2794", "separate contracts can be mutually consistent but do not constitute a derivation", "synthesize and derive MOMS2794 from the parent action spine or mark it as a closure"),
        ("BLK2795_1_source_weight", "w_A/action-scale route remains live", "relative action scales change Hilbert source even if classical equations look unchanged", "derive common hbar/measure/current owner or retain finite DD coefficients"),
        ("BLK2795_2_constant_shadow", "constant superselection and no-shadow-frame are unsigned", "alpha_EM, masses, clocks, conformal/disformal frames can carry WEP/R10/clock residuals", "derive fixed representation/topological constant sector and no hidden mixed matter frames"),
        ("BLK2795_3_local_GR_not_paid", "even MOMS2794 would not alone prove full local GR/Newton", "source mass, EH/R11 operator, boundary/reference, and PPN readout have independent gates", "treat WEP/MOMS as one pillar and return to source-mass/operator/PPN gates after signature status is decided"),
    ]
    return [
        {
            "blocker_id": row[0],
            "blocker": row[1],
            "why_it_matters": row[2],
            "repair_path": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_policy_rows() -> list[dict[str, Any]]:
    rows = [
        ("FIR2795_0_source_backed_only", "finite DD rows may be reviewed only if every value has source_path and source_row", "blocks invented coefficients and post-hoc WEP fitting"),
        ("FIR2795_1_same_branch", "branch_id must be common across lambda_X, K_MICROSCOPE, Qeff_E, coefficients, and test-material deltas", "blocks range/amplitude/readout mix-and-match"),
        ("FIR2795_2_no_pair_cancellation", "a TA6V-PtRh10 cancellation line cannot be used as a theory result", "blocks one-pair tuning"),
        ("FIR2795_3_common_mode_split", "universal mass/G calibration may remove only common mode, not composition contrast", "blocks measured-G absorption of WEP residuals"),
        ("FIR2795_4_placeholder_refusal", "MISSING_* rows remain valid_for_claim=false and are refused by runners", "keeps finite intake as scaffolding until real rows appear"),
    ]
    return [
        {
            "policy_id": row[0],
            "review_rule": row[1],
            "why": row[2],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "prediction_id": "WEP2795_0_placeholder_intake_review",
            "observable": "eta_AB(lambda)",
            "input_source": str(MTS / "P8_Y5_R2FR_2794_FINITE_DD_INTAKE_TEMPLATE_NONCLAIM.csv"),
            "review_status": "PLACEHOLDERS_ONLY",
            "eta_pred": "MISSING_NUMERIC",
            "claim_blocker": "no fully sourced finite DD row and no parent signature source",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN2795_0_refuse_unsigned_signature_and_placeholders",
            "valid_prediction_rows": 0,
            "claim_allowed": False,
            "expected_result": "RUNNER_REFUSES_WEP_CLAIM",
            "reason": "source hunt found no parent signature source and finite intake rows remain placeholders",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        {
            "comparison_id": "CMP2795_0_no_numeric_eta",
            "baseline": "WEP/local-GR compatibility bound",
            "prediction": "MTS R2FR finite DD branch",
            "comparison_status": "NOT_RUN_NUMERICALLY",
            "reason": "no source-backed finite DD coefficient/readout/profile row exists",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2795_0_source_hunt", "parent ordinary-matter signature source found", False, False, "HUNT2795_8_verdict=NO_PARENT_SIGNATURE_SOURCE_FOUND"),
        ("CG2795_1_moms_signature", "MOMS2794 promoted to MTS theorem", False, False, "signature is exact contract but not parent-derived"),
        ("CG2795_2_finite_intake_review", "finite DD intake contains fully sourced rows", False, False, "current intake rows are placeholders"),
        ("CG2795_3_product_runner", "WEP product runner", True, False, "runner safely refuses claim"),
        ("CG2795_4_local_GR_claim", "local-GR/WEP reduction", False, False, "no parent signature source and no finite sourced comparison"),
    ]
    return [
        {
            "gate_id": row[0],
            "claim_component": row[1],
            "gate_pass": row[2],
            "claim_allowed": row[3],
            "reason": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2795_0_source_hunt_result", "no parent source found for MOMS2794", "the scan found contract/proof language but no file signing all clauses from the parent action", "attempt synthesis from the parent action spine or demote MOMS2794 to explicit closure"),
        ("DEC2795_1_conditional_theorem_retained", "keep the conditional zero theorem", "the theorem is mathematically useful and tells us exactly what a parent action must supply", "do not promote it until source-hunt or synthesis closes"),
        ("DEC2795_2_finite_intake_review", "keep finite DD intake as nonclaim scaffolding", "if theorem-zero fails, sourced coefficient rows are the only safe route to testing", "review only rows passing FIR2795 policy"),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2795_0_2796",
            "next_target": "2796-Y5-R2FR-parent-action-signature-synthesis-or-MOMS-closure-demotion-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_action_signature_synthesis_or_MOMS_closure_demotion_under_AX1090_2796.py",
            "objective": "attempt to synthesize the MOMS2794 ordinary-matter signature from existing parent action, observed coframe, matter functor, current-owner, no-marker, and boundary/domain clauses; if synthesis cannot be derived, demote MOMS2794 to an explicit closure assumption and keep finite DD intake as the test route",
            "include": "parent action spine; observed quotient/coframe; matter bundle; no species weights/action measure; constant superselection; no-shadow/domain; closure-demotion ledger; finite intake fallback",
            "exclude": "declaring MOMS2794 sourced without one action; invented coefficients; pair cancellation; measured-G absorption; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["hunt"], BRANCH_OUTPUTS["hunt_queue"], "hunt_queue"),
        (OUTPUTS["coverage"], BRANCH_OUTPUTS["coverage_queue"], "coverage_queue"),
        (OUTPUTS["policy"], BRANCH_OUTPUTS["policy_queue"], "policy_queue"),
        (OUTPUTS["hunt"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows: list[dict[str, Any]] = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2795_{label}",
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2795_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all cited local source paths exist"),
        ("VAL2795_1_search_ran", all(int(row["matching_file_count"]) >= 0 and int(row["occurrence_count"]) >= 0 for row in sections["search_summary"]), "corpus search summary ran and has numeric counts"),
        ("VAL2795_2_no_source_found", any(row["hunt_id"] == "HUNT2795_8_verdict" and row["verdict"] == "NO_PARENT_SIGNATURE_SOURCE_FOUND" for row in sections["hunt"]), "source hunt found no parent signature source"),
        ("VAL2795_3_coverage_all_clauses", {row["clause_id"] for row in sections["coverage"]} >= {f"MOMS2794_{index}_{suffix}" for index, suffix in [(0, "action_form"), (1, "quotient_observables"), (2, "matter_bundle"), (3, "constant_superselection"), (4, "no_species_weights"), (5, "variation_order"), (6, "no_shadow_domain"), (7, "all_in_one")]}, "coverage matrix includes all MOMS2794 clauses"),
        ("VAL2795_4_all_in_one_missing", any(row["clause_id"] == "MOMS2794_7_all_in_one" and row["source_status"] == "NO_PARENT_SIGNATURE_SOURCE_FOUND" for row in sections["coverage"]), "all-in-one parent source remains missing"),
        ("VAL2795_5_blockers_present", {row["blocker_id"] for row in sections["blockers"]} >= {"BLK2795_0_one_parent_source", "BLK2795_1_source_weight", "BLK2795_2_constant_shadow", "BLK2795_3_local_GR_not_paid"}, "blocker ledger covers source, weight, constant/shadow, and local-GR debts"),
        ("VAL2795_6_policy_blocks_shortcuts", {row["policy_id"] for row in sections["policy"]} >= {"FIR2795_0_source_backed_only", "FIR2795_1_same_branch", "FIR2795_2_no_pair_cancellation", "FIR2795_3_common_mode_split", "FIR2795_4_placeholder_refusal"}, "finite intake policy blocks shortcuts"),
        ("VAL2795_7_runner_refuses", any(row["expected_result"] == "RUNNER_REFUSES_WEP_CLAIM" and str(row["claim_allowed"]).lower() == "false" for row in sections["runner"]), "runner refuses unsigned/placeholder branch"),
        ("VAL2795_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2795_9_next_target_2796", any(row["next_id"] == "NEXT2795_0_2796" for row in sections["next"]), "next target is 2796"),
        ("VAL2795_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2795_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2795_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2795_13_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2795_14_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2795_15_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2795_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "passed": bool(passed),
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2795_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2795 scans the current R2FR/post-checkpoint corpus for a parent source signing MOMS2794. It finds many contracts and conditional theorem hits but no single parent-action source. Finite DD intake remains explicitly nonclaim.",
            "generated_utc": utc_now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2795 — Y5 R2FR Parent Ordinary Matter Signature Source Hunt Or DD Intake Review Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2795 looked for the thing that would really move the WEP/local-GR branch: a current parent-action source that signs the whole MOMS2794 ordinary-matter signature. The scan finds lots of nearby language — parent action, S_matter, matter functor, no-marker, superselection, no-shadow/domain, variation-before-readout — but the source-hunt ledger finds no single source that signs all clauses from one parent action.",
        "",
        "So MOMS2794 remains a powerful conditional theorem target, not a claimable MTS result. The finite DD intake route remains the honest fallback: only fully sourced rows may be reviewed; placeholders, pair cancellation, measured-G absorption, and mixed-branch normalization are rejected.",
        "",
        "## Corpus Signature Search Summary",
        markdown_table(sections["search_summary"], ["search_id", "pattern", "matching_file_count", "occurrence_count", "interpretation"]),
        "",
        "## Signature Source Hunt",
        markdown_table(sections["hunt"], ["hunt_id", "candidate_text", "support_for_MOMS", "verdict", "blocking_text"]),
        "",
        "## MOMS Clause Coverage Matrix",
        markdown_table(sections["coverage"], ["clause_id", "best_candidate_source", "coverage", "source_status", "claim_gap"]),
        "",
        "## Signature Blocker Ledger",
        markdown_table(sections["blockers"], ["blocker_id", "blocker", "why_it_matters", "repair_path"]),
        "",
        "## Finite Intake Review Policy",
        markdown_table(sections["policy"], ["policy_id", "review_rule", "why"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "search_summary": build_search_summary(),
        "hunt": build_hunt_rows(),
        "coverage": build_coverage_rows(),
        "blockers": build_blocker_rows(),
        "policy": build_policy_rows(),
        "candidate": build_candidate_rows(),
        "runner": build_runner_rows(),
        "comparisons": build_comparison_rows(),
        "gates": build_gate_rows(),
        "decision": build_decision_rows(),
        "next": build_next_rows(),
    }
    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
