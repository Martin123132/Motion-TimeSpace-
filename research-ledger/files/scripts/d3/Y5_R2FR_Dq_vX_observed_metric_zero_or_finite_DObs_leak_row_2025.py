from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
DOC = ROOT / "2025-Y5-R2FR-Dq-vX-observed-metric-zero-or-finite-DObs-leak-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {"timestamp_utc": stamp(), "branch_id": BRANCH_ID, "valid_for_claim": False}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_rows_parse(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def md_cell(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines) + "\n"


def count_formalization_modified() -> int:
    if not FORMALIZATION.exists():
        return 0
    try:
        result = subprocess.run(
            ["git", "-C", str(FORMALIZATION), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def formalization_has_2025_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2025*Dq*")) or any(FORMALIZATION.rglob("*2025*observed*"))
    except Exception:
        return False


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2025_00_2024_handoff",
            ROOT / "2024-Y5-R2FR-observed-representative-split-or-active-ZX-MX2-row.md",
            ["NEXT2024_0_2025", "ORS2024_3_Dq_vX_gobs_zero", "VAL2024_OVERALL"],
            "2024 handoff selects Dq[v_X] and observed-metric invariance as the next gate.",
        ),
        (
            "SRC2025_01_2024_split_csv",
            OUT / "P8_Y5_PARENT_QLOC_2024_OBS_REP_SPLIT_THEOREM.csv",
            ["ORS2024_3_Dq_vX_gobs_zero", "ORS2024_8_verdict"],
            "machine-readable observed/representative split theorem.",
        ),
        (
            "SRC2025_02_2024_certificate_csv",
            OUT / "P8_Y5_PARENT_QLOC_2024_OBS_REP_CERTIFICATE_ROWS.csv",
            ["OSC2024_2_Dq_kernel", "OSC2024_3_gobs_invariance"],
            "unsigned certificate rows for Dq kernel and observed-metric invariance.",
        ),
        (
            "SRC2025_03_1737_doc",
            ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md",
            ["DQM1737_0_DObs_e", "DQM1737_5_Dq_total_kernel", "CFZ1737_0_exact_conditional"],
            "q-map/Dq/coframe-zero source theorem and its missing matrix rows.",
        ),
        (
            "SRC2025_04_1737_dq_csv",
            OUT / "P8_Y5_PARENT_QLOC_1737_DQ_MATRIX_REQUIREMENTS.csv",
            ["DQM1737_0_DObs_e", "DQM1737_5_Dq_total_kernel"],
            "Dq matrix requirements for observed coframe and total quotient kernel.",
        ),
        (
            "SRC2025_05_1737_vertical_csv",
            OUT / "P8_Y5_PARENT_QLOC_1737_VERTICAL_BASIS_CONTRACT.csv",
            ["VB1737_0_vZ", "VB1737_5_vtau_readout"],
            "candidate vertical-direction basis contract.",
        ),
        (
            "SRC2025_06_1737_coframe_csv",
            OUT / "P8_Y5_PARENT_QLOC_1737_COFRAME_FUNCTOR_ZERO_ATTEMPT.csv",
            ["CFZ1737_0_exact_conditional", "CFZ1737_3_current_verdict"],
            "coframe functor zero theorem attempt.",
        ),
        (
            "SRC2025_07_1780_doc",
            ROOT / "1780-Y5-R2FR-q-Dq-tau-source-functor-signature-or-Delta-frame-tau-first-row.md",
            ["QTS1780_1_Dq_kernel_basis", "FTZ1780_0_chain_rule_core", "DFT1780_0_DObs_e"],
            "q/Dq/tau/source functor signature gate and finite row fallback.",
        ),
        (
            "SRC2025_08_1780_signature_csv",
            OUT / "P8_Y5_PARENT_QLOC_1780_Q_DQ_TAU_SOURCE_FUNCTOR_SIGNATURE_GATE.csv",
            ["QTS1780_1_Dq_kernel_basis", "QTS1780_7_verdict"],
            "machine-readable q/Dq/tau/source functor signature gate.",
        ),
        (
            "SRC2025_09_1784_doc",
            ROOT / "1784-Y5-R2FR-parent-Omega-DCX-vertical-action-packet-or-DqZ-geometry-row.md",
            ["ODP1784_4_field_action", "DZG1784_0_eobs_metric", "ODP1784_8_verdict"],
            "parent Omega/DC_X/v_X action packet and Dq_Z observed-geometry fallback.",
        ),
        (
            "SRC2025_10_1784_packet_csv",
            OUT / "P8_Y5_PARENT_QLOC_1784_OMEGA_DCX_VERTICAL_PACKET_GATE.csv",
            ["ODP1784_4_field_action", "ODP1784_8_verdict"],
            "machine-readable parent vertical-action packet gate.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def zero_attempt_rows() -> list[dict[str, object]]:
    data = [
        (
            "DVO2025_0_chain_rule",
            "DObs_e vertical variation",
            "If e_obs=E(q(Phi)) and E is differentiable, then DObs_e[v_X]=DE_q(Dq[v_X]).",
            "EXACT_CONDITIONAL_THEOREM",
            "This is the right bridge: observed geometry is silent whenever the parent quotient kills v_X.",
            "Dq[v_X]=0 and parent-owned E(q) are not yet signed.",
            "construct parent q/Dq matrix and field action for each vertical direction",
        ),
        (
            "DVO2025_1_metric_pullback",
            "observed metric vertical variation",
            "With g_obs=eta_ab e_obs^a tensor e_obs^b, Dg_obs[v_X]=2 sym_eta(e_obs,DObs_e[v_X]); hence DObs_e[v_X]=0 implies Dg_obs[v_X]=0.",
            "EXACT_CONDITIONAL_THEOREM",
            "Metric invariance follows from coframe invariance; no separate metric miracle is needed.",
            "DObs_e[v_X]=0 is not parent-signed.",
            "source DObs_e[v_X] theorem-zero or finite leak row",
        ),
        (
            "DVO2025_2_Dq_kernel_requirement",
            "quotient-kernel condition",
            "Dq[v_X]=0 for the selected local representative direction and for every auxiliary field that enters readout.",
            "MISSING_PARENT_INPUT",
            "This is the actual missing lock, not the chain rule.",
            "no parent q map, no full Dq matrix, no field-by-field v_X action.",
            "write q(Phi), Dq, and v_X components in one parent chart",
        ),
        (
            "DVO2025_3_field_action_requirement",
            "field-by-field vertical generator",
            "v_X must act on coframe/metric, momenta, Gamma/Khat/q_loc, memory/domain/projector, matter/readout/constants, and boundary modes.",
            "MISSING_PARENT_INPUT",
            "A Lie derivative on geometry alone is too small to prove local silence.",
            "ODP1784_4 reports FIELD_MAP_INCOMPLETE.",
            "start with v_Z and either sign silence or emit finite DObs/Dg rows",
        ),
        (
            "DVO2025_4_functor_requirement",
            "observed coframe functor",
            "e_obs=E(q(Phi)) must be parent-owned rather than chosen by projection after variation.",
            "MISSING_PARENT_INPUT",
            "Prevents smuggling local-GR recovery in by representation choice.",
            "E(q), source readout, theta role, tau lock, and boundary projector remain unsigned together.",
            "derive Obs_e from the parent action/quotient or keep leak rows nonclaim",
        ),
        (
            "DVO2025_5_total_kernel_status",
            "all-direction kernel status",
            "The current branch has a conditional zero theorem but not a certified all-direction Dq kernel.",
            "ZERO_THEOREM_CONDITIONAL_ONLY",
            "We can use the theorem as a target, not as evidence.",
            "VB1737 vertical directions are named but not evaluated by a source-backed Dq matrix.",
            "move to first concrete direction row, preferably v_Z",
        ),
        (
            "DVO2025_6_verdict",
            "2025 local geometry zero verdict",
            "DObs_e[v_X]=0 and v_X[g_obs]=0 are derivable if Dq[v_X]=0 and e_obs=E(q(Phi)); those premises are unsigned, so no local-GR/R10/PPN claim is allowed.",
            "ZERO_THEOREM_NOT_ACTIVE",
            "This is a useful theorem-shaped gap: the target is sharp and falsifiable.",
            "missing Dq[v_X], E(q), and full v_X field action certificates.",
            "2026 should build q/Dq/v_Z or emit first finite DObs_e/Dg_obs leak row",
        ),
    ]
    rows = []
    for row_id, obj, statement, status, claim_effect, missing, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object": obj,
                "statement": statement,
                "status": status,
                "claim_effect": claim_effect,
                "missing_input": missing,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def vertical_direction_rows() -> list[dict[str, object]]:
    data = [
        ("VDS2025_0_vZ", "v_Z", "geometry/impedance representative direction", "VB1737_0_vZ;ODP1784_4_field_action", "Dq[v_Z]", "DObs_e[v_Z];Dg_obs[v_Z]"),
        ("VDS2025_1_vphi", "v_phi", "phase/clock representative direction", "VB1737_1_vphi;QTS1780_3_tau_projectability", "Dq[v_phi]", "Dtheta[v_phi];Dtau[v_phi]"),
        ("VDS2025_2_vRAB_Jq", "v_RAB_Jq", "source/readout representative direction", "VB1737_2_vRAB_Jq;QTS1780_4_source_readout_functor", "Dq[v_RAB/Jq]", "Dsource[v_RAB/Jq]"),
        ("VDS2025_3_vboundary", "v_boundary", "boundary/projector representative direction", "VB1737_3_vboundary", "Dq[v_boundary]", "Dboundary_projector[v_boundary]"),
        ("VDS2025_4_vtheta_marker", "v_theta_marker", "role-marker representative direction", "VB1737_4_vtheta_marker", "Dq[v_theta_marker]", "Dtheta_marker[v_theta_marker]"),
        ("VDS2025_5_vtau_readout", "v_tau_readout", "tau/readout representative direction", "VB1737_5_vtau_readout;FTZ1780_0_chain_rule_core", "Dq[v_tau_readout]", "Dtau_pushforward[v_tau_readout]"),
    ]
    rows = []
    for row_id, direction, interpretation, source_rows, needed_kernel, needed_leak in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "direction": direction,
                "interpretation": interpretation,
                "source_rows": source_rows,
                "needed_kernel": needed_kernel,
                "needed_leak_if_not_zero": needed_leak,
                "status": "MISSING_PARENT_DQ_MATRIX",
                "arena_status": "LOCAL_ARENAS_BLOCKED",
                "next_action": "evaluate direction in explicit q/Dq matrix or emit finite leak row",
            }
        )
        rows.append(row)
    return rows


def leak_schema_rows() -> list[dict[str, object]]:
    data = [
        ("DOL2025_0_direction_id", "direction_id", "which vertical direction is being tested", "dimensionless label", "MISSING_PARENT_INPUT", "all local arenas"),
        ("DOL2025_1_Dq_v", "Dq[v]", "quotient derivative on the direction", "units of q per direction amplitude", "MISSING_PARENT_INPUT", "R10/PPN/clocks/orbital"),
        ("DOL2025_2_DObs_e", "DObs_e[v]", "observed coframe leak under vertical variation", "coframe units per direction amplitude", "MISSING_PARENT_INPUT", "PPN/local-GR"),
        ("DOL2025_3_Dg_obs", "Dg_obs[v]", "observed metric leak induced by DObs_e", "metric units per direction amplitude", "MISSING_PARENT_INPUT", "PPN/local-GR/orbital"),
        ("DOL2025_4_Dsource_readout", "Dsource[v]", "matter/source readout leak", "source-readout units per direction amplitude", "MISSING_PARENT_INPUT", "WEP/R10"),
        ("DOL2025_5_Dtheta_marker", "Dtheta[v]", "role-marker leak", "dimensionless per direction amplitude", "MISSING_PARENT_INPUT", "clocks/EM"),
        ("DOL2025_6_Dboundary_projector", "Dboundary[v]", "boundary/projector leak", "projector units per direction amplitude", "MISSING_PARENT_INPUT", "orbital/R10"),
        ("DOL2025_7_Dtau_pushforward", "Dtau[v]", "time/readout pushforward leak", "seconds per direction amplitude", "MISSING_PARENT_INPUT", "clocks/cosmology"),
        ("DOL2025_8_norm", "norm", "norm used to combine DObs_e and Dg_obs leak components", "declared norm units", "MISSING_ARENA_PROJECTION", "PPN/R10"),
        ("DOL2025_9_arena_projection", "arena_projection", "map from parent leak to R10/PPN/clock/orbital observable", "arena-specific", "MISSING_ARENA_PROJECTION", "all local arenas"),
        ("DOL2025_10_total_abs", "epsilon_obs", "absolute observable-geometry leak score", "arena-specific", "MISSING_PARENT_INPUT", "all local arenas"),
    ]
    rows = []
    for row_id, quantity, definition, units, status, arena in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "definition": definition,
                "units": units,
                "status": status,
                "arena_link": arena,
                "source_path": "MISSING_PARENT_SOURCE",
                "claim_status": "NONCLAIM_SCHEMA_ONLY",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2025_0_chain_theorem", "chain-rule theorem may be cited", "DVO2025_0_chain_rule;DVO2025_1_metric_pullback", "THEOREM_WRITTEN_CONDITIONAL", False, "the theorem is exact but its premises are unsigned"),
        ("GATE2025_1_Dq_kernel_signed", "Dq[v_X]=0 is parent-signed", "DVO2025_2_Dq_kernel_requirement", "FAIL_MISSING_PARENT_INPUT", False, "no parent q/Dq matrix"),
        ("GATE2025_2_field_action_signed", "v_X action is field-complete", "DVO2025_3_field_action_requirement", "FAIL_MISSING_PARENT_INPUT", False, "matter/readout/boundary/tau fields unmapped"),
        ("GATE2025_3_obs_functor_signed", "e_obs=E(q(Phi)) is parent-owned", "DVO2025_4_functor_requirement", "FAIL_MISSING_PARENT_INPUT", False, "observed functor not derived from parent action"),
        ("GATE2025_4_DObs_zero_active", "DObs_e[v_X]=0 and Dg_obs[v_X]=0 are active", "GATE2025_1;GATE2025_2;GATE2025_3", "FAIL_CONDITIONAL_ONLY", False, "zero theorem cannot be promoted"),
        ("GATE2025_5_finite_leak_score_ready", "finite DObs/Dg leak rows can be scored", "DOL2025_*", "FAIL_MISSING_ARENA_PROJECTION", False, "schema exists but no numeric source rows"),
        ("GATE2025_6_local_GR_claim", "local GR/PPN/R10 pass can be claimed", "GATE2025_4 or GATE2025_5", "FAIL_BLOCKED", False, "neither theorem-zero nor finite leak score is source-backed"),
    ]
    rows = []
    for claim_id, claim, required_rows, status, allowed, reason in data:
        row = base_row()
        row.update(
            {
                "claim_id": claim_id,
                "claim": claim,
                "required_rows": required_rows,
                "status": status,
                "claim_allowed": allowed,
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2025_0_chain_rule_without_Dq", "Do not promote DObs_e=DE_q(Dq[v]) to zero unless Dq[v]=0 is parent-signed.", "ACTIVE_REFUSAL"),
        ("REF2025_1_projection_by_declaration", "Do not define observed variables after variation just to hide the leak.", "ACTIVE_REFUSAL"),
        ("REF2025_2_single_direction_as_all", "Do not treat one candidate v_Z row as the whole vertical basis.", "ACTIVE_REFUSAL"),
        ("REF2025_3_local_GR_claim", "Do not claim local GR, PPN, R10, WEP, clock, or orbital pass from this checkpoint.", "ACTIVE_REFUSAL"),
        ("REF2025_4_active_X_scoring", "Do not score active X until Z_X/M_X^2 and numerator coefficients are source-backed.", "ACTIVE_REFUSAL"),
        ("REF2025_5_github", "No GitHub push or public-facing claim from this private checkpoint.", "ACTIVE_REFUSAL"),
    ]
    rows = []
    for refusal_id, rule, status in data:
        row = base_row()
        row.update({"refusal_id": refusal_id, "rule": rule, "status": status})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2025_0_result", "exact DObs/Dg chain theorem exists, but it is only a conditional zero theorem", "keep theorem as bridge target; do not claim local silence"),
        ("DEC2025_1_gap", "the real missing object is parent q/Dq plus field-complete v_X action", "stop adding downstream tests until at least one direction is evaluated"),
        ("DEC2025_2_best_next_route", "start with v_Z because it is the geometry/impedance representative direction closest to DObs_e and Dg_obs", "build q/Dq/v_Z first, then decide theorem-zero versus finite leak"),
        ("DEC2025_3_fallback", "if v_Z cannot be signed zero, emit numeric/source-ready DObs_e[v_Z] and Dg_obs[v_Z] leak rows", "local branch becomes bounded-residual rather than exact-closure route"),
    ]
    rows = []
    for decision_id, decision, consequence in data:
        row = base_row()
        row.update({"decision_id": decision_id, "decision": decision, "consequence": consequence})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "next_id": "NEXT2025_0_2026",
            "target_doc": "2026-Y5-R2FR-parent-q-Dq-matrix-field-action-or-first-vZ-DObs-row.md",
            "objective": "construct parent q/Dq matrix and field-by-field v_X for observed metric, beginning with v_Z; if fail, source first DObs_e[v_Z]/Dg_obs[v_Z] leak row",
            "required_inputs": "parent field chart; q(Phi); Dq matrix; v_Z action on coframe/metric/matter/readout/boundary/tau; E(q) functor; leak norm and arena projection",
            "exclusions": "projection by declaration; chain-rule zero without Dq; local-GR claim; active X scoring; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def write_branch_copies(zero_rows: list[dict[str, object]], vertical_rows: list[dict[str, object]], leak_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2025_0_source_weight",
            SOURCE_WEIGHT_DOCS / "AFRAME_DQ_VX_OBS_ZERO_2025_NONCLAIM.csv",
            zero_rows,
        ),
        (
            "COPY2025_1_wep_lock",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2025_DQ_VX_STATUS_NONCLAIM.csv",
            vertical_rows,
        ),
        (
            "COPY2025_2_acquisition_queue",
            QUEUE / "JR2025_DOBS_DGOBS_LEAK_ROW_QUEUE.csv",
            leak_rows,
        ),
    ]
    rows = []
    for copy_id, path, payload in copies:
        write_csv(path, payload)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "status": "WRITTEN_NONCLAIM_COPY" if path.exists() and csv_rows_parse(path) else "COPY_WRITE_FAIL",
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    vertical_rows: list[dict[str, object]],
    leak_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    refusal_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "VAL2025_00_sources_exist",
            all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows),
            "every cited local source path exists and required source needles were found",
        )
    )
    checks.append(
        (
            "VAL2025_01_csv_parse",
            all(path.exists() and csv_rows_parse(path) for path in csv_paths),
            "all generated CSV files parse cleanly",
        )
    )
    checks.append(
        (
            "VAL2025_02_chain_theorem_present",
            any(row["row_id"] == "DVO2025_0_chain_rule" and "DE_q(Dq[v_X])" in str(row["statement"]) for row in zero_rows),
            "chain-rule bridge is written explicitly",
        )
    )
    checks.append(
        (
            "VAL2025_03_metric_pullback_present",
            any(row["row_id"] == "DVO2025_1_metric_pullback" and "Dg_obs" in str(row["statement"]) for row in zero_rows),
            "observed metric pullback condition is written explicitly",
        )
    )
    checks.append(
        (
            "VAL2025_04_zero_not_promoted",
            any(row["row_id"] == "DVO2025_6_verdict" and row["status"] == "ZERO_THEOREM_NOT_ACTIVE" and row["valid_for_claim"] is False for row in zero_rows),
            "conditional theorem is not promoted to local-GR evidence",
        )
    )
    expected_directions = {
        "VDS2025_0_vZ",
        "VDS2025_1_vphi",
        "VDS2025_2_vRAB_Jq",
        "VDS2025_3_vboundary",
        "VDS2025_4_vtheta_marker",
        "VDS2025_5_vtau_readout",
    }
    checks.append(
        (
            "VAL2025_05_vertical_direction_coverage",
            expected_directions == {str(row["row_id"]) for row in vertical_rows},
            "all six inherited vertical directions are represented",
        )
    )
    checks.append(
        (
            "VAL2025_06_leak_rows_nonclaim",
            all(row["valid_for_claim"] is False and str(row["status"]).startswith("MISSING_") for row in leak_rows),
            "finite leak row schema remains blocked/nonclaim",
        )
    )
    checks.append(
        (
            "VAL2025_07_local_claims_blocked",
            all(row["claim_allowed"] is False for row in gate_rows),
            "all local arena claims remain blocked unless theorem-zero or finite leak rows are sourced",
        )
    )
    checks.append(
        (
            "VAL2025_08_refusals_active",
            all(row["status"] == "ACTIVE_REFUSAL" for row in refusal_rows_),
            "anti-smuggling refusals are active",
        )
    )
    checks.append(
        (
            "VAL2025_09_next_selected",
            len(next_rows) == 1 and next_rows[0]["next_id"] == "NEXT2025_0_2026",
            "next target is selected",
        )
    )
    checks.append(
        (
            "VAL2025_10_formalization_unchanged",
            count_formalization_modified() == 0,
            "formalization-workbench modified-file count remains 0",
        )
    )
    checks.append(
        (
            "VAL2025_11_no_formalization_2025_artifacts",
            not formalization_has_2025_artifacts(),
            "no 2025 Dq/observed artifacts were written under formalization-workbench",
        )
    )
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = base_row()
    overall.update(
        {
            "check_id": "VAL2025_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2025 Dq/vX observed-metric zero gate is internally valid and nonclaim.",
        }
    )
    rows.append(overall)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    vertical_rows: list[dict[str, object]],
    leak_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    refusal_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 2025 Y5 R2FR Dq[v_X] Observed-Metric Zero Or Finite DObs Leak Row",
        "",
        "## Current Verdict",
        "The useful theorem is now sharp: if `e_obs=E(q(Phi))` and `Dq[v_X]=0`, then `DObs_e[v_X]=DE_q(Dq[v_X])=0`, and the induced observed metric variation `Dg_obs[v_X]` also vanishes. That is a real bridge toward derived local GR silence, but the parent `q/Dq/v_X` certificates are still missing, so this checkpoint does **not** claim local GR, PPN, R10, WEP, clock, or orbital success.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "needles", "note", "valid_for_claim"]),
        "## Dq[v_X] / Observed-Metric Zero Attempt",
        md_table(zero_rows, ["row_id", "object", "statement", "status", "claim_effect", "missing_input", "next_action", "valid_for_claim"]),
        "## Vertical Direction Status",
        md_table(vertical_rows, ["row_id", "direction", "interpretation", "source_rows", "needed_kernel", "needed_leak_if_not_zero", "status", "arena_status", "next_action", "valid_for_claim"]),
        "## Finite DObs/Dg Leak Row Schema",
        md_table(leak_rows, ["row_id", "quantity", "definition", "units", "status", "arena_link", "source_path", "claim_status", "valid_for_claim"]),
        "## Claim Gate",
        md_table(gate_rows, ["claim_id", "claim", "required_rows", "status", "claim_allowed", "reason", "valid_for_claim"]),
        "## Refusal Runner",
        md_table(refusal_rows_, ["refusal_id", "rule", "status", "valid_for_claim"]),
        "## Decision Ledger",
        md_table(decision_rows_, ["decision_id", "decision", "consequence", "valid_for_claim"]),
        "## Next Target",
        md_table(next_rows, ["next_id", "target_doc", "objective", "required_inputs", "exclusions", "valid_for_claim"]),
        "## Branch Copies",
        md_table(branch_rows, ["copy_id", "path", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows_, ["check_id", "status", "detail", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    zero_rows = zero_attempt_rows()
    vertical_rows = vertical_direction_rows()
    leak_rows = leak_schema_rows()
    gate_rows = claim_gate_rows()
    refusal_rows_ = refusal_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "source": OUT / "P8_Y5_PARENT_QLOC_2025_SOURCE_REGISTER.csv",
        "zero": OUT / "P8_Y5_PARENT_QLOC_2025_DQ_VX_OBS_METRIC_ZERO_ATTEMPT.csv",
        "leak": OUT / "P8_Y5_PARENT_QLOC_2025_DOBS_LEAK_ROW_SCHEMA.csv",
        "vertical": OUT / "P8_Y5_PARENT_QLOC_2025_VERTICAL_DIRECTION_STATUS.csv",
        "gate": OUT / "P8_Y5_PARENT_QLOC_2025_CLAIM_GATE.csv",
        "refusal": OUT / "P8_Y5_PARENT_QLOC_2025_REFUSAL_RUNNER.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2025_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2025_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2025_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2025_VALIDATION.csv",
    }

    write_csv(paths["source"], source_rows)
    write_csv(paths["zero"], zero_rows)
    write_csv(paths["leak"], leak_rows)
    write_csv(paths["vertical"], vertical_rows)
    write_csv(paths["gate"], gate_rows)
    write_csv(paths["refusal"], refusal_rows_)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(zero_rows, vertical_rows, leak_rows)
    write_csv(paths["branch"], branch_rows)

    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [
        Path(row["path"]) for row in branch_rows
    ]
    validation_rows_ = validation_rows(
        source_rows,
        zero_rows,
        vertical_rows,
        leak_rows,
        gate_rows,
        refusal_rows_,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)

    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        zero_rows,
        vertical_rows,
        leak_rows,
        gate_rows,
        refusal_rows_,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        zero_rows,
        vertical_rows,
        leak_rows,
        gate_rows,
        refusal_rows_,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
