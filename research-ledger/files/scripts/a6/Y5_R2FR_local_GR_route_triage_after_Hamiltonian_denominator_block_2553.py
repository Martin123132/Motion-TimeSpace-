from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2553"
BRANCH_ID = "MTS_R2FR_LOCAL_GR_ROUTE_TRIAGE_AFTER_HAMILTONIAN_DENOMINATOR_BLOCK_2553"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SCRIPTS = ROOT / "scripts"

DOC = ROOT / "2553-Y5-R2FR-local-GR-route-triage-after-Hamiltonian-denominator-block.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2553_SOURCE_REGISTER.csv",
    "route_triage": OUT / "P8_Y5_NO_SHADOW_2553_LOCAL_GR_ROUTE_TRIAGE.csv",
    "prerequisite_matrix": OUT / "P8_Y5_NO_SHADOW_2553_PREREQUISITE_MATRIX.csv",
    "quick_test_paths": OUT / "P8_Y5_NO_SHADOW_2553_QUICK_TEST_PATHS.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2553_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2553_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2553_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2553_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2553_VALIDATION.csv",
}

COPY_TARGETS = {
    "local_route_triage": LOCAL_BOUNDS / "Local_GR_route_triage_2553_NONCLAIM.csv",
    "parent_action_requirements": QUEUE / "JR2553_PARENT_ACTION_SKELETON_REQUIREMENTS_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2553_00_2552_doc",
        "source_path": ROOT / "2552-Y5-R2FR-minimal-parent-current-chain-promotion-or-denominator-final-block.md",
        "needles": ["TQV2552_1_current_promotion", "DFB2552_0_MHref_unavailable", "NEXT2552_0_selected", "VAL2552_OVERALL"],
        "role": "active handoff proving the Hamiltonian denominator route is blocked for current corpus",
    },
    {
        "source_id": "SRC2553_01_2552_denominator_block",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2552_DENOMINATOR_FINAL_BLOCK.csv",
        "needles": ["DFB2552_0_MHref_unavailable", "UNAVAILABLE_UNTIL_NEW_PARENT_ACTION_MATERIAL"],
        "role": "machine-readable denominator final block",
    },
    {
        "source_id": "SRC2553_02_2552_reopen_material",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2552_REOPEN_MATERIAL_SPEC.csv",
        "needles": ["MAT2552_0_action_source", "MAT2552_3_GK_pack", "MAT2552_4_source_pack"],
        "role": "minimum material required to reopen parent-action route",
    },
    {
        "source_id": "SRC2553_03_2552_next_target",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2552_NEXT_TARGET.csv",
        "needles": ["NEXT2552_0_selected", "2553-Y5-R2FR-local-GR-route-triage-after-Hamiltonian-denominator-block.md"],
        "role": "explicit route-triage instruction",
    },
    {
        "source_id": "SRC2553_04_1010_gk_residual",
        "source_path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "needles": ["GKT1010_6_verdict", "QRES1010_0_q_loc_vector", "DEC1010_0_derivation_route_precise", "V1010_SUMMARY"],
        "role": "sharpest q_loc/Gamma-Khat nonclosure and route-to-proof statement",
    },
    {
        "source_id": "SRC2553_05_symbol_map",
        "source_path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "needles": ["q_loc^nu", "not_derived_zero; plateau_axiom_forbidden", "Pi_M"],
        "role": "symbol-level local-GR block map",
    },
    {
        "source_id": "SRC2553_06_variation_gates",
        "source_path": OUT / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        "needles": ["FV512_2_Gamma_Khat_q", "fail_for_current_claim"],
        "role": "first-variation gates for local residual sector",
    },
    {
        "source_id": "SRC2553_07_min_action_blocks",
        "source_path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "needles": ["A511_5_boundary_reference", "worldtube/source-measure equality shifts by boundary bookkeeping"],
        "role": "minimum local-GR action blocks and boundary/source warning",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: bool) -> str:
    return "true" if value else "false"


def base_row(valid_for_claim: bool = False, claim_allowed: bool = False) -> dict[str, str]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": truth(valid_for_claim),
        "claim_allowed": truth(claim_allowed),
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def cell(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def inside_root(path: Path) -> bool:
    resolved = path.resolve()
    root = ROOT.resolve()
    return resolved == root or root in resolved.parents


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                **base_row(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": truth(path.exists()),
                "missing_needles": ";".join(missing),
                "source_pass": truth(path.exists() and not missing),
                "role": source["role"],
            }
        )
    return rows


def route_triage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "LGR2553_R0_new_parent_action_skeleton",
            "route_name": "new parent-action skeleton",
            "route_type": "derivation_first",
            "score_derivability": 5,
            "score_scrutiny_resilience": 5,
            "score_speed": 2,
            "score_alignment": 5,
            "current_status": "SELECTED_PRIMARY_NEXT_ROUTE",
            "claim_ceiling": "none_now; if completed, can become a true GR/Newton reduction route",
            "required_inputs": "MAT2552_0_action_source; MAT2552_1_variation_pack; MAT2552_3_GK_pack; MAT2552_4_source_pack; fixed reference only after parent action",
            "fastest_discriminator": "write minimal covariant action skeleton and test whether variation can produce q_loc without plateau axiom or orbital-GM normalization",
            "failure_condition": "if q_loc/Gamma-Khat and Pi_M/worldtube cannot be generated as Euler/source terms from one parent action",
            "next_action": "build 2554 minimal parent-action skeleton focused on q_loc and source bridge",
            "selected_role": "primary",
        },
        {
            "route_id": "LGR2553_R1_direct_q_loc_residual_bounds",
            "route_name": "direct q_loc residual bounds",
            "route_type": "finite_bound_fallback",
            "score_derivability": 3,
            "score_scrutiny_resilience": 4,
            "score_speed": 4,
            "score_alignment": 4,
            "current_status": "KEEP_AS_FALLBACK",
            "claim_ceiling": "bounded local residual only; not a derivation of GR",
            "required_inputs": "physical q_loc profile; projection to PPN, clocks, orbital systems, R10; units and source normalisation independent of fitted GM",
            "fastest_discriminator": "derive or bound q_loc from source-worldtube geometry and test whether residual is below existing local arenas",
            "failure_condition": "if q_loc requires an arbitrary plateau or if normalization smuggles observed gravity back in",
            "next_action": "keep rows source-ready but do not spend as local-GR proof",
            "selected_role": "fallback",
        },
        {
            "route_id": "LGR2553_R2_non_Hamiltonian_normalization",
            "route_name": "non-Hamiltonian local normalization",
            "route_type": "normalization_alternative",
            "score_derivability": 3,
            "score_scrutiny_resilience": 3,
            "score_speed": 3,
            "score_alignment": 3,
            "current_status": "CONDITIONAL_ONLY",
            "claim_ceiling": "dimensionless residual scoring if a same-frame local geometric norm is derived",
            "required_inputs": "same-frame geometric norm; no orbital GM denominator; proof norm is nonzero, positive, and source-owned",
            "fastest_discriminator": "try to construct a norm from local curvature/source charge that is not just M_H_ref renamed",
            "failure_condition": "if denominator is fitted, reference-tuned, or observationally borrowed",
            "next_action": "defer until 2554 says whether parent-action route needs a normalization fallback",
            "selected_role": "secondary",
        },
        {
            "route_id": "LGR2553_R3_empirical_only_deferral",
            "route_name": "empirical-only deferral",
            "route_type": "data_pressure_only",
            "score_derivability": 1,
            "score_scrutiny_resilience": 2,
            "score_speed": 5,
            "score_alignment": 2,
            "current_status": "NOT_ENOUGH_FOR_GOAL",
            "claim_ceiling": "phenomenology only; cannot carry unified-field or local-GR claim",
            "required_inputs": "robust cosmology/galaxy/local fits with honest baselines",
            "fastest_discriminator": "run data comparisons, but treat wins as motivation rather than derivation",
            "failure_condition": "if data success is used to bypass GR/Newton reduction proof",
            "next_action": "do not select as next local-GR route",
            "selected_role": "deferred",
        },
        {
            "route_id": "LGR2553_R4_closure_axiom_or_plateau",
            "route_name": "closure axiom / local plateau",
            "route_type": "forbidden_shortcut",
            "score_derivability": 0,
            "score_scrutiny_resilience": 0,
            "score_speed": 5,
            "score_alignment": 0,
            "current_status": "REJECTED",
            "claim_ceiling": "none; would be closure-only and too weak for claimed GR reduction",
            "required_inputs": "not applicable",
            "fastest_discriminator": "any F1=0, double-zero, or local silence asserted without parent variational source fails",
            "failure_condition": "automatic failure for current programme standards",
            "next_action": "keep forbidden",
            "selected_role": "rejected",
        },
    ]
    return [{**base_row(), **row} for row in rows]


def prerequisite_rows() -> list[dict[str, Any]]:
    rows = [
        ("PRE2553_0_field_inventory", "LGR2553_R0_new_parent_action_skeleton", "complete parent field inventory", "g_obs or g, tau/coframe, matter Psi, Gamma_eff, K_hat, Pi_M/source map, domain/projector and beta_ref are either included or explicitly demoted", "2552 material spec requires action source and variation pack", "MISSING", "single source field list", "blocks current local-GR claim"),
        ("PRE2553_1_variational_origin_q_loc", "LGR2553_R0_new_parent_action_skeleton", "q_loc generated by first variation", "Euler/Noether chain must produce P_loc(nabla Gamma_eff - nabla_mu K_hat^{mu nu}) or an exactly equivalent residual", "1010 retains q_loc as nonclaim residual", "MISSING", "S_GK, Helmholtz/integrability, Euler equation and projection map", "blocks theorem-zero route"),
        ("PRE2553_2_source_bridge", "LGR2553_R0_new_parent_action_skeleton", "Pi_M/worldtube/source bridge", "source charge must come from parent matter/worldtube current, not fitted orbital GM or observed mass readout", "2552 identifies Pi_M/worldtube as co-hardest block", "MISSING", "parent-owned source current and linking surface convention", "blocks Newton limit"),
        ("PRE2553_3_fixed_reference_late", "LGR2553_R0_new_parent_action_skeleton", "fixed reference only after parent ownership", "H_ref/B_ref/counterterms must be fixed before readout and cannot define the source normalization", "2552 final-blocks M_H_ref until new parent material", "MISSING", "reference/counterterm convention tied to parent action", "blocks denominator reuse"),
        ("PRE2553_4_local_vacuum_double_zero", "LGR2553_R0_new_parent_action_skeleton", "local vacuum double-zero", "linear and first-gradient local residual terms vanish by Euler/source equations, not by plateau axiom", "symbol map forbids not-derived plateau", "MISSING", "F1=0 and Delta m bound from variational equations", "blocks PPN pass"),
        ("PRE2553_5_direct_bound_units", "LGR2553_R1_direct_q_loc_residual_bounds", "direct residual units and projections", "q_loc amplitude must map to R10, PPN, clocks and orbital arenas with explicit units and signs", "earlier local-bound rows are nonclaim", "MISSING", "arena projection coefficients and sourced local profile", "allows only bounded residual fallback"),
        ("PRE2553_6_non_Hamiltonian_norm", "LGR2553_R2_non_Hamiltonian_normalization", "same-frame geometric norm", "normalizer must be positive, local, parent/source-owned and not observationally fitted", "Hamiltonian denominator unavailable", "MISSING", "candidate norm and positivity proof", "allows only dimensionless scoring fallback"),
    ]
    return [
        {
            **base_row(),
            "prereq_id": prereq_id,
            "owning_route": route,
            "requirement": requirement,
            "acceptance_rule": acceptance_rule,
            "current_evidence": current_evidence,
            "current_status": current_status,
            "missing_material": missing_material,
            "claim_effect": claim_effect,
        }
        for prereq_id, route, requirement, acceptance_rule, current_evidence, current_status, missing_material, claim_effect in rows
    ]


def quick_test_rows() -> list[dict[str, Any]]:
    rows = [
        ("QTP2553_0_action_skeleton_closure", "LGR2553_R0_new_parent_action_skeleton", "parent action closure dry-run", "candidate S_parent sector list", "all retained variables have an Euler/source/boundary owner", "any retained q_loc/Gamma-Khat/Pi_M variable is orphaned", "symbolic audit", "false", "SELECTED_FOR_2554"),
        ("QTP2553_1_linearized_local_vacuum", "LGR2553_R0_new_parent_action_skeleton", "linearized vacuum residual test", "weak-field local vacuum expansion", "O(h) and O(partial h) pieces cancel by field equations", "F1=0 is asserted rather than derived", "derivation gate", "false", "PENDING_PARENT_ACTION"),
        ("QTP2553_2_source_Ward_bridge", "LGR2553_R0_new_parent_action_skeleton", "source Ward bridge test", "matter/worldtube current and Pi_M map", "source mass/charge in Newton limit equals parent current integral", "observed GM or fitted mask enters as definition", "derivation gate", "false", "PENDING_PARENT_ACTION"),
        ("QTP2553_3_direct_q_loc_bound_smoke", "LGR2553_R1_direct_q_loc_residual_bounds", "direct q_loc bound smoke", "candidate q_loc profile and arena coefficients", "all units numeric and every row remains nonclaim until sourced", "placeholder coefficients are treated as evidence", "runner smoke", "false", "FALLBACK_ONLY"),
        ("QTP2553_4_non_Hamiltonian_norm_smoke", "LGR2553_R2_non_Hamiltonian_normalization", "non-Hamiltonian norm smoke", "candidate geometric normalizer", "positive same-frame norm derived without M_H_ref", "normalizer reuses orbital GM, fitted mass or reference cancellation", "symbolic/numeric audit", "false", "DEFERRED"),
    ]
    return [
        {
            **base_row(),
            "test_id": test_id,
            "route_id": route_id,
            "test_name": test_name,
            "dry_run_input": dry_run_input,
            "pass_rule": pass_rule,
            "fail_rule": fail_rule,
            "output_type": output_type,
            "long_run_required": long_run_required,
            "status": status,
        }
        for test_id, route_id, test_name, dry_run_input, pass_rule, fail_rule, output_type, long_run_required, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2553_0_no_local_GR_claim", "No local-GR/Newton/PPN claim from 2553.", "BLOCKED", "2553 is route triage only and inherits 2552 denominator block", "false"),
        ("GATE2553_1_no_MHref_reopen", "Do not reopen M_H_ref/N_E without MAT2552 material.", "PASS_GUARDRAIL", "selected route starts a new parent-action skeleton rather than spending M_H_ref", "false"),
        ("GATE2553_2_no_plateau_axiom", "No local plateau or closure axiom as proof.", "PASS_GUARDRAIL", "closure axiom route is rejected", "false"),
        ("GATE2553_3_best_route_selected", "A next derivation route is selected.", "PASS_AS_WORKFLOW", "new parent-action skeleton is selected as primary because it is the only route that can actually derive GR reduction", "false"),
        ("GATE2553_4_direct_bounds_nonclaim", "Direct q_loc bounds remain fallback nonclaim.", "PASS_GUARDRAIL", "direct bound route can discipline the theory but cannot replace derivation", "false"),
    ]
    return [
        {
            **base_row(),
            "gate_id": gate_id,
            "claim": claim,
            "gate_status": gate_status,
            "reason": reason,
            "claim_allowed": claim_allowed,
        }
        for gate_id, claim, gate_status, reason, claim_allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2553_0_denominator_not_retried", "Do not retry the Hamiltonian denominator branch in 2553.", "2552 already final-blocked M_H_ref/N_E for current corpus", "prevents circular work"),
        ("DEC2553_1_select_parent_action", "Select a new parent-action skeleton as the primary route.", "it is slower but is the only route with a ceiling high enough to derive GR/Newton reduction", "2554 will attempt the constructive leap"),
        ("DEC2553_2_keep_bounds_fallback", "Keep direct q_loc residual bounds as a fallback.", "bounds are useful for falsifiability and local tests but cannot be sold as derivation", "local-bound rows remain nonclaim"),
        ("DEC2553_3_reject_closure_axiom", "Reject closure axioms and plateau assertions.", "the project standard is derivation-first; closure-only would be too easy to criticize", "no theorem-zero by assertion"),
        ("DEC2553_4_next_target", "Move to 2554 parent-action skeleton.", "this attacks the hardest missing coupling/source origin instead of circling the same denominator", "next work becomes constructive rather than forensic"),
    ]
    return [
        {
            **base_row(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "effect": effect,
        }
        for decision_id, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2553_0_selected",
            "selection_status": "selected",
            "target_file": "2554-Y5-R2FR-minimal-parent-action-skeleton-for-q_loc-and-source-bridge.md",
            "target_script": "scripts/Y5_R2FR_minimal_parent_action_skeleton_for_q_loc_and_source_bridge_2554.py",
            "task": "construct the smallest parent-action skeleton that could own Gamma/Khat/q_loc and Pi_M/worldtube source bridge, then fail it honestly if any retained variable remains orphaned",
            "acceptance_target": "explicit field list, candidate action terms, variation ownership table, q_loc/source bridge derivation attempts, and nonclaim gates",
            "guardrails": "no M_H_ref reuse; no orbital-GM denominator; no plateau axiom; no local-GR claim; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["route_triage"], COPY_TARGETS["local_route_triage"])
    shutil.copyfile(OUTPUTS["prerequisite_matrix"], COPY_TARGETS["parent_action_requirements"])
    rows = []
    for copy_id, target in COPY_TARGETS.items():
        source = OUTPUTS["route_triage"] if copy_id == "local_route_triage" else OUTPUTS["prerequisite_matrix"]
        rows.append(
            {
                **base_row(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": truth(source.exists()),
                "target_exists": truth(target.exists()),
            }
        )
    return rows


def csv_parse_status(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:
        return False, 0, repr(exc)


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    artifact_markers = (
        "2553-Y5",
        "_2553_",
        "_2553.",
        "JR2553",
        "P8_Y5_NO_SHADOW_2553",
        "P8_Y5_BRR545_2553",
        "Y5_R2FR_local_GR_route_triage_after_Hamiltonian_denominator_block_2553",
    )
    return [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in artifact_markers)
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    prereqs: list[dict[str, Any]],
    tests: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail})

    add("VAL2553_00_sources_exist", all(row["source_pass"] == "true" for row in sources), "all cited source paths exist and needles are present", ";".join(row["source_id"] for row in sources if row["source_pass"] != "true"))
    add("VAL2553_01_routes_complete", len(routes) >= 5, "route triage covers parent action, direct bounds, non-Hamiltonian normalization, empirical deferral and closure rejection", str(len(routes)))
    add("VAL2553_02_primary_route_selected", any(row["selected_role"] == "primary" and row["current_status"] == "SELECTED_PRIMARY_NEXT_ROUTE" for row in routes), "primary derivation route selected")
    add("VAL2553_03_all_routes_nonclaim", all(row["claim_allowed"] == "false" for row in routes), "route triage makes no claim")
    add("VAL2553_04_prereqs_written", len(prereqs) >= 7 and all(row["current_status"] == "MISSING" for row in prereqs), "missing prerequisites are explicit")
    add("VAL2553_05_quick_tests_written", len(tests) >= 5, "quick falsification paths are written")
    add("VAL2553_06_claim_gates_safe", all(row["claim_allowed"] == "false" for row in gates), "local-GR claims remain blocked")
    add("VAL2553_07_decisions_written", len(decisions) >= 5, "decision ledger written")
    add("VAL2553_08_next_target_written", bool(next_rows) and next_rows[0]["route_id"] == "NEXT2553_0_selected", "2554 parent-action skeleton target selected")
    add("VAL2553_09_branch_copies", all(row["source_exists"] == "true" and row["target_exists"] == "true" for row in branch_rows), "nonclaim branch copies exist")
    add("VAL2553_10_no_formalization_artifacts", not formalization_hits(), "no 2553 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_hits()))
    add("VAL2553_11_all_outputs_inside_post_checkpoint", all(inside_root(path) for path in list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]), "all 2553 outputs stay inside post-checkpoint-work")
    add("VAL2553_12_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent after cleanup")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2553_CSV_{path.stem}", ok and count > 0, f"CSV parses with {count} rows" if ok else "CSV parse failed", detail or str(path))

    for copy_id, path in COPY_TARGETS.items():
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2553_COPY_CSV_{copy_id}", ok and count > 0, f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed", detail or str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2553_OVERALL", overall, "2553 selects new parent-action skeleton as primary route while keeping all local-GR claims blocked")
    return [{**base_row(), **row} for row in rows]


def write_doc(
    sources: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    prereqs: list[dict[str, Any]],
    tests: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2553 Y5 R2FR Local GR Route Triage After Hamiltonian Denominator Block",
        "",
        "**Result:** route triage complete. The Hamiltonian denominator route is not reopened. The primary next route is a new parent-action skeleton aimed directly at the missing coupling/source origin: Gamma/Khat/q_loc plus Pi_M/worldtube. Direct q_loc bounds are retained as a fallback, not as a GR derivation.",
        "",
        "**Private reading:** this is the anti-circling checkpoint. The best route is not the fastest route; it is the route with a ceiling high enough to reduce to GR/Newton without smuggling in the result. If 2554 cannot even write an honest parent skeleton, the programme should pivot to bounded-residual nonclaim mode rather than pretend local GR has been derived.",
        "",
        "## Source Register",
        markdown_table(sources, ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Route Triage",
        markdown_table(routes, ["route_id", "route_name", "route_type", "score_derivability", "score_scrutiny_resilience", "score_speed", "score_alignment", "current_status", "claim_ceiling", "fastest_discriminator", "selected_role"]),
        "",
        "## Prerequisite Matrix",
        markdown_table(prereqs, ["prereq_id", "owning_route", "requirement", "acceptance_rule", "current_evidence", "current_status", "missing_material", "claim_effect"]),
        "",
        "## Quick Test Paths",
        markdown_table(tests, ["test_id", "route_id", "test_name", "dry_run_input", "pass_rule", "fail_rule", "output_type", "long_run_required", "status"]),
        "",
        "## Claim Gates",
        markdown_table(gates, ["gate_id", "claim", "gate_status", "reason", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(decisions, ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(branch_rows, ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(validations, ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    routes = route_triage_rows()
    prereqs = prerequisite_rows()
    tests = quick_test_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["route_triage"], routes)
    write_csv(OUTPUTS["prerequisite_matrix"], prereqs)
    write_csv(OUTPUTS["quick_test_paths"], tests)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validations = validation_rows(sources, routes, prereqs, tests, gates, decisions, next_rows, branch_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, routes, prereqs, tests, gates, decisions, next_rows, branch_rows, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
