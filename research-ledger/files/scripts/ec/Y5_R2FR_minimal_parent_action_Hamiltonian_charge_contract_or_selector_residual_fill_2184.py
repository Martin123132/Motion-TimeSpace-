from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2184"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2184-Y5-R2FR-minimal-parent-action-Hamiltonian-charge-contract-or-selector-residual-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2184_SOURCE_REGISTER.csv",
    "action_skeleton": OUT / "P8_Y5_PARENT_QLOC_2184_MINIMAL_PARENT_ACTION_SKELETON.csv",
    "noether_chain": OUT / "P8_Y5_PARENT_QLOC_2184_NOETHER_HAMILTONIAN_CHARGE_CHAIN.csv",
    "v_bridge": OUT / "P8_Y5_PARENT_QLOC_2184_V_AS_LOCAL_LAPSE_READOUT_BRIDGE.csv",
    "residual_rows": OUT / "P8_Y5_PARENT_QLOC_2184_PARENT_ACTION_RESIDUAL_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2184_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2184_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2184_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2184_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2184_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2184_PARENT_ACTION_RESIDUAL_ROWS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2184_ACTION_SKELETON_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MINIMAL_PARENT_ACTION_HAMILTONIAN_CHARGE_2184_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2184_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2184-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2184*",
        "*P8_Y5_BRR545_2184*",
        "*Y5_R2FR_minimal_parent_action_Hamiltonian_charge_contract_or_selector_residual_fill_2184*",
        "*JR2184*",
        "*MINIMAL_PARENT_ACTION_HAMILTONIAN_CHARGE_2184*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2183_handoff",
            ROOT / "2183-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R_eq-fill.md",
            ["NEXT2183_0_2184", "BUILD_MINIMAL_PARENT_ACTION_CHARGE_CONTRACT_NEXT", "VAL2183_OVERALL"],
            "2183 selects minimal parent-action/Hamiltonian charge construction as the next route.",
        ),
        (
            "2183_validation",
            OUT / "P8_Y5_BRR545_2183_VALIDATION.csv",
            ["VAL2183_OVERALL", "PASS"],
            "2183 validation passed before 2184 continues the chain.",
        ),
        (
            "parent_action_derivation_attempt",
            OUT / "P8_Y5_PARENT_ACTION_DERIVATION_ATTEMPT.csv",
            ["DAT537_0_variation", "DAT537_4_PiM_Hilbert_identification", "DAT537_5_local_readout"],
            "prior parent-action derivation attempt gives the formal Noether chain and names the missing PiM/Hilbert identity.",
        ),
        (
            "parent_action_clause_map",
            OUT / "P8_Y5_PARENT_ACTION_TO_HWT536_CLAUSE_MAP.csv",
            ["HWT536_0_parent_worldtube_fixed", "HWT536_3_Hilbert_to_PiM_charge_map", "HWT536_8_weak_field_readout_after_charge_glue"],
            "maps parent-action outputs to the Hilbert-worldtube clauses.",
        ),
        (
            "noether_closure",
            OUT / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
            ["T505_conditional_Noether_mass_charge_closure", "T505_source_measure_matching", "T505_Newton_limit_corollary"],
            "Noether theorem gives the conditional radial mass-charge closure and Newton/Gauss corollary.",
        ),
        (
            "minimal_local_gr_blocks",
            OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            ["A511_0_EH_core", "A511_2_universal_matter", "A511_6_metric_readout"],
            "minimal local-GR action blocks list EH core, universal matter, and readout/PiM double-zero structure.",
        ),
        (
            "fixed_point_conditions",
            OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            ["FP511_1_double_zero_nonEH_coupling", "FP511_5_parent_PiM_lock", "FP511_7_metric_PPN_readout"],
            "fixed-point conditions define the double-zero, PiM lock, and PPN readout requirements.",
        ),
        (
            "v_action_coefficients",
            OUT / "P8_Y5_PARENT_QLOC_2179_V_ACTION_COEFFICIENT_AUDIT.csv",
            ["VAC2179_1_target_coefficients", "VAC2179_2_parent_origin_test", "VAC2179_5_current_verdict"],
            "2179 records the target K_v/C_v normalization and the fact that current MTS has not parent-derived it.",
        ),
    ]
    rows = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def action_skeleton_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "MAS2184_0_field_content",
            "minimal local fields",
            "Phi=(e_obs, omega or Gamma, psi_m, X^A, kappa_eff, A_3, B_ref/top).",
            "MINIMAL_FIELD_LIST_CANDIDATE",
            "e_obs owns clocks/orbits/sources; X^A are MTS motion/time/domain/memory/range sectors; A_3 can freeze kappa_eff locally.",
        ),
        (
            "MAS2184_1_action_skeleton",
            "parent action skeleton",
            "S_min = S_EH[e_obs,kappa_eff] + S_matter[psi_m,e_obs] + S_X[X,e_obs] + S_kappa_top[kappa_eff,A_3] + S_boundary[e_obs,B_ref] + S_readout_constraint.",
            "MINIMAL_PARENT_ACTION_SKELETON_WRITTEN",
            "this is a construction contract, not a claim that the corpus already supplies all terms.",
        ),
        (
            "MAS2184_2_EH_fixed_point",
            "local EH fixed point",
            "At X=X0, C_i(X0)=partial_A C_i(X0)=0, positive non-gauge Hessian, and d kappa_eff=0, the local exterior equations and symplectic charge reduce to EH plus residuals.",
            "CONDITIONAL_EH_FIXED_POINT_ROUTE",
            "this is how MTS can reduce to GR locally without being only GR globally.",
        ),
        (
            "MAS2184_3_universal_matter",
            "single observed source frame",
            "S_matter depends on e_obs and psi_m only at leading local order; J_H[tau] := delta S_matter/delta e_obs contracted with tau.",
            "CONDITIONAL_HILBERT_SOURCE_OWNER",
            "source universality and WEP are owned by the action if no X^A species/source slot survives.",
        ),
        (
            "MAS2184_4_Hamiltonian_PiM",
            "Hamiltonian mass map",
            "Pi_M J_H is identified with the covariant phase-space Hamiltonian mass-charge map ell_H[J_H;tau,S] omega_M^H.",
            "CORE_ADOPTION_NEEDED_NOT_PROVED",
            "this is the live identity; without it, Pi_M may be a conserved wrong object.",
        ),
        (
            "MAS2184_5_worldtube_selector",
            "source support selector",
            "W_source := supp(J_H[e_obs,tau]) and S1,S2 must link the same W_source before fitting any exterior readout.",
            "CONDITIONAL_SELECTOR_DERIVED_IF_JH_OWNED",
            "this turns worldtube selection into source support, not a post-readout domain choice.",
        ),
        (
            "MAS2184_6_boundary_reference",
            "fixed reference and zero-flux boundary",
            "S_boundary must make H_tau integrable with one reference and zero compact exterior flux from B_ref/top, symplectic improvements, and inner/outer boundaries.",
            "BOUNDARY_CONTRACT_WRITTEN_NOT_CERTIFIED",
            "B_zero_flux remains open until the boundary variation is actually computed.",
        ),
        (
            "MAS2184_7_current_verdict",
            "current corpus status",
            "The minimal action/charge contract is coherent, but it is not yet a derived MTS parent action because PiM adoption, X-sector double zeros, and boundary zero are unsigned.",
            "COHERENT_CONTRACT_CURRENT_CLAIM_FAILS",
            "do not claim Newton/local-GR; use this to drive the next coefficient extraction.",
        ),
    ]
    return [
        base_row(
            skeleton_id=skeleton_id,
            component=component,
            statement=statement,
            status=status,
            implication=implication,
        )
        for skeleton_id, component, statement, status, implication in specs
    ]


def noether_chain_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NHC2184_0_variation",
            "covariant variation",
            "delta L = E_A delta Phi^A + dTheta(Phi,delta Phi).",
            "FORMAL_EXACT_IF_ACTION_SUPPLIED",
            "the symplectic potential exists once S_min is explicit.",
        ),
        (
            "NHC2184_1_Noether_current",
            "diffeomorphism Noether current",
            "J_tau = Theta(Phi,L_tau Phi) - i_tau L.",
            "FORMAL_EXACT_IF_TAU_FIXED",
            "tau must be selected before source scoring.",
        ),
        (
            "NHC2184_2_charge_decomposition",
            "surface charge plus constraints",
            "On shell in a source-free annulus, J_tau = dQ_tau + C_tau and Delta H_tau[S2,S1] = integral_A C_tau + boundary_flux.",
            "EXACT_CONDITIONAL_HAMILTONIAN_CHAIN",
            "radial closure follows from vanishing constraints and zero boundary flux.",
        ),
        (
            "NHC2184_3_source_measure",
            "dressed source mass",
            "M_source[W] := H_tau[S] - H_tau[reference], with W_source=supp(J_H[e_obs,tau]).",
            "CONDITIONAL_SOURCE_MEASURE_DEFINITION",
            "bare rest mass is not enough; the dressed Hamiltonian charge is the measured source object.",
        ),
        (
            "NHC2184_4_PiM_identification",
            "PiM/Hilbert identity",
            "(4*pi*G_ref)^-1 integral_S Pi_M J_H = H_tau[S] - H_tau[reference].",
            "CORE_MISSING_IDENTITY_NOT_DERIVED",
            "this remains the main equality that must be adopted or derived.",
        ),
        (
            "NHC2184_5_topological_PD",
            "topological representative",
            "J_M_top := M_source[W] omega_W, d omega_W=0, integral_link omega_W=1 for the same W_source.",
            "EXACT_CONDITIONAL_PD_MAP",
            "if NHC2184_4 holds, J_M_top is the same measured source object.",
        ),
        (
            "NHC2184_6_R_eq_zero",
            "R_eq zero theorem",
            "If Pi_M J_H and J_M_top represent the same compact Hilbert source class, then Pi_M J_H-J_M_top=dB_zero and R_eq=0.",
            "EXACT_CONDITIONAL_R_EQ_ZERO",
            "R_eq zero is downstream of the PiM/Hamiltonian identity, not an independent axiom.",
        ),
        (
            "NHC2184_7_Newton_corollary",
            "Newton/Gauss corollary",
            "If the same charge controls the weak-field metric, exterior grad Phi flux equals 4*pi*G_ref M_source and is radius-independent.",
            "CONDITIONAL_NEWTON_COROLLARY",
            "the remaining work is coefficient/readout extraction, not source-label philosophy.",
        ),
    ]
    return [
        base_row(
            chain_id=chain_id,
            step=step,
            equation=equation,
            status=status,
            implication=implication,
        )
        for chain_id, step, equation, status, implication in specs
    ]


def v_bridge_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "VBR2184_0_local_readout_choice",
            "v as local lapse/coframe readout",
            "On the compact local branch, define v := log(N_obs^2/c^2) with g_obs(tau,tau)=-N_obs^2, so g_tt=-e^v c^2 in the adapted static chart.",
            "LOCAL_READOUT_DEFINITION_CANDIDATE",
            "this avoids treating v as an independently fitted local force field unless the parent action proves one.",
        ),
        (
            "VBR2184_1_extra_field_descent",
            "independent MTS sectors freeze locally",
            "X^A=X0 with C_i(X0)=partial_A C_i(X0)=0 and positive non-gauge Hessian makes g_readout=g_obs+O((X-X0)^2).",
            "CONDITIONAL_DOUBLE_ZERO_DESCENT",
            "motion/time/domain fields can still exist globally while being locally silent.",
        ),
        (
            "VBR2184_2_EH_to_v_coefficients",
            "EH fixed point should determine K_v and C_v",
            "Expand S_EH+S_GHY+S_matter on the constrained static weak-field branch g_tt=-e^v c^2 and compare with L_v=-K_v(grad v)^2-C_v rho c^2 v.",
            "NEXT_COMPUTATION_NOT_DONE_IN_2184",
            "this is the first non-handwave route to K_v=c^4/(32piG_ref), C_v=1/2 without fitting.",
        ),
        (
            "VBR2184_3_beta_readout",
            "beta from lapse logarithm",
            "If the EH fixed-point solution gives v=-2U/c^2+O(U^3/c^6), then exp(v)=1-2U/c^2+2U^2/c^4+... and beta=1.",
            "CONDITIONAL_BETA_ZERO_ROUTE",
            "kappa_v=0 becomes an EH fixed-point/readout extraction target.",
        ),
        (
            "VBR2184_4_gamma_readout",
            "gamma from reciprocal coframe branch",
            "With the constrained local reciprocal branch sqrt(S)=exp(-v/2), first-order spatial curvature gives gamma=1 once v source normalization is fixed.",
            "CONDITIONAL_GAMMA_ROUTE",
            "gamma is downstream of the same v amplitude/source theorem.",
        ),
        (
            "VBR2184_5_no_GR_import_guard",
            "GR import guard",
            "Using EH is allowed only as a parent-derived local fixed point of MTS, not as a late replacement of MTS by GR.",
            "GUARDRAIL_ACTIVE",
            "2185 must compute the coefficient extraction and record whether it is inherited, derived, or merely imported.",
        ),
        (
            "VBR2184_6_current_status",
            "v bridge status",
            "The lapse-readout route is coherent but the EH expansion to K_v/C_v and kappa_v=0 has not been performed here.",
            "BRIDGE_OPEN_NOT_CLAIMED",
            "next target should do the actual expansion or demote K_v/C_v to finite rows.",
        ),
    ]
    return [
        base_row(
            bridge_id=bridge_id,
            bridge=bridge,
            statement=statement,
            status=status,
            implication=implication,
        )
        for bridge_id, bridge, statement, status, implication in specs
    ]


def residual_row_rows() -> list[dict[str, Any]]:
    specs = [
        ("PAR2184_0_action", "epsilon_parent_action", "gap between written action skeleton and explicit MTS parent Lagrangian", "MISSING_EXPLICIT_PARENT_LAGRANGIAN", "declared_action_norm", "field-theory-spine;local-GR"),
        ("PAR2184_1_PiM", "epsilon_PiM_Hamiltonian", "failure of Pi_M J_H to equal the Hamiltonian mass-charge form", "MISSING_PIM_HAMILTONIAN_IDENTITY", "dimensionless_or_GM_flux", "Newton;PPN;R10;R11"),
        ("PAR2184_2_tau", "epsilon_tau_fixed", "unfixed observed time generator contribution to H_tau", "MISSING_TAU_SELECTOR", "dimensionless_or_charge_fraction", "clocks;Newton;orbital"),
        ("PAR2184_3_reference", "epsilon_reference_flux", "fixed-reference/integrability/boundary flux residual", "MISSING_FIXED_REFERENCE_ZERO_FLUX", "dimensionless_or_GM_flux", "Newton;PPN;R10;R11"),
        ("PAR2184_4_extra", "epsilon_X_charge", "non-EH MTS sector mass charge in compact local exterior", "MISSING_EXTRA_SECTOR_DOUBLE_ZERO_OR_BOUND", "dimensionless_or_GM_flux", "local-GR;WEP;PPN"),
        ("PAR2184_5_v_coeff", "delta_v_source_norm", "C_v c^4/(16piG_ref K_v)-1 from the local v/lapse action extraction", "MISSING_EH_TO_V_COEFFICIENT_EXTRACTION", "dimensionless", "Newton;PPN;orbital"),
        ("PAR2184_6_kappa", "kappa_v", "quadratic lapse/readout drift v=-2U/c^2+kappa_v U^2/c^4", "MISSING_KAPPA_V_ZERO_OR_VALUE", "dimensionless", "PPN_beta;local_GR"),
        ("PAR2184_7_R_eq", "R_eq_integral", "topological-Hilbert equality residual after Hamiltonian PiM adoption", "MISSING_R_EQ_ZERO_OR_VALUE", "dimensionless_after_M_H_ref", "Newton;R10;R11"),
        ("PAR2184_8_total", "Delta_Newton_local_abs", "absolute envelope combining delta_v_source_norm, epsilon_M, kappa_v and parent-action residuals", "MISSING_COMPONENT_INPUTS", "dimensionless", "Newton;local-GR;PPN"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            status=status,
            units=units,
            observable_link=observable_link,
            value="MISSING_NUMERIC_VALUE",
            source_path="MISSING_SOURCE_PATH",
            score_ready=False,
        )
        for row_id, symbol, definition, status, units, observable_link in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2184_0_skeleton", "minimal action/charge skeleton is written", "PASS_GUARDRAIL", "coherent construction target exists but remains nonclaim"),
        ("CG2184_1_parent_action", "explicit MTS parent action is supplied and varied", "BLOCKED_NONCLAIM", "2184 writes a skeleton/contract, not a completed Lagrangian derivation"),
        ("CG2184_2_PiM", "Pi_M is proved to be the Hamiltonian mass map", "BLOCKED_NONCLAIM", "core PiM/Hilbert identity remains unsigned"),
        ("CG2184_3_boundary", "B_zero/reference boundary flux is zero", "BLOCKED_NONCLAIM", "fixed reference and compact leak cancellation are not computed"),
        ("CG2184_4_v_coefficients", "K_v/C_v and kappa_v=0 are extracted from the parent action", "BLOCKED_NONCLAIM", "EH-to-v coefficient expansion is next, not done here"),
        ("CG2184_5_Newton_GR", "Newton/local-GR reduction can be claimed", "BLOCKED_NONCLAIM", "source, coefficient, PPN, and residual gates are still open"),
        ("CG2184_6_no_cheat", "no late multiplier, post-readout domain, fitted G, or GR-import shortcut", "PASS_GUARDRAIL", "2184 explicitly sends the coefficient extraction to a testable next gate"),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2184_0_gain",
            "MINIMAL_PARENT_ACTION_CHARGE_CONTRACT_WRITTEN",
            "The local branch now has a coherent action skeleton, Noether/Hamiltonian charge chain, source selector, and v-as-lapse bridge.",
            "selected",
        ),
        (
            "DEC2184_1_leap",
            "V_CAN_BE_LOCAL_READOUT_NOT_SEPARATE_FORCE_FIELD",
            "Treating v as log lapse on the compact local branch may let K_v/C_v and beta come from the EH fixed point rather than an inserted motion field.",
            "selected",
        ),
        (
            "DEC2184_2_limit",
            "NOT_A_CLAIM_UNTIL_EXPANSION",
            "The EH-to-v coefficient extraction and PiM/Hamiltonian identity are not yet computed/proved.",
            "selected",
        ),
        (
            "DEC2184_3_next",
            "EH_FIXED_POINT_TO_V_COEFFICIENT_EXTRACTION_NEXT",
            "The next best test is to expand the local EH fixed-point action/readout into the v coefficient law and beta drift, or mark it as GR import/finite residual.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2184_0_2185",
            selection_status="selected",
            target_file="2185-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md",
            target_script="scripts/Y5_R2FR_EH_fixed_point_to_v_action_coefficient_extraction_or_GR_import_demotion_2185.py",
            objective="compute the constrained local EH fixed-point expansion for v=log lapse, extract K_v/C_v and kappa_v, and decide whether the result is derived inheritance, GR import, or finite residual",
            success_condition="derives K_v=c^4/(32piG_ref), C_v=1/2, delta_v_source_norm=0 and kappa_v=0 from the parent fixed-point/readout chain without post-readout fitting; otherwise emits nonclaim finite rows",
            do_not_do="do not fit G, do not assume beta=1 from gamma, do not replace MTS by GR without a fixed-point descent clause, do not claim local-GR from a skeleton",
        ),
        base_row(
            route_id="NEXT2184_1_residual_parallel",
            selection_status="held_parallel",
            target_file="2185b-Y5-R2FR-parent-action-residual-source-backed-fill.md",
            target_script="scripts/Y5_R2FR_parent_action_residual_source_backed_fill_2185b.py",
            objective="if coefficient extraction fails, acquire source-backed residual rows for PiM/Hamiltonian identity, boundary flux, delta_v_source_norm, and kappa_v",
            success_condition="at least one residual row gains a real source path, units, normalization, arena projection, and valid_for_claim=false until the no-cancellation envelope closes",
            do_not_do="do not score placeholders, cancellation-only rows, or unsourced numeric guesses",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["residual_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["action_skeleton"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["v_bridge"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    source_rows = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2184_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2184_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    skeleton_statuses = {row["status"] for row in rows_by_name["action_skeleton"]}
    skeleton_pass = {"MINIMAL_PARENT_ACTION_SKELETON_WRITTEN", "CONDITIONAL_EH_FIXED_POINT_ROUTE", "COHERENT_CONTRACT_CURRENT_CLAIM_FAILS"}.issubset(skeleton_statuses)
    validations.append(base_row(validation_id="VAL2184_02_action_skeleton", status="PASS" if skeleton_pass else "FAIL", detail="minimal action skeleton written and kept nonclaim"))

    chain_statuses = {row["status"] for row in rows_by_name["noether_chain"]}
    chain_pass = {"EXACT_CONDITIONAL_HAMILTONIAN_CHAIN", "CORE_MISSING_IDENTITY_NOT_DERIVED", "EXACT_CONDITIONAL_R_EQ_ZERO"}.issubset(chain_statuses)
    validations.append(base_row(validation_id="VAL2184_03_noether_chain", status="PASS" if chain_pass else "FAIL", detail="Noether/Hamiltonian chain is exact conditional and PiM identity remains open"))

    bridge_statuses = {row["status"] for row in rows_by_name["v_bridge"]}
    bridge_pass = {"LOCAL_READOUT_DEFINITION_CANDIDATE", "NEXT_COMPUTATION_NOT_DONE_IN_2184", "GUARDRAIL_ACTIVE"}.issubset(bridge_statuses)
    validations.append(base_row(validation_id="VAL2184_04_v_bridge", status="PASS" if bridge_pass else "FAIL", detail="v-as-lapse bridge written; EH-to-v expansion deferred to 2185"))

    residual_rows = rows_by_name["residual_rows"]
    residual_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) and row.get("source_path") == "MISSING_SOURCE_PATH" for row in residual_rows)
    validations.append(base_row(validation_id="VAL2184_05_residual_rows_nonclaim", status="PASS" if residual_ok else "FAIL", detail=f"residual rows={len(residual_rows)} remain missing/source-free/nonclaim"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2184_06_claim_gate", status="PASS" if "BLOCKED_NONCLAIM" in claim_statuses and "PASS_GUARDRAIL" in claim_statuses else "FAIL", detail="claim gate blocks Newton/local-GR and keeps no-cheat guard"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2184_07_decision", status="PASS" if "EH_FIXED_POINT_TO_V_COEFFICIENT_EXTRACTION_NEXT" in decision_text else "FAIL", detail="decision selects EH fixed-point to v coefficient extraction next"))

    validations.append(base_row(validation_id="VAL2184_08_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2185" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2185 EH-to-v coefficient extraction target selected"))

    validations.append(base_row(validation_id="VAL2184_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2184_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2184_11_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2184_artifacts()
    validations.append(base_row(validation_id="VAL2184_12_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2184 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2184_13_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2184_OVERALL", status="PASS" if overall else "FAIL", detail="2184 writes minimal parent-action/Hamiltonian charge contract and selects EH-to-v coefficient extraction next"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2184 - Y5/R2FR Minimal Parent-Action Hamiltonian Charge Contract Or Selector Residual Fill

## Current Verdict

2184 makes a real leap instead of circling the same hole.

The compact local branch should not treat `v` as a free fitted force field unless a parent action proves it. The cleaner route is:

`v := log(N_obs^2/c^2)`, with `g_obs(tau,tau)=-N_obs^2`.

So locally `v` is a lapse/coframe readout of the same observed metric/coframe that owns matter, clocks, and orbits. The MTS extra sectors can still exist globally, but in compact local systems they must sit at a double-zero fixed point:

`X^A=X0`, `C_i(X0)=0`, `partial_A C_i(X0)=0`,

with positive non-gauge operator and no boundary/source flux.

The minimal parent-action charge contract is:

`S_min = S_EH[e_obs,kappa_eff] + S_matter[psi_m,e_obs] + S_X[X,e_obs] + S_kappa_top[kappa_eff,A_3] + S_boundary[e_obs,B_ref] + S_readout_constraint`.

From that, the Noether/Hamiltonian chain is formal and sharp:

`delta L = E_A delta Phi^A + dTheta`,

`J_tau = Theta(Phi,L_tau Phi) - i_tau L`,

`J_tau = dQ_tau + C_tau`,

`M_source[W] := H_tau[S] - H_tau[reference]`,

`W_source := supp(J_H[e_obs,tau])`.

If `Pi_M J_H` is the Hamiltonian mass-charge map and `J_M_top=PD(W_source)`, then `R_eq=0` is no longer an axiom; it follows from same compact source class. But that PiM/Hamiltonian identity is still not proved.

The new best attack is therefore concrete:

expand the local EH fixed-point action/readout for `v=log lapse` and see whether it actually gives

`K_v=c^4/(32piG_ref)`, `C_v=1/2`, `delta_v_source_norm=0`, and `kappa_v=0`.

If yes, we have a serious local GR/Newton descent route. If no, we demote the bridge to finite residuals. No pretending either way.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Minimal Parent Action Skeleton

{md_table(rows_by_name["action_skeleton"], ["skeleton_id", "component", "statement", "status", "implication", "valid_for_claim"])}

## Noether-Hamiltonian Charge Chain

{md_table(rows_by_name["noether_chain"], ["chain_id", "step", "equation", "status", "implication", "valid_for_claim"])}

## V As Local Lapse Readout Bridge

{md_table(rows_by_name["v_bridge"], ["bridge_id", "bridge", "statement", "status", "implication", "valid_for_claim"])}

## Parent Action Residual Rows

{md_table(rows_by_name["residual_rows"], ["row_id", "symbol", "definition", "status", "units", "observable_link", "value", "source_path", "score_ready", "valid_for_claim"])}

## Claim Gate

{md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is the strongest route now:

`MTS parent action -> local EH fixed point -> v as lapse readout -> EH/Hamiltonian charge -> K_v/C_v and beta extraction`.

It is not a surrender to GR. It is the exact Grossmann-style question: can MTS contain GR as its compact local fixed point in the same way GR contains Newton as its weak-field limit?

The project is getting more serious because the missing piece is no longer "make MTS look like GR". It is a calculable extraction:

`EH fixed point + constrained v readout -> {{K_v, C_v, kappa_v}}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "action_skeleton": action_skeleton_rows(),
        "noether_chain": noether_chain_rows(),
        "v_bridge": v_bridge_rows(),
        "residual_rows": residual_row_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in [
        "source_register",
        "action_skeleton",
        "noether_chain",
        "v_bridge",
        "residual_rows",
        "claim_gate",
        "decision",
        "next_target",
    ]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
