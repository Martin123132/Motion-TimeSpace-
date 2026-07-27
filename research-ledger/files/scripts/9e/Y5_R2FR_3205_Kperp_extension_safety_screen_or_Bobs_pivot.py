from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3205-Y5-R2FR-Kperp-extension-safety-screen-or-Bobs-pivot-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3205_INPUTS.csv"
SAFETY = OUT / "P8_Y5_R2FR_3205_SAFETY_SCREEN_RESULTS.csv"
SPECTRAL = OUT / "P8_Y5_R2FR_3205_ZERO_MODE_SPECTRAL_LEDGER.csv"
TRACE_SUPPRESSION = OUT / "P8_Y5_R2FR_3205_TRACE_MAP_AND_LOCAL_SUPPRESSION_AUDIT.csv"
BOBS_PIVOT = OUT / "P8_Y5_R2FR_3205_BOBS_PIVOT_TRIGGER.csv"
DECISION = OUT / "P8_Y5_R2FR_3205_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3205_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


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
    if location == "formalization":
        return FW / relative_path
    if location == "post_checkpoint":
        return ROOT / relative_path
    raise ValueError(location)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lower_terms = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lower_terms):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def b(value: bool) -> str:
    return "true" if value else "false"


SOURCES = [
    {
        "input_id": "SRC3205_00",
        "location": "post_checkpoint",
        "relative_path": "3204-Y5-R2FR-explicit-Kperp-parent-action-extension-contract-or-Bobs-pivot-under-AX1090.md",
        "role": "3204 explicit private Kperp extension and safety gates",
        "terms": ["S_ext", "Delta_perp", "Safety Gates", "Bobs"],
    },
    {
        "input_id": "SRC3205_01",
        "location": "post_checkpoint",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_3204_EXTENSION_SAFETY_GATES.csv",
        "role": "3204 machine-readable safety gates",
        "terms": ["parent-owned observer", "zero modes", "local safety", "no tuned trace"],
    },
    {
        "input_id": "SRC3205_02",
        "location": "formalization",
        "relative_path": "83-parent-equations-v1.md",
        "role": "coarse-grained frame and local-safety parent scaffold",
        "terms": ["coarse-grained frame", "matter/environment frame", "must later be derived", "Kperp"],
    },
    {
        "input_id": "SRC3205_03",
        "location": "formalization",
        "relative_path": "48-routing-projector-definitions.md",
        "role": "projector definitions and not-derived status",
        "terms": ["projector_functions_defined_not_derived", "P_loc", "matter frame", "local safety"],
    },
    {
        "input_id": "SRC3205_04",
        "location": "formalization",
        "relative_path": "75-projected-source-laws.md",
        "role": "Kperp source/boundary suppression conditions",
        "terms": ["K_perp", "L_T", "zero modes", "boundary data are unsuppressed"],
    },
    {
        "input_id": "SRC3205_05",
        "location": "formalization",
        "relative_path": "81-local-closure-status-and-parent-roadmap.md",
        "role": "local closure status and Kperp finite-margin values",
        "terms": ["K_perp", "closure", "not derived", "PPN-bounded"],
    },
    {
        "input_id": "SRC3205_06",
        "location": "post_checkpoint",
        "relative_path": "1650-Y5-R2FR-response-displacement-parent-owner-or-Bobs-source-acquisition.md",
        "role": "Bobs residual acquisition route",
        "terms": ["Bobs", "M_H_ref", "source-measure", "projector"],
    },
]


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        rows.append(
            {
                "input_id": source["input_id"],
                "source_path": rel(path),
                "exists": b(path.exists()),
                "role": source["role"],
                "evidence": evidence(path, source["terms"]),
                "generated_utc": now,
            }
        )
    return rows


def safety_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gate_id": "SCR3205_00_no_ghost_scope",
            "gate": "elliptic/static scope",
            "screen_result": "PASS_PRIVATE_CONTRACT",
            "reason": "the extension explicitly forbids covariant Box^2/fourth-time dynamics and keeps Delta_perp elliptic/domain-normal",
            "claim_impact": "keeps candidate alive privately; does not parent-sign it",
            "next_action": "retain no-ghost restriction in all future rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SCR3205_01_parent_frame_projector",
            "gate": "parent-owned frame/projector",
            "screen_result": "FAIL_CURRENT_CORPUS",
            "reason": "current sources use matter/environment frame and projectors, but record that they must later be derived or are defined-not-derived",
            "claim_impact": "projector/frame leakage must enter Bobs_projector_commutator if not repaired",
            "next_action": "pivot scoring to Bobs; keep extension as private candidate only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SCR3205_02_positive_eta",
            "gate": "positive tensor weight",
            "screen_result": "PASS_AS_EXTENSION_CHOICE_UNSOURCED",
            "reason": "eta_T>0 and positive tensor inner product are consistent as a private action choice, but no parent normalization fixes eta_T",
            "claim_impact": "no physical coefficient or local-GR claim",
            "next_action": "eta_T requires parent normalization or empirical nuisance bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SCR3205_03_zero_modes",
            "gate": "zero-mode control",
            "screen_result": "CONDITIONAL_MATH_PASS_PARENT_TOPOLOGY_OPEN",
            "reason": "with A=-Delta_perp>=0 and D_T=1+ell_T^2 A, D_T has no spectral zero; pure gauge/topological projector kernels remain parent-open",
            "claim_impact": "mathematical kernel control is possible but not parent-signed",
            "next_action": "add zero-mode/topology ledger if extension continues",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SCR3205_04_local_suppression",
            "gate": "local source/boundary suppression",
            "screen_result": "CONDITIONAL_NOT_PARENT_DERIVED",
            "reason": "source laws allow Kperp suppression if J_perp and boundary data carry U_B powers or vanish, but current framework labels this conditional/closure",
            "claim_impact": "Kperp extension cannot prove local GR until suppression is parent-owned or bounded",
            "next_action": "source/bound Kperp and Bobs components",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "SCR3205_05_no_tuned_trace_rank",
            "gate": "actual trace rank map",
            "screen_result": "FAIL_CURRENT_CORPUS",
            "reason": "H2 trace capacity is real, but current MTS does not derive the full-rank map from mismatch slots z into Kperp traces",
            "claim_impact": "rank-four owner remains closure-only unless the parent trace map is derived",
            "next_action": "do not spend another loop on rank without new parent trace primitive; pivot to Bobs for scoring",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def spectral_rows() -> list[dict[str, object]]:
    now = stamp()
    length = 1.0
    ell = 0.2
    rows: list[dict[str, object]] = []
    for mode in range(4):
        lambda_a = (mode * math.pi / length) ** 2
        good_eig = 1.0 + ell**2 * lambda_a
        bad_eig = 1.0 - ell**2 * lambda_a
        rows.append(
            {
                "mode_id": f"SPEC3205_good_{mode}",
                "operator_sign": "D_T=1+ell_T^2 A_with_A_nonnegative",
                "mode_index": mode,
                "lambda_A": f"{lambda_a:.12g}",
                "D_eigenvalue": f"{good_eig:.12g}",
                "DdagD_eigenvalue": f"{good_eig * good_eig:.12g}",
                "zero_mode_status": "NO_ZERO_FOR_THIS_SIGN_CONVENTION",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
        rows.append(
            {
                "mode_id": f"SPEC3205_bad_{mode}",
                "operator_sign": "D_T=1-ell_T^2 A_bad_sign_reference",
                "mode_index": mode,
                "lambda_A": f"{lambda_a:.12g}",
                "D_eigenvalue": f"{bad_eig:.12g}",
                "DdagD_eigenvalue": f"{bad_eig * bad_eig:.12g}",
                "zero_mode_status": "BAD_SIGN_CAN_APPROACH_OR_CROSS_ZERO",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    rows.append(
        {
            "mode_id": "SPEC3205_projector_kernel",
            "operator_sign": "Pi_perp_projector",
            "mode_index": "gauge_or_topological",
            "lambda_A": "not_applicable",
            "D_eigenvalue": "not_applicable",
            "DdagD_eigenvalue": "not_applicable",
            "zero_mode_status": "PARENT_PROJECTOR_OR_TOPOLOGY_OPEN",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    )
    return rows


def trace_suppression_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "audit_id": "TS3205_00_H2_trace",
            "topic": "abstract H2 trace theorem",
            "screen_result": "MATH_PASS",
            "detail": "a fourth-order/H2 operator naturally carries value and normal-derivative traces at both boundaries",
            "claim_impact": "supports private extension mechanics only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "TS3205_01_parent_trace_map",
            "topic": "actual MTS mismatch-to-Kperp trace map",
            "screen_result": "FAIL_CURRENT_CORPUS",
            "detail": "no source derives R:z=(Delta_F_L,Delta_Fprime_L,Delta_F_R,Delta_Fprime_R)->tr(Kperp) with rank four",
            "claim_impact": "blocks parent rank-four promotion",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "TS3205_02_Kperp_suppression_law",
            "topic": "Kperp local suppression",
            "screen_result": "CONDITIONAL_CLOSURE_ONLY",
            "detail": "elliptic estimate works if source and boundary data vanish/suppress with U_B powers; this is not parent-derived in current corpus",
            "claim_impact": "blocks local-GR proof; can become residual bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "TS3205_03_existing_finite_margin_values",
            "topic": "existing finite-margin Kperp values",
            "screen_result": "CLOSURE_EVIDENCE_NOT_DERIVATION",
            "detail": "closure files contain tiny Kperp actual values, but also label local branch as disciplined closure/not derived",
            "claim_impact": "useful for bound intuition; not a parent theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def pivot_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "pivot_id": "BP3205_00_extension_retained",
            "route": "Kperp extension",
            "trigger_state": "RETAIN_PRIVATE_CANDIDATE_ONLY",
            "reason": "no-ghost scope, dimensions, variation, positive choice, and conditional zero-mode math are coherent",
            "next_action": "do not promote; only revisit if parent frame/projector and trace map are newly derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "pivot_id": "BP3205_01_bobs_triggered",
            "route": "Bobs residual acquisition",
            "trigger_state": "TRIGGERED_FOR_SCORING_PATH",
            "reason": "parent frame/projector and actual trace-rank map fail current corpus; local suppression remains conditional",
            "next_action": "build Bobs runner: M_H_ref, source-measure, boundary, projector, corner, total no-cancellation rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "pivot_id": "BP3205_02_claim_forbidden",
            "route": "local-GR/Newton/PPN claim",
            "trigger_state": "FORBIDDEN",
            "reason": "hard safety screen does not parent-sign extension or close local suppression",
            "next_action": "no public/workbench promotion",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "DEC3205_00",
            "result": "KPERP_EXTENSION_RETAINED_PRIVATE_BOBS_PIVOT_TRIGGERED_FOR_SCORING",
            "claim_status": "NO_PARENT_PROMOTION_LOCAL_GR_NEWTON_OR_PPN_CLAIM",
            "decision": "the Kperp extension passes private mathematical sanity but fails current-corpus parent frame/projector and actual trace-map ownership; local suppression is conditional, so empirical/local scoring must pivot to Bobs residual acquisition",
            "best_next_route": "build the Bobs residual acquisition runner with M_H_ref and source-measure/boundary/projector components; keep Kperp extension parked as a future parent-action candidate",
            "next_target": "3206-Y5-R2FR-Bobs-residual-acquisition-runner-after-Kperp-screen-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    safety: list[dict[str, object]],
    spectral: list[dict[str, object]],
    trace_suppression: list[dict[str, object]],
    pivots: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    csv_paths = [INPUTS, SAFETY, SPECTRAL, TRACE_SUPPRESSION, BOBS_PIVOT, DECISION]
    fail_rows = [row for row in safety if row["screen_result"] == "FAIL_CURRENT_CORPUS"]
    good_sign_rows = [row for row in spectral if row["operator_sign"].startswith("D_T=1+")]
    bad_sign_rows = [row for row in spectral if row["operator_sign"].startswith("D_T=1-")]
    return [
        {
            "check_id": "VAL3205_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in inputs)),
            "detail": f"inputs={len(inputs)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3205_01_safety_screen_has_failures",
            "check": "hard screen records current-corpus failures for parent frame/projector and trace map",
            "pass": b(
                len(fail_rows) >= 2
                and any(row["gate"] == "parent-owned frame/projector" for row in fail_rows)
                and any(row["gate"] == "actual trace rank map" for row in fail_rows)
            ),
            "detail": ";".join(f"{row['gate']}={row['screen_result']}" for row in safety),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3205_02_zero_mode_sign_screen",
            "check": "zero-mode ledger keeps good elliptic sign and rejects bad sign risk",
            "pass": b(
                good_sign_rows
                and all(float(row["DdagD_eigenvalue"]) > 0.0 for row in good_sign_rows)
                and any(row["zero_mode_status"] == "BAD_SIGN_CAN_APPROACH_OR_CROSS_ZERO" for row in bad_sign_rows)
            ),
            "detail": "good sign positive; bad sign warning retained",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3205_03_trace_and_suppression_nonclaim",
            "check": "abstract trace passes but parent trace and suppression remain nonclaim",
            "pass": b(
                any(row["screen_result"] == "MATH_PASS" for row in trace_suppression)
                and any(row["screen_result"] == "FAIL_CURRENT_CORPUS" for row in trace_suppression)
                and any(row["screen_result"] == "CONDITIONAL_CLOSURE_ONLY" for row in trace_suppression)
            ),
            "detail": ";".join(f"{row['topic']}={row['screen_result']}" for row in trace_suppression),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3205_04_bobs_pivot_triggered",
            "check": "Bobs residual acquisition is triggered for scoring path",
            "pass": b(any(row["trigger_state"] == "TRIGGERED_FOR_SCORING_PATH" for row in pivots)),
            "detail": ";".join(f"{row['route']}={row['trigger_state']}" for row in pivots),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3205_05_decision_nonclaim",
            "check": "decision parks Kperp and pivots scoring to Bobs without claim",
            "pass": b(
                decisions[0]["result"] == "KPERP_EXTENSION_RETAINED_PRIVATE_BOBS_PIVOT_TRIGGERED_FOR_SCORING"
                and decisions[0]["valid_for_claim"] == "false"
            ),
            "detail": decisions[0]["next_target"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3205_06_no_claim_leak",
            "check": "all generated non-input rows remain valid_for_claim=false",
            "pass": b(all(row.get("valid_for_claim") == "false" for table in [safety, spectral, trace_suppression, pivots, decisions] for row in table)),
            "detail": "no parent promotion, local-GR, Newton, PPN, rank-four, or scoring claim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3205_07_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths)),
            "detail": ";".join(path.name for path in csv_paths),
            "generated_utc": now,
        },
    ]


def write_doc(
    safety: list[dict[str, object]],
    spectral: list[dict[str, object]],
    trace_suppression: list[dict[str, object]],
    pivots: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    lines = [
        "# 3205 - Kperp Extension Safety Screen Or Bobs Pivot Under AX1090",
        "",
        "Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, parent-action promotion, rank-four proof, residual score, R10 pass, clock pass, orbital pass, or public-facing result.",
        "",
        "## Result",
        "",
        "3205 hard-screens the private `K_perp` extension.",
        "",
        "Verdict:",
        "",
        "```text",
        "K_perp extension: retain as private mathematical candidate.",
        "Local/empirical scoring path: pivot to Bobs residual acquisition.",
        "Public/local-GR claim: forbidden.",
        "```",
        "",
        "The reason is precise: no-ghost scope, dimensions, variation, and zero-mode math are salvageable, but the current corpus does not parent-own the frame/projector or the actual rank-four trace map. Local suppression remains conditional.",
        "",
        "## Safety Screen",
        "",
    ]
    for row in safety:
        lines.append(f"- `{row['gate_id']}`: `{row['gate']}` -> `{row['screen_result']}`; {row['reason']}")
    lines.extend(["", "## Zero-Mode Ledger", ""])
    lines.append("- Good sign: `D_T=1+ell_T^2 A` with `A=-Delta_perp>=0` has positive `D_T^dagger D_T` eigenvalues.")
    lines.append("- Bad sign: `D_T=1-ell_T^2 A` is retained as a rejection warning because it can cross zero.")
    lines.append("- Projector/gauge/topology kernels remain parent-open.")
    lines.extend(["", "## Trace And Suppression Audit", ""])
    for row in trace_suppression:
        lines.append(f"- `{row['audit_id']}`: `{row['topic']}` -> `{row['screen_result']}`; {row['detail']}")
    lines.extend(["", "## Pivot", ""])
    for row in pivots:
        lines.append(f"- `{row['pivot_id']}`: `{row['route']}` -> `{row['trigger_state']}`")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"`{decisions[0]['result']}`.",
            "",
            f"Claim status: `{decisions[0]['claim_status']}`.",
            "",
            f"Decision: {decisions[0]['decision']}",
            "",
            f"Best next route: {decisions[0]['best_next_route']}",
            "",
            "Next target:",
            "",
            "```text",
            str(decisions[0]["next_target"]),
            "```",
            "",
            "## Generated Evidence",
            "",
            f"- `{rel(INPUTS)}`",
            f"- `{rel(SAFETY)}`",
            f"- `{rel(SPECTRAL)}`",
            f"- `{rel(TRACE_SUPPRESSION)}`",
            f"- `{rel(BOBS_PIVOT)}`",
            f"- `{rel(DECISION)}`",
            f"- `{rel(VALIDATION)}`",
            "",
            "## Validation",
            "",
        ]
    )
    for row in validations:
        lines.append(f"- `{row['check_id']}`: `{row['pass']}` - {row['detail']}")
    lines.extend(["", "All generated rows remain `valid_for_claim=false`.", ""])
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    inputs = input_rows()
    safety = safety_rows()
    spectral = spectral_rows()
    trace_suppression = trace_suppression_rows()
    pivots = pivot_rows()
    decisions = decision_rows()

    write_csv(INPUTS, inputs)
    write_csv(SAFETY, safety)
    write_csv(SPECTRAL, spectral)
    write_csv(TRACE_SUPPRESSION, trace_suppression)
    write_csv(BOBS_PIVOT, pivots)
    write_csv(DECISION, decisions)

    validations = validation_rows(inputs, safety, spectral, trace_suppression, pivots, decisions)
    write_csv(VALIDATION, validations)
    write_doc(safety, spectral, trace_suppression, pivots, decisions, validations)

    failed = [row for row in validations if row["pass"] != "true"]
    if failed:
        detail = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"3205 validation failed: {detail}")
    print(f"3205 generated {DOC}")


if __name__ == "__main__":
    main()
