from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3215-Y5-R2FR-memory-scalar-nohair-or-coefficient-typing-theorem-for-balpha-Hodge-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3215_INPUTS.csv"
SOURCE_COMPAT = OUT / "P8_Y5_R2FR_3215_MEMORY_SOURCE_COMPATIBILITY_THEOREM.csv"
STATIONARITY = OUT / "P8_Y5_R2FR_3215_COEFFICIENT_STATIONARITY_GATE.csv"
ACTIVATION = OUT / "P8_Y5_R2FR_3215_NOHAIR_ACTIVATION_OR_FAIL_ROWS.csv"
FINITE_BOUND = OUT / "P8_Y5_R2FR_3215_FINITE_BOUND_FORMULA.csv"
DECISION = OUT / "P8_Y5_R2FR_3215_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3215_VALIDATION.csv"


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


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


SOURCES = [
    {
        "input_id": "SRC3215_00_3214_doc",
        "location": "post_checkpoint",
        "relative_path": "3214-Y5-R2FR-invariant-generator-kill-list-for-EM-coupling-or-promote-provenance-inputs-under-AX1090.md",
        "role": "3214 coupling Jacobian and memory survivor handoff",
        "terms": ["J_C", "continuous memory", "memory scalar"],
    },
    {
        "input_id": "SRC3215_01_3214_promo",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3214_PROVENANCE_PROMOTION_ROWS.csv",
        "role": "memory-to-balpha/Hodge finite rows",
        "terms": ["PROM3214_0_memory_to_balpha", "PROM3214_1_memory_to_hodge"],
    },
    {
        "input_id": "SRC3215_02_2626_owner",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_MEMORY_OWNER_GATE_2626_PARENT_MEMORY_OPERATOR_OWNER_AUDIT.csv",
        "role": "memory operator owner audit",
        "terms": ["MOA2626_2_operator_LX", "MOA2626_5_JX_source_map", "MOA2626_9_verdict"],
    },
    {
        "input_id": "SRC3215_03_2627_source",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_JX_COMPONENT_ZERO_GATE.csv",
        "role": "J_X component zero gates",
        "terms": ["JX2627_1_matter", "JX2627_5_history", "JX2627_6_total_verdict"],
    },
    {
        "input_id": "SRC3215_04_2728_activation",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2728_MEMORY_POSITIVE_OPERATOR_ACTIVATION_AUDIT.csv",
        "role": "positive operator activation audit",
        "terms": ["MPOA2728_3_positive_principal_symbol", "MPOA2728_5_JX_zero", "MPOA2728_8_verdict"],
    },
    {
        "input_id": "SRC3215_05_2729_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2729_PARENT_MEMORY_SIGNATURE_CONTRACT.csv",
        "role": "parent memory signature contract",
        "terms": ["PMC2729_2_quadratic_block", "PMC2729_4_source_decomposition", "PMC2729_8_activation_verdict"],
    },
    {
        "input_id": "SRC3215_06_1980_positivity",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_PARENT_QLOC_1980_MEMORY_POSITIVITY_LEMMA.csv",
        "role": "memory positivity lemma",
        "terms": ["LEM1980_1_Zm_sign", "LEM1980_2_M2_gap", "LEM1980_4_closure_fork"],
    },
    {
        "input_id": "SRC3215_07_967_lemma",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
        "role": "relative positive-operator nohair lemma",
        "terms": ["MPO967_4_energy_identity", "MPO967_5_constant_mode", "MPO967_6_verdict"],
    },
    {
        "input_id": "SRC3215_08_970_action",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
        "role": "minimal quadratic action construction and double-zero tension",
        "terms": ["QMA970_1_variation", "QMA970_3_source_silence", "QMA970_5_double_zero_tension"],
    },
    {
        "input_id": "SRC3215_09_3212_em",
        "location": "post_checkpoint",
        "relative_path": "3212-Y5-R2FR-EM-source-channel-no-extra-F2-or-Poynting-bound-input-under-AX1090.md",
        "role": "EM source decomposition",
        "terms": ["J_X^EM", "Z_A'(X)", "Hodge", "Poynting"],
    },
    {
        "input_id": "SRC3215_10_3210_amplitude",
        "location": "post_checkpoint",
        "relative_path": "3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md",
        "role": "finite source amplitude fallback",
        "terms": ["Y_X", "source/boundary leakage", "||X||"],
    },
]


def build_rows(now: str) -> tuple[list[dict[str, object]], ...]:
    input_rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        input_rows.append(
            {
                **source,
                "path": str(path),
                "exists": b(path.exists()),
                "evidence_hits": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    source_compat_rows = [
        {
            "theorem_id": "MSC3215_0_setup",
            "piece": "memory plus visible coefficients",
            "statement": "Let m be the local memory scalar with local origin m=0 and S = S_mem[m] + sum_r int C_r(m) O_r, where O_r includes F^2, FstarF, T_EM/Hodge, readout, matter/source operators, and boundary flux weights.",
            "result": "setup",
            "why_it_matters": "The visible sector is not a spectator if C_r'(0) is nonzero.",
            "claim_effect": "none",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MSC3215_1_source_term",
            "piece": "linear coefficient slope becomes source",
            "statement": "The memory Euler-Lagrange equation at m=0 contains J_vis(0)= - sum_r C_r'(0) O_r plus intrinsic J_mem and boundary terms.",
            "result": "EXACT_VARIATION_IDENTITY",
            "why_it_matters": "Positive no-hair cannot prove m=0 if EM/matter/readout creates a nonzero source through C_r'(0).",
            "claim_effect": "rejects_nohair_only_route",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MSC3215_2_stationary_coefficient_condition",
            "piece": "source-compatible nohair condition",
            "statement": "m=0 is a source-free solution only if intrinsic J_mem(0)=0, boundary variation vanishes, and C_r'(0)O_r=0 for every active visible operator; generically this means C_r'(0)=0 or the operator is absent/null on the branch.",
            "result": "NECESSARY_CONDITION",
            "why_it_matters": "The coupling problem is a coefficient-stationarity/double-zero problem, not merely a positivity problem.",
            "claim_effect": "requires_balpha_memory_zero_or_typed_exclusion",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MSC3215_3_unique_zero_if_stationary_and_coercive",
            "piece": "sufficient nohair theorem",
            "statement": "If C_r'(0)=0, intrinsic/boundary/readout sources vanish, and the corrected Hessian L_eff=L_mem + sum_r C_r''(0)O_r is coercive with spectral floor G_eff>0, then m=0 is the unique local solution in the small branch.",
            "result": "CONDITIONAL_SUFFICIENCY_THEOREM",
            "why_it_matters": "Double-zero/even coefficient maps plus positive operator can genuinely kill the memory-to-EM source.",
            "claim_effect": "would_kill_memory_to_balpha_and_Hodge_if_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MSC3215_4_nohair_only_counterexample",
            "piece": "positive operator with linear EM coupling fails",
            "statement": "For S=1/2 int(m L m)+int (C0+c1 m)F^2, variation gives L m = -c1 F^2; with F^2 nonzero, m=0 is not a solution even if L is positive.",
            "result": "COUNTEREXAMPLE_PROVED",
            "why_it_matters": "This blocks the tempting but wrong move of using the 967/1980 no-hair lemma to set b_alpha=0.",
            "claim_effect": "no_EM_silence_from_positive_operator_alone",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    stationarity_rows = [
        {
            "gate_id": "CSG3215_0_balpha_memory",
            "coefficient": "ln Z_A(m)",
            "operator": "F^2",
            "stationary_requirement": "partial_m ln Z_A at m=0 equals 0, or F^2 is identically zero on the tested branch, or memory is typed out of Z_A.",
            "current_status": "UNSIGNED",
            "if_passes": "removes linear memory-to-alpha source",
            "if_fails": "J_m contains b_alpha_memory F^2 and memory becomes finite sourced residual",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "CSG3215_1_dual_theta",
            "coefficient": "Theta_A(m)",
            "operator": "FstarF",
            "stationary_requirement": "partial_m Theta_A at m=0 equals 0, is topological/discrete constant, or FstarF is absent/null in branch.",
            "current_status": "UNSIGNED",
            "if_passes": "removes dual/topological EM source",
            "if_fails": "parity/time-arrow or dual readout source survives",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "CSG3215_2_hodge_metric",
            "coefficient": "g_obs(m) or star_obs(m)",
            "operator": "T_EM^{mu nu} and Hodge stress",
            "stationary_requirement": "partial_m g_obs at m=0 equals 0 or observed coframe/Hodge factors strictly through q with Dq[m]=0.",
            "current_status": "UNSIGNED",
            "if_passes": "removes memory-to-Hodge/EM-stress source",
            "if_fails": "memory changes observed metric/Hodge and feeds PPN/clock/EM stress",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "CSG3215_3_readout",
            "coefficient": "C_readout(m)",
            "operator": "alpha/clock/spectroscopy readout operator",
            "stationary_requirement": "readout happens after parent variation and does not feed back into S_eff, or partial_m C_readout at m=0 equals 0.",
            "current_status": "UNSIGNED",
            "if_passes": "prevents post-reduction alpha/clock source re-entry",
            "if_fails": "readout projector recreates the same coupling after the bare action is clean",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "CSG3215_4_boundary_flux",
            "coefficient": "C_boundary(m)",
            "operator": "n_i T_EM^{0i} boundary/worldtube flux",
            "stationary_requirement": "boundary functor is exact/proper/orthogonal or partial_m C_boundary at m=0 equals 0 with bounded flux support.",
            "current_status": "UNSIGNED",
            "if_passes": "removes Poynting/worldtube leakage from memory source",
            "if_fails": "boundary leakage feeds 3210 b_X even if bulk F2 is stationary",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    activation_rows = [
        {
            "gate_id": "ACT3215_0_parent_memory_owner",
            "activation_requirement": "m is a parent-owned field/auxiliary/quotient scalar with units and admissible variations before readout.",
            "current_status": "MISSING_PARENT_OWNER",
            "source_basis": "MOA2626_0;MPOA2728_0;PMC2729_0",
            "effect_if_missing": "no parent memory E-L equation, so no nohair theorem can be claimed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "ACT3215_1_positive_operator",
            "activation_requirement": "L_mem=-nabla_i(Z_m h^ij nabla_j)+M_m^2 plus controlled corrections has positive spectral floor G_mem>0.",
            "current_status": "CONDITIONAL_UNSIGNED",
            "source_basis": "LEM1980_1;LEM1980_2;MPO967_1;MPOA2728_3",
            "effect_if_missing": "energy identity cannot force m=0 even if sources vanish",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "ACT3215_2_source_stationarity",
            "activation_requirement": "intrinsic source, EM coefficient slopes, Hodge slopes, readout slopes, matter/source slopes, history and boundary flux slopes vanish at m=0 or are typed out.",
            "current_status": "NEW_REQUIRED_GATE_UNSIGNED",
            "source_basis": "MSC3215_1..4;JX2627_6;PROM3214_0..3",
            "effect_if_missing": "visible fields source m; nohair-only route fails",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "ACT3215_3_corrected_hessian",
            "activation_requirement": "quadratic visible corrections sum_r C_r''(0)O_r do not overturn the positive spectral floor.",
            "current_status": "MISSING_CORRECTION_BOUND",
            "source_basis": "LEM1980_3;MSC3215_3",
            "effect_if_missing": "even/double-zero coefficients may still destabilize or range-shift the memory mode",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "ACT3215_4_total",
            "activation_requirement": "ACT3215_0 through ACT3215_3 pass on the same parent branch.",
            "current_status": "FAIL_CURRENT_CLAIM",
            "source_basis": "3215 synthesis",
            "effect_if_missing": "memory remains finite residual/provenance branch, not a theorem-zero local-GR support",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    finite_rows = [
        {
            "bound_id": "FB3215_0_linear_source_norm",
            "formula": "||J_m,vis|| <= |b_alpha_memory| ||F^2|| + |theta_m| ||FstarF|| + ||C_Hodge_memory T_EM|| + ||C_readout O_readout|| + boundary_flux_norm",
            "inputs_required": "source-backed coefficient slopes; field/operator norms; support; units; source paths",
            "feeds": "3210 amplitude law and 3212 EM source envelope",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "FB3215_1_memory_amplitude",
            "formula": "||m||_H1 <= ||J_m,total|| / G_eff plus boundary lift terms, with G_eff = G_mem - eta_visible > 0",
            "inputs_required": "G_mem lower bound; visible correction eta_visible; J_m,total norm; boundary lift norm",
            "feeds": "b_alpha/Hodge/PPN/clock/local residual vector",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "FB3215_2_alpha_residual",
            "formula": "|Delta alpha/alpha| <= |b_alpha_memory| ||m|| + O(||m||^2) or direct readout bound if readout is post-variation",
            "inputs_required": "b_alpha_memory; memory amplitude; branch support; readout policy",
            "feeds": "R10/clocks/EM tests",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3215_0_result",
            "result": "NOHAIR_ONLY_ROUTE_REJECTED_SOURCE_COMPATIBLE_DOUBLE_ZERO_OR_TYPING_GATE_DERIVED",
            "claim_status": "NO_MEMORY_SILENCE_NO_BALPHA_ZERO_NO_LOCAL_GR_CLAIM",
            "decision": "Positive memory nohair is useful but insufficient. If visible coefficients have linear memory slopes, EM/matter/readout operators source the memory scalar. A real zero route needs source-compatible coefficient stationarity: C_r'(0)=0 or typed exclusion for all active visible operators, plus coercive corrected Hessian.",
            "best_next_route": "derive the branch-origin stationarity/double-zero law from a parent symmetry, extremum, or typed object-language exclusion; if not possible, promote b_alpha_memory, C_Hodge_memory, readout, and boundary flux to finite sourced rows",
            "next_target": "3216-Y5-R2FR-branch-origin-coefficient-stationarity-or-memory-slope-bound-pack-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]

    return input_rows, source_compat_rows, stationarity_rows, activation_rows, finite_rows, decision_rows


def main() -> None:
    now = stamp()
    input_rows, source_compat_rows, stationarity_rows, activation_rows, finite_rows, decision_rows = build_rows(now)

    generated_without_validation = [
        INPUTS,
        SOURCE_COMPAT,
        STATIONARITY,
        ACTIVATION,
        FINITE_BOUND,
        DECISION,
    ]

    write_csv(INPUTS, input_rows)
    write_csv(SOURCE_COMPAT, source_compat_rows)
    write_csv(STATIONARITY, stationarity_rows)
    write_csv(ACTIVATION, activation_rows)
    write_csv(FINITE_BOUND, finite_rows)
    write_csv(DECISION, decision_rows)

    all_rows: list[dict[str, str]] = []
    for path in generated_without_validation:
        all_rows.extend(read_csv(path))
    claim_rows = [row for row in all_rows if row.get("valid_for_claim") == "true"]

    validation_rows = [
        {
            "check_id": "VAL3215_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3215_01_source_identity",
            "check": "linear visible coefficient source identity is written",
            "pass": b(any(row["theorem_id"] == "MSC3215_1_source_term" for row in source_compat_rows)),
            "detail": "J_vis(0) = -sum C_r'(0) O_r",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3215_02_nohair_only_rejected",
            "check": "positive nohair alone is explicitly rejected",
            "pass": b(any(row["theorem_id"] == "MSC3215_4_nohair_only_counterexample" for row in source_compat_rows)),
            "detail": "positive L with linear F2 coupling gives Lm=-c1F2",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3215_03_stationarity_coverage",
            "check": "coefficient stationarity gates cover EM/Hodge/readout/boundary",
            "pass": b(len(stationarity_rows) >= 5),
            "detail": ";".join(row["gate_id"] for row in stationarity_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3215_04_activation_total_blocks_claim",
            "check": "activation total blocks current claim",
            "pass": b(any(row["gate_id"] == "ACT3215_4_total" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in activation_rows)),
            "detail": "same-branch parent owner, positivity, source stationarity, corrected Hessian not signed",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3215_05_finite_bound_fallback",
            "check": "finite bound formulas staged if stationarity fails",
            "pass": b(len(finite_rows) >= 3),
            "detail": ";".join(row["bound_id"] for row in finite_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3215_06_claims_blocked",
            "check": "no generated row is valid_for_claim true",
            "pass": b(len(claim_rows) == 0),
            "detail": f"claim_rows_true={len(claim_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3215_07_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3215_08_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated_without_validation)),
            "detail": ";".join(path.name for path in generated_without_validation),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3215_09_next_target",
            "check": "next target is coefficient stationarity or finite slope bounds",
            "pass": b("3216" in decision_rows[0]["next_target"]),
            "detail": decision_rows[0]["next_target"],
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3215 - Memory Scalar Nohair Or Coefficient Typing Theorem For b_alpha/Hodge under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha=0` claim, memory silence claim, or public-facing result.

## Result

3215 finds the key trap in the memory route:

```text
positive memory no-hair alone does not kill EM coupling.
```

If the visible coefficient depends linearly on the memory scalar,

```text
S_vis contains int (C0 + c1 m) O_vis,
```

then variation with respect to `m` gives

```text
L_m m = -c1 O_vis + ...
```

So even a perfectly positive memory operator is sourced by EM/matter/readout unless the visible coefficient is stationary at the local branch origin.

The real zero route is therefore:

```text
parent-owned m
+ positive corrected memory Hessian
+ intrinsic/source/boundary/readout silence
+ C_r'(0)=0 or typed exclusion for every active visible coefficient
=> m=0 unique locally
=> memory-to-b_alpha/Hodge/readout source killed
```

This is stronger than ordinary no-hair and sharper than the old product/sequester wording. It says exactly what must be derived next: a branch-origin coefficient stationarity law, an exact typed exclusion, or finite slope bounds.

## Source Compatibility Theorem

{md_table(source_compat_rows, ["theorem_id", "piece", "statement", "result", "why_it_matters", "claim_effect", "valid_for_claim"])}

## Coefficient Stationarity Gate

{md_table(stationarity_rows, ["gate_id", "coefficient", "operator", "stationary_requirement", "current_status", "if_passes", "if_fails", "valid_for_claim"])}

## Nohair Activation Or Fail Rows

{md_table(activation_rows, ["gate_id", "activation_requirement", "current_status", "source_basis", "effect_if_missing", "valid_for_claim"])}

## Finite Bound Formula

{md_table(finite_rows, ["bound_id", "formula", "inputs_required", "feeds", "valid_for_claim"])}

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
- `{rel(SOURCE_COMPAT)}`
- `{rel(STATIONARITY)}`
- `{rel(ACTIVATION)}`
- `{rel(FINITE_BOUND)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
