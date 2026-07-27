from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1277"
TITLE = "1277-Y5-R10-RAB-local-EH-fixed-point-inheritance-or-explicit-closure-runner"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
INHERITANCE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_EH_FIXED_POINT_INHERITANCE_AUDIT.csv"
CONDITIONAL_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_CONDITIONAL_EH_INHERITANCE_THEOREM.csv"
CLOSURE_RUNNER_PATH = OUT_DIR / f"{PACK_ID}_EXPLICIT_CLOSURE_RUNNER_SPEC.csv"
DERIVATION_PRIORITY_PATH = OUT_DIR / f"{PACK_ID}_A511_ORIGIN_PRIORITY_LADDER.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1277_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def contains_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def validate_intake_row(path: Path, intake_class: str, row: dict[str, str]) -> dict[str, object]:
    row_id = row.get("row_id") or row.get("template_id") or row.get("coefficient_symbol") or "MISSING_ROW_ID"
    required_columns = [
        "coefficient_symbol",
        "coefficient_value",
        "coefficient_units",
        "normalization_convention",
        "parent_action_block",
        "source_path",
        "source_anchor",
        "arena_projection",
        "valid_for_claim",
        "claim_allowed",
    ]
    missing_columns = [column for column in required_columns if column not in row]
    source_raw = str(row.get("source_path", "")).strip()
    anchor = str(row.get("source_anchor", "")).strip()
    source = None if not source_raw or source_raw.startswith("MISSING_") else source_path(source_raw)
    source_exists = bool(source and source.exists())
    anchor_found = bool(source_exists and anchor and not anchor.startswith("MISSING_") and anchor in read_text(source))
    reasons: list[str] = []
    if intake_class == "docs":
        reasons.append("DOCS_TEMPLATE_NOT_LIVE_INTAKE")
    if missing_columns:
        reasons.append("MISSING_REQUIRED_COLUMNS:" + ";".join(missing_columns))
    if contains_missing_marker(row):
        reasons.append("MISSING_MARKER_PRESENT")
    if source is None:
        reasons.append("SOURCE_PATH_MISSING_OR_PLACEHOLDER")
    elif not source_exists:
        reasons.append("SOURCE_PATH_NOT_FOUND")
    if not anchor or anchor.startswith("MISSING_"):
        reasons.append("SOURCE_ANCHOR_MISSING_OR_PLACEHOLDER")
    elif source_exists and not anchor_found:
        reasons.append("SOURCE_ANCHOR_NOT_FOUND")
    if str(row.get("valid_for_claim", "")).strip().lower() == "true" or str(row.get("claim_allowed", "")).strip().lower() == "true":
        reasons.append("CLAIM_FLAG_TRUE_REJECTED_IN_PRIVATE_NONCLAIM_PHASE")
    return {
        "scan_id": f"SCAN1277_{intake_class}_{path.stem}_{row_id}",
        "intake_class": intake_class,
        "file_path": str(path),
        "row_id": row_id,
        "coefficient_symbol": row.get("coefficient_symbol", ""),
        "status": "REJECT" if reasons else "ACCEPT_NONCLAIM_SOURCE_READY",
        "reasons": "|".join(reasons) if reasons else "NO_PLACEHOLDERS_SOURCE_ANCHOR_FOUND_NONCLAIM",
        "source_exists": source_exists,
        "anchor_found": anchor_found,
        "intake_eligible": not reasons,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def scan_rab_intake() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for intake_class in ["docs", "raw", "accepted"]:
        directory = RAB_INTAKE_DIR / intake_class
        directory.mkdir(parents=True, exist_ok=True)
        for path in sorted(directory.glob("*.csv")):
            for row in read_csv(path):
                results.append(validate_intake_row(path, intake_class, row))
    return results


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        INHERITANCE_AUDIT_PATH,
        CONDITIONAL_THEOREM_PATH,
        CLOSURE_RUNNER_PATH,
        DERIVATION_PRIORITY_PATH,
        VALIDATOR_RESCAN_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1277_0_1276_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1276_NEXT_TARGET.csv",
            "needle": "NEXT1276_0_1277",
            "purpose": "handoff into EH fixed-point inheritance gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1277_1_1276_coverage",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1276_A511_ACTION_BLOCK_COVERAGE.csv",
            "needle": "AC1276_0_EH_core",
            "purpose": "A511 action-block coverage from 1276",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1277_2_1276_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1276_PARENT_EULER_SOURCE_CONTRACT.csv",
            "needle": "ESC1276_1_local_EH_fixed_point",
            "purpose": "local EH fixed-point contract from 1276",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1277_3_A511_blocks",
            "local_path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "needle": "A511_6_metric_readout",
            "purpose": "candidate minimum parent local-GR action blocks",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1277_4_1009_EH_anchor",
            "local_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needle": "SVC1009_0_EH_anchor_only",
            "purpose": "prior audit marks EH block as anchor-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1277_5_1009_total_action",
            "local_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needle": "CG1009_0_total_parent_action",
            "purpose": "prior audit blocks total parent action acceptance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1277_6_zero_chain",
            "local_path": "source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_VARIATION_CHAIN.csv",
            "needle": "V5_delta_g_stress",
            "purpose": "metric-stress and source-normalization debts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1277_7_symbol_map",
            "local_path": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            "needle": "Pi_M",
            "purpose": "readout/projector and source-measure map debts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1277_8_closure_scorecard",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1276_CLOSURE_BASELINE_SCORECARD.csv",
            "needle": "CS1276_4_overall",
            "purpose": "explicit closure baseline scorecard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1277_9_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "finite residual source rows remain absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    inheritance_audit = [
        {
            "audit_id": "EHI1277_0_parent_action_acceptance",
            "A511_block": "A511_all",
            "inheritance_clause": "total parent action is accepted as MTS-owned local fixed-point action",
            "evidence": "1009 claim gate CG1009_0_total_parent_action is false",
            "status": "FAIL_CURRENT_CORPUS",
            "failure_mode": "sector action blocks are candidates, not a signed parent action",
            "would_unlock": "all later EH inheritance checks could become meaningful",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "EHI1277_1_EH_core",
            "A511_block": "A511_0_EH_core",
            "inheritance_clause": "local spin-2 operator is EH and MTS-derived",
            "evidence": "1009 marks SVC1009_0_EH_anchor_only; 1276 marks candidate reference not MTS-derived",
            "status": "ANCHOR_ONLY_NOT_INHERITED",
            "failure_mode": "EH core can be a benchmark or fixed-point target, but not proof by itself",
            "would_unlock": "E_time/E_radial can use EH equations after inheritance is proved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "EHI1277_2_kappa_constant",
            "A511_block": "A511_1_kappa_topological",
            "inheritance_clause": "local coupling is constant and topological/global, not source or domain dependent",
            "evidence": "A511_1 is candidate; 1276 marks not adopted as parent theorem",
            "status": "UNSIGNED",
            "failure_mode": "G_eff/kappa drift remains a residual",
            "would_unlock": "source normalization and D_R coefficient stability",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "EHI1277_3_universal_matter",
            "A511_block": "A511_2_universal_matter",
            "inheritance_clause": "matter couples universally to g_obs and defines same Hilbert/source current",
            "evidence": "symbol map says same-frame source theorem is not parent-derived",
            "status": "UNSIGNED_SOURCE_MAP",
            "failure_mode": "source mass, orbital mass, and Hamiltonian mass can separate",
            "would_unlock": "S_R source-balance map for local vacuum/exteriors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "EHI1277_4_extra_silence",
            "A511_block": "A511_3_extra_field_silence",
            "inheritance_clause": "motion/time/domain/memory/range fields have zero first variation/stress in local branch",
            "evidence": "V5_delta_g_stress and V7_R11_source leave metric stress and non-EH source debts",
            "status": "BLOCKED_BY_STRESS_DEBT",
            "failure_mode": "extra fields can create scalar/vector/tensor hair or source-normalized residuals",
            "would_unlock": "clean EH local fixed point without MTS residual stress",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "EHI1277_5_domain_projector",
            "A511_block": "A511_4_domain_projector_selector",
            "inheritance_clause": "domain/projector variables vanish or become topological on local stationary compact branch",
            "evidence": "V4_delta_chi_D_or_D fails for claim; V6_boundary_flux fails for alpha3/preferred momentum",
            "status": "BLOCKED_BY_PROJECTOR_AND_BOUNDARY",
            "failure_mode": "preferred-frame or source-normalization patch can leak into local equations",
            "would_unlock": "projector silence in E_time-E_radial",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "EHI1277_6_boundary_reference",
            "A511_block": "A511_5_boundary_reference",
            "inheritance_clause": "boundary/reference variation is fixed, topological, or vanishing",
            "evidence": "1276 keeps boundary/no-charge normalization blocked; 1009 keeps H_tau/M_H_ref/local-GR gates closed",
            "status": "BLOCKED_BY_BOUNDARY_REFERENCE",
            "failure_mode": "hidden boundary mass flux or Q_R hair can remain",
            "would_unlock": "Q_R=0 and C_R normalization after integration",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "EHI1277_7_metric_readout",
            "A511_block": "A511_6_metric_readout",
            "inheritance_clause": "g_readout=g_obs+O((Phi-Phi0)^2) and Pi_M=Pi_EH+silent terms",
            "evidence": "symbol map marks Pi_M and M_eff/M_source as not parent-derived",
            "status": "BLOCKED_BY_READOUT_PROJECTOR",
            "failure_mode": "Newton/PPN/R10 readout can receive first-order leakage or calibration residuals",
            "would_unlock": "local test branch can inherit EH readout consistently",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "EHI1277_8_verdict",
            "A511_block": "A511_all",
            "inheritance_clause": "MTS inherits local EH fixed point with silent extras",
            "evidence": "EHI1277_0..7 contain multiple unsigned clauses",
            "status": "EH_FIXED_POINT_NOT_INHERITED",
            "failure_mode": "current corpus has a useful scaffold but not a derivation",
            "would_unlock": "GR-style D_R route can reopen only after all rows pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    conditional_theorem = [
        {
            "theorem_id": "CEH1277_0_if_all_A511_signed",
            "conditional_statement": "If A511_0..A511_6 are parent-signed and all extra first variations vanish/source-bound, then MTS has a local EH fixed point.",
            "then_result": "Use EH Euler equations as an inherited local limit, not as an import.",
            "current_status": "CONDITIONAL_ONLY",
            "missing_certificate": "all A511 ownership/silence/readout/boundary/source certificates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "CEH1277_1_then_DR",
            "conditional_statement": "If local EH fixed point is inherited, static spherical source-balanced exteriors may use the GR-style time-radial equation difference.",
            "then_result": "D_R yields C_R=constant and source/boundary gates can set C_R=0.",
            "current_status": "DOWNSTREAM_CONDITIONAL",
            "missing_certificate": "CEH1277_0 plus source-balance and boundary normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "CEH1277_2_current_verdict",
            "conditional_statement": "Current corpus does not satisfy CEH1277_0 or CEH1277_1.",
            "then_result": "local branch remains closure-only or finite-residual-scored after source rows exist",
            "current_status": "NOT_CLOSED",
            "missing_certificate": "EH fixed point, source map, boundary no-charge, finite rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_runner = [
        {
            "runner_id": "ECR1277_0_inputs",
            "branch": "local_closure_baseline",
            "required_inputs": "C_R=0; Q_R=0; S_R=0; C_R_boundary=0",
            "runner_behavior": "label outputs closure_only=true and derived_local_GR=false",
            "claim_status": "NONCLAIM_CONTROL_BRANCH",
            "do_not": "do not compare as parent-derived MTS local-GR pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "ECR1277_1_allowed_outputs",
            "branch": "local_closure_baseline",
            "required_inputs": "explicit closure flags from 1275/1276",
            "runner_behavior": "may produce benchmark residual vector for Newton/PPN/R10/clocks/orbits",
            "claim_status": "INTERNAL_BENCHMARK_ONLY",
            "do_not": "do not mix closure rows with finite residual rows in one score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "ECR1277_2_finite_branch",
            "branch": "finite_residual",
            "required_inputs": "source-backed Z_R/W/J_R/Q_R/tau rows passing validator",
            "runner_behavior": "score finite residual only after rows are accepted",
            "claim_status": "LOCKED_NO_ROWS",
            "do_not": "do not use placeholder templates as data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "ECR1277_3_inheritance_branch",
            "branch": "EH_inheritance",
            "required_inputs": "CEH1277_0 and CEH1277_1 pass",
            "runner_behavior": "only then mark inherited_local_EH=true and attempt derived local-GR claim gates",
            "claim_status": "BLOCKED",
            "do_not": "do not treat EH anchor-only block as inheritance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    priority_ladder = [
        {
            "priority_id": "APL1277_0_extra_silence",
            "target": "A511_3_extra_field_silence",
            "why_first": "without extra-sector silence the EH fixed point is contaminated regardless of the EH core",
            "next_test": "derive double-zero/Hessian/source silence for retained motion/time/domain/memory/range fields",
            "status": "HIGH_PRIORITY_OPEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "APL1277_1_readout_projector",
            "target": "A511_6_metric_readout",
            "why_first": "even a silent field can re-enter through g_readout or Pi_M",
            "next_test": "prove no first-order readout/projector leakage and same-frame mass projector",
            "status": "HIGH_PRIORITY_OPEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "APL1277_2_universal_matter",
            "target": "A511_2_universal_matter",
            "why_first": "source-balance and WEP/source-measure equality depend on universal coupling",
            "next_test": "derive same observed coframe/source current for matter and clocks",
            "status": "HIGH_PRIORITY_OPEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "APL1277_3_boundary_reference",
            "target": "A511_5_boundary_reference",
            "why_first": "AB=constant becomes AB=1 only after no-charge/boundary normalization",
            "next_test": "derive Q_R=0 and fixed reference boundary class",
            "status": "OPEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "APL1277_4_closure_runner",
            "target": "explicit closure runner",
            "why_first": "testing can proceed safely while derivations are open",
            "next_test": "implement runner flags that separate closure baseline, finite residual, and inherited-EH branches",
            "status": "SELECTED_PARALLEL_PRACTICAL_TARGET",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    validator_rescan = scan_rab_intake()
    docs_rows = [row for row in validator_rescan if row["intake_class"] == "docs"]
    raw_rows = [row for row in validator_rescan if row["intake_class"] == "raw"]
    accepted_rows = [row for row in validator_rescan if row["intake_class"] == "accepted"]
    accepted_ready = [row for row in validator_rescan if row["intake_eligible"] and row["intake_class"] in {"raw", "accepted"}]

    claim_gates = [
        {
            "gate_id": "GATE1277_0_EH_inheritance",
            "claim": "MTS inherits local EH fixed point",
            "status": "BLOCKED",
            "reason": "A511 action blocks remain scaffold/anchor-only with unsigned silence and readout clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1277_1_GR_DR",
            "claim": "GR-style D_R is legitimate MTS-derived local equation",
            "status": "BLOCKED",
            "reason": "requires EH inheritance plus source/boundary gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1277_2_closure_runner",
            "claim": "explicit closure runner spec is written",
            "status": "PASS_NONCLAIM",
            "reason": "closure branch can be used as internal benchmark only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1277_3_finite_rows",
            "claim": "finite residual branch can be scored",
            "status": "BLOCKED",
            "reason": f"docs={len(docs_rows)} raw={len(raw_rows)} accepted={len(accepted_rows)} accepted_ready={len(accepted_ready)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1277_4_local_tests",
            "claim": "local GR/Newton/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "inherited-EH branch blocked; closure branch nonclaim; finite branch has no accepted rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1277_0_EH_inheritance_result",
            "decision": "do not promote A511 scaffold to local EH fixed point",
            "because": "multiple A511 clauses are unsigned and 1009 blocks total parent action acceptance",
            "status": "EH_INHERITANCE_FAILED_CURRENT_CORPUS",
            "next_action": "attack A511 extra silence/readout/source clauses or implement explicit closure runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1277_1_practical_branch",
            "decision": "write explicit closure runner next while derivation remains open",
            "because": "testing can proceed safely only if closure/finite/inherited-EH branches are separated",
            "status": "CLOSURE_RUNNER_SELECTED",
            "next_action": "implement branch flags and refusal logic before any local tests are scored",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1277_2_derivation_branch",
            "decision": "keep A511 block-by-block derivation route alive",
            "because": "EH inheritance is the cleanest way to make the GR-style route respectable if the blocks can be parent-signed",
            "status": "A511_PRIORITY_LADDER_WRITTEN",
            "next_action": "start with extra-sector silence and readout/projector leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1277_0_1278",
            "target_file": "1278-Y5-R10-RAB-explicit-local-closure-runner-and-A511-origin-priority-ladder.md",
            "target_script": "scripts/Y5_R10_RAB_explicit_local_closure_runner_and_A511_origin_priority_ladder.py",
            "task": "implement an explicit nonclaim local-closure runner/spec that separates closure, finite-residual, and inherited-EH branches, while keeping A511 block-origin derivations queued by priority",
            "success_condition": "future local tests cannot accidentally treat closure baseline as derived MTS local GR, and the next derivation targets are ordered by A511 dependency risk",
            "do_not": "do not score closure and finite residual rows together or promote EH anchor-only as inherited",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (INHERITANCE_AUDIT_PATH, inheritance_audit),
        (CONDITIONAL_THEOREM_PATH, conditional_theorem),
        (CLOSURE_RUNNER_PATH, closure_runner),
        (DERIVATION_PRIORITY_PATH, priority_ladder),
        (VALIDATOR_RESCAN_PATH, validator_rescan),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    inheritance_fails = any(
        row["audit_id"] == "EHI1277_8_verdict" and row["status"] == "EH_FIXED_POINT_NOT_INHERITED"
        for row in inheritance_audit
    )
    all_blocks_audited = {row["A511_block"] for row in inheritance_audit if row["A511_block"].startswith("A511_")} >= {
        "A511_0_EH_core",
        "A511_1_kappa_topological",
        "A511_2_universal_matter",
        "A511_3_extra_field_silence",
        "A511_4_domain_projector_selector",
        "A511_5_boundary_reference",
        "A511_6_metric_readout",
    }
    conditional_only = all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in conditional_theorem)
    closure_runner_ready = len(closure_runner) == 4 and all(row["claim_status"] in {"NONCLAIM_CONTROL_BRANCH", "INTERNAL_BENCHMARK_ONLY", "LOCKED_NO_ROWS", "BLOCKED"} for row in closure_runner)
    priority_ladder_ready = any(row["priority_id"] == "APL1277_4_closure_runner" and row["status"] == "SELECTED_PARALLEL_PRACTICAL_TARGET" for row in priority_ladder)
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_live_rows = len(raw_rows) == 0 and len(accepted_rows) == 0 and len(accepted_ready) == 0
    claim_gates_safe = all(row["status"] in {"BLOCKED", "PASS_NONCLAIM"} for row in claim_gates)
    no_claim_promoted = all(
        row["status"] != "PASS_NONCLAIM" or row["gate_id"] == "GATE1277_2_closure_runner"
        for row in claim_gates
    )
    all_generated_rows = [
        *source_register,
        *inheritance_audit,
        *conditional_theorem,
        *closure_runner,
        *priority_ladder,
        *validator_rescan,
        *claim_gates,
        *decisions,
        *next_target,
    ]
    nonclaim_policy = all(is_false(row.get("valid_for_claim")) and is_false(row.get("claim_allowed")) for row in all_generated_rows)
    formalization_generated = generated_inside_formalization()

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in generated_tables:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")

    validation = [
        validation_row(
            "VAL1277_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1277_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1277_2_A511_audit",
            "all A511 inheritance blocks are audited",
            all_blocks_audited and len(inheritance_audit) >= 9,
            f"inheritance_audit_rows={len(inheritance_audit)}",
        ),
        validation_row(
            "VAL1277_3_inheritance_not_claimed",
            "EH fixed-point inheritance is blocked",
            inheritance_fails,
            "EHI1277_8_verdict=EH_FIXED_POINT_NOT_INHERITED",
        ),
        validation_row(
            "VAL1277_4_conditional_theorem",
            "conditional EH inheritance theorem remains nonclaim",
            conditional_only,
            f"conditional_rows={len(conditional_theorem)}",
        ),
        validation_row(
            "VAL1277_5_closure_runner",
            "explicit closure runner spec is written as nonclaim",
            closure_runner_ready,
            f"closure_runner_rows={len(closure_runner)}",
        ),
        validation_row(
            "VAL1277_6_priority_ladder",
            "A511 derivation priority ladder is written",
            priority_ladder_ready,
            f"priority_ladder_rows={len(priority_ladder)}",
        ),
        validation_row(
            "VAL1277_7_finite_fallback_locked",
            "finite branch has no source-backed accepted rows",
            docs_rejected and no_live_rows,
            f"docs_rows={len(docs_rows)}; raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1277_8_claim_gates_safe",
            "claim gates remain blocked except closure-runner nonclaim gate",
            claim_gates_safe and no_claim_promoted,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1277_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1277_10_next_target_1278",
            "next target routes to explicit closure runner and A511 priority ladder",
            next_target[0]["next_id"] == "NEXT1277_0_1278",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1277_11_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1277_12_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1277_13_overall",
            "overall 1277 validation",
            overall_pass,
            "1277 audits A511 local EH fixed-point inheritance, blocks it as not parent-signed, writes conditional theorem and closure runner specs, and queues A511 block-origin priorities",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1277 does not inherit the local EH fixed point. The A511 scaffold is valuable, but it is still a scaffold: the EH core is anchor-only, the total parent action remains unaccepted, and extra-sector silence, source universality, projector/readout, coupling drift, and boundary/reference clauses are not parent-signed.

**Main progress:** this prevents the clean-looking but dangerous shortcut: `A511 contains EH, therefore MTS reduces to GR`. Not yet. The honest state is now three-lane: inherited-EH branch blocked, closure baseline available only as nonclaim control, finite residual branch locked until real rows exist.

**No-claim guard:** no local-GR/Newton, R10, PPN, clock, orbital, zero-residual, EH-inheritance, or finite-`Z_R` row is claimed.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## EH Fixed-Point Inheritance Audit
{markdown_table(inheritance_audit, ["audit_id", "A511_block", "inheritance_clause", "evidence", "status", "failure_mode", "would_unlock", "valid_for_claim", "claim_allowed"])}

## Conditional EH Inheritance Theorem
{markdown_table(conditional_theorem, ["theorem_id", "conditional_statement", "then_result", "current_status", "missing_certificate", "valid_for_claim", "claim_allowed"])}

## Explicit Closure Runner Spec
{markdown_table(closure_runner, ["runner_id", "branch", "required_inputs", "runner_behavior", "claim_status", "do_not", "valid_for_claim", "claim_allowed"])}

## A511 Origin Priority Ladder
{markdown_table(priority_ladder, ["priority_id", "target", "why_first", "next_test", "status", "valid_for_claim", "claim_allowed"])}

## Z_R Validator Rescan
{markdown_table(validator_rescan, ["scan_id", "intake_class", "row_id", "coefficient_symbol", "status", "reasons", "source_exists", "anchor_found", "intake_eligible", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
