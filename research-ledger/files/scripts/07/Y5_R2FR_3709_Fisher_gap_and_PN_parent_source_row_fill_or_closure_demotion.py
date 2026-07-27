from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3709"
BRANCH_ID = "MTS_R2FR_Y5_FISHER_GAP_AND_PN_PARENT_SOURCE_ROW_FILL_OR_CLOSURE_DEMOTION_3709"
DOC = ROOT / "3709-Y5-R2FR-Fisher-gap-and-PN-parent-source-row-fill-or-closure-demotion.md"

DOC_3708 = ROOT / "3708-Y5-R2FR-u1-parent-relaxation-functional-origin-or-local-mass-gap-closure.md"
DERIVATION_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"
CONTRACT_3708 = RESIDUALS / "P8_Y5_R2FR_3708_PARENT_INPUT_CONTRACT_ROWS.csv"
SCORE_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_SCORE_ROWS.csv"
ANCHOR_3708 = RESIDUALS / "P8_Y5_R2FR_3708_OFFICIAL_ANCHOR_FISHER_GAP_ROWS.csv"
ARENA_3708 = RESIDUALS / "P8_Y5_R2FR_3708_LOCAL_ARENA_GATE_ROWS.csv"
DOC_3707 = ROOT / "3707-Y5-R2FR-PN-lambdaH-parent-source-product-origin-or-R10-score-gate.md"
INPUT_3707 = RESIDUALS / "P8_Y5_R2FR_3707_PARENT_INPUT_AUDIT_ROWS.csv"
OBSTRUCTION_3707 = RESIDUALS / "P8_Y5_R2FR_3707_OBSTRUCTION_ROWS.csv"
MISSING_3703 = RESIDUALS / "P8_Y5_R2FR_3703_MISSING_PARENT_INPUT_ROWS.csv"
READY_3701 = RESIDUALS / "P8_Y5_R2FR_3701_SCORE_READINESS_ROWS.csv"
U1_3698 = RESIDUALS / "P8_Y5_R2FR_3698_U1_CLOSURE_RUNNER_ROWS.csv"


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


def sci(value: float) -> str:
    return f"{value:.12e}"


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3708", DOC_3708, "Xi_H := mu_H^2", "3708 Fisher-gap contract"),
        ("derivation_3708", DERIVATION_3708, "FGD3708_4_R10_rewrite", "Fisher-gap R10 rewrite"),
        ("contract_3708", CONTRACT_3708, "PCI3708_5_PN", "parent input contract ledger"),
        ("score_3708", SCORE_3708, "FGS3708_066", "Fisher-gap score table"),
        ("anchor_3708", ANCHOR_3708, "FGA3708_0_alpha1_anchor_gap", "official alpha=1 anchor row"),
        ("arena_3708", ARENA_3708, "LAG3708_0_R10", "local arena gates in Fisher variables"),
        ("doc_3707", DOC_3707, "P_N <=", "R10 parent score gate"),
        ("input_3707", INPUT_3707, "PIN3707_1_P_N", "P_N parent audit"),
        ("obstruction_3707", OBSTRUCTION_3707, "OBS3707_1_PN", "R10 obstruction ledger"),
        ("missing_3703", MISSING_3703, "MISS3703_0_P_N", "earlier missing input source"),
        ("ready_3701", READY_3701, "READY3701_0_R10", "external/MTS score readiness"),
        ("u1_3698", U1_3698, "u_1_parent", "relative-entropy u1 runner"),
    ]
    rows = []
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


def source_hunt_rows(timestamp: str, contracts_3708: list[dict[str, str]], inputs_3707: list[dict[str, str]]) -> list[dict[str, object]]:
    contract_status = {row["quantity"]: row["status"] for row in contracts_3708}
    input_status = {row["quantity"]: row["status"] for row in inputs_3707}
    rows = [
        {
            **base(timestamp),
            "hunt_id": "HUNT3709_0_XiH",
            "quantity": "Xi_H",
            "candidate_formula": "Xi_H = Theta_H*iota_H - R_loss",
            "source_status": ";".join([
                contract_status.get("I_H^perp", "MISSING_IH_CONTRACT"),
                contract_status.get("T_eff", "MISSING_TEFF_CONTRACT"),
                contract_status.get("R_loss", "MISSING_RLOSS_CONTRACT"),
            ]),
            "verdict": "SYMBOLIC_PARENT_CONTRACT_ONLY_NO_NUMERIC_SOURCE_ROW",
            "next_action": "source Theta_H, I_H^perp eigenvalue and R_loss; use Theta_H name to avoid T_eff stress/coupling collision",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "hunt_id": "HUNT3709_1_PN",
            "quantity": "P_N",
            "candidate_formula": "P_N = K_N*rho_Newton*C_H^2||J_y+B_y||^2",
            "source_status": input_status.get("P_N", "MISSING_PN_AUDIT"),
            "verdict": "SYMBOLIC_SOURCE_PRODUCT_ONLY_NO_NUMERIC_SOURCE_ROW",
            "next_action": "source K_N, rho_Newton normalization, C_H and J_eff:=||J_y+B_y|| in one parent basis",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "hunt_id": "HUNT3709_2_Teff_notation",
            "quantity": "Theta_H",
            "candidate_formula": "Theta_H := Fisher/free-energy conversion scale formerly written T_eff in 3698-3708",
            "source_status": "NOTATION_GUARD_REQUIRED",
            "verdict": "RENAME_IN_NEW_ROWS_TO_AVOID_T_eff_STRESS_SOURCE_COLLISION",
            "next_action": "reserve T_eff/T_matter for stress-energy/effective source weights; use Theta_H for Fisher temperature/action scale",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "hunt_id": "HUNT3709_3_score_readiness",
            "quantity": "R10 score readiness",
            "candidate_formula": "P_N <= 2*(1-eta)*alpha_bound_R10(Xi_H^-1/2)*Xi_H^2",
            "source_status": "CURVE_CANDIDATE_AND_EXTERNAL_ANCHOR_AVAILABLE_MTS_PRODUCTS_MISSING",
            "verdict": "NONCLAIM_SCORE_GATE_READY_NOT_SCORE_READY",
            "next_action": "fill at least Xi_H or P_N source row before running a numerical branch",
            "claim_allowed": False,
        },
    ]
    return rows


def parent_fill_rows(timestamp: str, anchor: dict[str, str], tightest: dict[str, str]) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "fill_id": "FILL3709_0_XiH_symbolic",
            "quantity": "Xi_H",
            "formula_or_value": "Theta_H*iota_H - R_loss",
            "units": "m^-2",
            "row_kind": "symbolic_parent_contract",
            "source_path": str(DERIVATION_3708),
            "missing_before_claim": "Theta_H numeric/source; iota_H eigenvalue/source; R_loss bound/source; units normalization",
            "row_status": "FILLED_SYMBOLIC_NOT_NUMERIC",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "fill_id": "FILL3709_1_XiH_alpha1_anchor_requirement",
            "quantity": "Xi_H_min_for_alpha1_anchor",
            "formula_or_value": anchor["Xi_H_required_clean_m2"],
            "units": "m^-2",
            "row_kind": "source_anchor_requirement",
            "source_path": str(ANCHOR_3708),
            "missing_before_claim": "only constrains lambda_H=38.6um anchor; does not source parent Xi_H",
            "row_status": "ANCHOR_REQUIREMENT_NOT_PARENT_VALUE",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "fill_id": "FILL3709_2_PN_symbolic",
            "quantity": "P_N",
            "formula_or_value": "K_N*rho_Newton*C_H^2*J_eff^2 with J_eff:=||J_y+B_y||",
            "units": "m^-4",
            "row_kind": "symbolic_parent_contract",
            "source_path": str(INPUT_3707),
            "missing_before_claim": "K_N; rho_Newton; C_H; J_eff; same-basis source normalization",
            "row_status": "FILLED_SYMBOLIC_NOT_NUMERIC",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "fill_id": "FILL3709_3_PN_alpha1_anchor_budget",
            "quantity": "P_N_max_eta10_at_alpha1_anchor",
            "formula_or_value": anchor["P_N_max_eta10_m4"],
            "units": "m^-4",
            "row_kind": "source_anchor_budget",
            "source_path": str(ANCHOR_3708),
            "missing_before_claim": "budget only; does not source actual P_N",
            "row_status": "ANCHOR_BUDGET_NOT_PARENT_VALUE",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "fill_id": "FILL3709_4_private_candidate_tightest_budget",
            "quantity": "P_N_max_eta10_private_candidate",
            "formula_or_value": tightest["P_N_max_eta10_m4"],
            "units": "m^-4",
            "row_kind": "private_candidate_curve_budget",
            "source_path": str(SCORE_3708),
            "missing_before_claim": "candidate curve requires review/official table; not public evidence",
            "row_status": "PRIVATE_STRESS_BUDGET_ONLY",
            "claim_allowed": False,
        },
    ]


def design_inequality_rows(timestamp: str, anchor: dict[str, str], tightest: dict[str, str]) -> list[dict[str, object]]:
    alpha_anchor = 1.0
    eta_anchor = 0.1
    xi_anchor = float(anchor["Xi_H_required_clean_m2"])
    pn_anchor = float(anchor["P_N_max_eta10_m4"])
    xi_tight = float(tightest["Xi_H_required_clean_m2"])
    pn_tight = float(tightest["P_N_max_eta10_m4"])
    return [
        {
            **base(timestamp),
            "inequality_id": "DI3709_0_general_R10_pass",
            "scope": "general R10/local Newton",
            "inequality": "P_N <= 2*(1-eta)*alpha_bound_R10(Xi_H^-1/2)*Xi_H^2",
            "equivalent_form": "Xi_H >= sqrt(P_N/(2*(1-eta)*alpha_bound_R10)) at fixed alpha_bound",
            "numeric_anchor": "symbolic",
            "status": "DERIVED_SCORE_CONSTRAINT",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "inequality_id": "DI3709_1_parent_gap_requirement",
            "scope": "Fisher parent gap",
            "inequality": "Theta_H*iota_H >= R_loss + sqrt(P_N/(2*(1-eta)*alpha_bound_R10))",
            "equivalent_form": "source product and correction losses set a lower bound on Fisher stiffness",
            "numeric_anchor": "symbolic",
            "status": "DERIVED_COUPLED_PARENT_REQUIREMENT",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "inequality_id": "DI3709_2_alpha1_anchor_lambda",
            "scope": "official alpha=1 anchor",
            "inequality": "Theta_H*iota_H - R_loss >= 1/(38.6um)^2",
            "equivalent_form": f"Xi_H >= {sci(xi_anchor)} m^-2",
            "numeric_anchor": f"eta={eta_anchor}; alpha={alpha_anchor}; P_N_max_eta10={sci(pn_anchor)} m^-4",
            "status": "SOURCE_ANCHOR_DESIGN_TARGET",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "inequality_id": "DI3709_3_PN_factor_budget",
            "scope": "source product decomposition",
            "inequality": "K_N*rho_Newton*C_H^2*J_eff^2 <= P_N_max",
            "equivalent_form": "J_eff <= sqrt(P_N_max/(K_N*rho_Newton*C_H^2))",
            "numeric_anchor": f"anchor_eta10_P_N_max={sci(pn_anchor)} m^-4; private_tightest_eta10_P_N_max={sci(pn_tight)} m^-4",
            "status": "DERIVED_FACTOR_BUDGET",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "inequality_id": "DI3709_4_private_candidate_pressure",
            "scope": "private candidate curve stress row",
            "inequality": f"Xi_H >= {sci(xi_tight)} m^-2 and P_N <= {sci(pn_tight)} m^-4 at eta=0.1 on the tightest candidate row",
            "equivalent_form": f"lambda_H={tightest['lambda_um']} um candidate only",
            "numeric_anchor": "private_candidate_curve_not_claim",
            "status": "PRIVATE_STRESS_TARGET_ONLY",
            "claim_allowed": False,
        },
    ]


def closure_demotion_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CLOS3709_0_XiH_closure", "Xi_H_closure", "declare Xi_H>0 as a nonclaim closure coefficient only when parent Theta_H/iota_H/R_loss are absent", "feeds R10/PPN/EM/clock/orbit smoke gates; cannot claim derived local GR"),
        ("CLOS3709_1_PN_closure", "P_N_closure", "declare P_N as a nonclaim source-product closure only when K_N/rho_Newton/C_H/J_eff are absent", "tests whether source amplitude could be viable; cannot claim Newton reduction"),
        ("CLOS3709_2_zero_control", "Xi_H_zero_or_low_gap_control", "set Xi_H=0 or too small as a fail/control branch", "checks whether exact projection alone would be needed if screening is absent"),
        ("CLOS3709_3_claim_rule", "promotion_rule", "promote only when Xi_H and P_N have source paths and units, eta is finite/zero, and curve is reviewed", "prevents closure from silently becoming evidence"),
    ]
    return [
        {
            **base(timestamp),
            "closure_id": closure_id,
            "parameter": parameter,
            "closure_rule": closure_rule,
            "use": use,
            "row_status": "EXPLICIT_NONCLAIM_CLOSURE_IF_PARENT_FILL_FAILS",
            "claim_allowed": False,
        }
        for closure_id, parameter, closure_rule, use in specs
    ]


def decision_rows(timestamp: str, anchor: dict[str, str], tightest: dict[str, str]) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "decision_id": "DEC3709_0_symbolic_rows_filled",
            "decision": "Fill symbolic parent rows for Xi_H and P_N, but do not promote them as source-owned values.",
            "rationale": "This preserves derivation structure while refusing to pretend missing coefficients are data.",
            "status": "SYMBOLIC_FILL_NONCLAIM",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3709_1_coupled_design_gate",
            "decision": "Use Theta_H*iota_H >= R_loss + sqrt(P_N/(2*(1-eta)*alpha_bound)) as the next hard design gate.",
            "rationale": "This couples the local Fisher gap to the source product and prevents independent tuning.",
            "status": "DERIVED_GATE_ADOPTED",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3709_2_Teff_renamed",
            "decision": "Use Theta_H for the Fisher/free-energy scale from now on.",
            "rationale": "T_eff is overloaded in the corpus by effective stress/source-weight language; the local gap scale needs a distinct symbol.",
            "status": "NOTATION_GUARD_ADOPTED",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3709_3_closure_demoted",
            "decision": "Until Xi_H and P_N are source-owned, the local mass-gap route is explicit closure for smoke tests only.",
            "rationale": f"At the official anchor Xi_H={anchor['Xi_H_required_clean_m2']} m^-2 and P_N_max_eta10={anchor['P_N_max_eta10_m4']} m^-4 are requirements, not predictions; the private tightest candidate P_N_max is {tightest['P_N_max_eta10_m4']} m^-4.",
            "status": "CLOSURE_ONLY_UNTIL_PARENT_ROWS_EXIST",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3709_4_next_target",
            "decision": "Next attack should fill either the Fisher stiffness side (Theta_H, iota_H, R_loss) or the source-product side (K_N, rho_Newton, C_H, J_eff), not both vaguely.",
            "rationale": "A single sourced side is enough to run meaningful nonclaim sensitivity against the other side.",
            "status": "ADVANCE_TO_ONE_SIDE_FILL",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3709_0_XiH_source", "Theta_H, iota_H and R_loss are source-owned and units-normalized"),
        ("CG3709_1_PN_source", "K_N, rho_Newton, C_H and J_eff are source-owned in one parent basis"),
        ("CG3709_2_coupled_gate", "Theta_H*iota_H >= R_loss + sqrt(P_N/(2*(1-eta)*alpha_bound)) passes with sourced values"),
        ("CG3709_3_eta_curve", "eta boundary/edge values and R10 curve are reviewed/source-owned"),
        ("CG3709_4_arena_residuals", "PPN/EM/clock/WEP/orbit residual tensors are sourced before local-GR wording"),
        ("CG3709_5_public", "public local GR/Newton/Maxwell/R10 claim allowed"),
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


def status_rows(timestamp: str, anchor: dict[str, str], tightest: dict[str, str]) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3709_0",
            "status": "SYMBOLIC_XIH_PN_ROWS_FILLED_DESIGN_GATE_DERIVED_CLOSURE_DEMOTED",
            "summary": (
                "3709 does not find source-owned numeric Xi_H or P_N rows, so it fills only symbolic parent rows and explicitly demotes the local mass-gap branch to nonclaim closure. "
                "The real advance is the coupled gate Theta_H*iota_H >= R_loss + sqrt(P_N/(2*(1-eta)*alpha_bound)), which prevents tuning Xi_H and P_N independently. "
                f"The official alpha=1 anchor gives Xi_H_min={anchor['Xi_H_required_clean_m2']} m^-2 and P_N_max_eta10={anchor['P_N_max_eta10_m4']} m^-4; "
                f"the tightest private candidate row gives lambda={tightest['lambda_um']} um and P_N_max_eta10={tightest['P_N_max_eta10_m4']} m^-4."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3709_0",
            "target_doc": "3710-Y5-R2FR-one-sided-Fisher-gap-or-PN-fill-and-R10-closure-sensitivity.md",
            "target_script": "scripts/Y5_R2FR_3710_one_sided_Fisher_gap_or_PN_fill_and_R10_closure_sensitivity.py",
            "objective": "choose one side of the coupled gate to fill first: either Fisher stiffness rows Theta_H/iota_H/R_loss or source-product rows K_N/rho_Newton/C_H/J_eff; then run a nonclaim R10 closure sensitivity grid against the unfixed side",
            "success_gate": "one side of the Xi_H/P_N gate becomes source-bounded or a closure sensitivity grid proves which missing coefficient range is viable or impossible",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    hunts: list[dict[str, object]],
    fills: list[dict[str, object]],
    inequalities: list[dict[str, object]],
    closures: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3709 Y5 R2FR Fisher Gap And P_N Parent Source Row Fill Or Closure Demotion",
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
        "- No parent-owned numeric `Xi_H` or `P_N` row is found in the current checkpoint chain.",
        "- The work does move forward: `Xi_H` and `P_N` now obey one coupled design gate, not two independent knobs.",
        "- Rename the Fisher/free-energy conversion scale to `Theta_H`; reserve `T_eff` language for stress/source-weight contexts.",
        "- Core gate: `Theta_H*iota_H >= R_loss + sqrt(P_N/(2*(1-eta)*alpha_bound_R10))`.",
        "- Source product budget: `K_N*rho_Newton*C_H^2*J_eff^2 <= P_N_max`, with `J_eff:=||J_y+B_y||`.",
        "- `valid_for_claim=false`: until those rows are source-owned, the mass-gap route is closure-only smoke machinery.",
        "",
        "## Source Hunt",
        "",
    ]
    for row in hunts:
        lines.append(f"- `{row['hunt_id']}` `{row['quantity']}`: `{row['verdict']}` | {row['candidate_formula']}")
    lines.extend(["", "## Filled Rows", ""])
    for row in fills:
        lines.append(f"- `{row['fill_id']}` `{row['quantity']}`: `{row['row_status']}` | {row['formula_or_value']} `{row['units']}`")
    lines.extend(["", "## Design Inequalities", ""])
    for row in inequalities:
        lines.append(f"- `{row['inequality_id']}` `{row['status']}`: {row['inequality']} | {row['equivalent_form']}")
    lines.extend(["", "## Closure Demotion", ""])
    for row in closures:
        lines.append(f"- `{row['closure_id']}` `{row['parameter']}`: {row['closure_rule']}")
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
    hunts: list[dict[str, object]],
    fills: list[dict[str, object]],
    inequalities: list[dict[str, object]],
    closures: list[dict[str, object]],
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
    checks.append(("hunt_verdicts", "hunt rows explicitly refuse numeric source promotion", any(row["quantity"] == "Xi_H" and "NO_NUMERIC" in row["verdict"] for row in hunts) and any(row["quantity"] == "P_N" and "NO_NUMERIC" in row["verdict"] for row in hunts), ""))
    checks.append(("filled_symbolic", "symbolic Xi_H and P_N rows are filled without claims", {"Xi_H", "P_N"} <= {row["quantity"] for row in fills} and all(row["claim_allowed"] is False for row in fills), ""))
    inequality_text = " ".join(str(row["inequality"]) for row in inequalities)
    checks.append(("coupled_gate", "coupled Theta_H/iota_H/P_N inequality is present", "Theta_H*iota_H" in inequality_text and "sqrt(P_N" in inequality_text, ""))
    checks.append(("factor_budget", "P_N factor budget is present", any("K_N*rho_Newton*C_H^2*J_eff^2" in row["inequality"] for row in inequalities), ""))
    checks.append(("closure_nonclaim", "closure rows demote mass-gap route without claims", len(closures) >= 4 and all(row["claim_allowed"] is False for row in closures), ""))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3710", "next target advances to one-sided fill/sensitivity", str(next_target[0]["target_doc"]).startswith("3710-"), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core 3709 terms", all(term in doc_text for term in ["Theta_H*iota_H", "K_N*rho_Newton", "closure-only", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3709*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3709 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
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
    contracts_3708 = parse_csv(CONTRACT_3708)
    inputs_3707 = parse_csv(INPUT_3707)
    anchor = parse_csv(ANCHOR_3708)[0]
    score_rows = parse_csv(SCORE_3708)
    tightest = min(score_rows, key=lambda row: float(row["P_N_max_eta10_m4"]))

    sources = source_register(timestamp)
    hunts = source_hunt_rows(timestamp, contracts_3708, inputs_3707)
    fills = parent_fill_rows(timestamp, anchor, tightest)
    inequalities = design_inequality_rows(timestamp, anchor, tightest)
    closures = closure_demotion_rows(timestamp)
    decisions = decision_rows(timestamp, anchor, tightest)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp, anchor, tightest)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3709_SOURCE_REGISTER.csv",
        "hunts": RESIDUALS / "P8_Y5_R2FR_3709_SOURCE_HUNT_ROWS.csv",
        "fills": RESIDUALS / "P8_Y5_R2FR_3709_PARENT_FILL_ROWS.csv",
        "inequalities": RESIDUALS / "P8_Y5_R2FR_3709_DESIGN_INEQUALITY_ROWS.csv",
        "closures": RESIDUALS / "P8_Y5_R2FR_3709_CLOSURE_DEMOTION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3709_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3709_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3709_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3709_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3709_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["hunts"], hunts)
    write_csv(outputs["fills"], fills)
    write_csv(outputs["inequalities"], inequalities)
    write_csv(outputs["closures"], closures)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, hunts, fills, inequalities, closures, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, hunts, fills, inequalities, closures, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3709 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3709 checkpoint: symbolic Xi_H/P_N fills, coupled design gate, closure demotion")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
