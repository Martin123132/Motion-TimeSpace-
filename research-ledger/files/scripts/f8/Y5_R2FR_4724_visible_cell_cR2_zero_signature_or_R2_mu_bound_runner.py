from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4724"
CLAIM_ID = "L-566"
MARKER = "PPC4161_VISIBLE_CELL_CR2_ZERO_SIGNATURE_OR_R2_MU_BOUND_RUNNER_4724"
PACKET_MARKER = "PPC4161_PACKET_VISIBLE_CELL_CR2_ZERO_SIGNATURE_OR_R2_MU_BOUND_RUNNER_4724"
DECISION = "VISIBLE_CELL_CR2_ZERO_DERIVED_CONDITIONAL_TOTAL_CR2EFF_UNSIGNED_FINITE_MU_BOUND_RUNNER_STAGED_NONCLAIM"
NEXT_TARGET = "4725-Y5-R2FR-no-bare-R2-parent-grammar-proof-or-cbare-finite-row.md"

DOC_PATH = POST / "4724-Y5-R2FR-visible-cell-cR2-zero-signature-or-R2-mu-bound-runner.md"
FORMAL_PATH = FORMAL / "740-PPC4161-visible-cell-cR2-zero-signature-or-R2-mu-bound-runner.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4724_SOURCE_REGISTER.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4724_TOTAL_CR2_ZERO_THEOREM_ROWS.csv"
COMPONENT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4724_CR2_COMPONENT_SIGNATURE_AUDIT.csv"
MU_RUNNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4724_MU_BOUND_RUNNER_INPUT.csv"
MU_RUNNER_RESULTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4724_MU_BOUND_RUNNER_RESULTS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4724_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4724_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4724_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4724_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4724_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4724_VALIDATION.csv"


SOURCE_SPECS = [
    ("SRC4724_0", POST / "4723-Y5-R2FR-parent-EH-signature-evidence-hunt-or-R2-mR-alpha-first-source-row.md", "visible-cell", "4723 handoff to c_R2 gate."),
    ("SRC4724_1", SOURCE_DIR / "P8_Y5_R2FR_4723_R2_MR_ALPHA_FIRST_SOURCE_ROW.csv", "R2SRC4723_0_mu_or_cR2eff", "4723 first R2 source row."),
    ("SRC4724_2", SOURCE_DIR / "P8_Y5_R2FR_4471_NO_GRAIN_THEOREM.csv", "NG4471_5_verdict", "4471 no-grain visible-cell theorem verdict."),
    ("SRC4724_3", SOURCE_DIR / "P8_Y5_R2FR_4471_FIRST_CR2EFF_INTAKE_ROW.csv", "CR2I4471_2_total_effective_component", "4471 total c_R2_eff intake row."),
    ("SRC4724_4", SOURCE_DIR / "P8_Y5_R2FR_4471_CONTINUUM_SCALING_DERIVATION.csv", "SCL4471_1_quadratic_visible", "4471 visible quadratic scaling derivation."),
    ("SRC4724_5", SOURCE_DIR / "P8_Y5_R2FR_4504_FINITE_BOUND_CONTRACT.csv", "FB4504_1_standard_mu_bound", "4504 finite mu bound contract."),
    ("SRC4724_6", SOURCE_DIR / "P8_Y5_R2FR_4504_STANDARD_BOUND_IMPORT.csv", "SB4504_2_combined_range", "4504 standard scalar range bound import."),
    ("SRC4724_7", SOURCE_DIR / "P8_Y5_R2FR_4504_R2FR_SCALARON_VARIATION_LAW.csv", "R2V4504_2_trace", "4504 scalaron equation."),
    ("SRC4724_8", SOURCE_DIR / "P8_Y5_PARENT_QLOC_1589_COEFFICIENT_SOURCE_HUNT.csv", "HUNT1589_7_verdict", "1589 coefficient source hunt verdict."),
    ("SRC4724_9", SOURCE_DIR / "P8_Y5_R2FR_4540_EFT_RESIDUAL_ENVELOPE.csv", "EFT4540_5_cR2", "4540 live c_R2 residual envelope."),
    ("SRC4724_10", SOURCE_DIR / "P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv", "R2_fR_scalar_mode", "R11 R2/f(R) double-zero map."),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    write_text(path, existing + separator + block.rstrip() + "\n")


def source_path(source_id: str) -> str:
    for row_id, path, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path)
    raise KeyError(source_id)


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def zero_theorem_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "TCZ4724_0_total_law",
            "Define the local scalar curvature-square coefficient as c_R2_eff_total = c_R2_cell + c_bare + 1/2 B^T L^-1 B + c_measure + c_boundary.",
            "This is the exact object that must vanish or be bounded before the R2/f(R) channel can be removed from the local-GR residual.",
            "DERIVED_BOOKKEEPING_LAW",
            "All components need same-normalization source ownership.",
        ),
        (
            "TCZ4724_1_no_cancellation_rule",
            "A total-zero claim is not accepted from accidental cancellation between independent unknown components.",
            "Require componentwise zero, sign/positive identity, or a parent Ward/topological identity explicitly tying the components.",
            "DERIVED_NO_SMUGGLING_RULE",
            "No such cross-component cancellation identity is currently sourced.",
        ),
        (
            "TCZ4724_2_visible_cell_zero",
            "c_R2_cell -> 0 if ell is pure refinement gauge, c2_visible is smooth, and no singular counterterm/physical grain is introduced.",
            "This closes only the visible-cell contribution, not the total coefficient.",
            "CONDITIONAL_DERIVATION_AVAILABLE",
            "Parent refinement-gauge/no-physical-grain signature is not globally signed.",
        ),
        (
            "TCZ4724_3_bare_operator_zero",
            "c_bare=0 only if the parent grammar excludes bare R^2, f(R), R F(Box) R and curvature-square counterterms before reduction.",
            "This is the next least-ambiguous proof target because it attacks an action-language term directly.",
            "UNPROVED_PARENT_GRAMMAR_CLAUSE",
            "No parent-owned no-bare-R2 grammar row has been found.",
        ),
        (
            "TCZ4724_4_hidden_exchange_zero",
            "1/2 B^T L^-1 B=0 if the hidden-visible linear vertex B vanishes, L^-1 is projected out, or hidden modes are absent/heavy with a signed decoupling theorem.",
            "This captures memory/fibre exchange without pretending it is already gone.",
            "UNSIGNED_HIDDEN_VERTEX_CLAUSE",
            "1589 found B_mem/B_h zero only as private closure or unsigned branch.",
        ),
        (
            "TCZ4724_5_measure_boundary_zero",
            "c_measure+c_boundary=0 only if the measure/Jacobian and boundary/corner terms are exact, topological, fixed or Hamiltonian-routed without bulk scalar source.",
            "This prevents boundary or measure leakage from masquerading as a vanished R2 channel.",
            "UNSIGNED_MEASURE_BOUNDARY_CLAUSE",
            "No sourced global measure/boundary no-residue theorem is present.",
        ),
        (
            "TCZ4724_6_verdict",
            "Visible-cell suppression is a real derivation, but total c_R2_eff=0 is not yet proved.",
            "The correct branch is a conditional zero theorem plus a finite mu bound runner, both nonclaim until parent rows exist.",
            "TOTAL_ZERO_NOT_PROVED",
            "Move next to no-bare-R2 parent grammar proof or c_bare finite row.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "statement": statement,
            "derivation_effect": effect,
            "current_status": status,
            "open_debt": debt,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for theorem_id, statement, effect, status, debt in specs
    ]


def component_audit_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("CR2COMP4724_0_visible_cell", "c_R2_cell", "xi_shape*c2_visible*ell_cell^2/N_EH", "zero if ell is gauge refinement, c2 smooth, no singular running", "conditional_available_parent_unsigned", False, "CONDITIONAL_ZERO_ONLY"),
        ("CR2COMP4724_1_bare", "c_bare", "bare R^2/f(R)/R F(Box) R coefficient", "zero if parent grammar forbids the operator or makes it exact/topological", "missing_parent_grammar_proof", False, "MISSING_c_bare_ZERO_OR_VALUE"),
        ("CR2COMP4724_2_hidden_exchange", "0.5 B^T L^-1 B", "hidden/memory/fibre exchange contribution", "zero if B=0, projected out, or hidden modes absent/heavy by signed theorem", "hidden_vertex_unsigned", False, "MISSING_B_L_MAP_OR_ZERO"),
        ("CR2COMP4724_3_measure", "c_measure", "measure/Jacobian/frame-transfer contribution", "zero if measure is curvature-square blind or only renormalizes EH/topological terms", "measure_owner_missing", False, "MISSING_MEASURE_ZERO_OR_VALUE"),
        ("CR2COMP4724_4_boundary", "c_boundary", "boundary/corner/Hamiltonian-routed contribution", "zero if fixed/topological/source-blind with no bulk scalar source", "boundary_no_residue_unsigned", False, "MISSING_BOUNDARY_ZERO_OR_VALUE"),
        ("CR2COMP4724_5_total", "c_R2_eff_total", "sum of all components", "zero if every component zero or a signed no-cancellation identity exists", "total_zero_unsigned", False, "MISSING_TOTAL_ZERO_CERTIFICATE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": component_id,
            "component": component,
            "formula": formula,
            "zero_condition": zero_condition,
            "evidence_status": status,
            "parent_signed": parent_signed,
            "current_value": value,
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_action": "prove no-bare parent grammar first" if component_id.endswith("_bare") else "retain as component of total c_R2_eff audit",
            "timestamp_utc": ts,
        }
        for component_id, component, formula, zero_condition, status, parent_signed, value in specs
    ]


def mu_runner_input_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_row_id": "MURUN4724_0_missing_total_mu",
            "branch": "finite_R2_fR_bound",
            "mu_m2": "MISSING_PARENT_MU_OR_c_R2_eff_total",
            "lambda_R_m": "MISSING_mu_SO_lambda_R_NOT_NUMERIC",
            "alpha_eff": "MISSING_C_body_OR_SCREENING",
            "mu_bound_m2": "1.443476e15",
            "source_path": source_path("SRC4724_6"),
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "runner_row_id": "MURUN4724_1_total_zero_if_signed",
            "branch": "exact_selector_zero",
            "mu_m2": "0_IF_TOTAL_c_R2_eff_ZERO_PARENT_SIGNED",
            "lambda_R_m": "0_OR_NO_SCALARON_IF_SELECTOR_ZERO",
            "alpha_eff": "0_IF_SELECTOR_ZERO",
            "mu_bound_m2": "not_needed_if_exact_zero",
            "source_path": source_path("SRC4724_2"),
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "runner_row_id": "MURUN4724_2_standard_template_bound",
            "branch": "standard_template_only",
            "mu_m2": "1.443476e15_BOUND_NOT_PREDICTION",
            "lambda_R_m": "9.306372e7_BOUND_NOT_PREDICTION",
            "alpha_eff": "1/3_TEMPLATE_UNSCREENED_NOT_MTS_ALPHA",
            "mu_bound_m2": "1.443476e15",
            "source_path": source_path("SRC4724_6"),
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def mu_runner_result_rows(ts: str, inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs:
        mu = str(row["mu_m2"])
        if mu.startswith("MISSING"):
            verdict = "BLOCKED_MISSING_PARENT_MU_ALPHA"
            passes = False
            reason = "mu/c_R2_eff_total and alpha_eff/body charge are not parent-owned"
        elif mu.startswith("0_IF"):
            verdict = "BLOCKED_TOTAL_ZERO_UNSIGNED"
            passes = False
            reason = "exact zero branch is conditional but parent signature is unsigned"
        else:
            verdict = "TEMPLATE_ONLY_NOT_MTS_PREDICTION"
            passes = False
            reason = "standard bound is a target, not a prediction row"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "runner_row_id": row["runner_row_id"],
                "verdict": verdict,
                "passes_bound": passes,
                "claim_allowed": False,
                "valid_for_claim": False,
                "reason": reason,
                "timestamp_utc": ts,
            }
        )
    return rows


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4724_0_sources_verified", "All 4724 sources exist and needles are found.", True, "NONE"),
        ("GATE4724_1_visible_cell_zero_parent_signed", "Visible-cell no-grain/refinement-gauge zero is parent-signed.", False, "REFINEMENT_GAUGE_SIGNATURE_UNSIGNED"),
        ("GATE4724_2_total_cR2eff_zero", "All c_R2_eff components are zero or tied by a signed identity.", False, "BARE_HIDDEN_MEASURE_BOUNDARY_TERMS_UNSIGNED"),
        ("GATE4724_3_mu_numeric_or_zero", "mu/c_R2_eff_total is numeric or exactly zero.", False, "MISSING_PARENT_MU_OR_TOTAL_ZERO"),
        ("GATE4724_4_alpha_eff_numeric_or_zero", "alpha_eff/body charge/screening is numeric or exactly zero.", False, "MISSING_ALPHA_EFF_BODY_CHARGE"),
        ("GATE4724_5_bound_runner_claim_ready", "finite mu/lambda/alpha bound runner has claim-grade MTS prediction rows.", False, "RUNNER_FAILS_CLOSED_NONCLAIM"),
        ("GATE4724_6_local_GR_R2_channel_closed", "R2/f(R) channel is removed or bounded tightly enough for local-GR claim.", False, "R2_CHANNEL_RETAINED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "condition": condition,
            "passed": passed,
            "blocker": blocker,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, condition, passed, blocker in specs
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4724_0_componentwise_zero", "No total c_R2_eff zero claim from an unsourced cancellation between components."),
        ("FW4724_1_visible_cell_limit", "Visible-cell no-grain only kills c_R2_cell, not c_bare/hidden/measure/boundary residues."),
        ("FW4724_2_mu_bound_not_prediction", "The standard mu bound is a threshold, not an MTS-derived mu."),
        ("FW4724_3_alpha_template_guard", "alpha_eff=1/3 is only the unscreened standard metric f(R) template, not an MTS body-charge derivation."),
        ("FW4724_4_no_G_scale_shortcut", "Do not define ell_cell or c_R2_eff using measured G/GM/Planck length by declaration."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derivation_result": "visible c_R2_cell zero route is conditionally derived; total c_R2_eff zero is not proved",
            "runner_result": "mu/lambda/alpha runner exists but fails closed because parent mu and alpha_eff are missing or zero signature is unsigned",
            "local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4724_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated under post-checkpoint-work and formalization-workbench only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4724_1_science_verdict",
            "status": "actual_derivation_gain_but_R2_channel_retained",
            "detail": "The visible-cell piece has a real conditional zero derivation; the total coefficient remains open because bare, hidden, measure and boundary residues survive.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The cleanest next leap is the bare-operator question: either the parent grammar forbids a bare R2/f(R) term before reduction, or c_bare becomes the first finite source row.",
            "first_task": "Search/derive a parent object-language exclusion of bare curvature-square operators.",
            "fallback_task": "If no exclusion exists, create a finite c_bare row with units and projection to mu/lambda/alpha.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(ts: str, theorem: list[dict[str, Any]], components: list[dict[str, Any]], runner: list[dict[str, Any]], gates: list[dict[str, Any]]) -> None:
    doc = f"""# 4724 - Visible-Cell cR2 Zero Signature or R2 Mu Bound Runner

Generated: `{ts}`

## Purpose

4724 takes the best leap-forward route after 4723: try to make `c_R2_eff_total=0` from the visible-cell/no-grain derivation, and if that fails, stage a finite `mu/lambda_R/alpha_eff` runner without claiming local GR.

## What Actually Derived

- `c_R2_cell` has a genuine conditional zero route: the visible quadratic term scales like `ell_cell^2` and vanishes in the gauge-refinement/smooth-response/no-singular-counterterm limit.
- The total coefficient is larger: `c_R2_eff_total = c_R2_cell + c_bare + 1/2 B^T L^-1 B + c_measure + c_boundary`.
- Therefore the local R2 channel is not closed unless the bare, hidden-exchange, measure and boundary pieces are also zero or source-bounded.

## Total Zero Theorem Rows

{bullets(theorem, "theorem_id", "current_status")}

## Component Audit

{bullets(components, "component_id", "current_value")}

## Mu Runner Results

{bullets(runner, "runner_row_id", "verdict")}

## Gates

{bullets(gates, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 740 - Visible-Cell cR2 Zero Signature or R2 Mu Bound Runner

Generated: `{ts}`

## Result

The visible-cell/no-grain calculation is a real conditional derivation, not merely a missing-input note: `c_R2_cell` scales away as `ell_cell^2` if `ell` is gauge refinement and the parent response is smooth. The total scalaron coefficient still survives through `c_bare`, hidden exchange, measure and boundary terms.

## Exact Gate

`c_R2_eff_total = c_R2_cell + c_bare + 1/2 B^T L^-1 B + c_measure + c_boundary`.

The R2/f(R) branch closes only if each component is parent-zero/source-blind or the parent supplies a signed identity tying the components. Current evidence does not.

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(ts: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: the visible-cell `c_R2_cell` zero route is exact conditionally, but total `c_R2_eff_total=0` requires no-bare, no-hidden-exchange, no-measure and no-boundary signatures.
- Runner gain: a finite `mu/lambda_R/alpha_eff` runner now fails closed rather than being hand-waved.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: converts the visible-cell no-grain theorem into a componentwise total `c_R2_eff` gate and a fail-closed `mu` bound runner.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`{DOC_PATH.name}`

## Decision

`{DECISION}`

## What moved forward

- The visible-cell `c_R2_cell` zero route was derived as a conditional theorem.
- The total `c_R2_eff_total` gate was split into visible, bare, hidden-exchange, measure and boundary components.
- A finite `mu/lambda_R/alpha_eff` runner was staged and fails closed because parent `mu` and `alpha_eff` are still missing or zero signature is unsigned.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4724 derives the conditional visible-cell c_R2 zero route but shows total c_R2_eff remains unsigned because bare, hidden-exchange, measure and boundary residues survive; a finite mu/lambda/alpha runner is staged fail-closed.",
        "current_evidence": "Generated source register, total c_R2 zero theorem rows, component signature audit, mu bound runner input/results, promotion gates, firewalls, decision, status, next target and validation.",
        "status": "visible_cell_cR2_zero_conditional_total_cR2eff_unsigned_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating visible-cell suppression as total R2/f(R) closure or treating the standard mu bound as an MTS prediction.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Bare R2 or hidden/measure/boundary residues can keep the scalaron channel alive.",
        "title": "Visible-cell cR2 zero signature or R2 mu bound runner",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def parse_csv(path: Path) -> bool:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    components: list[dict[str, Any]],
    runner_results: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        ZERO_THEOREM_CSV,
        COMPONENT_AUDIT_CSV,
        MU_RUNNER_INPUT_CSV,
        MU_RUNNER_RESULTS_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    component_names = {row["component"] for row in components}
    checks = [
        ("VAL4724_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4724 source paths exist"),
        ("VAL4724_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4724 source needles found"),
        ("VAL4724_2_total_law_written", any(row["theorem_id"] == "TCZ4724_0_total_law" for row in theorem), "total c_R2_eff law written"),
        ("VAL4724_3_visible_zero_not_overclaimed", any(row["theorem_id"] == "TCZ4724_2_visible_cell_zero" for row in theorem) and any(row["theorem_id"] == "TCZ4724_6_verdict" and row["current_status"] == "TOTAL_ZERO_NOT_PROVED" for row in theorem), "visible-cell zero is present but total zero not claimed"),
        ("VAL4724_4_all_components_audited", {"c_R2_cell", "c_bare", "0.5 B^T L^-1 B", "c_measure", "c_boundary", "c_R2_eff_total"}.issubset(component_names), "all c_R2_eff components audited"),
        ("VAL4724_5_runner_fails_closed", all(row["verdict"] != "PASS" and not bool(row["claim_allowed"]) for row in runner_results), "mu runner has no claim-grade pass"),
        ("VAL4724_6_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] != "GATE4724_0_sources_verified"), "all claim gates remain closed except source verification"),
        ("VAL4724_7_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4724_8_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4724_9_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4725 next target"),
        ("VAL4724_10_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4724 CSV files parse cleanly"),
        ("VAL4724_11_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    overall = all(result for _check_id, result, _detail in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "timestamp_utc": ts,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4724_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4724 visible-cell c_R2 zero signature or R2 mu bound runner validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()
    sources = source_register(ts)
    theorem = zero_theorem_rows(ts)
    components = component_audit_rows(ts)
    runner_inputs = mu_runner_input_rows(ts)
    runner_results = mu_runner_result_rows(ts, runner_inputs)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(ZERO_THEOREM_CSV, theorem)
    write_csv(COMPONENT_AUDIT_CSV, components)
    write_csv(MU_RUNNER_INPUT_CSV, runner_inputs)
    write_csv(MU_RUNNER_RESULTS_CSV, runner_results)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, theorem, components, runner_results, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, theorem, components, runner_results, gates, ts))


if __name__ == "__main__":
    main()
