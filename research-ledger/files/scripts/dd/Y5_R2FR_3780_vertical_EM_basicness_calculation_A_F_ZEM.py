import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3780"
BRANCH = "MTS_R2FR_Y5_VERTICAL_EM_BASICNESS_CALCULATION_A_F_ZEM_3780"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3780-Y5-R2FR-vertical-EM-basicness-calculation-A-F-ZEM.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3780_SOURCE_REGISTER.csv",
    "derivation": RESIDUALS / "P8_Y5_R2FR_3780_VERTICAL_EM_BASICNESS_DERIVATION.csv",
    "a_variation": RESIDUALS / "P8_Y5_R2FR_3780_A_VARIATION_DECOMPOSITION.csv",
    "f_obstruction": RESIDUALS / "P8_Y5_R2FR_3780_F_VARIATION_OBSTRUCTION.csv",
    "zem_action": RESIDUALS / "P8_Y5_R2FR_3780_ZEM_VARIATION_AND_ACTION_LEAK.csv",
    "cohomology": RESIDUALS / "P8_Y5_R2FR_3780_LOCAL_COHOMOLOGY_CERTIFICATE.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_3780_EM_RESIDUAL_BOUND_VECTOR.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3780_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3780_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3780_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3780_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3780_VALIDATION.csv",
}

SOURCE_PATHS = {
    "spine_after_3779": PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
    "doc_3779": PCW / "3779-Y5-R2FR-qobs-EM-readout-gauge-and-universal-ZEM-certificate.md",
    "theorem_3779": RESIDUALS / "P8_Y5_R2FR_3779_QOBS_EM_CERTIFICATE_THEOREM.csv",
    "extension_3779": RESIDUALS / "P8_Y5_R2FR_3779_QOBS_EM_EXTENSION_MAP.csv",
    "audit_3779": RESIDUALS / "P8_Y5_R2FR_3779_EM_CERTIFICATE_AUDIT.csv",
    "residuals_3779": RESIDUALS / "P8_Y5_R2FR_3779_EM_QOBS_ZEM_RESIDUAL_COEFFICIENTS.csv",
    "bounds_3779": RESIDUALS / "P8_Y5_R2FR_3779_EM_QOBS_ZEM_BOUND_VECTOR.csv",
    "gates_3779": RESIDUALS / "P8_Y5_R2FR_3779_CLAIM_GATES.csv",
    "validation_3779": RESIDUALS / "P8_Y5_BRR545_3779_VALIDATION.csv",
    "doc_3778": PCW / "3778-Y5-R2FR-MTS-to-Maxwell-Hilbert-descent-or-EM-tail-domain-bound.md",
    "maxwell_theorem_3778": RESIDUALS / "P8_Y5_R2FR_3778_MAXWELL_HILBERT_DESCENT_THEOREM.csv",
    "tail_formulas_3778": RESIDUALS / "P8_Y5_R2FR_3778_EM_TAIL_DOMAIN_FORMULAS.csv",
    "kernel_theorem_3766": RESIDUALS / "P8_Y5_R2FR_3766_KERNEL_NULL_THEOREM.csv",
    "qobs_map_3765": RESIDUALS / "P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv",
}

BOUNDS = {
    "wep": "2.8e-15",
    "gamma": "2.3e-05",
    "beta": "7.8e-05",
    "gdot": "9.6e-15",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(timestamp: str) -> dict[str, object]:
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
        row = base_row(timestamp)
        row.update(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "role": "input used to derive or validate the 3780 vertical EM basicness calculation",
            }
        )
        rows.append(row)
    return rows


def derivation_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "VED3780_0_vertical_setup",
            "Let E_A be a basis vector in ker(Dq_obs). For any observed EM potential A_obs(Phi), define delta_A A_obs := Lie_EA A_obs.",
            "Dq_obs[E_A]=0",
            "This is the exact fibre direction whose physical invisibility must be proved.",
            "EXACT_DEFINITION",
            True,
        ),
        (
            "VED3780_1_A_split",
            "Decompose delta_A A_obs = d lambda_A + R_A, where lambda_A is the best gauge representative and R_A is the gauge-orthogonal residue.",
            "Hodge/gauge split on the chosen local patch",
            "R_A is the honest non-gauge obstruction; setting it to zero by naming it gauge would be cheating.",
            "EXACT_LOCAL_DECOMPOSITION_WITH_TOPOLOGY_CAVEAT",
            True,
        ),
        (
            "VED3780_2_F_variation",
            "Since F_obs=dA_obs, delta_A F_obs = d(delta_A A_obs)=dR_A because d^2 lambda_A=0.",
            "F_obs=dA_obs",
            "The local EM readout test is now concrete: prove dR_A=0 or bound ||dR_A||.",
            "EXACT_DERIVATION",
            True,
        ),
        (
            "VED3780_3_local_exactness",
            "On a contractible local patch, dR_A=0 implies R_A=d sigma_A, so delta_A A_obs=d(lambda_A+sigma_A) and delta_A F_obs=0.",
            "H^1(U)=0 or explicit Wilson-cycle silence",
            "Local GR only needs this on the local domain, but global Wilson residues must be declared if H^1(U) is nontrivial.",
            "CONDITIONAL_LOCAL_PLATEAU_FOR_EM_READOUT",
            True,
        ),
        (
            "VED3780_4_pullback_connection_route",
            "If A_obs=Abar(q_obs(Phi))+d Lambda(Phi), then delta_A A_obs=d(Lie_EA Lambda) and delta_A F_obs=0 for every E_A in ker(Dq_obs).",
            "EM is a connection on the observed quotient bundle plus gauge choice",
            "This is the constructive route: make EM a q_obs-bundle connection, not an extra hidden representative field.",
            "EXACT_SUFFICIENT_ZERO_PROOF",
            True,
        ),
        (
            "VED3780_5_ZEM_split",
            "Write ln Z_EM(Phi)=ln Zbar_EM(q_obs(Phi))+z_perp(Phi). Then beta_Z,A:=Lie_EA ln Z_EM=Lie_EA z_perp.",
            "Dq_obs[E_A]=0",
            "Z_EM is the coupling throat: q_obs-owned or superselected gives beta_Z,A=0; otherwise WEP/clocks/Gdot/PPN feel it.",
            "EXACT_COEFFICIENT_EXTRACTION",
            True,
        ),
        (
            "VED3780_6_EM_action_leak",
            "For S_EM=-(1/4) int sqrt(-g_eff) Z_EM F_ab F^ab, the vertical bulk leak is proportional to beta_Z,A F^2 plus the Maxwell-current pairing with R_A, up to boundary terms.",
            "same g_eff and tail/domain boundary terms handled by 3778",
            "A pure-gauge A variation and beta_Z,A=0 make the EM action vertically silent; R_A or beta_Z,A are physical residuals.",
            "EXACT_ACTION_VARIATION_SCHEMA",
            True,
        ),
        (
            "VED3780_7_verdict",
            "The calculation closes the local EM readout only under the pullback-connection/cohomology/Z_EM-superselection clauses; the present parent corpus has not signed those clauses.",
            "requires parent construction of Abar, Lambda, H^1 silence, and Z_EM superselection",
            "3780 is real progress but not a claim: the next step must construct the q_obs U(1) connection from MTS flow/phase data or keep R_A and beta_Z,A as bounded residues.",
            "DERIVED_NOT_PARENT_SIGNED",
            False,
        ),
    ]
    rows = []
    for item_id, formula, assumptions, meaning, status, closes_claim in items:
        row = base_row(timestamp)
        row.update(
            {
                "derivation_id": item_id,
                "formula_or_statement": formula,
                "assumptions": assumptions,
                "meaning": meaning,
                "status": status,
                "closes_claim": closes_claim,
            }
        )
        rows.append(row)
    return rows


def a_variation_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "AVD3780_0_qobs_owned_part",
            "delta_A Abar(q_obs)=D Abar[Dq_obs(E_A)]=0",
            "proved by E_A in ker(Dq_obs)",
            "PASS_CONDITIONAL_ON_Abar_EXISTENCE",
            "no physical EM leakage from the quotient-owned part",
        ),
        (
            "AVD3780_1_gauge_part",
            "delta_A dLambda=d(delta_A Lambda)",
            "ordinary U(1) gauge redundancy",
            "PASS_IF_PARENT_U1_GAUGE_SIGNED",
            "pure gauge, harmless for F and Hilbert stress",
        ),
        (
            "AVD3780_2_residue_part",
            "R_A := delta_A A_obs - d lambda_A",
            "defined after gauge minimization",
            "LIVE_RESIDUAL",
            "physical non-gauge vertical EM potential residue",
        ),
        (
            "AVD3780_3_exact_zero_condition",
            "R_A=0, or R_A=d sigma_A on the local patch",
            "requires parent proof or H^1-local exactness",
            "UNSIGNED",
            "closes A basicness and forces F vertical silence",
        ),
        (
            "AVD3780_4_wilson_obstruction",
            "W_A(C)=int_C R_A",
            "only relevant when nontrivial local/global cycles exist",
            "UNSIGNED_TOPOLOGY_BOUND",
            "flat but non-exact A residue can affect phases even when dR_A=0",
        ),
    ]
    rows = []
    for item_id, expression, condition, status, consequence in items:
        row = base_row(timestamp)
        row.update(
            {
                "decomposition_id": item_id,
                "expression": expression,
                "condition": condition,
                "status": status,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def f_obstruction_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "FOD3780_0_exact_curvature_identity",
            "delta_A F_obs=dR_A",
            "EXACT",
            "The entire F-basicness problem is dR_A.",
            "epsilon_F_vertical=||dR_A||/||F_obs||",
        ),
        (
            "FOD3780_1_local_closed_residue",
            "dR_A=0",
            "UNSIGNED",
            "Locally sufficient for F vertical silence; A is pure gauge if H^1(U)=0.",
            "must prove or bound",
        ),
        (
            "FOD3780_2_harmonic_cycle_residue",
            "R_A=R_A^harm with dR_A=0 but int_C R_A != 0",
            "UNSIGNED_GLOBAL_OR_MESOSCOPIC_CAVEAT",
            "F is silent but charged phases/Wilson loops can still see hidden fibre data.",
            "epsilon_Wilson=max_C |int_C R_A|/Phi0",
        ),
        (
            "FOD3780_3_source_pairing",
            "int sqrt(-g_eff) (nabla_a(Z_EM F^{ab})-J^b) R_{A,b}",
            "UNSIGNED_CURRENT_DESCENT_CAVEAT",
            "A non-gauge residue couples to Maxwell-current failure unless same-source Ward descent is signed.",
            "epsilon_JR",
        ),
    ]
    rows = []
    for item_id, expression, status, meaning, residual in items:
        row = base_row(timestamp)
        row.update(
            {
                "obstruction_id": item_id,
                "expression": expression,
                "status": status,
                "meaning": meaning,
                "residual_row": residual,
            }
        )
        rows.append(row)
    return rows


def zem_action_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "ZAD3780_0_ZEM_pullback",
            "Z_EM=Zbar_EM(q_obs) or Z_EM is superselected",
            "beta_Z,A=Lie_EA ln Z_EM=0",
            "UNSIGNED_ZERO_ROUTE",
            "closes universal EM normalization leakage",
        ),
        (
            "ZAD3780_1_ZEM_perp",
            "ln Z_EM=ln Zbar_EM(q_obs)+z_perp",
            "beta_Z,A=Lie_EA z_perp",
            "EXACT_RESIDUAL_COEFFICIENT",
            "feeds WEP, clocks, Gdot, PPN, and material response",
        ),
        (
            "ZAD3780_2_action_variation",
            "delta_A S_EM=-(1/4) int sqrt(-g_eff) beta_Z,A F^2 - (1/2) int sqrt(-g_eff) Z_EM F^{ab}(dR_A)_{ab} + boundary",
            "same metric and tail/domain terms treated separately",
            "EXACT_VERTICAL_ACTION_LEAK_FORM",
            "shows why beta_Z,A and dR_A are not bookkeeping; they move action and stress",
        ),
        (
            "ZAD3780_3_integrated_by_parts",
            "delta_A S_EM=-(1/4) int sqrt(-g_eff) beta_Z,A F^2 + int sqrt(-g_eff) R_{A,b}(nabla_a(Z_EM F^{ab})-J^b) + boundary/source-exchange",
            "requires same-current convention for J",
            "EXACT_CURRENT_PAIRING_SCHEMA",
            "if Ward descent holds and R_A is gauge/exact, only beta_Z,A remains",
        ),
        (
            "ZAD3780_4_stress_variation",
            "delta_A T_EM^{ab}=beta_Z,A zeta^A T_EM^{ab}+Z_EM[F^{a}{}_c(dR_A)^{bc}+F^{b}{}_c(dR_A)^{ac}-(1/2)g_eff^{ab}F_cd(dR_A)^{cd}]",
            "linearized in vertical amplitude zeta^A",
            "EXACT_STRESS_LEAK_SCHEMA",
            "maps directly into local-GR source residuals",
        ),
    ]
    rows = []
    for item_id, expression, coefficient, status, consequence in items:
        row = base_row(timestamp)
        row.update(
            {
                "action_id": item_id,
                "expression": expression,
                "coefficient_or_condition": coefficient,
                "status": status,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def cohomology_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "LCC3780_0_patch_contractible",
            "H^1(U)=0 for the local patch used by the local-GR expansion",
            "NOT_DOCUMENTED_IN_PARENT_CORPUS",
            False,
            "needed to turn dR_A=0 into R_A=d sigma_A",
        ),
        (
            "LCC3780_1_boundary_wilson_silence",
            "all relevant Wilson cycles either absent, fixed as boundary data, or q_obs-owned",
            "NOT_DOCUMENTED_IN_PARENT_CORPUS",
            False,
            "needed to prevent flat A residues from becoming phase observables",
        ),
        (
            "LCC3780_2_charge_sector_superselection",
            "charge labels and EM phase normalization are q_obs-owned or superselected",
            "NOT_DOCUMENTED_IN_PARENT_CORPUS",
            False,
            "needed to keep Z_EM/charge normalization from becoming composition dependence",
        ),
        (
            "LCC3780_3_local_result_safe",
            "for simply-connected weak-field laboratory/solar-system patches, the local proof can ignore global Wilson sectors if the boundary data are fixed",
            "CONDITIONAL_LOCAL_SIMPLIFICATION",
            True,
            "lets local PPN/Newton work proceed while global/topological EM remains a separate bound row",
        ),
    ]
    rows = []
    for item_id, condition, status, local_use_allowed, consequence in items:
        row = base_row(timestamp)
        row.update(
            {
                "certificate_id": item_id,
                "condition": condition,
                "status": status,
                "local_use_allowed": local_use_allowed,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "EVB3780_0_A_perp",
            "epsilon_A_perp",
            "inf_lambda ||Lie_EA A_obs-dlambda_A||/||A_obs|| = ||R_A||/||A_obs||",
            "MISSING_PARENT_A_RESIDUE",
            "dimensionless_or_field_norm",
            "gauge/current conservation",
            False,
        ),
        (
            "EVB3780_1_F_vertical",
            "epsilon_F_vertical",
            "||dR_A||/||F_obs||",
            "MISSING_PARENT_DRA_NORM",
            "dimensionless",
            "EM stress; Newton GM; PPN",
            False,
        ),
        (
            "EVB3780_2_Wilson",
            "epsilon_Wilson",
            "max_C |int_C R_A|/Phi0",
            "MISSING_WILSON_OR_H1_CERTIFICATE",
            "dimensionless",
            "charged phase; quantum/EM sectors",
            False,
        ),
        (
            "EVB3780_3_ZEM",
            "epsilon_ZEM",
            "|beta_Z,A zeta^A|",
            "MISSING_ZEM_SUPERSELECTION_OR_BETA_ZERO",
            "dimensionless",
            "WEP; clocks; Gdot; PPN",
            False,
        ),
        (
            "EVB3780_4_SEM",
            "epsilon_SEM_vertical",
            "|delta_A S_EM|/|S_EM|",
            "MISSING_VERTICAL_ACTION_SILENCE",
            "dimensionless",
            "same-source Hilbert stress",
            False,
        ),
        (
            "EVB3780_5_WEP",
            "eta_EM_AB",
            "C_Z epsilon_ZEM + C_F epsilon_F_vertical + C_A epsilon_A_perp + C_mat epsilon_EM_material",
            BOUNDS["wep"],
            "dimensionless",
            "WEP",
            False,
        ),
        (
            "EVB3780_6_gamma",
            "delta_gamma_EM",
            "C_g epsilon_EM_shadow_metric + C_q Delta_q_EM + C_F epsilon_F_vertical",
            BOUNDS["gamma"],
            "dimensionless",
            "PPN gamma",
            False,
        ),
        (
            "EVB3780_7_beta",
            "delta_beta_EM",
            "C_beta_Z epsilon_ZEM + C_beta_F epsilon_F_vertical + C_beta_mat epsilon_EM_material",
            BOUNDS["beta"],
            "dimensionless",
            "PPN beta",
            False,
        ),
        (
            "EVB3780_8_Gdot",
            "dln_Geff_dt_EM",
            "|d_t ln Z_EM| + |d_t epsilon_F_vertical| + source-exchange rate",
            BOUNDS["gdot"],
            "yr^-1",
            "Gdot",
            False,
        ),
    ]
    rows = []
    for item_id, symbol, expression, bound, units, arena, claim_ready in items:
        row = base_row(timestamp)
        row.update(
            {
                "bound_id": item_id,
                "symbol": symbol,
                "expression": expression,
                "bound_or_status": bound,
                "units": units,
                "observable_arena": arena,
                "claim_ready": claim_ready,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(row["exists"] for row in grouped["sources"])
    derivation_exact = all(row["closes_claim"] in (True, False) for row in grouped["derivation"])
    pullback_route_present = any(row["derivation_id"] == "VED3780_4_pullback_connection_route" for row in grouped["derivation"])
    a_residue_unsigned = any(row["bound_id"] == "EVB3780_0_A_perp" and str(row["bound_or_status"]).startswith("MISSING") for row in grouped["bounds"])
    f_residue_unsigned = any(row["bound_id"] == "EVB3780_1_F_vertical" and str(row["bound_or_status"]).startswith("MISSING") for row in grouped["bounds"])
    zem_unsigned = any(row["bound_id"] == "EVB3780_3_ZEM" and str(row["bound_or_status"]).startswith("MISSING") for row in grouped["bounds"])
    gates = [
        ("CG3780_0_sources", "all cited 3778/3779/qobs source paths exist", all_sources, "source register checked", False),
        ("CG3780_1_derivation", "vertical A/F/ZEM derivation emitted", derivation_exact, "A split, F=dR_A, Z coefficient, and action leak emitted", False),
        ("CG3780_2_pullback_route", "constructive pullback-connection zero route emitted", pullback_route_present, "A=Abar(q_obs)+dLambda suffices", False),
        ("CG3780_3_A_residue", "A non-gauge residue zeroed", not a_residue_unsigned, "R_A remains parent-unsigned", False),
        ("CG3780_4_F_residue", "F vertical residue zeroed", not f_residue_unsigned, "dR_A remains parent-unsigned", False),
        ("CG3780_5_ZEM", "Z_EM beta coefficient zeroed", not zem_unsigned, "beta_Z,A remains parent-unsigned", False),
        ("CG3780_6_EM_local_GR_claim", "EM local-GR descent claim allowed", False, "blocked until R_A, dR_A, Wilson, beta_Z,A, current, and metric clauses are signed or bounded", False),
    ]
    rows = []
    for gate_id, gate, passed, details, claim_allowed in gates:
        row = base_row(timestamp)
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
            "DEC3780_0",
            "The EM problem has been reduced to a connection-descent problem.",
            "Try to construct A_obs as a U(1) connection over q_obs, with hidden-fibre changes acting only as gauge transformations.",
        ),
        (
            "DEC3780_1",
            "The real obstruction is R_A, not the word coupling.",
            "Either prove R_A is exact/zero on local patches or carry epsilon_A_perp, epsilon_F_vertical, and epsilon_Wilson into WEP/PPN/source bounds.",
        ),
        (
            "DEC3780_2",
            "Z_EM is the normalization throat.",
            "Do not claim universal EM unless beta_Z,A=0, Z_EM is superselected, or a sourced bound beats WEP/clock/Gdot limits.",
        ),
        (
            "DEC3780_3",
            "Poynting/wave energy is not an enemy of the route.",
            "If EM descends as the same q_obs Maxwell sector, Poynting is internal total Hilbert stress; otherwise it remains Q_EM_Poynting or a flux residual.",
        ),
        (
            "DEC3780_4",
            "Next route should be constructive, not another blocker inventory.",
            "Attempt the principal-bundle/flow-phase construction of the EM connection from MTS variables.",
        ),
    ]
    rows = []
    for decision_id, finding, action in items:
        row = base_row(timestamp)
        row.update({"decision_id": decision_id, "finding": finding, "action": action})
        rows.append(row)
    return rows


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    row = base_row(timestamp)
    row.update(
        {
            "next_doc": "3781-Y5-R2FR-construct-EM-connection-from-MTS-flow-or-bound-RA-betaZ.md",
            "next_script": "scripts/Y5_R2FR_3781_construct_EM_connection_from_MTS_flow_or_bound_RA_betaZ.py",
            "objective": "Try to construct A_obs as a q_obs U(1) connection generated by MTS flow/phase data; prove vertical changes are pure gauge and Z_EM is superselected, or emit RA/betaZ bounds.",
            "why_next": "3780 derived the exact conditions; 3781 must supply the parent construction rather than restating missing certificates.",
        }
    )
    return [row]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    row = base_row(timestamp)
    row.update(
        {
            "status": "VERTICAL_EM_BASICNESS_DERIVED_AS_PULLBACK_CONNECTION_CONDITION_NOT_PARENT_SIGNED",
            "claim": "No EM/local-GR pass is claimed.",
            "summary": "A/F basicness closes if A_obs=Abar(q_obs)+dLambda and local cohomology/Wilson residues are silent; Z_EM closes if q_obs-owned or superselected. Parent construction is still required.",
        }
    )
    return [row]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization = PCW.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*3780*")) if formalization.exists() else []
    checks = [
        ("sources_exist", "every cited source path exists", all(row["exists"] for row in grouped["sources"])),
        ("csv_outputs_parse", "all generated CSV outputs exist and parse", all(path.exists() and list(csv.DictReader(path.open(encoding="utf-8"))) for path in generated)),
        ("doc_written", "3780 markdown document written", DOC_PATH.exists()),
        ("a_split", "A variation split emitted", any(row["decomposition_id"] == "AVD3780_2_residue_part" for row in grouped["a_variation"])),
        ("f_derivation", "F=dR_A obstruction emitted", any(row["obstruction_id"] == "FOD3780_0_exact_curvature_identity" for row in grouped["f_obstruction"])),
        ("zem_beta", "beta_Z,A coefficient emitted", any(row["action_id"] == "ZAD3780_1_ZEM_perp" for row in grouped["zem_action"])),
        ("action_leak", "vertical EM action leak emitted", any(row["action_id"] == "ZAD3780_2_action_variation" for row in grouped["zem_action"])),
        ("cohomology_guard", "Wilson/cohomology guard emitted", any(row["certificate_id"] == "LCC3780_1_boundary_wilson_silence" for row in grouped["cohomology"])),
        ("nonclaim_bounds", "missing parent rows remain nonclaim", all(not row["claim_ready"] for row in grouped["bounds"])),
        ("claim_gate_closed", "EM/local-GR claim gate remains closed", any(row["gate_id"] == "CG3780_6_EM_local_GR_claim" and not row["claim_allowed"] for row in grouped["claim_gates"])),
        ("next_target", "3781 constructive EM connection target emitted", grouped["next_target"][0]["next_doc"].startswith("3781-")),
        ("formalization_clean", "no 3780 files written under formalization-workbench", len(formalization_hits) == 0),
    ]
    rows = []
    for validation_id, description, result in checks:
        row = base_row(timestamp)
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
        "# 3780 - Vertical EM Basicness Calculation for A, F, and Z_EM",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        str(grouped["status"][0]["summary"]),
        "",
        "## Result In Plain Terms",
        "",
        "The calculation does not merely say EM is missing. It proves the exact shape of the missing or closing term. For a q_obs-vertical direction `E_A`, split `Lie_EA A_obs=d lambda_A+R_A`. Then `Lie_EA F_obs=dR_A`. So the EM route closes locally if `R_A` is zero/exact and `Z_EM` is q_obs-owned or superselected. If not, `R_A`, `dR_A`, Wilson residues, and `beta_Z,A=Lie_EA ln Z_EM` are the physical residuals that must be bounded.",
        "",
        "## Vertical Derivation",
    ]
    for row in grouped["derivation"]:
        lines.append(f"- `{row['derivation_id']}` `{row['status']}`: {row['formula_or_statement']} Meaning: {row['meaning']}")

    lines.extend(["", "## A Variation Decomposition"])
    for row in grouped["a_variation"]:
        lines.append(f"- `{row['decomposition_id']}` `{row['status']}`: {row['expression']}. Consequence: {row['consequence']}")

    lines.extend(["", "## F Obstruction"])
    for row in grouped["f_obstruction"]:
        lines.append(f"- `{row['obstruction_id']}` `{row['status']}`: {row['expression']}. Residual: `{row['residual_row']}`. Meaning: {row['meaning']}")

    lines.extend(["", "## Z_EM and Action Leak"])
    for row in grouped["zem_action"]:
        lines.append(f"- `{row['action_id']}` `{row['status']}`: {row['expression']}. Consequence: {row['consequence']}")

    lines.extend(["", "## Local Cohomology Guard"])
    for row in grouped["cohomology"]:
        lines.append(f"- `{row['certificate_id']}` local_use=`{row['local_use_allowed']}`: {row['condition']}. Status: `{row['status']}`. Consequence: {row['consequence']}")

    lines.extend(["", "## Residual Bound Vector"])
    for row in grouped["bounds"]:
        lines.append(f"- `{row['bound_id']}` `{row['symbol']}`: {row['expression']} <= `{row['bound_or_status']}` `{row['units']}`. Arena: {row['observable_arena']}")

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
    timestamp = stamp()
    grouped = {
        "sources": source_rows(timestamp),
        "derivation": derivation_rows(timestamp),
        "a_variation": a_variation_rows(timestamp),
        "f_obstruction": f_obstruction_rows(timestamp),
        "zem_action": zem_action_rows(timestamp),
        "cohomology": cohomology_rows(timestamp),
        "bounds": bound_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["derivation"], grouped["derivation"])
    write_csv(OUTPUTS["a_variation"], grouped["a_variation"])
    write_csv(OUTPUTS["f_obstruction"], grouped["f_obstruction"])
    write_csv(OUTPUTS["zem_action"], grouped["zem_action"])
    write_csv(OUTPUTS["cohomology"], grouped["cohomology"])
    write_csv(OUTPUTS["bounds"], grouped["bounds"])
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
        raise SystemExit(f"3780 validation failed: {failures}")
    print("wrote 3780 checkpoint: vertical EM basicness calculation emitted")


if __name__ == "__main__":
    main()
