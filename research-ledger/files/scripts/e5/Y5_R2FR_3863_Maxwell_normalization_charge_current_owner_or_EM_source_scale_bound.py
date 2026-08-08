from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3863"
BRANCH = "MTS_R2FR_Y5_MAXWELL_NORMALIZATION_CHARGE_CURRENT_OWNER_OR_EM_SOURCE_SCALE_BOUND_3863"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3863-Y5-R2FR-Maxwell-normalization-charge-current-owner-or-EM-source-scale-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3862_THEOREM = OUT / "P8_Y5_R2FR_3862_EM_HODGE_ZERO_THEOREM.csv"
CSV_3862_BOUND = OUT / "P8_Y5_R2FR_3862_EM_HODGE_OBSERVABLE_BOUND.csv"
CSV_3862_GATES = OUT / "P8_Y5_R2FR_3862_CLAIM_GATES.csv"
CSV_3862_VALIDATION = OUT / "P8_Y5_BRR545_3862_VALIDATION.csv"
CSV_3809_NORM = OUT / "P8_Y5_R2FR_3809_MAXWELL_NORMALIZATION_THEOREM.csv"
CSV_3464_ALPHA = OUT / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv"
CSV_3650_CURRENT = OUT / "P8_Y5_R2FR_3650_CHARGE_CURRENT_CLAUSE_AUDIT.csv"
CSV_CHARGE_CURRENT_RES = OUT / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv"
CSV_1812_ALPHA_LEVEL = OUT / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv"
CSV_765_KINETIC = OUT / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv"
CSV_1057_UNIQUE = OUT / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv"
CSV_3621_PACKET = OUT / "P8_Y5_joint_TQ_NQ_JQ_owner_packet_status.csv"
CSV_3119_DELTAJ = OUT / "P8_Y5_R2FR_3119_SAME_CURRENT_OWNER_DELTAJ_GATE.csv"
CSV_3143_CURRENT = OUT / "P8_Y5_R2FR_3143_SAME_CURRENT_OWNER_THEOREM.csv"
CSV_3781_ZEM = OUT / "P8_Y5_R2FR_3781_ZEM_ALPHA_OWNER_GUARD.csv"
CSV_3503_BOUND = OUT / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"
CSV_3503_OWNER = OUT / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv"
CSV_3465_OWNER = OUT / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv"
CSV_3463_POYNTING = OUT / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"
CSV_3343_MAXWELL = OUT / "P8_Y5_R2FR_3343_PUBLIC_MAXWELL_ACTION_DERIVATION.csv"
CSV_3116_LOCK = OUT / "P8_Y5_R2FR_3116_PUBLIC_HODGE_MAXWELL_STRESS_LOCK.csv"
CSV_2340_CHARGE = OUT / "P8_Y5_PARENT_QLOC_2340_PARENT_CHARGE_EXTRACTION_SPINE.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3863_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv",
    "audit": OUT / "P8_Y5_R2FR_3863_CHARGE_CURRENT_SLOT_AUDIT.csv",
    "bound": OUT / "P8_Y5_R2FR_3863_EM_SOURCE_SCALE_BOUND.csv",
    "gates": OUT / "P8_Y5_R2FR_3863_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3863_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3863_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3863_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3863_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3863_00_3862_theorem", CSV_3862_THEOREM, "NEXT_GATE_IS_MAXWELL_NORMALIZATION_AND_CHARGE_CURRENT_OWNER", "3862 coupling handoff"),
    ("SRC3863_01_3862_bound", CSV_3862_BOUND, "B_EM_scale_3862", "3862 EM source scale gate"),
    ("SRC3863_02_3862_gates", CSV_3862_GATES, "PASS_3863_MAXWELL_NORMALIZATION_CHARGE_CURRENT_TARGET", "3862 next-target gate"),
    ("SRC3863_03_3862_validation", CSV_3862_VALIDATION, "PASS", "previous validation"),
    ("SRC3863_04_3809_norm", CSV_3809_NORM, "MNT3809_4_ZQeff_descent", "Maxwell normalization descent theorem"),
    ("SRC3863_05_3809_verdict", CSV_3809_NORM, "MNT3809_6_strict_verdict", "strict current Maxwell normalization verdict"),
    ("SRC3863_06_3464_alpha", CSV_3464_ALPHA, "EAC3464_0_gauge_rescaling", "gauge rescaling redundancy"),
    ("SRC3863_07_3464_verdict", CSV_3464_ALPHA, "EAC3464_5_verdict", "EM action normalization verdict"),
    ("SRC3863_08_3650_current", CSV_3650_CURRENT, "SCA3650_0_TQ_same_owner", "same T_Q owner audit"),
    ("SRC3863_09_3650_total", CSV_3650_CURRENT, "SCA3650_6_total", "source-current total closure"),
    ("SRC3863_10_charge_current_residual", CSV_CHARGE_CURRENT_RES, "Delta_G", "source charge residual decomposition"),
    ("SRC3863_11_1812_alpha_level", CSV_1812_ALPHA_LEVEL, "ALO1812_5_verdict", "alpha level owner verdict"),
    ("SRC3863_12_765_kinetic", CSV_765_KINETIC, "MKI765_2_unique_F2", "Maxwell kinetic inheritance gate"),
    ("SRC3863_13_1057_unique", CSV_1057_UNIQUE, "UMS1057_5_verdict", "unique Maxwell subblock verdict"),
    ("SRC3863_14_3621_packet", CSV_3621_PACKET, "lambda_F2;b_alpha;kappa_J;w_EM;Phi_EM_boundary", "joint TQ/NQ/JQ packet status"),
    ("SRC3863_15_3119_deltaJ", CSV_3119_DELTAJ, "SCJ3119_0", "same-current owner deltaJ gate"),
    ("SRC3863_16_3143_current", CSV_3143_CURRENT, "SCOT3143_3_same_current_owner", "same-current owner theorem"),
    ("SRC3863_17_3781_ZEM", CSV_3781_ZEM, "ZOG3781_2_norm_owner", "Z_EM norm owner guard"),
    ("SRC3863_18_3503_bound", CSV_3503_BOUND, "EMB3503_1_w_EM", "EM current owner bound vector"),
    ("SRC3863_19_3503_owner", CSV_3503_OWNER, "OHM3503_2_charge_current_owner", "observed Hodge charge/current owner"),
    ("SRC3863_20_3465_owner", CSV_3465_OWNER, "EMO3465_5_verdict", "EM owner package verdict"),
    ("SRC3863_21_3463_poynting", CSV_3463_POYNTING, "EM3463_4_multiplier_obstruction", "Poynting multiplier obstruction"),
    ("SRC3863_22_3343_maxwell", CSV_3343_MAXWELL, "EMD3343_2_current_variation", "public Maxwell current variation"),
    ("SRC3863_23_3116_lock", CSV_3116_LOCK, "EMH3116_4", "same current owner lock"),
    ("SRC3863_24_2340_charge", CSV_2340_CHARGE, "PCS2340_7_local_limit", "local source-charge limit"),
]

RESCALING_NORMAL_FORM = (
    "For S_EM=-1/4 int Z_Q F_Q wedge *_obs F_Q + int A_Q_mu J_Q^mu, "
    "the constant field redefinition A_Q' = s A_Q sends Z_Q' = Z_Q/s^2 and J_Q' = J_Q/s. "
    "Thus Maxwell equations alone fix only a convention class; a parent-owned norm/lattice/current owner is needed to make Z_Q and J_Q physical source data."
)
OWNER_THEOREM = (
    "If T_Q is a parent generator with fixed nonrescalable fibre norm N_Q, the parent curvature coefficient C_P is q-basic, "
    "the visible action excludes independent lambda_A F_Q^2/f_X F_Q^2 terms, matter charges are fixed representation/lattice labels, "
    "J_Q is extracted by variation before readout from the same A_Q, and radiative/readout/current re-entry is absent or q-basic, "
    "then D_v ln Z_Q_eff = D_v ln J_Q = D_v ln alpha_EM = 0 along ker(Dq_obs), and the EM source-scale residual vanishes locally."
)
ABSOLUTE_VALUE_GUARD = (
    "This theorem can give local drift/source-coupling silence without predicting the numerical value of alpha_EM or mu0; an absolute prediction requires C_P, N_Q, hbar/c conventions and charge units to be derived, not calibrated."
)
CURRENT_BLOCK = (
    "The current corpus has exact conditional routes, but does not parent-sign C_P/N_Q, no-extra-F2, same-current owner, alpha/readout radiative closure, EM binding/source sensitivity, or boundary Poynting flux silence."
)
Z_BOUND = (
    "b_Z := |D_v ln Z_Q_eff| <= b_CP+b_NQ+b_lambdaF2+b_hiddenF2+b_rad+b_readout"
)
J_BOUND = (
    "b_J := |D_v ln J_Q| <= b_TQ_norm+b_charge_lattice+b_current_measure+b_material_marker+b_current_readout+b_boundary_current"
)
SOURCE_SCALE_BOUND = (
    "B_EM_scale_3863 <= b_Z+b_J+|b_alpha|+|w_EM|+|C_XF2|+|C_JQ|+|Delta_M_EM_binding|+|Phi_EM_boundary|/(G_ref M_H)"
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


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
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
                "claim_use": "nonclaim_Maxwell_normalization_charge_current_derivation",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "MNO3863_0_rescaling_normal_form",
            "claim_piece": "Maxwell normalization gauge/convention split",
            "statement": RESCALING_NORMAL_FORM,
            "derivation": "Direct substitution of A_Q'=s A_Q into the kinetic and source terms.",
            "result": "EXACT_RESCALING_NORMAL_FORM",
            "status": "CONVENTION_GUARD_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MNO3863_1_parent_subblock_owner",
            "claim_piece": "parent Maxwell coefficient candidate",
            "statement": "If the parent curvature norm contains -C_P/4 int <F_parent,F_parent>_P and F_parent=F_Q T_Q+F_perp, then the visible Q subblock has Z_parent=C_P N_Q with N_Q=<T_Q,T_Q>_P.",
            "derivation": "Orthogonal projection of the parent fibre inner product onto the Q generator subblock.",
            "result": "EXACT_CONDITIONAL_PARENT_SUBBLOCK_COEFFICIENT",
            "status": "CONDITIONAL_COEFFICIENT_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MNO3863_2_normalization_owner_theorem",
            "claim_piece": "local EM source-scale zero theorem",
            "statement": OWNER_THEOREM,
            "derivation": "Apply q-basic chain rule to Z_Q_eff, fixed representation labels and variation-before-readout current; exclude independent F2/source/readout morphisms so no vertical derivative remains.",
            "result": "EXACT_CONDITIONAL_EM_SOURCE_SCALE_ZERO_THEOREM",
            "status": "CONDITIONAL_THEOREM_PROVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MNO3863_3_absolute_value_guard",
            "claim_piece": "local silence versus absolute alpha prediction",
            "statement": ABSOLUTE_VALUE_GUARD,
            "derivation": "A universal constant normalization can be calibrated into measured units, while local tests constrain vertical drift and source-response products.",
            "result": "NO_ALPHA_VALUE_OVERCLAIM",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MNO3863_4_Poynting_source_scale",
            "claim_piece": "Poynting stress scale alignment",
            "statement": "With Delta_Hodge_EM=0 from 3862 and B_EM_scale_3863=0, EM Hilbert stress and Poynting flux enter the total source current with the same parent normalization as charged matter.",
            "derivation": "Compose the 3862 observed-Hodge stress alignment with the 3863 Z_Q/J_Q normalization-owner theorem.",
            "result": "CONDITIONAL_MAXWELL_STRESS_SOURCE_CALIBRATION",
            "status": "CONDITIONAL_LOCAL_GR_EM_SOURCE_HANDOFF",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MNO3863_5_current_verdict",
            "claim_piece": "strict current corpus verdict",
            "statement": CURRENT_BLOCK,
            "derivation": "3809/3464/3650/3143 give exact conditional routes; 1812/1057/765/3621 keep the owner and no-counterterm clauses unsigned.",
            "result": "MAXWELL_NORMALIZATION_NOT_CLAIMED_CURRENT_CORPUS",
            "status": "CURRENT_NONCLAIM_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MNO3863_6_next_handoff",
            "claim_piece": "next obstruction",
            "statement": "The narrowest remaining derivation target is the no-extra-F2/operator-domain clause: if independent lambda_A or f_X F_Q^2 is legal, no parent subblock calculation can own alpha/source normalization.",
            "derivation": "3809 and 1057 both retain the independent F2 countermodel as the direct obstruction to Z_Q_eff descent.",
            "result": "NEXT_GATE_IS_NO_EXTRA_F2_OPERATOR_DOMAIN_OR_FINITE_LAMBDA_BOUND",
            "status": "COUPLING_ROUTE_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "CCA3863_0_parent_norm",
            "slot": "C_P and N_Q parent norm",
            "zero_condition": "C_P and N_Q are q-basic/superselected parent data with nonrescalable fibre norm",
            "current_evidence": "3809 and 3781 give the candidate Z_Q=C_P N_Q route but mark fixed norm owner unsigned",
            "passes_current_branch": False,
            "residual_owner": "b_CP+b_NQ",
            "observable_links": "alpha_EM;clock;source_normalization",
            "next_action": "prove fixed parent fibre metric/level or keep b_Z component",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CCA3863_1_unique_F2",
            "slot": "independent Maxwell F2 coefficient",
            "zero_condition": "Allowed[S_vis] excludes lambda_A F_Q^2, f_X(Phi)F_Q^2 and hidden-visible coefficient morphisms",
            "current_evidence": "1057/765 say gauge/diffeomorphism invariance alone does not ban F2 counterterms",
            "passes_current_branch": False,
            "residual_owner": "b_lambdaF2+b_hiddenF2+C_XF2+w_EM",
            "observable_links": "alpha_EM;WEP;R10;clock;source_normalization",
            "next_action": "make no-extra-F2 operator-domain theorem the next derivation target or acquire finite lambda_F2 bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CCA3863_2_same_current",
            "slot": "A_Q/J_Q same-current owner",
            "zero_condition": "J_Q is variation-before-readout current of the same A_Q/T_Q owner with fixed representation charges",
            "current_evidence": "3143 proves exact conditional same-current owner; 3650 says clauses remain unsigned",
            "passes_current_branch": False,
            "residual_owner": "b_J+C_JQ+kappa_J",
            "observable_links": "WEP;R10;source_coupling;local_GR",
            "next_action": "prove no c_A/w_A/source-marker/readout current slots or keep delta_J rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CCA3863_3_alpha_level",
            "slot": "alpha_EM level/readout",
            "zero_condition": "alpha_EM=alpha_*(ell_EM,g_*) with Lie_v ell_EM=0 and readout/radiative closure",
            "current_evidence": "1812 and 3464 keep alpha level owner and readout/radiative closure unsigned",
            "passes_current_branch": False,
            "residual_owner": "b_alpha",
            "observable_links": "clock;WEP;R10;spectroscopy",
            "next_action": "derive alpha level owner or retain product-level b_alpha branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CCA3863_4_EM_binding_source",
            "slot": "EM binding/source mass calibration",
            "zero_condition": "EM binding and Poynting flux enter M_H/J_H_total with parent-owned normalization and boundary flux silence",
            "current_evidence": "3503/3463 align Poynting conditionally but keep w_EM, Phi_EM_boundary and source calibration gaps",
            "passes_current_branch": False,
            "residual_owner": "Delta_M_EM_binding+Phi_EM_boundary",
            "observable_links": "Newton_GM;orbital;WEP;local_GR;source_mass",
            "next_action": "after no-extra-F2, connect total Hilbert current to source mass calibration",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CCA3863_5_absolute_prediction",
            "slot": "absolute alpha/mu0 value",
            "zero_condition": "C_P, N_Q, hbar/c conventions and charge unit are numerically derived from parent data",
            "current_evidence": "3809 explicitly separates local drift silence from absolute alpha prediction",
            "passes_current_branch": False,
            "residual_owner": "absolute_alpha_value_not_predicted",
            "observable_links": "absolute_constant_prediction",
            "next_action": "do not claim alpha value; local tests use drift/source products unless parent values are derived",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "ESB3863_0_Z_drift",
            "target": "b_Z",
            "formula": Z_BOUND,
            "derivation": "no-cancellation envelope for vertical drift of effective Maxwell kinetic normalization",
            "observables": "alpha_EM;clock;source_normalization;EM_binding",
            "status": "NONCLAIM_Z_NORMALIZATION_BOUND",
            "numeric_status": "MISSING_COMPONENT_COEFFICIENTS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "ESB3863_1_current_drift",
            "target": "b_J",
            "formula": J_BOUND,
            "derivation": "same-current owner residual if charge lattice/current/source measure/readout are not all q-basic",
            "observables": "WEP;R10;source_coupling;local_GR",
            "status": "NONCLAIM_CURRENT_BOUND",
            "numeric_status": "MISSING_COMPONENT_COEFFICIENTS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "ESB3863_2_EM_source_scale",
            "target": "B_EM_scale_3863",
            "formula": SOURCE_SCALE_BOUND,
            "derivation": "combines normalization, charge/current, alpha, hidden F2, EM binding and boundary Poynting source-scale residuals",
            "observables": "WEP;R10;clock;Newton_GM;orbital;source_calibration",
            "status": "NONCLAIM_SOURCE_SCALE_BOUND",
            "numeric_status": "SYMBOLIC_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "ESB3863_3_total_EM_clean_branch",
            "target": "Delta_T_EM_source",
            "formula": "Delta_T_EM_source <= ||Delta_Hodge_EM|| + B_EM_scale_3863 + B_current_owner + B_boundary_flux",
            "derivation": "EM source stress is clean only when Hodge shape, normalization/current owner and boundary flux all close",
            "observables": "local_GR;PPN;source_mass;Poynting",
            "status": "MAXWELL_TO_SOURCE_BOUND_REFINED",
            "numeric_status": "SYMBOLIC_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "ESB3863_4_no_extra_F2_priority",
            "target": "lambda_F2_or_C_XF2",
            "formula": "|lambda_F2|+|C_XF2| <= B_alpha_clock+B_WEP_EM_binding+B_R10_alpha_lambda+B_PPN_source_scale",
            "derivation": "fallback if operator-domain theorem cannot exclude standalone F_Q^2 coefficients",
            "observables": "clock;WEP;R10;PPN;source_normalization",
            "status": "NEXT_TARGET_BOUND_IF_DERIVATION_FAILS",
            "numeric_status": "MISSING_OBSERVABLE_PROJECTION_ROWS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G3863_0_rescaling_guard",
            "gate": "Maxwell normalization convention split is explicit",
            "status": "PASS_RESCALING_NORMAL_FORM",
            "claim_allowed": False,
            "reason": "the script distinguishes field normalization convention from parent-owned source coupling",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3863_1_zero_theorem",
            "gate": "conditional EM source-scale zero theorem is explicit",
            "status": "PASS_EXACT_CONDITIONAL_EM_SOURCE_SCALE_ZERO",
            "claim_allowed": False,
            "reason": "zero follows only if parent norm, no-extra-F2, same-current and readout/radiative clauses close together",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3863_2_no_current_claim",
            "gate": "current local-GR/Newton/EM source claim remains blocked",
            "status": "BLOCKED_MAXWELL_NORMALIZATION_OWNER_UNSIGNED",
            "claim_allowed": False,
            "reason": "C_P/N_Q, no-extra-F2, same-current, alpha and source-calibration clauses are not parent-signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3863_3_absolute_guard",
            "gate": "absolute alpha prediction is not claimed",
            "status": "PASS_NO_ALPHA_VALUE_OVERCLAIM",
            "claim_allowed": False,
            "reason": "local drift/source silence is weaker than deriving the numerical value of alpha_EM or mu0",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3863_4_next_target",
            "gate": "next target selected",
            "status": "PASS_3864_NO_EXTRA_F2_OPERATOR_DOMAIN_TARGET",
            "claim_allowed": False,
            "reason": "independent F_Q^2 is the direct countermodel to parent-owned Maxwell normalization",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D3863_0",
            "decision": "Do not treat EM normalization as a harmless unit choice after source coupling is involved.",
            "consequence": "A field rescaling is convention, but a vertical derivative or material/source dependence in Z_Q/J_Q is physical.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3863_1",
            "decision": "Separate local drift silence from absolute alpha prediction.",
            "consequence": "MTS can close local tests without predicting alpha's number, but cannot claim an absolute constant derivation yet.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3863_2",
            "decision": "Attack no-extra-F2 next.",
            "consequence": "If standalone lambda_A F_Q^2 is legal, the parent subblock coefficient cannot uniquely own EM coupling.",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3863_0",
            "target_checkpoint": "3864-Y5-R2FR-no-extra-F2-operator-domain-theorem-or-lambdaF2-bound.md",
            "script": "scripts/Y5_R2FR_3864_no_extra_F2_operator_domain_theorem_or_lambdaF2_bound.py",
            "objective": "derive an operator-domain exclusion forbidding independent lambda_A F_Q^2 / f_X F_Q^2 terms outside the parent curvature norm, or retain source-backed lambda_F2/C_XF2 bounds",
            "why_next": "3863 shows this is the direct countermodel to parent-owned Maxwell normalization and alpha/source-scale silence",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_MAXWELL_NORMALIZATION_OWNER_THEOREM_AND_EM_SOURCE_SCALE_BOUND",
            "summary": "3863 derives the Maxwell normalization/charge-current owner theorem conditionally, blocks absolute alpha overclaim, retains EM source-scale residuals, and selects no-extra-F2 as the next derivation target.",
            "doc": rel(DOC_PATH),
            "validation": rel(OUTPUTS["validation"]),
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    bound: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3863 — Maxwell Normalization / Charge-Current Owner Or EM Source-Scale Bound

Generated: `{timestamp}`

## Purpose

3862 reduced hidden EM Hodge to constitutive shape plus a separate source-scale gate. This checkpoint attacks that source-scale gate.

## Result

First, the convention guard:

`{RESCALING_NORMAL_FORM}`

The exact local zero route is:

`{OWNER_THEOREM}`

The overclaim guard is:

`{ABSOLUTE_VALUE_GUARD}`

The strict current verdict is:

`{CURRENT_BLOCK}`

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Maxwell Normalization Owner Theorem

{markdown_table(theorem, ["theorem_id", "claim_piece", "status", "result"])}

## Charge / Current Slot Audit

{markdown_table(audit, ["audit_id", "slot", "passes_current_branch", "residual_owner", "next_action"])}

## EM Source-Scale Bound

{markdown_table(bound, ["bound_id", "target", "status", "formula"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3863 isolates the coupling throat. Maxwell normalization is not just units once it controls source stress, EM binding energy, Poynting flux, WEP composition response and Newtonian source mass. The clean route is exact: parent-owned `T_Q/N_Q`, no independent `F_Q^2`, same-current owner, alpha/readout closure and EM source calibration make the local EM source-scale residual vanish. The current corpus does not yet sign those clauses, so the honest residual is `B_EM_scale_3863`.

Next target: `3864-Y5-R2FR-no-extra-F2-operator-domain-theorem-or-lambdaF2-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3862", "Current State After 3863", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3863 at ")
    )
    paragraph = (
        "`3863` isolates the EM coupling/source-normalization throat. "
        "For `S_EM=-1/4 int Z_Q F_Q wedge *_obs F_Q + int A_Q_mu J_Q^mu`, the field redefinition `A_Q'=s A_Q` gives `Z_Q'=Z_Q/s^2` and `J_Q'=J_Q/s`, so Maxwell equations alone fix only a convention class. "
        "The exact local zero theorem is: if `T_Q` has fixed nonrescalable parent norm `N_Q`, the parent coefficient `C_P` is q-basic, no independent `lambda_A F_Q^2`/`f_X F_Q^2` term is legal, matter charges are fixed representation/lattice labels, `J_Q` is extracted by variation before readout from the same `A_Q`, and radiative/readout/current re-entry is absent or q-basic, then `D_v ln Z_Q_eff = D_v ln J_Q = D_v ln alpha_EM = 0` on `ker(Dq_obs)` and the local EM source-scale residual vanishes. "
        "This does not predict the numerical value of `alpha_EM`/`mu0`; it only closes local drift/source coupling if the parent ownership clauses are signed. "
        "The retained bound is `B_EM_scale_3863 <= b_Z+b_J+|b_alpha|+|w_EM|+|C_XF2|+|C_JQ|+|Delta_M_EM_binding|+|Phi_EM_boundary|/(G_ref M_H)`, with `b_Z <= b_CP+b_NQ+b_lambdaF2+b_hiddenF2+b_rad+b_readout` and `b_J <= b_TQ_norm+b_charge_lattice+b_current_measure+b_material_marker+b_current_readout+b_boundary_current`. "
        "The next direct countermodel is independent `F_Q^2`; without a no-extra-F2 operator-domain theorem, parent-owned Maxwell normalization cannot be claimed.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3863-Y5-R2FR-Maxwell-normalization-charge-current-owner-or-EM-source-scale-bound.md`

Target: prove `Z_Q/mu0`, charge-current normalization, `alpha_EM`, and EM source-mass calibration are parent-owned/q-basic, or retain explicit `w_EM`, `C_JQ`, `C_XF2`, `b_alpha`, and `B_EM_scale` bounds.

This is the best next move because 3862 reduces the Hodge-shape problem, leaving the actual coupling/source-normalization gate."""
    new_gate = """`3864-Y5-R2FR-no-extra-F2-operator-domain-theorem-or-lambdaF2-bound.md`

Target: derive an operator-domain exclusion forbidding independent `lambda_A F_Q^2` / `f_X F_Q^2` terms outside the parent curvature norm, or retain source-backed `lambda_F2` / `C_XF2` bounds.

This is the best next move because 3863 shows independent `F_Q^2` is the direct countermodel to parent-owned Maxwell normalization and alpha/source-scale silence."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3863_CHARGE_CURRENT_SLOT_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3863_EM_SOURCE_SCALE_BOUND.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3863_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3863 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    bound: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in theorem + audit + bound + gates)
    add(
        "VAL3863_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3863_1_rescaling",
        "rescaling normal form is explicit",
        "EXACT_RESCALING_NORMAL_FORM" in all_text and "Z_Q' = Z_Q/s^2" in all_text,
        "Maxwell convention/source split present",
    )
    add(
        "VAL3863_2_zero_theorem",
        "EM source-scale zero theorem is explicit",
        "EXACT_CONDITIONAL_EM_SOURCE_SCALE_ZERO_THEOREM" in all_text and "D_v ln Z_Q_eff" in all_text,
        "conditional source-scale zero theorem present",
    )
    add(
        "VAL3863_3_absolute_guard",
        "absolute alpha overclaim guard is explicit",
        "NO_ALPHA_VALUE_OVERCLAIM" in all_text and "PASS_NO_ALPHA_VALUE_OVERCLAIM" in all_text,
        "absolute alpha guard present",
    )
    add(
        "VAL3863_4_current_block",
        "current claim remains blocked",
        "MAXWELL_NORMALIZATION_NOT_CLAIMED_CURRENT_CORPUS" in all_text and "BLOCKED_MAXWELL_NORMALIZATION_OWNER_UNSIGNED" in all_text,
        "no current local-GR/Newton/EM source promotion",
    )
    add(
        "VAL3863_5_bounds",
        "Z/J/EM source-scale bounds are explicit",
        "b_Z :=" in all_text and "b_J :=" in all_text and "B_EM_scale_3863 <=" in all_text,
        "normalization/current/source-scale bounds present",
    )
    add(
        "VAL3863_6_nonclaim",
        "all rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem + audit + bound + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3863_7_next",
        "next target is no-extra-F2 operator-domain gate",
        DOC_PATH.exists() and "3864-Y5-R2FR-no-extra-F2-operator-domain-theorem-or-lambdaF2-bound" in read_text(DOC_PATH),
        "3864 no-extra-F2 target visible",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3863_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3863_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "3862 reduced hidden EM Hodge" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3863*", "P8_Y5_BRR545_3863*", "*Y5_R2FR_3863*", "3863-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3863_10_formalization_clean",
        "formalization-workbench has no generated 3863 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3863 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3863_11_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    bound = bound_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["bound"], bound)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, audit, bound, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, audit, bound, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_MAXWELL_NORMALIZATION_OWNER_THEOREM_AND_BOUND")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
