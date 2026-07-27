from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "931-Y5-R10-gamma-PPN-projection-coefficient-or-KBFH-bound-envelope.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "930_doc",
            "path": "930-Y5-R10-KBFH-coupling-origin-minimal-input-contract-or-first-scoreable-bound-row.md",
            "role": "selected R3_gamma as first scoreable target and wrote KBFH envelope",
            "needle": "least-messy first empirical row is `R3_gamma`",
        },
        {
            "source_id": "930_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_930_VALIDATION.csv",
            "role": "proves 930 validation passed",
            "needle": "V930_12_validation_rows_ready",
        },
        {
            "source_id": "930_envelope",
            "path": "source-intake/mts_residuals/P8_Y5_R10_930_SYMBOLIC_BOUND_ENVELOPE.csv",
            "role": "symbolic gamma K_BF_H bound envelope",
            "needle": "ENV930_3_R3_gamma",
        },
        {
            "source_id": "930_first_scoreable",
            "path": "source-intake/mts_residuals/P8_Y5_R10_930_FIRST_SCOREABLE_ROW_AUDIT.csv",
            "role": "R3_gamma selection rationale",
            "needle": "FS930_0_R3_gamma",
        },
        {
            "source_id": "local_bound_claims",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "Cassini gamma bound source row",
            "needle": "Cassini_Shapiro_gamma_2003",
        },
        {
            "source_id": "930_chain",
            "path": "source-intake/mts_residuals/P8_Y5_R10_930_COUPLING_DERIVATION_CHAIN.csv",
            "role": "epsilon_FM=|K_BF_H| X_FM residual amplitude definition",
            "needle": "KD930_5_weak_field_residual_amplitude",
        },
    ]
    rows = []
    for spec in specs:
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def gamma_projection_derivation() -> list[dict[str, str]]:
    rows = [
        {
            "derivation_id": "GAM931_0_metric_ansatz",
            "step": "write weak-field residual split",
            "mathematical_form": "g_00=-1+2 U_N + 2 a_FM epsilon_FM U_N; g_ij=delta_ij(1+2 U_N + 2 b_FM epsilon_FM U_N)",
            "result": "a_FM controls Newtonian time-potential response; b_FM controls spatial-curvature response",
            "status": "ansatz_for_projection_not_parent_derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "GAM931_1_observed_G_calibration",
            "step": "calibrate U_obs by g_00",
            "mathematical_form": "U_obs := U_N(1+a_FM epsilon_FM)",
            "result": "a universal time-potential rescaling is absorbed into measured GM only after source normalization is fixed",
            "status": "conditional_readout_definition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "GAM931_2_gamma_projection",
            "step": "compute gamma_eff relative to U_obs",
            "mathematical_form": "gamma_eff=(1+b_FM epsilon_FM)/(1+a_FM epsilon_FM)=1+(b_FM-a_FM)epsilon_FM+O(epsilon_FM^2)",
            "result": "C_gamma_FM = b_FM - a_FM",
            "status": "projection_formula_derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "GAM931_3_gamma_bound",
            "step": "apply Cassini-style gamma lock",
            "mathematical_form": "|gamma-1| = |C_gamma_FM epsilon_FM| <= 2.3e-05",
            "result": "|epsilon_FM| <= 2.3e-05/|b_FM-a_FM| when C_gamma_FM is nonzero",
            "status": "symbolic_bound_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "GAM931_4_KBFH_bound",
            "step": "substitute epsilon_FM=|K_BF_H|X_FM",
            "mathematical_form": "|K_BF_H| <= 2.3e-05/(|b_FM-a_FM| X_FM)",
            "result": "K_BF_H can be bounded only after C_gamma_FM and X_FM are parent-derived or sourced",
            "status": "symbolic_bound_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def zero_conditions() -> list[dict[str, str]]:
    specs = [
        ("ZG931_0_equal_metric_response", "a_FM=b_FM", "residual is conformal/universal at first PPN order", "sets C_gamma_FM=0"),
        ("ZG931_1_same_source_charge", "U_obs sourced by the same Hilbert/worldtube charge as spatial curvature", "prevents hidden source-frame split", "keeps gamma from seeing wrong-source curvature"),
        ("ZG931_2_no_anisotropic_spatial_stress", "tracefree spatial residual stress vanishes or is second order", "prevents b_FM-only curvature leakage", "protects gamma and preferred-frame rows"),
        ("ZG931_3_no_offdiagonal_vector_hair", "g_0i/vector residuals vanish in local static branch", "prevents alpha_i leakage while deriving gamma", "keeps PPN sector separated"),
        ("ZG931_4_XFM_finite_and_source_owned", "X_FM finite, source-owned, and not calibrated per experiment", "prevents bound envelope from hiding a fit knob", "makes gamma row scoreable if C_gamma_FM nonzero"),
    ]
    rows = []
    for condition_id, condition, meaning, effect in specs:
        rows.append(
            {
                "condition_id": condition_id,
                "condition": condition,
                "meaning": meaning,
                "effect_if_parent_signed": effect,
                "current_status": "not_parent_signed",
                "missing_evidence": "weak-field parent variation and source/readout map",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def bound_envelope() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "GB931_0_gamma_epsilon_bound",
            "input_needed": "C_gamma_FM=b_FM-a_FM",
            "bound_formula": "|epsilon_FM| <= 2.3e-05/|C_gamma_FM|",
            "numeric_status": "blocked_missing_C_gamma_FM",
            "interpretation": "if C_gamma_FM is order unity, epsilon_FM must be below Cassini gamma scale",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "bound_id": "GB931_1_gamma_KBFH_bound",
            "input_needed": "C_gamma_FM and X_FM",
            "bound_formula": "|K_BF_H| <= 2.3e-05/(|C_gamma_FM| X_FM)",
            "numeric_status": "blocked_missing_C_gamma_FM_and_X_FM",
            "interpretation": "this becomes the first scoreable non-R10 K_BF_H bound if the projection coefficient and amplitude are derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "bound_id": "GB931_2_gamma_zero_branch",
            "input_needed": "parent proof a_FM=b_FM",
            "bound_formula": "C_gamma_FM=0 => gamma row silent at O(epsilon_FM)",
            "numeric_status": "blocked_missing_zero_proof",
            "interpretation": "a successful zero proof is good for local GR but forces the next bound to beta, WEP, clocks, or alpha_i",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC931_0_projection_result",
            "decision": "C_gamma_FM_equals_b_minus_a",
            "reason": "gamma compares spatial curvature against the Newtonian potential calibrated by g_00",
            "consequence": "the gamma row is a clean test of unequal residual metric response",
            "next_action": "try to prove a_FM=b_FM from parent/source readout, or source C_gamma_FM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC931_1_bound_status",
            "decision": "retain_symbolic_bound_only",
            "reason": "C_gamma_FM and X_FM are not yet parent-derived",
            "consequence": "no gamma pass/fail and no numeric K_BF_H bound",
            "next_action": "932-Y5-R10-gamma-zero-parent-condition-or-beta-WEP-pivot.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC931_2_GR_route",
            "decision": "gamma_zero_is_better_than_gamma_fit",
            "reason": "local GR wants C_gamma_FM=0 from structure, not a small tuned residual",
            "consequence": "next derivation should attempt the equal-response/no-anisotropic-stress theorem",
            "next_action": "derive equal metric response conditions before scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE931_0_Cgamma_numeric",
            "claim": "C_gamma_FM is known numerically or zero",
            "evidence": "C_gamma_FM=b_FM-a_FM derived, but a_FM and b_FM are not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE931_1_gamma_bound_score",
            "claim": "R3_gamma scores or bounds K_BF_H numerically",
            "evidence": "X_FM remains missing and C_gamma_FM is symbolic",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE931_2_local_GR_gamma",
            "claim": "local GR gamma limit is derived",
            "evidence": "zero conditions listed but not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            count += 1
    return count


def validation(
    sources: list[dict[str, str]],
    gamma_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    bounds: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, ok: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": stamp()})

    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    v930 = read_csv(OUT / "P8_Y5_BRR545_930_VALIDATION.csv")
    v930_clean = v930 and all(row.get("result") == "pass" for row in v930)
    projection_written = any(row["derivation_id"] == "GAM931_2_gamma_projection" and "b_FM-a_FM" in row["mathematical_form"] for row in gamma_rows)
    symbolic_bound_written = any(row["bound_id"] == "GB931_1_gamma_KBFH_bound" and "2.3e-05" in row["bound_formula"] for row in bounds)
    zero_conditions_complete = len(zero_rows) == 5 and all(row["valid_for_claim"] == "false" for row in zero_rows)
    no_claims = all(row["valid_for_claim"] == "false" for row in gamma_rows + zero_rows + bounds + decision_rows + gates)
    gates_false = all(row["claim_allowed"] == "false" for row in gates)
    next_ok = any("932-Y5-R10-gamma-zero" in row["next_action"] for row in decision_rows)
    fw_changed = formalization_changed_after_start()

    add("V931_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present" if source_ok else "missing source path or needle")
    add("V931_1_prior_930_clean", v930_clean, "P8_Y5_BRR545_930_VALIDATION.csv clean")
    add("V931_2_gamma_projection_written", projection_written, "C_gamma_FM=b_FM-a_FM projection formula written")
    add("V931_3_symbolic_bound_written", symbolic_bound_written, "gamma K_BF_H symbolic bound envelope written")
    add("V931_4_zero_conditions_complete", zero_conditions_complete, "five gamma-zero conditions listed")
    add("V931_5_no_claims_promoted", no_claims, "all generated rows are nonclaim")
    add("V931_6_claim_gates_false", gates_false, "all claim gates remain false")
    add("V931_7_formalization_workbench_untouched", fw_changed == 0, f"formalization_changed_after_start={fw_changed}")
    add("V931_8_next_target_selected", next_ok, "932-Y5-R10-gamma-zero-parent-condition-or-beta-WEP-pivot.md")
    add("V931_9_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    gamma_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    bounds: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    gates: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 931 - Y5/R10 Gamma PPN Projection Coefficient Or KBFH Bound Envelope

Generated: `{stamp()}`

Status: `Y5_R10_931_gamma_projection_formula_derived_symbolic_KBFH_bound_only_no_claim`

Claim ceiling: `PPN_gamma_projection_contract_only_no_numeric_Cgamma_no_KBFH_bound_no_local_GR_pass`

## Result

For the direct metric PPN row, the residual projection is clean:

```text
g_00 = -1 + 2 U_N + 2 a_FM epsilon_FM U_N,
g_ij = delta_ij(1 + 2 U_N + 2 b_FM epsilon_FM U_N),
gamma_eff = (1+b_FM epsilon_FM)/(1+a_FM epsilon_FM)
          = 1 + (b_FM-a_FM) epsilon_FM + O(epsilon_FM^2).
```

So

```text
C_gamma_FM = b_FM - a_FM.
```

This is a useful fork. If the parent theory proves `a_FM=b_FM`, then the gamma row is silent at first order and that is good news for the local-GR route. If not, Cassini-style gamma gives the symbolic envelope

```text
|K_BF_H| <= 2.3e-05 / (|C_gamma_FM| X_FM).
```

No numeric bound is claimed because `C_gamma_FM` and `X_FM` are still not parent-derived.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Gamma Projection Derivation

{md_table(gamma_rows, ["derivation_id", "step", "mathematical_form", "result", "status", "valid_for_claim"])}

## Gamma-Zero Conditions

{md_table(zero_rows, ["condition_id", "condition", "meaning", "effect_if_parent_signed", "current_status", "valid_for_claim"])}

## Bound Envelope

{md_table(bounds, ["bound_id", "input_needed", "bound_formula", "numeric_status", "interpretation", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

`932-Y5-R10-gamma-zero-parent-condition-or-beta-WEP-pivot.md`

Try to prove `a_FM=b_FM` from parent/source readout. If that fails, keep the gamma envelope as a symbolic bound and pivot to `beta`, WEP, or clocks.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    gamma_rows = gamma_projection_derivation()
    zero_rows = zero_conditions()
    bounds = bound_envelope()
    decision_rows = decisions()
    gates = claim_gates()
    validation_rows = validation(sources, gamma_rows, zero_rows, bounds, decision_rows, gates)

    write_csv(
        OUT / "P8_Y5_R10_931_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_931_GAMMA_PROJECTION_DERIVATION.csv",
        gamma_rows,
        ["derivation_id", "step", "mathematical_form", "result", "status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_931_GAMMA_ZERO_CONDITIONS.csv",
        zero_rows,
        ["condition_id", "condition", "meaning", "effect_if_parent_signed", "current_status", "missing_evidence", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_931_KBFH_BOUND_ENVELOPE.csv",
        bounds,
        ["bound_id", "input_needed", "bound_formula", "numeric_status", "interpretation", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_931_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_931_CLAIM_GATE.csv",
        gates,
        ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_931_NEXT_TARGET.csv",
        [
            {
                "next_target": "932-Y5-R10-gamma-zero-parent-condition-or-beta-WEP-pivot.md",
                "objective": "prove a_FM=b_FM from parent/source readout, or retain gamma symbolic bound and pivot to beta/WEP/clocks",
                "include": "equal metric response theorem, no anisotropic spatial stress, source/readout equality, beta/WEP fallback decision",
                "exclude": "numeric gamma pass without C_gamma_FM, hidden G/M absorption, R10 placeholder claim, GitHub action, formalization-workbench edits",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        ],
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_931_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, gamma_rows, zero_rows, bounds, decision_rows, gates, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")
    print("Y5_R10_931_gamma_projection_formula_derived_symbolic_KBFH_bound_only_no_claim")
    print(f"wrote {DOC}")
    print("next target: 932-Y5-R10-gamma-zero-parent-condition-or-beta-WEP-pivot.md")


if __name__ == "__main__":
    main()
