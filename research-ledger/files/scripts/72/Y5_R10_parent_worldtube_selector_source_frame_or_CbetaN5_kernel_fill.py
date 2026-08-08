from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "942-Y5-R10-parent-worldtube-selector-source-frame-or-CbetaN5-kernel-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "941_doc",
            "path": "941-Y5-R10-Hilbert-worldtube-same-object-glue-or-CbetaN5-operator-fill.md",
            "role": "handoff selecting parent worldtube selector and same-frame lock",
            "needle": "The next lever is now very concrete",
        },
        {
            "source_id": "941_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_941_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V941_14_validation_rows_ready",
        },
        {
            "source_id": "941_obstruction",
            "path": "source-intake/mts_residuals/P8_Y5_R10_941_OBSTRUCTION_AUDIT.csv",
            "role": "worldtube and frame blockers selected as primary next target",
            "needle": "OBS941_0_worldtube_selector",
        },
        {
            "source_id": "941_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_941_NEXT_TARGET.csv",
            "role": "942 target contract",
            "needle": "942-Y5-R10-parent-worldtube-selector-source-frame-or-CbetaN5-kernel-fill.md",
        },
        {
            "source_id": "PAC537_contract",
            "path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
            "role": "parent action clauses for same-frame and fixed-worldtube ownership",
            "needle": "PAC537_2_parent_fixed_worldtube",
        },
        {
            "source_id": "HWT536_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
            "role": "Hilbert worldtube theorem attempt rows",
            "needle": "HWT536_0_parent_worldtube_fixed",
        },
        {
            "source_id": "WT510_clauses",
            "path": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv",
            "role": "open one-observed-frame and source-measure clauses",
            "needle": "WG510_1_minimal_observed_matter_coupling",
        },
        {
            "source_id": "WT510_theorem",
            "path": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
            "role": "EH reference and MTS transfer condition",
            "needle": "T510_2_MTS_transfer_condition",
        },
        {
            "source_id": "WT510_proof",
            "path": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv",
            "role": "Noether/Stokes worldtube proof sketch",
            "needle": "P510_5",
        },
        {
            "source_id": "Hilbert_monopole",
            "path": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
            "role": "same observed matter current and measured-GM contract",
            "needle": "HM0_Hilbert_current_input",
        },
        {
            "source_id": "941_cbeta",
            "path": "source-intake/mts_residuals/P8_Y5_R10_941_CBETA_OPERATOR_FILL.csv",
            "role": "blocked CbetaN5 operator fallback",
            "needle": "CBF941_3_C_beta_N5",
        },
        {
            "source_id": "local_beta_bound",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "R4 beta observation row",
            "needle": "R4_beta",
        },
    ]
    rows = []
    for spec in specs:
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def selector_theorem_attempt() -> list[dict[str, str]]:
    specs = [
        (
            "SEL942_0_parent_variational_domain",
            "parent action has fields Phi and matter psi on one spacetime domain before fitting",
            "S_parent[Phi,psi]=S_geom[Phi]+S_m[e_obs(Phi),psi]",
            "needed so source support is a variational object, not a readout choice",
            "contract_only_no_full_Lagrangian",
        ),
        (
            "SEL942_1_unique_observed_coframe",
            "a single observed metric/coframe map is selected by the parent before source/readout",
            "e_obs = E[Phi], g_obs = eta_ab e_obs^a e_obs^b",
            "same source frame cannot be inferred after orbital fitting",
            "not_parent_signed_key_blocker",
        ),
        (
            "SEL942_2_Hilbert_current_definition",
            "Hilbert source current is the Noether/Hilbert current of that same observed matter action",
            "J_H[tau] = star(T_obs(tau,.)); T_obs^{mu nu}=2/sqrt(-g_obs) delta S_m/delta g_obs_munu",
            "turns source charge into a parent current with support",
            "conditional_on_SEL942_0_and_SEL942_1",
        ),
        (
            "SEL942_3_support_selector",
            "source worldtube is defined as the closed support of the positive observed Hilbert energy current",
            "W_source[tau] := closure supp rho_H, rho_H := T_obs(n,tau), with rho_H>0 on matter support",
            "fixes the compact source domain before exterior linking surfaces are chosen",
            "conditional_requires_energy_condition_and_tau_lock",
        ),
        (
            "SEL942_4_linking_surface_lock",
            "allowed exterior surfaces are surfaces in M\\W_source homologous around the fixed support",
            "S_1 ~ S_2 in H_2(M\\W_source); A subset M\\W_source; boundary A=S_2-S_1",
            "prevents selecting a different mass channel at a different radius",
            "conditional_if_SEL942_3_holds",
        ),
        (
            "SEL942_5_readout_independence",
            "worldtube support and generator are independent of later orbital/clock fit residuals",
            "delta_fit W_source = 0, delta_fit tau = 0, delta_fit e_obs = 0 on the local branch",
            "this is the exact no-smuggling clause for local GR reduction",
            "not_parent_signed",
        ),
        (
            "SEL942_6_same_worldtube_PD_candidate",
            "only after the selector holds can the topological current be the PD representative of the same source",
            "J_M^top = Q_H[W_source] PD(W_source)",
            "removes the wrong-conserved-object loophole",
            "blocked_until_SEL942_1_to_SEL942_5_are_signed",
        ),
        (
            "SEL942_7_total_verdict",
            "the selector theorem is mathematically clean but not a current MTS proof",
            "SEL942_1 and SEL942_5 are open in the current source hierarchy",
            "narrows the missing ingredient to the parent observed-coframe/matter-coupling clause",
            "conditional_theorem_built_no_claim",
        ),
    ]
    return [
        {
            "step_id": step_id,
            "needed_statement": needed_statement,
            "mathematical_form": mathematical_form,
            "why_needed": why_needed,
            "current_status": current_status,
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for step_id, needed_statement, mathematical_form, why_needed, current_status in specs
    ]


def source_frame_lock_audit() -> list[dict[str, str]]:
    specs = [
        (
            "FRAME942_0_unique_frame_map",
            "one observed frame map e_obs=E[Phi]",
            "source mass, clocks, rods, and orbits can otherwise use different effective metrics",
            "Delta_frame_source",
            "local_GR;WEP;clocks;orbital",
            "not_parent_signed",
        ),
        (
            "FRAME942_1_universal_matter_coupling",
            "all ordinary matter species couple to S_m[e_obs,psi_i] with no species-specific e_i",
            "species-dependent source charge becomes a WEP/fifth-force residual",
            "eta_AB;Delta_species_frame",
            "WEP;R10;orbital",
            "not_parent_signed",
        ),
        (
            "FRAME942_2_clock_rod_orbit_readout",
            "clock rates, rod lengths, and orbital geodesic/readout use g_obs",
            "a source can be Hilbert-measured in one frame and observed in another",
            "Delta_clock_frame;Delta_orbit_frame",
            "clocks;PPN;orbital",
            "not_parent_signed",
        ),
        (
            "FRAME942_3_tau_generator_lock",
            "the generator tau is fixed by the same observed asymptotic/time frame in source and readout",
            "mass normalization can drift through time-generator choice",
            "Delta_tau",
            "Gdot;clock;orbital",
            "open_from_WG510_2",
        ),
        (
            "FRAME942_4_no_disformal_leakage",
            "non-EH motion/time/domain fields do not induce a second matter frame in the compact exterior",
            "hidden disformal/Weyl source hair can mimic GR at leading order and fail PPN/R10",
            "Delta_disformal;Delta_Weyl",
            "R10;PPN;WEP",
            "not_parent_signed",
        ),
        (
            "FRAME942_5_support_frame_equivalence",
            "support of J_H[tau] in e_obs is the same support linked by exterior observed surfaces",
            "the PD/topological object can link a different domain than the measured source current",
            "Delta_support_frame",
            "local_GR;orbital",
            "blocked_by_FRAME942_0_to_FRAME942_4",
        ),
        (
            "FRAME942_6_total_verdict",
            "same-frame route remains the best derivation route, but the coupling clause is the key missing signature",
            "S_matter=S_matter[e_obs,psi] must be parent-owned before local-GR promotion",
            "Delta_frame_source_retained",
            "all_local_arenas",
            "conditional_no_claim",
        ),
    ]
    return [
        {
            "frame_id": frame_id,
            "required_lock": required_lock,
            "failure_mode": failure_mode,
            "residual_if_missing": residual_if_missing,
            "observable_link": observable_link,
            "current_status": current_status,
            "resolved": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for frame_id, required_lock, failure_mode, residual_if_missing, observable_link, current_status in specs
    ]


def worldtube_residual_rows() -> list[dict[str, str]]:
    specs = [
        (
            "WTR942_0_Delta_worldtube_domain",
            "Delta_worldtube_domain",
            "sup over allowed source-support/linking choices of |Q_H[S2]-Q_H[S1]|/M_ref",
            "system_id;W_rule;S1;S2;Q_H_S1;Q_H_S2;M_ref;units;source_file;valid_for_claim",
            "MISSING_PARENT_SELECTOR_OR_NUMERIC_BOUND",
        ),
        (
            "WTR942_1_Delta_support_choice",
            "Delta_support_choice",
            "change in compact source support under allowed tau/frame/support definitions",
            "system_id;support_rule_A;support_rule_B;Delta_support_choice;source_file;assumptions;valid_for_claim",
            "MISSING_SUPPORT_RULE_LOCK",
        ),
        (
            "WTR942_2_Delta_linking_surface",
            "Delta_linking_surface",
            "surface-charge variation across homologous exterior surfaces after W_source is fixed",
            "system_id;surface_family;Delta_linking_surface;boundary_flux_terms;source_file;valid_for_claim",
            "MISSING_LINKING_SURFACE_BOUND",
        ),
        (
            "WTR942_3_Delta_frame_source",
            "Delta_frame_source",
            "fractional mismatch between source Hilbert frame and readout frame",
            "system_id;frame_source;frame_readout;Delta_frame_source;observable_link;source_file;valid_for_claim",
            "MISSING_SAME_FRAME_THEOREM_OR_BOUND",
        ),
        (
            "WTR942_4_Delta_tau_lock",
            "Delta_tau",
            "mass-normalization drift from changing the generator tau between source and exterior readout",
            "system_id;tau_source;tau_readout;Delta_tau;source_file;assumptions;valid_for_claim",
            "MISSING_TAU_LOCK",
        ),
        (
            "WTR942_5_epsilon_selector",
            "epsilon_selector_frame",
            "component-sum absolute normalized selector/frame residual",
            "system_id;epsilon_selector_frame;component_sum_abs;M_ref;normalization;source_file;valid_for_claim",
            "MISSING_COMPONENT_INPUTS",
        ),
    ]
    return [
        {
            "input_id": input_id,
            "quantity": quantity,
            "definition": definition,
            "required_columns": required_columns,
            "current_status": current_status,
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for input_id, quantity, definition, required_columns, current_status in specs
    ]


def cbeta_kernel_fallback() -> list[dict[str, str]]:
    beta_bound = ""
    beta_source = ""
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == "R4_beta":
            beta_bound = row.get("upper_bound", "")
            beta_source = row.get("reference_path_or_url", "")
            break
    specs = [
        (
            "KER942_0_beta_bound",
            "beta_bound",
            beta_bound,
            beta_source,
            "source_bound_loaded",
        ),
        (
            "KER942_1_PPN_readout_identity",
            "g_00^(4)_beta",
            "g_00=-1+2U-2 beta U^2+O(v^6); delta beta = -delta g_00^(4)/(2U^2)",
            "standard_PPN_identity_needs_source_solver_before_score",
            "identity_only_not_prediction",
        ),
        (
            "KER942_2_EH_fourth_order_kernel",
            "L_EH^(4)",
            "schematic elliptic weak-field operator mapping retained N5 source vector into delta g_00^(4)",
            "MISSING_GAUGE_FIXED_SECOND_ORDER_OPERATOR_AND_BOUNDARY_CONDITIONS",
            "kernel_schematic_only",
        ),
        (
            "KER942_3_selector_frame_source_vector",
            "S_N5_selector_frame",
            "{Delta_worldtube_domain,Delta_support_choice,Delta_linking_surface,Delta_frame_source,Delta_tau,R_glue}",
            "MISSING_NUMERIC_OR_THEOREM_ZERO_SELECTOR_FRAME_COMPONENTS",
            "source_vector_missing",
        ),
        (
            "KER942_4_C_beta_N5",
            "C_beta_N5",
            "-L_EH^(4)^-1[S_N5_selector_frame]/(2 U^2 X_N5)",
            "MISSING_OPERATOR_SOLUTION_PROFILE_AND_X_N5",
            "formal_definition_only",
        ),
        (
            "KER942_5_score_gate",
            "score_gate",
            "|C_beta_N5 X_N5| <= 7.8e-05 only after selector/frame residuals are real or theorem-zero",
            "derived_gate_no_numeric_prediction",
            "score_blocked",
        ),
    ]
    return [
        {
            "kernel_id": kernel_id,
            "symbol": symbol,
            "definition_or_formula": definition_or_formula,
            "source_or_missing_input": source_or_missing_input,
            "status": status,
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for kernel_id, symbol, definition_or_formula, source_or_missing_input, status in specs
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC942_0_selector_theorem",
            "decision": "conditional_selector_theorem_built_not_parent_signed",
            "reason": "W_source=supp(J_H[tau]) follows cleanly if a unique observed coframe, universal matter coupling, tau lock, and positive Hilbert energy support are parent-owned",
            "consequence": "worldtube choice is narrowed to a concrete parent coupling/support clause, but cannot yet be promoted",
            "next_action": "try to sign the single observed coframe and universal matter coupling contract",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC942_1_same_frame",
            "decision": "same_frame_coupling_is_key_missing_ingredient",
            "reason": "PAC537_1, PAC537_2, WG510_1, and WG510_2 remain open/not_yet_derived in the current hierarchy",
            "consequence": "Delta_frame_source and Delta_worldtube_domain remain active blockers for local GR",
            "next_action": "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC942_2_Cbeta_fallback",
            "decision": "Cbeta_kernel_partially_schematized_still_unscoreable",
            "reason": "PPN beta readout identity can be written, but gauge-fixed L_EH^(4), boundary conditions, and numeric/theorem-zero source vector are missing",
            "consequence": "no beta score or local-GR claim",
            "next_action": "only fill Cbeta numerically after selector/frame residuals are either closed or retained as sourced rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE942_0_worldtube_selector",
            "claim": "W_source=supp(J_H[tau]) is parent-selected before readout",
            "blocker": "unique observed coframe, tau lock, energy-support condition, and fit-independence are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE942_1_same_source_frame",
            "claim": "source, clocks, rods, and orbits use one observed frame",
            "blocker": "S_matter[e_obs,psi] universal coupling clause remains unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE942_2_same_worldtube_PD",
            "claim": "J_M^top is the PD representative of the same Hilbert source worldtube",
            "blocker": "same-worldtube topology cannot be asserted until selector/frame locks hold",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE942_3_Cbeta_score",
            "claim": "C_beta_N5 is numeric and scoreable",
            "blocker": "kernel is schematic and selector/frame source vector is missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE942_4_local_GR",
            "claim": "Newton/local-GR/PPN branch is derived",
            "blocker": "source selector, frame lock, R_glue zero, measured-GM calibration, and PPN stability remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
            "objective": "try to derive/sign the unique observed coframe and universal matter-coupling clause that makes W_source=supp(J_H) parent-owned; otherwise source Delta_frame and Delta_worldtube residual rows",
            "include": "e_obs=E[Phi], S_matter[e_obs,psi_i], tau/n lock, clock/rod/orbit frame equality, no Weyl/disformal leakage, residual Delta_frame_source and Delta_worldtube_domain templates",
            "exclude": "declaring local GR from a conditional theorem, assuming W_source after fitting, hiding species/frame leakage, beta pass claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    selector_rows: list[dict[str, str]],
    frame_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    kernel_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    prior = read_csv(OUT / "P8_Y5_BRR545_941_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    selector_conditional = any(row["step_id"] == "SEL942_7_total_verdict" and row["current_status"] == "conditional_theorem_built_no_claim" for row in selector_rows)
    selector_blockers = any(row["step_id"] == "SEL942_1_unique_observed_coframe" and row["current_status"] == "not_parent_signed_key_blocker" for row in selector_rows) and any(row["step_id"] == "SEL942_5_readout_independence" and row["current_status"] == "not_parent_signed" for row in selector_rows)
    frame_key_missing = any(row["frame_id"] == "FRAME942_6_total_verdict" and row["current_status"] == "conditional_no_claim" for row in frame_rows)
    residuals_blocked = residual_rows and all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in residual_rows)
    cbeta_blocked = any(row["kernel_id"] == "KER942_4_C_beta_N5" and row["status"] == "formal_definition_only" for row in kernel_rows) and any(row["kernel_id"] == "KER942_5_score_gate" and row["status"] == "score_blocked" for row in kernel_rows)
    beta_bound_loaded = any(row["kernel_id"] == "KER942_0_beta_bound" and row["definition_or_formula"] == "7.8e-05" for row in kernel_rows)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decision_rows)
    claims_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
    next_selected = any(row["next_target"].startswith("943-Y5-R10-single-observed-coframe") for row in target_rows)
    no_claims = all(
        row.get("valid_for_claim") == "false"
        for row in sources + selector_rows + frame_rows + residual_rows + kernel_rows + decision_rows + claim_rows + target_rows
    )
    formalization_changed = formalization_changed_after_start()

    add("V942_0_sources_exist_and_needles", sources_ok, "all 942 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V942_1_prior_941_clean", prior_clean, "P8_Y5_BRR545_941_VALIDATION.csv clean")
    add("V942_2_selector_theorem_conditional", selector_conditional, "selector theorem built as conditional only")
    add("V942_3_selector_blockers_retained", selector_blockers, "unique frame and readout-independence blockers retained")
    add("V942_4_frame_key_missing", frame_key_missing, "same observed coframe/matter coupling remains the key missing signature")
    add("V942_5_residuals_blocked", residuals_blocked, "selector/frame residual rows remain non-scoreable")
    add("V942_6_Cbeta_blocked", cbeta_blocked, "C_beta_N5 kernel remains schematic/formal and blocked")
    add("V942_7_beta_bound_loaded", beta_bound_loaded, "R4 beta bound 7.8e-05 loaded")
    add("V942_8_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V942_9_claim_gates_false", claims_false, "all claim gates remain false")
    add("V942_10_next_target_selected", next_selected, "943 observed-coframe coupling target selected")
    add("V942_11_no_claims_promoted", no_claims, "all generated rows are valid_for_claim=false")
    add("V942_12_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V942_13_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    selector_rows: list[dict[str, str]],
    frame_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    kernel_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 942 - Y5/R10 Parent Worldtube Selector Source Frame Or CbetaN5 Kernel Fill

Generated: `{stamp()}`

Status: `Y5_R10_942_parent_worldtube_selector_source_frame_conditional_theorem_built_not_parent_signed_frame_coupling_selected_nonclaim`

Claim ceiling: `selector_frame_gate_only_no_same_worldtube_proof_no_R_glue_zero_no_beta_score_no_local_GR_pass`

## Result

The clean derivation route is now:

```text
S_matter = S_matter[e_obs(Phi), psi_i],
J_H[tau] = star(T_obs(tau,.)),
rho_H = T_obs(n,tau),
W_source[tau] = closure supp(rho_H),
S_1 ~ S_2 in M \\ W_source.
```

If `e_obs`, `tau`, the matter coupling, and the positive Hilbert-energy support are fixed by the parent before readout, then the worldtube is not a fit knob. It is the support of the observed Hilbert source current, and exterior linking surfaces are selected only after that support exists.

That is a useful conditional theorem, but 942 does **not** promote it to an MTS proof. The source hierarchy still has the same signatures unsigned:

```text
e_obs = E[Phi] unique,
S_matter[e_obs, psi_i] universal for ordinary matter,
tau/n fixed in the same observed frame,
delta_fit W_source = 0,
no Weyl/disformal/species leakage into a second source frame.
```

So `W_source=supp(J_H)`, same-worldtube `PD(W_source)`, `R_glue=0`, measured-GM normalization, beta safety, and local-GR reduction remain blocked. The good news is that the missing object is no longer vague: it is the parent coupling/source-frame signature.

The fallback `C_beta_N5` path was sharpened only to a schematic kernel:

```text
delta beta = -delta g_00^(4)/(2 U^2),
delta g_00_N5^(4) = L_EH^(4)^-1[S_N5_selector_frame],
S_N5_selector_frame = {{Delta_worldtube_domain, Delta_frame_source, Delta_tau, R_glue, ...}}.
```

That is still not scoreable until the source vector is theorem-zero or numeric/source-backed.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Selector Theorem Attempt

{md_table(selector_rows, ["step_id", "needed_statement", "mathematical_form", "current_status", "claim_allowed"])}

## Source Frame Lock Audit

{md_table(frame_rows, ["frame_id", "required_lock", "failure_mode", "residual_if_missing", "observable_link", "current_status"])}

## Worldtube Residual Rows

{md_table(residual_rows, ["input_id", "quantity", "definition", "current_status", "score_ready"])}

## Cbeta Kernel Fallback

{md_table(kernel_rows, ["kernel_id", "symbol", "definition_or_formula", "source_or_missing_input", "status", "score_ready"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def ensure_csv_roundtrip(paths: list[Path]) -> None:
    for path in paths:
        rows = read_csv(path)
        if rows and any(None in row for row in rows):
            raise SystemExit(f"malformed CSV row in {path}")


def main() -> None:
    sources = source_register()
    selector_rows = selector_theorem_attempt()
    frame_rows = source_frame_lock_audit()
    residual_rows = worldtube_residual_rows()
    kernel_rows = cbeta_kernel_fallback()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, selector_rows, frame_rows, residual_rows, kernel_rows, decision_rows, claim_rows, target_rows)

    output_specs = [
        (
            OUT / "P8_Y5_R10_942_SOURCE_REGISTER.csv",
            sources,
            ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_942_SELECTOR_THEOREM_ATTEMPT.csv",
            selector_rows,
            ["step_id", "needed_statement", "mathematical_form", "why_needed", "current_status", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_942_SOURCE_FRAME_LOCK_AUDIT.csv",
            frame_rows,
            ["frame_id", "required_lock", "failure_mode", "residual_if_missing", "observable_link", "current_status", "resolved", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_942_WORLDTUBE_RESIDUAL_ROWS.csv",
            residual_rows,
            ["input_id", "quantity", "definition", "required_columns", "current_status", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_942_CBETA_KERNEL_FALLBACK.csv",
            kernel_rows,
            ["kernel_id", "symbol", "definition_or_formula", "source_or_missing_input", "status", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_942_DECISION_LEDGER.csv",
            decision_rows,
            ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_942_CLAIM_GATE.csv",
            claim_rows,
            ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_942_NEXT_TARGET.csv",
            target_rows,
            ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_BRR545_942_VALIDATION.csv",
            validation_rows,
            ["check_id", "result", "detail", "generated_utc"],
        ),
    ]

    for path, rows, fieldnames in output_specs:
        write_csv(path, rows, fieldnames)

    ensure_csv_roundtrip([path for path, _rows, _fieldnames in output_specs])
    write_doc(sources, selector_rows, frame_rows, residual_rows, kernel_rows, decision_rows, claim_rows, target_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")

    print("Y5_R10_942_parent_worldtube_selector_source_frame_conditional_theorem_built_not_parent_signed_frame_coupling_selected_nonclaim")
    print(f"wrote {DOC}")
    print("next target: 943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md")


if __name__ == "__main__":
    main()
