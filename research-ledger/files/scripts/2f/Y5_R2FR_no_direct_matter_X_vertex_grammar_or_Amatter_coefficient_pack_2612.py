from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_DIRECT_MATTER_GRAMMAR_GATE_2612"
CHECKPOINT_ID = "2612"

DOC = ROOT / "2612-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_LINEAGE_LEDGER.csv",
    "no_direct_grammar": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
    "source_prefactor": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_PREFACTOR_CLASSIFICATION.csv",
    "hom_audit": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_SOURCE_ONLY_HOM_AUDIT.csv",
    "direct_vertex_audit": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_DIRECT_VERTEX_AND_NO_MARKER_AUDIT.csv",
    "coefficient_pack": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_AMATTER_COEFFICIENT_PACK.csv",
    "source_zero": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_SOURCE_ZERO_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2612_VALIDATION.csv",
}

COPY_TARGETS = {
    "no_direct_grammar": LOCAL_BOUNDS / "No_direct_matter_X_vertex_grammar_2612_NONCLAIM.csv",
    "coefficient_pack": LOCAL_BOUNDS / "Amatter_coefficient_pack_2612_NONCLAIM.csv",
    "source_zero": LOCAL_BOUNDS / "Direct_matter_source_zero_status_2612_NONCLAIM.csv",
    "next_target": QUEUE / "JR2612_PARENT_OBJECT_LANGUAGE_HOM_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def false_flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "accepted_for_scoring": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2612_00_2611_handoff_doc",
            "source_path": ROOT / "2611-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "needles": ["NEXT2611_0_selected", "MWD2611_2_direct_vertex_exclusion", "VAL2611_OVERALL"],
            "role": "current handoff selecting no-direct matter X vertex grammar gate",
        },
        {
            "source_id": "SRC2612_01_2611_amatter",
            "source_path": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_AMATTER_BOUND_INTERFACE.csv",
            "needles": ["AM2611_4_A_direct", "AM2611_8_A_matter", "AM2611_9_R_source_matter"],
            "role": "current A_matter interface containing direct matter/source vertex component",
        },
        {
            "source_id": "SRC2612_02_1761_doc",
            "source_path": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
            "needles": ["NDV1761_0_target", "DEC1761_3_best_next", "VAL1761_OVERALL"],
            "role": "prior no-direct matter X vertex grammar checkpoint",
        },
        {
            "source_id": "SRC2612_03_1761_no_direct",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1761_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
            "needles": ["NDV1761_0_target", "NDV1761_3_relative_countermodel", "NDV1761_4_current_verdict"],
            "role": "prior no-direct grammar rows",
        },
        {
            "source_id": "SRC2612_04_1761_prefactor",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1761_SOURCE_PREFACTOR_CLASSIFICATION.csv",
            "needles": ["SP1761_0_absent_slot", "SP1761_2_relative_species", "SP1761_6_readout_worldtube"],
            "role": "prior source-prefactor classification rows",
        },
        {
            "source_id": "SRC2612_05_1761_hom",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1761_NO_SOURCE_ONLY_HOM_AUDIT.csv",
            "needles": ["HOM1761_0_target", "HOM1761_3_readout_worldtube", "HOM1761_4_verdict"],
            "role": "prior no-source-only Hom audit",
        },
        {
            "source_id": "SRC2612_06_1761_direct_vertex",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1761_DIRECT_VERTEX_AND_NO_MARKER_AUDIT.csv",
            "needles": ["DV1761_0_Vm", "DV1761_1_wA", "DV1761_5_verdict"],
            "role": "prior direct-vertex and marker audit",
        },
        {
            "source_id": "SRC2612_07_1761_coefficients",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1761_AMATTER_COEFFICIENT_PACK.csv",
            "needles": ["CP1761_1_delta_w_A", "CP1761_6_A_direct_matter"],
            "role": "prior A_matter/delta_w coefficient pack",
        },
        {
            "source_id": "SRC2612_08_1762_next_doc",
            "source_path": ROOT / "1762-Y5-R2FR-parent-object-language-Hom-exclusion-from-minimality-or-deltaw-bound.md",
            "needles": ["HOM1762_0_target", "DEC1762_3_best_next", "VAL1762_OVERALL"],
            "role": "prior next route: parent object-language Hom exclusion or delta_w bound",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing_needles = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_path": spec["source_path"],
                    "exists": spec["source_path"].exists(),
                    "missing_needles": missing_needles,
                    "source_pass": spec["source_path"].exists() and not missing_needles,
                    "role": spec["role"],
                    **false_flags(),
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2612_0_2611",
            "checkpoint": "2611",
            "question": "Which matter obstruction is sharpest?",
            "result": "The direct matter/source grammar: V_m[X,rho_A,W_source], source-only prefactors, hidden frames, material markers and readout/worldtube masks.",
            "status": "CURRENT_HANDOFF_REBASED",
            "next_dependency": "typed no-direct-vertex grammar",
        },
        {
            "step_id": "LIN2612_1_1761_grammar",
            "checkpoint": "1761",
            "question": "Can the parent grammar forbid direct X matter vertices?",
            "result": "Conditionally yes: if ordinary matter syntax is minimal and has no active-source prefactor argument, then A_direct_matter=0.",
            "status": "EXACT_CONDITIONAL_SCHEMA_IMPORTED",
            "next_dependency": "parent object-language Hom exclusion",
        },
        {
            "step_id": "LIN2612_2_1761_countermodel",
            "checkpoint": "1761",
            "question": "Does covariance or Ward symmetry remove relative source prefactors?",
            "result": "No. Relative w_A survives covariance, additivity, Ward identities and common measured-G calibration.",
            "status": "COUNTERMODEL_RETAINED",
            "next_dependency": "delta_w_A retained",
        },
        {
            "step_id": "LIN2612_3_1761_coefficients",
            "checkpoint": "1761",
            "question": "What if the grammar theorem fails?",
            "result": "Carry delta_w_A, delta_w_species, delta_w_hidden, delta_w_marker, delta_w_readout and A_direct_matter as nonclaim residual inputs.",
            "status": "FINITE_FALLBACK_IMPORTED",
            "next_dependency": "source-ready delta_w/A_direct bounds",
        },
        {
            "step_id": "LIN2612_4_1762_preview",
            "checkpoint": "1762",
            "question": "What is the next derivation route?",
            "result": "No-source-only Hom theorem from primitive minimality, invariant algebra triviality, fixed representation data and label-forgetting source functor.",
            "status": "NEXT_ROUTE_IMPORTED",
            "next_dependency": "2613 Hom exclusion or delta_w bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def no_direct_grammar_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NDV2612_0_target",
            "no direct matter X vertex",
            "Allowed[S_ord] excludes V_m[X,rho_A,W_source], w_A(X,m,D,W), hidden frames g_A(X), and post-readout source masks outside q",
            "TARGET_EXACT",
            "ZERO_IF_PARENT_GRAMMAR_SIGNED",
            "absence of a slot is a parent object-language theorem, not a consequence of covariance or Ward identities alone",
        ),
        (
            "NDV2612_1_allowed_syntax",
            "minimal ordinary matter syntax",
            "S_ord=sum_A S_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A] with one common action measure and no active-source prefactor argument",
            "EXACT_CONDITIONAL_SCHEMA",
            "IF_SIGNED_THEN_A_DIRECT_MATTER_ZERO",
            "current parent action does not derive the syntax",
        ),
        (
            "NDV2612_2_common_mode",
            "common source prefactor",
            "S_ord -> w_* S_ord and kappa_univ w_* -> kappa_measured",
            "CALIBRATION_NUISANCE_ONLY",
            "NOT_A_WEP_OR_LOCAL_FORCE_RESIDUAL_BY_ITSELF",
            "does not remove relative or hidden-marker source weights",
        ),
        (
            "NDV2612_3_relative_countermodel",
            "relative source prefactor survives",
            "S_ord=sum_A w_A S_A gives T_source=sum_A w_A T_A while ordinary equations can still look acceptable",
            "COUNTERMODEL_SURVIVES",
            "NO_SOURCE_ONLY_HOM_NOT_DERIVED",
            "relative w_A is not killed by covariance, additivity, Ward identities, or common measured-G calibration",
        ),
        (
            "NDV2612_4_current_verdict",
            "current MTS no-direct-vertex theorem",
            "partial_X V_m|0=0 and delta_w_A=0 for ordinary matter/source sectors",
            "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "A_DIRECT_AND_DELTA_W_RETAINED",
            "Hom exclusion, no-marker minimality, no hidden frame, no alpha/mass vertex, and readout/worldtube silence remain unsigned",
        ),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "status": status,
                "proof_status": proof_status,
                "gap": gap,
                **false_flags(),
            }
        )
        for audit_id, claim_piece, mathematical_form, status, proof_status, gap in rows
    ]


def source_prefactor_rows() -> list[dict[str, Any]]:
    rows = [
        ("SP2612_0_absent_slot", "absent parent slot", "partial S_ord / partial w_A is undefined because w_A is not an argument", "DESIRED_ZERO_ROUTE_NOT_PARENT_SIGNED", "T_source=T_total once other Hilbert/current clauses close", "derive from parent object language or keep nonclaim"),
        ("SP2612_1_common_mode", "common universal prefactor", "w_A=w_* for every ordinary species", "CALIBRATION_MODE", "absorbed into kappa/G calibration, not a relative WEP/source residual by itself", "track separately from relative delta_w_A"),
        ("SP2612_2_relative_species", "relative species/source weight", "w_A=w_*(1+epsilon_A), epsilon_A != epsilon_B", "LIVE_COUNTERMODEL", "composition/source-normalization residual", "parent-forbid or source beta/delta_w bounds"),
        ("SP2612_3_hidden_marker", "hidden invariant/material/domain marker", "w_A=w(I_hid,m,D,boundary,A)", "LIVE_COUNTERMODEL", "source charge reopens under marker/domain/readout labels", "requires primitive minimality and invariant-algebra triviality or explicit A_marker/A_direct rows"),
        ("SP2612_4_hidden_frame", "universal or species hidden conformal/disformal frame", "g_A=A_A(X)^2 g_obs + disformal terms", "LIVE_UNLESS_DECLARED_EXTENSION", "can be WEP-safe narrowly but still affect clocks, PPN, R10 or source normalization", "forbid as parent grammar or bound as c_g/disformal-like residual"),
        ("SP2612_5_alpha_mass_vertex", "direct alpha/mass/charge vertex", "alpha_EM(X)F^2, m_A(X), q_A X_mu J_A^mu, theta_A(I_Q,m)", "FORBIDDEN_BY_POLICY_NOT_PARENT_THEOREM", "clock, WEP, fine-structure and fifth-force residuals return", "derive no-constant-vertex theorem or keep alpha/mass coefficient rows"),
        ("SP2612_6_readout_worldtube", "post-readout/source-worldtube source mask", "w=w(W_source,Pi_M,readout,domain) selected after variation", "LIVE_COUNTERMODEL", "active source can be changed without visibly changing matter equations", "requires before-readout source/worldtube owner theorem or explicit A_worldtube coefficient"),
    ]
    return [
        with_stamp(
            {
                "class_id": class_id,
                "class_name": class_name,
                "mathematical_form": mathematical_form,
                "current_status": current_status,
                "risk": risk,
                "required_resolution": required_resolution,
                **false_flags(),
            }
        )
        for class_id, class_name, mathematical_form, current_status, risk, required_resolution in rows
    ]


def hom_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "HOM2612_0_target",
            "Hom_parent(species_label or hidden_marker or readout_selector, R_+ active-source-prefactor) is empty or common-constant only",
            "TARGET_EXACT",
            "this is the exact grammar theorem that would remove source-only w_A and direct V_m slots",
            "MISSING_PARENT_OBJECT_LANGUAGE_EXCLUSION",
        ),
        (
            "HOM2612_1_species",
            "Hom(species label, R_+ active-source-prefactor)=common constants only",
            "NOT_DERIVED",
            "removes relative species source weights",
            "MISSING_LABEL_FORGETTING_PARENT_CATEGORY_THEOREM",
        ),
        (
            "HOM2612_2_hidden_invariant",
            "Hom(I_hid or invariant generator, R_+ source coefficient)=empty",
            "NOT_DERIVED",
            "removes hidden marker/domain/source coefficients",
            "MISSING_INVARIANT_ALGEBRA_TRIVIALITY",
        ),
        (
            "HOM2612_3_readout_worldtube",
            "Hom(readout/worldtube/domain selector, R_+ source weight)=empty before variation",
            "NOT_DERIVED",
            "prevents post-readout source masks and fitted active-source weights",
            "MISSING_BEFORE_READOUT_WORLDTUBE_SOURCE_OWNER",
        ),
        (
            "HOM2612_4_verdict",
            "no-source-only Hom exclusion is signed for current MTS",
            "FAIL_CURRENT_CLAIM_HOM_NOT_DERIVED",
            "would set delta_w_A=0 and remove A_direct_matter's prefactor branch",
            "retain delta_w and A_direct coefficient pack",
        ),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "claim_piece": claim_piece,
                "current_status": current_status,
                "derived_effect": derived_effect,
                "gap": gap,
                **false_flags(),
            }
        )
        for audit_id, claim_piece, current_status, derived_effect, gap in rows
    ]


def direct_vertex_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("DV2612_0_Vm", "V_m[X,rho_A,W_source]", "matter functor has only q-owned observed geometry, fixed constants, and parent-owned Hilbert worldtube support", "CONTRACT_ONLY", "A_direct_matter"),
        ("DV2612_1_wA", "source-only species/action prefactor w_A", "no-source-only Hom exclusion and single matter density line are parent-signed", "COUNTERMODEL_SURVIVES", "delta_w_A"),
        ("DV2612_2_marker", "theta_A(m), kappa_A(m), material/domain marker", "primitive minimality forbids co-moving marker quotient extensions and invariant algebra has no marker generators", "NOT_DERIVED", "delta_w_marker or A_theta_matter"),
        ("DV2612_3_shadow_frame", "hidden conformal/disformal matter/source frame", "one observed coframe is parent-owned before matter/readout and no shadow frame map is allowed", "NOT_PARENT_SIGNED", "A_shadow_frame or c_g-like disformal residual"),
        ("DV2612_4_alpha_mass", "alpha_EM(X), m_A(X), q_A X_mu J_A^mu", "constants are representation data and no direct constant vertices are parent-derived", "POLICY_ONLY", "A_alpha_mass or b_theta"),
        ("DV2612_5_verdict", "all direct matter/source vertices", "DV2612_0 through DV2612_4 are all signed in one parent branch", "FAIL_CURRENT_CLAIM_DIRECT_VERTEX_NOT_EXCLUDED", "A_direct_matter remains"),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "vertex_or_channel": vertex_or_channel,
                "zero_condition": zero_condition,
                "current_status": current_status,
                "fallback_quantity": fallback_quantity,
                **false_flags(),
            }
        )
        for audit_id, vertex_or_channel, zero_condition, current_status, fallback_quantity in rows
    ]


def coefficient_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("CP2612_0_w_star", "w_star", "common universal source/action prefactor", "CALIBRATION_NUISANCE_NONCLAIM", "common calibration owner if used; not a relative WEP/local-force proof", "kappa/G calibration only"),
        ("CP2612_1_delta_w_A", "delta_w_A", "finite ordinary source/action weight residual vector over source-relevant matter components", "RETAINED_RESIDUAL_SYMBOLIC", "parent Hom zero theorem or component basis with numeric/source-backed bounds", "A_direct_matter, WEP/source-normalization/PPN/R10 local source channels"),
        ("CP2612_2_delta_w_species", "delta_w_species", "species-label to active-source prefactor leakage", "MISSING_HOM_SPECIES_EXCLUSION_OR_BOUND", "label-forgetting parent category proof or source-specific beta/delta_w bound", "composition and source/test residuals"),
        ("CP2612_3_delta_w_hidden", "delta_w_hidden", "hidden invariant to source coefficient leakage", "MISSING_INVARIANT_ALGEBRA_TRIVIALITY_OR_BOUND", "hidden invariant no-Hom proof or coefficient target", "hidden-source A_direct/A_marker residuals"),
        ("CP2612_4_delta_w_marker", "delta_w_marker", "material/domain/boundary marker to source coefficient leakage", "MISSING_NO_MARKER_EXTENSION_THEOREM_OR_BOUND", "primitive minimality/no-marker proof or marker coefficient row", "A_theta_matter and A_direct_matter"),
        ("CP2612_5_delta_w_readout", "delta_w_readout", "post-variation source/readout/worldtube transfer leakage", "MISSING_BEFORE_READOUT_OWNER_OR_BOUND", "source/worldtube owner theorem or readout coefficient bound", "A_worldtube_matter and source-normalization rows"),
        ("CP2612_6_A_direct_matter", "A_direct_matter", "direct matter/source vertex component of A_matter", "MISSING_ZERO_THEOREM_OR_COMPONENT_VALUES", "||delta_v V_m||_{E*} or theorem-zero from no-direct-vertex grammar", "A_matter <= ... + A_direct_matter + ..."),
        ("CP2612_7_R_source_direct", "R_source_direct", "direct matter/source contribution to source residual", "MISSING_ADIRECT_AND_ESTAR_UNITS", "||R_source,direct||_{E*} <= U_B A_direct_matter", "retains repaired p_total=1 for bounded direct matter source"),
    ]
    return [
        with_stamp(
            {
                "coefficient_id": coefficient_id,
                "quantity": quantity,
                "role": role,
                "current_status": current_status,
                "needed_to_promote": needed_to_promote,
                "residual_link": residual_link,
                **false_flags(),
            }
        )
        for coefficient_id, quantity, role, current_status, needed_to_promote, residual_link in rows
    ]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        ("SZ2612_0_no_direct_vertex", "partial_X V_m|0", "NOT_ZEROED", "no-source-only Hom exclusion and no-marker/no-shadow-frame grammar remain unsigned", "parent object language must forbid w_A, hidden frame, marker, alpha/mass and readout/worldtube source slots"),
        ("SZ2612_1_delta_w", "delta_w_A", "RETAINED_NONCLAIM", "relative w_A survives Ward/additivity/common-calibration arguments", "parent Hom theorem or source-backed component bounds"),
        ("SZ2612_2_A_direct", "A_direct_matter", "NOT_ZEROED", "direct vertex and source-prefactor channels remain legal", "zero theorem or component values/common E* norm needed"),
        ("SZ2612_3_A_matter", "A_matter", "NOT_ZEROED", "2612 narrows A_direct_matter but does not close it", "A_geom, A_theta, A_lift, A_direct, A_worldtube, A_boundary and A_nonHilbert remain missing or unsigned"),
        ("SZ2612_4_source_silence", "S_cg(D_L=0,Y)", "NOT_DERIVED", "affine, coupling-chain and matter/direct hidden sources are nonzero/nonclaim", "J_hidden remains active"),
        ("SZ2612_5_GR_Newton", "local GR/Newton bridge", "CLOSER_BUT_BLOCKED", "direct matter/source grammar is now typed and ledgered", "no local-GR matter source closure without Hom exclusion or finite delta_w bounds"),
    ]
    return [
        with_stamp(
            {
                "status_id": status_id,
                "quantity": quantity,
                "current_status": current_status,
                "evidence": evidence,
                "remaining_gap": remaining_gap,
                **false_flags(),
            }
        )
        for status_id, quantity, current_status, evidence, remaining_gap in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2612_0_no_direct_vertex", "parent grammar forbids all direct matter X/source slots", "BLOCKED_PARENT_OBJECT_LANGUAGE_HOM_EXCLUSION_MISSING"),
        ("GATE2612_1_delta_w_zero", "delta_w_A=0", "BLOCKED_RELATIVE_SOURCE_PREFACTOR_COUNTERMODEL_SURVIVES"),
        ("GATE2612_2_A_direct_zero", "A_direct_matter=0", "BLOCKED_NO_MARKER_NO_SHADOW_NO_ALPHA_READOUT_SLOTS_UNSIGNED"),
        ("GATE2612_3_A_direct_bound", "A_direct_matter is finite and sourced in a declared E* norm", "BLOCKED_COMPONENT_BASIS_NUMERIC_BOUNDS_AND_SOURCE_PATHS_MISSING"),
        ("GATE2612_4_A_matter_zero", "A_matter=0", "BLOCKED_DIRECT_AND_WORLDTUBE_MATTER_COMPONENTS_LIVE"),
        ("GATE2612_5_local_GR_Newton", "local GR/Newton/PPN/R10/WEP branch can claim", "BLOCKED_NO_LOCAL_REENTRY"),
    ]
    return [
        with_stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": False,
                "status": "BLOCKED_NO_CLAIM",
                "blocker": blocker,
                **false_flags(),
            }
        )
        for gate_id, claim, blocker in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2612_0_common_mode",
            "decision": "common source prefactor is calibration only",
            "reason": "a single w_star can be absorbed into kappa/G calibration and is not the dangerous relative source charge",
            "effect": "keep w_star separate from delta_w_A",
        },
        {
            "decision_id": "DEC2612_1_relative_mode",
            "decision": "relative source prefactor survives",
            "reason": "Ward symmetry, covariance, additivity and common measured-G calibration do not remove w_A/w_B",
            "effect": "do not claim local-GR matter source closure from Hilbert-current prose alone",
        },
        {
            "decision_id": "DEC2612_2_no_hom",
            "decision": "no-source-only Hom theorem is not parent-derived",
            "reason": "the exact grammar theorem is known but current parent object language does not derive it",
            "effect": "retain delta_w_A and A_direct_matter",
        },
        {
            "decision_id": "DEC2612_3_A_direct",
            "decision": "direct matter/source coefficient pack remains nonclaim",
            "reason": "V_m, relative w_A, hidden markers, hidden frames, alpha/mass vertices and readout/worldtube masks remain legal",
            "effect": "do not set A_direct_matter=0",
        },
        {
            "decision_id": "DEC2612_4_best_next",
            "decision": "select parent object-language Hom exclusion or delta_w bound",
            "reason": "the derivation route now reduces to a typed parent grammar/minimality theorem; otherwise the honest path is finite delta_w bounds",
            "effect": "2613 should try Hom exclusion from minimality/invariant algebra or build delta_w source rows",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2612_0_selected",
            "selection_status": "selected",
            "target_file": "2613-Y5-R2FR-parent-object-language-Hom-exclusion-from-minimality-or-deltaw-bound.md",
            "target_script": "scripts/Y5_R2FR_parent_object_language_Hom_exclusion_from_minimality_or_deltaw_bound_2613.py",
            "task": "try to derive the no-source-only Hom theorem from primitive minimality, invariant-algebra triviality and fixed representation data; otherwise build source-ready delta_w/A_direct bound rows",
            "success_condition": "no-source-only Hom is theorem-zero or delta_w/A_direct is explicit finite nonclaim input",
            "fallback_condition": "rank invariant-generator debts and source delta_w component bounds",
            "guardrails": "do not hide material source charge inside readout definitions; no local-GR claim; no GitHub; no formalization-workbench edits",
        },
        {
            "route_id": "NEXT2612_1_deltaw_fallback",
            "selection_status": "held_fallback",
            "target_file": "2613b-Y5-R2FR-deltaw-Amatter-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_deltaw_Amatter_bound_runner_2613b.py",
            "task": "turn delta_w_A, delta_w_species, delta_w_hidden, delta_w_marker and delta_w_readout into nonclaim source-envelope inputs with units and source paths",
            "success_condition": "finite direct-matter source residual can be evaluated as nonclaim input",
            "fallback_condition": "local branch remains closure-only",
            "guardrails": "score only after units, E* norm, component basis and arena projections are real",
        },
        {
            "route_id": "NEXT2612_2_worldtube_fallback",
            "selection_status": "held_fallback",
            "target_file": "2613c-Y5-R2FR-worldtube-Hilbert-support-owner-or-Aworldtube-bound.md",
            "target_script": "scripts/Y5_R2FR_worldtube_Hilbert_support_owner_or_Aworldtube_bound_2613c.py",
            "task": "try to parent-own before-readout worldtube support or carry A_worldtube_matter",
            "success_condition": "readout/worldtube source mask is theorem-zero or finite bounded",
            "fallback_condition": "retain A_worldtube_matter",
            "guardrails": "no fitted source domain after orbital/readout data",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, target in COPY_TARGETS.items():
        source = OUTPUTS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2612_{key}",
                    "source_path": source,
                    "target_path": target,
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                    **false_flags(),
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "valid_prediction_row"}
    for rows in data.values():
        for row in rows:
            for field in forbidden_true_fields:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_not_ready(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            joined = " ".join(row_value(value) for value in row.values())
            if "MISSING" in joined:
                if row.get("score_ready") is True or row.get("claim_allowed") is True or row.get("valid_prediction_row") is True:
                    return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(with_stamp({"check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail, "valid_for_claim": False}))

    add("VAL2612_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2612_01_lineage_complete", {"2611", "1761", "1762"}.issubset({row["checkpoint"] for row in data["lineage"]}), "lineage covers current handoff, prior direct-vertex route and next Hom route")
    add("VAL2612_02_grammar_contract", any(row["audit_id"] == "NDV2612_1_allowed_syntax" and row["status"] == "EXACT_CONDITIONAL_SCHEMA" for row in data["no_direct_grammar"]), "minimal matter grammar contract recorded")
    add("VAL2612_03_countermodel_retained", any(row["audit_id"] == "NDV2612_3_relative_countermodel" and row["status"] == "COUNTERMODEL_SURVIVES" for row in data["no_direct_grammar"]), "relative source-prefactor countermodel retained")
    add("VAL2612_04_no_hom_blocked", any(row["audit_id"] == "HOM2612_4_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_HOM_NOT_DERIVED" for row in data["hom_audit"]), "no-source-only Hom remains unproved")
    add("VAL2612_05_direct_vertex_not_promoted", any(row["audit_id"] == "DV2612_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_DIRECT_VERTEX_NOT_EXCLUDED" for row in data["direct_vertex_audit"]), "direct matter/source vertex remains unpromoted")
    add("VAL2612_06_deltaw_nonclaim", all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["coefficient_pack"]), "delta_w/A_direct coefficient pack remains nonclaim")
    add("VAL2612_07_U_B_power_retained", any(row["coefficient_id"] == "CP2612_7_R_source_direct" and "U_B A_direct_matter" in row["needed_to_promote"] for row in data["coefficient_pack"]), "explicit U_B source-residual factor retained")
    add("VAL2612_08_source_zero_blocked", any(row["status_id"] == "SZ2612_0_no_direct_vertex" and row["current_status"] == "NOT_ZEROED" for row in data["source_zero"]), "direct source zero remains blocked")
    add("VAL2612_09_source_silence_blocked", any(row["status_id"] == "SZ2612_4_source_silence" and row["current_status"] == "NOT_DERIVED" for row in data["source_zero"]), "source silence remains blocked")
    add("VAL2612_10_claim_gates_safe", all(row["claim_allowed"] is False and row["gate_pass"] is False for row in data["claim_gates"]), "all claim gates remain blocked")
    add("VAL2612_11_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes scoring or claim flags")
    add("VAL2612_12_missing_not_ready", missing_rows_not_ready(data), "no MISSING_* row is marked ready")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*DIRECT_MATTER_GRAMMAR_GATE_2612*", "2612-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md", "*JR2612_PARENT_OBJECT_LANGUAGE_HOM_NEXT*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2612_13_no_formalization_artifacts", not formalization_artifacts, "no 2612 direct-matter artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2612_14_decision_next", any(row["decision_id"] == "DEC2612_4_best_next" for row in data["decisions"]), "decision selects parent object-language Hom route")
    add("VAL2612_15_next_selected", any(row["route_id"] == "NEXT2612_0_selected" and row["selection_status"] == "selected" for row in data["next"]), "next target selected")
    add("VAL2612_16_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")
    add("VAL2612_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2612_CSV_{path.stem}", parsed, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2612_COPY_CSV_{key}", parsed, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(with_stamp({"check_id": "VAL2612_OVERALL", "status": "PASS" if overall else "FAIL", "notes": "2612 no-direct matter X vertex grammar gate keeps delta_w/A_direct nonclaim and selects Hom exclusion next", "detail": "", "valid_for_claim": False}))
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row_value(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join([header, divider, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2612: R2FR No Direct Matter X Vertex Grammar Or A_matter Coefficient Pack",
        "",
        "**Status:** private nonclaim current-branch direct-matter grammar checkpoint. This does not claim `partial_X V_m|0=0`, `delta_w_A=0`, `A_direct_matter=0`, source silence, local GR, Newton, PPN, R10, WEP, clocks, or orbital closure.",
        "",
        "**Main result:** the direct matter/source obstruction is now a typed grammar problem. If the parent object language admits only `S_ord=sum_A S_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A]` with one common action measure and no active-source-prefactor argument, then the direct slot is absent and `A_direct_matter=0` for ordinary matter. But covariance, Ward identities, additivity, and common measured-G calibration do not remove relative source weights: `S_ord=sum_A w_A S_A` remains a legal countermodel unless the no-source-only Hom theorem is parent-derived. Therefore `delta_w_A`, `delta_w_species`, `delta_w_hidden`, `delta_w_marker`, `delta_w_readout`, and `A_direct_matter` remain explicit nonclaim residual inputs.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## No Direct Matter X Vertex Grammar",
        markdown_table(data["no_direct_grammar"], ["audit_id", "claim_piece", "mathematical_form", "status", "proof_status", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Source Prefactor Classification",
        markdown_table(data["source_prefactor"], ["class_id", "class_name", "mathematical_form", "current_status", "risk", "required_resolution", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## No-Source-Only Hom Audit",
        markdown_table(data["hom_audit"], ["audit_id", "claim_piece", "current_status", "derived_effect", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Direct Vertex And No-Marker Audit",
        markdown_table(data["direct_vertex_audit"], ["audit_id", "vertex_or_channel", "zero_condition", "current_status", "fallback_quantity", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## A_matter Coefficient Pack",
        markdown_table(data["coefficient_pack"], ["coefficient_id", "quantity", "role", "current_status", "needed_to_promote", "residual_link", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Source-Zero Status",
        markdown_table(data["source_zero"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Private Verdict",
        "",
        "This is a useful squeeze, not a closure. The dangerous matter source is no longer vague: it is a source-only Hom/direct-slot problem. If the typed parent object language is minimal enough, the slot is absent. If not, the surviving residual is finite and nameable: `delta_w_A` and `A_direct_matter`. The next derivation-first move is therefore 2613: try the Hom-exclusion theorem from minimality/invariant algebra; if it fails, start building real `delta_w` bound inputs.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def build_data() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "no_direct_grammar": no_direct_grammar_rows(),
        "source_prefactor": source_prefactor_rows(),
        "hom_audit": hom_audit_rows(),
        "direct_vertex_audit": direct_vertex_audit_rows(),
        "coefficient_pack": coefficient_pack_rows(),
        "source_zero": source_zero_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }


def main() -> None:
    data = build_data()

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["no_direct_grammar"], data["no_direct_grammar"])
    write_csv(OUTPUTS["source_prefactor"], data["source_prefactor"])
    write_csv(OUTPUTS["hom_audit"], data["hom_audit"])
    write_csv(OUTPUTS["direct_vertex_audit"], data["direct_vertex_audit"])
    write_csv(OUTPUTS["coefficient_pack"], data["coefficient_pack"])
    write_csv(OUTPUTS["source_zero"], data["source_zero"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2612_OVERALL")
    print(f"wrote {DOC}")
    print(f"validation={OUTPUTS['validation']}")
    print(f"overall={overall['status']}")


if __name__ == "__main__":
    main()
