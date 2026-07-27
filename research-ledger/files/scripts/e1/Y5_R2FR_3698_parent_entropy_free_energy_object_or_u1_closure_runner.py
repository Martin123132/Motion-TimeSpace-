from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3698"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ENTROPY_FREE_ENERGY_OBJECT_OR_U1_CLOSURE_RUNNER_3698"
DOC = ROOT / "3698-Y5-R2FR-parent-entropy-free-energy-object-or-u1-closure-runner.md"


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
        ("handoff_3697", RESIDUALS / "P8_Y5_R2FR_3697_NEXT_TARGET.csv", "attempt to construct the parent S_cg/F_cg object"),
        ("entropy_3697", RESIDUALS / "P8_Y5_R2FR_3697_ENTROPY_DERIVATION_ROWS.csv", "entropy maximum would derive U_Z=u_1 s_L"),
        ("silence_3697", RESIDUALS / "P8_Y5_R2FR_3697_SOURCE_SILENCE_GATES.csv", "partial_z S_matter=0"),
        ("parent_roadmap_82", FORMALIZATION / "82-parent-dynamics-roadmap.md", "make the coarse-graining theorem the upgrade path"),
        ("parent_equations_83", FORMALIZATION / "83-parent-equations-v1.md", "universal invariant bundle controlling Pi_B, U_B, D_L, m_L, S_cg, and F_L."),
        ("coarse_graining_85", FORMALIZATION / "85-coarse-graining-invariants-XB.md", "This file does not prove the coarse-graining theorem."),
        ("source_silence_77", FORMALIZATION / "77-sigma-L-source-silence-theorem.md", "The exact `Sigma_L` source-silence theorem is not derived"),
        ("fixed_point_124", FORMALIZATION / "124-fixed-point-extremality-origin.md", "Z_L, G_AB, and scalar evenness are not parent-derived yet."),
        ("scalar_evenness_126", FORMALIZATION / "126-scalar-evenness-origin.md", "positive leakage-frame metric G_AB"),
        ("red_team_06", FORMALIZATION / "06-consistency-red-team.md", "Use doubled variables / Schwinger-Keldysh style effective action."),
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
                "role": "parent entropy/free-energy construction input",
            }
        )
    return rows


def relative_entropy_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "REC3698_0_state_split",
            "resolved plus unresolved local state",
            "X=(X_L,z^A), q(X)=q(X_L), z^A=0 on Sigma_L",
            "Use z^A only for quotient-null leakage directions, so the resolved GR/SM variables live in q(X_L) and the leakage sector is a bath/internal coordinate.",
            "CONSTRUCTIVE_CONTRACT",
            "q and z^A must be parent-defined, not chosen per arena",
        ),
        (
            "REC3698_1_exponential_family",
            "maximum-entropy bath family",
            "p_z(xi|X_L)=p_0(xi|X_L) exp[z^A Y_A(xi)-W(z;X_L)]",
            "The least-assumptive local parent object is an exponential-family coarse-graining around the fixed bath state p_0.",
            "DERIVATION_TEMPLATE",
            "Y_A observables and p_0 are not yet source-owned in the corpus",
        ),
        (
            "REC3698_2_relative_entropy",
            "entropy loss",
            "D_KL(p_z||p_0)=0.5 I_AB z^A z^B+O(z^3), I_AB=<Y_A Y_B>_0-<Y_A>_0<Y_B>_0",
            "Relative entropy has a fixed point minimum at p_0, so the coarse-grained entropy S_cg=S_0-D_KL has a maximum at z=0.",
            "DERIVED_IF_BATH_DEFINED",
            "Fisher matrix I_AB must be finite and positive on the physical horizontal subspace",
        ),
        (
            "REC3698_3_free_energy_penalty",
            "free-energy/action penalty",
            "Delta F_cg=T_eff D_KL=0.5 T_eff I_AB z^A z^B+O(z^3); if G_AB:=I_AB then U_Z=u_1 s_L with u_1 = T_eff/2",
            "This is the cleanest direct derivation found so far: the quadratic local penalty is the Fisher cost of moving the unresolved bath away from its local fixed distribution.",
            "CONDITIONAL_DERIVATION",
            "T_eff and action-density normalization remain unsourced",
        ),
        (
            "REC3698_4_anisotropic_bound",
            "non-isotropic leakage metric",
            "u_1,min=(T_eff/2) lambda_min(G^-1/2 I G^-1/2), u_1,max=(T_eff/2) lambda_max(G^-1/2 I G^-1/2)",
            "If G_AB is already fixed elsewhere, the derivation still gives a lower/upper mass-gap band rather than requiring exact alignment.",
            "BOUND_ROUTE_READY",
            "Need real G_AB and I_AB eigenvalue estimates before local numerical claims",
        ),
        (
            "REC3698_5_verdict",
            "constructive verdict",
            "relative-entropy parent object can derive positive U_Z, but current MTS files do not yet specify p_0, Y_A, I_AB, T_eff or units",
            "This advances the route: the missing object is no longer vague; it is a concrete bath distribution plus Fisher metric contract.",
            "PARENT_OBJECT_CONSTRUCTED_AS_CONTRACT_NOT_FILLED",
            "No local-GR/R10/PPN claim until those ingredients are populated",
        ),
    ]
    return [
        {
            **base(timestamp),
            "construction_id": construction_id,
            "piece": piece,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "open_requirement": open_requirement,
            "claim_allowed": False,
        }
        for construction_id, piece, formula, derivation, status, open_requirement in specs
    ]


def fisher_alignment_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "FMA3698_0_positive_metric",
            "I_AB is a covariance/Fisher matrix and is positive semidefinite; after removing exact vertical nulls it should be positive definite on horizontal leakage modes.",
            "This gives the sign of the local quadratic penalty without inventing a sign by hand.",
            "SIGN_CONDITIONAL_ON_NONDEGENERATE_FISHER",
        ),
        (
            "FMA3698_1_metric_definition",
            "Choose the leakage metric by parent pullback G_AB := I_AB on the horizontal bath-coordinate chart.",
            "This makes C_AB align with G_AB by construction, not by an extra fitted isotropy axiom.",
            "ALIGNMENT_DERIVED_IF_COORDINATE_CHOICE_PARENT_ALLOWED",
        ),
        (
            "FMA3698_2_existing_metric_case",
            "If G_AB has already been fixed by another parent block, keep C_AB=I_AB and carry C_perp=I_AB-2u_1 T_eff^-1 G_AB as an anisotropy residual.",
            "This prevents hiding anisotropy in notation and gives a testable residual vector.",
            "ANISOTROPY_EXPLICIT",
        ),
        (
            "FMA3698_3_mass_gap_map",
            "mu_H^2 >= T_eff lambda_min(G_H^-1/2 I_H G_H^-1/2) - R_domain - R_source_slope.",
            "The previous 3695/3696 mass-gap law now has a candidate parent origin for its positive Hessian.",
            "LOCAL_GAP_BOUND_CONDITIONAL",
        ),
    ]
    return [
        {
            **base(timestamp),
            "alignment_id": alignment_id,
            "statement": statement,
            "why_it_matters": why_it_matters,
            "status": status,
            "claim_allowed": False,
        }
        for alignment_id, statement, why_it_matters, status in specs
    ]


def u1_runner_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "U1R3698_0_parent_symbolic",
            "u_1_parent",
            "0.5*T_eff*lambda_min(G_H^-1/2 I_H G_H^-1/2)",
            "parent symbolic",
            "requires T_eff, G_H, I_H, R_domain, R_source_slope source rows",
        ),
        (
            "U1R3698_1_metric_aligned",
            "u_1_aligned",
            "0.5*T_eff",
            "metric aligned",
            "requires proof that G_AB := I_AB is parent-allowed and units are normalized",
        ),
        (
            "U1R3698_2_closure_numeric_slot",
            "u_1_closure",
            "user/sourced numeric closure coefficient",
            "nonclaim closure",
            "may be used only to run R10/PPN/clock/orbit smoke tests with valid_for_claim=false",
        ),
        (
            "U1R3698_3_no_penalty_control",
            "u_1_zero_control",
            "0",
            "control branch",
            "tests whether vertical/projected exact silence alone can satisfy local arenas",
        ),
    ]
    return [
        {
            **base(timestamp),
            "runner_id": runner_id,
            "parameter": parameter,
            "formula_or_value": formula_or_value,
            "branch": branch,
            "required_inputs": required_inputs,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, parameter, formula_or_value, branch, required_inputs in specs
    ]


def source_silence_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "SS3698_0_matter",
            "Matter action descends through q: partial_z S_matter[q(X),Psi,theta]=0 at fixed q, Psi, theta.",
            "If true, the Fisher bath penalty can screen leakage without changing ordinary local matter couplings.",
            "UNSIGNED_PARENT_DESCENT",
        ),
        (
            "SS3698_1_EM_poynting",
            "EM stress and Poynting flux enter only through quotient-owned T_EM^{mu nu}; direct z-dependence of alpha_fs or S^i_EM is forbidden unless separately bounded.",
            "This is where the Poynting-vector intuition belongs: it can be a resolved stress/flux source, not a hidden leakage knob.",
            "UNSIGNED_EM_STRESS_GATE",
        ),
        (
            "SS3698_2_Newton_G",
            "Observed G_N is the calibrated quotient coupling; leakage-sector shifts must appear as alpha(lambda) residuals, not as arbitrary G_N changes.",
            "This keeps the GR/Newton comparison fair: MTS may derive a coupling, but until then it must not smuggle it.",
            "UNSIGNED_COUPLING_GATE",
        ),
        (
            "SS3698_3_environment",
            "T_eff(X_B), I_AB(X_B), and p_0(xi|X_B) must be one environment law across local, galaxy, and cosmology branches.",
            "No per-arena screening switch is allowed.",
            "UNSIGNED_UNIVERSALITY_GATE",
        ),
    ]
    return [
        {
            **base(timestamp),
            "silence_id": silence_id,
            "condition": condition,
            "why_it_matters": why_it_matters,
            "status": status,
            "claim_allowed": False,
        }
        for silence_id, condition, why_it_matters, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3698_0",
            "relative-entropy/Fisher construction",
            "Adopt as the best current derivation candidate for the direct leakage penalty.",
            "ADVANCES_FRAMEWORK",
        ),
        (
            "DEC3698_1",
            "claim status",
            "Do not claim local GR/R10/PPN success: p_0, Y_A, I_AB, T_eff, units, and source-silence are not parent-filled.",
            "CLAIM_BLOCKED",
        ),
        (
            "DEC3698_2",
            "runner status",
            "Use u_1_parent, u_1_aligned, u_1_closure, and u_1_zero_control branches for future local Yukawa smoke tests.",
            "RUNNER_READY_NONCLAIM",
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
        ("CG3698_0_parent_distribution", "p_0(xi|X_B) source-owned and normalized", "BLOCKED"),
        ("CG3698_1_leakage_observables", "Y_A and z^A parent-owned and quotient-null", "BLOCKED"),
        ("CG3698_2_fisher_metric", "I_AB computed/sourced and positive on horizontal modes", "BLOCKED"),
        ("CG3698_3_temperature_units", "T_eff and action-density normalization sourced", "BLOCKED"),
        ("CG3698_4_source_silence", "matter/EM/Newton couplings prove partial_z silence or bounded residuals", "BLOCKED"),
        ("CG3698_5_universal_environment", "single X_B law across local/galaxy/cosmology", "BLOCKED"),
        ("CG3698_6_local_gr", "local GR/Newton/PPN/R10 pass from sourced numbers", "BLOCKED"),
        ("CG3698_7_public", "public claim wording allowed", "BLOCKED"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
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
            "status_id": "STATUS3698_0",
            "status": "RELATIVE_ENTROPY_FISHER_PARENT_OBJECT_CONSTRUCTED_AS_NONCLAIM_CONTRACT",
            "summary": (
                "3698 turns the direct leakage penalty into a concrete candidate derivation: a maximum-entropy bath p_z around the local fixed point gives "
                "D_KL=0.5 I_AB z^A z^B, Delta F=T_eff D_KL, and U_Z=u_1 s_L when G_AB is the Fisher pullback. "
                "This is real structural progress, but it is not claimable until p_0, Y_A, I_AB, T_eff, units, and source-silence are filled from parent sources."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3698_0",
            "target_doc": "3699-Y5-R2FR-parent-bath-observable-map-and-source-silence-fill.md",
            "target_script": "scripts/Y5_R2FR_3699_parent_bath_observable_map_and_source_silence_fill.py",
            "objective": "try to define p_0(xi|X_B), leakage observables Y_A, and quotient-null/source-silence map; include EM/Poynting stress as a resolved source gate rather than a hidden leakage knob",
            "success_gate": "either produce source-owned p_0/Y_A/I_AB/T_eff rows sufficient for a nonzero u_1 bound, or explicitly keep the u_1 closure runner as nonclaim test machinery",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    relative_entropy: list[dict[str, object]],
    fisher_alignment: list[dict[str, object]],
    u1_runner: list[dict[str, object]],
    silence: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3698 Y5 R2FR Parent Entropy Free-Energy Object Or u1 Closure Runner",
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
        "- The strongest route is now constructive: define an unresolved local bath distribution `p_z(xi|X_L)=p_0(xi|X_L) exp[z^A Y_A(xi)-W(z;X_L)]`.",
        "- The relative entropy expansion gives `D_KL(p_z||p_0)=0.5 I_AB z^A z^B+O(z^3)` with `I_AB` the Fisher/covariance matrix.",
        "- The free-energy penalty is `Delta F_cg=T_eff D_KL=0.5 T_eff I_AB z^A z^B+O(z^3)`.",
        "- If the leakage metric is the parent Fisher pullback, `G_AB:=I_AB`, then `U_Z=u_1 s_L` with `u_1 = T_eff/2`.",
        "- If `G_AB` is fixed independently, carry the eigenvalue bound `u_1,min=(T_eff/2) lambda_min(G^-1/2 I G^-1/2)` plus an anisotropy residual.",
        "",
        "## What This Fixes",
        "",
        "- `u_1` is no longer just an arbitrary symbol in the best branch: it can be the local bath temperature/response scale times a Fisher information metric.",
        "- The sign problem improves: Fisher covariance is positive semidefinite, so the local penalty has the right sign after vertical nulls are removed.",
        "- The metric-alignment problem improves: if `G_AB` is defined from the same bath Fisher metric, `C_AB~G_AB` is a definition from the parent chart rather than a new axiom.",
        "",
        "## What Still Blocks A Claim",
        "",
        "- The corpus still does not provide the actual bath state `p_0`, leakage observables `Y_A`, Fisher matrix `I_AB`, effective temperature `T_eff`, or units normalization.",
        "- Source silence is still unsigned: matter, EM/Poynting flux, and observed Newton coupling must descend through `q` or appear as bounded residuals.",
        "- Therefore this checkpoint upgrades the route to a serious derivation contract, not to a local-GR/R10/PPN pass.",
        "",
        "## Relative-Entropy Construction Rows",
        "",
    ]
    for row in relative_entropy:
        lines.append(f"- `{row['construction_id']}`: {row['piece']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Fisher Alignment Rows", ""])
    for row in fisher_alignment:
        lines.append(f"- `{row['alignment_id']}`: `{row['status']}` | {row['statement']}")
    lines.extend(["", "## u1 Runner Rows", ""])
    for row in u1_runner:
        lines.append(f"- `{row['runner_id']}`: `{row['parameter']}` = `{row['formula_or_value']}` | `{row['branch']}` | claim=false")
    lines.extend(["", "## Source-Silence Gates", ""])
    for row in silence:
        lines.append(f"- `{row['silence_id']}`: `{row['status']}` | {row['condition']}")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']} | {row['rationale']}")
    lines.extend(["", "## Claim Gates", ""])
    for row in claim_gates:
        lines.append(f"- `{row['gate_id']}`: `{row['status']}` | {row['requirement']}")
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
    relative_entropy: list[dict[str, object]],
    fisher_alignment: list[dict[str, object]],
    u1_runner: list[dict[str, object]],
    silence: list[dict[str, object]],
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
            if path.name.endswith("VALIDATION.csv"):
                continue
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    rec_by_id = {str(row["construction_id"]): row for row in relative_entropy}
    fma_by_id = {str(row["alignment_id"]): row for row in fisher_alignment}
    u1_by_id = {str(row["runner_id"]): row for row in u1_runner}
    checks.append(("relative_entropy_formula", "relative entropy row contains D_KL and Fisher matrix", "D_KL" in str(rec_by_id["REC3698_2_relative_entropy"]["formula"]) and "I_AB" in str(rec_by_id["REC3698_2_relative_entropy"]["formula"]), ""))
    checks.append(("free_energy_u1_formula", "free-energy row derives U_Z and u_1", "U_Z" in str(rec_by_id["REC3698_3_free_energy_penalty"]["formula"]) and "u_1 = T_eff/2" in str(rec_by_id["REC3698_3_free_energy_penalty"]["formula"]), ""))
    checks.append(("metric_alignment_formula", "metric alignment row defines G_AB from I_AB", "G_AB := I_AB" in str(fma_by_id["FMA3698_1_metric_definition"]["statement"]), ""))
    checks.append(("runner_rows_nonclaim", "all u1 runner rows are nonclaim", all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in u1_runner), ""))
    checks.append(("runner_control_exists", "u1 zero-control branch exists", "U1R3698_3_no_penalty_control" in u1_by_id, ""))
    checks.append(("poynting_gate_exists", "EM/Poynting source gate exists", any("Poynting" in str(row["condition"]) for row in silence), ""))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3699", "next target advances to 3699 bath observable map", str(next_target[0]["target_doc"]).startswith("3699-") and "bath" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core construction terms", all(term in doc_text for term in ["p_z(xi|X_L)", "D_KL(p_z||p_0)", "G_AB:=I_AB", "u_1 = T_eff/2", "Poynting"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3698*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3698 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
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
    relative_entropy = relative_entropy_rows(timestamp)
    fisher_alignment = fisher_alignment_rows(timestamp)
    u1_runner = u1_runner_rows(timestamp)
    silence = source_silence_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3698_SOURCE_REGISTER.csv",
        "relative_entropy": RESIDUALS / "P8_Y5_R2FR_3698_RELATIVE_ENTROPY_CONSTRUCTION_ROWS.csv",
        "fisher_alignment": RESIDUALS / "P8_Y5_R2FR_3698_FISHER_ALIGNMENT_ROWS.csv",
        "u1_runner": RESIDUALS / "P8_Y5_R2FR_3698_U1_CLOSURE_RUNNER_ROWS.csv",
        "silence": RESIDUALS / "P8_Y5_R2FR_3698_SOURCE_SILENCE_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3698_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3698_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3698_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3698_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3698_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["relative_entropy"], relative_entropy)
    write_csv(outputs["fisher_alignment"], fisher_alignment)
    write_csv(outputs["u1_runner"], u1_runner)
    write_csv(outputs["silence"], silence)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, relative_entropy, fisher_alignment, u1_runner, silence, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, relative_entropy, fisher_alignment, u1_runner, silence, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3698 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3698 checkpoint: relative-entropy/Fisher parent object built as nonclaim u1 derivation contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
