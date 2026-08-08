from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2686"
BRANCH_ID = "Y5_R2FR_PARENT_ACTION_ADMISSIBILITY_FROM_Q_DESCENT_OR_DELTA_W_FIRST_ROW_2686"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"

DOC_PATH = ROOT / "2686-Y5-R2FR-parent-action-admissibility-from-q-descent-or-delta-w-first-row.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2686_SOURCE_REGISTER.csv",
    "q_descent_audit": RESIDUALS / "P8_Y5_R2FR_2686_Q_DESCENT_ADMISSIBILITY_AUDIT.csv",
    "derivation_result": RESIDUALS / "P8_Y5_R2FR_2686_ADMISSIBILITY_DERIVATION_RESULT.csv",
    "sort_nohom_requirements": RESIDUALS / "P8_Y5_R2FR_2686_SORT_DISJOINTNESS_NOHOM_REQUIREMENTS_NONCLAIM.csv",
    "delta_w_first_row": RESIDUALS / "P8_Y5_R2FR_2686_DELTA_W_FIRST_ROW_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2686_ADMISSIBILITY_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2686_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2686_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2686_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2686_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2686_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_admissibility_audit": LOCAL_BOUNDS / "q_descent_admissibility_audit_2686_NONCLAIM.csv",
    "local_nohom_requirements": LOCAL_BOUNDS / "sort_disjointness_nohom_requirements_2686_NONCLAIM.csv",
    "local_delta_w_first_row": LOCAL_BOUNDS / "delta_w_first_row_2686_NONCLAIM.csv",
    "wep_nohom_requirements": WEP_COEFF / "sort_disjointness_nohom_requirements_2686_NONCLAIM.csv",
    "source_weight_delta_w_first_row": SOURCE_WEIGHT / "DELTA_W_FIRST_ROW_2686_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2686_2685_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2685_NEXT_TARGET.csv",
        "required_needles": ["NEXT2685_0_selected", "admissible parent action argument list", "adopting object-language admissibility as an axiom"],
        "purpose": "confirms selected q-descent/admissibility target",
    },
    {
        "source_id": "SRC2686_2685_ZERO",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2685_PARENT_SOURCE_PREFACTOR_ZERO_THEOREM_CONTRACT_NONCLAIM.csv",
        "required_needles": ["ZTC2685_0_parent_action_domain", "ROOT_OBJECT_LANGUAGE_ADMISSIBILITY_NOT_DERIVED", "ZTC2685_7_verdict"],
        "purpose": "imports root admissibility debt",
    },
    {
        "source_id": "SRC2686_1895_ATTEMPT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1895_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv",
        "required_needles": ["NSP1895_1_exact_if_typed", "PARENT_TYPED_OBJECT_LANGUAGE_NOT_DERIVED", "NSP1895_5_verdict"],
        "purpose": "imports no-source-prefactor object-language attempt",
    },
    {
        "source_id": "SRC2686_1220_TYPED",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
        "required_needles": ["PTOL1220_0_parent_domain", "PTOL1220_3_source_weight_exclusion", "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED"],
        "purpose": "imports parent typed signature status",
    },
    {
        "source_id": "SRC2686_1236_CERT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
        "required_needles": ["CERT1236_0_parent_sorts", "CERT1236_5_source_label_forgetting", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"],
        "purpose": "imports sort certificate attempt",
    },
    {
        "source_id": "SRC2686_1045_FUNCTOR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "required_needles": ["MFS1045_0_parent_field_quotient", "MFS1045_2_matter_bundle_functor", "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED"],
        "purpose": "imports q-descent and matter functor status",
    },
    {
        "source_id": "SRC2686_1045_LIFT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv",
        "required_needles": ["VLG1045_0_fixed_lift", "VLG1045_2_physical_lift_forbidden", "FAIL_CURRENT_CLAIM_VERTICAL_LIFT_NOT_SIGNED"],
        "purpose": "imports vertical lift status",
    },
    {
        "source_id": "SRC2686_1055_ACTION",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
        "required_needles": ["PAC1055_0_configuration_and_quotient", "PAC1055_4_source_label_forgetting", "PAC1055_6_single_parent_action"],
        "purpose": "imports parent action contract candidate",
    },
    {
        "source_id": "SRC2686_1066_SCALAR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
        "required_needles": ["SSE1066_1_object_language_route", "SSE1066_4_quantum_action_scale_obstruction", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED"],
        "purpose": "imports source-scalar exclusion status",
    },
    {
        "source_id": "SRC2686_1090_SYNTHESIS",
        "relative_path": "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md",
        "required_needles": ["SYN1090_8_verdict", "SYNTHESIS_FAILS_MISSING_AXIOMS", "AX1090_1_no_hidden_visible_hom"],
        "purpose": "imports synthesis failure and missing no-Hom axiom",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def q_descent_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "QDA2686_0_q_vertical_blindness",
            "claim_piece": "q-descent makes observed geometry blind to vertical representative motion",
            "derivation_test": "Dq[v_X]=0 implies DObs_e[Dq[v_X]]=0 for e_obs(q(Phi)) and g_obs",
            "result": "EXACT_CONDITIONAL_GEOMETRY_LEMMA",
            "what_it_buys": "no direct vertical variation of observed coframe/metric terms",
            "what_it_does_not_buy": "does not classify action coefficient targets or species/source labels",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "QDA2686_1_matter_pullback",
            "claim_piece": "ordinary matter can be pulled back through observed coframe and fixed theta_A",
            "derivation_test": "S_A[Psi_A,e_obs(q),omega(e_obs),A_Q,theta_A] has no vertical source current if matter lift and constants are owned",
            "result": "EXACT_CONDITIONAL_MATTER_LEMMA",
            "what_it_buys": "would remove qbar_geom/qbar_marker for owned ordinary matter",
            "what_it_does_not_buy": "does not prevent an external multiplier w_A S_A or hidden scalar coefficient c(I_hid) O_source",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "QDA2686_2_source_prefactor_counterexample",
            "claim_piece": "q-descent alone forbids source-only coefficients",
            "derivation_test": "try S_matter=sum_A w_A S_A with w_A independent of q and with all e_obs(q) descent clauses true",
            "result": "COUNTEREXAMPLE_SURVIVES_Q_DESCENT_ALONE",
            "what_it_buys": "identifies why the proof cannot be only geometric",
            "what_it_does_not_buy": "pre-action weights remain legal unless the parent object language lacks a source-prefactor target",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2685_ZERO_THEOREM_PROOF_ATTEMPT_LEDGER.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "QDA2686_3_typed_sort_route",
            "claim_piece": "typed parent sorts can forbid SpeciesLabel -> Coeff_active_source",
            "derivation_test": "derive disjoint parent sorts and no-Hom constructor rules from MTS primitives rather than declare them",
            "result": "RIGHT_MISSING_THEOREM_NOT_DERIVED",
            "what_it_buys": "if proved, no source-only species slot and no hidden source-prefactor target",
            "what_it_does_not_buy": "current corpus marks sort certificate as schema, not derivation",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "QDA2686_4_action_scale_survival",
            "claim_piece": "classical EOM equivalence removes action multipliers",
            "derivation_test": "test S_A -> w_A S_A against Hilbert source and path-integral/action measure",
            "result": "FALSE_SHORTCUT_REJECTED",
            "what_it_buys": "prevents a bad proof",
            "what_it_does_not_buy": "action-scale/measure owner remains required",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "QDA2686_5_verdict",
            "claim_piece": "parent action admissibility follows from q-descent",
            "derivation_test": "combine q-descent, matter pullback, fixed constants, typed sorts and source-label forgetting",
            "result": "Q_DESCENT_INSUFFICIENT_NEEDS_SORT_DISJOINTNESS_NOHOM",
            "what_it_buys": "narrows the root theorem to sort disjointness/no-Hom plus source-label forgetting",
            "what_it_does_not_buy": "no local-GR/WEP/R10 claim; Delta_w fallback remains live",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2685_NEXT_TARGET.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def derivation_result_rows() -> list[dict[str, Any]]:
    return [
        {
            "result_id": "ADR2686_0_positive",
            "statement": "q-descent is genuinely useful for the left part of the proof: observed geometry/coframe terms are vertically blind under Dq[v_X]=0.",
            "status": "POSITIVE_CONDITIONAL_RESULT",
            "consequence": "ordinary matter terms that depend only on e_obs(q), owned matter lifts and fixed theta_A are silent to the local vertical generator",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "result_id": "ADR2686_1_negative",
            "statement": "q-descent does not by itself define the full parent action object language.",
            "status": "DERIVATION_GAP",
            "consequence": "a q-blind term can still be multiplied by source-only w_A unless the coefficient target is syntactically absent",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "result_id": "ADR2686_2_root_theorem",
            "statement": "The needed next theorem is no-Hom(SpeciesLabel/Hidden/Readout, Coeff_active_source) from disjoint parent sorts and constructor exhaustion.",
            "status": "ROOT_THEOREM_SELECTED",
            "consequence": "this is stronger and cleaner than fitting Delta_w_AB, but it is not yet proven",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "result_id": "ADR2686_3_fallback",
            "statement": "If sort-disjointness/no-Hom fails, Delta_w_AB must become the first finite source row with values, units, normalizer, projections and no-cancellation.",
            "status": "FALLBACK_STAGED_NONCLAIM",
            "consequence": "finite path remains disciplined without pretending the theorem passed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def sort_nohom_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("SDN2686_0_parent_sorts", "derive disjoint parent sorts Q_obs, MatterField, Theta_rep, GaugeCurrent, Coeff_active_source, SpeciesLabel, HiddenMarker, Readout", "sorts cannot be declared by discipline only", "MISSING_PRIMITIVE_SORT_CONSTRUCTION"),
        ("SDN2686_1_constructor_exhaustion", "show all parent action constructors factor through allowed sorts before readout", "otherwise source-only constructor can be added after the fact", "MISSING_CONSTRUCTOR_EXHAUSTION"),
        ("SDN2686_2_nohom_species_source", "prove Hom(SpeciesLabel, Coeff_active_source)=empty_or_common", "kills Delta_w_AB/source-only w_A", "MISSING_SPECIES_TO_SOURCE_NOHOM"),
        ("SDN2686_3_nohom_hidden_source", "prove Hom(HiddenMarker, Coeff_active_source)=empty_or_common", "kills c(I_hid) active-source prefactor", "MISSING_HIDDEN_TO_SOURCE_NOHOM"),
        ("SDN2686_4_source_label_forgetting", "source functor maps ordinary matter to total Hilbert source, not per-species source selector", "prevents post-variation species labels becoming coupling selectors", "MISSING_SOURCE_LABEL_FORGETTING_FUNCTOR"),
        ("SDN2686_5_action_scale_owner", "one parent action-scale/measure owner covers all ordinary species", "removes w_A as a quantum/action-measure multiplier", "MISSING_ACTION_SCALE_MEASURE_OWNER"),
        ("SDN2686_6_readout_stability", "readout/radiative/effective maps preserve no-Hom domains", "prevents C_eff_source_tail and arena-specific source legs", "MISSING_READOUT_RADIATIVE_STABILITY"),
        ("SDN2686_7_verdict", "all no-Hom/sort clauses are parent-derived", "would close ZTC2685_0 and advance zero theorem", "SORT_DISJOINTNESS_NOHOM_NOT_PROVED"),
    ]
    return [
        {
            "requirement_id": req_id,
            "required_theorem_piece": piece,
            "why_needed": why,
            "current_status": status,
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv")),
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive this from primitive MTS object language or keep Delta_w finite row live",
            "timestamp_utc": stamp(),
        }
        for req_id, piece, why, status in rows
    ]


def delta_w_first_row() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DWF2686_0_delta_w_AB",
            "quantity": "Delta_w_AB",
            "branch_role": "first finite fallback if no-Hom/sort theorem fails",
            "formula_or_contract": "Delta_w_AB is a source-normalized relative pre-action/source weight; it cannot be inferred from WEP/R10 bounds",
            "required_value_source": "independent parent/source coefficient or explicit theorem-zero",
            "required_units": "dimensionless common source fraction",
            "required_projection": "K_WEP*tau_WEP; K_R10(lambda)*tau_R10(lambda)*Qbar; M_PPN; K_orbital; common normalizer",
            "current_value": "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "do not score; attack sort no-Hom first",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "DWF2686_1_refusal",
            "quantity": "Delta_w_AB",
            "branch_role": "anti-shortcut guard",
            "formula_or_contract": "forbid Delta_w_AB=0 by preference, covariance-only proof, measured-G absorption, or WEP/R10 bound inversion",
            "required_value_source": "none; this is a refusal rule",
            "required_units": "n/a",
            "required_projection": "n/a",
            "current_value": "REFUSAL_ACTIVE",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "preserve until theorem-zero or independent source value exists",
            "timestamp_utc": stamp(),
        },
    ]


def runner_rows(audit: list[dict[str, Any]], requirements: list[dict[str, Any]], delta_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in audit:
        rows.append(
            {
                "runner_id": f"RUN2686_{row['audit_id']}",
                "stage": "q_descent_admissibility",
                "target_id": row["audit_id"],
                "q_descent_available": "true" if "QDA2686_0" in row["audit_id"] or "QDA2686_1" in row["audit_id"] else "conditional",
                "sort_nohom_available": "false",
                "delta_w_value_available": "false",
                "bound_inversion_used": "false",
                "score_ready": "false",
                "valid_for_claim": "false",
                "runner_verdict": row["result"],
                "timestamp_utc": stamp(),
            }
        )
    rows.append(
        {
            "runner_id": "RUN2686_SORT_NOHOM_VERDICT",
            "stage": "sort_disjointness_nohom",
            "target_id": "SDN2686_0..7",
            "q_descent_available": "conditional_geometry_only",
            "sort_nohom_available": "false",
            "delta_w_value_available": "false",
            "bound_inversion_used": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "runner_verdict": ";".join(row["current_status"] for row in requirements),
            "timestamp_utc": stamp(),
        }
    )
    for row in delta_rows:
        rows.append(
            {
                "runner_id": f"RUN2686_{row['row_id']}",
                "stage": "delta_w_fallback",
                "target_id": row["row_id"],
                "q_descent_available": "not_sufficient",
                "sort_nohom_available": "false",
                "delta_w_value_available": "false",
                "bound_inversion_used": "false",
                "score_ready": row["score_ready"],
                "valid_for_claim": row["valid_for_claim"],
                "runner_verdict": row["current_value"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2686_0_q_descent_geometry", "q-descent geometry vertical blindness", "PASS_CONDITIONAL_ONLY", "useful conditional lemma, not full admissibility proof"),
        ("CG2686_1_parent_admissibility", "source-only labels are proved nonarguments of S_parent", "FAIL", "q-descent alone does not derive sort disjointness/no-Hom"),
        ("CG2686_2_sort_nohom", "no-Hom SpeciesLabel/Hidden/Readout to Coeff_active_source", "FAIL", "sort no-Hom remains unsigned"),
        ("CG2686_3_delta_w_finite", "Delta_w_AB finite row is source-ready", "FAIL", "no theorem-zero or independent numeric value"),
        ("CG2686_4_bound_inversion", "WEP/R10 bounds are not used as Delta_w values", "PASS_GUARD_ONLY", "explicit refusal rule remains active"),
        ("CG2686_5_local_claim", "local GR/WEP/R10/PPN/clock/orbital promotion", "REFUSED", "2686 is a derivation gate only"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "current_status": status,
            "reason": reason,
            "gate_pass": "true" if status in {"PASS_CONDITIONAL_ONLY", "PASS_GUARD_ONLY"} else "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2686_0_q_descent_result",
            "decision": "Q_DESCENT_IS_NECESSARY_NOT_SUFFICIENT",
            "rationale": "it proves geometry/matter pullback silence conditionally, but does not forbid q-blind source multipliers",
            "claim_allowed": "false",
            "next_action": "attack parent sort disjointness/no-Hom theorem",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2686_1_root_target",
            "decision": "SORT_DISJOINTNESS_NOHOM_IS_THE_NEXT_ROOT",
            "rationale": "NoSourceOnlySpeciesSlot requires SpeciesLabel/Hidden/Readout to have no morphism into Coeff_active_source",
            "claim_allowed": "false",
            "next_action": "derive or reject the no-Hom theorem directly",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2686_2_fallback",
            "decision": "DELTA_W_AB_REMAINS_FIRST_FINITE_FALLBACK",
            "rationale": "if no-Hom fails, this is the highest-leverage finite local coupling row",
            "claim_allowed": "false",
            "next_action": "keep finite row nonclaim until value/projection/normalizer exists",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2686_0_selected",
            "kind": "selected",
            "target_doc": "2687-Y5-R2FR-parent-sort-disjointness-nohom-proof-or-finite-delta-w-basis.md",
            "target_script": "scripts/Y5_R2FR_parent_sort_disjointness_nohom_proof_or_finite_delta_w_basis_2687.py",
            "purpose": "derive or reject no-Hom(SpeciesLabel/Hidden/Readout, Coeff_active_source) from parent sort disjointness and constructor exhaustion; if rejected, build the finite Delta_w component basis",
            "acceptance_gate": "either no source-prefactor target is parent-forbidden, or Delta_w_AB is decomposed into finite nonclaim component rows with units, common-mode projector, norm and no-cancellation policy",
            "forbidden_shortcuts": "using q-descent geometry as full action-domain proof; syntax by decree; Delta_w=0 by preference; WEP/R10 bound inversion; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2686_0_positive", "q-descent", "USEFUL_CONDITIONAL_GEOMETRY_RESULT", "q-descent supports vertical blindness of observed geometry/coframe"),
        ("STATUS2686_1_root_gap", "parent action admissibility", "SORT_DISJOINTNESS_NOHOM_MISSING", "the action-domain proof needs no-Hom into active-source coefficients"),
        ("STATUS2686_2_fallback", "Delta_w_AB", "FINITE_FALLBACK_LIVE_NONCLAIM", "Delta_w remains the first finite row if no-Hom fails"),
    ]
    return [
        {
            "status_id": status_id,
            "sector": sector,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "false",
            "next_action": "run 2687 sort-disjointness/no-Hom target",
            "timestamp_utc": stamp(),
        }
        for status_id, sector, status, meaning in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": f"BC2686_{name}",
            "absolute_path": str(path),
            "relative_path": rel_path(path),
            "exists": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for name, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(source_rows: list[dict[str, Any]], audit: list[dict[str, Any]], results: list[dict[str, Any]], requirements: list[dict[str, Any]], delta_rows: list[dict[str, Any]], runner: list[dict[str, Any]], claim_gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    q_positive = any(row["audit_id"] == "QDA2686_0_q_vertical_blindness" and row["result"] == "EXACT_CONDITIONAL_GEOMETRY_LEMMA" for row in audit)
    q_insufficient = any(row["audit_id"] == "QDA2686_5_verdict" and row["result"] == "Q_DESCENT_INSUFFICIENT_NEEDS_SORT_DISJOINTNESS_NOHOM" for row in audit)
    counterexample_retained = any(row["audit_id"] == "QDA2686_2_source_prefactor_counterexample" and "COUNTEREXAMPLE_SURVIVES" in row["result"] for row in audit)
    root_selected = any(row["result_id"] == "ADR2686_2_root_theorem" and row["status"] == "ROOT_THEOREM_SELECTED" for row in results)
    requirements_nonclaim = all(row["parent_signed"] == "false" and row["claim_allowed"] == "false" for row in requirements)
    delta_nonclaim = all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in delta_rows)
    runner_refuses = all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in runner)
    claim_blocked = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_gates)
    bound_refused = any(row["gate_id"] == "CG2686_4_bound_inversion" and row["gate_pass"] == "true" and row["claim_allowed"] == "false" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2687" in read_text(OUTPUTS["next_target"])
    checks = [
        ("VAL2686_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2686_q_descent_positive_piece", q_positive, "q-descent geometry lemma retained as positive conditional result"),
        ("VAL2686_q_descent_insufficient", q_insufficient, "q-descent alone is marked insufficient for parent admissibility"),
        ("VAL2686_counterexample_retained", counterexample_retained, "source-prefactor counterexample remains active"),
        ("VAL2686_root_nohom_selected", root_selected, "sort disjointness/no-Hom root theorem selected"),
        ("VAL2686_nohom_requirements_nonclaim", requirements_nonclaim, "no-Hom requirements are unsigned/nonclaim"),
        ("VAL2686_delta_w_fallback_nonclaim", delta_nonclaim, "Delta_w fallback rows remain nonclaim"),
        ("VAL2686_runner_refuses_unsigned_rows", runner_refuses, "runner refuses all unsigned rows"),
        ("VAL2686_claim_gates_block_claims", claim_blocked, "claim gates block promotion"),
        ("VAL2686_bound_inversion_refused", bound_refused, "bound inversion guard active"),
        ("VAL2686_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2686_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2686_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2686_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2686_next_target_selected", next_target_ok, "2687 no-Hom target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2686_OVERALL",
            "passed": as_bool(overall),
            "detail": "2686 proves q-descent is necessary but insufficient, selects sort-disjointness/no-Hom as the root theorem, and keeps Delta_w_AB nonclaim",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(source_rows: list[dict[str, Any]], audit: list[dict[str, Any]], results: list[dict[str, Any]], requirements: list[dict[str, Any]], delta_rows: list[dict[str, Any]], runner: list[dict[str, Any]], claim_gates: list[dict[str, Any]], decisions: list[dict[str, Any]], next_target: list[dict[str, Any]], status: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 2686 — Y5/R2FR Parent Action Admissibility From q-Descent or Delta-w First Row",
                "",
                "## Private Verdict",
                "",
                "`q`-descent gives a real positive result: if `Dq[v_X]=0`, observed geometry and owned pullback matter terms are vertically blind. That is useful for the GR/Newton reduction spine.",
                "",
                "But `q`-descent is not enough to prove parent action admissibility. A source-only multiplier `w_A S_A` can be q-blind and still change the Hilbert/source normalization. The missing theorem is sort-disjointness/no-Hom: `SpeciesLabel`, hidden markers, and readout labels must have no morphism into `Coeff_active_source`.",
                "",
                "So the next derivation target is not another broad audit. It is the direct parent sort-disjointness/no-Hom proof. If that fails, `Delta_w_AB` stays as the first finite nonclaim coupling basis row.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## q-Descent Admissibility Audit",
                "",
                markdown_table(audit),
                "",
                "## Derivation Result",
                "",
                markdown_table(results),
                "",
                "## Sort-Disjointness / No-Hom Requirements",
                "",
                markdown_table(requirements),
                "",
                "## Delta-w First Row",
                "",
                markdown_table(delta_rows),
                "",
                "## Runner Results",
                "",
                markdown_table(runner),
                "",
                "## Claim Gates",
                "",
                markdown_table(claim_gates),
                "",
                "## Decisions",
                "",
                markdown_table(decisions),
                "",
                "## Next Target",
                "",
                markdown_table(next_target),
                "",
                "## Project Status Snapshot",
                "",
                markdown_table(status),
                "",
                "## Validation",
                "",
                markdown_table(validation),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    audit = q_descent_audit_rows()
    results = derivation_result_rows()
    requirements = sort_nohom_requirement_rows()
    delta_rows = delta_w_first_row()
    runner = runner_rows(audit, requirements, delta_rows)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["q_descent_audit"], audit)
    write_csv(OUTPUTS["derivation_result"], results)
    write_csv(OUTPUTS["sort_nohom_requirements"], requirements)
    write_csv(OUTPUTS["delta_w_first_row"], delta_rows)
    write_csv(OUTPUTS["runner_results"], runner)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_admissibility_audit"], audit)
    write_csv(BRANCH_OUTPUTS["local_nohom_requirements"], requirements)
    write_csv(BRANCH_OUTPUTS["local_delta_w_first_row"], delta_rows)
    write_csv(BRANCH_OUTPUTS["wep_nohom_requirements"], requirements)
    write_csv(BRANCH_OUTPUTS["source_weight_delta_w_first_row"], delta_rows)

    branch_copies = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validation = validation_rows(source_rows, audit, results, requirements, delta_rows, runner, claim_gates)
    write_csv(OUTPUTS["validation"], validation)
    write_document(source_rows, audit, results, requirements, delta_rows, runner, claim_gates, decisions, next_target, status, validation)

    print(f"wrote {DOC_PATH}")
    for key, path in OUTPUTS.items():
        print(f"{key}: {path}")
    for key, path in BRANCH_OUTPUTS.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
