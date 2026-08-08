from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2086-Y5-R2FR-parent-reciprocal-quadratic-form-extraction-or-PiR-flux-switch.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
Q_R_HAT_POLICY_CEILING = 4.6e-05


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "claim_allowed", "valid"}


def formalization_has_2086_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2086-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2086*",
        "*Y5_R2FR_parent_reciprocal_quadratic_form_extraction_or_PiR_flux_switch_2086*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2086_00_2085_doc",
            ROOT / "2085-Y5-R2FR-RAB-energy-weight-wRAB-and-trace-constant-owner-or-flux-switch.md",
            ["NEXT2085_0_2086", "w_RAB=lambda_min", "VAL2085_OVERALL"],
            "2085 handoff: inspect parent reciprocal quadratic form before activating flux switch.",
        ),
        (
            "SRC2086_01_2085_validation",
            OUT / "P8_Y5_BRR545_2085_VALIDATION.csv",
            ["VAL2085_OVERALL", "2086 parent quadratic-form/flux switch target selected", "claim_allowed"],
            "2085 validation confirms trace absence was not claimed and 2086 was selected.",
        ),
        (
            "SRC2086_02_1256_minimal_density",
            ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            ["HC1256_0_minimal_density", "H_R = int_Sigma", "FORMAL_VARIATIONAL_CONTRACT_NOT_PARENT_SIGNED"],
            "1256 supplies the strongest current formal H_R density candidate.",
        ),
        (
            "SRC2086_03_1256_exterior",
            ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            ["HC1256_1_spherical_exterior", "r^2 Z_R partial_r R_AB = Q_R", "Pi_R^n"],
            "1256 supplies the exterior flux/current shape.",
        ),
        (
            "SRC2086_04_1251_blocker",
            ROOT / "1251-Y5-R10-Hcore-to-qRhat-coefficient-map-attempt-or-phenomenological-row.md",
            ["BLK1251_0_Hcore", "explicit weak-field H_core missing", "cannot derive q_R_hat coefficient"],
            "1251 records that H_core coefficient ownership was previously missing.",
        ),
        (
            "SRC2086_05_1253_hcore",
            ROOT / "1253-Y5-R10-reciprocal-Hcore-boundary-charge-derivation-attempt.md",
            ["HCE1253_0_reciprocal_euler_source", "SOURCE_EQUATION_NOT_DERIVED", "MISSING_EXPLICIT_HCORE"],
            "1253 records source-equation failure before the 1256 formal contract.",
        ),
        (
            "SRC2086_06_05_radial_action",
            ROOT / "05-reciprocity-theorem-attempt.md",
            ["S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB].", "W R_AB' = Q_R", "conserved reciprocal charge"],
            "early radial action gives the old kinetic gradient shape.",
        ),
        (
            "SRC2086_07_06_boundary",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["delta S_boundary = [W R_AB' + Pi_R] delta R_AB|_surface.", "Q_R = -Pi_R", "source reciprocal momentum/charge"],
            "early boundary audit supplies Pi_R matching logic.",
        ),
        (
            "SRC2086_08_07_constraint",
            ROOT / "07-nonpropagating-reciprocity-constraint.md",
            ["S_constraint = integral lambda_R R_AB.", "no R_AB kinetic term", "no conserved Q_R"],
            "constraint branch is a separate zero route if parent-signed.",
        ),
        (
            "SRC2086_09_1172_trace",
            ROOT / "1172-Y5-R10-BC-primitive-norm-owner-or-local-finite-bound-runner.md",
            ["HBP1172_2_trace_to_boundary", "C_trace(D,gamma)", "MISSING_TRACE_CONSTANT"],
            "trace theorem grammar remains selected-domain missing.",
        ),
        (
            "SRC2086_10_2062_orientation",
            ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
            ["BGA2062_4_orientation", "Pi_R^tot", "MISSING_ORIENTATION_CONVENTION"],
            "finite Pi_R flux fallback still lacks normalization/orientation.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                exists=path.exists(),
                needle_count=len(needles),
                missing_needles=";".join(missing),
                status="EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                note=note,
            )
        )
    return rows


def quadratic_extraction_rows() -> list[dict[str, object]]:
    return [
        row(
            extraction_id="QF2086_0_formal_HR_density",
            branch="formal reciprocal quadratic form",
            extracted_object="H_R = int sqrt(h)[1/2 Z_R |D R_AB|^2 + 1/2 M_R^2 R_AB^2 + lambda_R R_AB + J_R R_AB] + boundary B_R",
            condition="candidate from 1256, not parent-signed",
            derived_weight="none yet",
            verdict="FORMAL_VARIATIONAL_CONTRACT_NOT_PARENT_SIGNED",
            missing_inputs="parent origin of Z_R,M_R^2,lambda_R,J_R,B_R; coefficient-variation terms; matter descent",
            claim_allowed=False,
        ),
        row(
            extraction_id="QF2086_1_massive_bulk_trace",
            branch="trace",
            extracted_object="positive R_AB bulk H1 slot",
            condition="Z_R >= Z_min > 0 and M_R^2 >= M_min^2 > 0 on D_ext; source terms absent/shifted; boundary not negative",
            derived_weight="w_RAB = min(Z_min, M_min^2) after norm/unit matching",
            verdict="EXACT_IF_SIGNS_PARENT_SIGNED",
            missing_inputs="Z_min;M_min^2;unit matching;source silence;boundary positivity;C_tr;GM_source",
            claim_allowed=False,
        ),
        row(
            extraction_id="QF2086_2_massless_gradient_trace",
            branch="trace",
            extracted_object="massless kinetic R_AB slot",
            condition="Z_R >= Z_min > 0, M_R=0, and reference/Dirichlet/Poincare control gives ||R_AB||_L2^2 <= C_P,RAB^2 ||D R_AB||_L2^2",
            derived_weight="w_RAB = Z_min/(1 + C_P,RAB^2) for the H1 norm",
            verdict="EXACT_IF_POINCARE_AND_REFERENCE_SIGNED",
            missing_inputs="Z_min;C_P,RAB;finite domain/reference condition;no negative boundary term;C_tr;GM_source",
            claim_allowed=False,
        ),
        row(
            extraction_id="QF2086_3_mixed_quadratic_trace",
            branch="trace",
            extracted_object="R_AB mixed with other reciprocal variables",
            condition="quadratic Hessian block [[A,B],[B^T,C]] has C>0 and Schur complement A-B C^{-1}B^T >= w_RAB I",
            derived_weight="w_RAB = lambda_min(A - B C^{-1}B^T)",
            verdict="EXACT_IF_SCHUR_COERCIVITY_PARENT_SIGNED",
            missing_inputs="A;B;C;C inverse/domain;unit matching;boundary terms;C_tr;GM_source",
            claim_allowed=False,
        ),
        row(
            extraction_id="QF2086_4_constraint_zero_branch",
            branch="constraint zero",
            extracted_object="lambda_R R_AB with no kinetic R_AB mode",
            condition="Z_R=0 and parent-owned lambda_R R_AB is a true constrained variable with compatible Dirac chain and boundary silence",
            derived_weight="not a finite w_RAB route; it would imply R_AB=0/Q_R=0 if parent-signed",
            verdict="STRONGER_ZERO_ROUTE_UNSIGNED",
            missing_inputs="lambda_R parent origin;first-class/Dirac chain;matter compatibility;boundary/corner silence",
            claim_allowed=False,
        ),
        row(
            extraction_id="QF2086_5_flux_switch_candidate",
            branch="flux fallback",
            extracted_object="Pi_R flux bound",
            condition="no coercive R_AB H1 slot is parent-signed, but Pi_R^n density or total flux is parent-owned and bounded by X_E",
            derived_weight="C_QX=sqrt(area_ext)*C_flux_out for density, or C_QX=C_flux_total for total-flux normalization",
            verdict="FALLBACK_READY_NOT_ACTIVATED",
            missing_inputs="proof trace slot absent or failed;Pi_R normalization;C_flux_out/C_flux_total;orientation;absolute tails;GM_source",
            claim_allowed=False,
        ),
    ]


def decision_matrix_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DM2086_0_formal_quadratic_exists",
            question="Does the corpus contain a quadratic-form candidate?",
            current_evidence="1256 HC1256_0_minimal_density supplies a formal H_R density with Z_R and M_R^2.",
            decision="YES_FORMAL_NOT_PARENT_SIGNED",
            consequence="do not abandon trace route yet",
            claim_allowed=False,
        ),
        row(
            decision_id="DM2086_1_parent_signed",
            question="Is the quadratic form parent-signed?",
            current_evidence="1256 explicitly marks the density as FORMAL_VARIATIONAL_CONTRACT_NOT_PARENT_SIGNED; 1251/1253 record H_core/source equation blockers.",
            decision="NO",
            consequence="no K_qR score or local-test claim",
            claim_allowed=False,
        ),
        row(
            decision_id="DM2086_2_trace_switch",
            question="Should the branch switch to Pi_R flux now?",
            current_evidence="missing w_RAB is not proof that H_R lacks a positive R_AB slot; a formal Z_R/M_R^2 slot is already staged.",
            decision="NO_NOT_YET",
            consequence="next work should sign/refute Z_R/M_R^2/Poincare before flux switch",
            claim_allowed=False,
        ),
        row(
            decision_id="DM2086_3_zero_route",
            question="Is the lambda_R constraint route better than finite trace?",
            current_evidence="07/1256 identify it as clean but parent-unsigned.",
            decision="POTENTIALLY_STRONGER_BUT_UNSIGNED",
            consequence="keep as zero-route watch; finite branch still needs sourceable residual map",
            claim_allowed=False,
        ),
    ]


def source_pack_rows() -> list[dict[str, object]]:
    specs = [
        ("PACK2086_0_Zmin", "Z_min", "lower bound for Z_R on D_ext", "MISSING_PARENT_SIGNED_VALUE"),
        ("PACK2086_1_Mmin", "M_min^2", "lower bound for M_R^2 on D_ext", "MISSING_PARENT_SIGNED_VALUE"),
        ("PACK2086_2_CP", "C_P,RAB", "Poincare/reference constant for massless kinetic route", "MISSING_DOMAIN_REFERENCE_ROW"),
        ("PACK2086_3_Ctr", "C_tr(D_ext,S_ext,gamma)", "selected-domain trace theorem constant", "MISSING_TRACE_CONSTANT"),
        ("PACK2086_4_boundary", "B_R positivity/silence", "exclude negative boundary energy and source/corner hair", "MISSING_BOUNDARY_GRAMMAR"),
        ("PACK2086_5_sources", "lambda_R,J_R source policy", "zero/shift/source-bound linear terms before using homogeneous norm", "MISSING_SOURCE_SILENCE_OR_SHIFT"),
        ("PACK2086_6_flux", "Pi_R density/total flux constants", "fallback if trace slot fails", "MISSING_FLUX_NORMALIZATION"),
        ("PACK2086_7_GM", "source_body;GM_source", "raw Q_R to q_R_hat conversion", "CONVENTION_ONLY_VALUE_MISSING"),
    ]
    return [
        row(
            pack_id=pack_id,
            required_input=required_input,
            purpose=purpose,
            current_status=current_status,
            source_ready=False,
            score_ready=False,
            claim_allowed=False,
        )
        for pack_id, required_input, purpose, current_status in specs
    ]


def dry_run_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2086_0_massive_bulk_trace",
            attempted_route="Z_R/M_R massive trace",
            formula="K_qR=(c^2/(G*M_source))*C_tr/sqrt(4*pi*min(Z_min,M_min^2))",
            input_status="REFUSED_MISSING_ZMIN_MMIN_CTR_GM",
            missing_inputs="Z_min;M_min^2;C_tr;GM_source;boundary positivity;source silence",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2086_1_massless_gradient_trace",
            attempted_route="Z_R plus Poincare/reference trace",
            formula="K_qR=(c^2/(G*M_source))*C_tr*sqrt(1+C_P,RAB^2)/sqrt(4*pi*Z_min)",
            input_status="REFUSED_MISSING_ZMIN_CP_CTR_GM",
            missing_inputs="Z_min;C_P,RAB;reference condition;C_tr;GM_source",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2086_2_constraint_zero_route",
            attempted_route="lambda_R nonpropagating zero route",
            formula="R_AB=0 and Q_R=0 if parent-owned lambda_R R_AB with Dirac/boundary closure",
            input_status="REFUSED_MISSING_PARENT_CONSTRAINT_CHAIN",
            missing_inputs="lambda_R origin;Dirac chain;matter compatibility;boundary silence",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2086_3_flux_fallback",
            attempted_route="Pi_R flux fallback",
            formula="K_qR=(c^2/(G*M_source))*sqrt(area_ext)*C_flux_out or (c^2/(G*M_source))*C_flux_total",
            input_status="REFUSED_MISSING_TRACE_FAILURE_PROOF_AND_FLUX_INPUTS",
            missing_inputs="proof trace slot failed;Pi_R normalization;C_flux_out/C_flux_total;orientation;GM_source",
            K_qR_value="NOT_EVALUATED",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            pass_status="NO_SCORE",
            claim_allowed=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2086_0_formal_HR", "formal H_R candidate extracted", "PASS_FORMAL_ONLY", "1256 minimal density gives Z_R/M_R/lambda/J/B_R structure"),
        ("GATE2086_1_parent_signature", "H_R is parent-signed", "FAIL_BLOCKED", "parent origin of Z_R,M_R^2,lambda_R,J_R,B_R and coefficient variations is missing"),
        ("GATE2086_2_trace_score", "trace branch can score K_qR", "FAIL_REFUSED", "Z_min/M_min or Poincare, C_tr, GM, and source/boundary silence are missing"),
        ("GATE2086_3_flux_switch", "Pi_R flux switch is active", "FAIL_BLOCKED", "trace-slot absence is not proved and flux constants are missing"),
        ("GATE2086_4_zero_route", "lambda_R constraint proves R_AB=0", "FAIL_BLOCKED", "constraint origin/Dirac chain/boundary silence are missing"),
        ("GATE2086_5_local_claim", "local GR/Newton/PPN claim", "FAIL_BLOCKED", "no q_R prediction or zero theorem plus q_loc bridge/retained-channel closure"),
    ]
    return [
        row(
            gate_id=gate_id,
            condition=condition,
            status=status,
            reason=reason,
            claim_allowed=False,
        )
        for gate_id, condition, status, reason in specs
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2086_0_trace_not_dead",
            decision="Do not switch to flux yet.",
            because="1256 already contains a formal Z_R/M_R^2 quadratic candidate; missing signed coefficients is not a trace failure proof.",
            next_action="source/sign Z_R, M_R^2, boundary positivity, source silence, and C_tr",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2086_1_massless_route_valid_if_reference_signed",
            decision="Massless kinetic route can still control trace if Poincare/reference data is supplied.",
            because="Z_R gradient control plus ||R||<=C_P||grad R|| gives w_RAB=Z_min/(1+C_P^2).",
            next_action="look for reference subtraction/finite shell/Poincare owner before demoting M_R=0",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2086_2_constraint_route_watch",
            decision="lambda_R constraint remains the strongest local-GR route if parent-signed.",
            because="it would kill R_AB hair rather than merely bound it, but it is still a closure-like contract without the parent Dirac chain.",
            next_action="keep it separate from finite trace/flux scoring",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2086_3_next_target",
            decision="Next target is Z_R/M_R signature plus Poincare/reference owner.",
            because="those are the minimum signs/constants needed to turn the formal H_R candidate into a real w_RAB owner.",
            next_action="build 2087 Z_R-M_R-signature-and-Poincare-domain-owner-or-flux-switch.md",
            claim_allowed=False,
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2086_0_2087",
            target_doc="2087-Y5-R2FR-ZR-MR-signature-and-Poincare-domain-owner-or-flux-switch.md",
            objective="derive/source the signs and lower bounds for Z_R and M_R^2 in the formal H_R density, plus the Poincare/reference constant for the massless route; if these fail by parent proof, activate Pi_R flux ownership instead",
            must_include="Z_R origin/sign; M_R^2 origin/sign; coefficient-variation terms; source silence or shift for lambda_R,J_R; boundary B_R positivity/silence; C_P,RAB; C_tr; flux fallback only after trace failure proof",
            exclusions="scoring K_qR from formal H_R alone; assuming trace failure from missing rows; using Cassini ceiling as prediction; closure q_R=0; local GR/Newton/PPN claim; GitHub; formalization-workbench edits",
            claim_allowed=False,
        )
    ]


def write_branch_copies(
    qforms: list[dict[str, object]],
    matrix: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2086_0_source_weight_qform",
            SOURCE_WEIGHT_DOCS / "AFRAME_PARENT_RECIPROCAL_QFORM_2086_NONCLAIM.csv",
            qforms + matrix + dry,
        ),
        (
            "COPY2086_1_wep_qform",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2086_QFORM_NONCLAIM.csv",
            qforms + dry,
        ),
        (
            "COPY2086_2_queue_2087",
            QUEUE / "JR2086_ZR_MR_POINCARE_OR_FLUX_SWITCH_QUEUE.csv",
            pack + next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data_rows in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=copy_id,
                path=str(path),
                rows_written=len(data_rows),
                status="WRITTEN_NONCLAIM_COPY",
                claim_allowed=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    qforms: list[dict[str, object]],
    matrix: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    formal_hr_ok = any(r["extraction_id"] == "QF2086_0_formal_HR_density" for r in qforms)
    massive_ok = any("min(Z_min, M_min^2)" in str(r["derived_weight"]) for r in qforms)
    massless_ok = any("Z_min/(1 + C_P,RAB^2)" in str(r["derived_weight"]) for r in qforms)
    constraint_ok = any(r["extraction_id"] == "QF2086_4_constraint_zero_branch" for r in qforms)
    flux_ok = any(r["extraction_id"] == "QF2086_5_flux_switch_candidate" for r in qforms)
    no_flux_switch_yet = any(r["decision_id"] == "DM2086_2_trace_switch" and r["decision"] == "NO_NOT_YET" for r in matrix)
    pack_ok = all(not truthy(r.get("score_ready")) for r in pack)
    dry_refused = all(str(r["input_status"]).startswith("REFUSED") for r in dry)
    gates_blocked = all(not truthy(r.get("claim_allowed")) for r in gates)
    next_signature = any(r["decision_id"] == "DEC2086_3_next_target" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2086_0_2087"
    copies_ok = all(Path(str(r["path"])).exists() and csv_rows_parse(Path(str(r["path"]))) for r in copies)
    no_claims = all(
        not truthy(item.get("claim_allowed")) and not truthy(item.get("valid_for_claim"))
        for collection in [qforms, matrix, pack, dry, gates, decisions, next_rows_]
        for item in collection
    )
    formalization_clean = count_formalization_modified() == 0
    no_formalization_artifacts = not formalization_has_2086_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()

    checks = [
        ("VAL2086_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2086_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2086_02_formal_HR", formal_hr_ok, "formal H_R density is extracted"),
        ("VAL2086_03_massive_formula", massive_ok, "massive Z_R/M_R trace weight formula is written"),
        ("VAL2086_04_massless_formula", massless_ok, "massless Poincare trace weight formula is written"),
        ("VAL2086_05_constraint_route", constraint_ok, "lambda_R zero route is kept separate"),
        ("VAL2086_06_flux_fallback", flux_ok, "Pi_R flux fallback is prepared"),
        ("VAL2086_07_no_flux_switch_yet", no_flux_switch_yet, "flux switch is not activated without trace-failure proof"),
        ("VAL2086_08_pack_nonclaim", pack_ok, "source pack rows remain unscored/nonclaim"),
        ("VAL2086_09_dry_refusal", dry_refused, "all dry-run branches refuse missing inputs"),
        ("VAL2086_10_claim_gates_blocked", gates_blocked, "claim gates remain blocked"),
        ("VAL2086_11_next_signature", next_signature, "Z_R/M_R/Poincare signature selected as next target"),
        ("VAL2086_12_next_selected", next_ok, "2087 target selected"),
        ("VAL2086_13_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2086_14_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2086_15_formalization_unchanged", formalization_clean, "formalization-workbench modified-file count remains 0"),
        ("VAL2086_16_no_formalization_artifacts", no_formalization_artifacts, "no 2086 artifacts were written under formalization-workbench"),
        ("VAL2086_17_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(status for _, status, _ in checks)
    checks.append(("VAL2086_OVERALL", overall, "2086 extracts the formal parent reciprocal quadratic form, refuses scoring, and selects Z_R/M_R/Poincare signature"))
    return [
        row(
            check_id=check_id,
            status="PASS" if status else "FAIL",
            detail=detail,
            claim_allowed=False,
        )
        for check_id, status, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    qforms: list[dict[str, object]],
    matrix: list[dict[str, object]],
    pack: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2086 Y5 R2FR Parent Reciprocal Quadratic Form Extraction Or Pi_R Flux Switch",
        "",
        "## Current Verdict",
        "",
        "2086 extracts the strongest current quadratic-form candidate: the 1256 formal reciprocal density `H_R = int sqrt(h)[1/2 Z_R |D R_AB|^2 + 1/2 M_R^2 R_AB^2 + lambda_R R_AB + J_R R_AB] + B_R`. This means the trace route is not dead; it has a concrete engine block. But the engine block is still not parent-signed.",
        "",
        "If `Z_R >= Z_min > 0` and `M_R^2 >= M_min^2 > 0`, the finite trace weight is `w_RAB=min(Z_min,M_min^2)`. If the branch is massless with `M_R=0`, gradient control can still work if a reference/Poincare condition is parent-signed, giving `w_RAB=Z_min/(1+C_P,RAB^2)`.",
        "",
        "So we should not switch to `Pi_R` flux merely because `w_RAB` is missing. Flux is a fallback only after the parent quadratic-form audit proves no coercive `R_AB` H1 route exists, or after the sign/domain constants fail by theorem rather than by missing rows.",
        "",
        "The lambda_R constraint route remains the stronger local-GR route if parent-signed: it would kill `R_AB` hair rather than bound it. But it is a separate zero theorem route, not a finite trace score.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "exists", "needle_count", "missing_needles", "status", "note", "valid_for_claim"]),
        "## Quadratic Form Extraction",
        md_table(qforms, ["extraction_id", "branch", "extracted_object", "condition", "derived_weight", "verdict", "missing_inputs", "claim_allowed", "valid_for_claim"]),
        "## Decision Matrix",
        md_table(matrix, ["decision_id", "question", "current_evidence", "decision", "consequence", "claim_allowed", "valid_for_claim"]),
        "## Source Pack",
        md_table(pack, ["pack_id", "required_input", "purpose", "current_status", "source_ready", "score_ready", "claim_allowed", "valid_for_claim"]),
        "## Dry Run",
        md_table(dry, ["run_id", "attempted_route", "formula", "input_status", "missing_inputs", "K_qR_value", "q_R_hat_policy_ceiling", "pass_status", "claim_allowed", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "condition", "status", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "claim_allowed", "valid_for_claim"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "exclusions", "claim_allowed", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows_written", "status", "claim_allowed", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    qforms = quadratic_extraction_rows()
    matrix = decision_matrix_rows()
    pack = source_pack_rows()
    dry = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2086_SOURCE_REGISTER.csv",
        "qforms": OUT / "P8_Y5_PARENT_QLOC_2086_QUADRATIC_FORM_EXTRACTION.csv",
        "matrix": OUT / "P8_Y5_PARENT_QLOC_2086_DECISION_MATRIX.csv",
        "pack": OUT / "P8_Y5_PARENT_QLOC_2086_SOURCE_PACK.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2086_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2086_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2086_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2086_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2086_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2086_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["qforms"], qforms)
    write_csv(paths["matrix"], matrix)
    write_csv(paths["pack"], pack)
    write_csv(paths["dry"], dry)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(qforms, matrix, pack, dry, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, qforms, matrix, pack, dry, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, qforms, matrix, pack, dry, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
