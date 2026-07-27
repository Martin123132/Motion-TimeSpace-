from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
METADATA = MICROSCOPE / "metadata"
BRANCH_ROOT = MICROSCOPE / "branch_locked_wep"
COEFFICIENT_ROOT = BRANCH_ROOT / "coefficients"
RESIDUAL_ROOT = BRANCH_ROOT / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1441-Y5-R10-RAB-AX1090-parent-axiom-reduction-or-source-pack-acquisition-priority.md"

BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
NEXT_1440 = OUT / "P8_Y5_R10_1440_NEXT_TARGET.csv"
VALIDATION_1440 = OUT / "P8_Y5_BRR545_1440_VALIDATION.csv"
PROOF_1440 = OUT / "P8_Y5_R10_1440_PROOF_OBLIGATION_AUDIT.csv"
CLOSURE_1440 = OUT / "P8_Y5_R10_1440_CLOSURE_DEMOTION_REGISTER.csv"
SOURCE_ROUTE_1440 = OUT / "P8_Y5_R10_1440_SOURCE_PACK_ONLY_ROUTE_STATUS.csv"
REOPEN_1440 = OUT / "P8_Y5_R10_1440_REOPEN_CONDITIONS.csv"
AXIOM_1090 = OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
MOMS_1088 = OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv"
THM_1088 = OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv"
CLOSURE_1090 = OUT / "P8_Y5_R10_1090_CLOSURE_DEMOTION_REGISTER.csv"
SOURCE_PACK_MANIFEST_1438 = OUT / "P8_Y5_R10_1438_OFFICIAL_MICROSCOPE_SOURCE_PACK_MANIFEST.csv"
PARSER_1439 = OUT / "P8_Y5_R10_1439_SOURCE_PACK_PARSER_DRYRUN.csv"
WEB_SOURCES_1336 = METADATA / "P8_Y5_R10_1336_WEB_SOURCE_CANDIDATE_REGISTER.csv"
LOCAL_AUDIT_1336 = METADATA / "P8_Y5_R10_1336_LOCAL_MICROSCOPE_INTAKE_AUDIT.csv"
BRANCH_CLOSURE_1440 = COEFFICIENT_ROOT / "C_parent_WEP_clause_closure_demotion.csv"
BRANCH_SOURCE_ROUTE_1440 = RESIDUAL_ROOT / "source_pack_only_route_status.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1441_SOURCE_REGISTER.csv"
AX1090_REDUCTION_AUDIT = OUT / "P8_Y5_R10_1441_AX1090_REDUCTION_AUDIT.csv"
AX1090_DEPENDENCY_GRAPH = OUT / "P8_Y5_R10_1441_AX1090_DEPENDENCY_GRAPH.csv"
SOURCE_PACK_ACQUISITION_PRIORITY = OUT / "P8_Y5_R10_1441_SOURCE_PACK_ACQUISITION_PRIORITY.csv"
ACTIVE_ROUTE_STATUS = OUT / "P8_Y5_R10_1441_ACTIVE_ROUTE_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1441_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1441_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1441_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1441_VALIDATION.csv"

BRANCH_AX1090_STATUS = COEFFICIENT_ROOT / "AX1090_reduction_status.csv"
BRANCH_SOURCE_PRIORITY = RESIDUAL_ROOT / "source_pack_acquisition_priority.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


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


def branch_id() -> str:
    rows = read_csv(BRANCH_ID_FILE)
    if len(rows) != 1:
        raise ValueError(f"expected one branch row, got {len(rows)}")
    value = rows[0].get("same_parent_branch_id", "").strip()
    if not value:
        raise ValueError("same_parent_branch_id missing")
    return value


def source_register_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC1441_0_1440_next", NEXT_1440, "NEXT1440_0_1441", "1440 handoff selecting AX1090 reduction or source-pack priority."),
        ("SRC1441_1_1440_validation", VALIDATION_1440, "VAL1440_11_overall", "1440 validation summary."),
        ("SRC1441_2_1440_proof", PROOF_1440, "PO1440_7_countermodel_exclusion", "1440 proof obligation audit."),
        ("SRC1441_3_1440_closure", CLOSURE_1440, "CLOS1440_0_minimal_WEP_parent_clause", "1440 closure demotion."),
        ("SRC1441_4_1440_source_route", SOURCE_ROUTE_1440, "SPR1440_0_source_pack_only_score_route", "1440 source-pack-only route."),
        ("SRC1441_5_1440_reopen", REOPEN_1440, "REOPEN1440_5_source_pack", "1440 reopen conditions."),
        ("SRC1441_6_AXIOM1090", AXIOM_1090, "AX1090_4_variation_domain_order", "AX1090 missing axiom ledger."),
        ("SRC1441_7_MOMS1088", MOMS_1088, "MOMS1088_7_verdict", "minimal ordinary-matter signature."),
        ("SRC1441_8_THM1088", THM_1088, "THM1088_6_current_corpus_verdict", "conditional theorem stack."),
        ("SRC1441_9_CLOS1090", CLOSURE_1090, "CLOS1090_0_MOMS", "prior closure demotion precedent."),
        ("SRC1441_10_manifest1438", SOURCE_PACK_MANIFEST_1438, "PACK1438_5_C_parent_import", "official source-pack manifest."),
        ("SRC1441_11_parser1439", PARSER_1439, "PARSE1439_5", "source-pack parser dry-run."),
        ("SRC1441_12_web1336", WEB_SOURCES_1336, "WEB1336_1_CMSM_MICROSCOPE_portal", "official web source candidates."),
        ("SRC1441_13_local1336", LOCAL_AUDIT_1336, "LOCAL1336_9_branch_classifier", "local MICROSCOPE intake audit."),
        ("SRC1441_14_branch_id", BRANCH_ID_FILE, branch, "active branch lock."),
        ("SRC1441_15_branch_closure", BRANCH_CLOSURE_1440, "CLOS1440_1_C_parent_WEP_zero", "branch closure demotion copy."),
        ("SRC1441_16_branch_source_route", BRANCH_SOURCE_ROUTE_1440, "SPR1440_0_source_pack_only_score_route", "branch source-pack route copy."),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "path_exists": path.exists(),
            "anchor": anchor,
            "anchor_found": text_has(path, anchor),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, anchor, role in specs
    ]


def ax1090_reduction_rows(branch: str) -> list[dict[str, Any]]:
    rows = [
        (
            "AXRED1441_0_parent_object",
            "AX1090_0_parent_object",
            "single parent action owner before all readout/projection choices",
            "MTS primitive candidate: one variational parent object S_MTS[Phi,Psi] with sector certificates and a fixed variation domain",
            "NOT_REDUCED",
            "current files provide sector contracts and closure scaffolds, not one parent action that owns matter/source/readout together",
            "source-pack remains required",
        ),
        (
            "AXRED1441_1_no_hidden_visible_hom",
            "AX1090_1_no_hidden_visible_hom",
            "hidden/representative variables cannot enter visible matter coefficients except via q_obs or fixed representation data",
            "MTS primitive candidate: quotient category/functor with no-shadow/no-homomorphism theorem",
            "NOT_REDUCED",
            "no parent category theorem excludes conformal/disformal frames, marker functions, or hidden visible homomorphisms",
            "finite residual/source rows remain live",
        ),
        (
            "AXRED1441_2_common_measure",
            "AX1090_2_common_quantum_measure",
            "one action measure/current normalization with no species-dependent Jacobian",
            "MTS primitive candidate: universal action/current normalization from the parent symplectic measure",
            "NOT_REDUCED",
            "current corpus does not derive quantum/statistical measure universality from MTS primitives",
            "species-weight countermodel remains live",
        ),
        (
            "AXRED1441_3_fixed_constants",
            "AX1090_3_fixed_constant_sector",
            "ordinary masses, charges, alpha_EM, clocks, and material labels fixed or explicitly retained as residuals",
            "MTS primitive candidate: constants as representation/topological data plus explicit residual-register fallback",
            "PARTIAL_CONTRACT_NOT_REDUCED",
            "representation/superselection language exists, but EM/mass/material owner is not derived in one parent action",
            "no-marker theorem remains closure-only",
        ),
        (
            "AXRED1441_4_variation_order",
            "AX1090_4_variation_domain_order",
            "all source/current variations occur before readout, material projection, source-worldtube selection, or calibration",
            "MTS primitive candidate: parent Noether/current extraction before empirical projection",
            "PARTIAL_CONTRACT_NOT_REDUCED",
            "variation-before-readout is a correct gate, but not yet derived with detector/source model and official data",
            "official source-pack parser remains active",
        ),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "reduction_id": reduction_id,
            "axiom_id": axiom_id,
            "axiom_target": axiom_target,
            "candidate_MTS_reduction": candidate,
            "reduction_status": status,
            "why_not_reduced": why_not_reduced,
            "consequence": consequence,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for reduction_id, axiom_id, axiom_target, candidate, status, why_not_reduced, consequence in rows
    ]


def dependency_graph_rows(branch: str) -> list[dict[str, Any]]:
    edges = [
        ("EDGE1441_0", "AX1090_0_parent_object", "PO1440_0_parent_object", "owns all other WEP proof obligations"),
        ("EDGE1441_1", "AX1090_1_no_hidden_visible_hom", "PO1440_5_no_shadow_domain", "excludes hidden/shadow matter channels"),
        ("EDGE1441_2", "AX1090_2_common_quantum_measure", "PO1440_4_no_species_weights", "excludes species-dependent action weights"),
        ("EDGE1441_3", "AX1090_3_fixed_constant_sector", "PO1440_3_no_marker_constants", "excludes material/EM/clock marker currents"),
        ("EDGE1441_4", "AX1090_4_variation_domain_order", "PO1440_6_readout_silence", "prevents readout/source selection from creating or erasing residuals"),
        ("EDGE1441_5", "AX1090_0_parent_object", "official_source_pack_route", "if not reduced, finite source-pack route is required"),
        ("EDGE1441_6", "AX1090_3_fixed_constant_sector", "C_parent_WEP_slot_import", "if not reduced, C_parent/material tensor rows must carry constants explicitly"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "edge_id": edge_id,
            "from_node": from_node,
            "to_node": to_node,
            "relation": relation,
            "edge_status": "ACTIVE_UNPROVED_DEPENDENCY",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for edge_id, from_node, to_node, relation in edges
    ]


def acquisition_priority_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        (
            1,
            "PACK1438_5_C_parent_import",
            "C_parent_WEP_slot_import.csv",
            "branch_locked_wep_coefficients",
            "physics bottleneck: without a derived-zero or numeric C_parent slot there is no MTS WEP prediction",
            "derive/import C_parent_WEP with units, sign convention, basis, parent_status, zero_certificate_status",
            "HIGHEST",
            "MISSING_C_PARENT_IMPORT_FILE",
        ),
        (
            2,
            "PACK1438_3_branch_classifier",
            "P_WEP_same_parent_branch_lock.csv",
            "branch_classifier",
            "basis-integrity bottleneck: prevents mixing surrogate, DD-only, readout, and parent coefficient rows",
            "write strict same_parent_branch_id and forbidden_mixing_rule row after all candidate factors are named",
            "HIGH",
            "MISSING_PARENT_BRANCH_CLASSIFIER_FILE",
        ),
        (
            3,
            "PACK1438_2_product_convention",
            "P_WEP_eta_product_convention.csv",
            "product_convention",
            "comparison bottleneck: eta formula, body order, sign, units, and tau/readout average must be fixed",
            "extract PRL/CQG eta/sign convention and branch-lock it; keep tau_eff=1 forbidden",
            "HIGH",
            "MISSING_PRODUCT_CONVENTION_FILE",
        ),
        (
            4,
            "PACK1438_0_official_readout",
            "P_WEP_K_CMSM_readout.csv",
            "official_readout",
            "readout bottleneck: K_CMSM/orbit/mask columns define how source/material response projects into eta",
            "acquire official CMSM/ONERA readout or reproducible design matrix with required columns",
            "HIGH",
            "MISSING_OFFICIAL_FILE",
        ),
        (
            5,
            "PACK1438_4_material_tensor",
            "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv",
            "derived",
            "material bottleneck: composition/DD smoke is not full same-basis material response",
            "derive full material tensor after C_parent basis is declared; include double-count rule and provenance",
            "MEDIUM_HIGH",
            "MISSING_FULL_MATERIAL_TENSOR_FILE",
        ),
        (
            6,
            "PACK1438_1_source_worldtube",
            "P_WEP_R_source_Earth_worldtube.csv",
            "source_worldtube",
            "source bottleneck: Earth/source vector and orbit/worldtube weights are needed for finite source projection",
            "build/source Earth profile plus orbit/readout projection in same parent basis",
            "MEDIUM_HIGH",
            "MISSING_SOURCE_WORLDTUBE_FILE",
        ),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "priority_rank": rank,
            "manifest_id": manifest_id,
            "target_file": target_file,
            "pack_item": pack_item,
            "why_priority": why_priority,
            "next_action": next_action,
            "priority_class": priority_class,
            "current_status": current_status,
            "score_status": "NOT_SCORE_READY",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rank, manifest_id, target_file, pack_item, why_priority, next_action, priority_class, current_status in specs
    ]


def active_route_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "route_id": "ARS1441_0_axiom_reduction",
            "route": "AX1090 reduction to MTS primitives",
            "route_status": "ATTEMPTED_NOT_REDUCED",
            "result": "minimal WEP clause remains closure-only",
            "claim_consequence": "no derived WEP/local-GR claim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "route_id": "ARS1441_1_source_pack",
            "route": "official/same-basis source-pack acquisition",
            "route_status": "ACTIVE_ONLY_SCORE_ROUTE",
            "result": "ranked but all target files remain missing",
            "claim_consequence": "no score until C_parent and official/source/material/readout/product/branch rows pass parser",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(branch: str) -> list[dict[str, Any]]:
    gates = [
        ("CG1441_0_no_axiom_adoption", "AX1090 rows are not adopted as axioms or derived theorems"),
        ("CG1441_1_closure_only", "minimal WEP parent clause remains closure-only"),
        ("CG1441_2_source_pack_missing", "source-pack target files remain missing and non-score-ready"),
        ("CG1441_3_no_priority_as_progress_claim", "priority ranking is workflow triage, not evidence"),
        ("CG1441_4_no_shortcuts", "no tau_eff=1, measured-G absorption, bound-as-prediction, or surrogate basis mixing"),
        ("CG1441_5_local_gr_blocked", "local-GR/Newton derivation claim remains blocked while WEP/source/matter descent is unresolved"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "LOCKED_CLAIM_FALSE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def decision_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1441_0_axioms_not_reduced",
            "decision": "do not reduce/adopt AX1090 axioms as current MTS derivations",
            "why": "each axiom has a plausible MTS target but still needs a parent action, quotient/category, measure, constant-sector, or variation-order derivation",
            "consequence": "minimal WEP parent clause stays closure-only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1441_1_rank_source_pack",
            "decision": "rank source-pack acquisition with C_parent first, then branch/product/readout/material/source files",
            "why": "finite WEP scoring needs a same-basis MTS prediction before comparing with MICROSCOPE",
            "consequence": "next checkpoint should create the first strict acquisition/import template rather than scoring",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1441_0_1442",
            "next_target": "1442-Y5-R10-RAB-C-parent-WEP-slot-import-template-or-product-branch-first-fill.md",
            "script": "scripts/Y5_R10_RAB_C_parent_WEP_slot_import_template_or_product_branch_first_fill.py",
            "objective": "create the first strict source-pack acquisition/import target: either a C_parent_WEP slot import template with theorem/numeric guards, or the product/branch convention first-fill if C_parent remains unavailable.",
            "include": "C_parent import template; branch/product first-fill option; parser expectations; no-claim gates",
            "exclude": "numeric WEP score; local-GR claim; invented coefficient value; official data fabrication; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_branch_files(reduction: list[dict[str, Any]], priority: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_AX1090_STATUS, reduction)
    write_csv(BRANCH_SOURCE_PRIORITY, priority)


def validation_rows(
    sources: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    dependency: list[dict[str, Any]],
    priority: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        AX1090_REDUCTION_AUDIT,
        AX1090_DEPENDENCY_GRAPH,
        SOURCE_PACK_ACQUISITION_PRIORITY,
        ACTIVE_ROUTE_STATUS,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_AX1090_STATUS,
        BRANCH_SOURCE_PRIORITY,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    truthy_claim_flags: list[str] = []
    for path in csvs:
        try:
            parsed_rows = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue
        for index, row in enumerate(parsed_rows, start=2):
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    sources_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    reductions_safe = all(row["reduction_status"] in {"NOT_REDUCED", "PARTIAL_CONTRACT_NOT_REDUCED"} for row in reduction)
    dependencies_active = all(row["edge_status"] == "ACTIVE_UNPROVED_DEPENDENCY" for row in dependency)
    priority_ranked = [int(row["priority_rank"]) for row in priority] == [1, 2, 3, 4, 5, 6]
    priority_nonclaim = all(row["score_status"] == "NOT_SCORE_READY" for row in priority)
    routes_ok = any(row["route_status"] == "ACTIVE_ONLY_SCORE_ROUTE" for row in routes) and any(
        row["route_status"] == "ATTEMPTED_NOT_REDUCED" for row in routes
    )
    gates_safe = all(row["gate_status"] == "LOCKED_CLAIM_FALSE" for row in gates) and not truthy_claim_flags
    branch_files_ok = BRANCH_AX1090_STATUS.exists() and BRANCH_SOURCE_PRIORITY.exists()
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1441_0_source_register", sources_ok, "all 1441 cited source paths and anchors resolve"),
        ("VAL1441_1_axioms_not_reduced", reductions_safe, "AX1090 reduction audit does not adopt missing axioms"),
        ("VAL1441_2_dependencies_active", dependencies_active, "AX1090 dependency graph remains active/unproved"),
        ("VAL1441_3_priority_ranked", priority_ranked and priority_nonclaim, "source-pack acquisition priorities are ranked and nonclaim"),
        ("VAL1441_4_routes", routes_ok, "axiom route attempted-not-reduced and source-pack route active"),
        ("VAL1441_5_claim_gates", gates_safe, "all claim/valid/prediction flags remain false"),
        ("VAL1441_6_csv_parse", parse_ok, "all generated 1441 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1441_7_branch_files", branch_files_ok, "branch AX1090 status and source priority files written"),
        ("VAL1441_8_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1441_9_next_target", True, "1442 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1441_10_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1441 keeps AX1090 unreduced and ranks the finite WEP source-pack acquisition route without claims",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1441 - AX1090 parent axiom reduction or source-pack acquisition priority",
            "**Current verdict:** AX1090 is not reduced to MTS primitives in the current corpus. The minimal WEP clause remains closure-only, so the official/same-basis source-pack route is the active scoring route.",
            "**Main progress:** the finite WEP route now has a ranked acquisition order: `C_parent_WEP` first, then branch/product/readout/material/source rows, all still nonclaim.",
            "## Source register\n" + md_table(sections["sources"]),
            "## AX1090 reduction audit\n" + md_table(sections["reduction"]),
            "## AX1090 dependency graph\n" + md_table(sections["dependency"]),
            "## Source-pack acquisition priority\n" + md_table(sections["priority"]),
            "## Active route status\n" + md_table(sections["routes"]),
            "## Claim gates\n" + md_table(sections["gates"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    COEFFICIENT_ROOT.mkdir(parents=True, exist_ok=True)
    RESIDUAL_ROOT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    sources = source_register_rows(branch)
    reduction = ax1090_reduction_rows(branch)
    dependency = dependency_graph_rows(branch)
    priority = acquisition_priority_rows(branch)
    routes = active_route_rows(branch)
    gates = claim_gate_rows(branch)
    decisions = decision_rows(branch)
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(AX1090_REDUCTION_AUDIT, reduction)
    write_csv(AX1090_DEPENDENCY_GRAPH, dependency)
    write_csv(SOURCE_PACK_ACQUISITION_PRIORITY, priority)
    write_csv(ACTIVE_ROUTE_STATUS, routes)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    write_branch_files(reduction, priority)

    validation = validation_rows(sources, reduction, dependency, priority, routes, gates)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "reduction": reduction,
            "dependency": dependency,
            "priority": priority,
            "routes": routes,
            "gates": gates,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1441_AX1090_not_reduced_source_pack_priority_ranked_nonclaim")


if __name__ == "__main__":
    main()
