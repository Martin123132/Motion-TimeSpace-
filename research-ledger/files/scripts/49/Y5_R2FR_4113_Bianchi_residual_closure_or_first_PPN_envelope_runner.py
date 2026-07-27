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
DOC_PATH = ROOT / "4113-Y5-R2FR-Bianchi-residual-closure-or-first-PPN-envelope-runner.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_BIANCHI_PPN_INVENTORY_CURRENT_SPINE_4113"
CHECKPOINT_ID = "4113"
DECISION = "BIANCHI_CONDITIONAL_LAW_AND_RESIDUAL_OWNER_INVENTORY_IMPORTED_GK_ORPHAN_NEXT"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4113_00_4112_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4112_NEXT_TARGET.csv",
        "4113-Y5-R2FR-Bianchi-residual-closure-or-first-PPN-envelope-runner.md",
        "4112 selected Bianchi residual closure or first PPN/Newton envelope runner.",
    ),
    "SRC4113_01_4112_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4112_STATUS.csv",
        "XI_Q_JQ_EM_BRANCH_IMPORTED_TO_MINIMAL_LOCAL_GR_CONTRACT_BIANCHI_NEXT",
        "Current-chain local-GR contract handoff.",
    ),
    "SRC4113_02_3625_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3625_STATUS.csv",
        "BIANCHI_CONDITIONAL_DERIVATION_AND_PPN_ENVELOPE_SCHEMA_WRITTEN_NO_CLAIM",
        "3625 Bianchi/Noether conditional law and PPN/Newton schema.",
    ),
    "SRC4113_03_3625_bianchi": (
        SOURCE_DIR / "P8_Y5_R2FR_3625_BIANCHI_NOETHER_DERIVATION.csv",
        "BND3625_3_residual_closure_law",
        "Exact conditional residual closure law.",
    ),
    "SRC4113_04_3625_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_3625_RESIDUAL_CLOSURE_AUDIT.csv",
        "RCA3625_6_Delta_PPN_abs",
        "Residual-by-residual Bianchi closure audit.",
    ),
    "SRC4113_05_3625_schema": (
        SOURCE_DIR / "P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv",
        "ENV3625_6_total",
        "First PPN/Newton no-cancellation envelope schema.",
    ),
    "SRC4113_06_3625_smoke": (
        SOURCE_DIR / "P8_Y5_R2FR_3625_NONCLAIM_SMOKE_ROWS.csv",
        "BLOCKED_NOT_SCORED",
        "Smoke runner rows correctly refuse missing component values.",
    ),
    "SRC4113_07_3626_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3626_STATUS.csv",
        "LOCAL_RESIDUAL_LAGRANGIAN_INVENTORY_COMPLETE_NONCLAIM",
        "3626 attaches every explicit residual to candidate action/current/boundary owner.",
    ),
    "SRC4113_08_3626_inventory": (
        SOURCE_DIR / "P8_Y5_R2FR_3626_LOCAL_RESIDUAL_LAGRANGIAN_INVENTORY.csv",
        "INV3626_6_PPN_total",
        "Local residual Lagrangian/source owner inventory.",
    ),
    "SRC4113_09_3626_euler": (
        SOURCE_DIR / "P8_Y5_R2FR_3626_EULER_VARIATION_CLOSURE_MAP.csv",
        "EVM3626_5_PPN_projection",
        "Euler/variation closure map for residual owners.",
    ),
    "SRC4113_10_3626_ppn_rows": (
        SOURCE_DIR / "P8_Y5_R2FR_3626_PPN_COMPONENT_FILL_ROWS.csv",
        "PCF3626_6_total",
        "Component-addressed PPN/Newton rows.",
    ),
    "SRC4113_11_3626_scorecard": (
        SOURCE_DIR / "P8_Y5_R2FR_3626_OWNERSHIP_SCORECARD.csv",
        "OSC3626_1_GK_q_loc",
        "Ownership scorecard naming the hard GK/q_loc orphan.",
    ),
    "SRC4113_12_3626_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3626_NEXT_TARGET.csv",
        "3627-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md",
        "3626 selected Gamma/Khat response action Helmholtz as next target.",
    ),
    "SRC4113_13_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4113_Bianchi_residual_closure_or_first_PPN_envelope_runner.py",
        "Reproducible generator for this 4113 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **row_base(),
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_string(path.exists()),
                "needle": needle,
                "needle_found": bool_string(path.exists() and needle in text),
                "role": role,
                "claim_allowed": bool_string(False),
                "valid_for_claim": bool_string(False),
            }
        )
    return rows


def bianchi_law_rows() -> List[dict]:
    rows = [
        (
            "BLC4113_0_parent_action",
            "single diffeomorphism-invariant parent action",
            "delta_xi S_parent=0",
            "Noether identity applies only to the whole retained system, not to selected convenient pieces.",
            "CONDITIONAL_PARENT_ACTION_NOT_SIGNED",
        ),
        (
            "BLC4113_1_noether_identity",
            "diffeomorphism Noether identity",
            "nabla_m(2E_g^{mn}) + E_A nabla^n Phi^A + E_psi D^n psi + B_boundary^n = 0",
            "Bianchi closure must come from parent symmetry plus Euler/boundary terms.",
            "EXACT_CONDITIONAL_IDENTITY_IMPORTED",
        ),
        (
            "BLC4113_2_residual_closure",
            "local residual closure law",
            "nabla_m[DeltaE_MTS^{mn}-kappa_eff DeltaT_MTS^{mn}]=C_B^n",
            "C_B^n is zero only when parent Euler/source/boundary package closes; otherwise it is an observable residual.",
            "EXACT_CONDITIONAL_CLOSURE_LAW_IMPORTED",
        ),
        (
            "BLC4113_3_not_sufficient",
            "closure is not local-GR silence",
            "nabla_m DeltaR^{mn}=0 does not imply DeltaR^{mn}=0",
            "A conserved residual can still fail gamma, beta, preferred-frame, Newton/source, clock or orbital tests.",
            "NO_SMUGGLING_GUARD",
        ),
        (
            "BLC4113_4_calibrated_drift",
            "calibrated constants consistency",
            "nabla_m[kappa_eff T^{mn}]=(nabla_m kappa_eff)T^{mn}+kappa_eff nabla_m T^{mn}",
            "Measured G_eff/alpha_eff are allowed, but local drift must be zeroed or bounded.",
            "DRIFT_WARNING_RETAINED",
        ),
    ]
    return [
        {
            **row_base(),
            "law_id": law_id,
            "piece": piece,
            "formula": formula,
            "effect": effect,
            "status": status,
            "source_id": "SRC4113_03_3625_bianchi",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for law_id, piece, formula, effect, status in rows
    ]


def ppn_envelope_rows() -> List[dict]:
    rows = [
        ("ENV4113_0_gamma", "gamma_minus_1", "gamma_minus_1=K_gamma_DeltaE*Pi_gamma(DeltaE_MTS)+K_gamma_readout*epsilon_readout+K_gamma_q*q_loc_projection", "MISSING_COMPONENT_VALUES_AND_BOUND"),
        ("ENV4113_1_beta", "beta_minus_1", "beta_minus_1=sum_abs(beta_source+beta_operator+beta_readout+beta_boundary)", "MISSING_SECOND_ORDER_COMPONENT_VALUES_AND_BOUND"),
        ("ENV4113_2_preferred_frame", "alpha_i;xi", "Delta_PF_abs=|alpha1|+|alpha2|+|alpha3|+|xi| from projected residual basis", "MISSING_PROJECTION_MATRIX_AND_BOUNDS"),
        ("ENV4113_3_conservation", "zeta_i;Bianchi leakage", "Delta_cons_abs=|Pi_zeta(C_B)|+|Pi_orbit(C_B)|", "MISSING_C_B_VALUE_AND_PROJECTION"),
        ("ENV4113_4_Newton_Poisson", "delta_Newton_MTS", "nabla^2 Phi-4*pi*G_eff*rho_H=Pi_00(DeltaE_MTS)-4*pi*G_eff*delta_rho_source+boundary", "MISSING_SOURCE_MASS_CLOSURE_AND_BOUND"),
        ("ENV4113_5_EM_source", "w_EM;Phi_EM_boundary", "Delta_EM_source_abs=|w_EM|*f_EM+|Phi_EM_boundary|/M_H_ref", "MISSING_EM_FRACTION_OR_FLUX_NORMALIZATION"),
        ("ENV4113_6_total", "Delta_local_GR_total_abs", "Delta_total_abs=sum_abs(ENV4113_0..ENV4113_5); pass only if each component has theorem-zero or numeric bound pass", "RUNNER_SCHEMA_READY_INPUTS_MISSING"),
    ]
    return [
        {
            **row_base(),
            "envelope_id": envelope_id,
            "observable_component": component,
            "prediction_formula_template": formula,
            "current_status": status,
            "runner_verdict": "BLOCKED_NOT_SCORED",
            "source_id": "SRC4113_05_3625_schema",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for envelope_id, component, formula, status in rows
    ]


def residual_inventory_rows() -> List[dict]:
    rows = [
        ("INV4113_0_DeltaE", "DeltaE_MTS_mn", "S_EH plus retained S_GK/S_selector/S_boundary/S_readout variations", "OWNER_DECOMPOSITION_AVAILABLE_NOT_SIGNED", "EH dominance and retained residual coefficient map missing"),
        ("INV4113_1_source_weight", "DeltaT_source;w_EM;kappa_J;delta_ellJ", "S_matter[e_obs,psi]+S_EM[g_obs,A,J] with same Hilbert/Noether source current", "CONDITIONAL_CURRENT_OWNER_NOT_SIGNED", "Pi_M/H_tau denominator and same-frame readout unsigned"),
        ("INV4113_2_coupling_drift", "delta_kappa;b_alpha;lambda_F2", "topological kappa sector plus parent EM level/fibre metric and unique F_Q^2 domain", "PARTIAL_KAPPA_CANDIDATE_ALPHA_LEVEL_UNSIGNED", "parent EM level/Q_* certificate missing"),
        ("INV4113_3_q_loc", "q_loc^nu", "S_GK[g,Phi] or response-doublet action whose Ward identity yields q_loc", "ACTION_EXISTENCE_AND_HELMHOLTZ_NOT_PROVED", "Gamma/Khat stress may be non-variational bookkeeping"),
        ("INV4113_4_GK_stress", "T_GK_mn;T_tau/P_mn", "positive auxiliary/response-doublet sector or topological exact sector", "CANDIDATE_NOT_MATCHED_TO_EXISTING_MTS_SYMBOLS", "positive operator/no-hair and physical residual lock not derived"),
        ("INV4113_5_PiM_boundary", "delta_PiM;Phi_EM_boundary;Q_boundary", "parent boundary symplectic metric, fixed Pi_M, Hamiltonian H_tau and fixed reference/boundary terms", "PROJECTOR_VARIATION_AND_DENOMINATOR_NOT_PARENT_DERIVED", "source mass can still be laundered through Pi_M/H_tau/reference"),
        ("INV4113_6_PPN_total", "Delta_PPN_abs", "derived weak-field/readout solution from the full owned local action", "AGGREGATE_SCHEMA_READY_COMPONENT_VALUES_MISSING", "beta, preferred-frame, source, boundary and q_loc projection coefficients missing"),
    ]
    return [
        {
            **row_base(),
            "inventory_id": inventory_id,
            "residual_symbol": symbol,
            "candidate_owner": owner,
            "current_status": status,
            "blocks": blocks,
            "source_id": "SRC4113_08_3626_inventory",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for inventory_id, symbol, owner, status, blocks in rows
    ]


def orphan_scorecard_rows() -> List[dict]:
    rows = [
        ("OSC4113_0_EH_matter_EM", "EH/matter/visible EM", "CONDITIONAL_STANDARD_OWNER", "parent descent of observed fields and source current/readout closure", "medium"),
        ("OSC4113_1_GK_q_loc", "Gamma/Khat/q_loc/GK stress", "HARD_ORPHAN", "S_GK variational owner or response-doublet physical lock", "highest"),
        ("OSC4113_2_PiM_source_denominator", "Pi_M/H_tau/source mass boundary denominator", "HARD_ORPHAN", "M_H_ref / Pi_M J_H / H_tau reference lock", "highest_parallel"),
        ("OSC4113_3_PPN_component_vector", "PPN/Newton component rows", "RUNNER_SCHEMA_ONLY", "weak-field projection from action-owned residuals", "after_owner_attempt_or_parallel_data_fill"),
    ]
    return [
        {
            **row_base(),
            "score_id": score_id,
            "sector": sector,
            "ownership_level": level,
            "main_gap": gap,
            "next_priority": priority,
            "source_id": "SRC4113_11_3626_scorecard",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for score_id, sector, level, gap, priority in rows
    ]


def decision_rows() -> List[dict]:
    rows = [
        (
            "DEC4113_0_bianchi",
            "Bianchi closure is derived as an exact conditional Noether law, not an axiom.",
            "CONDITIONAL_DERIVATION_IMPORTED",
            "do not claim closure until parent action/Euler/boundary package signs C_B^nu=0",
        ),
        (
            "DEC4113_1_envelope",
            "The first PPN/Newton envelope is explicit and refuses to score missing component values.",
            "RUNNER_SCHEMA_READY_BLOCKED_CORRECTLY",
            "fill component rows only from owner theorem or source-backed data",
        ),
        (
            "DEC4113_2_inventory",
            "Every local residual now has a candidate owner; the true hard orphan is GK/q_loc/T_GK, with Pi_M/H_tau parallel.",
            "OWNER_INVENTORY_IMPORTED",
            "attack highest-leverage orphan instead of recircling the full vector",
        ),
        (
            "DEC4113_3_claim_guard",
            "No local-GR/Newton/PPN/conservation claim follows.",
            "CLAIM_BLOCKED_NOT_WORK_BLOCKED",
            "Bianchi closure is necessary but not sufficient for local tests",
        ),
        (
            "DEC4113_4_next",
            "Next current-chain target is Gamma/Khat response-action Helmholtz or q_loc/T_GK bound rows.",
            "NEXT_TARGET_SELECTED",
            "4114-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md",
        ),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "next_action": next_action,
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
        for decision_id, decision, status, next_action in rows
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4113_0",
            "target_doc": "4114-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md",
            "target_script": "scripts/Y5_R2FR_4114_Gamma_Khat_response_action_Helmholtz_or_qloc_TGK_bound.py",
            "objective": "test whether Gamma_eff/K_hat/q_loc/T_GK are generated by a legitimate variational S_GK via Helmholtz, metric-response, Euler, double-zero and boundary clauses; if not, fill q_loc/T_GK PPN/Newton component-bound rows as nonclaim",
            "success_gate": "either S_GK passes action-existence, Euler closure, double-zero and boundary no-flux gates, or q_loc/T_GK receive component-level nonclaim coefficient rows with value/unit/bound/source placeholders explicit",
            "reason": "4113 imports Bianchi closure and residual inventory; S_GK is the highest-leverage orphan because it controls DeltaE, q_loc, T_GK, Bianchi and PPN pressure together.",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4113_0",
            "decision": DECISION,
            "strongest_result": "4113 imports the conditional Noether/Bianchi residual closure law, the first PPN/Newton no-cancellation envelope schema, and the local residual owner inventory into the active 411x spine.",
            "what_changed": "The local-GR path now has a consistency law plus a component test scaffold; the bottleneck is no longer vague conservation but the hard orphan S_GK/q_loc/T_GK and the parallel Pi_M/H_tau source denominator.",
            "still_missing": "parent action/Euler/boundary package for C_B^nu=0, variational S_GK/Helmholtz proof, q_loc/T_GK weak-field projections, Pi_M/H_tau source denominator, and source-backed PPN/Newton component bounds",
            "claim_state": "no local_GR_Newton_PPN_conservation_WEP_R10_R11 claim",
            "next_target": "4114 Gamma/Khat response action Helmholtz or q_loc/T_GK bound rows",
            "claim_allowed": bool_string(False),
            "valid_for_claim": bool_string(False),
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4113_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4113_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4113_BIANCHI_CLOSURE_LAW": SOURCE_DIR / "P8_Y5_R2FR_4113_BIANCHI_CLOSURE_LAW.csv",
        "P8_Y5_R2FR_4113_PPN_NEWTON_ENVELOPE": SOURCE_DIR / "P8_Y5_R2FR_4113_PPN_NEWTON_ENVELOPE.csv",
        "P8_Y5_R2FR_4113_RESIDUAL_OWNER_INVENTORY": SOURCE_DIR / "P8_Y5_R2FR_4113_RESIDUAL_OWNER_INVENTORY.csv",
        "P8_Y5_R2FR_4113_ORPHAN_SCORECARD": SOURCE_DIR / "P8_Y5_R2FR_4113_ORPHAN_SCORECARD.csv",
        "P8_Y5_R2FR_4113_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4113_DECISION_GATE.csv",
        "P8_Y5_R2FR_4113_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4113_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4113_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4113_STATUS.csv",
    }


def markdown_table(rows: List[dict], columns: List[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    status = status_rows()[0]
    lines = [
        "# 4113 - Bianchi residual closure or first PPN envelope runner",
        "",
        "## Verdict",
        "4113 imports the useful `3625-3626` work into the active `411x` spine: Bianchi closure is now an exact conditional Noether law, the first PPN/Newton envelope exists, and every local residual has a candidate owner inventory.",
        "",
        "This is still not a local-GR claim. The key guard is that Bianchi closure is necessary, not sufficient: a conserved residual can still fail `gamma`, `beta`, preferred-frame, Newton/source, clock, or orbital tests.",
        "",
        "## Strongest Current Result",
        f"- `{status['decision']}`",
        f"- {status['strongest_result']}",
        f"- {status['what_changed']}",
        "",
        "## Bianchi / Noether Closure Law",
        markdown_table(bianchi_law_rows(), ["law_id", "piece", "formula", "effect", "status"]),
        "",
        "## PPN / Newton Envelope",
        markdown_table(ppn_envelope_rows(), ["envelope_id", "observable_component", "prediction_formula_template", "current_status", "runner_verdict"]),
        "",
        "## Residual Owner Inventory",
        markdown_table(residual_inventory_rows(), ["inventory_id", "residual_symbol", "candidate_owner", "current_status", "blocks"]),
        "",
        "## Orphan Scorecard",
        markdown_table(orphan_scorecard_rows(), ["score_id", "sector", "ownership_level", "main_gap", "next_priority"]),
        "",
        "## Decisions",
        markdown_table(decision_rows(), ["decision_id", "decision", "status", "next_action"]),
        "",
        "## Next Target",
        markdown_table(next_target_rows(), ["target_doc", "target_script", "objective", "success_gate"]),
        "",
        "## Claim Ceiling",
        "- No local-GR, Newton, PPN, WEP, R10/R11, Maxwell-source, or conservation pass is claimed.",
        "- The next proof target is the hard orphan: `S_GK/q_loc/T_GK` variational ownership.",
        "- `Pi_M/H_tau/source denominator` remains a parallel pressure point for Newton/source mass.",
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4113_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4113_BIANCHI_CLOSURE_LAW"], bianchi_law_rows())
    write_csv(outputs["P8_Y5_R2FR_4113_PPN_NEWTON_ENVELOPE"], ppn_envelope_rows())
    write_csv(outputs["P8_Y5_R2FR_4113_RESIDUAL_OWNER_INVENTORY"], residual_inventory_rows())
    write_csv(outputs["P8_Y5_R2FR_4113_ORPHAN_SCORECARD"], orphan_scorecard_rows())
    write_csv(outputs["P8_Y5_R2FR_4113_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4113_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4113_STATUS"], status_rows())
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
                "claim_allowed": bool_string(False),
            }
        )

    missing_sources = [source_id for source_id, (path, _, _) in LOCAL_SOURCES.items() if not path.exists()]
    missing_needles = []
    for source_id, (path, needle, _) in LOCAL_SOURCES.items():
        if path.exists() and needle not in read_text(path):
            missing_needles.append(f"{source_id}:{needle}")
    add("VAL4113_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4113_1_sources_contain_needles", "every local source contains expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_ok = True
    parse_counts = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4113_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    bianchi_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4113_BIANCHI_CLOSURE_LAW"]))
    bianchi_ok = all(token in bianchi_text for token in ["Noether", "C_B^n", "nabla_m[DeltaE_MTS", "NO_SMUGGLING_GUARD"])
    add("VAL4113_3_bianchi_law", "Bianchi closure law and no-smuggling guard present", bianchi_ok, "Bianchi tokens checked")

    ppn_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4113_PPN_NEWTON_ENVELOPE"]))
    ppn_ok = all(token in ppn_text for token in ["gamma_minus_1", "beta_minus_1", "delta_Newton_MTS", "Delta_local_GR_total_abs", "BLOCKED_NOT_SCORED"])
    add("VAL4113_4_ppn_envelope", "PPN/Newton envelope schema blocks missing inputs", ppn_ok, "PPN tokens checked")

    inventory_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4113_RESIDUAL_OWNER_INVENTORY"]))
    inventory_ok = all(token in inventory_text for token in ["DeltaE_MTS", "q_loc", "T_GK", "Pi_M/H_tau", "Delta_PPN_abs"])
    add("VAL4113_5_inventory", "residual owner inventory covers major residuals", inventory_ok, "inventory tokens checked")

    orphan_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4113_ORPHAN_SCORECARD"]))
    orphan_ok = all(token in orphan_text for token in ["HARD_ORPHAN", "Gamma/Khat/q_loc/GK stress", "Pi_M/H_tau/source mass boundary denominator"])
    add("VAL4113_6_orphan_scorecard", "orphan scorecard identifies GK and PiM/Htau", orphan_ok, "orphan tokens checked")

    decision_rows_local = parse_csv(outputs["P8_Y5_R2FR_4113_DECISION_GATE"])
    next_decision = any(row.get("status") == "NEXT_TARGET_SELECTED" and "4114" in row.get("next_action", "") for row in decision_rows_local)
    add("VAL4113_7_decision", "decision gate selects 4114 GK/q_loc target", next_decision, str(decision_rows_local))

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4113_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4114-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md"
    add("VAL4113_8_next_target", "next target is 4114 Gamma/Khat Helmholtz", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4113_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("decision") == DECISION and "no local_GR" in status_rows_local[0].get("claim_state", "")
    add("VAL4113_9_status", "status records Bianchi/inventory import and no-claim state", status_ok, "status row checked")

    all_rows = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") for row in all_rows)
    add("VAL4113_10_no_claim_flags", "all generated rows remain no-claim", no_claim, f"row_count={len(all_rows)}")

    output_paths = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4113*")) or any(FORMALIZATION.rglob("4113-Y5-R2FR*"))
    add("VAL4113_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4113_12_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4113_VALIDATION.csv"
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
