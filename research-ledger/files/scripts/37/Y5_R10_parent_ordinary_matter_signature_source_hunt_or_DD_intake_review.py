from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1089-Y5-R10-parent-ordinary-matter-signature-source-hunt-or-DD-intake-review.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1089-parent-ordinary-matter-signature-source-hunt" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1089_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1089_WEP_BOUND_IMPORT.csv"
ETA_BOUND = 2.8e-15


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1089_0_1088_next", "source-intake/mts_residuals/P8_Y5_R10_1088_NEXT_TARGET.csv", "NEXT1088_0_1089", "1088 handoff."),
        ("SRC1089_1_1088_doc", "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md", "MOMS1088_7_verdict", "minimal signature verdict."),
        ("SRC1089_2_1055_contract", "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md", "PAC1055_6_single_parent_action", "single parent action contract candidate."),
        ("SRC1089_3_990_contract", "990-Y5-R10-minimal-parent-action-coupling-contract-EM-matter-GR-reentry.md", "PAC990_2_matter_functor", "parent action coupling contract."),
        ("SRC1089_4_943_coframe", "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md", "CFC943_7_contract_verdict", "single observed coframe descent contract."),
        ("SRC1089_5_1045_functor", "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md", "MFS1045_6_verdict", "matter functor signature audit."),
        ("SRC1089_6_1067_action_scale", "1067-Y5-R10-parent-quantum-action-scale-normalization-or-WEP-tau-projection.md", "ASO1067_5_verdict", "action-scale/species-weight audit."),
        ("SRC1089_7_formal_parent_v0", "../formalization-workbench/36-minimal-parent-equations-v0.md", "not action-derived", "formal parent equation scaffold."),
        ("SRC1089_8_formal_core_repair", "../formalization-workbench/10-core-consistency-repair.md", "Parent Action Skeleton", "early parent action skeleton."),
        ("SRC1089_9_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
        ("SRC1089_10_1088_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1088_VALIDATION.csv", "V1088_SUMMARY", "1088 validation summary."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle_found = exists and needle.lower() in text.lower()
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def corpus_search_summary_rows() -> list[dict[str, str]]:
    patterns = [
        ("SEARCH1089_0_matter_action", "S_matter"),
        ("SEARCH1089_1_parent_action", "parent action"),
        ("SEARCH1089_2_species_weight", "w_A"),
        ("SEARCH1089_3_superselection", "superselection"),
        ("SEARCH1089_4_shadow_frame", "shadow frame"),
        ("SEARCH1089_5_variation_readout", "variation-before-readout"),
    ]
    roots = [ROOT, FORMALIZATION]
    rows: list[dict[str, str]] = []
    for search_id, pattern in patterns:
        matching_files: set[str] = set()
        occurrences = 0
        for root in roots:
            if not root.exists():
                continue
            for path in root.rglob("*.md"):
                if "runs" in path.parts:
                    continue
                text = read_text(path)
                count = text.lower().count(pattern.lower())
                if count:
                    occurrences += count
                    matching_files.add(str(path))
        rows.append(
            {
                "search_id": search_id,
                "pattern": pattern,
                "matching_file_count": str(len(matching_files)),
                "occurrence_count": str(occurrences),
                "interpretation": "many contracts/hits exist; candidate rows below decide whether any hit is parent-signed",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def candidate_hunt_rows() -> list[dict[str, str]]:
    return [
        {
            "hunt_id": "HUNT1089_0_1088",
            "source": "1088 MOMS signature gate",
            "candidate_text": "conditional zero theorem under MOMS1088",
            "support_for_MOMS": "strong exact contract and proof route",
            "blocking_text": "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
            "verdict": "CONTRACT_NOT_SOURCE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hunt_id": "HUNT1089_1_1055",
            "source": "1055 parent action contract",
            "candidate_text": "S_parent = S_geom + S_hidden + S_EM + sum_A S_A + S_boundary",
            "support_for_MOMS": "closest single-action schema for EM, matter, constants, and source-label forgetting",
            "blocking_text": "SCHEMA_WRITTEN_NOT_DERIVED_FROM_DEEPER_MTS",
            "verdict": "BEST_CONTRACT_BUT_NOT_PARENT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hunt_id": "HUNT1089_2_990",
            "source": "990 GR/EM/matter reentry contract",
            "candidate_text": "PAC990_2 all matter descends through one species-blind observed matter functor",
            "support_for_MOMS": "connects matter functor to local GR/Newton reentry checklist",
            "blocking_text": "explicit_closure_not_theorem",
            "verdict": "CLOSURE_CONTRACT_NOT_SOURCE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hunt_id": "HUNT1089_3_943",
            "source": "943 single observed coframe",
            "candidate_text": "q:Phi -> Q_obs; e_obs=Obs_e(q(Phi)); S_matter=sum_A S_A[psi_A,e_obs,omega,theta_A]",
            "support_for_MOMS": "chain-rule coframe/matter descent route is exact",
            "blocking_text": "contract_exact_but_unsigned",
            "verdict": "EXACT_DESCENT_CONTRACT_UNSIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hunt_id": "HUNT1089_4_1045",
            "source": "1045 matter functor audit",
            "candidate_text": "MFS1045_0 through MFS1045_5 define the required matter functor signature",
            "support_for_MOMS": "complete matter-bundle/coframe/vertical-lift/no-shadow/constants checklist",
            "blocking_text": "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED",
            "verdict": "AUDIT_CONFIRMS_UNSIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hunt_id": "HUNT1089_5_1067",
            "source": "1067 action-scale owner",
            "candidate_text": "single hbar/action measure plus species-blind Jacobian would close w_A",
            "support_for_MOMS": "sharpest source for no species weights/action-scale clause",
            "blocking_text": "CONDITIONAL_NOT_PARENT_DERIVED",
            "verdict": "NO_SPECIES_WEIGHT_CLAUSE_UNSIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hunt_id": "HUNT1089_6_formal36",
            "source": "formalization-workbench 36 parent equations v0",
            "candidate_text": "one parent conservation structure and ordinary matter/MTS exchange",
            "support_for_MOMS": "global parent-equation scaffold exists",
            "blocking_text": "partially_derived scaffold; not action-derived; not public-claim ready",
            "verdict": "FORMAL_SPINE_NOT_ACTION_SIGNATURE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hunt_id": "HUNT1089_7_core10",
            "source": "formalization-workbench 10 core consistency repair",
            "candidate_text": "S_total skeleton with L_int and L_matter",
            "support_for_MOMS": "early action skeleton names matter and interaction sectors",
            "blocking_text": "skeleton lacks ordinary-matter quotient functor, constants, no-weight, no-shadow, and readout clauses",
            "verdict": "SKELETON_INSUFFICIENT",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hunt_id": "HUNT1089_8_verdict",
            "source": "1089 source hunt",
            "candidate_text": "any real parent-action source signing all MOMS1088 clauses",
            "support_for_MOMS": "none found in inspected current corpus",
            "blocking_text": "all available sources are contracts, conditional theorems, scaffolds, or explicit not-derived verdicts",
            "verdict": "NO_PARENT_SIGNATURE_SOURCE_FOUND",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def moms_coverage_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "MOMS1088_0_action_form",
            "best_candidate_source": "1055 PAC1055_6; 990 PAC990_0/PAC990_2; formalization 36",
            "coverage": "single-action schema exists",
            "source_status": "schema_written_not_derived",
            "claim_gap": "derive from MTS primitives rather than adopt a discipline contract",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_1_quotient_observables",
            "best_candidate_source": "943 CFC943_0/CFC943_1; 1045 MFS1045_0/MFS1045_1",
            "coverage": "chain-rule descent exact",
            "source_status": "conditional_lemma_not_parent_signed",
            "claim_gap": "parent-owned q and Obs_e functor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_2_matter_bundle",
            "best_candidate_source": "1045 MFS1045_2/MFS1045_3; 1055 PAC1055_2",
            "coverage": "matter bundle/functor language exists",
            "source_status": "matter_category_and_vertical_lift_unsigned",
            "claim_gap": "species-complete parent matter bundle and owned lift",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_3_constant_superselection",
            "best_candidate_source": "1055 PAC1055_2/PAC1055_3; 1045 MFS1045_5",
            "coverage": "constant-sector route is named",
            "source_status": "constant_superselection_unsigned",
            "claim_gap": "ordinary masses, charges, clocks, and alpha_EM fixed by parent representation/topological data",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_4_no_species_weights",
            "best_candidate_source": "1067 ASO1067_5; 1055 PAC1055_4",
            "coverage": "relative action-scale obstruction is explicit",
            "source_status": "single_hbar_measure_current_owner_unsigned",
            "claim_gap": "parent action-scale/measure/source-label forgetting theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_5_variation_order",
            "best_candidate_source": "1066 SSE1066_2; 1079 current-owner stack; 1087 ZCC1087_2",
            "coverage": "variation-before-readout rule exists as a gate",
            "source_status": "conditional_subtheorem_only",
            "claim_gap": "parent-side rule tied to one action and readout map",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_6_no_shadow_domain",
            "best_candidate_source": "943 CFC943_6; 1045 MFS1045_4; 1055 CE1055_2",
            "coverage": "shadow/disformal/domain countermodels are known",
            "source_status": "guard_written_not_parent_derived",
            "claim_gap": "parent operator-domain theorem or retained coefficient rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_7_all_in_one",
            "best_candidate_source": "none found",
            "coverage": "no single source signs all clauses",
            "source_status": "NO_PARENT_SIGNATURE_SOURCE_FOUND",
            "claim_gap": "derive one parent ordinary-matter action signature or demote MOMS to explicit closure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def blocker_rows() -> list[dict[str, str]]:
    return [
        {
            "blocker_id": "BLK1089_0_one_parent_source",
            "blocker": "no single parent-action source signs MOMS1088",
            "why_it_matters": "separate contracts can be mutually consistent but do not constitute a derivation",
            "repair_path": "synthesize and derive MOMS from existing PAC1055/PAC990 parent spine or mark it as new axiom/closure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "blocker_id": "BLK1089_1_source_weight",
            "blocker": "w_A/action-scale route remains live",
            "why_it_matters": "relative action scales change Hilbert source even if classical EOM look unchanged",
            "repair_path": "derive common hbar/measure/current owner or retain finite DD coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "blocker_id": "BLK1089_2_constant_shadow",
            "blocker": "constant superselection and no-shadow-frame are unsigned",
            "why_it_matters": "alpha_EM, masses, clocks, conformal/disformal frames can carry WEP/R10/clock residuals",
            "repair_path": "derive fixed representation/topological constant sector and no mixed hidden-visible operators",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "blocker_id": "BLK1089_3_local_GR_not_paid",
            "blocker": "even MOMS would not alone prove full local GR/Newton",
            "why_it_matters": "source mass, EH/R11 operator, boundary/reference, and PPN readout still have independent gates",
            "repair_path": "keep WEP/MOMS as one pillar and return to source-mass/operator/PPN gates after signature status is decided",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def intake_review_policy_rows() -> list[dict[str, str]]:
    return [
        {
            "policy_id": "IRP1089_0_no_filled_rows",
            "review_item": "finite DD intake rows from 1088",
            "current_status": "no filled source-backed values found",
            "allowed_next": "review only rows with numeric value, units, source path, source row, derivation status, same-branch lock, and bound link",
            "forbidden": "invented coefficient values; pair cancellation; measured-G absorption; unit source proxy promoted to claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "policy_id": "IRP1089_1_closure_label",
            "review_item": "MOMS1088 as closure",
            "current_status": "not adopted",
            "allowed_next": "if user deliberately chooses closure route later, label as closure_assumed and compare honestly",
            "forbidden": "calling closure a derivation or using it for local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1089_0_source_hunt_no_signature",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_SIGNATURE_SOURCE_OR_FILLED_DD_INTAKE",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1089_SIGNATURE_SOURCE_HUNT.csv",
            "inputs_present": "candidate contracts; MOMS coverage matrix; MICROSCOPE bound",
            "required_inputs": "one source signing all MOMS1088 clauses or filled same-branch finite DD intake",
            "derivation_status": "SOURCE_HUNT_FAILED_NO_NUMERIC_INTAKE",
            "valid_for_claim": "false",
            "notes": "runner must refuse; 1089 is a source-hunt verdict, not a physical prediction",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1089_0_MICROSCOPE_WEP",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": f"{ETA_BOUND:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "bound_type": "absolute_eta_upper_bound",
            "valid_for_claim": "true",
            "notes": "source-backed comparator bound; MTS prediction row remains invalid",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1089_0_source_hunt_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject source-hunt placeholder until parent signature source or filled intake exists",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1089_0_parent_signature_source",
            "claim_component": "real source for MOMS1088",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "HUNT1089_8_verdict=NO_PARENT_SIGNATURE_SOURCE_FOUND",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1089_1_finite_intake_review",
            "claim_component": "filled finite DD intake",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "no filled source-backed finite coefficient rows available",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1089_2_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": str(product_status.get("valid_prediction_rows") == 0).lower(),
            "claim_allowed": "false",
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1089_0_hunt_result",
            "decision": "do not keep re-hunting the current corpus for a signed MOMS source",
            "because": "the strongest files contain the right contract but explicitly label it unsigned, closure, scaffold, or not action-derived",
            "next_action": "attempt a synthesis/derivation from PAC1055 and PAC990, or write a missing-axiom ledger if the synthesis fails",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1089_1_finite_route",
            "decision": "finite DD intake remains allowed only as labelled phenomenology",
            "because": "no filled finite rows exist and no source-backed same-branch coefficient pack is available",
            "next_action": "review filled rows only after provenance, units, and same-branch locks are present",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1089_0_1090",
            "next_target": "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md",
            "objective": "try to synthesize MOMS1088 from PAC1055/PAC990/943/1045/1067 into one parent ordinary-matter action derivation; if it cannot be derived, write the exact missing axiom/closure ledger and stop treating MOMS as derivable from current files",
            "include": "single parent action synthesis; clause-by-clause derivation dependencies; ordinary matter signature; no species weights; constant superselection; no shadow frame; closure demotion if synthesis fails",
            "exclude": "claiming MOMS by contract repetition; invented finite coefficients; pair cancellation; measured-G absorption; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_outputs_parse(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    search_rows: list[dict[str, str]],
    hunt_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
    blockers: list[dict[str, str]],
    policies: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1089_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited source paths and needles are present"))
    checks.append(("V1089_1_search_summary_written", len(search_rows) == 6 and all(int(row["matching_file_count"]) >= 0 for row in search_rows), "corpus search summary rows are written"))
    checks.append(("V1089_2_no_signature_source_found", any(row["hunt_id"] == "HUNT1089_8_verdict" and row["verdict"] == "NO_PARENT_SIGNATURE_SOURCE_FOUND" for row in hunt_rows), "source hunt ends in no parent signature source found"))
    checks.append(("V1089_3_all_candidates_nonclaim", len(hunt_rows) == 9 and all(row["valid_for_claim"] == "false" for row in hunt_rows), "all candidate source rows remain nonclaim"))
    checks.append(("V1089_4_moms_coverage_complete", len(coverage_rows) == 8 and coverage_rows[-1]["source_status"] == "NO_PARENT_SIGNATURE_SOURCE_FOUND", "MOMS coverage matrix covers all clauses and all-in-one failure"))
    checks.append(("V1089_5_blockers_written", len(blockers) == 4 and all(row["valid_for_claim"] == "false" for row in blockers), "blocker ledger is explicit"))
    checks.append(("V1089_6_intake_policy_nonclaim", len(policies) == 2 and all(row["valid_for_claim"] == "false" for row in policies), "finite intake review policy remains nonclaim"))
    checks.append(("V1089_7_prediction_missing_nonclaim", any("MISSING_PARENT_SIGNATURE_SOURCE" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "prediction row remains missing source or filled intake"))
    checks.append(("V1089_8_bound_numeric", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "MICROSCOPE bound import is positive numeric"))
    checks.append(("V1089_9_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1089_10_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1089_11_next_target", any(row["next_target"].startswith("1090-Y5-R10-MOMS-parent-action") for row in next_rows), "1090 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1089_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1089_13_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1089 CSV outputs parse cleanly"))
    checks.append(("V1089_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1089_SUMMARY", True, "source hunt found contracts and conditional theorems but no parent-signed MOMS source; finite DD intake remains empty and nonclaim"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    search_rows: list[dict[str, str]],
    hunt_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
    blockers: list[dict[str, str]],
    policies: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1089-Y5-R10 parent ordinary-matter signature source hunt or DD intake review",
            "",
            "## Current verdict",
            "1089 searched the current corpus for a real parent-action source that signs the MOMS1088 ordinary-matter signature. The result is not a collapse, but it is a hard truth: the right clauses already exist in several places, yet every strong candidate labels itself as a contract, scaffold, closure, conditional theorem, or not action-derived. So MOMS is not promoted. The next move is not another blind hunt; it is a synthesis attempt from PAC1055/PAC990/943/1045/1067, or an explicit missing-axiom ledger if that synthesis fails.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Corpus search summary",
            md_table(search_rows, ["search_id", "pattern", "matching_file_count", "occurrence_count", "interpretation"]),
            "## Signature source hunt",
            md_table(hunt_rows, ["hunt_id", "source", "candidate_text", "support_for_MOMS", "blocking_text", "verdict"]),
            "## MOMS clause coverage",
            md_table(coverage_rows, ["clause_id", "best_candidate_source", "coverage", "source_status", "claim_gap"]),
            "## Blocker ledger",
            md_table(blockers, ["blocker_id", "blocker", "why_it_matters", "repair_path"]),
            "## Finite intake review policy",
            md_table(policies, ["policy_id", "review_item", "current_status", "allowed_next", "forbidden"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    search_rows = corpus_search_summary_rows()
    hunt_rows = candidate_hunt_rows()
    coverage_rows = moms_coverage_rows()
    blockers = blocker_rows()
    policies = intake_review_policy_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1089_SOURCE_REGISTER.csv",
        "search_summary": OUT / "P8_Y5_R10_1089_CORPUS_SIGNATURE_SEARCH_SUMMARY.csv",
        "signature_hunt": OUT / "P8_Y5_R10_1089_SIGNATURE_SOURCE_HUNT.csv",
        "moms_coverage": OUT / "P8_Y5_R10_1089_MOMS_CLAUSE_COVERAGE_MATRIX.csv",
        "blockers": OUT / "P8_Y5_R10_1089_SIGNATURE_BLOCKER_LEDGER.csv",
        "intake_policy": OUT / "P8_Y5_R10_1089_FINITE_INTAKE_REVIEW_POLICY.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1089_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1089_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1089_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1089_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1089_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1089_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["search_summary"], search_rows)
    write_csv(outputs["signature_hunt"], hunt_rows)
    write_csv(outputs["moms_coverage"], coverage_rows)
    write_csv(outputs["blockers"], blockers)
    write_csv(outputs["intake_policy"], policies)
    write_csv(outputs["prediction"], prediction_rows_, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    product_comparisons = product_result["comparisons"]
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_comparisons)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        search_rows,
        hunt_rows,
        coverage_rows,
        blockers,
        policies,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        search_rows,
        hunt_rows,
        coverage_rows,
        blockers,
        policies,
        product_status_rows_,
        product_comparisons,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
