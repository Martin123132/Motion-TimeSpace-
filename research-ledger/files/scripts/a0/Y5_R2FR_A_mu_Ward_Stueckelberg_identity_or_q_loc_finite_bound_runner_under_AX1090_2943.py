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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2943"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2943-Y5-R2FR-A-mu-Ward-Stueckelberg-identity-or-q_loc-finite-bound-runner-under-AX1090.md"

SRC_2942_DOC = ROOT / "2942-Y5-R2FR-vertical-generator-origin-gauge-symmetry-or-A-mu-closure-demotion-under-AX1090.md"
SRC_2942_NEXT = RESIDUALS / "P8_Y5_R2FR_2942_NEXT_TARGET.csv"
SRC_2942_GAUGE = RESIDUALS / "P8_Y5_R2FR_2942_GAUGE_SYMMETRY_WARD_GATE.csv"
SRC_2942_BOUNDS = RESIDUALS / "P8_Y5_R2FR_2942_QLOC_FINITE_BOUND_HANDOFF.csv"
SRC_2942_DEMOTION = RESIDUALS / "P8_Y5_R2FR_2942_SGK_CLOSURE_DEMOTION_LEDGER.csv"
SRC_2942_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2942_A_MU_PARENT_ADOPTION_CONTRACT.csv"
SRC_2465_VARIATION = RESIDUALS / "P8_Y5_PARENT_ACTION_2465_VARIATION_AUDIT.csv"
SRC_2465_SOURCE = RESIDUALS / "P8_Y5_PARENT_ACTION_2465_SOURCE_CURRENT_DESCENT.csv"
SRC_2465_BOUNDARY = RESIDUALS / "P8_Y5_PARENT_ACTION_2465_BOUNDARY_AUDIT.csv"
SRC_WARD_OWNER = RESIDUALS / "P8_Ward_source_owner_identity_CONTRACT.csv"
SRC_WARD_UNIVERSALITY = RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv"
SRC_EULER_CHAIN = RESIDUALS / "P8_Y5_EULER_WARD_CHAIN_TEST.csv"
SRC_EULER_DECISION = RESIDUALS / "P8_Y5_EULER_WARD_DECISION.csv"
SRC_GAUGE_NOETHER = RESIDUALS / "P8_Y5_PARENT_QLOC_1555_GAUGE_NOETHER_ROUTE_AUDIT.csv"
SRC_WARD_PPN = RESIDUALS / "P8_Y5_PARENT_QLOC_1561_WARD_PPN_GATE.csv"
SRC_HILBERT_DIV = RESIDUALS / "P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv"
SRC_HILBERT_EXCHANGE = RESIDUALS / "P8_Y5_HILBERT_CURRENT_2467_EXCHANGE_CURRENT_IDENTITY.csv"
SRC_HILBERT_PROMOTION = RESIDUALS / "P8_Y5_HILBERT_CURRENT_2467_PROMOTION_VERDICT.csv"
SRC_HILBERT_WORLDTUBE = RESIDUALS / "P8_Y5_HILBERT_CURRENT_2467_WORLDTUBE_SURFACE_GATE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2943_SOURCE_REGISTER.csv",
    "rescue": RESIDUALS / "P8_Y5_R2FR_2943_WARD_STUECKELBERG_RESCUE_ATTEMPT.csv",
    "obstruction": RESIDUALS / "P8_Y5_R2FR_2943_WARD_OBSTRUCTION_DECOMPOSITION.csv",
    "current": RESIDUALS / "P8_Y5_R2FR_2943_CURRENT_SOURCE_EVIDENCE_AUDIT.csv",
    "bound_start": RESIDUALS / "P8_Y5_R2FR_2943_QLOC_FINITE_BOUND_RUNNER_START.csv",
    "requirements": RESIDUALS / "P8_Y5_R2FR_2943_BOUND_INPUT_REQUIREMENTS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2943_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2943_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2943_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2943_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2943_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "rescue_copy": PARENT_ACTION / "A_mu_Ward_Stueckelberg_rescue_attempt_2943_NONCLAIM.csv",
    "obstruction_copy": PARENT_ACTION / "A_mu_Ward_obstruction_decomposition_2943_NONCLAIM.csv",
    "bound_start_copy": LOCAL_BOUNDS / "Qloc_finite_bound_runner_start_2943_NONCLAIM.csv",
    "requirements_copy": LOCAL_BOUNDS / "Qloc_bound_input_requirements_2943_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2943_QLOC_BOUND_RUNNER_NEXT_NONCLAIM.csv",
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
        ("SRC2943_00_2942_doc", SRC_2942_DOC, "delta_epsilon S_GK;A_mu origin not derived;Validation overall: `True`", "2942 exact Ward obstruction and handoff"),
        ("SRC2943_01_2942_next", SRC_2942_NEXT, "NEXT2942_0_2943", "selected 2943 objective"),
        ("SRC2943_02_2942_gauge", SRC_2942_GAUGE, "WARD2942_0_pure_gauge_requirement;WARD2942_4_verdict", "pure gauge obstruction"),
        ("SRC2943_03_2942_bounds", SRC_2942_BOUNDS, "QB2942_0_bulk_source;QB2942_5_denominator", "finite q_loc bound handoff"),
        ("SRC2943_04_2942_demotion", SRC_2942_DEMOTION, "DEM2942_0_SGK_status;DEM2942_1_q_loc_status", "closure demotion policy"),
        ("SRC2943_05_2942_contract", SRC_2942_CONTRACT, "CON2942_0_parent_chart;CON2942_6_projector_boundary", "A_mu adoption contract"),
        ("SRC2943_06_2465_variation", SRC_2465_VARIATION, "VAR2465_5_integrability;VAR2465_6_not_theorem", "A-equation integrability warning"),
        ("SRC2943_07_2465_source", SRC_2465_SOURCE, "SRC2465_1_vertical_generator;SRC2465_6_candidate_route", "source-current descent blockers"),
        ("SRC2943_08_2465_boundary", SRC_2465_BOUNDARY, "BND2465_0_A_boundary;BND2465_4_distributional_source", "boundary and jump-condition blockers"),
        ("SRC2943_09_ward_owner", SRC_WARD_OWNER, "C0_on_shell_total_Ward;C4_constant_universal_coupling", "source owner Ward contract"),
        ("SRC2943_10_ward_universality", SRC_WARD_UNIVERSALITY, "SC2_Ward_conservation_on_matter_shell;SC7_no_time_range_radial_species_drift", "Hilbert current universality contract"),
        ("SRC2943_11_euler_chain", SRC_EULER_CHAIN, "EW538_1_Noether_current;EW538_4_PiM_Hilbert_identification", "Euler-Ward route status"),
        ("SRC2943_12_euler_decision", SRC_EULER_DECISION, "D538_1_PiM_identification_fails_current_claim;D538_3_no_PPN_readout_yet", "Euler-Ward decision"),
        ("SRC2943_13_gauge_noether", SRC_GAUGE_NOETHER, "GAUGE1555_3_noether_identity;GAUGE1555_5_current_verdict", "gauge/Noether no-origin audit"),
        ("SRC2943_14_ward_ppn", SRC_WARD_PPN, "WPPN1561_3_Bianchi;WPPN1561_5_local_claim", "local PPN Ward gate"),
        ("SRC2943_15_hilbert_div", SRC_HILBERT_DIV, "DIV2467_4_Killing_clock;DIV2467_5_generic_clock", "Hilbert current divergence identity"),
        ("SRC2943_16_hilbert_exchange", SRC_HILBERT_EXCHANGE, "EXC2467_0_required_identity;EXC2467_3_local_stationary_escape", "exchange-current identity"),
        ("SRC2943_17_hilbert_promotion", SRC_HILBERT_PROMOTION, "PV2467_0_conservation;PV2467_4_overall", "Hilbert current promotion verdict"),
        ("SRC2943_18_hilbert_worldtube", SRC_HILBERT_WORLDTUBE, "WTG2467_1_stationary_surface;WTG2467_4_external_vacuum", "worldtube surface gate"),
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


def rescue_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "attempt_id": "WS2943_0_pure_gauge_A",
            "route": "A_mu -> A_mu + nabla_mu epsilon",
            "required_identity": "nabla_mu(nabla^mu Gamma_eff - J_M^mu)=0 plus boundary silence",
            "evidence": "2942 derives the variation obstruction; no current corpus row supplies this off-shell identity.",
            "status": "FAIL_CURRENT_CORPUS",
            "adopt_A_mu": False,
        },
        {
            "attempt_id": "WS2943_1_Gamma_Stueckelberg",
            "route": "assign Gamma_eff a compensating Stueckelberg transformation",
            "required_identity": "delta Gamma_eff and L_Gamma must cancel delta_epsilon S_GK without imposing the field equation by hand",
            "evidence": "2942 and 2465 have no parent-signed Gamma_eff transformation or L_Gamma cancellation law.",
            "status": "MISSING_PARENT_TRANSFORMATION",
            "adopt_A_mu": False,
        },
        {
            "attempt_id": "WS2943_2_source_exchange",
            "route": "derive an exchange law for J_M",
            "required_identity": "nabla_mu J_M^mu = Box Gamma_eff plus owned exchange/boundary terms",
            "evidence": "2467 derives a Hilbert-current divergence identity, but generic clocks need an exchange current that is not parent-owned.",
            "status": "FORM_IDENTIFIED_NOT_OWNED",
            "adopt_A_mu": False,
        },
        {
            "attempt_id": "WS2943_3_local_stationary_escape",
            "route": "restrict to stationary compact-support collars",
            "required_identity": "tau Killing, side flux zero, compact support, and no A/Gamma boundary leakage",
            "evidence": "2467 supports conditional stationary source independence; 2465 still leaves A/Gamma boundary and jump conditions unsigned.",
            "status": "CONDITIONAL_SUPPORT_NOT_GENERAL_THEOREM",
            "adopt_A_mu": False,
        },
        {
            "attempt_id": "WS2943_4_verdict",
            "route": "current 2943 rescue",
            "required_identity": "one signed Ward/Stueckelberg/source theorem that makes A_mu a legitimate parent vertical connection",
            "evidence": "all available rows are conditional, missing, or closure-only.",
            "status": "WARD_STUECKELBERG_RESCUE_NOT_DERIVED",
            "adopt_A_mu": False,
        },
    ]
    return [add_common(row) for row in rows]


def obstruction_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "obstruction_id": "OBS2943_0_variation",
            "term": "delta_epsilon S_GK",
            "mathematical_form": "-int sqrt(-g) epsilon nabla_mu(nabla^mu Gamma_eff - J_M^mu) + boundary",
            "must_vanish_by": "off-shell Ward identity or Stueckelberg cancellation",
            "current_status": "NOT_SIGNED",
            "finite_bound_component": "C_bulk_source plus C_boundary",
        },
        {
            "obstruction_id": "OBS2943_1_Box_Gamma",
            "term": "nabla_mu nabla^mu Gamma_eff",
            "mathematical_form": "Box Gamma_eff",
            "must_vanish_by": "Gamma equation, Stueckelberg law, or local extremum theorem",
            "current_status": "NO_PARENT_GAMMA_LAW",
            "finite_bound_component": "C_Gamma_curvature",
        },
        {
            "obstruction_id": "OBS2943_2_source_current",
            "term": "nabla_mu J_M^mu",
            "mathematical_form": "(nabla ell_J)T tau + ell_J T nabla tau after matter shell",
            "must_vanish_by": "constant ell_J plus Killing clock, or parent exchange current",
            "current_status": "CONDITIONAL_ONLY",
            "finite_bound_component": "C_source_divergence",
        },
        {
            "obstruction_id": "OBS2943_3_boundary",
            "term": "boundary flux",
            "mathematical_form": "n_mu K_hat^{mu nu}, n.A, worldtube jump terms",
            "must_vanish_by": "Dirichlet/Neumann/counterterm or compact collar theorem",
            "current_status": "MISSING_BOUNDARY_CONDITION",
            "finite_bound_component": "C_boundary_flux",
        },
        {
            "obstruction_id": "OBS2943_4_projection",
            "term": "P_loc projection",
            "mathematical_form": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "must_vanish_by": "parent local projection theorem and symbol match",
            "current_status": "HANDOFF_TO_FINITE_BOUND_RUNNER",
            "finite_bound_component": "C_projector_leak plus C_symbol_mismatch",
        },
    ]
    return [add_common(row) for row in rows]


def current_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "evidence_id": "CUR2943_0_Hilbert_definition",
            "candidate": "J_M^nu = ell_J T_matter^{nu rho} tau_rho",
            "support": "2467 defines this candidate and derives its product-rule divergence.",
            "limitation": "ell_J is not parent-derived and generic tau is not Killing.",
            "effect": "good stationary/local source candidate, not full dynamic theorem",
        },
        {
            "evidence_id": "CUR2943_1_divergence",
            "candidate": "nabla_nu J_M^nu",
            "support": "exact product-rule identity is derived.",
            "limitation": "generic clock strain gives nonzero leakage unless exchange is derived.",
            "effect": "forces either exchange-current proof or finite residual bound",
        },
        {
            "evidence_id": "CUR2943_2_exchange",
            "candidate": "I_tau + I_A cancels source-current divergence",
            "support": "required exchange form is identified.",
            "limitation": "source action for exchange and total stress route remain missing.",
            "effect": "cannot close Ward identity from existing corpus",
        },
        {
            "evidence_id": "CUR2943_3_worldtube",
            "candidate": "stationary compact-support collar",
            "support": "surface independence closes conditionally when tau is Killing and side flux vanishes.",
            "limitation": "dynamic surface drift and boundary layers remain unsigned.",
            "effect": "useful local theorem candidate but not enough for local-GR claim",
        },
        {
            "evidence_id": "CUR2943_4_universality",
            "candidate": "universal source coupling",
            "support": "standard Hilbert-current route is available as a conditional template.",
            "limitation": "universal kappa, no species drift, no range/radial hair are not parent-derived.",
            "effect": "R10/WEP/PPN remains nonclaim until real inputs are supplied",
        },
    ]
    return [add_common(row) for row in rows]


def bound_start_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "runner_id": "QBR2943_0_total_envelope",
            "bound_statement": "||q_loc||_collar <= C_bulk_source + C_Gamma_curvature + C_source_divergence + C_boundary_flux + C_projector_leak + C_symbol_mismatch",
            "input_status": "RUNNER_STARTED_SYMBOLIC_ONLY",
            "claim_policy": "not evidence until every C_i has numeric source-backed input and arena projection",
        },
        {
            "runner_id": "QBR2943_1_R10_interface",
            "bound_statement": "alpha_predicted(lambda) requires finite q_loc amplitude, source normalization and lambda_X mapping",
            "input_status": "MISSING_PARENT_INPUTS",
            "claim_policy": "valid_for_claim=false",
        },
        {
            "runner_id": "QBR2943_2_PPN_interface",
            "bound_statement": "PPN residual vector requires gamma-1, beta-1, alpha_i and source/current tails from the same q_loc envelope",
            "input_status": "MISSING_ARENA_PROJECTION",
            "claim_policy": "local-GR claim blocked",
        },
        {
            "runner_id": "QBR2943_3_clock_orbital_interface",
            "bound_statement": "clock/orbital residuals require tau-strain and worldtube side-flux bounds",
            "input_status": "MISSING_DYNAMIC_EXCHANGE",
            "claim_policy": "clock/orbital claim blocked",
        },
        {
            "runner_id": "QBR2943_4_verdict",
            "bound_statement": "finite q_loc residual path replaces zero-plateau assumption",
            "input_status": "BOUND_RUNNER_OPENED_NONCLAIM",
            "claim_policy": "continue to 2944 source-input fill",
        },
    ]
    return [add_common(row) for row in rows]


def requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("REQ2943_0_C_bulk_source", "C_bulk_source", "||P_loc J_M||_collar", "source current support, ell_J scale, matter shell, collar geometry", "MISSING_PARENT_INPUT", "False"),
        ("REQ2943_1_C_Gamma_curvature", "C_Gamma_curvature", "||P_loc grad Gamma_eff|| or ||Box Gamma_eff||", "Gamma_eff equation, local extremum law, curvature/memory projection", "MISSING_GAMMA_PARENT_LAW", "False"),
        ("REQ2943_2_C_source_divergence", "C_source_divergence", "||nabla_mu J_M^mu||", "tau strain, ell_J derivative, exchange current I_tau/I_A", "MISSING_DYNAMIC_EXCHANGE", "False"),
        ("REQ2943_3_C_boundary_flux", "C_boundary_flux", "||n_mu K_hat^{mu nu}|| + ||n.A|| + jump terms", "A/Gamma boundary condition or counterterm and worldtube jump law", "MISSING_BOUNDARY_CONDITION", "False"),
        ("REQ2943_4_C_projector_leak", "C_projector_leak", "||delta P_loc||", "local projection definition and gauge-invariant collar norm", "MISSING_ARENA_PROJECTION", "False"),
        ("REQ2943_5_C_symbol_mismatch", "C_symbol_mismatch", "||Khat_old - partial L_K/partial(nabla A)||", "single K_hat symbol map across old/new conventions", "MISSING_SYMBOL_LOCK", "False"),
        ("REQ2943_6_C_denominator", "C_denominator", "M_H_ref or parent source charge", "non-circular mass/source normalization", "MISSING_SOURCE_NORMALIZATION", "False"),
    ]
    return [
        add_common(
            {
                "requirement_id": requirement_id,
                "input_name": input_name,
                "mathematical_object": mathematical_object,
                "required_data": required_data,
                "status": status,
                "valid_for_claim": valid_for_claim,
            }
        )
        for requirement_id, input_name, mathematical_object, required_data, status, valid_for_claim in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2943_0_A_mu_origin", "A_mu is derived as parent vertical/gauge connection", False, "BLOCKED_NO_WARD_STUECKELBERG_SOURCE_THEOREM", False),
        ("CG2943_1_SGK_adoption", "S_GK/ACT2464_A promoted as parent action sector", False, "CLOSURE_ONLY", False),
        ("CG2943_2_q_loc_zero", "q_loc=0 local-vacuum plateau", False, "ZERO_ROUTE_FAILED_USE_FINITE_BOUND", False),
        ("CG2943_3_finite_q_loc_bound", "finite q_loc residual bound is source-ready", False, "RUNNER_STARTED_INPUTS_MISSING", False),
        ("CG2943_4_Newton_GR", "Newton/local-GR branch derived", False, "SOURCE_CURRENT_AND_BOUNDARY_STILL_OPEN", False),
        ("CG2943_5_R10_PPN_clock_orbital", "local arenas pass", False, "NO_NUMERIC_SOURCE_BACKED_INPUTS", False),
        ("CG2943_6_public_claim", "public claim allowed from 2943", False, "PRIVATE_NONCLAIM_CHECKPOINT", False),
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
        ("DEC2943_0_rescue_failed", "Ward/Stueckelberg rescue not proved", "no off-shell Ward identity, no Gamma transformation, no parent-owned exchange current", "do not adopt A_mu as parent generator"),
        ("DEC2943_1_not_dead", "failure is useful not fatal", "the obstruction has become a finite residual-vector problem", "start q_loc finite bound runner"),
        ("DEC2943_2_stationary_branch", "stationary collar remains a possible local theorem", "Hilbert current closes conditionally under Killing clock and no side flux", "treat as support, not a full dynamic/local-GR proof"),
        ("DEC2943_3_bound_inputs", "bound route needs actual sourced inputs", "bulk/source, Gamma, boundary, projector, symbol, denominator rows are all unsigned", "2944 must fill/source or explicitly block each C_i"),
        ("DEC2943_4_claim_discipline", "no R10/PPN/Newton/local-GR claim from 2943", "all new rows remain valid_for_claim=false", "private checkpoint only"),
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
                "next_id": "NEXT2943_0_2944",
                "priority": "selected_primary",
                "next_doc": "2944-Y5-R2FR-q_loc-finite-residual-bound-runner-source-inputs-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_q_loc_finite_residual_bound_runner_source_inputs_under_AX1090_2944.py",
                "objective": "Convert the symbolic q_loc finite envelope into a source-input ledger: either fill/bound C_bulk_source, C_Gamma_curvature, C_source_divergence, C_boundary_flux, C_projector_leak, C_symbol_mismatch and C_denominator, or prove exactly which row blocks local tests.",
                "include": "2943 bound-input requirements; Hilbert stationary support; 2465 boundary audit; 2942 q_loc handoff; R10/PPN/clock/orbital arena projections",
                "exclude": "zero plateau axiom; direct A_mu multiplier adoption; local-GR/Newton/R10 claim; GitHub action; formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("rescue_copy", OUTPUTS["rescue"], BRANCH_OUTPUTS["rescue_copy"]),
        ("obstruction_copy", OUTPUTS["obstruction"], BRANCH_OUTPUTS["obstruction_copy"]),
        ("bound_start_copy", OUTPUTS["bound_start"], BRANCH_OUTPUTS["bound_start_copy"]),
        ("requirements_copy", OUTPUTS["requirements"], BRANCH_OUTPUTS["requirements_copy"]),
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
    formalization_has_2943 = False
    if FORMALIZATION.exists():
        formalization_has_2943 = any(FORMALIZATION.rglob("*2943*"))
    rescue = read_csv_rows(OUTPUTS["rescue"])
    bound_start = read_csv_rows(OUTPUTS["bound_start"])
    requirements = read_csv_rows(OUTPUTS["requirements"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_target = read_csv_rows(OUTPUTS["next"])
    checks = [
        ("VAL2943_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2943_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2943_2_rescue_attempted", any(row.get("attempt_id") == "WS2943_4_verdict" for row in rescue), "Ward/Stueckelberg rescue verdict row exists", True),
        ("VAL2943_3_rescue_refused", any(row.get("attempt_id") == "WS2943_4_verdict" and row.get("adopt_A_mu") == "False" for row in rescue), "A_mu rescue refused in current corpus", True),
        ("VAL2943_4_bound_runner_started", any(row.get("runner_id") == "QBR2943_4_verdict" for row in bound_start), "q_loc finite residual bound runner started", True),
        ("VAL2943_5_requirements_nonclaim", all(row.get("valid_for_claim") == "False" for row in requirements), "all bound requirements remain nonclaim", True),
        ("VAL2943_6_claims_blocked", all(row.get("claim_allowed") == "False" for row in claims), "all claims blocked", True),
        ("VAL2943_7_next_target_selected", any(row.get("next_id") == "NEXT2943_0_2944" for row in next_target), "2944 q_loc finite-bound input target selected", True),
        ("VAL2943_8_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        ("VAL2943_9_csvs_parse", all(csv_parses(path) for path in generated_csvs), "all generated CSV files parse", True),
        ("VAL2943_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2943_11_formalization_clean", not formalization_has_2943, "no 2943 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "check": check, "required": required} for validation_id, passed, check, required in checks]
    rows.append({"validation_id": "VAL2943_OVERALL", "passed": overall, "check": "2943 validation overall", "required": True})
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    rescue: list[dict[str, Any]],
    obstruction: list[dict[str, Any]],
    current: list[dict[str, Any]],
    bound_start: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation if row["validation_id"] == "VAL2943_OVERALL")["passed"]
    text = f"""# 2943 - Y5 R2FR: A_mu Ward/Stueckelberg identity or q_loc finite-bound runner under AX1090

Status: `Y5_R2FR_2943_Ward_Stueckelberg_rescue_not_derived_q_loc_finite_bound_runner_started`

Claim ceiling: `A_mu_origin_no_SGK_adoption_no_q_loc_zero_no_F1_zero_no_Newton_no_local_GR_no_R10_no_public_claim`

2943 takes the promised honest route: try the rescue derivation once, then do not pretend it closed. The pure-gauge route requires

`nabla_mu(nabla^mu Gamma_eff - J_M^mu)=0`

plus boundary silence, or else a parent-signed Stueckelberg cancellation for `Gamma_eff`. The current corpus supports pieces of this shape, especially a conditional Hilbert-current/stationary-collar route, but it does not supply the off-shell Ward identity, the `Gamma_eff` transformation, or the parent-owned exchange current needed to promote `A_mu` as a genuine vertical/gauge connection.

The useful gain is that the local branch is no longer allowed to hide behind a plateau axiom. The next path is a finite residual envelope for physical `q_loc`, with each term either sourced, bounded, or explicitly blocking local tests.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Ward/Stueckelberg Rescue Attempt

{md_table(rescue, ["attempt_id", "route", "required_identity", "status", "adopt_A_mu"])}

## Ward Obstruction Decomposition

{md_table(obstruction, ["obstruction_id", "term", "mathematical_form", "must_vanish_by", "current_status", "finite_bound_component"])}

## Current/Source Evidence Audit

{md_table(current, ["evidence_id", "candidate", "support", "limitation", "effect"])}

## q_loc Finite Bound Runner Start

{md_table(bound_start, ["runner_id", "bound_statement", "input_status", "claim_policy"])}

## Bound Input Requirements

{md_table(requirements, ["requirement_id", "input_name", "mathematical_object", "required_data", "status", "valid_for_claim"])}

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

    rescue = rescue_rows()
    obstruction = obstruction_rows()
    current = current_rows()
    bound_start = bound_start_rows()
    requirements = requirement_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["rescue"], rescue)
    write_csv(OUTPUTS["obstruction"], obstruction)
    write_csv(OUTPUTS["current"], current)
    write_csv(OUTPUTS["bound_start"], bound_start)
    write_csv(OUTPUTS["requirements"], requirements)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(source_rows)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(source_rows, rescue, obstruction, current, bound_start, requirements, claims, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL2943_OVERALL")["passed"]
    print(f"2943 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
