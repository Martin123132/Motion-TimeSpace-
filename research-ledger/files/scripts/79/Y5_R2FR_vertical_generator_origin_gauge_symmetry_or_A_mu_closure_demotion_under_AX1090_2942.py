from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2942"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2942-Y5-R2FR-vertical-generator-origin-gauge-symmetry-or-A-mu-closure-demotion-under-AX1090.md"

SRC_2941_DOC = ROOT / "2941-Y5-R2FR-Gamma-Khat-q_loc-action-existence-Helmholtz-or-parent-action-adoption-gate-under-AX1090.md"
SRC_2941_NEXT = RESIDUALS / "P8_Y5_R2FR_2941_NEXT_TARGET.csv"
SRC_2941_THEOREM = RESIDUALS / "P8_Y5_R2FR_2941_GK_ACTION_EXISTENCE_THEOREM_GATE.csv"
SRC_2941_ADOPTION = RESIDUALS / "P8_Y5_R2FR_2941_PARENT_ACTION_ADOPTION_GATE.csv"
SRC_2911_DOC = ROOT / "2911-Y5-R2FR-parent-field-chart-q-map-kernel-basis-or-finite-DqZ-norm-under-AX1090.md"
SRC_2911_CHART = RESIDUALS / "P8_Y5_R2FR_2911_PARENT_FIELD_CHART_ATTEMPT.csv"
SRC_2911_QMAP = RESIDUALS / "P8_Y5_R2FR_2911_Q_MAP_DERIVATIVE_AUDIT.csv"
SRC_2911_KERNEL = RESIDUALS / "P8_Y5_R2FR_2911_KERNEL_BASIS_ATTEMPT.csv"
SRC_2902_QV = RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_EXTRACTION_CONTRACT.csv"
SRC_2892_GEN = RESIDUALS / "P8_Y5_R2FR_2892_VERTICAL_GENERATOR_CONSTRUCTION_ATTEMPT.csv"
SRC_2913_GATE = RESIDUALS / "P8_Y5_R2FR_2913_ACTION_IMAGE_AND_GENERATOR_GATE.csv"
SRC_2465_VARIATION = RESIDUALS / "P8_Y5_PARENT_ACTION_2465_VARIATION_AUDIT.csv"
SRC_2465_SOURCE = RESIDUALS / "P8_Y5_PARENT_ACTION_2465_SOURCE_CURRENT_DESCENT.csv"
SRC_2465_DIMENSION = RESIDUALS / "P8_Y5_PARENT_ACTION_2465_DIMENSION_AUDIT.csv"
SRC_2465_REDTEAM = RESIDUALS / "P8_Y5_PARENT_ACTION_2465_TAUTOLOGY_RED_TEAM.csv"
SRC_2857_HUNT = RESIDUALS / "P8_Y5_R2FR_2857_EXISTING_GENERATOR_HUNT.csv"
SRC_2867_VGEN = RESIDUALS / "P8_Y5_R2FR_2867_VERTICAL_GENERATOR_DERIVATION_GATE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2942_SOURCE_REGISTER.csv",
    "origin": RESIDUALS / "P8_Y5_R2FR_2942_A_MU_VERTICAL_GENERATOR_ORIGIN_ATTEMPT.csv",
    "gauge": RESIDUALS / "P8_Y5_R2FR_2942_GAUGE_SYMMETRY_WARD_GATE.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2942_A_MU_PARENT_ADOPTION_CONTRACT.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_2942_SGK_CLOSURE_DEMOTION_LEDGER.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_2942_QLOC_FINITE_BOUND_HANDOFF.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2942_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2942_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2942_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2942_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2942_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "origin_copy": PARENT_ACTION / "A_mu_vertical_generator_origin_attempt_2942_NONCLAIM.csv",
    "contract_copy": PARENT_ACTION / "A_mu_parent_adoption_contract_2942_NONCLAIM.csv",
    "bound_handoff_copy": LOCAL_BOUNDS / "Qloc_finite_bound_handoff_2942_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2942_A_MU_WARD_OR_QLOC_BOUND_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2942_00_2941_doc", SRC_2941_DOC, "A_nu vertical-generator origin;Validation overall: `True`", "2941 handoff to A_mu origin"),
        ("SRC2942_01_2941_next", SRC_2941_NEXT, "NEXT2941_0_2942", "machine-readable 2942 target"),
        ("SRC2942_02_2941_theorem", SRC_2941_THEOREM, "GKT2941_0_weak_action_existence;GKT2941_3_strong_parent_action", "weak action pass and strong adoption fail"),
        ("SRC2942_03_2941_adoption", SRC_2941_ADOPTION, "AD2941_3_A_origin;AD2941_9_total_adoption", "A origin blocker"),
        ("SRC2942_04_2911_doc", SRC_2911_DOC, "v_Z in ker(Dq);PARENT_QMAP_NOT_SIGNED", "q-map/kernel ownership audit"),
        ("SRC2942_05_2911_chart", SRC_2911_CHART, "PFC2911_0_domain;PFC2911_6_verdict", "parent field chart attempt"),
        ("SRC2942_06_2911_qmap", SRC_2911_QMAP, "QMAP2911_0_projection_form;QMAP2911_7_verdict", "Dq derivative audit"),
        ("SRC2942_07_2911_kernel", SRC_2911_KERNEL, "KB2911_0_Zq;KB2911_8_verdict", "kernel basis attempt"),
        ("SRC2942_08_2902_qv", SRC_2902_QV, "VQC2902_1_vertical_generator;VQC2902_7_verdict", "vertical Qv extraction contract"),
        ("SRC2942_09_2892_gen", SRC_2892_GEN, "VGC2892_0_generator;VGC2892_5_verdict", "conditional vertical generator construction"),
        ("SRC2942_10_2913_action_image", SRC_2913_GATE, "AIG2913_1_generator_origin;AIG2913_5_current_verdict", "action image generator gate"),
        ("SRC2942_11_2465_variation", SRC_2465_VARIATION, "VAR2465_0_action_assumed;VAR2465_6_not_theorem", "ACT2464_A variation audit"),
        ("SRC2942_12_2465_source", SRC_2465_SOURCE, "SRC2465_1_vertical_generator;SRC2465_6_candidate_route", "source current/vertical generator source descent"),
        ("SRC2942_13_2465_dimension", SRC_2465_DIMENSION, "DIM2465_3_viable_branch;DIM2465_6_parent_scale_needed", "dimension branch and scale warning"),
        ("SRC2942_14_2465_redteam", SRC_2465_REDTEAM, "RED2465_0_not_multiplier;RED2465_5_claim_discipline", "tautology red-team"),
        ("SRC2942_15_2857_hunt", SRC_2857_HUNT, "HUNT2857_0_dcdagger_map;HUNT2857_5_component_map", "existing generator hunt"),
        ("SRC2942_16_2867_vgen", SRC_2867_VGEN, "VGEN2867_0_candidate;VGEN2867_6_verdict", "vertical generator derivation gate"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def origin_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "origin_id": "AMO2942_0_vertical_bundle_connection",
            "candidate_origin": "A_mu is a connection one-form on the vertical fibre of q:Conf_parent->Q_vis",
            "required_statement": "There is a vertical algebra V with generators R_a satisfying Dq[R_a Phi]=0, and A_mu=A_mu^a R_a enters only through parent covariant derivatives or a symmetry-derived current law.",
            "current_evidence": "q-map and kernel basis are candidate-only; A_mu is marked new material in the action skeleton.",
            "status": "FAIL_CURRENT_PROOF",
            "blocking_gap": "no parent field chart, regular kernel distribution, transformation law, or all-field vertical action is signed.",
            "adopt_A_mu": False,
        },
        {
            "origin_id": "AMO2942_1_DCDagger_Omega",
            "candidate_origin": "A_mu is the Omega-raised vertical generator sourced by a constraint/current variation",
            "required_statement": "A_mu or its field-space generator must be v_X=Omega^{-1}[(DC_X)^dagger X] with parent Omega, DC_X and boundary charge supplied.",
            "current_evidence": "existing generator hunt finds the formal map but parent Omega and field action are missing.",
            "status": "FORMAL_MAP_EXISTS_NOT_PARENT_OWNED",
            "blocking_gap": "Omega, DC, field-by-field vertical action and Q_v flux zero are missing.",
            "adopt_A_mu": False,
        },
        {
            "origin_id": "AMO2942_2_matter_gauge_current",
            "candidate_origin": "A_mu is a universal matter/source vertical gauge connection",
            "required_statement": "D_mu^A Psi=D_mu Psi+A_mu R_M Psi must be parent-specified, universal, WEP-safe, and yield J_M^nu=-delta S_matter/delta A_nu with a Ward identity.",
            "current_evidence": "2465 records this as candidate-only and missing.",
            "status": "CANDIDATE_ONLY",
            "blocking_gap": "R_M, universality, conservation, worldtube readout and external-vacuum support are missing.",
            "adopt_A_mu": False,
        },
        {
            "origin_id": "AMO2942_3_constraint_multiplier",
            "candidate_origin": "A_mu is a multiplier enforcing q current law",
            "required_statement": "A direct multiplier is acceptable only if the multiplier is forced by a gauge/constraint system already present in the parent action.",
            "current_evidence": "ACT2464_A is better than a direct multiplier because L_K supplies a conjugate Khat, but A_mu itself is still new.",
            "status": "DEMOTE_IF_USED_NOW",
            "blocking_gap": "without generator origin, the action remains closure in a nicer suit.",
            "adopt_A_mu": False,
        },
        {
            "origin_id": "AMO2942_4_verdict",
            "candidate_origin": "current MTS A_mu origin",
            "required_statement": "A_mu is promoted as actual MTS vertical/local generator.",
            "current_evidence": "all available origin routes are conditional or missing parent signatures.",
            "status": "A_MU_ORIGIN_NOT_DERIVED",
            "blocking_gap": "A_mu remains an excellent constructive extension variable, not a theorem-grade parent object.",
            "adopt_A_mu": False,
        },
    ]
    return [add_common(row) for row in rows]


def gauge_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "WARD2942_0_pure_gauge_requirement",
            "gate": "pure vertical gauge invariance",
            "math_test": "A_mu -> A_mu + nabla_mu epsilon is compatible with S_GK only if delta_epsilon S_GK = -int sqrt(-g) epsilon nabla_mu(nabla^mu Gamma_eff-J_M^mu) plus boundary vanishes as an off-shell identity or by a Stueckelberg transformation.",
            "finding": "current corpus has no off-shell Ward identity nabla_mu(nabla^mu Gamma_eff-J_M^mu)=0.",
            "gate_passed": False,
            "impact": "pure gauge origin is not proved.",
        },
        {
            "gate_id": "WARD2942_1_stueckelberg_rescue",
            "gate": "Gamma_eff transforms to rescue gauge invariance",
            "math_test": "A_mu and Gamma_eff may form a Stueckelberg pair only if Gamma_eff transformation and L_Gamma are parent-signed and remove the A_mu nabla^mu Gamma_eff gauge variation.",
            "finding": "no Gamma_eff transformation law or parent L_Gamma is signed.",
            "gate_passed": False,
            "impact": "Stueckelberg rescue remains a future derivation target.",
        },
        {
            "gate_id": "WARD2942_2_massive_auxiliary_branch",
            "gate": "A_mu is not gauge but a massive/auxiliary vertical field",
            "math_test": "If A_mu has L_K/L_Gamma gap terms, it can be a legitimate auxiliary/vector field, but then its stress, boundary flux and local tails are physical unless theorem-zero/bounded.",
            "finding": "allowed as an extension branch but not as vertical gauge proof.",
            "gate_passed": True,
            "impact": "keeps ACT2464_A as closure-only/nonclaim until stress/source/boundary rows close.",
        },
        {
            "gate_id": "WARD2942_3_source_current_ward",
            "gate": "J_M conservation and worldtube current",
            "math_test": "nabla_mu J_M^mu=0 or controlled exchange must follow from the same matter/gauge symmetry that defines A_mu.",
            "finding": "2465 source descent rows remain missing.",
            "gate_passed": False,
            "impact": "Newton/source bridge cannot be claimed.",
        },
        {
            "gate_id": "WARD2942_4_verdict",
            "gate": "current A_mu gauge-origin theorem",
            "math_test": "all Ward/gauge/source clauses pass with source paths.",
            "finding": "fails current corpus.",
            "gate_passed": False,
            "impact": "A_mu is demoted to closure-only unless 2943 derives the Ward/Stueckelberg identity.",
        },
    ]
    return [add_common(row) for row in rows]


def contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("CON2942_0_parent_chart", "Conf_parent and q", "parent action declares fields, q(Phi), Q_vis, Z/A sectors and readout order before variation", "MISSING", False),
        ("CON2942_1_vertical_algebra", "R_a in ker(Dq)", "Dq[R_a Phi]=0 on geometry, source, readout, boundary and support data", "MISSING", False),
        ("CON2942_2_A_connection", "A_mu=A_mu^a R_a", "A_mu has a transformation law and units fixed by parent geometry or gauge principle", "MISSING", False),
        ("CON2942_3_action_image", "L_K/L_Gamma", "kinetic/gap terms are forced by symmetry/positivity/minimality, not chosen to manufacture Khat", "MISSING", False),
        ("CON2942_4_Ward_identity", "gauge/source identity", "nabla_mu(nabla^mu Gamma_eff-J_M^mu)=0 off shell or Stueckelberg/exchange law is parent-derived", "MISSING", False),
        ("CON2942_5_matter_source", "J_M", "same matter action produces universal WEP-safe current and worldtube source charge", "MISSING", False),
        ("CON2942_6_projector_boundary", "P_loc/B_GK", "projector and boundary terms are parent-owned and cannot tune hidden components", "MISSING", False),
        ("CON2942_7_stress_silence", "T_GK", "A/Gamma/Khat stress vanishes, is second-order bounded, or is included consistently in the GR limit", "MISSING", False),
        ("CON2942_8_adoption", "A_mu as current MTS object", "all previous clauses pass", "FAIL_CURRENT_MTS", False),
    ]
    return [
        add_common(
            {
                "contract_id": contract_id,
                "object": obj,
                "required_clause": clause,
                "current_status": status,
                "clause_passed": passed,
            }
        )
        for contract_id, obj, clause, status, passed in rows
    ]


def demotion_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEM2942_0_SGK_status", "S_GK/ACT2464_A", "weak action template remains useful", "CLOSURE_ONLY_UNTIL_A_ORIGIN_WARD_SOURCE_SIGNED", "do not use for local-GR claim"),
        ("DEM2942_1_q_loc_status", "q_loc zero", "conditional law q_loc=P_loc J_M remains", "NOT_CURRENT_THEOREM", "retain finite residual"),
        ("DEM2942_2_A_mu_status", "A_mu", "not derived as vertical/gauge generator", "NEW_AUXILIARY_OR_CLOSURE_FIELD", "needs Ward/Stueckelberg rescue or demotion"),
        ("DEM2942_3_multiplier_guard", "direct multiplier reading", "would force the desired equation by design", "REJECT_AS_CLAIM_INPUT", "only revisit if symmetry-derived"),
        ("DEM2942_4_project_policy", "local GR/Newton/R10", "still blocked by parent-origin/source/stress/boundary gates", "NO_CLAIM", "next work must target identity or bound"),
    ]
    return [
        add_common(
            {
                "demotion_id": demotion_id,
                "object": obj,
                "reason": reason,
                "status": status,
                "policy": policy,
            }
        )
        for demotion_id, obj, reason, status, policy in rows
    ]


def bound_rows() -> list[dict[str, Any]]:
    rows = [
        ("QB2942_0_bulk_source", "||P_loc J_M||_collar", "needs J_M origin, support theorem, units and norm", "source-intake/matter-current", "blocks q_loc zero/F1"),
        ("QB2942_1_boundary_flux", "||B_GK|| or ||n_mu Khat^{mu nu}||_S", "needs boundary condition or source-backed flux bound", "source-intake/local_bounds", "blocks local vacuum law"),
        ("QB2942_2_projector_leak", "||delta P_loc|| and hidden components", "needs parent projector/action and frame lock", "source-intake/local_bounds", "blocks PPN/R10 projection"),
        ("QB2942_3_stress_tail", "||T_GK||, ||dT_GK||", "needs metric variation and stealth/double-zero branch", "source-intake/parent-action", "blocks local GR"),
        ("QB2942_4_symbol_mismatch", "||Khat_old - partial L_K/partial(nabla A)||", "needs symbol identity source paths", "source-intake/mts_residuals", "blocks adoption of old MTS symbols"),
        ("QB2942_5_denominator", "M_H_ref or source charge", "needs PiM/worldtube/H_ref noncircular denominator", "source-intake/parent-action", "blocks scoring"),
    ]
    return [
        add_common(
            {
                "bound_id": bound_id,
                "residual_component": component,
                "required_inputs": required,
                "queue": queue,
                "impact_if_missing": impact,
            }
        )
        for bound_id, component, required, queue, impact in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2942_0_A_origin", "A_mu is derived as current MTS vertical/local generator", False, "BLOCKED_PARENT_QMAP_GAUGE_WARD", False),
        ("CG2942_1_weak_SGK", "ACT2464_A remains useful as weak action template", True, "PASS_CONDITIONAL_NONCLAIM", False),
        ("CG2942_2_gauge_origin", "A_mu has gauge/vertical connection origin", False, "BLOCKED_WARD_STUECKELBERG_IDENTITY", False),
        ("CG2942_3_SGK_adoption", "S_GK promoted as accepted MTS parent sector", False, "DEMOTED_TO_CLOSURE_ONLY", False),
        ("CG2942_4_q_loc_zero", "q_loc=0/F1=0 claimed", False, "BLOCKED_SOURCE_BOUNDARY_STRESS", False),
        ("CG2942_5_Newton_GR", "Newton/local-GR branch derived", False, "BLOCKED_PARENT_ACTION_AND_SOURCE_MASS", False),
        ("CG2942_6_public_claim", "public empirical/local claim allowed from 2942", False, "NO_PUBLIC_CLAIM", False),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": allowed,
            }
        )
        for gate_id, claim, passed, status, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2942_0_result", "A_mu origin not derived", "vertical/gauge routes require q-map/kernel/Ward/source data that remain unsigned", "demote S_GK adoption to closure-only for now"),
        ("DEC2942_1_useful_gain", "the obstruction is now exact", "pure gauge A_mu requires a Ward/Stueckelberg identity for nabla_mu Gamma_eff-J_M", "try this identity once before pure finite-bound work"),
        ("DEC2942_2_no_multiplier_smuggling", "do not treat A_mu as direct multiplier evidence", "without origin it can impose the target current law by design", "keep nonclaim closure label"),
        ("DEC2942_3_bound_fallback", "q_loc finite bound inputs are staged", "if Ward identity fails, the honest path is residual bounds not claims", "prepare q_loc component bound runner"),
        ("DEC2942_4_source_parallel", "J_M/worldtube remains parallel bottleneck", "even A_mu origin cannot give Newton without source mass descent", "keep source bridge in next includes"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "next_action": next_action,
            }
        )
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2942_0_2943",
                "priority": "selected_primary",
                "next_doc": "2943-Y5-R2FR-A-mu-Ward-Stueckelberg-identity-or-q_loc-finite-bound-runner-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_A_mu_Ward_Stueckelberg_identity_or_q_loc_finite_bound_runner_under_AX1090_2943.py",
                "objective": "Attempt one rescue derivation: prove the Ward/Stueckelberg identity that makes A_mu a legitimate vertical/gauge connection for the Gamma_eff-J_M current. If it fails, start the q_loc finite residual bound runner using the 2942 handoff rows.",
                "include": "delta_epsilon S_GK; divergence identity; Gamma_eff transformation; J_M conservation/exchange; boundary variation; source support; q_loc bound components",
                "exclude": "local-GR/Newton/R10 claim; direct multiplier adoption; plateau axiom; fitted orbital GM; GitHub action; formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("origin_copy", OUTPUTS["origin"], BRANCH_OUTPUTS["origin_copy"]),
        ("contract_copy", OUTPUTS["contract"], BRANCH_OUTPUTS["contract_copy"]),
        ("bound_handoff_copy", OUTPUTS["bounds"], BRANCH_OUTPUTS["bound_handoff_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, copy_path in copies:
        if source_path.exists():
            shutil.copyfile(source_path, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "copy_path": str(copy_path),
                    "source_exists": source_path.exists(),
                    "copy_exists": copy_path.exists(),
                }
            )
        )
    return rows


def validation_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_has_2942 = False
    if FORMALIZATION.exists():
        formalization_has_2942 = any(FORMALIZATION.rglob("*2942*"))
    checks = [
        ("VAL2942_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2942_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2942_2_A_origin_refused", any(row.get("origin_id") == "AMO2942_4_verdict" and row.get("adopt_A_mu") == "False" for row in read_csv_rows(OUTPUTS["origin"])), "A_mu origin adoption refused", True),
        ("VAL2942_3_gauge_gate_failed", any(row.get("gate_id") == "WARD2942_4_verdict" and row.get("gate_passed") == "False" for row in read_csv_rows(OUTPUTS["gauge"])), "gauge-origin theorem fails current corpus", True),
        ("VAL2942_4_closure_demotion", any(row.get("demotion_id") == "DEM2942_0_SGK_status" for row in read_csv_rows(OUTPUTS["demotion"])), "S_GK closure demotion row exists", True),
        ("VAL2942_5_bound_handoff", any(row.get("bound_id") == "QB2942_0_bulk_source" for row in read_csv_rows(OUTPUTS["bounds"])), "q_loc finite-bound handoff rows exist", True),
        ("VAL2942_6_claims_blocked", all(row.get("claim_allowed") == "False" for row in read_csv_rows(OUTPUTS["claims"])), "no Newton/local-GR/R10 claim allowed", True),
        ("VAL2942_7_next_target_selected", any(row.get("next_id") == "NEXT2942_0_2943" for row in read_csv_rows(OUTPUTS["next"])), "2943 Ward/Stueckelberg or bound target selected", True),
        ("VAL2942_8_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        ("VAL2942_9_csvs_parse", all(csv_parses(path) for path in generated_csvs), "all generated CSV files parse", True),
        ("VAL2942_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2942_11_formalization_clean", not formalization_has_2942, "no 2942 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "check": check, "required": required} for validation_id, passed, check, required in checks]
    rows.append({"validation_id": "VAL2942_OVERALL", "passed": overall, "check": "2942 validation overall", "required": True})
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    origin: list[dict[str, Any]],
    gauge: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation if row["validation_id"] == "VAL2942_OVERALL")["passed"]
    text = f"""# 2942 - Y5 R2FR: vertical-generator origin gauge symmetry or A_mu closure demotion under AX1090

Status: `Y5_R2FR_2942_A_mu_origin_not_derived_SGK_demoted_to_closure_only_Ward_Stueckelberg_or_q_loc_bound_next`

Claim ceiling: `A_mu_origin_no_current_SGK_adoption_no_q_loc_zero_no_F1_zero_no_Newton_no_local_GR_no_R10_no_GitHub_claim`

2942 attacks the line between a derivation and a clever added vector field. The result is disciplined: `ACT2464_A` remains the best constructive template, but `A_mu` is not yet derived as the actual MTS vertical/local generator.

The clean obstruction is now explicit. If `A_mu` is supposed to be a vertical gauge connection with `A_mu -> A_mu + nabla_mu epsilon`, the linear current-law term requires

`delta_epsilon S_GK = -int sqrt(-g) epsilon nabla_mu(nabla^mu Gamma_eff - J_M^mu) + boundary = 0`.

So a real gauge origin needs an off-shell Ward identity, a Stueckelberg transformation for `Gamma_eff`, or a parent-derived exchange law for `J_M`. Current MTS has none of those signed. Therefore `S_GK` is kept as closure-only/nonclaim until that identity is derived; otherwise the honest fallback is a finite `q_loc` residual-bound runner.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## A_mu Vertical Generator Origin Attempt

{md_table(origin, ["origin_id", "candidate_origin", "required_statement", "status", "blocking_gap", "adopt_A_mu"])}

## Gauge Symmetry Ward Gate

{md_table(gauge, ["gate_id", "gate", "math_test", "finding", "gate_passed", "impact"])}

## A_mu Parent Adoption Contract

{md_table(contract, ["contract_id", "object", "required_clause", "current_status", "clause_passed"])}

## S_GK Closure Demotion Ledger

{md_table(demotion, ["demotion_id", "object", "reason", "status", "policy"])}

## q_loc Finite Bound Handoff

{md_table(bounds, ["bound_id", "residual_component", "required_inputs", "queue", "impact_if_missing"])}

## Claim Gates

{md_table(claims, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branches, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{overall}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    write_csv(OUTPUTS["sources"], source_rows)

    origin = origin_rows()
    gauge = gauge_rows()
    contract = contract_rows()
    demotion = demotion_rows()
    bounds = bound_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["origin"], origin)
    write_csv(OUTPUTS["gauge"], gauge)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["demotion"], demotion)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(source_rows)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(source_rows, origin, gauge, contract, demotion, bounds, claims, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL2942_OVERALL")["passed"]
    print(f"2942 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
