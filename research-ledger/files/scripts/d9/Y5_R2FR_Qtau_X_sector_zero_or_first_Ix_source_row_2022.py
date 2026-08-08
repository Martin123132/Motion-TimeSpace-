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
DOC = ROOT / "2022-Y5-R2FR-Qtau-X-sector-zero-or-first-Ix-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "valid_for_claim": False,
    }


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
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines) + "\n"


def count_formalization_modified_since_start() -> int:
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


def formalization_has_2022_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2022*Ix*")) or any(FORMALIZATION.rglob("*2022*IX*"))
    except Exception:
        return False


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2022_00_2021_handoff",
            ROOT / "2021-Y5-R2FR-Aframe-Qtau-sector-owner-or-MHref-first-source-row.md",
            ["NEXT2021_0_2022", "QSO2021_6_first_live_obstruction", "QSL2021_1_X_extra"],
            "2021 handoff selects Q_tau_X/I_X as first non-EH obstruction.",
        ),
        (
            "SRC2022_01_1799_ix",
            ROOT / "1799-Y5-R2FR-minimal-parent-current-action-skeleton-or-first-Ix-row.md",
            ["MXA1799_7_verdict", "IXR1799_0_identity", "DEC1799_1_ix_row"],
            "minimal X-action skeleton and first I_X row.",
        ),
        (
            "SRC2022_02_1800_x_nohair",
            ROOT / "1800-Y5-R2FR-X-positive-operator-activation-or-Yukawa-fallback-row.md",
            ["XPA1800_5_verdict", "YFR1800_0_formula", "DEC1800_0_nohair"],
            "positive-operator nohair attempt and Yukawa fallback.",
        ),
        (
            "SRC2022_03_1801_jx",
            ROOT / "1801-Y5-R2FR-JX-source-zero-or-component-bound-pack.md",
            ["JZS1801_8_verdict", "JCB1801_5_total_abs_guard", "OBS1801_2_PPN_Newton"],
            "J_X source-zero and component-bound pack.",
        ),
        (
            "SRC2022_04_1802_matter_readout",
            ROOT / "1802-Y5-R2FR-parent-matter-functor-readout-no-reentry-or-qbar-readout-row.md",
            ["MRT1802_7_verdict", "QRC1802_5_total_abs_guard", "RTS1802_0_pure_postprocessing"],
            "matter/readout no-reentry and qbar component envelope.",
        ),
        (
            "SRC2022_05_1803_shadow",
            ROOT / "1803-Y5-R2FR-no-shadow-constant-marker-or-qbar-coefficient-pack.md",
            ["no-shadow theorem", "qbar_marker", "Claim ceiling"],
            "hidden-coupling/no-shadow/constant-marker coefficient pack.",
        ),
        (
            "SRC2022_06_1785_parent_lagrangian",
            ROOT / "1785-Y5-R2FR-parent-Lagrangian-theta-vX-minimal-fill-or-DqZ-geometry-source-row.md",
            ["PLT1785_0_L_parent", "NPJ1785_6_verdict", "DEC1785_0_exact_contract"],
            "parent Lagrangian/theta/vX gate needed to own X-sector current.",
        ),
        (
            "SRC2022_07_2021_theorem_csv",
            OUT / "P8_Y5_PARENT_QLOC_2021_QTAU_SECTOR_OWNER_THEOREM.csv",
            ["QSO2021_6_first_live_obstruction", "QSO2021_7_verdict"],
            "machine-readable 2021 Q_tau sector-owner theorem.",
        ),
        (
            "SRC2022_08_2021_sector_csv",
            OUT / "P8_Y5_PARENT_QLOC_2021_QTAU_SECTOR_LEDGER.csv",
            ["QSL2021_1_X_extra", "QSL2021_7_total"],
            "machine-readable 2021 Q_tau sector ledger.",
        ),
        (
            "SRC2022_09_1799_ix_csv",
            OUT / "P8_Y5_PARENT_QLOC_1799_FIRST_IX_SOURCE_BOUND_ROW.csv",
            ["IXR1799_0_identity", "IXR1799_7_acceptance"],
            "machine-readable first I_X source-bound row.",
        ),
        (
            "SRC2022_10_1800_activation_csv",
            OUT / "P8_Y5_PARENT_QLOC_1800_POSITIVE_OPERATOR_ACTIVATION_AUDIT.csv",
            ["XPA1800_1_operator_sign_gap", "XPA1800_5_verdict"],
            "machine-readable X positive-operator activation audit.",
        ),
        (
            "SRC2022_11_1801_jx_csv",
            OUT / "P8_Y5_PARENT_QLOC_1801_JX_COMPONENT_BOUND_PACK.csv",
            ["JCB1801_0_matter", "JCB1801_5_total_abs_guard"],
            "machine-readable J_X component bound pack.",
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


def x_zero_theorem_rows() -> list[dict[str, object]]:
    data = [
        {
            "theorem_id": "XZT2022_0_parent_route",
            "claim": "X-sector route is selected by the parent action",
            "mathematical_form": "X is either absent/gauge/topological, or an active positive operator field, or a finite sourced residual",
            "status": "ROUTE_NOT_PARENT_SELECTED",
            "missing_input": "MISSING_PARENT_X_NORMAL_FORM",
            "consequence": "cannot set Q_tau_X=0 or compute alpha_X until route is selected",
        },
        {
            "theorem_id": "XZT2022_1_positive_action",
            "claim": "active X field has positive quadratic local operator",
            "mathematical_form": "L_X=-1/2 Z_X nabla_mu X nabla^mu X -1/2 M_X^2 X^2 + X J_X + dB_X, with Z_X>0 and M_X^2>=0 after zero-mode removal",
            "status": "CONDITIONAL_NOHAIR_FORM_WRITTEN",
            "missing_input": "MISSING_ZX;MISSING_MX2;MISSING_ZERO_MODE_RULE;MISSING_OPERATOR_SOURCE",
            "consequence": "operator sign/gap is required before the energy identity can kill X",
        },
        {
            "theorem_id": "XZT2022_2_energy_identity",
            "claim": "positive operator plus zero source/boundary implies X=0",
            "mathematical_form": "0=int_D X E_X = int_D(Z_X |nabla X|^2 + M_X^2 X^2) - int_D X J_X + boundary_X",
            "status": "DERIVED_CONDITIONAL_IDENTITY",
            "missing_input": "MISSING_JX_ZERO;MISSING_BOUNDARY_X_ZERO;MISSING_DOMAIN_REGULARITY",
            "consequence": "if J_X=0 and boundary_X=0, then X=0 and Q_tau_X/C_tau_X/I_X vanish",
        },
        {
            "theorem_id": "XZT2022_3_source_silence",
            "claim": "J_X source term is zero in the local exterior",
            "mathematical_form": "J_X=J_matter+J_chiD_wall+J_boundary+J_readout+J_history+Pi_M_tail=0",
            "status": "SOURCE_SILENCE_NOT_PROVED",
            "missing_input": "MISSING_JX_COMPONENT_ZERO_OR_BOUNDS",
            "consequence": "nonzero J_X forces finite source/test charge rows",
        },
        {
            "theorem_id": "XZT2022_4_boundary_zero",
            "claim": "X has no improper boundary, edge, history, or zero-mode tail",
            "mathematical_form": "boundary_X=0, Pi_X delta X|partialD=0, Q_edge_X=0, and constant/topological zero modes are removed or universal",
            "status": "BOUNDARY_ZERO_NOT_SIGNED",
            "missing_input": "MISSING_BOUNDARY_FLUX_ZERO;MISSING_EDGE_CHARGE_ZERO;MISSING_ZERO_MODE_CERTIFICATE",
            "consequence": "boundary/history tails stay inside the absolute I_X envelope",
        },
        {
            "theorem_id": "XZT2022_5_Hamiltonian_projection",
            "claim": "X charge is orthogonal to measured Hamiltonian mass",
            "mathematical_form": "Pi_M^H[Q_tau_X]=0 or |Pi_M^H Q_tau_X|/M_H_ref is source-backed finite",
            "status": "PIM_PROJECTION_NOT_SIGNED",
            "missing_input": "MISSING_PIM_H_ORTHOGONALITY;MISSING_MH_REF;MISSING_PROJECTION_COEFFICIENT",
            "consequence": "X can contaminate the denominator until projection is zero/bounded",
        },
        {
            "theorem_id": "XZT2022_6_Ix_bound_identity",
            "claim": "if zero theorem fails, I_X has a no-cancellation bound target",
            "mathematical_form": "|I_X|/M_H_ref <= (|int_S i_tau omega_X|+|int_A C_X|+|boundary_X|+|Pi_M_tail|)/M_H_ref",
            "status": "FINITE_ROW_SCHEMA_READY_VALUES_MISSING",
            "missing_input": "MISSING_OMEGA_X;MISSING_C_X;MISSING_BOUNDARY_X;MISSING_PIM_TAIL;MISSING_MH_REF",
            "consequence": "testing route is available but not scoreable yet",
        },
        {
            "theorem_id": "XZT2022_7_verdict",
            "claim": "Q_tau_X/C_tau_X/I_X are theorem-zero for current MTS",
            "mathematical_form": "XZT2022_0 through XZT2022_5 close in one parent branch",
            "status": "X_SECTOR_ZERO_NOT_PROVED",
            "missing_input": "MISSING_PARENT_X_NORMAL_FORM_AND_SOURCE_BOUNDARY_PROJECTION_PACK",
            "consequence": "Q_tau^MTS/M_H_ref/local-GR branch remains blocked by I_X",
        },
    ]
    rows = []
    for item in data:
        row = base_row()
        row.update({**item, "parent_signed": False, "theorem_zero": False})
        rows.append(row)
    return rows


def ix_source_rows() -> list[dict[str, object]]:
    data = [
        ("IXS2022_0_ZX", "Z_X", "X kinetic/operator normalization", "MISSING_ZX", "operator_or_action_units"),
        ("IXS2022_1_MX2", "M_X^2", "X mass/range term; lambda_X=sqrt(Z_X/M_X^2)", "MISSING_MX2", "inverse_length_squared_or_action_units"),
        ("IXS2022_2_Jmatter", "J_matter", "ordinary matter source leg for X", "MISSING_JMATTER_ZERO_OR_BOUND", "source_current"),
        ("IXS2022_3_JchiD", "J_chiD_wall", "chi_D wall/source tail for X", "MISSING_CHID_WALL_BOUND", "source_current"),
        ("IXS2022_4_Jboundary", "J_boundary", "boundary/edge/reference source tail for X", "MISSING_BOUNDARY_EDGE_FLUX", "source_current_or_charge"),
        ("IXS2022_5_Jreadout", "J_readout", "readout/calibration/source-mask reentry tail", "MISSING_READOUT_REENTRY_COEFFICIENTS", "source_current"),
        ("IXS2022_6_Jhistory", "J_history", "memory/history kernel source tail", "MISSING_HISTORY_KERNEL_NORM", "source_current"),
        ("IXS2022_7_boundaryX", "boundary_X", "boundary flux and zero-mode contribution in energy identity", "MISSING_BOUNDARY_X_ZERO_OR_BOUND", "charge_or_flux"),
        ("IXS2022_8_omegaX", "int_S i_tau omega_X", "X symplectic flux contribution to Hamiltonian curl", "MISSING_OMEGA_X", "charge_variation"),
        ("IXS2022_9_PiMtail", "Pi_M^H Q_tau_X", "Hamiltonian mass projection tail", "MISSING_PIM_PROJECTION_COEFFICIENT", "dimensionless_after_MHref"),
        ("IXS2022_10_MHref", "M_H_ref", "common positive source denominator", "MISSING_STABLE_MH_REF", "mass_or_charge"),
        ("IXS2022_11_Ix_abs", "I_X/M_H_ref", "absolute no-cancellation X obstruction envelope", "NOT_COMPUTED_COMPONENTS_MISSING", "dimensionless"),
        ("IXS2022_12_alphaX", "alpha_X(lambda_X)", "finite-range fallback if X is active and sourced", "MISSING_KX_QBAR_XH_QBAR_XT_BOUND", "dimensionless"),
    ]
    rows = []
    for row_id, symbol, definition, current_status, units in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "required_payload": "numeric_or_theorem_zero_value;units;source_path;assumptions;valid_for_claim",
                "current_status": current_status,
                "numeric_value": "MISSING",
                "units": units,
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def activation_gate_rows() -> list[dict[str, object]]:
    data = [
        ("XAG2022_0_absent_gauge_topological", "X is absent/gauge/topological in local branch", False, "parent normal form not selected"),
        ("XAG2022_1_positive_operator", "active X operator is positive with no physical zero mode", False, "Z_X/M_X^2/zero-mode certificate missing"),
        ("XAG2022_2_JX_zero", "all J_X source channels vanish", False, "matter, chiD, boundary, readout, history, and projection channels open"),
        ("XAG2022_3_boundary_zero", "boundary_X and improper edge charge vanish", False, "boundary/edge/reference certificate missing"),
        ("XAG2022_4_PiM_orthogonal", "X charge is orthogonal to measured M_H_ref", False, "Pi_M^H projection coefficient missing"),
        ("XAG2022_5_Ix_zero", "I_X/M_H_ref is theorem-zero", False, "requires all previous gates in one branch"),
        ("XAG2022_6_Ix_finite", "I_X/M_H_ref finite row is score-ready", False, "all numeric/source-backed values missing"),
    ]
    rows = []
    for gate_id, gate, passed_for_claim, reason in data:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "passed_for_nonclaim": True,
                "passed_for_claim": passed_for_claim,
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2022_0_X_zero", "claim X=0 or I_X=0 now", "REFUSE", "operator sign/gap, J_X=0, boundary zero and Pi_M projection are not signed together."),
        ("REF2022_1_absent_X_axiom", "declare X absent/gauge/topological without parent normal form", "REFUSE", "route selection must come from the parent action, not a closure axiom."),
        ("REF2022_2_score_Ix", "score I_X/M_H_ref", "REFUSE", "all numerator components and M_H_ref are missing source-backed values."),
        ("REF2022_3_score_alphaX", "score alpha_X(lambda_X)", "REFUSE", "Z_X, M_X^2, K_X, Qbar_XH, qbar_XT, tails, and real bound curve are not jointly present."),
        ("REF2022_4_cancel_components", "cancel J_X or I_X components against each other", "REFUSE", "the fallback must use absolute no-cancellation envelopes."),
        ("REF2022_5_local_GR", "claim local GR/Newton after this pass", "REFUSE", "I_X remains open, and Q_tau/M_H_ref/Pi_GRH are still nonclaim."),
    ]
    rows = []
    for refusal_id, attempted_claim, verdict, reason in data:
        row = base_row()
        row.update(
            {
                "refusal_id": refusal_id,
                "attempted_claim": attempted_claim,
                "verdict": verdict,
                "reason": reason,
                "accepted_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2022_0_result",
            "X_NOHAIR_IDENTITY_DERIVED_CONDITIONALLY_NOT_ACTIVATED",
            "The multiply-by-X energy identity gives a clean zero theorem if the parent X operator is positive and source/boundary/projection terms vanish.",
            "do not claim X=0; use the identity as the activation contract",
        ),
        (
            "DEC2022_1_fallback",
            "IX_SOURCE_ROW_SCHEMA_READY_NONCLAIM",
            "If the zero theorem fails, I_X/M_H_ref is now a concrete absolute envelope with source, boundary, symplectic and projection slots.",
            "fill or derive each slot with common units and source paths",
        ),
        (
            "DEC2022_2_best_next",
            "PARENT_X_NORMAL_FORM_OR_ZX_MX2_FIRST_ROW_NEXT",
            "The first missing upstream decision is whether X is absent/gauge/topological or an active positive field; without that, J_X details are downstream.",
            "select parent X normal form and sign Z_X/M_X^2 or stage first operator coefficient rows",
        ),
    ]
    rows = []
    for decision_id, verdict, rationale, next_action in data:
        row = base_row()
        row.update({"decision_id": decision_id, "verdict": verdict, "rationale": rationale, "next_action": next_action})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2022_0_2023",
            "next_doc": "2023-Y5-R2FR-parent-X-normal-form-or-ZX-MX2-first-row.md",
            "objective": "select the parent X-sector normal form: absent/gauge/topological, active positive operator, or sourced residual; if active, derive/source Z_X and M_X^2 with zero-mode rule",
            "required_inputs": "parent L_X normal form; field type; gauge/topological certificate; Z_X sign; M_X^2 sign/range; zero-mode rule; boundary convention; source path; units",
            "excluded": "declaring X absent by axiom; scoring I_X; scoring alpha_X; cancellation; orbital GM denominator; local-GR/R10/PPN claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update({"copy_id": f"COPY2022_{idx}", "path": str(path), "exists": path.exists(), "note": note})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    ix_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    root_resolved = ROOT.resolve()
    scoped_paths = output_paths + branch_paths + [DOC]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2022_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"))
    checks.append(("VAL2022_01_energy_identity", any(row["theorem_id"] == "XZT2022_2_energy_identity" and "int_D" in row["mathematical_form"] for row in theorem), "X energy identity is written"))
    checks.append(("VAL2022_02_zero_not_promoted", any(row["theorem_id"] == "XZT2022_7_verdict" and row["status"] == "X_SECTOR_ZERO_NOT_PROVED" for row in theorem), "X-sector zero theorem is not falsely promoted"))
    checks.append(("VAL2022_03_ix_bound_identity", any(row["theorem_id"] == "XZT2022_6_Ix_bound_identity" and "M_H_ref" in row["mathematical_form"] for row in theorem), "I_X finite-row bound identity is explicit"))
    checks.append(("VAL2022_04_ix_rows_nonclaim", all(row["score_ready"] is False and row["valid_for_claim"] is False and row["numeric_value"] == "MISSING" for row in ix_rows), "all I_X first-row slots remain missing/nonclaim"))
    checks.append(("VAL2022_05_gates_blocked", all(row["passed_for_claim"] is False for row in gates), "all activation gates remain blocked for claim"))
    checks.append(("VAL2022_06_refusals_active", all(row["verdict"] == "REFUSE" and row["accepted_for_claim"] is False for row in refusals), "refusals remain active"))
    checks.append(("VAL2022_07_no_absent_axiom", any(row["refusal_id"] == "REF2022_1_absent_X_axiom" for row in refusals), "absent-X closure axiom is refused"))
    checks.append(("VAL2022_08_next_target", any(row["target_id"] == "NEXT2022_0_2023" and "normal form" in row["objective"] for row in next_target), "2023 parent X normal-form target is selected"))
    checks.append(("VAL2022_09_decision_next", any(row["decision_id"] == "DEC2022_2_best_next" and ("ZX_MX2" in row["verdict"] or "Z_X" in row["next_action"]) for row in decisions), "decision selects Z_X/M_X^2 normal-form route"))
    checks.append(("VAL2022_10_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"))
    checks.append(("VAL2022_11_branch_copies", all(path.exists() and csv_rows_parse(path) for path in branch_paths), "branch-copy CSVs exist and parse"))
    checks.append(("VAL2022_12_no_formalization_edits", count_formalization_modified_since_start() == 0 and not formalization_has_2022_artifacts(), "formalization-workbench modified-file count remains 0 and no 2022 Ix artifacts appear there"))
    checks.append(("VAL2022_13_output_scope", all(root_resolved == path.resolve() or root_resolved in path.resolve().parents for path in scoped_paths), "all outputs are under post-checkpoint-work"))
    overall = all(passed for _, passed, _ in checks)
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    row = base_row()
    row.update({"check_id": "VAL2022_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "2022 Q_tau X-sector zero or first I_X source row"})
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    ix_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    parts = [
        "# 2022 Y5 R2FR: Qtau X-Sector Zero Or First Ix Source Row\n",
        "Private checkpoint. This pass tries the first real non-EH obstruction selected by 2021: can the local motion/time `X` sector be theorem-zeroed, or must it become a finite source row?\n",
        "## Current Verdict\n",
        "The clean zero route is now mathematically explicit: if the parent `X` sector is a positive local operator, `J_X=0`, boundary/zero-mode terms vanish, and `Pi_M^H` does not project `X` into measured mass, then the integrated energy identity forces `X=0`. In that case `Q_tau_X`, `C_tau_X`, and `I_X` vanish and the local `Q_tau` denominator can move closer to the GR/EH charge.\n",
        "But the route is not activated. The parent normal form for `X` is not selected, `Z_X/M_X^2` are not signed, `J_X` component silence is open, boundary tails are open, and `Pi_M^H` projection is open. So the fair result is not `X=0`; it is a sharp activation theorem plus a first honest `I_X/M_H_ref` source-row schema.\n",
        "This is still forward motion: the first non-EH obstruction is no longer vague. Either 2023 selects a parent `X` normal form and signs the positive-operator route, or `I_X` becomes a finite coefficient row for testing instead of being hidden inside the mass denominator.\n",
        "## Source Register\n",
        md_table(sources, ["source_id", "source_path", "status", "needles", "note"]),
        "## X-Sector Zero Theorem Attempt\n",
        md_table(theorem, ["theorem_id", "claim", "mathematical_form", "status", "missing_input", "consequence", "parent_signed", "theorem_zero"]),
        "## First I_X Source Row Schema\n",
        md_table(ix_rows, ["row_id", "symbol", "definition", "required_payload", "current_status", "numeric_value", "units", "score_ready", "valid_for_claim"]),
        "## Activation Gates\n",
        md_table(gates, ["gate_id", "gate", "passed_for_nonclaim", "passed_for_claim", "reason"]),
        "## Refusal Runner\n",
        md_table(refusals, ["refusal_id", "attempted_claim", "verdict", "reason", "accepted_for_claim"]),
        "## Decision Ledger\n",
        md_table(decisions, ["decision_id", "verdict", "rationale", "next_action"]),
        "## Branch Copies\n",
        md_table(branch_copies, ["copy_id", "path", "exists", "note"]),
        "## Next Target\n",
        md_table(next_target, ["target_id", "next_doc", "objective", "required_inputs", "excluded"]),
        "## Validation\n",
        md_table(validation, ["check_id", "status", "detail"]),
    ]
    DOC.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    theorem = x_zero_theorem_rows()
    ix_rows = ix_source_rows()
    gates = activation_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2022_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2022_X_SECTOR_ZERO_THEOREM_ATTEMPT.csv",
        "ix_rows": OUT / "P8_Y5_PARENT_QLOC_2022_IX_FIRST_SOURCE_ROW_SCHEMA.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2022_X_SECTOR_ACTIVATION_GATES.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2022_REFUSAL_RUNNER.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2022_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2022_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["theorem"], theorem)
    write_csv(output_map["ix_rows"], ix_rows)
    write_csv(output_map["gates"], gates)
    write_csv(output_map["refusals"], refusals)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_QTAU_X_ZERO_2022_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2022_IX_STATUS_NONCLAIM.csv",
        QUEUE / "JR2022_IX_FIRST_SOURCE_ROW_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["theorem"], branch_paths[0])
    shutil.copyfile(output_map["gates"], branch_paths[1])
    shutil.copyfile(output_map["ix_rows"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "Q_tau X-sector zero theorem nonclaim copy",
            "I_X activation gate status nonclaim copy",
            "I_X first source-row acquisition queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2022_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, theorem, ix_rows, gates, refusals, decisions, next_target, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2022_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, theorem, ix_rows, gates, refusals, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2022_OVERALL"][0]["status"]
    print(f"VAL2022_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
