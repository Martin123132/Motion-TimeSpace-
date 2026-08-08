from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3233-Y5-R2FR-no-extra-F2-or-source-root-owner-for-transverse-EMF2-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3233_INPUTS.csv"
DECOMP = OUT / "P8_Y5_R2FR_3233_TRANSVERSE_EMF2_OWNER_DECOMPOSITION.csv"
ZERO_AUDIT = OUT / "P8_Y5_R2FR_3233_CF2PERP_ZERO_ROUTE_AUDIT.csv"
COUNTER = OUT / "P8_Y5_R2FR_3233_EMF2_COUNTERMODEL_TRANSFER.csv"
FINITE = OUT / "P8_Y5_R2FR_3233_CF2PERP_FINITE_BOUND.csv"
DECISION = OUT / "P8_Y5_R2FR_3233_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3233_VALIDATION.csv"


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


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:220]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


SOURCES = [
    {
        "input_id": "SRC3233_00_3232_doc",
        "location": "post_checkpoint",
        "relative_path": "3232-Y5-R2FR-EMF2-and-Poynting-transverse-source-zero-or-bound-under-AX1090.md",
        "role": "3232 handoff selecting C_F2_perp owner",
        "terms": ["C_F2_perp", "f_perp_prime", "no-extra-F2", "3233"],
    },
    {
        "input_id": "SRC3233_01_3232_emf2",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3232_EMF2_ZERO_OR_BOUND_AUDIT.csv",
        "role": "machine EM_F2 zero/bound audit",
        "terms": ["EF3232_1_no_extra_F2", "EF3232_2_strict_source_root", "EF3232_3_readout_reentry"],
    },
    {
        "input_id": "SRC3233_02_3218_decomp",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3218_ZA_MEMORY_DECOMPOSITION.csv",
        "role": "machine Z_A decomposition",
        "terms": ["ZA3218_0_parent_norm", "ZA3218_2_hidden_scalar", "ZA3218_3_radiative_readout"],
    },
    {
        "input_id": "SRC3233_03_3218_zero",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3218_BALPHA_M_ZERO_THEOREM_ATTEMPT.csv",
        "role": "machine b_alpha zero theorem attempt",
        "terms": ["BAM3218_1_Q_ONLY_zero", "BAM3218_2_no_extra_F2_zero", "BAM3218_4_readout_guard"],
    },
    {
        "input_id": "SRC3233_04_3218_counter",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3218_EM_F2_COUNTERMODEL_LEDGER.csv",
        "role": "machine EM F2 countermodels",
        "terms": ["CEX3218_0_fm_linear", "CEX3218_3_readout_return"],
    },
    {
        "input_id": "SRC3233_05_3220_ownership",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3220_EM_SOURCE_ROOT_OWNERSHIP_TEST.csv",
        "role": "machine EM source-root ownership test",
        "terms": ["ROOT3220_0_target", "ROOT3220_7_verdict", "ROOT3220_6_wave_stress_channel"],
    },
    {
        "input_id": "SRC3233_06_3220_transfer",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3220_GENERIC_DZ_TO_EM_F2_TRANSFER_AUDIT.csv",
        "role": "machine generic double-zero transfer warning",
        "terms": ["TR3220_1_generic_root_not_enough", "TR3220_2_hidden_counterterm_survives"],
    },
    {
        "input_id": "SRC3233_07_3219_law",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3219_EM_F2_STRICT_DOUBLE_ZERO_LAW.csv",
        "role": "machine strict double-zero EM F2 law",
        "terms": ["DZ3219_1_exact_slope_zero", "DZ3219_4_not_no_extra_F2"],
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

    decomp_rows = [
        {
            "component_id": "CF23233_0_definition",
            "component": "C_F2_perp",
            "formula": "C_F2_perp := |D_perp ln Z_A| or |D_perp Z_A|/Z_min in the transverse EM F2 branch",
            "zero_condition": "D_perp Z_A=0 with Z_A positive/fixed",
            "finite_bound": "C_F2_perp <= |D_perp Z_A|_bound / Z_min",
            "status": "TARGET_DEFINED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "CF23233_1_parent_Q_ONLY",
            "component": "D_perp(C_P N_Q)",
            "formula": "parent gauge norm contribution",
            "zero_condition": "C_P, T_Q, N_Q, charge lattice, and current owner are Q_ONLY or REP_TOPOLOGICAL and transverse variations are outside that domain",
            "finite_bound": "C_Q_leak := |D_perp(C_P N_Q)|",
            "status": "EXACT_ZERO_IF_Q_ONLY_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "CF23233_2_visible_lambda",
            "component": "D_perp lambda_A",
            "formula": "independent visible Maxwell kinetic counterterm",
            "zero_condition": "no-extra-F2 operator-domain theorem forbids independent lambda_A(Phi)F_Q^2 terms",
            "finite_bound": "C_lambda_leak := |D_perp lambda_A|",
            "status": "COUNTERMODEL_UNLESS_FORBIDDEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "CF23233_3_hidden_scalar",
            "component": "f_perp_prime(0)",
            "formula": "hidden/transverse scalar gauge-kinetic coefficient",
            "zero_condition": "typed exclusion, exact even/fixed-point symmetry, or strict EM source-root f_perp=lambda_F F_EM with F_EM_prime(0)=0",
            "finite_bound": "C_hidden_leak := |f_perp_prime(0)|",
            "status": "LIVE_TARGET_NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "CF23233_4_readout",
            "component": "D_perp readout/radiative alpha coefficient",
            "formula": "D_perp(delta_lambda_rad + readout_alpha)",
            "zero_condition": "effective/readout functor preserves the same Q_ONLY/no-extra-F2/source-root rule",
            "finite_bound": "C_readout_leak := |D_perp(delta_lambda_rad + readout_alpha)|",
            "status": "REQUIRED_GUARD_UNSIGNED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "CF23233_5_total",
            "component": "total transverse EM F2 slope",
            "formula": "C_F2_perp <= (C_Q_leak + C_lambda_leak + C_hidden_leak + C_readout_leak) / Z_min",
            "zero_condition": "all numerator leaks vanish and Z_min>0",
            "finite_bound": "feeds ||J_EM_F2||_2 <= (1/4) C_F2_perp ||F^2||_2",
            "status": "FINITE_BOUND_FORMULA",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    zero_rows = [
        {
            "route_id": "ZCF3233_0_no_extra_F2",
            "route": "operator-domain exclusion",
            "theorem": "If the parent visible operator domain has no independent transverse scalar multiplying F_Q^2, then D_perp lambda_A=f_perp_prime(0)=0 by absence.",
            "required_parent_signature": "operator-domain exhaustion/no-hidden-visible coefficient theorem or product sequester signed for EM",
            "current_status": "NOT_PARENT_SIGNED",
            "claim_effect": "kills visible and hidden transverse F2 source terms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "ZCF3233_1_Q_ONLY",
            "route": "fixed parent gauge norm",
            "theorem": "If the EM coefficient is only C_P N_Q with fixed representation/topological data, then D_perp(C_P N_Q)=0.",
            "required_parent_signature": "fixed nonrescalable gauge norm, charge lattice, and current owner; no independent lambda/readout terms",
            "current_status": "CONDITIONAL_ONLY",
            "claim_effect": "kills parent norm numerator but not independent visible/hidden/readout counterterms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "ZCF3233_2_strict_source_root",
            "route": "same-branch strict EM source-root",
            "theorem": "If f_perp=lambda_F F_EM(X_perp), F_EM(0)=F_EM_prime(0)=0, and X_perp=0 is the local transverse branch, then f_perp_prime(0)=0.",
            "required_parent_signature": "EM-specific source-root owner, same transverse branch, no multiplier cheat, finite Hessian, readout closure",
            "current_status": "THEOREM_SHAPE_NOT_EM_ATTACHED",
            "claim_effect": "kills hidden scalar slope while retaining second-order finite correction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "ZCF3233_3_readout_closure",
            "route": "observed alpha/readout closure",
            "theorem": "Bare F2 silence promotes to observed alpha silence only if S_eff and readout maps preserve Q_ONLY/no-extra-F2/source-root rules.",
            "required_parent_signature": "radiative/readout functor with no transverse alpha regeneration",
            "current_status": "UNSIGNED_REQUIRED_GUARD",
            "claim_effect": "prevents alpha_eff from reintroducing f_perp_prime",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "route_id": "ZCF3233_4_total_zero",
            "route": "C_F2_perp=0 promotion",
            "theorem": "C_F2_perp=0 only if Q_ONLY/fixed norm, no-extra-F2 or strict source-root, and readout closure all close on the same transverse branch.",
            "required_parent_signature": "ZCF3233_0 or ZCF3233_2, plus ZCF3233_1 where relevant, plus ZCF3233_3",
            "current_status": "FAIL_CURRENT_CLAIM",
            "claim_effect": "would remove EM_F2 from J_perp and leave Poynting/other channels",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    counter_rows = [
        {
            "counter_id": "CEX3233_0_linear_transverse_F2",
            "countermodel": "Z_A=Z_0+epsilon X_perp",
            "why_allowed_now": "X_perp is a scalar direction and F_Q^2 is gauge/diffeomorphism invariant unless no-extra-F2 or source-root forbids it",
            "effect": "C_F2_perp=|epsilon|/Z_min and J_EM_F2 survives",
            "needed_to_remove": "operator-domain exclusion or strict even/source-root symmetry",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CEX3233_1_fixed_norm_plus_lambda",
            "countermodel": "Z_A=C_P N_Q + lambda_A(X_perp)",
            "why_allowed_now": "fixed gauge norm does not by itself forbid independent visible kinetic counterterms",
            "effect": "Q_ONLY parent piece is silent while lambda_A sources EM_F2",
            "needed_to_remove": "no independent F_Q^2 coefficient theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CEX3233_2_strict_root_not_same_branch",
            "countermodel": "metric/local chain has a double-zero but EM transverse coefficient has a linear term",
            "why_allowed_now": "generic double-zero does not transfer to the EM F2 vertex without ownership",
            "effect": "local GR-looking sector may be quiet while transverse EM_F2 source remains live",
            "needed_to_remove": "same parent vertex identity F_GR=F_EM or unique visible-operator domain",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "counter_id": "CEX3233_3_readout_return",
            "countermodel": "bare Z_A is transverse-silent but alpha_eff=alpha_0 exp(epsilon X_perp)",
            "why_allowed_now": "radiative/readout closure remains unsigned",
            "effect": "observed clock/spectroscopy alpha channel sees a transverse source",
            "needed_to_remove": "effective-action/readout functor closure",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    finite_rows = [
        {
            "bound_id": "CFB3233_0_CF2perp",
            "quantity": "C_F2_perp",
            "formula": "C_F2_perp <= (C_Q_leak + C_lambda_leak + C_hidden_leak + C_readout_leak) / Z_min",
            "required_inputs": "Z_min; C_Q_leak; C_lambda_leak; C_hidden_leak; C_readout_leak",
            "status": "FINITE_BOUND_FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "CFB3233_1_JEMF2",
            "quantity": "||J_EM_F2||_2",
            "formula": "||J_EM_F2||_2 <= (1/4) C_F2_perp ||F^2||_2",
            "required_inputs": "C_F2_perp; ||F^2||_2 on scored support",
            "status": "FEEDS_3232_JPERP_BOUND",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "CFB3233_2_zero_switch",
            "quantity": "C_F2_perp_zero",
            "formula": "C_F2_perp=0 if C_Q_leak=C_lambda_leak=C_hidden_leak=C_readout_leak=0",
            "required_inputs": "parent-signed zero for each numerator leak and Z_min>0",
            "status": "ZERO_SWITCH_DEFINED_NOT_ACTIVE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3233_0_result",
            "decision": "CF2PERP_OWNER_GATE_DERIVED_COUNTERMODELS_RETAINED_NO_ZERO_CLAIM",
            "because": "C_F2_perp decomposes into fixed-norm, independent visible, hidden/source-root, and readout terms; exact zero has clear sufficient clauses, but current sources do not sign them on the same transverse branch",
            "claim_status": "NO_ALPHA_NO_CLOCK_NO_WEP_NO_R10_NO_LOCAL_GR_NO_MAXWELL_STRESS_CLAIM",
            "next_action": "either source a finite C_F2_perp bound or move to the separate Poynting boundary flux channel, since EM_F2 zero is not parent-signed yet",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3233_1_next_target",
            "decision": "3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090",
            "because": "EM_F2 zero is now reduced to a parent owner gate; Poynting remains an independent stress/flux channel that F2 algebra cannot remove",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "derive exact/proper/orthogonal Poynting boundary silence or a finite C_flux ||S_EM.n||_B bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, decomp_rows, zero_rows, counter_rows, finite_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    decomp_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, DECOMP, ZERO_AUDIT, COUNTER, FINITE, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    decomp_present = any(row["component_id"] == "CF23233_5_total" for row in decomp_rows)
    zero_total = any(row["route_id"] == "ZCF3233_4_total_zero" for row in zero_rows)
    counter_present = len(counter_rows) >= 4
    finite_present = any(row["bound_id"] == "CFB3233_1_JEMF2" for row in finite_rows)
    next_target = decision_rows[-1]["decision"].startswith("3234-")
    claim_true_count = 0
    for rows in [input_rows, decomp_rows, zero_rows, counter_rows, finite_rows, decision_rows]:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
    no_fw_outputs = all(FW not in [path, *path.parents] for path in out_paths + [DOC])
    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in out_paths:
        try:
            parsed = read_csv(path)
            if not parsed:
                csv_parse_ok = False
            csv_parse_detail.append(path.name)
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    return [
        {"check_id": "VAL3233_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3233_01_decomposition", "pass": b(decomp_present), "detail": "C_F2_perp decomposition present", "generated_utc": now},
        {"check_id": "VAL3233_02_zero_route", "pass": b(zero_total), "detail": "total zero route specified", "generated_utc": now},
        {"check_id": "VAL3233_03_countermodels_retained", "pass": b(counter_present), "detail": f"countermodels={len(counter_rows)}", "generated_utc": now},
        {"check_id": "VAL3233_04_finite_bound", "pass": b(finite_present), "detail": "J_EM_F2 finite bound retained", "generated_utc": now},
        {"check_id": "VAL3233_05_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3233_06_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3233_07_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3233_08_next_target", "pass": b(next_target), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    decomp_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3233 - No-extra-F2 Or Source-root Owner for Transverse EMF2 under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, Maxwell-stress claim, or public-facing result.

## Result

3233 reduces the transverse EM_F2 problem to ownership of one coefficient:

```text
C_F2_perp := |D_perp ln Z_A|
```

or, with a positive denominator,

```text
C_F2_perp <= |D_perp Z_A|_bound / Z_min.
```

The decomposition is:

```text
D_perp Z_A
= D_perp(C_P N_Q)
 + D_perp lambda_A
 + f_perp_prime(0)
 + D_perp(delta_lambda_rad + readout_alpha).
```

Therefore:

```text
C_F2_perp
<= (C_Q_leak + C_lambda_leak + C_hidden_leak + C_readout_leak) / Z_min,

||J_EM_F2||_2 <= (1/4) C_F2_perp ||F^2||_2.
```

Exact zero would follow if all of this is parent-signed on the same transverse branch:

```text
D_perp(C_P N_Q)=0,
D_perp lambda_A=0,
f_perp_prime(0)=0,
D_perp(delta_lambda_rad + readout_alpha)=0.
```

The two strongest zero routes are:

```text
no-extra-F2 operator-domain exclusion,
or same-branch strict EM source-root.
```

But the old countermodels still survive: a legal scalar `Z_A=Z_0+epsilon X_perp`, a fixed gauge norm plus independent `lambda_A(X_perp)`, and readout return.

Current verdict: `CF2PERP_OWNER_GATE_DERIVED_COUNTERMODELS_RETAINED_NO_ZERO_CLAIM`.

## Transverse EMF2 Owner Decomposition

{md_table(decomp_rows, ["component_id", "component", "formula", "zero_condition", "finite_bound", "status", "valid_for_claim"])}

## CF2perp Zero Route Audit

{md_table(zero_rows, ["route_id", "route", "theorem", "required_parent_signature", "current_status", "claim_effect", "valid_for_claim"])}

## EMF2 Countermodel Transfer

{md_table(counter_rows, ["counter_id", "countermodel", "why_allowed_now", "effect", "needed_to_remove", "valid_for_claim"])}

## CF2perp Finite Bound

{md_table(finite_rows, ["bound_id", "quantity", "formula", "required_inputs", "status", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3233_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3233_TRANSVERSE_EMF2_OWNER_DECOMPOSITION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3233_CF2PERP_ZERO_ROUTE_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3233_EMF2_COUNTERMODEL_TRANSFER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3233_CF2PERP_FINITE_BOUND.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3233_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3233_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, decomp_rows, zero_rows, counter_rows, finite_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (DECOMP, decomp_rows),
        (ZERO_AUDIT, zero_rows),
        (COUNTER, counter_rows),
        (FINITE, finite_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, decomp_rows, zero_rows, counter_rows, finite_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, decomp_rows, zero_rows, counter_rows, finite_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()
