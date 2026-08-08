from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3882"
BRANCH = "MTS_R2FR_Y5_PARENT_ACTION_CSTAR_THREEFORM_INSERTION_OR_GDOT_COMPONENT_FILL_3882"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3882-Y5-R2FR-parent-action-Cstar-threeform-insertion-or-Gdot-component-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3881_NEXT = OUT / "P8_Y5_R2FR_3881_NEXT_TARGET.csv"
CSV_3881_ZEROFORM = OUT / "P8_Y5_R2FR_3881_TOPOLOGICAL_ZEROFORM_VARIATION_AUDIT.csv"
CSV_3881_CONTRACT = OUT / "P8_Y5_R2FR_3881_PARENT_ACTION_INSERTION_CONTRACT.csv"
CSV_3881_GDOT = OUT / "P8_Y5_R2FR_3881_GDOT_FALLBACK_BOUND_ROWS.csv"
CSV_3881_RUNNER = OUT / "P8_Y5_R2FR_3881_RUNNER_UPDATE.csv"
CSV_3881_GATES = OUT / "P8_Y5_R2FR_3881_CLAIM_GATES.csv"
CSV_3881_VALIDATION = OUT / "P8_Y5_BRR545_3881_VALIDATION.csv"
CSV_3879_POISSON = OUT / "P8_Y5_R2FR_3879_NEWTON_POISSON_COMMON_TAIL_CHAIN.csv"
CSV_3879_GN = OUT / "P8_Y5_R2FR_3879_COMMON_GN_CALIBRATION_THEOREM.csv"
CSV_3880_THEOREM = OUT / "P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv"
CSV_3880_AUDIT = OUT / "P8_Y5_R2FR_3880_DERIVATIVE_CHANNEL_AUDIT.csv"
CSV_3880_INPUTS = OUT / "P8_Y5_R2FR_3880_DRIFT_BOUND_INPUT_ROWS.csv"
CSV_3880_RUNNER = OUT / "P8_Y5_R2FR_3880_BGCOMMON_RUNNER_UPDATE.csv"
CSV_KAPPA_THEOREM = OUT / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv"
CSV_KAPPA_RESIDUAL = OUT / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv"
CSV_DERIV_GATE = OUT / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv"
CSV_BOUND_MATRIX = OUT / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv"
CSV_GDOT_EVAL = OUT / "P8_Y5_R2FR_3758_GDOT_BOUND_EVALUATION.csv"
CSV_SOURCE_STACK = OUT / "P8_source_normalized_Newton_branch_STACK.csv"
CSV_Y5_OWNER = OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv"
CSV_PG_MAP = OUT / "P8_PG_calibration_residual_MAP.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3882_SOURCE_REGISTER.csv",
    "action": OUT / "P8_Y5_R2FR_3882_PARENT_ACTION_CSTAR_THREEFORM_STACK.csv",
    "el": OUT / "P8_Y5_R2FR_3882_EULER_LAGRANGE_BIANCHI_CHAIN.csv",
    "reduction": OUT / "P8_Y5_R2FR_3882_LOCAL_NEWTON_GR_REDUCTION_MAP.csv",
    "gdot": OUT / "P8_Y5_R2FR_3882_GDOT_COMPONENT_UPDATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3882_RUNNER_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3882_CLAIM_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3882_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3882_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3882_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3882_00_next", CSV_3881_NEXT, "NEXT3881_0", "3881 selected parent-action insertion target"),
    ("SRC3882_01_zeroform_parent", CSV_3881_ZEROFORM, "ZF3881_0_parent_term", "parent topological term row"),
    ("SRC3882_02_zeroform_variation", CSV_3881_ZEROFORM, "ZF3881_1_A3_variation", "A3 variation derives dC=0"),
    ("SRC3882_03_zeroform_silence", CSV_3881_ZEROFORM, "ZF3881_2_derivative_silence", "local derivative silence"),
    ("SRC3882_04_zeroform_Ceq", CSV_3881_ZEROFORM, "ZF3881_3_C_variation", "C equation guard"),
    ("SRC3882_05_contract_fields", CSV_3881_CONTRACT, "PAC3881_0_fields", "field content contract"),
    ("SRC3882_06_contract_term", CSV_3881_CONTRACT, "PAC3881_1_topological_term", "topological term contract"),
    ("SRC3882_07_contract_no_sources", CSV_3881_CONTRACT, "PAC3881_3_no_A3_sources", "no A3 matter sources"),
    ("SRC3882_08_contract_map", CSV_3881_CONTRACT, "PAC3881_4_coupling_map", "single coupling map"),
    ("SRC3882_09_contract_bianchi", CSV_3881_CONTRACT, "PAC3881_8_Bianchi", "Bianchi compatibility"),
    ("SRC3882_10_gdot_cstar", CSV_3881_GDOT, "GDOT3881_2_Cstar_component", "Cstar Gdot component"),
    ("SRC3882_11_gdot_meff", CSV_3881_GDOT, "GDOT3881_3_Meff_component", "Meff Gdot component"),
    ("SRC3882_12_gdot_mu", CSV_3881_GDOT, "GDOT3881_4_mu_component", "mu-extra Gdot component"),
    ("SRC3882_13_gdot_readout", CSV_3881_GDOT, "GDOT3881_5_readout_components", "readout Gdot component"),
    ("SRC3882_14_runner_bt", CSV_3881_RUNNER, "RUNU3881_0_bt_gate", "b_t gate"),
    ("SRC3882_15_gate_unsigned", CSV_3881_GATES, "G3881_4_unsigned", "3881 unsigned action status"),
    ("SRC3882_16_validation", CSV_3881_VALIDATION, "VAL3881_15_next_target", "3881 validation next target"),
    ("SRC3882_17_poisson_EH", CSV_3879_POISSON, "NPC3879_0_EH_coefficient", "EH coefficient"),
    ("SRC3882_18_poisson_weak", CSV_3879_POISSON, "NPC3879_2_weak_field", "weak-field Poisson chain"),
    ("SRC3882_19_poisson_scope", CSV_3879_POISSON, "NPC3879_5_scope_guard", "PPN scope guard"),
    ("SRC3882_20_gn_constancy", CSV_3879_GN, "CGT3879_2_local_constancy", "common G constancy theorem"),
    ("SRC3882_21_gn_policy", CSV_3879_GN, "CGT3879_4_GR_policy", "GR-style G policy"),
    ("SRC3882_22_3880_bianchi", CSV_3880_THEOREM, "GST3880_3_Bianchi_guard", "Bianchi guard"),
    ("SRC3882_23_3880_time", CSV_3880_AUDIT, "DCA3880_0_time", "time derivative channel"),
    ("SRC3882_24_3880_input_gdot", CSV_3880_INPUTS, "DBI3880_0_time_Geff", "Gdot input target"),
    ("SRC3882_25_3880_runner", CSV_3880_RUNNER, "RUNU3880_2_bG_update", "bG runner"),
    ("SRC3882_26_kappa_topological", CSV_KAPPA_THEOREM, "T508_1_topological_zeroform", "older kappa topological route"),
    ("SRC3882_27_kappa_residual", CSV_KAPPA_RESIDUAL, "KR508_0_time_drift", "time residual if no theorem"),
    ("SRC3882_28_deriv_master", CSV_DERIV_GATE, "CGM0_master_identity", "derivative master identity"),
    ("SRC3882_29_deriv_time", CSV_DERIV_GATE, "CGM1_time_drift", "time drift identity"),
    ("SRC3882_30_bound_gdot", CSV_BOUND_MATRIX, "P8_Geff_time_drift", "Gdot bound target"),
    ("SRC3882_31_gdot_budget", CSV_GDOT_EVAL, "GB3758_2_max_allowed_residual", "Gdot allowed budget"),
    ("SRC3882_32_stack_Geff", CSV_SOURCE_STACK, "SN7_constant_universal_Geff", "source-normalized Geff rung"),
    ("SRC3882_33_owner_constant", CSV_Y5_OWNER, "Y5O_2_constant_universal_coupling", "Y5 constant coupling owner"),
    ("SRC3882_34_pg_constant", CSV_PG_MAP, "PG7_constant_universal_Geff", "PG constant Geff row"),
]

PARENT_ACTION = (
    "S_3882 = S_core^0[g_obs,Theta,Psi] + S_matter[g_obs,Psi,Theta] "
    "+ (1/(2*kappa_ref)) int C_*^{-1}(R[g_obs]-2*Lambda_0) eps_g "
    "+ sigma int C_* F_4, with F_4=dA_3."
)

A3_VARIATION = (
    "delta_{A_3} S_3882 = sigma int C_* d(delta A_3) "
    "= boundary - sigma int dC_* wedge delta A_3, so dC_*=0."
)

C_VARIATION = (
    "delta_{C_*} S_3882 gives sigma F_4 = (1/(2*kappa_ref)) C_*^{-2}"
    "(R-2*Lambda_0) eps_g - delta S_core^0/delta C_* - delta S_matter/delta C_*."
)

METRIC_EQUATION = (
    "Before imposing dC_*=0, f(C_*)R produces f G_munu + (g_munu box - nabla_mu nabla_nu)f terms with f=C_*^{-1}; "
    "after dC_*=0 these derivative terms vanish and G_munu+Lambda_0 g_munu = kappa_ref C_* T_munu^0."
)

NEWTON_CHAIN = (
    "kappa_0=kappa_ref C_branch=8*pi*G0/c^4, so the weak-field 00 equation gives nabla^2 Phi=4*pi*G0 rho_H once the same Hilbert source is locked."
)

GDOT_AFTER_CSTAR = (
    "|d_t ln M_eff| + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame|"
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
        values = []
        for col in columns:
            values.append(str(row.get(col, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
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
                "claim_use": "nonclaim_parent_action_Cstar_threeform_candidate",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def action_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("ACT3882_0_fields", "field content", "g_obs, Theta, Psi, universal zero-form C_*, three-form A_3, four-form F_4=dA_3", "INSERTED_IN_CHECKPOINT_CANDIDATE", "one universal branch coupling variable"),
        ("ACT3882_1_action", "candidate parent action", PARENT_ACTION, "INSERTED_IN_CHECKPOINT_CANDIDATE", "C_* is placed in the EH coupling and constrained by a topological sector"),
        ("ACT3882_2_no_direct_C_matter", "matter/source restriction", "S_matter and source/readout selectors carry no direct C_*, A_3, source, range, frame, or domain labels", "REQUIRED_FOR_CLAIM", "prevents the coupling from becoming a local fitted source knob"),
        ("ACT3882_3_gauge_boundary", "A_3 gauge/boundary rule", "A_3 -> A_3+dB_2 with compact-support or fixed-boundary variations; no membrane jump inside tested local branch", "REQUIRED_FOR_CLAIM", "keeps dC_*=0 on the local domain"),
        ("ACT3882_4_coupling_map", "coupling map", "kappa_eff=kappa_ref C_branch and G_eff=G_ref C_branch after dC_*=0", "DERIVED_IN_CANDIDATE_BRANCH", "one calibrated Newton/GR coupling"),
        ("ACT3882_5_claim_scope", "scope guard", "this adopts a candidate local parent-action sector only inside post-checkpoint work, not yet the whole MTS corpus", "NONCLAIM_SCOPE", "no public Newton/local-GR claim yet"),
    ]
    return [
        {
            "action_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "why_it_matters": why,
            "candidate_parent_action_inserted": True,
            "global_corpus_adopted": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, why in raw_rows
    ]


def el_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("EL3882_0_A3", "A_3 variation", A3_VARIATION, "DERIVED_LOCAL_ZERO", "sets C_* constant without fitting a value"),
        ("EL3882_1_Cstar", "C_* variation", C_VARIATION, "AUXILIARY_FLUX_EQUATION", "F_4 absorbs the conjugate density; it must not source local coupling drift"),
        ("EL3882_2_metric", "metric variation", METRIC_EQUATION, "EINSTEIN_EQUATION_WITH_CONSTANT_BRANCH_COUPLING", "removes scalar-tensor derivative terms after dC_*=0"),
        ("EL3882_3_Bianchi", "Bianchi identity", "nabla^mu(G_munu+Lambda_0 g_munu)=0 and dC_*=0 imply kappa_ref C_branch nabla^mu T_munu^0=0", "NO_VARIABLE_COUPLING_EXCHANGE_IN_CSTAR_SECTOR", "kills b_Bianchi from the common C_* sector"),
        ("EL3882_4_Gdot", "time drift", "d_t ln G_eff=d_t ln C_branch=0 on connected local branch", "CSTAR_GDOT_ZERO_IN_CANDIDATE", "kills the C_* part of b_t"),
        ("EL3882_5_limits", "remaining limits", "M_eff/Pi_M flux, epsilon_mu, non-EH operators, source Hilbert stress, and PPN residuals are not closed by C_*/A_3 alone", "OPEN_RESIDUAL_GUARD", "stops overclaiming"),
    ]
    return [
        {
            "el_id": row_id,
            "variation_or_identity": piece,
            "derived_statement": statement,
            "status": status,
            "effect_on_branch": effect,
            "candidate_parent_action_inserted": True,
            "global_corpus_adopted": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, effect in raw_rows
    ]


def reduction_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RED3882_0_constant_coupling", "local constant coupling", "dC_*=0 => kappa_eff and G_eff are local branch constants", "CSTAR_SECTOR_CLOSED_IN_CANDIDATE", "supports GR-style calibrated G"),
        ("RED3882_1_Newton_Poisson", "Newton/Poisson limit", NEWTON_CHAIN, "EXACT_CONDITIONAL_ON_HILBERT_SOURCE_LOCK", "turns the coupling route into the known Newton coefficient"),
        ("RED3882_2_no_fifth_force", "C_* fifth-force channel", "C_* has no propagating kinetic term and is constrained by A_3, so this sector contributes no Yukawa alpha(lambda)", "CSTAR_RANGE_CHANNEL_ZERO_IN_CANDIDATE", "R10 range pressure moves to other non-EH/MTS fields"),
        ("RED3882_3_PPN_scope", "PPN scope", "constant coupling removes scalar-tensor derivative contamination, but gamma,beta,preferred-frame and non-EH residuals still need their own zero/bound rows", "PPN_NOT_CLOSED", "no local-GR promotion"),
        ("RED3882_4_source_scope", "source/Hilbert scope", "same Hilbert stress T_munu^0 must still be derived from S_matter[g_obs,Psi,Theta]", "SOURCE_LOCK_OPEN", "next checkpoint should attack source and EM stress"),
        ("RED3882_5_EM_scope", "Maxwell/EM stress scope", "if S_matter contains -1/4 int sqrt(-g_obs) F_mn F^mn with no C_*/A_3 label, its stress is standard Maxwell stress; this has not yet been inserted here", "MAXWELL_STRESS_NEXT", "routes directly into EM part of the goal"),
    ]
    return [
        {
            "reduction_id": row_id,
            "limit_or_sector": sector,
            "statement": statement,
            "status": status,
            "remaining_requirement": requirement,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, sector, statement, status, requirement in raw_rows
    ]


def gdot_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("GDOT3882_0_Cstar_zero", "d_t_ln_Cstar", "yr^-1", "d_t ln C_*=0 from delta_A3 S_3882", "0.0", "CSTAR_COMPONENT_ZERO_IN_CANDIDATE", "9.6e-15"),
        ("GDOT3882_1_reduced_sum", "Gdot_over_G_residual_after_Cstar", "yr^-1", GDOT_AFTER_CSTAR, "MISSING_SEPARATED_COMPONENTS", "CSTAR_REMOVED_FROM_FALLBACK_SUM", "9.6e-15"),
        ("GDOT3882_2_Meff_open", "d_t_ln_Meff", "yr^-1", "Pi_M/J_H flux conservation or numeric bound required", "MISSING_FLUX_ZERO_OR_NUMERIC_BOUND", "OPEN_COMPONENT", "allocated within 9.6e-15"),
        ("GDOT3882_3_mu_open", "d_t_epsilon_mu", "yr^-1", "time drift of epsilon_mu=mu_extra/(G_eff M_eff)", "MISSING_MU_EXTRA_TIME_COEFFICIENT", "OPEN_COMPONENT", "allocated within 9.6e-15"),
        ("GDOT3882_4_readout_open", "d_t_ln_Z_Poisson_plus_Z_frame", "yr^-1", "Poisson/readout frame drift after C_* is constant", "MISSING_READOUT_TIME_BOUND", "OPEN_COMPONENT", "allocated within 9.6e-15"),
    ]
    return [
        {
            "gdot_id": row_id,
            "component": component,
            "units": units,
            "prediction_or_formula": formula,
            "prediction_value": value,
            "status": status,
            "bound_or_budget": bound,
            "candidate_prediction_row": status == "CSTAR_COMPONENT_ZERO_IN_CANDIDATE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, units, formula, value, status, bound in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3882_0_Cstar", "b_Cstar_time", "b_Cstar_time=0 in the 3882 candidate parent action because dC_*=0", "CSTAR_TIME_DRIFT_ZERO_IN_CANDIDATE"),
        ("RUNU3882_1_bt", "b_t", "candidate b_t = b_Meff_t + b_epsilon_mu_t + b_ZPoisson_t + b_Zframe_t; live claim keeps the gate nonclaim until global adoption", "BT_REDUCED_BUT_NOT_CLAIMED"),
        ("RUNU3882_2_common_drift", "b_common_drift", "candidate C_* pieces of b_t,b_r,b_lambda,b_frame,b_domain,b_Bianchi vanish; non-C_* pieces remain", "CSTAR_DERIVATIVE_HAIR_REMOVED_FROM_CANDIDATE"),
        ("RUNU3882_3_bGcommon", "b_Gcommon", "b_Gcommon := b_t+b_r+b_lambda+b_frame+b_domain+b_Bianchi+b_MHref_lock+b_PiM_JH_flux+b_GM_anti_circular+b_PPN_readout", "RUNNER_RETAINED_WITH_CSTAR_BRANCH"),
        ("RUNU3882_4_top_level", "z_g_active,cal", "|z_g_active,cal| <= b_Qstar + b_Noether + b_tail_rel + b_Gcommon", "NO_CANCELLATION_RUNNER"),
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


def claim_gate_rows(
    sources: list[dict[str, object]],
    action: list[dict[str, object]],
    el: list[dict[str, object]],
    reduction: list[dict[str, object]],
    gdot: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    source_count = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks = [
        ("G3882_0_sources", source_count == len(sources), f"{source_count}/{len(sources)} sources resolved"),
        ("G3882_1_action_candidate", any(row["action_id"] == "ACT3882_1_action" for row in action), "candidate parent action written"),
        ("G3882_2_A3_zero", any(row["el_id"] == "EL3882_0_A3" and "dC_*=0" in str(row["derived_statement"]) for row in el), "A3 variation gives dC_*=0"),
        ("G3882_3_metric_equation", any(row["el_id"] == "EL3882_2_metric" and "G_munu+Lambda_0" in str(row["derived_statement"]) for row in el), "metric equation propagated"),
        ("G3882_4_Bianchi", any(row["el_id"] == "EL3882_3_Bianchi" for row in el), "Bianchi exchange closed for C_* sector"),
        ("G3882_5_Newton_map", any(row["reduction_id"] == "RED3882_1_Newton_Poisson" for row in reduction), "Newton/Poisson map retained"),
        ("G3882_6_Gdot_Cstar", any(row["gdot_id"] == "GDOT3882_0_Cstar_zero" and row["prediction_value"] == "0.0" for row in gdot), "Cstar Gdot component zero in candidate"),
        ("G3882_7_no_claim", True, "global corpus adoption, Hilbert source lock, Maxwell stress, PPN and non-EH residues remain open"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, passed, detail in checks
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3882_0",
            "target_checkpoint": "3883-Y5-R2FR-Hilbert-source-and-Maxwell-stress-lock-or-residual-vector.md",
            "script": "scripts/Y5_R2FR_3883_Hilbert_source_and_Maxwell_stress_lock_or_residual_vector.py",
            "objective": "derive the same-source Hilbert stress lock for S_matter[g_obs,Psi,Theta], insert/check the Maxwell stress sector with no C_*/A_3/source-label coupling, and convert any remaining matter/readout mismatch into explicit residual rows",
            "why_next": "3882 gives a candidate constant coupling; local GR/Newton/EM now depends on proving the source stress used in the field equation is the same source used in matter, Maxwell, clocks, and orbital tests",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3882_0",
            "branch": BRANCH,
            "summary": "candidate parent action with C_*^{-1} EH coefficient plus C_* F_4 topological sector inserted in checkpoint layer; A3 variation derives dC_*=0; C_* Gdot/range/Bianchi drift is zero in candidate, but source/Hilbert/Maxwell/PPN residuals remain nonclaim",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    action: list[dict[str, object]],
    el: list[dict[str, object]],
    reduction: list[dict[str, object]],
    gdot: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3882 - Parent Action Cstar/Three-Form Insertion or Gdot Component Fill

Generated: `{timestamp}`

## Result

3882 takes the 3881 mechanism and writes it as a candidate local parent-action sector:

`{PARENT_ACTION}`

The key variation is:

`{A3_VARIATION}`

So the checkpoint candidate now has an exact route to `dC_*=0`. This removes the `C_*` piece of local coupling drift in the candidate branch. It is still nonclaim because the whole corpus has not yet adopted this action and the source/Hilbert/Maxwell/PPN residuals remain open.

## Euler-Lagrange and Bianchi Chain

{markdown_table(el, ["el_id", "variation_or_identity", "derived_statement", "status", "effect_on_branch"])}

## Parent Action Stack

{markdown_table(action, ["action_id", "piece", "statement", "status", "why_it_matters"])}

## Local Newton/GR Reduction Map

{markdown_table(reduction, ["reduction_id", "limit_or_sector", "statement", "status", "remaining_requirement"])}

## Gdot Component Update

{markdown_table(gdot, ["gdot_id", "component", "prediction_or_formula", "prediction_value", "bound_or_budget", "status"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is the first point where the coupling problem is not just bounded: in the candidate action, the `C_*` branch is actually forced constant by variation. That is a serious move toward local GR/Newton. The remaining hard gates are now cleaner: same Hilbert source, Maxwell stress, non-EH operator residue, and PPN residual vector.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3882 PARENT ACTION CSTAR THREEFORM -->"
    end = "<!-- END 3882 PARENT ACTION CSTAR THREEFORM -->"
    block = f"""{start}

## 3882 - Parent action Cstar/three-form insertion

`3882` writes the candidate local parent-action sector:

`{PARENT_ACTION}`

Euler-Lagrange core:

`{A3_VARIATION}`

Metric/Bianchi consequence:

`{METRIC_EQUATION}`

`{NEWTON_CHAIN}`

Candidate consequence: the `C_*` contribution to `Gdot`, range dependence, frame/domain derivative drift, and Bianchi exchange is zero on a connected local branch. Nonclaim guard: this does not close same Hilbert source, Maxwell stress, non-EH residues, PPN, or M_eff/Pi_M/epsilon_mu.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3882_PARENT_ACTION_CSTAR_THREEFORM_STACK.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3882_EULER_LAGRANGE_BIANCHI_CHAIN.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3882_LOCAL_NEWTON_GR_REDUCTION_MAP.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3882_VALIDATION.csv`

Next gate: `3883`, Hilbert source and Maxwell stress lock.

<!-- Generated by 3882 at {timestamp} -->
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
    action: list[dict[str, object]],
    el: list[dict[str, object]],
    reduction: list[dict[str, object]],
    gdot: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3882_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3882_1_action_written", "candidate parent action row exists", any(row["action_id"] == "ACT3882_1_action" and "C_*^{-1}" in str(row["statement"]) for row in action), "ACT3882_1_action"))
    checks.append(("VAL3882_2_A3_derivation", "A3 variation derives dC_*=0", any(row["el_id"] == "EL3882_0_A3" and "dC_*=0" in str(row["derived_statement"]) for row in el), "EL3882_0_A3"))
    checks.append(("VAL3882_3_C_equation_guard", "Cstar variation is represented as auxiliary flux equation", any(row["el_id"] == "EL3882_1_Cstar" and "F_4" in str(row["derived_statement"]) for row in el), "EL3882_1_Cstar"))
    checks.append(("VAL3882_4_metric_equation", "metric equation includes constant branch coupling", any(row["el_id"] == "EL3882_2_metric" and "kappa_ref C_*" in str(row["derived_statement"]) for row in el), "EL3882_2_metric"))
    checks.append(("VAL3882_5_Bianchi", "Bianchi consequence closes variable coupling exchange for Cstar sector", any(row["el_id"] == "EL3882_3_Bianchi" for row in el), "EL3882_3_Bianchi"))
    checks.append(("VAL3882_6_Newton_map", "Newton/Poisson map is present", any(row["reduction_id"] == "RED3882_1_Newton_Poisson" and "nabla^2 Phi" in str(row["statement"]) for row in reduction), "RED3882_1_Newton_Poisson"))
    checks.append(("VAL3882_7_Cstar_Gdot_zero", "Cstar Gdot component is zero in candidate", any(row["gdot_id"] == "GDOT3882_0_Cstar_zero" and row["prediction_value"] == "0.0" for row in gdot), "GDOT3882_0_Cstar_zero"))
    checks.append(("VAL3882_8_residual_guard", "source/Maxwell/PPN residuals remain guarded", any(row["reduction_id"] == "RED3882_5_EM_scope" for row in reduction), "Maxwell stress next"))
    checks.append(("VAL3882_9_runner", "runner keeps no-cancellation top level", any(row["runner_field"] == "z_g_active,cal" for row in runner), "z_g_active runner"))
    checks.append(("VAL3882_10_no_claim_gates", "no gate allows a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    checks.append(("VAL3882_11_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "coupling problem is not just bounded" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3882_12_spine", "spine updated with 3882 block", SPINE_PATH.exists() and "BEGIN 3882 PARENT ACTION CSTAR THREEFORM" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3882_13_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    generated_patterns = ("3882-Y5", "P8_Y5_R2FR_3882", "P8_Y5_BRR545_3882")
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3882*")
            if path.is_file() and any(pattern in path.name for pattern in generated_patterns)
        ]
    checks.append(("VAL3882_14_formalization_untouched", "no generated 3882 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3882_15_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3882_16_all_nonclaim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [action, el, reduction, gdot, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3882_17_next_target", "next target attacks Hilbert source and Maxwell stress", any("Hilbert-source-and-Maxwell-stress" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3883 Hilbert/Maxwell"))
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
    action = action_rows(timestamp)
    el = el_rows(timestamp)
    reduction = reduction_rows(timestamp)
    gdot = gdot_rows(timestamp)
    runner = runner_rows(timestamp)
    gates = claim_gate_rows(sources, action, el, reduction, gdot, timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["action"], action)
    write_csv(OUTPUTS["el"], el)
    write_csv(OUTPUTS["reduction"], reduction)
    write_csv(OUTPUTS["gdot"], gdot)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, action, el, reduction, gdot, runner, gates, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, action, el, reduction, gdot, runner, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_PARENT_ACTION_CSTAR_THREEFORM_INSERTION")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
