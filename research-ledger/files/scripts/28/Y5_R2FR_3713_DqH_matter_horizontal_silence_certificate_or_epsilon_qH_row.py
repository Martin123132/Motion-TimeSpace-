from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3713"
BRANCH_ID = "MTS_R2FR_Y5_DQH_MATTER_HORIZONTAL_SILENCE_CERTIFICATE_OR_EPSILON_QH_ROW_3713"
DOC = ROOT / "3713-Y5-R2FR-DqH-matter-horizontal-silence-certificate-or-epsilon-qH-row.md"

DOC_3712 = ROOT / "3712-Y5-R2FR-Jeff-zero-or-finite-bound-horizontal-source-amplitude.md"
NEXT_3712 = RESIDUALS / "P8_Y5_R2FR_3712_NEXT_TARGET.csv"
FINITE_3712 = RESIDUALS / "P8_Y5_R2FR_3712_FINITE_BOUND_ROWS.csv"
BUDGET_3712 = RESIDUALS / "P8_Y5_R2FR_3712_BUDGET_MATCH_ROWS.csv"
OBSTRUCTION_3712 = RESIDUALS / "P8_Y5_R2FR_3712_OBSTRUCTION_ROWS.csv"
MPD_1044 = RESIDUALS / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv"
MFS_1045 = RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv"
MMA_955 = RESIDUALS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv"
NSF_953 = RESIDUALS / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv"
NQ_670 = RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv"
DOC_1055 = ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md"
DOC_1038 = ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md"


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
        ("doc_3712", DOC_3712, "Dq_obs P_H=0", "3712 next target and matter silence criterion"),
        ("next_3712", NEXT_3712, "Dq_obs P_H=0", "3712 declared 3713 target"),
        ("finite_3712", FINITE_3712, "T_matter * epsilon_qH", "3712 finite matter-pullback bound"),
        ("budget_3712", BUDGET_3712, "epsilon_geom + T_matter*epsilon_qH", "3712 budget match rows"),
        ("obstruction_3712", OBSTRUCTION_3712, "OBS3712_0_DqH", "3712 obstruction naming epsilon_qH"),
        ("mpd_1044", MPD_1044, "MPD1044_7_exact_theorem_if_signed", "matter pullback exact conditional theorem"),
        ("mfs_1045", MFS_1045, "MFS1045_0_parent_field_quotient", "parent matter functor signature audit"),
        ("mma_955", MMA_955, "MMA955_6_verdict", "minimal matter action source-coupling lemma"),
        ("nsf_953", NSF_953, "NSF953_5_verdict", "source functor label-forgetting theorem attempt"),
        ("nq_670", NQ_670, "NQ670_2_kernel_transfer", "quotient-kernel transfer chain"),
        ("doc_1055", DOC_1055, "PAC1055_2_matter_functor", "parent action matter functor contract"),
        ("doc_1038", DOC_1038, "ODC1038_7_matter_readout", "matter/no-marker descent obstruction"),
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


def chain_rule_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "CR3713_0_matter_descent_setup",
            "S_matter[Phi,Psi,theta]=bar S_matter[q_obs(Phi),Psi,theta]",
            "ordinary matter only sees parent fields through observed quotient/readout q_obs plus fixed representation data theta",
            "CONDITIONAL_SETUP",
        ),
        (
            "CR3713_1_horizontal_variation",
            "delta_H S_matter = <T_q, Dq_obs P_H delta Phi> + <E_Psi,delta_H Psi> + <J_theta,delta_H theta> + boundary",
            "chain rule isolates the only possible horizontal matter source terms",
            "DERIVED_CHAIN_RULE",
        ),
        (
            "CR3713_2_on_shell_fixed_constants",
            "E_Psi=0, delta_H theta=0, and owned gauge/lift boundary terms vanish",
            "ordinary matter equations, fixed constants, and allowed gauge lifts remove non-quotient terms",
            "CONDITIONAL_REDUCTION",
        ),
        (
            "CR3713_3_matter_covector",
            "J_matter = P_H^* Dq_obs^* T_q",
            "the horizontal matter source is exactly the pullback of the observed stress/source covector through Dq_obs P_H",
            "DERIVED_CONDITIONAL_IDENTITY",
        ),
        (
            "CR3713_4_operator_bound",
            "||J_matter|| <= ||T_q|| ||Dq_obs P_H|| := T_matter epsilon_qH",
            "this proves the 3712 matter term bound with epsilon_qH as the operator norm from horizontal fields to observed readout",
            "DERIVED_FINITE_BOUND",
        ),
        (
            "CR3713_5_zero_condition",
            "Dq_obs P_H=0 => epsilon_qH=0 => J_matter=0",
            "matter horizontal silence follows if the local horizontal directions lie inside the quotient kernel",
            "EXACT_ZERO_CONDITION_CONDITIONAL",
        ),
    ]
    return [
        {
            **base(timestamp),
            "chain_id": row_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, formula, meaning, status in specs
    ]


def certificate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "CERT3713_0_qobs_owner",
            "q_obs is parent-owned before local testing",
            "q_obs: Conf_parent -> Q_obs is fixed by the parent action/quotient, not chosen after seeing R10/PPN",
            "MFS1045_0;NQ670_1",
            "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE",
            "MISSING_PARENT_QOBS_OWNER",
        ),
        (
            "CERT3713_1_PH_kernel_selector",
            "local horizontal projector is quotient-silent",
            "im(P_H) subset ker(Dq_obs), equivalently Dq_obs P_H=0",
            "NQ670_2;PAC1055_0",
            "EXACT_IF_SELECTOR_SIGNED",
            "MISSING_PH_KERNEL_SELECTOR",
        ),
        (
            "CERT3713_2_observed_coframe_functor",
            "observed coframe/metric descends through q_obs",
            "e_obs=Obs_e(q_obs(Phi)); g_obs=eta(e_obs,e_obs); D e_obs P_H=0 if Dq_obs P_H=0",
            "MFS1045_1;MPD1044_2",
            "SUFFICIENT_SIGNATURE_NOT_PARENT_SIGNED",
            "MISSING_OBSERVED_COFRAME_FUNCTOR",
        ),
        (
            "CERT3713_3_constants_fixed",
            "ordinary matter constants are fixed representation/superselection data",
            "delta_H theta_A=0 for masses, charges, alpha_EM, clocks, representation labels, and material standards",
            "MFS1045_5;MPD1044_3",
            "CONSTANT_SUPERSELECTION_UNSIGNED",
            "MISSING_CONSTANT_OWNER",
        ),
        (
            "CERT3713_4_matter_lift",
            "matter field lift is on-shell/gauge only",
            "delta_H Psi_A=0 or an owned local Lorentz/diffeomorphism/gauge lift with boundary-only variation",
            "MFS1045_3;MPD1044_4",
            "VERTICAL_LIFT_NOT_PARENT_SIGNED",
            "MISSING_MATTER_LIFT",
        ),
        (
            "CERT3713_5_no_shadow_frame",
            "no hidden matter-frame or material-marker slot",
            "no A_A(X)^2 g_obs, B_A(X), source-only metric, m_A(X), or post-readout material marker enters S_A",
            "MFS1045_4;PAC1055_3",
            "GUARD_WRITTEN_NOT_PARENT_DERIVED",
            "MISSING_NO_SHADOW_FRAME_THEOREM",
        ),
        (
            "CERT3713_6_verdict",
            "matter horizontal silence theorem",
            "CERT3713_0 through CERT3713_5 imply Dq_obs P_H=0 and J_matter=0 for ordinary matter",
            "MPD1044_7;MFS1045_6",
            "CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "ALL_CERTIFICATE_CLAUSES_NOT_PARENT_SIGNED_TOGETHER",
        ),
    ]
    return [
        {
            **base(timestamp),
            "certificate_id": row_id,
            "clause": clause,
            "formal_requirement": requirement,
            "source_clauses": sources,
            "status": status,
            "remaining_gap": gap,
            "claim_allowed": False,
        }
        for row_id, clause, requirement, sources, status, gap in specs
    ]


def epsilon_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "EPS3713_0_epsilon_qH",
            "epsilon_qH",
            "||Dq_obs P_H||_{H->Q}",
            "dimensionless if H and Q norms are fixed; otherwise Q_units/H_units",
            "MISSING_ZERO_THEOREM_OR_OPERATOR_NORM",
            "equals zero only when im(P_H) subset ker(Dq_obs) is parent-signed",
        ),
        (
            "EPS3713_1_Tmatter",
            "T_matter",
            "||delta bar S_matter/delta q_obs||_{Q*}",
            "dual units to q_obs so T_matter*epsilon_qH has J_eff units",
            "MISSING_SAME_FRAME_STRESS_NORM",
            "can be sourced from the observed Hilbert stress/source norm once the same-frame matter sector is owned",
        ),
        (
            "EPS3713_2_Jmatter_bound",
            "J_matter_bound",
            "||J_matter|| <= T_matter*epsilon_qH",
            "same units as J_eff",
            "DERIVED_BOUND_WAITING_FOR_INPUTS",
            "feeds 3712 master J_eff bound",
        ),
        (
            "EPS3713_3_zero_branch",
            "J_matter_zero_branch",
            "epsilon_qH=0 => ||J_matter||=0",
            "same units as J_eff",
            "CONDITIONAL_ZERO_BRANCH_NOT_PROMOTED",
            "requires full DqH certificate",
        ),
    ]
    return [
        {
            **base(timestamp),
            "epsilon_id": row_id,
            "quantity": quantity,
            "formula_or_value": formula,
            "units": units,
            "row_status": status,
            "notes": notes,
            "claim_allowed": False,
        }
        for row_id, quantity, formula, units, status, notes in specs
    ]


def budget_rows(timestamp: str, budget_3712: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, source_row in enumerate(budget_3712):
        right_side = source_row["right_side"]
        rows.append({
            **base(timestamp),
            "budget_id": f"DQH3713_{index}_{source_row['match_id']}",
            "budget_role": source_row["budget_role"],
            "lambda_um": source_row["lambda_um"],
            "P_N_max_eta10_m4": source_row["P_N_max_eta10_m4"],
            "matter_only_pass_condition": f"T_matter*epsilon_qH <= {right_side} - epsilon_geom - epsilon_boundary",
            "zero_branch_result": "if epsilon_qH=0, the matter part contributes zero to this budget",
            "status": "NONCLAIM_EXECUTABLE_MATTER_SUBGATE",
            "claim_allowed": False,
        })
    return rows


def fork_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "FORK3713_0_exact_kernel",
            "exact quotient-kernel branch",
            "prove q_obs and P_H are parent-owned with im(P_H) subset ker(Dq_obs)",
            "sets epsilon_qH=0 and removes J_matter from the local source-product",
            "BEST_ROUTE_BUT_UNSIGNED",
        ),
        (
            "FORK3713_1_finite_leak",
            "finite quotient-leak branch",
            "source or bound epsilon_qH and T_matter",
            "keeps J_matter as T_matter*epsilon_qH in the 3712 budget",
            "FALLBACK_ROUTE_EXECUTABLE",
        ),
        (
            "FORK3713_2_fail_branch",
            "large quotient-leak branch",
            "if T_matter*epsilon_qH exceeds the R10/local budget after geometry and boundary terms, local suppression fails",
            "forces revision of P_H/q_obs/local branch rather than hiding the coupling",
            "FAILURE_RULE_WRITTEN",
        ),
    ]
    return [
        {
            **base(timestamp),
            "fork_id": row_id,
            "branch": branch,
            "condition": condition,
            "consequence": consequence,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, branch, condition, consequence, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3713_0_chain_rule_closed", "The matter term is now reduced to a precise chain-rule object: J_matter=P_H^* Dq_obs^* T_q.", "This is actual structure: the coupling can only enter through Dq_obs P_H, stress/source norm, constants/lift, or boundary terms.", "MATTER_SOURCE_OBJECT_DERIVED"),
        ("DEC3713_1_zero_not_promoted", "Dq_obs P_H=0 is not claimed for current MTS.", "The parent q_obs owner, P_H kernel selector, observed coframe functor, constants, matter lift, and no-shadow-frame theorem are not signed together.", "ZERO_BRANCH_CONDITIONAL_ONLY"),
        ("DEC3713_2_bound_ready", "epsilon_qH and T_matter are staged as explicit nonclaim coefficient rows.", "If the exact kernel proof fails, the finite-leak branch is ready for numerical/source filling without pretending closure.", "BOUND_BRANCH_STAGED"),
        ("DEC3713_3_next", "Next target should construct the P_H kernel selector or write the first finite epsilon_qH coefficient pack.", "That is the shortest path to turning the matter coupling from symbolic debt into a real zero/bound.", "ADVANCE_TO_PH_KERNEL_SELECTOR"),
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
        ("CG3713_0_qobs", "q_obs is parent-owned before local testing"),
        ("CG3713_1_PH", "P_H is parent-owned and im(P_H) subset ker(Dq_obs), or epsilon_qH has a finite source-backed norm"),
        ("CG3713_2_matter", "matter functor, constants, and lift are parent-signed for ordinary species"),
        ("CG3713_3_shadow", "hidden matter-frame/material-marker slots are theorem-forbidden or bounded"),
        ("CG3713_4_budget", "T_matter*epsilon_qH fits inside the 3712 local-source budget with geometry/boundary terms"),
        ("CG3713_5_public", "local GR/Newton/R10 matter-coupling silence claim allowed"),
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
            "status_id": "STATUS3713_0",
            "status": "DQH_MATTER_SILENCE_REDUCED_TO_KERNEL_CERTIFICATE_OR_EPSILON_QH_BOUND_NONCLAIM",
            "summary": (
                "3713 derives J_matter=P_H^*Dq_obs^*T_q and ||J_matter||<=T_matter epsilon_qH. "
                "Exact matter silence follows from im(P_H) subset ker(Dq_obs), but the current corpus only has conditional support, so epsilon_qH/T_matter are retained as explicit nonclaim rows."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3713_0",
            "target_doc": "3714-Y5-R2FR-PH-kernel-selector-owner-or-epsilon-qH-coefficient-pack.md",
            "target_script": "scripts/Y5_R2FR_3714_PH_kernel_selector_owner_or_epsilon_qH_coefficient_pack.py",
            "objective": "construct the parent-owned P_H selector with im(P_H) subset ker(Dq_obs), or produce the finite epsilon_qH coefficient pack with norm convention, source path, and local-arena budget impact",
            "success_gate": "either epsilon_qH=0 is parent-signed for ordinary matter or epsilon_qH becomes a finite nonclaim input row suitable for the 3712 budget runner",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    chain: list[dict[str, object]],
    certificates: list[dict[str, object]],
    epsilons: list[dict[str, object]],
    budgets: list[dict[str, object]],
    forks: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3713 Y5 R2FR DqH Matter Horizontal Silence Certificate Or epsilon_qH Row",
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
        "- The matter-coupling term has been reduced to `J_matter=P_H^* Dq_obs^* T_q`.",
        "- Therefore `||J_matter|| <= T_matter epsilon_qH`, where `epsilon_qH:=||Dq_obs P_H||`.",
        "- Exact matter silence is no longer vague: `im(P_H) subset ker(Dq_obs)` implies `epsilon_qH=0` and `J_matter=0`.",
        "- Current MTS does not yet parent-sign the full certificate, so `epsilon_qH` stays an explicit nonclaim coefficient row.",
        "- `valid_for_claim=false`: this is a derivation/bound gate, not a local-GR/R10 pass.",
        "",
        "## Chain Rule Derivation",
        "",
    ]
    for row in chain:
        lines.append(f"- `{row['chain_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Kernel Certificate", ""])
    for row in certificates:
        lines.append(f"- `{row['certificate_id']}` `{row['status']}`: {row['clause']} | `{row['formal_requirement']}` | gap: {row['remaining_gap']}")
    lines.extend(["", "## epsilon_qH Rows", ""])
    for row in epsilons:
        lines.append(f"- `{row['epsilon_id']}` `{row['quantity']}`: `{row['formula_or_value']}` | {row['row_status']} | {row['notes']}")
    lines.extend(["", "## Matter Budget Subgates", ""])
    for row in budgets:
        lines.append(f"- `{row['budget_id']}` `{row['budget_role']}`: `{row['matter_only_pass_condition']}`")
    lines.extend(["", "## Forks", ""])
    for row in forks:
        lines.append(f"- `{row['fork_id']}` `{row['status']}`: {row['branch']} | {row['condition']} | {row['consequence']}")
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
    chain: list[dict[str, object]],
    certificates: list[dict[str, object]],
    epsilons: list[dict[str, object]],
    budgets: list[dict[str, object]],
    forks: list[dict[str, object]],
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
    chain_text = "\n".join(str(row["formula"]) for row in chain)
    checks.append(("chain_identity", "J_matter pullback identity is present", "J_matter = P_H^* Dq_obs^* T_q" in chain_text, ""))
    checks.append(("bound_identity", "T_matter epsilon_qH bound is present", "T_matter epsilon_qH" in chain_text, ""))
    cert_text = "\n".join(str(row["formal_requirement"]) for row in certificates)
    checks.append(("kernel_certificate", "im(P_H) subset ker(Dq_obs) certificate clause is present", "im(P_H) subset ker(Dq_obs)" in cert_text, ""))
    quantities = {row["quantity"] for row in epsilons}
    checks.append(("epsilon_rows", "epsilon_qH and T_matter rows are staged", {"epsilon_qH", "T_matter", "J_matter_bound"} <= quantities, ""))
    checks.append(("budget_subgates", "three matter budget subgates are written", len(budgets) == 3 and all(row["status"] == "NONCLAIM_EXECUTABLE_MATTER_SUBGATE" for row in budgets), ""))
    fork_status = {row["status"] for row in forks}
    checks.append(("forks", "zero, finite, and fail branches are represented", {"BEST_ROUTE_BUT_UNSIGNED", "FALLBACK_ROUTE_EXECUTABLE", "FAILURE_RULE_WRITTEN"} <= fork_status, ""))
    checks.append(("nonclaim_decisions", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3714", "next target advances to P_H kernel selector", str(next_target[0]["target_doc"]).startswith("3714-") and "PH-kernel" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core 3713 terms", all(term in doc_text for term in ["J_matter=P_H^* Dq_obs^* T_q", "epsilon_qH:=||Dq_obs P_H||", "im(P_H) subset ker(Dq_obs)", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3713*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3713 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
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
    budget_3712 = parse_csv(BUDGET_3712)
    sources = source_register(timestamp)
    chain = chain_rule_rows(timestamp)
    certificates = certificate_rows(timestamp)
    epsilons = epsilon_rows(timestamp)
    budgets = budget_rows(timestamp, budget_3712)
    forks = fork_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3713_SOURCE_REGISTER.csv",
        "chain": RESIDUALS / "P8_Y5_R2FR_3713_CHAIN_RULE_DERIVATION_ROWS.csv",
        "certificates": RESIDUALS / "P8_Y5_R2FR_3713_DQH_ZERO_CERTIFICATE_ROWS.csv",
        "epsilons": RESIDUALS / "P8_Y5_R2FR_3713_EPSILON_QH_ROWS.csv",
        "budgets": RESIDUALS / "P8_Y5_R2FR_3713_MATTER_BUDGET_SUBGATE_ROWS.csv",
        "forks": RESIDUALS / "P8_Y5_R2FR_3713_FORK_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3713_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3713_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3713_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3713_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3713_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["chain"], chain)
    write_csv(outputs["certificates"], certificates)
    write_csv(outputs["epsilons"], epsilons)
    write_csv(outputs["budgets"], budgets)
    write_csv(outputs["forks"], forks)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, chain, certificates, epsilons, budgets, forks, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, chain, certificates, epsilons, budgets, forks, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3713 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3713 checkpoint: DqH matter silence reduced to kernel certificate or epsilon_qH bound")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
