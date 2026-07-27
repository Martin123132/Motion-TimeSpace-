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
DOC = ROOT / "2019-Y5-R2FR-Aframe-GR-source-decomposition-PiAres-zero-or-residual-normalization.md"
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
            "SRC2019_00_2018_handoff",
            ROOT / "2018-Y5-R2FR-Aframe-source-boundary-action-PiA-zero-or-finite-PiA-source-prior.md",
            ["NEXT2018_0_2019", "SBA2018_4_residual_charge_target", "VAL2018_OVERALL"],
            "2018 handoff to GR-source decomposition and residual normalization.",
        ),
        (
            "SRC2019_01_2017_generator",
            ROOT / "2017-Y5-R2FR-Aframe-split-gauge-generator-boundary-charge-zero-or-finite-A-source-row.md",
            ["SGG2017_2_constraint_candidate", "SGG2017_3_boundary_charge", "VAL2017_OVERALL"],
            "A split generator and total boundary charge skeleton.",
        ),
        (
            "SRC2019_02_1017_reference_lock",
            ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
            ["HRL1017_5_MHref_denominator", "MHR1017_0_M_H_ref_denominator", "DEC1017_1_no_MHref_shortcut"],
            "Hamiltonian source denominator and no-shortcut guard.",
        ),
        (
            "SRC2019_03_1014_projector",
            ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            ["PCT1014_0_product_rule", "PCT1014_2_commutator_zero", "DEC1014_1_Hodge_route_retained"],
            "Pi_M commutator/projector variation obstruction.",
        ),
        (
            "SRC2019_04_1015_hilbert",
            ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
            ["SOL1015_1_source_measure", "SOL1015_3_de_rham_equality", "REB1015_5_M_H_ref"],
            "same Hilbert source measure and source equality conditions.",
        ),
        (
            "SRC2019_05_1019_boundary_projector",
            ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            ["PO1019_0_projector_definition", "DC1019_0_orthogonal_split", "DEC1019_1_best_route"],
            "boundary exactness, projector orthogonality, and no-double-count guard.",
        ),
        (
            "SRC2019_06_2018_audit_csv",
            OUT / "P8_Y5_PARENT_QLOC_2018_AFRAME_SOURCE_BOUNDARY_ACTION_AUDIT.csv",
            ["SBA2018_2_total_PiA_identity", "SBA2018_8_verdict"],
            "2018 source-boundary action audit CSV.",
        ),
        (
            "SRC2019_07_2018_prior_csv",
            OUT / "P8_Y5_PARENT_QLOC_2018_AFRAME_RESIDUAL_SOURCE_PRIOR_ROWS.csv",
            ["PR2018_2_PiA_res", "PR2018_5_MH_normalization"],
            "2018 residual source-prior rows.",
        ),
        (
            "SRC2019_08_1017_reference_csv",
            OUT / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv",
            ["HRL1017_5_MHref_denominator", "HRL1017_6_FB5540_zero_law"],
            "reference lock law CSV.",
        ),
        (
            "SRC2019_09_671_boundary_gate",
            OUT / "P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
            ["BCG671_4_projector_orthogonality", "BCG671_6_no_double_count", "BCG671_7_verdict"],
            "boundary charge owner, projector, and no-double-count gates.",
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


def decomposition_rows() -> list[dict[str, object]]:
    data = [
        {
            "decomp_id": "GSD2019_0_total_charge",
            "object": "total A split charge",
            "formula": "Q_A^total[epsilon]=int_partialSigma epsilon_a Pi_A^{n a,total} + improvement_total",
            "status": "TOTAL_CHARGE_FORM_INHERITED_FROM_2017",
            "derivation": "2017 gives the split generator boundary term.",
            "missing_before_claim": "total charge contains GR source and residual pieces; it is not a zero target.",
        },
        {
            "decomp_id": "GSD2019_1_GR_source_piece",
            "object": "GR/Hamiltonian source piece",
            "formula": "Q_A^GR[epsilon] := Pi_GR/H[Q_A^total] = delta_epsilon H_tau^GR[e_pub,psi]/delta epsilon with M_H_ref = G_ref^-1 int_S Q_tau",
            "status": "CONDITIONAL_DEFINITION_NOT_PARENT_SIGNED",
            "derivation": "if e=dX+A and matter is public-frame-only, the A variation pulls back to the tetrad/Hilbert source charge.",
            "missing_before_claim": "stable M_H_ref, tau lock, source worldtube, and fixed reference remain unsigned.",
        },
        {
            "decomp_id": "GSD2019_2_proper_exact_piece",
            "object": "proper/exact boundary piece",
            "formula": "Q_A^proper/exact[epsilon]=0 for epsilon|partial=0 or Q_A=d_boundary b_A with fixed closed boundary and no kernel derivative term",
            "status": "CONDITIONAL_BOUNDARY_EXACTNESS_ONLY",
            "derivation": "proper gauge and exact boundary forms are the legitimate zero channels.",
            "missing_before_claim": "boundary class, cohomology, corner terms, kernel derivative terms, and counterterms are not parent-signed.",
        },
        {
            "decomp_id": "GSD2019_3_residual_definition",
            "object": "residual A source charge",
            "formula": "Q_A^res := Q_A^total - Q_A^GR - Q_A^proper/exact; Pi_A^{n,res} defined by Q_A^res=int_partial epsilon_a Pi_A^{n a,res}+improvements",
            "status": "RESIDUAL_DEFINITION_DERIVED_AS_BOOKKEEPING",
            "derivation": "this isolates extra A hair after measured GR source charge and pure gauge/exact pieces are removed.",
            "missing_before_claim": "bookkeeping identity is not a zero theorem; each subtracted piece must be parent-owned.",
        },
        {
            "decomp_id": "GSD2019_4_cocycle_decomposition",
            "object": "residual boundary cocycle",
            "formula": "K_A^res = K_A^total - K_A^GR/Hamiltonian - K_A^proper/exact",
            "status": "RESIDUAL_COCYCLE_DEFINITION_DERIVED_AS_BOOKKEEPING",
            "derivation": "bulk split shifts are abelian, so any surviving obstruction is boundary/source/reference residue.",
            "missing_before_claim": "bracket computation and reference/counterterm silence are missing.",
        },
        {
            "decomp_id": "GSD2019_5_no_double_count_projector",
            "object": "no-double-count source projector",
            "formula": "Pi_GR/H[Q_A^res]=0 and Pi_res[Q_A^GR]=0 with Q_total=Q_GR orthogonal_sum Q_res orthogonal_sum Q_exact",
            "status": "PROJECTOR_ORTHOGONALITY_REQUIRED_NOT_DERIVED",
            "derivation": "residual A hair must not be counted once as measured mass and again as fifth-force hair.",
            "missing_before_claim": "Pi_M^H definition, symplectic block, reference silence, and source/edge independence are unsigned.",
        },
        {
            "decomp_id": "GSD2019_6_zero_theorem_contract",
            "object": "Pi_A_res zero theorem",
            "formula": "Pi_A^{res}=0 and K_A^{res}=0 if public-frame source measure, M_H_ref, exact/proper boundary class, and projector orthogonality all close",
            "status": "VALID_CONDITIONAL_THEOREM_CONTRACT",
            "derivation": "this is the local-GR route: all A boundary charge is either measured GR source or pure gauge/exact.",
            "missing_before_claim": "the required clauses are spread across unsigned 1017, 1019, 1045, and 2018 gates.",
        },
        {
            "decomp_id": "GSD2019_7_finite_residual_fallback",
            "object": "residual-normalized finite A branch",
            "formula": "alpha_A^res(lambda)=K_A(lambda) Qbar_AH^res(lambda) qbar_AT /(4*pi*Z_A*G_ref) plus absolute tails, normalized by M_H_ref",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "derivation": "if residual zero fails, compare only the residual source charge, not total measured mass.",
            "missing_before_claim": "Z_A, lambda_A, K_A, Qbar_AH^res, qbar_AT, M_H_ref, and promoted bound rows are missing.",
        },
        {
            "decomp_id": "GSD2019_8_verdict",
            "object": "GR-source decomposition for A-frame residual",
            "formula": "Q_A^total=Q_A^GR+Q_A^proper/exact+Q_A^res and only Q_A^res is test/fifth-force material",
            "status": "DECOMPOSITION_WRITTEN_RESIDUAL_ZERO_NOT_SIGNED",
            "derivation": "the A-coupling problem is now a no-double-count residual source-normalization problem.",
            "missing_before_claim": "M_H_ref, projector orthogonality, exact boundary class, and residual coefficients remain unsigned.",
        },
    ]
    rows = []
    for item in data:
        row = base_row()
        row.update({**item, "parent_signed": False})
        rows.append(row)
    return rows


def residual_rows() -> list[dict[str, object]]:
    data = [
        ("RN2019_0_M_H_ref", "M_H_ref", "same-frame Hamiltonian/Noether source denominator", "MISSING_STABLE_MH_REF", "mass_or_charge"),
        ("RN2019_1_QA_total", "Q_A^total", "raw A split boundary charge from 2017 generator", "FORMULA_ONLY_NOT_ZERO_TARGET", "A-charge"),
        ("RN2019_2_QA_GR", "Q_A^GR", "measured GR/Hamiltonian source contribution to A variation", "MISSING_GR_SOURCE_MAP", "A-charge"),
        ("RN2019_3_QA_exact", "Q_A^proper/exact", "proper gauge or exact boundary contribution", "MISSING_BOUNDARY_EXACTNESS_CERTIFICATE", "A-charge"),
        ("RN2019_4_QA_res", "Q_A^res", "extra residual A source charge after subtraction", "CORRECT_ZERO_OR_BOUND_TARGET_MISSING_VALUE", "A-charge"),
        ("RN2019_5_KA_res", "K_A^res", "residual boundary cocycle", "MISSING_BRACKET_AND_REFERENCE_LOCK", "charge_algebra_units"),
        ("RN2019_6_Qbar_AH_res", "Qbar_AH^res(lambda)", "Hamiltonian/source projection of residual A charge", "MISSING_PROJECTOR_OR_BOUND", "dimensionless_or_declared"),
        ("RN2019_7_qbar_AT", "qbar_AT", "test/readout coupling to residual A", "MISSING_TEST_LEG", "dimensionless"),
        ("RN2019_8_alphaA_res", "alpha_A^res(lambda)", "Yukawa-equivalent residual A strength", "MISSING_ALL_JOIN_INPUTS", "dimensionless"),
        ("RN2019_9_no_cancellation_guard", "abs_envelope_Ares", "absolute sum of residual A plus retained boundary/source tails", "NOT_COMPUTED_COMPONENTS_MISSING", "dimensionless"),
    ]
    rows = []
    for row_id, symbol, meaning, status, units in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "meaning": meaning,
                "status": status,
                "numeric_value": "MISSING",
                "units": units,
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2019_0_decomposition_written", "Q_A total decomposition is explicit", True, "GR, proper/exact, and residual pieces are separated"),
        ("CG2019_1_total_not_scored", "Q_A_total is not used as fifth-force source", True, "prevents measured-mass double counting"),
        ("CG2019_2_MHref_owned", "M_H_ref is stable same-frame denominator", False, "1017 source-measure/reference locks remain unsigned"),
        ("CG2019_3_projector_orthogonal", "GR source and residual A projectors are orthogonal", False, "Pi_M^H definition, symplectic block, and source independence are not derived"),
        ("CG2019_4_boundary_exact", "proper/exact boundary piece is theorem-zero", False, "boundary cohomology/counterterm/cocycle gates remain open"),
        ("CG2019_5_PiAres_zero", "Pi_A_res and K_A_res vanish", False, "requires M_H_ref, projector orthogonality, boundary exactness, and matter/source silence together"),
        ("CG2019_6_residual_score_ready", "finite residual A comparator row is score-ready", False, "all residual coefficients and test/source legs are missing"),
        ("CG2019_7_local_GR_Newton", "local GR/Newton reduction from A branch is derived", False, "residual zero theorem is not parent-signed"),
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
        ("REF2019_0_score_total_QA", "score Q_A_total as fifth-force source", "REFUSE", "Q_A_total includes measured GR/Hamiltonian mass source and would double count Newtonian mass."),
        ("REF2019_1_MHref_shortcut", "use orbital GM, bare mass, or reference 1 as M_H_ref", "REFUSE", "1017 forbids replacing the source theorem denominator with the readout being derived."),
        ("REF2019_2_PiAres_zero", "claim Pi_A_res=0", "REFUSE", "M_H_ref, projector orthogonality, boundary exactness, and source/functor silence are not signed together."),
        ("REF2019_3_KAres_zero", "claim K_A_res=0", "REFUSE", "residual boundary bracket and reference/counterterm silence are uncomputed."),
        ("REF2019_4_residual_score", "score alpha_A_res(lambda)", "REFUSE", "Z_A, lambda_A, K_A, Qbar_AH_res, qbar_AT, profile, and bounds are missing."),
        ("REF2019_5_local_GR", "claim local GR/Newton reduction", "REFUSE", "A residual source theorem remains open and finite residual rows are nonclaim."),
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
            "DEC2019_0_result",
            "A_FRAME_SOURCE_DECOMPOSITION_WRITTEN_RESIDUAL_ZERO_UNSIGNED",
            "Q_A_total is now decomposed into measured GR/Hamiltonian source, proper/exact boundary, and residual A hair. Only the residual belongs in local fifth-force tests.",
            "do not score total A charge; attack M_H_ref/Pi_GR owner and projector orthogonality next",
        ),
        (
            "DEC2019_1_route_status",
            "LOCAL_GR_ROUTE_IS_NOW_A_NO_DOUBLE_COUNT_THEOREM",
            "To reduce to GR/Newton, MTS must show every A boundary charge is either the ordinary measured source or pure gauge/exact, with no residual projection.",
            "derive M_H_ref plus Pi_GR map before attempting R10/PPN scoring",
        ),
        (
            "DEC2019_2_testing_status",
            "FINITE_A_TESTING_REQUIRES_RESIDUAL_NORMALIZATION",
            "If residual A survives, its amplitude must be normalized by same-frame M_H_ref and absolute-summed with no cancellation against unknown boundary/source tails.",
            "create residual rows only after source/test legs and M_H_ref are sourced",
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
            "target_id": "NEXT2019_0_2020",
            "next_doc": "2020-Y5-R2FR-Aframe-MHref-PiGR-owner-or-PiAres-first-row.md",
            "objective": "derive the same-frame Hamiltonian source denominator M_H_ref and Pi_GR/H map needed to subtract measured GR mass from Q_A_total; if not, create the first residual-normalized Pi_A_res row without claims",
            "required_inputs": "Q_tau integral; fixed H_ref; tau lock; source worldtube; public tetrad source measure; Pi_GR/H projector; no-double-count proof; M_H_ref units; Pi_A_res schema",
            "excluded": "orbital GM denominator; bare mass shortcut; total Q_A scoring; reference-only zero; cancellation between unknown residuals; R10/local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update({"copy_id": f"COPY2019_{idx}", "path": str(path), "exists": path.exists(), "note": note})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    decomp: list[dict[str, object]],
    residuals: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2019_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"))
    checks.append(("VAL2019_01_decomposition_written", any(row["decomp_id"] == "GSD2019_8_verdict" and "Q_A^GR" in row["formula"] for row in decomp), "Q_A total decomposition is explicit"))
    checks.append(("VAL2019_02_total_not_scored", any(row["refusal_id"] == "REF2019_0_score_total_QA" and row["verdict"] == "REFUSE" for row in refusals), "total Q_A scoring is refused"))
    checks.append(("VAL2019_03_projector_gate_present", any(row["decomp_id"] == "GSD2019_5_no_double_count_projector" for row in decomp), "no-double-count projector gate is present"))
    checks.append(("VAL2019_04_zero_not_promoted", any(row["decomp_id"] == "GSD2019_8_verdict" and row["status"] == "DECOMPOSITION_WRITTEN_RESIDUAL_ZERO_NOT_SIGNED" for row in decomp), "Pi_A_res zero is not falsely promoted"))
    checks.append(("VAL2019_05_residual_rows_nonclaim", all(row["score_ready"] is False and row["numeric_value"] == "MISSING" for row in residuals), "residual-normalized rows remain missing/nonclaim"))
    checks.append(("VAL2019_06_claim_gates_blocked", all(row["passed_for_claim"] is False for row in claim_gates), "all claim gates remain blocked"))
    checks.append(("VAL2019_07_refusals_active", all(row["verdict"] == "REFUSE" and row["accepted_for_claim"] is False for row in refusals), "refusals remain active"))
    checks.append(("VAL2019_08_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"))
    checks.append(("VAL2019_09_branch_copies", all(path.exists() and csv_rows_parse(path) for path in branch_paths), "branch-copy CSVs exist and parse"))
    checks.append(("VAL2019_10_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"))
    checks.append(("VAL2019_11_output_scope", all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in output_paths + branch_paths + [DOC]), "all outputs are under post-checkpoint-work"))
    overall = all(passed for _, passed, _ in checks)
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    row = base_row()
    row.update(
        {
            "check_id": "VAL2019_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2019 A-frame GR-source decomposition Pi_A_res zero or residual normalization",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    decomp: list[dict[str, object]],
    residuals: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    parts = [
        "# 2019 Y5 R2FR: A-Frame GR-Source Decomposition PiAres Zero Or Residual Normalization\n",
        "Private checkpoint. This converts the 2018 residual target into a proper source decomposition and no-double-count gate.\n",
        "## Current Verdict\n",
        "The decomposition is now explicit: `Q_A^total = Q_A^GR + Q_A^proper/exact + Q_A^res`. The measured GR/Hamiltonian source piece is not evidence for an extra force; it is the Newtonian source. The only A-frame object that belongs in R10/PPN/clock/orbital tests is the residual charge `Q_A^res`, normalized by a same-frame `M_H_ref`.\n",
        "`Pi_A_res=0` is still not a claim. It requires four locks at once: stable `M_H_ref`, a parent-owned `Pi_GR/H` projector, boundary exact/proper silence, and no-double-count orthogonality. Current MTS has the correct contract but not the signatures.\n",
        "So the route improves again: the coupling bottleneck is now a concrete no-double-count theorem. Either every A boundary charge is measured GR source or exact gauge, or the residual A charge becomes the only finite source row to test.\n",
        "## Source Register\n",
        md_table(sources, ["source_id", "source_path", "status", "needles", "note"]),
        "## GR-Source Decomposition\n",
        md_table(decomp, ["decomp_id", "object", "formula", "status", "derivation", "missing_before_claim", "parent_signed"]),
        "## Residual-Normalized Rows\n",
        md_table(residuals, ["row_id", "symbol", "meaning", "status", "numeric_value", "units", "score_ready", "valid_for_claim"]),
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
    decomp = decomposition_rows()
    residuals = residual_rows()
    claim_gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2019_SOURCE_REGISTER.csv",
        "decomp": OUT / "P8_Y5_PARENT_QLOC_2019_AFRAME_GR_SOURCE_DECOMPOSITION.csv",
        "residuals": OUT / "P8_Y5_PARENT_QLOC_2019_AFRAME_RESIDUAL_NORMALIZED_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2019_CLAIM_GATE.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2019_REFUSAL_RUNNER.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2019_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2019_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["decomp"], decomp)
    write_csv(output_map["residuals"], residuals)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["refusals"], refusals)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_GR_SOURCE_DECOMPOSITION_2019_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2019_AFRAME_RESIDUAL_SOURCE_STATUS_NONCLAIM.csv",
        QUEUE / "JR2019_AFRAME_RESIDUAL_NORMALIZED_SOURCE_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["decomp"], branch_paths[0])
    shutil.copyfile(output_map["claim_gates"], branch_paths[1])
    shutil.copyfile(output_map["residuals"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame GR-source decomposition nonclaim copy",
            "A-frame residual source claim-gate status nonclaim copy",
            "A-frame residual-normalized source queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2019_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, decomp, residuals, claim_gates, refusals, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2019_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, decomp, residuals, claim_gates, refusals, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2019_OVERALL"][0]["status"]
    print(f"VAL2019_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
