from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3207-Y5-R2FR-MHref-denominator-lower-bound-law-or-Bobs-refusal-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3207_INPUTS.csv"
LAW = OUT / "P8_Y5_R2FR_3207_MHREF_DENOMINATOR_LOWER_BOUND_LAW.csv"
CANDIDATE = OUT / "P8_Y5_R2FR_3207_MHREF_FIRST_ROW_CANDIDATE.csv"
GATE = OUT / "P8_Y5_R2FR_3207_POSITIVITY_BOUND_GATE.csv"
PATCH_QUEUE = OUT / "P8_Y5_R2FR_3207_BOBS_3206_PATCH_QUEUE.csv"
DECISION = OUT / "P8_Y5_R2FR_3207_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3207_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "parent_action":
        return ROOT / "source-intake" / "parent-action" / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


SOURCES = [
    {
        "input_id": "SRC3207_00_3206_doc",
        "location": "post_checkpoint",
        "relative_path": "3206-Y5-R2FR-Bobs-residual-acquisition-runner-after-Kperp-screen-under-AX1090.md",
        "role": "Bobs denominator refusal target",
        "terms": ["M_H_ref", "positive same-frame", "Residual score: refused", "Next target"],
    },
    {
        "input_id": "SRC3207_01_3206_schema",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3206_BOBS_COMPONENT_SCHEMA.csv",
        "role": "Bobs denominator schema",
        "terms": ["M_H_ref_same_frame", "denominator", "source_path", "valid_for_claim"],
    },
    {
        "input_id": "SRC3207_02_2550_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_NO_SHADOW_2550_HAMILTONIAN_DENOMINATOR_CONTRACT.csv",
        "role": "exact Hamiltonian denominator contract",
        "terms": ["M_H_ref", "H_tau", "H_ref", "positivity"],
    },
    {
        "input_id": "SRC3207_03_2946_theorem",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2946_DENOMINATOR_PACKAGE_THEOREM_ATTEMPT.csv",
        "role": "denominator package theorem attempt",
        "terms": ["M_H_ref", "denominator package", "MISSING_H_TAU", "anti"],
    },
    {
        "input_id": "SRC3207_04_2947_runner",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2947_MHREF_PIM_FIRST_ROW_RUNNER_ROWS.csv",
        "role": "theta/Qtau and MHref first-row runner schema",
        "terms": ["M_H_ref", "theta_Qtau", "integrability", "MISSING"],
    },
    {
        "input_id": "SRC3207_05_3005_audit",
        "location": "parent_action",
        "relative_path": "Mref_denominator_ownership_3005_NOT_SIGNED.csv",
        "role": "latest denominator ownership audit",
        "terms": ["positive", "same-frame", "M_H_ref", "DENOMINATOR_NOT_DERIVED"],
    },
    {
        "input_id": "SRC3207_06_3031_asource",
        "location": "parent_action",
        "relative_path": "A_source_denominator_owner_audit_3031_NOT_SIGNED.csv",
        "role": "A_source denominator owner audit",
        "terms": ["M_H_ref", "MISSING_POSITIVE", "G_ref", "denominator"],
    },
    {
        "input_id": "SRC3207_07_3059_lock",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3059_NO_GM_ABSORPTION_DENOMINATOR_LOCK_ATTEMPT.csv",
        "role": "no orbital-GM absorption guard",
        "terms": ["G_ref", "orbital", "denominator", "FAILED"],
    },
]


def build_inputs(now: str) -> list[dict[str, object]]:
    rows = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        rows.append(
            {
                "input_id": source["input_id"],
                "path": str(path),
                "exists": b(path.exists()),
                "role": source["role"],
                "evidence": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def build_law(now: str) -> list[dict[str, object]]:
    return [
        {
            "law_id": "LAW3207_0_phase_space_one_form",
            "object": "alpha_tau",
            "statement": "alpha_tau[deltaPhi]=int_S(delta Q_tau^MTS-i_tau Theta_MTS)-delta H_ref; H_tau exists on a branch only if d_F alpha_tau=0",
            "derivation_status": "EXACT_CONDITIONAL_COVARIANT_PHASE_SPACE_CRITERION",
            "what_it_buys": "turns H_tau from a named object into a closed field-space one-form requirement",
            "missing_for_claim": "theta_MTS;Q_tau_MTS;boundary_policy;reference_lock;field_space_curl_zero_or_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "LAW3207_1_MHref_definition",
            "object": "M_H_ref",
            "statement": "M_H_ref := G_ref^-1*(H_tau[S_outer]-H_ref) in one tau/coframe/source/readout branch",
            "derivation_status": "DEFINITION_LAW_SOURCE_BACKED_BY_2550_NOT_VALUE",
            "what_it_buys": "fixes the denominator object without importing orbital GM",
            "missing_for_claim": "finite_H_tau;fixed_H_ref;constant_G_ref;same_frame_lock;positive_value",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "LAW3207_2_EH_plus_residual_decomposition",
            "object": "G_ref*M_H_ref",
            "statement": "G_ref*M_H_ref = G_ref*M_EH + Delta_nonEH + Delta_ref + Delta_boundary + Delta_projector + Delta_source_measure + Delta_coupling + Delta_Kperp + Delta_EM",
            "derivation_status": "LINEAR_RESIDUAL_DECOMPOSITION_OF_THE_CHARGE_BRANCH",
            "what_it_buys": "moves positivity from a magic value to component residual bounds",
            "missing_for_claim": "source_backed_M_EH_comparator;all_Delta_i_zero_or_finite_bounds_same_frame",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "LAW3207_3_positive_lower_bound",
            "object": "M_H_ref_lower_bound",
            "statement": "If M_EH>0 and epsilon_abs:=sum_i |Delta_i|/(G_ref*M_EH)<1, then M_H_ref >= M_EH*(1-epsilon_abs)>0",
            "derivation_status": "DERIVED_TRIANGLE_INEQUALITY_BOUND",
            "what_it_buys": "gives a non-orbital route to a positive denominator using no-cancellation residual rows",
            "missing_for_claim": "M_EH_source_row;Delta_i_bound_rows;shared_units;shared_surface;no_EH_import_claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "LAW3207_4_Bobs_acceptance_rule",
            "object": "Bobs_denominator_input",
            "statement": "3206 may accept either exact positive M_H_ref or a source-backed same-frame lower bound M_H_ref_lower_bound, but not observed orbital GM",
            "derivation_status": "ACCEPTANCE_RULE_FOR_FUTURE_RUNNER_PATCH",
            "what_it_buys": "lets Bobs scoring become possible after bounded residual acquisition without denominator laundering",
            "missing_for_claim": "no current exact value or lower-bound rows exist",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "LAW3207_5_current_verdict",
            "object": "current_MTS_Bobs_denominator",
            "statement": "law derived, but no current source-backed row satisfies the 3206 positive same-frame denominator gate",
            "derivation_status": "BOBS_REFUSAL_REMAINS_ACTIVE",
            "what_it_buys": "progresses from missing-value refusal to a precise lower-bound acquisition route",
            "missing_for_claim": "M_EH and Delta_i rows or parent theta/Qtau certificate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_candidate(now: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "MH3207_0_exact_candidate",
            "system_id": "local_compact_source_branch",
            "domain_id": "same_frame_outer_surface",
            "symbol": "M_H_ref",
            "definition": "G_ref^-1*(H_tau[S_outer]-H_ref)",
            "candidate_expression": "requires exact H_tau, fixed H_ref, G_ref and same tau/coframe/source frame",
            "M_H_ref": "MISSING_EXACT_PARENT_CHARGE_VALUE",
            "M_H_ref_lower_bound": "NOT_APPLICABLE_EXACT_ROUTE",
            "units": "mass_or_energy_over_G_ref_convention",
            "frame_definition": "MISSING_SAME_FRAME_TAU_COFRAME_SOURCE_READOUT_CERTIFICATE",
            "source_path": rel(INPUTS),
            "equation_ref": "LAW3207_1_MHref_definition",
            "acceptance_rule": "positive finite numeric value or theorem-positive value with source-backed H_tau/H_ref/G_ref",
            "status": "NOT_VALID_FOR_3206",
            "valid_for_claim": "false",
            "feeds_3206": "DEN3206_00_MH_ref",
            "generated_utc": now,
        },
        {
            "row_id": "MH3207_1_lower_bound_candidate",
            "system_id": "local_compact_source_branch",
            "domain_id": "same_frame_outer_surface",
            "symbol": "M_H_ref_lower_bound",
            "definition": "M_EH*(1-epsilon_abs), epsilon_abs=sum_i |Delta_i|/(G_ref*M_EH)",
            "candidate_expression": "M_H_ref >= M_EH*(1-epsilon_abs) if M_EH>0 and epsilon_abs<1",
            "M_H_ref": "MISSING_FROM_BOUND_UNTIL_COMPONENTS_FILLED",
            "M_H_ref_lower_bound": "MISSING_M_EH_AND_DELTA_I_ROWS",
            "units": "same_as_M_EH",
            "frame_definition": "same tau/coframe/source/readout branch as exact candidate",
            "source_path": rel(LAW),
            "equation_ref": "LAW3207_3_positive_lower_bound",
            "acceptance_rule": "M_EH source-backed and every Delta_i bound source-backed with sum_abs_ratio<1",
            "status": "SOURCE_READY_TEMPLATE_ONLY",
            "valid_for_claim": "false",
            "feeds_3206": "DEN3206_00_MH_ref_after_runner_patch_or_manual_review",
            "generated_utc": now,
        },
    ]


def build_gate(now: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G3207_0_system_worldtube",
            "gate": "source system and worldtube fixed before readout",
            "pass": "false",
            "status": "MISSING_SYSTEM_WORLDTUBE_SOURCE_ROW",
            "why_it_matters": "anonymous denominators can normalize the wrong source",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3207_1_same_frame",
            "gate": "same tau/coframe/source/readout frame",
            "pass": "false",
            "status": "MISSING_SAME_FRAME_CERTIFICATE",
            "why_it_matters": "frame mismatch can fake a denominator agreement",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3207_2_Htau_integrability",
            "gate": "alpha_tau field-space curl zero or finite bound",
            "pass": "false",
            "status": "MISSING_DELTA_H_TAU_CURL_ZERO_OR_BOUND",
            "why_it_matters": "without integrability H_tau is not a state function",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3207_3_fixed_reference",
            "gate": "H_ref fixed and source/readout silent",
            "pass": "false",
            "status": "MISSING_FIXED_REFERENCE_LOCK",
            "why_it_matters": "a moving reference can absorb local residuals",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3207_4_Gref_lock",
            "gate": "G_ref constant and parent-owned before orbital calibration",
            "pass": "false",
            "status": "CONDITIONAL_ROUTE_NOT_PARENT_ADOPTED",
            "why_it_matters": "G drift or fitted G can hide source normalization failure",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3207_5_EH_positive_comparator",
            "gate": "M_EH positive same-frame comparator/source row",
            "pass": "false",
            "status": "MISSING_SOURCE_BACKED_M_EH_ROW",
            "why_it_matters": "the lower-bound law needs a positive baseline scale",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3207_6_residual_bounds",
            "gate": "all Delta_i residuals zero or source-backed finite with shared units",
            "pass": "false",
            "status": "MISSING_DELTA_I_BOUND_ROWS",
            "why_it_matters": "epsilon_abs cannot be evaluated without component bounds",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3207_7_epsilon_less_than_one",
            "gate": "epsilon_abs < 1",
            "pass": "false",
            "status": "NOT_EVALUATED_COMPONENTS_MISSING",
            "why_it_matters": "positivity lower bound fails if residuals can exceed baseline",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3207_8_no_orbital_GM",
            "gate": "no orbital GM, EH-only charge, fitted reference, or post-readout calibration is used as denominator proof",
            "pass": "true",
            "status": "ANTI_CIRCULARITY_GUARD_ACTIVE",
            "why_it_matters": "keeps Newton/GR reduction as output rather than input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3207_9_verdict",
            "gate": "positive same-frame Bobs denominator exists now",
            "pass": "false",
            "status": "DENOMINATOR_LAW_DERIVED_ROW_NOT_FILLED",
            "why_it_matters": "3206 remains honestly refused until exact or lower-bound route is sourced",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_patch_queue(now: str) -> list[dict[str, object]]:
    return [
        {
            "queue_id": "BQ3207_0_exact_MHref",
            "target": "P8_Y5_R2FR_3206_BOBS_COMPONENT_SCHEMA DEN3206_00_MH_ref",
            "patch_or_fill_action": "fill exact M_H_ref row only after H_tau/H_ref/G_ref/same-frame certificates exist",
            "minimum_new_columns": "H_tau;H_ref;G_ref;tau_id;coframe_id;surface_outer;integrability_certificate;reference_lock;source_path",
            "current_status": "WAITING_FOR_PARENT_CHARGE_CERTIFICATE",
            "priority": 0,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "queue_id": "BQ3207_1_lower_bound",
            "target": "3206 denominator acceptance extension",
            "patch_or_fill_action": "allow a source-backed positive lower bound M_H_ref_lower_bound as denominator scale after manual runner patch",
            "minimum_new_columns": "M_EH;Delta_i_bounds;epsilon_abs;M_H_ref_lower_bound;units;source_path;no_cancellation_flag",
            "current_status": "DERIVED_LAW_NO_VALUES",
            "priority": 1,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "queue_id": "BQ3207_2_first_component",
            "target": "epsilon_abs residual components",
            "patch_or_fill_action": "start with Delta_ref and delta_H_tau curl because they block both exact and lower-bound routes",
            "minimum_new_columns": "component_id;raw_bound;normalization;units;source_path;zero_theorem_or_bound",
            "current_status": "NEXT_DERIVATION_TARGET",
            "priority": 2,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_decision(now: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3207_0",
            "result": "MHREF_DENOMINATOR_LOWER_BOUND_LAW_DERIVED_BOBS_REFUSAL_REMAINS",
            "claim_status": "NO_LOCAL_GR_NEWTON_PPN_R10_OR_BOBS_SCORE_CLAIM",
            "decision": "do not keep looking for an unsourced M_H_ref value; use either parent charge exactness or the new no-cancellation lower-bound law",
            "best_next_route": "derive or source the first epsilon_abs component, starting with delta_H_tau curl and fixed-reference residual",
            "next_target": "3208-Y5-R2FR-Htau-one-form-exactness-or-first-DeltaH-curl-bound-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def main() -> None:
    now = stamp()
    input_rows = build_inputs(now)
    law_rows = build_law(now)
    candidate_rows = build_candidate(now)
    gate_rows = build_gate(now)
    patch_rows = build_patch_queue(now)
    decision_rows = build_decision(now)

    for path, rows in [
        (INPUTS, input_rows),
        (LAW, law_rows),
        (CANDIDATE, candidate_rows),
        (GATE, gate_rows),
        (PATCH_QUEUE, patch_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)

    generated = [INPUTS, LAW, CANDIDATE, GATE, PATCH_QUEUE, DECISION]
    validation_rows = [
        {
            "check_id": "VAL3207_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3207_01_definition_law_present",
            "check": "M_H_ref exact definition law is present",
            "pass": b(any(row["law_id"] == "LAW3207_1_MHref_definition" and "H_tau" in row["statement"] for row in law_rows)),
            "detail": "M_H_ref := G_ref^-1*(H_tau[S_outer]-H_ref)",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3207_02_lower_bound_law_present",
            "check": "positive lower-bound law is present",
            "pass": b(any(row["law_id"] == "LAW3207_3_positive_lower_bound" and "epsilon_abs" in row["statement"] for row in law_rows)),
            "detail": "M_H_ref >= M_EH*(1-epsilon_abs)>0 if M_EH>0 and epsilon_abs<1",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3207_03_candidate_rows_nonclaim",
            "check": "candidate denominator rows remain nonclaim",
            "pass": b(all(row["valid_for_claim"] == "false" for row in candidate_rows)),
            "detail": f"candidate_rows={len(candidate_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3207_04_positivity_gate_refuses",
            "check": "positivity gate still refuses current claim",
            "pass": b(any(row["gate_id"] == "G3207_9_verdict" and row["pass"] == "false" for row in gate_rows)),
            "detail": "denominator law derived but exact/lower-bound values missing",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3207_05_anti_circularity_guard",
            "check": "orbital GM shortcut remains rejected",
            "pass": b(any(row["gate_id"] == "G3207_8_no_orbital_GM" and row["pass"] == "true" for row in gate_rows)),
            "detail": "observed orbital GM is test output, not denominator proof input",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3207_06_decision_next_target",
            "check": "decision selects component derivation instead of circling M_H_ref",
            "pass": b(decision_rows[0]["next_target"].startswith("3208-Y5-R2FR-Htau-one-form-exactness")),
            "detail": decision_rows[0]["next_target"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3207_07_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3207_08_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated)),
            "detail": ";".join(path.name for path in generated),
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3207 - MHref Denominator Lower-Bound Law Or Bobs Refusal Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, R10 pass, clock pass, orbital pass, Bobs residual score, or public-facing result.

## Result

3207 does **not** find a current claim-valid `M_H_ref` value.

It does move the branch forward: the denominator route is no longer only "find `M_H_ref` or stop". The derived escape hatch is a no-cancellation lower-bound law:

```text
alpha_tau[deltaPhi] = int_S(delta Q_tau^MTS - i_tau Theta_MTS) - delta H_ref
M_H_ref := G_ref^-1 * (H_tau[S_outer] - H_ref)
G_ref M_H_ref = G_ref M_EH + sum_i Delta_i
epsilon_abs := sum_i |Delta_i| / (G_ref M_EH)
if M_EH > 0 and epsilon_abs < 1, then M_H_ref >= M_EH(1 - epsilon_abs) > 0
```

That gives two honest routes into the 3206 Bobs runner:

1. exact route: derive `H_tau`, `H_ref`, `G_ref`, same-frame locks, and positivity directly;
2. bound route: source `M_EH` plus every `Delta_i` residual with no cancellation and prove `epsilon_abs < 1`.

Current verdict:

```text
M_H_ref law: derived conditionally.
M_H_ref row: not claim-valid.
Bobs score: still refused.
New route: fill epsilon_abs components, starting with delta_H_tau curl and fixed-reference residual.
```

## Denominator Law

{md_table(law_rows, ["law_id", "object", "statement", "derivation_status", "missing_for_claim", "valid_for_claim"])}

## First Candidate Rows

{md_table(candidate_rows, ["row_id", "symbol", "definition", "M_H_ref", "M_H_ref_lower_bound", "status", "feeds_3206", "valid_for_claim"])}

## Positivity Gate

{md_table(gate_rows, ["gate_id", "gate", "pass", "status", "why_it_matters", "valid_for_claim"])}

## Bobs Patch Queue

{md_table(patch_rows, ["queue_id", "target", "patch_or_fill_action", "current_status", "priority", "valid_for_claim"])}

## Decision

`{decision_rows[0]["result"]}`.

Claim status: `{decision_rows[0]["claim_status"]}`.

Best next route: {decision_rows[0]["best_next_route"]}.

Next target:

```text
{decision_rows[0]["next_target"]}
```

## Generated Evidence

- `{rel(INPUTS)}`
- `{rel(LAW)}`
- `{rel(CANDIDATE)}`
- `{rel(GATE)}`
- `{rel(PATCH_QUEUE)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
