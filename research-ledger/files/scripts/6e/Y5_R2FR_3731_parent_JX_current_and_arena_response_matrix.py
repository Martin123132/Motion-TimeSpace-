from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3731"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_JX_CURRENT_AND_ARENA_RESPONSE_MATRIX_3731"
DOC = ROOT / "3731-Y5-R2FR-parent-JX-current-and-arena-response-matrix.md"

DOC_3730 = ROOT / "3730-Y5-R2FR-coupling-source-norm-derivation-hunt.md"
NEXT_3730 = RESIDUALS / "P8_Y5_R2FR_3730_NEXT_TARGET.csv"
VALIDATION_3730 = RESIDUALS / "P8_Y5_BRR545_3730_VALIDATION.csv"
CFC943 = RESIDUALS / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv"
SWA951 = RESIDUALS / "P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv"
MMA955 = RESIDUALS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv"
DOC_1035 = ROOT / "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3730", DOC_3730, "ATTACK_PARENT_JX_AND_RESPONSE_MATRICES_NEXT", "3730 selects parent J_X and response matrices"),
        ("next_3730", NEXT_3730, "3731-Y5-R2FR-parent-JX-current-and-arena-response-matrix.md", "3730 handoff target"),
        ("validation_3730", VALIDATION_3730, "next_target_3731", "3730 validation"),
        ("cfc943", CFC943, "ordinary matter action is a functor", "coframe/matter action descent contract"),
        ("swa951", SWA951, "countermodel_blocks_unconditional_theorem", "Ward/source-current countermodel"),
        ("mma955", MMA955, "strong_clean_principle", "minimal matter action lemma"),
        ("doc_1035", DOC_1035, "alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda)", "R10 source-test product law"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(ts),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
        })
    return rows


def current_component_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "JXC3731_0_variational_definition",
            "total_parent_current",
            "delta_X S_parent = int_M sqrt(|g_obs|) J_X delta X + int_boundary Theta_X",
            "J_X = J_geom + J_marker + J_connection + J_nonH + J_boundary + J_EM",
            "defines the source side of sigma_A",
            "MISSING_PARENT_ACTION_DENSITY_AND_X_DIRECTION",
        ),
        (
            "JXC3731_1_visible_geometry",
            "J_geom",
            "J_geom = 1/2 T_matter^{mu nu} H^X_{mu nu}; H^X_{mu nu}:=partial_X g^matter_{mu nu}|branch",
            "quotient branch gives H^X=0; Weyl branch gives H^X_{mu nu}=2 c_g g_{mu nu} and J_geom=c_g T up to stress-sign convention",
            "common fifth-force / PPN / clock / Newton coupling",
            "MISSING_HX_OR_NO_SHADOW_FRAME_THEOREM",
        ),
        (
            "JXC3731_2_disformal_frame",
            "J_dis",
            "J_dis = 1/2 T^{mu nu} D^X_{mu nu}, with D^X_{mu nu}=partial_X(B_g U_mu U_nu + extra frame slots)",
            "zero only if disformal/no-shadow slot is parent-forbidden",
            "preferred-frame, clock, PPN, orbital residuals",
            "MISSING_DISFORMAL_ABSENCE_OR_BOUND",
        ),
        (
            "JXC3731_3_marker_constants",
            "J_marker",
            "J_marker = sum_I (partial_X theta_I) partial L_matter/partial theta_I",
            "zero only if material constants, masses, charges, and clock markers descend through q",
            "clock, WEP, EM constants, material R10 response",
            "MISSING_NO_MARKER_THEOREM_OR_BOUNDS",
        ),
        (
            "JXC3731_4_connection_nonHilbert",
            "J_connection_nonH",
            "J_connection_nonH = delta_X S_nonHilbert + delta_X S_connection + source-support/domain terms",
            "Ward conservation does not kill this without an explicit parent source action",
            "source-normalization, orbital, Newton, local-GR residuals",
            "MISSING_SOURCE_ACTION_AND_DOMAIN_BOUND",
        ),
        (
            "JXC3731_5_boundary",
            "J_boundary",
            "J_boundary = div Theta_X plus corner/support flux projected into arena A",
            "zero only after boundary flux and support-deformation silence are proved",
            "R10 support, orbital/source-normalization, local vacuum plateau",
            "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
        ),
        (
            "JXC3731_6_EM_Hodge_Poynting",
            "J_EM",
            "J_EM = 1/4 (partial_X chi^{mu nu rho sigma}) F_{mu nu}F_{rho sigma} + 1/2 T_EM^{mu nu} H^X_{mu nu} + tail_EM",
            "the Poynting route is a constitutive/Hodge variation plus stress response, not a free Maxwell pass",
            "Maxwell stress, waves, Poynting balance, fine-structure/charge routes",
            "MISSING_PARENT_HODGE_CONSTITUTIVE_RULE",
        ),
    ]
    return [
        {
            **base(ts),
            "component_id": component_id,
            "component": component,
            "variational_formula": formula,
            "branch_effect": branch_effect,
            "feeds": feeds,
            "current_status": "CONTRACT_DERIVED_INPUTS_MISSING",
            "missing_for_claim": missing,
            "claim_allowed": False,
        }
        for component_id, component, formula, branch_effect, feeds, missing in rows
    ]


def sigma_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("R10_short_range", "Pi_R10[J_X]", "sigma_R10 <= |K_X^R10 beta_source beta_test| + |tail_R10|", "K_X^R10,beta_source,beta_test,profile,tail"),
        ("PPN_solar_system", "Pi_PPN[J_X]", "sigma_PPN <= |c_g C_geom| + |b_dis C_dis| + |tail_PPN|", "c_g,b_dis,weak-field profile,gauge,tail"),
        ("clock_redshift", "Pi_clock[J_X]", "sigma_clock <= sum_I |b_I C_clock,I| + |c_g C_geom_clock| + |tail_clock|", "marker constants, clock material sensitivities, frame coupling, tail"),
        ("orbital_dynamics", "Pi_orbit[J_X]", "sigma_orbit <= |Delta_GM| + |source_support| + |boundary| + |tail_orbit|", "measured-GM calibration, support, boundary, source-normalization"),
        ("EM_Poynting_waves", "Pi_EM[J_X]", "sigma_EM <= |delta_X chi| ||F^2|| + |H^X:T_EM|/2 + |tail_EM|", "Hodge/constitutive variation, EM stress projection, tail"),
        ("Newton_limit", "Pi_Newton[J_X]", "sigma_Newton <= |Delta_rho_Poisson| + |Delta_G| + |boundary_Newton|", "Poisson source, G calibration, boundary and left-hand Newton limit"),
    ]
    return [
        {
            **base(ts),
            "arena": arena,
            "projection": projection,
            "sigma_bound_formula": formula,
            "missing_inputs": missing,
            "ready_for_3729": False,
            "claim_allowed": False,
        }
        for arena, projection, formula, missing in rows
    ]


def response_matrix_rows(ts: str) -> list[dict[str, object]]:
    formula = "beta_A^2=lambda_max(G_H^{-1/2} B_A^T W_A B_A G_H^{-1/2})"
    rows = [
        ("R10_short_range", "h_X radial/profile coefficients", "alpha(lambda) or torque harmonic residuals", "W_R10 from alpha/torque covariance", formula, "R10 geometry/profile B_A"),
        ("PPN_solar_system", "weak-field metric/source perturbation coefficients", "gamma-1,beta-1,preferred-frame residual vector", "W_PPN from experimental covariance/bounds", formula, "PPN gauge-fixed response matrix"),
        ("clock_redshift", "local frame/time/material marker perturbation coefficients", "fractional frequency/redshift residuals", "W_clock from clock comparison covariance", formula, "clock/readout response derivative"),
        ("orbital_dynamics", "potential/acceleration/source-normalization perturbation coefficients", "range,timing,perihelion,acceleration residual vector", "W_orbit from ephemeris covariance/bounds", formula, "orbital dynamics sensitivity matrix"),
        ("EM_Poynting_waves", "Hodge/constitutive/stress perturbation coefficients", "Poynting theorem, Maxwell stress, wave-speed/polarization residuals", "W_EM from EM measurement or theorem norm", formula, "EM observable derivative D O_Poynting"),
        ("Newton_limit", "Poisson potential/source perturbation coefficients", "acceleration and potential residuals", "W_Newton from local Newton precision or theorem norm", formula, "Newton-limit acceleration/potential response"),
    ]
    return [
        {
            **base(ts),
            "arena": arena,
            "domain_basis_h": domain_basis,
            "observable_basis_y": observable_basis,
            "weight_matrix_WA": weight_matrix,
            "beta_formula": beta_formula,
            "needed_matrix": needed_matrix,
            "matrix_entries_status": "MISSING_BA_WA_GH_NUMERIC_OR_THEOREM",
            "ready_for_beta": False,
            "claim_allowed": False,
        }
        for arena, domain_basis, observable_basis, weight_matrix, beta_formula, needed_matrix in rows
    ]


def matrix_template_rows(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for arena in ["R10_short_range", "PPN_solar_system", "clock_redshift", "orbital_dynamics", "EM_Poynting_waves", "Newton_limit"]:
        for matrix_name in ["G_H", "B_A", "W_A"]:
            rows.append({
                **base(ts),
                "entry_id": f"ME3731_{arena}_{matrix_name}_template",
                "arena": arena,
                "matrix_name": matrix_name,
                "row_index": "MISSING_ROW",
                "col_index": "MISSING_COL",
                "value": "MISSING_NUMERIC_ENTRY",
                "units": "MISSING_UNITS",
                "source_path": "MISSING_SOURCE_OR_DERIVATION_PATH",
                "source_owned": False,
                "claim_allowed": False,
            })
    return rows


def runner_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "runner_id": "RUN3731_0_JX_BETA_CONTRACT",
        "JX_contract_ready": True,
        "sigma_projection_contract_ready": True,
        "response_matrix_contract_ready": True,
        "matrix_beta_executable": False,
        "source_current_numeric": False,
        "zero_branch_parent_signed": False,
        "status": "JX_AND_RESPONSE_MATRIX_CONTRACT_READY_VALUES_MISSING",
        "feeds_3729": "sigma_A and beta_A columns once parent current and B_A/W_A/G_H matrices are source-owned",
        "claim_allowed": False,
    }]


def theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "THM3731_0_JX_variational_identity",
            "For any local branch coordinate X, delta_X S_parent = int sqrt(|g|) J_X delta X + boundary terms.",
            "This is the parent-owned definition of the coupling source; it replaces fitted coupling talk with a variational object.",
            "DERIVED_IDENTITY",
        ),
        (
            "THM3731_1_matter_frame_current",
            "If matter sees g_m(X), then J_geom = 1/2 T^{mu nu} partial_X g^m_{mu nu}; quotient descent sets this to zero only if partial_X g_m=0 by parent theorem.",
            "This is the exact fork between closure-zero and finite common coupling.",
            "DERIVED_CONDITIONAL",
        ),
        (
            "THM3731_2_response_matrix_norm",
            "With domain Gram G_H and observable weight W_A, beta_A^2=lambda_max(G_H^{-1/2} B_A^T W_A B_A G_H^{-1/2}).",
            "This makes beta_A computable once the arena readout map is written.",
            "DERIVED_OPERATOR_NORM",
        ),
        (
            "THM3731_3_EM_constitutive_current",
            "EM/Poynting residuals require delta_X chi, H^X:T_EM, and tail_EM; ordinary Poynting balance is recovered only if those terms vanish or are bounded.",
            "This keeps Maxwell/EM stress derivable rather than assumed.",
            "ROUTE_OPEN_CONTRACT",
        ),
        (
            "THM3731_4_no_claim_gate",
            "A symbolic J_X and symbolic beta_A cannot pass 3729; both need numeric/source-owned rows or theorem-zero certificates.",
            "Prevents smuggling closure assumptions into local-GR/Newton/Maxwell claims.",
            "ANTI_OVERCLAIM",
        ),
    ]
    return [
        {
            **base(ts),
            "theorem_id": theorem_id,
            "clause": clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for theorem_id, clause, meaning, status in rows
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3731_0_contract_closed",
            "JX_AND_BETA_CONTRACT_READY",
            "The parent-current and arena-response sides now have exact formulas feeding 3729.",
        ),
        (
            "DEC3731_1_no_numeric_claim",
            "NO_ARENA_SCORE_YET",
            "Current rows lack parent-owned H^X, chi_X, marker derivatives, B_A, W_A, and G_H matrices.",
        ),
        (
            "DEC3731_2_best_next",
            "SPECIALIZE_ONE_ARENA_NEXT",
            "The next leap is to pick the least slippery arena and write its B_A/W_A plus source-current specialization; Newton/PPN is the cleanest GR bridge, EM/Poynting is the parallel Maxwell bridge.",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in rows
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    gates = [
        ("CG3731_0_sources", "PASS_NONCLAIM", "source trail exists"),
        ("CG3731_1_JX_identity", "PASS_NONCLAIM", "variational J_X identity written"),
        ("CG3731_2_HX", "BLOCKED", "H^X or quotient-zero/no-shadow theorem missing"),
        ("CG3731_3_EM_chi", "BLOCKED", "delta_X chi/Hodge/constitutive rule missing"),
        ("CG3731_4_markers", "BLOCKED", "marker constants theorem-zero or bounds missing"),
        ("CG3731_5_Bmatrix", "BLOCKED", "B_A/W_A/G_H response matrices missing"),
        ("CG3731_6_3729_feed", "BLOCKED", "no numeric sigma_A or beta_A can feed 3729 yet"),
        ("CG3731_7_claim", "BLOCKED", "no local-GR/Newton/Maxwell/PPN/R10 claim allowed"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate_status": status,
            "required_before_claim": required,
            "claim_allowed": False,
        }
        for gate_id, status, required in gates
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "status_id": "STATUS3731_0",
        "status": "JX_AND_RESPONSE_MATRIX_CONTRACT_READY_VALUES_MISSING",
        "summary": "3731 derives the parent current decomposition and the finite response-matrix norm required for sigma_A and beta_A. It is not score-ready until parent current components and arena matrices are source-owned.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3731_0",
        "target_doc": "3732-Y5-R2FR-first-arena-response-specialization-Newton-PPN-and-EM.md",
        "target_script": "scripts/Y5_R2FR_3732_first_arena_response_specialization_Newton_PPN_and_EM.py",
        "objective": "specialize the 3731 J_X/B_A/W_A contract into the Newton-PPN bridge and EM/Poynting bridge, choosing exact observable bases and first response matrices",
        "success_gate": "Newton/PPN and EM/Poynting have concrete basis vectors, matrix-entry schemas, and theorem-zero-or-bound clauses ready for future numeric/source rows",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3731*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    components = parse_csv(paths["components"])
    response = parse_csv(paths["response"])
    matrix = parse_csv(paths["matrix_template"])
    theorem_text = read_text(paths["theorems"])
    doc_text = read_text(paths["doc"])
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("component_schema", "seven J_X components present", len(components) == 7),
        ("J_geom_formula", "visible geometry current formula present", any("1/2 T_matter" in row["variational_formula"] for row in components)),
        ("EM_current_formula", "EM Hodge/Poynting current present", any(row["component"] == "J_EM" and "partial_X chi" in row["variational_formula"] for row in components)),
        ("sigma_schema", "six sigma projection rows present", len(parse_csv(paths["sigma"])) == 6),
        ("response_schema", "six response matrix rows present", len(response) == 6),
        ("beta_formula", "beta matrix norm present", all("lambda_max" in row["beta_formula"] for row in response)),
        ("matrix_template", "G/B/W templates present for each arena", len(matrix) == 18),
        ("theorems", "J_X and beta theorems present", all(token in theorem_text for token in ["delta_X S_parent", "beta_A^2", "EM/Poynting"])),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3732", "next target is first arena specialization", all(token in read_text(paths["next_target"]) for token in ["3732", "Newton", "EM"])),
        ("doc_core_terms", "doc contains current-response contract", all(token in doc_text for token in ["J_X", "beta_A", "B_A", "EM_Poynting"])),
        ("no_formalization_leak", "no 3731 files in formalization-workbench", len(formal_files) == 0),
    ]
    return [
        {
            **base(ts),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3731 - Parent J_X Current and Arena Response Matrix",
        "",
        "## Status",
        "- `JX_AND_RESPONSE_MATRIX_CONTRACT_READY_VALUES_MISSING`",
        "- Parent source current: `delta_X S_parent = int sqrt(|g_obs|) J_X delta X + int_boundary Theta_X`.",
        "- Arena response norm: `beta_A^2=lambda_max(G_H^{-1/2} B_A^T W_A B_A G_H^{-1/2})`.",
        "- These formulas feed `sigma_A` and `beta_A` into the 3729 response inequality, but no local-GR/Newton/Maxwell claim is allowed yet.",
        "",
        "## Parent Current Components",
    ]
    for row in grouped["components"]:
        lines.append(f"- `{row['component_id']}` `{row['component']}`: {row['variational_formula']} | missing: {row['missing_for_claim']}")
    lines.extend(["", "## Sigma Projection Rows"])
    for row in grouped["sigma"]:
        lines.append(f"- `{row['arena']}`: {row['sigma_bound_formula']} | missing: {row['missing_inputs']}")
    lines.extend(["", "## Response Matrix Rows"])
    for row in grouped["response"]:
        lines.append(f"- `{row['arena']}`: domain `{row['domain_basis_h']}` -> observable `{row['observable_basis_y']}` with `{row['beta_formula']}`")
    lines.extend(["", "## Theorem Rows"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['clause']} | {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` `{row['gate_status']}` | {row['required_before_claim']}")
    lines.extend(["", "## Next Target"])
    lines.append("- `3732-Y5-R2FR-first-arena-response-specialization-Newton-PPN-and-EM.md`")
    lines.append("- Objective: specialize the `J_X/B_A/W_A` contract into Newton/PPN and EM/Poynting first-arena response matrices.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3731_SOURCE_REGISTER.csv",
        "components": RESIDUALS / "P8_Y5_R2FR_3731_PARENT_CURRENT_COMPONENTS.csv",
        "sigma": RESIDUALS / "P8_Y5_R2FR_3731_SIGMA_PROJECTION_ROWS.csv",
        "response": RESIDUALS / "P8_Y5_R2FR_3731_RESPONSE_MATRIX_ROWS.csv",
        "matrix_template": RESIDUALS / "P8_Y5_R2FR_3731_MATRIX_ENTRIES_TEMPLATE.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3731_RUNNER_STATUS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3731_THEOREM_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3731_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3731_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3731_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3731_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3731_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(ts),
        "components": current_component_rows(ts),
        "sigma": sigma_rows(ts),
        "response": response_matrix_rows(ts),
        "matrix_template": matrix_template_rows(ts),
        "runner": runner_rows(ts),
        "theorems": theorem_rows(ts),
        "decisions": decision_rows(ts),
        "claim_gates": claim_gate_rows(ts),
        "status": status_rows(ts),
        "next_target": next_target_rows(ts),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(ts, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3731 validation failed: {failures}")
    print("wrote 3731 checkpoint: parent J_X current and response-matrix contract ready, values missing")


if __name__ == "__main__":
    main()
