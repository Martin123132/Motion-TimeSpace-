import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3767"
BRANCH = "MTS_R2FR_Y5_PARENT_ACTION_PULLBACK_DECOMPOSITION_OR_LLEAK_FIRST_BOUND_3767"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3767-Y5-R2FR-parent-action-pullback-decomposition-or-Lleak-first-bound.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3767_SOURCE_REGISTER.csv",
    "decomposition": RESIDUALS / "P8_Y5_R2FR_3767_PARENT_ACTION_PULLBACK_DECOMPOSITION.csv",
    "operator_basis": RESIDUALS / "P8_Y5_R2FR_3767_LLEAK_OPERATOR_BASIS.csv",
    "vertical_audit": RESIDUALS / "P8_Y5_R2FR_3767_VERTICAL_VARIATION_AUDIT.csv",
    "bound_interface": RESIDUALS / "P8_Y5_R2FR_3767_LLEAK_BOUND_INTERFACE.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3767_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3767_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3767_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3767_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3767_VALIDATION.csv",
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
        "SRC3767_0_3766_doc": PCW / "3766-Y5-R2FR-prove-qobs-kernel-presymplectic-null-or-first-frame-residual-bound.md",
        "SRC3767_1_3766_kernel_theorem": RESIDUALS / "P8_Y5_R2FR_3766_KERNEL_NULL_THEOREM.csv",
        "SRC3767_2_3766_proof_attempt": RESIDUALS / "P8_Y5_R2FR_3766_QOBS_KERNEL_PROOF_ATTEMPT.csv",
        "SRC3767_3_3766_leakage_norms": RESIDUALS / "P8_Y5_R2FR_3766_VERTICAL_LEAKAGE_NORMS.csv",
        "SRC3767_4_3766_frame_bound": RESIDUALS / "P8_Y5_R2FR_3766_FIRST_FRAME_RESIDUAL_BOUND.csv",
        "SRC3767_5_3763_action_ansatz": RESIDUALS / "P8_Y5_R2FR_3763_LOCAL_PARENT_ACTION_ANSATZ.csv",
        "SRC3767_6_3763_signature_set": RESIDUALS / "P8_Y5_R2FR_3763_MINIMAL_PARENT_SIGNATURE_SET.csv",
        "SRC3767_7_3765_qobs_candidate": RESIDUALS / "P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv",
        "SRC3767_8_3633_strict_quotient": RESIDUALS / "P8_Y5_R2FR_3633_STRICT_QUOTIENT_THEOREM.csv",
        "SRC3767_9_3646_matter_descent": RESIDUALS / "P8_Y5_R2FR_3646_MATTER_DESCENT_THEOREM_ATTEMPT.csv",
        "SRC3767_10_3764_source_theorem": RESIDUALS / "P8_Y5_R2FR_3764_SAME_TOTAL_SOURCE_VARIATION_THEOREM.csv",
        "SRC3767_11_3765_sector_residual": RESIDUALS / "P8_Y5_R2FR_3765_SECTOR_READOUT_RESIDUAL_MAP.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3767 parent action pullback and L_leak decomposition input",
        }
        for source_id, path in source_paths().items()
    ]


def decomposition_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "PAD3767_0_fibre_path",
            "Let Q=q_obs(Phi), choose a local section sigma(Q), and write a vertical path Phi_lambda=sigma(Q)+lambda zeta^A E_A with E_A in ker(Dq_obs).",
            "Dq_obs[d Phi_lambda/dlambda]=0 along the path.",
            "Sets up a genuine decomposition along the unobserved fibre rather than assuming the fibre is harmless.",
            "EXACT_LOCAL_FIBRE_SETUP",
        ),
        (
            "PAD3767_1_homotopy_identity",
            "L_parent(Phi)-L_parent(sigma(Q)) = integral_0^1 zeta^A partial_A L_parent(Phi_lambda) dlambda.",
            "This is the fundamental theorem of calculus on the vertical fibre.",
            "Every non-q_obs dependence must appear in this integral; there is nowhere left to hide it.",
            "EXACT_ACTION_IDENTITY",
        ),
        (
            "PAD3767_2_total_derivative_split",
            "Split partial_A L_parent(Phi_lambda)=d b_A(Phi_lambda)+r_A(Phi_lambda).",
            "b_A is the boundary/improvement part; r_A is the non-exact bulk vertical residue.",
            "This separates harmless boundary variation from a physical leak that can source local tests.",
            "DEFINITION_WITH_UNIQUE_RESIDUAL_AFTER_BOUNDARY_CHOICE",
        ),
        (
            "PAD3767_3_pullback_decomposition",
            "Define L_red(Q):=L_parent(sigma(Q)), B:=integral_0^1 zeta^A b_A(Phi_lambda)dlambda, and L_leak:=integral_0^1 zeta^A r_A(Phi_lambda)dlambda.",
            "Then L_parent=q_obs^*L_red+dB+L_leak.",
            "This is the exact action-level object demanded by 3766.",
            "EXACT_DECOMPOSITION",
        ),
        (
            "PAD3767_4_zero_condition",
            "L_leak=0 iff every vertical derivative of L_parent is a total derivative with silent local boundary/support.",
            "r_A=0 and int_boundary B=0 for all E_A in ker(Dq_obs).",
            "This is the parent-action version of the q_obs kernel-null certificate.",
            "EXACT_ZERO_CONDITION",
        ),
        (
            "PAD3767_5_kernel_consequence",
            "If L_leak=0, source/readout descent holds, and the boundary is silent, 3766 gives i_EA Omega_parent=0, Lie_EA S_src=0, and Lie_EA r_s=0.",
            "L_parent=q_obs^*L_red+dB is the missing premise of KNT3766_2.",
            "This would close the single-frame/same-source kernel part of the local-GR route.",
            "EXACT_CONDITIONAL_CONSEQUENCE",
        ),
        (
            "PAD3767_6_failure_bound",
            "If L_leak != 0, define epsilon_L:=||L_leak||_U/||L_red||_U and propagate it into epsilon_Omega, epsilon_src, and delta_frame_source bounds.",
            "delta_frame_source <= C_L epsilon_L + C_boundary epsilon_boundary + C_readout max_s epsilon_readout_s.",
            "Failure becomes a bounded residual coefficient rather than a closure assumption.",
            "RESIDUAL_BOUND_INTERFACE",
        ),
    ]
    return [
        {
            **base(timestamp),
            "decomposition_id": decomposition_id,
            "statement": statement,
            "identity": identity,
            "meaning": meaning,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for decomposition_id, statement, identity, meaning, status in rows
    ]


def operator_basis_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "LOB3767_0_topological_bulk",
            "L_leak_top",
            "integral_0^1 zeta^A r_A^top(Phi_lambda) dlambda",
            "MTS/topological/motion-time-space term has non-exact vertical bulk variation",
            "r_A^top=0 or total derivative with silent boundary",
            "Gdot, radial hair, PPN beta, source conservation",
        ),
        (
            "LOB3767_1_kappa_EH_coefficient",
            "L_leak_kappa",
            "-(partial_A ln kappa_*) zeta^A L_EH plus higher vertical orders",
            "local EH coefficient varies along a vertical/representative direction",
            "Lie_EA kappa_*=0 or kappa_* quotient-owned/superselected",
            "Gdot, Newtonian GM calibration, PPN gamma/beta",
        ),
        (
            "LOB3767_2_shadow_metric_frame",
            "L_leak_shadow_g",
            "(delta L_EH/dg_eff_ab) Delta g_shadow_ab + source-frame analogues",
            "a Weyl/disformal/representative metric component survives outside q_obs",
            "Delta g_shadow=0 modulo diffeomorphism/local Lorentz/q_obs gauge",
            "single observed frame, light bending, clocks, WEP",
        ),
        (
            "LOB3767_3_source_action",
            "L_leak_src",
            "zeta^A J_A^src with J_A^src:=delta S_src/dzeta^A",
            "matter, EM, binding, apparatus, or interaction action sees vertical variables",
            "S_src=Sbar_src(q_obs,psi,A,theta)",
            "WEP, EM stress, source universality, PPN source projection",
        ),
        (
            "LOB3767_4_constants_markers",
            "L_leak_theta",
            "zeta^A sum_i (partial L_src/partial theta_i) partial_A theta_i",
            "masses, charges, clock ratios, material labels, binding fractions, or calibrations carry vertical dependence",
            "Lie_EA theta_i=0 or theta_i quotient-owned/superselected",
            "WEP, clocks, alpha_fs drift, calibrated source coupling",
        ),
        (
            "LOB3767_5_auxiliary_range",
            "L_leak_aux",
            "kinetic/mass/source terms for chi that are not algebraically eliminated, heavy/decoupled, or quotient-silent",
            "extra field creates finite-range mediator or exterior hair",
            "chi vertical/gauge, algebraic, heavy/decoupled, or explicitly bounded",
            "R10 fifth-force, radial hair, PPN, orbital systems",
        ),
        (
            "LOB3767_6_boundary_support",
            "L_leak_boundary",
            "dB with int_boundary B != 0 or source-support variation not quotient-owned",
            "bulk-null vertical direction still visible through side flux, support motion, or denominator/current boundary",
            "compact local variations and source worldtube/support descend through q_obs",
            "Gdot, radial hair, source conservation, H_tau/H_ref",
        ),
        (
            "LOB3767_7_readout_postprocessing",
            "L_leak_readout",
            "post-action readout weights W_s(Phi) not expressible as F_s(q_obs)",
            "observable map adds sector-dependent physics after the variational action",
            "all readouts factor as r_s=F_s o q_obs",
            "Delta q_s vector, preferred frame, local calibration",
        ),
    ]
    return [
        {
            **base(timestamp),
            "operator_id": operator_id,
            "symbol": symbol,
            "operator_form": operator_form,
            "leak_channel": leak_channel,
            "zero_condition": zero_condition,
            "feeds_observables": feeds_observables,
            "coefficient_status": "MISSING_PARENT_COEFFICIENT",
            "claim_allowed": False,
        }
        for operator_id, symbol, operator_form, leak_channel, zero_condition, feeds_observables in rows
    ]


def vertical_audit_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "VAA3767_0_EH_pullback",
            "Einstein-Hilbert local operator from 3763 ansatz",
            "pullback if g_eff/e_obs and kappa_* are q_obs-owned",
            "metric part conditional pass; kappa ownership unsigned",
            False,
            "L_leak_kappa and L_leak_shadow_g remain live",
        ),
        (
            "VAA3767_1_source_action",
            "same-source action term from 3763/3764",
            "pullback if S_src=Sbar_src(q_obs,psi,A,theta) and Lie_EA theta=0",
            "chain-rule theorem exists, parent constants/material-marker descent unsigned",
            False,
            "L_leak_src and L_leak_theta remain live",
        ),
        (
            "VAA3767_2_auxiliary_silence",
            "S_aux[chi;g_eff] branch",
            "pullback if chi is gauge/algebraic/heavy/decoupled or bounded",
            "3763 states signature but does not derive from parent dynamics",
            False,
            "L_leak_aux remains live",
        ),
        (
            "VAA3767_3_topological_sector",
            "S_top[MTS]",
            "harmless if vertical variation is exact/topological with silent local boundary",
            "no explicit vertical Euler derivative calculation found",
            False,
            "L_leak_top remains live",
        ),
        (
            "VAA3767_4_boundary_support",
            "source support and boundary class",
            "harmless if source worldtube/support is quotient-owned and boundary flux vanishes",
            "3766/3756 keep boundary and exchange channels live",
            False,
            "L_leak_boundary remains live",
        ),
        (
            "VAA3767_5_readout_layer",
            "sector readouts after variation",
            "harmless if r_s=F_s o q_obs for all sectors",
            "3765 emits residual vector rather than full factorization proof",
            False,
            "L_leak_readout and Delta q_s remain live",
        ),
    ]
    return [
        {
            **base(timestamp),
            "audit_id": audit_id,
            "action_piece": action_piece,
            "pullback_condition": pullback_condition,
            "current_evidence": current_evidence,
            "passes_current_branch": passes_current_branch,
            "live_residual": live_residual,
            "claim_allowed": False,
        }
        for audit_id, action_piece, pullback_condition, current_evidence, passes_current_branch, live_residual in rows
    ]


def bound_interface_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "LBI3767_0_total_action_leak",
            "epsilon_L",
            "||L_leak||_U/||L_red||_U",
            "epsilon_L <= epsilon_top + epsilon_kappa + epsilon_shadow_g + epsilon_src + epsilon_theta + epsilon_aux + epsilon_boundary + epsilon_readout",
            "triangle inequality on the L_leak operator basis",
            "requires each operator coefficient or proof of zero",
        ),
        (
            "LBI3767_1_kappa_EH_leak",
            "epsilon_kappa",
            "sup_A |Lie_EA ln kappa_*|",
            "contributes |delta G/G|, Newtonian source calibration drift, and EH coefficient variation",
            "vertical derivative of 1/kappa_* times L_EH",
            "prove kappa_* q_obs-owned or bound from Gdot/PPN/orbital rows",
        ),
        (
            "LBI3767_2_shadow_frame_leak",
            "epsilon_shadow_g",
            "sup_A ||Lie_EA g_eff||_g modulo diffeo/Lorentz/q_obs gauge",
            "contributes frame split, gamma, clocks, and light/matter mismatch",
            "metric variation term in L_EH and source variation",
            "prove single frame descent or bound from PPN/clock/preferred-frame tests",
        ),
        (
            "LBI3767_3_source_leak",
            "epsilon_src",
            "sup_A |J_A^src zeta^A|/|L_src|",
            "contributes WEP/source universality and EM stress split",
            "vertical source current norm",
            "prove source action descent or bound with composition/EM/apparatus sensitivities",
        ),
        (
            "LBI3767_4_constants_markers",
            "epsilon_theta",
            "sup_A,i |Lie_EA theta_i|/|theta_i|",
            "contributes mass, charge, clock, alpha, and material dependence",
            "constant/material marker derivative term",
            "prove theta superselection or create coefficient rows b_mass,b_alpha,b_clock,b_material",
        ),
        (
            "LBI3767_5_aux_range",
            "epsilon_aux",
            "normalized unscreened chi source/range amplitude",
            "contributes R10 alpha(lambda), radial hair, and PPN extra-channel terms",
            "auxiliary operator projection",
            "prove chi heavy/algebraic/gauge or use R10/PPN/radial bounds",
        ),
        (
            "LBI3767_6_boundary_support",
            "epsilon_boundary",
            "|int_boundary B|/E_U plus support-owner variation",
            "contributes side flux, source conservation, radial hair, H_tau/H_ref",
            "boundary term in the action homotopy",
            "prove compact boundary silence or bound flux/current terms",
        ),
        (
            "LBI3767_7_frame_propagation",
            "delta_frame_source",
            "single observed-frame residual",
            "delta_frame_source <= C_L epsilon_L + C_readout max_s epsilon_readout_s + C_boundary epsilon_boundary",
            "combines 3766 kernel-leak bound with action-leak decomposition",
            "requires C_L,C_readout,C_boundary or conservative normalized unit coefficients for smoke tests",
        ),
    ]
    return [
        {
            **base(timestamp),
            "bound_id": bound_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": bound_formula,
            "derivation": derivation,
            "inputs_required": inputs_required,
            "numeric_value": "MISSING_COEFFICIENTS",
            "claim_allowed": False,
        }
        for bound_id, symbol, definition, bound_formula, derivation, inputs_required in rows
    ]


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    sources_exist = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    decomposition_emitted = any(row["decomposition_id"] == "PAD3767_3_pullback_decomposition" for row in grouped["decomposition"])
    basis_emitted = len(grouped["operator_basis"]) >= 8
    bound_emitted = any(row["bound_id"] == "LBI3767_7_frame_propagation" for row in grouped["bound_interface"])
    pullback_signed = all(row["passes_current_branch"] is True for row in grouped["vertical_audit"])
    rows = [
        ("CG3767_0_sources", "all 3767 source paths exist", sources_exist, "path hygiene"),
        ("CG3767_1_decomposition_identity", "L_parent=q_obs^*L_red+dB+L_leak identity emitted", decomposition_emitted, "fibre homotopy decomposition exists"),
        ("CG3767_2_operator_basis", "L_leak operator basis emitted", basis_emitted, "leak channels are named"),
        ("CG3767_3_bound_interface", "epsilon_L and delta_frame_source bound emitted", bound_emitted, "failure is boundable"),
        ("CG3767_4_pullback_signed", "current MTS parent action signs L_leak=0", pullback_signed, "blocked by live kappa/source/topological/aux/boundary/readout residuals"),
        ("CG3767_5_kernel_claim", "q_obs kernel-null claim allowed", False, "blocked until CG3767_4 plus source/readout descent pass"),
        ("CG3767_6_local_gr_claim", "local GR/Newton branch claim allowed", False, "blocked until L_leak coefficients vanish or are below all local bounds"),
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
            "DEC3767_0",
            "The parent-action problem is now reduced to an exact identity plus named leak operators.",
            "stop treating the coupling gap as a single mystery; attack the L_leak coefficients one by one",
        ),
        (
            "DEC3767_1",
            "The easiest first zero target is the EH coefficient: if kappa_* is q_obs-owned, the EH coefficient does not leak along ker(Dq_obs).",
            "make kappa/EH coefficient the next derivation target",
        ),
        (
            "DEC3767_2",
            "The most dangerous non-geometric leak remains source constants and material markers.",
            "keep L_leak_theta and L_leak_src live until superselection or coefficient bounds are written",
        ),
        (
            "DEC3767_3",
            "If no coefficient can be proved zero, the project still has a disciplined empirical route.",
            "fill epsilon_i coefficients and compare against Gdot, WEP, PPN, R10, clock, and orbital constraints",
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
            "next_id": "NEXT3767_0",
            "target_doc": "3768-Y5-R2FR-kappa-EH-coefficient-quotient-zero-or-Gdot-PPN-bound.md",
            "target_script": "scripts/Y5_R2FR_3768_kappa_EH_coefficient_quotient_zero_or_Gdot_PPN_bound.py",
            "objective": "prove the EH coupling coefficient kappa_* is q_obs-owned/superselected so L_leak_kappa=0, or turn Lie_EA ln kappa_* into the first numeric residual coefficient bounded by Gdot, Newtonian calibration, and PPN constraints",
            "reason": "3767 isolates L_leak_kappa as the cleanest first action-leak coefficient and it directly controls local Newton/GR calibration",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "PARENT_ACTION_PULLBACK_DECOMPOSITION_DERIVED_LLEAK_BASIS_AND_BOUND_EMITTED_NOT_ZERO",
            "summary": "3767 derives the exact fibre-homotopy decomposition L_parent=q_obs^*L_red+dB+L_leak. It does not prove L_leak=0 for the current MTS branch; instead it names the live leak operators and gives an epsilon_L bound that propagates into delta_frame_source and local-GR residuals.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3767 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3767 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("decomposition_identity", "pullback decomposition identity emitted", any(row["decomposition_id"] == "PAD3767_3_pullback_decomposition" for row in grouped["decomposition"])),
        ("zero_condition", "L_leak zero condition emitted", any(row["decomposition_id"] == "PAD3767_4_zero_condition" for row in grouped["decomposition"])),
        ("operator_basis", "at least eight L_leak operators emitted", len(grouped["operator_basis"]) >= 8),
        ("vertical_audit_nonclaim", "current branch audit leaves residuals live", any(row["passes_current_branch"] is False for row in grouped["vertical_audit"])),
        ("bound_interface", "epsilon_L to delta_frame_source bound emitted", any(row["bound_id"] == "LBI3767_7_frame_propagation" for row in grouped["bound_interface"])),
        ("coefficients_missing", "bound rows remain nonclaim without coefficients", all(row["numeric_value"] == "MISSING_COEFFICIENTS" for row in grouped["bound_interface"])),
        ("claim_gates_closed", "kernel/local-GR claims remain closed", all(row["passed"] is False for row in grouped["claim_gates"] if row["gate_id"] in {"CG3767_4_pullback_signed", "CG3767_5_kernel_claim", "CG3767_6_local_gr_claim"})),
        ("next_target", "3768 kappa/EH coefficient target emitted", grouped["next_target"][0]["target_doc"] == "3768-Y5-R2FR-kappa-EH-coefficient-quotient-zero-or-Gdot-PPN-bound.md"),
        ("no_formalization_leak", "no 3767 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3767*"))),
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
        "# 3767 - Parent Action Pullback Decomposition Or L_leak First Bound",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "This checkpoint turns the parent-action gap into an exact decomposition. Along the vertical fibre of `q_obs`, the difference between the real parent action and the reduced observed action is split into a boundary term plus `L_leak`. If `L_leak=0` and the boundary is silent, 3766 gives the kernel-null certificate. If not, `L_leak` is the residual object to bound.",
        "",
        "## Pullback Decomposition",
    ]
    for row in grouped["decomposition"]:
        lines.append(f"- `{row['decomposition_id']}` `{row['status']}`: {row['statement']} Identity: `{row['identity']}`")
    lines.extend(["", "## L_leak Operator Basis"])
    for row in grouped["operator_basis"]:
        lines.append(f"- `{row['operator_id']}` `{row['symbol']}`: {row['operator_form']} Feeds: `{row['feeds_observables']}`.")
    lines.extend(["", "## Vertical Variation Audit"])
    for row in grouped["vertical_audit"]:
        lines.append(f"- `{row['audit_id']}` pass=`{row['passes_current_branch']}`: {row['action_piece']}. Residual: `{row['live_residual']}`.")
    lines.extend(["", "## Bound Interface"])
    for row in grouped["bound_interface"]:
        lines.append(f"- `{row['bound_id']}` `{row['symbol']}`: {row['bound_formula']} Inputs: {row['inputs_required']}.")
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
        "decomposition": decomposition_rows(timestamp),
        "operator_basis": operator_basis_rows(timestamp),
        "vertical_audit": vertical_audit_rows(timestamp),
        "bound_interface": bound_interface_rows(timestamp),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["decomposition"], grouped["decomposition"])
    write_csv(OUTPUTS["operator_basis"], grouped["operator_basis"])
    write_csv(OUTPUTS["vertical_audit"], grouped["vertical_audit"])
    write_csv(OUTPUTS["bound_interface"], grouped["bound_interface"])
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
        raise SystemExit(f"3767 validation failed: {failures}")
    print("wrote 3767 checkpoint: parent action pullback decomposition and L_leak bound emitted")


if __name__ == "__main__":
    main()
