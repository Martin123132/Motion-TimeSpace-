from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4290"
CLAIM_ID = "L-131"
BRANCH = "MTS_R2FR_Y5_TRANSITION_HILBERT_MONOPOLE_SOURCE_LOCK_OR_FIRST_RESIDUAL_BOUND_ROW_4290"
DECISION = "SOURCE_LOCK_NOT_PARENT_SIGNED_FIRST_EPSILON_MU_TRANSITION_BOUND_ROW_NONCLAIM"
MARKER = "PPC4161_TRANSITION_HILBERT_MONOPOLE_SOURCE_LOCK_OR_FIRST_RESIDUAL_BOUND_ROW_4290"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_HILBERT_MONOPOLE_SOURCE_LOCK_OR_FIRST_RESIDUAL_BOUND_ROW_4290"
NEXT_TARGET = "4291-Y5-R2FR-PiM-Htau-glue-proof-or-shared-source-residual-bound-runner.md"

FORMAL_PATH = FORMAL / "306-PPC4161-transition-Hilbert-monopole-source-lock-or-first-residual-bound-row.md"
DOC_PATH = POST / "4290-Y5-R2FR-transition-Hilbert-monopole-source-lock-or-first-residual-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4290_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
PI_B_COEFFICIENT = 0.167893843691
TRANSITION_PIB = 0.5000000000287336
UNIT_T_RES_OVER_TAU_L = 1.0
UNIT_ABS_CGAMMA = 1.0

SOURCES = {
    "SRC4290_00_4289_split": (
        FORMAL / "305-PPC4161-transition-monopole-absorption-or-residual-profile-gate.md",
        "q_tr = q_tr^Hilbert-monopole + q_tr^residual.",
        "4289 supplies the exact transition split to be source-locked or bounded.",
    ),
    "SRC4290_01_4155_worldtube_glue": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK.csv",
        "WT4155_4_remaining_glue",
        "4155 says Pi_M/H_tau same-branch glue remains unsigned.",
    ),
    "SRC4290_02_4155_unsigned_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK.csv",
        "PIM_HTAU_GLUE_UNSIGNED",
        "This is the exact blocker preventing a source-lock theorem.",
    ),
    "SRC4290_03_4151_no_extra_monopole": (
        SOURCE_DIR / "P8_Y5_R2FR_4151_SOURCE_NORMALIZATION_PROOF.csv",
        "P4151_3_no_extra_monopole",
        "4151 identifies zero non-EH monopole as required.",
    ),
    "SRC4290_04_4151_not_parent_derived": (
        SOURCE_DIR / "P8_Y5_R2FR_4151_SOURCE_NORMALIZATION_PROOF.csv",
        "NOT_PARENT_DERIVED",
        "The zero non-EH monopole clause is not parent-derived.",
    ),
    "SRC4290_05_4151_epsilon_mu": (
        SOURCE_DIR / "P8_Y5_R2FR_4151_MEASURED_GM_RESIDUAL_ROWS.csv",
        "epsilon_mu=mu_extra/(G_eff M_H)",
        "4151 defines the monopole residual variable used here.",
    ),
    "SRC4290_06_3998_anti_backfill": (
        SOURCE_DIR / "P8_Y5_R2FR_3998_GM_ANTI_BACKFILL_CONTRACT.csv",
        "do not set M_H_ref=mu_obs/G0",
        "3998 forbids measured-GM denominator laundering.",
    ),
    "SRC4290_07_3820_independent_mass": (
        SOURCE_DIR / "P8_Y5_R2FR_3820_GM_SPLIT_TEST_CONTRACT.csv",
        "M_H_ref = M_source_independent*(1+epsilon_source_total)",
        "3820 requires independent source normalization before orbital scoring.",
    ),
    "SRC4290_08_4171_gauss": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "int_S grad Phi_N dot dS = 4*pi G_N M_H^dress.",
        "4171 is the Hamiltonian-source Gauss readout route.",
    ),
    "SRC4290_09_4178_no_orbital_gm": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "No orbital `GM`, fitted acceleration, or measured numerical `G` is used",
        "4178 keeps calibrated coupling separate from orbital source definition.",
    ),
    "SRC4290_10_4284_direct_shell_fail": (
        FORMAL / "300-PPC4161-real-transition-shell-profile-calculator.md",
        "So the transition shell cannot be treated as a direct local metric source.",
        "4284 prevents returning to direct shell projection as a shortcut.",
    ),
    "SRC4290_11_4286_no_closure_credit": (
        FORMAL / "302-PPC4161-transition-closure-local-sanity-and-cGamma-AJ-interface-runner.md",
        "The closure lock cannot be used as credit for them.",
        "4286 forbids closure evidence being spent as cGamma/AJ proof.",
    ),
    "SRC4290_12_4287_AJ_capacity": (
        FORMAL / "303-PPC4161-cGamma-AJ-real-profile-or-parent-coefficient-derivation.md",
        "A_J,eff_private <= 0.167893843691 * Pi_B * (T_res/tau_L) / abs(c_Gamma).",
        "4287 gives the algebraic capacity law used for the first bound row.",
    ),
    "SRC4290_13_4288_transition_piB": (
        FORMAL / "304-PPC4161-finite-margin-AJ-zero-domain-split-and-transition-frontier.md",
        "rough transition-shell `Pi_B=0.5000000000287336`",
        "4288 supplies the rough transition anchor for private smoke bounds.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_line(values: List[str]) -> str:
    handle = io.StringIO()
    writer = csv.writer(handle, lineterminator="")
    writer.writerow(values)
    return handle.getvalue()


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if any(line.startswith(f"{CLAIM_ID},") for line in text.splitlines()):
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr",
            (
                "4290 tries to close the transition-shell source-lock route rather than only naming it. "
                "The parent proof still does not fire: the same-branch Pi_M/H_tau glue is unsigned and the "
                "zero non-EH monopole clause is not parent-derived. The checkpoint therefore sets "
                "Z_source_lock=false, blocks local-GR/PPN/R10 claims, and converts the first live residual "
                "into an executable private bound row: |epsilon_mu_tr| <= 0.167893843691*Pi_B_tr*(T_res/tau_L)/|c_Gamma|. "
                "At the rough transition anchor Pi_B_tr=0.5000000000287336 this gives |epsilon_mu_tr|<=0.08394692185032 "
                "for T_res/tau_L=1 and |c_Gamma|=1, or T_res/tau_L>=1.1912289074553 for |epsilon_mu_tr|=0.1."
            ),
            (
                "4290 source register, source-lock audit, epsilon_mu transition bound rows, residual vector carryforward, "
                "strict control runner, decision, status and firewall."
            ),
            "private_transition_source_lock_not_signed_first_epsilon_mu_bound_row_nonclaim",
            (
                "Either derive same-branch Pi_M/H_tau source glue plus zero non-EH monopole, or run the shared "
                "source-residual vector against WEP/R10/PPN/clocks/orbital source bounds."
            ),
            (
                "Claiming source lock while Pi_M/H_tau glue is unsigned, hiding epsilon_mu inside calibrated G, "
                "using measured orbital GM to define M_H, using closure credit, or treating the private AJ capacity row "
                "as an empirical local-GR pass."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


def aj_capacity(pi_b: float, t_res_over_tau_l: float, abs_cgamma: float) -> float:
    if pi_b <= 0 or t_res_over_tau_l < 0 or abs_cgamma <= 0:
        return 0.0
    return PI_B_COEFFICIENT * pi_b * t_res_over_tau_l / abs_cgamma


def required_t_for_epsilon(epsilon_mu_abs: float, pi_b: float, abs_cgamma: float) -> float:
    if epsilon_mu_abs <= 0:
        return 0.0
    if pi_b <= 0 or abs_cgamma <= 0:
        return float("inf")
    return epsilon_mu_abs * abs_cgamma / (PI_B_COEFFICIENT * pi_b)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def source_lock_audit_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "SLA4290_0_transition_split",
            "use 4289 decomposition",
            "q_tr=q_tr^Hilbert-monopole+q_tr^residual",
            "AVAILABLE_CONDITIONAL_SPLIT",
            "allows a source-lock attempt but does not itself prove the Hilbert piece owns all shell mass",
            False,
        ),
        (
            "SLA4290_1_same_worldtube_source",
            "transition Hilbert monopole must be in the same pre-readout worldtube",
            "M_H^dress[W;tau] -> M_H^dress[W;tau]+M_tr^H before Newton/PPN readout",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "otherwise the shell is a separate residual, not source dressing",
            False,
        ),
        (
            "SLA4290_2_total_current_once",
            "all retained stress sectors enter one Hilbert current once",
            "J_H_total=J_matter+J_EM+J_binding+dB_impr+J_rest_retained",
            "CONDITIONAL_FROM_4155",
            "prevents per-arena source retuning",
            False,
        ),
        (
            "SLA4290_3_surface_glue",
            "Noether/Gauss surface charge is independent of linking surface",
            "on shell J_tau=dQ_tau+C_tau and C_tau=0 in exterior annulus",
            "CONDITIONAL_FROM_4155",
            "needed for a real source charge rather than a chosen surface",
            False,
        ),
        (
            "SLA4290_4_support_lock",
            "worldtube support belongs to the parent current",
            "W_H=closure(supp J_H_total); D_v W_H=0 under descent and regularity",
            "CONDITIONAL_WITH_REGULARITY_GUARD",
            "prevents post-fit orbit masking",
            False,
        ),
        (
            "SLA4290_5_PiM_Htau_same_branch",
            "mass projector and Hamiltonian charge must name the same source measure",
            "Q_M=ell_M(Pi_M J_H_total)=M_H^dress only if H_tau,Pi_M,tau,reference,frame and rest-sector silence are same-branch",
            "PIM_HTAU_GLUE_UNSIGNED",
            "this is the live parent-source-lock blocker",
            False,
        ),
        (
            "SLA4290_6_no_extra_nonEH_monopole",
            "non-Hilbert transition monopole must vanish or be bounded",
            "mu_extra_tr=0 or epsilon_mu_tr=mu_extra_tr/(G_cal M_H^dress) is controlled",
            "NOT_PARENT_DERIVED",
            "this is the first executable residual row",
            False,
        ),
        (
            "SLA4290_7_anti_backfill",
            "measured orbital GM cannot define the source denominator",
            "do not set M_H_ref=mu_obs/G0",
            "GUARD_AVAILABLE",
            "keeps Newton recovery non-circular",
            True,
        ),
        (
            "SLA4290_8_independent_source_gate",
            "independent source normalization must precede orbital/PPN scoring",
            "M_H_ref=M_source_independent*(1+epsilon_source_total)",
            "REQUIRED_FOR_CLAIM",
            "the shared residual vector must be scored across arenas",
            False,
        ),
        (
            "SLA4290_9_verdict",
            "Z_source_lock verdict",
            "Z_source_lock=false until Pi_M/H_tau glue and no-extra-monopole are parent-signed or bounded",
            "ZERO_PROOF_FAILED_CLEANLY",
            "move to bound runner rather than closure smuggling",
            False,
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "clause": clause,
            "formula": formula,
            "status": status,
            "blocker_or_use": blocker,
            "clause_sufficient_for_claim": str(sufficient),
            "Z_source_lock": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, clause, formula, status, blocker, sufficient in raw
    ]


def epsilon_bound_rows() -> List[Dict[str, str]]:
    unit_bound = aj_capacity(TRANSITION_PIB, UNIT_T_RES_OVER_TAU_L, UNIT_ABS_CGAMMA)
    eps_01_t = required_t_for_epsilon(0.1, TRANSITION_PIB, UNIT_ABS_CGAMMA)
    eps_1_t = required_t_for_epsilon(1.0, TRANSITION_PIB, UNIT_ABS_CGAMMA)
    raw = [
        (
            "EB4290_0_unit_transition_AJ_capacity",
            "epsilon_mu_tr",
            0.0,
            UNIT_T_RES_OVER_TAU_L,
            UNIT_ABS_CGAMMA,
            unit_bound,
            "At the rough transition anchor, an epsilon_mu_tr-only residual must be <= this value to fit the private cGamma/AJ capacity.",
        ),
        (
            "EB4290_1_required_window_for_epsilon_0p1",
            "epsilon_mu_tr",
            0.1,
            eps_01_t,
            UNIT_ABS_CGAMMA,
            aj_capacity(TRANSITION_PIB, eps_01_t, UNIT_ABS_CGAMMA),
            "A ten-percent transition monopole residual would require this strong-window ratio at the same rough transition Pi_B.",
        ),
        (
            "EB4290_2_required_window_for_order_one_epsilon",
            "epsilon_mu_tr",
            1.0,
            eps_1_t,
            UNIT_ABS_CGAMMA,
            aj_capacity(TRANSITION_PIB, eps_1_t, UNIT_ABS_CGAMMA),
            "An order-one non-Hilbert monopole is only privately controllable with the same large transition window already seen in 4288.",
        ),
        (
            "EB4290_3_public_claim_gate",
            "epsilon_mu_tr",
            0.0,
            UNIT_T_RES_OVER_TAU_L,
            UNIT_ABS_CGAMMA,
            unit_bound,
            "This is not an empirical bound; it needs independent source normalization plus PPN/WEP/R10/orbital/clocks scoring before claim use.",
        ),
    ]
    rows = []
    for bound_id, symbol, epsilon_probe, t_value, abs_cgamma, bound_value, interpretation in raw:
        rows.append(
            {
                **common(),
                "bound_id": bound_id,
                "symbol": symbol,
                "definition": "epsilon_mu_tr = mu_extra_tr/(G_cal M_H^dress)",
                "law": "|epsilon_mu_tr| <= 0.167893843691 * Pi_B_tr * (T_res/tau_L) / |c_Gamma|",
                "Pi_B_tr": f"{TRANSITION_PIB:.16g}",
                "T_res_over_tau_L": f"{t_value:.16g}",
                "abs_cGamma": f"{abs_cgamma:.16g}",
                "epsilon_probe_abs": f"{epsilon_probe:.16g}",
                "epsilon_mu_tr_AJ_bound": f"{bound_value:.16g}",
                "source_basis": "4287 capacity law plus 4288 rough transition Pi_B anchor plus 4289 residual split",
                "missing_for_public_claim": "parent Pi_M/H_tau glue; zero/bound for non-EH monopole; independent source ledger; shared arena scoring",
                "interpretation": interpretation,
                "bound_type": "private_AJ_capacity_not_empirical_bound",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def residual_vector_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "RV4290_0_epsilon_mu_tr",
            "epsilon_mu_tr",
            "extra non-Hilbert transition monopole",
            "epsilon_mu_tr=mu_extra_tr/(G_cal M_H^dress)",
            "first_private_AJ_capacity_row_built",
            "WEP; PPN gamma/beta; orbital GM split; R10 if range hair couples",
        ),
        (
            "RV4290_1_transition_multipoles",
            "Q_l_ge_1_tr",
            "non-monopole transition shell field",
            "Q_l>=1_tr=0 or bounded exterior multipole series",
            "MISSING_PARENT_ZERO_OR_PROFILE",
            "PPN anisotropy; orbital precession; local tidal tests",
        ),
        (
            "RV4290_2_time_drift",
            "dln_mu_tr_dt",
            "time drift in source normalization",
            "dln mu_obs/dt=dln G_eff/dt+dln M_H/dt+dln(1+epsilon_mu)/dt",
            "MISSING_NUMERIC_OR_PARENT_ZERO",
            "Gdot; clocks; ephemerides; binary timing",
        ),
        (
            "RV4290_3_range_hair",
            "alpha_tr(lambda)",
            "finite-range transition/coupling hair",
            "G_eff(r,lambda)=G_*[1+alpha(lambda) exp(-r/lambda)]",
            "MISSING_R10_CURVE_OR_ZERO_THEOREM",
            "short-range fifth-force; R10; lab tests",
        ),
        (
            "RV4290_4_frame_source",
            "delta_frame_source",
            "source readout differs between matter/clock/EH frames",
            "Delta_frame ln mu_obs=0 required for same-frame source normalization",
            "MISSING_PARENT_SAME_FRAME_SIGNATURE",
            "WEP; clocks; PPN source normalization",
        ),
        (
            "RV4290_5_species_blindness",
            "eta_source_AB",
            "composition dependence of active source charge",
            "eta_source_AB ~= Delta_AB ln mu_obs",
            "MISSING_SOURCE_BLINDNESS_THEOREM_OR_BOUND",
            "Eotvos/WEP; source-charge universality",
        ),
        (
            "RV4290_6_beta_source",
            "delta_beta_source",
            "post-Newtonian source beta residual",
            "S_beta^source=0 or |delta_beta_source| <= beta_gate",
            "MISSING_BETA_SOURCE_BOUND",
            "PPN beta; perihelion; Shapiro consistency",
        ),
        (
            "RV4290_7_transport",
            "R_transport_to_local",
            "transition transport leakage into local metric channel",
            "A_J,eff_private <= |R_transport_to_local|+|R_Bgrad_to_local|",
            "MISSING_REAL_PROFILE_OR_PARENT_ZERO",
            "local-GR cGamma/AJ branch",
        ),
        (
            "RV4290_8_Bgrad",
            "R_Bgrad_to_local",
            "transition B-gradient leakage into local metric channel",
            "A_J,eff_private <= |R_transport_to_local|+|R_Bgrad_to_local|",
            "MISSING_REAL_PROFILE_OR_PARENT_ZERO",
            "local-GR cGamma/AJ branch",
        ),
    ]
    return [
        {
            **common(),
            "residual_id": residual_id,
            "symbol": symbol,
            "meaning": meaning,
            "formula_or_gate": formula,
            "status": status,
            "observable_link": observable_link,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for residual_id, symbol, meaning, formula, status, observable_link in raw
    ]


def control_rows() -> List[Dict[str, str]]:
    threshold_for_0p1 = required_t_for_epsilon(0.1, TRANSITION_PIB, UNIT_ABS_CGAMMA)
    controls = [
        {
            "control_id": "CTRL4290_0_parent_signed_pure_hilbert",
            "description": "pure same-worldtube Hilbert monopole with signed parent source lock",
            "parent_source_lock_signed": True,
            "hilbert_monopole_only": True,
            "epsilon_mu_tr_abs": 0.0,
            "multipole_l_ge_1_norm": 0.0,
            "time_range_frame_hair_norm": 0.0,
            "T_res_over_tau_L": UNIT_T_RES_OVER_TAU_L,
            "Pi_B_tr": TRANSITION_PIB,
            "abs_cGamma": UNIT_ABS_CGAMMA,
            "expected_pass": True,
        },
        {
            "control_id": "CTRL4290_1_small_epsilon_unit_window",
            "description": "small epsilon_mu_tr inside the unit transition AJ capacity",
            "parent_source_lock_signed": True,
            "hilbert_monopole_only": True,
            "epsilon_mu_tr_abs": 0.01,
            "multipole_l_ge_1_norm": 0.0,
            "time_range_frame_hair_norm": 0.0,
            "T_res_over_tau_L": UNIT_T_RES_OVER_TAU_L,
            "Pi_B_tr": TRANSITION_PIB,
            "abs_cGamma": UNIT_ABS_CGAMMA,
            "expected_pass": True,
        },
        {
            "control_id": "CTRL4290_2_epsilon_0p1_unit_window",
            "description": "ten-percent epsilon_mu_tr is too large for the unit transition AJ capacity",
            "parent_source_lock_signed": True,
            "hilbert_monopole_only": True,
            "epsilon_mu_tr_abs": 0.1,
            "multipole_l_ge_1_norm": 0.0,
            "time_range_frame_hair_norm": 0.0,
            "T_res_over_tau_L": UNIT_T_RES_OVER_TAU_L,
            "Pi_B_tr": TRANSITION_PIB,
            "abs_cGamma": UNIT_ABS_CGAMMA,
            "expected_pass": False,
        },
        {
            "control_id": "CTRL4290_3_epsilon_0p1_threshold",
            "description": "ten-percent epsilon_mu_tr passes exactly at the required transition window",
            "parent_source_lock_signed": True,
            "hilbert_monopole_only": True,
            "epsilon_mu_tr_abs": 0.1,
            "multipole_l_ge_1_norm": 0.0,
            "time_range_frame_hair_norm": 0.0,
            "T_res_over_tau_L": threshold_for_0p1,
            "Pi_B_tr": TRANSITION_PIB,
            "abs_cGamma": UNIT_ABS_CGAMMA,
            "expected_pass": True,
        },
        {
            "control_id": "CTRL4290_4_missing_source_lock",
            "description": "same-worldtube parent source lock absent",
            "parent_source_lock_signed": False,
            "hilbert_monopole_only": True,
            "epsilon_mu_tr_abs": 0.0,
            "multipole_l_ge_1_norm": 0.0,
            "time_range_frame_hair_norm": 0.0,
            "T_res_over_tau_L": UNIT_T_RES_OVER_TAU_L,
            "Pi_B_tr": TRANSITION_PIB,
            "abs_cGamma": UNIT_ABS_CGAMMA,
            "expected_pass": False,
        },
        {
            "control_id": "CTRL4290_5_live_multipole",
            "description": "epsilon is small but a live l>=1 multipole remains",
            "parent_source_lock_signed": True,
            "hilbert_monopole_only": True,
            "epsilon_mu_tr_abs": 0.01,
            "multipole_l_ge_1_norm": 0.001,
            "time_range_frame_hair_norm": 0.0,
            "T_res_over_tau_L": UNIT_T_RES_OVER_TAU_L,
            "Pi_B_tr": TRANSITION_PIB,
            "abs_cGamma": UNIT_ABS_CGAMMA,
            "expected_pass": False,
        },
        {
            "control_id": "CTRL4290_6_live_time_range_frame_hair",
            "description": "epsilon is small but time/range/frame hair remains",
            "parent_source_lock_signed": True,
            "hilbert_monopole_only": True,
            "epsilon_mu_tr_abs": 0.01,
            "multipole_l_ge_1_norm": 0.0,
            "time_range_frame_hair_norm": 0.001,
            "T_res_over_tau_L": UNIT_T_RES_OVER_TAU_L,
            "Pi_B_tr": TRANSITION_PIB,
            "abs_cGamma": UNIT_ABS_CGAMMA,
            "expected_pass": False,
        },
        {
            "control_id": "CTRL4290_7_non_hilbert_shell",
            "description": "transition shell is not proven to be Hilbert-monopole-only",
            "parent_source_lock_signed": True,
            "hilbert_monopole_only": False,
            "epsilon_mu_tr_abs": 0.0,
            "multipole_l_ge_1_norm": 0.0,
            "time_range_frame_hair_norm": 0.0,
            "T_res_over_tau_L": UNIT_T_RES_OVER_TAU_L,
            "Pi_B_tr": TRANSITION_PIB,
            "abs_cGamma": UNIT_ABS_CGAMMA,
            "expected_pass": False,
        },
    ]
    rows = []
    for control in controls:
        capacity = aj_capacity(control["Pi_B_tr"], control["T_res_over_tau_L"], control["abs_cGamma"])
        if not control["parent_source_lock_signed"]:
            actual_pass = False
            outcome = "UNSCOREABLE_SOURCE_LOCK_UNSIGNED"
        elif not control["hilbert_monopole_only"]:
            actual_pass = False
            outcome = "FAIL_NOT_HILBERT_MONOPOLE_ONLY"
        elif control["multipole_l_ge_1_norm"] != 0.0:
            actual_pass = False
            outcome = "FAIL_MULTIPOLE_RESIDUAL_NOT_ABSORBABLE"
        elif control["time_range_frame_hair_norm"] != 0.0:
            actual_pass = False
            outcome = "FAIL_SECOND_ORDER_HAIR_REMAINS"
        else:
            actual_pass = control["epsilon_mu_tr_abs"] <= capacity + 1.0e-15
            outcome = "PASS_CAPACITY" if actual_pass else "FAIL_EPSILON_EXCEEDS_CAPACITY"
        expected = bool(control["expected_pass"])
        rows.append(
            {
                **common(),
                "control_id": str(control["control_id"]),
                "description": str(control["description"]),
                "parent_source_lock_signed": str(control["parent_source_lock_signed"]),
                "hilbert_monopole_only": str(control["hilbert_monopole_only"]),
                "epsilon_mu_tr_abs": f"{control['epsilon_mu_tr_abs']:.16g}",
                "multipole_l_ge_1_norm": f"{control['multipole_l_ge_1_norm']:.16g}",
                "time_range_frame_hair_norm": f"{control['time_range_frame_hair_norm']:.16g}",
                "T_res_over_tau_L": f"{control['T_res_over_tau_L']:.16g}",
                "Pi_B_tr": f"{control['Pi_B_tr']:.16g}",
                "abs_cGamma": f"{control['abs_cGamma']:.16g}",
                "epsilon_mu_tr_AJ_capacity": f"{capacity:.16g}",
                "required_T_res_over_tau_L_for_this_epsilon": f"{required_t_for_epsilon(control['epsilon_mu_tr_abs'], control['Pi_B_tr'], control['abs_cGamma']):.16g}",
                "actual_pass": str(actual_pass),
                "expected_pass": str(expected),
                "expected_matches_actual": str(actual_pass == expected),
                "outcome": outcome,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "D4290_0",
            "decision": DECISION,
            "Z_source_lock": "False",
            "why": "Pi_M/H_tau same-branch glue is unsigned and zero non-EH monopole is not parent-derived.",
            "positive_progress": "The first residual bound row is executable: epsilon_mu_tr has a private cGamma/AJ capacity law.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "FW4290_0_no_source_lock_claim",
            "Z_source_lock=false blocks local-GR/PPN/R10 claims from this branch.",
        ),
        (
            "FW4290_1_no_measured_GM_backfill",
            "Do not define M_H from mu_obs/G0; orbital data can only constrain residuals after source normalization.",
        ),
        (
            "FW4290_2_no_G_cal_hiding",
            "A non-Hilbert monopole epsilon_mu_tr cannot be hidden by renaming the calibrated Newton coupling.",
        ),
        (
            "FW4290_3_no_closure_credit",
            "Transition closure/no-leak rows cannot pay for parent source-lock or cGamma/AJ profile rows.",
        ),
        (
            "FW4290_4_private_capacity_only",
            "The epsilon_mu_tr row is a private AJ capacity gate, not an empirical public bound.",
        ),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    unit_bound = aj_capacity(TRANSITION_PIB, UNIT_T_RES_OVER_TAU_L, UNIT_ABS_CGAMMA)
    return [
        {
            **common(),
            "status_id": "STATUS4290_0",
            "status": "BOUND_ROW_CREATED_SOURCE_LOCK_NOT_CLOSED",
            "Z_source_lock": "False",
            "epsilon_mu_tr_unit_bound": f"{unit_bound:.16g}",
            "required_T_for_epsilon_0p1": f"{required_t_for_epsilon(0.1, TRANSITION_PIB, UNIT_ABS_CGAMMA):.16g}",
            "required_T_for_epsilon_1": f"{required_t_for_epsilon(1.0, TRANSITION_PIB, UNIT_ABS_CGAMMA):.16g}",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "target_id": "NEXT4290_0",
            "next_target": NEXT_TARGET,
            "route": "derive Pi_M/H_tau glue and zero non-EH monopole; failing that, score epsilon_mu/source residual vector against WEP/R10/PPN/clocks/orbital bounds",
            "reason": "4290 reduced the transition source problem to a specific unsigned source-glue theorem plus an executable epsilon_mu residual row.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    unit_bound = aj_capacity(TRANSITION_PIB, UNIT_T_RES_OVER_TAU_L, UNIT_ABS_CGAMMA)
    t_for_01 = required_t_for_epsilon(0.1, TRANSITION_PIB, UNIT_ABS_CGAMMA)
    t_for_1 = required_t_for_epsilon(1.0, TRANSITION_PIB, UNIT_ABS_CGAMMA)
    return f"""
# 306 transition Hilbert monopole source lock or first residual bound row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4290 tries the parent source-lock proof first.

It does **not** close.

The attempted theorem would be:

```text
q_tr = q_tr^Hilbert-monopole + q_tr^residual,
q_tr^Hilbert-monopole included in M_H^dress[W;tau] before readout,
q_tr^residual = 0.
```

That would make the transition monopole ordinary source dressing rather than a separate local metric residual.

The proof fails cleanly because:

```text
Pi_M/H_tau same-branch glue = unsigned,
zero non-EH monopole = not parent-derived.
```

So the source-lock verdict is:

```text
Z_source_lock = false.
```

## First Residual Bound Row

The live monopole residual is:

```text
epsilon_mu_tr = mu_extra_tr/(G_cal M_H^dress).
```

Using the 4287 cGamma/AJ capacity law and the 4288 rough transition anchor:

```text
|epsilon_mu_tr| <= 0.167893843691 * Pi_B_tr * (T_res/tau_L) / |c_Gamma|.
```

At:

```text
Pi_B_tr = {TRANSITION_PIB:.16g},
T_res/tau_L = 1,
|c_Gamma| = 1,
```

the private capacity is:

```text
|epsilon_mu_tr| <= {unit_bound:.16g}.
```

A ten-percent residual would need:

```text
T_res/tau_L >= {t_for_01:.16g}.
```

An order-one residual would need:

```text
T_res/tau_L >= {t_for_1:.16g}.
```

## Meaning

This is not a local-GR claim and not an empirical R10/PPN/WEP bound.

It is progress because the transition source problem is now binary:

1. derive the source-lock theorem by signing `Pi_M/H_tau` glue and zero non-EH monopole; or
2. treat `epsilon_mu_tr` as a real shared source-normalization residual and score it against WEP, R10, PPN, clocks and orbital data.

No closure credit or measured-`GM` backfill is allowed.
"""


def checkpoint_doc() -> str:
    unit_bound = aj_capacity(TRANSITION_PIB, UNIT_T_RES_OVER_TAU_L, UNIT_ABS_CGAMMA)
    return f"""
# 4290 Y5 R2FR transition Hilbert monopole source lock or first residual bound row

## Purpose

This checkpoint tries to avoid circling the same missing-source issue by forcing a fork:

- prove the transition monopole is the same parent Hilbert source;
- or write the first executable residual bound row.

## Outcome

The proof route fails cleanly, not vaguely.

The unsigned clauses are:

- `Pi_M/H_tau` same-branch glue;
- parent zero for the non-EH monopole `mu_extra_tr`.

Therefore:

```text
Z_source_lock=false.
```

## New Executable Row

The first transition residual bound is:

```text
|epsilon_mu_tr| <= 0.167893843691 * Pi_B_tr * (T_res/tau_L) / |c_Gamma|.
```

At the rough transition anchor this gives:

```text
|epsilon_mu_tr| <= {unit_bound:.16g}
```

for `Pi_B_tr={TRANSITION_PIB:.16g}`, `T_res/tau_L=1`, and `|c_Gamma|=1`.

This is private capacity plumbing only; it must not be used as public evidence.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    audits = csv_rows(paths["source_lock_audit"])
    bounds = csv_rows(paths["epsilon_bound_rows"])
    residuals = csv_rows(paths["residual_vector"])
    controls = csv_rows(paths["control_runner"])

    unit_bound_rows = [row for row in bounds if row["bound_id"] == "EB4290_0_unit_transition_AJ_capacity"]
    unit_bound_positive = bool(unit_bound_rows) and float(unit_bound_rows[0]["epsilon_mu_tr_AJ_bound"]) > 0
    control_match = bool(controls) and all(row["expected_matches_actual"] == "True" for row in controls)
    missing_lock_fails = any(
        row["control_id"] == "CTRL4290_4_missing_source_lock" and row["actual_pass"] == "False"
        for row in controls
    )
    threshold_passes = any(
        row["control_id"] == "CTRL4290_3_epsilon_0p1_threshold" and row["actual_pass"] == "True"
        for row in controls
    )
    unit_0p1_fails = any(
        row["control_id"] == "CTRL4290_2_epsilon_0p1_unit_window" and row["actual_pass"] == "False"
        for row in controls
    )
    all_generated_csvs = [path for key, path in paths.items() if key != "validation"]
    no_claim_rows = True
    for path in all_generated_csvs:
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        (
            "VAL4290_0_sources_exist",
            bool(sources) and all(row["exists"] == "True" for row in sources),
            "all cited sources exist",
        ),
        (
            "VAL4290_1_needles_found",
            bool(sources) and all(row["required_text_found"] == "True" for row in sources),
            "all source needles found",
        ),
        (
            "VAL4290_2_source_lock_false",
            bool(audits)
            and any(row["audit_id"] == "SLA4290_9_verdict" and row["Z_source_lock"] == "False" for row in audits)
            and any(row["status"] == "PIM_HTAU_GLUE_UNSIGNED" for row in audits)
            and any(row["status"] == "NOT_PARENT_DERIVED" for row in audits),
            "source lock is explicitly blocked by unsigned glue and no-extra-monopole",
        ),
        (
            "VAL4290_3_epsilon_bound_positive_nonclaim",
            unit_bound_positive and all(row["valid_for_claim"] == "False" for row in bounds),
            "epsilon_mu_tr bound rows are positive private nonclaim rows",
        ),
        (
            "VAL4290_4_residual_vector_carryforward",
            bool(residuals)
            and any(row["symbol"] == "epsilon_mu_tr" for row in residuals)
            and any(row["symbol"] == "Q_l_ge_1_tr" for row in residuals),
            "residual vector carries epsilon and multipole blockers forward",
        ),
        (
            "VAL4290_5_control_expected_matches_actual",
            control_match,
            "strict control runner has no expected/pass mismatch",
        ),
        (
            "VAL4290_6_threshold_and_fail_controls",
            threshold_passes and unit_0p1_fails and missing_lock_fails,
            "threshold, unit-fail, and missing-source controls behave correctly",
        ),
        (
            "VAL4290_7_formal_doc",
            FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH),
            "formal document exists with marker",
        ),
        (
            "VAL4290_8_checkpoint_doc",
            DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH),
            "post-checkpoint document exists",
        ),
        (
            "VAL4290_9_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-131 private nonclaim row",
        ),
        (
            "VAL4290_10_no_claim_rows",
            no_claim_rows,
            "all generated rows remain nonclaim rows",
        ),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4290_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4290_SOURCE_REGISTER.csv",
        "source_lock_audit": SOURCE_DIR / "P8_Y5_R2FR_4290_SOURCE_LOCK_AUDIT.csv",
        "epsilon_bound_rows": SOURCE_DIR / "P8_Y5_R2FR_4290_EPSILON_MU_BOUND_ROW.csv",
        "residual_vector": SOURCE_DIR / "P8_Y5_R2FR_4290_RESIDUAL_VECTOR_CARRYFORWARD.csv",
        "control_runner": SOURCE_DIR / "P8_Y5_R2FR_4290_CONTROL_RUNNER.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4290_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4290_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4290_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4290_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }

    write_csv(paths["sources"], source_rows())
    write_csv(paths["source_lock_audit"], source_lock_audit_rows())
    write_csv(paths["epsilon_bound_rows"], epsilon_bound_rows())
    write_csv(paths["residual_vector"], residual_vector_rows())
    write_csv(paths["control_runner"], control_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4290 transition source-lock and epsilon bound",
        (
            "4290 attempts to parent-sign the transition Hilbert-monopole source lock. It does not close because "
            "`Pi_M/H_tau` same-branch glue remains unsigned and zero non-EH monopole is not parent-derived. "
            "The branch now has its first executable transition residual bound row: "
            "`|epsilon_mu_tr| <= 0.167893843691 * Pi_B_tr * (T_res/tau_L) / |c_Gamma|`, "
            "with rough unit-window capacity `0.08394692185032` at `Pi_B_tr=0.5000000000287336`."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4290 packet source-lock failed first epsilon bound row",
        (
            "Packet update: the local transition frontier is no longer just 'source coupling missing'. "
            "The exact unsigned clauses are `Pi_M/H_tau` glue and zero non-EH monopole. "
            "The first residual to score is `epsilon_mu_tr`, now with a private cGamma/AJ capacity law."
        ),
    )
    write_csv(paths["validation"], validation_rows(paths))
    failed = [row for row in csv_rows(paths["validation"]) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths) - 1} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(paths['validation']))} failed={len(failed)}")
    print(
        f"{CHECKPOINT}: epsilon_mu_tr unit transition capacity="
        f"{aj_capacity(TRANSITION_PIB, UNIT_T_RES_OVER_TAU_L, UNIT_ABS_CGAMMA):.12e}"
    )
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
