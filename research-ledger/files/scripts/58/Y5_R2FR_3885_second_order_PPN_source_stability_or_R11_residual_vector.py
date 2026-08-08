from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3885"
BRANCH = "MTS_R2FR_Y5_SECOND_ORDER_PPN_SOURCE_STABILITY_OR_R11_VECTOR_3885"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3885-Y5-R2FR-second-order-PPN-source-stability-or-R11-residual-vector.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3884_NEXT = OUT / "P8_Y5_R2FR_3884_NEXT_TARGET.csv"
CSV_3884_ORBITAL = OUT / "P8_Y5_R2FR_3884_ORBITAL_NEWTON_READOUT_CHAIN.csv"
CSV_3884_RESIDUAL = OUT / "P8_Y5_R2FR_3884_MASS_GAUSS_RESIDUAL_BOUND_ROWS.csv"
CSV_3884_RUNNER = OUT / "P8_Y5_R2FR_3884_RUNNER_UPDATE.csv"
CSV_3884_VALIDATION = OUT / "P8_Y5_BRR545_3884_VALIDATION.csv"
CSV_SOURCE_STACK = OUT / "P8_source_normalized_Newton_branch_STACK.csv"
CSV_PG = OUT / "P8_PG_calibration_residual_MAP.csv"
CSV_BOUND_MATRIX = OUT / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv"
CSV_R11_STACK = OUT / "P8_R11_BOUNDARY_STRESS_THEOREM_STACK.csv"
CSV_R11_PROMOTION = OUT / "P8_R11_BOUNDARY_STRESS_PROMOTION_GATE.csv"
CSV_R11_FILL = OUT / "P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv"
CSV_LOCAL_EH_AUDIT = OUT / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv"
CSV_LOCAL_EH_SELECTOR = OUT / "P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv"
CSV_LOCAL_EH_DECISION = OUT / "P8_LOCAL_EH_R11_DECISION.csv"
CSV_R11_ROUTE = OUT / "P8_R11_SOURCE_NORMALIZATION_THEOREM_OR_NUMERIC_ROUTE.csv"
CSV_R11_MIN_FILL = OUT / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"
CSV_R11_ACCEPT = OUT / "P8_R11_SOURCE_NORMALIZATION_ACCEPTANCE_GATES.csv"
CSV_R11_MISSING = OUT / "P8_R11_SOURCE_NORMALIZATION_MISSING_LEDGER.csv"
CSV_DELTA_BETA = OUT / "P8_Y5_DELTA_BETA_SOURCE_DERIVATION.csv"
CSV_DELTA_BETA_REQ = OUT / "P8_Y5_DELTA_BETA_INPUT_REQUIREMENTS.csv"
CSV_DELTA_BETA_R11 = OUT / "P8_Y5_DELTA_BETA_R11_LINK.csv"
CSV_DELTA_BETA_DECISION = OUT / "P8_Y5_DELTA_BETA_DECISION.csv"
CSV_BETA_ENV = OUT / "P8_Y5_BETA_ENVELOPE_COMPONENTS.csv"
CSV_BETA_TEMPLATE = OUT / "P8_Y5_BETA_ENVELOPE_INPUT_TEMPLATE.csv"
CSV_BETA_FILL = OUT / "P8_Y5_BETA_COEFFICIENT_FILL_INPUT.csv"
CSV_BETA_DEMOTION = OUT / "P8_Y5_BETA_DEMOTION_RESIDUAL_ROW.csv"
CSV_GR_PPN = OUT / "P8_Y5_GR_LEFT_HAND_GATE_2619_PPN_BRIDGE_LEDGER.csv"
CSV_GR_OP = OUT / "P8_Y5_GR_LEFT_HAND_GATE_2619_OPERATOR_RESIDUAL_PACK.csv"
CSV_EH_DOM = OUT / "P8_Y5_EH_DOMINANCE_GATE_2620_OPERATOR_COEFFICIENT_PACK.csv"
CSV_LOVELOCK = OUT / "P8_Y5_LOVELOCK_GATE_2622_OPERATOR_SELECTION_VERDICT.csv"
CSV_HCORE = OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv"
CSV_GPT = OUT / "P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3885_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv",
    "r11": OUT / "P8_Y5_R2FR_3885_R11_OPERATOR_RESIDUAL_VECTOR.csv",
    "ppn": OUT / "P8_Y5_R2FR_3885_PPN_PARAMETER_RESIDUAL_ROWS.csv",
    "gate": OUT / "P8_Y5_R2FR_3885_LOCAL_GR_PROMOTION_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3885_RUNNER_UPDATE.csv",
    "next": OUT / "P8_Y5_R2FR_3885_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3885_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3885_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3885_00_next", CSV_3884_NEXT, "NEXT3884_0", "3884 selected PPN/R11 target"),
    ("SRC3885_01_not_GR", CSV_3884_ORBITAL, "ORB3884_3_not_GR", "Newton is not local GR"),
    ("SRC3885_02_PPN_resid", CSV_3884_RESIDUAL, "MGR3884_6_PPN", "PPN residual row"),
    ("SRC3885_03_runner_no_GR", CSV_3884_RUNNER, "RUNU3884_4_no_GR", "no local GR runner guard"),
    ("SRC3885_04_valid", CSV_3884_VALIDATION, "VAL3884_15_next_target", "3884 validation"),
    ("SRC3885_05_SN1", CSV_SOURCE_STACK, "SN1_EH_or_R11_operator_zero", "EH/R11 operator zero rung"),
    ("SRC3885_06_SN11", CSV_SOURCE_STACK, "SN11_second_order_PPN_source_stability", "second-order PPN rung"),
    ("SRC3885_07_PG9", CSV_PG, "PG9_second_order_source_stability", "PG9 PPN source stability"),
    ("SRC3885_08_bound_beta", CSV_BOUND_MATRIX, "P8_nonlinear_beta_source_residue", "beta residual bound"),
    ("SRC3885_09_R11_T3", CSV_R11_STACK, "T3_local_EH_R11_selector", "local EH/R11 selector theorem"),
    ("SRC3885_10_R11_T4", CSV_R11_STACK, "T4_projector_stress_Bianchi", "projector stress/Bianchi"),
    ("SRC3885_11_R11_T6", CSV_R11_STACK, "T6_channel_guard", "R11 channel guard"),
    ("SRC3885_12_R11_G3", CSV_R11_PROMOTION, "G3_R11_EH_operator", "R11 EH operator promotion gate"),
    ("SRC3885_13_R11_G4", CSV_R11_PROMOTION, "G4_stress_Bianchi", "stress Bianchi promotion gate"),
    ("SRC3885_14_R11_F0", CSV_R11_FILL, "F0_boundary_alpha3", "boundary alpha3 fill"),
    ("SRC3885_15_R11_F5", CSV_R11_FILL, "F5_R11_source_normalization", "R11 source normalization fill"),
    ("SRC3885_16_R11_F6", CSV_R11_FILL, "F6_projector_stress", "projector stress fill"),
    ("SRC3885_17_EH_audit_R2", CSV_LOCAL_EH_AUDIT, "R2_fR_scalar_mode", "R2/fR scalar mode"),
    ("SRC3885_18_EH_audit_vector", CSV_LOCAL_EH_AUDIT, "vector_preferred_frame", "preferred-frame vector audit"),
    ("SRC3885_19_EH_selector_L2", CSV_LOCAL_EH_SELECTOR, "L2_double_zero_sufficient", "double-zero selector lemma"),
    ("SRC3885_20_EH_selector_L4", CSV_LOCAL_EH_SELECTOR, "L4_selector_theorem_target", "selector theorem target"),
    ("SRC3885_21_EH_decision", CSV_LOCAL_EH_DECISION, "D2_actual_R11_rows", "actual R11 rows not selected"),
    ("SRC3885_22_R11_route", CSV_R11_ROUTE, "T1_numeric_vector", "numeric R11 vector route"),
    ("SRC3885_23_R11_min_R2", CSV_R11_MIN_FILL, "R11SN_4_nonEH_operator_potential", "nonEH operator potential row"),
    ("SRC3885_24_R11_min_domain", CSV_R11_MIN_FILL, "R11SN_2_domain_projector_mass", "domain projector mass row"),
    ("SRC3885_25_R11_accept", CSV_R11_ACCEPT, "G5_no_promotion", "R11 no promotion gate"),
    ("SRC3885_26_R11_missing", CSV_R11_MISSING, "R11SN_4_nonEH_operator_potential", "R11 missing operator row"),
    ("SRC3885_27_beta_law", CSV_DELTA_BETA, "DB525_2_extract_beta", "beta extraction law"),
    ("SRC3885_28_beta_resid", CSV_DELTA_BETA, "DB525_3_beta_residual", "beta residual law"),
    ("SRC3885_29_beta_split", CSV_DELTA_BETA, "DB525_6_R11_and_q_loc_split", "beta split law"),
    ("SRC3885_30_beta_req_source", CSV_DELTA_BETA_REQ, "BI525_2_delta_beta_source", "delta beta source input"),
    ("SRC3885_31_beta_req_R11", CSV_DELTA_BETA_REQ, "BI525_3_delta_beta_R11", "delta beta R11 input"),
    ("SRC3885_32_beta_R11_link", CSV_DELTA_BETA_R11, "source_normalization_operator", "beta R11 link"),
    ("SRC3885_33_beta_decision", CSV_DELTA_BETA_DECISION, "D525_3_R11_or_q_loc_fill_required", "beta fill required"),
    ("SRC3885_34_beta_env_q", CSV_BETA_ENV, "ENV531_3_q_loc", "q_loc beta component"),
    ("SRC3885_35_beta_template_R11", CSV_BETA_TEMPLATE, "IN531_1_R11", "R11 beta input template"),
    ("SRC3885_36_beta_fill", CSV_BETA_FILL, "BETA526_0_source_AB", "beta coefficient fill input"),
    ("SRC3885_37_beta_demote", CSV_BETA_DEMOTION, "BD527_5_total_beta_envelope", "total beta envelope"),
    ("SRC3885_38_GR_gamma", CSV_GR_PPN, "PPN2619_0_gamma", "gamma bridge ledger"),
    ("SRC3885_39_GR_beta", CSV_GR_PPN, "PPN2619_1_beta", "beta bridge ledger"),
    ("SRC3885_40_GR_pref", CSV_GR_PPN, "PPN2619_2_preferred_frame", "preferred-frame ledger"),
    ("SRC3885_41_GR_op", CSV_GR_OP, "ORP2619_0_E_LHS_GR_residual", "operator residual pack"),
    ("SRC3885_42_EH_delta", CSV_EH_DOM, "OPC2620_7_total_DeltaE", "total DeltaE operator pack"),
    ("SRC3885_43_lovelock", CSV_LOVELOCK, "OPS2622_4_overall", "Lovelock verdict"),
    ("SRC3885_44_Hcore_beta", CSV_HCORE, "LAW2576_6_beta", "Hcore beta law"),
    ("SRC3885_45_GPT_beta", CSV_GPT, "GPT540_4_beta_source_stability", "Hamiltonian PiM Gauss beta test"),
    ("SRC3885_46_GPT_ppn", CSV_GPT, "GPT540_5_full_PPN_vector", "full PPN vector test"),
]

PPN_THEOREM = (
    "If the 3882-3884 candidate branch is globally adopted, the compact local exterior is EH-only through O(U^2), "
    "G0 is constant, the same Hilbert source is used, PiM/Gauss calibration is closed, and all R11/projector/boundary/domain/readout stresses vanish, "
    "then the standard GR PPN expansion follows: gamma=1, beta=1, alpha1=alpha2=alpha3=xi=zeta_i=0."
)

BETA_LAW = "beta_eff = B_source/A_source^2; delta_beta_source = B_source/A_source^2 - 1"

R11_SUM = (
    "Delta_PPN_abs <= |delta_gamma_R11|+|delta_beta_source|+|delta_beta_R11|+"
    "|delta_beta_q_loc|+|delta_beta_boundary_domain|+|delta_beta_readout|+"
    "|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns) + " |")
    return "\n".join(lines)


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_second_order_PPN_R11_gate",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("PPT3885_0_target", "local-GR PPN theorem target", PPN_THEOREM, "EXACT_CONDITIONAL_GR_LIMIT", "would promote first-order Newton to local GR if all premises are parent-signed"),
        ("PPT3885_1_gamma", "gamma condition", "EH-only spatial and temporal weak-field potentials satisfy Psi=Phi, hence gamma-1=0.", "CONDITIONAL_ON_EH_ONLY_AND_READOUT", "blocked by DeltaE/R11/frame/readout rows"),
        ("PPT3885_2_beta", "beta condition", BETA_LAW + "; GR requires B_source=A_source^2 after all source/operator/readout splits.", "EXACT_BETA_LAW_INPUTS_MISSING", "prevents constant-GM absorption from faking beta"),
        ("PPT3885_3_preferred_frame", "preferred-frame condition", "No independent local vector/domain/coframe/memory marker through O(U^2) implies alpha1=alpha2=alpha3=0.", "CONDITIONAL_ON_NO_VECTOR_SELECTOR", "domain/boundary/projector alpha rows remain live"),
        ("PPT3885_4_conservation", "conservation condition", "No extra non-Hilbert stress/source leakage plus Bianchi conservation implies zeta_i=0 in the candidate GR branch.", "CONDITIONAL_ON_TOTAL_STRESS_CLOSURE", "extra stress and nonconservation rows remain live"),
        ("PPT3885_5_verdict", "current verdict", "3885 writes the theorem route and residual vector; current corpus still has R11/operator/source/readout rows unsigned, so no local-GR claim.", "NONCLAIM_THEOREM_OR_VECTOR", "next step must derive EH-only/R11 selector or fill executable coefficients"),
    ]
    return [
        {
            "theorem_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "remaining_gate": gate,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, gate in raw_rows
    ]


def r11_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("R11V3885_0_total", "DeltaE_munu", "total non-Einstein left-hand residual", "sum_i c_i O_i_munu", "PPN gamma,beta,R10,clocks,orbits", "EH-only theorem or executable coefficient vector", "OPEN"),
        ("R11V3885_1_higher_curvature", "c_R2;c_Ricci;c_Weyl", "higher-curvature/f(R)/Weyl corrections", "delta_gamma_R11;delta_beta_R11;alpha(lambda)", "R3;R4;R10;R11", "double-zero/topological silence or coefficients", "OPEN"),
        ("R11V3885_2_scalar_tensor", "F_phi_C;c_scalar", "scalar/class field metric response", "gamma_minus_1;beta_minus_1;Gdot;R10", "R2;R3;R4;R9;R10;R11", "fixed scalar or coefficient bound", "OPEN"),
        ("R11V3885_3_preferred_frame", "c_domain_vector", "domain/vector/coframe selector", "alpha1;alpha2;alpha3;xi", "R5;R6;R7;R8;R11", "no-vector selector theorem or numeric products", "OPEN"),
        ("R11V3885_4_boundary_domain", "W_boundary;W_domain", "boundary/domain/projector stress", "alpha3;xi;delta_beta_boundary_domain", "R7;R8;R11", "scalar no-flux/topological theorem or coefficient map", "OPEN"),
        ("R11V3885_5_projector", "T_extra_munu_or_c_projector_domain_stress", "PiM/projector/domain stress", "gamma;beta;preferred-frame;source-normalization", "R3;R4;R5;R6;R7;R8;R11", "metric-independent topological PiM or retained stress score", "OPEN"),
        ("R11V3885_6_nonlocal_memory", "c_nonlocal;K_history", "nonlocal/history memory tail", "beta;preferred-frame;clock/orbital hysteresis", "R7;R9;R10;R11", "compact-local silence or kernel bound", "OPEN"),
        ("R11V3885_7_source_norm", "c_domain_source_normalization_operator", "source-normalization operator family", "delta_beta_source;radial hair;alpha(lambda);operator ledger", "R4;R10;R11", "measured-GM theorem or executable vector", "OPEN"),
    ]
    return [
        {
            "r11_id": row_id,
            "symbol": symbol,
            "meaning": meaning,
            "map_to_ppn_or_test": mapping,
            "affected_rows": affected,
            "closure_condition": close,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, meaning, mapping, affected, close, status in raw_rows
    ]


def ppn_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("PPN3885_0_gamma", "gamma_minus_1", "dimensionless", "delta_gamma_R11 + delta_gamma_readout + delta_gamma_frame + delta_gamma_source", "0 if EH-only same-readout theorem holds", "MISSING_EH_ONLY_OR_GAMMA_VECTOR", "R3_gamma;R11"),
        ("PPN3885_1_beta", "beta_minus_1", "dimensionless", "delta_beta_source + delta_beta_R11 + delta_beta_q_loc + delta_beta_boundary_domain + delta_beta_readout", "abs <= 7.8e-05 or theorem-zero", "MISSING_A_B_AND_COMPONENT_VECTOR", "R4_beta"),
        ("PPN3885_2_alpha1", "alpha1", "dimensionless", "alpha1_domain + alpha1_frame + alpha1_vector + alpha1_memory", "abs <= 1e-04 or theorem-zero", "MISSING_NO_VECTOR_SELECTOR_OR_COEFFICIENT", "R5_alpha1"),
        ("PPN3885_3_alpha2", "alpha2", "dimensionless", "alpha2_domain + alpha2_frame + alpha2_vector + alpha2_memory", "abs <= 2e-09 or theorem-zero", "MISSING_NO_VECTOR_SELECTOR_OR_COEFFICIENT", "R6_alpha2"),
        ("PPN3885_4_alpha3", "alpha3", "dimensionless", "alpha3_boundary + alpha3_domain + alpha3_flux + alpha3_nonconservation", "abs <= 4e-20 or theorem-zero", "MISSING_INDIVIDUAL_ALPHA3_CHANNELS", "R7_alpha3"),
        ("PPN3885_5_xi", "xi", "dimensionless", "xi_domain + xi_boundary + xi_anisotropy + xi_nonlocal", "abs <= 4e-09 or theorem-zero", "MISSING_ANISOTROPY_STF_ZERO_OR_COEFFICIENT", "R8_xi"),
        ("PPN3885_6_zeta", "zeta_i", "dimensionless", "stress nonconservation / non-Hilbert source leakage components", "zero by total stress conservation or explicit bounds", "MISSING_EXTRA_STRESS_CONSERVATION_VECTOR", "PPN_conservation"),
        ("PPN3885_7_yukawa", "alpha(lambda)", "range-dependent", "finite-range source/R11/bulk-X tail", "verified alpha(lambda) curve or no-range theorem", "MISSING_EXECUTABLE_R10_CURVE_OR_NO_RANGE_THEOREM", "R10"),
        ("PPN3885_8_total", "Delta_PPN_abs", "dimensionless_envelope", R11_SUM, "every component theorem-zero or bounded with no cancellation", "NOT_RUN_COMPONENTS_MISSING", "local_GR_gate"),
    ]
    return [
        {
            "ppn_id": row_id,
            "parameter": parameter,
            "units": units,
            "formula_or_decomposition": formula,
            "target_or_bound": bound,
            "current_status": status,
            "observable_link": link,
            "valid_prediction_row": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, parameter, units, formula, bound, status, link in raw_rows
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("LGG3885_0_first_order", "first-order Newton bridge", "3882-3884 candidate ladder supplies constant coupling, same Hilbert source, Gauss monopole and slow readout", "PASS_CANDIDATE_NONCLAIM"),
        ("LGG3885_1_EH_only", "EH-only exterior through O(U^2)", "all non-EH R11 families absent, topological, double-zero, or executable-bounded", "FAIL_R11_VECTOR_OPEN"),
        ("LGG3885_2_beta", "beta source stability", "A_source and B_source filled and B_source=A_source^2 or beta residual below lock", "FAIL_A_B_MISSING"),
        ("LGG3885_3_gamma", "gamma spatial/temporal equality", "DeltaE and readout/frame residuals zero or bounded", "FAIL_GAMMA_VECTOR_OPEN"),
        ("LGG3885_4_preferred", "preferred-frame/conservation rows", "alpha1,alpha2,alpha3,xi,zeta_i all zero/bounded individually", "FAIL_VECTOR_OPEN"),
        ("LGG3885_5_local_GR", "local-GR promotion", "all above gates pass simultaneously with no cancellation", "BLOCKED_NO_CLAIM"),
    ]
    return [
        {
            "gate_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3885_0_PPN", "b_PPN_readout", "b_PPN_readout := |gamma-1|+|beta-1|+|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|+|alpha(lambda)|", "PPN_VECTOR_EXPLICIT"),
        ("RUNU3885_1_R11", "b_R11_operator", "b_R11_operator := sum over active R11 coefficient/operator weak-field maps, with no cancellation credit", "R11_VECTOR_EXPLICIT"),
        ("RUNU3885_2_beta", "delta_beta_total", "delta_beta_total := delta_beta_source+delta_beta_R11+delta_beta_q_loc+delta_beta_boundary_domain+delta_beta_readout", "BETA_SPLIT_EXPLICIT"),
        ("RUNU3885_3_localGR", "local_GR_claim", "false until first-order Newton gates plus all PPN/R11 rows are theorem-zero or source-backed bounded", "NO_LOCAL_GR_CLAIM"),
        ("RUNU3885_4_next", "next attack", "derive EH-only/R11 selector or fill executable PPN/R11 coefficient vector", "NEXT_3886"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, status in raw_rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3885_0",
            "target_checkpoint": "3886-Y5-R2FR-EH-only-R11-selector-or-executable-PPN-coefficient-vector.md",
            "script": "scripts/Y5_R2FR_3886_EH_only_R11_selector_or_executable_PPN_coefficient_vector.py",
            "objective": "try to derive the EH-only/R11 double-zero selector across active local operator families; if it fails, build the executable PPN/R11 coefficient vector with units, source paths, weak-field maps and no missing fields",
            "why_next": "3885 shows the candidate first-order Newton branch cannot be promoted to local GR until R11/PPN rows are actually zeroed or numerically bounded",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3885_0",
            "branch": BRANCH,
            "summary": "conditional GR PPN theorem written; beta law and full PPN/R11 residual vector emitted; first-order Newton candidate remains, local-GR promotion blocked until EH-only/R11 selector or executable coefficient vector closes",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    r11: list[dict[str, object]],
    ppn: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3885 - Second-Order PPN Source Stability or R11 Residual Vector

Generated: `{timestamp}`

## Result

3885 tests whether the first-order Newton candidate can promote to local GR.

`{PPN_THEOREM}`

The key nonlinear source-normalization law is:

`{BETA_LAW}`

So a fitted first-order `GM` is not enough. The quadratic source response must square the first-order response, and every non-EH/operator/readout contribution must either vanish by theorem or enter the PPN/R11 vector.

## Conditional PPN Theorem

{markdown_table(theorem, ["theorem_id", "piece", "statement", "status", "remaining_gate"])}

## R11 Operator Residual Vector

{markdown_table(r11, ["r11_id", "symbol", "meaning", "map_to_ppn_or_test", "closure_condition", "current_status"])}

## PPN Parameter Residual Rows

{markdown_table(ppn, ["ppn_id", "parameter", "formula_or_decomposition", "target_or_bound", "current_status"])}

## Local-GR Promotion Gate

{markdown_table(gate, ["gate_id", "gate", "requirement", "status", "claim_allowed"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3885 does not kill the theory; it draws the real local-GR line. The branch has a credible first-order Newton ladder, but local GR now depends on the EH-only/R11 selector or an executable PPN coefficient vector. The next move is not another broad audit: it is R11 selector proof or coefficient fill.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3885 SECOND ORDER PPN R11 -->"
    end = "<!-- END 3885 SECOND ORDER PPN R11 -->"
    block = f"""{start}

## 3885 - Second-order PPN/R11 local-GR gate

Conditional theorem:

`{PPN_THEOREM}`

Beta law:

`{BETA_LAW}`

PPN/R11 no-cancellation envelope:

`{R11_SUM}`

Candidate status: first-order Newton survives as a candidate branch; local GR is blocked until gamma, beta, preferred-frame, conservation, Yukawa/range and R11 operator rows are theorem-zero or source-backed bounded.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3885_SECOND_ORDER_PPN_EH_STABILITY_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3885_R11_OPERATOR_RESIDUAL_VECTOR.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3885_PPN_PARAMETER_RESIDUAL_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3885_VALIDATION.csv`

Next gate: `3886`, EH-only/R11 selector or executable PPN coefficient vector.

<!-- Generated by 3885 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    r11: list[dict[str, object]],
    ppn: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3885_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3885_1_theorem", "conditional PPN theorem exists", any(row["theorem_id"] == "PPT3885_0_target" and "gamma=1" in str(row["statement"]) for row in theorem), "PPT3885_0"))
    checks.append(("VAL3885_2_beta_law", "beta law is explicit", any(row["theorem_id"] == "PPT3885_2_beta" and "B_source/A_source^2" in str(row["statement"]) for row in theorem), "PPT3885_2"))
    required_r11 = {"DeltaE_munu", "c_R2;c_Ricci;c_Weyl", "c_domain_vector", "T_extra_munu_or_c_projector_domain_stress", "c_domain_source_normalization_operator"}
    checks.append(("VAL3885_3_r11_vector", "R11 vector covers key operator families", required_r11.issubset({str(row["symbol"]) for row in r11}), "key R11 symbols"))
    required_ppn = {"gamma_minus_1", "beta_minus_1", "alpha1", "alpha2", "alpha3", "xi", "zeta_i", "alpha(lambda)", "Delta_PPN_abs"}
    checks.append(("VAL3885_4_ppn_rows", "PPN rows cover gamma beta preferred frame conservation range", required_ppn.issubset({str(row["parameter"]) for row in ppn}), "required PPN symbols"))
    checks.append(("VAL3885_5_local_gr_blocked", "local GR promotion gate is blocked", any(row["gate_id"] == "LGG3885_5_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3885_5"))
    checks.append(("VAL3885_6_runner", "runner has PPN vector", any(row["runner_field"] == "b_PPN_readout" for row in runner), "b_PPN_readout"))
    checks.append(("VAL3885_7_no_claim", "all promotion gates are nonclaim", all(str(row["claim_allowed"]) == "False" for row in gate), "claim_allowed=false"))
    checks.append(("VAL3885_8_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "real local-GR line" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3885_9_spine", "spine updated with 3885 block", SPINE_PATH.exists() and "BEGIN 3885 SECOND ORDER PPN R11" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3885_10_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    generated_patterns = ("3885-Y5", "P8_Y5_R2FR_3885", "P8_Y5_BRR545_3885")
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3885*")
            if path.is_file() and any(pattern in path.name for pattern in generated_patterns)
        ]
    checks.append(("VAL3885_11_formalization_untouched", "no generated 3885 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3885_12_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3885_13_all_nonclaim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [theorem, r11, ppn, gate, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3885_14_next_target", "next target attacks EH/R11 selector or executable vector", any("EH-only-R11-selector" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3886 EH/R11"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    r11 = r11_rows(timestamp)
    ppn = ppn_rows(timestamp)
    gate = promotion_gate_rows(timestamp)
    runner = runner_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["r11"], r11)
    write_csv(OUTPUTS["ppn"], ppn)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, r11, ppn, gate, runner, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, r11, ppn, gate, runner, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_SECOND_ORDER_PPN_R11_GATE")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
