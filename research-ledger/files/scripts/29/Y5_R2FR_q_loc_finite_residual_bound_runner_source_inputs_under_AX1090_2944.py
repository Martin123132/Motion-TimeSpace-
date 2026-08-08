from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2944"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2944-Y5-R2FR-q_loc-finite-residual-bound-runner-source-inputs-under-AX1090.md"

SRC_2943_DOC = ROOT / "2943-Y5-R2FR-A-mu-Ward-Stueckelberg-identity-or-q_loc-finite-bound-runner-under-AX1090.md"
SRC_2943_REQ = RESIDUALS / "P8_Y5_R2FR_2943_BOUND_INPUT_REQUIREMENTS.csv"
SRC_2943_START = RESIDUALS / "P8_Y5_R2FR_2943_QLOC_FINITE_BOUND_RUNNER_START.csv"
SRC_2943_NEXT = RESIDUALS / "P8_Y5_R2FR_2943_NEXT_TARGET.csv"
SRC_2943_OBS = RESIDUALS / "P8_Y5_R2FR_2943_WARD_OBSTRUCTION_DECOMPOSITION.csv"
SRC_2943_CUR = RESIDUALS / "P8_Y5_R2FR_2943_CURRENT_SOURCE_EVIDENCE_AUDIT.csv"
SRC_2465_BOUNDARY = RESIDUALS / "P8_Y5_PARENT_ACTION_2465_BOUNDARY_AUDIT.csv"
SRC_2465_SOURCE = RESIDUALS / "P8_Y5_PARENT_ACTION_2465_SOURCE_CURRENT_DESCENT.csv"
SRC_2467_DIV = RESIDUALS / "P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv"
SRC_2467_EXCHANGE = RESIDUALS / "P8_Y5_HILBERT_CURRENT_2467_EXCHANGE_CURRENT_IDENTITY.csv"
SRC_2467_WORLDTUBE = RESIDUALS / "P8_Y5_HILBERT_CURRENT_2467_WORLDTUBE_SURFACE_GATE.csv"
SRC_2615_EXCHANGE = RESIDUALS / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv"
SRC_2577_SELECTOR = RESIDUALS / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_RESIDUAL_INPUT_LEDGER.csv"
SRC_QLOC_SPEC = RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv"
SRC_GK_CONTRACT = RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"
SRC_GAMMA_DECISION = RESIDUALS / "P8_GAMMA_OWNER_OR_QLOC_BOUND_DECISION.csv"
SRC_PLOC_AUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_1523_PLOC_PROJECTOR_AUDIT.csv"
SRC_KHAT_ORIGIN = RESIDUALS / "P8_Y5_PARENT_QLOC_1525_KHAT_ORIGIN_AUDIT.csv"
SRC_KHAT_ADOPTION = RESIDUALS / "P8_Y5_PARENT_QLOC_1527_KHAT_ADOPTION_ROW.csv"
SRC_PLOC_UNIT = RESIDUALS / "P8_Y5_R2FR_2810_PLOC_UNIT_CERTIFICATE.csv"
SRC_PLOC_COMM = RESIDUALS / "P8_Y5_R2FR_2811_PLOC_COMMUTATOR_THEOREM_ATTEMPT.csv"
SRC_MASS_FLUX = RESIDUALS / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv"
SRC_SOURCE_NORM = RESIDUALS / "P8_R11_SOURCE_NORMALIZATION_MISSING_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2944_SOURCE_REGISTER.csv",
    "inputs": RESIDUALS / "P8_Y5_R2FR_2944_QLOC_BOUND_INPUT_STATUS_LEDGER.csv",
    "partials": RESIDUALS / "P8_Y5_R2FR_2944_PARTIAL_DERIVATION_LEDGER.csv",
    "arenas": RESIDUALS / "P8_Y5_R2FR_2944_LOCAL_ARENA_PROJECTION_GATE.csv",
    "hierarchy": RESIDUALS / "P8_Y5_R2FR_2944_BLOCKER_HIERARCHY.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2944_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2944_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2944_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2944_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2944_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "input_copy": LOCAL_BOUNDS / "Qloc_bound_input_status_ledger_2944_NONCLAIM.csv",
    "hierarchy_copy": LOCAL_BOUNDS / "Qloc_blocker_hierarchy_2944_NONCLAIM.csv",
    "partial_copy": PARENT_ACTION / "Qloc_partial_derivation_ledger_2944_NONCLAIM.csv",
    "arena_copy": LOCAL_BOUNDS / "Qloc_local_arena_projection_gate_2944_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2944_SOURCE_NORMALIZED_QLOC_INPUT_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2944_00_2943_doc", SRC_2943_DOC, "NEXT2943_0_2944;Validation overall: `True`", "2943 handoff to q_loc finite source inputs"),
        ("SRC2944_01_2943_req", SRC_2943_REQ, "REQ2943_0_C_bulk_source;REQ2943_6_C_denominator", "seven C_i bound requirements"),
        ("SRC2944_02_2943_start", SRC_2943_START, "QBR2943_0_total_envelope;QBR2943_4_verdict", "finite envelope start"),
        ("SRC2944_03_2943_next", SRC_2943_NEXT, "NEXT2943_0_2944", "machine-readable 2944 target"),
        ("SRC2944_04_2943_obs", SRC_2943_OBS, "OBS2943_1_Box_Gamma;OBS2943_4_projection", "obstruction-to-C_i map"),
        ("SRC2944_05_2943_current", SRC_2943_CUR, "CUR2943_0_Hilbert_definition;CUR2943_4_universality", "current/source evidence audit"),
        ("SRC2944_06_2465_boundary", SRC_2465_BOUNDARY, "BND2465_0_A_boundary;BND2465_4_distributional_source", "A/Gamma boundary and jump blockers"),
        ("SRC2944_07_2465_source", SRC_2465_SOURCE, "SRC2465_1_vertical_generator;SRC2465_6_candidate_route", "source-current descent blockers"),
        ("SRC2944_08_2467_divergence", SRC_2467_DIV, "DIV2467_1_full_divergence;DIV2467_5_generic_clock", "exact Hilbert-current divergence"),
        ("SRC2944_09_2467_exchange", SRC_2467_EXCHANGE, "EXC2467_0_required_identity;EXC2467_3_local_stationary_escape", "exchange-current requirement"),
        ("SRC2944_10_2467_worldtube", SRC_2467_WORLDTUBE, "WTG2467_1_stationary_surface;WTG2467_4_external_vacuum", "worldtube stationary/exterior support"),
        ("SRC2944_11_2615_exchange", SRC_2615_EXCHANGE, "NEC2615_2_weight_collapse;NEC2615_5_current_verdict", "conditional source-weight collapse"),
        ("SRC2944_12_2577_selector", SRC_2577_SELECTOR, "SRR2577_0_W_selector;SRR2577_6_delta_ellJ", "source selector/coupling residuals"),
        ("SRC2944_13_qloc_spec", SRC_QLOC_SPEC, "QB516_0_compact_shell_budget;QB516_4_R11_operator", "older q_loc bound runner spec"),
        ("SRC2944_14_gk_contract", SRC_GK_CONTRACT, "GK513_2_Euler_closure;GK513_5_boundary_no_flux", "Gamma/Khat action contract"),
        ("SRC2944_15_gamma_decision", SRC_GAMMA_DECISION, "D516_2;D516_3", "Gamma owner or bound decision"),
        ("SRC2944_16_ploc_audit", SRC_PLOC_AUDIT, "PLOC1523_1_parent_ownership;PLOC1523_4_verdict", "P_loc ownership audit"),
        ("SRC2944_17_khat_origin", SRC_KHAT_ORIGIN, "KOR1525_3_current_symbol_match;KOR1525_5_verdict", "Khat origin and symbol mismatch"),
        ("SRC2944_18_khat_adoption", SRC_KHAT_ADOPTION, "KAD1527_0_adoption_contract;KAD1527_4_verdict", "staged Khat adoption row"),
        ("SRC2944_19_ploc_unit", SRC_PLOC_UNIT, "PLC2810_2_qDelta_units;PLC2810_5_verdict", "P_loc units partial pass"),
        ("SRC2944_20_ploc_comm", SRC_PLOC_COMM, "COM2811_0_product_rule;COM2811_4_verdict", "P_loc commutator obstruction"),
        ("SRC2944_21_mass_flux", SRC_MASS_FLUX, "MF2_Euler_flux_closure;MF7_constant_universal_coupling_needed", "mass-flux/source calibration contract"),
        ("SRC2944_22_source_norm", SRC_SOURCE_NORM, "R11SN_0_radial_Meff_hair;R11SN_3_bulk_X_Yukawa_tail", "source-normalization missing ledger"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def input_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "input_id": "IN2944_0_C_bulk_source",
            "input_name": "C_bulk_source",
            "bound_object": "||P_loc J_M||_collar",
            "current_best_evidence": "Hilbert candidate J_M^nu=ell_J T^{nu rho}tau_rho exists; exterior compact-support zero is conditional.",
            "partial_closure": "source-free exterior can be quiet if T=0, tau support is stationary, P_loc is fixed, and side flux vanishes.",
            "missing_for_score": "parent ell_J scale, source support/worldtube selector, P_loc ownership, and source/current universality",
            "status": "PARTIAL_STATIONARY_SUPPORT_INPUT_MISSING",
            "arenas_blocked": "R10;PPN;Newton;clock;orbital",
        },
        {
            "input_id": "IN2944_1_C_Gamma_curvature",
            "input_name": "C_Gamma_curvature",
            "bound_object": "||P_loc nabla Gamma_eff|| or ||Box Gamma_eff||",
            "current_best_evidence": "Gamma/Khat action contract keeps Euler closure and double-zero as not derived.",
            "partial_closure": "none claim-grade; can only retain as symbolic curvature/memory tail.",
            "missing_for_score": "Gamma_eff parent equation, local extremum law, memory projection, units and collar norm",
            "status": "MISSING_GAMMA_PARENT_LAW",
            "arenas_blocked": "R10;PPN;clock;orbital",
        },
        {
            "input_id": "IN2944_2_C_source_divergence",
            "input_name": "C_source_divergence",
            "bound_object": "||nabla_mu J_M^mu||",
            "current_best_evidence": "2467 derives the product-rule divergence exactly.",
            "partial_closure": "zero if ell_J is constant, matter stress is conserved, tau is Killing, and exchange/side flux is absent.",
            "missing_for_score": "parent-owned exchange current I_tau/I_A or numeric tau-strain/ell_J drift bound",
            "status": "DERIVED_FORMULA_NOT_BOUNDED",
            "arenas_blocked": "PPN;clock;orbital;Gdot;Newton",
        },
        {
            "input_id": "IN2944_3_C_boundary_flux",
            "input_name": "C_boundary_flux",
            "bound_object": "||n_mu K_hat^{mu nu}|| + ||n.A|| + worldtube jump terms",
            "current_best_evidence": "2465 boundary audit explicitly records missing A/Gamma boundary conditions and source jump conditions.",
            "partial_closure": "fixed Dirichlet/Neumann/counterterm options are known but not parent-selected.",
            "missing_for_score": "one signed boundary condition/counterterm and compact collar jump theorem or finite flux value",
            "status": "MISSING_BOUNDARY_AND_JUMP_CONDITION",
            "arenas_blocked": "Newton;PPN;R10;clock;orbital",
        },
        {
            "input_id": "IN2944_4_C_projector_leak",
            "input_name": "C_projector_leak",
            "bound_object": "||delta P_loc|| and ||[nabla,P_loc]X||",
            "current_best_evidence": "P_loc can be typed dimensionless, but norm-one and commutator-zero are not certified.",
            "partial_closure": "unit chain is sharpened: P_loc is a same-domain dimensionless projector if parent typing is signed.",
            "missing_for_score": "parent-owned orthogonal projector, local inner product, covariant parallel collar, domain/readout independence",
            "status": "PARTIAL_UNITS_PASS_COMMUTATOR_ACTIVE",
            "arenas_blocked": "PPN;R10;clock;orbital",
        },
        {
            "input_id": "IN2944_5_C_symbol_mismatch",
            "input_name": "C_symbol_mismatch",
            "bound_object": "||Khat_old - partial L_K/partial(nabla A)||",
            "current_best_evidence": "trace-free improvement K_L route is the least-scrutiny candidate but is not live K_hat.",
            "partial_closure": "a staged adoption row exists for a precise K_hat response definition.",
            "missing_for_score": "signed parent action term, phi owner, coefficient, boundary convention, trace-free projection and live-symbol adoption",
            "status": "STAGED_KHAT_MATCH_NOT_PROMOTED",
            "arenas_blocked": "PPN;R10;Newton;local_GR",
        },
        {
            "input_id": "IN2944_6_C_denominator",
            "input_name": "C_denominator",
            "bound_object": "M_H_ref, Pi_M J_H, G_ref/source charge normalization",
            "current_best_evidence": "mass-flux and source-normalization ledgers say calibration, Pi_M ownership and universal coupling remain unsigned.",
            "partial_closure": "a common source scale may be absorbed only after universality and no drift/range/species/frame dependence are proved.",
            "missing_for_score": "absolute parent calibration, Pi_M/Hamiltonian equality, constant kappa/ell_J, no radial/range/boundary/source hair",
            "status": "ROOT_DENOMINATOR_BLOCKER",
            "arenas_blocked": "Newton;R10;PPN;clock;orbital;WEP",
        },
        {
            "input_id": "IN2944_7_total",
            "input_name": "q_loc_total_envelope",
            "bound_object": "||q_loc|| <= sum_i C_i",
            "current_best_evidence": "2944 resolves the queue into a finite-input ledger, not a score-ready bound.",
            "partial_closure": "some algebraic identities are exact; no full local arena projection is source-ready.",
            "missing_for_score": "all C_i source-backed values/theorems plus arena maps and denominator",
            "status": "NOT_SOURCE_READY",
            "arenas_blocked": "all_local_arenas",
        },
    ]
    return [add_common(row) for row in rows]


def partial_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "partial_id": "PD2944_0_source_divergence_identity",
            "derived_piece": "nabla_nu J_M^nu = (nabla_nu ell_J)T^{nu rho}tau_rho + ell_J(nabla_nu T^{nu rho})tau_rho + ell_J T^{nu rho}nabla_nu tau_rho",
            "value": "exact product-rule formula",
            "use": "turns source divergence into measurable tau-strain/ell_J/exchange inputs",
            "why_not_claim": "generic clock strain and exchange current remain unsigned",
        },
        {
            "partial_id": "PD2944_1_stationary_collar",
            "derived_piece": "If tau is Killing, ell_J is constant, matter is on shell and side flux is zero, Q is surface-independent.",
            "value": "conditional local support",
            "use": "possible low-scrutiny local theorem branch",
            "why_not_claim": "boundary/jump/P_loc/source normalization remain open",
        },
        {
            "partial_id": "PD2944_2_projector_product_rule",
            "derived_piece": "nabla(P_loc X)=P_loc nabla X + (nabla P_loc)X plus connection/domain terms",
            "value": "exact obstruction identity",
            "use": "makes C_projector_leak finite rather than invisible",
            "why_not_claim": "P_loc parallel-chainmap theorem is conditional and unsigned",
        },
        {
            "partial_id": "PD2944_3_Khat_improvement_route",
            "derived_piece": "trace-free scalar-curvature improvement can generate the K_L tensor shape",
            "value": "least-scrutiny candidate origin",
            "use": "points to a clean symbol-lock route",
            "why_not_claim": "live K_hat is not adopted as K_L by parent action",
        },
        {
            "partial_id": "PD2944_4_common_calibration_rule",
            "derived_piece": "connected ordinary matter would collapse relative source weights to a common calibration",
            "value": "conditional coupling theorem",
            "use": "could protect Newton/WEP/R10 from source-weight freedom",
            "why_not_claim": "ordinary-matter exchange connectivity and source-shadow exclusion remain parent-unsigned",
        },
    ]
    return [add_common(row) for row in rows]


def arena_rows() -> list[dict[str, Any]]:
    rows = [
        ("AR2944_0_Newton", "Newton/Poisson/source-mass", "C_denominator;C_boundary_flux;C_bulk_source", "M_H_ref/Pi_M/G_ref and compact source flux", "BLOCKED_BY_DENOMINATOR"),
        ("AR2944_1_PPN", "gamma beta alpha_i xi", "C_source_divergence;C_projector_leak;C_symbol_mismatch;C_Gamma_curvature", "metric response map and source-normalized weak-field solution", "BLOCKED_BY_SOURCE_AND_SYMBOL"),
        ("AR2944_2_R10", "short-range alpha(lambda)", "C_Gamma_curvature;C_bulk_source;C_denominator;C_symbol_mismatch", "lambda_X, alpha amplitude, denominator and real curve comparison", "BLOCKED_BY_PARENT_INPUTS"),
        ("AR2944_3_clocks", "clock/time tests", "C_source_divergence;C_denominator", "tau-strain/exchange-current value and constant coupling", "BLOCKED_BY_DYNAMIC_EXCHANGE"),
        ("AR2944_4_orbital", "orbital systems", "C_source_divergence;C_boundary_flux;C_denominator", "side flux, tau drift, measured GM and non-fitted source mass", "BLOCKED_BY_SOURCE_NORMALIZATION"),
        ("AR2944_5_WEP", "source universality/composition", "C_denominator;C_bulk_source", "connected source graph, no species/source-shadow channel, common measure/current owner", "BLOCKED_BY_COUPLING_OWNER"),
    ]
    return [
        add_common(
            {
                "arena_id": arena_id,
                "arena": arena,
                "required_inputs": required_inputs,
                "missing_bridge": missing_bridge,
                "status": status,
            }
        )
        for arena_id, arena, required_inputs, missing_bridge, status in rows
    ]


def hierarchy_rows() -> list[dict[str, Any]]:
    rows = [
        (1, "BH2944_0_denominator_source_normalization", "C_denominator", "without source mass/G_ref/ell_J/kappa normalization no local bound can be compared honestly", "attack first"),
        (2, "BH2944_1_source_divergence_exchange", "C_source_divergence", "exact formula exists, so a theorem or finite tau-strain value may be achievable next", "attack with denominator"),
        (3, "BH2944_2_boundary_flux", "C_boundary_flux", "bulk silence can be spoiled by boundary/jump terms; must be zeroed or bounded before claims", "attack before scoring"),
        (4, "BH2944_3_projector_and_Khat_symbol", "C_projector_leak;C_symbol_mismatch", "projection and K_hat notation can manufacture fake closure if not locked", "parallel technical track"),
        (5, "BH2944_4_Gamma_curvature", "C_Gamma_curvature", "parent Gamma law remains hardest and may need action-level derivation", "defer until source denominator branch is locked"),
    ]
    return [
        add_common(
            {
                "priority": priority,
                "blocker_id": blocker_id,
                "input_focus": input_focus,
                "reason": reason,
                "recommendation": recommendation,
            }
        )
        for priority, blocker_id, input_focus, reason, recommendation in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2944_0_q_loc_bound_ready", "finite q_loc bound is source-ready", False, "all C_i remain theorem/numeric-input missing", False),
        ("CG2944_1_Newton_GR", "Newton/local-GR branch derived", False, "denominator/source normalization and PPN map blocked", False),
        ("CG2944_2_R10", "R10/local fifth-force pass", False, "alpha(lambda) cannot be claimed without C_i values and denominator", False),
        ("CG2944_3_PPN", "PPN residual vector pass", False, "source divergence, projector and Khat symbol locks missing", False),
        ("CG2944_4_stationary_local_support", "stationary local collar theorem accepted as full proof", False, "conditional support only, not dynamic/local-GR proof", False),
        ("CG2944_5_public_claim", "public claim allowed from 2944", False, "private nonclaim checkpoint", False),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": allowed,
            }
        )
        for gate_id, claim, passed, status, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2944_0_runner_built", "q_loc finite residual runner input ledger is built", "all seven C_i terms are now mapped to concrete missing theorems or finite inputs", "use ledger rather than plateau axiom"),
        ("DEC2944_1_primary_blocker", "source denominator is the first wall", "M_H_ref/Pi_M/G_ref/ell_J/kappa normalization blocks every empirical arena", "target denominator plus source-current scale next"),
        ("DEC2944_2_best_partial_win", "source divergence has an exact formula", "2467 gives a real expression, so finite tau-strain/exchange bounds are more tractable than blind Gamma law hunting", "derive stationary/source-normalized branch first"),
        ("DEC2944_3_not_over", "Gamma law remains hard but not the only route", "local scoring can progress by bounding q_loc components even before proving full zero", "keep C_Gamma retained"),
        ("DEC2944_4_claim_policy", "no claims unlocked", "partial identities are useful engineering, not proof of GR reduction", "continue private nonclaim gates"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "next_action": next_action,
            }
        )
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2944_0_2945",
                "priority": "selected_primary",
                "next_doc": "2945-Y5-R2FR-source-normalized-stationary-q_loc-current-scale-or-denominator-blocker-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_source_normalized_stationary_q_loc_current_scale_or_denominator_blocker_under_AX1090_2945.py",
                "objective": "Try the least-scrutiny next derivation: combine Hilbert current, stationary collar, constant ell_J/kappa, Pi_M/M_H_ref calibration and no side flux into a source-normalized local q_loc input. If it fails, emit the exact denominator/source-scale blocker rows for R10, PPN, clocks and orbital tests.",
                "include": "C_denominator;C_source_divergence;C_bulk_source;stationary tau;ell_J;kappa;Pi_M;M_H_ref;side flux;source selector residuals",
                "exclude": "Gamma zero axiom; direct measured-GM fitting; A_mu multiplier adoption; local-GR/Newton/R10 claim; GitHub action; formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("input_copy", OUTPUTS["inputs"], BRANCH_OUTPUTS["input_copy"]),
        ("hierarchy_copy", OUTPUTS["hierarchy"], BRANCH_OUTPUTS["hierarchy_copy"]),
        ("partial_copy", OUTPUTS["partials"], BRANCH_OUTPUTS["partial_copy"]),
        ("arena_copy", OUTPUTS["arenas"], BRANCH_OUTPUTS["arena_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, copy_path in copies:
        if source_path.exists():
            shutil.copyfile(source_path, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "copy_path": str(copy_path),
                    "source_exists": source_path.exists(),
                    "copy_exists": copy_path.exists(),
                }
            )
        )
    return rows


def validation_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_has_2944 = False
    if FORMALIZATION.exists():
        formalization_has_2944 = any(FORMALIZATION.rglob("*2944*"))
    inputs = read_csv_rows(OUTPUTS["inputs"])
    hierarchy = read_csv_rows(OUTPUTS["hierarchy"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_target = read_csv_rows(OUTPUTS["next"])
    checks = [
        ("VAL2944_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2944_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2944_2_all_inputs_represented", len([row for row in inputs if row.get("input_id", "").startswith("IN2944_")]) >= 8, "all q_loc C_i inputs plus total row are represented", True),
        ("VAL2944_3_inputs_nonclaim", all(row.get("valid_for_claim") == "False" for row in inputs), "all input rows remain nonclaim", True),
        ("VAL2944_4_total_not_ready", any(row.get("input_id") == "IN2944_7_total" and row.get("status") == "NOT_SOURCE_READY" for row in inputs), "total q_loc envelope is not source-ready", True),
        ("VAL2944_5_denominator_primary", any(row.get("priority") == "1" and row.get("input_focus") == "C_denominator" for row in hierarchy), "denominator/source normalization selected as primary blocker", True),
        ("VAL2944_6_claims_blocked", all(row.get("claim_allowed") == "False" for row in claims), "all claims blocked", True),
        ("VAL2944_7_next_target_selected", any(row.get("next_id") == "NEXT2944_0_2945" for row in next_target), "2945 source-normalized q_loc target selected", True),
        ("VAL2944_8_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        ("VAL2944_9_csvs_parse", all(csv_parses(path) for path in generated_csvs), "all generated CSV files parse", True),
        ("VAL2944_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2944_11_formalization_clean", not formalization_has_2944, "no 2944 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "check": check, "required": required} for validation_id, passed, check, required in checks]
    rows.append({"validation_id": "VAL2944_OVERALL", "passed": overall, "check": "2944 validation overall", "required": True})
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    partials: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    hierarchy: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation if row["validation_id"] == "VAL2944_OVERALL")["passed"]
    text = f"""# 2944 - Y5 R2FR: q_loc finite residual bound runner source inputs under AX1090

Status: `Y5_R2FR_2944_q_loc_finite_input_ledger_built_not_source_ready_denominator_primary`

Claim ceiling: `q_loc_bound_not_source_ready_no_Newton_no_local_GR_no_R10_no_PPN_no_public_claim`

2944 converts the physical `q_loc` problem from a symbolic envelope into a concrete input ledger. The useful result is not a pass; it is a sharper attack order. The finite envelope is

`||q_loc||_collar <= C_bulk_source + C_Gamma_curvature + C_source_divergence + C_boundary_flux + C_projector_leak + C_symbol_mismatch`.

The missing denominator/source-normalization object is just as important as the numerator terms: without `M_H_ref`, `Pi_M J_H`, `G_ref`, `ell_J` and `kappa` fixed by the parent theory, even a small-looking numerator cannot be honestly compared to Newton, PPN, R10, clocks or orbital systems.

The best next route is not to keep smacking the hardest Gamma wall. The least-scrutiny route is to try the source-normalized stationary collar: Hilbert current plus Killing/local stationary `tau`, constant `ell_J/kappa`, parent `Pi_M/M_H_ref` calibration and no side flux. If that route fails, it gives exact denominator/source-scale blocker rows.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## q_loc Bound Input Status Ledger

{md_table(inputs, ["input_id", "input_name", "bound_object", "partial_closure", "missing_for_score", "status", "arenas_blocked"])}

## Partial Derivation Ledger

{md_table(partials, ["partial_id", "derived_piece", "value", "use", "why_not_claim"])}

## Local Arena Projection Gate

{md_table(arenas, ["arena_id", "arena", "required_inputs", "missing_bridge", "status"])}

## Blocker Hierarchy

{md_table(hierarchy, ["priority", "blocker_id", "input_focus", "reason", "recommendation"])}

## Claim Gates

{md_table(claims, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branches, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{overall}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    write_csv(OUTPUTS["sources"], source_rows)

    inputs = input_rows()
    partials = partial_rows()
    arenas = arena_rows()
    hierarchy = hierarchy_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["inputs"], inputs)
    write_csv(OUTPUTS["partials"], partials)
    write_csv(OUTPUTS["arenas"], arenas)
    write_csv(OUTPUTS["hierarchy"], hierarchy)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(source_rows)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(source_rows, inputs, partials, arenas, hierarchy, claims, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL2944_OVERALL")["passed"]
    print(f"2944 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
