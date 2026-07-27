from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3693"
BRANCH_ID = "MTS_R2FR_Y5_VERTICAL_HORIZONTAL_Z_SPLIT_AND_LOCAL_MASS_GAP_SUPPRESSION_3693"
DOC = ROOT / "3693-Y5-R2FR-vertical-horizontal-Z-split-and-local-mass-gap-suppression.md"


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


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3692", RESIDUALS / "P8_Y5_R2FR_3692_NEXT_TARGET.csv", "vertical-horizontal"),
        ("split_3692", RESIDUALS / "P8_Y5_R2FR_3692_VERTICAL_HORIZONTAL_Z_SPLIT_ROWS.csv", "Z^A = V^A_a chi^a + H^A_I y^I"),
        ("runner_3692", RESIDUALS / "P8_Y5_R2FR_3692_DQJA_COEFFICIENT_RUNNER_ROWS.csv", "L_H_inverse"),
        ("omega_3692", RESIDUALS / "P8_Y5_R2FR_3692_OMEGA_OWNER_CONTRACT_ROWS.csv", "Dq[e_epsilon]=0"),
        ("clean_action_3686", ROOT / "3686-Y5-R2FR-GK-q_loc-action-existence-Helmholtz-or-RGK-action-bound-row.md", "S_GK^clean"),
        ("helmholtz_3687", ROOT / "3687-Y5-R2FR-clean-response-action-Helmholtz-matrix-or-DeltaK-bound-row.md", "E_A = -D_mu"),
        ("green_3690", ROOT / "3690-Y5-R2FR-canonical-source-coupling-JA-zero-theorem-or-Green-profile-bound.md", "L_AB Z^B + J_A + B_A = 0"),
        ("arena_3690", RESIDUALS / "P8_Y5_R2FR_3690_JA_ARENA_TEMPLATE_ROWS.csv", "JAR3690_3_Newton_source"),
    ]
    rows = []
    for source_id, path, needle in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                **base(timestamp),
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "input for split/operator/suppression derivation",
            }
        )
    return rows


def split_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "ZST3693_0_field_space",
            "linearized canonical response space",
            "T_Z F = V_Z \u2295 H_Z with V_Z:=im(R_C) and H_Z chosen G-orthogonal to V_Z after gauge fixing",
            "Use the clean action pairing G_AB from the response action to define projectors P_V and P_H on the quotient domain.",
            "FORMAL_SPLIT_DERIVED_PARENT_BASIS_UNSIGNED",
            "R_Zbasis",
        ),
        (
            "ZST3693_1_projectors",
            "projector algebra",
            "P_V^2=P_V, P_H^2=P_H, P_V P_H=0, P_V+P_H=1 on the gauge-fixed response domain",
            "If Omega/q owns V_Z and the gauge slice is regular, this split prevents vertical and physical response terms being mixed by notation.",
            "PROJECTOR_LAW_DERIVED_REGULARITY_UNSIGNED",
            "R_projector",
        ),
        (
            "ZST3693_2_vertical_readout",
            "vertical q silence",
            "Dq[P_V Z]=0 and Dq[Z]=Dq[P_H Z]",
            "All observable q/readout leakage is horizontal unless the parent q map fails to be a Dirac observable.",
            "VERTICAL_DQ_ZERO_CONDITIONAL",
            "Dq_V_norm",
        ),
        (
            "ZST3693_3_vertical_current",
            "vertical source current",
            "J_chi := P_V^T J = 0 under q-descent, source-current descent, and silent/proper boundary charge",
            "This is the recovered exact zero theorem, but only for the gauge block.",
            "JCHI_ZERO_THEOREM_CONDITIONAL",
            "R_Jvertical",
        ),
        (
            "ZST3693_4_horizontal_current",
            "horizontal source current",
            "J_y := P_H^T J is not killed by gauge descent",
            "The physical source-response block must be suppressed by operator coercivity, screening, projection silence, or a new symmetry.",
            "JY_REMAINS_LIVE",
            "R_Jhorizontal",
        ),
    ]
    return [
        {
            **base(timestamp),
            "split_id": split_id,
            "object": object_name,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "residual_if_failed": residual,
            "claim_allowed": False,
        }
        for split_id, object_name, formula, derivation, status, residual in specs
    ]


def horizontal_operator_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "HOP3693_0_full_operator",
            "full response operator",
            "L_AB Z^B := -D_mu(G_AB D^mu Z^B)+M_AB Z^B+O(Z^2)",
            "From the clean response action/Helmholtz branch; it is action-defined if G_AB, M_AB, D_mu and boundary class are parent-owned.",
            "FORMAL_OPERATOR_AVAILABLE_PARENT_OWNER_UNSIGNED",
        ),
        (
            "HOP3693_1_horizontal_operator",
            "horizontal block",
            "L_H := P_H^T L P_H after gauge fixing and boundary-domain restriction",
            "Vertical gauge zero modes are removed before inverse norms are discussed.",
            "HORIZONTAL_OPERATOR_DEFINED",
        ),
        (
            "HOP3693_2_schur_mixing",
            "vertical-horizontal mixing",
            "L_eff,H = L_HH - L_HV L_VV^+ L_VH if the gauge-fixed block has residual algebraic mixing",
            "If the gauge condition kills L_HV or the quotient action is block diagonal, L_eff,H=L_HH; otherwise use Schur complement.",
            "MIXING_ACCOUNTED_NOT_NUMERIC",
        ),
        (
            "HOP3693_3_coercivity",
            "mass gap/coercivity",
            "<y,L_eff,H y> >= kappa_D ||D y||^2 + mu_H^2 ||y||^2 - R_domain ||y||^2",
            "Positive mu_H^2-R_domain gives a bounded inverse on the local domain.",
            "COERCIVITY_CONDITION_DERIVED_NUMERIC_GAP_MISSING",
        ),
        (
            "HOP3693_4_inverse_bound",
            "horizontal Green bound",
            "||y||_X <= C_H ||J_y+B_y||_{X*} + ||y_boundary||_X + O(||J_y||^2)",
            "C_H <= 1/(mu_H^2-R_domain) in the simplest elliptic norm; local arenas may use Yukawa kernel estimates.",
            "GREEN_BOUND_DERIVED_NUMERIC_INPUTS_MISSING",
        ),
    ]
    return [
        {
            **base(timestamp),
            "operator_id": operator_id,
            "object": object_name,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": False,
        }
        for operator_id, object_name, formula, derivation, status in specs
    ]


def suppression_law_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "SPL3693_0_exact_silence",
            "exact horizontal silence",
            "J_y+B_y=0 or M_y=N_Dq=0 on the local arena",
            "R_local=0 up to edge and quadratic terms if horizontal current or horizontal projection is exactly silent.",
            "SUFFICIENT_CONDITION_FORMAL_NOT_SIGNED",
        ),
        (
            "SPL3693_1_norm_bound",
            "operator-norm suppression",
            "A_loc <= (||M_y||+||N_Dq||||Dq_H||) C_H ||J_y+B_y||/N_GR + ||B_edge||/N_GR",
            "This is the main non-smuggled local-GR gate: compare A_loc to each arena tolerance epsilon_A.",
            "LOCAL_SUPPRESSION_BOUND_DERIVED_VALUES_MISSING",
        ),
        (
            "SPL3693_2_yukawa_kernel",
            "massive local kernel",
            "|R_A(r)|/|R_GR(r)| <= |alpha_A| exp(-r/ell_H)(1+r/ell_H)+R_edge_A+R_proj_A",
            "For a massive horizontal mode, ell_H=1/mu_H. This directly interfaces with R10/PPN/orbital bound curves.",
            "YUKAWA_INTERFACE_DERIVED_ALPHA_ELL_VALUES_MISSING",
        ),
        (
            "SPL3693_3_transition_ratio",
            "local/cosmological length separation",
            "ell_H/L_cg <= (r_A/L_cg)/ln(|alpha_A|/epsilon_A) when |alpha_A|>epsilon_A and edge/projection terms are subdominant",
            "This is the concrete ell_tr/L_cg-style gate: local screening is possible only if the local horizontal response length is short enough relative to the tested baseline.",
            "ELL_RATIO_GATE_DERIVED_VALUES_MISSING",
        ),
        (
            "SPL3693_4_environmental_gap",
            "density/arena dependent gap",
            "mu_H^2(local)=lambda_min(G_H^{-1}M_H)[rho_local,theta,J_phys] and mu_H^2(cosmic)=lambda_min(...)[rho_cosmic]",
            "A viable unified branch may keep cosmological/galaxy response long-range while making local response short-range, but only if this dependence is parent-derived.",
            "ENVIRONMENTAL_SCREENING_ROUTE_IDENTIFIED_NOT_CLAIMED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "law_id": law_id,
            "law": law,
            "formula": formula,
            "use": use,
            "status": status,
            "claim_allowed": False,
        }
        for law_id, law, formula, use, status in specs
    ]


def arena_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "ASG3693_0_PPN",
            "PPN gamma/beta/preferred-frame",
            "A_PPN := |Delta gamma|+|Delta beta|+sum_i |Delta alpha_i|+|Delta xi|",
            "A_PPN <= C_PPN[(||M_y||+||N_Dq||||Dq_H||)C_H||J_y||+||B_edge||]",
            "NEEDS_PPN_PROJECTION_NUMBERS",
        ),
        (
            "ASG3693_1_Newton_R10",
            "Newton/R10 short-range",
            "alpha_eff(lambda=ell_H) := K_N (||M_y||+||N_Dq||||Dq_H||) C_H ||J_y||",
            "Pass requires |alpha_eff(lambda)| <= alpha_bound(lambda) using real bound curve rows.",
            "NEEDS_REAL_ALPHA_BOUND_AND_K_N",
        ),
        (
            "ASG3693_2_clocks_WEP_Gdot",
            "clock/WEP/Gdot",
            "A_clock/WEP := K_clock/WEP C_H ||J_y|| + K_Dq Dq_H C_H ||J_y||",
            "Source-coupled horizontal response must not move dimensionless clock ratios, composition dependence, or Gdot above bounds.",
            "NEEDS_SPECIES_AND_CLOCK_PROJECTIONS",
        ),
        (
            "ASG3693_3_EM_Maxwell",
            "Maxwell/EM stress",
            "A_EM := ||Delta T_EM||/||T_EM|| <= K_EM C_H||J_y^EM|| + K_charge |beta_source_alpha|",
            "EM survives if horizontal response either reproduces Maxwell stress covariantly or is projected/screened below precision.",
            "NEEDS_EM_STRESS_AND_CHARGE_NORMALIZATION",
        ),
        (
            "ASG3693_4_orbital",
            "orbital/ephemeris",
            "A_orb := |delta a_r/a_N|+|delta dot_omega|/dot_omega_bound",
            "Use Yukawa or norm-bound residuals at system baseline r_A.",
            "NEEDS_ORBITAL_KERNEL_AND_SOURCE_PROFILE",
        ),
    ]
    return [
        {
            **base(timestamp),
            "arena_id": arena_id,
            "arena": arena,
            "diagnostic": diagnostic,
            "gate": gate,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for arena_id, arena, diagnostic, gate, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3693_0",
            "Adopt split-first local branch",
            "All future local-GR claims must be stated on the horizontal quotient block; vertical zero theorem alone is insufficient.",
            "ADOPTED_FOR_PRIVATE_FRAMEWORK",
        ),
        (
            "DEC3693_1",
            "Best next derivation",
            "Derive or source mu_H^2=lambda_min(G_H^-1 M_H) and its environmental dependence from the parent action.",
            "NEXT_HIGH_VALUE_TARGET",
        ),
        (
            "DEC3693_2",
            "No plateau axiom",
            "The local vacuum plateau is replaced by either exact projection silence or a quantified Green/Yukawa suppression bound.",
            "PLATEAU_AXIOM_AVOIDED",
        ),
    ]
    return [
        {**base(timestamp), "decision_id": decision_id, "decision": decision, "rationale": rationale, "status": status}
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3693_0_vertical_zero", "J_chi=0 is conditional on parent Omega/q/source/boundary descent", "BLOCKED"),
        ("CG3693_1_horizontal_suppression", "J_y suppression needs mu_H, C_H, projections and source norms", "BLOCKED"),
        ("CG3693_2_local_GR", "local GR not claimed until A_loc <= epsilon_A in PPN/Newton/R10/clocks/WEP/EM/orbital arenas", "BLOCKED"),
        ("CG3693_3_public", "private checkpoint; no GitHub/public claim", "BLOCKED"),
    ]
    return [
        {**base(timestamp), "gate_id": gate_id, "gate": gate, "status": status, "claim_allowed": False}
        for gate_id, gate, status in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3693_0",
            "status": "VERTICAL_HORIZONTAL_SPLIT_DERIVED_HORIZONTAL_LOCAL_SUPPRESSION_BOUND_STAGED",
            "summary": "The local branch is no longer a plateau axiom. The vertical block has a conditional zero theorem; the horizontal block has a concrete coercivity/Yukawa suppression gate that can be scored once mu_H, J_y, Dq_H, projections and arena tolerances are sourced.",
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3693_0",
            "target_doc": "3694-Y5-R2FR-horizontal-mass-gap-parent-origin-or-arena-Yukawa-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_3694_horizontal_mass_gap_parent_origin_or_arena_Yukawa_bound_runner.py",
            "objective": "derive mu_H^2=lambda_min(G_H^-1 M_H) from the parent action or convert it into arena-specific Yukawa/nonclaim rows for PPN, Newton/R10, clocks, WEP, EM and orbital tests",
            "success_gate": "parent-derived positive local mass gap/environmental screening exists, or every local arena receives explicit nonclaim alpha/lambda/projection rows",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    split_rows: list[dict[str, object]],
    operator_rows: list[dict[str, object]],
    suppression_rows: list[dict[str, object]],
    arena_rows_data: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3693 - Vertical-horizontal Z split and local mass-gap suppression",
        "",
        "Private checkpoint. No GitHub action. No public local-GR/Newton/R10/PPN/EM claim.",
        "",
        "## Status",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Derivation",
        "- Split the canonical response variable using the clean response-sector pairing: `T_Z F = V_Z \\oplus H_Z`, with `V_Z:=im(R_C)` and `H_Z` the gauge-fixed complement.",
        "- Write `Z^A = V^A_a chi^a + H^A_I y^I`, with projectors `P_V` and `P_H`.",
        "- The Omega/q theorem gives `Dq[P_V Z]=0`; therefore `Dq[Z]=Dq[P_H Z]`.",
        "- If matter/source/boundary data descend through the quotient, `J_chi=P_V^T J=0`; this is the exact zero theorem but only for the vertical gauge block.",
        "- The horizontal current `J_y=P_H^T J` remains physical. It must be killed by extra symmetry, projection silence, or bounded by a mass gap/screening mechanism.",
        "",
        "## Horizontal Operator",
        "- Start from `L_AB Z^B := -D_mu(G_AB D^mu Z^B)+M_AB Z^B+O(Z^2)`.",
        "- Gauge-fix/quotient first, then define `L_H := P_H^T L P_H`; include the Schur complement if vertical-horizontal mixing remains.",
        "- If `<y,L_eff,H y> >= kappa_D ||D y||^2 + mu_H^2 ||y||^2 - R_domain ||y||^2`, then `||y|| <= C_H ||J_y+B_y|| + ||y_boundary|| + O(J_y^2)`.",
        "",
        "## Local Suppression Law",
        "- Main gate: `A_loc <= (||M_y||+||N_Dq||||Dq_H||) C_H ||J_y+B_y||/N_GR + ||B_edge||/N_GR`.",
        "- Massive/Yukawa interface: `|R_A(r)|/|R_GR(r)| <= |alpha_A| exp(-r/ell_H)(1+r/ell_H)+R_edge_A+R_proj_A`, with `ell_H=1/mu_H`.",
        "- Concrete transition ratio: `ell_H/L_cg <= (r_A/L_cg)/ln(|alpha_A|/epsilon_A)` when `|alpha_A|>epsilon_A` and edge/projection terms are subdominant.",
        "",
        "## Why This Matters",
        "- This is the cleanest non-smuggled route to local GR so far: vertical pieces can vanish by theorem; horizontal pieces must be quantitatively screened or projected.",
        "- It keeps the field-theory route alive without pretending the coupling problem has disappeared.",
        "- The next pressure point is `mu_H^2=lambda_min(G_H^-1 M_H)` and whether the parent action derives a local/environmental mass gap.",
        "",
        "## Split Theorem Rows",
    ]
    for row in split_rows:
        lines.append(f"- `{row['split_id']}`: {row['object']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Horizontal Operator Rows"])
    for row in operator_rows:
        lines.append(f"- `{row['operator_id']}`: {row['object']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Suppression Law Rows"])
    for row in suppression_rows:
        lines.append(f"- `{row['law_id']}`: {row['law']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Arena Gates"])
    for row in arena_rows_data:
        lines.append(f"- `{row['arena_id']}`: {row['arena']} | `{row['status']}` | {row['diagnostic']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` - {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in claim_gates:
        lines.append(f"- `{row['gate_id']}`: `{row['status']}` - {row['gate']}")
    lines.extend(["", "## Source Register"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']}, needle_found={row['needle_found']}, path=`{row['path']}`")
    lines.extend(["", "## Next Target"])
    lines.append(f"- `{next_target[0]['target_doc']}`")
    lines.append(f"- Objective: {next_target[0]['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    timestamp: str,
    generated_paths: list[Path],
    sources: list[dict[str, object]],
    split_rows: list[dict[str, object]],
    operator_rows: list[dict[str, object]],
    suppression_rows: list[dict[str, object]],
    arena_rows_data: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    def row(check_id: str, result: bool, detail: str) -> dict[str, object]:
        return {**base(timestamp), "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}

    parsed_ok = True
    parse_details = []
    for path in generated_paths:
        if path.suffix.lower() == ".csv":
            try:
                parse_csv(path)
                parse_details.append(f"{path.name}:ok")
            except Exception as exc:  # noqa: BLE001
                parsed_ok = False
                parse_details.append(f"{path.name}:{exc}")

    doc_text = read_text(DOC) if DOC.exists() else ""
    source_ok = all(bool(source["exists"]) for source in sources)
    needles_ok = all(bool(source["needle_found"]) for source in sources)
    no_leak = not any(FORMALIZATION.rglob("*3693*"))
    split_ok = any(row_data["split_id"] == "ZST3693_3_vertical_current" and "JCHI_ZERO" in row_data["status"] for row_data in split_rows) and any(row_data["split_id"] == "ZST3693_4_horizontal_current" and row_data["status"] == "JY_REMAINS_LIVE" for row_data in split_rows)
    operator_ok = any(row_data["operator_id"] == "HOP3693_3_coercivity" and "mu_H^2" in row_data["formula"] for row_data in operator_rows)
    suppression_ok = any(row_data["law_id"] == "SPL3693_1_norm_bound" and "A_loc" in row_data["formula"] for row_data in suppression_rows) and any(row_data["law_id"] == "SPL3693_3_transition_ratio" and "ell_H/L_cg" in row_data["formula"] for row_data in suppression_rows)
    arena_ok = {row_data["arena_id"] for row_data in arena_rows_data} == {"ASG3693_0_PPN", "ASG3693_1_Newton_R10", "ASG3693_2_clocks_WEP_Gdot", "ASG3693_3_EM_Maxwell", "ASG3693_4_orbital"}
    gates_blocked = all(row_data["status"] == "BLOCKED" for row_data in claim_gates)
    nonclaim = all(
        not bool(row_data.get("valid_for_claim"))
        for table in [sources, split_rows, operator_rows, suppression_rows, arena_rows_data, decisions, claim_gates, status, next_target]
        for row_data in table
    )
    next_ok = str(next_target[0]["target_doc"]).startswith("3694-") and "mass-gap" in str(next_target[0]["target_doc"])
    doc_ok = all(needle in doc_text for needle in ["Z^A = V^A_a chi^a + H^A_I y^I", "A_loc <=", "ell_H/L_cg", "mu_H^2=lambda_min"])

    return [
        row("VAL3693_0_sources_exist", source_ok, "all input source files exist"),
        row("VAL3693_1_needles_found", needles_ok, "all source needles found"),
        row("VAL3693_2_outputs_exist", all(path.exists() for path in generated_paths), "all generated outputs exist"),
        row("VAL3693_3_csv_parse", parsed_ok, "; ".join(parse_details)),
        row("VAL3693_4_split_theorem", split_ok, "vertical zero/horizontal live split recorded"),
        row("VAL3693_5_operator_coercivity", operator_ok, "horizontal mass-gap/coercivity condition recorded"),
        row("VAL3693_6_suppression_laws", suppression_ok, "A_loc and ell_H/L_cg gates recorded"),
        row("VAL3693_7_arena_coverage", arena_ok, "PPN/Newton-R10/clock-WEP-Gdot/EM/orbital arenas covered"),
        row("VAL3693_8_claim_gates_blocked", gates_blocked, "all claim gates remain blocked"),
        row("VAL3693_9_all_nonclaim", nonclaim, "all tables remain nonclaim"),
        row("VAL3693_10_next_target", next_ok, "3694 mass-gap/Yukawa target selected"),
        row("VAL3693_11_doc_written", doc_ok, "doc contains split, local bound, transition ratio and mass-gap target"),
        row("VAL3693_12_no_formalization_leak", no_leak, "no 3693 files under formalization-workbench"),
    ]


def main() -> int:
    timestamp = stamp()
    sources = source_register(timestamp)
    split_rows = split_theorem_rows(timestamp)
    operator_rows = horizontal_operator_rows(timestamp)
    suppression_rows = suppression_law_rows(timestamp)
    arena_rows_data = arena_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3693_SOURCE_REGISTER.csv",
        "split": RESIDUALS / "P8_Y5_R2FR_3693_VERTICAL_HORIZONTAL_SPLIT_THEOREM_ROWS.csv",
        "operator": RESIDUALS / "P8_Y5_R2FR_3693_HORIZONTAL_OPERATOR_ROWS.csv",
        "suppression": RESIDUALS / "P8_Y5_R2FR_3693_LOCAL_SUPPRESSION_LAW_ROWS.csv",
        "arenas": RESIDUALS / "P8_Y5_R2FR_3693_ARENA_SUPPRESSION_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3693_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3693_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3693_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3693_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3693_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["split"], split_rows)
    write_csv(outputs["operator"], operator_rows)
    write_csv(outputs["suppression"], suppression_rows)
    write_csv(outputs["arenas"], arena_rows_data)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, split_rows, operator_rows, suppression_rows, arena_rows_data, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(timestamp, generated_paths, sources, split_rows, operator_rows, suppression_rows, arena_rows_data, decisions, claim_gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3693 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3693 checkpoint: vertical/horizontal split derived; local mass-gap suppression law staged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
