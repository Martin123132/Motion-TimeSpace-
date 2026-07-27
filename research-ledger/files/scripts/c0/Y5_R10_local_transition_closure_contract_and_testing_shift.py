from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "809-Y5-R10-local-transition-closure-contract-and-testing-shift.md"
NEXT_TARGET = "810-Y5-R10-cosmology-evidence-readout-pack.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_809_SOURCE_REGISTER.csv"
CLOSURE_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_809_CLOSURE_CONTRACT.csv"
TEST_READINESS_PATH = RESIDUALS / "P8_Y5_R10_809_TEST_READINESS_MAP.csv"
CLAIM_LABELS_PATH = RESIDUALS / "P8_Y5_R10_809_CLAIM_LABELS.csv"
GR_REQUIREMENTS_PATH = RESIDUALS / "P8_Y5_R10_809_GR_LIMIT_REQUIREMENTS.csv"
PILLAR_SELECTION_PATH = RESIDUALS / "P8_Y5_R10_809_EMPIRICAL_PILLAR_SELECTION.csv"
NEXT_STEPS_PATH = RESIDUALS / "P8_Y5_R10_809_NEXT_STEPS.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_809_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_809_VALIDATION.csv"

STATUS = "Y5_R10_809_local_transition_closure_contract_testing_ready_with_GR_limit_guardrail_nonclaim"
CLAIM_CEILING = "testing_ready_as_effective_empirical_pillars_only_GR_limit_not_derived"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    CLOSURE_CONTRACT_PATH,
    TEST_READINESS_PATH,
    CLAIM_LABELS_PATH,
    GR_REQUIREMENTS_PATH,
    PILLAR_SELECTION_PATH,
    NEXT_STEPS_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "808_doc",
        "path": POST_CHECKPOINT / "808-Y5-R10-boundary-topological-backup-or-local-transition-demotion.md",
        "needles": ["q_metric,loc^nu = 0 is a closure assumption", "Galaxy/cosmology tests remain allowed empirical pillars", "809-Y5-R10-local-transition-closure-contract-and-testing-shift.md"],
        "role": "immediate 808 demotion result",
    },
    {
        "source_id": "808_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_808_VALIDATION.csv",
        "needles": ["V808_5_demotion_contract_set,pass", "V808_8_next_target_selected,pass,809-Y5-R10-local-transition-closure-contract-and-testing-shift.md"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_144_closure",
        "path": FORMALIZATION / "144-local-transition-closure-contract.md",
        "needles": ["local transition branch = explicit closure-only", "weak-field slow-motion limit", "MTS empirical testing = allowed but cannot substitute for derivation"],
        "role": "closure contract source",
    },
    {
        "source_id": "formal_145_testing",
        "path": FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "needles": ["MTS parent equations -> Einstein/GR local limit -> Newtonian weak-field limit", "Test Readiness Table", "cosmology robustness / residual anatomy"],
        "role": "testing readiness and GR-limit map",
    },
    {
        "source_id": "formal_146_pillar",
        "path": FORMALIZATION / "146-empirical-pillar-selection.md",
        "needles": ["cosmology robustness / residual-anatomy readout", "effective empirical clue only", "147-cosmology-evidence-readout-pack.md"],
        "role": "empirical pillar selection",
    },
    {
        "source_id": "spine_145_146",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["testing_ready_with_GR_limit_guardrail", "cosmology robustness / residual-anatomy readout", "147-cosmology-evidence-readout-pack.md"],
        "role": "spine testing transition",
    },
    {
        "source_id": "red_145_146",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["testing_ready_with_GR_limit_guardrail.", "cosmology robustness / residual-anatomy readout.", "cosmology success would be an effective empirical clue only"],
        "role": "red-team testing transition",
    },
]


def utc_stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_file"
    source_text = read_text(path)
    missing_needles = [needle for needle in needles if needle not in source_text]
    if missing_needles:
        return "missing_needles:" + ";".join(missing_needles)
    return "pass"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def validation_file_clean(check_number: int) -> tuple[bool, str]:
    validation_file = RESIDUALS / f"P8_Y5_BRR545_{check_number}_VALIDATION.csv"
    if not validation_file.exists():
        return False, f"missing={validation_file}"
    failures: list[str] = []
    with validation_file.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{validation_file.name} clean"


def formalization_change_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION.rglob("*")
        if candidate_path.is_file() and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        source_path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(source_path),
                "exists": str(source_path.exists()).lower(),
                "needle_check": needle_status(source_path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def closure_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "CC809_0_local_metric_quarantine",
            "statement": "q_metric,loc^nu = 0 is an explicit closure assumption, not a parent theorem.",
            "allowed_use": "local PPN/Solar predictions may use GR recovery as a guardrail",
            "forbidden_use": "claiming transition-shell machinery derives local GR",
            "promotion_condition": "parent theorem for Sigma_metric[q_tr]=0 or equivalent exact metric-null response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CC809_1_current_visibility",
            "statement": "q_tr^nu remains visible in an owner/global ledger and is not set to zero.",
            "allowed_use": "internal conservation bookkeeping",
            "forbidden_use": "erasing transition current to save PPN",
            "promotion_condition": "owner equations from parent action, symmetry, or transport theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CC809_2_GR_Newton_standard",
            "statement": "MTS must reduce to GR locally, and GR must reduce to Newton in weak-field slow-motion domains.",
            "allowed_use": "hard standard for future theory status",
            "forbidden_use": "using empirical fits as a substitute for local reduction",
            "promotion_condition": "derive MTS -> GR -> Newton from the parent field equations",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CC809_3_empirical_quarantine",
            "statement": "Galaxy/cosmology/time/EM tests are allowed as empirical/effective pillars only.",
            "allowed_use": "rank branches, find residual anatomy, falsify closures",
            "forbidden_use": "fundamental-theory claim before local and sector limits are derived",
            "promotion_condition": "data survival plus parent derivation of the relevant sector limit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def test_readiness_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "sector": "cosmology",
            "ready_status": "yes_with_discipline",
            "test_arenas": "Pantheon+, BAO, CMB distance priors, growth",
            "allowed_readout": "activation/memory branch may be effective empirical clue",
            "cannot_claim": "parent memory field or local PPN safety",
            "missing_derivation": "FLRW projection from parent action plus GR early/late limits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "sector": "galaxy_dynamics",
            "ready_status": "yes_as_second_pillar",
            "test_arenas": "SPARC, ETG, rotation curves, residual structure",
            "allowed_readout": "stationary effective law and residual anatomy",
            "cannot_claim": "universal dark-matter replacement or local GR derivation",
            "missing_derivation": "stationary weak-field limit and stress-energy source map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "sector": "local_gr_ppn",
            "ready_status": "guardrail_only",
            "test_arenas": "Solar system, binary pulsars, laboratory gravity",
            "allowed_readout": "closures must not violate known GR/PPN limits",
            "cannot_claim": "transition shell validates local GR",
            "missing_derivation": "exact or bounded Sigma_metric[q_tr] plus K_perp theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "sector": "time_clocks",
            "ready_status": "partial",
            "test_arenas": "clock comparison, redshift, timing anomalies",
            "allowed_readout": "time-sector phenomenology constraints",
            "cannot_claim": "replacement of GR clock/redshift physics",
            "missing_derivation": "covariant clock observable and GR redshift recovery",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "sector": "EM_fine_structure",
            "ready_status": "partial",
            "test_arenas": "alpha variation, spectra, propagation",
            "allowed_readout": "constraints on EM-sector coupling",
            "cannot_claim": "unification of EM",
            "missing_derivation": "gauge-invariant EM action and Maxwell reduction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "sector": "orbital_systems",
            "ready_status": "partial_guardrail",
            "test_arenas": "perihelion, ephemerides, binaries",
            "allowed_readout": "bounds on deviations from GR",
            "cannot_claim": "galaxy/cosmology explanation",
            "missing_derivation": "post-Newtonian expansion with MTS corrections",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_label_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch": "cosmology",
            "allowed_label": "effective empirical clue only",
            "allowed_claim": "branch may capture expansion residual anatomy if robust against baselines and splits",
            "forbidden_claim": "fundamental cosmology or parent-derived memory field",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "galaxy",
            "allowed_label": "active empirical pillar",
            "allowed_claim": "stationary law may be useful if residual tests survive",
            "forbidden_claim": "complete unified field theory or local GR proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "local_GR",
            "allowed_label": "closure guardrail",
            "allowed_claim": "working model imposes local GR recovery as required limit",
            "forbidden_claim": "MTS derives local GR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch": "time_EM_orbital",
            "allowed_label": "partial exploratory constraints",
            "allowed_claim": "can constrain sector couplings and deviations",
            "forbidden_claim": "derived Maxwell/clock/PPN limit before parent reductions",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gr_requirement_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "requirement": "parent_field_equations",
            "must_show": "Euler-Lagrange or equivalent parent dynamics exist and define the source map.",
            "status": "missing_for_full_theory",
            "why_needed": "No parent action means no serious reduction proof.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement": "local_GR_limit",
            "must_show": "MTS equations reduce to Einstein/GR local metric dynamics in relativistic local domains.",
            "status": "closure_only_currently",
            "why_needed": "Fundamental-theory status requires GR recovery, not only empirical fits.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement": "Newtonian_limit",
            "must_show": "GR limit reduces to Newtonian gravity in weak-field slow-motion systems.",
            "status": "required_standard",
            "why_needed": "Matches the GR -> Newton relationship the programme must emulate.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement": "transition_metric_nullity",
            "must_show": "Sigma_metric[q_tr]=0 or bounded below local PPN thresholds by theorem.",
            "status": "not_derived",
            "why_needed": "Local transition branch failed all tested derivation routes.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement": "Kperp_control",
            "must_show": "K_perp absent, higher-order, pure gauge/boundary, or PPN-bounded.",
            "status": "open_independent_blocker",
            "why_needed": "Nulling q_tr does not automatically silence transverse tensor leakage.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement": "sector_limits",
            "must_show": "FLRW, stationary galaxy, Maxwell/EM, and clock limits are derived where claimed.",
            "status": "mixed_partial_effective",
            "why_needed": "Empirical sectors cannot be promoted without their own reductions.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def pillar_selection_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "rank": 1,
            "pillar": "cosmology_robustness_residual_anatomy",
            "reason": "fastest honest near-term readout inside this unified-theory thread",
            "claim_label": "effective_empirical_clue_only",
            "minimum_next_artifact": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank": 2,
            "pillar": "galaxy_stationary_law_residual_tests",
            "reason": "important but already active separately; import only as pillar evidence",
            "claim_label": "active_empirical_pillar_not_unification_proof",
            "minimum_next_artifact": "after cosmology readout is frozen",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank": 3,
            "pillar": "local_GR_PPN",
            "reason": "must remain guardrail until parent GR-limit theorem exists",
            "claim_label": "closure_guardrail_only",
            "minimum_next_artifact": "future parent GR-limit theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_step_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "priority": 1,
            "next_step": "assemble_cosmology_evidence_readout_pack",
            "purpose": "Use existing outputs first; summarize best branch, baselines, residual anatomy, and edge-dependence.",
            "target": NEXT_TARGET,
            "run_policy": "no long run unless a missing table is proven necessary",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "priority": 2,
            "next_step": "predeclare_baseline_comparisons",
            "purpose": "Compare against LambdaCDM, wCDM, CPL under the same diagnostics.",
            "target": "cosmology_readout_pack",
            "run_policy": "table/readout first",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "priority": 3,
            "next_step": "freeze_claim_labels_before_testing",
            "purpose": "Prevent empirical success from becoming a local-GR or fundamental-theory claim.",
            "target": "all_empirical_outputs",
            "run_policy": "documentation gate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "priority": 4,
            "next_step": "define_smallest_next_run_only_if_needed",
            "purpose": "If existing evidence is insufficient, design the smallest cosmology run with strict splits.",
            "target": "future_run_manifest",
            "run_policy": "dry-run command generation before execution",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_improved": "809 separates local GR derivation from empirical testing and selects cosmology readout as first honest pillar.",
            "what_blocks_claim": "GR-limit theorem, transition metric-nullity, K_perp, and sector reductions remain incomplete.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_outputs_scoped() -> bool:
    post_root = POST_CHECKPOINT.resolve()
    return all(path.resolve().is_relative_to(post_root) for path in OUTPUT_PATHS)


def all_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for row_group in row_groups:
        for row in row_group:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
    return True


def validation_rows(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    readiness: list[dict[str, object]],
    labels: list[dict[str, object]],
    requirements: list[dict[str, object]],
    pillars: list[dict[str, object]],
    next_steps: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    prior_ok, prior_detail = validation_file_clean(808)
    row_groups = [sources, contract, readiness, labels, requirements, pillars, next_steps, summary]
    nonclaim_ok = all_rows_nonclaim(row_groups)
    formalization_count = formalization_change_count()
    closure_set = any(row["contract_id"] == "CC809_0_local_metric_quarantine" for row in contract)
    gr_standard = any(row["requirement"] == "local_GR_limit" and row["status"] == "closure_only_currently" for row in requirements)
    cosmology_selected = any(row["pillar"] == "cosmology_robustness_residual_anatomy" and row["rank"] == 1 for row in pillars)
    local_guardrail = any(row["branch"] == "local_GR" and row["allowed_label"] == "closure guardrail" for row in labels)
    next_selected = any(row["target"] == NEXT_TARGET for row in next_steps)
    return [
        {"check_id": "V809_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V809_1_prior_808_clean", "result": "pass" if prior_ok else "fail", "detail": prior_detail},
        {"check_id": "V809_2_outputs_scoped", "result": "pass" if all_outputs_scoped() else "fail", "detail": str(POST_CHECKPOINT)},
        {"check_id": "V809_3_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V809_4_closure_contract_set", "result": "pass" if closure_set else "fail", "detail": "local metric quarantine closure set"},
        {"check_id": "V809_5_GR_limit_guardrail", "result": "pass" if gr_standard else "fail", "detail": "local GR limit is closure-only currently"},
        {"check_id": "V809_6_cosmology_pillar_selected", "result": "pass" if cosmology_selected else "fail", "detail": "cosmology readout selected first"},
        {"check_id": "V809_7_local_claim_guardrail", "result": "pass" if local_guardrail else "fail", "detail": "local GR branch labelled closure guardrail"},
        {"check_id": "V809_8_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V809_9_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V809_10_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    readiness: list[dict[str, object]],
    labels: list[dict[str, object]],
    requirements: list[dict[str, object]],
    pillars: list[dict[str, object]],
    next_steps: list[dict[str, object]],
    summary: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return f"""# 809 - Y5 R10 Local Transition Closure Contract And Testing Shift

Current result: **local transition safety is now explicitly closure-only, while empirical testing remains open under strict labels**. The programme standard is still `MTS -> GR -> Newton`; we are not lowering that bar. We are separating what can be tested now from what must be derived later.

Generated UTC: `{generated_utc}`

## Non-Claim Summary

{markdown_table(summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim"])}

## Closure Contract

{markdown_table(contract, ["contract_id", "statement", "allowed_use", "forbidden_use", "promotion_condition", "valid_for_claim"])}

## Test Readiness Map

{markdown_table(readiness, ["sector", "ready_status", "test_arenas", "allowed_readout", "cannot_claim", "missing_derivation", "valid_for_claim"])}

## Claim Labels

{markdown_table(labels, ["branch", "allowed_label", "allowed_claim", "forbidden_claim", "valid_for_claim"])}

## GR-Limit Requirements

{markdown_table(requirements, ["requirement", "must_show", "status", "why_needed", "valid_for_claim"])}

## Empirical Pillar Selection

{markdown_table(pillars, ["rank", "pillar", "reason", "claim_label", "minimum_next_artifact", "valid_for_claim"])}

## Next Steps

{markdown_table(next_steps, ["priority", "next_step", "purpose", "target", "run_policy", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Working Standard

```text
MTS parent equations -> Einstein/GR local limit -> Newtonian weak-field limit.
```

Until that is derived:

```text
local GR = closure guardrail
cosmology = effective empirical clue only
galaxy dynamics = active empirical pillar, not unification proof
time/EM/orbital = partial exploratory constraints
```

## Verdict

This is the right pivot. The local transition route has been disciplined, not swept under the rug. The next useful move is an evidence readout pack from existing cosmology outputs before any long run: what branch is alive, what is edge-dependent, what residuals it improves, and what claim label it is allowed to carry.

## Next Target

`{NEXT_TARGET}`
"""


def write_outputs() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    contract = closure_contract_rows(generated_utc)
    readiness = test_readiness_rows(generated_utc)
    labels = claim_label_rows(generated_utc)
    requirements = gr_requirement_rows(generated_utc)
    pillars = pillar_selection_rows(generated_utc)
    next_steps = next_step_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validations = validation_rows(sources, contract, readiness, labels, requirements, pillars, next_steps, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(CLOSURE_CONTRACT_PATH, contract, ["contract_id", "statement", "allowed_use", "forbidden_use", "promotion_condition", "valid_for_claim", "generated_utc"])
    write_csv(TEST_READINESS_PATH, readiness, ["sector", "ready_status", "test_arenas", "allowed_readout", "cannot_claim", "missing_derivation", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_LABELS_PATH, labels, ["branch", "allowed_label", "allowed_claim", "forbidden_claim", "valid_for_claim", "generated_utc"])
    write_csv(GR_REQUIREMENTS_PATH, requirements, ["requirement", "must_show", "status", "why_needed", "valid_for_claim", "generated_utc"])
    write_csv(PILLAR_SELECTION_PATH, pillars, ["rank", "pillar", "reason", "claim_label", "minimum_next_artifact", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_STEPS_PATH, next_steps, ["priority", "next_step", "purpose", "target", "run_policy", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_improved", "what_blocks_claim", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validations, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        build_doc(generated_utc, sources, contract, readiness, labels, requirements, pillars, next_steps, summary, validations),
        encoding="utf-8",
    )

    failed_checks = [row for row in validations if row["result"] != "pass"]
    if failed_checks:
        failed_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed_checks)
        raise SystemExit(f"809 validation failed: {failed_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    write_outputs()
