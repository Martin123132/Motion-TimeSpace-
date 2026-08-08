from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1756"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1756 - Two-Slot Source-Free Owner Or Hidden-Source Counterexample Ledger"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1756_0_1755_doc",
        "source_key": "1755_handoff",
        "source_path": ROOT / "1755-Y5-R2FR-source-silent-fixed-point-theorem-or-E-star-source-norm-row.md",
        "needles": ["TWO_SLOT_SOURCE_FREE_OWNER_IS_BEST_NEXT_ROUTE", "hidden marker/boundary/history source"],
    },
    {
        "source_id": "SRC1756_1_971_parent_split",
        "source_key": "971_parent_split_derivation",
        "source_path": RESIDUALS / "P8_Y5_R10_971_PARENT_SPLIT_DERIVATION_ATTEMPT.csv",
        "needles": ["PSD971_0_two_slot_ansatz", "PSD971_7_verdict"],
    },
    {
        "source_id": "SRC1756_2_972_local_zero_gate",
        "source_key": "972_local_zero_theorem_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_972_LOCAL_ZERO_THEOREM_GATE.csv",
        "needles": ["LZG972_2_source_zero", "LZG972_7_verdict"],
    },
    {
        "source_id": "SRC1756_3_973_source_free_sxkin",
        "source_key": "973_source_free_sxkin_lemma",
        "source_path": RESIDUALS / "P8_Y5_R10_973_SOURCE_FREE_SXKIN_LEMMA.csv",
        "needles": ["SFL973_0_homogeneous_quadratic", "SFL973_5_hidden_source_counterexamples"],
    },
    {
        "source_id": "SRC1756_4_974_zero_origin",
        "source_key": "974_zero_origin_evenness",
        "source_path": RESIDUALS / "P8_Y5_R10_974_ZERO_ORIGIN_EVENNESS_ATTEMPT.csv",
        "needles": ["ZOE974_3_zero_origin_stationary", "ZOE974_6_verdict"],
    },
    {
        "source_id": "SRC1756_5_974_marker_counterexamples",
        "source_key": "974_marker_counterexamples",
        "source_path": RESIDUALS / "P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv",
        "needles": ["MCE974_0_linear_marker_covector", "MCE974_5_verdict"],
    },
    {
        "source_id": "SRC1756_6_source_normalization_even_gate",
        "source_key": "518_even_scalar_source_normalization",
        "source_path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_EVEN_SCALAR_GATE.csv",
        "needles": ["ES518_2_physical_lock", "Y5 remains an active local-GR blocker"],
    },
    {
        "source_id": "SRC1756_7_source_normalization_split",
        "source_key": "source_normalization_even_odd_split",
        "source_path": RESIDUALS / "P8_SOURCE_NORMALIZATION_EVEN_ODD_SPLIT.csv",
        "needles": ["E2_even_extra_source", "not_killed_by_exchange"],
    },
    {
        "source_id": "SRC1756_8_local_EH_reduction",
        "source_key": "506_local_EH_reduction",
        "source_path": RESIDUALS / "P8_LOCAL_EH_REDUCTION_THEOREM_ATTEMPT.csv",
        "needles": ["T506_EH_plus_silent_reduction", "conditional_bridge_only"],
    },
    {
        "source_id": "SRC1756_9_1755_owner_audit",
        "source_key": "1755_two_slot_owner_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1755_TWO_SLOT_SOURCE_FREE_OWNER_AUDIT.csv",
        "needles": ["TSO1755_0_parent_contract", "TSO1755_7_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_SOURCE_REGISTER.csv",
    "owner_proof_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_TWO_SLOT_SOURCE_FREE_OWNER_PROOF_ATTEMPT.csv",
    "hidden_counterexamples": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_COUNTEREXAMPLE_LEDGER.csv",
    "finite_residual_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_FINITE_RESIDUAL_ROWS.csv",
    "gr_bridge_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_GR_NEWTON_BRIDGE_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1756_VALIDATION.csv",
}


COPY_MAP = {
    "owner_proof_attempt": "R2FR_1756_TWO_SLOT_SOURCE_FREE_OWNER_PROOF_ATTEMPT.csv",
    "hidden_counterexamples": "R2FR_1756_HIDDEN_SOURCE_COUNTEREXAMPLE_LEDGER.csv",
    "finite_residual_rows": "R2FR_1756_HIDDEN_SOURCE_FINITE_RESIDUAL_ROWS.csv",
    "gr_bridge_status": "R2FR_1756_GR_NEWTON_BRIDGE_STATUS.csv",
    "decision": "R2FR_1756_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1756_CLAIM_GATE.csv",
    "next_target": "R2FR_1756_NEXT_TARGET.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        needles_present = all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": "; ".join(needles),
                "needles_present": yesno(needles_present),
                "used_for": "1756 two-slot source-free owner or hidden-source counterexample ledger",
                "timestamp_utc": UTC,
            }
        )
    return rows


def owner_proof_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "proof_id": "OP1756_0_target",
            "clause": "target theorem",
            "mathematical_form": "delta_X S_parent|_{D_L=0,X=0}=0, with L_X positive and zero admissible boundary flux",
            "attempt_result": "TARGET_IDENTIFIED",
            "what_it_would_prove": "X=0 is stationary; hence S_cg(D_L=0,Y)=0 for the local source branch",
            "current_gap": "MISSING_PARENT_OWNER_FOR_SOURCE_FREE_TWO_SLOT_ACTION",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "OP1756_1_two_slot_action",
            "clause": "primitive two-slot decomposition",
            "mathematical_form": "S_parent=S_core[q,Psi,theta]+S_X^kin[X]+f(chi_D)C_obs[X,q,Psi]+S_matter[q,Psi,theta]+S_boundary",
            "attempt_result": "CANDIDATE_WRITTEN_NOT_PARENT_EXTRACTED",
            "what_it_would_prove": "separates local source-free X dynamics from observed/memory coupling",
            "current_gap": "MISSING_PRIMITIVE_PARENT_ACTION_DECOMPOSITION",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "OP1756_2_variation_identity",
            "clause": "X variation under the two-slot ansatz",
            "mathematical_form": "delta_X S_parent = L_X X + J_hidden + f(chi_D)delta_X C_obs + f'(chi_D)C_obs delta_X chi_D + boundary",
            "attempt_result": "EXACT_DECOMPOSITION_CONDITIONAL_ON_ANSATZ",
            "what_it_would_prove": "at chi_D=0 the source vanishes only if J_hidden=0, f(0)=0, and the chain source is zero",
            "current_gap": "MISSING_J_HIDDEN_ZERO_AND_NO_CHAIN_SOURCE_THEOREM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "OP1756_3_homogeneous_kinetic",
            "clause": "centered homogeneous X kinetic sector",
            "mathematical_form": "S_X^kin=1/2 <X,L_X X>, not 1/2<X-X0(q),L_X(X-X0(q))> + ell(X)",
            "attempt_result": "RELATIVE_LEMMA_AVAILABLE_PARENT_UNSIGNED",
            "what_it_would_prove": "J_X^kin(0)=0 and no affine kinetic source",
            "current_gap": "MISSING_CENTERED_ORIGIN_AND_NO_AFFINE_COVECTOR_THEOREM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "OP1756_4_quotient_matter",
            "clause": "quotient-invariant matter descent",
            "mathematical_form": "S_matter=Sbar_matter[q(Phi),Psi,theta] and delta_X q=0 on vertical local directions",
            "attempt_result": "CONDITIONAL_ONLY",
            "what_it_would_prove": "ordinary matter/worldtubes do not directly source X",
            "current_gap": "MISSING_Q_DESCENT_COFAME_CONSTANTS_AND_NO_MATTER_MARKER_VERTEX",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "OP1756_5_coupling_gate",
            "clause": "observable coupling gate",
            "mathematical_form": "f(0)=0, f'(0)=0 or delta_X chi_D=0 at the local fixed point",
            "attempt_result": "COUPLING_GATE_SHAPE_READY_PARENT_ORIGIN_UNSIGNED",
            "what_it_would_prove": "C_obs does not inject a source through either direct or chain variation",
            "current_gap": "MISSING_PARENT_ORIGIN_OF_F_DOUBLE_ZERO_OR_INDEPENDENT_CHI_D_THEOREM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "OP1756_6_boundary_history",
            "clause": "boundary/history silence",
            "mathematical_form": "Pi_local dB_X=0 and retained history tail J_hist(0)=0",
            "attempt_result": "NOT_PARENT_SIGNED",
            "what_it_would_prove": "bulk source-free proof is not spoiled by exterior flux or memory tail",
            "current_gap": "MISSING_BOUNDARY_NOFLUX_AND_HISTORY_TAIL_ZERO_CERTIFICATE",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "OP1756_7_operator_kernel",
            "clause": "positive operator and zero-mode control",
            "mathematical_form": "<X,L_X X> >= c_X ||X||_E^2 after gauge/kernel projection",
            "attempt_result": "NEEDED_AFTER_SOURCE_ZERO",
            "what_it_would_prove": "if all sources vanish, X=0 follows by energy identity",
            "current_gap": "MISSING_LX_SIGN_MASS_GAUGE_AND_ZERO_MODE_DATA",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "OP1756_8_verdict",
            "clause": "two-slot source-free owner verdict",
            "mathematical_form": "source-free owner theorem requires OP1756_1 through OP1756_7 all signed",
            "attempt_result": "PROOF_NOT_CLOSED_COUNTEREXAMPLES_ACTIVE",
            "what_it_would_prove": "would reopen derived local-GR/Newton route if sibling residuals also close",
            "current_gap": "MISSING_TWO_SLOT_OWNER; MISSING_HIDDEN_SOURCE_ZERO; MISSING_OPERATOR_AND_BOUNDARY_DATA",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def hidden_counterexample_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "HSC1756_0_shifted_origin",
            "source_channel": "shifted kinetic origin",
            "construction": "S_X=1/2 <X-X0(q),L_X(X-X0(q))>",
            "source_current": "J_shift=-L_X X0(q) at X=0",
            "why_not_excluded": "zero-origin X0(q)=0 is not parent-signed",
            "repair_or_bound": "derive centered origin theorem or carry ||L_X X0||_{E*}=A_shift",
            "counterexample_retained": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "HSC1756_1_linear_marker_covector",
            "source_channel": "linear material/domain/readout marker",
            "construction": "F_1(X)=ell_marker(X)",
            "source_current": "J_marker=ell_marker in E*",
            "why_not_excluded": "no O(E_X), Z2, or no-marker symmetry is parent-derived",
            "repair_or_bound": "derive no-linear-marker theorem or carry ||ell_marker||_{E*}=A_marker",
            "counterexample_retained": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "HSC1756_2_matter_worldtube_vertex",
            "source_channel": "matter/worldtube X vertex",
            "construction": "S_matter includes V_m[X,rho_A,W_source] outside quotient q",
            "source_current": "J_matter=delta_X V_m|_{X=0}",
            "why_not_excluded": "quotient-invariant matter descent and marker exclusion remain unsigned",
            "repair_or_bound": "derive matter descent through q or carry A_matter per material/source class",
            "counterexample_retained": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "HSC1756_3_coupling_chain_source",
            "source_channel": "observable coupling chain source",
            "construction": "delta_X[f(chi_D)C_obs]=f'(0)C_obs delta_X chi_D + f(0)delta_X C_obs",
            "source_current": "J_chain=f'(0)C_obs partial_X chi_D at chi_D=0 unless double-zero or independence holds",
            "why_not_excluded": "parent origin of f(0)=f'(0)=0 or delta_X chi_D=0 is not signed",
            "repair_or_bound": "derive coupling double-zero from parent symmetry or carry A_chain",
            "counterexample_retained": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "HSC1756_4_boundary_flux",
            "source_channel": "boundary/local projection flux",
            "construction": "boundary lift or Pi_local dB_X enters the X Euler-Lagrange equation",
            "source_current": "J_boundary=Pi_local dB_X",
            "why_not_excluded": "boundary primitive silence, projected flux zero, and secular drift gates are not parent-derived",
            "repair_or_bound": "derive no-flux/no-hair boundary class or carry A_boundary",
            "counterexample_retained": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "HSC1756_5_history_tail",
            "source_channel": "retained memory/history tail",
            "construction": "nonlocal history term leaves affine local tail at D_L=0",
            "source_current": "J_hist=delta_X S_hist|_{X=0}",
            "why_not_excluded": "history-tail zero theorem is absent",
            "repair_or_bound": "derive tail cancellation/decay or carry A_hist",
            "counterexample_retained": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "HSC1756_6_integrated_out_tower",
            "source_channel": "integrated-out non-EH tower",
            "construction": "solving X with nonzero source produces <J,L^{-1}J> and local R10/R11 leakage",
            "source_current": "J_tower maps into non-EH coefficients after reduction",
            "why_not_excluded": "no-extra-scalar/no-integrated-out-tower certificate remains unsigned",
            "repair_or_bound": "derive no-tower theorem or carry arena-specific K_R10/K_PPN/K_clock/K_orbital rows",
            "counterexample_retained": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "HSC1756_7_even_source_normalization",
            "source_channel": "physical even measured-GM/source-normalization residual",
            "construction": "mu_extra_even or c_domain_source_normalization_operator survives X -> -X",
            "source_current": "J_mu contributes to measured source normalization rather than auxiliary odd X",
            "why_not_excluded": "parity/evenness does not kill observed even source residuals",
            "repair_or_bound": "derive physical lock Z_Y5=epsilon_mu with zero even residual or carry A_mu_even",
            "counterexample_retained": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "HSC1756_8_operator_kernel",
            "source_channel": "operator kernel/zero mode",
            "construction": "L_X has uncontrolled kernel or gauge mode with nonzero boundary/readout projection",
            "source_current": "J_kernel is not erased by positivity on the orthogonal complement",
            "why_not_excluded": "A^ij, m_X^2, gauge, and zero-mode data are not parent-signed",
            "repair_or_bound": "derive kernel projection silence or carry A_kernel",
            "counterexample_retained": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "HSC1756_9_verdict",
            "source_channel": "hidden source verdict",
            "construction": "all above channels are still legal in the current corpus",
            "source_current": "J_hidden=sum(J_shift,J_marker,J_matter,J_chain,J_boundary,J_hist,J_tower,J_mu,J_kernel)",
            "why_not_excluded": "1756 cannot parent-prove J_hidden=0",
            "repair_or_bound": "prove selected source-zero clauses next or carry finite source envelope",
            "counterexample_retained": "True",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def finite_residual_rows() -> list[dict[str, Any]]:
    channels = [
        ("HSR1756_0_shift", "A_shift", "||L_X X0(q)||_{E*}", "shifted kinetic origin", "MISSING_CENTERED_ORIGIN_ZERO_OR_A_SHIFT"),
        ("HSR1756_1_marker", "A_marker", "||ell_marker||_{E*}", "linear marker covector", "MISSING_NO_MARKER_THEOREM_OR_A_MARKER"),
        ("HSR1756_2_matter", "A_matter", "||delta_X V_m||_{E*}", "matter/worldtube vertex", "MISSING_MATTER_DESCENT_OR_A_MATTER"),
        ("HSR1756_3_chain", "A_chain", "||f'(0)C_obs partial_X chi_D||_{E*}", "coupling chain source", "MISSING_COUPLING_DOUBLE_ZERO_OR_A_CHAIN"),
        ("HSR1756_4_boundary", "A_boundary", "||Pi_local dB_X||_{E*}", "boundary flux source", "MISSING_BOUNDARY_NOFLUX_OR_A_BOUNDARY"),
        ("HSR1756_5_history", "A_hist", "||delta_X S_hist|0||_{E*}", "history tail source", "MISSING_HISTORY_TAIL_ZERO_OR_A_HIST"),
        ("HSR1756_6_tower", "A_tower", "||K_tower <J,L^{-1}J>||", "integrated-out tower projection", "MISSING_NO_TOWER_OR_A_TOWER"),
        ("HSR1756_7_mu", "A_mu_even", "||J_mu_even||_{E* or arena}", "even source normalization residual", "MISSING_EVEN_SOURCE_NORMALIZATION_ZERO_OR_A_MU"),
        ("HSR1756_8_kernel", "A_kernel", "||P_kernel J||", "operator kernel projection", "MISSING_KERNEL_SILENCE_OR_A_KERNEL"),
    ]
    rows: list[dict[str, Any]] = []
    for residual_id, quantity, formula, source_channel, status in channels:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "residual_id": residual_id,
                "quantity": quantity,
                "source_channel": source_channel,
                "required_form": formula,
                "units": "E*_dual_or_declared_arena_units",
                "current_status": status,
                "bound_role": "adds to ||J_hidden|| and then to R_source through local operator/projection norms",
                "source_path": "see P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_COUNTEREXAMPLE_LEDGER.csv",
                "score_ready": no(),
                "valid_prediction_row": no(),
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "residual_id": "HSR1756_9_total",
            "quantity": "A_hidden_total",
            "source_channel": "total hidden source envelope",
            "required_form": "A_hidden_total <= A_shift+A_marker+A_matter+A_chain+A_boundary+A_hist+A_tower+A_mu_even+A_kernel in one declared norm",
            "units": "same_E*_dual_or_declared_arena_units",
            "current_status": "MISSING_TOTAL_HIDDEN_SOURCE_ENVELOPE",
            "bound_role": "if not theorem-zero, this becomes the finite residual replacing source silence",
            "source_path": "see individual HSR1756 rows",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
    )
    return rows


def gr_bridge_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "GRB1756_0_source_current",
            "bridge_piece": "source current zero",
            "current_status": "NOT_CLOSED",
            "evidence": "J_hidden counterexamples remain active",
            "needed_for_GR_Newton": "J_hidden=0 theorem or finite arena-safe residual envelope",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "GRB1756_1_positive_silence",
            "bridge_piece": "positive operator silence",
            "current_status": "CONDITIONAL_ONLY",
            "evidence": "energy identity works only after source and boundary vanish",
            "needed_for_GR_Newton": "L_X signs, masses, gauge/kernel data, and boundary class",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "GRB1756_2_source_normalization",
            "bridge_piece": "measured Newtonian source normalization",
            "current_status": "ACTIVE_BLOCKER",
            "evidence": "even measured-GM/source-normalization residual is not killed by parity",
            "needed_for_GR_Newton": "theorem-zero or coefficient-filled source-normalization row",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "GRB1756_3_sibling_residuals",
            "bridge_piece": "K_perp, boundary flux, arena projections",
            "current_status": "ACTIVE_BLOCKERS",
            "evidence": "1755 and red-team status retain sibling local residuals",
            "needed_for_GR_Newton": "exact-zero, stronger power, or explicit bound per residual",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "GRB1756_4_verdict",
            "bridge_piece": "derived local GR/Newton route",
            "current_status": "NARROWED_NOT_DERIVED",
            "evidence": "1756 converts the main source-zero gap into named proof clauses or finite residual rows",
            "needed_for_GR_Newton": "1757 must prove centered-origin/no-marker/coupling source silence or quantify A_hidden",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1756_0_proof_result",
            "decision": "TWO_SLOT_OWNER_NOT_PROVED",
            "reason": "the ansatz gives a clean variation identity, but parent ownership and hidden-source exclusion remain unsigned",
            "next_action": "do not promote source silence or local GR",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1756_1_counterexample_result",
            "decision": "HIDDEN_SOURCES_CONVERTED_TO_RESIDUAL_ROWS",
            "reason": "every surviving ghost source is now named with a formula-shaped source current and missing bound row",
            "next_action": "attack the biggest proof clauses or acquire A_hidden in E*/arena norms",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1756_2_best_next",
            "decision": "CENTERED_ORIGIN_NO_LINEAR_MARKER_IS_NEXT_BEST_ROUTE",
            "reason": "proving X0=0 and ell_marker=0 is the sharpest way to kill F_1 without relying on fitted small coefficients",
            "next_action": "build 1757 centered-origin/no-linear-marker symmetry proof or A_hidden bound",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1756_3_GR_status",
            "decision": "GR_NEWTON_BRIDGE_CLOSER_BUT_BLOCKED",
            "reason": "the source-current problem is better named, but source normalization, boundary, K_perp, operator/kernel, and arena projection rows remain open",
            "next_action": "keep local GR/Newton as derivation target, not a claim",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1756_0_two_slot_owner",
            "claim": "primitive parent action owns the two-slot source-free split",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_ACTION_DECOMPOSITION_UNSIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1756_1_hidden_sources_zero",
            "claim": "J_hidden=0 at D_L=0",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_SHIFTED_ORIGIN_MARKER_MATTER_CHAIN_BOUNDARY_HISTORY_TOWER_MU_KERNEL",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1756_2_hidden_sources_bounded",
            "claim": "all hidden source rows have finite sourced E*/arena bounds",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_A_HIDDEN_ROWS_MISSING",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1756_3_source_silence",
            "claim": "S_cg(D_L=0,Y)=0 is derived",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_J_HIDDEN_ACTIVE",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1756_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10/WEP/clock/orbital branch can claim",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_CURRENT_AND_SIBLING_LOCAL_RESIDUALS_ACTIVE",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1756_0_primary",
            "next_target": "1757-Y5-R2FR-centered-origin-no-linear-marker-symmetry-proof-or-Ahidden-bound.md",
            "script": "scripts/Y5_R2FR_centered_origin_no_linear_marker_symmetry_proof_or_Ahidden_bound.py",
            "objective": "try to prove X0(q)=0 and ell_marker=0 from parent symmetry/invariance; otherwise create A_shift and A_marker finite residual rows",
            "success_condition": "F_1 is killed by parent-owned symmetry/centering or the leading hidden affine source is bounded without claim promotion",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1756_1_coupling_fallback",
            "next_target": "1757b-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md",
            "script": "scripts/Y5_R2FR_coupling_chain_source_double_zero_proof_or_Achain_bound.py",
            "objective": "try to derive f(0)=f'(0)=0 or delta_X chi_D=0 at the local fixed point; otherwise carry A_chain",
            "success_condition": "observable coupling cannot inject J_X at chi_D=0 or it becomes an explicit finite residual",
            "selection_status": "held_fallback",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "owner_proof_attempt": owner_proof_attempt_rows(),
        "hidden_counterexamples": hidden_counterexample_rows(),
        "finite_residual_rows": finite_residual_rows(),
        "gr_bridge_status": gr_bridge_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1756_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1756_{key.upper()}.csv")


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if row.get(field) == "True":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text:
                for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                    if row.get(field) == "True":
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1756_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1756_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1756*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def proof_attempt_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["proof_id"] == "OP1756_8_verdict"
        and row["attempt_result"] == "PROOF_NOT_CLOSED_COUNTEREXAMPLES_ACTIVE"
        for row in rows_map["owner_proof_attempt"]
    )


def variation_decomposition_present(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["proof_id"] == "OP1756_2_variation_identity"
        and "J_hidden" in row["mathematical_form"]
        for row in rows_map["owner_proof_attempt"]
    )


def counterexamples_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["hidden_counterexamples"]
    return len(rows) >= 9 and all(row["counterexample_retained"] == "True" for row in rows)


def residual_rows_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["finite_residual_rows"]
    return len(rows) >= 10 and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in rows)


def gr_bridge_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["bridge_id"] == "GRB1756_4_verdict"
        and row["current_status"] == "NARROWED_NOT_DERIVED"
        for row in rows_map["gr_bridge_status"]
    )


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    sources = rows_map["source_register"]
    claims = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1756_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1756_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1756_2_variation_decomposition", variation_decomposition_present(rows_map), "variation decomposition exposes J_hidden", "variation decomposition missing J_hidden"),
        check("VAL1756_3_proof_not_promoted", proof_attempt_not_promoted(rows_map), "two-slot owner proof remains unpromoted", "proof verdict missing or promoted"),
        check("VAL1756_4_counterexamples_retained", counterexamples_retained(rows_map), "hidden-source counterexamples retained", "counterexample ledger incomplete or promoted"),
        check("VAL1756_5_residual_rows_nonclaim", residual_rows_nonclaim(rows_map), "finite residual fallback rows remain nonclaim", "finite residual rows missing or promoted"),
        check("VAL1756_6_gr_bridge_blocked", gr_bridge_blocked(rows_map), "GR/Newton bridge narrowed but blocked", "GR bridge status missing or promoted"),
        check("VAL1756_7_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1756_8_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1756_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1756_10_decision_next", any(row["decision_id"] == "DEC1756_2_best_next" and row["decision"] == "CENTERED_ORIGIN_NO_LINEAR_MARKER_IS_NEXT_BEST_ROUTE" for row in rows_map["decision"]), "decision selects centered-origin/no-linear-marker route", "best-next decision missing"),
        check("VAL1756_11_next_selected", any(row["route_id"] == "NEXT1756_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected", "next target missing"),
        check("VAL1756_12_csv_parse", parsed_ok, "all generated 1756 CSVs parse", "one or more generated 1756 CSVs failed to parse"),
        check("VAL1756_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1756_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1756_15_formalization_untouched", formalization_untouched(), "no 1756 outputs found under formalization-workbench", "1756 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1756_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1756 two-slot source-free owner or hidden-source counterexample ledger" if overall else "one or more 1756 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1756 attacks the two-slot source-free action directly.",
        "- The useful identity is now explicit: `delta_X S_parent = L_X X + J_hidden + gated coupling terms + boundary`.",
        "- The clean local source-zero result follows only if the parent signs the two-slot action, centered origin, quotient matter descent, coupling double-zero/no-chain rule, boundary/history silence, and operator/kernel data.",
        "- Current result: proof not closed. Every surviving hidden source is converted into an explicit nonclaim finite-residual row instead of being silently ignored.",
        "- Best next route is to try to prove `X0(q)=0` and `ell_marker=0`; this attacks the leading `F_1` obstruction without fitting small numbers.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, `q_loc=0`, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Two-Slot Source-Free Owner Proof Attempt",
        markdown_table(rows_map["owner_proof_attempt"], ["proof_id", "clause", "mathematical_form", "attempt_result", "what_it_would_prove", "current_gap"]),
        "",
        "## Hidden-Source Counterexample Ledger",
        markdown_table(rows_map["hidden_counterexamples"], ["counterexample_id", "source_channel", "construction", "source_current", "why_not_excluded", "repair_or_bound"]),
        "",
        "## Hidden-Source Finite Residual Rows",
        markdown_table(rows_map["finite_residual_rows"], ["residual_id", "quantity", "source_channel", "required_form", "current_status"]),
        "",
        "## GR/Newton Bridge Status",
        markdown_table(rows_map["gr_bridge_status"], ["bridge_id", "bridge_piece", "current_status", "evidence", "needed_for_GR_Newton"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is a strong sharpening step. The coupling intuition is real, but it is not the only leak: even a perfect `f(0)=0` gate does not save the local branch if `X0(q)`, `ell_marker`, matter/worldtube vertices, boundary flux, history tails, or even source-normalization residuals survive. The next best move is therefore to kill the leading affine obstruction at the root: prove the centered-origin/no-linear-marker symmetry, or quantify the hidden source envelope honestly.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1756_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1756 validation FAIL")
    print("1756 validation PASS")


if __name__ == "__main__":
    main()
