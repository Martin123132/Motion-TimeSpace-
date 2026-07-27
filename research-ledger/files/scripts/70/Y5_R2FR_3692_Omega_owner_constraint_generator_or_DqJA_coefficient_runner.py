from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3692"
BRANCH_ID = "MTS_R2FR_Y5_OMEGA_OWNER_CONSTRAINT_GENERATOR_OR_DQJA_COEFFICIENT_RUNNER_3692"
DOC = ROOT / "3692-Y5-R2FR-Omega-owner-constraint-generator-or-DqJA-coefficient-runner.md"


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
        ("handoff_3691", RESIDUALS / "P8_Y5_R2FR_3691_NEXT_TARGET.csv", "Omega"),
        ("vertical_3691", RESIDUALS / "P8_Y5_R2FR_3691_VERTICAL_QMAP_GATE_ROWS.csv", "Dq[e_A]=0"),
        ("orthogonality_3691", RESIDUALS / "P8_Y5_R2FR_3691_SOURCE_ORTHOGONALITY_ROWS.csv", "delta_Z S_matter"),
        ("coefficients_3691", RESIDUALS / "P8_Y5_R2FR_3691_JA_COEFFICIENT_ACQUISITION_ROWS.csv", "Dq_Z_norm"),
        ("dcdagger_3631", RESIDUALS / "P8_Y5_R2FR_3631_DCDAGGER_VERTICAL_GENERATOR_MAP.csv", "Omega_flat"),
        ("vertical_3631", RESIDUALS / "P8_Y5_R2FR_3631_VERTICAL_GENERATOR_TEST.csv", "VGT3631_4_verdict"),
        ("source_identity_2642", RESIDUALS / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_PROOF_ATTEMPT.csv", "SCI2642_1_JH_descent"),
        ("leak_bound_2643", RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_DQZ_JH_LEAK_BOUND_ROWS.csv", "Dq_Z_norm"),
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
                "role": "input contract/proof dependency",
            }
        )
    return rows


def omega_contract_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "OOT3692_0_parent_space",
            "parent phase/configuration space",
            "Phi carries presymplectic form Omega=dTheta plus first-class constraints C_a(Phi)=0",
            "Omega, Theta, C_a, domains and degeneracy/gauge quotient are supplied by one parent action",
            "CONTRACT_FORM_WRITTEN_PARENT_OWNER_MISSING",
            "R_Omega_owner",
        ),
        (
            "OOT3692_1_generator",
            "Hamiltonian/Noether generator",
            "i_{e_epsilon} Omega = delta G[epsilon], G[epsilon]=int_Sigma epsilon^a C_a + int_boundary Q_epsilon",
            "e_epsilon is proper gauge only when boundary charge Q_epsilon is zero, fixed, exact, or intentionally retained as an edge mode",
            "GENERATOR_CONTRACT_DERIVED_BOUNDARY_UNSIGNED",
            "R_boundary_charge",
        ),
        (
            "OOT3692_2_quotient_observable",
            "quotient readout",
            "q:Phi->Q_phys is a Dirac observable: {q,C_a}=0, equivalently Dq[e_epsilon]=0",
            "verticality closes if q is parent-owned and invariant under every proper generator e_epsilon",
            "VERTICALITY_THEOREM_CONDITIONAL",
            "Dq_Z_norm",
        ),
        (
            "OOT3692_3_descent_action",
            "matter/source descent",
            "S_matter+S_source=Sbar[q(Phi),Psi,theta,J_phys] with J_phys also invariant under e_epsilon",
            "delta_e S=0, so source/matter current has no component along pure vertical directions",
            "SOURCE_ORTHOGONALITY_THEOREM_CONDITIONAL",
            "eps_JH_Z_abs+eps_source_current",
        ),
        (
            "OOT3692_4_exact_theorem",
            "exact Omega-owner theorem",
            "If OOT3692_0..3 hold and boundary charge is silent, then e_epsilon=Omega^-1 DCdagger[epsilon] lies in ker(Dq) and J_vertical=0",
            "this proves vertical suppression only for directions genuinely generated by the parent constraint symmetry",
            "EXACT_CONTRACT_DERIVED_NOT_PARENT_SIGNED",
            "R_qmap+R_Zvertical+R_JA",
        ),
        (
            "OOT3692_5_no_magic",
            "anti-smuggling clause",
            "J_A=0 cannot be asserted for every canonical Z^A unless partial_ZA is inside ker(Dq) or is projected onto the vertical subbundle",
            "if Z contains physical source-response directions, those directions need a mass-gap/screening/projection bound instead of a zero theorem",
            "Z_SPLIT_FORCED_BY_THEOREM",
            "R_Zsplit",
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "object": theorem_object,
            "formula": formula,
            "closure_condition": condition,
            "status": status,
            "residual_if_failed": residual,
            "claim_allowed": False,
        }
        for theorem_id, theorem_object, formula, condition, status, residual in specs
    ]


def z_split_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "ZS3692_0_split",
            "vertical-horizontal split",
            "Z^A = V^A_a chi^a + H^A_I y^I",
            "Dq[V_a]=0 and V_a=Omega^-1 delta C_a for proper constraints; H_I spans the complement seen by q/source/readout",
            "SPLIT_LAW_DERIVED",
            "R_Zbasis",
        ),
        (
            "ZS3692_1_vertical_current",
            "pure gauge current",
            "J_chi,a = V^A_a J_A",
            "J_chi,a=0 follows from parent q-descent and proper boundary conditions",
            "CONDITIONAL_ZERO_FOR_VERTICAL_CURRENT",
            "R_Jvertical",
        ),
        (
            "ZS3692_2_horizontal_current",
            "physical response current",
            "J_y,I = H^A_I J_A",
            "J_y,I is not killed by descent; it is allowed to source physical response unless mass/projection/screening suppresses it",
            "HORIZONTAL_CURRENT_REMAINS_LIVE",
            "R_Jhorizontal",
        ),
        (
            "ZS3692_3_local_GR_gate",
            "local GR gate",
            "R_local = M_y L_H^{-1} J_y + N_Dq Dq_H[y] + B_edge + O(y^2)",
            "local GR requires either J_y=0 by an extra parent symmetry, L_H^{-1}J_y locally tiny, or M_y/N_Dq projection silence",
            "Z_SPLIT_REQUIRED_BEFORE_LOCAL_GR_CLAIM",
            "R_local_source_response",
        ),
        (
            "ZS3692_4_interpretation",
            "coupling knot",
            "the coupling is not one missing number; it is the choice of whether canonical Z is gauge, physical response, or mixed",
            "next work must choose/supply the parent Z basis and then score only the horizontal residue",
            "COUPLING_PROBLEM_REDUCED_TO_BASIS_AND_MASS_GAP",
            "R_coupling_basis",
        ),
    ]
    return [
        {
            **base(timestamp),
            "split_id": split_id,
            "piece": piece,
            "formula": formula,
            "derived_law": law,
            "status": status,
            "residual_if_failed": residual,
            "claim_allowed": False,
        }
        for split_id, piece, formula, law, status, residual in specs
    ]


def coefficient_runner_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DQR3692_0_DqV",
            "Dq_V_norm",
            "Dq_V_norm := ||Dq[V]||/||V||",
            "must be zero/theorem-owned for the vertical gauge block",
            "BLOCKED_UNTIL_PARENT_Q_OMEGA_SUPPLIED",
        ),
        (
            "DQR3692_1_DqH",
            "Dq_H_norm",
            "Dq_H_norm := ||Dq[H]||/||H||",
            "measures physical response leakage into observed q/readout",
            "ACQUISITION_ROW_READY_VALUES_MISSING",
        ),
        (
            "DQR3692_2_Jvertical",
            "J_chi",
            "J_chi = V^A_a J_A",
            "zero branch if q-descent plus boundary silence close",
            "CONDITIONAL_ZERO_VALUES_MISSING",
        ),
        (
            "DQR3692_3_Jhorizontal",
            "J_y",
            "J_y = H^A_I J_A",
            "bound through source profile, Pi_M, EM current, clock/WEP/orbital projections",
            "ACQUISITION_ROW_READY_VALUES_MISSING",
        ),
        (
            "DQR3692_4_mass_gap",
            "L_H_inverse",
            "||y|| <= ||L_H^{-1}|| ||J_y|| + boundary + O(J_y^2)",
            "local screening requires sourced mass/gap/domain norm or exact projection silence",
            "MISSING_MASS_GAP_OR_SCREENING_BOUND",
        ),
        (
            "DQR3692_5_arena_score",
            "R_local_horizontal",
            "R_local <= ||M_y||||L_H^{-1}||||J_y|| + ||N_Dq||||Dq_H||||y|| + ||B_edge||",
            "feeds PPN/Newton/R10/clocks/WEP/EM/orbital arenas without claiming pass",
            "SCORING_FORM_READY_NUMERIC_INPUTS_MISSING",
        ),
    ]
    return [
        {
            **base(timestamp),
            "runner_id": runner_id,
            "quantity": quantity,
            "definition": definition,
            "use": runner_use,
            "status": status,
            "valid_for_claim": False,
            "source_required": True,
        }
        for runner_id, quantity, definition, runner_use, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3692_0_vertical", "Dq[e]=0 is theorem-derived but not parent-owned", "BLOCKED"),
        ("CG3692_1_JA_zero", "J_A=0 applies only to vertical block, not to physical horizontal response", "BLOCKED"),
        ("CG3692_2_local_GR", "local GR needs horizontal response suppression/projection after Z split", "BLOCKED"),
        ("CG3692_3_public", "private derivation checkpoint only; no public claim", "BLOCKED"),
    ]
    return [
        {**base(timestamp), "gate_id": gate_id, "gate": gate, "status": status, "claim_allowed": False}
        for gate_id, gate, status in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3692_0",
            "status": "OMEGA_OWNER_CONTRACT_DERIVED_Z_SPLIT_REQUIRED_PARENT_NOT_SIGNED",
            "summary": "The Omega/constraint route gives an exact vertical-current theorem only for true gauge directions; canonical Z must now be split into vertical chi and physical horizontal y before local-GR suppression can be claimed.",
            "claim_allowed": False,
        }
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3692_0",
            "exact theorem",
            "Use Omega-owner constraint generator as the clean route: e=Omega^-1 DCdagger, Dq[e]=0, J_vertical=0.",
            "ADOPT_AS_PARENT_CONTRACT_NOT_AS_CLAIM",
        ),
        (
            "DEC3692_1",
            "forced split",
            "Stop treating all Z components as one thing; split Z=V chi + H y.",
            "NEXT_DERIVATION_REQUIRED",
        ),
        (
            "DEC3692_2",
            "local branch",
            "Do not demand J_y=0 unless extra symmetry exists; derive mass-gap/screening/projection bound for y.",
            "LOCAL_GR_ROUTE_REFINED",
        ),
    ]
    return [
        {**base(timestamp), "decision_id": decision_id, "decision": decision, "rationale": rationale, "status": status}
        for decision_id, decision, rationale, status in specs
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3692_0",
            "target_doc": "3693-Y5-R2FR-vertical-horizontal-Z-split-and-local-mass-gap-suppression.md",
            "target_script": "scripts/Y5_R2FR_3693_vertical_horizontal_Z_split_and_local_mass_gap_suppression.py",
            "objective": "derive the Z=V chi+H y split, prove J_chi=0 under Omega/q descent, then derive or bound ||L_H^{-1}J_y|| and its PPN/Newton/R10/clock/WEP/EM/orbital residuals",
            "success_gate": "either a parent-owned vertical/horizontal split plus local suppression theorem exists, or the local branch is reduced to explicit horizontal coefficient rows with no GR claim",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    omega_rows: list[dict[str, object]],
    split_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3692 - Omega-owner constraint generator or Dq/J_A coefficient runner",
        "",
        "Private checkpoint. No GitHub action. No R10, PPN, local-GR, Newton, EM, WEP, clock, or orbital claim.",
        "",
        "## Status",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Derivation",
        "- Start with a parent phase/configuration space `Phi`, presymplectic form `Omega=dTheta`, and first-class constraints `C_a(Phi)=0`.",
        "- A proper vertical generator must satisfy `i_e Omega = delta G[epsilon]`, with `G[epsilon]=int_Sigma epsilon^a C_a + int_boundary Q_epsilon`.",
        "- The quotient readout must be a Dirac observable: `{q,C_a}=0`, equivalently `Dq[e_epsilon]=0`.",
        "- If matter/source actions descend as `S_matter+S_source=Sbar[q(Phi),Psi,theta,J_phys]`, and boundary charge is silent, then `delta_e S=0` and the vertical source current vanishes.",
        "- This proves only `J_vertical=0`. It does **not** prove `J_A=0` for every canonical `Z^A` unless those `Z^A` directions are the parent vertical directions.",
        "",
        "## Forced Z Split",
        "- The clean law is `Z^A = V^A_a chi^a + H^A_I y^I`.",
        "- Vertical block: `Dq[V_a]=0` and `J_chi,a=V^A_a J_A=0` under the parent Omega/q-descent theorem.",
        "- Horizontal block: `J_y,I=H^A_I J_A` remains physical source response unless an extra symmetry, projection silence, mass gap, or screening mechanism suppresses it.",
        "- Local-GR recovery therefore moves from a fake plateau axiom to a sharper bound: `R_local = M_y L_H^{-1}J_y + N_Dq Dq_H[y] + B_edge + O(y^2)`.",
        "",
        "## What This Means",
        "- The coupling problem is now narrowed: decide whether the live MTS `Z` variables are gauge, physical response, or mixed.",
        "- If mixed, only the gauge block gets a zero theorem; the physical block must be bounded by mass gap/screening/projection data.",
        "- This is progress because it stops the theory from smuggling `J_A=0` and gives the exact next derivation target.",
        "",
        "## Omega Contract Rows",
    ]
    for row in omega_rows:
        lines.append(f"- `{row['theorem_id']}`: {row['object']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Z Split Rows"])
    for row in split_rows:
        lines.append(f"- `{row['split_id']}`: {row['piece']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Dq/J_A Runner Rows"])
    for row in runner_rows:
        lines.append(f"- `{row['runner_id']}`: `{row['quantity']}` | `{row['status']}` | {row['definition']}")
    lines.extend(["", "## Claim Gates"])
    for row in claim_gates:
        lines.append(f"- `{row['gate_id']}`: `{row['status']}` - {row['gate']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` - {row['rationale']}")
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
    omega_rows: list[dict[str, object]],
    split_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
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
    no_leak = not any(FORMALIZATION.rglob("*3692*"))
    omega_contract_ok = any(row_data["theorem_id"] == "OOT3692_4_exact_theorem" and row_data["status"] == "EXACT_CONTRACT_DERIVED_NOT_PARENT_SIGNED" for row_data in omega_rows)
    split_required_ok = any(row_data["split_id"] == "ZS3692_3_local_GR_gate" and "Z_SPLIT_REQUIRED" in row_data["status"] for row_data in split_rows)
    runner_keys = {row_data["runner_id"] for row_data in runner_rows}
    runner_ok = {"DQR3692_0_DqV", "DQR3692_3_Jhorizontal", "DQR3692_4_mass_gap", "DQR3692_5_arena_score"}.issubset(runner_keys)
    gates_blocked = all(row_data["status"] == "BLOCKED" for row_data in claim_gates)
    nonclaim = all(not bool(row_data.get("valid_for_claim")) for table in [sources, omega_rows, split_rows, runner_rows, claim_gates, status, next_target] for row_data in table)
    next_ok = str(next_target[0]["target_doc"]).startswith("3693-") and "mass-gap" in str(next_target[0]["target_doc"])
    doc_ok = all(needle in doc_text for needle in ["Dq[e_epsilon]=0", "Z^A = V^A_a chi^a + H^A_I y^I", "R_local = M_y L_H^{-1}J_y"])

    return [
        row("VAL3692_0_sources_exist", source_ok, "all input source files exist"),
        row("VAL3692_1_needles_found", needles_ok, "all source needles found"),
        row("VAL3692_2_outputs_exist", all(path.exists() for path in generated_paths), "all generated outputs exist"),
        row("VAL3692_3_csv_parse", parsed_ok, "; ".join(parse_details)),
        row("VAL3692_4_omega_contract", omega_contract_ok, "exact Omega-owner contract derived but not parent signed"),
        row("VAL3692_5_z_split_required", split_required_ok, "local GR gate forces vertical/horizontal Z split"),
        row("VAL3692_6_runner_rows", runner_ok, "DqV/Jhorizontal/mass-gap/arena runner rows present"),
        row("VAL3692_7_claim_gates_blocked", gates_blocked, "all claim gates remain blocked"),
        row("VAL3692_8_all_nonclaim", nonclaim, "all tables remain nonclaim"),
        row("VAL3692_9_next_target", next_ok, "3693 mass-gap split target selected"),
        row("VAL3692_10_doc_written", doc_ok, "doc contains theorem, split, and local residual law"),
        row("VAL3692_11_no_formalization_leak", no_leak, "no 3692 files under formalization-workbench"),
    ]


def main() -> int:
    timestamp = stamp()
    sources = source_register(timestamp)
    omega_rows = omega_contract_rows(timestamp)
    split_rows = z_split_rows(timestamp)
    runner_rows = coefficient_runner_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3692_SOURCE_REGISTER.csv",
        "omega": RESIDUALS / "P8_Y5_R2FR_3692_OMEGA_OWNER_CONTRACT_ROWS.csv",
        "split": RESIDUALS / "P8_Y5_R2FR_3692_VERTICAL_HORIZONTAL_Z_SPLIT_ROWS.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3692_DQJA_COEFFICIENT_RUNNER_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3692_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3692_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3692_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3692_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3692_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["omega"], omega_rows)
    write_csv(outputs["split"], split_rows)
    write_csv(outputs["runner"], runner_rows)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, omega_rows, split_rows, runner_rows, claim_gates, decisions, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(timestamp, generated_paths, sources, omega_rows, split_rows, runner_rows, claim_gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3692 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3692 checkpoint: Omega contract derived; Z split and horizontal mass-gap route forced")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
