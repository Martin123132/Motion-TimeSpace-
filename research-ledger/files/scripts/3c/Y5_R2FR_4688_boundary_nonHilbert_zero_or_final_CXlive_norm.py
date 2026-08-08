from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4688"
CLAIM_ID = "L-530"
MARKER = "PPC4161_BOUNDARY_NONHILBERT_GATE_CURRENT_BRANCH_4688"
PACKET_MARKER = "PPC4161_PACKET_BOUNDARY_NONHILBERT_GATE_CURRENT_BRANCH_4688"
DECISION = "BOUNDARY_NONHILBERT_ZERO_OR_FINAL_CX_LIVE_NORM_INSERTED_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4689-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md"

DOC_PATH = POST / "4688-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md"
FORMAL_PATH = FORMAL / "704-PPC4161-boundary-nonHilbert-zero-or-final-CXlive-norm.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4687_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4687_NEXT_TARGET.csv"
CSV_4687_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4687_STATUS.csv"
CSV_4600_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4600_BOUNDARY_NONHILBERT_ZERO_THEOREM.csv"
CSV_4600_NORM = SOURCE_DIR / "P8_Y5_R2FR_4600_FINAL_CXLIVE_NORM.csv"
CSV_4600_BODY = SOURCE_DIR / "P8_Y5_R2FR_4600_BODY_CHARGE_ENVELOPE_FINAL_CX_UPDATE.csv"
CSV_4600_INTERFACE = SOURCE_DIR / "P8_Y5_R2FR_4600_EMPIRICAL_SCORE_INPUT_INTERFACE.csv"
CSV_4600_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4600_STATUS.csv"
CSV_4600_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4600_NEXT_TARGET.csv"
CSV_4600_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4600_VALIDATION.csv"
CSV_4601_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4601_STATUS.csv"
CSV_4601_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4601_NEXT_TARGET.csv"
CSV_4601_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4601_VALIDATION.csv"
FORMAL_616 = FORMAL / "616-PPC4161-boundary-nonHilbert-zero-or-final-CXlive-norm.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4688_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4688_BOUNDARY_NONHILBERT_ZERO_THEOREM.csv"
NORM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4688_FINAL_CXLIVE_NORM.csv"
BODY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4688_BODY_CHARGE_ENVELOPE_FINAL_CX_UPDATE.csv"
INTERFACE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4688_EMPIRICAL_SCORE_INPUT_INTERFACE.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4688_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4688_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4688_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4688_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4688_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4688_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4688_00_4687_next", CSV_4687_NEXT, "4688-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md", "4687 selected boundary/non-Hilbert target."),
        ("SRC4688_01_4687_status", CSV_4687_STATUS, "PPC4161_LABEL_HODGE_SUPPORT_READOUT_GATE_CURRENT_BRANCH_4687", "4687 current branch status."),
        ("SRC4688_02_4600_theorem", CSV_4600_THEOREM, "BNH4600_4_final_CX_live", "4600 final C_X theorem row."),
        ("SRC4688_03_4600_norm", CSV_4600_NORM, "C4600_4_final", "4600 final C_X live norm rows."),
        ("SRC4688_04_4600_body", CSV_4600_BODY, "BU4600_0_Csplit_final", "4600 body-charge final C update."),
        ("SRC4688_05_4600_interface", CSV_4600_INTERFACE, "E4600_4_EM_Poynting", "4600 empirical arena interface."),
        ("SRC4688_06_4600_status", CSV_4600_STATUS, "PPC4161_BOUNDARY_NONHILBERT_ZERO_OR_FINAL_CXLIVE_NORM_4600", "4600 status."),
        ("SRC4688_07_4600_next", CSV_4600_NEXT, "4601-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md", "4600 next target."),
        ("SRC4688_08_4600_validation", CSV_4600_VALIDATION, "VAL4600_OVERALL", "4600 validation passed."),
        ("SRC4688_09_4601_status", CSV_4601_STATUS, "PPC4161_CX_JX_BX_BODY_CHARGE_VECTOR_TO_EMPIRICAL_SCORE_INPUTS_4601", "4601 score-interface rung exists."),
        ("SRC4688_10_4601_next", CSV_4601_NEXT, "4602-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md", "4601 next target."),
        ("SRC4688_11_4601_validation", CSV_4601_VALIDATION, "VAL4601_OVERALL", "4601 validation passed."),
        ("SRC4688_12_formal616", FORMAL_616, "C_X^final_live = C_X^std_weight_live", "formal boundary/non-Hilbert final C gate."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "BNH4688_0_boundary_variation",
            "C_X^boundary",
            "parent variational principle fixes X boundary data or zero flux/topological class; improvement/reference form is exact with no compact representative; no wall/domain selector stress is varied",
            "delta_X S_boundary=0 and Pi_local J_boundary_X=0 => C_X^boundary=0",
            "|C_X^boundary T| <= ||Pi_local J_boundary_X|| + ||boundary_lift_X|| + ||wall_stress_X|| + ||Delta_symp_X||",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED_BOUND_ROW_REQUIRED",
        ),
        (
            "BNH4688_1_nonHilbert_decomposition",
            "C_X^nonHilbert",
            "after Hilbert source extraction, spin/torsion, boundary/worldtube, improvement, readout reentry, shadow/projector and decoupled conserved source blocks are each absent, exact, or locally projection-silent in the same branch",
            "P_source[J_NH]=0 => C_X^nonHilbert=0",
            "|C_X^nonHilbert T| <= E_spin + E_boundary + E_improvement + E_readout + E_shadow_projector + E_decoupled",
            "TOTAL_ZERO_CONDITIONAL_OFFICIAL_FALLBACK_ACTIVE",
        ),
        (
            "BNH4688_2_shadow_split",
            "source-shadow subblock of C_X^nonHilbert",
            "pure source-only shadow vanishes if total Hilbert source owner is parent-signed; action-scale, hidden-marker and readout-projector survivors are reassigned to explicit live C sectors",
            "C_shadow_pure_source_only=0, while C_shadow_total -> C_action_scale + C_hidden_return + C_readout_projector unless their gates close",
            "|K_m_shadow C_shadow_total| kept as a nonclaim bound target until all subblocks are zero or numeric",
            "PURE_SOURCE_ZERO_CONTRACT_READY_SURVIVORS_RETAINED",
        ),
        (
            "BNH4688_3_combined_boundary_nonHilbert",
            "C_X^boundary_nonHilbert_live",
            "BNH4688_0 and BNH4688_1 hold in the same parent branch with no calibration hiding or cancellation between channels",
            "C_X^boundary_nonHilbert_live = C_X^boundary + C_X^nonHilbert = 0",
            "|C_X^boundary_nonHilbert_live| <= |C_X^boundary| + |C_X^nonHilbert|",
            "COMBINED_ZERO_OR_ABSOLUTE_SUM_READY",
        ),
        (
            "BNH4688_4_final_CX_live",
            "C_X^final_live",
            "all post4686 standard/weight, post4687 LHRS and 4688 boundary/non-Hilbert blocks vanish or have source-backed values below arena bounds",
            "C_X^final_live = C_X^std_weight_live + C_X^LHRS_live + C_X^boundary_nonHilbert_live",
            "|C_X^final_live| <= |C_X^std_weight_live| + |C_X^LHRS_live| + |C_X^boundary| + |C_X^nonHilbert|",
            "FINAL_CX_LIVE_NORM_INSERTED_VALUES_MISSING",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "target": target,
            "conditional_zero_route": route,
            "formula": formula,
            "finite_fallback": fallback,
            "current_status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, target, route, formula, fallback, status in data
    ]


def norm_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("C4688_0_boundary", "C_X^boundary", "boundary/reference/domain-wall leakage into matter-trace coupling", "prove parent boundary neutrality and compact local projection silence", "Delta_boundary_X"),
        ("C4688_1_nonHilbert", "C_X^nonHilbert", "non-Hilbert source-current bypass leakage", "prove P_source[J_NH]=0 componentwise in same branch", "epsilon_current_owner_NH_abs"),
        ("C4688_2_shadow_projector", "E_shadow_projector", "shadow/projector/support source-current tail inside non-Hilbert envelope", "prove terminal public coframe/source-shadow no-return and projector silence", "K_m_shadow*C_shadow_total"),
        ("C4688_3_boundary_nonHilbert", "C_X^boundary_nonHilbert_live", "combined boundary plus non-Hilbert live coefficient", "zero C4688_0 and C4688_1 in same branch", "absolute sum C4688_0+C4688_1"),
        ("C4688_4_final", "C_X^final_live", "final matter-trace coupling coefficient for memory/fibre body charge", "zero or source-bound all standard/weight/LHRS/boundary/non-Hilbert blocks", "absolute sum post4686+post4687+4688 live blocks"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "role": role,
            "derive_first": derive_first,
            "finite_fallback": fallback,
            "current_status": "FINAL_CX_LIVE_NORM_READY_VALUES_MISSING" if symbol == "C_X^final_live" else "MISSING_PARENT_ZERO_OR_VALUE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for coefficient_id, symbol, role, derive_first, fallback in data
    ]


def body_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "BU4688_0_Csplit_final",
            "C_X live after 4688",
            "C_X^final_live = C_X^std_weight_live + C_X^LHRS_live + C_X^boundary_nonHilbert_live",
            "C_X^final_live=0 only if all standard/weight, LHRS, boundary and non-Hilbert subblocks vanish in the same parent branch",
            "|C_X^final_live| <= |C_X^std_weight_live|+|C_X^LHRS_live|+|C_X^boundary|+|C_X^nonHilbert|",
        ),
        (
            "BU4688_1_memory",
            "A_mem",
            "|A_mem| <= [exp(R/lambda_mem) int_body (||B_mem_eff||||R_obs|| + ||C_mem^final_live||||T|| + ||J_mem_live||) dV + ||Q_boundary_mem||]/(4*pi||Z_mem||)",
            "B_mem_eff=C_mem^final_live=J_mem_live=Q_boundary_mem=0",
            "C_mem^boundary and C_mem^nonHilbert now enter through C_mem^final_live; Q_boundary_mem remains a separate Green-function boundary charge",
        ),
        (
            "BU4688_2_fibre",
            "A_h",
            "|A_h| <= [exp(R/lambda_h) int_body (||B_h||||R_obs|| + ||C_h^final_live||||T|| + ||J_h_live||) dV + ||Q_boundary_h||]/(4*pi||Z_h||)",
            "B_h=C_h^final_live=J_h_live=Q_boundary_h=0",
            "C_h^boundary and C_h^nonHilbert now enter through C_h^final_live; Q_boundary_h remains a separate Green-function boundary charge",
        ),
        (
            "BU4688_3_boundary_separation",
            "boundary bookkeeping",
            "C_X^boundary is matter-trace/source-coupling leakage; Q_boundary_X is exterior Green-function boundary charge",
            "both must be zero or bounded separately; one cannot be used as a calibration sink for the other",
            "|A_X| keeps both ||C_X^final_live||||T|| and ||Q_boundary_X|| terms",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": update_id,
            "target": target,
            "formula": formula,
            "zero_condition": zero_condition,
            "finite_bound": finite_bound,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, target, formula, zero_condition, finite_bound in data
    ]


def interface_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("E4688_0_R10", "R10/short-range fifth force", "Z_X;M_X^2;lambda_X;B_X_eff;C_X^final_live;J_X_live;Q_boundary_X;K_R10", "alpha(lambda) prediction or theorem-zero certificate"),
        ("E4688_1_PPN", "PPN/local-GR vector", "Z_X;M_X^2;B_X_eff;C_X^final_live;J_X_live;Q_boundary_X;K_gamma,K_beta,K_alpha_i,K_xi,K_Gdot", "bounded residual vector compared with GR/PPN limits"),
        ("E4688_2_clock_WEP", "clock/WEP/source universality", "C_X^final_live;E_shadow_projector;C_standard_weight;readout kernels;material sensitivities", "clock/WEP response rows with units and source paths"),
        ("E4688_3_orbital_GM", "orbital/GM/light-time", "Q_boundary_X;Delta_symp_X;J_boundary_X;C_X^final_live;GM calibration rule", "orbital residual not absorbed into fitted GM"),
        ("E4688_4_EM_Poynting", "EM/Poynting/local energy flow", "J_EM_open;Delta_Hodge_EM_X;Poynting source leg;C_X^Hodge;C_X^final_live", "EM/Poynting contribution either theorem-owned or bounded"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "interface_id": interface_id,
            "arena": arena,
            "required_inputs": required_inputs,
            "score_object": score_object,
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for interface_id, arena, required_inputs, score_object in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4688_0_boundary_nonHilbert", "boundary/non-Hilbert C_X rows", "zero-or-final-norm law imported; values/source-zero certificates still missing", NEXT_TARGET),
        ("SURV4688_1_CX_final", "C_X^final_live", "matter-trace coupling ledger now fully split into explicit subblocks", NEXT_TARGET),
        ("SURV4688_2_A_mem_A_h", "body-charge envelopes", "A_mem/A_h updated to use C_mem^final_live/C_h^final_live", NEXT_TARGET),
        ("SURV4688_3_Q_boundary", "Green-function boundary charges", "kept separate from C_X^boundary; cannot be calibration sink", "carry into score vector"),
        ("SURV4688_4_operator_block", "Z_X/M_X^2/lambda_X", "hard scoring blocker remains range/operator ownership", "4689 then range-owner fill"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4688": status,
            "next_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for survivor_id, family, status, action in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4688_0", "Do not treat imposed boundary conditions as derived parent silence unless the parent variational principle selects them."),
        ("CTRL4688_1", "Do not hide boundary matter-trace leakage inside Q_boundary_X or fitted GM; C_X^boundary and Q_boundary_X are separate terms."),
        ("CTRL4688_2", "Do not erase non-Hilbert source-current bypasses unless P_source[J_NH]=0 is componentwise parent-signed."),
        ("CTRL4688_3", "Do not cancel standard/weight, LHRS, boundary and non-Hilbert blocks against one another; use absolute envelopes."),
        ("CTRL4688_4", "Score interfaces remain nonclaim until Z_X, M_X^2, lambda_X and all source charge rows are numeric or theorem-zero."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "rule": rule,
            "status": "ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for control_id, rule in controls
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "summary": "4688 imports the 4600 boundary/non-Hilbert gate into the current branch. The remaining C_X matter-trace coupling is now a final explicit norm: C_X^final_live = C_X^std_weight_live + C_X^LHRS_live + C_X^boundary_nonHilbert_live. Boundary and non-Hilbert pieces vanish only under parent-signed boundary silence and componentwise P_source[J_NH]=0; otherwise the score interface stays nonclaim.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "boundary zero-or-bound theorem; non-Hilbert/shadow zero-or-bound theorem; C_X^boundary_nonHilbert_live; C_X^final_live; A_mem/A_h final C update; empirical score interface handoff",
            "not_derived": "parent-signed compact boundary silence; total non-Hilbert source-current zero; numeric C_X^final_live values; B_X/J_X/Q_boundary/Z_X/M_X^2 arena scoring; local-GR/R10/PPN pass",
            "claim_status": "PRIVATE_NONCLAIM",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4688_0",
            "target": NEXT_TARGET,
            "reason": "The C_X matter-trace ledger is now fully split; the next useful move is to assemble B_X, C_X, J_X, Q_boundary_X, Z_X and M_X^2 into arena score inputs.",
            "derive_first": "try to zero or source-own the full body-charge vector componentwise before numeric scoring",
            "fallback": "build nonclaim empirical score rows for R10/PPN/clock/orbital/EM with values missing rather than hiding placeholders",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4688 - Y5/R2FR Boundary/Non-Hilbert Zero Or Final C_X Live Norm

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4688 imports the final boundary/non-Hilbert `C_X` gate:

```text
C_X^boundary_nonHilbert_live = C_X^boundary + C_X^nonHilbert

C_X^final_live = C_X^std_weight_live
               + C_X^LHRS_live
               + C_X^boundary_nonHilbert_live.
```

The zero route is conditional:

```text
delta_X S_boundary=0 and Pi_local J_boundary_X=0 => C_X^boundary=0
P_source[J_NH]=0 => C_X^nonHilbert=0
```

Those conditions are not promoted as parent-signed in this checkpoint. The useful win is bookkeeping: `C_X` is no longer fog. It is now a visible final residual vector that can be theorem-zeroed or score-bounded in R10, PPN, clocks/WEP, orbital/GM and EM/Poynting arenas.

## Source Register

{table(rows["sources"])}

## Boundary / Non-Hilbert Zero Theorem

{table(rows["theorems"])}

## Final C_X Live Norm

{table(rows["norms"])}

## Body-Charge Envelope Update

{table(rows["body"])}

## Empirical Score Interface

{table(rows["interfaces"])}

## Survivor Update

{table(rows["survivors"])}

## Controls

{table(rows["controls"])}

## Decision

{table(rows["decisions"])}

## Status

{table(rows["statuses"])}

## Next Target

{table(rows["next"])}

## Validation

{table(rows.get("validations", []))}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4688 - Y5/R2FR", "# 704 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4688 imports the boundary/non-Hilbert gate into the current branch. C_X^final_live is the explicit matter-trace coupling residual and vanishes only when standard/weight, LHRS, boundary and non-Hilbert blocks all zero or source-bound in the same branch.",
                "current_evidence": "Generated source register, boundary/non-Hilbert zero theorem, final C_X norm rows, body-charge envelope update, empirical score interface, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Boundary hair or non-Hilbert source-current bypass can survive Hilbert extraction and mimic a local-GR/PPN residual.",
                "sector": "local_gr",
                "evidence": str(DOC_PATH),
                "next_action": NEXT_TARGET,
            }
        )
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writerow(row)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""## Local GR Parent-Derivation Update - Current Boundary/Non-Hilbert Gate

Marker: `{MARKER}`

4688 imports the final `C_X` zero-or-norm law into the current branch:

```text
C_X^final_live = C_X^std_weight_live
               + C_X^LHRS_live
               + C_X^boundary_nonHilbert_live.
```

This is a real consolidation step: local source coupling is now an explicit residual vector rather than a mixed phrase. Boundary charges remain separate from matter-trace leakage, and non-Hilbert/shadow currents cannot be erased without a parent zero certificate.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current Boundary/Non-Hilbert Gate

Marker: `{PACKET_MARKER}`

The packet now carries `C_X^final_live` explicitly and separates `C_X^boundary` from `Q_boundary_X`. No R10/PPN/clock/orbital/EM pass is allowed until the score rows receive source-backed operator and charge inputs.

- theorem csv: `{THEOREM_CSV.name}`
- interface csv: `{INTERFACE_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4688_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4688_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4688_2_zero_theorem_rows", len(rows["theorems"]) == 5, "boundary/non-Hilbert theorem rows present"),
        ("VAL4688_3_final_norm", any(row["symbol"] == "C_X^final_live" for row in rows["norms"]), "final C_X live norm present"),
        ("VAL4688_4_body_update", any("C_X^final_live" in row["formula"] for row in rows["body"]), "A_mem/A_h final C update present"),
        ("VAL4688_5_boundary_separation", any(row["target"] == "boundary bookkeeping" for row in rows["body"]), "C boundary and Q boundary separation present"),
        ("VAL4688_6_interface_rows", len(rows["interfaces"]) == 5, "five empirical arena interface rows present"),
        ("VAL4688_7_next_score_vector", rows["next"][0]["target"] == NEXT_TARGET, "next score-vector target selected"),
        ("VAL4688_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-530"),
        ("VAL4688_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4688_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4688_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4688_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4688_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4688_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4688_13_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4688_14_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4688_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "theorems": theorem_rows(timestamp),
        "norms": norm_rows(timestamp),
        "body": body_rows(timestamp),
        "interfaces": interface_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": control_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        THEOREM_CSV: rows["theorems"],
        NORM_CSV: rows["norms"],
        BODY_CSV: rows["body"],
        INTERFACE_CSV: rows["interfaces"],
        SURVIVOR_CSV: rows["survivors"],
        CONTROL_CSV: rows["controls"],
        DECISION_CSV: rows["decisions"],
        STATUS_CSV: rows["statuses"],
        NEXT_CSV: rows["next"],
    }
    for path, data in csv_map.items():
        write_csv(path, data)
    write_documents(rows)
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    rows["validations"] = validation_rows(rows, list(csv_map))
    write_csv(VALIDATION_CSV, rows["validations"])
    write_documents(rows)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
