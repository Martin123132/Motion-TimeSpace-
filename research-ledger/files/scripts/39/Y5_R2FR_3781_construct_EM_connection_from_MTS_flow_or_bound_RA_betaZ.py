import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3781"
BRANCH = "MTS_R2FR_Y5_CONSTRUCT_EM_CONNECTION_FROM_MTS_FLOW_OR_BOUND_RA_BETAZ_3781"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3781-Y5-R2FR-construct-EM-connection-from-MTS-flow-or-bound-RA-betaZ.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3781_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3781_PHASE_FLOW_CONNECTION_THEOREM.csv",
    "input_audit": RESIDUALS / "P8_Y5_R2FR_3781_PHASE_FLOW_INPUT_AUDIT.csv",
    "residual_formulas": RESIDUALS / "P8_Y5_R2FR_3781_RA_BETAZ_RESIDUAL_FORMULAS.csv",
    "zem_guard": RESIDUALS / "P8_Y5_R2FR_3781_ZEM_ALPHA_OWNER_GUARD.csv",
    "local_vector": RESIDUALS / "P8_Y5_R2FR_3781_EM_LOCAL_RESIDUAL_VECTOR.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3781_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3781_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3781_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3781_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3781_VALIDATION.csv",
}

SOURCE_PATHS = {
    "spine_after_3780": PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
    "doc_3780": PCW / "3780-Y5-R2FR-vertical-EM-basicness-calculation-A-F-ZEM.md",
    "derivation_3780": RESIDUALS / "P8_Y5_R2FR_3780_VERTICAL_EM_BASICNESS_DERIVATION.csv",
    "a_variation_3780": RESIDUALS / "P8_Y5_R2FR_3780_A_VARIATION_DECOMPOSITION.csv",
    "f_obstruction_3780": RESIDUALS / "P8_Y5_R2FR_3780_F_VARIATION_OBSTRUCTION.csv",
    "zem_action_3780": RESIDUALS / "P8_Y5_R2FR_3780_ZEM_VARIATION_AND_ACTION_LEAK.csv",
    "bounds_3780": RESIDUALS / "P8_Y5_R2FR_3780_EM_RESIDUAL_BOUND_VECTOR.csv",
    "doc_3779": PCW / "3779-Y5-R2FR-qobs-EM-readout-gauge-and-universal-ZEM-certificate.md",
    "doc_1398": PCW / "1398-Y5-R10-RAB-no-observed-counterterm-action-principle-or-lambdaA-prior-bound.md",
    "doc_1399": PCW / "1399-Y5-R10-RAB-gauge-level-index-owner-for-lambdaA-or-finite-alphaEM-prior-vector.md",
    "doc_1400": PCW / "1400-Y5-R10-RAB-joined-EM-coupling-owner-contract-or-finite-local-residual-vector.md",
    "joined_contract_1400": RESIDUALS / "P8_Y5_R10_1400_JOINED_EM_OWNER_CONTRACT.csv",
    "finite_vector_1400": RESIDUALS / "P8_Y5_R10_1400_FINITE_EM_LOCAL_RESIDUAL_VECTOR.csv",
    "fine_structure_alpha": ROOT / "archive" / "uncategorised" / "the-fine-structure-constant.md",
    "fine_structure_angular": ROOT / "archive" / "uncategorised" / "the-fine-structure-constant-from-angular-bandwidth-in-motion-timespace-theory.md",
    "mts_gravity": ROOT / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md",
    "mts_gravity_core": ROOT / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md",
    "yang_mills": ROOT / "quantum-particle-field" / "yang-mills" / "yang-mills-mass-gap-via-the-motion-theory.md",
    "private_heuristics": PCW / "00-martin-fork-heuristics-private.md",
}

BOUNDS = {
    "wep": "2.8e-15",
    "gamma": "2.3e-05",
    "beta": "7.8e-05",
    "gdot": "9.6e-15",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": False,
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_PATHS.items():
        row = base(timestamp)
        row.update(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "role": "evidence or guardrail for the 3781 EM phase-flow connection route",
            }
        )
        rows.append(row)
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "PFC3781_0_parent_data",
            "Assume a parent U(1)-phase variable theta_Q, a phase-flow one-form Pi_Q, and a charge unit q_*.",
            "theta_Q is an S^1 fibre coordinate; Pi_Q is the gauge-invariant observed phase-flow/current one-form; q_* is fixed or superselected.",
            "This is the minimal constructive EM connection package.",
            "SETUP",
            True,
        ),
        (
            "PFC3781_1_connection_definition",
            "Define A_obs := q_*^{-1}(d theta_Q - Pi_Q).",
            "A_obs is not arbitrary; it is reconstructed from phase plus flow.",
            "Under theta_Q -> theta_Q + q_* chi, A_obs -> A_obs + d chi if Pi_Q is gauge invariant.",
            "EXACT_CONNECTION_ANSATZ",
            True,
        ),
        (
            "PFC3781_2_vertical_variation",
            "For E_A in ker(Dq_obs), Lie_EA A_obs = d(Lie_EA theta_Q/q_*) - q_*^{-1} Lie_EA Pi_Q - beta_q,A A_obs.",
            "beta_q,A := Lie_EA ln q_*; terms with spacetime d q_* are forbidden by fixed local charge-unit convention.",
            "The non-gauge residue is R_A = -q_*^{-1} Lie_EA Pi_Q - beta_q,A A_obs.",
            "EXACT_RESIDUE_FORMULA",
            True,
        ),
        (
            "PFC3781_3_zero_condition",
            "If Lie_EA Pi_Q=0 and beta_q,A=0, then Lie_EA A_obs=d(Lie_EA theta_Q/q_*), hence R_A=0.",
            "Pi_Q and q_* must be q_obs-owned or superselected.",
            "This closes the 3780 A-basicness branch without pretending a physical residue is gauge.",
            "EXACT_CONDITIONAL_ZERO_PROOF",
            True,
        ),
        (
            "PFC3781_4_curvature",
            "F_obs=dA_obs=-q_*^{-1} dPi_Q when q_* is fixed, so Lie_EA F_obs=-q_*^{-1} d(Lie_EA Pi_Q)-beta_q,A F_obs.",
            "same fixed-charge convention as PFC3781_2",
            "If Pi_Q and q_* are vertical-silent, F is q_obs-basic.",
            "EXACT_F_BASICNESS_ROUTE",
            True,
        ),
        (
            "PFC3781_5_current_Ward",
            "Gauge symmetry of theta_Q with the same source action gives the Ward identity nabla_a J_Q^a=0 and makes R_A couple only to a genuine current-descent failure.",
            "requires one source action and one q_obs current owner",
            "This connects the EM readout route to same-source Hilbert stress.",
            "CONDITIONAL_WARD_ROUTE",
            True,
        ),
        (
            "PFC3781_6_ZEM_owner",
            "If Z_EM = C_Q N_Q with C_Q and the charge-generator norm N_Q q_obs-owned or superselected, then beta_Z,A=Lie_EA ln Z_EM=0.",
            "compact U(1) gives charge labels, but not N_Q by itself",
            "This is the extra owner needed for the Maxwell kinetic normalization.",
            "CONDITIONAL_ZEM_ZERO_ROUTE_WITH_GUARD",
            True,
        ),
        (
            "PFC3781_7_no_go_guard",
            "Phase-flow construction can close A/F readout but cannot by itself prove unique F^2 or alpha_EM; 1398-1400 keep lambda_A and alpha_EM finite unless the operator/norm/current owner is signed.",
            "uses previous no-counterterm and joined-owner guardrails",
            "No local-GR or EM-lock claim follows from compact U(1) alone.",
            "NO_OVERCLAIM_GUARD",
            False,
        ),
    ]
    rows = []
    for theorem_id, statement, assumptions, meaning, status, constructive in items:
        row = base(timestamp)
        row.update(
            {
                "theorem_id": theorem_id,
                "statement": statement,
                "assumptions": assumptions,
                "meaning": meaning,
                "status": status,
                "constructive": constructive,
            }
        )
        rows.append(row)
    return rows


def input_audit_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "PFI3781_0_theta_Q",
            "parent U(1) phase theta_Q",
            "suggested by MTS phase/psi/gauge material, not formalized as a q_obs bundle coordinate",
            "MOTIVATED_NOT_PARENT_SIGNED",
            "define S^1 phase field and transformation law",
            False,
        ),
        (
            "PFI3781_1_Pi_Q",
            "phase-flow one-form Pi_Q",
            "MTS has flow/phase/current language, but no unique q_obs-owned Pi_Q map is currently supplied",
            "MISSING_EXPLICIT_PARENT_MAP",
            "construct Pi_Q from psi phase/current or mark residual",
            False,
        ),
        (
            "PFI3781_2_q_star",
            "fixed charge unit q_*",
            "compact U(1) supports a charge lattice only after a base unit exists",
            "MISSING_FIXED_CHARGE_UNIT_OWNER",
            "parent-own q_* or keep beta_q,A residual",
            False,
        ),
        (
            "PFI3781_3_N_Q",
            "charge-generator norm or kinetic normalization N_Q",
            "1399/1400 say compact U(1) does not fix the continuous Maxwell kinetic coefficient",
            "MISSING_ZEM_NORM_OWNER",
            "derive N_Q from parent metric/topological level/spectral owner or bound alpha_EM",
            False,
        ),
        (
            "PFI3781_4_no_pullback_lambda",
            "no standalone observed Maxwell pullback counterterm lambda_A",
            "1398 gives a no-go for locality/gauge/diffeomorphism-only exclusion",
            "NOT_EXCLUDED",
            "needs primitive-only operator basis or finite lambda_A vector",
            False,
        ),
        (
            "PFI3781_5_same_source_current",
            "same q_obs source action owns J_Q",
            "3779/3780 require Ward/current descent but current corpus has not signed it",
            "MISSING_CURRENT_OWNER",
            "connect phase-flow current to total Hilbert source",
            False,
        ),
        (
            "PFI3781_6_local_patch",
            "local contractible patch or Wilson silence",
            "3780 allows local simplification but parent document has not declared the patch/cohomology guard",
            "MISSING_LOCAL_COHOMOLOGY_CERTIFICATE",
            "declare H^1(U)=0 for local PPN/Newton patch or bound Wilson terms",
            False,
        ),
    ]
    rows = []
    for audit_id, required_input, evidence, status, next_action, signed in items:
        row = base(timestamp)
        row.update(
            {
                "audit_id": audit_id,
                "required_input": required_input,
                "evidence": evidence,
                "status": status,
                "next_action": next_action,
                "parent_signed": signed,
            }
        )
        rows.append(row)
    return rows


def residual_formula_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "RBF3781_0_RA",
            "R_A",
            "-q_*^{-1} Lie_EA Pi_Q - beta_q,A A_obs",
            "non-gauge vertical EM potential residue",
            "zero iff Pi_Q and q_* are vertical-silent",
        ),
        (
            "RBF3781_1_dRA",
            "dR_A",
            "-q_*^{-1} d(Lie_EA Pi_Q) - beta_q,A F_obs - d(beta_q,A) wedge A_obs",
            "vertical EM field-strength leakage",
            "zero iff Pi_Q/q_* are silent and beta_q,A is zero/constant-silent",
        ),
        (
            "RBF3781_2_beta_q",
            "beta_q,A",
            "Lie_EA ln q_*",
            "charge-unit leakage along hidden fibre",
            "feeds A/F residue and alpha normalization",
        ),
        (
            "RBF3781_3_beta_Z",
            "beta_Z,A",
            "Lie_EA ln Z_EM = Lie_EA ln C_Q + Lie_EA ln N_Q",
            "Maxwell kinetic/alpha_EM leakage",
            "zero only from q_obs/superselected normalization owner",
        ),
        (
            "RBF3781_4_lambda_A",
            "lambda_A",
            "coefficient of allowed observed Maxwell pullback counterterm",
            "unique F2 failure from 1398/1400",
            "finite residual unless primitive-only operator basis forbids it",
        ),
        (
            "RBF3781_5_R_EM_local",
            "R_EM_local",
            "(R_A,dR_A,beta_q,A,beta_Z,A,lambda_A,current_owner,Wilson)",
            "joined local EM residual vector",
            "must be zeroed or bounded before local-GR EM promotion",
        ),
    ]
    rows = []
    for formula_id, symbol, expression, meaning, zero_condition in items:
        row = base(timestamp)
        row.update(
            {
                "formula_id": formula_id,
                "symbol": symbol,
                "expression": expression,
                "meaning": meaning,
                "zero_condition": zero_condition,
            }
        )
        rows.append(row)
    return rows


def zem_guard_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "ZOG3781_0_compact_U1",
            "compact U(1) phase/charge lattice",
            "helps define charge labels and gauge orbit",
            "does not fix continuous Maxwell kinetic coefficient N_Q or alpha_EM",
            "SUPPORT_ONLY",
            False,
        ),
        (
            "ZOG3781_1_phase_flow_connection",
            "A_obs=q_*^{-1}(d theta_Q-Pi_Q)",
            "can close q_obs A/F readout if Pi_Q and q_* descend",
            "does not prove Z_EM or exclude lambda_A F^2",
            "A_F_ROUTE_ONLY",
            False,
        ),
        (
            "ZOG3781_2_norm_owner",
            "Z_EM=C_Q N_Q",
            "would close beta_Z,A if C_Q,N_Q are q_obs-owned/superselected",
            "current corpus has no fixed N_Q owner",
            "PROMISING_BUT_UNSIGNED",
            False,
        ),
        (
            "ZOG3781_3_no_counterterm_guard",
            "primitive-only/no-pullback operator basis",
            "would exclude standalone lambda_A",
            "1398 says ordinary locality/gauge/diffeomorphism do not exclude it",
            "REQUIRES_STRONG_PARENT_SELECTION_RULE",
            False,
        ),
        (
            "ZOG3781_4_finite_alpha_route",
            "finite alpha_EM residual vector",
            "honest fallback if norm owner is not derived",
            "requires clock/WEP/R10/PPN source-backed projections",
            "FALLBACK_NONCLAIM",
            False,
        ),
    ]
    rows = []
    for guard_id, route, helps, does_not_do, verdict, claim_ready in items:
        row = base(timestamp)
        row.update(
            {
                "guard_id": guard_id,
                "route": route,
                "helps": helps,
                "does_not_do": does_not_do,
                "verdict": verdict,
                "claim_ready": claim_ready,
            }
        )
        rows.append(row)
    return rows


def local_vector_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "ELR3781_0_epsilon_A_perp",
            "epsilon_A_perp",
            "||R_A||/||A_obs|| with R_A=-q_*^{-1}Lie_EA Pi_Q-beta_q,A A_obs",
            "MISSING_PI_Q_AND_QSTAR_VERTICAL_SILENCE",
            "dimensionless_or_field_norm",
            "gauge/current; EM readout",
        ),
        (
            "ELR3781_1_epsilon_F_vertical",
            "epsilon_F_vertical",
            "||dR_A||/||F_obs||",
            "MISSING_DPI_Q_VERTICAL_SILENCE",
            "dimensionless",
            "EM stress; PPN; Newton GM",
        ),
        (
            "ELR3781_2_beta_q",
            "beta_q,A",
            "Lie_EA ln q_*",
            "MISSING_CHARGE_UNIT_SUPERSELECTION",
            "dimensionless",
            "charge normalization; alpha_EM",
        ),
        (
            "ELR3781_3_beta_Z",
            "beta_Z,A",
            "Lie_EA ln Z_EM",
            "MISSING_ZEM_NORM_OWNER",
            "dimensionless",
            "WEP; clocks; Gdot; PPN",
        ),
        (
            "ELR3781_4_lambda_A",
            "lambda_A",
            "standalone observed Maxwell pullback coefficient",
            "MISSING_PRIMITIVE_ONLY_OPERATOR_BASIS",
            "declared_action_units",
            "unique F2; alpha_EM",
        ),
        (
            "ELR3781_5_current_owner",
            "epsilon_J_Q",
            "||nabla_a J_Q^a|| + ||J_Q-J_qobs||",
            "MISSING_SAME_SOURCE_WARD_OWNER",
            "current_norm",
            "same-source Hilbert stress",
        ),
        (
            "ELR3781_6_Wilson",
            "epsilon_Wilson",
            "max_C |int_C R_A|/Phi0",
            "MISSING_LOCAL_COHOMOLOGY_OR_BOUNDARY_SILENCE",
            "dimensionless",
            "phase; quantum/EM readout",
        ),
        (
            "ELR3781_7_WEP",
            "eta_EM_AB",
            "C_A epsilon_A_perp + C_F epsilon_F_vertical + C_Z epsilon_ZEM + C_J epsilon_J_Q",
            BOUNDS["wep"],
            "dimensionless",
            "WEP envelope",
        ),
        (
            "ELR3781_8_gamma",
            "delta_gamma_EM",
            "C_g epsilon_EM_shadow_metric + C_F epsilon_F_vertical + C_q Delta_q_EM",
            BOUNDS["gamma"],
            "dimensionless",
            "PPN gamma envelope",
        ),
        (
            "ELR3781_9_Gdot",
            "dln_Geff_dt_EM",
            "|d_t ln Z_EM| + |d_t beta_q| + |d_t epsilon_F_vertical| + source exchange",
            BOUNDS["gdot"],
            "yr^-1",
            "Gdot envelope",
        ),
    ]
    rows = []
    for residual_id, symbol, expression, status_or_bound, units, arena in items:
        row = base(timestamp)
        row.update(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "expression": expression,
                "status_or_bound": status_or_bound,
                "units": units,
                "observable_arena": arena,
                "claim_ready": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(row["exists"] for row in grouped["sources"])
    theorem_emitted = any(row["theorem_id"] == "PFC3781_3_zero_condition" for row in grouped["theorem"])
    residue_formula = any(row["formula_id"] == "RBF3781_0_RA" for row in grouped["residual_formulas"])
    guard_emitted = any(row["guard_id"] == "ZOG3781_3_no_counterterm_guard" for row in grouped["zem_guard"])
    inputs_signed = all(row["parent_signed"] for row in grouped["input_audit"])
    finite_vector_blocked = all(not row["claim_ready"] for row in grouped["local_vector"])
    gates = [
        ("CG3781_0_sources", "all source paths exist", all_sources, "source register resolves", False),
        ("CG3781_1_theorem", "phase-flow connection theorem emitted", theorem_emitted, "A=q^-1(dtheta-Pi) route derived", False),
        ("CG3781_2_residue_formula", "R_A and beta residual formulas emitted", residue_formula, "R_A=-q^-1 Lie Pi - beta_q A", False),
        ("CG3781_3_zem_guard", "Z_EM/alpha no-overclaim guard emitted", guard_emitted, "compact U(1) not enough for alpha", False),
        ("CG3781_4_inputs_parent_signed", "phase-flow inputs parent-signed", inputs_signed, "theta_Q/Pi_Q/q*/N_Q/current/Wilson clauses unsigned", False),
        ("CG3781_5_finite_vector_nonclaim", "finite local EM vector remains nonclaim", finite_vector_blocked, "missing parent/source inputs retained", False),
        ("CG3781_6_EM_promotion", "EM promoted to descended local-GR Hilbert stress", False, "blocked until A/F route and Z_EM/unique-F2/current clauses close", False),
    ]
    rows = []
    for gate_id, gate, passed, details, claim_allowed in gates:
        row = base(timestamp)
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "passed": passed,
                "details": details,
                "claim_allowed": claim_allowed,
            }
        )
        rows.append(row)
    return rows


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "DEC3781_0_best_news",
            "A/F basicness has a constructive route.",
            "If `Pi_Q` is q_obs-owned and `q_*` is fixed, then `R_A=0` and `dR_A=0` follow exactly.",
        ),
        (
            "DEC3781_1_hard_wall",
            "Z_EM/alpha is still a separate owner problem.",
            "Do not let a successful phase-flow connection imply a fixed Maxwell kinetic coefficient.",
        ),
        (
            "DEC3781_2_less_scrutinized_route",
            "The least-cheaty route is to derive the U(1) bundle connection first, then derive or bound the kinetic normalization second.",
            "This separates gauge/readout success from alpha_EM overclaim.",
        ),
        (
            "DEC3781_3_next",
            "Instantiate `Pi_Q` from actual MTS `psi` phase/current/flow objects.",
            "Build the `psi` phase-current source map and test whether it is q_obs-owned or only a finite residual.",
        ),
    ]
    rows = []
    for decision_id, finding, action in items:
        row = base(timestamp)
        row.update({"decision_id": decision_id, "finding": finding, "action": action})
        rows.append(row)
    return rows


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    row = base(timestamp)
    row.update(
        {
            "next_doc": "3782-Y5-R2FR-instantiate-PiQ-from-psi-phase-current-or-finite-EM-vector.md",
            "next_script": "scripts/Y5_R2FR_3782_instantiate_PiQ_from_psi_phase_current_or_finite_EM_vector.py",
            "objective": "Try to define Pi_Q from the actual MTS psi/phase/current/flow corpus and prove it is q_obs-owned; if not, wire Lie_EA Pi_Q, beta_q,A, beta_Z,A, and lambda_A into the finite EM local residual vector.",
            "why_next": "3781 derived the exact connection formula; 3782 must fill the actual parent object rather than creating another abstract contract.",
        }
    )
    return [row]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    row = base(timestamp)
    row.update(
        {
            "status": "PHASE_FLOW_CONNECTION_ROUTE_DERIVED_A_F_CONDITIONAL_ZEM_ALPHA_STILL_UNSIGNED",
            "claim": "No EM-lock, alpha_EM, local-GR, WEP, PPN, or Newton pass is claimed.",
            "summary": "A_obs=q_*^{-1}(dtheta_Q-Pi_Q) gives an exact route to R_A=0 if Pi_Q and q_* are q_obs-owned; Z_EM/alpha still requires an independent norm/operator/current owner.",
        }
    )
    return [row]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization = ROOT / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*3781*")) if formalization.exists() else []
    checks = [
        ("sources_exist", "every cited source path exists", all(row["exists"] for row in grouped["sources"])),
        ("csv_outputs_parse", "all generated CSV outputs exist and parse", all(path.exists() and list(csv.DictReader(path.open(encoding="utf-8"))) for path in generated)),
        ("doc_written", "3781 markdown document written", DOC_PATH.exists()),
        ("connection_theorem", "phase-flow connection theorem emitted", any(row["theorem_id"] == "PFC3781_1_connection_definition" for row in grouped["theorem"])),
        ("ra_formula", "R_A residual formula emitted", any(row["formula_id"] == "RBF3781_0_RA" for row in grouped["residual_formulas"])),
        ("dRA_formula", "dR_A residual formula emitted", any(row["formula_id"] == "RBF3781_1_dRA" for row in grouped["residual_formulas"])),
        ("zem_guard", "Z_EM/alpha guard emitted", any(row["guard_id"] == "ZOG3781_0_compact_U1" for row in grouped["zem_guard"])),
        ("nonclaim_vector", "finite EM local vector remains nonclaim", all(not row["claim_ready"] for row in grouped["local_vector"])),
        ("claim_gate_closed", "EM promotion claim gate remains closed", any(row["gate_id"] == "CG3781_6_EM_promotion" and not row["claim_allowed"] for row in grouped["claim_gates"])),
        ("next_target", "3782 Pi_Q instantiation target emitted", grouped["next_target"][0]["next_doc"].startswith("3782-")),
        ("formalization_clean", "no 3781 files written under formalization-workbench", len(formalization_hits) == 0),
    ]
    rows = []
    for validation_id, description, result in checks:
        row = base(timestamp)
        row.update(
            {
                "validation_id": validation_id,
                "description": description,
                "result": "PASS" if result else "FAIL",
                "details": "",
            }
        )
        rows.append(row)
    return rows


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3781 - Construct EM Connection from MTS Flow or Bound R_A and beta_Z",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        str(grouped["status"][0]["summary"]),
        "",
        "## Result In Plain Terms",
        "",
        "3781 finds the clean constructive route for the EM readout. If MTS supplies a U(1) phase `theta_Q`, a q_obs-owned phase-flow one-form `Pi_Q`, and a fixed charge unit `q_*`, then `A_obs=q_*^{-1}(dtheta_Q-Pi_Q)`. Along hidden q_obs fibres, the only non-gauge residue is `R_A=-q_*^{-1}Lie_EA Pi_Q-beta_q,A A_obs`. So `Pi_Q` vertical silence and fixed `q_*` give `R_A=0` and `dR_A=0`. That is real progress. But `Z_EM`/alpha still needs an independent norm/operator/current owner; compact U(1) alone does not fix the Maxwell kinetic coefficient.",
        "",
        "## Phase-Flow Connection Theorem",
    ]
    for row in grouped["theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} Meaning: {row['meaning']}")

    lines.extend(["", "## Parent Input Audit"])
    for row in grouped["input_audit"]:
        lines.append(f"- `{row['audit_id']}` `{row['status']}`: {row['required_input']}. Evidence: {row['evidence']}. Next: {row['next_action']}")

    lines.extend(["", "## Residual Formulas"])
    for row in grouped["residual_formulas"]:
        lines.append(f"- `{row['formula_id']}` `{row['symbol']}`: {row['expression']}. Meaning: {row['meaning']}. Zero condition: {row['zero_condition']}")

    lines.extend(["", "## Z_EM / Alpha Guard"])
    for row in grouped["zem_guard"]:
        lines.append(f"- `{row['guard_id']}` `{row['verdict']}`: {row['route']} helps: {row['helps']}; does not do: {row['does_not_do']}")

    lines.extend(["", "## Local EM Residual Vector"])
    for row in grouped["local_vector"]:
        lines.append(f"- `{row['residual_id']}` `{row['symbol']}`: {row['expression']} <= `{row['status_or_bound']}` `{row['units']}`. Arena: {row['observable_arena']}")

    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}` claim_allowed=`{row['claim_allowed']}`: {row['gate']}. Details: {row['details']}")

    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}`: {row['finding']} Action: {row['action']}")

    lines.extend(["", "## Next Target"])
    target = grouped["next_target"][0]
    lines.append(f"- `{target['next_doc']}`: {target['objective']}")

    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")

    return "\n".join(lines) + "\n"


def main() -> None:
    timestamp = now()
    grouped = {
        "sources": source_rows(timestamp),
        "theorem": theorem_rows(timestamp),
        "input_audit": input_audit_rows(timestamp),
        "residual_formulas": residual_formula_rows(timestamp),
        "zem_guard": zem_guard_rows(timestamp),
        "local_vector": local_vector_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["input_audit"], grouped["input_audit"])
    write_csv(OUTPUTS["residual_formulas"], grouped["residual_formulas"])
    write_csv(OUTPUTS["zem_guard"], grouped["zem_guard"])
    write_csv(OUTPUTS["local_vector"], grouped["local_vector"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = []
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3781 validation failed: {failures}")
    print("wrote 3781 checkpoint: phase-flow EM connection route emitted")


if __name__ == "__main__":
    main()
