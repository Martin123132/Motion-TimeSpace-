from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3651"
BRANCH_ID = "MTS_R2FR_Y5_MATTER_REPRESENTATION_SOURCE_SENSITIVITY_OR_COMPOSITION_MATRIX_ROW_3651"
DOC = ROOT / "3651-Y5-R2FR-matter-representation-source-sensitivity-or-composition-matrix-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def row_base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("next_3650", RESIDUALS / "P8_Y5_R2FR_3650_NEXT_TARGET.csv", "matter-representation-source-sensitivity", "3650 selected material/source sensitivity next"),
        ("doc_3650", ROOT / "3650-Y5-R2FR-EM-source-current-normalization-or-beta-source-alpha-row.md", "B_A_EM", "3650 source-current coefficient bottleneck"),
        ("beta_rows_3650", RESIDUALS / "P8_Y5_R2FR_3650_BETA_SOURCE_ALPHA_ROWS.csv", "BSA3650_5_BAEM", "3650 B_A_EM source sensitivity row"),
        ("projection_3650", RESIDUALS / "P8_Y5_R2FR_3650_SOURCE_TEST_PROJECTION_ROWS.csv", "WEP_source_charge", "3650 WEP/R10/PPN source projections"),
        ("matrix_1048", RESIDUALS / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv", "composition charge matrix", "1048 alpha/mass/clock composition matrix requirement"),
        ("vertex_1048", RESIDUALS / "P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv", "PVS1048_4_no_material_marker_vertex", "1048 no material/source marker audit"),
        ("em_lock_989", RESIDUALS / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_4_no_alpha_vertex", "989 matter functor no-alpha/no-mass vertex audit"),
        ("local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local WEP/R10/PPN bound source ledger"),
        ("doc_1048", ROOT / "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md", "DeltaQ_alpha_AB*beta_source_alpha*b_alpha", "1048 WEP source-charge formula"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append(
            {
                **row_base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
            }
        )
    return rows


def theorem_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **row_base(ts),
            "theorem_id": "MSS3651_0_representation_descent",
            "claim": "Matter labels and source sensitivities vanish as independent couplings if matter is fixed representation data.",
            "mathematical_form": "material_A in Rep(P), rho_A=rho_bar_A(q,Psi_A), theta_A=theta_rep or theta_bar(q), and S_A=S_A[Psi_A,e_obs(q),omega(e_obs),A_Q rho_A(T_Q),theta_A].",
            "derivation_step": "For vertical v_X in ker(Dq), fixed representation labels and quotient-owned densities give Lie_vX material_A=Lie_vX theta_A=Lie_vX rho_A=0.",
            "result": "b_material_marker=0, beta_charge_lattice=0, and explicit source-label leakage vanish under this parent-action signature.",
            "status": "EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED",
            "missing_for_claim": "parent-signed matter representation and source-measure clause",
        },
        {
            **row_base(ts),
            "theorem_id": "MSS3651_1_mass_sensitivity_law",
            "claim": "The testable source charge is a logarithmic mass/source sensitivity.",
            "mathematical_form": "Q_A^X = partial ln M_A^eff/partial Xhat = beta_source_alpha,A*b_alpha + B_A^EM*f_EM + B_A^m*b_m + B_A^nuc*b_nuc + b_J_source,A + b_material_marker,A + b_boundary,A.",
            "derivation_step": "Different local arenas see products or differences of Q_A^X; the same source charge must be used for WEP, R10, PPN/source calibration, and orbital source maps.",
            "result": "Composition dependence is not a vague missing item: it is the coefficient vector Q_A^X.",
            "status": "SOURCE_CHARGE_VECTOR_DERIVED",
            "missing_for_claim": "numeric/source-backed component sensitivities and domain tau factors",
        },
        {
            **row_base(ts),
            "theorem_id": "MSS3651_2_EM_binding_law",
            "claim": "The leading EM composition sensitivity is the Coulomb binding fraction.",
            "mathematical_form": "B_A^EM = partial ln M_A/partial ln alpha_EM ~= E_C(A,Z)/(M_A c^2), with E_C=a_C Z(Z-1)A^(-1/3); for mixtures B_mat^EM=sum_i w_i B_i^EM.",
            "derivation_step": "In the semi-empirical mass split, the Coulomb term scales with alpha_EM. The sign convention is fixed by M_A=sum constituents - B_nuc, so the positive Coulomb energy increases M_A relative to non-EM binding.",
            "result": "This gives the concrete composition row needed for WEP/R10 once material isotopes or mixture weights are sourced.",
            "status": "EM_BINDING_FORMULA_DERIVED_SYMBOLICALLY",
            "missing_for_claim": "sourced a_C convention, isotope/mixture table, atomic mass convention",
        },
        {
            **row_base(ts),
            "theorem_id": "MSS3651_3_WEP_R10_projection",
            "claim": "WEP and R10 use the same source/test charge matrix.",
            "mathematical_form": "DeltaQ_AB^X=Q_A^X-Q_B^X; eta_AB ~= DeltaQ_AB^X Q_source^X tau_WEP; alpha_X(lambda)=K_X Q_source^X Q_test^X/(4*pi Z_X G_obs).",
            "derivation_step": "A WEP difference and a Yukawa strength are different projections of one source/test matrix, not separate fitted knobs.",
            "result": "The composition matrix ties the coupling branch directly to empirical tests without assuming local silence.",
            "status": "COMMON_SOURCE_TEST_MATRIX_DERIVED",
            "missing_for_claim": "Q_source, Q_test, tau_WEP, tau_R10, K_X, Z_X, lambda_X",
        },
        {
            **row_base(ts),
            "theorem_id": "MSS3651_4_PPN_orbital_projection",
            "claim": "PPN and orbital fits must separate source calibration from fitted GM.",
            "mathematical_form": "delta(GM)_obs/(GM) = delta G/G + delta M_source/M_source + q_source_EM_abs + q_source_mass_abs + boundary/domain terms.",
            "derivation_step": "If source mass/charge calibration is not parent-owned, local GR/Newton fits can absorb it into GM rather than proving the source branch is zero.",
            "result": "The same composition/source matrix must feed PPN and orbital residual vectors before claiming a GR/Newton limit.",
            "status": "SOURCE_CALIBRATION_GUARD_DERIVED",
            "missing_for_claim": "weak-field source Hamiltonian and orbital source-map rows",
        },
        {
            **row_base(ts),
            "theorem_id": "MSS3651_5_material_countermodel",
            "claim": "A material sensitivity countermodel remains legal unless parent matter forbids it.",
            "mathematical_form": "Delta S_A = -int mu_obs M_A[1+kappa_A(X_N)] n_A or E_C -> E_C[1+kappa_C,A(X_N)] gives Q_A^X -> Q_A^X + Lie_vX kappa_A.",
            "derivation_step": "The counterterm is local and scalar unless representation/source labels are declared non-dynamical or quotient-owned.",
            "result": "Matter/source sensitivities cannot be declared zero from WEP notation or from a fitted GR background alone.",
            "status": "COUNTERMODEL_LIVE",
            "missing_for_claim": "operator-classification ban or numeric sensitivity bounds",
        },
        {
            **row_base(ts),
            "theorem_id": "MSS3651_6_verdict",
            "claim": "Current MTS proves the matter/source sensitivity matrix is zero.",
            "mathematical_form": "MSS3651_0 through MSS3651_5 parent-signed => Q_A^X=0 for retained nonmetric matter/source rows; otherwise score Q_A^X with no-cancellation bounds.",
            "derivation_step": "The zero route needs representation, mass/binding, source measure, material marker, and boundary/domain signatures together.",
            "result": "Current MTS has a derived matrix law but not a parent-signed zero theorem; composition rows remain nonclaim.",
            "status": "FAIL_CURRENT_CLAIM_MATTER_SENSITIVITY_UNSIGNED",
            "missing_for_claim": "parent-signed matter/source sensitivity theorem or numeric matrix",
        },
    ]


def sensitivity_rows(ts: str) -> list[dict[str, object]]:
    base = {**row_base(ts), "score_ready": False}
    specs = [
        ("MSR3651_0_QA_vector", "Q_A_X", "partial ln M_A^eff / partial Xhat total source charge vector", "dimensionless", "3651 symbolic derivation; material mass/source convention", "MATERIAL_COMPONENT_VALUES_REQUIRED", "WEP;R10;PPN;orbital", "tau_WEP;tau_R10;tau_PPN;tau_orbital"),
        ("MSR3651_1_BAEM", "B_A_EM", "partial ln M_A / partial ln alpha_EM ~= E_C/(M_A c^2)", "dimensionless sensitivity", "3651 EM binding law; requires sourced SEMF/nuclear convention", "SOURCE_CONSTANT_AND_ISOTOPE_TABLE_REQUIRED", "WEP;R10;EM", "tau_WEP;tau_R10"),
        ("MSR3651_2_Coulomb_energy", "E_C", "a_C Z(Z-1)A^(-1/3) in energy units", "MeV or joule after convention", "3651 symbolic SEMF law", "A_Z_aC_SOURCE_REQUIRED", "material_sensitivity", "not arena tau; feeds B_A_EM"),
        ("MSR3651_3_DeltaQ", "DeltaQ_AB_X", "Q_A_X - Q_B_X for test-body pair A/B", "dimensionless", "composition rows for both test bodies", "TEST_BODY_COMPOSITION_REQUIRED", "WEP", "tau_WEP"),
        ("MSR3651_4_Qsource", "Q_source_X", "source-body charge vector for Earth/Sun/lab attractor", "dimensionless", "source-body composition/source Hamiltonian row", "SOURCE_BODY_COMPOSITION_REQUIRED", "WEP;R10;PPN;orbital", "tau_WEP;tau_R10;tau_PPN;tau_orbital"),
        ("MSR3651_5_tau_WEP", "tau_WEP", "local transfer factor mapping source charge to Eotvos observable", "dimensionless/domain factor", "local_bounds.csv:R1_WEP_source_charge plus local domain map", "LOCAL_DOMAIN_MAP_REQUIRED", "WEP", "tau_WEP"),
        ("MSR3651_6_tau_R10", "tau_R10", "short-range transfer factor for source/test charge product", "dimensionless/domain factor", "local_bounds.csv:R10_fifth_force plus lambda_X", "LOCAL_DOMAIN_MAP_AND_LAMBDA_REQUIRED", "R10", "tau_R10"),
        ("MSR3651_7_tau_PPN", "tau_PPN", "weak-field transfer from source calibration into PPN residual vector", "dimensionless/domain factor", "local_bounds.csv:R3-R9 plus source Hamiltonian", "WEAK_FIELD_SOURCE_MAP_REQUIRED", "PPN", "tau_PPN"),
        ("MSR3651_8_tau_orbital", "tau_orbital", "orbital transfer from source calibration into fitted GM/residuals", "dimensionless/domain factor", "3651 source-calibration guard; orbital dataset pending", "ORBITAL_SOURCE_MAP_REQUIRED", "orbital", "tau_orbital"),
        ("MSR3651_9_total_guard", "q_matter_source_abs", "sum of absolute material/source components |Q_A_X| envelope with no cancellations", "dimensionless", "all component rows theorem-zero or numeric/source-backed", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas", "all_tau"),
    ]
    return [
        {
            **base,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "source_path_or_formula": source,
            "current_status": status,
            "observable_links": links,
            "tau_domain_link": tau,
        }
        for row_id, symbol, definition, units, source, status, links, tau in specs
    ]


def composition_schema_rows(ts: str) -> list[dict[str, object]]:
    base = {**row_base(ts), "score_ready": False}
    specs = [
        ("CMS3651_0_material_schema", "material_A", "material label must expand to isotope/element mixture rows, not a free X_N marker", "label", "material_name;component_id;Z;A;mass_fraction;atomic_mass;source_path", "MATERIAL_TABLE_SCHEMA_READY_VALUES_MISSING", "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge"),
        ("CMS3651_1_test_A", "test_body_A", "first WEP/R10 test body composition vector", "mixture row set", "Z;A;mass_fraction;B_A_EM;Q_A_X", "TEST_A_COMPOSITION_REQUIRED", "MICROSCOPE Ti/Pt row names source only; numeric composition not inserted"),
        ("CMS3651_2_test_B", "test_body_B", "second WEP/R10 test body composition vector", "mixture row set", "Z;A;mass_fraction;B_A_EM;Q_B_X", "TEST_B_COMPOSITION_REQUIRED", "MICROSCOPE Ti/Pt row names source only; numeric composition not inserted"),
        ("CMS3651_3_source_body", "source_body_S", "attractor/source composition vector for Earth/Sun/lab body", "mixture row set", "Z;A;mass_fraction;Q_source_X", "SOURCE_BODY_COMPOSITION_REQUIRED", "source model not supplied in current corpus"),
        ("CMS3651_4_pair_matrix", "DeltaQ_AB_X", "pairwise sensitivity difference used by WEP", "dimensionless", "Q_A_X-Q_B_X", "PAIR_MATRIX_READY_VALUES_MISSING", "derived row"),
        ("CMS3651_5_yukawa_matrix", "Q_source_X_Q_test_X", "source-test product used by R10 alpha(lambda)", "dimensionless squared", "Q_source_X*Q_test_X", "YUKAWA_PRODUCT_READY_VALUES_MISSING", "derived row"),
        ("CMS3651_6_no_cancellation", "composition_no_cancellation_guard", "use absolute envelope unless a theorem signs cancellation", "policy", "|sum_i terms_i| <= sum_i |terms_i|; score upper envelope", "ACTIVE_NONCLAIM_GUARD", "3651 policy"),
    ]
    return [
        {
            **base,
            "schema_id": schema_id,
            "object": obj,
            "definition": definition,
            "units": units,
            "required_columns_or_formula": required,
            "current_status": status,
            "source_path_or_note": source,
        }
        for schema_id, obj, definition, units, required, status, source in specs
    ]


def projection_rows(ts: str) -> list[dict[str, object]]:
    base = {**row_base(ts), "score_ready": False}
    specs = [
        ("MPR3651_0_WEP", "MICROSCOPE_WEP", "eta_AB ~= DeltaQ_AB_X Q_source_X tau_WEP with DeltaQ including EM/mass/source rows", "DeltaQ_AB_X;Q_source_X;tau_WEP;R1_WEP_source_charge", "COMPOSITION_VALUES_MISSING"),
        ("MPR3651_1_R10", "R10_short_range", "alpha_X(lambda)=K_X Q_source_X Q_test_X/(4*pi Z_X G_obs)", "K_X;Z_X;lambda_X;Q_source_X;Q_test_X;R10_curve", "MTS_AND_BOUND_INPUTS_MISSING"),
        ("MPR3651_2_PPN", "PPN_source_calibration", "PPN vector receives q_matter_source_abs through source Hamiltonian and measured-GM calibration", "source Hamiltonian;q_matter_source_abs;R3-R9 PPN bounds", "SOURCE_HAMILTONIAN_MAP_MISSING"),
        ("MPR3651_3_orbital", "orbital_source_calibration", "orbital fits require separating fitted GM from source mass/charge residuals", "orbital residual vector;source mass map;q_matter_source_abs", "ORBITAL_DATA_MAP_MISSING"),
        ("MPR3651_4_clock", "clock_crosscheck", "clock alpha rows constrain b_alpha/readout but do not replace material sensitivity matrix", "b_alpha;DeltaK_alpha;Q_A_X bridge", "CROSS_CHANNEL_BRIDGE_NOT_SCORE_READY"),
        ("MPR3651_5_EM", "EM_stress_material", "EM stress/source rows use B_A_EM and source-current owner consistently", "f_EM;B_A_EM;beta_source_alpha;T_EM", "EM_SOURCE_OWNER_UNSIGNED"),
        ("MPR3651_6_total", "all_local_arenas", "same Q_A_X matrix must be used across WEP, R10, PPN, orbital, and EM rows", "all component rows;all tau links;source paths", "NO_CANCELLATION_POLICY_ACTIVE"),
    ]
    return [
        {
            **base,
            "projection_id": projection_id,
            "arena": arena,
            "projection_law": law,
            "required_inputs": required,
            "current_status": status,
        }
        for projection_id, arena, law, required, status in specs
    ]


def decisions(ts: str) -> list[dict[str, object]]:
    return [
        {
            **row_base(ts),
            "decision_id": "DEC3651_0_derivation",
            "decision": "The material/source sensitivity law is now derived as Q_A^X=partial ln M_A^eff/partial Xhat, with EM Coulomb binding B_A^EM ~= E_C/(M_A c^2).",
            "status": "MATERIAL_SENSITIVITY_LAW_DERIVED",
        },
        {
            **row_base(ts),
            "decision_id": "DEC3651_1_verdict",
            "decision": "Current MTS does not parent-sign representation/source measure/material/binding closure, so Q_A^X is not zero-claimed.",
            "status": "PARENT_MATTER_SENSITIVITY_UNSIGNED",
        },
        {
            **row_base(ts),
            "decision_id": "DEC3651_2_matrix",
            "decision": "Composition matrix schema is staged with units, formulas, source-path hooks, tau links, and no-cancellation guards, but numeric material values are absent.",
            "status": "COMPOSITION_MATRIX_SCHEMA_CREATED_NOT_SCORE_READY",
        },
        {
            **row_base(ts),
            "decision_id": "DEC3651_3_next",
            "decision": "Next target is weak-field source Hamiltonian/GM calibration: derive how Q_A^X enters Newtonian source mass and PPN residuals or keep a bounded source-calibration vector.",
            "status": "WEAK_FIELD_SOURCE_HAMILTONIAN_NEXT",
        },
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **row_base(ts),
            "status": "MATTER_SENSITIVITY_LAW_DERIVED_COMPOSITION_SCHEMA_NONCLAIM",
            "summary": "3651 derives the material/source sensitivity law and EM Coulomb binding row, then stages a nonclaim composition matrix for WEP/R10/PPN/orbital tests.",
            "claim_ceiling": "no material-sensitivity zero theorem, WEP, R10, PPN, orbital, local-GR/Newton, or source-calibration pass is claimed",
            "useful_result": "The coupling branch now has a concrete source-charge vector Q_A^X and a formula for B_A^EM instead of only a missing-composition label.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **row_base(ts),
            "next_id": "NEXT3651_0",
            "target_doc": "3652-Y5-R2FR-weak-field-source-Hamiltonian-GM-calibration-or-source-vector-bound.md",
            "target_script": "scripts/Y5_R2FR_3652_weak_field_source_Hamiltonian_GM_calibration_or_source_vector_bound.py",
            "objective": "derive how the matter/source charge vector enters Newtonian source mass, fitted GM, PPN residuals, and orbital dynamics; if unsigned, create a bounded source-calibration residual vector",
            "success_gate": "either source Hamiltonian/GM calibration is parent-signed, or source-calibration vector rows have units, source paths, PPN/orbital/WEP links, and no-cancellation guards",
        }
    ]


def write_doc(sources, theorem, sensitivities, schema, projections, decision_rows, status, next_target) -> None:
    lines = [
        "# 3651 - Matter representation source sensitivity or composition matrix row",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The useful forward step is that the composition problem now has a formula. The source charge vector is `Q_A^X = partial ln M_A^eff / partial Xhat`; its leading EM channel is `B_A^EM = partial ln M_A / partial ln alpha_EM ~= E_C/(M_A c^2)` with `E_C=a_C Z(Z-1)A^(-1/3)` before isotope/mixture sourcing.",
        "",
        "If matter labels, current/source measure, and binding data are fixed representation or quotient-owned data, this matrix can theorem-zero. Current MTS does not yet sign that parent clause, so the matrix is staged as nonclaim evidence plumbing rather than a WEP/R10 pass.",
        "",
        "## Theorem rows",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: `{row['status']}` — {row['result']}")
    lines.extend(["", "## Sensitivity rows"])
    for row in sensitivities:
        lines.append(f"- `{row['row_id']}`: `{row['symbol']}` — {row['current_status']}")
    lines.extend(["", "## Composition schema rows"])
    for row in schema:
        lines.append(f"- `{row['schema_id']}`: `{row['object']}` — {row['current_status']}")
    lines.extend(["", "## Projection rows"])
    for row in projections:
        lines.append(f"- `{row['projection_id']}`: `{row['arena']}` — {row['current_status']}")
    lines.extend(["", "## Decisions"])
    for row in decision_rows:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` — {row['decision']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
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


def validate(ts, output_paths, sources, theorem, sensitivities, schema, projections, decision_rows, status, next_target):
    rows = []

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

    add("VAL3651_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3651_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3651_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3651 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3651_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3651_4_QA_law", any("partial ln M_A^eff" in row["mathematical_form"] for row in theorem), "Q_A^X sensitivity law present")
    add("VAL3651_5_EM_binding", any("E_C=a_C Z(Z-1)A^(-1/3)" in row["mathematical_form"] for row in theorem), "Coulomb EM binding formula present")
    add("VAL3651_6_common_matrix", any("DeltaQ_AB^X" in row["mathematical_form"] and "alpha_X(lambda)" in row["mathematical_form"] for row in theorem), "WEP/R10 common source-test matrix present")
    add("VAL3651_7_countermodel_live", any(row["status"] == "COUNTERMODEL_LIVE" for row in theorem), "material countermodel retained")
    add("VAL3651_8_verdict_unsigned", any(row["status"] == "FAIL_CURRENT_CLAIM_MATTER_SENSITIVITY_UNSIGNED" for row in theorem), "matter sensitivity zero not claimed")
    required_symbols = {"Q_A_X", "B_A_EM", "E_C", "DeltaQ_AB_X", "Q_source_X", "tau_WEP", "tau_R10", "tau_PPN", "tau_orbital", "q_matter_source_abs"}
    add("VAL3651_9_sensitivity_rows_complete", required_symbols.issubset({row["symbol"] for row in sensitivities}), "sensitivity/tau rows complete")
    required_schema = {"material_A", "test_body_A", "test_body_B", "source_body_S", "DeltaQ_AB_X", "Q_source_X_Q_test_X", "composition_no_cancellation_guard"}
    add("VAL3651_10_schema_complete", required_schema.issubset({row["object"] for row in schema}), "composition schema rows complete")
    required_proj = {"MICROSCOPE_WEP", "R10_short_range", "PPN_source_calibration", "orbital_source_calibration", "clock_crosscheck", "EM_stress_material"}
    add("VAL3651_11_projection_rows_complete", required_proj.issubset({row["arena"] for row in projections}), "WEP/R10/PPN/orbital/clock/EM projections complete")
    add("VAL3651_12_tau_links", all(row["tau_domain_link"] for row in sensitivities), "every sensitivity row has a tau/domain link or formula note")
    add("VAL3651_13_no_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in sensitivities + schema + projections), "no 3651 rows score-ready")
    generated = sources + theorem + sensitivities + schema + projections + decision_rows + status + next_target
    add("VAL3651_14_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3651_15_no_cancellation", any(row["object"] == "composition_no_cancellation_guard" and "absolute envelope" in row["definition"] for row in schema), "composition no-cancellation guard present")
    add("VAL3651_16_status_honest", status[0]["status"] == "MATTER_SENSITIVITY_LAW_DERIVED_COMPOSITION_SCHEMA_NONCLAIM", "status keeps composition rows nonclaim")
    doc_text = read_text(DOC)
    add("VAL3651_17_doc_written", "Q_A^X" in doc_text and "B_A^EM" in doc_text and "Current MTS does not yet sign" in doc_text, "doc records formula and caveat")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3651*", "3651-Y5-R2FR-*", "Y5_R2FR_3651_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3651_18_no_formalization_leak", not leaks, "no 3651 checkpoint files in formalization-workbench")
    add("VAL3651_19_next_target", next_target[0]["target_doc"].startswith("3652-") and "source-Hamiltonian" in next_target[0]["target_doc"], "3652 source Hamiltonian target selected")
    return rows


def main() -> int:
    ts = now()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    theorem = theorem_rows(ts)
    sensitivities = sensitivity_rows(ts)
    schema = composition_schema_rows(ts)
    projections = projection_rows(ts)
    decision_rows = decisions(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3651_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_R2FR_3651_MATTER_SENSITIVITY_THEOREM_ATTEMPT.csv",
        "sensitivities": RESIDUALS / "P8_Y5_R2FR_3651_MATERIAL_SENSITIVITY_ROWS.csv",
        "schema": RESIDUALS / "P8_Y5_R2FR_3651_COMPOSITION_MATRIX_SCHEMA_ROWS.csv",
        "projections": RESIDUALS / "P8_Y5_R2FR_3651_PROJECTION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3651_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3651_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3651_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3651_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["sensitivities"], sensitivities)
    write_csv(outputs["schema"], schema)
    write_csv(outputs["projections"], projections)
    write_csv(outputs["decisions"], decision_rows)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, theorem, sensitivities, schema, projections, decision_rows, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, theorem, sensitivities, schema, projections, decision_rows, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3651 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3651 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
