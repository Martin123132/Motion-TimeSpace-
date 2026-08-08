from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3967"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3967-Y5-R2FR-second-order-PPN-source-stability-or-Delta-PPN-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3967_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3967_PPN_STABILITY_THEOREM_OR_BOUND.csv",
    "residual_vector": SRC / "P8_Y5_R2FR_3967_PPN_RESIDUAL_VECTOR.csv",
    "beta_law": SRC / "P8_Y5_R2FR_3967_BETA_AB_LAW_ROLLED_FORWARD.csv",
    "bound_interface": SRC / "P8_Y5_R2FR_3967_EMPIRICAL_BOUND_INTERFACE.csv",
    "feed": SRC / "P8_Y5_R2FR_3967_LOCAL_GR_GATE_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3967_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3967_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3967_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3967_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3967_VALIDATION.csv",
}

NEXT_DOC = "3968-Y5-R2FR-quadratic-source-closure-B-equals-A2-or-finite-beta-vector.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3968_quadratic_source_closure_B_equals_A2_or_finite_beta_vector.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3967_00_3966_next", SRC / "P8_Y5_R2FR_3966_NEXT_TARGET.csv", "NEXT3966_0", "3966 handoff"),
        ("SRC3967_01_3966_ppn_feed", SRC / "P8_Y5_R2FR_3966_NEWTON_SCORE_DELTA_CAL_FEED_UPDATE.csv", "DCF3966_2_PPN_next", "PPN next gate"),
        ("SRC3967_02_3966_local_gr_claim", SRC / "P8_Y5_R2FR_3966_CLAIM_GATE.csv", "CLG3966_4_local_GR", "local GR blocked by PPN"),
        ("SRC3967_03_3966_delta_ppn", SRC / "P8_Y5_R2FR_3966_DELTA_CAL_RESIDUAL_VECTOR.csv", "DCR3966_6_PPN", "Delta_PPN_source component"),
        ("SRC3967_04_pg9", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG9_second_order_source_stability", "second-order source stability contract"),
        ("SRC3967_05_go523_ppn", SRC / "P8_Y5_GAUSS_ORBITAL_FORMULA_LEDGER.csv", "GO523_6_PPN_residual_vector", "Gauss/orbital PPN residual vector"),
        ("SRC3967_06_ag523_ppn", SRC / "P8_Y5_GAUSS_ORBITAL_ACCEPTANCE_GATES.csv", "AG523_4_PPN_source_stability", "PPN acceptance gate"),
        ("SRC3967_07_db_beta_law", SRC / "P8_Y5_DELTA_BETA_SOURCE_DERIVATION.csv", "DB525_2_extract_beta", "beta_eff law"),
        ("SRC3967_08_db_beta_residual", SRC / "P8_Y5_DELTA_BETA_SOURCE_DERIVATION.csv", "DB525_3_beta_residual", "delta_beta_source law"),
        ("SRC3967_09_db_split", SRC / "P8_Y5_DELTA_BETA_SOURCE_DERIVATION.csv", "DB525_6_R11_and_q_loc_split", "beta split"),
        ("SRC3967_10_bi_A", SRC / "P8_Y5_DELTA_BETA_INPUT_REQUIREMENTS.csv", "BI525_0_A_source", "A_source input"),
        ("SRC3967_11_bi_B", SRC / "P8_Y5_DELTA_BETA_INPUT_REQUIREMENTS.csv", "BI525_1_B_source", "B_source input"),
        ("SRC3967_12_2619_gamma", SRC / "P8_Y5_GR_LEFT_HAND_GATE_2619_PPN_BRIDGE_LEDGER.csv", "PPN2619_0_gamma", "gamma bridge"),
        ("SRC3967_13_2619_beta", SRC / "P8_Y5_GR_LEFT_HAND_GATE_2619_PPN_BRIDGE_LEDGER.csv", "PPN2619_1_beta", "beta bridge"),
        ("SRC3967_14_2619_pref", SRC / "P8_Y5_GR_LEFT_HAND_GATE_2619_PPN_BRIDGE_LEDGER.csv", "PPN2619_2_preferred_frame", "preferred-frame bridge"),
        ("SRC3967_15_2489_vector", SRC / "P8_Y5_NO_SHADOW_2489_PPN_RESIDUAL_VECTOR_INTERFACE.csv", "PPNV2489_7_total_abs", "PPN absolute vector"),
        ("SRC3967_16_2489_gamma_kernel", SRC / "P8_Y5_NO_SHADOW_2489_PPN_RESPONSE_KERNEL.csv", "PPNK2489_0_conformal_gamma_kernel", "gamma response kernel"),
        ("SRC3967_17_2489_beta_kernel", SRC / "P8_Y5_NO_SHADOW_2489_PPN_RESPONSE_KERNEL.csv", "PPNK2489_2_beta_second_order_placeholder", "beta response placeholder"),
        ("SRC3967_18_2489_pref_kernel", SRC / "P8_Y5_NO_SHADOW_2489_PPN_RESPONSE_KERNEL.csv", "PPNK2489_3_disformal_preferred_frame_placeholder", "preferred-frame response placeholder"),
        ("SRC3967_19_2489_bounds", SRC / "P8_Y5_NO_SHADOW_2489_PPN_BOUND_LEDGER.csv", "PBOUND2489_5_xi", "PPN bound ledger"),
        ("SRC3967_20_2500_requirements", SRC / "P8_Y5_NO_SHADOW_2500_FULL_PPN_VECTOR_REQUIREMENTS.csv", "VREQ2500_6_total_no_cancellation", "full PPN vector requirements"),
        ("SRC3967_21_2514_beta_vector", SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv", "DBETA2514_6_total_abs", "finite beta vector"),
        ("SRC3967_22_2515_r11_beta", SRC / "P8_Y5_NO_SHADOW_2515_R11_BETA_RESIDUAL_VECTOR.csv", "R11_2515_01", "R11 beta residual operator"),
        ("SRC3967_23_2576_kappa", SRC / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv", "LAW2576_5_kappa_v", "kappa_v second-order ledger"),
        ("SRC3967_24_2576_beta", SRC / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv", "LAW2576_6_beta", "beta-1=kappa_v/2 conditional law"),
        ("SRC3967_25_2636_interface", SRC / "P8_Y5_GENERATOR_EFFECTIVE_PACK_2636_PPN_INTERFACE_MAP.csv", "PPNI2636_6_total_abs", "generator PPN interface"),
        ("SRC3967_26_2469_stress", SRC / "P8_Y5_GK_STRESS_2469_PPN_RESIDUAL_LEDGER.csv", "PPN2469_2_hair_bound", "metric stress hair bound"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PPN3967_0_fixed_GM_convention",
            "clause": "fixed observed Newton potential",
            "mathematical_form": "U := mu_obs/r = G_obs M_obs/r is fixed before PPN extraction",
            "meaning": "only one first-order calibration is allowed; second-order and vector tails cannot be laundered into GM",
            "zero_condition": "Delta_cal=0 or bounded, then all PPN coefficients are compared after the same U normalization",
            "status": "DERIVED_CONVENTION_FROM_3966",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PPN3967_1_gamma_stability",
            "clause": "spatial-temporal potential equality",
            "mathematical_form": "g_ij=(1+2(1+delta_gamma_source)U/c^2)delta_ij+O(c^-4)",
            "meaning": "gamma=1 requires the same parent source/readout metric in spatial and temporal sectors",
            "zero_condition": "EH dominance plus no projector, memory, coframe, or non-EH spatial-slip residual",
            "status": "CONDITIONAL_THEOREM_OR_DELTA_GAMMA_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PPN3967_2_beta_AB_law",
            "clause": "quadratic source closure",
            "mathematical_form": "g_00=-1+2 A W/c^2-2 B W^2/c^4; U=A W; beta_eff=B/A^2",
            "meaning": "Newtonian agreement does not imply beta agreement; the quadratic coefficient must be the square of the first-order one",
            "zero_condition": "B_source=A_source^2 and all operator/readout/q_loc/boundary beta pieces vanish or are bounded",
            "status": "EXACT_BETA_LAW_ROLLED_FORWARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PPN3967_3_preferred_frame_stability",
            "clause": "no local preferred-frame vector",
            "mathematical_form": "alpha1=alpha2=alpha3=0 after e_obs, u_D, v_X, endpoint, and source-exchange projections",
            "meaning": "a successful scalar/Newton branch can still fail local GR through vector/coframe/domain leakage",
            "zero_condition": "no disformal/vector slot, or a normalized response matrix below alpha_i locks",
            "status": "CONDITIONAL_OR_PREFERRED_FRAME_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PPN3967_4_preferred_location_and_conservation",
            "clause": "xi and zeta_i silence",
            "mathematical_form": "xi=zeta1=zeta2=zeta3=zeta4=0",
            "meaning": "boundary/domain anisotropy and source-exchange currents must not violate local position invariance or conservation-law PPN channels",
            "zero_condition": "boundary/local-projection silence plus total Hilbert/source-current closure through PPN order",
            "status": "CONDITIONAL_OR_ZETA_BOUND_ACQUISITION_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PPN3967_5_absolute_no_cancellation_envelope",
            "clause": "componentwise PPN residual score",
            "mathematical_form": "Delta_PPN_abs := |delta_gamma|+|delta_beta_total|+|alpha1|+|alpha2|+|alpha3|+|xi|+sum_i|zeta_i|",
            "meaning": "PPN/local-GR credit needs zeros or finite bounds component by component, not sign-tuned cancellation",
            "zero_condition": "every term theorem-zero or below its comparator in the same fixed-GM convention",
            "status": "BOUND_BRANCH_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def ppn_residual_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("DPPN3967_0_gamma", "delta_gamma_source", "gamma_minus_1", "spatial-temporal potential slip", "EH dominance/common metric readout or gamma response bound", "|delta_gamma_source|", "2.3e-05 comparator available"),
        ("DPPN3967_1_beta_source", "delta_beta_source", "beta_minus_1", "B_source/A_source^2-1", "derive A_source and B_source then prove B_source=A_source^2 or bound", "|delta_beta_source|", "7.8e-05 comparator available"),
        ("DPPN3967_2_beta_operator", "delta_beta_operator", "beta_minus_1", "non-EH/R11 operator beta contribution", "EH-only operator selection or R11 coefficient vector", "|delta_beta_operator|", "7.8e-05 comparator available"),
        ("DPPN3967_3_beta_q_loc", "delta_beta_q_loc", "beta_minus_1", "O(U^2) q_loc projection", "Ward-zero at second order or finite q_loc beta kernel", "|delta_beta_q_loc|", "7.8e-05 comparator available"),
        ("DPPN3967_4_beta_boundary_domain", "delta_beta_boundary_domain", "beta_minus_1", "boundary/domain/projector stress beta tail", "topological/no-flux silence or finite boundary beta row", "|delta_beta_boundary_domain|", "7.8e-05 comparator available"),
        ("DPPN3967_5_beta_readout", "delta_beta_readout", "beta_minus_1", "PPN gauge/readout/radial coframe beta transfer", "fixed-before-readout theorem through O(U^2)", "|delta_beta_readout|", "7.8e-05 comparator available"),
        ("DPPN3967_6_alpha1", "alpha1_source", "alpha1", "preferred-frame orbital polarization source", "no local vector/disformal/domain slot or response bound", "|alpha1_source|", "1e-04 comparator available"),
        ("DPPN3967_7_alpha2", "alpha2_source", "alpha2", "preferred-frame spin/precession source", "no local vector/disformal/domain slot or response bound", "|alpha2_source|", "2e-09 comparator available"),
        ("DPPN3967_8_alpha3", "alpha3_source", "alpha3", "self-acceleration/source-exchange channel", "source-current closure and no momentum-flux leakage", "|alpha3_source|", "4e-20 comparator available"),
        ("DPPN3967_9_xi", "xi_source", "xi", "preferred-location/boundary anisotropy channel", "boundary/domain anisotropy silence or finite xi kernel", "|xi_source|", "4e-09 comparator available"),
        ("DPPN3967_10_zeta1", "zeta1_source", "zeta1", "conservation-law source prefactor channel", "total Hilbert/source-current closure through PPN order", "|zeta1_source|", "local bound source not yet imported"),
        ("DPPN3967_11_zeta2", "zeta2_source", "zeta2", "momentum-conservation/source exchange channel", "total Hilbert/source-current closure through PPN order", "|zeta2_source|", "local bound source not yet imported"),
        ("DPPN3967_12_zeta3", "zeta3_source", "zeta3", "Newton-third-law/source exchange channel", "total Hilbert/source-current closure through PPN order", "|zeta3_source|", "local bound source not yet imported"),
        ("DPPN3967_13_zeta4", "zeta4_source", "zeta4", "pressure/internal-energy coupling channel", "matter-source coupling closure through PPN order", "|zeta4_source|", "local bound source not yet imported"),
        ("DPPN3967_14_total_abs", "Delta_PPN_source_abs", "all_PPN", "absolute no-cancellation envelope", "all previous components theorem-zero or finite-sourced", "sum(component_abs)", "claim blocked until every component is owned"),
    ]
    return [
        {
            "component_id": component_id,
            "symbol": symbol,
            "observable": observable,
            "meaning": meaning,
            "zero_or_bound_requirement": requirement,
            "score_term": score_term,
            "comparator_note": note,
            "status": "RETAINED_SYMBOLIC_RESIDUAL",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, symbol, observable, meaning, requirement, score_term, note in specs
    ]


def beta_law_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BLAW3967_0_unmeasured_source_potential",
            "quantity": "W",
            "formula": "g_00=-1+2 A_source W/c^2-2 B_source W^2/c^4+O(c^-6)",
            "meaning": "A_source is the first-order source amplitude and B_source is the quadratic response before observed-GM normalization",
            "status": "DEFINITION_ROLLED_FORWARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BLAW3967_1_fixed_GM_normalization",
            "quantity": "U",
            "formula": "U=A_source W",
            "meaning": "the observed Newton potential is fixed once; remaining PPN shifts cannot be absorbed into GM again",
            "status": "FIXED_GM_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BLAW3967_2_beta_exact",
            "quantity": "beta_eff",
            "formula": "beta_eff=B_source/A_source^2",
            "meaning": "the clean route to beta=1 is a quadratic closure theorem, not a fit",
            "status": "EXACT_KINEMATIC_LAW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BLAW3967_3_delta_beta_source",
            "quantity": "delta_beta_source",
            "formula": "delta_beta_source=B_source/A_source^2-1",
            "meaning": "this is the source-normalization beta residual feeding the PPN vector",
            "status": "COEFFICIENTS_UNFILLED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BLAW3967_4_linear_guard",
            "quantity": "first_order_shift",
            "formula": "if A=1+a1 eps and B=1+b1 eps, beta_eff-1=(b1-2a1)eps+O(eps^2)",
            "meaning": "a linear source/coupling correction is safe only if the quadratic response tracks it with b1=2a1",
            "status": "NO_SIMPLE_ABSORPTION_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BLAW3967_5_kappa_v_branch",
            "quantity": "kappa_v",
            "formula": "kappa_v=-eta_v+kappa_source_quad+kappa_PiM+kappa_boundary+kappa_readout+kappa_operator+kappa_coupling",
            "meaning": "in the constrained v-readout branch beta-1=kappa_v/2, so coupling/source terms remain live",
            "status": "ALTERNATE_EXACT_LEDGER_COMPATIBLE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_interface_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        ("BND3967_0_gamma", "gamma_minus_1", "2.3e-05", "dimensionless", "Cassini_Shapiro_gamma_2003", "https://www.nature.com/articles/nature01997; doi:10.1038/nature01997", "COMPARATOR_READY_NOT_MTS_PREDICTION"),
        ("BND3967_1_beta", "beta_minus_1", "7.8e-05", "dimensionless", "Will_2014_PPN_beta_table", "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html", "COMPARATOR_READY_NOT_MTS_PREDICTION"),
        ("BND3967_2_alpha1", "alpha1", "1e-04", "dimensionless", "Will_2014_PPN_alpha1_table", "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html", "COMPARATOR_READY_NOT_MTS_PREDICTION"),
        ("BND3967_3_alpha2", "alpha2", "2e-09", "dimensionless", "Will_2014_PPN_alpha2_table", "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html", "COMPARATOR_READY_NOT_MTS_PREDICTION"),
        ("BND3967_4_alpha3", "alpha3", "4e-20", "dimensionless", "Will_2014_PPN_alpha3_table", "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html", "COMPARATOR_READY_NOT_MTS_PREDICTION"),
        ("BND3967_5_xi", "xi", "4e-09", "dimensionless", "Will_2014_PPN_xi_table", "https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html", "COMPARATOR_READY_NOT_MTS_PREDICTION"),
        ("BND3967_6_zeta1", "zeta1", "", "dimensionless", "MISSING_LOCAL_BOUND_SOURCE", "source acquisition required before scoring", "ACQUISITION_REQUIRED"),
        ("BND3967_7_zeta2", "zeta2", "", "dimensionless", "MISSING_LOCAL_BOUND_SOURCE", "source acquisition required before scoring", "ACQUISITION_REQUIRED"),
        ("BND3967_8_zeta3", "zeta3", "", "dimensionless", "MISSING_LOCAL_BOUND_SOURCE", "source acquisition required before scoring", "ACQUISITION_REQUIRED"),
        ("BND3967_9_zeta4", "zeta4", "", "dimensionless", "MISSING_LOCAL_BOUND_SOURCE", "source acquisition required before scoring", "ACQUISITION_REQUIRED"),
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for row_id, observable, upper_bound, units, source_dataset, reference, status in bound_interface_rows(timestamp):
        rows.append(
            {
                "row_id": row_id,
                "observable": observable,
                "upper_bound": upper_bound,
                "units": units,
                "source_dataset": source_dataset,
                "reference": reference,
                "status": status,
                "required_for_claim": "matching MTS residual numeric/theorem-zero row in fixed-GM convention",
                "score_ready": False,
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "LGF3967_0_epsilon_PPN_source_update",
            "target": "epsilon_PPN_source",
            "update_formula": "epsilon_PPN_source <= |delta_gamma_source|+|delta_beta_total|+|alpha1_source|+|alpha2_source|+|alpha3_source|+|xi_source|+sum_i|zeta_i_source|",
            "meaning": "3966 Delta_cal now receives an explicit second-order PPN source vector instead of a single loose symbol",
            "feeds": "Delta_cal; epsilon_Newton_source; local_GR_claim_gate",
            "status": "SYMBOLIC_FEED_READY_NO_NUMERIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "LGF3967_1_beta_total_update",
            "target": "delta_beta_total",
            "update_formula": "delta_beta_total=delta_beta_source+delta_beta_operator+delta_beta_q_loc+delta_beta_boundary_domain+delta_beta_readout",
            "meaning": "beta is now split into source, operator, q_loc, boundary/domain, and readout pieces under no-cancellation policy",
            "feeds": "PPN beta; perihelion; LLR; local_GR_claim_gate",
            "status": "EXACT_SPLIT_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "LGF3967_2_local_GR_gate",
            "target": "local_GR_source_branch",
            "update_formula": "local_GR_source_branch requires Delta_cal=0/bounded and Delta_PPN_source_abs below all locks",
            "meaning": "Newtonian GM calibration is necessary but not sufficient for local GR",
            "feeds": "R2FR local-GR promotion verdict",
            "status": "BLOCKED_UNTIL_PPN_VECTOR_FILLED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "LGF3967_3_bound_interface_status",
            "target": "PPN empirical comparator interface",
            "update_formula": "gamma,beta,alpha1,alpha2,alpha3,xi comparators are imported; zeta_i bound rows require acquisition",
            "meaning": "we can smoke-score six PPN channels once MTS values exist; conservation-law zeta channels still need source-backed locks",
            "feeds": "future PPN runner",
            "status": "PARTIAL_COMPARATOR_INTERFACE_READY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3967_0_beta_law_survives_rollforward",
            "status": "EXACT_BETA_AB_LAW_ACTIVE",
            "meaning": "the source-normalization beta test is now tied to the current Newton bridge: beta_eff=B/A^2 after fixed observed GM",
            "claim_status": "formula_only_no_beta_pass",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3967_1_ppn_vector_expanded",
            "status": "FULL_PPN_SOURCE_VECTOR_WRITTEN",
            "meaning": "gamma, beta components, preferred-frame alpha_i, xi, and zeta_i are explicit residual channels",
            "claim_status": "local_GR_blocked_until_vector_zero_or_bounded",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3967_2_comparators_partial",
            "status": "SIX_PPN_COMPARATORS_IMPORTED_ZETA_PENDING",
            "meaning": "existing local rows provide gamma/beta/alpha_i/xi comparators; zeta_i needs source acquisition before scoring",
            "claim_status": "no_claim_no_runner_pass",
            "next_action": "acquire zeta locks or prove conservation-current zeta silence",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3967_3_best_next_target",
            "status": "GO_AFTER_QUADRATIC_SOURCE_CLOSURE",
            "meaning": "the least hand-wavy route is to try proving B_source=A_source^2; if it fails, fill a finite beta residual vector",
            "claim_status": "private_derivation_continues",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3967_0_sources",
            "gate": "source register",
            "requirement": "all cited local sources and needles found",
            "status": "PASS_PRIVATE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3967_1_beta_law",
            "gate": "second-order beta",
            "requirement": "derive beta_eff=B/A^2 and identify exact inputs needed for beta=1",
            "status": "PASS_FORMULA_ONLY",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3967_2_ppn_vector",
            "gate": "Delta_PPN_source residual vector",
            "requirement": "all PPN source-stability failures mapped to explicit residual components",
            "status": "PASS_SYMBOLIC_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3967_3_bounds",
            "gate": "empirical comparator locks",
            "requirement": "all PPN channels have source-backed comparator rows before scoring",
            "status": "PARTIAL_ZETA_PENDING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3967_4_local_GR_claim",
            "gate": "local GR source branch",
            "requirement": "Delta_cal=0/bounded plus Delta_PPN_source_abs=0/below locks with no cancellation",
            "status": "BLOCKED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3967_5_next_target",
            "gate": "next derivation target",
            "requirement": "prove B_source=A_source^2 or fill finite beta vector",
            "status": "NEXT_TARGET_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3967_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive quadratic source closure B_source=A_source^2 under fixed observed GM, or produce a finite beta residual vector with source/operator/q_loc/boundary/readout pieces",
            "success_condition": "delta_beta_source is theorem-zero from parent/source coupling, or becomes a finite nonclaim vector row that can be compared to beta bounds without cancellation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PPN_SOURCE_STABILITY_VECTOR_READY_NONCLAIM",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "fixed-GM PPN vector assembled; exact beta_eff=B/A^2 law rolled into local-GR gate; claim remains blocked",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3967 - Second Order PPN Source Stability Or Delta PPN Bound

Timestamp: `{timestamp}`

## Result

3967 pushes the Newton bridge into the real local-GR danger zone: second-order PPN source stability.

The useful derived piece is not a claim of local GR. It is the fixed-`GM` bookkeeping:

```text
U := G_obs M_obs/r = A_source W
g_00 = -1 + 2 A_source W/c^2 - 2 B_source W^2/c^4 + O(c^-6)
beta_eff = B_source/A_source^2
delta_beta_source = B_source/A_source^2 - 1
```

So a Newtonian fit only fixes the first-order amplitude. It does **not** fix `beta`.
The clean route is now sharp: prove `B_source = A_source^2` from the parent/source coupling, or keep a finite beta residual.

## PPN Vector

The source-stability vector is now:

```text
Delta_PPN_source =
  (delta_gamma_source,
   delta_beta_source,
   delta_beta_operator,
   delta_beta_q_loc,
   delta_beta_boundary_domain,
   delta_beta_readout,
   alpha1_source,
   alpha2_source,
   alpha3_source,
   xi_source,
   zeta1_source,
   zeta2_source,
   zeta3_source,
   zeta4_source)
```

with the no-cancellation envelope:

```text
Delta_PPN_abs =
 |delta_gamma| + |delta_beta_total| + |alpha1| + |alpha2| + |alpha3| + |xi| + sum_i |zeta_i|
```

## Comparator Status

- Gamma, beta, alpha1, alpha2, alpha3, and xi comparator rows are imported from existing local PPN ledgers.
- Zeta comparator rows are explicitly marked acquisition-required.
- No generated row is valid for public/local-GR claim.

## Source Intake

Source needles found: `{found}/{len(sources)}`.

## Outputs

- `source-intake/mts_residuals/P8_Y5_R2FR_3967_PPN_STABILITY_THEOREM_OR_BOUND.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3967_PPN_RESIDUAL_VECTOR.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3967_BETA_AB_LAW_ROLLED_FORWARD.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3967_EMPIRICAL_BOUND_INTERFACE.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3967_LOCAL_GR_GATE_FEED_UPDATE.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_3967_VALIDATION.csv`

## Decision

The best next attack is not another broad audit. It is the hard derivation:

```text
B_source = A_source^2
```

If that parent/source-coupling square law closes, the local GR route gets substantially stronger.
If it fails, the beta branch becomes a finite residual vector and must be tested.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3967 - Second-Order PPN Source Stability

- Timestamp: `{timestamp}`
- Status: `PPN_SOURCE_STABILITY_VECTOR_READY_NONCLAIM`
- Fixed observed Newton potential before PPN extraction:
  `U := G_obs M_obs/r = A_source W`.
- Exact rolled-forward beta law:
  `beta_eff = B_source/A_source^2`,
  `delta_beta_source = B_source/A_source^2 - 1`.
- Expanded local-GR residual vector:
  `Delta_PPN_source = (delta_gamma, delta_beta_source, delta_beta_operator, delta_beta_q_loc, delta_beta_boundary_domain, delta_beta_readout, alpha1, alpha2, alpha3, xi, zeta1, zeta2, zeta3, zeta4)`.
- Claim status: no local-GR claim. Gamma/beta/alpha_i/xi comparators are imported; zeta_i locks and MTS coefficient rows remain nonclaim.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3967 - Second-Order PPN Source Stability"
    block = spine_block(timestamp)
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def all_generated_rows(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    sources = source_register_rows(timestamp)
    return {
        "sources": sources,
        "theorem": theorem_rows(timestamp),
        "residual_vector": ppn_residual_rows(timestamp),
        "beta_law": beta_law_rows(timestamp),
        "bound_interface": bound_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    source_rows = rows["sources"]
    theorem = rows["theorem"]
    residual = rows["residual_vector"]
    beta = rows["beta_law"]
    bounds = rows["bound_interface"]
    feed = rows["feed"]
    decisions = rows["decision"]
    claims = rows["claim_gate"]
    next_target = rows["next"]

    def val(validation_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }

    residual_symbols = {row["symbol"] for row in residual}
    needed_symbols = {
        "delta_gamma_source",
        "delta_beta_source",
        "delta_beta_operator",
        "delta_beta_q_loc",
        "delta_beta_boundary_domain",
        "delta_beta_readout",
        "alpha1_source",
        "alpha2_source",
        "alpha3_source",
        "xi_source",
        "zeta1_source",
        "zeta2_source",
        "zeta3_source",
        "zeta4_source",
        "Delta_PPN_source_abs",
    }
    bound_observables = {row["observable"] for row in bounds}
    parsed = True
    parse_detail = "generated CSV files parse cleanly"
    for path in generated_csvs:
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover - defensive validation row
            parsed = False
            parse_detail = f"{path} failed to parse: {exc}"
            break

    return [
        val("VAL3967_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        val("VAL3967_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        val("VAL3967_02_theorem", any(row["row_id"] == "PPN3967_2_beta_AB_law" for row in theorem), "beta AB law theorem row present"),
        val("VAL3967_03_vector_complete", needed_symbols <= residual_symbols, "PPN residual vector covers gamma, beta pieces, alpha_i, xi, and zeta_i"),
        val("VAL3967_04_beta_rollforward", any(row["row_id"] == "BLAW3967_2_beta_exact" and "B_source/A_source^2" in row["formula"] for row in beta), "exact beta law rolled forward"),
        val("VAL3967_05_bounds_partial", {"gamma_minus_1", "beta_minus_1", "alpha1", "alpha2", "alpha3", "xi", "zeta1", "zeta2", "zeta3", "zeta4"} <= bound_observables, "bound interface includes comparator/acquisition rows"),
        val("VAL3967_06_zeta_pending", all(row["status"] == "ACQUISITION_REQUIRED" for row in bounds if row["observable"].startswith("zeta")), "zeta rows explicitly acquisition-required"),
        val("VAL3967_07_feed", {"epsilon_PPN_source", "delta_beta_total", "local_GR_source_branch"} <= {row["target"] for row in feed}, "local-GR feed rows present"),
        val("VAL3967_08_decision", any(row["status"] == "GO_AFTER_QUADRATIC_SOURCE_CLOSURE" for row in decisions), "decision selects quadratic source closure next"),
        val("VAL3967_09_claim_gate", any(row["status"] == "BLOCKED_NONCLAIM" for row in claims), "claim gate blocks local-GR promotion"),
        val("VAL3967_10_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to B=A^2 closure or finite beta vector"),
        val("VAL3967_11_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3967_12_score_ready", all(row["score_ready"] for row in residual), "PPN residual rows are score-ready symbolics"),
        val("VAL3967_13_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3967_14_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3967_15_spine_updated", SPINE_PATH.exists() and "3967 - Second-Order PPN Source Stability" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3967_16_csv_parse", parsed, parse_detail),
        val("VAL3967_17_script_compile", True, "script compiled before validation write"),
        val("VAL3967_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_generated_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["residual_vector"], rows["residual_vector"])
    write_csv(OUTPUTS["beta_law"], rows["beta_law"])
    write_csv(OUTPUTS["bound_interface"], rows["bound_interface"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3967 validation failed: {failed}")

    print(f"3967 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Second-order PPN source-stability vector assembled; beta AB law rolled forward")


if __name__ == "__main__":
    run()
