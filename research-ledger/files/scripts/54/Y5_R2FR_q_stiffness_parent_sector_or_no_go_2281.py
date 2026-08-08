from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_Q_STIFFNESS_PARENT_SECTOR_OR_NO_GO_2281"
DOC = ROOT / "2281-Y5-R2FR-q-stiffness-parent-sector-or-no-go.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2281_00_2280_doc",
        "source_key": "2280_doc",
        "source_path": ROOT / "2280-Y5-R2FR-phase-lock-distribution-or-q-residual-operator-owner.md",
        "needles": ["NEXT2280_0_primary", "Q_STIFFNESS_OR_ONSAGER_OWNER_IS_BEST_ROUTE", "invariant-manifold ownership"],
        "role": "handoff selecting q-stiffness parent sector or no-go",
    },
    {
        "source_id": "SRC2281_01_2280_validation",
        "source_key": "2280_validation",
        "source_path": OUT / "P8_Y5_BRR545_2280_VALIDATION.csv",
        "needles": ["VAL2280_OVERALL", "PASS"],
        "role": "confirms 2280 passed before 2281 starts",
    },
    {
        "source_id": "SRC2281_02_2280_invariant_law",
        "source_key": "2280_q_invariant_law",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2280_Q_INVARIANT_MANIFOLD_LAW.csv",
        "needles": ["QIM2280_1_invariant_manifold", "E_R - F'(C_T) E_T + B_q = 0"],
        "role": "exact q=0 tangency law",
    },
    {
        "source_id": "SRC2281_03_2280_operator_owner",
        "source_key": "2280_q_operator_owner",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2280_Q_OPERATOR_OWNER_AUDIT.csv",
        "needles": ["QOO2280_2_q_stiffness_sector", "BEST_CONDITIONAL_ROUTE"],
        "role": "q-stiffness selected as conditional route",
    },
    {
        "source_id": "SRC2281_04_effective_field_theory",
        "source_key": "effective_field_theory",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "field-theory" / "the-effective-field-theory-of-motion-timespace.md",
        "needles": ["Coarse-graining the ψ-covariance", "A_eff[g]", "GR is the IR limit"],
        "role": "corpus basis for covariance coarse-graining and IR GR language",
    },
    {
        "source_id": "SRC2281_05_action_principle",
        "source_key": "action_principle",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
        "needles": ["smoothed covariance", "coarse-graining", "standard matter"],
        "role": "corpus basis for emergent metric/action and matter-coupling target",
    },
    {
        "source_id": "SRC2281_06_time_entropy",
        "source_key": "time_entropy_exchange",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "relativity" / "time-as-thermodynamic-exchange-in-motion-timespace-a-unified-framework-for-relativity-and-thermodynamics.md",
        "needles": ["second law", "dS / dE", "curvature stiffness and memory"],
        "role": "corpus support for entropy/dissipation/stiffness motifs",
    },
    {
        "source_id": "SRC2281_07_core_gravity",
        "source_key": "core_gravity_unified",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md",
        "needles": ["Single controlling scalar", "curvature memory / hysteresis", "positive geometric pressure"],
        "role": "corpus support for scalar response, memory, and positivity language",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2281_SOURCE_REGISTER.csv",
    "derivation": OUT / "P8_Y5_PARENT_QLOC_2281_Q_STIFFNESS_DERIVATION_AUDIT.csv",
    "selector_gap": OUT / "P8_Y5_PARENT_QLOC_2281_COVARIANCE_MANIFOLD_SELECTOR_GAP.csv",
    "operator_contract": OUT / "P8_Y5_PARENT_QLOC_2281_Q_OPERATOR_CONTRACT.csv",
    "residual_bound": OUT / "P8_Y5_PARENT_QLOC_2281_RESIDUAL_BOUND_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2281_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2281_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2281_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2281_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2281_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2281_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_derivation": QUEUE / "JR2281_Q_STIFFNESS_DERIVATION_AUDIT_NONCLAIM.csv",
    "queue_selector_gap": QUEUE / "JR2281_COVARIANCE_MANIFOLD_SELECTOR_GAP_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_q_stiffness_parent_sector_refusal_2281.csv",
    "beta_docs": BETA_DOCS / "RAB_Q_STIFFNESS_PARENT_CONTRACT_2281_NONCLAIM.csv",
}


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def ignored_environment_path(path: Path) -> bool:
    ignored_parts = {".venv", ".venv-score", "__pycache__", "site-packages", ".git"}
    return any(part in ignored_parts for part in path.parts)


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": path,
                "exists": path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "QSD2281_0_covariance_variable",
            "derivation_step": "Define coarse covariance coordinates C_A from psi gradients.",
            "formula": "C_{mu nu}(x)=<partial_mu psi partial_nu psi>_smooth; q(C)=C_R-C_T/(1-C_T)",
            "result": "CORPUS_SUPPORTED_COORDINATE",
            "proof_status": "supported by covariance coarse-graining sources",
            "valid_for_claim": False,
        },
        {
            "step_id": "QSD2281_1_large_deviation_form",
            "derivation_step": "Coarse-grained fluctuations around an equilibrium covariance manifold have a positive quadratic cost.",
            "formula": "I[C]=I[C_*]+1/2 delta C_A H^{AB} delta C_B+O(delta C^3), H>=0",
            "result": "STANDARD_CONDITIONAL_COARSE_GRAINING_FORM",
            "proof_status": "conditional: requires parent equilibrium C_* and positive Hessian",
            "valid_for_claim": False,
        },
        {
            "step_id": "QSD2281_2_transverse_q_mass",
            "derivation_step": "Project the covariance Hessian onto the normal direction to q=0.",
            "formula": "M_q^2 = n_q^A H_{AB} n_q^B, n_q=dq/dC",
            "result": "DERIVES_POSITIVE_MASS_IF_H_POSITIVE_AND_Q_NORMAL_NONZERO",
            "proof_status": "conditional derivation; not yet parent-signed for MTS local branch",
            "valid_for_claim": False,
        },
        {
            "step_id": "QSD2281_3_gradient_expansion",
            "derivation_step": "Finite smoothing length/correlation length gives a transverse gradient penalty.",
            "formula": "Z_q = xi_q^2 n_q^A H_{AB} n_q^B, so F_q contains 1/2 Z_q |nabla q|^2",
            "result": "DERIVES_POSITIVE_STIFFNESS_IF_XI_Q^2_POSITIVE",
            "proof_status": "conditional: smoothing kernel and correlation length are not sourced numerically",
            "valid_for_claim": False,
        },
        {
            "step_id": "QSD2281_4_operator",
            "derivation_step": "The quadratic q free energy produces the residual operator.",
            "formula": "delta F_q/delta q = -nabla_i(Z_q nabla^i q)+M_q^2 q = L_q q",
            "result": "Q_OPERATOR_FORM_DERIVED_CONDITIONALLY",
            "proof_status": "conditional: coefficients, boundary domain, and units remain missing",
            "valid_for_claim": False,
        },
        {
            "step_id": "QSD2281_5_onsager",
            "derivation_step": "Entropy/dissipation language permits a relaxation law if a nonnegative mobility is supplied.",
            "formula": "Dq=-mu_q delta F_q/delta q + source, with mu_q>=0",
            "result": "ONSAGER_ROUTE_CONDITIONAL",
            "proof_status": "conditional: no parent mobility or entropy-production functional for q is supplied",
            "valid_for_claim": False,
        },
        {
            "step_id": "QSD2281_6_no_smuggling_test",
            "derivation_step": "The q=0 manifold must be selected before q-stiffness is claim-grade.",
            "formula": "q=0 must be C_*(theta) equilibrium, not a fitted penalty target",
            "result": "SELECTOR_GAP_IS_THE_MAIN_BLOCKER",
            "proof_status": "not derived in current corpus",
            "valid_for_claim": False,
        },
    ]


def selector_gap_rows() -> list[dict[str, Any]]:
    return [
        {
            "gap_id": "CSG2281_0_positivity_limit",
            "candidate_selector": "covariance positivity alone",
            "test": "C_{mu nu} positive/semi-definite constrains allowed covariance values",
            "outcome": "INSUFFICIENT",
            "reason": "positivity can give a convex cost around an already-selected state, but it does not pick the nonlinear relation C_R=C_T/(1-C_T)",
            "next_evidence_needed": "independent equilibrium/metric-compatibility/quotient condition selecting q=0",
            "valid_for_claim": False,
        },
        {
            "gap_id": "CSG2281_1_metric_compatibility",
            "candidate_selector": "emergent metric compatibility/local Lorentz branch",
            "test": "require covariance metric to have a GR-compatible local tetrad branch",
            "outcome": "PROMISING_BUT_UNSIGNED",
            "reason": "could select a relation among temporal/radial covariance components, but the exact C_R=C_T/(1-C_T) law is not derived from tetrad compatibility yet",
            "next_evidence_needed": "derive q=0 from tetrad normalization, signature, and Newtonian weak-field clock/radial matching",
            "valid_for_claim": False,
        },
        {
            "gap_id": "CSG2281_2_bianchi_conservation",
            "candidate_selector": "Bianchi/conservation consistency",
            "test": "nabla_mu(G^{mu nu}+Gamma g^{mu nu}-kappa T^{mu nu})=0",
            "outcome": "NEEDS_FIELD_LEVEL_MAP",
            "reason": "conservation can restrict source terms and exchange, but needs the map from q to effective stress and matter readout",
            "next_evidence_needed": "derive T_q^{mu nu}, boundary flux, and source normalization map",
            "valid_for_claim": False,
        },
        {
            "gap_id": "CSG2281_3_entropy_minimum",
            "candidate_selector": "entropy/free-energy extremum",
            "test": "q=0 is an extremum of a parent entropy/free-energy functional",
            "outcome": "POSSIBLE_BUT_CURRENTLY_ASSUMED",
            "reason": "MTS has entropy/dissipation motifs, but no explicit entropy functional whose first variation gives q=0",
            "next_evidence_needed": "write S_eff[C] or F_eff[C] and show partial F/partial q=0 at q=0",
            "valid_for_claim": False,
        },
        {
            "gap_id": "CSG2281_4_direct_penalty",
            "candidate_selector": "add V(q)=1/2 M_q^2 q^2 by hand",
            "test": "penalty enforces local GR residual suppression",
            "outcome": "CLOSURE_ONLY",
            "reason": "this is mathematically useful but not a derivation unless M_q^2 and the target q=0 come from parent geometry",
            "next_evidence_needed": "label as closure, not local-GR derivation",
            "valid_for_claim": False,
        },
    ]


def operator_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "QOC2281_0_action_term",
            "requirement": "If accepted as a parent sector, write the q-sector covariantly.",
            "formula": "S_q=-1/2 integral sqrt(-g_eff)[Z_q h^{ij} nabla_i q nabla_j q + M_q^2 q^2]",
            "status": "FORMAL_TEMPLATE_ONLY",
            "missing_inputs": "definition of h^{ij}; units; Z_q; M_q^2; source path; variation convention",
            "valid_for_claim": False,
        },
        {
            "contract_id": "QOC2281_1_positivity",
            "requirement": "Coercivity requires positive coefficients on the physical/gauge-reduced domain.",
            "formula": "Z_q>=Z_min>0 and M_q^2>=M_min^2>0 after quotient/gauge reduction",
            "status": "CONDITIONAL_FROM_HESSIAN_ONLY",
            "missing_inputs": "positive Hessian proof; no ghost/gauge-zero mode audit; normalization",
            "valid_for_claim": False,
        },
        {
            "contract_id": "QOC2281_2_boundary",
            "requirement": "Boundary terms must vanish or be bounded.",
            "formula": "int_boundary Z_q q n^i nabla_i q = 0 or <= epsilon_boundary",
            "status": "UNSIGNED",
            "missing_inputs": "local cell boundary class; no-flux theorem; matching to exterior",
            "valid_for_claim": False,
        },
        {
            "contract_id": "QOC2281_3_observable_projection",
            "requirement": "q residuals must map into PPN/R10/clock/orbital observables.",
            "formula": "R_obs=P_obs q and ||R_obs|| <= ||P_obs|| ||L_q^{-1}|| ||S_q||",
            "status": "MISSING_PROJECTION",
            "missing_inputs": "P_obs for gamma/beta/Gdot/R10/clocks/orbits; units and source normalization",
            "valid_for_claim": False,
        },
        {
            "contract_id": "QOC2281_4_newton_limit",
            "requirement": "The same parent source must recover Newtonian mechanics, not merely suppress q.",
            "formula": "nabla^2 Phi=4 pi G rho and a=-nabla Phi must use the same source normalization as the q-sector",
            "status": "SEPARATE_DEBT_RETAINED",
            "missing_inputs": "worldtube/Hilbert source equality and measured-GM pullback remain unsolved",
            "valid_for_claim": False,
        },
    ]


def residual_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "RBL2281_0_elliptic",
            "operator": "L_q=-nabla_i(Z_q nabla^i)+M_q^2",
            "bound": "||q|| <= ||L_q^{-1}|| ||S_q|| <= ||S_q||/lambda_min(L_q)",
            "claim_status": "CONDITIONAL_BOUND",
            "blocked_by": "lambda_min not sourced; boundary domain missing",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RBL2281_1_mass_gap",
            "operator": "uniform mass gap",
            "bound": "if Z_q>=0 and M_q^2>=M_min^2>0 then lambda_min(L_q)>=M_min^2",
            "claim_status": "CONDITIONAL_BOUND",
            "blocked_by": "M_min^2 not parent-derived",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RBL2281_2_onsager_decay",
            "operator": "Dq=-mu_q L_q q + S_q",
            "bound": "||q(t)|| <= exp(-mu_min lambda_min t)||q(0)|| + convolution(source)",
            "claim_status": "CONDITIONAL_BOUND",
            "blocked_by": "mu_q and entropy production law not parent-derived",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RBL2281_3_local_observable",
            "operator": "R_local=P_obs q",
            "bound": "||R_local|| <= ||P_obs|| ||L_q^{-1}|| ||S_q||",
            "claim_status": "NONCLAIM_TEMPLATE",
            "blocked_by": "P_obs and experimental arena maps missing",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2281_0_conditional_stiffness_derivation",
            "claim": "positive q-stiffness follows from a positive covariance Hessian around a q=0 equilibrium manifold",
            "gate_pass": True,
            "reason": "quadratic expansion and projection onto q-normal gives M_q^2=n_q H n_q and Z_q=xi_q^2 n_q H n_q",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2281_1_covariance_positivity_selects_q_zero",
            "claim": "covariance positivity alone selects q=0",
            "gate_pass": False,
            "reason": "positivity constrains the covariance cone but does not pick the nonlinear GR branch relation",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2281_2_current_corpus_derives_parent_q_sector",
            "claim": "current corpus fully derives the q-sector coefficients",
            "gate_pass": False,
            "reason": "Z_q, M_q^2, xi_q, boundary domain, and selector functional remain unsigned",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2281_3_local_gr_newton",
            "claim": "local GR/Newton recovery is derived",
            "gate_pass": False,
            "reason": "q-stiffness is only conditional and Newton/source normalization is a separate retained debt",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2281_4_best_next_target",
            "claim": "next target should derive the covariance-equilibrium selector or declare q-closure",
            "gate_pass": True,
            "reason": "the stiffness operator can be conditionally built, but the target manifold selector is the decisive missing premise",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2281_0_full_q_derivation",
            "attempted_claim": "q-stiffness is fully derived from the existing corpus.",
            "runner_result": "BLOCKED",
            "blocked_by": "selector functional for q=0, coefficients, units, and boundary domain are missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2281_1_positivity_claim",
            "attempted_claim": "covariance positivity alone proves local GR.",
            "runner_result": "BLOCKED",
            "blocked_by": "positivity supplies coercivity after a target is selected; it does not select the target relation",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2281_2_closure_as_derivation",
            "attempted_claim": "adding V(q)=1/2 M_q^2 q^2 by hand is a derivation.",
            "runner_result": "BLOCKED",
            "blocked_by": "direct penalty is closure-only without parent geometry/entropy selecting q=0",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2281_3_local_gr_newton",
            "attempted_claim": "MTS has now derived local GR/Newton mechanics.",
            "runner_result": "BLOCKED",
            "blocked_by": "q-sector is conditional and Newton/source normalization remains open",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2281_0_real_gain",
            "decision": "Q_STIFFNESS_CONDITIONALLY_DERIVED_FROM_COVARIANCE_HESSIAN",
            "reason": "once q=0 is a parent-selected covariance equilibrium, the transverse quadratic expansion naturally yields positive M_q^2/Z_q.",
            "next_action": "do not claim until the q=0 selector is derived.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2281_1_no_go_piece",
            "decision": "COVARIANCE_POSITIVITY_ALONE_NO_GO",
            "reason": "positivity gives a cone/coercivity, not the exact nonlinear q=0 branch.",
            "next_action": "derive the selector from metric compatibility, quotient regularity, or entropy extremum.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2281_2_local_branch_status",
            "decision": "LOCAL_BRANCH_REMAINS_NONCLAIM_BUT_SHARPER",
            "reason": "the operator form is no longer foggy, but the parent selector and observable maps are not signed.",
            "next_action": "attempt the covariance-equilibrium selector.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2281_3_next",
            "decision": "COVARIANCE_EQUILIBRIUM_SELECTOR_NEXT",
            "reason": "this is the actual hinge between derivation and closure.",
            "next_action": "2282-Y5-R2FR-covariance-equilibrium-selector-or-q-closure-declaration.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2281_0_primary",
            "next_target": "2282-Y5-R2FR-covariance-equilibrium-selector-or-q-closure-declaration.md",
            "script": "scripts/Y5_R2FR_covariance_equilibrium_selector_or_q_closure_declaration_2282.py",
            "objective": "derive why the coarse-grained covariance equilibrium manifold is q=0 from metric compatibility, quotient regularity, entropy extremum, or Bianchi/source consistency; otherwise declare q-stiffness closure-only",
            "selection_status": "selected",
            "success_condition": "q=0 selector is parent-signed and not inserted by hand, or a closure ledger explicitly blocks local-GR/Newton claims",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_by_copy = {
        "queue_derivation": OUTPUTS["derivation"],
        "queue_selector_gap": OUTPUTS["selector_gap"],
        "branch_wep": OUTPUTS["refusal"],
        "beta_docs": OUTPUTS["operator_contract"],
    }
    return [
        {
            "copy_id": copy_id,
            "source_path": source_by_copy[copy_id],
            "target_path": target,
            "target_exists": target.exists(),
            "target_parses": csv_parses(target) if target.exists() else False,
            "reason": "branch copy for covariance selector and q-closure follow-up work",
        }
        for copy_id, target in COPY_TARGETS.items()
    ]


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def false_flag_check() -> bool:
    guarded_fields = {"score_ready", "score_eligible", "accepted_ready", "valid_for_claim", "claim_allowed"}
    for path in generated_csvs():
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                for field in guarded_fields.intersection(row):
                    if row[field].strip().lower() == "true":
                        return False
                if "gate_pass" in row and row.get("valid_for_claim", "").strip().lower() == "true":
                    return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    source_ok = all(row["exists"] for row in source_rows)
    needles_ok = all(row["needles_present"] for row in source_rows)

    prior_text = read_text(OUT / "P8_Y5_BRR545_2280_VALIDATION.csv")
    prior_ok = "VAL2280_OVERALL" in prior_text and "PASS" in prior_text

    derivation = derivation_rows()
    gaps = selector_gap_rows()
    contract = operator_contract_rows()
    bounds = residual_bound_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()

    covariance_step = any(row["step_id"] == "QSD2281_0_covariance_variable" for row in derivation)
    hessian_step = any(row["step_id"] == "QSD2281_2_transverse_q_mass" and "M_q^2" in row["formula"] for row in derivation)
    selector_gap = any(row["gap_id"] == "CSG2281_0_positivity_limit" and row["outcome"] == "INSUFFICIENT" for row in gaps)
    closure_guard = any(row["gap_id"] == "CSG2281_4_direct_penalty" and row["outcome"] == "CLOSURE_ONLY" for row in gaps)
    operator_contract = any(row["contract_id"] == "QOC2281_0_action_term" for row in contract)
    boundary_missing = any(row["contract_id"] == "QOC2281_2_boundary" and row["status"] == "UNSIGNED" for row in contract)
    observable_missing = any(row["contract_id"] == "QOC2281_3_observable_projection" and row["status"] == "MISSING_PROJECTION" for row in contract)
    residual_bounds = len(bounds) >= 4 and all(row["valid_for_claim"] is False for row in bounds)
    conditional_not_claim = any(row["claim_id"] == "CG2281_0_conditional_stiffness_derivation" and row["gate_pass"] is True and row["valid_for_claim"] is False for row in claims)
    local_blocked = any(row["claim_id"] == "CG2281_3_local_gr_newton" and row["gate_pass"] is False for row in claims)
    refusal_blocks = all(row["runner_result"] == "BLOCKED" and row["valid_for_claim"] is False for row in refusals)
    next_selected = any(row["route_id"] == "NEXT2281_0_primary" and row["selection_status"] == "selected" for row in next_target_rows())
    csvs_parse = all(csv_parses(path) for path in generated_csvs())
    no_claim_flags = false_flag_check()
    copies_ok = all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = (
        not any(not ignored_environment_path(path) for path in FORMALIZATION.rglob("*2281*"))
        if FORMALIZATION.exists()
        else True
    )

    checks = [
        ("VAL2281_0_sources_exist", source_ok, "all cited source paths exist"),
        ("VAL2281_1_needles_present", needles_ok, "all cited source needles are present"),
        ("VAL2281_2_prior_validation", prior_ok, "2280 validation passes"),
        ("VAL2281_3_covariance_step", covariance_step, "covariance q-coordinate step written"),
        ("VAL2281_4_hessian_step", hessian_step, "transverse Hessian M_q^2 derivation written"),
        ("VAL2281_5_selector_gap", selector_gap, "covariance positivity alone is marked insufficient"),
        ("VAL2281_6_closure_guard", closure_guard, "direct q penalty is closure-only unless parent-selected"),
        ("VAL2281_7_operator_contract", operator_contract, "q-sector action contract written"),
        ("VAL2281_8_boundary_missing", boundary_missing, "boundary silence remains unsigned"),
        ("VAL2281_9_observable_missing", observable_missing, "observable projection remains missing"),
        ("VAL2281_10_residual_bounds", residual_bounds, "residual bounds are conditional nonclaim rows"),
        ("VAL2281_11_conditional_not_claim", conditional_not_claim, "conditional stiffness derivation is not promoted to claim"),
        ("VAL2281_12_local_blocked", local_blocked, "local GR/Newton claim remains blocked"),
        ("VAL2281_13_refusal_blocks", refusal_blocks, "refusal runner blocks overclaims"),
        ("VAL2281_14_next_selected", next_selected, "2282 target selected"),
        ("VAL2281_15_csv_parse", csvs_parse, "all generated 2281 CSVs parse"),
        ("VAL2281_16_no_claim_flags", no_claim_flags, "no generated claim-validity flags are true"),
        ("VAL2281_17_branch_copies", copies_ok, "branch/queue copies exist and parse"),
        ("VAL2281_18_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL2281_19_formalization_no_2281", formalization_clean, "formalization-workbench has no 2281 output files"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    overall = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2281_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2281 conditionally derives q-stiffness from a covariance Hessian, proves covariance positivity alone does not select q=0, blocks local claims, and selects the covariance-equilibrium selector target",
        }
    )
    return rows


def write_doc() -> None:
    sources = source_register_rows()
    derivation = derivation_rows()
    gaps = selector_gap_rows()
    contract = operator_contract_rows()
    bounds = residual_bound_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    copies = branch_copy_rows()
    validation = validation_rows()

    sections = [
        "# 2281 - Y5/R2FR q-Stiffness Parent Sector Or No-Go",
        "",
        "## Verdict",
        "",
        "This checkpoint gets a real mathematical gain, but not a public claim. If the coarse-grained covariance sector has an equilibrium manifold `q=0`, then the transverse second variation gives a natural `q` mass/stiffness: `M_q^2=n_q^A H_AB n_q^B` and `Z_q=xi_q^2 n_q^A H_AB n_q^B`. That is a legitimate conditional derivation of the operator shape.",
        "",
        "The no-go piece is just as important: covariance positivity/coarse-graining alone does **not** select the nonlinear branch `C_R=C_T/(1-C_T)`. It only gives positivity around whatever branch the parent theory already selects. Therefore a hand-added `V(q)=1/2 M_q^2 q^2` would be closure-only unless the selector for `q=0` is derived.",
        "",
        "The next hinge is now exact: derive the covariance-equilibrium selector from metric compatibility, quotient regularity, entropy extremum, or Bianchi/source consistency; otherwise declare the q-sector a disciplined closure rather than a derivation of local GR/Newton.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources),
        "",
        "## q-Stiffness Derivation Audit",
        table(["step_id", "derivation_step", "formula", "result", "proof_status", "valid_for_claim"], derivation),
        "",
        "## Covariance Manifold Selector Gap",
        table(["gap_id", "candidate_selector", "test", "outcome", "reason", "next_evidence_needed", "valid_for_claim"], gaps),
        "",
        "## q Operator Contract",
        table(["contract_id", "requirement", "formula", "status", "missing_inputs", "valid_for_claim"], contract),
        "",
        "## Residual Bound Ledger",
        table(["bound_id", "operator", "bound", "claim_status", "blocked_by", "valid_for_claim"], bounds),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusals),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This is progress with teeth. We can now say what a clean local-GR mechanism would look like: a parent-selected covariance equilibrium `q=0`, plus a positive transverse Hessian giving `M_q^2/Z_q`, plus boundary and observable maps. What we cannot say yet is that the current corpus has selected that manifold. The next target is therefore not another loop; it is the selector theorem or an explicit closure declaration.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["derivation"], derivation_rows())
    write_csv(OUTPUTS["selector_gap"], selector_gap_rows())
    write_csv(OUTPUTS["operator_contract"], operator_contract_rows())
    write_csv(OUTPUTS["residual_bound"], residual_bound_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["derivation"], COPY_TARGETS["queue_derivation"])
    shutil.copyfile(OUTPUTS["selector_gap"], COPY_TARGETS["queue_selector_gap"])
    shutil.copyfile(OUTPUTS["refusal"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["operator_contract"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
