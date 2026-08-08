import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3766"
BRANCH = "MTS_R2FR_Y5_PROVE_QOBS_KERNEL_PRESYMPLECTIC_NULL_OR_FIRST_FRAME_RESIDUAL_BOUND_3766"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3766-Y5-R2FR-prove-qobs-kernel-presymplectic-null-or-first-frame-residual-bound.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3766_SOURCE_REGISTER.csv",
    "kernel_theorem": RESIDUALS / "P8_Y5_R2FR_3766_KERNEL_NULL_THEOREM.csv",
    "proof_attempt": RESIDUALS / "P8_Y5_R2FR_3766_QOBS_KERNEL_PROOF_ATTEMPT.csv",
    "leakage_norms": RESIDUALS / "P8_Y5_R2FR_3766_VERTICAL_LEAKAGE_NORMS.csv",
    "frame_bound": RESIDUALS / "P8_Y5_R2FR_3766_FIRST_FRAME_RESIDUAL_BOUND.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3766_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3766_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3766_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3766_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3766_VALIDATION.csv",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str, valid_for_claim: bool = False) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": valid_for_claim,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3766_0_3765_doc": PCW / "3765-Y5-R2FR-construct-qobs-parent-quotient-or-frame-residual-map.md",
        "SRC3766_1_3765_candidate": RESIDUALS / "P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv",
        "SRC3766_2_3765_certificates": RESIDUALS / "P8_Y5_R2FR_3765_QOBS_CERTIFICATE_TESTS.csv",
        "SRC3766_3_3765_residual_map": RESIDUALS / "P8_Y5_R2FR_3765_SECTOR_READOUT_RESIDUAL_MAP.csv",
        "SRC3766_4_3765_verdict": RESIDUALS / "P8_Y5_R2FR_3765_PARENT_QOBS_VERDICT.csv",
        "SRC3766_5_3633_strict_quotient": RESIDUALS / "P8_Y5_R2FR_3633_STRICT_QUOTIENT_THEOREM.csv",
        "SRC3766_6_3646_matter_descent": RESIDUALS / "P8_Y5_R2FR_3646_MATTER_DESCENT_THEOREM_ATTEMPT.csv",
        "SRC3766_7_3699_projection_rows": RESIDUALS / "P8_Y5_R2FR_3699_QUOTIENT_PROJECTION_ROWS.csv",
        "SRC3766_8_3138_qobs_certificates": RESIDUALS / "P8_Y5_R2FR_3138_REP_QOBS_CERTIFICATE_MATRIX.csv",
        "SRC3766_9_3763_action_ansatz": RESIDUALS / "P8_Y5_R2FR_3763_LOCAL_PARENT_ACTION_ANSATZ.csv",
        "SRC3766_10_3764_quotient_theorem": RESIDUALS / "P8_Y5_R2FR_3764_PARENT_QUOTIENT_DESCENT_THEOREM.csv",
        "SRC3766_11_3764_source_theorem": RESIDUALS / "P8_Y5_R2FR_3764_SAME_TOTAL_SOURCE_VARIATION_THEOREM.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3766 kernel-null proof and residual-bound input",
        }
        for source_id, path in source_paths().items()
    ]


def kernel_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "KNT3766_0_vertical_split",
            "Choose a local section sigma of q_obs and vertical coordinates zeta^A so Phi=sigma(Q)+zeta^A E_A with Q=q_obs(Phi).",
            "Dq_obs[E_A]=0 by construction; E_A span ker(Dq_obs).",
            "This is the mathematical fibre split needed to talk about kernel directions without pretending they are physical fields.",
            "EXACT_LOCAL_FIBRE_IDENTITY",
        ),
        (
            "KNT3766_1_pullback_action",
            "If L_parent(Phi)=q_obs^* L_red(Q)+dB(Q,zeta) and S_src(Phi,psi,A,theta)=Sbar_src(q_obs(Phi),psi,A,theta), then vertical bulk variations vanish.",
            "delta_EA L_parent=d(delta_EA B), delta_EA S_src=0.",
            "This is the non-smuggled version of 'the omitted variables are gauge': it is a statement about the action, not about taste.",
            "EXACT_CONDITIONAL_ACTION_THEOREM",
        ),
        (
            "KNT3766_2_presymplectic_contraction",
            "For L_parent=q_obs^*L_red+dB, the covariant symplectic current obeys i_EA Omega_parent=0 in the bulk and i_EA Theta_parent=dB_EA up to the same boundary term.",
            "Theta_parent=q_obs^*Theta_red+delta B, so Omega_parent=q_obs^*Omega_red; contracting with E_A gives zero because Dq_obs[E_A]=0.",
            "This is the desired kernel-null proof once the parent action really has pullback form.",
            "EXACT_CONDITIONAL_PRESYMPLECTIC_THEOREM",
        ),
        (
            "KNT3766_3_boundary_silence",
            "For compact local variations or quotient-owned boundary/support data, the surface integral of B_EA vanishes.",
            "int_boundary B_EA=0 implies no side flux, no boundary owner current, and no radial leakage from the vertical sector.",
            "This is why the proof must include support/boundary ownership; otherwise the vertical direction can be bulk-null but still physically visible at the edge.",
            "EXACT_CONDITIONAL_BOUNDARY_THEOREM",
        ),
        (
            "KNT3766_4_matter_invisibility",
            "If S_src=Sbar_src(q_obs(Phi),psi,A,theta) and Lie_EA theta=0, then Lie_EA S_src=0 for matter, EM, binding, apparatus, and interaction terms.",
            "Lie_EA S_src=(delta Sbar/dQ)Dq_obs[E_A]+sum_i(partial Sbar/partial theta_i)Lie_EA theta_i=0.",
            "This kills the source-coupling channel only if constants, masses, material labels, and clock ratios are quotient-owned or superselected.",
            "EXACT_CONDITIONAL_SOURCE_THEOREM",
        ),
        (
            "KNT3766_5_readout_zero",
            "If every sector readout r_s factors as F_s o q_obs, then Lie_EA r_s=0 and Delta q_s=0 for matter, EM, light, clocks, orbital/source, boundary/current, and range sectors.",
            "Lie_EA r_s=DF_s[Dq_obs[E_A]]=0.",
            "This turns the 3765 residual vector into zeros only when sector descent is proved, not assumed.",
            "EXACT_CONDITIONAL_READOUT_THEOREM",
        ),
        (
            "KNT3766_6_kernel_null_result",
            "Under KNT3766_1 through KNT3766_5, ker(Dq_obs) is presymplectic-null, matter-invisible, boundary-silent, and readout-silent.",
            "i_EA Omega_parent=0; Lie_EA S_src=0; Lie_EA r_s=0; int_boundary B_EA=0.",
            "This is the exact local-GR kernel certificate that would make the 3764 single-frame/same-source theorem live.",
            "EXACT_CONDITIONAL_KERNEL_CERTIFICATE",
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "statement": statement,
            "identity": identity,
            "meaning": meaning,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for theorem_id, statement, identity, meaning, status in rows
    ]


def proof_attempt_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "KPA3766_0_candidate_qobs",
            "q_obs candidate exists",
            "3765 writes q_obs_candidate and Q_obs tuple",
            True,
            "candidate map available for proof attempt",
        ),
        (
            "KPA3766_1_vertical_split",
            "local fibre split Phi=sigma(Q)+zeta^A E_A with Dq_obs[E_A]=0",
            "can be introduced locally as differential geometry of the candidate map",
            True,
            "mathematical split exists locally where q_obs is regular",
        ),
        (
            "KPA3766_2_parent_pullback_action",
            "L_parent=q_obs^*L_red+dB plus no local vertical leakage",
            "3763 action ansatz and 3633 theorem support the target form, but no parent-owned pullback proof is present",
            False,
            "proof cannot be live without action decomposition",
        ),
        (
            "KPA3766_3_presymplectic_null",
            "i_EA Omega_parent=0 and i_EA Theta_parent=dB_EA",
            "derived conditionally in KNT3766_2; current corpus still lacks Omega_parent calculation",
            False,
            "kernel-null claim remains blocked",
        ),
        (
            "KPA3766_4_boundary_silence",
            "int_boundary B_EA=0 for compact local/source support",
            "3756-3758 keep side flux and exchange as live gates",
            False,
            "boundary/current residual remains live",
        ),
        (
            "KPA3766_5_source_descent",
            "S_src=Sbar_src(q_obs,psi,A,theta) and Lie_EA theta=0",
            "3764/3646 provide the theorem but not parent-signed constants/material-marker descent",
            False,
            "matter and EM source residuals remain live",
        ),
        (
            "KPA3766_6_sector_readout_descent",
            "all r_s=F_s o q_obs",
            "3765 sector residual map exists; factorization is not signed for all sectors",
            False,
            "Delta q_s vector remains live",
        ),
        (
            "KPA3766_7_kernel_certificate_verdict",
            "ker(Dq_obs) proof live for MTS local-GR branch",
            "requires KPA3766_2 through KPA3766_6",
            False,
            "do not claim local GR; use residual-bound theorem",
        ),
    ]
    return [
        {
            **base(timestamp),
            "attempt_id": attempt_id,
            "required_clause": required_clause,
            "evidence": evidence,
            "passes_clause": passes_clause,
            "consequence": consequence,
            "claim_allowed": False,
        }
        for attempt_id, required_clause, evidence, passes_clause, consequence in rows
    ]


def leakage_norm_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "VLN3766_0_action_leak",
            "epsilon_L",
            "sup_A ||delta_EA L_parent - dB_EA||_U / ||L_red||_U",
            "bulk parent action dependence on vertical variables",
            "zero iff parent action is a q_obs pullback up to boundary",
            "MISSING_PARENT_LAGRANGIAN",
        ),
        (
            "VLN3766_1_symplectic_leak",
            "epsilon_Omega",
            "sup_A ||i_EA Omega_parent||_U / ||Omega_red||_U",
            "physical phase-space charge in the q_obs kernel",
            "zero iff the vertical direction is presymplectic-null",
            "MISSING_PARENT_SYMPLECTIC_FORM",
        ),
        (
            "VLN3766_2_boundary_leak",
            "epsilon_boundary",
            "sup_A |int_boundary B_EA| / E_U",
            "compact-support, side-flux, or boundary-owner visibility",
            "zero iff the vertical boundary term is silent on the local system",
            "MISSING_BOUNDARY_CERTIFICATE",
        ),
        (
            "VLN3766_3_source_leak",
            "epsilon_src",
            "sup_A |Lie_EA S_src| / |S_src|",
            "matter, EM, binding, apparatus, or interaction dependence on vertical variables",
            "zero iff same-source matter action descends through q_obs",
            "MISSING_SOURCE_ACTION_DESCENT",
        ),
        (
            "VLN3766_4_constant_marker_leak",
            "epsilon_theta",
            "sup_A,i |Lie_EA theta_i| / |theta_i|",
            "mass, charge, clock-ratio, material-marker, or calibration dependence outside q_obs",
            "zero iff constants/material markers are quotient-owned or superselected",
            "MISSING_CONSTANT_MARKER_PROOF",
        ),
        (
            "VLN3766_5_readout_leak",
            "epsilon_readout_s",
            "sup_A ||Lie_EA r_s|| / ||r_s|| for each sector s",
            "sector readout mismatch Delta q_s",
            "zero iff r_s=F_s o q_obs",
            "MISSING_SECTOR_FACTORIZATION",
        ),
        (
            "VLN3766_6_range_hair_leak",
            "epsilon_range",
            "sup_A (|alpha_A(lambda)| + |hair_A(r)|)",
            "finite-range or exterior radial hair carried by vertical variables",
            "zero iff no unscreened mediator/hair survives the local q_obs quotient",
            "MISSING_NO_RANGE_NO_HAIR_PROOF",
        ),
    ]
    return [
        {
            **base(timestamp),
            "norm_id": norm_id,
            "symbol": symbol,
            "definition": definition,
            "physical_meaning": physical_meaning,
            "zero_condition": zero_condition,
            "numeric_value": missing,
            "units": "dimensionless_or_normalized_sector_units",
            "claim_allowed": False,
        }
        for norm_id, symbol, definition, physical_meaning, zero_condition, missing in rows
    ]


def frame_bound_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "FRB3766_0_sector_path_bound",
            "Delta q_s",
            "|Delta q_s| <= integral_0^1 ||D r_s[E_A]|| |d zeta^A/dlambda| dlambda",
            "fundamental theorem of calculus along the vertical fibre path from q_obs representative to sector readout representative",
            "requires sector sensitivity ||D r_s[E_A]|| and vertical amplitude |zeta^A|",
            "not numeric yet",
        ),
        (
            "FRB3766_1_lipschitz_bound",
            "Delta q_s",
            "|Delta q_s| <= sum_A L_{sA} |zeta^A|",
            "if each sector readout has a local vertical Lipschitz coefficient L_{sA}",
            "requires L_{sA} from parent readout map or empirical residual model",
            "not numeric yet",
        ),
        (
            "FRB3766_2_frame_summary_bound",
            "delta_frame_source",
            "delta_frame_source <= w_m|Delta q_matter|+w_EM|Delta q_EM|+w_l|Delta q_light|+w_c|Delta q_clock|+w_o|Delta q_orbit_source|",
            "single-frame failure is a weighted sum of sector quotient mismatches",
            "requires sector weights from target observable or conservative w_s=1 discipline",
            "ready as symbolic residual budget",
        ),
        (
            "FRB3766_3_kernel_leak_bound",
            "delta_frame_source",
            "delta_frame_source <= C_Omega epsilon_Omega + C_src epsilon_src + C_theta epsilon_theta + C_boundary epsilon_boundary + C_readout max_s epsilon_readout_s",
            "if sector sensitivity is controlled by vertical symplectic/source/boundary/readout leakage",
            "requires constants C_i from parent linearization or empirical calibration",
            "not numeric yet",
        ),
        (
            "FRB3766_4_ppn_gamma_bound",
            "abs(gamma-1)_frame",
            "abs(gamma-1)_frame <= C_gamma_frame delta_frame_source + C_gamma_range epsilon_range + C_gamma_EH delta_EH",
            "feeds the PPN light/source-frame branch",
            "requires C_gamma coefficients and PPN observable mapping",
            "not numeric yet",
        ),
        (
            "FRB3766_5_wep_bound",
            "eta_source_AB",
            "eta_source_AB <= C_AB^m |Delta q_matter| + C_AB^theta epsilon_theta + C_AB^EM |Delta q_EM| + C_AB^boundary epsilon_boundary",
            "feeds composition/WEP and source universality branch",
            "requires composition sensitivities and material constants",
            "not numeric yet",
        ),
        (
            "FRB3766_6_newton_gm_bound",
            "delta_mu_obs",
            "|delta mu_obs| <= |Delta q_orbit_source| + epsilon_boundary + epsilon_src",
            "feeds Newtonian GM, Gdot, radial-hair, and orbital tests",
            "requires source monopole map and boundary/current denominator coefficients",
            "not numeric yet",
        ),
    ]
    return [
        {
            **base(timestamp),
            "bound_id": bound_id,
            "target": target,
            "bound_formula": formula,
            "derivation": derivation,
            "inputs_required": inputs_required,
            "numeric_status": numeric_status,
            "claim_allowed": False,
        }
        for bound_id, target, formula, derivation, inputs_required, numeric_status in rows
    ]


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    sources_exist = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    theorem_emitted = any(row["theorem_id"] == "KNT3766_6_kernel_null_result" for row in grouped["kernel_theorem"])
    proof_live = all(row["passes_clause"] is True for row in grouped["proof_attempt"] if row["attempt_id"] != "KPA3766_7_kernel_certificate_verdict")
    bounds_emitted = len(grouped["frame_bound"]) >= 7
    rows = [
        ("CG3766_0_sources", "all 3766 source paths exist", sources_exist, "path hygiene"),
        ("CG3766_1_kernel_theorem_emitted", "kernel-null theorem emitted", theorem_emitted, "exact conditional proof exists"),
        ("CG3766_2_proof_live_for_MTS", "kernel-null proof live for current MTS parent branch", proof_live, "blocked by unsigned parent action/symplectic/source/boundary clauses"),
        ("CG3766_3_leakage_norms_emitted", "vertical leakage norms emitted", len(grouped["leakage_norms"]) >= 7, "first measurable/boundable residual interface exists"),
        ("CG3766_4_frame_bound_emitted", "first frame residual bound emitted", bounds_emitted, "failure branch is now a bound formula rather than a vague gap"),
        ("CG3766_5_single_frame_claim", "single observed frame claim allowed", False, "blocked until CG3766_2 passes or residual bounds are filled below tests"),
        ("CG3766_6_local_gr_claim", "local GR/Newton/PPN claim allowed", False, "blocked until kernel proof plus local EH/no-range/global-kappa gates close"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3766_0",
            "The exact mathematical route to a live q_obs kernel proof is now written as a covariant phase-space theorem.",
            "do not relitigate the target; attack the missing parent action pullback and Omega_parent calculation",
        ),
        (
            "DEC3766_1",
            "The current MTS corpus still does not sign the proof because the parent action/symplectic/source/boundary clauses are not explicit enough.",
            "keep local GR unclaimed",
        ),
        (
            "DEC3766_2",
            "If the proof remains unsigned, the first fallback is no longer a vague closure label: delta_frame_source has a bound in terms of vertical leakage norms.",
            "next fill or derive epsilon_L, epsilon_Omega, epsilon_src, epsilon_theta, epsilon_boundary, and epsilon_readout_s",
        ),
        (
            "DEC3766_3",
            "The highest-value next derivation is the parent action pullback decomposition L_parent=q_obs^*L_red+dB+L_leak.",
            "try to force all non-q_obs terms into L_leak and either prove L_leak=0 or make it the first numeric residual object",
        ),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "action": action,
            "claim_allowed": False,
        }
        for decision_id, decision, action in rows
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3766_0",
            "target_doc": "3767-Y5-R2FR-parent-action-pullback-decomposition-or-Lleak-first-bound.md",
            "target_script": "scripts/Y5_R2FR_3767_parent_action_pullback_decomposition_or_Lleak_first_bound.py",
            "objective": "decompose the local parent action as L_parent=q_obs^*L_red+dB+L_leak, then either prove L_leak=0 for the q_obs kernel or promote L_leak into the first source-ready residual coefficient set",
            "reason": "3766 shows kernel-null follows exactly from action pullback; the next work must attack L_parent itself, not another external consequence",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "KERNEL_NULL_THEOREM_DERIVED_CONDITIONALLY_FRAME_RESIDUAL_BOUND_EMITTED_NOT_PARENT_SIGNED",
            "summary": "3766 derives the exact covariant phase-space condition under which ker(Dq_obs) is presymplectic-null, matter-invisible, boundary-silent, and readout-silent. The current MTS branch does not yet sign the parent action pullback/symplectic/source/boundary clauses, so local GR is not claimed. The fallback is now a concrete delta_frame_source bound in terms of vertical leakage norms.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3766 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3766 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("kernel_result", "kernel-null result theorem emitted", any(row["theorem_id"] == "KNT3766_6_kernel_null_result" for row in grouped["kernel_theorem"])),
        ("proof_attempt_closed", "live MTS proof remains blocked rather than claimed", any(row["attempt_id"] == "KPA3766_7_kernel_certificate_verdict" and row["passes_clause"] is False for row in grouped["proof_attempt"])),
        ("leakage_norms", "at least seven vertical leakage norms emitted", len(grouped["leakage_norms"]) >= 7),
        ("frame_bound", "first frame residual bound emitted", any(row["bound_id"] == "FRB3766_2_frame_summary_bound" for row in grouped["frame_bound"])),
        ("numeric_status_nonclaim", "frame-bound rows remain nonclaim without coefficients", all(row["claim_allowed"] is False for row in grouped["frame_bound"])),
        ("claim_gates_closed", "single-frame/local-GR claims remain closed", all(row["passed"] is False for row in grouped["claim_gates"] if row["gate_id"] in {"CG3766_2_proof_live_for_MTS", "CG3766_5_single_frame_claim", "CG3766_6_local_gr_claim"})),
        ("next_target", "3767 parent action pullback target emitted", grouped["next_target"][0]["target_doc"] == "3767-Y5-R2FR-parent-action-pullback-decomposition-or-Lleak-first-bound.md"),
        ("no_formalization_leak", "no 3766 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3766*"))),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "" if result else "check failed",
        }
        for validation_id, description, result in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3766 - Prove q_obs Kernel Presymplectic Null Or First Frame Residual Bound",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "The clean route is now exact: if the parent local action is a pullback through `q_obs` up to a boundary term, and the source/readout sectors also descend through `q_obs`, then every vertical direction in `ker(Dq_obs)` is gauge/null/matter-invisible. That would make the 3764 single-frame/same-source theorem live.",
        "",
        "The current corpus does not yet sign the parent action pullback or the symplectic calculation, so this is not a local-GR claim. The fallback is stronger than before: the failure is now bounded by named vertical leakage norms rather than left as an undefined coupling gap.",
        "",
        "## Kernel-Null Theorem",
    ]
    for row in grouped["kernel_theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} Identity: `{row['identity']}`")
    lines.extend(["", "## Proof Attempt Against Current Branch"])
    for row in grouped["proof_attempt"]:
        lines.append(f"- `{row['attempt_id']}` pass=`{row['passes_clause']}`: {row['required_clause']}. Evidence: {row['evidence']}.")
    lines.extend(["", "## Vertical Leakage Norms"])
    for row in grouped["leakage_norms"]:
        lines.append(f"- `{row['norm_id']}` `{row['symbol']}`: {row['definition']} Meaning: {row['physical_meaning']}.")
    lines.extend(["", "## First Frame Residual Bound"])
    for row in grouped["frame_bound"]:
        lines.append(f"- `{row['bound_id']}` `{row['target']}`: {row['bound_formula']} Inputs: {row['inputs_required']}.")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} - {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decision_rows"]:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} Action: {row['action']}.")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(timestamp),
        "kernel_theorem": kernel_theorem_rows(timestamp),
        "proof_attempt": proof_attempt_rows(timestamp),
        "leakage_norms": leakage_norm_rows(timestamp),
        "frame_bound": frame_bound_rows(timestamp),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["kernel_theorem"], grouped["kernel_theorem"])
    write_csv(OUTPUTS["proof_attempt"], grouped["proof_attempt"])
    write_csv(OUTPUTS["leakage_norms"], grouped["leakage_norms"])
    write_csv(OUTPUTS["frame_bound"], grouped["frame_bound"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decision_rows"], grouped["decision_rows"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3766 validation failed: {failures}")
    print("wrote 3766 checkpoint: kernel-null theorem derived conditionally and frame residual bound emitted")


if __name__ == "__main__":
    main()
