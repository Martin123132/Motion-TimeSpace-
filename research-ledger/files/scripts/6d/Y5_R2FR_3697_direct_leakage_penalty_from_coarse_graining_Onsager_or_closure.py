from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3697"
BRANCH_ID = "MTS_R2FR_Y5_DIRECT_LEAKAGE_PENALTY_FROM_COARSE_GRAINING_ONSAGER_OR_CLOSURE_3697"
DOC = ROOT / "3697-Y5-R2FR-direct-leakage-penalty-from-coarse-graining-Onsager-or-closure.md"


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
        ("handoff_3696", RESIDUALS / "P8_Y5_R2FR_3696_NEXT_TARGET.csv", "coarse-graining entropy"),
        ("contract_3696", RESIDUALS / "P8_Y5_R2FR_3696_DIRECT_PENALTY_CONTRACT_ROWS.csv", "S_leak"),
        ("u1_origin_3696", RESIDUALS / "P8_Y5_R2FR_3696_U1_ORIGIN_ROWS.csv", "U_Z"),
        ("coarse_XB_85", FORMALIZATION / "85-coarse-graining-invariants-XB.md", "D_L ="),
        ("DL_silence_122", FORMALIZATION / "122-parent-DL-fixed-point-silence.md", "D_L = U_B H_L"),
        ("fixed_point_124", FORMALIZATION / "124-fixed-point-extremality-origin.md", "But no parent environmental functional currently exists."),
        ("red_team_06", FORMALIZATION / "06-consistency-red-team.md", "doubled variables / Schwinger-Keldysh style effective action"),
        ("equations_05", FORMALIZATION / "05-equation-register.md", "Effective open-system gradient flow"),
        ("metric_null_138", FORMALIZATION / "138-metric-null-action-block-contract.md", "doubled open-system action"),
        ("scalar_evenness_126", FORMALIZATION / "126-scalar-evenness-origin.md", "Scalar evenness has a clean parity/isotropy theorem form"),
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
                "role": "direct leakage penalty derivation input",
            }
        )
    return rows


def entropy_derivation_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "EDR3697_0_state",
            "coarse-grained local state",
            "X=(X_L,z^A), z=0 is the local fixed point, s_L=G_AB z^A z^B",
            "The previous corpus gives candidate signed leakage coordinates and fixed-point distance architecture, not a parent entropy functional.",
            "STATE_SPACE_CANDIDATE_NOT_PARENT_COMPLETE",
            "R_state_owner",
        ),
        (
            "EDR3697_1_entropy_maximum",
            "entropy/free-energy maximum",
            "S_cg(X_L,z)=S_0(X_L)-0.5 C_AB(X_L) z^A z^B+O(z^4), C_AB>=0",
            "If the local fixed point is a stable coarse-grained entropy maximum, the negative Hessian supplies a positive quadratic penalty.",
            "THEOREM_FORM_DERIVED_ENTROPY_FUNCTIONAL_MISSING",
            "R_Scg_parent",
        ),
        (
            "EDR3697_2_free_energy",
            "free-energy penalty",
            "F_cg=-T_eff S_cg => U_Z=0.5 T_eff C_AB z^A z^B+O(z^4)",
            "This is the clean derivation route for a leakage penalty from coarse-graining.",
            "FORMAL_ROUTE_READY_TEFF_AND_CAB_MISSING",
            "R_Teff_CAB",
        ),
        (
            "EDR3697_3_metric_alignment",
            "alignment with G_AB",
            "C_AB=2u_1 T_eff^{-1} G_AB + C_perp, with ||C_perp|| bounded or symmetry-forbidden",
            "To recover M_AB=2u_1G_AB rather than an arbitrary Hessian, the entropy Hessian must align with the leakage metric.",
            "ALIGNMENT_CONDITION_DERIVED_NOT_SIGNED",
            "R_Cperp",
        ),
        (
            "EDR3697_4_units",
            "units and normalization",
            "[u_1] is fixed by the action density convention; T_eff C_AB/2 must match the response-action mass term units",
            "Entropy alone is dimensionless; the conversion into action/free-energy needs a real normalization.",
            "UNITS_NORMALIZATION_MISSING",
            "R_units",
        ),
        (
            "EDR3697_5_verdict",
            "entropy route verdict",
            "entropy maximum would derive U_Z=u_1 s_L if S_cg, T_eff, C_AB~G_AB and units are parent-owned",
            "Current corpus has the theorem form but not the parent entropy/free-energy object.",
            "ENTROPY_ROUTE_CONDITIONAL_CLOSURE_IF_UNSIGNED",
            "R_entropy_claim",
        ),
    ]
    return [
        {
            **base(timestamp),
            "entropy_id": entropy_id,
            "piece": piece,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "residual_if_failed": residual,
            "claim_allowed": False,
        }
        for entropy_id, piece, formula, derivation, status, residual in specs
    ]


def onsager_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "ONR3697_0_gradient_flow",
            "Onsager gradient flow",
            "dot z^A = -L^{AB} partial_B F_cg + noise/source terms",
            "A positive free-energy Hessian plus positive Onsager matrix gives relaxation, not just a static penalty.",
            "FORMAL_OPEN_SYSTEM_ROUTE_READY_PARENT_L_MISSING",
            "R_Onsager_L",
        ),
        (
            "ONR3697_1_OM_action",
            "Onsager-Machlup/doubled action",
            "S_OM ~ int (dot z + L C z)^T (4L)^{-1} (dot z + L C z)",
            "This is the action-language route compatible with the corpus warning that dissipative equations need doubled/open-system machinery.",
            "FORMAL_DOUBLED_ACTION_ROUTE_NOT_PARENT_BUILT",
            "R_OM_action",
        ),
        (
            "ONR3697_2_static_limit",
            "static local gap",
            "omega_H ~ eigen(L C), mu_H^2 ~ eigen(G_H^{-1} T_eff C) after static/elliptic reduction",
            "The local screening mass must be linked to a static response operator, not only to relaxation rate.",
            "STATIC_REDUCTION_REQUIRED",
            "R_static_limit",
        ),
        (
            "ONR3697_3_noise_FDT",
            "fluctuation-dissipation consistency",
            "noise covariance ~ 2 L T_eff if the open system is thermal/effective-equilibrium",
            "Without FDT/noise normalization, the entropy penalty can be a fitted damping knob.",
            "FDT_OR_NOISE_NORMALIZATION_MISSING",
            "R_noise",
        ),
        (
            "ONR3697_4_verdict",
            "Onsager route verdict",
            "Onsager can justify the dynamics around U_Z but does not by itself supply u_1 unless F_cg/S_cg is parent-derived",
            "Open-system route remains the best mathematical language, not yet a derivation.",
            "ONSAGER_ROUTE_CONTRACT_ONLY",
            "R_open_action",
        ),
    ]
    return [
        {
            **base(timestamp),
            "onsager_id": onsager_id,
            "piece": piece,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "residual_if_failed": residual,
            "claim_allowed": False,
        }
        for onsager_id, piece, formula, derivation, status, residual in specs
    ]


def closure_classifier_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "CLC3697_0_claim_branch",
            "claim-eligible direct penalty",
            "S_cg/T_eff/C_AB/G_AB/u_1/source silence/environment dependence all parent-owned",
            "Only this branch can promote local mass-gap screening to a derived local-GR route.",
            "NOT_AVAILABLE_CURRENTLY",
            False,
        ),
        (
            "CLC3697_1_closure_branch",
            "disciplined closure",
            "declare U_Z=u_1 s_L and pass u_1 to Yukawa runner with valid_for_claim=false",
            "Allowed as internal scaffolding and test discipline, not as evidence for derived GR reduction.",
            "AVAILABLE_NONCLAIM",
            False,
        ),
        (
            "CLC3697_2_no_penalty_branch",
            "no local mass-gap branch",
            "u_1=0 or not introduced; local safety must come from exact projection/metric-null/vertical theorem only",
            "If direct penalty is rejected, the local branch falls back to projection silence, not screening.",
            "AVAILABLE_BUT_STRICT",
            False,
        ),
        (
            "CLC3697_3_phenomenology_branch",
            "Yukawa phenomenology",
            "lambda_H and alpha_A fitted/sourced per shared closure parameters, then tested against R10/PPN/clocks/WEP/EM/orbits",
            "Can be useful for empirical pressure but remains nonclaim until parent origin exists.",
            "AVAILABLE_NONCLAIM",
            False,
        ),
    ]
    return [
        {
            **base(timestamp),
            "classifier_id": classifier_id,
            "branch": branch,
            "rule": rule,
            "meaning": meaning,
            "status": status,
            "claim_allowed": claim_allowed,
        }
        for classifier_id, branch, rule, meaning, status, claim_allowed in specs
    ]


def source_silence_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "SS3697_0_matter",
            "ordinary matter silence",
            "partial_z S_matter=0 at fixed q/Psi/theta and no z-dependent species masses",
            "prevents WEP/clock leakage from the new penalty sector",
            "UNSIGNED",
        ),
        (
            "SS3697_1_EM",
            "EM charge/stress silence",
            "partial_z Z_EM=0 and partial_z alpha_fs=0 unless quotient-owned",
            "prevents the penalty from renormalizing Maxwell/charge data",
            "UNSIGNED",
        ),
        (
            "SS3697_2_Newton",
            "Newton normalization silence",
            "partial_z G_N^obs=0 after fixed-point calibration, or residual alpha/lambda row must be scored",
            "keeps measured G calibration from being moved by the closure",
            "UNSIGNED",
        ),
        (
            "SS3697_3_environment",
            "environment dependence guard",
            "u_1(local), u_1(galaxy), u_1(cosmic) come from one function of X_B, not per-arena selection",
            "prevents solving local tests by erasing galaxy/cosmology response by hand",
            "UNSIGNED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "silence_id": silence_id,
            "sector": sector,
            "condition": condition,
            "why_it_matters": why,
            "status": status,
            "claim_allowed": False,
        }
        for silence_id, sector, condition, why, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3697_0",
            "Entropy/Onsager route is theorem-shaped",
            "A parent entropy/free-energy maximum can derive U_Z=u_1 s_L and an Onsager action can supply dynamics.",
            "FORMAL_ROUTE_IDENTIFIED",
        ),
        (
            "DEC3697_1",
            "No parent object found",
            "The corpus does not yet supply S_cg, T_eff, C_AB~G_AB, units, FDT/noise, or source silence.",
            "CLAIM_BLOCKED",
        ),
        (
            "DEC3697_2",
            "Closure classification",
            "Until the parent object is derived, u_1 must be treated as closure/nonclaim and scored through the Yukawa runner.",
            "CLOSURE_ONLY_FOR_NOW",
        ),
    ]
    return [
        {**base(timestamp), "decision_id": decision_id, "decision": decision, "rationale": rationale, "status": status}
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3697_0_entropy", "parent S_cg/free-energy functional missing", "BLOCKED"),
        ("CG3697_1_alignment", "entropy Hessian C_AB~G_AB not derived", "BLOCKED"),
        ("CG3697_2_units", "T_eff/action normalization and units missing", "BLOCKED"),
        ("CG3697_3_onsager", "doubled/open-system Onsager action not built", "BLOCKED"),
        ("CG3697_4_source_silence", "ordinary matter/EM/Newton source silence not signed", "BLOCKED"),
        ("CG3697_5_environment", "single u_1(X_B) environment law not derived", "BLOCKED"),
        ("CG3697_6_local_GR", "local GR mass-gap screening is closure-only until above gates pass", "BLOCKED"),
        ("CG3697_7_public", "private checkpoint only; no public/GitHub claim", "BLOCKED"),
    ]
    return [
        {**base(timestamp), "gate_id": gate_id, "gate": gate, "status": status, "claim_allowed": False}
        for gate_id, gate, status in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3697_0",
            "status": "DIRECT_LEAKAGE_PENALTY_THEOREM_SHAPED_BUT_PARENT_ENTROPY_ONSAGER_OBJECT_MISSING_CLOSURE_ONLY",
            "summary": "A coarse-grained entropy/free-energy maximum plus Onsager/open-system dynamics would derive U_Z=u_1 s_L, but the corpus does not yet own S_cg, T_eff, C_AB~G_AB, FDT/noise, units, source silence, or one environment law. Therefore u_1 remains closure-only/nonclaim for local mass-gap screening.",
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3697_0",
            "target_doc": "3698-Y5-R2FR-parent-entropy-free-energy-object-or-u1-closure-runner.md",
            "target_script": "scripts/Y5_R2FR_3698_parent_entropy_free_energy_object_or_u1_closure_runner.py",
            "objective": "attempt to construct the parent S_cg/F_cg object with Hessian C_AB aligned to G_AB and source-silence gates; if absent, write explicit u1 closure runner rows for local Yukawa tests",
            "success_gate": "S_cg/F_cg is parent-owned enough to derive positive u_1, or u_1 is formally demoted to a nonclaim closure coefficient with arena runner inputs",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    entropy: list[dict[str, object]],
    onsager: list[dict[str, object]],
    classifiers: list[dict[str, object]],
    silence: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3697 - Direct leakage penalty from coarse-graining Onsager or closure",
        "",
        "Private checkpoint. No GitHub action. No local-GR/Newton/R10/PPN/EM claim.",
        "",
        "## Status",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "- A real derivation of `U_Z=u_1 s_L` is possible in form, but not yet supplied by the corpus.",
        "- Entropy/free-energy route: if `S_cg=S_0-0.5 C_AB z^A z^B+O(z^4)`, then `F_cg=-T_eff S_cg` gives `U_Z=0.5 T_eff C_AB z^A z^B`.",
        "- To recover the 3695 mass-gap law, the Hessian must align with the leakage metric: `C_AB=2u_1 T_eff^{-1}G_AB+C_perp`, with `C_perp` zero or bounded.",
        "- Onsager route supplies dynamics, `dot z=-L partial F_cg`, but it does not supply `u_1` unless `F_cg/S_cg` is parent-derived.",
        "",
        "## Verdict",
        "- The theorem shape is good.",
        "- The parent object is missing.",
        "- Therefore `u_1` is closure-only/nonclaim until a parent entropy/free-energy/Onsager object is built.",
        "",
        "## Entropy Derivation Rows",
    ]
    for row in entropy:
        lines.append(f"- `{row['entropy_id']}`: {row['piece']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Onsager Rows"])
    for row in onsager:
        lines.append(f"- `{row['onsager_id']}`: {row['piece']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Closure Classifier"])
    for row in classifiers:
        lines.append(f"- `{row['classifier_id']}`: {row['branch']} | `{row['status']}` | {row['rule']}")
    lines.extend(["", "## Source-Silence Gates"])
    for row in silence:
        lines.append(f"- `{row['silence_id']}`: {row['sector']} | `{row['status']}` | {row['condition']}")
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
    entropy: list[dict[str, object]],
    onsager: list[dict[str, object]],
    classifiers: list[dict[str, object]],
    silence: list[dict[str, object]],
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
    no_leak = not any(FORMALIZATION.rglob("*3697*"))
    entropy_ok = any(row_data["entropy_id"] == "EDR3697_2_free_energy" and "U_Z" in row_data["formula"] for row_data in entropy)
    alignment_ok = any(row_data["entropy_id"] == "EDR3697_3_metric_alignment" and "C_AB" in row_data["formula"] and "G_AB" in row_data["formula"] for row_data in entropy)
    onsager_ok = any(row_data["onsager_id"] == "ONR3697_1_OM_action" and "S_OM" in row_data["formula"] for row_data in onsager)
    closure_ok = any(row_data["classifier_id"] == "CLC3697_1_closure_branch" and row_data["status"] == "AVAILABLE_NONCLAIM" for row_data in classifiers)
    silence_ok = {row_data["silence_id"] for row_data in silence} == {"SS3697_0_matter", "SS3697_1_EM", "SS3697_2_Newton", "SS3697_3_environment"}
    gates_blocked = all(row_data["status"] == "BLOCKED" for row_data in claim_gates)
    nonclaim = all(
        not bool(row_data.get("valid_for_claim"))
        for table in [sources, entropy, onsager, classifiers, silence, decisions, claim_gates, status, next_target]
        for row_data in table
    )
    next_ok = str(next_target[0]["target_doc"]).startswith("3698-") and "entropy" in str(next_target[0]["target_doc"])
    doc_ok = all(needle in doc_text for needle in ["U_Z=u_1 s_L", "S_cg=S_0-0.5 C_AB", "C_AB=2u_1", "closure-only/nonclaim"])

    return [
        row("VAL3697_0_sources_exist", source_ok, "all input source files exist"),
        row("VAL3697_1_needles_found", needles_ok, "all source needles found"),
        row("VAL3697_2_outputs_exist", all(path.exists() for path in generated_paths), "all generated outputs exist"),
        row("VAL3697_3_csv_parse", parsed_ok, "; ".join(parse_details)),
        row("VAL3697_4_entropy_route", entropy_ok, "free-energy route to U_Z recorded"),
        row("VAL3697_5_metric_alignment", alignment_ok, "C_AB to G_AB alignment condition recorded"),
        row("VAL3697_6_onsager_route", onsager_ok, "Onsager-Machlup/open-system route recorded"),
        row("VAL3697_7_closure_classification", closure_ok, "u1 closure branch explicitly nonclaim"),
        row("VAL3697_8_source_silence", silence_ok, "matter/EM/Newton/environment silence gates present"),
        row("VAL3697_9_claim_gates_blocked", gates_blocked, "all claim gates remain blocked"),
        row("VAL3697_10_all_nonclaim", nonclaim, "all tables remain nonclaim"),
        row("VAL3697_11_next_target", next_ok, "3698 entropy/free-energy target selected"),
        row("VAL3697_12_doc_written", doc_ok, "doc contains penalty, entropy Hessian, alignment and closure verdict"),
        row("VAL3697_13_no_formalization_leak", no_leak, "no 3697 files under formalization-workbench"),
    ]


def main() -> int:
    timestamp = stamp()
    sources = source_register(timestamp)
    entropy = entropy_derivation_rows(timestamp)
    onsager = onsager_rows(timestamp)
    classifiers = closure_classifier_rows(timestamp)
    silence = source_silence_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3697_SOURCE_REGISTER.csv",
        "entropy": RESIDUALS / "P8_Y5_R2FR_3697_ENTROPY_DERIVATION_ROWS.csv",
        "onsager": RESIDUALS / "P8_Y5_R2FR_3697_ONSAGER_ROWS.csv",
        "classifiers": RESIDUALS / "P8_Y5_R2FR_3697_CLOSURE_CLASSIFIER_ROWS.csv",
        "silence": RESIDUALS / "P8_Y5_R2FR_3697_SOURCE_SILENCE_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3697_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3697_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3697_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3697_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3697_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["entropy"], entropy)
    write_csv(outputs["onsager"], onsager)
    write_csv(outputs["classifiers"], classifiers)
    write_csv(outputs["silence"], silence)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, entropy, onsager, classifiers, silence, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(timestamp, generated_paths, sources, entropy, onsager, classifiers, silence, decisions, claim_gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3697 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3697 checkpoint: direct leakage penalty theorem-shaped; u1 closure-only until parent entropy/Onsager object exists")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
