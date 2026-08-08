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
DOC = ROOT / "2024-Y5-R2FR-observed-representative-split-or-active-ZX-MX2-row.md"
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


def formalization_has_2024_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2024*representative*")) or any(FORMALIZATION.rglob("*2024*Dq*"))
    except Exception:
        return False


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2024_00_2023_handoff",
            ROOT / "2023-Y5-R2FR-parent-X-normal-form-or-ZX-MX2-first-row.md",
            ["NEXT2023_0_2024", "DEC2023_1_best_route", "XNF2023_3_EH_plus_quotient_extra"],
            "2023 handoff selects observed/representative split as best GR bridge.",
        ),
        (
            "SRC2024_01_1022_vertical",
            ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
            ["VQC1022_0_q_map", "VQC1022_2_matter_descent", "VQC1022_7_verdict"],
            "vertical quotient construction and no-pole theorem contract.",
        ),
        (
            "SRC2024_02_1737_qmap",
            OUT / "P8_Y5_PARENT_QLOC_1737_Q_MAP_CONTRACT.csv",
            ["QMAP1737_1_e_obs", "QMAP1737_5_Z_phi_RAB"],
            "Q map contract with observed geometry and candidate vertical directions.",
        ),
        (
            "SRC2024_03_1737_dq",
            OUT / "P8_Y5_PARENT_QLOC_1737_DQ_MATRIX_REQUIREMENTS.csv",
            ["DQM1737_0_DObs_e", "DQM1737_5_Dq_total_kernel"],
            "Dq matrix requirements for observed coframe and total kernel.",
        ),
        (
            "SRC2024_04_1737_coframe",
            OUT / "P8_Y5_PARENT_QLOC_1737_COFRAME_FUNCTOR_ZERO_ATTEMPT.csv",
            ["CFZ1737_0_exact_conditional", "CFZ1737_3_current_verdict"],
            "coframe functor zero theorem attempt.",
        ),
        (
            "SRC2024_05_1780_signature",
            OUT / "P8_Y5_PARENT_QLOC_1780_Q_DQ_TAU_SOURCE_FUNCTOR_SIGNATURE_GATE.csv",
            ["QTS1780_0_parent_q_map", "QTS1780_7_verdict"],
            "q/Dq/tau/source functor signature gate.",
        ),
        (
            "SRC2024_06_1786_hybrid",
            OUT / "P8_Y5_PARENT_QLOC_1786_HYBRID_EH_QUOTIENT_AUDIT.csv",
            ["HQA1786_0_EH_core", "HQA1786_5_verdict"],
            "hybrid EH-plus-quotient-extra selected nonclaim route.",
        ),
        (
            "SRC2024_07_1786_strict",
            OUT / "P8_Y5_PARENT_QLOC_1786_STRICT_QUOTIENT_ZERO_AUDIT.csv",
            ["SQA1786_0_q_candidate", "SQA1786_5_verdict"],
            "strict quotient-zero audit and failure to promote.",
        ),
        (
            "SRC2024_08_1787_split",
            OUT / "P8_Y5_PARENT_QLOC_1787_HYBRID_ACTION_SPLIT.csv",
            ["HAS1787_1_action", "HAS1787_5_verdict"],
            "hybrid action split machine-readable source.",
        ),
        (
            "SRC2024_09_1787_theorem",
            OUT / "P8_Y5_PARENT_QLOC_1787_CONDITIONAL_REDUCTION_THEOREM.csv",
            ["HCT1787_0_conditional_GR_reduction", "HCT1787_4_verdict"],
            "conditional GR/Newton reduction theorem.",
        ),
        (
            "SRC2024_10_1787_silence",
            OUT / "P8_Y5_PARENT_QLOC_1787_EXTRA_SECTOR_SILENCE_MATRIX.csv",
            ["ESM1787_5_bulk_X_memory", "ESM1787_7_matter_frame"],
            "extra-sector silence matrix.",
        ),
        (
            "SRC2024_11_2023_routes",
            OUT / "P8_Y5_PARENT_QLOC_2023_X_NORMAL_FORM_ROUTE_MATRIX.csv",
            ["XNF2023_3_EH_plus_quotient_extra", "XNF2023_4_active_positive_operator"],
            "2023 normal-form route matrix.",
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


def split_theorem_rows() -> list[dict[str, object]]:
    data = [
        (
            "ORS2024_0_field_split",
            "observed/representative field split",
            "Phi_parent=(e_obs,g_obs,Psi_m,theta_A; R_X,Phi_red,boundary,Pi_M,D,Gamma)",
            "SPLIT_CONTRACT_WRITTEN",
            "separates the GR-observed variables from representative/MTS extra variables",
            "parent action field chart and q/pi map are not signed",
        ),
        (
            "ORS2024_1_EH_core",
            "observed local EH core",
            "S_obs=S_EH[g_obs]+S_matter[Psi,e_obs,theta]+B_ref[g_obs,S]",
            "CONDITIONAL_EH_CORE_AVAILABLE",
            "provides the GR/Newton target if extra sectors are silent",
            "metric-only, second-order, common-source and reference clauses are unsigned",
        ),
        (
            "ORS2024_2_q_map",
            "quotient map to observed data",
            "q:Conf_parent -> Q_vis=(e_obs,g_obs,source/readout data,theta_owned), with X representative directions excluded",
            "Q_MAP_CANDIDATE_NOT_COMPUTABLE",
            "would make X representative rather than physical if its vertical basis is in ker(Dq)",
            "q is a contract, not derived from a parent variational reduction",
        ),
        (
            "ORS2024_3_Dq_vX_gobs_zero",
            "observed geometry invariant under X",
            "Dq[v_X]=0 and e_obs=E(q(Phi)) imply DObs_e[v_X]=DE_q(Dq[v_X])=0 and v_X[g_obs]=0",
            "EXACT_CHAIN_RULE_CONDITIONAL",
            "this is the cleanest theorem for preventing X from sourcing local GR geometry",
            "Dq[v_X], E(q), and field-by-field v_X are not parent-computable",
        ),
        (
            "ORS2024_4_representative_theta_exact",
            "representative-sector symplectic silence",
            "theta_rep(v_X)=dB_X or 0, Q_X proper/exact, and omega_rep(delta,v_X)=0 modulo fixed boundary class",
            "THETA_EXACTNESS_NOT_SIGNED",
            "would remove X from Q_tau/M_H_ref instead of fitting its coefficient",
            "boundary class, differentiable generator, and exact representative theta are open",
        ),
        (
            "ORS2024_5_matter_readout_descent",
            "ordinary matter and readout descend through observed variables",
            "S_m=sum_A S_A[Psi_A,e_obs,theta_A], Dsource_readout[Dq(v_X)]=0, and no shadow/source marker depends on X",
            "MATTER_READOUT_DESCENT_NOT_SIGNED",
            "would make qbar_XT=0 and prevent WEP/clock/orbit leakage",
            "hidden frames, material markers, source prefactors, and readout feedback remain open",
        ),
        (
            "ORS2024_6_extra_sector_filter",
            "hybrid extra-sector silence/bound filter",
            "DeltaE_extra_i in {0,gauge,topological_no_flux,positive_source_free_silent,retained_bound} and |Delta_local|<=sum_i|Delta_i|",
            "FILTER_EXACT_INPUTS_MISSING",
            "prevents smuggling non-EH sectors into the EH core",
            "R2/fR, connection, projector, boundary, source, matter-frame and bulk-X rows remain open",
        ),
        (
            "ORS2024_7_active_ZX_fallback",
            "active X coefficient fallback",
            "if v_X[g_obs] or theta_rep exactness fails, use active L_X with Z_X,M_X^2,J_X,boundary,Pi_M rows",
            "FALLBACK_SCHEMA_ONLY",
            "keeps empirical testing honest if X is physical",
            "Z_X/M_X^2/source/boundary/projection rows are missing",
        ),
        (
            "ORS2024_8_verdict",
            "observed/representative split currently proves local GR",
            "ORS2024_0 through ORS2024_6 close in one parent branch",
            "SPLIT_THEOREM_NOT_SIGNED",
            "the bridge theorem is now explicit and targets the right missing clauses",
            "q/Dq/g_obs invariance, theta exactness, boundary, matter/readout and residual filter are unsigned",
        ),
    ]
    rows = []
    for theorem_id, claim, mathematical_form, status, proof_value, missing_for_claim in data:
        row = base_row()
        row.update(
            {
                "theorem_id": theorem_id,
                "claim": claim,
                "mathematical_form": mathematical_form,
                "status": status,
                "proof_value": proof_value,
                "missing_for_claim": missing_for_claim,
                "parent_signed": False,
                "valid_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def certificate_rows() -> list[dict[str, object]]:
    data = [
        ("OSC2024_0_q_map", "q/pi map", "explicit parent quotient map and observed functor", "MISSING_Q_MAP"),
        ("OSC2024_1_vX_basis", "v_X field action", "field-by-field representative vertical generator", "MISSING_VERTICAL_BASIS"),
        ("OSC2024_2_Dq_kernel", "Dq[v_X]=0", "computed Dq matrix proves X direction is in kernel", "MISSING_DQ_KERNEL_CERTIFICATE"),
        ("OSC2024_3_gobs_invariance", "v_X[g_obs]=0", "observed coframe/metric invariant under representative direction", "MISSING_DOBS_E_ZERO"),
        ("OSC2024_4_theta_exact", "theta_rep(v_X)=dB_X or 0", "representative symplectic charge is exact/proper/fixed-boundary", "MISSING_REP_THETA_EXACTNESS"),
        ("OSC2024_5_boundary_class", "boundary/reference class", "no improper X edge charge and fixed B_ref/H_ref", "MISSING_BOUNDARY_CLASS"),
        ("OSC2024_6_matter_descent", "S_matter descends", "ordinary matter uses only e_obs/theta_owned with no X marker", "MISSING_MATTER_FUNCTOR_DESCENT"),
        ("OSC2024_7_readout_descent", "source/clock/orbit/readout descends", "readout is post-solution functor of Q_vis only", "MISSING_READOUT_FUNCTOR_DESCENT"),
        ("OSC2024_8_tau_lock", "tau projectability", "Dq(L_tau Phi)=L_tau_red q(Phi) and one tau across source/clock/orbit/charge", "MISSING_TAU_PROJECTABILITY"),
        ("OSC2024_9_residual_filter", "extra-sector residual filter", "all non-EH sectors theorem-zero or source-backed bounded", "MISSING_EXTRA_SECTOR_SILENCE"),
        ("OSC2024_10_active_fallback", "active Z_X/M_X^2 fallback", "if split fails, active operator rows exist with units/source paths", "MISSING_ACTIVE_COEFFICIENT_ROWS"),
    ]
    rows = []
    for row_id, certificate, definition, current_status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "certificate": certificate,
                "definition": definition,
                "required_payload": "theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim",
                "current_status": current_status,
                "numeric_value": "MISSING",
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2024_0_split_theorem_written", "observed/representative split theorem is explicit", True, "chain-rule bridge and required certificates are named"),
        ("CG2024_1_hybrid_route_retained", "EH-plus-quotient-extra remains active nonclaim route", True, "hybrid is best GR bridge but not promoted"),
        ("CG2024_2_q_map_signed", "q/pi map is parent-signed", False, "q is candidate-only"),
        ("CG2024_3_Dq_gobs_zero", "Dq[v_X]=0 and v_X[g_obs]=0 are signed", False, "Dq matrix and observed functor not computable"),
        ("CG2024_4_theta_boundary_exact", "representative theta and boundary charge are exact/proper", False, "boundary/generator exactness open"),
        ("CG2024_5_matter_readout_descends", "matter/readout sees only observed variables", False, "no-shadow/source/readout functor clauses open"),
        ("CG2024_6_extra_sector_silence", "all non-EH sectors zero/bounded", False, "silence matrix remains open"),
        ("CG2024_7_local_GR_Newton", "local GR/Newton reduction follows", False, "split certificates and Q_tau/M_H_ref gates remain open"),
    ]
    rows = []
    for gate_id, gate, passed_for_nonclaim, reason in data:
        row = base_row()
        row.update({"gate_id": gate_id, "gate": gate, "passed_for_nonclaim": passed_for_nonclaim, "passed_for_claim": False, "reason": reason})
        rows.append(row)
    return rows


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2024_0_projection_by_declaration", "put e_obs inside q by declaration and call X gauge", "REFUSE", "q and ker(Dq) must be derived from parent reduction, not declared."),
        ("REF2024_1_chain_rule_without_Dq", "use chain-rule zero without Dq[v_X]=0", "REFUSE", "DObs_e[v_X]=DE(Dq[v_X]) vanishes only after Dq[v_X] is signed."),
        ("REF2024_2_EH_core_as_full_theory", "treat EH core as full local theory", "REFUSE", "S_extra and residual silence matrix are still open."),
        ("REF2024_3_matter_blind_by_words", "assume ordinary matter/readout is blind to X", "REFUSE", "hidden frames, constants, source prefactors, and readout feedback need theorem or bounds."),
        ("REF2024_4_score_active_X", "score active X/Z_X/M_X^2 fallback now", "REFUSE", "active coefficient rows remain missing/nonclaim."),
        ("REF2024_5_local_GR", "claim local GR/Newton after 2024", "REFUSE", "bridge theorem is conditional and all major certificates remain unsigned."),
    ]
    rows = []
    for refusal_id, attempted_claim, verdict, reason in data:
        row = base_row()
        row.update({"refusal_id": refusal_id, "attempted_claim": attempted_claim, "verdict": verdict, "reason": reason, "accepted_for_claim": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2024_0_result",
            "OBS_REP_SPLIT_BRIDGE_WRITTEN_NOT_SIGNED",
            "The exact chain-rule route is now written: if q and Dq place v_X in the kernel and e_obs factors through q, then X cannot move the observed metric.",
            "do not claim local GR; attack Dq[v_X] and DObs_e[v_X] directly",
        ),
        (
            "DEC2024_1_best_next",
            "DQ_VX_GOBS_ZERO_IS_FIRST_CERTIFICATE",
            "Without Dq[v_X]=0 and v_X[g_obs]=0, the quotient/hybrid route cannot even start.",
            "build 2025 to prove Dq/v_X observed-metric zero or emit a finite DObs_e leak row",
        ),
        (
            "DEC2024_2_active_fallback",
            "ACTIVE_ZX_MX2_REMAINS_FALLBACK",
            "If observed/representative split fails, X returns as active residual and must be treated with Z_X/M_X^2/source/bound rows.",
            "keep active coefficient queue but do not prioritize it ahead of Dq/g_obs zero",
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
            "target_id": "NEXT2024_0_2025",
            "next_doc": "2025-Y5-R2FR-Dq-vX-observed-metric-zero-or-finite-DObs-leak-row.md",
            "objective": "prove Dq[v_X]=0 and v_X[g_obs]=0 for the observed/representative split, or emit a finite DObs_e/Dg_obs leak row with units and source paths",
            "required_inputs": "parent field chart; q/pi map; v_X action on all fields; Dq matrix; Obs_e(q) functor; norm for DObs_e leak; source path; boundary/matter assumptions",
            "excluded": "projection by declaration; chain-rule zero without Dq; local-GR claim; active X scoring; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update({"copy_id": f"COPY2024_{idx}", "path": str(path), "exists": path.exists(), "note": note})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    split: list[dict[str, object]],
    certs: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    root_resolved = ROOT.resolve()
    scoped_paths = output_paths + branch_paths + [DOC]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2024_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"))
    checks.append(("VAL2024_01_chain_rule", any(row["theorem_id"] == "ORS2024_3_Dq_vX_gobs_zero" and "DE_q" in row["mathematical_form"] for row in split), "chain-rule observed geometry zero is explicit"))
    checks.append(("VAL2024_02_split_not_promoted", any(row["theorem_id"] == "ORS2024_8_verdict" and row["status"] == "SPLIT_THEOREM_NOT_SIGNED" for row in split), "observed/representative split is not falsely promoted"))
    checks.append(("VAL2024_03_certificate_rows_nonclaim", all(row["score_ready"] is False and row["valid_for_claim"] is False and row["numeric_value"] == "MISSING" for row in certs), "all certificate/source rows remain missing/nonclaim"))
    checks.append(("VAL2024_04_claim_gates_blocked", all(row["passed_for_claim"] is False for row in claim_gates), "all claim gates remain blocked"))
    checks.append(("VAL2024_05_refusals_active", all(row["verdict"] == "REFUSE" and row["accepted_for_claim"] is False for row in refusals), "refusals remain active"))
    checks.append(("VAL2024_06_projection_refused", any(row["refusal_id"] == "REF2024_0_projection_by_declaration" for row in refusals), "projection-by-declaration shortcut is refused"))
    checks.append(("VAL2024_07_next_decision", any(row["decision_id"] == "DEC2024_1_best_next" and "DQ_VX_GOBS_ZERO" in row["verdict"] for row in decisions), "decision selects Dq/vX/g_obs zero next"))
    checks.append(("VAL2024_08_next_target", any(row["target_id"] == "NEXT2024_0_2025" and "Dq[v_X]" in row["objective"] for row in next_target), "2025 Dq/vX observed metric target is selected"))
    checks.append(("VAL2024_09_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"))
    checks.append(("VAL2024_10_branch_copies", all(path.exists() and csv_rows_parse(path) for path in branch_paths), "branch-copy CSVs exist and parse"))
    checks.append(("VAL2024_11_no_formalization_edits", count_formalization_modified_since_start() == 0 and not formalization_has_2024_artifacts(), "formalization-workbench modified-file count remains 0 and no 2024 split artifacts appear there"))
    checks.append(("VAL2024_12_output_scope", all(root_resolved == path.resolve() or root_resolved in path.resolve().parents for path in scoped_paths), "all outputs are under post-checkpoint-work"))
    overall = all(passed for _, passed, _ in checks)
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    row = base_row()
    row.update({"check_id": "VAL2024_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "2024 observed representative split or active Z_X M_X^2 row"})
    rows.append(row)
    return rows


def write_doc(sources, split, certs, claim_gates, refusals, decisions, branch_copies, next_target, validation) -> None:
    parts = [
        "# 2024 Y5 R2FR: Observed-Representative Split Or Active Z_X M_X^2 Row\n",
        "Private checkpoint. This pass writes the bridge theorem behind the hybrid route: local GR lives on `g_obs/e_obs`, while the MTS `X` direction must be quotient-vertical/exact or else become an active residual.\n",
        "## Current Verdict\n",
        "The observed/representative split is now precise but not signed. If a parent map `q` exists, `Dq[v_X]=0`, and `e_obs=E(q(Phi))`, then the chain rule gives `DObs_e[v_X]=0` and hence `v_X[g_obs]=0`. That is the clean way for MTS extra motion/time representatives to avoid sourcing the observed local GR metric.\n",
        "The missing bridge is concrete: compute the parent `q/pi` map, the field-by-field `v_X`, and the `Dq` matrix. Matter/readout descent, representative theta exactness, boundary class, tau lock, and extra-sector silence remain required before any local-GR/Newton claim. If the split fails, the active `Z_X/M_X^2` row remains the fallback.\n",
        "## Source Register\n",
        md_table(sources, ["source_id", "source_path", "status", "needles", "note"]),
        "## Observed/Representative Split Theorem\n",
        md_table(split, ["theorem_id", "claim", "mathematical_form", "status", "proof_value", "missing_for_claim", "parent_signed", "valid_for_claim"]),
        "## Certificate / Leak Rows\n",
        md_table(certs, ["row_id", "certificate", "definition", "required_payload", "current_status", "numeric_value", "score_ready", "valid_for_claim"]),
        "## Claim Gates\n",
        md_table(claim_gates, ["gate_id", "gate", "passed_for_nonclaim", "passed_for_claim", "reason"]),
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
    split = split_theorem_rows()
    certs = certificate_rows()
    claim_gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2024_SOURCE_REGISTER.csv",
        "split": OUT / "P8_Y5_PARENT_QLOC_2024_OBS_REP_SPLIT_THEOREM.csv",
        "certs": OUT / "P8_Y5_PARENT_QLOC_2024_OBS_REP_CERTIFICATE_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2024_CLAIM_GATE.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2024_REFUSAL_RUNNER.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2024_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2024_NEXT_TARGET.csv",
    }
    for rows_key, path in output_map.items():
        write_csv(path, locals()[rows_key])

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_OBS_REP_SPLIT_2024_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2024_OBS_REP_SPLIT_STATUS_NONCLAIM.csv",
        QUEUE / "JR2024_DQ_VX_GOBS_LEAK_ROW_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["split"], branch_paths[0])
    shutil.copyfile(output_map["claim_gates"], branch_paths[1])
    shutil.copyfile(output_map["certs"], branch_paths[2])

    branch_copies = branch_copy_rows(branch_paths, ["observed/representative split theorem nonclaim copy", "split claim-gate status nonclaim copy", "Dq/vX/g_obs leak row acquisition queue"])
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2024_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, split, certs, claim_gates, refusals, decisions, next_target, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2024_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, split, certs, claim_gates, refusals, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2024_OVERALL"][0]["status"]
    print(f"VAL2024_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
