from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4104-Y5-R2FR-no-homogeneous-exterior-mode-or-extra-hair-epsilon-row.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_NO_HOMOGENEOUS_EXTRA_HAIR_4104"
CHECKPOINT_ID = "4104"
DECISION = (
    "NO_HOMOGENEOUS_MODE_CHANNELIZED_GK_COERCIVE_BOUND_IMPORTED_"
    "ZERO_THEOREMS_CONDITIONAL_EXTRA_HAIR_RETAINED"
)

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4104_00_4103_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4103_NEXT_TARGET.csv",
        "4104-Y5-R2FR-no-homogeneous-exterior-mode-or-extra-hair-epsilon-row.md",
        "4103 selects no homogeneous exterior mode or extra hair as next target.",
    ),
    "SRC4104_01_4103_certificate": (
        SOURCE_DIR / "P8_Y5_R2FR_4103_LOCAL_EXTERIOR_CERTIFICATE.csv",
        "EXT4103_5_parent_Estat_route",
        "4103 reduces E_stat to uniqueness/no-homogeneous-mode route.",
    ),
    "SRC4104_02_4103_flux": (
        SOURCE_DIR / "P8_Y5_R2FR_4103_FLUX_RESIDUAL_STACK.csv",
        "FLUX4103_1_Estat",
        "4103 flux residual stack contains epsilon_Estat with epsilon_hom_mode and epsilon_extra_hair.",
    ),
    "SRC4104_03_3584_estat": (
        SOURCE_DIR / "P8_Y5_R2FR_3584_PARENT_ESTAT_THEOREM_ATTEMPT.csv",
        "PET3584_6_current_verdict",
        "3584 identifies no-homogeneous-mode as the hard E_stat clause.",
    ),
    "SRC4104_04_3584_stack": (
        SOURCE_DIR / "P8_Y5_R2FR_3584_ESTAT_EPSILON_STACK.csv",
        "ESE3584_5_epsilon_Estat",
        "3584 epsilon_Estat stack before hair refinement.",
    ),
    "SRC4104_05_3585_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3585_NO_HOMOGENEOUS_MODE_THEOREM.csv",
        "NHE3585_6_Estat_update",
        "3585 channelizes homogeneous/exterior hair.",
    ),
    "SRC4104_06_3585_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_3585_EXTRA_HAIR_CHANNEL_AUDIT.csv",
        "CHA3585_6_source_normalization",
        "3585 audit lists radiative, extra-sector, topological, projector and non-EH hair channels.",
    ),
    "SRC4104_07_3585_rows": (
        SOURCE_DIR / "P8_Y5_R2FR_3585_EPSILON_HAIR_BOUND_ROWS.csv",
        "EHB3585_6_epsilon_hom_mode",
        "3585 epsilon hair rows.",
    ),
    "SRC4104_08_3586_gk_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3586_GK_COERCIVE_NOHAIR_THEOREM.csv",
        "GKC3586_3_zero_theorem",
        "3586 turns Gamma/Khat into a concrete coercive theorem-or-bound channel.",
    ),
    "SRC4104_09_3586_gk_source": (
        SOURCE_DIR / "P8_Y5_R2FR_3586_GK_SOURCE_CHARGE_ZERO_AUDIT.csv",
        "GSC3586_5_audit_verdict",
        "3586 source-charge audit for GK channel.",
    ),
    "SRC4104_10_3586_gk_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_3586_GK_HAIR_BOUND_ROWS.csv",
        "GHB3586_4_epsilon_GK_hair",
        "3586 concrete finite bound formula for GK hair.",
    ),
    "SRC4104_11_3586_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3586_NEXT_TARGET.csv",
        "3587-Y5-R2FR-GK-parent-coefficient-source-boundary-owner-or-numeric-bound-inputs.md",
        "3586 selects GK input fill as next target.",
    ),
    "SRC4104_12_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4104_no_homogeneous_exterior_mode_or_extra_hair_epsilon_row.py",
        "Reproducible generator for this 4104 checkpoint.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def row_base() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                **row_base(),
                "source_id": source_id,
                "source_type": "local_checkpoint_or_generator",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "contains_needle": bool_string(path.exists() and needle in read_text(path)),
                "valid_for_claim": "False",
            }
        )
    return rows


def no_homogeneous_theorem_rows() -> List[dict]:
    entries = [
        (
            "NH4104_0_decomposition",
            "homogeneous exterior split",
            "delta Phi_hom = h_TT^rad + X_coercive + X_cross + X_top_boundary + X_projector + X_nonEH.",
            "Any hidden stationary exterior mode must live in radiative EH waves, coercive extra fields, cross/mixed operators, topological/boundary charges, projector/gauge kernels, or retained non-EH metric operators.",
            "DECOMPOSITION_REANCHORED",
            "prevents one word, 'hair', from hiding many different physical escape channels",
            "SRC4104_05_3585_theorem",
        ),
        (
            "NH4104_1_EH_no_news",
            "radiative EH zero route",
            "Bondi/news or Killing-energy flux N_AB N^AB=0 plus stationary boundary data kills h_TT^rad in the local stationary branch.",
            "Stationary no-radiation boundary data exclude radiative homogeneous GR waves. If news is nonzero, it is epsilon_news.",
            "CONDITIONAL_ZERO_FOR_RADIATIVE_EH_MODES",
            "links the 4103 no-radiation anchor to the gravitational exterior, but only conditionally",
            "SRC4104_05_3585_theorem",
        ),
        (
            "NH4104_2_coercive_extra_zero",
            "massive/coercive extra-sector zero route",
            "For any extra field X, if L_X X=0, <X,L_X X> >= c_X||X||^2, boundary flux_X=0, source charge_X=0, and gauge/projector kernel is fixed, then X=0.",
            "Multiply by X and integrate. Positive self-adjoint energy plus zero boundary/source terms forces the trivial exterior solution.",
            "EXACT_CONDITIONAL_NO_HAIR_THEOREM",
            "this is the non-smuggled way to kill extra MTS hair",
            "SRC4104_05_3585_theorem",
        ),
        (
            "NH4104_3_GK_first_channel",
            "Gamma/Khat coercive channel",
            "For u_GK=(A,gamma), lambda_GK>0, J_GK=0, Phi_boundary_GK=0, Q_top_GK=0, and fixed projector/gauge kernel imply u_GK=0.",
            "3586 gives a named field-specific theorem and the finite nonzero bound formula, so one extra-hair channel is no longer generic.",
            "FIELD_SPECIFIC_CHANNEL_BOUND_FILLED_NONCLAIM",
            "moves epsilon_coercive_extra from a placeholder to a concrete GK input contract",
            "SRC4104_08_3586_gk_theorem",
        ),
        (
            "NH4104_4_escape_channels",
            "unavoidable escape channels",
            "Cross terms, topological/boundary hair, projector-hidden modes and retained non-EH operators do not vanish from local positivity alone.",
            "Topological charges may be real observables; projector silence is not full-field silence; cross terms can defeat coercivity; non-EH operators can source local residuals.",
            "ESCAPE_CHANNELS_RETAINED",
            "keeps the no-hair proof honest and prevents closure-by-projection",
            "SRC4104_06_3585_audit",
        ),
        (
            "NH4104_5_Estat_update",
            "E_stat homogeneous-mode update",
            "Z_no_hom_mode = Z_EH_no_news & Z_coercive_extra & Z_cross_bound & Z_top_boundary & Z_projector_kernel & Z_nonEH_silence.",
            "4104 gives theorem routes and residual rows but does not make every factor one.",
            "NO_HOM_MODE_ROUTE_SHARPENED_NOT_CLAIMED",
            "E_stat uniqueness remains blocked until the channels are zeroed or bounded",
            "SRC4104_05_3585_theorem",
        ),
    ]
    return [
        {
            **row_base(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": statement,
            "derivation": derivation,
            "status": status,
            "effect": effect,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, statement, derivation, status, effect, source_key in entries
    ]


def hair_channel_audit_rows() -> List[dict]:
    entries = [
        ("HAIR4104_0_EH_TT", "EH radiative TT", "PASS_IF_ZERO_NEWS_OR_NO_RADIATION_BOUNDARY_SIGNED", "epsilon_news", "zero-news/no incoming gravitational wave boundary must be parent-owned", "SRC4104_05_3585_theorem"),
        ("HAIR4104_1_GK", "Gamma/Khat local response", "FIELD_SPECIFIC_THEOREM_AND_BOUND_READY_NONCLAIM", "epsilon_GK_hair", "lambda_GK,J_GK,boundary,topology,kernel inputs not signed", "SRC4104_08_3586_gk_theorem"),
        ("HAIR4104_2_bulk_memory_range", "bulk/memory/range extra modes", "COERCIVE_ROUTE_WRITTEN_GENERIC", "epsilon_bulk_memory_range_hair", "field-specific operator positivity and source charge zero missing", "SRC4104_06_3585_audit"),
        ("HAIR4104_3_cross_terms", "mixed A/Gamma/memory/operator terms", "BOUND_REQUIRED_FOR_COERCIVITY", "epsilon_cross_hair", "Young/Schur row-sum or finite cross bound missing", "SRC4104_05_3585_theorem"),
        ("HAIR4104_4_boundary_topology", "boundary/topological sector", "UNSIGNED_RELATIVE_COHOMOLOGY_OR_BOUNDARY_FLUX_REQUIRED", "epsilon_top_boundary_hair", "topological charges cannot be positivity-killed", "SRC4104_06_3585_audit"),
        ("HAIR4104_5_projector_kernel", "domain/projector/gauge kernel", "UNSIGNED_PROJECTOR_KERNEL_AUDIT_REQUIRED", "epsilon_projector_hair", "P_loc delta Phi=0 is not delta Phi=0", "SRC4104_05_3585_theorem"),
        ("HAIR4104_6_nonEH_metric", "retained non-EH metric operator family", "UNSIGNED_EH_DOMINANCE_OR_NON_EH_VECTOR_REQUIRED", "epsilon_nonEH_hair", "Lovelock/EH dominance not proven for full MTS exterior", "SRC4104_06_3585_audit"),
        ("HAIR4104_7_source_coupling", "source/coupling normalization", "STILL_SEPARATE_SOURCE_COUPLING_GATE", "epsilon_source_coupling", "zero exterior hair does not calibrate G, measured GM or source weights", "SRC4104_06_3585_audit"),
    ]
    return [
        {
            **row_base(),
            "channel_id": channel_id,
            "channel": channel,
            "status": status,
            "fallback_row": fallback,
            "notes": notes,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for channel_id, channel, status, fallback, notes, source_key in entries
    ]


def gk_bound_rows() -> List[dict]:
    entries = [
        (
            "GK4104_0_operator",
            "u_GK=(A,gamma)",
            "E_GK[u]=int[1/2 Z_A|DA|^2+1/2 m_A2|A|^2+1/2 Z_G|Dgamma|^2+1/2 m_G2 gamma^2+c_AG A.Dgamma]",
            "operator/action units",
            "OPERATOR_FORM_IMPORTED_NONCLAIM",
            "Z_A,m_A2,Z_G,m_G2,c_AG,domain constants",
            "SRC4104_08_3586_gk_theorem",
        ),
        (
            "GK4104_1_lambda",
            "lambda_GK",
            "lambda_GK := lower coercivity bound after cross-term control and kernel/gauge removal",
            "operator eigenvalue/action-normalized stiffness",
            "MISSING_PARENT_SIGNED_VALUE",
            "positive coefficients, domain, gauge/kernel audit, cross-term row-sum",
            "SRC4104_10_3586_gk_bound",
        ),
        (
            "GK4104_2_source",
            "J_GK_norm",
            "||(J_A,J_gamma)||_*",
            "dual source norm",
            "MISSING_PARENT_ZERO_OR_SOURCE_NORM",
            "source-charge owner or finite norm",
            "SRC4104_09_3586_gk_source",
        ),
        (
            "GK4104_3_boundary_topology",
            "Phi_boundary_GK + Q_top_GK",
            "absolute GK boundary flux plus topological charge in the same operator channel",
            "field-energy or Hamiltonian numerator",
            "MISSING_BOUNDARY_TOPOLOGY_ZERO_OR_VALUE",
            "boundary/reference flux and topology class",
            "SRC4104_10_3586_gk_bound",
        ),
        (
            "GK4104_4_hair_bound",
            "epsilon_GK_hair",
            "K_GK * [(J_GK_norm + sqrt(J_GK_norm^2 + 4 lambda_GK |Phi_boundary_GK+Q_top_GK|))/(2 lambda_GK)]",
            "local exterior residual units",
            "FINITE_BOUND_FORMULA_READY_VALUES_MISSING",
            "K_GK, lambda_GK, J_GK_norm, Phi_boundary_GK, Q_top_GK",
            "SRC4104_10_3586_gk_bound",
        ),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "status": status,
            "required_inputs": required,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, symbol, formula, units, status, required, source_key in entries
    ]


def epsilon_hair_rows() -> List[dict]:
    entries = [
        ("EHR4104_0_news", "epsilon_news", "integral_Iplus |N_AB|^2 duduOmega or local gravitational-wave energy flux through exterior boundary", "energy/time or normalized Hamiltonian residual", "MISSING_NUMERIC_OR_PARENT_ZERO", "SRC4104_07_3585_rows"),
        ("EHR4104_1_coercive_extra", "epsilon_coercive_extra", "epsilon_GK_hair + epsilon_bulk_memory_range_hair + remaining_named_coercive_channels", "field-energy or normalized source residual", "REFINED_BY_GK_CHANNEL_NONCLAIM", "SRC4104_10_3586_gk_bound"),
        ("EHR4104_2_cross", "epsilon_cross_hair", "uncancelled mixed A/Gamma/memory/operator cross-term bound", "field-energy or normalized source residual", "MISSING_CROSS_TERM_BOUND", "SRC4104_07_3585_rows"),
        ("EHR4104_3_top_boundary", "epsilon_top_boundary_hair", "absolute boundary/topological flux or relative cohomology charge not fixed by reference class", "boundary flux/source norm", "MISSING_TOPOLOGY_OR_BOUNDARY_FLUX_VALUE", "SRC4104_07_3585_rows"),
        ("EHR4104_4_projector", "epsilon_projector_hair", "norm((1-P_loc)delta Phi_hair) plus induced stress/source projection", "operator/stress norm", "MISSING_PROJECTOR_KERNEL_AUDIT", "SRC4104_07_3585_rows"),
        ("EHR4104_5_nonEH", "epsilon_nonEH_hair", "norm of retained R11/non-EH operator response in the local exterior", "PPN/source norm", "MISSING_EH_DOMINANCE_OR_NON_EH_VECTOR", "SRC4104_07_3585_rows"),
        ("EHR4104_6_hom_mode", "epsilon_hom_mode", "epsilon_news + epsilon_coercive_extra + epsilon_cross_hair + epsilon_top_boundary_hair + epsilon_projector_hair + epsilon_nonEH_hair", "same normalization as epsilon_Estat", "NO_CANCELLATION_HOM_STACK_READY_VALUES_MISSING", "SRC4104_07_3585_rows"),
        ("EHR4104_7_Estat", "epsilon_Estat", "epsilon_boundary_K + epsilon_source_K + epsilon_unique_ext + epsilon_hom_mode + epsilon_extra_hair", "same normalization as R_ann residual", "REFINED_NONCLAIM", "SRC4104_04_3584_stack"),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, symbol, definition, units, status, source_key in entries
    ]


def activation_gate_rows() -> List[dict]:
    entries = [
        ("GATE4104_0_sources", "all source checkpoints available", "PASS", "4103/3585/3586 sources found and parsed"),
        ("GATE4104_1_nohair_method", "energy-identity/coercivity no-hair method", "PASS_CONDITIONAL_THEOREM", "zero route written, not activated globally"),
        ("GATE4104_2_EH_news", "radiative EH zero", "PASS_IF_ZERO_NEWS_BOUNDARY_SIGNED", "gravitational news/no incoming boundary still parent-signed only conditionally"),
        ("GATE4104_3_GK_channel", "Gamma/Khat theorem-or-bound", "PASS_NONCLAIM_CHANNEL_FILLED", "GK has named formula but missing values"),
        ("GATE4104_4_escape_channels", "topology/projector/nonEH/cross escape channels", "FAIL_CURRENT_PUBLIC_CLAIM", "must be fixed, bounded or audited channel by channel"),
        ("GATE4104_5_Estat", "E_stat uniqueness/no-homogeneous-mode", "FAIL_CURRENT_PUBLIC_CLAIM", "epsilon_hom_mode and epsilon_extra_hair retained"),
        ("GATE4104_6_local_GR", "local GR/Newton/PPN", "FAIL_CURRENT_PUBLIC_CLAIM", "source coupling, GM calibration and PPN remain downstream"),
    ]
    return [
        {
            **row_base(),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status, detail in entries
    ]


def decision_rows() -> List[dict]:
    entries = [
        (
            "DEC4104_0_channelize",
            "accept the homogeneous-mode decomposition as canonical",
            "it prevents hidden exterior modes from being erased by one generic no-hair phrase",
            "future no-hair work is channel-by-channel",
            "CHANNEL_DECOMPOSITION_CANONICAL",
            "SRC4104_05_3585_theorem",
        ),
        (
            "DEC4104_1_GK_import",
            "import Gamma/Khat as the first concrete extra-hair theorem-or-bound channel",
            "3586 gives lambda_GK, J_GK, boundary and topology input slots plus epsilon_GK_hair formula",
            "coercive extra hair is no longer completely generic",
            "GK_CHANNEL_ADVANCED_NONCLAIM",
            "SRC4104_08_3586_gk_theorem",
        ),
        (
            "DEC4104_2_escape_guard",
            "retain topology, projector, cross-term and non-EH escapes",
            "local positivity cannot kill topological charges, hidden projector kernels or retained non-EH operators",
            "no public E_stat/no-hair claim",
            "ESCAPE_CHANNELS_RETAINED",
            "SRC4104_06_3585_audit",
        ),
        (
            "DEC4104_3_no_public_claim",
            "do not claim local GR/Newton/PPN/Maxwell completion",
            "E_stat, EM gauge corner, source coupling, GM calibration and PPN residuals remain open",
            "continue private derivation and bound filling",
            "PUBLIC_CLAIM_BLOCKED",
            "SRC4104_02_4103_flux",
        ),
        (
            "DEC4104_4_next",
            "attack GK parent inputs next",
            "the cleanest next move is to source/sign lambda_GK, J_GK_norm, Phi_boundary_GK and Q_top_GK rather than start another vague channel",
            "4105 targets GK parent coefficient/source/boundary owner or numeric bound inputs",
            "NEXT_TARGET_SELECTED",
            "SRC4104_11_3586_next",
        ),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, consequence, status, source_key in entries
    ]


def claim_gate_rows() -> List[dict]:
    entries = [
        ("CLAIM4104_0_EH_no_news", "radiative EH mode absent", "CONDITIONAL_ONLY", "requires zero-news/no-radiation boundary in same stationary branch", "parent no-news boundary"),
        ("CLAIM4104_1_GK_zero", "Gamma/Khat exterior hair zero", "BLOCKED", "lambda_GK/source/boundary/topology/kernel inputs not parent-signed", "GK input fill"),
        ("CLAIM4104_2_all_extra_hair", "all extra exterior hair zero", "BLOCKED", "topological, projector, cross and non-EH channels retained", "channel-by-channel zero or bounds"),
        ("CLAIM4104_3_Estat", "E_stat uniqueness/no-homogeneous-mode closes", "BLOCKED", "epsilon_hom_mode and epsilon_extra_hair are explicit but unfilled", "hair residual rows"),
        ("CLAIM4104_4_local_GR", "local GR/Newton/PPN recovery", "BLOCKED", "source coupling/GM calibration/PPN remain downstream", "source and PPN gates"),
    ]
    return [
        {
            **row_base(),
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "missing_gate": missing,
            "public_claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for claim_id, claim, status, reason, missing in entries
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4104_0",
            "target_doc": "4105-Y5-R2FR-GK-parent-coefficient-source-boundary-owner-or-numeric-bound-inputs.md",
            "target_script": "scripts/Y5_R2FR_4105_GK_parent_coefficient_source_boundary_owner_or_numeric_bound_inputs.py",
            "objective": "try to source/sign the concrete GK inputs lambda_GK, J_GK_norm, Phi_boundary_GK and Q_top_GK, or fill them as finite nonclaim rows with units",
            "success_gate": "GK channel becomes theorem-zero with parent-signed inputs, or epsilon_GK_hair has all finite bound terms populated with units and no missing markers",
            "reason": "4104 channelizes no-hair and imports the first concrete field-specific channel; filling GK inputs is now the sharpest non-generic next step",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4104_0",
            "decision": DECISION,
            "nohair_status": "homogeneous/extra exterior hair channelized; EH no-news and coercive zero routes conditional",
            "gk_status": "Gamma/Khat first field-specific theorem-or-bound channel imported; inputs still missing",
            "estat_status": "epsilon_hom_mode and epsilon_extra_hair retained in epsilon_Estat",
            "public_status": "no local_GR_Newton_Maxwell_PPN claim",
            "next_target": "4105 GK parent coefficient/source/boundary owner or numeric bound inputs",
            "valid_for_claim": "False",
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4104_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4104_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4104_NO_HOMOGENEOUS_MODE_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4104_NO_HOMOGENEOUS_MODE_THEOREM.csv",
        "P8_Y5_R2FR_4104_HAIR_CHANNEL_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4104_HAIR_CHANNEL_AUDIT.csv",
        "P8_Y5_R2FR_4104_GK_BOUND_INPUT_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4104_GK_BOUND_INPUT_ROWS.csv",
        "P8_Y5_R2FR_4104_EPSILON_HAIR_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4104_EPSILON_HAIR_ROWS.csv",
        "P8_Y5_R2FR_4104_ACTIVATION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4104_ACTIVATION_GATES.csv",
        "P8_Y5_R2FR_4104_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4104_DECISION_GATE.csv",
        "P8_Y5_R2FR_4104_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4104_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4104_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4104_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4104_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4104_STATUS.csv",
    }


def write_doc() -> None:
    lines = [
        "# 4104 - No homogeneous exterior mode or extra-hair epsilon row",
        "",
        "## Verdict",
        "4104 does not pretend to prove full no-hair. It does something more useful: it makes the exterior-hair problem channel-by-channel and imports the first concrete field-specific channel, `Gamma/Khat`.",
        "",
        "The homogeneous exterior split is now `delta Phi_hom = h_TT^rad + X_coercive + X_cross + X_top_boundary + X_projector + X_nonEH`. Radiative EH modes are killed only by a zero-news/no-radiation boundary. Coercive extra modes are killed only by a positive self-adjoint energy identity with zero source charge, zero boundary/topological flux and fixed gauge/projector kernel.",
        "",
        "For `Gamma/Khat`, the nonzero route is explicit: `epsilon_GK_hair = K_GK * [(J_GK_norm + sqrt(J_GK_norm^2 + 4 lambda_GK |Phi_boundary_GK+Q_top_GK|))/(2 lambda_GK)]`. That is a real bound contract, not a placeholder.",
        "",
        f"Decision: `{DECISION}`",
        "",
        "## What Advanced",
        "- `epsilon_hom_mode` is decomposed into physical channels rather than one vague row.",
        "- EH radiative hair has a zero-news/no-radiation theorem route.",
        "- Coercive extra hair has an energy-identity zero theorem route.",
        "- `Gamma/Khat` is now a concrete theorem-or-bound channel with `lambda_GK`, `J_GK_norm`, `Phi_boundary_GK`, and `Q_top_GK` inputs.",
        "",
        "## What Remains Live",
        "- `lambda_GK`, source charge, boundary flux, topology and projector/gauge kernel are not parent-signed.",
        "- Topological/boundary hair, projector-hidden hair, cross terms and non-EH operators remain explicit residual channels.",
        "- No local GR/Newton/Maxwell/PPN claim follows.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4104_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4104_NO_HOMOGENEOUS_MODE_THEOREM.csv`",
        "- `P8_Y5_R2FR_4104_HAIR_CHANNEL_AUDIT.csv`",
        "- `P8_Y5_R2FR_4104_GK_BOUND_INPUT_ROWS.csv`",
        "- `P8_Y5_R2FR_4104_EPSILON_HAIR_ROWS.csv`",
        "- `P8_Y5_R2FR_4104_ACTIVATION_GATES.csv`",
        "- `P8_Y5_R2FR_4104_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4104_CLAIM_GATE.csv`",
        "- `P8_Y5_R2FR_4104_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4104_STATUS.csv`",
        "- `P8_Y5_BRR545_4104_VALIDATION.csv`",
        "",
        "## Next target",
        "- `4105-Y5-R2FR-GK-parent-coefficient-source-boundary-owner-or-numeric-bound-inputs.md`",
        "- Objective: source/sign `lambda_GK`, `J_GK_norm`, `Phi_boundary_GK`, and `Q_top_GK`, or fill them as finite nonclaim rows with units.",
    ]
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4104_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4104_NO_HOMOGENEOUS_MODE_THEOREM"], no_homogeneous_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4104_HAIR_CHANNEL_AUDIT"], hair_channel_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4104_GK_BOUND_INPUT_ROWS"], gk_bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4104_EPSILON_HAIR_ROWS"], epsilon_hair_rows())
    write_csv(outputs["P8_Y5_R2FR_4104_ACTIVATION_GATES"], activation_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4104_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4104_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4104_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4104_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **row_base(),
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "valid_for_claim": "False",
            }
        )

    source_rows = source_register_rows()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "True"]
    missing_needles = [row["source_id"] for row in source_rows if row["contains_needle"] != "True"]
    add("VAL4104_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4104_1_sources_contain_needles", "every local source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_counts = {}
    parse_ok = True
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[name] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_counts[name] = f"ERROR:{exc}"
            parse_ok = False
    add("VAL4104_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    theorem_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4104_NO_HOMOGENEOUS_MODE_THEOREM"]))
    theorem_tokens = ["delta Phi_hom", "h_TT", "X_coercive", "Gamma/Khat", "lambda_GK", "Z_no_hom_mode"]
    missing_theorem = [token for token in theorem_tokens if token not in theorem_text]
    add("VAL4104_3_theorem_tokens", "no-homogeneous theorem contains split and GK route", not missing_theorem, ";".join(missing_theorem) or "all theorem tokens present")

    audit_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4104_HAIR_CHANNEL_AUDIT"]))
    audit_tokens = ["epsilon_news", "epsilon_GK_hair", "epsilon_cross_hair", "epsilon_top_boundary_hair", "epsilon_projector_hair", "epsilon_nonEH_hair", "epsilon_source_coupling"]
    missing_audit = [token for token in audit_tokens if token not in audit_text]
    add("VAL4104_4_channel_coverage", "hair audit covers all escape channels", not missing_audit, ";".join(missing_audit) or "all channel tokens present")

    gk_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4104_GK_BOUND_INPUT_ROWS"]))
    gk_tokens = ["lambda_GK", "J_GK_norm", "Phi_boundary_GK", "Q_top_GK", "epsilon_GK_hair"]
    missing_gk = [token for token in gk_tokens if token not in gk_text]
    add("VAL4104_5_GK_bound_contract", "GK bound rows expose required inputs", not missing_gk, ";".join(missing_gk) or "all GK tokens present")

    epsilon_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4104_EPSILON_HAIR_ROWS"]))
    epsilon_tokens = ["epsilon_hom_mode", "epsilon_Estat", "epsilon_coercive_extra", "epsilon_projector_hair", "epsilon_nonEH_hair"]
    missing_epsilon = [token for token in epsilon_tokens if token not in epsilon_text]
    add("VAL4104_6_epsilon_stack", "epsilon hair rows feed epsilon_Estat", not missing_epsilon, ";".join(missing_epsilon) or "all epsilon tokens present")

    claims = parse_csv(outputs["P8_Y5_R2FR_4104_CLAIM_GATE"])
    no_public_claim = all(row.get("public_claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    add("VAL4104_7_no_public_claims", "all claim rows remain nonpublic and nonclaim", no_public_claim, f"claim_rows={len(claims)}")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4104_NEXT_TARGET"])
    next_ok = any("4105-Y5-R2FR-GK-parent-coefficient-source-boundary-owner-or-numeric-bound-inputs.md" in row.get("target_doc", "") for row in next_rows)
    add("VAL4104_8_next_target", "next target fills GK parent inputs", next_ok, str(next_rows))

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    add("VAL4104_9_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4104_10_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4104_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
