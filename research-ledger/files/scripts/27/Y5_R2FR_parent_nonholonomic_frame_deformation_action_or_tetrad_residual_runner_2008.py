from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
DOC = ROOT / "2008-Y5-R2FR-parent-nonholonomic-frame-deformation-action-or-tetrad-residual-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "branch_id": BRANCH_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp(),
    }


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


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
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_rows_parse(path: Path) -> bool:
    try:
        read_csv(path)
    except csv.Error:
        return False
    return True


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2008_00_2007_handoff",
            "2007-Y5-R2FR-full-tetrad-completion-from-radial-seed-or-residual-interface.md",
            ["NEXT2007_0_2008", "NHC2007_0_candidate", "VAL2007_OVERALL"],
            "2007 selected A^a_MTS parent action/rank/gauge law or residual runner.",
        ),
        (
            "SRC2008_01_787_rank",
            "787-Y5-R10-multifield-pregeometry-rank-gate-or-independent-metric-branch-decision.md",
            ["MPR787_2_surjectivity_condition", "MPR787_3_internal_signature", "CIG787_1_nonholonomic_coframe"],
            "rank, signature, and nonholonomic escape from exact-gradient flatness.",
        ),
        (
            "SRC2008_02_788_nonholonomic",
            "788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md",
            ["NHC788_1_nonholonomic_ansatz", "PAC788_1_distortion_owned_contract", "NHC788_4_ownership_warning"],
            "nonholonomic coframe route, owned distortion contract, and ownership warning.",
        ),
        (
            "SRC2008_03_789_palatini",
            "789-Y5-R10-palatini-tetrad-GR-limit-with-MTS-exchange-contract.md",
            ["PTG789_1_action_form", "MIR789_4_matter_universality", "D789_1_no_local_GR_claim"],
            "Palatini/tetrad GR bridge and matter-universality gate.",
        ),
        (
            "SRC2008_04_790_residuals",
            "790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md",
            ["LSG790_0_Ward_compatible_split", "LSG790_6_matter_frame_universality", "D790_1_Q_first"],
            "local residual decomposition and Bianchi-compatible exchange gate.",
        ),
        (
            "SRC2008_05_791_q_loc",
            "791-Y5-R10-Ward-compatible-exchange-current-q-loc-zero-or-bound.md",
            ["ECT791_1_q_loc_geometric", "WZG791_3_geometric_q_loc_zero", "D791_1_q_loc_still_open"],
            "matter Ward split and geometric q_loc still-open warning.",
        ),
        (
            "SRC2008_06_1965_R2FR",
            "1965-Y5-R2FR-R2-fR-zero-proof-or-executable-R11-bound-row.md",
            ["ZP1965_3_minimality_route", "ZP1965_6_verdict", "EXR1965_1_mts_prediction"],
            "higher-curvature/EH-minimality residual remains unsigned.",
        ),
        (
            "SRC2008_07_1966_R2FR_smoke",
            "1966-Y5-R2FR-R2FR-bound-curve-and-parent-coefficient-smoke-runner.md",
            ["SMOKE1966_2_mts_coefficient", "DEC1966_0_verdict", "VAL1966_OVERALL"],
            "real-bound plumbing exists, but parent coefficients remain missing.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, relative_path, needles, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "2008 parent nonholonomic frame-deformation action or tetrad residual runner",
                "needles": ";".join(needles),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "note": note,
            }
        )
        rows.append(row)
    return rows


def aframe_action_attempt_rows() -> list[dict[str, object]]:
    specs = [
        (
            "AFF2008_0_field_content",
            "X^a, A^a_MTS, e^a=dX^a+A^a_MTS",
            "Treat X^a as clock/ruler Stueckelberg labels and A^a_MTS as a Lorentz-vector-valued frame-deformation one-form.",
            "KINEMATIC_CONTRACT_WRITTEN",
            "This escapes exact-gradient flatness because de^a=dA^a_MTS can be nonzero.",
            "false",
        ),
        (
            "AFF2008_1_translation_split_gauge",
            "X^a -> X^a+xi^a, A^a_MTS -> A^a_MTS-dxi^a",
            "The X/A split can be made unphysical if only e^a enters observables.",
            "GOOD_GAUGE_IDEA_BUT_NOT_OWNERSHIP",
            "This protects the split, but it means the physical variable is still e^a unless A^a is derived from parent MTS equations.",
            "false",
        ),
        (
            "AFF2008_2_local_Lorentz_law",
            "e^a -> Lambda^a_b(x)e^b",
            "A^a_MTS must transform so e^a is a genuine tetrad and matter sees no preferred representative.",
            "CONDITIONAL_GAUGE_RULE",
            "Matter representation and no-spurion theorem are not parent-signed.",
            "false",
        ),
        (
            "AFF2008_3_parent_action_candidate",
            "S = S_EH[e,omega] + S_A[A,X,Xi_MTS,e,omega] + S_matter[e,omega,Psi]",
            "A covariant action can be written formally, but S_A is not sourced by a derived MTS invariant algebra or coefficient hierarchy.",
            "FORMAL_ACTION_ONLY",
            "No parent L_A fixes coefficients, constraints, mass gap, or local suppression.",
            "false",
        ),
        (
            "AFF2008_4_variation_identity",
            "delta S/delta A^a_mu = delta S/delta e^a_mu when A enters only through e",
            "If A has no independent physical terms, varying A is just varying the tetrad.",
            "EQUIVALENT_TO_TETRAD_CLOSURE",
            "Clean for local GR, but not a derivation of tetrad from motion/time/space.",
            "false",
        ),
        (
            "AFF2008_5_kinetic_A_branch",
            "S_A contains F_A^a wedge *F_A_a or torsion-like kinetic terms",
            "A genuine kinetic A sector creates extra propagating or constrained modes unless killed by gauge/topological/no-mode theorem.",
            "EXTRA_MODE_RISK",
            "Needs mass gap, constraint, or pure-gauge proof plus PPN/clock/orbital/R10 bounds.",
            "false",
        ),
        (
            "AFF2008_6_determinant_constraint",
            "det(e)!=0 and Lorentzian signature",
            "A parent action must protect the nondegenerate Lorentzian domain rather than assuming it after the fact.",
            "MISSING_DOMAIN_ACTION",
            "No potential/constraint/rank theorem currently derives det(e) and signature stability.",
            "false",
        ),
        (
            "AFF2008_7_verdict",
            "A^a_MTS parent action",
            "The serious route is identified, but current corpus does not derive A^a_MTS from parent MTS variables.",
            "PARENT_ACTION_NOT_DERIVED",
            "Proceed as nonclaim: independent/effective tetrad closure or residual response runner.",
            "false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for action_id, object_text, attempt, status, blocker, parent_signed in specs:
        row = base_row()
        row.update(
            {
                "action_id": action_id,
                "object": object_text,
                "attempt": attempt,
                "status": status,
                "blocker": blocker,
                "parent_signed": parent_signed,
            }
        )
        rows.append(row)
    return rows


def gauge_rank_audit_rows() -> list[dict[str, object]]:
    specs = [
        (
            "GRK2008_0_exact_gradient_rank",
            "e^a=dX^a",
            "FAIL_REJECTED",
            "exact gradients are integrable and cannot represent generic local anholonomy/curvature",
            "false",
        ),
        (
            "GRK2008_1_A_full_component_rank",
            "A^a_mu as sixteen local components",
            "PASS_AS_INDEPENDENT_A_ONLY",
            "delta e^a_mu / delta A^b_nu = delta^a_b delta^nu_mu, so tetrad rank is available if A is independent",
            "false",
        ),
        (
            "GRK2008_2_parent_map_rank",
            "rank(delta A^a_mu / delta Phi_MTS)",
            "MISSING_PARENT_RANK_CERTIFICATE",
            "the corpus has no parent map from motion/time/space variables to a full-rank nonholonomic A^a_mu",
            "false",
        ),
        (
            "GRK2008_3_gauge_quotient",
            "local Lorentz + diffeomorphism + X/A split gauge",
            "CONDITIONAL_NOT_SIGNED",
            "gauge can prevent representative leakage only if matter and boundary terms depend on e, not X or A separately",
            "false",
        ),
        (
            "GRK2008_4_determinant_domain",
            "det(dX+A)!=0, signature=(-,+,+,+)",
            "MISSING_NONZERO_DOMAIN_PROOF",
            "formal rank does not guarantee the solution stays in a Lorentzian, oriented, time-oriented domain",
            "false",
        ),
        (
            "GRK2008_5_matter_functor",
            "S_matter[e,omega[e],Psi,owned gauge]",
            "CONDITIONAL_WARD_GATE",
            "if true, ordinary matter exchange Q_matter can vanish by Ward identity; if false, frame leakage returns",
            "false",
        ),
        (
            "GRK2008_6_EH_gate",
            "omega equation -> torsionless, e equation -> Einstein plus bounded residuals",
            "MISSING_EH_AND_RESIDUAL_SUPPRESSION",
            "Palatini/tetrad machinery gives the bridge only after A, S_MTS, boundary, and R11 residuals are silent or bounded",
            "false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for audit_id, gate, formal_rank, result, parent_rank_signed in specs:
        row = base_row()
        row.update(
            {
                "audit_id": audit_id,
                "gate": gate,
                "formal_rank": formal_rank,
                "result": result,
                "parent_rank_signed": parent_rank_signed,
            }
        )
        rows.append(row)
    return rows


def mode_risk_rows() -> list[dict[str, object]]:
    specs = [
        (
            "MODE2008_0_pure_tetrad_rewrite",
            "A enters only through e",
            "LOW_LOCAL_GR_RISK_HIGH_OWNERSHIP_RISK",
            "becomes ordinary tetrad closure; local GR path is clean but emergence claim weakens",
            "label as independent/effective tetrad unless parent map is derived",
        ),
        (
            "MODE2008_1_kinetic_translation_field",
            "F_A^2 or torsion-like A kinetic term",
            "HIGH_EXTRA_MODE_RISK",
            "adds vector/torsion-like local degrees that must be absent, massive, screened, or bounded",
            "derive no-extra-mode theorem or create PPN/clock/orbital/R10 rows",
        ),
        (
            "MODE2008_2_constraint_only_A",
            "lambda_A enforcing A=A[Phi_MTS] or determinant/rank constraints",
            "PROMISING_BUT_UNSIGNED",
            "could own the tetrad if the constraint follows from a parent variational principle",
            "derive constraint origin and prove constraint algebra closes",
        ),
        (
            "MODE2008_3_boundary_source_measure",
            "boundary/source terms depend on X or A separately",
            "FRAME_LEAK_RISK",
            "split-gauge breaks and matter/source readout can see an unphysical representative",
            "no-spurion boundary audit and bound rows",
        ),
        (
            "MODE2008_4_R2_R11_counterterms",
            "integrating out A/Xi_MTS generates R^2, f(R), or nonlocal operators",
            "EH_MINIMALITY_RISK",
            "local GR can be spoiled even if the tetrad exists",
            "zero theorem or executable scalar/R11 bound branch",
        ),
    ]
    rows: list[dict[str, object]] = []
    for mode_id, branch, risk_level, consequence, next_action in specs:
        row = base_row()
        row.update(
            {
                "mode_id": mode_id,
                "branch": branch,
                "risk_level": risk_level,
                "consequence": consequence,
                "next_action": next_action,
                "claim_status": "NONCLAIM_RISK_LEDGER",
            }
        )
        rows.append(row)
    return rows


def residual_runner_schema_rows() -> list[dict[str, object]]:
    specs = [
        (
            "RUN2008_0_transverse_frame",
            "epsilon_perp",
            "PPN light-bending; preferred-frame; orbital light-time",
            "project missing transverse tetrad legs into metric/light-cone residuals",
            "A^2_mu,A^3_mu source law; tetrad response Jacobian",
            "PPN/light-time bound vector",
        ),
        (
            "RUN2008_1_determinant_domain",
            "epsilon_det",
            "metric-domain validity",
            "measure distance to det(e)=0 or signature flip across local domain",
            "determinant lower bound from parent action or solution family",
            "domain stability criterion",
        ),
        (
            "RUN2008_2_common_frame",
            "b_g_or_c_g",
            "R10; PPN; clocks; WEP common-mode/source leg",
            "common Weyl/source-frame derivative of matter-visible tetrad",
            "parent zero or coefficient K_X,Qbar_XH,lambda_X",
            "R10/PPN/clock/WEP bounds",
        ),
        (
            "RUN2008_3_disformal_frame",
            "b_dis",
            "preferred-frame PPN; clock; orbital",
            "disformal/preferred-frame component of matter-visible tetrad",
            "projection of A/Xi_MTS onto local velocity or source direction",
            "alpha_1, alpha_2, clock anisotropy, orbital residual bounds",
        ),
        (
            "RUN2008_4_matter_functor",
            "epsilon_matter_frame",
            "WEP; clock; source normalization",
            "direct Phi_MTS, X, A, species, or readout dependence outside e",
            "parent-signed no-spurion matter action",
            "composition/WEP and clock universality bounds",
        ),
        (
            "RUN2008_5_connection",
            "epsilon_P4",
            "spin/precession; PPN; source-side GR",
            "independent connection/torsion/nonmetricity response if omega is not canonicalized",
            "delta_omega S_A and torsion source",
            "spin/precession/contact-force bounds",
        ),
        (
            "RUN2008_6_R11_operator",
            "Xi_R11",
            "Newton/Poisson; PPN gamma/beta; R10",
            "higher-curvature, scalaron, or nonlocal local-exterior operator",
            "R2/fR coefficient or zero theorem",
            "full alpha(lambda), PPN, and scalar range map",
        ),
        (
            "RUN2008_7_q_loc_exchange",
            "q_loc^nu",
            "PPN; orbital; matter conservation; clocks",
            "project P_loc(nabla Gamma_eff - div K_hat) into stress/force residuals",
            "Gamma_eff,K_hat equations or T_Q carrier response",
            "acceleration/PPN/orbital/clock residual bounds",
        ),
        (
            "RUN2008_8_total_envelope",
            "epsilon_Aframe_abs",
            "all local arenas",
            "absolute envelope over tetrad, frame, connection, q_loc, and R11 channels",
            "all component coefficients with units and source paths",
            "arena-specific pass/fail comparator",
        ),
    ]
    rows: list[dict[str, object]] = []
    for runner_id, symbol, arenas, projection_rule, required_parent_inputs, required_bound_inputs in specs:
        row = base_row()
        row.update(
            {
                "runner_id": runner_id,
                "symbol": symbol,
                "arenas": arenas,
                "projection_rule": projection_rule,
                "required_parent_inputs": required_parent_inputs,
                "required_bound_inputs": required_bound_inputs,
                "numeric_value": "MISSING",
                "units": "MISSING",
                "source_path": "MISSING_PARENT_INPUT_OR_BOUND",
                "status": "SCHEMA_ONLY_BLOCKED_NONCLAIM",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("CG2008_0_2007_handoff", "2007 nonholonomic target exists", "PASS_NONCLAIM", "A^a_MTS route is the selected serious route"),
        ("CG2008_1_exact_gradient_not_used", "exact-gradient tetrad not promoted", "PASS_REJECTION", "full GR is not smuggled through integrable scalar gradients"),
        ("CG2008_2_A_action_parent_signed", "A^a_MTS action derived from parent MTS variables", "FAIL_BLOCKED", "S_A, coefficients, constraints, and source map are not parent-derived"),
        ("CG2008_3_A_rank_parent_signed", "rank(delta A/delta Phi_MTS) gives full tetrad modulo gauges", "FAIL_BLOCKED", "formal rank only passes if A is independent"),
        ("CG2008_4_no_extra_modes", "A sector adds no local extra modes or bounded modes only", "FAIL_BLOCKED", "kinetic/constraint branch lacks no-mode theorem and bounds"),
        ("CG2008_5_matter_universality", "matter sees only e, omega[e], and owned gauge fields", "FAIL_BLOCKED", "no-spurion/no-representative-leak theorem still unsigned"),
        ("CG2008_6_residual_runner_score_ready", "local residual rows numeric and sourced", "FAIL_BLOCKED", "schemas exist but parent coefficients and bounds are missing"),
        ("CG2008_7_local_GR_Newton_claim", "local GR/Newton derived", "FAIL_BLOCKED", "tetrad ownership, EH minimality, q_loc, and residual suppression remain open"),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, gate, status, reason in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "status": status,
                "reason": reason,
                "passed_for_claim": "false",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2008_0_result",
            "A_FRAME_ACTION_NOT_PARENT_DERIVED_BUT_GATE_IS_NOW_EXACT",
            "The A^a_MTS route is not dead; it is the correct nonholonomic door. But without a parent S_A or source/rank theorem, it is an independent/effective tetrad closure, not a derived MTS tetrad.",
            "target the no-extra-mode/source-map theorem or use the residual runner schemas for local testing",
        ),
        (
            "DEC2008_1_actual_progress",
            "THE_LOOP_NARROWED_TO_A_CONCRETE_ACTION_OWNERSHIP_TEST",
            "We are no longer asking vaguely how to get GR; the test is whether A^a_MTS is pure gauge/constraint-owned or a real extra field with measurable residuals.",
            "do not keep re-auditing exact gradients; either prove A is harmless/owned or score its residuals",
        ),
        (
            "DEC2008_2_boxing_score",
            "MTS_STAYS_IN_THE_ROUND_NONCLAIM",
            "A tetrad/Palatini closure can still make MTS become GR locally, but the judges will not give the round until A ownership and residual silence are shown.",
            "next step should be a sharp no-extra-mode theorem attempt, then first numeric residual kernel if it fails",
        ),
    ]
    rows: list[dict[str, object]] = []
    for decision_id, verdict, rationale, next_action in specs:
        row = base_row()
        row.update(
            {
                "decision_id": decision_id,
                "verdict": verdict,
                "rationale": rationale,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2008_0_2009",
            "selected": "true",
            "next_doc": "2009-Y5-R2FR-Aframe-no-extra-mode-theorem-or-first-residual-response-kernel.md",
            "next_script": "scripts/Y5_R2FR_Aframe_no_extra_mode_theorem_or_first_residual_response_kernel_2009.py",
            "objective": "try to prove A^a_MTS is pure gauge/constraint-owned/no-extra-mode in the local GR domain; if not, instantiate the first numeric residual response kernel from the 2008 schema",
            "include": "translation split gauge; local Lorentz quotient; A constraint algebra; determinant domain; matter no-spurion theorem; q_loc/R11 residual handoff",
            "exclude": "another exact-gradient retry; unlabelled independent tetrad; local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2008_{idx}",
                "copy_path": str(path),
                "exists": str(path.exists()),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    action_rows: list[dict[str, object]],
    gauge_rows: list[dict[str, object]],
    mode_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks = [
        ("VAL2008_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"),
        ("VAL2008_01_A_action_attempted", any(row["action_id"] == "AFF2008_7_verdict" and row["status"] == "PARENT_ACTION_NOT_DERIVED" for row in action_rows), "A^a_MTS action derivation attempted and not falsely promoted"),
        ("VAL2008_02_formal_rank_labeled", any(row["formal_rank"] == "PASS_AS_INDEPENDENT_A_ONLY" for row in gauge_rows), "full A rank passes only as independent/effective A"),
        ("VAL2008_03_parent_rank_blocked", all(row["parent_rank_signed"] == "false" for row in gauge_rows), "no parent rank certificate is claimed"),
        ("VAL2008_04_mode_risks_nonclaim", all(row["claim_status"] == "NONCLAIM_RISK_LEDGER" for row in mode_rows), "mode risks are recorded as nonclaim"),
        ("VAL2008_05_residual_schema_blocked", all(row["numeric_value"] == "MISSING" and row["valid_for_claim"] == "false" for row in residual_rows), "residual runner rows remain schema-only until inputs exist"),
        ("VAL2008_06_claim_gates_blocked", all(row["passed_for_claim"] == "false" for row in claim_gates), "all claim gates remain blocked"),
        ("VAL2008_07_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2008_08_branch_copies", all(path.exists() for path in branch_paths), "branch-copy CSVs exist"),
        ("VAL2008_09_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"),
        ("VAL2008_10_output_scope", all(ROOT in [path, *path.parents] for path in [*output_paths, *branch_paths, DOC]), "all outputs are under post-checkpoint-work"),
    ]
    rows: list[dict[str, object]] = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = all(row["status"] == "PASS" for row in rows)
    row = base_row()
    row.update(
        {
            "check_id": "VAL2008_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2008 parent nonholonomic frame-deformation action or tetrad residual runner",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    action_rows: list[dict[str, object]],
    gauge_rows: list[dict[str, object]],
    mode_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 2008 Y5 R2FR: Parent Nonholonomic Frame-Deformation Action Or Tetrad Residual Runner

Private checkpoint. This tries the direct leap from the 2007 tetrad result: make the nonholonomic frame-deformation one-form `A^a_MTS` owned by the parent theory rather than quietly becoming an inserted tetrad.

## Current Verdict

The derivation attempt does **not** close. The useful structure is sharp: write `e^a=dX^a+A^a_MTS`, make the `X/A` split gauge, and let only the completed tetrad `e^a` enter ordinary matter. This avoids the exact-gradient flatness trap and gives a clean Palatini/tetrad route to local GR if every residual is silent.

But the parent action for `A^a_MTS` is not derived. If `A^a_MTS` enters only through `e^a`, then it is just an ordinary tetrad variable in disguise. If `A^a_MTS` has its own kinetic/constraint sector, it risks extra local modes unless a no-extra-mode theorem, mass gap, screening law, or residual bound is supplied.

So this is progress, but not a claim: the route is now reduced to one concrete gate. Either prove `A^a_MTS` is pure-gauge/constraint-owned/no-extra-mode in the local GR domain, or score the residual rows below.

No local-GR/Newton/WEP/R10 claim is promoted.

## Source Register
{md_table(sources, ["source_id", "source_path", "status", "needles", "note"])}

## A-Frame Action Attempt
{md_table(action_rows, ["action_id", "object", "status", "blocker", "parent_signed"])}

## Gauge And Rank Audit
{md_table(gauge_rows, ["audit_id", "gate", "formal_rank", "result", "parent_rank_signed"])}

## Mode Risk Ledger
{md_table(mode_rows, ["mode_id", "branch", "risk_level", "consequence", "next_action"])}

## Tetrad Residual Runner Schema
{md_table(residual_rows, ["runner_id", "symbol", "arenas", "projection_rule", "required_parent_inputs", "required_bound_inputs", "status"])}

## Claim Gates
{md_table(claim_gates, ["gate_id", "gate", "status", "reason", "passed_for_claim"])}

## Decision Ledger
{md_table(decisions, ["decision_id", "verdict", "rationale", "next_action"])}

## Branch Copies
{md_table(branch_copies, ["copy_id", "copy_path", "exists", "note"])}

## Next Target
{md_table(next_target, ["target_id", "next_doc", "objective", "include", "exclude"])}

## Validation
{md_table(validation, ["check_id", "status", "detail"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    action_rows = aframe_action_attempt_rows()
    gauge_rows = gauge_rank_audit_rows()
    mode_rows = mode_risk_rows()
    residual_rows = residual_runner_schema_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2008_SOURCE_REGISTER.csv",
        "actions": OUT / "P8_Y5_PARENT_QLOC_2008_AFRAME_ACTION_ATTEMPT.csv",
        "gauge_rank": OUT / "P8_Y5_PARENT_QLOC_2008_GAUGE_RANK_AUDIT.csv",
        "mode_risk": OUT / "P8_Y5_PARENT_QLOC_2008_MODE_RISK_LEDGER.csv",
        "residual_schema": OUT / "P8_Y5_PARENT_QLOC_2008_TETRAD_RESIDUAL_RUNNER_SCHEMA.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2008_CLAIM_GATE.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2008_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2008_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["actions"], action_rows)
    write_csv(output_map["gauge_rank"], gauge_rows)
    write_csv(output_map["mode_risk"], mode_rows)
    write_csv(output_map["residual_schema"], residual_rows)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "NONHOLONOMIC_AFRAME_ACTION_2008_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2008_AFRAME_STATUS_NONCLAIM.csv",
        QUEUE / "JR2008_TETRAD_RESIDUAL_RUNNER_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["actions"], branch_paths[0])
    shutil.copyfile(output_map["gauge_rank"], branch_paths[1])
    shutil.copyfile(output_map["residual_schema"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame action attempt nonclaim copy",
            "A-frame gauge/rank status nonclaim copy",
            "tetrad residual runner schema queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2008_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(
        sources,
        action_rows,
        gauge_rows,
        mode_rows,
        residual_rows,
        claim_gates,
        output_paths,
        branch_paths,
    )
    validation_path = OUT / "P8_Y5_BRR545_2008_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(
        sources,
        action_rows,
        gauge_rows,
        mode_rows,
        residual_rows,
        claim_gates,
        decisions,
        branch_copies,
        next_target,
        validation,
    )
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2008_OVERALL"][0]["status"]
    print(f"VAL2008_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
