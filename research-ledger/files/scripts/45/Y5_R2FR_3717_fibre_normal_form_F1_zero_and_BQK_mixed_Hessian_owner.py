from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3717"
BRANCH_ID = "MTS_R2FR_Y5_FIBRE_NORMAL_FORM_F1_ZERO_AND_BQK_MIXED_HESSIAN_OWNER_3717"
DOC = ROOT / "3717-Y5-R2FR-fibre-normal-form-F1-zero-and-BQK-mixed-Hessian-owner.md"

DOC_3716 = ROOT / "3716-Y5-R2FR-LH-block-diagonal-from-quotient-action-or-epsilon-LP-source-row.md"
NEXT_3716 = RESIDUALS / "P8_Y5_R2FR_3716_NEXT_TARGET.csv"
COEFF_3716 = RESIDUALS / "P8_Y5_R2FR_3716_COEFFICIENT_PACK_ROWS.csv"
NORMAL_3716 = RESIDUALS / "P8_Y5_R2FR_3716_NORMAL_FORM_AUDIT_ROWS.csv"
THEOREM_3716 = RESIDUALS / "P8_Y5_R2FR_3716_BLOCK_DIAGONAL_THEOREM_ROWS.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"
FILL_3709 = RESIDUALS / "P8_Y5_R2FR_3709_PARENT_FILL_ROWS.csv"
NQ_670 = RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv"
NORMAL_FORM_3519 = RESIDUALS / "P8_EM_vq_parent_object_language_normal_form_candidate.csv"
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
        ("doc_3716", DOC_3716, "ADVANCE_TO_F1_BQK_OWNER", "3716 selected F1/BQK owner target"),
        ("next_3716", NEXT_3716, "F_1=0 and B_QK=0", "3716 declared 3717 target"),
        ("coeff_3716", COEFF_3716, "COEF3716_0_F1", "3716 coefficient pack"),
        ("normal_3716", NORMAL_3716, "NF3716_2_viable_fibre_gap_form", "3716 fibre normal form route"),
        ("theorem_3716", THEOREM_3716, "THM3716_0_normal_form_to_block_diagonal", "3716 normal-form theorem"),
        ("fisher_3708", FISHER_3708, "D_KL(p_z||p_0)=0.5", "3708 Fisher/KL local bath expansion"),
        ("fill_3709", FILL_3709, "Theta_H*iota_H", "3709 renamed Fisher scale and parent gap contract"),
        ("nq_670", NQ_670, "NQ670_3_action_descent", "quotient/fibre action descent route"),
        ("normal_form_3519", NORMAL_FORM_3519, "NF3519_1_quotient_visible_stack", "parent object-language normal-form candidate"),
        ("doc_1038", DOC_1038, "MISSING_DCX_OPERATOR", "operator owner obstruction"),
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


def zero_section_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "ZS3717_0_bundle_patch",
            "local bundle patch",
            "Phi -> (q,z) with q=q_obs(Phi), z in ker(Dq_obs), and z=0 the local zero-section",
            "defines the branch on which fibre force and mixed Hessian are evaluated",
            "SETUP",
        ),
        (
            "ZS3717_1_fibre_force",
            "fibre force",
            "F_z(q):=partial_z S_parent(q,z)|_{z=0}",
            "F_z is the coefficient called F_1 in 3716",
            "DEFINITION",
        ),
        (
            "ZS3717_2_family_extremum",
            "zero-section family extremum",
            "F_z(q)=0 for every q in the local observed branch U",
            "stronger than F_z(q0)=0; it is the condition needed to kill the mixed derivative",
            "KEY_PARENT_CLAUSE",
        ),
        (
            "ZS3717_3_mixed_derivative",
            "mixed Hessian identity",
            "B_QK(q):=partial_q partial_z S_parent(q,0)=partial_q F_z(q)",
            "turns B_QK into the q-derivative of the fibre-force row",
            "DERIVED_IDENTITY",
        ),
        (
            "ZS3717_4_F1_to_BQK",
            "family zero implies mixed zero",
            "F_z(q)=0 on U => B_QK(q)=partial_q F_z(q)=0 on U",
            "this is the clean proof route: parent-sign a family extremum, not a point extremum",
            "DERIVED_EXACT_CONDITIONAL",
        ),
        (
            "ZS3717_5_point_warning",
            "point extremum warning",
            "F_z(q0)=0 alone does not imply B_QK(q0)=0",
            "prevents a fake proof by tuning only the tested local point",
            "ANTI_SMUGGLING_GUARD",
        ),
    ]
    return [
        {
            **base(timestamp),
            "zero_section_id": row_id,
            "object": obj,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, obj, formula, meaning, status in specs
    ]


def fisher_route_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "FISH3717_0_exponential_bath",
            "p_z(xi|X_B,q)=p_0 exp[z^A Y_A^perp-W(z;X_B,q)]",
            "normalization by W makes z=0 the reference bath point at each q",
            "CONDITIONAL_SOURCE_FROM_3708",
        ),
        (
            "FISH3717_1_KL_expansion",
            "D_KL(p_z||p_0)=0.5 I_AB(q) z^A z^B + O(||z||^3)",
            "the KL divergence has no linear z term at the reference distribution",
            "DERIVED_IF_BATH_OWNED",
        ),
        (
            "FISH3717_2_parent_fibre_potential",
            "Delta S_fibre(q,z)=Theta_H(q) D_KL(p_z||p_0(q)) + R_even(q,z) + R_odd(q,z)",
            "separates the Fisher quadratic core from correction terms that can reintroduce F_1 or B_QK",
            "NORMAL_FORM_TEMPLATE",
        ),
        (
            "FISH3717_3_F1_zero_core",
            "partial_z [Theta_H D_KL]|_{z=0}=0",
            "the Fisher/KL core gives F_1=0 without fitting",
            "DERIVED_EXACT_FOR_CORE",
        ),
        (
            "FISH3717_4_BQK_zero_core",
            "partial_q partial_z [Theta_H D_KL]|_{z=0}=partial_q 0=0",
            "q-dependence of Theta_H or I_AB(q) does not create a q-z mixed Hessian at z=0",
            "DERIVED_EXACT_FOR_CORE",
        ),
        (
            "FISH3717_5_gap_core",
            "M_K,core(q)=Theta_H(q) I_AB(q)",
            "the same core can supply a positive fibre gap while keeping F_1 and B_QK zero",
            "DERIVED_CONDITIONAL_GAP_ROUTE",
        ),
    ]
    return [
        {
            **base(timestamp),
            "fisher_id": row_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, formula, meaning, status in specs
    ]


def correction_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "CORR3717_0_Rodd_force",
            "R_odd,F1",
            "partial_z R_odd(q,z)|_{z=0}",
            "action per fibre coordinate",
            "any odd/cubic correction with a linear remnant reopens F_1",
            "MISSING_ZERO_OR_BOUND",
        ),
        (
            "CORR3717_1_Rodd_mixed",
            "R_odd,BQK",
            "partial_q partial_z R_odd(q,z)|_{z=0}",
            "local Hessian/operator units",
            "any q-dependent odd correction reopens B_QK",
            "MISSING_ZERO_OR_BOUND",
        ),
        (
            "CORR3717_2_boundary_force",
            "B_boundary,F1",
            "partial_z S_boundary(q,z)|_{z=0}",
            "boundary action per fibre coordinate",
            "boundary can spoil the bulk zero-section extremum",
            "MISSING_BOUNDARY_ZERO_OR_BOUND",
        ),
        (
            "CORR3717_3_boundary_mixed",
            "B_boundary,QK",
            "partial_q partial_z S_boundary(q,z)|_{z=0}",
            "local boundary Hessian/operator units",
            "boundary can spoil mixed Hessian silence",
            "MISSING_BOUNDARY_MIXED_ZERO_OR_BOUND",
        ),
        (
            "CORR3717_4_total_F1",
            "F_1_total",
            "F_1_total = R_odd,F1 + B_boundary,F1",
            "action per fibre coordinate",
            "Fisher/KL core contributes zero; retained terms must vanish or be bounded",
            "DERIVED_RETAINED_FORCE_ROW",
        ),
        (
            "CORR3717_5_total_BQK",
            "B_QK,total",
            "B_QK,total = R_odd,BQK + B_boundary,QK",
            "local Hessian/operator units",
            "Fisher/KL core contributes zero; retained terms feed epsilon_LP",
            "DERIVED_RETAINED_MIXED_ROW",
        ),
    ]
    return [
        {
            **base(timestamp),
            "correction_id": row_id,
            "quantity": quantity,
            "formula_or_value": formula,
            "units": units,
            "use": use,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, quantity, formula, units, use, status in specs
    ]


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "THM3717_0_family_extremum",
            "If F_z(q)=0 for all q in the local observed patch, then B_QK(q)=0 throughout that patch.",
            "B_QK=partial_q partial_z S=partial_q F_z; differentiating the identity F_z(q)=0 gives zero.",
            "DERIVED_EXACT_CONDITIONAL",
            "requires parent-owned zero-section family, not just one tuned local point",
        ),
        (
            "THM3717_1_Fisher_core",
            "The Fisher/KL fibre core gives F_1=0 and B_QK=0 while retaining M_K=Theta_H I_H.",
            "D_KL has no linear term at the reference distribution; q derivatives of that zero linear term remain zero.",
            "DERIVED_EXACT_FOR_CORE",
            "requires p_z, p_0, Theta_H, I_H, and units to be parent-owned",
        ),
        (
            "THM3717_2_gap_survives",
            "A positive Fisher matrix supplies a kernel-sector gap without introducing a q-z mixed Hessian at z=0.",
            "M_K,core=Theta_H I_H can be positive even when B_QK,core=0.",
            "DERIVED_CONDITIONAL_ROUTE",
            "requires matching M_K or Xi_H to the actual local sector gap",
        ),
        (
            "THM3717_3_retained_terms",
            "Any non-Fisher odd correction or boundary mixed term must be theorem-zero or retained as a finite coefficient.",
            "The total F_1 and B_QK rows reduce to correction and boundary rows once the Fisher core is accepted.",
            "DERIVED_NONCLAIM_BOUND_ROUTE",
            "requires numeric/source rows for retained corrections before local-GR promotion",
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": row_id,
            "statement": statement,
            "proof_sketch": proof,
            "status": status,
            "remaining_gap": gap,
            "claim_allowed": False,
        }
        for row_id, statement, proof, status, gap in specs
    ]


def coefficient_pack_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "PACK3717_0_F1_core",
            "F_1,core",
            "0",
            "action per fibre coordinate",
            "Fisher/KL core zero force",
            "CONDITIONAL_ZERO_VALUE_NOT_CLAIMED",
        ),
        (
            "PACK3717_1_BQK_core",
            "B_QK,core",
            "0",
            "local Hessian/operator units",
            "Fisher/KL core mixed Hessian silence",
            "CONDITIONAL_ZERO_VALUE_NOT_CLAIMED",
        ),
        (
            "PACK3717_2_MK_core",
            "M_K,core",
            "Theta_H I_H plus corrections",
            "local Hessian/operator units",
            "candidate owner for kernel gap",
            "MISSING_THETA_IH_UNITS_AND_CORRECTIONS",
        ),
        (
            "PACK3717_3_F1_total_bound",
            "||F_1,total||",
            "<= ||R_odd,F1|| + ||B_boundary,F1||",
            "action per fibre coordinate",
            "finite nonclaim branch if exact force zero is not signed",
            "DERIVED_BOUND",
        ),
        (
            "PACK3717_4_BQK_total_bound",
            "||B_QK,total||",
            "<= ||R_odd,BQK|| + ||B_boundary,QK||",
            "local Hessian/operator units",
            "finite nonclaim branch feeding epsilon_LP",
            "DERIVED_BOUND",
        ),
        (
            "PACK3717_5_epsilon_LP_update",
            "epsilon_LP",
            "<= ||B_QK,total|| + ||B_KQ,total|| + ||B_boundary,QK||",
            "local Hessian/operator units",
            "safe update for 3716/3715 dynamic leakage",
            "DERIVED_LINK_TO_3716",
        ),
    ]
    return [
        {
            **base(timestamp),
            "pack_id": row_id,
            "quantity": quantity,
            "formula_or_value": formula,
            "units": units,
            "use": use,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, quantity, formula, units, use, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3717_0_family_not_point", "The correct zero theorem is a zero-section family extremum F_z(q)=0 over the local patch, not a point condition F_z(q0)=0.", "Only the family identity differentiates to B_QK=0 without tuning.", "FAMILY_EXTREMUM_REQUIREMENT_ADOPTED"),
        ("DEC3717_1_Fisher_route", "The Fisher/KL bath core supplies a real candidate parent route for F_1=0 and B_QK=0 while keeping a positive gap.", "This is the first non-smuggled path where local matter silence and local mass gap can coexist.", "FISHER_FIBRE_CORE_ROUTE_SELECTED"),
        ("DEC3717_2_retained_corrections", "Odd correction and boundary mixed terms are retained explicitly rather than assumed absent.", "This prevents the fibre normal form from becoming a disguised closure axiom.", "CORRECTION_ROWS_RETAINED"),
        ("DEC3717_3_next", "Next target should own or bound Theta_H, I_H, R_odd, and boundary mixed rows so M_K and epsilon_LP become executable.", "That moves the derivation from formal normal form to numeric/source-backed local screening tests.", "ADVANCE_TO_FISHER_GAP_INPUT_OWNER"),
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
        ("CG3717_0_zero_section", "local q,z zero-section family is parent-owned over an open q patch"),
        ("CG3717_1_Fisher_core", "p_z, p_0, Theta_H, and I_H are parent-owned with units"),
        ("CG3717_2_gap", "M_K=Theta_H I_H plus corrections is positive and matched to m_K_or_Xi_H"),
        ("CG3717_3_corrections", "R_odd,F1 and R_odd,BQK are theorem-zero or finite source-backed rows"),
        ("CG3717_4_boundary", "boundary F1 and boundary mixed Hessian are theorem-zero or finite source-backed rows"),
        ("CG3717_5_public", "F_1/B_QK block diagonal local dynamics claim allowed"),
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
            "status_id": "STATUS3717_0",
            "status": "F1_BQK_REDUCED_TO_ZERO_SECTION_FAMILY_AND_FISHER_KL_CORE_NONCLAIM",
            "summary": (
                "3717 sharpens the F_1/B_QK target: point extremum is insufficient, but a parent-owned zero-section family F_z(q)=0 implies B_QK=partial_q F_z=0. "
                "The Fisher/KL fibre core from 3708 gives F_1=0, B_QK=0, and M_K=Theta_H I_H conditionally, while odd corrections and boundary mixed terms are retained as explicit nonclaim rows."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3717_0",
            "target_doc": "3718-Y5-R2FR-Fisher-fibre-gap-input-owner-Theta-IH-corrections.md",
            "target_script": "scripts/Y5_R2FR_3718_Fisher_fibre_gap_input_owner_Theta_IH_corrections.py",
            "objective": "try to source-own Theta_H, I_H, and the retained correction/boundary rows so M_K, F_1,total, B_QK,total, and epsilon_LP become executable local screening inputs",
            "success_gate": "Theta_H/I_H/gap inputs are either parent-owned or retained as explicit finite nonclaim rows with units and local arena impact",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    zero_sections: list[dict[str, object]],
    fisher_routes: list[dict[str, object]],
    corrections: list[dict[str, object]],
    theorems: list[dict[str, object]],
    packs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3717 Y5 R2FR Fibre Normal Form F1 Zero And BQK Mixed Hessian Owner",
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
        "- A point condition `F_z(q0)=0` is not enough; the needed clause is a zero-section family `F_z(q)=0` over the local observed patch.",
        "- Then `B_QK(q)=partial_q partial_z S_parent(q,0)=partial_q F_z(q)=0` follows by differentiating the family identity.",
        "- The Fisher/KL fibre core gives exactly that structure: `D_KL(p_z||p_0)=0.5 I_AB(q) z^A z^B+O(||z||^3)` has no linear z term.",
        "- Therefore the core gives `F_1,core=0`, `B_QK,core=0`, and `M_K,core=Theta_H I_H` without sacrificing the local mass gap.",
        "- Odd correction rows and boundary mixed rows remain explicit nonclaim coefficients.",
        "- `valid_for_claim=false`: the derivation route is sharper, but parent ownership of the bath, scale, units, and retained corrections is still required.",
        "",
        "## Zero-Section Family",
        "",
    ]
    for row in zero_sections:
        lines.append(f"- `{row['zero_section_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Fisher/KL Route", ""])
    for row in fisher_routes:
        lines.append(f"- `{row['fisher_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Retained Corrections", ""])
    for row in corrections:
        lines.append(f"- `{row['correction_id']}` `{row['quantity']}`: `{row['formula_or_value']}` | {row['status']} | {row['use']}")
    lines.extend(["", "## Theorems", ""])
    for row in theorems:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} | gap: {row['remaining_gap']}")
    lines.extend(["", "## Coefficient Pack", ""])
    for row in packs:
        lines.append(f"- `{row['pack_id']}` `{row['quantity']}`: `{row['formula_or_value']}` | {row['status']} | {row['use']}")
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
    zero_sections: list[dict[str, object]],
    fisher_routes: list[dict[str, object]],
    corrections: list[dict[str, object]],
    theorems: list[dict[str, object]],
    packs: list[dict[str, object]],
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
    zero_text = "\n".join(str(row["formula"]) for row in zero_sections)
    checks.append(("family_extremum", "family extremum and point warning are present", "F_z(q)=0 for every q" in zero_text and "F_z(q0)=0 alone" in zero_text, ""))
    fish_text = "\n".join(str(row["formula"]) for row in fisher_routes)
    checks.append(("fisher_core", "Fisher/KL F1 and BQK zero core rows are present", "partial_z [Theta_H D_KL]|_{z=0}=0" in fish_text and "partial_q partial_z [Theta_H D_KL]|_{z=0}=partial_q 0=0" in fish_text, ""))
    correction_quantities = {row["quantity"] for row in corrections}
    checks.append(("correction_rows", "odd and boundary retained correction rows are present", {"R_odd,F1", "R_odd,BQK", "B_boundary,F1", "B_boundary,QK"} <= correction_quantities, ""))
    theorem_text = "\n".join(str(row["statement"]) for row in theorems)
    checks.append(("theorems", "family and Fisher core theorems are present", "F_z(q)=0" in theorem_text and "Fisher/KL fibre core" in theorem_text, ""))
    pack_quantities = {row["quantity"] for row in packs}
    checks.append(("coefficient_pack", "F1/BQK core and total bound rows are present", {"F_1,core", "B_QK,core", "M_K,core", "||F_1,total||", "||B_QK,total||", "epsilon_LP"} <= pack_quantities, ""))
    checks.append(("nonclaim_decisions", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3718", "next target advances to Fisher gap input owner", str(next_target[0]["target_doc"]).startswith("3718-") and "Fisher" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core 3717 terms", all(term in doc_text for term in ["F_z(q)=0", "B_QK(q)=partial_q", "F_1,core=0", "Odd correction", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3717*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3717 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
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
    zero_sections = zero_section_rows(timestamp)
    fisher_routes = fisher_route_rows(timestamp)
    corrections = correction_rows(timestamp)
    theorems = theorem_rows(timestamp)
    packs = coefficient_pack_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3717_SOURCE_REGISTER.csv",
        "zero_sections": RESIDUALS / "P8_Y5_R2FR_3717_ZERO_SECTION_FAMILY_ROWS.csv",
        "fisher_routes": RESIDUALS / "P8_Y5_R2FR_3717_FISHER_KL_CORE_ROWS.csv",
        "corrections": RESIDUALS / "P8_Y5_R2FR_3717_RETAINED_CORRECTION_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3717_THEOREM_ROWS.csv",
        "packs": RESIDUALS / "P8_Y5_R2FR_3717_COEFFICIENT_PACK_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3717_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3717_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3717_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3717_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3717_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["zero_sections"], zero_sections)
    write_csv(outputs["fisher_routes"], fisher_routes)
    write_csv(outputs["corrections"], corrections)
    write_csv(outputs["theorems"], theorems)
    write_csv(outputs["packs"], packs)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, zero_sections, fisher_routes, corrections, theorems, packs, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, zero_sections, fisher_routes, corrections, theorems, packs, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3717 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3717 checkpoint: F1/BQK reduced to zero-section family and Fisher/KL fibre core")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
