from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
DOC = ROOT / "2018-Y5-R2FR-Aframe-source-boundary-action-PiA-zero-or-finite-PiA-source-prior.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_rows_parse(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def md_cell(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    try:
        result = subprocess.run(
            ["git", "-C", str(FORMALIZATION), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2018_00_2017_handoff",
            ROOT / "2017-Y5-R2FR-Aframe-split-gauge-generator-boundary-charge-zero-or-finite-A-source-row.md",
            ["NEXT2017_0_2018", "SGG2017_3_boundary_charge", "VAL2017_OVERALL"],
            "2017 handoff to source-boundary Pi_A zero or finite source-prior row.",
        ),
        (
            "SRC2018_01_2010_no_spurion",
            ROOT / "2010-Y5-R2FR-Aframe-parent-source-map-rank-certificate-or-residual-coefficient-source-pack.md",
            ["NSP2010_0_matter_functor", "NSP2010_5_boundary_source_measure", "NSP2010_6_verdict"],
            "A-frame ordinary matter/source no-spurion clauses.",
        ),
        (
            "SRC2018_02_2012_PiA_rows",
            ROOT / "2012-Y5-R2FR-Aframe-current-nohair-source-neutrality-theorem-or-finite-QA-row.md",
            ["NHA2012_0_target", "FQA2012_1_PiA", "DEC2012_1_best_derivation_route"],
            "finite Pi_A/Q_A rows and source-neutrality target.",
        ),
        (
            "SRC2018_03_2013_boundary_attempt",
            ROOT / "2013-Y5-R2FR-Aframe-finite-QA-bound-source-acquisition-or-boundary-neutrality-proof.md",
            ["BNA2013_1_variation_formula", "BNA2013_3_fixed_boundary_risk", "VAL2013_OVERALL"],
            "prior boundary/source neutrality attempt and countermodel.",
        ),
        (
            "SRC2018_04_410_functor",
            ROOT / "410-quotient-matter-functor-theorem-attempt.md",
            ["S_matter = sum_A S_A", "delta S_matter / delta Z_I", "local_GR_promoted"],
            "early quotient matter functor theorem and counterexample warning.",
        ),
        (
            "SRC2018_05_1045_functor",
            ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
            ["MFS1045_0_parent_field_quotient", "VLG1045_3_boundary_lift", "DEC1045_0_theorem_shape"],
            "matter functor descent signature and boundary-lift gap.",
        ),
        (
            "SRC2018_06_767_reaudit",
            OUT / "P8_Y5_R10_767_PARENT_MATTER_FUNCTOR_REAUDIT.csv",
            ["PMR767_0_explicit_parent_matter_functor", "PMR767_5_domain_selection_predata"],
            "parent matter functor reaudit.",
        ),
        (
            "SRC2018_07_HSM541_source_measure",
            OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            ["HSM541_1_integrable_charge", "HSM541_2_observed_worldtube_source", "HSM541_4_zero_extra_source_channels"],
            "Hamiltonian/source-measure contract.",
        ),
        (
            "SRC2018_08_667_boundary_action",
            OUT / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
            ["PBA667_2_boundary_action", "PBA667_3_charge_definition", "PBA667_5_denominator_rule"],
            "parent boundary-action ansatz and charge definition.",
        ),
        (
            "SRC2018_09_671_boundary_gate",
            OUT / "P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
            ["BCG671_1_proper_gauge", "BCG671_5_boundary_cocycle", "BCG671_7_verdict"],
            "boundary charge owner/proper/exact/cocycle gates.",
        ),
        (
            "SRC2018_10_reciprocal_neutrality",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["Pi_R = 0 -> Q_R = 0", "fixed source R_AB boundary", "Q_R neutrality is the missing source theorem"],
            "analogy showing source momentum zero is a real source theorem, not a conservation shortcut.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def boundary_action_rows() -> list[dict[str, object]]:
    data = [
        {
            "attempt_id": "SBA2018_0_source_action_domain",
            "object": "parent source/boundary action",
            "formula": "S_source+boundary = S_src[Psi,e,omega[e],theta] + B_GR[e] + B_ref + B_extra",
            "status": "CONDITIONAL_E_ONLY_SOURCE_GRAMMAR",
            "derivation": "if no direct X/A/Phi_MTS/q_loc/source-marker argument exists, visible matter is split-gauge invariant.",
            "why_not_claim": "the actual parent source/boundary action and B_extra exclusion are not signed.",
            "claim_result": "nonclaim",
        },
        {
            "attempt_id": "SBA2018_1_variation_split",
            "object": "source variation under e=dX+A",
            "formula": "delta S_src = int_W E_e^a_mu delta e_a^mu + int_partialW Pi_e^{n a} delta e_a + ... with delta e = d(delta X)+delta A",
            "status": "CHAIN_RULE_FORM_DERIVED_CONDITIONAL",
            "derivation": "A variation at fixed X pulls back to the tetrad/coframe variation.",
            "why_not_claim": "Pi_e and boundary terms require the parent symplectic/source measure.",
            "claim_result": "nonclaim",
        },
        {
            "attempt_id": "SBA2018_2_total_PiA_identity",
            "object": "total A normal momentum",
            "formula": "Pi_A^{n a,total} = Pi_e^{n a} + Pi_A^{n a,extra} + Pi_A^{n a,edge}",
            "status": "TOTAL_PIA_IS_NOT_THE_RIGHT_ZERO_TARGET",
            "derivation": "in the e-only branch Pi_A inherits the ordinary tetrad/Hilbert source momentum.",
            "why_not_claim": "ordinary compact mass sources should have a nonzero GR/Hilbert source momentum.",
            "claim_result": "do_not_set_total_PiA_to_zero",
        },
        {
            "attempt_id": "SBA2018_3_split_charge_cancellation",
            "object": "combined split transformation",
            "formula": "delta_epsilon X=epsilon, delta_epsilon A=-D epsilon, delta_epsilon e=0, so delta_epsilon S_src=0 inside e-only grammar",
            "status": "SPLIT_INVARIANCE_NOT_TOTAL_CHARGE_ZERO",
            "derivation": "the X and A variations cancel in the public tetrad channel.",
            "why_not_claim": "cancellation of the combined generator does not imply Pi_A^{n,total}=0.",
            "claim_result": "nonclaim",
        },
        {
            "attempt_id": "SBA2018_4_residual_charge_target",
            "object": "extra A charge after GR source subtraction",
            "formula": "Pi_A^{n,res} := Pi_A^{n,total} - Pi_e^{n,GR/Hamiltonian}[M_H,e_pub] - Pi_A^{n,proper/exact}",
            "status": "CORRECT_ZERO_TARGET_IDENTIFIED",
            "derivation": "local GR needs no extra A hair beyond the measured GR/Hamiltonian source charge, not zero total source momentum.",
            "why_not_claim": "the GR/Hamiltonian subtraction map and exact/proper boundary class are not parent-owned yet.",
            "claim_result": "residual_zero_target_nonclaim",
        },
        {
            "attempt_id": "SBA2018_5_matter_functor_implication",
            "object": "no-spurion matter/source silence",
            "formula": "partial_A_direct S_src|e = 0 and partial_marker S_src = 0 if matter functor is strictly public-frame only",
            "status": "DIRECT_SPURION_SOURCE_BLOCKED_CONDITIONALLY",
            "derivation": "e-only/no-marker grammar kills direct representative-field source coupling.",
            "why_not_claim": "1045/767 keep matter functor and boundary lift unsigned.",
            "claim_result": "nonclaim",
        },
        {
            "attempt_id": "SBA2018_6_Kboundary_residual",
            "object": "boundary cocycle after source subtraction",
            "formula": "K_boundary^{A,res}=K_boundary^{A,total}-K_boundary^{GR/Hamiltonian}-K_boundary^{proper/exact}",
            "status": "RESIDUAL_COCYCLE_TARGET_IDENTIFIED",
            "derivation": "bulk split shifts are abelian; only boundary/source/reference terms can leave an obstruction.",
            "why_not_claim": "the parent bracket, Q_A differentiability, and reference subtraction are missing.",
            "claim_result": "nonclaim",
        },
        {
            "attempt_id": "SBA2018_7_counterexample",
            "object": "ordinary massive e-only source",
            "formula": "S_src=-m int ds[e] is split-invariant but delta S_src/delta A = delta S_src/delta e is not zero",
            "status": "COUNTEREXAMPLE_TO_TOTAL_PIA_ZERO",
            "derivation": "a source can be perfectly public-frame-only and still carry the GR stress/mass source.",
            "why_not_claim": "therefore Pi_A^{total}=0 is too strong and would erase Newtonian mass.",
            "claim_result": "blocks_total_zero_shortcut",
        },
        {
            "attempt_id": "SBA2018_8_verdict",
            "object": "source-boundary Pi_A zero theorem",
            "formula": "Pi_A^{n,res}=0 and K_boundary^{A,res}=0 are the viable local-GR targets; Pi_A^{n,total}=0 is rejected",
            "status": "TOTAL_ZERO_REJECTED_RESIDUAL_ZERO_NOT_SIGNED",
            "derivation": "the route now separates GR/Newton source charge from extra A hair.",
            "why_not_claim": "residual subtraction, source normalization, boundary exactness, and matter functor descent are still unsigned.",
            "claim_result": "finite_residual_rows_retained",
        },
    ]
    rows = []
    for item in data:
        row = base_row()
        row.update({**item, "parent_signed": False})
        rows.append(row)
    return rows


def residual_source_prior_rows() -> list[dict[str, object]]:
    data = [
        ("PR2018_0_PiA_total", "Pi_A^{n,total}", "normal A momentum at source/boundary", "NOT_ZERO_TARGET_GR_SOURCE_INCLUDED", "MISSING", "action/A/area"),
        ("PR2018_1_PiA_GR", "Pi_e^{n,GR/Hamiltonian}", "ordinary tetrad/Hamiltonian source momentum to be absorbed into measured mass", "MISSING_GR_SOURCE_SUBTRACTION_MAP", "MISSING", "action/e/area"),
        ("PR2018_2_PiA_res", "Pi_A^{n,res}", "extra A source momentum after GR/proper/exact subtraction", "CORRECT_ZERO_OR_BOUND_TARGET", "MISSING", "action/A/area"),
        ("PR2018_3_QA_res", "Q_A^{res}[epsilon]", "int_partial epsilon_a Pi_A^{n,res a} plus residual improvements", "MISSING_RESIDUAL_BOUNDARY_CHARGE", "MISSING", "A-charge"),
        ("PR2018_4_Kboundary_res", "K_boundary^{A,res}", "residual split-gauge boundary cocycle", "MISSING_RESIDUAL_BRACKET", "MISSING", "charge algebra units"),
        ("PR2018_5_MH_normalization", "M_H_ref", "measured Hamiltonian/Noether mass denominator used to remove GR source charge", "MISSING_SOURCE_NORMALIZATION", "MISSING", "mass"),
        ("PR2018_6_alphaA_res", "alpha_A^{res}(lambda_A)", "R10 Yukawa-equivalent amplitude from residual A hair only", "MISSING_ZA_KAPPA_LAMBDA_P00_PROFILE", "MISSING", "dimensionless"),
        ("PR2018_7_PPN_res", "delta_PPN_A^{res}", "PPN residual vector after GR source subtraction", "MISSING_ARENA_PROJECTION", "MISSING", "dimensionless"),
    ]
    rows = []
    for row_id, symbol, meaning, status, value, units in data:
        row = base_row()
        row.update(
            {
                "prior_id": row_id,
                "symbol": symbol,
                "meaning": meaning,
                "status": status,
                "numeric_value": value,
                "units": units,
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2018_0_total_zero_rejected", "total Pi_A zero is rejected as a GR-source eraser", True, "ordinary e-only mass sources can have nonzero Pi_A=Pi_e"),
        ("CG2018_1_residual_target_written", "Pi_A residual zero target is explicit", True, "Pi_A_res = Pi_A_total - Pi_GR/Hamiltonian - proper/exact pieces"),
        ("CG2018_2_matter_functor_sufficient", "matter functor alone proves Pi_A_res=0", False, "functor kills direct spurions, not boundary/source/reference residuals"),
        ("CG2018_3_PiA_res_zero", "Pi_A_res=0 is parent-derived", False, "GR subtraction map, source normalization, and boundary exactness are unsigned"),
        ("CG2018_4_Kboundary_res_zero", "K_boundary_A_res=0 is parent-derived", False, "boundary bracket/reference subtraction are not computed"),
        ("CG2018_5_finite_residual_score", "finite residual A source row is score-ready", False, "numeric/source-backed residual coefficients missing"),
        ("CG2018_6_local_GR_Newton", "local GR/Newton reduction from A branch is derived", False, "residual zero theorem remains unsigned"),
    ]
    rows = []
    for gate_id, gate, passed_for_nonclaim, reason in data:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "passed_for_nonclaim": passed_for_nonclaim,
                "passed_for_claim": False,
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2018_0_total_PiA_zero", "claim Pi_A^{total}=0", "REFUSE", "would erase ordinary GR/Newton source momentum for e-only massive matter; correct target is residual Pi_A."),
        ("REF2018_1_matter_functor_zero", "claim no-spurion matter functor proves source-boundary zero", "REFUSE", "it blocks direct spurions but does not compute boundary momentum, source normalization, or exact/proper charge."),
        ("REF2018_2_residual_zero", "claim Pi_A^{res}=0", "REFUSE", "GR/Hamiltonian subtraction map, M_H_ref, boundary exactness, and K_boundary residual are unsigned."),
        ("REF2018_3_finite_residual_score", "score finite A residual", "REFUSE", "Pi_A_res, Q_A_res, Z_A, lambda_A, kappa_A, P_00, and arena projections are missing."),
        ("REF2018_4_local_GR", "claim local GR/Newton derivation", "REFUSE", "A branch is sharper but residual source theorem is not closed."),
    ]
    rows = []
    for refusal_id, attempted_claim, verdict, reason in data:
        row = base_row()
        row.update(
            {
                "refusal_id": refusal_id,
                "attempted_claim": attempted_claim,
                "verdict": verdict,
                "reason": reason,
                "accepted_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2018_0_result",
            "TOTAL_PIA_ZERO_REJECTED_RESIDUAL_PIA_TARGET_IDENTIFIED",
            "The source-boundary action attempt shows that total Pi_A should include the ordinary tetrad/Hilbert source momentum in the e-only branch. Killing total Pi_A would also kill the Newtonian source.",
            "target Pi_A_res and K_boundary_A_res, not total Pi_A",
        ),
        (
            "DEC2018_1_actual_progress",
            "A_COUPLING_BOTTLENECK_IS_NOW_A_GR_SOURCE_SUBTRACTION_PROBLEM",
            "The correct local-GR question is whether the A boundary charge is only the GR/Hamiltonian mass source or whether an extra residual A charge remains.",
            "derive the GR-source decomposition and no-double-count projector next",
        ),
        (
            "DEC2018_2_testing_status",
            "FINITE_A_TESTING_REMAINS_BLOCKED_BUT_BETTER_NORMALIZED",
            "Future R10/PPN rows must use residual A hair after measured-mass normalization, not total source momentum.",
            "do not score A residuals until Pi_A_res, M_H_ref, and projection coefficients are real",
        ),
    ]
    rows = []
    for decision_id, verdict, rationale, next_action in data:
        row = base_row()
        row.update({"decision_id": decision_id, "verdict": verdict, "rationale": rationale, "next_action": next_action})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2018_0_2019",
            "next_doc": "2019-Y5-R2FR-Aframe-GR-source-decomposition-PiAres-zero-or-residual-normalization.md",
            "objective": "derive the decomposition Pi_A_total = Pi_GR/Hamiltonian + Pi_A_res + proper/exact boundary terms, prove Pi_A_res=0 and K_boundary_A_res=0 if possible, or build residual-normalized finite A rows",
            "required_inputs": "GR/tetrad source momentum; Hamiltonian mass M_H_ref; public tetrad source measure; boundary exact/proper class; K_boundary residual bracket; no-double-count projector; Pi_A_res units; R10/PPN residual routing",
            "excluded": "total Pi_A zero shortcut; matter-functor-only zero; measured mass double counting; invented residual coefficients; R10/local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update({"copy_id": f"COPY2018_{idx}", "path": str(path), "exists": path.exists(), "note": note})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    boundary: list[dict[str, object]],
    priors: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2018_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"))
    checks.append(("VAL2018_01_total_zero_rejected", any(row["attempt_id"] == "SBA2018_2_total_PiA_identity" and row["status"] == "TOTAL_PIA_IS_NOT_THE_RIGHT_ZERO_TARGET" for row in boundary), "total Pi_A zero shortcut is rejected"))
    checks.append(("VAL2018_02_residual_target_written", any(row["attempt_id"] == "SBA2018_4_residual_charge_target" and "Pi_A^{n,res}" in row["formula"] for row in boundary), "Pi_A residual target is explicit"))
    checks.append(("VAL2018_03_counterexample_present", any(row["attempt_id"] == "SBA2018_7_counterexample" for row in boundary), "e-only massive source counterexample blocks total-zero overclaim"))
    checks.append(("VAL2018_04_verdict_nonclaim", any(row["attempt_id"] == "SBA2018_8_verdict" and row["status"] == "TOTAL_ZERO_REJECTED_RESIDUAL_ZERO_NOT_SIGNED" for row in boundary), "residual zero not falsely promoted"))
    checks.append(("VAL2018_05_priors_nonclaim", all(row["score_ready"] is False and row["numeric_value"] == "MISSING" for row in priors), "residual source-prior rows remain missing/nonclaim"))
    checks.append(("VAL2018_06_claim_gates_blocked", all(row["passed_for_claim"] is False for row in claim_gates), "all claim gates remain blocked"))
    checks.append(("VAL2018_07_refusals_active", all(row["verdict"] == "REFUSE" and row["accepted_for_claim"] is False for row in refusals), "refusals remain active"))
    checks.append(("VAL2018_08_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"))
    checks.append(("VAL2018_09_branch_copies", all(path.exists() and csv_rows_parse(path) for path in branch_paths), "branch-copy CSVs exist and parse"))
    checks.append(("VAL2018_10_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"))
    checks.append(("VAL2018_11_output_scope", all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in output_paths + branch_paths + [DOC]), "all outputs are under post-checkpoint-work"))
    overall = all(passed for _, passed, _ in checks)
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    row = base_row()
    row.update(
        {
            "check_id": "VAL2018_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2018 A-frame source-boundary action Pi_A zero or finite Pi_A source prior",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    boundary: list[dict[str, object]],
    priors: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    parts = [
        "# 2018 Y5 R2FR: A-Frame Source-Boundary Action PiA Zero Or Finite PiA Source Prior\n",
        "Private checkpoint. This tests whether the source/boundary action kills the A-frame boundary charge, or whether finite A source rows must be retained.\n",
        "## Current Verdict\n",
        "The target changes in an important way. The total `Pi_A^n` should **not** be forced to zero. In the strict e-only branch, varying `A` at fixed `X` is just varying the public tetrad, so `Pi_A^{n,total}` inherits the ordinary tetrad/Hilbert source momentum. A compact mass source should carry that; otherwise we erase the Newtonian source itself.\n",
        "The correct local-GR zero theorem is therefore residual: split `Pi_A^{n,total}=Pi_GR/Hamiltonian^n + Pi_A^{n,res} + proper/exact boundary pieces`. The GR/Hamiltonian piece is the measured mass source. The object that must vanish or be bounded is `Pi_A^{n,res}` and its cocycle `K_boundary^{A,res}`.\n",
        "This is a genuine route improvement: the coupling bottleneck is no longer just 'missing coupling'. It is now a source-normalization/no-double-count problem. No local-GR/R10/PPN claim is made yet because the residual decomposition and Hamiltonian normalization are still unsigned.\n",
        "## Source Register\n",
        md_table(sources, ["source_id", "source_path", "status", "needles", "note"]),
        "## Source-Boundary Action Audit\n",
        md_table(boundary, ["attempt_id", "object", "formula", "status", "derivation", "why_not_claim", "claim_result", "parent_signed"]),
        "## Residual Source-Prior Rows\n",
        md_table(priors, ["prior_id", "symbol", "meaning", "status", "numeric_value", "units", "score_ready", "valid_for_claim"]),
        "## Claim Gates\n",
        md_table(claim_gates, ["gate_id", "gate", "passed_for_nonclaim", "passed_for_claim", "reason"]),
        "## Refusal Runner\n",
        md_table(refusals, ["refusal_id", "attempted_claim", "verdict", "reason", "accepted_for_claim"]),
        "## Decision Ledger\n",
        md_table(decisions, ["decision_id", "verdict", "rationale", "next_action"]),
        "## Branch Copies\n",
        md_table(branch_copies, ["copy_id", "path", "exists", "note"]),
        "## Next Target\n",
        md_table(next_target, ["target_id", "next_doc", "objective", "required_inputs", "excluded"]),
        "## Validation\n",
        md_table(validation, ["check_id", "status", "detail"]),
    ]
    DOC.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    boundary = boundary_action_rows()
    priors = residual_source_prior_rows()
    claim_gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2018_SOURCE_REGISTER.csv",
        "boundary": OUT / "P8_Y5_PARENT_QLOC_2018_AFRAME_SOURCE_BOUNDARY_ACTION_AUDIT.csv",
        "priors": OUT / "P8_Y5_PARENT_QLOC_2018_AFRAME_RESIDUAL_SOURCE_PRIOR_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2018_CLAIM_GATE.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2018_REFUSAL_RUNNER.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2018_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2018_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["boundary"], boundary)
    write_csv(output_map["priors"], priors)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["refusals"], refusals)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_SOURCE_BOUNDARY_PIA_2018_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2018_AFRAME_PIA_RESIDUAL_STATUS_NONCLAIM.csv",
        QUEUE / "JR2018_AFRAME_PIA_RESIDUAL_SOURCE_PRIOR_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["boundary"], branch_paths[0])
    shutil.copyfile(output_map["claim_gates"], branch_paths[1])
    shutil.copyfile(output_map["priors"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame source-boundary Pi_A audit nonclaim copy",
            "A-frame Pi_A residual claim-gate status nonclaim copy",
            "A-frame Pi_A residual source-prior queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2018_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, boundary, priors, claim_gates, refusals, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2018_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, boundary, priors, claim_gates, refusals, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2018_OVERALL"][0]["status"]
    print(f"VAL2018_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
