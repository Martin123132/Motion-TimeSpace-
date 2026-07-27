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


DOC = ROOT / "2058-Y5-R2FR-parent-radial-cell-owner-or-local-closure-baseline.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2058_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2058-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2058*",
            "*Y5_R2FR_parent_radial_cell_owner_or_local_closure_baseline_2058*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2058_00_2057_doc",
            ROOT / "2057-Y5-R2FR-ZR-infinity-owner-or-auxiliary-protection-signature.md",
            ["NEXT2057_0_2058", "Lambda_R C_R is required by a parent radial-cell owner", "AUXILIARY_SIGNATURE_NOT_CLOSED"],
            "2057 handoff: parent radial-cell owner is the upstream gap.",
        ),
        (
            "SRC2058_01_2057_next",
            OUT / "P8_Y5_PARENT_QLOC_2057_NEXT_TARGET.csv",
            ["NEXT2057_0_2058", "J_q=T sqrt(S)", "parent L_core/H_core owner"],
            "machine-readable 2058 target.",
        ),
        (
            "SRC2058_02_1272_parent_necessity",
            ROOT / "1272-Y5-R10-RAB-auxiliary-parent-necessity-from-radial-cell-variational-principle-or-finite-source-row.md",
            ["RCD1272_1_liouville_phase_volume", "PARENT_NECESSITY_NOT_DERIVED", "J_q=1"],
            "most direct prior derivation attempt for radial-cell owner.",
        ),
        (
            "SRC2058_03_2049_euler_gate",
            ROOT / "2049-Y5-R2FR-motion-load-parent-Euler-difference-or-RAB-finite-residual.md",
            ["ECO2049_5_verdict", "COORDINATES_READY_EULER_PAIR_MISSING", "RAB2049_VERDICT"],
            "R2FR motion-load Euler gate and finite residual fallback.",
        ),
        (
            "SRC2058_04_observer_contract",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["R_AB = ln(T^2 S) = 2 ln(J_q).", "all matter sectors couple to the same observer coframe"],
            "observer-cell identity and same-coframe contract.",
        ),
        (
            "SRC2058_05_phase_volume",
            ROOT / "08-phase-volume-reciprocity-origin.md",
            ["phase_volume_reciprocity_motivated_not_parent_derived"],
            "phase-volume route motivation and obstruction.",
        ),
        (
            "SRC2058_06_hamiltonian_cell",
            ROOT / "09-hamiltonian-radial-cell-derivation.md",
            ["hamiltonian_radial_cell_sharpened_not_parent_derived"],
            "Hamiltonian radial-cell sharpening without parent derivation.",
        ),
        (
            "SRC2058_07_cell_current",
            ROOT / "11-cell-current-origin-attempt.md",
            ["cell_current_origin_no_charge_obstruction"],
            "current/no-charge route obstruction.",
        ),
        (
            "SRC2058_08_closure_firewall",
            ROOT / "1278-Y5-R10-RAB-explicit-local-closure-runner-and-A511-origin-priority-ladder.md",
            ["local_closure_baseline", "closure_only=true", "BR1278_0_local_closure_baseline"],
            "existing closure firewall and no-claim branch separation.",
        ),
        (
            "SRC2058_09_finite_schema_2057",
            OUT / "P8_Y5_PARENT_QLOC_2057_STRICT_FINITE_SOURCE_SCHEMA.csv",
            ["FSR2057_0_ZR_infty", "MISSING_Z_R_INFTY_OR_PARENT_ZERO_THEOREM", "FSR2057_8_q_loc_profile"],
            "strict finite source schema from 2057.",
        ),
        (
            "SRC2058_10_ppn_bound_2053",
            OUT / "P8_Y5_PARENT_QLOC_2053_QR_BOUND_ROWS_NONCLAIM.csv",
            ["QB2053_0_areal_qR_conservative", "6.7e-05", "CONDITIONAL_BOUND_ROW_NONCLAIM"],
            "source-backed Cassini q_R bound row, still nonclaim.",
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


def radial_owner_attempt_rows() -> list[dict[str, object]]:
    data = [
        (
            "OWN2058_0_identity",
            "observer radial-cell identity",
            "J_q=T sqrt(S), C_R=ln(T^2S)=2lnJ_q",
            "PASS_IDENTITY_NONCLAIM",
            "defines the GR-lock variable exactly",
            "identity has no Euler-Lagrange force",
        ),
        (
            "OWN2058_1_liouville",
            "full radial phase-volume/Liouville preservation",
            "J_q J_p=1 for compensating momentum cell",
            "FAILS_PRODUCT_ONLY",
            "works for arbitrary J_q if J_p compensates",
            "cannot derive J_q=1 or C_R=0",
        ),
        (
            "OWN2058_2_null_ratio",
            "radial null propagation",
            "light cone constrains a T/sqrt(S)-type ratio",
            "FAILS_TO_FIX_PRODUCT",
            "ratio constraints do not determine T sqrt(S)",
            "cannot select the reciprocal product",
        ),
        (
            "OWN2058_3_newton_limit",
            "Newtonian slow-particle limit",
            "fixes lapse/clock normalization at leading order",
            "FAILS_TO_FIX_RADIAL_ROUTING",
            "Newtonian recovery does not select S or beta/local spatial law",
            "cannot derive p=1 or AB=1",
        ),
        (
            "OWN2058_4_capacity_reciprocity",
            "motion/time/space reciprocal capacity",
            "local vacuum calibration wants T sqrt(S)=1",
            "MOTIVATED_NOT_VARIATIONAL",
            "this is physically coherent and matches the desired lock",
            "needs L_core/H_core owner, not prose motivation",
        ),
        (
            "OWN2058_5_direct_multiplier",
            "Lambda_R C_R constraint",
            "delta_Lambda gives C_R=0 exactly",
            "CLOSURE_IF_UNOWNED",
            "the algebra works and is the cleanest mechanism",
            "Lambda_R origin and necessity are not parent-derived",
        ),
        (
            "OWN2058_6_parent_Euler_pair",
            "E_time/E_radial parent action difference",
            "D_R[MTS] should follow from delta S_parent/delta lnT and delta S_parent/delta lnsqrtS",
            "TARGET_NOT_EXTRACTED",
            "this is the correct non-smuggling derivation route",
            "full parent radial action is absent",
        ),
        (
            "OWN2058_7_current_route",
            "second-order reciprocal current",
            "partial_r(W_R partial_r C_R)=J_R",
            "LEAVES_HAIR_WITHOUT_NO_CHARGE",
            "useful finite residual framework",
            "Q_R/Pi_R no-charge theorem is unsigned",
        ),
        (
            "OWN2058_8_verdict",
            "parent radial-cell owner",
            "no available route derives J_q=1 or Lambda_R C_R necessity from current corpus",
            "PARENT_OWNER_NOT_DERIVED",
            "local closure can be used only as an explicit nonclaim control",
            "finite residual acquisition remains mandatory for claims",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, candidate, formula, status, useful_part, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "candidate": candidate,
                "formula_or_test": formula,
                "status": status,
                "useful_part": useful_part,
                "blocker": blocker,
                "derives_C_R_zero": status in {"PASS_DERIVED"},
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def closure_baseline_rows() -> list[dict[str, object]]:
    data = [
        (
            "LCB2058_0_branch",
            "local_closure_baseline",
            "C_R=0; Q_R=0; S_R=0; boundary normalization fixed",
            True,
            False,
            False,
            "internal control/baseline only",
            "promoting it as derived MTS local GR",
        ),
        (
            "LCB2058_1_ppn_gamma",
            "closure PPN gamma control",
            "q_R^PPN=0 by closure assumption",
            True,
            False,
            False,
            "debugs PPN pipeline against GR-like zero residual",
            "using closure gamma as beta/Newton proof",
        ),
        (
            "LCB2058_2_finite_branch_separation",
            "finite residual branch",
            "requires live source-backed C_R/q_R/Pi_R/Z_R/tau rows",
            False,
            False,
            False,
            "disabled until source rows exist",
            "mixing finite templates with closure assumptions",
        ),
        (
            "LCB2058_3_public_claim",
            "claim posture",
            "derived_local_GR=false; pass_for_claim=false",
            True,
            False,
            False,
            "honest private control statement",
            "public/local-GR claim from closure",
        ),
        (
            "LCB2058_4_reopen_condition",
            "derivation route reopen",
            "new parent L_core/H_core owner or extracted Euler pair",
            False,
            False,
            False,
            "reopens derivation if genuinely new parent input arrives",
            "another AP1265 replay without new parent action",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, branch, assumption, closure_only, derived_local_gr, pass_for_claim, allowed_use, hard_refusal in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "branch": branch,
                "assumption_or_rule": assumption,
                "closure_only": closure_only,
                "derived_local_GR": derived_local_gr,
                "pass_for_claim": pass_for_claim,
                "allowed_use": allowed_use,
                "hard_refusal": hard_refusal,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_acquisition_gate_rows() -> list[dict[str, object]]:
    data = [
        ("FAG2058_0_C_R_profile", "C_R(r)=ln(T^2S)", "finite radial-cell strain profile", "profile formula, units, source path, gauge/readout convention", "MISSING_PROFILE_OR_ZERO_THEOREM", "PPN;orbital;clock;local_GR"),
        ("FAG2058_1_qR_PiR", "q_R^PPN or Pi_R", "massless 1/r reciprocal hair", "q_R profile or Pi_R boundary flux plus N_sphere/Z_R/r_s convention", "MISSING_QR_OR_PIR_VALUE", "PPN;Cassini;Shapiro"),
        ("FAG2058_2_ZR_Nsphere", "Z_R_infty;N_sphere", "omega_W owner for finite kinetic branch", "parent coefficient/theorem-zero and boundary normalization", "MISSING_Z_R_INFTY_OR_N_SPHERE", "PPN;R10;orbital"),
        ("FAG2058_3_MR2", "M_R^2", "screened/massive branch range", "local Hessian or sourced screening scale ell_R", "MISSING_M_R2_OR_ELL_R", "R10;PPN;orbital"),
        ("FAG2058_4_source_balance", "S_R[source]", "time-radial source anisotropy", "source-balance theorem or finite source row", "MISSING_SOURCE_BALANCE", "Newton;WEP;orbital"),
        ("FAG2058_5_boundary_tail", "B_R;Pi_R;Q_R", "boundary no-charge or finite flux", "boundary class, orientation, reference subtraction, no-cancellation policy", "MISSING_BOUNDARY_ZERO_OR_FLUX", "PPN;clock;orbital"),
        ("FAG2058_6_same_frame_mass", "r_s=2GM_obs/c^2", "same-frame source mass for observed metric", "mass/readout calibration from same coframe", "MISSING_SAME_FRAME_SOURCE_MASS", "PPN;Newton"),
        ("FAG2058_7_tail_budget", "delta_tail/gauge/readout/source", "absolute residual vector budget", "component bounds or theorem-zero certificates", "MISSING_ABSOLUTE_TAIL_BUDGET", "all_local_arenas"),
        ("FAG2058_8_tau_kernels", "tau_PPN;tau_R10;tau_clock;tau_orbital", "arena projections", "source-backed kernels and units", "MISSING_ARENA_PROJECTIONS", "PPN;R10;clock;orbital"),
        ("FAG2058_9_q_loc_profile", "epsilon_GK_q_loc", "Gamma/Khat local response leak", "metric-response identity or bounded profile", "MISSING_Q_LOC_PROFILE_OR_ZERO", "local_GR;PPN;clock"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, role, required_input, missing_marker, arenas in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "role": role,
                "required_input": required_input,
                "current_status": missing_marker,
                "observable_arenas": arenas,
                "ready_for_scoring": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows(
    owner_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    owner_verdict = next(row for row in owner_rows if row["row_id"] == "OWN2058_8_verdict")
    closure_branch = next(row for row in closure_rows if row["row_id"] == "LCB2058_0_branch")
    finite_missing = ";".join(str(row["current_status"]) for row in finite_rows)
    data = [
        (
            "RUN2058_0_parent_owner",
            "derive parent radial-cell owner",
            False,
            owner_verdict["status"],
            owner_verdict["blocker"],
        ),
        (
            "RUN2058_1_closure_baseline",
            "enable local closure baseline",
            False,
            "ENABLED_CONTROL_ONLY_NONCLAIM",
            f"closure_only={closure_branch['closure_only']}; derived_local_GR={closure_branch['derived_local_GR']}; pass_for_claim={closure_branch['pass_for_claim']}",
        ),
        (
            "RUN2058_2_finite_acquisition",
            "score finite local residual branch",
            False,
            "LOCKED_NO_SOURCE_READY_ROWS",
            finite_missing,
        ),
        (
            "RUN2058_3_ppn_bound",
            "use Cassini q_R bound",
            False,
            "BOUND_EXISTS_NONCLAIM_GUARDS_OPEN",
            "q_R profile/value, same-frame mass, gauge/readout and tail-zero/bounds missing",
        ),
        (
            "RUN2058_VERDICT",
            "2058 branch status",
            False,
            "PARENT_OWNER_NOT_DERIVED_CLOSURE_BASELINE_ONLY",
            "local route is now explicit closure/control unless a new parent L_core/H_core owner or source-backed finite residual rows are supplied",
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
        ("GATE2058_0_identity", "J_q and C_R identities established", "PASS_NONCLAIM", "C_R=2lnJ_q exactly"),
        ("GATE2058_1_parent_owner", "parent radial-cell owner derived", "FAIL_BLOCKED", "no L_core/H_core term or Euler pair forces J_q=1"),
        ("GATE2058_2_closure_baseline", "closure baseline explicitly labeled", "PASS_NONCLAIM", "closure_only=true and pass_for_claim=false"),
        ("GATE2058_3_finite_residual", "finite residual branch scoreable", "FAIL_BLOCKED", "all acquisition rows remain missing/nonclaim"),
        ("GATE2058_4_local_GR_Newton", "derived local GR/Newton", "FAIL_BLOCKED", "closure is not derivation and finite branch is unscored"),
        ("GATE2058_5_no_branch_mixing", "closure/finite/EH lanes separated", "PASS_NONCLAIM", "closure control cannot be mixed with finite residual scoring"),
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
            "DEC2058_0_result",
            "Current corpus does not derive the parent radial-cell owner.",
            "`J_q=1` is the right local-GR lock, but identity, Liouville, null propagation, Newtonian limit, and current conservation do not force it.",
        ),
        (
            "DEC2058_1_closure",
            "The local zero branch is now closure baseline/control only.",
            "It can be useful for pipeline debugging and comparison, but cannot be cited as derived MTS local GR.",
        ),
        (
            "DEC2058_2_finite",
            "The claimable route now requires either a new parent L_core/H_core owner or source-backed finite residual rows.",
            "The finite acquisition gates name every missing quantity instead of letting closure hide them.",
        ),
        (
            "DEC2058_3_next",
            "Next useful work is a local closure scorecard plus finite residual acquisition pack.",
            "This moves toward testability while keeping the derivation route reopenable only with genuinely new parent action evidence.",
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
            "target_id": "NEXT2058_0_2059",
            "target_doc": "2059-Y5-R2FR-local-closure-scorecard-and-finite-residual-acquisition-pack.md",
            "objective": "build a nonclaim local closure control scorecard and a strict finite residual acquisition pack for PPN/R10/clock/orbital/Newton arenas; reopen derivation only if a concrete parent L_core/H_core owner is supplied",
            "must_include": "closure branch flags; no branch mixing; finite residual rows from FAG2058; Cassini q_R guard status; acquisition priorities; dry-run-only runner; no-cancellation vector",
            "excluded": "claiming closure as derived GR; scoring missing finite rows; repeating AP1265 or radial-cell owner without new parent action input; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    owner_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2058_0_source_weight_owner_attempt",
            SOURCE_WEIGHT_DOCS / "AFRAME_RADIAL_CELL_OWNER_2058_NONCLAIM.csv",
            owner_rows,
        ),
        (
            "COPY2058_1_wep_closure_baseline",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2058_LOCAL_CLOSURE_BASELINE_NONCLAIM.csv",
            closure_rows,
        ),
        (
            "COPY2058_2_wep_finite_gates",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2058_FINITE_ACQUISITION_GATES_NONCLAIM.csv",
            finite_rows,
        ),
        (
            "COPY2058_3_wep_runner",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2058_BRANCH_RUNNER_NONCLAIM.csv",
            runner,
        ),
        (
            "COPY2058_4_rab_next",
            QUEUE / "JR2058_LOCAL_CLOSURE_SCORECARD_FINITE_ACQUISITION_NEXT_NONCLAIM.csv",
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
    owner_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    owner_verdict = next(row for row in owner_rows if row["row_id"] == "OWN2058_8_verdict")
    closure_branch = next(row for row in closure_rows if row["row_id"] == "LCB2058_0_branch")
    finite_ready = all(not bool(row["ready_for_scoring"]) for row in finite_rows) and len(finite_rows) >= 10
    runner_verdict = next(row for row in runner if row["run_id"] == "RUN2058_VERDICT")
    owner_gate = next(row for row in gates if row["row_id"] == "GATE2058_1_parent_owner")
    finite_gate = next(row for row in gates if row["row_id"] == "GATE2058_3_finite_residual")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2058_4_local_GR_Newton")
    no_score = all(not bool(row.get("accepted_for_scoring", False)) for row in runner) and all(
        not bool(row.get("pass_for_claim", False)) for row in closure_rows
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2058_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2058_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2058_02_identity_ready", any(row["row_id"] == "OWN2058_0_identity" and row["status"] == "PASS_IDENTITY_NONCLAIM" for row in owner_rows), "J_q/C_R identity recorded"))
    checks.append(("VAL2058_03_parent_owner_rejected", owner_verdict["status"] == "PARENT_OWNER_NOT_DERIVED", "parent radial-cell owner is not derived"))
    checks.append(("VAL2058_04_closure_flags", bool(closure_branch["closure_only"]) and not bool(closure_branch["derived_local_GR"]) and not bool(closure_branch["pass_for_claim"]), "closure branch flags force nonclaim control"))
    checks.append(("VAL2058_05_finite_gates_ready", finite_ready, "finite acquisition gates are present and nonclaim"))
    checks.append(("VAL2058_06_runner_verdict", runner_verdict["verdict"] == "PARENT_OWNER_NOT_DERIVED_CLOSURE_BASELINE_ONLY", "runner demotes local branch to closure baseline"))
    checks.append(("VAL2058_07_no_score", no_score, "no closure or finite row is accepted for scoring/claim"))
    checks.append(("VAL2058_08_owner_gate_blocked", owner_gate["status"] == "FAIL_BLOCKED", "parent owner gate remains blocked"))
    checks.append(("VAL2058_09_finite_gate_blocked", finite_gate["status"] == "FAIL_BLOCKED", "finite residual gate remains blocked"))
    checks.append(("VAL2058_10_local_GR_blocked", local_gate["status"] == "FAIL_BLOCKED", "derived local GR/Newton claim remains blocked"))
    checks.append(("VAL2058_11_next_selected", next_rows_[0]["target_id"] == "NEXT2058_0_2059", "2059 closure scorecard/acquisition target selected"))
    checks.append(("VAL2058_12_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2058_13_no_formalization_2058_artifacts", not formalization_has_2058_artifacts(), "no 2058 artifacts were written under formalization-workbench"))
    checks.append(("VAL2058_14_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2058_OVERALL", overall, "2058 rejects parent owner from current evidence and installs explicit nonclaim closure baseline plus finite acquisition gates"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2058 Y5 R2FR Parent Radial-Cell Owner Or Local Closure Baseline",
        "",
        "## Current Verdict",
        "",
        "2058 rejects the parent radial-cell owner as a current derivation. The identity is sharp: `J_q=T sqrt(S)` and `C_R=ln(T^2S)=2lnJ_q`, so `J_q=1` would give the desired local reciprocal/GR lock. But identity is not dynamics, Liouville only fixes `J_q J_p=1`, null propagation fixes a ratio rather than the product, and the Newtonian limit fixes the lapse but not the radial routing.",
        "",
        "The direct `Lambda_R C_R` route still works algebraically, but without a parent `L_core/H_core` owner it is closure, not derivation. Therefore the local zero branch is now explicitly `local_closure_baseline`: useful as an internal control, never as a derived local-GR/Newton claim.",
        "",
        "The finite branch remains the claimable fallback only after source-backed residual inputs exist: `C_R(r)`, `q_R/Pi_R`, `Z_R_infty`, `N_sphere`, `M_R^2`, source balance, boundary charge, same-frame mass, tails and arena kernels. Until then no local-GR, Newton, PPN, R10, clock or orbital pass is claim-valid.",
        "",
        "No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Parent Radial-Cell Owner Attempt",
        md_table(owner_rows, ["row_id", "candidate", "formula_or_test", "status", "useful_part", "blocker", "derives_C_R_zero", "claim_allowed"]),
        "## Local Closure Baseline",
        md_table(closure_rows, ["row_id", "branch", "assumption_or_rule", "closure_only", "derived_local_GR", "pass_for_claim", "allowed_use", "hard_refusal", "claim_allowed"]),
        "## Finite Residual Acquisition Gates",
        md_table(finite_rows, ["row_id", "quantity", "role", "required_input", "current_status", "observable_arenas", "ready_for_scoring", "valid_for_claim", "claim_allowed"]),
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
    owner_rows = radial_owner_attempt_rows()
    closure_rows = closure_baseline_rows()
    finite_rows = finite_acquisition_gate_rows()
    runner = runner_rows(owner_rows, closure_rows, finite_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2058_SOURCE_REGISTER.csv",
        "owner": OUT / "P8_Y5_PARENT_QLOC_2058_RADIAL_CELL_OWNER_ATTEMPT.csv",
        "closure": OUT / "P8_Y5_PARENT_QLOC_2058_LOCAL_CLOSURE_BASELINE.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2058_FINITE_ACQUISITION_GATES.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2058_BRANCH_RUNNER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2058_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2058_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2058_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2058_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2058_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["owner"], owner_rows)
    write_csv(paths["closure"], closure_rows)
    write_csv(paths["finite"], finite_rows)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(owner_rows, closure_rows, finite_rows, runner, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, owner_rows, closure_rows, finite_rows, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, owner_rows, closure_rows, finite_rows, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, owner_rows, closure_rows, finite_rows, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
