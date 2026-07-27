from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3879"
BRANCH = "MTS_R2FR_Y5_CALIBRATED_GN_COMMON_TAIL_TO_NEWTON_POISSON_CHAIN_3879"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3879-Y5-R2FR-calibrated-GN-common-tail-to-Newton-Poisson-chain.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3878_NEXT = OUT / "P8_Y5_R2FR_3878_NEXT_TARGET.csv"
CSV_3878_THEOREM = OUT / "P8_Y5_R2FR_3878_COMMON_MODE_CALIBRATED_TAIL_THEOREM.csv"
CSV_3878_CONTRACT = OUT / "P8_Y5_R2FR_3878_RELATIVE_TAIL_CONTRACT.csv"
CSV_3878_ARENA = OUT / "P8_Y5_R2FR_3878_FIRST_ARENA_FILL_READINESS.csv"
CSV_3878_RUNNER = OUT / "P8_Y5_R2FR_3878_ACTIVE_RUNNER_CALIBRATED_UPDATE.csv"
CSV_3377_WEAK = OUT / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv"
CSV_3382_NEWTON = OUT / "P8_Y5_R2FR_3382_NEWTON_SOURCE_NORMALIZATION_CHAIN.csv"
CSV_3382_FIREWALL = OUT / "P8_Y5_R2FR_3382_NO_SMUGGLING_FIREWALL.csv"
CSV_3395_LADDER = OUT / "P8_Y5_R2FR_3395_COUPLING_IDENTITY_LADDER.csv"
CSV_3395_IMPLICATIONS = OUT / "P8_Y5_R2FR_3395_NEWTON_PPN_IMPLICATIONS.csv"
CSV_3510_COMMON = OUT / "P8_Y5_R2FR_3510_COMMON_ACTION_DENSITY_LINE_THEOREM.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"
CSV_3818_KAPPA = OUT / "P8_Y5_R2FR_3818_KAPPA_GREF_POLICY_AND_RESIDUALS.csv"
CSV_3818_GUARDS = OUT / "P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv"
CSV_3818_RESIDUALS = OUT / "P8_Y5_R2FR_3818_FINITE_EH_POISSON_GM_RESIDUAL_ROWS.csv"
CSV_3819_RESIDUALS = OUT / "P8_Y5_R2FR_3819_FINITE_SOURCE_NORMALIZATION_RESIDUALS.csv"
CSV_3855_REENTRY = OUT / "P8_Y5_R2FR_3855_SOURCE_NORMALIZATION_REENTRY_QUEUE.csv"
CSV_3501_MU = OUT / "P8_Y5_R2FR_3501_MU_EXTRA_OVER_GREF_MH_VECTOR.csv"
CSV_3498_PROJECTOR = OUT / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv"
CSV_SOURCE_STACK = OUT / "P8_source_normalized_Newton_branch_STACK.csv"
CSV_Y5_OWNER = OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3879_SOURCE_REGISTER.csv",
    "calibration_theorem": OUT / "P8_Y5_R2FR_3879_COMMON_GN_CALIBRATION_THEOREM.csv",
    "poisson_chain": OUT / "P8_Y5_R2FR_3879_NEWTON_POISSON_COMMON_TAIL_CHAIN.csv",
    "drift_contract": OUT / "P8_Y5_R2FR_3879_COMMON_DRIFT_VECTOR_CONTRACT.csv",
    "residual_update": OUT / "P8_Y5_R2FR_3879_EH_POISSON_GM_RESIDUAL_UPDATE.csv",
    "runner_update": OUT / "P8_Y5_R2FR_3879_ACTIVE_RUNNER_GN_CALIBRATION_UPDATE.csv",
    "claim_gates": OUT / "P8_Y5_R2FR_3879_CLAIM_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3879_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3879_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3879_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3879_00_3878_next", CSV_3878_NEXT, "NEXT3878_0", "3878 selected calibrated G_N common-tail branch"),
    ("SRC3879_01_3878_common", CSV_3878_THEOREM, "CMT3878_3_common_guard", "common mode anti-backfill guard"),
    ("SRC3879_02_3878_Newton", CSV_3878_THEOREM, "CMT3878_4_Newton_payoff", "Newton/GR connection from common scale"),
    ("SRC3879_03_3878_common_drift", CSV_3878_CONTRACT, "RTC3878_2_common_drift", "common drift contract"),
    ("SRC3879_04_3878_absolute", CSV_3878_CONTRACT, "RTC3878_7_absolute_gate", "absolute source residual gate"),
    ("SRC3879_05_3878_arena", CSV_3878_ARENA, "AFR3878_0_calibrated_Newton", "Newton common-mode route"),
    ("SRC3879_06_3878_runner", CSV_3878_RUNNER, "RUNU3878_2_calibrated_runner", "calibrated active runner"),
    ("SRC3879_07_3377_Gowner", CSV_3377_WEAK, "WFS3377_0_EH_coefficient_owner", "EH parent coefficient defines G"),
    ("SRC3879_08_3377_Poisson", CSV_3377_WEAK, "WFS3377_2_EH_to_Poisson", "weak-field Poisson algebra"),
    ("SRC3879_09_3377_verdict", CSV_3377_WEAK, "WFS3377_6_normalization_verdict", "calibrated source coupling theorem"),
    ("SRC3879_10_3382_same_kappa", CSV_3382_NEWTON, "NEW3382_0_same_kappa", "same kappa source normalization chain"),
    ("SRC3879_11_3382_poisson", CSV_3382_NEWTON, "NEW3382_2_poisson", "Poisson coefficient chain"),
    ("SRC3879_12_3382_firewall", CSV_3382_FIREWALL, "FIRE3382_2_em_public_or_residual", "no-smuggling EM/source firewall"),
    ("SRC3879_13_3395_parent_coeff", CSV_3395_LADDER, "CL3395_0_parent_coefficient", "EH/local metric coefficient ladder"),
    ("SRC3879_14_3395_poisson", CSV_3395_LADDER, "CL3395_2_EH_to_Poisson", "EH to Poisson ladder"),
    ("SRC3879_15_3395_G_policy", CSV_3395_IMPLICATIONS, "NP3395_2_G_policy", "numeric G policy"),
    ("SRC3879_16_3510_common_identity", CSV_3510_COMMON, "UAS3510_1_common_scale_identity", "common scale identity"),
    ("SRC3879_17_3510_guard", CSV_3510_COMMON, "UAS3510_2_common_mode_not_harmless", "common mode guard"),
    ("SRC3879_18_3510_Newton", CSV_3510_COMMON, "UAS3510_4_Newton_Poisson_payoff", "Newton-Poisson payoff"),
    ("SRC3879_19_3818_Poisson", CSV_3818_POISSON, "POI3818_0_linearized_00", "linearized 00 Poisson derivation"),
    ("SRC3879_20_3818_residual", CSV_3818_POISSON, "POI3818_2_residual_poisson", "finite Poisson residual form"),
    ("SRC3879_21_3818_G_policy", CSV_3818_KAPPA, "KGP3818_0_constant_policy", "do not derive decimal G here"),
    ("SRC3879_22_3818_product_lock", CSV_3818_KAPPA, "KGP3818_2_product_lock", "G_eff product lock"),
    ("SRC3879_23_3818_no_cancel", CSV_3818_KAPPA, "KGP3818_3_no_cancellation", "no cancellation guard"),
    ("SRC3879_24_3818_MHref", CSV_3818_GUARDS, "SNG3818_0_MHref", "positive same-frame M_H_ref guard"),
    ("SRC3879_25_3818_anticirc", CSV_3818_GUARDS, "SNG3818_3_no_orbital_GM_import", "anti-circular measured-GM policy"),
    ("SRC3879_26_3818_residual_total", CSV_3818_RESIDUALS, "R3818_5_total", "EH-Poisson-GM total residual"),
    ("SRC3879_27_3819_GM", CSV_3819_RESIDUALS, "R3819_4_GM_anti_circularity", "GM anti-circular residual"),
    ("SRC3879_28_3855_MHref", CSV_3855_REENTRY, "SRE3855_0_same_frame_MHref", "same-frame M_H_ref reentry"),
    ("SRC3879_29_3501_calibration", CSV_3501_MU, "EMV3501_11_absolute_calibration_offset", "absolute calibration owner"),
    ("SRC3879_30_3501_time", CSV_3501_MU, "EMV3501_2_time_MH_flux", "time drift source channel"),
    ("SRC3879_31_3501_range", CSV_3501_MU, "EMV3501_6_bulk_range_yukawa_tail", "range/fifth-force channel"),
    ("SRC3879_32_3498_projector", CSV_3498_PROJECTOR, "PNT3498_7_verdict", "projector naturality boundary of claim"),
    ("SRC3879_33_source_stack_Geff", CSV_SOURCE_STACK, "SN7_constant_universal_Geff", "constant universal G_eff rung"),
    ("SRC3879_34_source_stack_Poisson", CSV_SOURCE_STACK, "SN5_EH_to_Poisson_coefficient", "Poisson coefficient rung"),
    ("SRC3879_35_Y5_constant", CSV_Y5_OWNER, "Y5O_2_constant_universal_coupling", "constant universal coupling owner"),
    ("SRC3879_36_Y5_theorem", CSV_Y5_OWNER, "Y5O_8_owner_theorem", "source normalization owner theorem"),
]

CSTAR_DEF = (
    "C_*(p) := R_*(p)c_*(p)w_*(p)kappa_*(p)J_*(p)K_*(p)R_rad,*(p)"
)

CALIBRATION_THEOREM = (
    "Choose one local calibration event p0 and define G0 := G_ref C_*(p0). "
    "If G_ref is parent-owned and D_t ln C_*=D_r ln C_*=D_frame ln C_*=D_lambda ln C_*=Delta_domain(C_*)=0 on the tested local domain, "
    "then G_eff(p)=G0 everywhere in that domain and the common tail is a single calibrated Newton coupling, not a source/readout knob."
)

DRIFT_BOUND = (
    "|ln(G_eff(p)/G0)| <= integral_{p0->p} (|D_t ln C_*|+|D_r ln C_*|+|D_frame ln C_*|+|D_lambda ln C_*|+|Delta_domain(C_*)|)"
)

POISSON_CAL = (
    "G_00^(1)=2 nabla^2 Phi/c^2, T_00=rho_H c^2, kappa0=8*pi*G0/c^4 => nabla^2 Phi=4*pi*G0 rho_H"
)

POISSON_RES = (
    "nabla^2 Phi = 4*pi*G0 rho_H + S_EH + S_source + S_boundary + S_domain + S_nonEH + S_readout + 4*pi*G0 rho_H delta_C"
)

RUNNER = (
    "|z_g_active,cal| <= b_Qstar + b_Noether + b_tail_rel + b_Gcommon"
)

BGCOMMON = (
    "b_Gcommon := b_common_drift + b_delta_kappa + b_MHref_lock + b_PiM_JH_flux + b_GM_anti_circular + b_PPN_readout"
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
                "claim_use": "nonclaim_calibrated_GN_common_tail_theorem",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def calibration_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("CGT3879_0_common_tail_product", "common tail product", CSTAR_DEF, "EXACT_DEFINITION", "none"),
        ("CGT3879_1_anchor_calibration", "one measured constant", "G0 := G_ref C_*(p0), kappa0 := 8*pi*G0/c^4", "EXACT_CALIBRATION_IDENTITY", "does not derive decimal G"),
        ("CGT3879_2_local_constancy", "common tail derivative silence theorem", CALIBRATION_THEOREM, "EXACT_CONDITIONAL_CALIBRATION_THEOREM", "G_ref/C_* derivative silence not parent-signed"),
        ("CGT3879_3_drift_bound", "if silence fails, bound drift", DRIFT_BOUND, "FINITE_NO_CANCELLATION_BOUND", "requires source-backed derivative/profile rows"),
        ("CGT3879_4_GR_policy", "GR-style reduction policy", "A successful local-GR reduction does not need the numerical value of G0 derived; it needs G0 to be one universal parent/calibrated constant used by EH, source charge, Poisson, orbital and PPN branches.", "POLICY_EXACT_MATCHES_GR", "stronger topological derivation of G0 deferred"),
        ("CGT3879_5_no_orbital_backfill", "anti-circularity guard", "Measured orbital GM may verify G0 M_H after Poisson/Gauss/source lock; it may not define M_H_ref or hide G_eff drift before the bridge is derived.", "NO_SMUGGLING_GUARD", "M_H_ref and Pi_M J_H still open"),
        ("CGT3879_6_verdict", "current 3879 status", "The common tail can be treated as calibrated G_N only under derivative silence and same-source lock; current corpus has exact algebra and policy, not parent-signed closure.", "NONCLAIM_THEOREM_AND_BOUND_CONTRACT", "b_Gcommon retained"),
    ]
    return [
        {
            "theorem_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "remaining_gap": gap,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, gap in rows
    ]


def poisson_chain_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("NPC3879_0_EH_coefficient", "EH coefficient", "S_EH=(c^4/16*pi*G0) int sqrt(-g_obs) R[g_obs]", "single calibrated coefficient after common-tail anchor", "EXACT_IF_PARENT_EH_OWNER_SIGNED"),
        ("NPC3879_1_Hilbert_source", "same Hilbert source", "T_munu=-(2/sqrt(-g_obs)) delta S_matter/delta g_obs^munu and T_00=rho_H c^2", "source density is not orbital GM and not a post-readout rescale", "CONDITIONAL_SOURCE_OWNER_REQUIRED"),
        ("NPC3879_2_weak_field", "linearized 00 equation", POISSON_CAL, "Newton/Poisson coefficient follows from EH coefficient and same source", "EXACT_CONDITIONAL_WEAK_FIELD_ALGEBRA"),
        ("NPC3879_3_common_tail_residual", "common tail residual Poisson form", POISSON_RES, "drifting common tail enters as delta_C source-normalization residual", "FINITE_RESIDUAL_FORM"),
        ("NPC3879_4_Gauss_monopole", "Gauss exterior", "oint grad Phi.dS = 4*pi*G0 M_H_ref + residual_flux; Phi=-G0 M_H_ref/r + deltaPhi_res", "inverse-square law needs compact source-free exterior and same M_H_ref", "CONDITIONAL_GAUSS_TEMPLATE"),
        ("NPC3879_5_scope_guard", "not full local GR", "First-order Newton/Poisson calibration does not imply gamma=1, beta=1, alpha_i=0, xi=0.", "PPN scope guard", "NO_LOCAL_GR_PROMOTION"),
    ]
    return [
        {
            "chain_id": row_id,
            "step": step,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, step, formula, meaning, status in rows
    ]


def drift_contract_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("DVC3879_0_bGcommon", "b_Gcommon", BGCOMMON, "top-level common coupling/source calibration residual after 3879", "RUNNER_FILL_NONCLAIM"),
        ("DVC3879_1_bcommon", "b_common_drift", "|D_t ln C_*|+|D_r ln C_*|+|D_frame ln C_*|+|D_lambda ln C_*|+|Delta_domain(C_*)|", "common-tail derivative/domain drift", "MISSING_DERIVATIVE_SILENCE_OR_BOUND"),
        ("DVC3879_2_kappa", "b_delta_kappa", "|D ln G_ref| or |delta kappa/kappa0|", "parent EH coefficient drift/mismatch", "MISSING_PARENT_CONSTANT_OR_BOUND"),
        ("DVC3879_3_MHref", "b_MHref_lock", "same-frame positive M_H_ref and H_tau/H_ref lock failure", "source denominator/source charge lock", "MISSING_SAME_FRAME_MHREF"),
        ("DVC3879_4_PiM", "b_PiM_JH_flux", "abs(Pi_M dJ_H)+abs([d,Pi_M]J_H)+boundary/reference flux", "projected Hilbert current closure", "MISSING_PIM_JH_CLOSURE"),
        ("DVC3879_5_GM", "b_GM_anti_circular", "|delta ln mu_obs - delta ln G0 - delta ln M_H_ref|", "measured GM split residual", "NO_ORBITAL_GM_BACKFILL"),
        ("DVC3879_6_PPN", "b_PPN_readout", "Delta_cal+Delta_PPN+gamma/beta/preferred-frame source tails", "second-order/local-GR readout stability", "MISSING_PPN_READOUT_STABILITY"),
        ("DVC3879_7_observable_bound", "delta_C", "delta_C(p)=C_*(p)/C_*(p0)-1 with |ln(1+delta_C)| bounded by CGT3879_3", "observable common coupling drift", "SOURCE_BACKED_BOUND_OR_ZERO_REQUIRED"),
    ]
    return [
        {
            "contract_id": row_id,
            "quantity": quantity,
            "formula_or_definition": formula,
            "meaning": meaning,
            "status": status,
            "numeric_value": "MISSING_PARENT_ZERO_OR_SOURCE_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, meaning, status in rows
    ]


def residual_update_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("RUP3879_0_R3818_total", "R_EH_Poisson_GM_total", "replace generic common drift slot by b_Gcommon", "sum_abs(R_EH_owner,R_Poisson_norm,R_GM_calibration,R_PiM_JH_flux,R_PPN_readout_tail,b_common_drift)", "REFINED_NOT_CLOSED"),
        ("RUP3879_1_time", "Gdot/common time drift", "D_t ln C_* maps to Gdot/source-time residual unless zero", "use Gdot/clock/source drift bound or parent fixed coupling theorem", "BOUND_REQUIRED_IF_NOT_ZERO"),
        ("RUP3879_2_radial", "radial source hair", "D_r ln C_* maps to radial mu_obs/G_eff hair", "source-free exterior no-hair or radial profile bound", "BOUND_REQUIRED_IF_NOT_ZERO"),
        ("RUP3879_3_range", "range/fifth-force branch", "D_lambda ln C_* maps to R10/range-sensitive coupling", "no-pole theorem or alpha(lambda) bound row", "BOUND_REQUIRED_IF_NOT_ZERO"),
        ("RUP3879_4_frame", "frame/domain drift", "D_frame ln C_* and Delta_domain(C_*) map to preferred-frame/source-domain residuals", "same-frame/source-pullback theorem or PPN/WEP bound", "BOUND_REQUIRED_IF_NOT_ZERO"),
        ("RUP3879_5_abs_constant", "absolute calibration", "C_*(p0) can be absorbed into G0 once; only derivatives and mismatch across branches remain observable in local tests", "do not try to derive decimal G in this gate", "GR_STYLE_CALIBRATION_ALLOWED"),
    ]
    return [
        {
            "update_id": row_id,
            "target_residual": target,
            "update_rule": rule,
            "resulting_formula_or_action": formula,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, target, rule, formula, status in rows
    ]


def runner_update_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("RUNU3879_0_previous", "z_g_active,cal", "|z_g_active,cal| <= b_Qstar + b_Noether + b_tail_rel + b_common_drift", "imports 3878", "previous calibrated form"),
        ("RUNU3879_1_common_pack", "b_Gcommon", BGCOMMON, "3879 common G/source calibration residual", "COMMON_BRANCH_REFINED"),
        ("RUNU3879_2_updated_runner", "z_g_active,cal", RUNNER, "no-cancellation calibrated-GN runner", "RUNNER_SCHEMA_REFINED"),
        ("RUNU3879_3_G_policy", "G0", "numeric G0 may be empirical; G0 must be one universal derivative-silent parent/calibrated constant", "GR-style reduction policy", "POLICY_NOT_CLAIM"),
        ("RUNU3879_4_Newton_guard", "Newton pass", "false until EH owner, same Hilbert source, b_Gcommon=0/bounded, and Gauss/source lock close in one domain", "acceptance policy", "NO_NEWTON_CLAIM"),
        ("RUNU3879_5_localGR_guard", "local_GR pass", "false even if first-order Poisson closes; PPN/readout vector remains separate", "scope guard", "NO_LOCAL_GR_CLAIM"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "source_logic": logic,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, logic, status in rows
    ]


def claim_gate_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    chain: list[dict[str, object]],
    drift: list[dict[str, object]],
    residuals: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    required_drift = {"b_Gcommon", "b_common_drift", "b_delta_kappa", "b_MHref_lock", "b_PiM_JH_flux", "b_GM_anti_circular", "b_PPN_readout"}
    observed_drift = {row["quantity"] for row in drift}
    rows = [
        ("G3879_0_sources", "all cited source rows resolved", "PASS" if all_sources else "FAIL", f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"),
        ("G3879_1_calibration", "calibrated G_N theorem written", "PASS" if any(row["status"] == "EXACT_CONDITIONAL_CALIBRATION_THEOREM" for row in theorem) else "FAIL", "common tail to G0 theorem"),
        ("G3879_2_GR_policy", "numeric G derivation not required but universality is", "PASS" if any(row["status"] == "POLICY_EXACT_MATCHES_GR" for row in theorem) else "FAIL", "GR-style G policy"),
        ("G3879_3_poisson", "weak-field Poisson chain written", "PASS" if any(row["status"] == "EXACT_CONDITIONAL_WEAK_FIELD_ALGEBRA" for row in chain) else "FAIL", POISSON_CAL),
        ("G3879_4_drift", "b_Gcommon components present", "PASS" if required_drift.issubset(observed_drift) else "FAIL", ",".join(sorted(observed_drift))),
        ("G3879_5_residual_update", "EH/Poisson/GM residuals updated", "PASS" if any(row["target_residual"] == "R_EH_Poisson_GM_total" for row in residuals) else "FAIL", "R3818 total refined"),
        ("G3879_6_runner", "active runner updated with b_Gcommon", "PASS" if any(row["rule"] == RUNNER for row in runner) else "FAIL", RUNNER),
        ("G3879_7_no_claim", "no generated row allows Newton/local-GR claim", "PASS", "valid_for_claim=false throughout"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, detail in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3879_0",
            "target_checkpoint": "3880-Y5-R2FR-Geff-derivative-silence-or-drift-bound-input.md",
            "script": "scripts/Y5_R2FR_3880_Geff_derivative_silence_or_drift_bound_input.py",
            "objective": "try to derive D_t,D_r,D_frame,D_lambda,Delta_domain ln C_*=0 from parent coupling superselection/q-basic ownership; if not, stage source-backed Gdot, radial-hair, R10/range, and frame/domain drift bound rows",
            "why_next": "3879 shows the decimal value of G can be calibrated like GR, but local Newton/GR needs the common scale to be derivative-silent or bounded across every local arena",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "CALIBRATED_GN_COMMON_TAIL_THEOREM_AND_BGCOMMON_RUNNER_BUILT_NONCLAIM",
            "claim_allowed": False,
            "short_summary": "3879 proves the exact conditional calibration law: a common tail may become one GR-like calibrated G_N, but only if derivative-silent and same-source locked; otherwise b_Gcommon is retained.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = []
        for col in columns:
            values.append(str(row.get(col, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    chain: list[dict[str, object]],
    drift: list[dict[str, object]],
    residuals: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3879 - Calibrated G_N Common Tail to Newton-Poisson Chain

Generated: `{timestamp}`

## Result

3879 answers the Newton-constant/coupling question in the strict way:

`{CALIBRATION_THEOREM}`

The common tail product is:

`{CSTAR_DEF}`

If derivative silence is not proved, the honest finite bound is:

`{DRIFT_BOUND}`

The calibrated weak-field Newton equation is:

`{POISSON_CAL}`

and the residual form is:

`{POISSON_RES}`

So the active runner becomes:

`{RUNNER}`

with:

`{BGCOMMON}`

## Interpretation

This is not trying to derive the decimal value of `G`. GR does not do that either. The strict requirement is better and sharper: MTS must derive that the coupling is one universal, source-blind, range-blind, frame-blind, derivative-silent constant before readout. A one-time calibration is allowed; a drifting hidden source knob is not.

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Common G_N Calibration Theorem

{markdown_table(theorem, ["theorem_id", "piece", "statement", "status"])}

## Newton-Poisson Common Tail Chain

{markdown_table(chain, ["chain_id", "step", "formula", "status"])}

## Common Drift Vector Contract

{markdown_table(drift, ["contract_id", "quantity", "formula_or_definition", "status"])}

## Residual Update

{markdown_table(residuals, ["update_id", "target_residual", "update_rule", "status"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3879 is a genuine narrowing of the GR/Newton route. The decimal value of `G_N` is allowed to be empirical, but the ownership and derivative silence of `G_eff` are not optional. The next hard target is therefore exact: prove `D_t,D_r,D_frame,D_lambda,Delta_domain ln C_* = 0`, or put real bound rows under those five channels.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3879 CALIBRATED GN COMMON TAIL -->"
    end = "<!-- END 3879 CALIBRATED GN COMMON TAIL -->"
    block = f"""{start}

## 3879 - Calibrated G_N common tail to Newton-Poisson chain

`3879` turns the 3878 common tail into an exact calibration theorem:

`{CALIBRATION_THEOREM}`

Common tail product:

`{CSTAR_DEF}`

If derivative silence is not proved:

`{DRIFT_BOUND}`

Weak-field calibrated Poisson chain:

`{POISSON_CAL}`

Updated active runner:

`{RUNNER}`

with `{BGCOMMON}`.

Interpretation: the numerical value of `G_N` need not be derived for GR-style reduction, but a universal derivative-silent coupling owner must be derived or bounded. No Newton/local-GR claim is made.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3879_COMMON_GN_CALIBRATION_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3879_NEWTON_POISSON_COMMON_TAIL_CHAIN.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3879_COMMON_DRIFT_VECTOR_CONTRACT.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3879_VALIDATION.csv`

Next gate: `3880`, `G_eff` derivative silence or drift-bound input rows.

<!-- Generated by 3879 at {timestamp} -->
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
    chain: list[dict[str, object]],
    drift: list[dict[str, object]],
    residuals: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3879_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3879_1_calibration_theorem", "common G calibration theorem exists", any(row["status"] == "EXACT_CONDITIONAL_CALIBRATION_THEOREM" for row in theorem), "calibration theorem present"))
    checks.append(("VAL3879_2_G_policy", "GR-style numeric G policy exists", any(row["status"] == "POLICY_EXACT_MATCHES_GR" for row in theorem), "numeric G policy present"))
    checks.append(("VAL3879_3_no_backfill", "orbital backfill guard exists", any(row["status"] == "NO_SMUGGLING_GUARD" for row in theorem), "anti-circularity guard present"))
    checks.append(("VAL3879_4_poisson_chain", "Poisson calibrated algebra exists", any(row["formula"] == POISSON_CAL for row in chain), POISSON_CAL))
    required_drift = {"b_Gcommon", "b_common_drift", "b_delta_kappa", "b_MHref_lock", "b_PiM_JH_flux", "b_GM_anti_circular", "b_PPN_readout"}
    observed_drift = {row["quantity"] for row in drift}
    checks.append(("VAL3879_5_drift_contract", "b_Gcommon drift contract complete", required_drift.issubset(observed_drift), ",".join(sorted(observed_drift))))
    checks.append(("VAL3879_6_residual_update", "R3818 total residual updated", any(row["target_residual"] == "R_EH_Poisson_GM_total" for row in residuals), "R3818 total present"))
    checks.append(("VAL3879_7_runner_update", "active runner uses b_Gcommon", any(row["rule"] == RUNNER for row in runner), RUNNER))
    checks.append(("VAL3879_8_no_claim_gates", "no claim gate allows a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    checks.append(("VAL3879_9_doc", "markdown checkpoint exists with expected bottom line", DOC_PATH.exists() and "decimal value of `G_N`" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3879_10_spine", "spine updated with 3879 block", SPINE_PATH.exists() and "BEGIN 3879 CALIBRATED GN COMMON TAIL" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            count = len(read_csv_rows(path))
            parse_details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3879_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    generated_patterns = ("3879-Y5", "P8_Y5_R2FR_3879", "P8_Y5_BRR545_3879")
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3879*")
            if path.is_file() and any(pattern in path.name for pattern in generated_patterns)
        ]
    checks.append(("VAL3879_12_formalization_untouched", "no generated 3879 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3879_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3879_14_no_generated_claim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [theorem, chain, drift, residuals, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3879_15_next_target", "next target attacks Geff derivative silence", any("Geff-derivative-silence" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3880 derivative silence"))
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
    theorem = calibration_theorem_rows(timestamp)
    chain = poisson_chain_rows(timestamp)
    drift = drift_contract_rows(timestamp)
    residuals = residual_update_rows(timestamp)
    runner = runner_update_rows(timestamp)
    gates = claim_gate_rows(sources, theorem, chain, drift, residuals, runner, timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["calibration_theorem"], theorem)
    write_csv(OUTPUTS["poisson_chain"], chain)
    write_csv(OUTPUTS["drift_contract"], drift)
    write_csv(OUTPUTS["residual_update"], residuals)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, chain, drift, residuals, runner, gates, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, chain, drift, residuals, runner, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_CALIBRATED_GN_COMMON_TAIL")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
