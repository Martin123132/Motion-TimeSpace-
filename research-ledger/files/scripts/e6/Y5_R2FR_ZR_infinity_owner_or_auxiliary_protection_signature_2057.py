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


DOC = ROOT / "2057-Y5-R2FR-ZR-infinity-owner-or-auxiliary-protection-signature.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2057_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2057-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2057*",
            "*Y5_R2FR_ZR_infinity_owner_or_auxiliary_protection_signature_2057*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2057_00_2056_doc",
            ROOT / "2056-Y5-R2FR-WR-radial-measure-owner-or-omegaW-symbolic-runner.md",
            ["NEXT2056_0_2057", "omega_W=N_sphere Z_R_infty", "q_R^PPN=Pi_R/(N_sphere Z_R_infty r_s)"],
            "2056 handoff: omega_W owner narrowed to Z_R_infty/N_sphere or auxiliary escape.",
        ),
        (
            "SRC2057_01_2056_next",
            OUT / "P8_Y5_PARENT_QLOC_2056_NEXT_TARGET.csv",
            ["NEXT2056_0_2057", "AP1265 clause audit", "Z_R_infty source schema"],
            "machine-readable 2057 target.",
        ),
        (
            "SRC2057_02_1268_aux_action",
            ROOT / "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
            ["CAC1268_5_conditional_theorem", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED", "AP1265_1_no_derivatives"],
            "best existing second-class auxiliary compatibility mechanism.",
        ),
        (
            "SRC2057_03_1563_sort_grammar",
            ROOT / "1563-Y5-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
            ["parent sort/quotient map not derived", "FAILED_CURRENT_OPERATOR_BAN", "FINITE_ZR_QR_FALLBACK_RETAINED_NONCLAIM"],
            "later parent-sort/no-derivative grammar audit.",
        ),
        (
            "SRC2057_04_1272_parent_necessity",
            ROOT / "1272-Y5-R10-RAB-auxiliary-parent-necessity-from-radial-cell-variational-principle-or-finite-source-row.md",
            ["parent-owned radial observer configuration-cell normalization", "PARENT_NECESSITY_NOT_DERIVED", "J_q=1"],
            "radial-cell necessity synthesis: why Lambda_R C_R is not yet parent-forced.",
        ),
        (
            "SRC2057_05_2049_euler_gate",
            ROOT / "2049-Y5-R2FR-motion-load-parent-Euler-difference-or-RAB-finite-residual.md",
            ["R_AB=0 derivation attempt", "NOT_DERIVED_CURRENT_CORPUS", "RAB2049_VERDICT"],
            "newer R2FR Euler-difference gate and finite residual fallback.",
        ),
        (
            "SRC2057_06_1256_finite_coeffs",
            ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            ["partial_r(r^2 Z_R partial_r R_AB)=0", "COEF1256_0_ZR", "COEF1256_1_MR2"],
            "finite kinetic/massive coefficient contract.",
        ),
        (
            "SRC2057_07_1261_source_hunt",
            ROOT / "1261-Y5-R10-ZR-coefficient-source-hunt-or-operator-exhaustion-reentry.md",
            ["NO_SOURCE_BACKED_ROW_FOUND", "HUNT1261_0_Z_R", "HUNT1261_1_M_R^2"],
            "source hunt confirms no live finite coefficient row.",
        ),
        (
            "SRC2057_08_1281_qloc",
            ROOT / "1281-Y5-R10-RAB-Gamma-Khat-metric-response-symbol-match-or-q_loc-profile-template.md",
            ["SYMBOL_MATCH_NOT_CLOSED", "epsilon_GK_q_loc profile template", "GATE1281_2_q_loc_zero"],
            "later q_loc/Gamma-Khat route remains a nonclaim template.",
        ),
        (
            "SRC2057_09_source_mass_tail",
            OUT / "P8_Y5_PARENT_QLOC_1639_SOURCE_MASS_AND_TAIL_BLOCKERS.csv",
            ["NRB1639_0_tail_normalization", "NRB1639_1_same_frame_mass", "MISSING_PARENT_SOURCE_MASS_CALIBRATION"],
            "same-frame source mass blockers for finite q_R scoring.",
        ),
        (
            "SRC2057_10_tail_inputs",
            OUT / "P8_Y5_PARENT_QLOC_1872_ABSOLUTE_TAIL_BOUND_INPUTS_NONCLAIM.csv",
            ["ABI1872_1_PiR", "MISSING_Pi_R_BOUND_OR_ZERO_THEOREM", "ABI1872_3_gamma_bound"],
            "absolute tail/Pi_R blocker rows.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needles, note in specs:
        exists = source_path.exists()
        text = read_text(source_path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(source_path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def auxiliary_signature_rows() -> list[dict[str, object]]:
    data = [
        (
            "AUX2057_0_parent_sort",
            "R_AB is auxiliary compatibility data, not a physical scalar",
            "1268/1563 write the correct typed target, but no parent field/sort list derives it from MTS primitives.",
            "FAIL_CURRENT_PARENT_SIGNATURE",
            "R_AB can still be physical or vertically metrized in a countermodel.",
            "finite Z_R branch must remain live",
        ),
        (
            "AUX2057_1_no_derivative_operator",
            "D R_AB, D Lambda_R, vertical metric/connection and boundary derivative terms are illegal",
            "The ban is exactly what is needed, but 1563 records FAILED_CURRENT_OPERATOR_BAN.",
            "FAIL_CURRENT_OPERATOR_EXCLUSION",
            "Z_R h^{ij}D_iR_ABD_jR_AB remains legal unless object-language exclusion is proved.",
            "Z_R_infty source/theorem-zero row required",
        ),
        (
            "AUX2057_2_algebraic_elimination",
            "E_Lambda enforces R_AB=C_AB and E_R kills Lambda_R",
            "The second-class compatibility variation is formally correct if J_R, B_R, readout regeneration and derivatives are absent.",
            "PASS_EXACT_CONDITIONAL_ONLY",
            "This is the real mechanism, not fake first-class gauge language.",
            "cannot claim while source/boundary/readout terms remain unsigned",
        ),
        (
            "AUX2057_3_boundary_silence",
            "B_R, Pi_R^n and Q_R vanish for the local source boundary class",
            "Existing files repeatedly identify the needed no-charge/no-hair theorem but do not parent-sign it.",
            "FAIL_CURRENT_BOUNDARY_SIGNATURE",
            "A boundary charge can generate the same exterior q_R hair even if the bulk is auxiliary.",
            "Pi_R/B_R source or zero theorem required",
        ),
        (
            "AUX2057_4_readout_stability",
            "local readout/EFT preserves the eliminated auxiliary grammar",
            "No current proof blocks readout-regenerated Z_R, Khat/Gamma residual, or q_loc profile.",
            "FAIL_CURRENT_READOUT_SIGNATURE",
            "Even a clean tree-level auxiliary block can leak through effective/readout response.",
            "q_loc/Gamma-Khat response map or finite profile required",
        ),
        (
            "AUX2057_5_parent_necessity",
            "Lambda_R C_R is required by a parent radial-cell owner, not appended",
            "1272 and 2049 narrow this to parent-owned radial observer configuration-cell normalization / Euler pair.",
            "FAIL_CURRENT_PARENT_NECESSITY",
            "Without this, the auxiliary block is a disciplined closure mechanism rather than a derivation.",
            "derive L_core/H_core radial-cell owner or demote to closure baseline",
        ),
        (
            "AUX2057_6_verdict",
            "protected auxiliary theorem",
            "AET/CAC route is the cleanest exact conditional mechanism, but AP1265-style protections are not parent-signed.",
            "AUXILIARY_SIGNATURE_NOT_CLOSED",
            "No Z_R=0, q_R=0 or local-GR claim is allowed.",
            "finite source rows remain mandatory fallback",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, evidence, status, failure_mode, required_next in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "evidence": evidence,
                "status": status,
                "failure_mode": failure_mode,
                "required_next": required_next,
                "closes_zero_theorem": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_source_schema_rows() -> list[dict[str, object]]:
    data = [
        (
            "FSR2057_0_ZR_infty",
            "Z_R_infty",
            "asymptotic kinetic coefficient for massless 1/r branch",
            "coefficient_units_or_dimensionless_after_normalization",
            "parent action coefficient or theorem-zero",
            "MISSING_Z_R_INFTY_OR_PARENT_ZERO_THEOREM",
        ),
        (
            "FSR2057_1_N_sphere",
            "N_sphere",
            "angular/boundary normalization convention in omega_W=N_sphere Z_R_infty",
            "dimensionless",
            "boundary flux convention tied to Pi_R/Q_R",
            "MISSING_N_SPHERE_BOUNDARY_CONVENTION",
        ),
        (
            "FSR2057_2_MR2",
            "M_R^2",
            "local Hessian/mass-gap coefficient for screened branch",
            "inverse_length_squared_after_ZR_normalization_or_declared",
            "parent second variation around local branch",
            "MISSING_M_R2_OR_SCREENING_SCALE",
        ),
        (
            "FSR2057_3_PiR",
            "Pi_R",
            "boundary reciprocal momentum/charge entering q_R^PPN",
            "boundary_current_units_or_dimensionless_after_convention",
            "source-boundary theorem-zero or sourced finite flux",
            "MISSING_PIR_VALUE_OR_ZERO_THEOREM",
        ),
        (
            "FSR2057_4_same_frame_rs",
            "r_s",
            "same-frame source radius 2GM_obs/c^2 used by the photon/readout metric",
            "length",
            "source mass calibration from the same observed frame",
            "MISSING_SAME_FRAME_SOURCE_MASS",
        ),
        (
            "FSR2057_5_tail_budget",
            "B_tail_abs",
            "absolute budget for tail/gauge/readout/source residuals",
            "dimensionless",
            "component bounds or parent-zero certificate",
            "MISSING_ABSOLUTE_TAIL_BUDGET",
        ),
        (
            "FSR2057_6_tau_PPN",
            "tau_PPN_R",
            "projection from finite C_R/q_R branch to gamma,beta and preferred-frame PPN components",
            "dimensionless_response_matrix",
            "PPN arena projection kernel and no-cancellation policy",
            "MISSING_PPN_PROJECTION",
        ),
        (
            "FSR2057_7_tau_R10_clock_orbital",
            "tau_R10_R;tau_clock_R;tau_orbital_R",
            "arena projections for short-range, clock and orbital tests",
            "arena_specific",
            "source-backed kernels or theorem-zero per arena",
            "MISSING_ARENA_PROJECTIONS",
        ),
        (
            "FSR2057_8_q_loc_profile",
            "epsilon_GK_q_loc",
            "finite local response profile if auxiliary/readout protection fails",
            "declared_norm_units",
            "Gamma_eff/K_hat metric response or bounded profile row",
            "MISSING_Q_LOC_PROFILE_OR_ZERO_CERTIFICATE",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, role, units, required_source, missing_marker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "role": role,
                "units": units,
                "required_source": required_source,
                "current_value": missing_marker,
                "valid_prediction_row": False,
                "ready_for_scoring": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def branch_runner_rows(aux_rows: list[dict[str, object]], finite_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    aux_blockers = ";".join(row["row_id"] for row in aux_rows if str(row["status"]).startswith("FAIL"))
    finite_blockers = ";".join(row["current_value"] for row in finite_rows)
    data = [
        (
            "RUN2057_0_auxiliary_zero",
            "Z_R=0 protected auxiliary theorem",
            False,
            "REJECTED_AUXILIARY_SIGNATURE_UNSIGNED",
            aux_blockers,
        ),
        (
            "RUN2057_1_massless_finite_qR",
            "q_R^PPN=Pi_R/(N_sphere Z_R_infty r_s)",
            False,
            "REJECTED_FINITE_INPUTS_MISSING",
            "MISSING_Z_R_INFTY;MISSING_N_SPHERE;MISSING_PIR;MISSING_SAME_FRAME_RS;MISSING_TAIL_BUDGET",
        ),
        (
            "RUN2057_2_massive_screened",
            "ell_R=sqrt(Z_R/M_R^2) screened branch",
            False,
            "REJECTED_SCREENING_INPUTS_MISSING",
            "MISSING_Z_R_INFTY;MISSING_M_R2;MISSING_SOURCE_PROFILE;MISSING_ARENA_KERNELS",
        ),
        (
            "RUN2057_3_q_loc_profile",
            "Gamma/Khat q_loc finite residual route",
            False,
            "REJECTED_QLOC_PROFILE_MISSING",
            "MISSING_GAMMA_EFF;MISSING_K_HAT;MISSING_METRIC_RESPONSE;MISSING_PROFILE_BOUND",
        ),
        (
            "RUN2057_4_source_rows",
            "strict finite source-row pack",
            False,
            "SOURCE_SCHEMA_READY_BUT_NO_LIVE_ROWS",
            finite_blockers,
        ),
        (
            "RUN2057_VERDICT",
            "branch choice",
            False,
            "AUXILIARY_NOT_SIGNED_FINITE_NOT_SOURCE_READY_NONCLAIM",
            "best next move is parent radial-cell owner/auxiliary necessity, with finite rows kept as strict fallback",
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, accepted, verdict, reason in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "accepted_for_scoring": accepted,
                "verdict": verdict,
                "reason": reason,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2057_0_aux_route_attempted", "auxiliary route audited against AP1265/1563/1272", "PASS_NONCLAIM", "exact conditional mechanism retained"),
        ("GATE2057_1_aux_signature", "protected auxiliary signature parent-signed", "FAIL_BLOCKED", "sort/operator/boundary/readout/necessity clauses remain unsigned"),
        ("GATE2057_2_ZR_zero", "Z_R=0 theorem allowed", "FAIL_BLOCKED", "auxiliary signature is not closed"),
        ("GATE2057_3_finite_rows", "finite Z_R/Pi_R/q_loc rows scoreable", "FAIL_BLOCKED", "strict schema only; no numeric/source-backed live rows"),
        ("GATE2057_4_local_GR", "local GR/Newton claimed", "FAIL_BLOCKED", "neither zero theorem nor finite residual pass exists"),
        ("GATE2057_5_formalization", "formalization-workbench untouched", "PASS_NONCLAIM", "checkpoint remains private post-checkpoint work"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2057_0_result",
            "The auxiliary route is still the best exact derivation route, but it is not parent-signed.",
            "Existing work already found the right second-class/algebraic mechanism; 2057 confirms the remaining gap is parent necessity plus protection, not algebra.",
        ),
        (
            "DEC2057_1_no_circling",
            "Do not keep re-testing the same AP1265 clauses without a new parent action/grammar input.",
            "1563 and 1272 already show parent sort, no-derivative grammar and radial-cell owner are the missing upstream inputs.",
        ),
        (
            "DEC2057_2_finite_fallback",
            "Finite residual testing remains possible but cannot be scored from templates.",
            "The required rows are Z_R_infty, N_sphere, M_R^2, Pi_R, same-frame r_s, tails and arena kernels, all source-backed or theorem-zero.",
        ),
        (
            "DEC2057_3_next",
            "Next best route is parent radial-cell owner / Lambda_R necessity.",
            "If that fails again, the honest move is closure baseline plus empirical finite residual acquisition, not claiming derived local GR.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update({"row_id": row_id, "decision": decision, "rationale": rationale, "claim_allowed": False})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2057_0_2058",
            "target_doc": "2058-Y5-R2FR-parent-radial-cell-owner-or-local-closure-baseline.md",
            "objective": "derive or reject the parent radial-cell owner that makes Lambda_R C_R necessary; if it cannot be derived, convert the local branch into an explicit closure baseline with finite residual acquisition gates",
            "must_include": "J_q=T sqrt(S); C_R=2lnJ_q; parent L_core/H_core owner; Dirac/preservation check; matter/boundary/readout silence; finite residual fallback scorecard; no-cancellation guards",
            "excluded": "repeating AP1265 without new parent input; setting Lambda_R by preference; scoring template rows; claiming local GR/Newton; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    aux_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2057_0_source_weight_aux_signature",
            SOURCE_WEIGHT_DOCS / "AFRAME_AUXILIARY_SIGNATURE_2057_NONCLAIM.csv",
            aux_rows,
        ),
        (
            "COPY2057_1_wep_finite_schema",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2057_FINITE_SOURCE_SCHEMA_NONCLAIM.csv",
            finite_rows,
        ),
        (
            "COPY2057_2_wep_runner",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2057_BRANCH_RUNNER_NONCLAIM.csv",
            runner,
        ),
        (
            "COPY2057_3_rab_next",
            QUEUE / "JR2057_RADIAL_CELL_OWNER_OR_CLOSURE_BASELINE_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY", "claim_allowed": False})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    aux_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    aux_verdict = next(row for row in aux_rows if row["row_id"] == "AUX2057_6_verdict")
    source_pack_ready = len(finite_rows) >= 8 and all(not bool(row["ready_for_scoring"]) for row in finite_rows)
    missing_markers_present = all(str(row["current_value"]).startswith("MISSING_") for row in finite_rows)
    runner_verdict = next(row for row in runner if row["run_id"] == "RUN2057_VERDICT")
    aux_gate = next(row for row in gates if row["row_id"] == "GATE2057_1_aux_signature")
    finite_gate = next(row for row in gates if row["row_id"] == "GATE2057_3_finite_rows")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2057_4_local_GR")
    no_score = all(not bool(row.get("accepted_for_scoring", False)) for row in runner) and all(
        not bool(row.get("ready_for_scoring", False)) for row in finite_rows
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2057_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2057_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2057_02_aux_signature_not_closed", aux_verdict["status"] == "AUXILIARY_SIGNATURE_NOT_CLOSED", "auxiliary theorem remains conditional/unsigned"))
    checks.append(("VAL2057_03_source_schema_strict", source_pack_ready and missing_markers_present, "finite source schema exists but remains missing/nonclaim"))
    checks.append(("VAL2057_04_runner_blocks_all", runner_verdict["verdict"] == "AUXILIARY_NOT_SIGNED_FINITE_NOT_SOURCE_READY_NONCLAIM", "runner blocks zero theorem and finite scoring"))
    checks.append(("VAL2057_05_no_score", no_score, "no theorem/template row is accepted for scoring"))
    checks.append(("VAL2057_06_aux_gate_blocked", aux_gate["status"] == "FAIL_BLOCKED", "auxiliary signature gate remains blocked"))
    checks.append(("VAL2057_07_finite_gate_blocked", finite_gate["status"] == "FAIL_BLOCKED", "finite source-row gate remains blocked"))
    checks.append(("VAL2057_08_local_GR_blocked", local_gate["status"] == "FAIL_BLOCKED", "local GR/Newton claim remains blocked"))
    checks.append(("VAL2057_09_next_selected", next_rows_[0]["target_id"] == "NEXT2057_0_2058", "2058 radial-cell owner/closure baseline target selected"))
    checks.append(("VAL2057_10_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2057_11_no_formalization_2057_artifacts", not formalization_has_2057_artifacts(), "no 2057 artifacts were written under formalization-workbench"))
    checks.append(("VAL2057_12_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2057_OVERALL", overall, "2057 rejects current auxiliary claim, stages strict finite source schema, and selects radial-cell owner next"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    aux_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2057 Y5 R2FR Z_R Infinity Owner Or Auxiliary Protection Signature",
        "",
        "## Current Verdict",
        "",
        "2057 attempts the clean route first and rejects it as a current claim. The second-class/algebraic auxiliary compatibility mechanism is still the best exact derivation candidate: if `R_AB,Lambda_R` are parent-owned auxiliaries, protected from derivative operators, boundary charge, matter source and readout regeneration, then the `R_AB` branch can be eliminated before local readout.",
        "",
        "But the current corpus does not parent-sign those protections. The live gap is no longer algebraic manipulation; it is parent necessity. We need the parent radial-cell owner that makes `Lambda_R C_R` required rather than appended. Without that, `Z_R=0`, `q_R=0`, local GR and Newton remain blocked.",
        "",
        "The finite fallback is now strict: if the parent owner cannot be derived, the branch needs source-backed `Z_R_infty`, `N_sphere`, `M_R^2`, `Pi_R`, same-frame `r_s`, absolute tails, and arena kernels before any score. Template rows remain invalid by design.",
        "",
        "No `Z_R=0`, `omega_W=1`, `q_R=0`, local-GR/Newton, PPN pass, GitHub action, or `formalization-workbench` edit is claimed.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Auxiliary Protection Signature Audit",
        md_table(aux_rows, ["row_id", "clause", "evidence", "status", "failure_mode", "required_next", "closes_zero_theorem", "claim_allowed"]),
        "## Strict Finite Source Schema",
        md_table(finite_rows, ["row_id", "quantity", "role", "units", "required_source", "current_value", "valid_prediction_row", "ready_for_scoring", "valid_for_claim", "claim_allowed"]),
        "## Branch Runner",
        md_table(runner, ["run_id", "target", "accepted_for_scoring", "verdict", "reason", "claim_allowed"]),
        "## Claim Gate",
        md_table(gates, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decisions, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    aux_rows = auxiliary_signature_rows()
    finite_rows = finite_source_schema_rows()
    runner = branch_runner_rows(aux_rows, finite_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2057_SOURCE_REGISTER.csv",
        "aux": OUT / "P8_Y5_PARENT_QLOC_2057_AUXILIARY_SIGNATURE_AUDIT.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2057_STRICT_FINITE_SOURCE_SCHEMA.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2057_BRANCH_RUNNER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2057_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2057_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2057_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2057_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2057_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["aux"], aux_rows)
    write_csv(paths["finite"], finite_rows)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(aux_rows, finite_rows, runner, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, aux_rows, finite_rows, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, aux_rows, finite_rows, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, aux_rows, finite_rows, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
