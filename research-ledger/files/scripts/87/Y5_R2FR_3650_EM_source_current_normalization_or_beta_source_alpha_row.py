from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3650"
BRANCH_ID = "MTS_R2FR_Y5_EM_SOURCE_CURRENT_NORMALIZATION_OR_BETA_SOURCE_ALPHA_ROW_3650"
DOC = ROOT / "3650-Y5-R2FR-EM-source-current-normalization-or-beta-source-alpha-row.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3649", RESIDUALS / "P8_Y5_R2FR_3649_NEXT_TARGET.csv", "EM-source-current-normalization", "3649 selected source-current normalization as next target"),
        ("doc_3649", ROOT / "3649-Y5-R2FR-EM-Maxwell-same-frame-stress-or-fEM-coefficient-row.md", "charge current descends from the same owner", "3649 EM-Maxwell theorem caveat"),
        ("coeff_3649", RESIDUALS / "P8_Y5_R2FR_3649_FEM_BALPHA_COEFFICIENT_ROWS.csv", "beta_source_alpha", "3649 beta/source coefficient row"),
        ("proj_3649", RESIDUALS / "P8_Y5_R2FR_3649_EM_OBSERVABLE_PROJECTION_ROWS.csv", "charge_current_Ward", "3649 charge-current observable projection"),
        ("em_lock_989", RESIDUALS / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_2_current_owner", "989 EM-lock current-owner audit"),
        ("alpha_audit_1047", RESIDUALS / "P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv", "AGN1047_1_charge_lattice", "1047 alpha/gauge charge-lattice audit"),
        ("vertex_1048", RESIDUALS / "P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv", "PVS1048_4_no_material_marker_vertex", "1048 material-marker/source audit"),
        ("matrix_1048", RESIDUALS / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv", "BM1048_2_WEP_alpha_mass", "1048 WEP/R10 source projection matrix"),
        ("doc_1048", ROOT / "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md", "beta_source_alpha*b_alpha", "1048 bound-matrix source-coupling formula"),
        ("doc_1054", ROOT / "1054-Y5-R10-beta-source-alpha-zero-theorem-or-first-numeric-prior-width.md", "beta_source_alpha", "1054 beta-source-alpha zero/prior checkpoint"),
        ("doc_1055", ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md", "PAC1055_1_EM_owner", "1055 matter functor parent-action contract"),
        ("local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local WEP/source bound anchor"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
            }
        )
    return rows


def theorem_attempt(ts: str) -> list[dict[str, object]]:
    rows = [
        {
            **base(ts),
            "theorem_id": "SCT3650_0_parent_current_action",
            "claim": "Source-current normalization descends from the same compact charge owner.",
            "mathematical_form": "S_matter=sum_A int mu_obs L_A(Psi_A,D_Q Psi_A,theta_A); D_Q=nabla[e_obs(q)]+A_Q rho_A(T_Q); S_int=int mu_obs A_Q_mu J_Q^mu.",
            "derivation_step": "Varying the same parent EM connection gives J_Q^mu=delta S_matter/dA_Q_mu; the charge generator T_Q and representation rho_A(T_Q) must be the same objects that fixed the Maxwell norm.",
            "result": "If T_Q, rho_A(T_Q), theta_A, particle-number measure, and source Hamiltonian descend through q or fixed representation data, EM source normalization is not an extra fitted coupling.",
            "status": "EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED",
            "missing_for_claim": "parent-signed matter representation/current owner",
        },
        {
            **base(ts),
            "theorem_id": "SCT3650_1_Ward_identity",
            "claim": "Gauge invariance buys conservation, not source calibration by itself.",
            "mathematical_form": "delta_lambda S=0 => nabla_mu J_Q^mu=0 on matter equations, but J_Q^mu -> zeta_A(X_N)J_Q^mu is still a source-normalization leak unless zeta_A is forbidden.",
            "derivation_step": "The Ward identity controls divergence. It does not fix the material charge-to-source map unless the matter functor owns the representation labels and source measure.",
            "result": "Charge conservation is necessary but not sufficient for beta_source_alpha=0.",
            "status": "WARD_CONSERVATION_NOT_ENOUGH",
            "missing_for_claim": "normalization owner, not only conservation owner",
        },
        {
            **base(ts),
            "theorem_id": "SCT3650_2_beta_zero_law",
            "claim": "beta_source_alpha has an exact zero law under representation descent.",
            "mathematical_form": "Q_A^eff=int_Sigma dSigma_mu J_A^mu; beta_source_alpha,A = Lie_vX ln Q_A^eff = Lie_vX ln n_A + Lie_vX ln Z_JA + Lie_vX ln N_A + Lie_vX ln chi_material,A.",
            "derivation_step": "For fixed discrete charge lattice n_A, quotient-owned current renormalization Z_JA, quotient-owned particle/source measure N_A, and no material marker chi_A(X_N), every term on the right vanishes.",
            "result": "beta_source_alpha,A=0 is derivable only from a parent representation/source-measure theorem, not from notation.",
            "status": "BETA_ZERO_LAW_DERIVED_CONDITIONALLY",
            "missing_for_claim": "Z_JA/N_A/material-source descent signatures",
        },
        {
            **base(ts),
            "theorem_id": "SCT3650_3_force_projection",
            "claim": "The observable source coupling has a no-cancellation envelope.",
            "mathematical_form": "qbar_A^EM = beta_source_alpha,A*b_alpha + B_A^EM*f_EM + r_A^Hodge*b_Hodge + r_A^opt*b_optical + q_A^rad; |qbar_A^EM| bounded by the sum of absolute component rows.",
            "derivation_step": "WEP/R10/source-calibration tests see source-test charge products. A quiet clock alpha channel does not silence EM source coupling unless beta_source_alpha and the source sensitivities are also zero or bounded.",
            "result": "This connects the coupling throat to WEP, R10, clocks, PPN/source calibration, and EM stress without assuming cancellations.",
            "status": "OBSERVABLE_ENVELOPE_DERIVED",
            "missing_for_claim": "material sensitivities B_A^EM, source/test composition matrix, tau/domain map",
        },
        {
            **base(ts),
            "theorem_id": "SCT3650_4_current_rescaling_countermodel",
            "claim": "A current rescaling is the live countermodel.",
            "mathematical_form": "Delta S_source=int mu_obs A_Q_mu zeta_A(X_N)J_A^mu or n_A -> n_A[1+epsilon_A(X_N)]; beta_source_alpha,A=Lie_vX ln zeta_A + Lie_vX ln n_A.",
            "derivation_step": "The counterterm is diffeomorphism/gauge compatible if zeta_A is neutral and the parent action has not fixed representation/source labels.",
            "result": "Source/test EM charge can float independently of the Maxwell kinetic coefficient unless the parent matter functor forbids it.",
            "status": "COUNTERMODEL_LIVE",
            "missing_for_claim": "operator-classification/source-label superselection theorem",
        },
        {
            **base(ts),
            "theorem_id": "SCT3650_5_verdict",
            "claim": "Current MTS proves beta_source_alpha=0.",
            "mathematical_form": "SCT3650_0 through SCT3650_4 parent-signed => beta_source_alpha,A=0 and source-current coupling cannot be tuned separately from alpha_EM.",
            "derivation_step": "All source-current, representation, material marker, and source-measure clauses must close together.",
            "result": "The derivation path is precise but unsigned; beta_source_alpha and source/test sensitivity rows remain live.",
            "status": "FAIL_CURRENT_CLAIM_SOURCE_CURRENT_OWNER_UNSIGNED",
            "missing_for_claim": "parent-signed representation/source-measure/material-label owner",
        },
    ]
    return rows


def clause_audit(ts: str) -> list[dict[str, object]]:
    specs = [
        ("SCA3650_0_TQ_same_owner", "same compact T_Q owns Maxwell norm and matter charge", "T_Q appears in both S_EM and D_Q matter with fixed norm/lattice", "PARTIAL_UNSIGNED", "gauge current normalization can be rescaled", "beta_source_alpha;b_alpha"),
        ("SCA3650_1_rep_lattice", "discrete representation charge labels", "rho_A(T_Q), n_A in fixed representation data with Lie_vX n_A=0", "UNSIGNED", "smooth source charge label can leak", "beta_charge_lattice"),
        ("SCA3650_2_current_measure", "current density/source measure descent", "J_Q^mu and source measure N_A descend through q/e_obs", "UNSIGNED", "source/test charge strength can vary by material", "b_J_source"),
        ("SCA3650_3_material_marker", "no material preparation/source marker", "material labels are representation/composition data, not chi_A(X_N)", "UNSIGNED", "WEP/R10 source charges can be hidden in preparation labels", "b_material_marker"),
        ("SCA3650_4_EM_binding_sensitivity", "EM binding/source sensitivity matrix", "B_A^EM or theorem-zero supplied for source/test materials", "MISSING_SENSITIVITY_MATRIX", "eta_AB and R10 qbar cannot score", "B_A_EM;DeltaQ_EM_AB"),
        ("SCA3650_5_Ward_boundary", "Ward identity plus boundary/source flux closure", "nabla_mu J_Q^mu=0 and boundary flux silence in the local domain", "UNSIGNED", "local source charge can leak through boundaries or screening domain", "b_boundary_current"),
        ("SCA3650_6_total", "source-current coupling closure", "all clauses signed or all component rows numeric/source-backed", "SOURCE_CURRENT_OWNER_UNSIGNED", "no WEP/R10/PPN/source-calibration pass", "q_source_EM_abs"),
    ]
    return [
        {
            **base(ts),
            "audit_id": audit_id,
            "clause": clause,
            "required_signature": required,
            "current_status": status,
            "blocks": blocks,
            "fallback_symbol": fallback,
        }
        for audit_id, clause, required, status, blocks, fallback in specs
    ]


def beta_rows(ts: str) -> list[dict[str, object]]:
    row_base = {**base(ts), "score_ready": False}
    specs = [
        ("BSA3650_0_beta_zero", "beta_source_alpha_zero_candidate", "beta_source_alpha,A=0 if charge-current/source representation theorem is parent-signed", "dimensionless", "parent theorem certificate; source-current owner path", "MISSING_PARENT_SOURCE_CURRENT_THEOREM", "WEP;R10;source_calibration"),
        ("BSA3650_1_beta_source_alpha", "beta_source_alpha", "vertical derivative of effective source/test EM charge normalization", "dimensionless per normalized Xhat", "T_Q owner; representation labels; current measure; material source path", "MISSING_SOURCE_CURRENT_NORMALIZATION", "WEP;R10;PPN_source"),
        ("BSA3650_2_beta_charge_lattice", "beta_charge_lattice", "Lie_vX ln n_A or charge-lattice representation leakage", "dimensionless per normalized Xhat", "fixed representation lattice theorem or charge-label source", "MISSING_CHARGE_LATTICE_OWNER", "charge_current_Ward;WEP"),
        ("BSA3650_3_bJ_source", "b_J_source", "vertical derivative of current density/source measure normalization Z_JA*N_A", "dimensionless per normalized Xhat", "current-measure descent theorem or source-measure coefficient", "MISSING_CURRENT_MEASURE_DESCENT", "source_calibration;PPN"),
        ("BSA3650_4_bmaterial", "b_material_marker", "material/preparation marker derivative in source/test charge map", "dimensionless per normalized Xhat", "no-marker theorem for source labels or composition matrix", "MISSING_MATERIAL_MARKER_DESCENT", "WEP;R10"),
        ("BSA3650_5_BAEM", "B_A_EM", "EM binding/source sensitivity for material A", "dimensionless sensitivity", "composition/material sensitivity matrix with source path", "MISSING_EM_BINDING_SENSITIVITY_MATRIX", "WEP;R10"),
        ("BSA3650_6_boundary", "b_boundary_current", "boundary/domain current leakage in local source charge", "dimensionless per domain", "local domain/boundary flux silence theorem", "MISSING_BOUNDARY_CURRENT_CLOSURE", "R10;PPN;orbital"),
        ("BSA3650_7_total_guard", "q_source_EM_abs", "sum of absolute source-current components: |q_source_EM| <= |beta_source_alpha|+|beta_charge_lattice|+|b_J_source|+|b_material_marker|+|B_A_EM f_EM|+|b_boundary_current|", "dimensionless/source-normalized envelope", "all component rows theorem-zero or numeric/source-backed", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
    ]
    return [
        {
            **row_base,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "required_inputs": required,
            "current_status": status,
            "observable_links": links,
        }
        for row_id, symbol, definition, units, required, status, links in specs
    ]


def projection_rows(ts: str) -> list[dict[str, object]]:
    row_base = {**base(ts), "score_ready": False}
    specs = [
        ("SP3650_0_Ward", "charge_current_Ward", "nabla_mu J_Q^mu=0 follows from gauge invariance, but beta_source_alpha=0 requires fixed normalization owner", "T_Q;rho_A;J_Q;boundary terms", "CONSERVATION_READY_NORMALIZATION_UNSIGNED"),
        ("SP3650_1_WEP", "WEP_source_charge", "eta_AB_EM receives Delta(beta_source_alpha*b_alpha + B_A_EM*f_EM + material/source rows)*tau_WEP", "DeltaQ_EM_AB;beta_source_alpha;b_alpha;f_EM;tau_WEP;WEP bound", "COMPOSITION_MATRIX_MISSING"),
        ("SP3650_2_R10", "R10_short_range_source_charge", "alpha_X(lambda) receives K_X Qbar_source Qbar_test/(4*pi Z_X G_obs) with Qbar including q_source_EM_abs", "K_X;Z_X;lambda_X;Qbar_source/test;q_source_EM_abs;R10 curve", "MTS_AND_BOUND_INPUTS_NOT_CLAIM_READY"),
        ("SP3650_3_clock", "clock_alpha_crosscheck", "clock alpha drift constrains b_alpha/readout but cannot alone bound source-current normalization", "DeltaK_alpha;b_alpha;b_Hodge;beta_source_alpha cross-channel rule", "CROSS_CHANNEL_RULE_MISSING"),
        ("SP3650_4_PPN", "PPN_source_calibration", "source Hamiltonian and measured GM can inherit q_source_EM_abs if matter source normalization is not owned", "source Hamiltonian;weak-field map;q_source_EM_abs;PPN bounds", "SOURCE_HAMILTONIAN_OWNER_MISSING"),
        ("SP3650_5_EM", "EM_Maxwell_stress_source", "Maxwell stress exchange closes only if J_Q and Z_EM/Hodge are same-frame and parent-owned", "J_Q;Z_EM;Hodge;f_EM;b_J_source", "SAME_FRAME_SOURCE_OWNER_UNSIGNED"),
        ("SP3650_6_orbital", "orbital_source_mass_charge", "orbital dynamics need source mass/charge calibration separated from fitted GM", "source mass map;EM binding;boundary;orbital residual vector", "ORBITAL_SOURCE_MAP_MISSING"),
        ("SP3650_7_total_guard", "all_local_arenas", "no cancellation between charge lattice, current measure, material marker, EM binding, boundary, and metric residuals", "all component rows;units;source paths", "NO_CANCELLATION_POLICY_ACTIVE"),
    ]
    return [
        {
            **row_base,
            "projection_id": projection_id,
            "arena": arena,
            "projection_law": law,
            "required_inputs": required,
            "current_status": status,
        }
        for projection_id, arena, law, required, status in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "decision_id": "DEC3650_0_theorem_shape",
            "decision": "The source-current zero route is mathematically clear: fixed T_Q plus fixed matter representation/source measure gives beta_source_alpha=0.",
            "status": "SOURCE_CURRENT_THEOREM_SHAPE_EXACT",
        },
        {
            **base(ts),
            "decision_id": "DEC3650_1_current_verdict",
            "decision": "Current MTS does not parent-sign representation labels, current measure, material source markers, or boundary/source flux silence.",
            "status": "PARENT_SOURCE_CURRENT_OWNER_UNSIGNED",
        },
        {
            **base(ts),
            "decision_id": "DEC3650_2_coefficients",
            "decision": "beta_source_alpha, beta_charge_lattice, b_J_source, b_material_marker, B_A_EM, b_boundary_current, and q_source_EM_abs remain nonclaim rows.",
            "status": "BETA_SOURCE_ROWS_CREATED_NOT_SCORE_READY",
        },
        {
            **base(ts),
            "decision_id": "DEC3650_3_next",
            "decision": "Next target is matter representation/source sensitivity: either prove material labels and EM binding sensitivities are quotient-owned, or build the composition matrix rows.",
            "status": "MATTER_REPRESENTATION_SOURCE_SENSITIVITY_NEXT",
        },
    ]


def status_row(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "SOURCE_CURRENT_THEOREM_CONDITIONAL_BETA_ROWS_CREATED",
            "summary": "3650 derives the conditional source-current normalization theorem, shows Ward conservation is insufficient by itself, and creates explicit beta_source_alpha/source-test coupling rows.",
            "claim_ceiling": "no beta_source_alpha=0, source-current owner, local-GR/Newton, WEP, R10, PPN, clock, orbital, or EM stress pass is claimed",
            "useful_result": "The coupling problem is now localized: prove fixed representation/source measure/material labels, or score source-test residuals with a composition/sensitivity matrix.",
        }
    ]


def next_target(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3650_0",
            "target_doc": "3651-Y5-R2FR-matter-representation-source-sensitivity-or-composition-matrix-row.md",
            "target_script": "scripts/Y5_R2FR_3651_matter_representation_source_sensitivity_or_composition_matrix_row.py",
            "objective": "prove material labels, source measures, and EM binding sensitivities are fixed representation/quotient data; if unsigned, build source/test composition matrix rows for WEP, R10, PPN/source, and orbital tests",
            "success_gate": "either matter/source sensitivity is parent-signed, or composition rows have units, source paths, material sensitivities, tau/domain links, and no-cancellation guards",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    beta: list[dict[str, object]],
    projections: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    lines: list[str] = [
        "# 3650 - EM source-current normalization or beta_source_alpha row",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The source-current throat is sharper than the earlier ledger: gauge invariance gives `nabla_mu J_Q^mu=0`, but it does **not** by itself fix source/test charge normalization. The exact zero theorem needs the same compact `T_Q` owner in `S_EM` and `D_Q`, fixed representation labels `rho_A(T_Q)`, a quotient-owned current/source measure, and no material/source marker `chi_A(X_N)`.",
        "",
        "Under those clauses, `Q_A^eff=int_Sigma dSigma_mu J_A^mu` has `beta_source_alpha,A = Lie_vX ln Q_A^eff = 0`. Current MTS does not yet sign those clauses, so `beta_source_alpha` and source/test sensitivity rows remain live.",
        "",
        "## Theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: `{row['status']}` — {row['result']}")
    lines.extend(["", "## Source-current audit"])
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: `{row['fallback_symbol']}` — {row['current_status']}")
    lines.extend(["", "## beta/source coefficient rows"])
    for row in beta:
        lines.append(f"- `{row['row_id']}`: `{row['symbol']}` — {row['current_status']}")
    lines.extend(["", "## Observable projections"])
    for row in projections:
        lines.append(f"- `{row['projection_id']}`: `{row['arena']}` — {row['current_status']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` — {row['decision']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_rows[0]['target_doc']}` via `{next_rows[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    beta: list[dict[str, object]],
    projections: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3650_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3650_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3650_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3650 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3650_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3650_4_theorem_shape", any("D_Q=nabla" in row["mathematical_form"] and "rho_A(T_Q)" in row["mathematical_form"] for row in theorem), "source-current parent-action theorem shape present")
    add("VAL3650_5_Ward_not_enough", any(row["status"] == "WARD_CONSERVATION_NOT_ENOUGH" for row in theorem), "Ward conservation separated from normalization ownership")
    add("VAL3650_6_beta_zero_law", any("beta_source_alpha,A = Lie_vX ln Q_A^eff" in row["mathematical_form"] for row in theorem), "beta_source_alpha zero/amplitude law recorded")
    add("VAL3650_7_countermodel_live", any(row["status"] == "COUNTERMODEL_LIVE" for row in theorem), "source-current countermodel retained")
    add("VAL3650_8_verdict_unsigned", any(row["status"] == "FAIL_CURRENT_CLAIM_SOURCE_CURRENT_OWNER_UNSIGNED" for row in theorem), "source-current owner not claimed")
    required_audit = {"beta_source_alpha;b_alpha", "beta_charge_lattice", "b_J_source", "b_material_marker", "B_A_EM;DeltaQ_EM_AB", "b_boundary_current", "q_source_EM_abs"}
    add("VAL3650_9_audit_complete", required_audit.issubset({row["fallback_symbol"] for row in audit}), "charge lattice, current measure, material, binding, boundary, and total audit rows present")
    required_symbols = {"beta_source_alpha_zero_candidate", "beta_source_alpha", "beta_charge_lattice", "b_J_source", "b_material_marker", "B_A_EM", "b_boundary_current", "q_source_EM_abs"}
    add("VAL3650_10_beta_rows_complete", required_symbols.issubset({row["symbol"] for row in beta}), "beta/source coefficient rows complete")
    required_proj = {"charge_current_Ward", "WEP_source_charge", "R10_short_range_source_charge", "clock_alpha_crosscheck", "PPN_source_calibration", "EM_Maxwell_stress_source"}
    add("VAL3650_11_projection_rows_complete", required_proj.issubset({row["arena"] for row in projections}), "source-current projections complete")
    add("VAL3650_12_no_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in beta + projections), "no 3650 beta/projection rows score-ready")
    add("VAL3650_13_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in sources + theorem + audit + beta + projections + decisions + status + next_rows), "all generated rows remain nonclaim")
    add("VAL3650_14_no_cancellation_guard", any(row["symbol"] == "q_source_EM_abs" and "sum of absolute" in row["definition"] for row in beta), "source coupling no-cancellation envelope present")
    add("VAL3650_15_status_honest", status[0]["status"] == "SOURCE_CURRENT_THEOREM_CONDITIONAL_BETA_ROWS_CREATED", "status keeps theorem conditional")
    doc_text = read_text(DOC)
    add("VAL3650_16_doc_written", "beta_source_alpha" in doc_text and "gauge invariance gives" in doc_text and "Current MTS does not yet sign" in doc_text, "doc records source-current theorem and caveat")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3650*", "3650-Y5-R2FR-*", "Y5_R2FR_3650_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3650_17_no_formalization_leak", not leaks, "no 3650 checkpoint files in formalization-workbench")
    add("VAL3650_18_next_target", next_rows[0]["target_doc"].startswith("3651-") and "composition" in next_rows[0]["target_doc"], "3651 matter/source sensitivity target selected")
    add("VAL3650_19_source_calibration_bridge", any(row["symbol"] == "beta_source_alpha" for row in beta) and any(row["arena"] == "PPN_source_calibration" for row in projections), "source calibration bridge retained")
    return rows


def main() -> int:
    ts = utc_now()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    theorem = theorem_attempt(ts)
    audit = clause_audit(ts)
    beta = beta_rows(ts)
    projections = projection_rows(ts)
    decisions = decision_rows(ts)
    status = status_row(ts)
    next_rows = next_target(ts)

    output_map = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3650_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3650_SOURCE_CURRENT_THEOREM_ATTEMPT.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3650_CHARGE_CURRENT_CLAUSE_AUDIT.csv",
        "beta": RESIDUALS / "P8_Y5_R2FR_3650_BETA_SOURCE_ALPHA_ROWS.csv",
        "projections": RESIDUALS / "P8_Y5_R2FR_3650_SOURCE_TEST_PROJECTION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3650_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3650_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3650_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3650_VALIDATION.csv",
    }

    write_csv(output_map["sources"], sources)
    write_csv(output_map["theorem"], theorem)
    write_csv(output_map["audit"], audit)
    write_csv(output_map["beta"], beta)
    write_csv(output_map["projections"], projections)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["status"], status)
    write_csv(output_map["next"], next_rows)
    write_doc(sources, theorem, audit, beta, projections, decisions, status, next_rows)

    generated_paths = [path for key, path in output_map.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, theorem, audit, beta, projections, decisions, status, next_rows)
    write_csv(output_map["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3650 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3650 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
