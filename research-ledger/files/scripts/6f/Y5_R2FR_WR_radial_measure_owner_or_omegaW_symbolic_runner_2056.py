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


DOC = ROOT / "2056-Y5-R2FR-WR-radial-measure-owner-or-omegaW-symbolic-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2056_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2056-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2056*",
            "*Y5_R2FR_WR_radial_measure_owner_or_omegaW_symbolic_runner_2056*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2056_00_2055_doc",
            DOC.parent / "2055-Y5-R2FR-PiR-boundary-momentum-or-WR-asymptotic-normalization.md",
            ["NEXT2055_0_2056", "omega_W=lim W_R/r^2", "q_R^PPN=Pi_R/(omega_W r_s)"],
            "2055 handoff: omega_W is the next local-GR bottleneck.",
        ),
        (
            "SRC2056_01_2055_next",
            OUT / "P8_Y5_PARENT_QLOC_2055_NEXT_TARGET.csv",
            ["NEXT2055_0_2056", "radial reduced action measure", "omega_W source row"],
            "machine-readable 2056 target from 2055.",
        ),
        (
            "SRC2056_02_reciprocity_action",
            ROOT / "05-reciprocity-theorem-attempt.md",
            ["S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB].", "W R_AB' = Q_R."],
            "one-dimensional reciprocal strain equation.",
        ),
        (
            "SRC2056_03_source_neutrality",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["delta S_boundary = [W R_AB' + Pi_R] delta R_AB|_surface.", "Q_R = -Pi_R."],
            "boundary sign convention for Pi_R.",
        ),
        (
            "SRC2056_04_2050_strain",
            ROOT / "2050-Y5-R2FR-minimal-motion-load-radial-action-or-RAB-residual-runner.md",
            ["S_strain=int dr [0.5 W_R (partial_r C_R)^2 + J_R C_R]", "W_R partial_r C_R=Q_R"],
            "minimal radial strain action and finite-hair warning.",
        ),
        (
            "SRC2056_05_1256_parent_Hcore",
            ROOT / "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            [
                "H_R = int_Sigma sqrt(h)[1/2 Z_R h^{ij} D_i R_AB D_j R_AB",
                "partial_r(r^2 Z_R partial_r R_AB)=0",
                "r^2 Z_R partial_r R_AB = Q_R",
            ],
            "parent H_core spherical reduction: omega_W is owned by Z_R and radial measure.",
        ),
        (
            "SRC2056_06_1253_boundary",
            ROOT / "1253-Y5-R10-reciprocal-Hcore-boundary-charge-derivation-attempt.md",
            ["BCA1253_0_QR_current_constant", "for W=r^2", "MISSING_BOUNDARY_CHARGE_CLASS"],
            "prior W=r^2 analogy is only a current-shape example, not normalization evidence.",
        ),
        (
            "SRC2056_07_1265_auxiliary",
            ROOT / "1265-Y5-R10-RAB-auxiliary-constraint-protection-or-finite-ZR-bound-runner.md",
            ["algebraic auxiliary elimination", "no legal `Z_R` kinetic operator", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"],
            "alternative clean route: protect auxiliary R_AB so Z_R is absent instead of normalized.",
        ),
        (
            "SRC2056_08_wr_contract",
            OUT / "P8_Y5_PARENT_QLOC_1886_FINITE_WR_BETAW_ROW_CONTRACT.csv",
            ["FWR1886_1_wR", "numeric source/action weight coefficient or theorem-zero", "tau_PPN"],
            "source-weight contract forbids unity-by-convenience.",
        ),
        (
            "SRC2056_09_source_mass_tail",
            OUT / "P8_Y5_PARENT_QLOC_1639_SOURCE_MASS_AND_TAIL_BLOCKERS.csv",
            ["NRB1639_0_tail_normalization", "NRB1639_1_same_frame_mass", "MISSING_PARENT_SOURCE_MASS_CALIBRATION"],
            "same-frame source mass and tail blockers remain live.",
        ),
        (
            "SRC2056_10_tail_inputs",
            OUT / "P8_Y5_PARENT_QLOC_1872_ABSOLUTE_TAIL_BOUND_INPUTS_NONCLAIM.csv",
            ["ABI1872_1_PiR", "MISSING_Pi_R_BOUND_OR_ZERO_THEOREM", "ABI1872_3_gamma_bound"],
            "absolute tail and Pi_R source-row blockers.",
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


def wr_measure_derivation_rows() -> list[dict[str, object]]:
    data = [
        (
            "WRD2056_0_starting_contract",
            "3D parent kinetic sector",
            "H_R contains integral sqrt(h) 0.5 Z_R h^{ij} D_i C_R D_j C_R plus non-kinetic terms",
            "FORMAL_FROM_1256_NOT_PARENT_SIGNED",
            "Z_R is the owner of the radial strain weight if a kinetic R_AB/C_R sector exists",
            "Z_R origin and allowed sector are not signed by the parent action",
        ),
        (
            "WRD2056_1_spherical_reduction",
            "static areal exterior",
            "for C_R=C_R(r), the radial coefficient is W_R(r)=N_sphere Z_R(r) sqrt(h) h^{rr} after angular/1D normalization",
            "DERIVED_AS_REDUCTION_RULE",
            "the r^2 part comes from the areal sphere measure, not from a chosen closure",
            "N_sphere convention and asymptotic coframe normalization must be declared",
        ),
        (
            "WRD2056_2_asymptotic_limit",
            "asymptotically flat observed frame",
            "if h_rr -> 1 and Z_R(r)->Z_R_infty, then omega_W:=lim W_R/r^2 = N_sphere Z_R_infty",
            "OMEGA_OWNER_IDENTIFIED_SYMBOLICALLY",
            "omega_W is now tied to the parent kinetic coefficient and angular normalization",
            "Z_R_infty and N_sphere are not numeric/source-backed here",
        ),
        (
            "WRD2056_3_1256_match",
            "1256 constant-coefficient limit",
            "partial_r(r^2 Z_R partial_r R_AB)=0 is the N_sphere-absorbed convention with omega_W=Z_R",
            "MATCHES_PRIOR_HCORE_SHAPE",
            "explains why W_R=r^2 was only the special Z_R=1 absorbed-normalization case",
            "does not prove Z_R=1 or Q_R=0",
        ),
        (
            "WRD2056_4_gamma_conversion",
            "PPN q_R conversion",
            "q_R^PPN = Pi_R/(N_sphere Z_R_infty r_s) when the massless 1/r branch and 06 boundary orientation apply",
            "CONVERSION_REFINED_NONCLAIM",
            "2055 omega_W slot is replaced by explicit owners",
            "Pi_R, Z_R_infty, N_sphere, r_s and tails remain missing",
        ),
        (
            "WRD2056_5_massive_exception",
            "massive or non-asymptotic branch",
            "if M_R^2>0 or Z_R lacks a finite limit, the 1/r Cassini q_R row must be replaced by a range/profile runner",
            "PROFILE_BRANCH_SPLIT_REQUIRED",
            "prevents forcing every residual into the same PPN-gamma coefficient",
            "M_R^2 and source profile are not parent-sourced",
        ),
        (
            "WRD2056_6_verdict",
            "2056 omega_W result",
            "omega_W is derivable as N_sphere Z_R_infty conditional on a kinetic radial sector and an asymptotically areal observed frame",
            "OWNER_DERIVED_SYMBOLIC_RUNNER_BLOCKED",
            "real progress: the missing coupling is no longer free-form",
            "numeric scoring waits on Z_R_infty or the auxiliary-protection theorem",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, item, derivation, status, meaning, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "item": item,
                "derivation": derivation,
                "status": status,
                "meaning": meaning,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def omega_owner_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "OWN2056_0_W_equals_r2",
            "W_R=r^2",
            "demoted",
            "allowed only as the special absorbed-normalization, Z_R_infty=1 example",
            "not a parent proof and not a numeric input",
        ),
        (
            "OWN2056_1_N_sphere",
            "N_sphere",
            "missing_convention",
            "equals 1 if the angular 4pi factor is absorbed into Q_R/Pi_R; equals 4pi if not",
            "must be declared with the same boundary flux normalization",
        ),
        (
            "OWN2056_2_ZR_infty",
            "Z_R_infty",
            "missing_parent_coefficient",
            "the actual asymptotic kinetic coefficient of the reciprocal/compatibility strain sector",
            "must come from parent action, source row, or protected-auxiliary zero theorem",
        ),
        (
            "OWN2056_3_auxiliary_escape",
            "protected auxiliary R_AB",
            "conditional_clean_route",
            "if AP1265 clauses are parent-signed, no kinetic sector exists and omega_W scoring is bypassed by Z_R=0/no Pi_R sector",
            "AP1265 grammar/protection/readout clauses are not signed",
        ),
        (
            "OWN2056_4_finite_kinetic_route",
            "finite kinetic R_AB branch",
            "source_row_required",
            "if Z_R_infty>0, q_R^PPN is finite and must be bounded through Pi_R/(N_sphere Z_R_infty r_s)",
            "needs Pi_R, same-frame r_s, tails and arena projection",
        ),
        (
            "OWN2056_5_massive_route",
            "massive/screened branch",
            "separate_profile_required",
            "if M_R^2>0, ell_R=sqrt(Z_R/M_R^2) controls suppression and Cassini/R10 need range kernels",
            "needs M_R^2 and source profile, not just omega_W",
        ),
        (
            "OWN2056_6_verdict",
            "omega ownership audit",
            "symbolic_owner_found_nonclaim",
            "omega_W is owned by N_sphere and Z_R_infty, or removed by a protected auxiliary theorem",
            "neither route is parent-signed enough to claim local GR",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, status, role, missing in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "status": status,
                "role": role,
                "missing_for_claim": missing,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def profile_update_rows() -> list[dict[str, object]]:
    data = [
        (
            "OPR2056_0_omega_owner",
            "omega_W",
            "omega_W=N_sphere Z_R_infty",
            "finite positive symbolic owner if kinetic branch is active",
            "same units as one-dimensional W_R/r^2 convention",
            "SYMBOLIC_OWNER_ROW_NONCLAIM",
            "MISSING_Z_R_INFTY;MISSING_N_SPHERE_CONVENTION",
        ),
        (
            "OPR2056_1_qR_refined",
            "q_R^PPN",
            "q_R^PPN=Pi_R/(N_sphere Z_R_infty r_s)",
            "Cassini row can be evaluated only after owner and tails are supplied",
            "dimensionless",
            "REFINED_SYMBOLIC_BOUND_NONCLAIM",
            "MISSING_PIR_VALUE;MISSING_Z_R_INFTY;MISSING_N_SPHERE;MISSING_SAME_FRAME_RS;MISSING_TAIL_BUDGET",
        ),
        (
            "OPR2056_2_auxiliary_zero_lane",
            "Z_R=0 protected auxiliary lane",
            "if AP1265 all signed, R_AB is eliminated and no omega_W/q_R hair exists",
            "cleanest local-GR route but only conditional",
            "theorem",
            "CONDITIONAL_ZERO_ROUTE_UNSIGNED",
            "MISSING_PARENT_AUXILIARY_PROTECTION_SIGNATURE",
        ),
        (
            "OPR2056_3_massive_profile_lane",
            "M_R^2 positive branch",
            "ell_R=sqrt(Z_R/M_R^2) replaces pure 1/r profile",
            "requires R10/PPN range/profile kernels",
            "length",
            "SEPARATE_PROFILE_RUNNER_REQUIRED",
            "MISSING_M_R2;MISSING_PROFILE_KERNELS",
        ),
        (
            "OPR2056_4_runner_status",
            "score state",
            "owner identified, no numeric/theorem owner accepted",
            "do not score",
            "nonclaim",
            "RUNNER_BLOCKED_NONCLAIM",
            "source-ready, not evidence",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, formula, rule, units, status, missing_for_score in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "rule": rule,
                "units": units,
                "status": status,
                "missing_for_score": missing_for_score,
                "source_ready_schema": True,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def omega_runner_rows(profile_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for profile_row in profile_rows:
        row = base_row()
        row.update(
            {
                "run_id": "RUN_" + str(profile_row["row_id"]),
                "quantity": profile_row["quantity"],
                "source_ready_schema": profile_row["source_ready_schema"],
                "accepted_for_scoring": False,
                "verdict": "SYMBOLIC_OWNER_ROW_NONCLAIM",
                "reason": profile_row["missing_for_score"],
                "claim_allowed": False,
            }
        )
        rows.append(row)
    verdict = base_row()
    verdict.update(
        {
            "run_id": "RUN2056_VERDICT",
            "quantity": "omega_W_owner",
            "source_ready_schema": True,
            "accepted_for_scoring": False,
            "verdict": "OMEGA_OWNER_IDENTIFIED_SYMBOLICALLY_BUT_BLOCKED",
            "reason": "omega_W=N_sphere Z_R_infty is derived conditionally; Z_R_infty/N_sphere/Pi_R/r_s/tails or auxiliary protection signature remain missing",
            "claim_allowed": False,
        }
    )
    rows.append(verdict)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "GATE2056_0_owner_formula",
            "omega_W owner formula derived",
            "PASS_NONCLAIM",
            "omega_W=N_sphere Z_R_infty follows from spherical radial reduction when a kinetic sector exists",
        ),
        (
            "GATE2056_1_no_unity_shortcut",
            "W_R=r^2 shortcut rejected",
            "PASS_NONCLAIM",
            "unity is allowed only after N_sphere and Z_R_infty conventions are parent-signed",
        ),
        (
            "GATE2056_2_numeric_omega",
            "numeric omega_W supplied",
            "FAIL_BLOCKED",
            "Z_R_infty and N_sphere are symbolic/missing",
        ),
        (
            "GATE2056_3_auxiliary_zero",
            "protected auxiliary zero theorem signed",
            "FAIL_BLOCKED",
            "AP1265 protection clauses remain candidate-only",
        ),
        (
            "GATE2056_4_PPN_score",
            "q_R/Pi_R row scoreable",
            "FAIL_BLOCKED",
            "Pi_R, same-frame r_s and tail budget remain missing",
        ),
        (
            "GATE2056_5_local_GR",
            "local GR/Newton claimed",
            "FAIL_BLOCKED",
            "neither finite residual bound nor auxiliary elimination theorem is complete",
        ),
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
            "DEC2056_0_result",
            "2056 identifies the owner of omega_W.",
            "In the kinetic branch, omega_W is not a free coupling: it is N_sphere Z_R_infty from radial measure plus parent kinetic coefficient.",
        ),
        (
            "DEC2056_1_not_claimed",
            "The owner is symbolic, not evidence.",
            "No current row supplies Z_R_infty, N_sphere, Pi_R, same-frame r_s, or a signed auxiliary-protection theorem.",
        ),
        (
            "DEC2056_2_best_next",
            "The next leap is choosing the branch.",
            "Either parent-sign AP1265 auxiliary protection and remove R_AB hair, or source Z_R_infty/M_R^2/Pi_R for a finite residual runner.",
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
            "target_id": "NEXT2056_0_2057",
            "target_doc": "2057-Y5-R2FR-ZR-infinity-owner-or-auxiliary-protection-signature.md",
            "objective": "try to parent-sign the AP1265 auxiliary-protection route; if it fails, create strict source rows for Z_R_infty, N_sphere, M_R^2, Pi_R and same-frame r_s without scoring",
            "must_include": "AP1265 clause audit; Z_R_infty source schema; N_sphere boundary normalization convention; massive-profile split; updated q_R runner; no-cancellation/tail guards",
            "excluded": "declaring Z_R=0 by preference; setting Z_R_infty=1 by normalization without boundary convention; scoring omega_W while symbolic; local-GR/Newton claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    derivation: list[dict[str, object]],
    owner_audit: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2056_0_source_weight_omega_owner",
            SOURCE_WEIGHT_DOCS / "AFRAME_OMEGAW_OWNER_2056_NONCLAIM.csv",
            derivation,
        ),
        (
            "COPY2056_1_wep_omega_owner",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2056_OMEGA_OWNER_AUDIT_NONCLAIM.csv",
            owner_audit,
        ),
        (
            "COPY2056_2_wep_profile_update",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2056_QR_PROFILE_UPDATE_NONCLAIM.csv",
            profile_rows,
        ),
        (
            "COPY2056_3_wep_runner",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2056_OMEGA_RUNNER_NONCLAIM.csv",
            runner,
        ),
        (
            "COPY2056_4_rab_next",
            QUEUE / "JR2056_ZR_INFINITY_OR_AUX_PROTECTION_NEXT_NONCLAIM.csv",
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
    derivation: list[dict[str, object]],
    owner_audit: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    verdict_row = next(row for row in derivation if row["row_id"] == "WRD2056_6_verdict")
    omega_row = next(row for row in derivation if row["row_id"] == "WRD2056_2_asymptotic_limit")
    owner_verdict = next(row for row in owner_audit if row["row_id"] == "OWN2056_6_verdict")
    profile_ids = {str(row["row_id"]) for row in profile_rows}
    runner_verdict = next(row for row in runner if row["run_id"] == "RUN2056_VERDICT")
    numeric_gate = next(row for row in gates if row["row_id"] == "GATE2056_2_numeric_omega")
    aux_gate = next(row for row in gates if row["row_id"] == "GATE2056_3_auxiliary_zero")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2056_5_local_GR")
    no_score = all(not bool(row.get("ready_for_scoring", False)) for row in profile_rows) and all(
        not bool(row.get("accepted_for_scoring", False)) for row in runner
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2056_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2056_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2056_02_owner_formula", "omega_W:=lim W_R/r^2 = N_sphere Z_R_infty" in str(omega_row["derivation"]), "omega_W owner formula is explicit"))
    checks.append(("VAL2056_03_symbolic_verdict", verdict_row["status"] == "OWNER_DERIVED_SYMBOLIC_RUNNER_BLOCKED", "owner is derived symbolically but blocked for scoring"))
    checks.append(("VAL2056_04_owner_audit_nonclaim", owner_verdict["status"] == "symbolic_owner_found_nonclaim", "owner audit remains nonclaim"))
    checks.append(("VAL2056_05_profile_coverage", {"OPR2056_0_omega_owner", "OPR2056_1_qR_refined", "OPR2056_2_auxiliary_zero_lane"}.issubset(profile_ids), "omega, q_R and auxiliary-zero lanes are present"))
    checks.append(("VAL2056_06_runner_blocked", runner_verdict["verdict"] == "OMEGA_OWNER_IDENTIFIED_SYMBOLICALLY_BUT_BLOCKED", "runner blocks scoring while preserving owner formula"))
    checks.append(("VAL2056_07_no_score", no_score, "no symbolic omega/profile row is accepted for scoring"))
    checks.append(("VAL2056_08_numeric_gate_blocked", numeric_gate["status"] == "FAIL_BLOCKED", "numeric omega gate remains blocked"))
    checks.append(("VAL2056_09_aux_gate_blocked", aux_gate["status"] == "FAIL_BLOCKED", "auxiliary zero theorem remains blocked"))
    checks.append(("VAL2056_10_local_GR_blocked", local_gate["status"] == "FAIL_BLOCKED", "local GR/Newton claim remains blocked"))
    checks.append(("VAL2056_11_next_selected", next_rows_[0]["target_id"] == "NEXT2056_0_2057", "2057 Z_R infinity/auxiliary protection target selected"))
    checks.append(("VAL2056_12_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2056_13_no_formalization_2056_artifacts", not formalization_has_2056_artifacts(), "no 2056 artifacts were written under formalization-workbench"))
    checks.append(("VAL2056_14_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2056_OVERALL", overall, "2056 derives symbolic omega_W ownership, blocks scoring and selects Z_R/auxiliary branch choice next"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    derivation: list[dict[str, object]],
    owner_audit: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2056 Y5 R2FR W_R Radial Measure Owner Or omega_W Symbolic Runner",
        "",
        "## Current Verdict",
        "",
        "2056 makes real progress on the coupling bottleneck. In the finite kinetic radial branch, `omega_W` is not a loose fitted coupling: reducing the parent kinetic sector `sqrt(h) Z_R h^{ij} D_i C_R D_j C_R` on a static areal exterior gives `W_R(r)=N_sphere Z_R(r) sqrt(h) h^{rr}` in the one-dimensional radial convention. If `h_rr -> 1` and `Z_R(r)->Z_R_infty`, then `omega_W=lim W_R/r^2=N_sphere Z_R_infty`.",
        "",
        "So the 2055 conversion sharpens to `q_R^PPN=Pi_R/(N_sphere Z_R_infty r_s)` on the massless `1/r` branch. This kills the hidden `W_R=r^2` shortcut: unity is only allowed after the angular/boundary normalization and `Z_R_infty` are parent-signed.",
        "",
        "This is still not a local-GR claim. The live fork is now explicit: either parent-sign the AP1265 protected auxiliary route so `R_AB` has no kinetic/boundary hair, or source the finite kinetic inputs `Z_R_infty`, `N_sphere`, `Pi_R`, `r_s`, tails and possibly `M_R^2` for the screened branch.",
        "",
        "No `Z_R=0`, `omega_W=1`, `q_R=0`, local-GR/Newton, PPN pass, GitHub action, or `formalization-workbench` edit is claimed.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## W_R Measure Derivation",
        md_table(derivation, ["row_id", "item", "derivation", "status", "meaning", "blocker", "claim_allowed"]),
        "## omega_W Owner Audit",
        md_table(owner_audit, ["row_id", "quantity", "status", "role", "missing_for_claim", "claim_allowed"]),
        "## Updated omega/q_R Profile Rows",
        md_table(profile_rows, ["row_id", "quantity", "formula", "rule", "units", "status", "missing_for_score", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
        "## Runner",
        md_table(runner, ["run_id", "quantity", "source_ready_schema", "accepted_for_scoring", "verdict", "reason", "claim_allowed"]),
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
    derivation = wr_measure_derivation_rows()
    owner_audit = omega_owner_audit_rows()
    profile_rows = profile_update_rows()
    runner = omega_runner_rows(profile_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2056_SOURCE_REGISTER.csv",
        "derivation": OUT / "P8_Y5_PARENT_QLOC_2056_WR_MEASURE_DERIVATION.csv",
        "owner_audit": OUT / "P8_Y5_PARENT_QLOC_2056_OMEGA_OWNER_AUDIT.csv",
        "profiles": OUT / "P8_Y5_PARENT_QLOC_2056_PROFILE_UPDATE_NONCLAIM.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2056_OMEGA_RUNNER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2056_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2056_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2056_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2056_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2056_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["derivation"], derivation)
    write_csv(paths["owner_audit"], owner_audit)
    write_csv(paths["profiles"], profile_rows)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(derivation, owner_audit, profile_rows, runner, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, derivation, owner_audit, profile_rows, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, derivation, owner_audit, profile_rows, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, derivation, owner_audit, profile_rows, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
