from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "843-Y5-R10-testing-readiness-and-GR-limit-map.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_843_SOURCE_REGISTER.csv"
READINESS_MAP_PATH = RESIDUALS / "P8_Y5_R10_843_TEST_READINESS_MAP.csv"
GR_LIMIT_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_843_GR_LIMIT_OBLIGATION_LEDGER.csv"
EMPIRICAL_GATE_PATH = RESIDUALS / "P8_Y5_R10_843_EMPIRICAL_GATE_CRITERIA.csv"
PILLAR_SELECTION_PATH = RESIDUALS / "P8_Y5_R10_843_EMPIRICAL_PILLAR_SELECTION.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_843_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_843_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_843_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_843_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_843_VALIDATION.csv"

STATUS = "Y5_R10_843_testing_readiness_mapped_cosmology_selected_nonclaim"
CLAIM_CEILING = "empirical_testing_allowed_GR_limit_derivation_still_missing"
SELECTED_PILLAR = "cosmology_robustness_residual_anatomy"
NEXT_TARGET = "844-Y5-R10-cosmology-evidence-readout-pack.md"

SOURCE_SPECS = [
    {
        "source_id": "842_doc",
        "path": POST_CHECKPOINT / "842-Y5-R10-doubled-open-system-metric-null-theorem-or-closure-demotion.md",
        "needles": [
            "local_transition_closure_only_no_derived_local_GR_or_PPN_pass",
            "successful galaxy/cosmology/EM fits prove the missing local-GR theorem",
            "843-Y5-R10-testing-readiness-and-GR-limit-map.md",
        ],
        "role": "local transition closure-only handoff",
    },
    {
        "source_id": "842_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_842_VALIDATION.csv",
        "needles": [
            "V842_6_closure_only_installed,pass",
            "V842_8_all_rows_nonclaim,pass",
            "V842_10_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "145_testing_readiness",
        "path": FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "needles": [
            "Private ruthless status: testing can proceed now, but it cannot replace the",
            "| Galaxy dynamics | Yes | SPARC, ETG, rotation curves, residual structure |",
            "good data fit -> accidental claim that the theory is fundamental.",
            "146-empirical-pillar-selection.md",
        ],
        "role": "testing readiness and GR-limit source map",
    },
    {
        "source_id": "146_empirical_pillar_selection",
        "path": FORMALIZATION / "146-empirical-pillar-selection.md",
        "needles": [
            "Private ruthless status: first near-term empirical pillar selected.",
            "cosmology robustness / residual-anatomy readout.",
            "147-cosmology-evidence-readout-pack.md",
        ],
        "role": "near-term empirical pillar selector",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def readiness_map_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch": "cosmology",
            "test_readiness": "yes_with_discipline",
            "data_arena": "Pantheon+, BAO, CMB distance priors, growth",
            "allowed_success_meaning": "may identify a real expansion-history clue",
            "forbidden_success_meaning": "proves the parent memory field or local PPN safety",
            "missing_reduction_link": "FLRW projection from parent action plus GR early/late limits",
            "priority": "first",
            "next_action": "assemble cosmology evidence readout pack from existing outputs and robustness gates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "galaxy_dynamics",
            "test_readiness": "yes",
            "data_arena": "SPARC, ETG, rotation curves, residual structure",
            "allowed_success_meaning": "may reveal a useful stationary effective law",
            "forbidden_success_meaning": "proves MTS is fundamental or universally replaces dark matter",
            "missing_reduction_link": "stationary weak-field limit and stress-energy source map",
            "priority": "second",
            "next_action": "import only as an empirical pillar after cosmology readout, without mixing with galaxy repo work",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "local_gr_ppn",
            "test_readiness": "guardrail_only",
            "data_arena": "solar system, binary pulsars, laboratory gravity",
            "allowed_success_meaning": "current working model imposes local GR recovery as a required limit",
            "forbidden_success_meaning": "MTS derives local GR",
            "missing_reduction_link": "exact or bounded Sigma_metric[q_tr] theorem and parent GR/Newton reduction",
            "priority": "constraint",
            "next_action": "carry closure-only label into every local test and forbid use as evidence for derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "time_clocks",
            "test_readiness": "partial",
            "data_arena": "clock comparison, redshift, timing anomalies",
            "allowed_success_meaning": "time-sector ideas can be formalised into observables",
            "forbidden_success_meaning": "time field replaces GR clock physics without derivation",
            "missing_reduction_link": "covariant clock observable and GR redshift recovery",
            "priority": "later_extension",
            "next_action": "define observables after cosmology readout, then check GR clock/redshift limits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "em_fine_structure",
            "test_readiness": "partial_pretest",
            "data_arena": "alpha variation, atomic spectra, propagation",
            "allowed_success_meaning": "possible extension arena",
            "forbidden_success_meaning": "unified EM field theory exists",
            "missing_reduction_link": "gauge-invariant EM action and Maxwell reduction",
            "priority": "later_extension",
            "next_action": "keep EM as a clue source, not a claim branch, until Maxwell limit is derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "orbital_systems",
            "test_readiness": "partial_bound",
            "data_arena": "perihelion, ephemerides, binaries",
            "allowed_success_meaning": "can bound deviations from GR",
            "forbidden_success_meaning": "explains galaxy/cosmology sectors",
            "missing_reduction_link": "post-Newtonian expansion with MTS corrections",
            "priority": "constraint",
            "next_action": "use only as deviation guardrail unless parent PPN map is derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "quantum_particle",
            "test_readiness": "not_ready",
            "data_arena": "masses, phases, quantum clocks",
            "allowed_success_meaning": "conceptual direction only",
            "forbidden_success_meaning": "evidence for unification",
            "missing_reduction_link": "Hilbert/action bridge and standard quantum limits",
            "priority": "defer",
            "next_action": "do not use as near-term support until a formal bridge exists",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gr_limit_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "obligation_id": "GR843_0_local_metric_response",
            "required_theorem": "Sigma_metric[q_tr]=0 or bounded local metric response",
            "needed_for": "local GR/PPN safety",
            "current_status": "missing_closure_only",
            "evidence_source": "842 demotion plus 145 local gravity row",
            "blocks": "claiming local GR/Newton derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obligation_id": "GR843_1_newton_weak_field",
            "required_theorem": "stationary weak-field limit with stress-energy source map",
            "needed_for": "galaxy branch interpretation as field-theory limit",
            "current_status": "missing",
            "evidence_source": "145 galaxy dynamics row",
            "blocks": "claiming galaxy success is fundamental-theory confirmation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obligation_id": "GR843_2_flrw_projection",
            "required_theorem": "FLRW projection from parent action with GR-compatible early/late limits",
            "needed_for": "cosmology branch interpretation",
            "current_status": "partial_incomplete",
            "evidence_source": "145 cosmology branch and 146 pillar selection",
            "blocks": "claiming cosmology fit proves parent memory field",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obligation_id": "GR843_3_covariance_conservation",
            "required_theorem": "conservation/covariance spine connecting parent fields to observed sectors",
            "needed_for": "serious fundamental theory candidate status",
            "current_status": "open",
            "evidence_source": "145 promotion criteria",
            "blocks": "promoting the programme from testable framework to fundamental theory claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obligation_id": "GR843_4_maxwell_limit",
            "required_theorem": "gauge-invariant EM action and Maxwell reduction",
            "needed_for": "EM/unification branch",
            "current_status": "missing",
            "evidence_source": "145 EM branch",
            "blocks": "claiming unified EM field theory",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def empirical_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "EG843_0_prior_edges",
            "gate": "no prior-edge dependence",
            "pass_condition": "best-fit preference survives narrowed and widened priors without edge-hitting",
            "failure_action": "mark branch edge-dependent and non-evidential",
            "applies_to": "cosmology first, then galaxy/EM/time as applicable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "EG843_1_data_splits",
            "gate": "stable data splits",
            "pass_condition": "preference survives no-SH0ES, SN/BAO/CMB/growth splits, and jackknife-like checks where baselines are subjected to the same test",
            "failure_action": "diagnose pipeline or demote signal",
            "applies_to": "cosmology and galaxy",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "EG843_2_baseline_fairness",
            "gate": "strict baseline comparison",
            "pass_condition": "compare against fitted LambdaCDM, wCDM, CPL, and any appropriate sector baseline using AIC/BIC and residual anatomy",
            "failure_action": "treat as weak or tied, not a knockout claim",
            "applies_to": "cosmology first",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "EG843_3_mechanism_match",
            "gate": "residual anatomy matches mechanism",
            "pass_condition": "surviving residuals have the shape expected from the proposed activation/memory or stationary-law mechanism",
            "failure_action": "record as phenomenological fit only",
            "applies_to": "all empirical pillars",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "EG843_4_gr_guardrail",
            "gate": "does not worsen local GR/PPN closure status",
            "pass_condition": "empirical branch remains explicitly separated from the closure-only local transition branch",
            "failure_action": "block interpretation until local closure conflict is resolved",
            "applies_to": "all empirical pillars",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def pillar_selection_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "selection_id": "PS843_0_first",
            "selected_pillar": SELECTED_PILLAR,
            "reason": "cosmology has the fastest honest readout and existing likelihood/model-comparison machinery",
            "claim_label": "effective_empirical_branch_nonclaim",
            "baselines_required": "fitted LambdaCDM, wCDM, CPL, plus MTS variants under same robustness gates",
            "success_language": "alive/promising empirical clue if robust against priors, splits, and baselines",
            "failure_language": "weak, edge-dependent, pipeline-limited, or demoted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "selection_id": "PS843_1_second",
            "selected_pillar": "galaxy_stationary_law_residual_tests",
            "reason": "galaxy branch is important but already active elsewhere and should not dominate the unified-theory thread",
            "claim_label": "second_empirical_pillar_nonclaim",
            "baselines_required": "Newtonian baryons, dark matter fits where appropriate, MOND-like baselines where applicable",
            "success_language": "useful stationary-law clue",
            "failure_language": "sector-specific phenomenology only",
            "next_target": "after_cosmology_readout",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG843_0_no_test_equals_foundation",
            "claim": "good empirical fit proves MTS is fundamental",
            "status": "forbidden",
            "reason": "145 explicitly blocks accidental theory confirmation from data fit alone",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG843_1_no_local_gr_derivation",
            "claim": "MTS derives local GR",
            "status": "forbidden",
            "reason": "842 demotes local transition branch to closure-only and 145 local branch repeats closure-only status",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG843_2_allowed_testing",
            "claim": "cosmology and galaxy branches can be tested as effective empirical branches",
            "status": "allowed_private_nonclaim",
            "reason": "testing is allowed when claims are labelled and GR-limit obligations remain explicit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG843_3_no_em_unification",
            "claim": "MTS has derived unified electromagnetism",
            "status": "forbidden",
            "reason": "Maxwell limit and gauge-invariant EM action remain missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D843_0",
            "finding": "testing may proceed now",
            "reason": "several branches have data-facing arenas and existing machinery",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D843_1",
            "finding": "testing cannot replace GR-limit derivation",
            "reason": "local transition safety and parent GR/Newton reduction remain missing or closure-only",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D843_2",
            "finding": "cosmology selected as first near-term empirical pillar",
            "reason": "fastest honest readout with strict baseline comparison available",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "assemble the fastest honest cosmology status readout from existing outputs and robustness gates",
            "include": "current cosmology branch, fitted baselines, prior-edge flags, data splits, residual anatomy, nonclaim language",
            "exclude": "public fundamental claim, local-GR derivation claim, galaxy repo changes, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "mapped all empirical branches against their missing GR-limit obligations and selected cosmology as the first nonclaim evidence readout",
            "what_is_not_claimed": "fundamental theory confirmation, derived local GR/Newton, parent memory field proof, Maxwell limit, quantum unification",
            "selected_pillar": SELECTED_PILLAR,
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    readiness_rows: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    selection_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_842_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    expected_branches = {
        "cosmology",
        "galaxy_dynamics",
        "local_gr_ppn",
        "time_clocks",
        "em_fine_structure",
        "orbital_systems",
        "quantum_particle",
    }
    branches_ok = {row["branch"] for row in readiness_rows} == expected_branches
    local_guardrail = any(row["branch"] == "local_gr_ppn" and row["test_readiness"] == "guardrail_only" for row in readiness_rows)
    gr_obligations = {row["obligation_id"] for row in gr_rows} == {
        "GR843_0_local_metric_response",
        "GR843_1_newton_weak_field",
        "GR843_2_flrw_projection",
        "GR843_3_covariance_conservation",
        "GR843_4_maxwell_limit",
    }
    empirical_gates = {row["gate_id"] for row in gate_rows} == {
        "EG843_0_prior_edges",
        "EG843_1_data_splits",
        "EG843_2_baseline_fairness",
        "EG843_3_mechanism_match",
        "EG843_4_gr_guardrail",
    }
    cosmology_selected = any(row["selected_pillar"] == SELECTED_PILLAR for row in selection_rows)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    forbidden_guards = all(row["status"] != "allowed_public_claim" for row in guard_rows)
    nonclaim_ok = all_valid_for_claim_false([source_rows, readiness_rows, gr_rows, gate_rows, selection_rows, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V843_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V843_1_prior_842_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V843_2_readiness_branches_complete",
            "result": "pass" if branches_ok else "fail",
            "detail": "cosmology, galaxy, local, time, EM, orbital, and quantum branches mapped",
        },
        {
            "check_id": "V843_3_local_gr_guardrail_only",
            "result": "pass" if local_guardrail else "fail",
            "detail": "local GR/PPN branch is guardrail-only, not a derivation branch",
        },
        {
            "check_id": "V843_4_gr_obligations_recorded",
            "result": "pass" if gr_obligations else "fail",
            "detail": "local metric response, Newton, FLRW, covariance, and Maxwell obligations recorded",
        },
        {
            "check_id": "V843_5_empirical_gates_recorded",
            "result": "pass" if empirical_gates else "fail",
            "detail": "prior-edge, split, baseline, mechanism, and GR guardrail gates recorded",
        },
        {
            "check_id": "V843_6_cosmology_selected_first",
            "result": "pass" if cosmology_selected else "fail",
            "detail": SELECTED_PILLAR,
        },
        {
            "check_id": "V843_7_no_overclaim_guards",
            "result": "pass" if no_claim and forbidden_guards else "fail",
            "detail": "no fundamental, local-GR, EM-unification, or empirical-substitution claim allowed",
        },
        {
            "check_id": "V843_8_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V843_9_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V843_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V843_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    readiness_rows: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    selection_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 843 - Y5 R10 Testing Readiness And GR-Limit Map",
        "",
        "Current result: **testing can proceed, but no empirical result is allowed to stand in for the missing GR/Newton reduction theorem**. Cosmology is selected as the first near-term empirical readout because it has the fastest honest path through fitted baselines, prior-edge checks, data splits, and residual anatomy. Local GR/PPN remains a closure guardrail only.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "selected_pillar", "next_target", "valid_for_claim"]),
        "",
        "## Test Readiness Map",
        "",
        csv_table(readiness_rows, ["branch", "test_readiness", "data_arena", "allowed_success_meaning", "forbidden_success_meaning", "missing_reduction_link", "priority", "next_action", "valid_for_claim"]),
        "",
        "## GR-Limit Obligation Ledger",
        "",
        csv_table(gr_rows, ["obligation_id", "required_theorem", "needed_for", "current_status", "evidence_source", "blocks", "valid_for_claim"]),
        "",
        "## Empirical Gate Criteria",
        "",
        csv_table(gate_rows, ["gate_id", "gate", "pass_condition", "failure_action", "applies_to", "valid_for_claim"]),
        "",
        "## Empirical Pillar Selection",
        "",
        csv_table(selection_rows, ["selection_id", "selected_pillar", "reason", "claim_label", "baselines_required", "success_language", "failure_language", "next_target", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    readiness_rows = readiness_map_rows(generated_utc)
    gr_rows = gr_limit_ledger_rows(generated_utc)
    gate_rows = empirical_gate_rows(generated_utc)
    selection_rows = pillar_selection_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, readiness_rows, gr_rows, gate_rows, selection_rows, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(READINESS_MAP_PATH, readiness_rows, ["branch", "test_readiness", "data_arena", "allowed_success_meaning", "forbidden_success_meaning", "missing_reduction_link", "priority", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(GR_LIMIT_LEDGER_PATH, gr_rows, ["obligation_id", "required_theorem", "needed_for", "current_status", "evidence_source", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(EMPIRICAL_GATE_PATH, gate_rows, ["gate_id", "gate", "pass_condition", "failure_action", "applies_to", "valid_for_claim", "generated_utc"])
    write_csv(PILLAR_SELECTION_PATH, selection_rows, ["selection_id", "selected_pillar", "reason", "claim_label", "baselines_required", "success_language", "failure_language", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "selected_pillar", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, readiness_rows, gr_rows, gate_rows, selection_rows, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"selected_pillar={SELECTED_PILLAR}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
