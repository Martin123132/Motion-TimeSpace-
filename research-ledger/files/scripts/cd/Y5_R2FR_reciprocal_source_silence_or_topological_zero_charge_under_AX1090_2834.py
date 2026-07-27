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
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2834-Y5-R2FR-reciprocal-source-silence-or-topological-zero-charge-under-AX1090.md"

SRC_2833_NEXT = RESIDUALS / "P8_Y5_R2FR_2833_NEXT_TARGET.csv"
SRC_2833_PARENT = RESIDUALS / "P8_Y5_R2FR_2833_QRHAT_PARENT_ZERO_PROOF_AUDIT.csv"
SRC_2833_GAMMA = RESIDUALS / "P8_Y5_R2FR_2833_QRHAT_TO_GAMMA_INTERFACE_NONCLAIM.csv"
SRC_1884_MATRIX = RESIDUALS / "P8_Y5_PARENT_QLOC_1884_SOURCE_DESCENT_PREMISE_MATRIX.csv"
SRC_06_NEUTRALITY = ROOT / "06-reciprocal-charge-source-neutrality.md"
SRC_11_CURRENT = ROOT / "11-cell-current-origin-attempt.md"
SRC_12_NOETHER = ROOT / "12-gauge-noether-origin-audit.md"
SRC_1246_DOC = ROOT / "1246-Y5-R10-parent-QR-zero-theorem-or-finite-residual-source-hunt.md"
SRC_1256_DOC = ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md"
SRC_NO_SPECIES = RESIDUALS / "P8_no_species_source_charge_CONTRACT.csv"
SRC_SPECIES_RESIDUAL = RESIDUALS / "P8_species_source_charge_residual_or_zero.csv"
SRC_2250 = BETA_DOCS / "RAB_SOURCE_SIGNATURE_BODY_CHARGE_2250_NONCLAIM.csv"
SRC_2251 = BETA_DOCS / "RAB_SOURCE_SLOT_BRR_CRT_QR_2251_NONCLAIM.csv"
SRC_2261 = BETA_DOCS / "RAB_PARENT_PRIMITIVE_DERIVATION_AUDIT_2261_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2834_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2834_RECIPROCAL_SOURCE_SILENCE_THEOREM_ATTEMPT.csv",
    "matching": RESIDUALS / "P8_Y5_R2FR_2834_SOURCE_MATCHING_AND_PIR_LEDGER.csv",
    "topology": RESIDUALS / "P8_Y5_R2FR_2834_TOPOLOGICAL_ZERO_CHARGE_AUDIT.csv",
    "finite_rows": RESIDUALS / "P8_Y5_R2FR_2834_FINITE_QR_SOURCE_BODY_ACQUISITION_ROWS_NONCLAIM.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2834_SOURCE_SILENCE_GUARDS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2834_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2834_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2834_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2834_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2834_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "finite_copy": LOCAL_BOUNDS / "QR_body_PiR_finite_acquisition_rows_2834_NONCLAIM.csv",
    "theorem_copy": SOURCE_WEIGHT / "reciprocal_source_silence_theorem_attempt_2834_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2834_RAB_SOURCE_SLOT_EXCLUSION_OR_BODY_CHARGE_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    paths = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for path in paths:
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
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2834_0_2833_next", SRC_2833_NEXT, "NEXT2833_0_2834", "2833 selected reciprocal source silence/topological zero"),
        ("SRC2834_1_2833_parent", SRC_2833_PARENT, "PZ2833_3_source_silence;PZ2833_5_parent_zero_verdict", "2833 parent-zero audit isolates source silence"),
        ("SRC2834_2_2833_gamma", SRC_2833_GAMMA, "GI2833_0_parent_zero;GI2833_2_score_guard", "2833 gamma interface and full-vector guard"),
        ("SRC2834_3_1884_matrix", SRC_1884_MATRIX, "SDM1884_2_source_silence;SDM1884_3_matter_action_descent;SDM1884_4_measure_connection_descent", "1884 source-descent premise matrix"),
        ("SRC2834_4_06_neutrality", SRC_06_NEUTRALITY, "Q_R = -Pi_R;Pi_R = 0 -> Q_R = 0", "source matching formula and reciprocal neutrality condition"),
        ("SRC2834_5_11_current", SRC_11_CURRENT, "topological_zero_charge;Q_R = integral rho_R = 0", "current conservation failure and topological route name"),
        ("SRC2834_6_12_noether", SRC_12_NOETHER, "Noether identity derives R_AB=0;first-class parent constraint", "Noether slogan refusal"),
        ("SRC2834_7_1246", SRC_1246_DOC, "QZT1246_5_topological;FQH1246_1_topological_neutrality", "prior topological zero theorem audit"),
        ("SRC2834_8_1256", SRC_1256_DOC, "HC1256_0_minimal_density;BR1256_3_boundary_nohair;COEF1256_3_JR", "minimal H_core contract and boundary/source blockers"),
        ("SRC2834_9_no_species", SRC_NO_SPECIES, "S1_matter_factorization;S4_source_normalization_species_blind;S7_R1_empirical_fallback", "species/source-charge silence conditions"),
        ("SRC2834_10_species_residual", SRC_SPECIES_RESIDUAL, "SSC2675_0_definition;SSC2675_1_conditional_zero", "species source residual fallback"),
        ("SRC2834_11_2250", SRC_2250, "ACQ2250_2_QR_body;ACQ2250_3_PiR;ACQ2250_4_total", "RAB source signature body charge rows"),
        ("SRC2834_12_2251", SRC_2251, "ACQ2251_3_QR_body;ACQ2251_4_PiR;ACQ2251_6_total_abs", "RAB source-slot acquisition rows"),
        ("SRC2834_13_2261", SRC_2261, "CON2261_2_matter_functor;CON2261_3_boundary_functor", "primitive derivation audit for matter and boundary functors"),
    ]
    return [source_row(*spec) for spec in specs]


def theorem_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "TH2834_0_source_matching",
            "source matching identity",
            "For a source boundary, delta S_boundary=[W R_AB' + Pi_R] delta R_AB, so Q_R=-Pi_R.",
            "Q_R = -Pi_R;Pi_R = 0 -> Q_R = 0",
            "DERIVED_CONDITIONAL",
            "06 gives the matching identity, but Pi_R=0 is still a source/boundary theorem target.",
            "source silence reduces to proving Pi_R=0 or bounding Pi_R",
            True,
        ),
        (
            "TH2834_1_matter_functor_silence",
            "ordinary matter source silence",
            "If S_matter=Sbar[q(Phi),Psi,theta] and R_AB is vertical/basic-invisible to q and e_obs, then J_R=delta S_matter/delta R_AB=0.",
            "SDM1884_2_source_silence;CON2261_2_matter_functor;S1_matter_factorization",
            "CONDITIONAL_NOT_ACTIVATED",
            "Current corpus has not proved the actual R_AB direction is vertical before matter coupling.",
            "J_R remains finite/source-acquisition unless source-slot exclusion closes",
            False,
        ),
        (
            "TH2834_2_boundary_functor_silence",
            "boundary/source-worldtube silence",
            "If boundary/reference/source-worldtube data descend through quotient boundary variables only, then B_R/Pi_R/Q_R_body vanish.",
            "CON2261_3_boundary_functor;BR1256_3_boundary_nohair;BA1256_2_source_worldtube",
            "NOT_DERIVED",
            "No primitive boundary generator or exact source-worldtube neutrality proof is signed.",
            "Pi_R and Q_R_body stay in finite source-body vector",
            False,
        ),
        (
            "TH2834_3_topological_zero",
            "topological zero charge",
            "If Q_R is the integral of an exact/topological source density over allowed compact local source class and the class is neutral, then Q_R=0.",
            "topological_zero_charge;QZT1246_5_topological;FQH1246_1_topological_neutrality",
            "NAMED_NOT_DERIVED",
            "Missing source complex, boundary class, and proof allowed local sources are neutral.",
            "topological route remains live but unclaimed",
            False,
        ),
        (
            "TH2834_4_noether_rejected",
            "Noether/Ward shortcut refusal",
            "Noether identity or WEP/source universality cannot set Q_R=0 unless the parent action already contains the relevant constraint/source-silence equation.",
            "Noether identity derives R_AB=0;S4_source_normalization_species_blind",
            "SHORTCUT_REJECTED",
            "Ward identities conserve owned currents; they do not prove the reciprocal source current is absent.",
            "do not use slogans as source silence proof",
            True,
        ),
        (
            "TH2834_5_current_verdict",
            "reciprocal source silence theorem",
            "Current parent derives ordinary-source reciprocal silence and therefore Q_R=Pi_R=Q_R_body=0.",
            "PZ2833_3_source_silence;ACQ2251_3_QR_body;ACQ2251_4_PiR",
            "SOURCE_SILENCE_NOT_DERIVED",
            "Matter functor, boundary functor and topological neutral source class remain unsigned.",
            "keep finite QR_body/Pi_R/source-tail rows nonclaim",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "theorem_id": row_id,
                "target": target,
                "statement": statement,
                "source_anchors": anchors,
                "status": status,
                "proof_or_blocker": blocker,
                "effect_or_fallback": effect,
                "conditional_piece_proved": conditional,
                "theorem_zero_closed": False,
                "control_only": True,
            }
        )
        for row_id, target, statement, anchors, status, blocker, effect, conditional in specs
    ]


def matching_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SM2834_0_boundary_variation",
            "source boundary variation",
            "delta S_boundary=[W R_AB' + Pi_R] delta R_AB|surface",
            "Q_R=-Pi_R",
            "Pi_R=0 theorem or finite Pi_R bound",
            "06-reciprocal-charge-source-neutrality.md",
        ),
        (
            "SM2834_1_body_charge",
            "body/worldtube charge",
            "Q_R_body=int_body rho_R dV plus boundary/support terms",
            "Q_R_total=Q_R_body+Pi_R+tail_R in an absolute source vector",
            "body neutrality theorem or finite source-body integral",
            "RAB_SOURCE_SLOT_BRR_CRT_QR_2251_NONCLAIM.csv",
        ),
        (
            "SM2834_2_exterior_bridge",
            "exterior gamma bridge",
            "Q_R controls q_R_hat and delta_p via q_R_hat=Q_R c^2/(G M_source), delta_p=-q_R_hat/2",
            "delta_p=0 only if Q_R=0 or finite row is bounded",
            "same measured-GM convention and denominator/full-vector guards",
            "P8_Y5_R2FR_2833_QRHAT_TO_GAMMA_INTERFACE_NONCLAIM.csv",
        ),
        (
            "SM2834_3_absolute_source_vector",
            "no-cancellation source vector",
            "S_R_abs=|B_RR|+|C_RT|+|epsilon_RAB_source|+|Q_R_body|+|Pi_R|+|tail_R|",
            "all terms zero or bounded before local source silence",
            "common source normalization and arena projections",
            "RAB_SOURCE_SLOT_BRR_CRT_QR_2251_NONCLAIM.csv",
        ),
    ]
    return [
        nonclaim(
            {
                "matching_id": row_id,
                "object": obj,
                "source_relation": relation,
                "consequence": consequence,
                "missing_for_claim": missing,
                "source_reference": source_ref,
                "matching_ready": True,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for row_id, obj, relation, consequence, missing, source_ref in specs
    ]


def topology_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "TOPO2834_0_source_complex",
            "source complex",
            "define rho_R or source cochain such that Q_R=int rho_R or a boundary/topological pairing",
            "MISSING_SOURCE_COMPLEX",
            "topological_zero_charge is named but no source complex is built",
        ),
        (
            "TOPO2834_1_allowed_class",
            "allowed local source class",
            "prove compact ordinary local sources belong to a neutral class for the reciprocal charge",
            "MISSING_ALLOWED_NEUTRAL_CLASS",
            "body/source-worldtube rows remain open",
        ),
        (
            "TOPO2834_2_exactness",
            "exact/cohomological triviality",
            "show rho_R=deta_R with vanishing allowed boundary pairing, or show reciprocal class is absent",
            "MISSING_EXACTNESS_OR_COHOMOLOGY_ARGUMENT",
            "cannot infer zero from compactness or asymptotic flatness",
        ),
        (
            "TOPO2834_3_boundary_pairing",
            "boundary pairing",
            "show Pi_R and boundary/source support terms vanish or are exact constants that do not enter observables",
            "MISSING_PIR_ZERO_OR_BOUND",
            "boundary momentum can reappear as q_R_hat/gamma hair",
        ),
        (
            "TOPO2834_4_matter_compatibility",
            "matter/readout compatibility",
            "show the topological/source-zero proof is compatible with matter action descent and observed readout",
            "MISSING_MATTER_READOUT_DESCENT",
            "topological gamma closure alone would not be full local GR",
        ),
    ]
    return [
        nonclaim(
            {
                "topology_id": row_id,
                "clause": clause,
                "required_statement": statement,
                "current_status": status,
                "failure_if_missing": failure,
                "topological_zero_ready": False,
                "control_only": True,
            }
        )
        for row_id, clause, statement, status, failure in specs
    ]


def finite_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FQR2834_0_QR_body",
            "Q_R_body",
            "body/source-worldtube reciprocal charge",
            "|Q_R_body| <= int_body abs(W_R rho_R) dV + |Q_R_boundary|",
            "body model; W_R; rho_R; Green normalization; boundary term",
            "MISSING_BODY_NEUTRALITY_OR_NUMERIC_BODY_CHARGE",
            "R10;PPN;orbital;local_GR",
            "ACQ2251_3_QR_body",
        ),
        (
            "FQR2834_1_PiR",
            "Pi_R",
            "boundary reciprocal momentum/source support term",
            "|Pi_R| <= theorem_zero_or_source_backed_boundary_bound",
            "boundary/support/reference variation and physical matching rule",
            "MISSING_PIR_ZERO_OR_BOUND",
            "boundary;R10;PPN;orbital",
            "ACQ2251_4_PiR",
        ),
        (
            "FQR2834_2_JR",
            "J_R",
            "bulk reciprocal source current",
            "|J_R| or int_body abs(W_R rho_R) dV in declared normalization",
            "matter/source variation map; source slot owner; quotient-basicity status",
            "MISSING_JR_SOURCE_OR_ZERO",
            "R10;PPN;clock;WEP",
            "COEF1256_3_JR",
        ),
        (
            "FQR2834_3_tail",
            "tail_R",
            "readout/history/projector/counterterm source-tail vector",
            "|tail_R| <= |C_readout_R| + ||K_history_R|| + ||Delta_projector_R|| + |C_counterterm_R|",
            "variation-before-readout theorem or finite tail coefficient rows",
            "MISSING_TAIL_ZERO_OR_BOUNDS",
            "clock;orbital;PPN;local_GR",
            "ACQ2251_5_tail_source_vector",
        ),
        (
            "FQR2834_4_total_abs",
            "RAB_source_vector_abs",
            "absolute reciprocal source vector",
            "S_R_abs=|B_RR|+|C_RT|+|epsilon_RAB_source|+|Q_R_body|+|Pi_R|+|tail_R|",
            "all theorem-zero certificates or numeric/source-backed bounds in common units",
            "SCHEMA_READY_VALUES_MISSING",
            "all_local_arenas",
            "ACQ2251_6_total_abs",
        ),
    ]
    return [
        nonclaim(
            {
                "finite_row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "formula_or_bound": formula,
                "required_source": required,
                "current_status": status,
                "observable_link": arenas,
                "source_anchor": anchor,
                "theorem_zero": False,
                "numeric_value_present": False,
                "source_backed": False,
                "control_only": True,
            }
        )
        for row_id, symbol, definition, formula, required, status, arenas, anchor in specs
    ]


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("GUARD2834_0_conservation", "conservation is not neutrality", "W R_AB'=Q_R only makes Q_R constant", "Q_R=0 still needs source/boundary/topological theorem"),
        ("GUARD2834_1_noether", "Noether/Ward slogans are not source silence", "Noether identities relate equations and Ward conservation can keep nonzero charges", "must produce matter/source variation zero or finite row"),
        ("GUARD2834_2_topology", "topological zero requires a source complex", "naming topological_zero_charge is not a derivation", "needs rho_R/cochain, allowed source class and boundary pairing"),
        ("GUARD2834_3_absolute", "body, boundary and tail terms do not cancel by assumption", "RAB_source_vector_abs is an absolute envelope", "all components must be zero/bounded separately"),
        ("GUARD2834_4_local_gr", "source silence is not local GR by itself", "beta, d_R, endpoint/readout, q_loc and full PPN gates remain open", "no local-GR/Newton claim"),
    ]
    return [
        nonclaim(
            {
                "guard_id": guard_id,
                "guard": guard,
                "because": because,
                "effect": effect,
                "guard_active": True,
                "control_only": True,
            }
        )
        for guard_id, guard, because, effect in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    theorem_open = not any(row["theorem_zero_closed"] for row in rows["theorem"])
    matching_ready = all(row["matching_ready"] and not row["numeric_value_present"] for row in rows["matching"])
    topology_open = not any(row["topological_zero_ready"] for row in rows["topology"])
    finite_nonclaim = all(not row["theorem_zero"] and not row["numeric_value_present"] and not row["source_backed"] for row in rows["finite_rows"])
    guards_active = all(row["guard_active"] for row in rows["guards"])
    specs = [
        ("GATE2834_0_sources", "all 2834 source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "reproducible local audit trail"),
        ("GATE2834_1_source_silence", "ordinary-source reciprocal silence is derived", False, "BLOCKED", "matter functor, boundary functor and source complex are unsigned"),
        ("GATE2834_2_source_matching", "source matching identity is usable internally", matching_ready, "PASS_INTERNAL_NONCLAIM" if matching_ready else "BLOCKED", "Q_R=-Pi_R route is explicit but Pi_R zero is unproved"),
        ("GATE2834_3_topological_zero", "topological/source zero charge is derived", False, "BLOCKED", "source complex, neutral class and boundary pairing are missing"),
        ("GATE2834_4_finite_rows", "finite QR_body/Pi_R acquisition rows are staged", finite_nonclaim, "PASS_INTERNAL_NONCLAIM" if finite_nonclaim else "BLOCKED", "rows are source-ready but value-missing"),
        ("GATE2834_5_guards", "no conservation/Noether/topology/cancellation shortcut is accepted", guards_active, "PASS_GUARDRAIL" if guards_active else "BLOCKED", "guard rows remain active"),
        ("GATE2834_6_no_claim", "all theorem routes remain unclaimed", theorem_open and topology_open, "PASS_NONCLAIM" if theorem_open and topology_open else "BLOCKED", "no Q_R=0/local-GR claim promoted"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "reason": reason,
            }
        )
        for gate_id, claim, passed, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2834_0_matching", "The useful exact relation is Q_R=-Pi_R.", "SOURCE_MATCHING_ROUTE_LOCKED", "06 already supplies the boundary matching identity.", "try to prove Pi_R=0 or bound Pi_R/Q_R_body"),
        ("DEC2834_1_silence", "Source silence is not currently derived.", "THEOREM_OPEN", "matter functor and boundary functor are conditional and not activated for the actual R_AB direction.", "go after RAB source-slot exclusion normal form"),
        ("DEC2834_2_topology", "Topological zero remains possible but empty without a source complex.", "TOPOLOGY_NEEDS_OBJECT_LANGUAGE", "topological_zero_charge is named in 11/1246 but lacks rho_R/cochain, neutral class and boundary pairing.", "derive source complex or demote topology to finite source-body acquisition"),
        ("DEC2834_3_finite", "Finite source-body branch is now explicitly staged.", "FINITE_ROWS_READY_NONCLAIM", "Q_R_body, Pi_R, J_R and tail_R rows name required sources and arenas.", "do not score until values or theorem-zero certificates exist"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2834_0_2835",
                "status": "selected_primary",
                "target_doc": "2835-Y5-R2FR-RAB-source-slot-exclusion-normal-form-or-finite-body-charge-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_RAB_source_slot_exclusion_normal_form_or_finite_body_charge_under_AX1090_2835.py",
                "mission": "try to prove the R_AB source slot is absent from the parent matter/boundary normal form; if not, instantiate finite Q_R_body/Pi_R/J_R acquisition rows without scoring",
                "acceptance": "must cite 2834 source matching, 2251 source-vector rows and 2261 primitive derivation audit; no Q_R=0 claim unless matter and boundary functors are signed; no local-GR claim",
                "forbidden": "do not replace source-slot exclusion with WEP, Ward, Noether, or asymptotic-flatness slogans; do not cancel body and boundary charges by assumption",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2834_0_finite_copy", OUTPUTS["finite_rows"], BRANCH_OUTPUTS["finite_copy"], "local-bounds copy of finite QR_body/Pi_R source acquisition rows"),
        ("BR2834_1_theorem_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"], "source-weight copy of reciprocal source silence theorem attempt"),
        ("BR2834_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for source-slot exclusion normal form or finite body charge"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http") or item.startswith("MISSING_"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def no_numeric_prediction_insertions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_value", "predicted_value", "coefficient_value", "alpha_bound", "lambda_value"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in numeric_keys and str(value).strip():
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
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
        ("VAL2834_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2834_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2834_2_theorem_unclaimed", not any(row["theorem_zero_closed"] for row in rows_by_name["theorem"]), "source silence theorem remains unclaimed"),
        ("VAL2834_3_matching_ready_nonclaim", all(row["matching_ready"] and not row["numeric_value_present"] for row in rows_by_name["matching"]), "source matching ledger is symbolic/value-free"),
        ("VAL2834_4_topology_open", not any(row["topological_zero_ready"] for row in rows_by_name["topology"]), "topological zero route remains open"),
        ("VAL2834_5_finite_rows_nonclaim", all(not row["theorem_zero"] and not row["numeric_value_present"] and not row["source_backed"] for row in rows_by_name["finite_rows"]), "finite QR_body/Pi_R rows remain source-ready nonclaims"),
        ("VAL2834_6_guards_active", all(row["guard_active"] for row in rows_by_name["guards"]), "all source-silence shortcut guards are active"),
        ("VAL2834_7_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows Q_R=0, gamma, full PPN or local GR"),
        ("VAL2834_8_no_numeric_predictions", no_numeric_prediction_insertions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2834_9_next_target_2835", any(row["next_id"] == "NEXT2834_0_2835" and row["selected"] for row in rows_by_name["next"]), "RAB source-slot exclusion normal form selected next"),
        ("VAL2834_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2834_11_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2834_12_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2834_13_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2834_14_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim or claim_allowed flag is true"),
        ("VAL2834_15_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2834_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2834_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2834_OVERALL",
            "passed": overall,
            "detail": "2834 attempts reciprocal source silence/topological zero, records Q_R=-Pi_R as the useful matching identity, refuses to claim Pi_R=0/source neutrality, stages finite QR_body/Pi_R/J_R/tail rows, and selects RAB source-slot exclusion normal form next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2834 - Y5 R2FR Reciprocal Source Silence Or Topological Zero Charge Under AX1090

Status: `Y5_R2FR_2834_source_silence_not_derived_finite_source_vector_staged`

## Private Verdict

2834 finds the right hinge but does not close it.

The exact useful relation is:

```text
delta S_boundary = [W R_AB' + Pi_R] delta R_AB
Q_R = -Pi_R
```

So source silence is now precise: prove `Pi_R=0` and ordinary matter/body terms carry no reciprocal charge, or keep `Q_R_body`, `Pi_R`, `J_R`, and tail terms as finite source rows.

The current corpus does **not** derive this silence. Conservation gives constant `Q_R`; it does not set it to zero. Noether/Ward/WEP language does not replace the source variation. Topological zero remains possible, but only after a real source complex, neutral allowed source class, and boundary pairing are supplied.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Reciprocal Source Silence Theorem Attempt

{markdown_table(rows["theorem"], ["theorem_id", "target", "status", "proof_or_blocker", "effect_or_fallback", "conditional_piece_proved", "valid_for_claim"])}

## Source Matching And Pi_R Ledger

{markdown_table(rows["matching"], ["matching_id", "object", "source_relation", "consequence", "missing_for_claim", "matching_ready", "valid_for_claim"])}

## Topological Zero Charge Audit

{markdown_table(rows["topology"], ["topology_id", "clause", "required_statement", "current_status", "failure_if_missing", "topological_zero_ready", "valid_for_claim"])}

## Finite QR Source Body Acquisition Rows

{markdown_table(rows["finite_rows"], ["finite_row_id", "symbol", "definition", "formula_or_bound", "current_status", "observable_link", "numeric_value_present", "valid_for_claim"])}

## Source Silence Guards

{markdown_table(rows["guards"], ["guard_id", "guard", "because", "effect", "guard_active", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

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
    rows["theorem"] = theorem_rows()
    rows["matching"] = matching_rows()
    rows["topology"] = topology_rows()
    rows["finite_rows"] = finite_rows()
    rows["guards"] = guard_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "theorem", "matching", "topology", "finite_rows", "guards", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2834_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2834_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
