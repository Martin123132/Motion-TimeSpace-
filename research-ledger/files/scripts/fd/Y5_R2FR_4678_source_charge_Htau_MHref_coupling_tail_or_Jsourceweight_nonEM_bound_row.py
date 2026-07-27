from __future__ import annotations

import csv
import io
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4678"
CLAIM_ID = "L-520"
BRANCH = "MTS_R2FR_Y5_SOURCE_CHARGE_HTAU_MHREF_NONEM_SOURCE_WEIGHT_4678"
MARKER = "PPC4161_SOURCE_CHARGE_HTAU_MHREF_NONEM_SOURCE_WEIGHT_4678"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_CHARGE_HTAU_MHREF_NONEM_SOURCE_WEIGHT_4678"
DECISION = "NONEM_CLASSICAL_SOURCE_WEIGHT_ROUTE_DERIVED_COMMON_G_CALIBRATION_SPLIT_REQ_BZERO_HTAU_TAILS_REMAIN"
NEXT_TARGET = "4679-Y5-R2FR-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md"

DOC_PATH = POST / "4678-Y5-R2FR-source-charge-Htau-MHref-coupling-tail-or-Jsourceweight-nonEM-bound-row.md"
FORMAL_PATH = FORMAL / "694-PPC4161-source-charge-Htau-MHref-coupling-tail-or-Jsourceweight-nonEM-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

FORMAL_377 = FORMAL / "377-PPC4161-transition-owner-no-wA-theorem-or-explicit-source-coupling-closure.md"
FORMAL_436 = FORMAL / "436-PPC4161-parent-action-measure-current-owner-or-Req-moment-bound.md"
FORMAL_456 = FORMAL / "456-PPC4161-source-charge-Htau-MHref-closure-or-epsilon-Gsrc-first-tail-value.md"
FORMAL_457 = FORMAL / "457-PPC4161-action-measure-current-owner-contract-after-EM-zero-or-Req-tail-values.md"
FORMAL_458 = FORMAL / "458-PPC4161-nonEM-universal-hbar-measure-owner-proof-or-first-Req-Bzero-tail-value.md"
FORMAL_481 = FORMAL / "481-PPC4161-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md"
FORMAL_693 = FORMAL / "693-PPC4161-visible-EM-action-edge-parent-signature-or-Jsourceweight-bound-input.md"
POST_4378 = POST / "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"
POST_3574 = POST / "3574-Y5-R2FR-topological-mass-current-origin-or-Meff-drift-source-row.md"

CSV_4677_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4677_NEXT_TARGET.csv"
CSV_4677_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4677_JSOURCEWEIGHT_AFTER_VISIBLE_EM.csv"
CSV_4677_OPEN = SOURCE_DIR / "P8_Y5_R2FR_4677_OPEN_EM_AND_NONEM_SURVIVORS.csv"
CSV_4440_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4440_DERIVATION_ROWS.csv"
CSV_4440_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4440_REDUCED_CONTRACT_ROWS.csv"
CSV_4440_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4440_EPSILON_GSRC_TAIL_BOUND_OUTPUT.csv"
CSV_4441_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4441_ACTION_MEASURE_CURRENT_OWNER_OUTPUT.csv"
CSV_4441_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4441_REDUCTION_ROWS.csv"
CSV_4442_ROUTE = SOURCE_DIR / "P8_Y5_R2FR_4442_NONEM_SOURCE_ROUTE_OUTPUT.csv"
CSV_4442_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4442_DERIVATION_ROWS.csv"
CSV_4442_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4442_REDUCTION_ROWS.csv"
CSV_4442_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4442_REQ_BZERO_FIRST_TAIL_OUTPUT.csv"
CSV_4442_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4442_VALIDATION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4678_SOURCE_REGISTER.csv"
DERIVATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4678_DERIVATION_ROWS.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4678_NONEM_CLASSICAL_SOURCE_WEIGHT_THEOREM.csv"
VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4678_JSOURCEWEIGHT_SOURCE_CHARGE_SPLIT.csv"
TAIL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4678_REQ_BZERO_HTAU_TAIL_CONTRACTS.csv"
COMMON_MODE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4678_COMMON_G_CALIBRATION_GUARD.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4678_CONTROL_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4678_RUNNER_RESULTS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4678_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4678_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4678_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4678_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4678_00_4677_next", CSV_4677_NEXT, "source-charge/H_tau/MHref/nonEM source-current ownership", "4677 selected this coupling/source-charge target."),
        ("SRC4678_01_4677_vector", CSV_4677_VECTOR, "JSW4677_1_after_fixed_visible_EM_import", "after visible EM, source-weight vector is open EM plus nonEM."),
        ("SRC4678_02_4677_open", CSV_4677_OPEN, "OPEN4677_3_nonEM_weight", "nonEM source-weight survivor from 4677."),
        ("SRC4678_03_formal693", FORMAL_693, "J_source_weight_abs_after_visible_EM", "formal 4677 source-weight rewrite."),
        ("SRC4678_04_4440_common", CSV_4440_DERIVATION, "SC4440_0_common_mode_split", "common Hilbert source mode is calibrated G, not physical tail."),
        ("SRC4678_05_4440_newton", CSV_4440_DERIVATION, "SC4440_1_structural_newton_bridge", "conditional GR/Newton source bridge."),
        ("SRC4678_06_4440_contract", CSV_4440_CONTRACT, "RC4440_0_clean_source_law", "source law reduced to Htau/MHref/action-current contract."),
        ("SRC4678_07_4440_tail", CSV_4440_TAIL, "TAIL4440_4_R10_contract", "R10/PPN/clock/orbital tail contract precedent."),
        ("SRC4678_08_4441_owner", CSV_4441_OWNER, "AMCO4441_0_current_after_EM_subcontract", "fixed EM subcontract closed, nonEM owner open."),
        ("SRC4678_09_4441_reduction", CSV_4441_REDUCTION, "RED4441_1_nonEM_owner", "nonEM owner exact conditional, unsigned."),
        ("SRC4678_10_4442_route", CSV_4442_ROUTE, "NEM4442_0_current_post_EM_branch", "current post-EM nonEM route state."),
        ("SRC4678_11_4442_derivation", CSV_4442_DERIVATION, "NEM4442_1_scalar_naturality_reused", "connected graph collapses source weights."),
        ("SRC4678_12_4442_reduction", CSV_4442_REDUCTION, "RED4442_1_classical_no_wA_route", "hbar-free classical no-wA route."),
        ("SRC4678_13_4442_tail", CSV_4442_TAIL, "TAIL4442_0_Req_compact_test_live", "R_eq/Bzero/Htau live tail rows."),
        ("SRC4678_14_4442_validation", CSV_4442_VALIDATION, "VAL4442_17_pycache_absent", "4442 validation."),
        ("SRC4678_15_formal456", FORMAL_456, "epsilon_Gsrc_perp", "physical source-coupling tail after common-mode split."),
        ("SRC4678_16_formal457", FORMAL_457, "AMCO4441_1_nonEM_owner_contract", "post-EM nonEM owner target."),
        ("SRC4678_17_formal458", FORMAL_458, "NEM4442_1_scalar_naturality_reused", "formal route split and scalar naturality theorem."),
        ("SRC4678_18_formal377", FORMAL_377, "TH4361_0_scalar_naturality", "older scalar action-weight naturality theorem."),
        ("SRC4678_19_formal436", FORMAL_436, "AMR4420_0_joint_contract", "same-current R_eq/Bzero source contract."),
        ("SRC4678_20_formal481", FORMAL_481, "COMMON_MODE_SURVIVES_WEP", "common mode can pass WEP while still affecting R10/PPN/orbital."),
        ("SRC4678_21_post4378", POST_4378, "topological profile defect", "R_eq/topological compact-test and multipole source row precedent."),
        ("SRC4678_22_post3574", POST_3574, "Pi_M J_H = J_M^top + dB_zero + R_eq", "topological source current decomposition."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line_number": line_number(path, needle),
                "note": note,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def derivation_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "DER4678_0_nonEM_weight_split",
            "After 4677, split the nonEM source-weight survivor into relative, common-derivative and same-current/source-charge tails.",
            "J_source_weight_nonEM = J_rel_nonEM + J_common_derivative + R_eq + B_zero + epsilon_HM",
            "This replaces one vague coupling term with five testable/derivable objects.",
            "SOURCE_WEIGHT_SPLIT_REFINED",
        ),
        (
            "DER4678_1_scalar_naturality_theorem",
            "A parent-owned connected nonEM matter graph collapses relative action/source weights.",
            "For every nonzero edge f:A->B, w_B F(f)=F(f)w_A. Since F(f) != 0, w_A=w_B; connectedness gives w_A=w_*.",
            "Relative nonEM source weights vanish if the edge graph, no-source-Hom and no-readout-reentry clauses are parent-signed.",
            "EXACT_CONDITIONAL_DERIVATION",
        ),
        (
            "DER4678_2_common_G_calibration_guard",
            "The surviving common w_* is not a prediction of numerical G_N; it is allowed as calibrated GR-style G only if derivative-silent.",
            "D_X w_* = D_t w_* = D_frame w_* = D_readout w_* = 0 on the tested branch.",
            "If derivative-silent, w_* is absorbed into G_cal/GM; if not, it becomes J_common_derivative and is tested by R10/PPN/clock/orbital rows.",
            "COMMON_MODE_NOT_HIDDEN",
        ),
        (
            "DER4678_3_same_current_gate",
            "Even with J_rel_nonEM=0, local Newton/GR still needs the source current equality.",
            "Pi_M J_H = J_M^top + dB_zero + R_eq, with R_eq=0, boundary flux zero and H_tau-H_ref=M_H_ref on the same worldtube.",
            "The next finite fallback is R_eq compact-test/multipole, B_zero flux, or epsilon_HM; not fitted GM.",
            "REQ_BZERO_HTAU_REMAIN",
        ),
        (
            "DER4678_4_hbar_guard",
            "Universal hbar/quantum measure remains important but is not the first classical local-source lock.",
            "Classical source weights are killed by parent action-density/current/graph/no-Hom/no-reentry. hbar closes quantum/statistical consistency after that.",
            "This is the less scrutiny-heavy route: do the classical source theorem first, then hbar/quantum guard.",
            "HBAR_DEMOTED_TO_QUANTUM_GUARD",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "derivation_id": row[0],
            "claim": row[1],
            "equation_or_rule": row[2],
            "consequence": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "THM4678_0_current_branch",
            "current post-4677 branch",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            "CURRENT_BRANCH_OPEN_NONCLAIM",
        ),
        (
            "THM4678_1_future_classical_owner",
            "future classical nonEM owner branch",
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            "RELATIVE_NONEM_SOURCE_WEIGHT_ZERO_READY_IF_PARENT_SIGNED",
        ),
        (
            "THM4678_2_hbar_only_counterroute",
            "hbar owner without classical graph/current",
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            "HBAR_ONLY_INADEQUATE_FOR_CLASSICAL_SOURCE_WEIGHT",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": row[0],
            "branch": row[1],
            "one_classical_parent_action": row[2],
            "no_source_Hom_and_no_reentry": row[3],
            "parent_owned_connected_nonEM_graph": row[4],
            "total_Hilbert_current_owner": row[5],
            "hbar_quantum_guard": row[6],
            "relative_nonEM_weight_zero": row[7],
            "claim_allowed": row[8],
            "status": row[9],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def vector_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "VEC4678_0_after_4677",
            "J_source_weight_abs_after_visible_EM",
            "|J_EM_open_dynamic| + |J_source_weight_nonEM|",
            "4677 state",
            "INPUT_VECTOR",
        ),
        (
            "VEC4678_1_split_nonEM",
            "J_source_weight_nonEM",
            "|J_rel_nonEM| + |J_common_derivative| + |R_eq| + |B_zero| + |epsilon_HM|",
            "4678 splits nonEM source weight into theorem-zero and source-current/Htau tails",
            "REFINED_VECTOR",
        ),
        (
            "VEC4678_2_future_classical_owner",
            "J_rel_nonEM",
            "0 if one parent action-density/current owner + no Hom + connected nonEM graph + no reentry are signed",
            "exact conditional zero branch",
            "DERIVED_ZERO_CONDITIONAL",
        ),
        (
            "VEC4678_3_current_claim_safe_vector",
            "J_source_weight_abs_4678_current",
            "|J_EM_open_dynamic| + |J_rel_nonEM_owner_gap| + |J_common_derivative| + |R_eq| + |B_zero| + |epsilon_HM|",
            "current branch keeps unsigned owner gap explicit",
            "NONCLAIM_BOUND_VECTOR",
        ),
        (
            "VEC4678_4_if_owner_signed",
            "J_source_weight_abs_4678_owner_signed",
            "|J_EM_open_dynamic| + |J_common_derivative| + |R_eq| + |B_zero| + |epsilon_HM|",
            "what remains after classical nonEM source-weight theorem is signed",
            "NEXT_REDUCED_VECTOR",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "vector_id": row[0],
            "symbol": row[1],
            "formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def tail_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("TAIL4678_0_R_eq", "R_eq_compact_test", "R_eq[varphi]=int_W (Pi_M J_H-J_M_top-dB_zero) varphi", "source_current_distribution", "MISSING_REQ_COMPACT_TEST_VALUE", "Newton/PPN/orbital same-current tests"),
        ("TAIL4678_1_B_zero", "B_zero_boundary_flux", "Phi_B=int_partialW B_zero/M_H_ref", "dimensionless", "MISSING_BZERO_FLUX_VALUE", "boundary silence/Gdot/orbital tests"),
        ("TAIL4678_2_epsilon_HM", "Htau_MHref_mismatch", "epsilon_HM=|H_tau[S]-H_ref-M_H_ref|/M_H_ref", "dimensionless", "MISSING_HTAU_MHREF_MISMATCH", "same-worldtube Hamiltonian/Hilbert source lock"),
        ("TAIL4678_3_common_derivative", "J_common_derivative", "|D_X ln w_*|+|D_t ln w_*|+|D_frame ln w_*|+|D_readout ln w_*|", "per_source_coordinate_or_declared", "MISSING_DERIVATIVE_SILENCE_ROW", "R10/PPN/clock/orbital common-mode pressure"),
        ("TAIL4678_4_open_EM", "J_EM_open_dynamic", "|E_rad_EM|+|C_EM_readout|+|C_XF2_global_dynamic|+|C_JQ_global_dynamic|", "common_source_weight_units", "MISSING_OPEN_EM_SOURCE_ROWS", "open radiation/readout/global EM branch"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "tail_id": row[0],
            "quantity": row[1],
            "definition": row[2],
            "units": row[3],
            "current_value": row[4],
            "test_arena": row[5],
            "numeric_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def common_mode_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CM4678_0_constant_common_mode", "w_* constant over tested branch", "absorbed into G_cal/GM", "allowed GR-style calibration", "NOT_A_CLAIM_TO_DERIVE_NUMERIC_G"),
        ("CM4678_1_derivative_common_mode", "D w_* != 0", "composition-blind fifth-force/time/source drift", "must be scored by R10/PPN/clock/orbital rows", "LIVE_TAIL"),
        ("CM4678_2_WEP_warning", "C_A=C_B=C_common", "differential WEP can pass while common fifth force remains", "do not use MICROSCOPE alone as local-GR safety", "COMMON_MODE_SURVIVES_WEP"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "mode_id": row[0],
            "condition": row[1],
            "effect": row[2],
            "interpretation": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4678_0_no_fitted_G_backfill", "Do not use observed orbital GM or fitted G_N as the source-charge proof.", "ACTIVE"),
        ("CTRL4678_1_common_mode_allowed_only_if_silent", "A universal common mode is calibration only if derivative/readout/range silent.", "ACTIVE"),
        ("CTRL4678_2_hbar_not_first_local_lock", "Do not block the classical local-source derivation on hbar before testing action-density/current/graph/no-Hom.", "ACTIVE"),
        ("CTRL4678_3_no_template_edges", "A physical standard-model graph template is not a parent-owned edge certificate.", "ACTIVE"),
        ("CTRL4678_4_no_local_GR_claim", "No local-GR/Newton/PPN/R10 claim until the theorem clauses or finite tails are source-backed.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "rule": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "why": "4678 imports 4440-4442 into the post-4677 source-weight language. The fixed EM piece is already removed. The nonEM relative source-weight route is now an exact classical scalar-naturality theorem, not a hbar-first bottleneck. Current parent graph/current/no-Hom/Htau clauses remain unsigned, so the residual vector is reduced but nonclaim.",
            "promoted": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "fixed_visible_EM_removed": True,
            "nonEM_classical_route_derived": True,
            "relative_nonEM_weight_zero_parent_signed": False,
            "common_G_calibration_guard_written": True,
            "Req_Bzero_Htau_tails_written": True,
            "numeric_bound_sourced": False,
            "local_GR_claim": False,
            "r10_claim": False,
            "ppn_claim": False,
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4678 turns the source-coupling problem into one concrete proof target: parent-sign a connected nonEM graph/current edge, or fill the first R_eq compact-test/B_zero/Htau tail value.",
            "derive_route": "Parent-sign one nonzero ordinary nonEM action-density/current graph edge with no species/source prefactor, constructor exhaustion, variation-before-readout and no hidden readout re-entry.",
            "fallback_route": "Fill R_eq compact-test/multipole, B_zero boundary flux or epsilon_HM with value, units, source path, projection coefficient, arena bound and no-cancellation guard.",
            "avoid": "Do not use hbar-only ownership, physical template edges, observed GM, or comparator bounds as source definitions.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def runner_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    derivations: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    vectors: list[dict[str, Any]],
    tails: list[dict[str, Any]],
    common_modes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    derivation_ok = any(row["derivation_id"] == "DER4678_1_scalar_naturality_theorem" for row in derivations)
    theorem_ok = any(row["theorem_id"] == "THM4678_1_future_classical_owner" and row["relative_nonEM_weight_zero"] for row in theorem)
    vector_ok = any(row["vector_id"] == "VEC4678_4_if_owner_signed" for row in vectors)
    tails_ok = all(any(row["tail_id"] == tail_id for row in tails) for tail_id in ["TAIL4678_0_R_eq", "TAIL4678_1_B_zero", "TAIL4678_2_epsilon_HM"])
    common_ok = any(row["mode_id"] == "CM4678_1_derivative_common_mode" for row in common_modes)
    nonclaim_ok = all(not row["valid_for_claim"] and not row["claim_allowed"] for row in [*derivations, *theorem, *vectors, *tails, *common_modes])
    checks = [
        ("RUN4678_0_sources", source_ok, "all source paths and needles found" if source_ok else "source path/needle failure"),
        ("RUN4678_1_derivation", derivation_ok, "scalar-naturality theorem imported" if derivation_ok else "derivation row missing"),
        ("RUN4678_2_theorem", theorem_ok, "future classical owner zero route staged" if theorem_ok else "theorem route missing"),
        ("RUN4678_3_vector", vector_ok, "post-owner-signed vector written" if vector_ok else "vector rewrite missing"),
        ("RUN4678_4_tails", tails_ok, "R_eq/B_zero/Htau tail contracts written" if tails_ok else "tail contract missing"),
        ("RUN4678_5_common", common_ok, "common G calibration guard written" if common_ok else "common mode guard missing"),
        ("RUN4678_6_nonclaim", nonclaim_ok, "all generated rows remain nonclaim" if nonclaim_ok else "claim flag promoted"),
        ("RUN4678_7_next", True, "next target selected"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": check_id,
            "passed": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]


def validation_rows(timestamp: str, csv_paths: list[Path], sources: list[dict[str, Any]], runners: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    rows.append({"validation_id": "VAL4678_0_sources", "passed": source_ok, "detail": "all source paths and needles found" if source_ok else "source path/needle failure", "timestamp_utc": timestamp})
    parse_ok = True
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            passed = bool(parsed)
            detail = f"rows={len(parsed)} columns={len(parsed[0]) if parsed else 0}"
        except Exception as exc:
            passed = False
            detail = repr(exc)
        parse_ok = parse_ok and passed
        rows.append({"validation_id": f"VAL4678_parse_{path.name}", "passed": passed, "detail": detail, "timestamp_utc": timestamp})
    runner_ok = all(row["passed"] for row in runners)
    rows.append({"validation_id": "VAL4678_1_runner_pass", "passed": runner_ok, "detail": "runner rows passed" if runner_ok else "runner failure", "timestamp_utc": timestamp})
    outputs_exist = all(path.exists() for path in [DOC_PATH, FORMAL_PATH, *csv_paths])
    rows.append({"validation_id": "VAL4678_2_outputs_exist", "passed": outputs_exist, "detail": "post/formal/csv outputs exist", "timestamp_utc": timestamp})
    claim_row = CLAIM_ID in read_text(CLAIMS_PATH)
    rows.append({"validation_id": "VAL4678_3_claim_row_exists", "passed": claim_row, "detail": f"{CLAIM_ID} present" if claim_row else f"{CLAIM_ID} missing", "timestamp_utc": timestamp})
    markers = MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH)
    rows.append({"validation_id": "VAL4678_4_markers", "passed": markers, "detail": "spine and packet markers present" if markers else "marker missing", "timestamp_utc": timestamp})
    no_claim = "valid_for_claim,true" not in read_text(RUNNER_CSV).lower() and "claim_allowed,true" not in read_text(RUNNER_CSV).lower()
    rows.append({"validation_id": "VAL4678_5_no_claim_promotion", "passed": no_claim, "detail": "runner remains nonclaim", "timestamp_utc": timestamp})
    pycache_absent = not (POST / "scripts" / "__pycache__").exists()
    rows.append({"validation_id": "VAL4678_6_pycache_absent", "passed": pycache_absent, "detail": "scripts __pycache__ absent" if pycache_absent else "scripts __pycache__ present", "timestamp_utc": timestamp})
    overall = source_ok and parse_ok and runner_ok and outputs_exist and claim_row and markers and no_claim and pycache_absent
    rows.append({"validation_id": "VAL4678_OVERALL", "passed": overall, "detail": "PASS" if overall else "FAIL", "timestamp_utc": timestamp})
    return rows


def write_documents(
    sources: list[dict[str, Any]],
    derivations: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    vectors: list[dict[str, Any]],
    tails: list[dict[str, Any]],
    common_modes: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    body = f"""# 4678 - Y5/R2FR Source-Charge Htau/MHref Coupling Tail or Jsourceweight nonEM Bound Row

**Current verdict:** 4678 makes the source-coupling route sharper and less circular.

After 4677:

```text
J_source_weight_abs_after_visible_EM
  = |J_EM_open_dynamic| + |J_source_weight_nonEM|
```

4678 splits the nonEM term:

```text
J_source_weight_nonEM
  = |J_rel_nonEM|
  + |J_common_derivative|
  + |R_eq|
  + |B_zero|
  + |epsilon_HM|.
```

The exact derivation route is:

```text
parent-owned connected nonEM graph
+ one action-density/current owner
+ no Hom(SpeciesLabel, active-source coefficient)
+ constructor exhaustion
+ no hidden/readout re-entry
=> w_A = w_* on the ordinary nonEM component.
```

`w_*` is allowed as calibrated `G_cal/GM` only if derivative-silent. If it varies, it becomes a common-mode fifth-force/source tail for R10/PPN/clock/orbital tests. This is not a public local-GR claim; it is the clean contract for the next proof.

## Runner results

{table(runners)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next target

{table(nexts)}

## Derivation rows

{table(derivations)}

## nonEM classical source-weight theorem

{table(theorem)}

## Jsourceweight/source-charge split

{table(vectors)}

## Req/Bzero/Htau tail contracts

{table(tails)}

## Common G calibration guard

{table(common_modes)}

## Controls

{table(controls)}

## Source register

{table(sources)}

## Validation

{table(validations)}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4678 -", "# 694 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        append_once(
            CLAIMS_PATH,
            CLAIM_ID,
            csv_line(
                [
                    CLAIM_ID,
                    "local_gr_empirical_interface",
                    "4678 imports the 4440-4442 source-charge trail into the post-4677 source-weight vector. It derives the classical nonEM relative source-weight route: parent-owned connected nonEM graph plus one action-density/current owner, no source-Hom, constructor exhaustion and no readout re-entry imply w_A=w_*. The common mode is calibrated G only if derivative-silent; R_eq, B_zero, H_tau/MHref and open-EM tails remain live.",
                    "Generated source register, derivation rows, nonEM classical source-weight theorem rows, source-charge split vector, Req/Bzero/Htau tail contracts, common G calibration guard, controls, runner, decision, status, next target and validation.",
                    DECISION.lower(),
                    NEXT_TARGET,
                    "Using observed GM or fitted G_N as source proof, treating hbar-only ownership as classical source closure, using physical template edges as parent-owned graph certificates, or claiming local GR before R_eq/B_zero/Htau/open-EM tails close.",
                    "local_gr",
                    str(DOC_PATH),
                    NEXT_TARGET,
                    "No public local-GR/Newton/PPN/R10 claim until the nonEM parent graph/current/no-Hom clauses are signed and same-current/Htau/open-EM tails are theorem-zero or source-backed bounded.",
                ]
            ),
        )

    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

4678 sharpens the coupling route after fixed visible EM removal:

```text
J_source_weight_nonEM
  = |J_rel_nonEM| + |J_common_derivative| + |R_eq| + |B_zero| + |epsilon_HM|
```

The relative nonEM term has an exact conditional zero route by scalar naturality on a parent-owned connected nonEM graph. The common mode is calibrated `G_cal/GM` only when derivative-silent; otherwise it is a common fifth-force/source tail. Remaining debts are `R_eq`, `B_zero`, `H_tau/MHref`, open/dynamic EM and the parent graph/current/no-Hom certificate.

- checkpoint: `{DOC_PATH.name}`
- formal note: `{FORMAL_PATH.name}`
- decision: `{DECISION}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

Packet update: the nonEM source-weight problem is no longer an undefined “coupling” blob. It is a classical connected-graph/no-Hom/current-owner theorem plus explicit `R_eq`, `B_zero`, `epsilon_HM`, common-derivative and open-EM tails.

- claim id: `{CLAIM_ID}`
- theorem csv: `{THEOREM_CSV.name}`
- vector csv: `{VECTOR_CSV.name}`
- tail csv: `{TAIL_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def main() -> None:
    timestamp = now()
    sources = source_rows(timestamp)
    derivations = derivation_rows(timestamp)
    theorem = theorem_rows(timestamp)
    vectors = vector_rows(timestamp)
    tails = tail_rows(timestamp)
    common_modes = common_mode_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    runners = runner_rows(timestamp, sources, derivations, theorem, vectors, tails, common_modes)

    csv_paths = [
        SOURCE_REGISTER,
        DERIVATION_CSV,
        THEOREM_CSV,
        VECTOR_CSV,
        TAIL_CSV,
        COMMON_MODE_CSV,
        CONTROL_CSV,
        RUNNER_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DERIVATION_CSV, derivations)
    write_csv(THEOREM_CSV, theorem)
    write_csv(VECTOR_CSV, vectors)
    write_csv(TAIL_CSV, tails)
    write_csv(COMMON_MODE_CSV, common_modes)
    write_csv(CONTROL_CSV, controls)
    write_csv(RUNNER_CSV, runners)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_documents(sources, derivations, theorem, vectors, tails, common_modes, controls, runners, decisions, statuses, nexts, [])
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    validations = validation_rows(timestamp, csv_paths, sources, runners)
    write_csv(VALIDATION_CSV, validations)
    write_documents(sources, derivations, theorem, vectors, tails, common_modes, controls, runners, decisions, statuses, nexts, validations)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
