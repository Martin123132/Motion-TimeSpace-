from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3239-Y5-R2FR-DeltaK-component-birth-certificate-or-qLoc-arena-bound-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3239_INPUTS.csv"
CHAIN = OUT / "P8_Y5_R2FR_3239_LOCAL_GR_OBSTRUCTION_CHAIN_ROLLFORWARD.csv"
STATUS = OUT / "P8_Y5_R2FR_3239_OBSTRUCTION_STATUS.csv"
FRONTIER = OUT / "P8_Y5_R2FR_3239_CURRENT_FRONTIER.csv"
DECISION = OUT / "P8_Y5_R2FR_3239_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3239_VALIDATION.csv"


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
        "input_id": "SRC3239_00_3238_doc",
        "location": "post_checkpoint",
        "relative_path": "3238-Y5-R2FR-SGK-metric-response-Helmholtz-gap-or-qLoc-bound-for-local-GR-under-AX1090.md",
        "role": "current chain SGK/DeltaK handoff",
        "terms": ["WEAK_SGK_TEMPLATE_EXISTS", "Delta_K", "3239-Y5-R2FR-DeltaK"],
    },
    {
        "input_id": "SRC3239_01_3238_decision",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3238_DECISION.csv",
        "role": "machine handoff to DeltaK component target",
        "terms": ["DEC3238_1_next_target", "DeltaK-component", "qLoc-arena-bound"],
    },
    {
        "input_id": "SRC3239_02_3077_doc",
        "location": "post_checkpoint",
        "relative_path": "3077-Y5-R2FR-DeltaK-component-birth-certificate-or-P4-numeric-source-fill-under-AX1090.md",
        "role": "prior DeltaK component birth certificate result",
        "terms": ["DeltaK Component Birth Certificate", "NO_LIVE_COMPONENT_SOURCE_FOUND", "P4_TQ"],
    },
    {
        "input_id": "SRC3239_03_3077_certificate",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3077_DELTAK_COMPONENT_BIRTH_CERTIFICATE_AUDIT.csv",
        "role": "component-level certificate rows",
        "terms": ["DBC3077_0_DeltaK_00", "BIRTH_CERTIFICATE_NOT_SIGNED", "DBC3077_7_total"],
    },
    {
        "input_id": "SRC3239_04_3077_khat_source",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3077_KHAT_LIVE_COMPONENT_SOURCE_AUDIT.csv",
        "role": "live Khat source absence audit",
        "terms": ["NO_LIVE_COMPONENT_SOURCE_FOUND", "KHS3077_7_verdict", "MISSING_LIVE_KHAT_TENSOR_DEFINITION"],
    },
    {
        "input_id": "SRC3239_05_3078_doc",
        "location": "post_checkpoint",
        "relative_path": "3078-Y5-R2FR-P4-TQ-first-source-or-theorem-zero-under-AX1090.md",
        "role": "P4 TQ theorem-zero/source fallback",
        "terms": ["conditional theorem is exact", "K_P4_TQ", "3079 local geometry field-list signature"],
    },
    {
        "input_id": "SRC3239_06_3078_next",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3078_NEXT_TARGET.csv",
        "role": "P4 TQ next target",
        "terms": ["NEXT3078_0_3079", "metric/coframe-only branch", "T=0,Q=0"],
    },
    {
        "input_id": "SRC3239_07_3079_doc",
        "location": "post_checkpoint",
        "relative_path": "3079-Y5-R2FR-local-geometry-field-list-signature-or-TQ-bound-source-acquisition-under-AX1090.md",
        "role": "local geometry field-list signature result",
        "terms": ["field-list not signed", "Delta_Gamma", "3080-Y5-R2FR"],
    },
    {
        "input_id": "SRC3239_08_3079_next",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3079_NEXT_TARGET.csv",
        "role": "no-hypermomentum/DeltaGamma next target",
        "terms": ["NEXT3079_0_3080", "Delta_Gamma", "boundary + projective"],
    },
    {
        "input_id": "SRC3239_09_3080_doc",
        "location": "post_checkpoint",
        "relative_path": "3080-Y5-R2FR-no-hypermomentum-source-readout-functor-or-DeltaGamma-bound-under-AX1090.md",
        "role": "DeltaGamma source-current obstruction",
        "terms": ["componentized", "mapping those components", "3081 DeltaGamma component map"],
    },
    {
        "input_id": "SRC3239_10_3080_next",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3080_NEXT_TARGET.csv",
        "role": "DeltaGamma component-map handoff",
        "terms": ["NEXT3080_0_3081", "Delta_spin", "Delta_boundary"],
    },
    {
        "input_id": "SRC3239_11_3081_doc",
        "location": "post_checkpoint",
        "relative_path": "3081-Y5-R2FR-DeltaGamma-component-map-to-P4-observables-under-AX1090.md",
        "role": "DeltaGamma observable routing skeleton",
        "terms": ["Projection Matrix Queue", "WEP/clock/lightcone", "3082-Y5-R2FR"],
    },
    {
        "input_id": "SRC3239_12_3081_next",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3081_NEXT_TARGET.csv",
        "role": "WEP/clock/lightcone projection skeleton handoff",
        "terms": ["NEXT3081_0_3082", "eta_AB", "P_WCL"],
    },
    {
        "input_id": "SRC3239_13_3082_doc",
        "location": "post_checkpoint",
        "relative_path": "3082-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton-under-AX1090.md",
        "role": "current first projection skeleton",
        "terms": ["P_WEP_FROM_MATTER_FUNCTOR", "RESPONSE_OPERATORS_NOT_DERIVED", "3083-Y5-R2FR"],
    },
    {
        "input_id": "SRC3239_14_3082_next",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3082_NEXT_TARGET.csv",
        "role": "current frontier after WCL skeleton",
        "terms": ["NEXT3082_0_3083", "P_WEP", "matter_funct"],
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

    chain_rows = [
        {
            "chain_id": "CHAIN3239_0_3238",
            "checkpoint": "3238",
            "result": "weak SGK template exists but strong metric-response/Helmholtz adoption fails",
            "do_not_repeat": "do not re-argue generic S_GK existence",
            "live_obstruction": "Delta_K, H_GK, q_loc residual split",
            "next_from_that_point": "DeltaK component birth certificate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "CHAIN3239_1_3077",
            "checkpoint": "3077",
            "result": "Delta_K component birth certificates are not signed",
            "do_not_repeat": "do not re-run a broad Khat component hunt without new source files",
            "live_obstruction": "no live K_hat source for 00,0i,trace,TF,derivative/boundary,units,projector/domain",
            "next_from_that_point": "P4 TQ fallback or source-bound route",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "CHAIN3239_2_3078",
            "checkpoint": "3078",
            "result": "metric/coframe-only T=Q=0 theorem is exact but not parent-signed",
            "do_not_repeat": "do not source-hunt torsion/nonmetricity coefficients before trying the field-list signature",
            "live_obstruction": "parent field list, derived connection declaration, source/readout connection-current silence",
            "next_from_that_point": "local geometry field-list signature",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "CHAIN3239_3_3079",
            "checkpoint": "3079",
            "result": "local geometry field-list signature remains unsigned",
            "do_not_repeat": "do not repeat the old distortion-owner target blindly",
            "live_obstruction": "Delta_Gamma source/readout current or no-hypermomentum theorem",
            "next_from_that_point": "no-hypermomentum/source-readout functor or DeltaGamma bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "CHAIN3239_4_3080",
            "checkpoint": "3080",
            "result": "no-hypermomentum/source-readout functor not signed; DeltaGamma components staged",
            "do_not_repeat": "do not swing at a broad source-current zero theorem without component maps",
            "live_obstruction": "Delta_spin, Delta_source, Delta_readout, Delta_projective, Delta_boundary values/maps",
            "next_from_that_point": "DeltaGamma component map to P4 observables",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "CHAIN3239_5_3081",
            "checkpoint": "3081",
            "result": "DeltaGamma observable map skeleton refreshed but projection matrices missing",
            "do_not_repeat": "do not score R10/PPN/WEP/clock/orbital without projection matrices",
            "live_obstruction": "P_R10, P_WEP, P_PPN, P_clock, P_lightcone, P_orbital",
            "next_from_that_point": "WEP/clock/lightcone projection block",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "chain_id": "CHAIN3239_6_3082",
            "checkpoint": "3082",
            "result": "WEP/clock/lightcone projection skeleton written; response operators not derived",
            "do_not_repeat": "do not insert coefficients for WEP/clock/lightcone",
            "live_obstruction": "P_WEP, P_clock, P_lightcone, projective guard, units, component values",
            "next_from_that_point": "P_WEP from matter functor or component-bound rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    status_rows = [
        {
            "status_id": "OBS3239_0_SGK_DeltaK",
            "layer": "SGK/DeltaK",
            "current_status": "EXPLICIT_RESIDUAL_NOT_ZERO",
            "what_is_known": "weak action template exists; strong live metric-response identity is not signed",
            "still_missing": "live Gamma_eff density, Khat component formulas, Kmetric values, Helmholtz evaluability",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "status_id": "OBS3239_1_P4_TQ",
            "layer": "connection torsion/nonmetricity",
            "current_status": "CONDITIONAL_ZERO_ONLY",
            "what_is_known": "metric/coframe-only branch would force T=Q=0 and K_P4_TQ=0",
            "still_missing": "parent field list, derived connection declaration, no independent connection/source current",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "status_id": "OBS3239_2_DeltaGamma",
            "layer": "source/readout connection current",
            "current_status": "COMPONENTS_STAGED_NO_VALUES",
            "what_is_known": "Delta_spin/material/source/clock/lightcone/orbital/projective channels are named",
            "still_missing": "component values or zero theorems, common units, response/projection matrices",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "status_id": "OBS3239_3_WCL_projection",
            "layer": "WEP/clock/lightcone first projection block",
            "current_status": "SKELETON_WRITTEN_NONCLAIM",
            "what_is_known": "(eta_AB, clock_residual, lightcone_residual)^T = P_WCL * DeltaGamma_block is declared",
            "still_missing": "P_WEP, P_clock, P_lightcone, projective all-sector silence, units, source bounds",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    frontier_rows = [
        {
            "frontier_id": "FR3239_0_current_best_target",
            "target": "P_WEP response operator from matter/source functor",
            "why_this_not_DeltaK": "DeltaK component birth certificate was already audited and failed without live Khat sources; P4/DeltaGamma chain has advanced to observable projection operators",
            "starting_equation": "eta_AB = P_WEP_spin*Delta_spin + P_WEP_material*Delta_material_marker + P_WEP_clock*Delta_clock_rod + P_WEP_projective*Delta_projective_boundary",
            "must_derive_or_bound": "P_WEP material/composition tensor, no species/source re-entry, eta units/source bound, component zero/value inputs",
            "blocked_claims": "WEP; local GR; Newton; source coupling; clock/lightcone consistency",
            "next_checkpoint": "3240-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "frontier_id": "FR3239_1_secondary_targets",
            "target": "P_clock and P_lightcone response operators",
            "why_this_not_DeltaK": "clock/lightcone share the same matter/coframe/readout leakage as WEP and should follow once P_WEP is formalized",
            "starting_equation": "clock_residual, lightcone_residual = functions of Delta_clock_rod, Delta_spin, Delta_material, Delta_lightcone, Delta_projective",
            "must_derive_or_bound": "clock functional, clock species basis, null-cone operator, photon branch, gamma output convention",
            "blocked_claims": "clock tests; gamma/lightcone; PPN scalar leakage",
            "next_checkpoint": "after P_WEP skeleton unless WEP route fails hard",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3239_0_rollforward",
            "decision": "DELTAK_TARGET_ALREADY_CLOSED_AS_UNSIGNED_IN_PRIOR_CHAIN",
            "because": "3077 already audited the requested DeltaK component birth certificate and found no live Khat/Kmetric component certificates; 3238 reintroduced it as the SGK bottleneck, so 3239 rolls that evidence forward instead of looping",
            "claim_status": "NO_DELTAK_ZERO_NO_QLOC_ZERO_NO_LOCAL_GR_CLAIM",
            "next_action": "use the downstream P4/DeltaGamma/WCL chain as the active local-coupling route",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3239_1_frontier",
            "decision": "CURRENT_FRONTIER_IS_PWEP_RESPONSE_OPERATOR",
            "because": "3082 has already built the WEP/clock/lightcone projection skeleton, and the first missing response operator is P_WEP from the matter/source functor",
            "claim_status": "NO_WEP_NO_CLOCK_NO_LIGHTCONE_NO_NEWTON_NO_LOCAL_GR_CLAIM",
            "next_action": "derive P_WEP from the matter/source functor or stage component-bound rows without coefficients or scores",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, chain_rows, status_rows, frontier_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    chain_rows: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    frontier_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    output_paths = [INPUTS, CHAIN, STATUS, FRONTIER, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    evidence_ready = all("MISSING_SOURCE" not in str(row["evidence_hits"]) and "NO_MATCH" not in str(row["evidence_hits"]) for row in input_rows)
    chain_checkpoints = {row["checkpoint"] for row in chain_rows}
    chain_complete = {"3238", "3077", "3078", "3079", "3080", "3081", "3082"}.issubset(chain_checkpoints)
    deltak_not_looped = any(row["decision_id"] == "DEC3239_0_rollforward" for row in decision_rows)
    frontier_pw = any(row["frontier_id"] == "FR3239_0_current_best_target" and "P_WEP" in str(row["target"]) for row in frontier_rows)
    claim_true_count = 0
    for row_group in [input_rows, chain_rows, status_rows, frontier_rows, decision_rows]:
        for row in row_group:
            if str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true":
                claim_true_count += 1
    no_fw_outputs = all(not str(path).lower().startswith(str(FW).lower()) for path in output_paths + [DOC])
    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in output_paths:
        try:
            parsed = read_csv(path)
            if not parsed:
                csv_parse_ok = False
            csv_parse_detail.append(path.name)
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    return [
        {"check_id": "VAL3239_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3239_01_evidence_hits", "pass": b(evidence_ready), "detail": "no MISSING_SOURCE or NO_MATCH in source register", "generated_utc": now},
        {"check_id": "VAL3239_02_chain_complete", "pass": b(chain_complete), "detail": "chain covers 3238 plus 3077-3082", "generated_utc": now},
        {"check_id": "VAL3239_03_no_DeltaK_loop", "pass": b(deltak_not_looped), "detail": "DeltaK component target rolled forward instead of repeated", "generated_utc": now},
        {"check_id": "VAL3239_04_frontier_PWEP", "pass": b(frontier_pw), "detail": "current frontier is P_WEP response operator", "generated_utc": now},
        {"check_id": "VAL3239_05_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3239_06_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3239_07_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    chain_rows: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    frontier_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3239 - DeltaK Component Birth Certificate Or qLoc Arena Bound under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, WEP pass, clock pass, lightcone pass, PPN pass, R10 pass, source-normalization claim, or public-facing result.

## Result

3239 answers the `3238` handoff without looping.

`3238` reduced the strong `S_GK` problem to `Delta_K`, `H_GK`, and `q_loc` residuals. But the exact `Delta_K` component-birth route was already attacked in the prior chain:

```text
3077: Delta_K component certificates not signed.
3078: P4_TQ conditional zero route written but not parent-signed.
3079: local geometry field list not signed.
3080: no-hypermomentum/source-readout functor not signed; DeltaGamma components staged.
3081: DeltaGamma observable map skeleton written; projection matrices missing.
3082: WEP/clock/lightcone projection skeleton written; response operators not derived.
```

So the current live frontier is not another broad `Delta_K` hunt. It is:

```text
eta_AB
= P_WEP_spin Delta_spin
 + P_WEP_material Delta_material_marker
 + P_WEP_clock Delta_clock_rod
 + P_WEP_projective Delta_projective_boundary.
```

The next useful derivation target is `P_WEP`: derive it from the matter/source functor, or stage component-bound rows without coefficients or scores.

Current verdict: `DELTAK_TARGET_ROLLED_FORWARD_CURRENT_FRONTIER_IS_PWEP_RESPONSE_OPERATOR`.

## Local-GR Obstruction Chain Rollforward

{md_table(chain_rows, ["chain_id", "checkpoint", "result", "do_not_repeat", "live_obstruction", "next_from_that_point", "valid_for_claim"])}

## Obstruction Status

{md_table(status_rows, ["status_id", "layer", "current_status", "what_is_known", "still_missing", "claim_allowed", "valid_for_claim"])}

## Current Frontier

{md_table(frontier_rows, ["frontier_id", "target", "why_this_not_DeltaK", "starting_equation", "must_derive_or_bound", "blocked_claims", "next_checkpoint", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3239_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3239_LOCAL_GR_OBSTRUCTION_CHAIN_ROLLFORWARD.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3239_OBSTRUCTION_STATUS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3239_CURRENT_FRONTIER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3239_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3239_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, chain_rows, status_rows, frontier_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (CHAIN, chain_rows),
        (STATUS, status_rows),
        (FRONTIER, frontier_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, chain_rows, status_rows, frontier_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, chain_rows, status_rows, frontier_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()
