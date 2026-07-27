from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3367-Y5-R2FR-first-DeltaGM-mass-charge-component-row-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3367_SOURCE_REGISTER.csv",
    "selection": OUT / "P8_Y5_R2FR_3367_COMPONENT_SELECTION.csv",
    "decomposition": OUT / "P8_Y5_R2FR_3367_RNONEH_CHARGE_DECOMPOSITION.csv",
    "zero_theorem": OUT / "P8_Y5_R2FR_3367_RNONEH_ZERO_THEOREM_CONTRACT.csv",
    "coefficient_contract": OUT / "P8_Y5_R2FR_3367_RNONEH_COEFFICIENT_CONTRACT.csv",
    "runner": OUT / "P8_Y5_R2FR_3367_RNONEH_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3367_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3367_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3367_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3367_VALIDATION.csv",
}

LOCAL_SOURCES = [
    (
        "SRC3367_0_3366_doc",
        ROOT / "3366-Y5-R2FR-WEP-live-projection-file-acquisition-or-refusal-under-AX1090.md",
        "3366 WEP live projection audit; selects parent source coupling as next route",
    ),
    (
        "SRC3367_1_3366_next",
        OUT / "P8_Y5_R2FR_3366_NEXT_TARGET.csv",
        "3366 next target names 3367 first DeltaGM/source-mass component row",
    ),
    (
        "SRC3367_2_3365_component_matrix",
        OUT / "P8_Y5_R2FR_3365_DELTAGM_COMPONENT_MATRIX.csv",
        "DGMC3365_4 identifies R_nonEH_charge as missing coefficient/theorem row",
    ),
    (
        "SRC3367_3_3109_doc",
        ROOT / "3109-Y5-R2FR-Hilbert-worldtube-source-mass-lock-or-DeltaGM-residual-row-under-AX1090.md",
        "public EH dressed Hamiltonian source-mass lock and R_Hsrc residual split",
    ),
    (
        "SRC3367_4_3109_rows",
        OUT / "P8_Y5_R2FR_3109_SOURCE_MASS_LOCK_DELTA_GM_ROWS.csv",
        "SML3109_2 R_nonEH_charge source-mass component row",
    ),
    (
        "SRC3367_5_3339_decomposition",
        OUT / "P8_Y5_R2FR_3339_COUPLING_DECOMPOSITION_THEOREM.csv",
        "source coupling split J=kappa*T+DeltaJ",
    ),
    (
        "SRC3367_6_3339_measuredG",
        OUT / "P8_Y5_R2FR_3339_MEASURED_G_ABSORPTION_THEOREM.csv",
        "universal common mode measured-G absorption theorem",
    ),
    (
        "SRC3367_7_3339_residual_vector",
        OUT / "P8_Y5_R2FR_3339_RESIDUAL_CHANNEL_VECTOR.csv",
        "non-common residual projections: tensor/species/EM/contact/boundary",
    ),
    (
        "SRC3367_8_3340_parent_clause",
        OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv",
        "exact conditional parent Hilbert source clause",
    ),
    (
        "SRC3367_9_3340_theorem",
        OUT / "P8_Y5_R2FR_3340_HILBERT_SOURCE_THEOREM_OR_FAIL.csv",
        "conditional theorem and fallback residual vector",
    ),
    (
        "SRC3367_10_3341_runner_contract",
        OUT / "P8_Y5_R2FR_3341_COMPONENT_RUNNER_CONTRACT.csv",
        "runner acceptance rules for theorem-zero or finite source-backed residuals",
    ),
    (
        "SRC3367_11_2904_nonEH_theorem",
        OUT / "P8_Y5_R2FR_2904_CONDITIONAL_NON_EH_SILENCE_THEOREM.csv",
        "conditional non-EH sector silence theorem",
    ),
    (
        "SRC3367_12_2904_source_pack",
        OUT / "P8_Y5_R2FR_2904_NON_EH_QV_SOURCE_PACK.csv",
        "non-EH source pack rows for boundary/extra/projector/matter/hidden/constraint pieces",
    ),
    (
        "SRC3367_13_3274_gauge_lock",
        OUT / "P8_Y5_R2FR_3274_CURRENT_NORMALIZATION_GAUGE_LOCK_LEMMA.csv",
        "current-normalization zero route and compensator caveat",
    ),
    (
        "SRC3367_14_3274_poynting",
        OUT / "P8_Y5_R2FR_3274_EM_STRESS_POYNTING_EXCHANGE_LAW.csv",
        "EM stress/Poynting source-exchange law",
    ),
    (
        "SRC3367_15_3355_boundary",
        OUT / "P8_Y5_R2FR_3355_BOUNDARY_CONTACT_DECOMPOSITION.csv",
        "boundary/contact decomposition and contact survivor",
    ),
    (
        "SRC3367_16_3089_stokes",
        OUT / "P8_Y5_R2FR_3089_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv",
        "weighted Stokes exactness/bound law for boundary source leakage",
    ),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def local_source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        parse_ok = False
        parse_error = ""
        if exists:
            parse_ok, parse_error = parse_csv(path) if path.suffix.lower() == ".csv" else parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def selection_rows() -> list[dict[str, str]]:
    return [
        {
            "selection_id": "SEL3367_0_selected_component",
            "selected_component": "R_nonEH_charge",
            "source_rows": "DGMC3365_4_nonEH_charge;SML3109_2",
            "reason": "it is the first source-mass component that controls both Newtonian GM normalization and WEP/C_parent executability",
            "not_selected": "R_symp_reference;R_extra_source;R_time_frame;R_worldtube_support;PPN_second_order",
            "selection_policy": "attack parent-owned source coupling before repeating data-portal or WEP readout loops",
            "valid_for_claim": "false",
        },
        {
            "selection_id": "SEL3367_1_exact_question",
            "selected_component": "R_nonEH_charge",
            "source_rows": "3109 residual vector;3339 DeltaJ decomposition;2904 non-EH silence theorem",
            "reason": "ask whether a non-EH/source operator is common-mode, exact-zero-flux, massive/suppressed, or a physical residual",
            "not_selected": "bare rest mass",
            "selection_policy": "use dressed public Hamiltonian source mass as denominator; do not revive bare-mass circularity",
            "valid_for_claim": "false",
        },
    ]


def decomposition_rows() -> list[dict[str, str]]:
    return [
        {
            "piece_id": "RN3367_0_definition",
            "piece": "R_nonEH_charge",
            "mathematical_form": "R_nonEH[W,S]=-(1/(kappa_* c^2)) int_W P_N[E_X^{00}] dV + (1/(kappa_* c^2)) int_S B_X",
            "derivation": "write the local field equation as E_EH[g]+E_X[g,X]=kappa_* T_H; the Newtonian monopole is the 00 constraint integrated over the source worldtube plus its fixed linking-surface charge",
            "zero_or_bound_route": "classify E_X into common EH-proportional, exact boundary/improvement, massive/Yukawa, tensor/species/source, and Bianchi-leak pieces",
            "current_status": "DECOMPOSITION_DERIVED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "RN3367_1_common_EH_proportional",
            "piece": "a_X E_EH",
            "mathematical_form": "E_X^{mu nu}=a_X E_EH^{mu nu} with constant universal a_X on the local branch",
            "derivation": "substituting into the field equation gives (1+a_X)E_EH=kappa_*T_H, equivalent to kappa_* -> kappa_*/(1+a_X)",
            "zero_or_bound_route": "absorbed into measured G_ref M_H if a_X is universal, derivative-silent, source-blind and same-frame",
            "current_status": "ABSORBABLE_COMMON_MODE_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "RN3367_2_exact_improvement_flux",
            "piece": "nabla_lambda B_X^{lambda mu nu}",
            "mathematical_form": "E_X^{mu nu}=nabla_lambda B_X^{lambda mu nu}; R_nonEH^B proportional to int_S B_X",
            "derivation": "Gauss/Stokes converts the volume divergence into a linking-surface charge; it vanishes only for fixed closed surface, exact representative and zero flux/readout",
            "zero_or_bound_route": "zero if B_X is fixed-before-readout, q-basic, exact on the boundary class, and has no harmonic/residual/corner leakage; otherwise weighted-Stokes bound",
            "current_status": "ZERO_FLUX_CONDITIONAL_OR_BOUND",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "RN3367_3_massive_or_Yukawa_tail",
            "piece": "massive_nonEH_operator",
            "mathematical_form": "(Box-M_X^2)X=J_X; Phi_X(r)~alpha_X exp(-r/lambda_X)/r",
            "derivation": "a finite-range sourced mode contributes a real fifth-force/source-mass tail unless lambda_X is microscopic or alpha_X is bounded below the arena threshold",
            "zero_or_bound_route": "needs Z_X,M_X^2,J_X,K_X,Qbar_XH,qbar_XT and R10/PPN/orbital projection; no zero from covariance alone",
            "current_status": "MISSING_PARENT_COEFFICIENTS_OR_BOUNDS",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "RN3367_4_tensor_species_source_selector",
            "piece": "noncommon_DeltaJ_projection",
            "mathematical_form": "P_res[E_X] -> {xi_tensor, eta_species, epsilon_EM, epsilon_contact, epsilon_boundary, epsilon_bianchi}",
            "derivation": "after measured-G fixes one common Newtonian coefficient, tensor ratios, species weights, EM/Hodge/current shifts and boundary/source selectors survive as observables",
            "zero_or_bound_route": "must be parent-signed zero by Hilbert source clause or finite source-backed residual rows with no-cancellation guard",
            "current_status": "PHYSICAL_RESIDUAL_IF_NONZERO",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "RN3367_5_Bianchi_balance",
            "piece": "unbalanced_nonEH_divergence",
            "mathematical_form": "nabla_mu(E_X^{mu nu}-DeltaJ_X^{mu nu}) != 0",
            "derivation": "Bianchi-constrained GR comparison cannot hide an unbalanced divergence; it becomes a fifth-force/nonconservation residual",
            "zero_or_bound_route": "requires same-branch Ward identity or signed compensating field equation; otherwise clocks/orbits/WEP carry it",
            "current_status": "CONSERVATION_GATE_REQUIRED",
            "valid_for_claim": "false",
        },
    ]


def zero_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "ZRN3367_0_statement",
            "claim": "R_nonEH_charge is locally silent only if every non-EH source-charge piece is common-mode absorbed, exact zero-flux, or source-backed below its arena gate",
            "proof_sketch": "integrate the 00 constraint over the compact source worldtube; EH-proportional terms rescale the calibrated common coupling, divergence terms reduce to linking-surface flux, and all remaining noncommon projections survive as residual source channels",
            "required_parent_clauses": "same observed metric/coframe; fixed public time/reference/surface; parent Hilbert source clause; non-EH sector q-basic or constraint-proportional; no hidden source selector; Bianchi balance",
            "current_result": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ZRN3367_1_no_free_silence_lemma",
            "claim": "a non-EH term with an unscreened monopole, species weight, tensor-ratio change, hidden EM/Hodge/current coefficient, or boundary/contact support cannot be erased by measured G",
            "proof_sketch": "measured G fixes one scalar Newtonian common mode only; residual projectors are linearly independent observables in WEP, PPN, EM stress, clocks, R10, and orbital arenas",
            "required_parent_clauses": "projector independence from 3339 residual vector plus 3341 no-cancellation runner contract",
            "current_result": "DERIVED_REJECTION_OF_CLOSURE_SHORTCUT",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ZRN3367_2_common_mode_allowed",
            "claim": "constant universal a_X E_EH is not a local-GR failure by itself",
            "proof_sketch": "(1+a_X)E_EH=kappa_*T_H is algebraically identical to a redefinition of the calibrated kappa/G slot if a_X is source-blind and derivative-silent",
            "required_parent_clauses": "a_X constant, universal, same for matter/EM/stress/clock sectors, and fixed before readout",
            "current_result": "ALLOWED_CALIBRATION_MODE_NOT_NUMERIC_G_DERIVATION",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ZRN3367_3_exact_flux_zero",
            "claim": "exact boundary/improvement terms do not shift source mass only when their fixed linking-surface flux vanishes",
            "proof_sketch": "R_nonEH^B is a surface term; Stokes gives zero only for closed/corner-free domain, exact primitive, closed kernel weight, no harmonic/residual piece, and fixed reference",
            "required_parent_clauses": "3089 weighted-Stokes zero conditions plus 3355 no contact/interface survivor",
            "current_result": "CONDITIONAL_ZERO_WITH_CONTACT_SURVIVOR_OPEN",
            "valid_for_claim": "false",
        },
    ]


def coefficient_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "CNR3367_0_required_parent_row",
            "quantity": "C_nonEH^I or DERIVED_ZERO",
            "required_columns": "branch_id;operator_id;operator_form;basis;coefficient_value;units;mass_dimension;sign_convention;source_path;parent_status;valid_for_claim",
            "acceptance_rule": "each retained non-EH operator must be parent-owned numeric/source-backed or exact theorem-zero in the same branch",
            "current_status": "MISSING_PARENT_COEFFICIENT_VECTOR",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CNR3367_1_required_green_row",
            "quantity": "nonEH Green/kernel data",
            "required_columns": "operator_id;Z_X;M_X2;lambda_X;kernel_type;local_limit;source_path;valid_for_claim",
            "acceptance_rule": "distinguish common local renormalization, finite-range Yukawa tail, derivative contact, and unscreened monopole before scoring",
            "current_status": "MISSING_OPERATOR_KERNEL",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CNR3367_2_required_projection_row",
            "quantity": "P_arena R_nonEH",
            "required_columns": "operator_id;arena;projection_formula;response_factor;bound_value;bound_units;no_cancellation_policy;source_path;valid_for_claim",
            "acceptance_rule": "PPN/R10/WEP/orbital/clock projections must use absolute no-cancellation unless a parent cancellation theorem is supplied",
            "current_status": "MISSING_ARENA_PROJECTIONS",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CNR3367_3_required_boundary_row",
            "quantity": "B_X flux or weighted-Stokes bound",
            "required_columns": "operator_id;surface_id;C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs;M_H_ref;units;source_path;valid_for_claim",
            "acceptance_rule": "zero only after exactness/cohomology/reference/contact clauses close; otherwise bound the surface term",
            "current_status": "MISSING_BOUNDARY_FLUX_OR_BOUND",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3367_0_common_mode_case",
            "case": "E_X=a_X E_EH with constant universal a_X",
            "result": "PASS_AS_CALIBRATION_MODE_NONCLAIM",
            "reason": "absorbed into measured G_ref M_H if source-blind, derivative-silent and same-frame; does not derive numeric G",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3367_1_exact_flux_case",
            "case": "E_X=nabla B_X with zero fixed linking-surface flux",
            "result": "PASS_CONDITIONAL_ZERO_NONCLAIM",
            "reason": "valid local math route, but boundary exactness/contact/support premises are not parent-owned in current corpus",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3367_2_Yukawa_case",
            "case": "finite-range non-EH source mode",
            "result": "REFUSE_UNTIL_COEFFICIENT_AND_ARENA_BOUND_EXIST",
            "reason": "needs Z_X,M_X2,J_X,K_X,Qbar_XH,qbar_XT and R10/PPN/orbital projection",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3367_3_noncommon_source_case",
            "case": "species/tensor/EM/boundary/source selector projection nonzero",
            "result": "REFUSE_MEASURED_G_ABSORPTION",
            "reason": "one G calibration cannot absorb non-common residual projectors",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3367_4_full_RnonEH_claim",
            "case": "R_nonEH_charge=0 for current MTS corpus",
            "result": "BLOCKED_NOT_PARENT_SIGNED",
            "reason": "conditional theorem exists, but parent action has not classified every retained non-EH operator",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3367_0_component_selected",
            "claim": "first DeltaGM source-mass component selected",
            "passed": "true",
            "reason": "R_nonEH_charge selected from DGMC3365_4/SML3109_2",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3367_1_decomposition_derived",
            "claim": "R_nonEH_charge decomposition derived",
            "passed": "true",
            "reason": "field-equation/constraint integration splits common, exact-flux, massive, noncommon, and Bianchi pieces",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3367_2_closure_shortcut_rejected",
            "claim": "non-EH source charge cannot be silently ignored",
            "passed": "true",
            "reason": "no-free-silence lemma forces common-mode, zero-flux, or source-backed residual route",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3367_3_parent_operator_classified",
            "claim": "every retained non-EH operator is parent-classified",
            "passed": "false",
            "reason": "C_nonEH/operator/kernel/projection rows are missing",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3367_4_RnonEH_zero_or_bound",
            "claim": "R_nonEH_charge is theorem-zero or source-backed bounded",
            "passed": "false",
            "reason": "conditional zero routes are not parent-signed and finite coefficient rows are missing",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3367_5_Newton_local_GR",
            "claim": "source-normalized Newton/local-GR branch is promoted",
            "passed": "false",
            "reason": "first component narrowed but not closed; other DeltaGM components also remain",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3367_0_progress",
            "question": "Did 3367 move beyond another missing ledger?",
            "answer": "yes",
            "reason": "it derives the exact R_nonEH charge decomposition and a no-free-silence lemma: non-EH source mass must be common-mode, exact-zero-flux, or bounded",
            "next_action": "classify actual parent non-EH operator terms instead of asking for generic coupling",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3367_1_common_mode",
            "question": "Can a non-EH term be harmless?",
            "answer": "yes, but only as universal common EH-proportional calibration or exact zero-flux improvement",
            "reason": "measured G absorbs one source-blind scalar common mode; exact improvements vanish only with fixed zero flux",
            "next_action": "look for parent action clauses that force retained non-EH terms into those classes",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3367_2_best_next",
            "question": "What is the next real derivation target?",
            "answer": "extract or construct the parent non-EH operator classification table",
            "reason": "without operator_id/coefficient/kernel/projection rows, neither WEP nor Newton can execute the source-coupling branch",
            "next_action": "3368 should parse/search parent action material for E_X operator forms and classify each as common/exact/massive/noncommon",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3368-Y5-R2FR-parent-nonEH-operator-classification-or-source-coefficient-first-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3368_parent_nonEH_operator_classification_or_source_coefficient_first_row.py",
            "objective": "extract the actual parent non-EH/source-coupling operator candidates from the corpus and classify each as common-mode, exact-flux, massive/Yukawa, noncommon residual, or absent",
            "why_next": "3367 derives the classifier; 3368 must feed it real operator rows so R_nonEH_charge can become theorem-zero or bounded rather than abstract",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3369-Y5-R2FR-RnonEH-bound-envelope-from-PPN-R10-WEP-orbit-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3369_RnonEH_bound_envelope_from_PPN_R10_WEP_orbit.py",
            "objective": "if parent operator extraction fails, build a nonclaim absolute bound envelope for R_nonEH pieces using existing PPN/R10/WEP/orbital comparator rows",
            "why_next": "a clean finite bound route is better than closure if the parent action will not yet give theorem-zero",
            "valid_for_claim": "false",
        },
    ]


def validate_rows(
    source_rows: list[dict[str, str]],
    selection: list[dict[str, str]],
    decomposition: list[dict[str, str]],
    zero_theorem: list[dict[str, str]],
    coefficient_contract: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    add(
        "VAL3367_0_local_sources_exist",
        "all cited local source paths exist",
        all(row["exists"] == "true" for row in source_rows),
    )
    add(
        "VAL3367_1_local_sources_parse",
        "all cited local source paths parse",
        all(row["parse_ok"] == "true" for row in source_rows),
    )
    add(
        "VAL3367_2_selected_RnonEH",
        "selected component is R_nonEH_charge",
        any(row["selected_component"] == "R_nonEH_charge" for row in selection),
    )
    required_pieces = {
        "R_nonEH_charge",
        "a_X E_EH",
        "nabla_lambda B_X^{lambda mu nu}",
        "massive_nonEH_operator",
        "noncommon_DeltaJ_projection",
        "unbalanced_nonEH_divergence",
    }
    seen_pieces = {row["piece"] for row in decomposition}
    add(
        "VAL3367_3_decomposition_complete",
        "decomposition covers definition/common/exact/massive/noncommon/Bianchi pieces",
        required_pieces == seen_pieces,
        "seen=" + ";".join(sorted(seen_pieces)),
    )
    add(
        "VAL3367_4_no_free_silence_lemma_present",
        "zero theorem includes no-free-silence lemma",
        any(row["theorem_id"] == "ZRN3367_1_no_free_silence_lemma" for row in zero_theorem),
    )
    add(
        "VAL3367_5_coefficient_contract_complete",
        "coefficient contract covers parent coefficient, kernel, projection and boundary rows",
        {row["quantity"] for row in coefficient_contract}
        == {"C_nonEH^I or DERIVED_ZERO", "nonEH Green/kernel data", "P_arena R_nonEH", "B_X flux or weighted-Stokes bound"},
    )
    add(
        "VAL3367_6_runner_blocks_current_RnonEH_claim",
        "runner blocks current R_nonEH zero claim",
        any(row["run_id"] == "RUN3367_4_full_RnonEH_claim" and row["result"] == "BLOCKED_NOT_PARENT_SIGNED" for row in runner),
    )
    add(
        "VAL3367_7_no_local_GR_promotion",
        "Newton/local-GR gate remains false",
        any(row["gate_id"] == "GATE3367_5_Newton_local_GR" and row["passed"] == "false" for row in gates),
    )
    add(
        "VAL3367_8_next_target_operator_classification",
        "next target extracts/classes actual parent non-EH operators",
        any(row["target_id"].startswith("3368-") for row in next_rows),
    )
    all_write_targets = list(OUTPUTS.values()) + [DOC]
    add(
        "VAL3367_9_write_scope_outside_formalization",
        "all 3367 write targets are outside formalization-workbench",
        all(not str(path).lower().startswith(str(FW).lower()) for path in all_write_targets),
        f"write_targets={len(all_write_targets)}",
    )
    passed_so_far = all(row["passed"] == "true" for row in rows)
    add(
        "VAL3367_10_overall",
        "3367 validation overall",
        passed_so_far,
        "all required checks passed" if passed_so_far else "one or more checks failed",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, str]],
    selection: list[dict[str, str]],
    decomposition: list[dict[str, str]],
    zero_theorem: list[dict[str, str]],
    coefficient_contract: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_rows: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    content = f"""# 3367 - Y5/R2FR first DeltaGM mass-charge component row under AX1090

## Summary
- This checkpoint takes the first hard `DeltaGM` source-mass component: `R_nonEH_charge`.
- Actual derivation gain: `R_nonEH_charge` is no longer a vague missing coupling. It is split into common EH-proportional calibration, exact/improvement flux, massive/Yukawa tail, non-common residual projector, and Bianchi-balance pieces.
- Useful theorem: a universal EH-proportional non-EH term can be absorbed into measured `G_ref M_H`; an exact improvement can vanish only by fixed zero flux; everything else is a physical residual and must be parent-zeroed or bounded.
- This rejects the closure shortcut: non-EH local charge hair cannot be silently erased by saying "measured G takes care of it" unless it is truly common-mode.
- No Newton/local-GR promotion is made; the next real job is to classify the actual parent non-EH operators against this new classifier.

Generated UTC: `{RUN_UTC}`

## Source Register
{markdown_table(sources)}

## Component Selection
{markdown_table(selection)}

## R_nonEH Charge Decomposition
{markdown_table(decomposition)}

## Zero Theorem Contract
{markdown_table(zero_theorem)}

## Coefficient Contract
{markdown_table(coefficient_contract)}

## Nonclaim Runner
{markdown_table(runner)}

## Promotion Gates
{markdown_table(gates)}

## Decision Ledger
{markdown_table(decisions)}

## Next Target
{markdown_table(next_rows)}

## Validation
{markdown_table(validations)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = local_source_rows()
    selection = selection_rows()
    decomposition = decomposition_rows()
    zero_theorem = zero_theorem_rows()
    coefficient_contract = coefficient_contract_rows()
    runner = runner_rows()
    gates = promotion_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    validations = validate_rows(
        sources,
        selection,
        decomposition,
        zero_theorem,
        coefficient_contract,
        runner,
        gates,
        next_rows,
    )

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["selection"], selection)
    write_csv(OUTPUTS["decomposition"], decomposition)
    write_csv(OUTPUTS["zero_theorem"], zero_theorem)
    write_csv(OUTPUTS["coefficient_contract"], coefficient_contract)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, selection, decomposition, zero_theorem, coefficient_contract, runner, gates, decisions, next_rows, validations)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
