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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2850-Y5-R2FR-core-amplitude-parent-source-equation-hunt-or-manual-source-ledger-under-AX1090.md"

SRC_2849_DOC = ROOT / "2849-Y5-R2FR-core-amplitude-source-acquisition-or-parent-zero-owner-under-AX1090.md"
SRC_2849_SCAN = RESIDUALS / "P8_Y5_R2FR_2849_CORE_AMPLITUDE_SOURCE_SCAN.csv"
SRC_2849_PARENT_ZERO = RESIDUALS / "P8_Y5_R2FR_2849_PARENT_ZERO_OWNER_ATTEMPT.csv"
SRC_2849_SCHEMA = RESIDUALS / "P8_Y5_R2FR_2849_FINITE_ROW_ACCEPTANCE_SCHEMA.csv"
SRC_2849_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2849_VALIDATION.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_PACK = RESIDUALS / "P8_Y5_R2FR_2844_CAB_AMPLITUDE_SOURCE_PACK.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2844_CANCEL = RESIDUALS / "P8_Y5_R2FR_2844_CAB_CANCELLATION_THEOREM_ATTEMPT.csv"
SRC_1063 = ROOT / "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md"
SRC_1078 = ROOT / "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md"
SRC_509 = RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"
SRC_510 = RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"
SRC_1149 = ROOT / "1149-Y5-R10-source-normalization-owner-minimal-lemma-or-channel-bound-fallback.md"
SRC_1150 = ROOT / "1150-Y5-R10-Hilbert-worldtube-glue-or-PiM-equality-commutator-first-row.md"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2850_SOURCE_REGISTER.csv",
    "hunt": RESIDUALS / "P8_Y5_R2FR_2850_PARENT_EQUATION_HUNT_LEDGER.csv",
    "equation_scan": RESIDUALS / "P8_Y5_R2FR_2850_CANDIDATE_SOURCE_EQUATION_SCAN.csv",
    "acceptance": RESIDUALS / "P8_Y5_R2FR_2850_ACCEPTANCE_DECISION_MATRIX.csv",
    "manual": RESIDUALS / "P8_Y5_R2FR_2850_MANUAL_SOURCE_LEDGER.csv",
    "routes": RESIDUALS / "P8_Y5_R2FR_2850_DERIVATION_ROUTE_RANKING.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2850_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2850_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2850_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2850_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2850_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "hunt_copy": LOCAL_BOUNDS / "RAB_PARENT_SOURCE_EQUATION_HUNT_2850_NONCLAIM.csv",
    "manual_copy": SOURCE_WEIGHT / "RAB_CORE_AMPLITUDE_MANUAL_SOURCE_LEDGER_2850_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2850_minimal_parent_amplitude_owner_ansatz_NEXT.csv",
    "routes_copy": BETA_DOCS / "RAB_CORE_AMPLITUDE_ROUTE_RANKING_2850_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
            "control_only": True,
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2850_0_2849_doc", SRC_2849_DOC, "NEXT2849_0_2850;VAL2849_OVERALL", "2849 selected the parent source-equation hunt"),
        ("SRC2850_1_2849_scan", SRC_2849_SCAN, "SCAN2849_0_Q_CAB;SCAN2849_7_relation", "2849 core amplitude source scan"),
        ("SRC2850_2_2849_parent_zero", SRC_2849_PARENT_ZERO, "PZ2849_0_charge_balance_condition;PZ2849_6_verdict", "2849 parent zero-owner attempt"),
        ("SRC2850_3_2849_schema", SRC_2849_SCHEMA, "SCH2849_1_value;SCH2849_8_GM_convention", "2849 finite-row acceptance schema"),
        ("SRC2850_4_2849_validation", SRC_2849_VALIDATION, "VAL2849_OVERALL", "2849 validation"),
        ("SRC2850_5_2844_flux", SRC_2844_FLUX, "FLUX2844_5_local_suppression_condition;Q_CAB=-sigma_R*q_R_eff", "symbolic local suppression condition"),
        ("SRC2850_6_2844_pack", SRC_2844_PACK, "PACK2844_0_Q_CAB;PACK2844_4_q_R_eff", "Q_CAB and q_R_eff pack statuses"),
        ("SRC2850_7_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign;CONTRACT2844_6_measured_GM", "parent amplitude contract"),
        ("SRC2850_8_2844_cancel", SRC_2844_CANCEL, "CANCEL2844_1_parent_source_identity;CANCEL2844_5_verdict", "cancellation theorem attempt"),
        ("SRC2850_9_1063_owner", SRC_1063, "NO1063_2_Noether_current_owner;candidate_missing", "Noether/current owner missing"),
        ("SRC2850_10_1078_owner", SRC_1078, "CO1078_4_verdict;CURRENT_OWNER_NOT_SIGNED", "current-owner proof unsigned"),
        ("SRC2850_11_509_source_measure", SRC_509, "T509_0_charge_identity_needed;T509_2_no_extra_mass_channel", "measured-GM source-measure conditional theorem"),
        ("SRC2850_12_510_worldtube", SRC_510, "T510_1_worldtube_source_measure;T510_3_Newton_PPN_readout", "worldtube source-measure and Newton/PPN readout theorem"),
        ("SRC2850_13_1149_minimal", SRC_1149, "LEM1149_0_same_frame_current;LEM1149_6_worldtube_glue", "source-normalization minimal lemma"),
        ("SRC2850_14_1150_glue", SRC_1150, "GLUE1150_2_dressed_charge_guardrail;GLUE1150_9_verdict", "Hilbert/worldtube glue verdict"),
        ("SRC2850_15_2631_vector", SRC_2631, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only", "full PPN vector guard"),
    ]
    return [source_row(*spec) for spec in specs]


def hunt_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "HUNT2850_0_Q_CAB",
            "Q_CAB",
            "look for a parent target-map source equation and monopole charge definition",
            "definition-only candidate: Q_CAB=4*pi*A_CAB",
            SRC_2844_PACK,
            "PACK2844_0_Q_CAB",
            "FOUND_DEFINITION_ONLY_PARENT_EQUATION_MISSING",
            "needs L_CAB C_AB=J_CAB, Q_CAB=int J_CAB with boundary terms and Green normalization",
        ),
        (
            "HUNT2850_1_q_R_eff",
            "q_R_eff",
            "look for a parent delta_R Green equation and source normalization",
            "missing-source candidate: q_R_eff appears as finite Green charge but no source equation owns it",
            SRC_2844_PACK,
            "PACK2844_4_q_R_eff",
            "FOUND_SYMBOL_ONLY_PARENT_EQUATION_MISSING",
            "needs L_R delta_R=J_R, q_R_eff=int J_R in the same charge convention as Q_CAB",
        ),
        (
            "HUNT2850_2_sigma_R",
            "sigma_R",
            "look for parent action sign/operator convention",
            "contract marks sign convention missing",
            SRC_2844_CONTRACT,
            "CONTRACT2844_5_sign",
            "NO_ACCEPTED_PARENT_SIGN_EQUATION",
            "needs quadratic operator sign and Green convention from parent action",
        ),
        (
            "HUNT2850_3_measured_GM",
            "M_source/GM",
            "look for measured-GM/source-charge owner",
            "conditional source-charge machinery exists: T509/T510/1149/1150",
            SRC_510,
            "T510_1_worldtube_source_measure",
            "CONDITIONAL_EQUATIONS_FOUND_PREMISES_OPEN",
            "needs same charge to control metric 1/r coefficient before orbital fitting; extra channels bounded or zeroed",
        ),
        (
            "HUNT2850_4_relation",
            "Q_CAB=-sigma_R*q_R_eff",
            "look for parent identity that forces cancellation",
            "symbolic suppression relation exists but is not owned by a parent current",
            SRC_2844_FLUX,
            "FLUX2844_5_local_suppression_condition",
            "CONDITION_FOUND_OWNER_MISSING",
            "needs one current/source owner or symmetry deriving opposite projected charges",
        ),
        (
            "HUNT2850_5_current_owner",
            "single parent current owner",
            "look for a no-rescaling owner of source/current normalization",
            "1078 verdict is CURRENT_OWNER_NOT_SIGNED",
            SRC_1078,
            "CO1078_4_verdict",
            "OWNER_NOT_SIGNED",
            "needs parent object-language, variation-before-readout, and no independent current rescaling",
        ),
    ]
    return [
        nonclaim(
            {
                "hunt_id": hunt_id,
                "target_quantity": quantity,
                "hunt_question": question,
                "best_current_hit": hit,
                "source_path": str(path),
                "source_anchor": anchor,
                "hunt_status": status,
                "missing_to_accept": missing,
                "accepted_parent_equation_found": False,
                "accepted_finite_value_found": False,
                "control_only": True,
            }
        )
        for hunt_id, quantity, question, hit, path, anchor, status, missing in specs
    ]


def equation_scan_rows() -> list[dict[str, Any]]:
    specs = [
        ("EQSCAN2850_0_Q_CAB_definition", SRC_2844_PACK, "PACK2844_0_Q_CAB", "Q_CAB=4*pi*A_CAB", "definition/placeholder", "MISSING_PARENT_INPUT", "not accepted: no source-current equation"),
        ("EQSCAN2850_1_q_R_eff_symbol", SRC_2844_PACK, "PACK2844_4_q_R_eff", "q_R_eff", "symbolic charge slot", "MISSING_SOURCE_NORMALIZATION", "not accepted: source normalization absent"),
        ("EQSCAN2850_2_suppression_condition", SRC_2844_FLUX, "FLUX2844_5_local_suppression_condition", "Q_CAB=-sigma_R*q_R_eff", "exact symbolic condition", "DERIVED_SYMBOLIC_TARGET", "not accepted: condition is not parent-owned"),
        ("EQSCAN2850_3_cancel_verdict", SRC_2844_CANCEL, "CANCEL2844_5_verdict", "amplitude cancellation law", "conditional theorem", "CONDITION_DERIVED_PARENT_PROOF_MISSING", "not accepted: parent source identity missing"),
        ("EQSCAN2850_4_GM_charge_identity", SRC_509, "T509_0_charge_identity_needed", "M_eff[W]=M_source[W]=int_S Q_M[tau]=(4*pi*G_ref)^-1 int_S Pi_M J_H", "conditional measured-GM owner equation", "not_parent_derived", "useful candidate for GM only; not accepted yet"),
        ("EQSCAN2850_5_worldtube_measure", SRC_510, "T510_1_worldtube_source_measure", "M_source[W]:=H_tau[outer S]-H_tau[reference]", "definition correction/guardrail", "definition_not_yet_locked", "not accepted: guardrail not parent derivation"),
        ("EQSCAN2850_6_Newton_readout", SRC_510, "T510_3_Newton_PPN_readout", "g_00=-1+2G_ref M_source/r+O(r^-2)", "Newton/PPN readout target", "not_reached", "downstream after source-charge glue"),
        ("EQSCAN2850_7_current_owner", SRC_1078, "CO1078_4_verdict", "current-owner proof closes theorem-zero premise", "owner proof attempt", "CURRENT_OWNER_NOT_SIGNED", "not accepted: rescaling counterexample survives"),
        ("EQSCAN2850_8_full_vector_guard", SRC_2631, "RG2631_0_no_gamma_only", "gamma-only Cassini pass", "forbidden local-GR shortcut", "FORBIDDEN", "not an equation; active guardrail"),
    ]
    rows: list[dict[str, Any]] = []
    for scan_id, path, anchor, equation, role, status, verdict in specs:
        rows.append(
            nonclaim(
                {
                    "scan_id": scan_id,
                    "source_path": str(path),
                    "source_anchor": anchor,
                    "candidate_equation_or_rule": equation,
                    "role": role,
                    "current_status": status,
                    "verdict": verdict,
                    "accepted_for_core_pack": False,
                    "accepted_for_measured_GM_only": scan_id in {"EQSCAN2850_4_GM_charge_identity", "EQSCAN2850_5_worldtube_measure"} and False,
                    "control_only": True,
                }
            )
        )
    return rows


def acceptance_rows() -> list[dict[str, Any]]:
    specs = [
        ("ACC2850_0_Q_CAB", "Q_CAB", "source-backed parent equation or finite numeric row", "FAIL", "definition exists but parent source equation and boundary convention are missing"),
        ("ACC2850_1_q_R_eff", "q_R_eff", "source-backed parent equation or finite numeric row", "FAIL", "symbol exists but source normalization and Green convention are missing"),
        ("ACC2850_2_sigma_R", "sigma_R", "parent action sign/operator convention", "FAIL", "sign remains contract-only"),
        ("ACC2850_3_GM", "M_source/GM", "same parent charge controls measured GM and weak-field metric coefficient", "PARTIAL_CONDITIONAL_ONLY", "T509/T510/1149/1150 give useful route but premises are open"),
        ("ACC2850_4_relation", "Q_CAB=-sigma_R*q_R_eff", "parent current/source identity", "FAIL_AS_THEOREM", "exact condition known but not forced by parent owner"),
        ("ACC2850_5_first_row", "first local PPN row", "all core fields accepted together", "FAIL", "cannot score with any one row missing"),
    ]
    return [
        nonclaim(
            {
                "acceptance_id": acc_id,
                "item": item,
                "acceptance_requirement": requirement,
                "decision": decision,
                "reason": reason,
                "accepted": False,
                "control_only": True,
            }
        )
        for acc_id, item, requirement, decision, reason in specs
    ]


def manual_rows() -> list[dict[str, Any]]:
    specs = [
        ("MAN2850_0_parent_action_sector", "parent action/source sector", "write the local parent terms whose variations define C_AB, delta_R, the observed source current, and any multiplier/current that links them", "MISSING_PARENT_ACTION_OR_SECTION"),
        ("MAN2850_1_CAB_equation", "target-map equation", "supply L_CAB C_AB = J_CAB plus exterior Green convention, boundary terms, and Q_CAB=int J_CAB normalization", "MISSING_Q_CAB_SOURCE_EQUATION"),
        ("MAN2850_2_deltaR_equation", "delta_R equation", "supply L_R delta_R = J_R plus q_R_eff=int J_R and the exact charge convention shared with Q_CAB", "MISSING_q_R_eff_SOURCE_EQUATION"),
        ("MAN2850_3_sign_operator", "operator/sign owner", "derive sigma_R from the parent quadratic operator sign and the chosen Green kernel", "MISSING_SIGMA_R_PARENT_SIGN"),
        ("MAN2850_4_identity", "amplitude identity", "derive Q_CAB + sigma_R*q_R_eff = 0 from a conservation law, constraint, symmetry, or shared current before readout", "MISSING_SOURCE_CURRENT_IDENTITY"),
        ("MAN2850_5_boundary", "boundary and representative terms", "prove boundary/corner fluxes vanish or include them explicitly in the charge relation", "MISSING_BOUNDARY_FLUX_LAW"),
        ("MAN2850_6_GM_charge", "measured-GM source charge", "close the T509/T510 path: M_source[W] equals exterior parent charge and controls g_00 1/r coefficient", "MISSING_GM_PARENT_GLUE"),
        ("MAN2850_7_full_vector", "full local PPN vector", "supply theorem-zero or finite source-backed rows for beta, preferred-frame, source, endpoint, clock, orbital and q_loc channels", "MISSING_FULL_VECTOR_CLOSURE"),
    ]
    return [
        nonclaim(
            {
                "manual_id": manual_id,
                "required_source": required_source,
                "what_must_be_supplied": must_supply,
                "current_gap_code": gap_code,
                "ready_to_score_after_supplied": False,
                "control_only": True,
            }
        )
        for manual_id, required_source, must_supply, gap_code in specs
    ]


def route_rows() -> list[dict[str, Any]]:
    specs = [
        ("ROUTE2850_0_shared_parent_current", 1, "derive one parent current whose two projections give Q_CAB and -sigma_R*q_R_eff", "best_derivation_route", "least arbitrary if it follows from symmetry/conservation and kills rescaling"),
        ("ROUTE2850_1_variation_before_readout", 2, "tie the current owner to variation-before-readout and the measured-GM charge path", "needed_parallel_route", "prevents a fake local PPN pass from hiding in orbital GM calibration"),
        ("ROUTE2850_2_minimal_auxiliary_constraint", 3, "test whether a parent auxiliary field naturally imposes Q_CAB+sigma_R*q_R_eff=0", "dangerous_but_tryable", "acceptable only if the auxiliary field is motivated by parent symmetry, not inserted as a plateau axiom"),
        ("ROUTE2850_3_finite_amplitude_bound", 4, "fallback to finite source-backed Q_CAB/q_R_eff/sigma_R rows and compare against PPN bounds", "empirical_fallback", "testable but less foundational; should not be sold as derived local GR"),
        ("ROUTE2850_4_absorb_into_GM", 5, "hide the residual in measured GM", "forbidden", "would erase the Newton/GR derivation rather than prove it"),
    ]
    return [
        nonclaim(
            {
                "route_id": route_id,
                "rank": rank,
                "route": route,
                "status": status,
                "reason": reason,
                "selected_next": route_id == "ROUTE2850_0_shared_parent_current",
                "control_only": True,
            }
        )
        for route_id, rank, route, status, reason in specs
    ]


def claim_gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_control = all(row["path_exists"] and row["anchors_found"] for row in rows_by_name["sources"])
    specs = [
        ("CG2850_0_source_register", "source register valid", "PASS_CONTROL_ONLY" if source_control else "BLOCKED", "control source check only", source_control),
        ("CG2850_1_parent_equations", "accepted parent equations for Q_CAB/q_R_eff/sigma_R/GM", "BLOCKED", "hunt found conditional/placeholder rows, not accepted parent-owned equations", False),
        ("CG2850_2_finite_rows", "finite core amplitude rows accepted", "BLOCKED", "no numeric source-backed rows were introduced", False),
        ("CG2850_3_theorem_zero", "parent theorem-zero accepted", "BLOCKED", "Q_CAB=-sigma_R*q_R_eff remains condition, not owned theorem", False),
        ("CG2850_4_local_GR_Newton", "local GR/Newton reduction claimed", "BLOCKED", "source-normalized Newton and full PPN vector remain open", False),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "control_check_passed": control_passed,
                "gate_passed": False,
                "control_only": True,
            }
        )
        for gate_id, claim, status, reason, control_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2850_0_hunt_result", "Parent source-equation hunt found no accepted core amplitude owner.", "NO_ACCEPTED_PARENT_EQUATION", "Q_CAB/q_R_eff/sigma_R are still definition, symbol, and sign-contract slots"),
        ("DEC2850_1_GM_result", "Measured-GM has the strongest existing conditional route.", "PARTIAL_CONDITIONAL_ROUTE_EXISTS", "T509/T510/1149/1150 already describe the charge glue but do not close it"),
        ("DEC2850_2_manual_ledger", "Manual source ledger is now explicit.", "CREATED", "we now know exactly what a future parent action/source document must contain"),
        ("DEC2850_3_best_next", "Best next route is shared parent-current derivation.", "SELECT_2851", "this attacks the coupling/amplitude owner rather than patching finite rows"),
        ("DEC2850_4_no_claim", "No local-GR/Newton/PPN/R10 claim.", "LOCKED", "2850 is a hunt and ledger, not evidence"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "control_only": True,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2850_0_2851",
                "status": "selected_primary",
                "target_doc": "2851-Y5-R2FR-minimal-parent-amplitude-owner-ansatz-or-no-go-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_minimal_parent_amplitude_owner_ansatz_or_no_go_under_AX1090_2851.py",
                "mission": "attempt a non-smuggled parent-current/auxiliary-field mechanism that derives Q_CAB+sigma_R*q_R_eff=0 with fixed sign and source normalization; if it needs an inserted plateau axiom, reject it as closure-only",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2850_0_hunt", OUTPUTS["hunt"], BRANCH_OUTPUTS["hunt_copy"], "parent source-equation hunt nonclaim copy"),
        ("COPY2850_1_manual", OUTPUTS["manual"], BRANCH_OUTPUTS["manual_copy"], "manual source ledger nonclaim copy"),
        ("COPY2850_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2851"),
        ("COPY2850_3_routes", OUTPUTS["routes"], BRANCH_OUTPUTS["routes_copy"], "route ranking nonclaim copy"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(nonclaim({"copy_id": copy_id, "source_table": str(src), "copy_path": str(dst), "purpose": purpose, "exists": dst.exists(), "control_only": True}))
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if isinstance(value, str) and value:
                    path = Path(value)
                    if path.is_absolute():
                        paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "accepted",
        "accepted_parent_equation_found",
        "accepted_finite_value_found",
        "accepted_for_core_pack",
        "accepted_for_measured_GM_only",
        "ready_to_score_after_supplied",
        "gate_passed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if key in row and row[key] is True:
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_prediction", "prediction_value", "mts_prediction_value", "A_total_value", "delta_p_value", "q_R_hat_value", "Q_CAB_value", "q_R_eff_value", "sigma_R_value", "GM_value"}
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("numeric_prediction_present") is True or row.get("numeric_value_present") is True:
                return False
            for key in numeric_keys:
                value = row.get(key)
                if value not in (None, "", "MISSING"):
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2850_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2850_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2850_2_no_accepted_parent_equations", not any(row["accepted_parent_equation_found"] for row in rows_by_name["hunt"]), "no accepted parent equations were found for the core amplitude pack"),
        ("VAL2850_3_GM_conditional_route_recorded", any(row["hunt_id"] == "HUNT2850_3_measured_GM" and row["hunt_status"] == "CONDITIONAL_EQUATIONS_FOUND_PREMISES_OPEN" for row in rows_by_name["hunt"]), "measured-GM conditional route is recorded without claim"),
        ("VAL2850_4_manual_ledger_complete", len(rows_by_name["manual"]) >= 8, "manual source ledger names every required future input"),
        ("VAL2850_5_route_selected", any(row["route_id"] == "ROUTE2850_0_shared_parent_current" and row["selected_next"] for row in rows_by_name["routes"]), "shared parent-current route selected as next derivation target"),
        ("VAL2850_6_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2850_7_next_target_2851", any(row["next_id"] == "NEXT2850_0_2851" and row["selected"] for row in rows_by_name["next"]), "2851 minimal parent amplitude owner ansatz selected"),
        ("VAL2850_8_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2850_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2850_10_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2850_11_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2850_12_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2850_13_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no MTS numeric prediction rows inserted"),
        ("VAL2850_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2850_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2850_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2850_OVERALL",
            "passed": overall,
            "detail": "2850 performs the parent source-equation hunt, records GM as conditional-only, creates the manual source ledger, and selects a shared parent-current ansatz/no-go target for 2851.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2850 - Y5 R2FR Core Amplitude Parent Source-Equation Hunt Or Manual Source Ledger Under AX1090

Status: `Y5_R2FR_2850_parent_source_equation_hunt_no_core_owner_GM_conditional_route_nonclaim`

## Private Verdict

2850 did the parent-equation hunt that 2849 asked for. The result is sharp:

```text
Q_CAB: definition-only, no parent source equation yet.
q_R_eff: symbol/charge slot, no parent source normalization yet.
sigma_R: sign convention still not parent-owned.
measured GM: real conditional source-charge machinery exists, but its premises are open.
```

So the coupling/amplitude gap is now localized. The strongest positive thing in the current corpus is the measured-GM/source-charge chain (`T509/T510/1149/1150`). The weakest exposed wire is the `Q_CAB/q_R_eff/sigma_R` owner: there is a clean cancellation condition, but not yet the parent current that forces it.

The next best move is therefore not another empirical run. It is a minimal parent-current ansatz/no-go attempt: either derive `Q_CAB + sigma_R*q_R_eff = 0` from a genuine shared current/source owner, or reject that route as closure-only before it contaminates the theory.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Parent Equation Hunt Ledger

{markdown_table(rows["hunt"], ["hunt_id", "target_quantity", "hunt_status", "best_current_hit", "missing_to_accept", "accepted_parent_equation_found", "valid_for_claim"])}

## Candidate Source Equation Scan

{markdown_table(rows["equation_scan"], ["scan_id", "candidate_equation_or_rule", "role", "current_status", "verdict", "accepted_for_core_pack", "valid_for_claim"])}

## Acceptance Decision Matrix

{markdown_table(rows["acceptance"], ["acceptance_id", "item", "decision", "reason", "accepted", "valid_for_claim"])}

## Manual Source Ledger

{markdown_table(rows["manual"], ["manual_id", "required_source", "current_gap_code", "what_must_be_supplied", "valid_for_claim"])}

## Derivation Route Ranking

{markdown_table(rows["routes"], ["route_id", "rank", "route", "status", "reason", "selected_next", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["claim_gate_id", "claim", "status", "reason", "gate_passed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["hunt"] = hunt_rows()
    rows["equation_scan"] = equation_scan_rows()
    rows["acceptance"] = acceptance_rows()
    rows["manual"] = manual_rows()
    rows["routes"] = route_rows()
    rows["claim_gates"] = claim_gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "hunt", "equation_scan", "acceptance", "manual", "routes", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2850_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2850_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
