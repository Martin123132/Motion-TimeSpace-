from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3699"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_BATH_OBSERVABLE_MAP_AND_SOURCE_SILENCE_FILL_3699"
DOC = ROOT / "3699-Y5-R2FR-parent-bath-observable-map-and-source-silence-fill.md"


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
        ("handoff_3698", RESIDUALS / "P8_Y5_R2FR_3698_NEXT_TARGET.csv", "try to define p_0"),
        ("status_3698", RESIDUALS / "P8_Y5_R2FR_3698_STATUS.csv", "maximum-entropy bath"),
        ("relative_entropy_3698", RESIDUALS / "P8_Y5_R2FR_3698_RELATIVE_ENTROPY_CONSTRUCTION_ROWS.csv", "D_KL"),
        ("source_silence_3698", RESIDUALS / "P8_Y5_R2FR_3698_SOURCE_SILENCE_GATES.csv", "Poynting"),
        ("source_silence_77", FORMALIZATION / "77-sigma-L-source-silence-theorem.md", "The exact `Sigma_L` source-silence theorem is not derived"),
        ("parent_roadmap_82", FORMALIZATION / "82-parent-dynamics-roadmap.md", "make the coarse-graining theorem the upgrade path"),
        ("parent_equations_83", FORMALIZATION / "83-parent-equations-v1.md", "Open-system memory law:"),
        ("coarse_graining_85", FORMALIZATION / "85-coarse-graining-invariants-XB.md", "This file does not prove the coarse-graining theorem."),
        ("scalar_evenness_126", FORMALIZATION / "126-scalar-evenness-origin.md", "positive leakage-frame metric G_AB"),
        ("red_team_06", FORMALIZATION / "06-consistency-red-team.md", "derived local GR/Newton limit"),
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
                "role": "bath observable and source-silence construction input",
            }
        )
    return rows


def bath_distribution_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "BD3699_0_parent_split",
            "microstate split",
            "Phi -> (q(Phi), xi), with q(Phi)=(g_mu_nu, Psi_matter, F_mu_nu or T_EM_mu_nu, theta_local, kappa_GR_calibration) and xi in ker(Dq)",
            "Local tested physics belongs to q; unresolved MTS/bath structure belongs to xi. This prevents leakage variables from rewriting matter, Maxwell, or Newton couplings by notation.",
            "CONSTRUCTIVE_DEFINITION",
            "q(Phi) still needs a final parent action map",
        ),
        (
            "BD3699_1_reference_bath",
            "local fixed bath state",
            "p_0(xi|X_B,q)=argmax_p S[p] subject to <C_i(q,xi)>_p=C_i^loc(q) and z^A=0",
            "This is the parent object 3698 was missing: a maximum-entropy reference distribution at the local GR/Maxwell/Newton fixed point.",
            "DEFINED_AS_PARENT_CONTRACT",
            "measure dmu(xi|X_B,q) and constraints C_i must be sourced",
        ),
        (
            "BD3699_2_leakage_family",
            "horizontal leakage family",
            "p_z(xi|X_B,q)=p_0 exp[z^A Y_A^perp(xi)-W(z;X_B,q)]",
            "Leakage modes are deformations of the bath distribution, not direct deformations of resolved local fields.",
            "CONSTRUCTIVE_DEFINITION",
            "Y_A^perp must be built from raw bath observables and projected against resolved sources",
        ),
        (
            "BD3699_3_entropy_penalty",
            "Fisher penalty",
            "D_KL(p_z||p_0)=0.5 I_AB^perp z^A z^B+O(z^3), I_AB^perp=<Y_A^perp Y_B^perp>_0",
            "This keeps the 3698 positive u_1 route alive with explicit source-silent observables.",
            "CONDITIONAL_DERIVATION",
            "I_AB^perp needs actual parent/bath data for numbers",
        ),
    ]
    return [
        {
            **base(timestamp),
            "bath_id": bath_id,
            "piece": piece,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "open_requirement": open_requirement,
            "claim_allowed": False,
        }
        for bath_id, piece, formula, derivation, status, open_requirement in specs
    ]


def quotient_projection_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "QP3699_0_resolved_scores",
            "resolved source scores",
            "C_i^0 := O_i(q,xi)-<O_i>_0 for O_i in {S_matter density, T_matter^mu_nu, T_EM^mu_nu, S_EM^i, kappa_GR, alpha_fs, theta_clock}",
            "These are the observables leakage is not allowed to shift at first order in local tested systems.",
            "SOURCE_BASIS_DEFINED",
        ),
        (
            "QP3699_1_raw_leakage_scores",
            "raw bath scores",
            "tildeY_A(xi;X_B,q) are candidate unresolved motion/time/space bath deformations in ker(Dq) before source projection",
            "Raw leakage can be broad; the projection step enforces local source silence.",
            "RAW_BASIS_OPEN",
        ),
        (
            "QP3699_2_fisher_projection",
            "source-silent projection",
            "Y_A^perp = tildeY_A - C_i^0 (C^-1)^{ij} <C_j^0 tildeY_A>_0",
            "This is the real mechanism: it subtracts every component of leakage correlated with resolved matter, EM/Poynting, clock, or Newton-coupling scores.",
            "DERIVED_ORTHOGONALIZATION_FORMULA",
        ),
        (
            "QP3699_3_orthogonality",
            "first-order source silence",
            "<C_i^0 Y_A^perp>_0=0 => partial_z <O_i>_z|_0=0",
            "This turns source silence from a verbal axiom into a checkable covariance condition.",
            "FIRST_ORDER_THEOREM_CONDITIONAL",
        ),
        (
            "QP3699_4_second_order_residual",
            "bounded residual",
            "partial_A partial_B <O_i>_z|_0 = <C_i^0 Y_A^perp Y_B^perp>_0 - <C_i^0>_0 I_AB^perp",
            "Even after first-order silence, local tests need a second-order residual bound.",
            "SECOND_ORDER_BOUND_REQUIRED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "projection_id": projection_id,
            "piece": piece,
            "formula": formula,
            "why_it_matters": why_it_matters,
            "status": status,
            "claim_allowed": False,
        }
        for projection_id, piece, formula, why_it_matters, status in specs
    ]


def source_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "SG3699_0_matter",
            "matter/SM source",
            "O_i includes S_matter and T_matter^mu_nu; require <C_matter Y_A^perp>_0=0",
            "ordinary matter follows the quotient metric/action at first order",
            "FIRST_ORDER_SILENT_CONDITIONAL",
        ),
        (
            "SG3699_1_EM_Maxwell",
            "Maxwell stress",
            "O_i includes F_mu_nu or T_EM^mu_nu and alpha_fs; require <C_EM Y_A^perp>_0=0 and partial_z alpha_fs|_0=0",
            "local Maxwell physics is preserved unless a separately bounded EM residual is intentionally tested",
            "FIRST_ORDER_SILENT_CONDITIONAL",
        ),
        (
            "SG3699_2_Poynting",
            "Poynting flux",
            "O_i includes S_EM^i=(E x B)^i/mu_0 as resolved flux; require <C_Poynting_i Y_A^perp>_0=0",
            "Poynting/vector-flow intuition is allowed as resolved stress/flux data, not as an untracked leakage force",
            "RESOLVED_SOURCE_GATE_DEFINED",
        ),
        (
            "SG3699_3_Newton_coupling",
            "Newton/GR coupling calibration",
            "O_i includes kappa_GR=8*pi*G_N/c^4 calibration; require partial_z kappa_GR|_0=0; deviations must be alpha(lambda) residuals",
            "MTS can later try to derive G_N, but local comparisons cannot hide leakage by renormalizing G_N per arena",
            "COUPLING_SILENCE_CONDITIONAL",
        ),
        (
            "SG3699_4_clock",
            "clock/time observable",
            "O_i includes theta_clock or proper-time calibration; require <C_clock Y_A^perp>_0=0",
            "time-sector novelty must not spoil tested local clock dilation at first order",
            "FIRST_ORDER_SILENT_CONDITIONAL",
        ),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "arena": arena,
            "condition": condition,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for gate_id, arena, condition, meaning, status in specs
    ]


def residual_bound_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "RB3699_0_local_observable_residual",
            "Delta O_i(z)=0.5 z^A z^B R_iAB + O(|z|^3), R_iAB=<C_i^0 Y_A^perp Y_B^perp>_0",
            "local residual starts second order after Fisher projection",
            "BOUND_FORM_DERIVED",
        ),
        (
            "RB3699_1_ppn_vector",
            "epsilon_PPN <= ||z||^2 max_i ||R_iAB|| / N_PPN_i + O(||z||^3)",
            "translates source-silence into a PPN residual vector target",
            "RUNNER_INPUT_READY",
        ),
        (
            "RB3699_2_yukawa_link",
            "||z|| <= C_H ||J_y+B_y||/mu_H^2, mu_H^2 >= T_eff lambda_min(I_H^perp) - R_domain - R_source_slope",
            "links the Fisher penalty back to the 3693-3696 local mass-gap chain",
            "CHAIN_CONNECTED_CONDITIONAL",
        ),
        (
            "RB3699_3_claim_requirement",
            "claim requires numeric/sourced p_0, C_i, tildeY_A, I_AB^perp, T_eff, R_iAB, and local test normalizers",
            "prevents the new orthogonality theorem from becoming another closure label",
            "NUMERIC_SOURCE_ROWS_MISSING",
        ),
    ]
    return [
        {
            **base(timestamp),
            "bound_id": bound_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for bound_id, formula, meaning, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3699_0",
            "Use Fisher projection as the default source-silence mechanism.",
            "It directly constructs quotient-null leakage observables by removing all resolved matter/EM/Newton/clock components.",
            "MECHANISM_ADVANCES",
        ),
        (
            "DEC3699_1",
            "Treat Poynting/vector-flow effects as resolved EM stress input unless a separate EM-emergence branch proves otherwise.",
            "This preserves Maxwell locally while still allowing the theory to learn from EM flow structure.",
            "EM_GATE_CLARIFIED",
        ),
        (
            "DEC3699_2",
            "No local-GR/R10/PPN claim yet.",
            "The theorem is first-order and structural; second-order residual tensors and numeric Fisher rows are still missing.",
            "CLAIM_BLOCKED",
        ),
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
        ("CG3699_0_parent_q", "parent quotient map q(Phi) owns local metric/matter/EM/coupling observables", "BLOCKED"),
        ("CG3699_1_measure", "bath measure dmu(xi|X_B,q) and maximum-entropy p_0 are sourced", "BLOCKED"),
        ("CG3699_2_constraints", "resolved constraint basis C_i is complete enough for matter/EM/Poynting/Newton/clock tests", "BLOCKED"),
        ("CG3699_3_raw_leakage", "raw leakage observables tildeY_A are parent-owned", "BLOCKED"),
        ("CG3699_4_fisher_rows", "I_AB^perp and second-order R_iAB are numeric/sourced", "BLOCKED"),
        ("CG3699_5_ppn_r10", "residual vector passes PPN/R10/clock/orbit bounds with sourced normalizers", "BLOCKED"),
        ("CG3699_6_public", "public local-GR/EM/Newton claim allowed", "BLOCKED"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
        }
        for gate_id, requirement, status in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3699_0",
            "status": "FISHER_SOURCE_SILENCE_MECHANISM_DEFINED_FIRST_ORDER_CLAIM_BLOCKED_BY_NUMERIC_PARENT_ROWS",
            "summary": (
                "3699 defines a constructive source-silence mechanism: split Phi into quotient variables q and bath variables xi; define a local maximum-entropy p_0; "
                "build leakage scores Y_A^perp by Fisher-projecting raw bath scores against resolved matter, EM/Poynting, Newton-coupling, and clock scores. "
                "Then partial_z<O_i>|_0=0 follows from covariance orthogonality. This advances the derivation, but second-order residual tensors and numeric parent rows are still required."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3699_0",
            "target_doc": "3700-Y5-R2FR-second-order-source-residual-vector-and-local-test-runner.md",
            "target_script": "scripts/Y5_R2FR_3700_second_order_source_residual_vector_and_local_test_runner.py",
            "objective": "derive the second-order residual vector R_iAB for matter, EM/Poynting, Newton coupling, and clocks; convert it into PPN/R10/clock/orbit bound rows",
            "success_gate": "either bound Delta O_i=O(z^2) tightly enough for local arenas or identify the first source channel that breaks local GR/Maxwell/Newton recovery",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    bath: list[dict[str, object]],
    projection: list[dict[str, object]],
    source_gates: list[dict[str, object]],
    residuals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3699 Y5 R2FR Parent Bath Observable Map And Source Silence Fill",
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
        "- The new mechanism is Fisher source-silence: leakage modes are allowed only after projecting out components correlated with resolved local observables.",
        "- Split parent fields as `Phi -> (q(Phi), xi)`, where `q` owns the tested metric, matter, EM/Maxwell stress, clock, and Newton-coupling data, while `xi` is bath/leakage structure in `ker(Dq)`.",
        "- Define `p_0(xi|X_B,q)` as the local maximum-entropy bath state and `p_z=p_0 exp[z^A Y_A^perp-W]`.",
        "- Build `Y_A^perp = tildeY_A - C_i^0 (C^-1)^{ij} <C_j^0 tildeY_A>_0`.",
        "- This gives `<C_i^0 Y_A^perp>_0=0`, hence `partial_z <O_i>_z|_0=0` for matter, EM/Poynting, Newton coupling, and clocks.",
        "",
        "## What This Actually Moves",
        "",
        "- Source silence is no longer only an axiom: it has a concrete covariance-orthogonalization mechanism.",
        "- Poynting/vector-flow is placed in the resolved EM stress/flux basis, so it can influence the environment/source data without becoming a hidden local-force knob.",
        "- The local branch is still not proved: second-order residuals `R_iAB=<C_i^0 Y_A^perp Y_B^perp>_0` must be bounded next.",
        "",
        "## Bath Distribution Rows",
        "",
    ]
    for row in bath:
        lines.append(f"- `{row['bath_id']}`: `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Quotient Projection Rows", ""])
    for row in projection:
        lines.append(f"- `{row['projection_id']}`: `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Source Gates", ""])
    for row in source_gates:
        lines.append(f"- `{row['gate_id']}`: {row['arena']} | `{row['status']}` | {row['condition']}")
    lines.extend(["", "## Residual Bound Rows", ""])
    for row in residuals:
        lines.append(f"- `{row['bound_id']}`: `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']} | {row['rationale']}")
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
    bath: list[dict[str, object]],
    projection: list[dict[str, object]],
    source_gates: list[dict[str, object]],
    residuals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    timestamp = stamp()
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("sources_exist", "all cited local sources exist", all(bool(row["exists"]) for row in sources), ""))
    checks.append(("needles_found", "all source needles were found", all(bool(row["needle_found"]) for row in sources), ""))
    checks.append(("outputs_exist", "all generated paths exist", all(path.exists() for path in generated_paths), ""))
    csv_paths = [path for path in generated_paths if path.suffix.lower() == ".csv"]
    csv_parse_ok = True
    csv_error = ""
    try:
        for path in csv_paths:
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    projection_by_id = {str(row["projection_id"]): row for row in projection}
    gate_by_id = {str(row["gate_id"]): row for row in source_gates}
    residual_by_id = {str(row["bound_id"]): row for row in residuals}
    checks.append(("projection_formula", "Fisher projection formula is present", "Y_A^perp" in str(projection_by_id["QP3699_2_fisher_projection"]["formula"]) and "C^-1" in str(projection_by_id["QP3699_2_fisher_projection"]["formula"]), ""))
    checks.append(("orthogonality_theorem", "first-order source silence theorem is present", "partial_z" in str(projection_by_id["QP3699_3_orthogonality"]["formula"]) and "<C_i^0 Y_A^perp>_0=0" in str(projection_by_id["QP3699_3_orthogonality"]["formula"]), ""))
    checks.append(("poynting_resolved", "Poynting gate is resolved-source not hidden knob", "Poynting" in str(gate_by_id["SG3699_2_Poynting"]["arena"]) and "RESOLVED_SOURCE_GATE_DEFINED" == gate_by_id["SG3699_2_Poynting"]["status"], ""))
    checks.append(("newton_coupling_gate", "Newton coupling silence gate exists", "kappa_GR" in str(gate_by_id["SG3699_3_Newton_coupling"]["condition"]), ""))
    checks.append(("second_order_bound", "second-order residual bound exists", "Delta O_i" in str(residual_by_id["RB3699_0_local_observable_residual"]["formula"]) and "z^A z^B" in str(residual_by_id["RB3699_0_local_observable_residual"]["formula"]), ""))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3700", "next target advances to second-order residual runner", str(next_target[0]["target_doc"]).startswith("3700-") and "second-order" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core mechanism terms", all(term in doc_text for term in ["Fisher source-silence", "Phi -> (q(Phi), xi)", "Y_A^perp", "partial_z <O_i>_z|_0=0", "Poynting"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3699*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3699 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
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

    sources = source_register(timestamp)
    bath = bath_distribution_rows(timestamp)
    projection = quotient_projection_rows(timestamp)
    source_gates = source_gate_rows(timestamp)
    residuals = residual_bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3699_SOURCE_REGISTER.csv",
        "bath": RESIDUALS / "P8_Y5_R2FR_3699_BATH_DISTRIBUTION_ROWS.csv",
        "projection": RESIDUALS / "P8_Y5_R2FR_3699_QUOTIENT_PROJECTION_ROWS.csv",
        "source_gates": RESIDUALS / "P8_Y5_R2FR_3699_SOURCE_GATE_ROWS.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3699_RESIDUAL_BOUND_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3699_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3699_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3699_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3699_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3699_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["bath"], bath)
    write_csv(outputs["projection"], projection)
    write_csv(outputs["source_gates"], source_gates)
    write_csv(outputs["residuals"], residuals)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, bath, projection, source_gates, residuals, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, bath, projection, source_gates, residuals, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3699 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3699 checkpoint: Fisher source-silence projection defined; second-order residual runner next")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
