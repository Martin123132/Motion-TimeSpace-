from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3711"
BRANCH_ID = "MTS_R2FR_Y5_PN_FACTOR_DECOMPOSITION_KN_RHO_CH_JEFF_SOURCE_BOUND_3711"
DOC = ROOT / "3711-Y5-R2FR-PN-factor-decomposition-KN-rho-CH-Jeff-source-bound.md"

DOC_3710 = ROOT / "3710-Y5-R2FR-one-sided-Fisher-gap-or-PN-fill-and-R10-closure-sensitivity.md"
BUDGET_3710 = RESIDUALS / "P8_Y5_R2FR_3710_FACTOR_BUDGET_ROWS.csv"
NEXT_3710 = RESIDUALS / "P8_Y5_R2FR_3710_NEXT_TARGET.csv"
PARENT_FILL_3709 = RESIDUALS / "P8_Y5_R2FR_3709_PARENT_FILL_ROWS.csv"
DESIGN_3709 = RESIDUALS / "P8_Y5_R2FR_3709_DESIGN_INEQUALITY_ROWS.csv"
LOCAL_SUPPRESSION_3693 = RESIDUALS / "P8_Y5_R2FR_3693_LOCAL_SUPPRESSION_LAW_ROWS.csv"
YUKAWA_3694 = RESIDUALS / "P8_Y5_R2FR_3694_YUKAWA_ARENA_BOUND_RUNNER_ROWS.csv"
RESIDUAL_TENSOR_3700 = RESIDUALS / "P8_Y5_R2FR_3700_RESIDUAL_TENSOR_ROWS.csv"
SOURCE_MEASURE_509 = RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"
KAPPA_3530 = RESIDUALS / "P8_local_GR_kappa_G_Newtonian_gate_status.csv"
DOC_1035 = ROOT / "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md"
DOC_1012 = ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"
DOC_1015 = ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md"
DOC_1038 = ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md"
DOC_1055 = ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3710", DOC_3710, "P_N=K_N*rho_Newton*C_H^2*J_eff^2", "3710 selected P_N source-product side"),
        ("budget_3710", BUDGET_3710, "FB3710_0_private_tightest", "3710 factor budget rows"),
        ("next_3710", NEXT_3710, "PN-factor-decomposition", "3710 declared 3711 target"),
        ("parent_fill_3709", PARENT_FILL_3709, "FILL3709_2_PN_symbolic", "symbolic P_N parent contract"),
        ("design_3709", DESIGN_3709, "DI3709_3_PN_factor_budget", "derived P_N factor inequality"),
        ("local_suppression_3693", LOCAL_SUPPRESSION_3693, "J_y+B_y=0", "exact horizontal silence and local suppression law"),
        ("yukawa_3694", YUKAWA_3694, "alpha_N=K_N C_H", "R10/Newton Yukawa readout schema"),
        ("residual_tensor_3700", RESIDUAL_TENSOR_3700, "z2_bound", "second-order residual and amplitude gate"),
        ("source_measure_509", SOURCE_MEASURE_509, "M_eff[W]", "source measure/flux theorem obstruction"),
        ("kappa_3530", KAPPA_3530, "Hilbert_source_denominator_MHref_ellJ_owner", "Newton/source denominator status"),
        ("doc_1035", DOC_1035, "MISSING_PARENT_NEWTON_MATCH", "K_X/Newton normalization and R10 profile factorization"),
        ("doc_1012", DOC_1012, "same charge sources Poisson/Gauss", "measured-GM/source-normalization owner theorem"),
        ("doc_1015", DOC_1015, "Q_M := H_tau", "topological-Hilbert same-source measure lemma"),
        ("doc_1038", DOC_1038, "MISSING_DCX_OPERATOR", "DC_X/vertical generator obstruction and beta product guard"),
        ("doc_1055", DOC_1055, "PAC1055_4_source_label_forgetting", "matter functor source-label forgetting route"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "role": role,
            "path": str(path),
            "needle": needle,
            "exists": exists,
            "needle_found": needle in text if exists else False,
            "claim_allowed": False,
        })
    return rows


def factor_decomposition_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        {
            "factor_id": "FAC3711_0_KN",
            "symbol": "K_N",
            "appears_in": "P_N=K_N*rho_Newton*C_H^2*J_eff^2",
            "mathematical_role": "dimensionless Newton/R10 readout factor converting the parent horizontal exchange into the standard alpha(lambda) convention",
            "current_best_definition": "K_N is the R10/Newton projection-normalization ratio after dividing the MTS interaction by the measured Newtonian baseline",
            "source_owner_needed": "parent weak-field Green normalization plus R10 harmonic/profile projection in the same Newton denominator",
            "units_status": "dimensionless only after G_N/source-test mass convention is fixed",
            "current_status": "SYMBOLIC_READOUT_FACTOR",
            "principal_blocker": "MISSING_PARENT_NEWTON_MATCH;MISSING_R10_HARMONIC_KERNEL",
            "best_attack_route": "derive the parent quadratic finite-X row and source/test normalization, or keep K_N inside the combined K_N*rho_Newton product",
            "source_evidence": "YBR3694_1_R10_Newton;PROF1035_4_measured_G_calibration;KXF1035_4_total",
        },
        {
            "factor_id": "FAC3711_1_rho_Newton",
            "symbol": "rho_Newton",
            "appears_in": "P_N=K_N*rho_Newton*C_H^2*J_eff^2",
            "mathematical_role": "same-frame Newton/Hilbert source density or charge used by Poisson, orbital acceleration, and R10 source normalization",
            "current_best_definition": "rho_Newton is the observed Hilbert/Noether source measure normalized against M_H_ref and the exterior Newtonian flux",
            "source_owner_needed": "fixed source worldtube, same observed coframe, closed Pi_M J_H flux, and no extra mass/source channels",
            "units_status": "source-density/charge units depend on M_H_ref and G_ref convention",
            "current_status": "SOURCE_DENOMINATOR_CONDITIONAL",
            "principal_blocker": "MISSING_HILBERT_SOURCE_DENOMINATOR;MISSING_M_H_REF;FLUX_CLOSURE_NOT_DERIVED",
            "best_attack_route": "attack Pi_M J_H flux closure/source-measure glue, but do not split rho_Newton from K_N until the denominator is owned",
            "source_evidence": "T509_0_charge_identity_needed;STAT3530_3_next;Y5O1012_7_Newton_Poisson_orbit;SOL1015_1_source_measure",
        },
        {
            "factor_id": "FAC3711_2_CH",
            "symbol": "C_H",
            "appears_in": "P_N=K_N*rho_Newton*C_H^2*J_eff^2",
            "mathematical_role": "operator/Green norm converting horizontal source amplitude into local field-response amplitude",
            "current_best_definition": "C_H bounds the inverse horizontal Hessian/Green response in the local arena after the mass gap Xi_H is chosen",
            "source_owner_needed": "operator domain, horizontal Hessian norm, boundary conditions, and compatibility with mu_H/lambda_H",
            "units_status": "operator units must make C_H*J_eff/mu_H^2 a dimensionless residual amplitude",
            "current_status": "OPERATOR_CONSTANT_DEFINED_NOT_SOURCED",
            "principal_blocker": "MISSING_OPERATOR_DOMAIN_AND_HESSIAN_NORM;MISSING_BOUNDARY_CONDITIONS",
            "best_attack_route": "prove a coercive Green/operator estimate once the local horizontal operator and domain are parent-declared",
            "source_evidence": "SPL3693_1_norm_bound;RT3700_3_amplitude_bound;YBR3694_0_master",
        },
        {
            "factor_id": "FAC3711_3_Jeff",
            "symbol": "J_eff",
            "appears_in": "P_N=K_N*rho_Newton*C_H^2*J_eff^2",
            "mathematical_role": "horizontal source-plus-boundary amplitude J_eff:=||J_y+B_y|| that drives the local residual",
            "current_best_definition": "J_eff is the norm of the nonvertical source current plus retained boundary contribution in the local horizontal sector",
            "source_owner_needed": "parent split of J_y and B_y plus a horizontal-silence theorem or a finite source-norm bound",
            "units_status": "same source-amplitude units as required by C_H so that P_N has m^-4",
            "current_status": "EXACT_ZERO_OR_BOUND_ROUTE_EXISTS_NOT_SIGNED",
            "principal_blocker": "MISSING_HORIZONTAL_SOURCE_CURRENT_AND_BOUNDARY_SILENCE",
            "best_attack_route": "try to prove J_y+B_y=0 from quotient-invariant matter/current descent; fallback to a finite nonclaim amplitude bound",
            "source_evidence": "SPL3693_0_exact_silence;SPL3693_1_norm_bound;RT3700_3_amplitude_bound;PAC1055_4_source_label_forgetting",
        },
    ]
    return [{**base(timestamp), **row, "claim_allowed": False} for row in specs]


def source_trace_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("TRACE3711_0_PN_contract", "all_factors", "FILL3709_2_PN_symbolic", str(PARENT_FILL_3709), "P_N=K_N*rho_Newton*C_H^2*J_eff^2 with J_eff:=||J_y+B_y||", "symbolic contract, not numeric"),
        ("TRACE3711_1_factor_budget", "all_factors", "DI3709_3_PN_factor_budget", str(DESIGN_3709), "K_N*rho_Newton*C_H^2*J_eff^2 <= P_N_max", "derived factor budget"),
        ("TRACE3711_2_R10_KN", "K_N", "YBR3694_1_R10_Newton", str(YUKAWA_3694), "alpha_N=K_N C_H||J_y|| plus projection/source-normalization corrections", "K_N readout appears but needs normalization"),
        ("TRACE3711_3_KN_newton_match", "K_N", "PROF1035_4_measured_G_calibration", str(DOC_1035), "alpha is dimensionless only after dividing by the Newton baseline", "Newton denominator is the real K_N owner"),
        ("TRACE3711_4_rho_source_measure", "rho_Newton", "T509_0_charge_identity_needed", str(SOURCE_MEASURE_509), "M_eff[W]=M_source[W]=integral_S Q_M[tau]", "same source measure condition"),
        ("TRACE3711_5_rho_newton_gate", "rho_Newton", "STAT3530_3_next", str(KAPPA_3530), "Hilbert_source_denominator_MHref_ellJ_owner", "next Newton source denominator target"),
        ("TRACE3711_6_CH_norm", "C_H", "SPL3693_1_norm_bound", str(LOCAL_SUPPRESSION_3693), "A_loc <= (...) C_H ||J_y+B_y||/N_GR + ...", "C_H appears in local suppression law"),
        ("TRACE3711_7_CH_second_order", "C_H", "RT3700_3_amplitude_bound", str(RESIDUAL_TENSOR_3700), "z2_bound := (C_H ||J_y+B_y||/mu_H^2)^2 + ...", "C_H tied to second-order local residual"),
        ("TRACE3711_8_Jeff_zero", "J_eff", "SPL3693_0_exact_silence", str(LOCAL_SUPPRESSION_3693), "J_y+B_y=0", "exact zero route for the source-product"),
        ("TRACE3711_9_Jeff_matter_functor", "J_eff", "PAC1055_4_source_label_forgetting", str(DOC_1055), "gravitational source is total Hilbert matter source with no source-only species prefactors", "candidate route to horizontal/source-label silence"),
        ("TRACE3711_10_DCX_obstruction", "J_eff", "ODC1038_1_DCX_operator", str(DOC_1038), "MISSING_DCX_OPERATOR", "explains why current vertical-generator proof cannot yet kill J_eff"),
    ]
    return [
        {
            **base(timestamp),
            "trace_id": trace_id,
            "factor": factor,
            "source_row_or_clause": source_row,
            "source_path": source_path,
            "quoted_or_paraphrased_content": content,
            "trace_result": result,
            "claim_allowed": False,
        }
        for trace_id, factor, source_row, source_path, content, result in specs
    ]


def theorem_attempt_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "THM3711_0_product_gate",
            "source-product factor law",
            "P_N=K_N*rho_Newton*C_H^2*J_eff^2",
            "If every factor is finite and source-owned, R10/Newton screening reduces to a single product inequality.",
            "DERIVED_CONDITIONAL",
            "factor values/owner rows are still absent",
        ),
        (
            "THM3711_1_Jeff_exact_zero",
            "horizontal silence zero theorem attempt",
            "J_eff:=||J_y+B_y||; if J_y+B_y=0 then J_eff=0 and P_N=0",
            "This would kill the R10 source-product without needing numerical K_N, rho_Newton, or C_H, provided those are finite.",
            "SUFFICIENT_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "need quotient-invariant matter/current descent plus boundary silence B_y=0",
        ),
        (
            "THM3711_2_Jeff_finite_bound",
            "finite amplitude pass law",
            "J_eff <= sqrt(P_N_max/(K_N*rho_Newton*C_H^2))",
            "This is the fallback if exact zero fails: R10 becomes a bounded source-amplitude budget, not a free coefficient.",
            "DERIVED_NONCLAIM_BOUND",
            "requires K_N*rho_Newton*C_H^2 denominator/source product",
        ),
        (
            "THM3711_3_CH_Jeff_product",
            "operator-amplitude product compression",
            "C_H*J_eff <= sqrt(P_N_max/(K_N*rho_Newton))",
            "C_H and J_eff can be attacked as a combined response norm if the operator and current split is convention-dependent.",
            "DERIVED_REPARAMETERIZATION",
            "still needs K_N*rho_Newton source normalization",
        ),
        (
            "THM3711_4_KNrho_composite",
            "Newton denominator composite",
            "K_N*rho_Newton is safer than separately claiming K_N or rho_Newton before the measured-G denominator is parent-owned",
            "This avoids fake progress from convention choices: the quotient that matters experimentally is the normalized source-test product.",
            "DERIVED_GAUGE_OF_ATTACK",
            "same-frame Hilbert source measure and Newton baseline remain unsigned",
        ),
        (
            "THM3711_5_best_next",
            "next theorem target",
            "prove J_y+B_y=0, or derive a finite bound for ||J_y+B_y||",
            "J_eff is the only factor with a true zero route already present in the corpus; that is the sharpest leap forward.",
            "NEXT_TARGET_SELECTED",
            "requires parent current split and boundary/local projection theorem",
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "theorem_name": name,
            "formal_statement": statement,
            "consequence": consequence,
            "status": status,
            "remaining_gap": gap,
            "claim_allowed": False,
        }
        for theorem_id, name, statement, consequence, status, gap in specs
    ]


def factor_budget_rows(timestamp: str, budget_rows_3710: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, source_row in enumerate(budget_rows_3710):
        pn = source_row["P_N_max_eta10_m4"]
        rows.append({
            **base(timestamp),
            "budget_id": f"FB3711_{index}_{source_row['factor_budget_id']}",
            "source_budget_id": source_row["factor_budget_id"],
            "budget_role": source_row["budget_role"],
            "lambda_um": source_row["lambda_um"],
            "Xi_H_clean_m2": source_row["Xi_H_clean_m2"],
            "P_N_max_eta10_m4": pn,
            "J_eff_bound_formula": f"J_eff <= sqrt({pn}/(K_N*rho_Newton*C_H^2))",
            "CH_Jeff_bound_formula": f"C_H*J_eff <= sqrt({pn}/(K_N*rho_Newton))",
            "KNrho_bound_formula": f"K_N*rho_Newton <= {pn}/(C_H^2*J_eff^2)",
            "unit_factor_from_3710": source_row["J_eff_bound_unit_factor"],
            "budget_status": "NONCLAIM_BUDGET_FROM_3710",
            "claim_allowed": False,
        })
    return rows


def priority_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("PRI3711_0_Jeff", "J_eff", 1, "exact-zero theorem or finite source-amplitude bound", "highest", "needs parent current split and B_y boundary silence", "if J_eff=0 then P_N=0 regardless of finite K_N/rho_Newton/C_H"),
        ("PRI3711_1_KNrho", "K_N*rho_Newton", 2, "same Newton denominator/source measure owner", "very_high", "requires Hilbert source worldtube, M_H_ref, Pi_M flux closure", "needed for true Newton/GR reduction and for making alpha(lambda) dimensionless"),
        ("PRI3711_2_CH", "C_H", 3, "coercive Green/operator norm estimate", "high", "requires parent local horizontal operator and boundary domain", "turns local branch into a theorem-bounded response instead of a fit"),
        ("PRI3711_3_KN", "K_N", 4, "R10 harmonic/profile projection", "medium", "requires official R10 kernel/profile and parent source-test charges", "important for R10 scoring but less fundamental than Newton source ownership"),
        ("PRI3711_4_rho", "rho_Newton", 5, "standalone density/source row", "medium", "cannot be isolated cleanly before K_N*rho_Newton denominator is fixed", "do not split from K_N until the observed Newton baseline is owned"),
    ]
    return [
        {
            **base(timestamp),
            "priority_id": priority_id,
            "factor_or_product": factor,
            "priority_rank": rank,
            "best_route": route,
            "local_gr_leverage": leverage,
            "main_hazard": hazard,
            "why_this_rank": reason,
            "claim_allowed": False,
        }
        for priority_id, factor, rank, route, leverage, hazard, reason in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3711_0_factor_split", "The P_N closure is now split into four named factors plus the safer K_N*rho_Newton composite.", "This turns the coupling gap into a small set of exact mathematical targets rather than a vague missing-input pile.", "PN_FACTORS_DECOMPOSED"),
        ("DEC3711_1_no_factor_promoted", "No individual factor is promoted as source-owned yet.", "Every path still depends on either Newton source normalization, local operator ownership, or horizontal current silence.", "NO_CLAIM_PROMOTION"),
        ("DEC3711_2_Jeff_first", "Attack J_eff first.", "J_eff has the unique exact-zero route: J_y+B_y=0 implies P_N=0 and would make R10/local suppression clean if the parent signs it.", "NEXT_ROUTE_SELECTED"),
        ("DEC3711_3_KNrho_composite", "Treat K_N*rho_Newton as the invariant denominator target until measured-G/source normalization is parent-owned.", "Splitting K_N and rho_Newton too early risks convention-chasing rather than deriving Newton.", "DENOMINATOR_GUARD_ADOPTED"),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "status": status,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3711_0_factor_owners", "K_N, rho_Newton, C_H, and J_eff each have source-owned definitions/units in one parent basis"),
        ("CG3711_1_Jeff_zero", "J_y+B_y=0 is derived from parent current descent and boundary silence, not assumed"),
        ("CG3711_2_KNrho_denominator", "K_N*rho_Newton is normalized by the same observed Hilbert/Newton source denominator"),
        ("CG3711_3_CH_operator", "C_H has a theorem-bounded local Green/operator norm on the declared domain"),
        ("CG3711_4_R10_curve", "private candidate R10 curve is replaced by reviewed/official source before public scoring"),
        ("CG3711_5_public", "local GR/Newton/R10 claim allowed"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": "BLOCKED",
            "claim_allowed": False,
        }
        for gate_id, requirement in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3711_0",
            "status": "PN_FACTORS_DECOMPOSED_AND_JEFF_ROUTE_SELECTED_NONCLAIM",
            "summary": (
                "3711 decomposes P_N into K_N, rho_Newton, C_H, and J_eff, keeps all factors nonclaim, "
                "and selects J_eff as the next derivation target because J_y+B_y=0 would force P_N=0 while a finite J_eff bound still gives executable R10 budgets."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3711_0",
            "target_doc": "3712-Y5-R2FR-Jeff-zero-or-finite-bound-horizontal-source-amplitude.md",
            "target_script": "scripts/Y5_R2FR_3712_Jeff_zero_or_finite_bound_horizontal_source_amplitude.py",
            "objective": "try to prove J_y+B_y=0 from parent current descent/boundary silence, or derive a finite J_eff bound that can feed the 3710/3711 P_N budgets",
            "success_gate": "J_eff receives either a parent-signed zero theorem or a retained finite source-amplitude bound row with units and source path, while all claims remain blocked until K_N*rho_Newton and C_H are owned",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    factors: list[dict[str, object]],
    traces: list[dict[str, object]],
    theorems: list[dict[str, object]],
    budgets: list[dict[str, object]],
    priorities: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3711 Y5 R2FR P_N Factor Decomposition K_N rho_Newton C_H J_eff Source Bound",
        "",
        "Private checkpoint. No GitHub action. No public claim.",
        "",
        "## Status",
        "",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "",
        "- The local coupling gap is now a four-factor product: `P_N=K_N*rho_Newton*C_H^2*J_eff^2`.",
        "- The useful leap is not another scan: if `J_y+B_y=0`, then `J_eff=0` and therefore `P_N=0` for finite `K_N`, `rho_Newton`, and `C_H`.",
        "- If exact silence fails, the fallback is still sharp: `J_eff <= sqrt(P_N_max/(K_N*rho_Newton*C_H^2))`.",
        "- `K_N*rho_Newton` should be treated as one denominator target until the measured-G/Newton source normalization is parent-owned.",
        "- `valid_for_claim=false`: this is a derivation route and budget ledger, not a local-GR/R10 pass.",
        "",
        "## Factor Decomposition",
        "",
    ]
    for row in factors:
        lines.append(f"- `{row['factor_id']}` `{row['symbol']}`: {row['current_status']} | blocker `{row['principal_blocker']}` | route: {row['best_attack_route']}")
    lines.extend(["", "## Theorem Attempts", ""])
    for row in theorems:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: `{row['formal_statement']}` | {row['consequence']}")
    lines.extend(["", "## Budget Rows", ""])
    for row in budgets:
        lines.append(f"- `{row['budget_id']}` `{row['budget_role']}`: P_N_max={row['P_N_max_eta10_m4']} m^-4; {row['J_eff_bound_formula']}")
    lines.extend(["", "## Priority Decision", ""])
    for row in priorities:
        lines.append(f"- rank {row['priority_rank']} `{row['factor_or_product']}`: {row['best_route']} | {row['why_this_rank']}")
    lines.extend(["", "## Source Trace", ""])
    for row in traces:
        lines.append(f"- `{row['trace_id']}` `{row['factor']}`: {row['source_row_or_clause']} | {row['trace_result']} | `{row['source_path']}`")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']}")
    lines.extend(["", "## Claim Gates", ""])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: `{row['status']}` | {row['requirement']}")
    lines.extend(["", "## Source Register", ""])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend(["", "## Next Target", ""])
    lines.append(f"- `{next_target[0]['target_doc']}`")
    lines.append(f"- Objective: {next_target[0]['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    generated_paths: list[Path],
    sources: list[dict[str, object]],
    factors: list[dict[str, object]],
    traces: list[dict[str, object]],
    theorems: list[dict[str, object]],
    budgets: list[dict[str, object]],
    priorities: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    timestamp = stamp()
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("sources_exist", "all cited local sources exist", all(bool(row["exists"]) for row in sources), ""))
    checks.append(("needles_found", "all source needles found", all(bool(row["needle_found"]) for row in sources), ""))
    checks.append(("outputs_exist", "all generated paths exist", all(path.exists() for path in generated_paths), ""))
    csv_parse_ok = True
    csv_error = ""
    try:
        for path in [path for path in generated_paths if path.suffix.lower() == ".csv"]:
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    expected = {"K_N", "rho_Newton", "C_H", "J_eff"}
    checks.append(("four_factors", "all four P_N factors are represented", expected <= {row["symbol"] for row in factors}, ""))
    checks.append(("source_trace", "source trace covers all four factors", expected <= {row["factor"] for row in traces if row["factor"] in expected}, ""))
    theorem_text = "\n".join(str(row["formal_statement"]) for row in theorems)
    checks.append(("zero_route", "J_eff exact-zero theorem route is present", "J_y+B_y=0" in theorem_text and "P_N=0" in theorem_text, ""))
    checks.append(("finite_bound_route", "J_eff finite-bound law is present", "sqrt(P_N_max/(K_N*rho_Newton*C_H^2))" in theorem_text, ""))
    checks.append(("budget_rows", "three 3710 budget branches are carried into 3711", len(budgets) == 3 and all(row["budget_status"] == "NONCLAIM_BUDGET_FROM_3710" for row in budgets), ""))
    checks.append(("priority_Jeff", "J_eff is selected as rank-1 target", any(row["factor_or_product"] == "J_eff" and row["priority_rank"] == 1 for row in priorities), ""))
    checks.append(("KNrho_guard", "K_N*rho_Newton composite denominator guard is present", any(row["factor_or_product"] == "K_N*rho_Newton" for row in priorities) and any("K_N*rho_Newton" in row["decision"] for row in decisions), ""))
    checks.append(("nonclaim_decisions", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3712", "next target advances to J_eff zero-or-bound", str(next_target[0]["target_doc"]).startswith("3712-") and "Jeff" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core 3711 terms", all(term in doc_text for term in ["P_N=K_N*rho_Newton", "J_y+B_y=0", "P_N=0", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3711*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3711 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
    return [
        {
            **base(timestamp),
            "validation_id": check_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": details,
        }
        for check_id, description, passed, details in checks
    ]


def main() -> int:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    budget_rows_3710 = parse_csv(BUDGET_3710)
    sources = source_register(timestamp)
    factors = factor_decomposition_rows(timestamp)
    traces = source_trace_rows(timestamp)
    theorems = theorem_attempt_rows(timestamp)
    budgets = factor_budget_rows(timestamp, budget_rows_3710)
    priorities = priority_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3711_SOURCE_REGISTER.csv",
        "factors": RESIDUALS / "P8_Y5_R2FR_3711_FACTOR_DECOMPOSITION_ROWS.csv",
        "traces": RESIDUALS / "P8_Y5_R2FR_3711_FACTOR_SOURCE_TRACE_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3711_THEOREM_ATTEMPT_ROWS.csv",
        "budgets": RESIDUALS / "P8_Y5_R2FR_3711_FACTOR_BUDGET_ROWS.csv",
        "priorities": RESIDUALS / "P8_Y5_R2FR_3711_FACTOR_PRIORITY_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3711_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3711_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3711_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3711_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3711_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["factors"], factors)
    write_csv(outputs["traces"], traces)
    write_csv(outputs["theorems"], theorems)
    write_csv(outputs["budgets"], budgets)
    write_csv(outputs["priorities"], priorities)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, factors, traces, theorems, budgets, priorities, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, factors, traces, theorems, budgets, priorities, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3711 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3711 checkpoint: P_N factors decomposed and J_eff route selected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
