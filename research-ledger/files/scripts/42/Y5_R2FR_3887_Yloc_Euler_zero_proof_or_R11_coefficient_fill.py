from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3887"
BRANCH = "MTS_R2FR_Y5_YLOC_EULER_ZERO_PROOF_OR_R11_COEFFICIENT_FILL_3887"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3887-Y5-R2FR-Yloc-Euler-zero-proof-or-R11-coefficient-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3886_NEXT = OUT / "P8_Y5_R2FR_3886_NEXT_TARGET.csv"
CSV_3886_SELECTOR = OUT / "P8_Y5_R2FR_3886_DOUBLE_ZERO_SELECTOR_DERIVATION_AUDIT.csv"
CSV_3886_FAMILY = OUT / "P8_Y5_R2FR_3886_R11_FAMILY_SELECTOR_OR_FILL_MATRIX.csv"
CSV_3886_COEFS = OUT / "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv"
CSV_3886_GATE = OUT / "P8_Y5_R2FR_3886_LOCAL_GR_DECISION_GATE.csv"
CSV_3886_VALIDATION = OUT / "P8_Y5_BRR545_3886_VALIDATION.csv"
CSV_YLOC_CONTRACT = OUT / "P8_YLOC_NO_LINEAR_SOURCE_PARENT_CONTRACT.csv"
CSV_EXTRA_ENERGY = OUT / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv"
CSV_POSITIVE_NOHAIR = OUT / "P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv"
CSV_YLOC_STATUS = OUT / "P8_local_GR_Yloc_Euler_Hessian_R11_factorization_status.csv"
CSV_LOCAL_ZERO_IMPACT = OUT / "P8_LOCAL_ZERO_BOUNDARY_R11_IMPLICATION_AUDIT.csv"
CSV_LOCAL_ZERO_DECISION = OUT / "P8_LOCAL_ZERO_BOUNDARY_R11_DECISION.csv"
CSV_PARENT_DOUBLE = OUT / "P8_Y5_PARENT_QLOC_1533_PARENT_ACTION_DOUBLE_ZERO_CONTRACT.csv"
CSV_LOCAL_LOCK = OUT / "P8_Y5_BRR545_LOCAL_LOCK_MAP.csv"
CSV_BOUNDARY_FILL = OUT / "P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3887_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3887_YLOC_EULER_ZERO_THEOREM_ATTEMPT.csv",
    "components": OUT / "P8_Y5_R2FR_3887_YLOC_COMPONENT_CLOSURE_MATRIX.csv",
    "clauses": OUT / "P8_Y5_R2FR_3887_PARENT_ACTION_CLAUSE_REQUIREMENTS.csv",
    "fill": OUT / "P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv",
    "gate": OUT / "P8_Y5_R2FR_3887_LOCAL_GR_DECISION_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3887_RUNNER_UPDATE.csv",
    "next": OUT / "P8_Y5_R2FR_3887_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3887_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3887_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3887_00_next", CSV_3886_NEXT, "NEXT3886_0", "3886 selected Yloc Euler-zero target"),
    ("SRC3887_01_selector", CSV_3886_SELECTOR, "DZS3886_6_verdict", "double-zero mechanism requiring Yloc=0"),
    ("SRC3887_02_family", CSV_3886_FAMILY, "projector_domain_stress", "active R11 family selector/fill matrix"),
    ("SRC3887_03_coefficients", CSV_3886_COEFS, "COEF3886_12_R11_total", "executable PPN/R11 coefficient skeleton"),
    ("SRC3887_04_gate", CSV_3886_GATE, "LGG3886_3_Yloc_Euler", "Yloc Euler proof failure gate"),
    ("SRC3887_05_validation", CSV_3886_VALIDATION, "VAL3886_14_mechanism_found", "3886 validation"),
    ("SRC3887_06_no_linear", CSV_YLOC_CONTRACT, "C2_matter_neutrality", "no-linear-source parent contract"),
    ("SRC3887_07_energy_identity", CSV_EXTRA_ENERGY, "E506_scalar_positive_operator", "positive operator energy identity"),
    ("SRC3887_08_nohair", CSV_POSITIVE_NOHAIR, "NH562_1_energy_identity", "source-free no-hair identity"),
    ("SRC3887_09_status", CSV_YLOC_STATUS, "STAT3535_2_next", "prior Yloc Hessian status"),
    ("SRC3887_10_local_zero", CSV_LOCAL_ZERO_IMPACT, "I5_projector_stress_Bianchi", "local zero implication limit"),
    ("SRC3887_11_local_decision", CSV_LOCAL_ZERO_DECISION, "D4_local_GR_promotion", "local GR promotion forbidden from scalar zero alone"),
    ("SRC3887_12_parent_double", CSV_PARENT_DOUBLE, "VAC1533_4_local_lock", "parent local lock clause"),
    ("SRC3887_13_local_lock", CSV_LOCAL_LOCK, "BRL547_0_boundary_alpha3", "local lock coefficient map"),
    ("SRC3887_14_boundary_fill", CSV_BOUNDARY_FILL, "F6_projector_stress", "projector stress retained-debt row"),
]

LOCAL_ACTION = (
    "S_y[A] = -1/2 int_A sqrt(h) [H_AB D_i y^A D^i y^B + M_AB y^A y^B] "
    "+ int_A sqrt(h) J_A y^A + int_boundary B_A y^A"
)
EULER_EQUATION = "-D_i(H_AB D^i y^B) + M_AB y^B = J_A"
ENERGY_IDENTITY = (
    "int_A sqrt(h)[H_AB D_i y^A D^i y^B + M_AB y^A y^B] "
    "= int_A sqrt(h) y^A J_A + int_boundary y^A n_i H_AB D^i y^B"
)
ZERO_THEOREM = (
    "If H_AB is positive on gauge-fixed modes, M_AB is nonnegative with no unsourced zero-mode, "
    "J_A=0, and the boundary term vanishes, then y^A=0 in the compact local exterior; hence Y_loc^A=0 only after residual-lock identifies y^A with the physical residuals."
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
        cells = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(cells) + " |")
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
                "claim_use": "nonclaim_Yloc_Euler_zero_or_coefficient_fill",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        (
            "YZT3887_0_parent_local_sector",
            "Write an honest local auxiliary sector rather than declaring Y_loc=0.",
            LOCAL_ACTION,
            "PARENT_ACTION_INSERTION_CANDIDATE",
            "still a clause until it is tied to the real parent variables",
        ),
        (
            "YZT3887_1_Euler_equation",
            "Varying y^A gives a local elliptic Euler equation in stationary compact domains.",
            EULER_EQUATION,
            "DERIVED_FROM_CANDIDATE_ACTION",
            "requires stationary/elliptic local reduction and gauge fixing",
        ),
        (
            "YZT3887_2_energy_identity",
            "Multiplying by y^A and integrating by parts gives the no-hair identity.",
            ENERGY_IDENTITY,
            "DERIVED_CONDITIONAL_IDENTITY",
            "source and boundary terms are the only escape channels",
        ),
        (
            "YZT3887_3_zero_result",
            "Positive Hessian plus no linear source plus no boundary flux forces the auxiliary local silence fields to vanish.",
            ZERO_THEOREM,
            "CONDITIONAL_EULER_ZERO_THEOREM",
            "does not close if J_A, boundary flux, gauge zero modes, topology, or residual-lock fail",
        ),
        (
            "YZT3887_4_double_zero_link",
            "Once y^A=0 and residual-lock hold, Sigma_loc=G_AB Y^A Y^B has both Sigma_loc=0 and delta Sigma_loc=0, so 3886 R11 terms are locally silent.",
            "y^A=0 and Y_loc^A=y^A_residual => Sigma_loc=0, delta Sigma_loc=0, delta[Sigma_loc c_A O_A]=0",
            "CONDITIONAL_LINK_TO_EH_ONLY_R11",
            "universal R11 factorization remains separate",
        ),
        (
            "YZT3887_5_verdict",
            "3887 derives the strongest clean route so far: an elliptic positive/no-source/no-flux theorem can produce Y_loc=0 without smuggling a plateau axiom.",
            "not a claim: parent insertion, matter neutrality, boundary silence, residual-lock and universal R11 factorization remain unsigned",
            "MECHANISM_ADVANCED_NOT_CLAIMED",
            "next attack should sign no-linear-source/residual-lock or pivot to first coefficient rows",
        ),
    ]
    return [
        {
            "theorem_id": row_id,
            "step": step,
            "math": math,
            "result": result,
            "remaining_failure": failure,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, step, math, result, failure in raw_rows
    ]


def component_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("YLC3887_0_XD_trace", "X_D or chi_D trace-load", "scalar positive operator", "(-Delta_A+m_chi^2)chi_D=J_chi", "J_chi=0; no inner boundary charge; m_chi^2>0", "CONDITIONAL_CLOSEST_TO_ZERO_PROOF", "R10;Gdot;source normalization"),
        ("YLC3887_1_Qcoh_STF", "Qcoh_STF or shear-free coherent tensor", "gauge-fixed tensor positive operator", "L_STF Q_STF=J_STF", "no anisotropic source; positive tensor Hessian; no boundary shear", "CONDITIONAL_BUT_SOURCE_NEUTRALITY_UNSIGNED", "gamma;xi;alpha2"),
        ("YLC3887_2_boundary_flux", "Phi_boundary^i or epsilon_B_flux", "boundary/collar mode", "boundary term y n.H.Dy", "exact no-flux or topological subtraction", "OPEN_BOUNDARY_ESCAPE_CHANNEL", "alpha3;xi;beta;Gdot"),
        ("YLC3887_3_domain_vector", "V_domain^i or preferred-frame marker", "vector Proca/gauge-fixed operator", "(-Delta_A+m_V^2)V_i=J_i", "matter neutrality forbids J_i; m_V^2>0; no harmonic vector", "CONDITIONAL_OPEN_SOURCE_NEUTRALITY", "alpha1;alpha2;alpha3;xi"),
        ("YLC3887_4_source_normalization", "Delta_mu_source", "scalar/source-normalization mode", "L_mu Delta_mu=J_mu", "same Hilbert source forbids J_mu and residual-lock identifies measured mass", "OPEN_RESIDUAL_LOCK", "beta;WEP;GM calibration"),
        ("YLC3887_5_nonlocal_memory", "K_history or memory norm", "positive local kernel/Lyapunov sector", "K_loc history response source-free and decaying", "compact-local reduction and no history injection", "OPEN_NONLOCAL_TAIL", "Gdot;clock/orbital hysteresis"),
        ("YLC3887_6_bulk_X_charge", "q_X or bulk force charge", "massive scalar/vector positive operator", "(-Delta_A+M_X^2)X=J_X", "J_X=0 and source monopole Q_X^H=0", "OPEN_SOURCE_CHARGE", "R10 alpha(lambda);WEP"),
        ("YLC3887_7_projector_stress", "projector/domain stress", "metric-variation residual", "delta_g S_projector or T_extra_munu", "metric-independent/topological projector or retained conserved stress", "NOT_ZEROED_BY_Y_PROOF_ALONE", "zeta_i;gamma;beta;alpha_i"),
        ("YLC3887_8_R11_selector_marker", "non-EH selector marker", "Sigma_loc-selected operator family", "c_A(Y)=cbar_A Sigma_loc+O(Sigma_loc^2)", "parent action factorizes every R11 family through Y", "OPEN_UNIVERSAL_FACTORIZATION", "R11;PPN;R10"),
    ]
    return [
        {
            "component_id": row_id,
            "Yloc_component": component,
            "field_class": field_class,
            "local_Euler_form": euler,
            "zero_conditions": conditions,
            "3887_status": status,
            "observable_risk": risk,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, field_class, euler, conditions, status, risk in raw_rows
    ]


def clause_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("PAC3887_0_true_parent_variables", "Introduce parent variables y^A, not only diagnostics.", "Without independent fields the Euler equation is bookkeeping.", "REQUIRED_UNSIGNED"),
        ("PAC3887_1_even_symmetry", "The compact-local parent sector is even under y^A -> -y^A or has an equivalent selection rule.", "Forbids J_A y^A linear source terms.", "REQUIRED_UNSIGNED"),
        ("PAC3887_2_matter_neutrality", "Matter couples only through g_obs/coframe and same Hilbert source, not linearly to y^A.", "Prevents compact bodies from sourcing preferred-frame/R10 hair.", "REQUIRED_UNSIGNED"),
        ("PAC3887_3_positive_Hessian", "H_AB positive and M_AB nonnegative after gauge/constraint modes are removed.", "Turns zero source into zero field rather than a flat or unstable mode.", "PARTIAL_FROM_ENERGY_IDENTITY"),
        ("PAC3887_4_boundary_no_flux", "Inner/outer collar terms vanish, are fixed topological charges, or are retained as bounded coefficients.", "Closes alpha3/xi/Gdot boundary escape.", "REQUIRED_UNSIGNED"),
        ("PAC3887_5_residual_lock", "The y^A fields equal the actual residuals in the PPN/R10/R11 ledgers.", "Avoids proving zero for a decoy auxiliary field.", "REQUIRED_UNSIGNED"),
        ("PAC3887_6_universal_R11_factorization", "Every active non-EH R11 family is absent, topological, or Sigma_loc-selected.", "Connects Yloc zero to EH-only local exterior.", "REQUIRED_UNSIGNED"),
        ("PAC3887_7_Bianchi_accounting", "Any remaining stress is topological, separately conserved, or explicitly retained in the coefficient vector.", "Keeps local conservation honest.", "REQUIRED_UNSIGNED"),
    ]
    return [
        {
            "clause_id": row_id,
            "required_parent_clause": clause,
            "why_needed": why,
            "status": status,
            "failure_effect": "local_GR_remains_nonclaim" if status != "PARTIAL_FROM_ENERGY_IDENTITY" else "helps_but_does_not_promote",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, why, status in raw_rows
    ]


def fill_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("FILL3887_0_boundary_alpha3", "epsilon_B_flux_abs", "alpha3", "abs(c_B_flux_to_alpha3*epsilon_B_flux_abs) <= 4e-20 or theorem-zero", "boundary no-flux clause fails", "P8_Y5_BRR545_LOCAL_LOCK_MAP.csv:BRL547_0_boundary_alpha3", "FIRST_NUMERIC_FILL_IF_NO_FLUX_FAILS"),
        ("FILL3887_1_gamma_R11", "delta_gamma_R11", "gamma_minus_1", "abs(delta_gamma_R11) <= 2.3e-05 or theorem-zero", "EH-only/R11 factorization fails", "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv:COEF3886_00_delta_gamma_R11", "FILL_WEAK_FIELD_MAP"),
        ("FILL3887_2_beta_source", "delta_beta_source", "beta_minus_1", "abs(B_source/A_source^2 - 1) <= 7.8e-05 or theorem-zero", "source residual-lock fails", "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv:COEF3886_03_delta_beta_source", "FILL_A_SOURCE_B_SOURCE"),
        ("FILL3887_3_alpha_lambda", "alpha(lambda)", "R10 fifth-force", "abs(alpha_predicted(lambda)) <= alpha_bound(lambda)", "bulk-X/source-charge zero fails", "P8_Y5_R2FR_3886_EXECUTABLE_PPN_COEFFICIENT_VECTOR_SKELETON.csv:COEF3886_11_alpha_lambda", "FILL_REAL_BOUND_AND_SOURCE_CHARGE"),
        ("FILL3887_4_Gdot_memory", "partial_t K_history or partial_t epsilon_B", "Gdot/G", "time drift below Gdot/G lock or theorem derivative-zero", "nonlocal memory/no-flux fails", "P8_Y5_BRR545_LOCAL_LOCK_MAP.csv:BRL547_3_boundary_Gdot", "FILL_TIME_PROFILE"),
        ("FILL3887_5_projector_stress", "T_extra_munu_or_c_projector_domain_stress", "zeta_i;gamma;beta;alpha_i", "retained stress vector individually bounded with no cancellation credit", "projector topological proof fails", "P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv:F6_projector_stress", "FILL_STRESS_VECTOR"),
    ]
    return [
        {
            "fill_id": row_id,
            "symbol": symbol,
            "observable": observable,
            "pass_rule": rule,
            "trigger": trigger,
            "source_anchor": anchor,
            "priority": priority,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, observable, rule, trigger, anchor, priority in raw_rows
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("LGG3887_0_double_zero", "3886 double-zero selector", "Sigma_loc and first variation vanish if Yloc=0", "PASS_CONDITIONAL"),
        ("LGG3887_1_Euler_identity", "Yloc Euler/no-hair identity", ENERGY_IDENTITY, "PASS_CONDITIONAL_IDENTITY"),
        ("LGG3887_2_no_linear_source", "J_A=0", "matter neutrality/even selection rule removes linear sources", "FAIL_UNSIGNED"),
        ("LGG3887_3_boundary", "boundary term zero", "inner/outer collar flux vanishes or is topological/retained", "FAIL_UNSIGNED"),
        ("LGG3887_4_residual_lock", "Yloc residual-lock", "auxiliary y^A equals physical residual components in local ledgers", "FAIL_UNSIGNED"),
        ("LGG3887_5_R11_factorization", "universal R11 factorization", "all active non-EH families use Sigma_loc/topological escape", "FAIL_UNSIGNED"),
        ("LGG3887_6_coefficient_pivot", "coefficient fill fallback", "first fallback rows identified for alpha3/gamma/beta/R10/Gdot/projector stress", "PASS_PIVOT_READY_NONCLAIM"),
        ("LGG3887_7_local_GR", "local-GR promotion", "all above gates pass simultaneously", "BLOCKED_NO_CLAIM"),
    ]
    return [
        {
            "gate_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3887_0_energy", "Yloc_energy_identity", "evaluate positive norm = source term + boundary term; theorem-zero only if source and boundary are zero", "IMPLEMENTED_CONDITIONAL_RULE"),
        ("RUNU3887_1_source", "linear_source_guard", "if any J_A row remains unsigned, route that component to coefficient fill rather than local-GR promotion", "NO_SMUGGLED_ZERO"),
        ("RUNU3887_2_boundary", "boundary_guard", "if inner/outer boundary flux is not theorem-zero, keep alpha3/xi/Gdot rows live", "NO_BOUNDARY_SHORTCUT"),
        ("RUNU3887_3_residual_lock", "residual_lock_guard", "do not let auxiliary variables replace physical residuals unless lock row is parent-signed", "NO_DECOY_FIELD"),
        ("RUNU3887_4_next", "next_attack", "sign no-linear-source/residual-lock from quotient-invariant matter action and same Hilbert source, or fill first fallback coefficients", "NEXT_3888"),
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


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3887_0",
            "target_checkpoint": "3888-Y5-R2FR-no-linear-source-and-residual-lock-or-first-coefficient-fill.md",
            "script": "scripts/Y5_R2FR_3888_no_linear_source_and_residual_lock_or_first_coefficient_fill.py",
            "objective": "derive matter neutrality/no-linear-source and residual-lock from the quotient-invariant same-Hilbert-source action; if either fails, fill the first coefficient rows for boundary alpha3, gamma_R11, beta_source, R10 alpha(lambda), Gdot memory and projector stress",
            "why_next": "3887 gives the clean Euler/no-hair theorem; the remaining proof is not the identity, it is whether the parent action really sets J_A=0 and identifies y^A with the physical residuals",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3887_0",
            "branch": BRANCH,
            "summary": "Yloc Euler-zero route advanced to a positive elliptic/no-source/no-flux theorem; no local-GR claim because no-linear-source, boundary silence, residual-lock and universal R11 factorization remain unsigned; coefficient fallback priorities are now explicit",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    components: list[dict[str, object]],
    clauses: list[dict[str, object]],
    fill: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3887 - Yloc Euler-Zero Proof or R11 Coefficient Fill

Generated: `{timestamp}`

## Result

3887 pushes the local-GR branch past "Yloc is missing" and writes the actual theorem route.

Candidate local silence sector:

`{LOCAL_ACTION}`

Euler equation:

`{EULER_EQUATION}`

Energy identity:

`{ENERGY_IDENTITY}`

Conditional theorem:

`{ZERO_THEOREM}`

This is the right kind of route: not a plateau axiom, not a fitted switch, and not "just set it to zero". It is a parent-action/no-hair mechanism. But it is still nonclaim until the parent action signs `J_A=0`, boundary no-flux, residual-lock, and universal R11 factorization.

## Euler-Zero Theorem Attempt

{markdown_table(theorem, ["theorem_id", "step", "math", "result", "remaining_failure"])}

## Yloc Component Closure Matrix

{markdown_table(components, ["component_id", "Yloc_component", "field_class", "local_Euler_form", "zero_conditions", "3887_status", "observable_risk"])}

## Parent Action Clause Requirements

{markdown_table(clauses, ["clause_id", "required_parent_clause", "why_needed", "status", "failure_effect"])}

## Coefficient Fill Pivot

{markdown_table(fill, ["fill_id", "symbol", "observable", "pass_rule", "trigger", "priority"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "requirement", "status", "claim_allowed"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

The grim bit got sharper but better: the algebraic route is no longer vague. If MTS can justify a source-neutral positive local silence sector, the local R11/PPN branch has a clean way to collapse toward EH/GR. If not, the fallback is now concrete: fill alpha3, gamma, beta, R10, Gdot and projector-stress coefficient rows instead of circling the same missing theorem.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3887 YLOC EULER ZERO -->"
    end = "<!-- END 3887 YLOC EULER ZERO -->"
    block = f"""{start}

## 3887 - Yloc Euler-zero/no-hair route

Candidate local sector:

`{LOCAL_ACTION}`

Euler identity:

`{ENERGY_IDENTITY}`

Conditional theorem:

`{ZERO_THEOREM}`

Status: real derivation route advanced. The local silence variable can be produced by a positive elliptic/no-source/no-flux theorem, not by a plateau axiom. Still nonclaim: no-linear-source, matter neutrality, residual-lock, boundary silence, and universal R11 factorization are not yet signed by the parent action.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3887_YLOC_EULER_ZERO_THEOREM_ATTEMPT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3887_YLOC_COMPONENT_CLOSURE_MATRIX.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3887_PARENT_ACTION_CLAUSE_REQUIREMENTS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3887_R11_PPN_COEFFICIENT_FILL_PIVOT.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3887_VALIDATION.csv`

Next gate: `3888`, sign no-linear-source/residual-lock from same-Hilbert-source quotient matter action or fill the first coefficient rows.

<!-- Generated by 3887 at {timestamp} -->
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
    components: list[dict[str, object]],
    clauses: list[dict[str, object]],
    fill: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks.append(("VAL3887_0_sources", "all cited source paths exist and needles are found", resolved == len(sources), f"{resolved}/{len(sources)} sources resolved"))
    checks.append(("VAL3887_1_action", "local parent action candidate is recorded", any("S_y[A]" in str(row["math"]) for row in theorem), "YZT3887_0"))
    checks.append(("VAL3887_2_energy_identity", "energy identity is explicit", any("int_A sqrt(h)" in str(row["math"]) and "boundary" in str(row["math"]) for row in theorem), "YZT3887_2"))
    checks.append(("VAL3887_3_zero_theorem", "zero theorem names no-source/no-flux/positive Hessian", any("J_A=0" in str(row["math"]) and "boundary" in str(row["math"]) for row in theorem), "YZT3887_3"))
    required_components = {"X_D or chi_D trace-load", "Qcoh_STF or shear-free coherent tensor", "Phi_boundary^i or epsilon_B_flux", "V_domain^i or preferred-frame marker", "Delta_mu_source", "K_history or memory norm", "q_X or bulk force charge", "projector/domain stress", "non-EH selector marker"}
    found_components = {str(row["Yloc_component"]) for row in components}
    checks.append(("VAL3887_4_component_coverage", "Yloc closure matrix covers physical residual components", required_components.issubset(found_components), f"{len(found_components)} components"))
    required_clauses = {"PAC3887_1_even_symmetry", "PAC3887_2_matter_neutrality", "PAC3887_4_boundary_no_flux", "PAC3887_5_residual_lock", "PAC3887_6_universal_R11_factorization"}
    found_clauses = {str(row["clause_id"]) for row in clauses}
    checks.append(("VAL3887_5_clause_coverage", "parent action clauses include source neutrality residual lock and factorization", required_clauses.issubset(found_clauses), f"{len(found_clauses)} clauses"))
    required_fill = {"epsilon_B_flux_abs", "delta_gamma_R11", "delta_beta_source", "alpha(lambda)", "partial_t K_history or partial_t epsilon_B", "T_extra_munu_or_c_projector_domain_stress"}
    found_fill = {str(row["symbol"]) for row in fill}
    checks.append(("VAL3887_6_fill_pivot", "coefficient fallback priorities are explicit", required_fill.issubset(found_fill), f"{len(found_fill)} fill rows"))
    checks.append(("VAL3887_7_local_gr_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3887_7_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3887_7"))
    checks.append(("VAL3887_8_all_nonclaim", "all generated analytic rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [theorem, components, clauses, fill, gate, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3887_9_runner_guard", "runner forbids smuggled source zero", any(row["runner_field"] == "linear_source_guard" and "coefficient fill" in str(row["rule"]) for row in runner), "RUNU3887_1_source"))
    checks.append(("VAL3887_10_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "source-neutral positive local silence sector" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3887_11_spine", "spine updated with 3887 block", SPINE_PATH.exists() and "BEGIN 3887 YLOC EULER ZERO" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3887_12_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3887*") if path.is_file() and ("3887-Y5" in path.name or "P8_Y5_R2FR_3887" in path.name or "P8_Y5_BRR545_3887" in path.name)]
    checks.append(("VAL3887_13_formalization_untouched", "no generated 3887 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3887_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3887_15_next_target", "next target attacks no-linear-source/residual-lock or coefficient fill", any("no-linear-source-and-residual-lock" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3888 no-linear-source"))
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
    theorem = theorem_rows(timestamp)
    components = component_rows(timestamp)
    clauses = clause_rows(timestamp)
    fill = fill_rows(timestamp)
    gate = gate_rows(timestamp)
    runner = runner_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["components"], components)
    write_csv(OUTPUTS["clauses"], clauses)
    write_csv(OUTPUTS["fill"], fill)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, components, clauses, fill, gate, runner, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, components, clauses, fill, gate, runner, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_YLOC_EULER_ZERO_CONDITIONAL_THEOREM")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
