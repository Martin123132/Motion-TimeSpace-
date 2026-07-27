from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "1988-Y5-R2FR-action-weight-source-beta-theorem-or-finite-row-fill.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1988_VALIDATION.csv"

SOURCES = {
    "1987_doc": {
        "path": ROOT / "1987-Y5-R2FR-first-residual-component-fill-selector.md",
        "needles": ["NEXT1987_0_primary", "CON1987_1_zero_formula"],
    },
    "1987_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1987_VALIDATION.csv",
        "needles": ["VAL1987_OVERALL", "PASS"],
    },
    "1912_axiom_debt": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1912_MINIMAL_AXIOM_DEBT_LEDGER_NONCLAIM.csv",
        "needles": ["AX1912_4_no_species_source_weights", "AX1912_5_common_measure_current"],
    },
    "1913_q_typing": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1913_Q_FUNCTOR_TYPING_MATRIX_NONCLAIM.csv",
        "needles": ["QTM1913_6_measure_current", "MISSING_AXIOM_NOT_ADOPTED"],
    },
    "1913_parent_action": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1913_PARENT_ACTION_Q_FUNCTOR_CONSTRUCTION_ATTEMPT.csv",
        "needles": ["PAQ1913_4_minimality_guard", "PAQ1913_5_verdict"],
    },
    "1387_action_weight": {
        "path": ROOT / "1387-Y5-R10-RAB-action-weight-exclusion-or-source-beta-first-fill.md",
        "needles": ["AWE1387_7_verdict", "DWB1387_4_beta_product_guard"],
    },
    "1920_delta_rows": {
        "path": ROOT / "1920-Y5-R2FR-source-weight-parent-current-owner-or-delta-w-first-rows.md",
        "needles": ["SWP1920_5_verdict", "DWA1920_0_WEP_TiPt"],
    },
    "1934_wep_bound": {
        "path": ROOT / "1934-Y5-R2FR-WEP-source-weight-first-finite-row-acquisition-nonclaim.md",
        "needles": ["WEP1934_0_MICROSCOPE_TiPt_eta", "REQ1934_0_projection_map"],
    },
    "1936_universality": {
        "path": ROOT / "1936-Y5-R2FR-source-weight-universality-theorem-or-TiPt-material-charge-ledger.md",
        "needles": ["UNIV1936_1_hilbert_source_theorem", "UNIV1936_4_verdict"],
    },
    "1027_coupling": {
        "path": ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
        "needles": ["CE1027_0_common_Weyl", "DEC1027_2_coupling_status"],
    },
    "1687_bound_contract": {
        "path": ROOT / "1687-Y5-R2FR-common-action-measure-current-owner-or-source-weight-bound-acquisition.md",
        "needles": ["BND1687_1_WEP", "BND1687_5_verdict"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1988_SOURCE_REGISTER.csv",
    "conditional_theorem": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1988_CONDITIONAL_THEOREM.csv",
    "parent_signature_gap": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1988_PARENT_SIGNATURE_GAP.csv",
    "countermodel": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1988_COUNTERMODEL_LEDGER.csv",
    "finite_rows": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1988_FINITE_SOURCE_BETA_ROWS.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1988_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1988_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1988_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1988_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "ACTION_WEIGHT_SOURCE_BETA_THEOREM_OR_FINITE_ROW_1988_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1988_WEP_SOURCE_WEIGHT_INEQUALITY_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1988_WEP_SOURCE_WEIGHT_PROJECTION_DENOMINATOR_QUEUE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)


def base_row(stamp: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register(stamp: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, spec in SOURCES.items():
        path = spec["path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in spec["needles"] if needle not in text]
        row = base_row(stamp)
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "1988 action-weight/source-beta theorem or finite row",
                "needles": ";".join(spec["needles"]),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_ANCHOR",
            }
        )
        rows.append(row)
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    stamp = now()

    def row(data: dict[str, str]) -> dict[str, str]:
        merged = base_row(stamp)
        merged.update(data)
        return merged

    conditional_theorem = [
        row(
            {
                "theorem_id": "THM1988_0_parent_form",
                "statement": "If ordinary matter descends from one parent Hilbert action S_matter=sum_A S_A[Psi_A,e_obs(q(Phi)),theta_A] with no independent w_A or kappa_A slot, then no relative action/source weight exists.",
                "derivation": "The Hilbert source is T_mn=-2/sqrt(-g_obs) delta S_matter/delta g_obs^mn; with no pre-variation multiplier, every ordinary sector couples through the same variation rule.",
                "result": "Delta_w_A=0 for ordinary sectors under the stated parent signature",
                "status": "EXACT_CONDITIONAL_THEOREM",
            }
        ),
        row(
            {
                "theorem_id": "THM1988_1_vertical_derivative",
                "statement": "If the memory/vertical generator X is silent on e_obs and theta_A, then beta_w_source=beta_w_test=0.",
                "derivation": "With no w_A(phi) slot and Lie_X e_obs=Lie_X theta_A=0, partial_phi ln w_A is undefined as a physical coefficient rather than nonzero.",
                "result": "beta_w_source=0 and beta_w_test=0 under derivative/readout silence",
                "status": "EXACT_CONDITIONAL_THEOREM",
            }
        ),
        row(
            {
                "theorem_id": "THM1988_2_common_factor",
                "statement": "A single universal constant w_* is calibration only if it is common, constant, and derivative-silent.",
                "derivation": "T_eff=w_* sum_A T_A changes the measured source normalization but not relative WEP/source charge; it cannot hide Delta_w_A or beta_w,A.",
                "result": "w_* may be absorbed into measured G only after Delta_w_A=0 and partial_phi w_*=0",
                "status": "ABSORPTION_GUARD_EXACT",
            }
        ),
        row(
            {
                "theorem_id": "THM1988_3_current_mts_verdict",
                "statement": "Does current MTS derive the parent signature needed by THM1988_0 through THM1988_2?",
                "derivation": "1912/1913/1936 all retain missing parent clauses: no species weights, common measure/current, no hidden homomorphism, and parent certification.",
                "result": "conditional theorem is exact, but not parent-signed in the current corpus",
                "status": "THEOREM_NOT_CLOSED_CURRENT_CORPUS",
            }
        ),
    ]

    parent_signature_gap = [
        row(
            {
                "gap_id": "GAP1988_0_no_species_weights",
                "required_clause": "no w_A(X)S_A, material marker, source-only multiplier, or species Jacobian exists before variation",
                "source_anchor": "AX1912_4_no_species_source_weights;HIL1936_2_no_species_weight",
                "current_status": "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED",
                "effect_if_missing": "Delta_w_A remains a live finite residual",
            }
        ),
        row(
            {
                "gap_id": "GAP1988_1_common_measure_current",
                "required_clause": "one hbar/action measure/current normalization applies to all ordinary sectors",
                "source_anchor": "AX1912_5_common_measure_current;QTM1913_6_measure_current",
                "current_status": "MISSING_AXIOM_NOT_ADOPTED",
                "effect_if_missing": "relative action/source weights survive classical EOM normalization",
            }
        ),
        row(
            {
                "gap_id": "GAP1988_2_no_hidden_hom",
                "required_clause": "hidden/representative variables cannot map into visible matter coefficients except through q_obs or fixed data",
                "source_anchor": "QTM1913_5_no_hidden_hom;CE1027_0_common_Weyl",
                "current_status": "MISSING_AXIOM_NOT_ADOPTED",
                "effect_if_missing": "common Weyl/disformal/source-beta couplings remain legal countermodels",
            }
        ),
        row(
            {
                "gap_id": "GAP1988_3_parent_certification",
                "required_clause": "the parent action/q construction is certified as derived rather than adopted by minimality",
                "source_anchor": "PAQ1913_4_minimality_guard;PAQ1913_5_verdict",
                "current_status": "CONSTRUCTION_CONTRACT_READY_PARENT_CERTIFICATION_FAILED",
                "effect_if_missing": "writing the clean action is a closure, not a derivation",
            }
        ),
        row(
            {
                "gap_id": "GAP1988_4_readout_preservation",
                "required_clause": "readout/projection/boundary maps preserve the no-source-weight theorem",
                "source_anchor": "REQ1934_0_projection_map;BND1687_1_WEP",
                "current_status": "MISSING_ARENA_PROJECTION_MAP",
                "effect_if_missing": "WEP/R10/local comparisons cannot score even if the bulk theorem is conditional",
            }
        ),
    ]

    countermodel = [
        row(
            {
                "countermodel_id": "CEX1988_0_species_action_weight",
                "construction": "S_matter=sum_A (1+epsilon_A f(X)) S_A[Psi_A,e_obs,theta_A]",
                "preserves": "ordinary covariance, locality, isolated classical EOM form after constant rescaling, and standard-looking matter equations",
                "violates": "universal Hilbert source normalization and derivative source-beta silence",
                "why_it_matters": "covariance/minimal-looking equations alone cannot prove Delta_w_A=0 or beta_w,A=0",
                "status": "COUNTERMODEL_SURVIVES_UNLESS_PARENT_OBJECT_LANGUAGE_FORBIDS_SLOT",
            }
        ),
        row(
            {
                "countermodel_id": "CEX1988_1_common_weyl",
                "construction": "g_matter=exp(2F(X)) g_obs for all species",
                "preserves": "composition-blind WEP at leading order",
                "violates": "qbar_XT/source-beta zero for common fifth-force and clock/R10 sectors",
                "why_it_matters": "a WEP-looking pass does not automatically imply local-GR source silence",
                "status": "COUNTERMODEL_SURVIVES_UNLESS_NO_SHADOW_FRAME_SIGNED",
            }
        ),
        row(
            {
                "countermodel_id": "CEX1988_2_constant_absorption",
                "construction": "T_eff=w_* sum_A T_A plus Delta_w_A or beta_w,A tails",
                "preserves": "one measured G calibration for the universal part",
                "violates": "relative/source-dependent components cannot be absorbed",
                "why_it_matters": "measured-G calibration is allowed only for the common constant part",
                "status": "ABSORPTION_GUARD_ACTIVE",
            }
        ),
    ]

    finite_rows = [
        row(
            {
                "row_id": "FIN1988_0_WEP_TiPt_inequality",
                "arena": "MICROSCOPE_WEP_TiPt",
                "quantity": "Delta_w_TiPt or source-weight projection product",
                "source_bound": "abs(eta_TiPt) <= 2.7e-15",
                "mts_formula": "abs(eta_w_TiPt) <= abs(P_WEP*Delta_w_TiPt)+tail_abs",
                "claim_blocker": "P_WEP, Delta_w_TiPt, material charges, source environment, and tail_abs are not derived",
                "status": "REAL_BOUND_SOURCE_BACKED_MTS_PROJECTION_MISSING",
            }
        ),
        row(
            {
                "row_id": "FIN1988_1_R10_product_inequality",
                "arena": "short_range_R10",
                "quantity": "beta_w_source*beta_w_test",
                "source_bound": "alpha_bound(lambda) from real curve required",
                "mts_formula": "K_w(lambda)*abs(beta_w_source*beta_w_test)+epsilon_tail_abs <= alpha_bound(lambda)",
                "claim_blocker": "K_w(lambda), full alpha_bound(lambda), lambda owner, and beta rows missing",
                "status": "FORMULA_READY_VALUES_MISSING",
            }
        ),
        row(
            {
                "row_id": "FIN1988_2_Newton_GM_guard",
                "arena": "Newton_orbital_measured_GM",
                "quantity": "DeltaGM_w/source normalization residual",
                "source_bound": "measured-G/calibration convention required",
                "mts_formula": "abs(DeltaGM_w/GM) <= abs(Delta_w_source)+tail_abs only after calibration body map is declared",
                "claim_blocker": "cannot absorb nonuniversal or derivative weights into measured G",
                "status": "CALIBRATION_CONVENTION_MISSING",
            }
        ),
        row(
            {
                "row_id": "FIN1988_3_PPN_vector_guard",
                "arena": "PPN_local_GR",
                "quantity": "Delta_PPN_source_weight",
                "source_bound": "PPN residual vector and projection rank required",
                "mts_formula": "||Delta_PPN_w|| <= ||P_PPN Delta_w|| + tail_abs",
                "claim_blocker": "P_PPN and source-weight vector not filled",
                "status": "PROJECTION_MATRIX_MISSING",
            }
        ),
        row(
            {
                "row_id": "FIN1988_4_clock_marker_guard",
                "arena": "clocks_constants",
                "quantity": "beta_clock/material marker contribution",
                "source_bound": "clock/frequency sensitivity row required",
                "mts_formula": "abs(delta_nu/nu)_w <= abs(S_clock beta_w)+tail_abs",
                "claim_blocker": "constant-sector and marker descent remain unsigned",
                "status": "MARKER_DESCENT_MISSING",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1988_0_theorem_route",
                "check": "can current corpus close Delta_w=beta_w=0 theorem",
                "result": "FAIL_NOT_PARENT_SIGNED",
                "reason": "countermodel survives and required parent signature clauses remain unsigned",
            }
        ),
        row(
            {
                "run_id": "RUN1988_1_finite_rows",
                "check": "can finite source-beta rows score",
                "result": "FAIL_VALUES_MISSING",
                "reason": "real WEP bound exists, but MTS projection denominator and Delta_w/beta rows are missing",
            }
        ),
        row(
            {
                "run_id": "RUN1988_2_no_cancellation",
                "check": "does runner allow cancellation between unknown residuals",
                "result": "PASS_GUARD",
                "reason": "all formulas are absolute/envelope inequalities",
            }
        ),
        row(
            {
                "run_id": "RUN1988_3_verdict",
                "check": "action-weight/source-beta branch",
                "result": "CONDITIONAL_THEOREM_PLUS_FINITE_NONCLAIM_ROWS",
                "reason": "this is progress, not a pass: the coupling gap is now theorem-or-inequality shaped",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1988_0_conditional_theorem",
                "claim": "universal Hilbert source coupling would imply Delta_w=beta_w=0",
                "status": "PASS_NONCLAIM_CONDITIONAL",
                "reason": "the conditional theorem is exact under explicit parent clauses",
            }
        ),
        row(
            {
                "gate_id": "CG1988_1_parent_signature",
                "claim": "current MTS parent signs the needed source-coupling clauses",
                "status": "FAIL_BLOCKED",
                "reason": "1912/1913/1936 leave no-species-weight and common-current clauses unsigned",
            }
        ),
        row(
            {
                "gate_id": "CG1988_2_wep_numeric",
                "claim": "MTS can compare to MICROSCOPE eta numerically",
                "status": "FAIL_BLOCKED",
                "reason": "P_WEP, Delta_w_TiPt, material charges, and tail_abs missing",
            }
        ),
        row(
            {
                "gate_id": "CG1988_3_local_GR_Newton",
                "claim": "local GR/Newton source coupling is derived",
                "status": "FAIL_BLOCKED",
                "reason": "source-weight theorem not parent-signed and finite rows not filled",
            }
        ),
        row(
            {
                "gate_id": "CG1988_4_R10_PPN_clock",
                "claim": "R10/PPN/clock/orbital branches can score",
                "status": "FAIL_BLOCKED",
                "reason": "arena kernels and source-beta coefficients remain missing",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1988_0_proof_result",
                "decision": "CONDITIONAL_THEOREM_EXACT_BUT_NOT_PARENT_SIGNED",
                "because": "the clean Hilbert source proof works only if the parent object language forbids w_A/kappa_A and readout re-entry; current corpus does not yet sign that",
                "next_action": "do not claim local GR; fill or derive the WEP projection denominator first",
            }
        ),
        row(
            {
                "decision_id": "DEC1988_1_finite_result",
                "decision": "FINITE_WEP_INEQUALITY_STAGED_NONCLAIM",
                "because": "MICROSCOPE gives a real eta bound, so the next useful finite row is P_WEP*Delta_w_TiPt rather than another broad source scan",
                "next_action": "derive P_WEP/material charge map or prove the parent Hilbert source signature",
            }
        ),
        row(
            {
                "decision_id": "DEC1988_2_project_position",
                "decision": "COUPLING_GAP_IS_NOW_SHARP",
                "because": "we know exactly which parent clause must be proved and exactly which finite inequality is used if it fails",
                "next_action": "1989-Y5-R2FR-WEP-source-weight-projection-denominator-or-Hilbert-signature.md",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1988_0_primary",
                "selection_status": "selected",
                "target_doc": "1989-Y5-R2FR-WEP-source-weight-projection-denominator-or-Hilbert-signature.md",
                "target_script": "scripts/Y5_R2FR_WEP_source_weight_projection_denominator_or_Hilbert_signature_1989.py",
                "task": "derive the P_WEP/material-charge denominator connecting Delta_w_TiPt to MICROSCOPE eta, while preserving the option to close the parent Hilbert no-source-weight signature if a proof appears",
                "success_condition": "either P_WEP*Delta_w_TiPt gets a sourced nonclaim inequality row, or the parent source-weight theorem is signed; no WEP/local-GR claim without both projection and coefficients",
                "do_not": "do not set P_WEP=1, invent material charges, absorb Delta_w into measured G, use cancellation, claim WEP/local-GR pass, or modify formalization-workbench",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1988_0_theorem_or_finite_record",
                "artifact_type": "action_weight_source_beta_contract",
                "selected_component": "RC1986_3_action_weight",
                "theorem_status": "CONDITIONAL_EXACT_PARENT_UNSIGNED",
                "finite_status": "WEP_INEQUALITY_STAGED_PROJECTION_MISSING",
                "source_path": str(DOC_PATH),
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1988_0_TiPt_projection_product",
                "observable": "eta_TiPt",
                "bound_abs": "2.7e-15",
                "bound_units": "dimensionless",
                "mts_symbolic_prediction": "eta_pred = P_WEP * Delta_w_TiPt + tail",
                "required_to_compare": "P_WEP;Delta_w_TiPt;tail_abs;material_charge_map;source_environment;sign_units",
                "status": "SOURCE_BOUND_REAL_MTS_PROJECTION_MISSING_NONCLAIM",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1988_0_WEP_denominator",
                "priority": "1",
                "target": "P_WEP material/source projection denominator",
                "inputs_needed": "Ti/Pt material charges; Earth/source environment; tau_WEP; local profile; Delta_w_TiPt convention; acceptance rule",
                "first_action": "derive symbolic eta_pred from action-weight residual using test-body acceleration response",
                "fallback_action": "record missing denominator rows and keep WEP/local-GR blocked",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "conditional_theorem": conditional_theorem,
        "parent_signature_gap": parent_signature_gap,
        "countermodel": countermodel,
        "finite_rows": finite_rows,
        "runner_dryrun": runner_dryrun,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_target,
        "source_weight": source_weight,
        "wep_coeffs": wep_coeffs,
        "queue": queue,
    }


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def val(validation_id: str, status: str, detail: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "status": status,
                "detail": detail,
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )

    source_failures = [row for row in tables["source_register"] if row["status"] != "EXISTS_NEEDLES_CONFIRMED"]
    val("VAL1988_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    theorem_exact = any(row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in tables["conditional_theorem"])
    theorem_not_closed = tables["conditional_theorem"][-1]["status"] == "THEOREM_NOT_CLOSED_CURRENT_CORPUS"
    val("VAL1988_01_theorem_status", "PASS" if theorem_exact and theorem_not_closed else "FAIL", "conditional theorem exact but not promoted")

    countermodel_survives = any("COUNTERMODEL_SURVIVES" in row["status"] for row in tables["countermodel"])
    val("VAL1988_02_countermodel", "PASS" if countermodel_survives else "FAIL", "countermodel retained against covariance/minimality shortcuts")

    wep_row = next((row for row in tables["finite_rows"] if row["row_id"] == "FIN1988_0_WEP_TiPt_inequality"), None)
    wep_ok = bool(wep_row and "2.7e-15" in wep_row["source_bound"] and "PROJECTION_MISSING" in wep_row["status"])
    val("VAL1988_03_wep_inequality", "PASS" if wep_ok else "FAIL", "real WEP bound staged as nonclaim inequality with MTS projection missing")

    runner_blocks = tables["runner_dryrun"][0]["result"] == "FAIL_NOT_PARENT_SIGNED" and tables["runner_dryrun"][1]["result"] == "FAIL_VALUES_MISSING"
    val("VAL1988_04_runner_blocks", "PASS" if runner_blocks else "FAIL", "runner refuses theorem and numeric claims")

    gates_safe = all(row["status"] in {"PASS_NONCLAIM_CONDITIONAL", "FAIL_BLOCKED"} for row in tables["claim_gate"])
    val("VAL1988_05_claim_gates", "PASS" if gates_safe else "FAIL", "all claim gates blocked except conditional nonclaim theorem")

    next_ok = tables["next"][0]["target_doc"] == "1989-Y5-R2FR-WEP-source-weight-projection-denominator-or-Hilbert-signature.md"
    val("VAL1988_06_next_target", "PASS" if next_ok else "FAIL", "1989 WEP projection denominator/Hilbert signature target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1988_07_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1988_08_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1988_09_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        formalization_artifacts = [path for path in FORMALIZATION.rglob("*1988*")]
    val("VAL1988_10_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1988_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1988_OVERALL", overall, "1988 action-weight/source-beta theorem or finite row fill")
    return rows


def markdown_table(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Conditional Theorem", tables["conditional_theorem"]),
        ("Parent Signature Gap", tables["parent_signature_gap"]),
        ("Countermodel Ledger", tables["countermodel"]),
        ("Finite Source-Beta Rows", tables["finite_rows"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1988 Y5 R2FR: Action-Weight Source-Beta Theorem Or Finite Row Fill",
        "",
        "Private checkpoint. This takes the `RC1986_3_action_weight` selection seriously: try the derivation first, then keep a finite row only where the parent proof does not close.",
        "",
        "Verdict: the clean theorem is exact but conditional. A universal parent Hilbert source action with no species/source multiplier and derivative/readout silence gives `Delta_w_A=0`, `beta_w_source=0`, and `beta_w_test=0`. Current MTS does not yet parent-sign those clauses, because the `w_A(X)S_A` countermodel survives covariance/minimality shortcuts.",
        "",
        "Finite fallback: the MICROSCOPE Ti/Pt bound gives a real nonclaim inequality target, `abs(P_WEP*Delta_w_TiPt)+tail_abs <= 2.7e-15`, but `P_WEP`, material charges, source environment, and tails are not derived. No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1988.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1988_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
