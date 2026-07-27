from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3730"
BRANCH_ID = "MTS_R2FR_Y5_COUPLING_SOURCE_NORM_DERIVATION_HUNT_3730"
DOC = ROOT / "3730-Y5-R2FR-coupling-source-norm-derivation-hunt.md"

DOC_3729 = ROOT / "3729-Y5-R2FR-Xiloc-to-local-arena-response-map.md"
NEXT_3729 = RESIDUALS / "P8_Y5_R2FR_3729_NEXT_TARGET.csv"
DOC_1027 = ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md"
DOC_1032 = ROOT / "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md"
DOC_1035 = ROOT / "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md"
HEURISTIC_00 = ROOT / "00-martin-fork-heuristics-private.md"
CFC943 = RESIDUALS / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv"
SWA951 = RESIDUALS / "P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv"
MMA955 = RESIDUALS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv"


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
        ("doc_3729", DOC_3729, "RESPONSE_MAP_CONTRACT_READY", "3729 response inequality contract"),
        ("next_3729", NEXT_3729, "3730-Y5-R2FR-coupling-source-norm-derivation-hunt.md", "3729 handoff to coupling source norms"),
        ("doc_1027", DOC_1027, "qbar_XT=0/J_X=0", "qbar_XT source-zero and bounded coupling split"),
        ("doc_1032", DOC_1032, "finite `c_g/tau_R10/tau_PPN` branch", "finite c_g/tau acquisition runner"),
        ("doc_1035", DOC_1035, "alpha_X = K_X^R10 beta_s beta_t", "R10 source-test product law"),
        ("cfc943", CFC943, "ordinary matter action is a functor", "coframe/matter functor coupling contract"),
        ("swa951", SWA951, "countermodel_blocks_unconditional_theorem", "Ward/source-current countermodel"),
        ("mma955", MMA955, "strong_clean_principle", "minimal matter action lemma"),
        ("heuristic_00", HEURISTIC_00, "Poynting", "Martin fork heuristic keeping EM/Poynting route open"),
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


def derivation_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DER3730_0_parent_current",
            "J_X := delta_X S_parent = delta_X S_matter + delta_X S_boundary + delta_X S_marker + delta_X S_nonH",
            "The source norm sigma_A must come from a parent variation/current, not from a fitted arena knob.",
            "DERIVED_DEFINITION",
            "parent action, variation direction X, boundary/current split",
        ),
        (
            "DER3730_1_sigma_envelope",
            "sigma_A <= ||Pi_A J_X|| + ||tail_A|| <= sum_i ||component_i,A||",
            "A no-cancellation absolute envelope is the safe finite-coupling route for every local arena.",
            "DERIVED_BOUND_CONTRACT",
            "component bounds or theorem-zero rows for geometry, marker, non-Hilbert, support, boundary tails",
        ),
        (
            "DER3730_2_beta_matrix_norm",
            "beta_A=sqrt(lambda_max(B_A^T W_A B_A)) for finite response matrices, or beta_A=||B_A||_{H_to_OA}",
            "The observable response norm is computable from the arena linearized readout map; it is not a new physical constant.",
            "DERIVED_OPERATOR_NORM_CONTRACT",
            "arena observable map B_A and norm/weight matrix W_A",
        ),
        (
            "DER3730_3_3729_response_link",
            "residual_bound_A=beta_A*sigma_A/(Xi_loc-ell_A)+epsilon_A",
            "The 3729 response law becomes scoreable exactly when Xi_loc, sigma_A, beta_A, ell_A, epsilon_A, and bound_A are owned.",
            "DERIVED_LINK_TO_3729",
            "numeric/source-owned values for every factor",
        ),
        (
            "DER3730_4_quotient_zero_branch",
            "If Dq[X]=0, e_obs=Obs_e(q(Phi)), S_matter=Sbar[Psi,e_obs,theta], Lie_X theta=0, and hidden tails vanish, then J_X=0 and sigma_A=0.",
            "The zero-coupling route is real mathematically, but only conditional until the parent action signs all clauses together.",
            "CONDITIONAL_ZERO_THEOREM",
            "q-kernel, observed-coframe descent, matter functor, no-marker theorem, hidden-tail silence",
        ),
        (
            "DER3730_5_R10_product_law",
            "alpha_X(lambda)=K_X^R10(lambda) beta_source(lambda) beta_test(lambda)+epsilon_tail(lambda)",
            "The R10 coupling is a source-test product; universal c_g normally enters as c_g^2 unless one leg is already inside Qbar_XH.",
            "DERIVED_PRODUCT_GUARD",
            "Z_X, lambda_X, source/test beta rows, profile/harmonic projection, tail envelope",
        ),
        (
            "DER3730_6_EM_Poynting_source",
            "sigma_EM <= ||Pi_EM delta_X(Hodge/constitutive/stress/Poynting balance)|| + ||tail_EM||",
            "The Poynting route is not discarded: it is converted into a gateable source-current/observable-response problem.",
            "ROUTE_OPEN_CONTRACT",
            "parent Hodge/constitutive variation and EM observable map",
        ),
    ]
    return [
        {
            **base(ts),
            "derivation_id": derivation_id,
            "formula_or_clause": formula,
            "meaning": meaning,
            "status": status,
            "missing_for_numeric_or_claim": missing,
            "claim_allowed": False,
        }
        for derivation_id, formula, meaning, status, missing in rows
    ]


def route_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "ROUTE3730_0_zero_sigma",
            "sigma_A=0",
            "quotient-zero branch",
            "qbar_XT/J_X conditional theorem from 1027 plus 943 coframe/matter descent",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "not ready for 3729",
        ),
        (
            "ROUTE3730_1_finite_sigma",
            "sigma_A <= |c_g tau_A|+|b_dis tau_dis,A|+sum|b_marker s_marker,A|+|q_nonH,A|+|Delta_W,A|+|boundary_A|",
            "finite no-cancellation source envelope",
            "1027/1032 bounded qbarXT and finite c_g/tau acquisition route",
            "SCHEMA_READY_VALUES_MISSING",
            "not ready for 3729",
        ),
        (
            "ROUTE3730_2_beta_matrix",
            "beta_A=sqrt(lambda_max(B_A^T W_A B_A))",
            "finite observable response norm",
            "new 3730 operator-norm contract feeding the 3729 beta_A column",
            "DERIVED_SCHEMA_VALUES_MISSING",
            "not ready for 3729",
        ),
        (
            "ROUTE3730_3_R10_product",
            "sigma_R10 or alpha_R10 uses K_X^R10 beta_source beta_test + epsilon_tail",
            "source-test product branch",
            "1035 Green-kernel/source-test product law",
            "DERIVED_PRODUCT_FORM_NUMERICALLY_BLOCKED",
            "not ready for 3729",
        ),
        (
            "ROUTE3730_4_EM_Poynting",
            "sigma_EM from Hodge/constitutive/stress/Poynting variation; beta_EM from D O_Poynting",
            "EM/Poynting branch",
            "3729 arena plus Martin heuristic kept as a formal route",
            "ROUTE_OPEN_PARENT_INPUTS_MISSING",
            "not ready for 3729",
        ),
    ]
    return [
        {
            **base(ts),
            "route_id": route_id,
            "quantity_or_formula": formula,
            "route": route,
            "source_basis": basis,
            "current_status": status,
            "readiness": readiness,
            "claim_allowed": False,
        }
        for route_id, formula, route, basis, status, readiness in rows
    ]


def arena_coupling_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("R10_short_range", "sigma_R10 from K_X^R10 beta_source beta_test plus retained tails", "beta_R10 from alpha/torque readout normalization", "K_X,Z_X,lambda_X,beta_source,beta_test,profile,tail"),
        ("PPN_solar_system", "sigma_PPN from c_g/b_dis/tail source current projected into weak-field metric equations", "beta_PPN from PPN response matrix M_PPN", "gauge, profile, M_gamma/M_beta, c_g or zero theorem, disformal split"),
        ("clock_redshift", "sigma_clock from marker/constants/time-readout variation", "beta_clock from frequency/redshift observable derivative", "clock material constants, no-marker theorem or b_A/b_alpha bounds"),
        ("orbital_dynamics", "sigma_orbit from source normalization, measured GM calibration, and boundary/support tails", "beta_orbit from orbit/range/timing response matrix", "GM calibration, ephemeris observable map, support/boundary rows"),
        ("EM_Poynting_waves", "sigma_EM from Hodge/constitutive/Poynting-balance variation", "beta_EM from Maxwell stress/Poynting observable map", "parent Hodge rule, constitutive law, EM stress-energy/source-current map"),
        ("Newton_limit", "sigma_Newton from Poisson-source and measured-G normalization residual", "beta_Newton from acceleration/potential residual map", "left-hand EH/Newton limit, G calibration, source-side mass current"),
    ]
    return [
        {
            **base(ts),
            "arena": arena,
            "sigma_A_route": sigma_route,
            "beta_A_route": beta_route,
            "missing_for_3729": missing,
            "current_status": "ROUTE_DERIVED_VALUES_MISSING",
            "ready_for_3729": False,
            "claim_allowed": False,
        }
        for arena, sigma_route, beta_route, missing in rows
    ]


def runner_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "runner_id": "RUN3730_0_coupling_hunt",
        "source_current_formula_ready": True,
        "sigma_envelope_formula_ready": True,
        "beta_matrix_formula_ready": True,
        "zero_branch_parent_signed": False,
        "finite_numeric_values_ready": False,
        "em_poynting_route_open": True,
        "status": "CONTRACT_ADVANCED_NUMERIC_VALUES_MISSING",
        "next_numeric_or_derivation_bottleneck": "parent J_X current and arena B_A/W_A response matrices",
        "claim_allowed": False,
    }]


def refusal_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("REF3730_0_parent_JX", "J_X", "missing parent-owned source current", "derive delta_X S_parent including matter, boundary, marker, and non-Hilbert tails"),
        ("REF3730_1_zero_signature", "sigma_A=0", "zero branch not parent-signed", "close q-kernel, observed coframe, matter functor, no-marker, and hidden-tail clauses together"),
        ("REF3730_2_finite_components", "finite sigma_A", "component values missing", "source c_g, b_dis, b_A, b_alpha, q_nonH, support and boundary rows with units"),
        ("REF3730_3_beta_matrix", "beta_A", "observable response matrices missing", "derive B_A and W_A for each arena, then compute singular/eigenvalue norm"),
        ("REF3730_4_R10_product", "R10 beta_source beta_test", "R10 product inputs missing", "derive K_X, Z_X, lambda_X, beta_source, beta_test, profile and tail envelope"),
        ("REF3730_5_EM_Poynting", "EM/Poynting", "Hodge/constitutive variation missing", "derive the parent EM observable map and Poynting-balance source current"),
    ]
    return [
        {
            **base(ts),
            "refusal_id": refusal_id,
            "quantity": quantity,
            "reason": reason,
            "required_fix": fix,
            "claim_allowed": False,
        }
        for refusal_id, quantity, reason, fix in rows
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3730_0_real_progress",
            "COUPLING_BOTTLENECK_SPLIT_INTO_SIGMA_AND_BETA",
            "The framework no longer has a vague coupling gap: sigma_A is the parent source-current norm and beta_A is an arena response matrix norm.",
        ),
        (
            "DEC3730_1_best_route",
            "ATTACK_PARENT_JX_AND_RESPONSE_MATRICES_NEXT",
            "The fastest route to local-GR/Newton testing is not another bound table; it is deriving J_X plus B_A/W_A for at least one arena.",
        ),
        (
            "DEC3730_2_R10_warning",
            "KEEP_SOURCE_TEST_PRODUCT_LAW",
            "R10 finite exchange is product-shaped, so linear c_g shortcuts are rejected unless one leg is explicitly packed into the source normalization.",
        ),
        (
            "DEC3730_3_EM_route",
            "KEEP_EM_POYNTING_AS_GATEABLE_BRANCH",
            "Poynting/vector-wave intuition survives as a formal response arena but still needs parent Hodge/constitutive variation.",
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
        ("CG3730_0_sources", "PASS_NONCLAIM", "source trail exists for prior coupling work"),
        ("CG3730_1_JX", "BLOCKED", "parent J_X current is not owned numerically/theorem-zero"),
        ("CG3730_2_zero", "BLOCKED", "zero branch needs parent-signed quotient/matter/no-marker/hidden-tail chain"),
        ("CG3730_3_sigma", "BLOCKED", "finite sigma_A component envelope lacks numeric/source-owned rows"),
        ("CG3730_4_beta", "BLOCKED", "arena B_A/W_A response matrices are not supplied"),
        ("CG3730_5_3729_feed", "BLOCKED", "3729 response runner cannot be filled from 3730 yet"),
        ("CG3730_6_claim", "BLOCKED", "no local-GR/Newton/EM/R10/PPN/clock/orbit claim allowed"),
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
        "status_id": "STATUS3730_0",
        "status": "COUPLING_SOURCE_NORM_CONTRACT_ADVANCED_VALUES_MISSING",
        "summary": "3730 derives the sigma_A/beta_A split that 3729 needs. It preserves quotient-zero, finite-coupling, R10 product, and EM/Poynting routes, but no arena is score-ready until parent J_X and response matrices are supplied.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3730_0",
        "target_doc": "3731-Y5-R2FR-parent-JX-current-and-arena-response-matrix.md",
        "target_script": "scripts/Y5_R2FR_3731_parent_JX_current_and_arena_response_matrix.py",
        "objective": "attempt the parent J_X current derivation and write the finite B_A/W_A response-matrix template for one or more arenas",
        "success_gate": "at least one arena has a source-current formula and response-matrix norm route that can feed sigma_A and beta_A into 3729",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3730*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    derivation_text = read_text(paths["derivations"])
    route_text = read_text(paths["routes"])
    arenas = parse_csv(paths["arena_couplings"])
    runner = parse_csv(paths["runner"])[0]
    claim_gates = parse_csv(paths["claim_gates"])
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("JX_formula", "parent J_X formula written", "J_X := delta_X S_parent" in derivation_text),
        ("beta_matrix", "beta matrix norm written", "beta_A=sqrt(lambda_max" in derivation_text),
        ("R10_product", "R10 source-test product written", "beta_source(lambda) beta_test(lambda)" in derivation_text),
        ("zero_and_finite_routes", "zero and finite routes present", all(token in route_text for token in ["sigma_A=0", "finite no-cancellation source envelope"])),
        ("arena_schema", "six arena coupling rows present", len(arenas) == 6),
        ("em_poynting_included", "EM/Poynting coupling route included", any(row["arena"] == "EM_Poynting_waves" for row in arenas)),
        ("runner_status", "runner records advanced nonnumeric contract", runner["status"] == "CONTRACT_ADVANCED_NUMERIC_VALUES_MISSING"),
        ("claim_gates_blocked", "claim gates blocked except source trail pass", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("next_target_3731", "next target is parent J_X/response matrix", all(token in read_text(paths["next_target"]) for token in ["3731", "J_X", "response-matrix"])),
        ("doc_core_terms", "doc contains coupling split status", all(token in read_text(paths["doc"]) for token in ["sigma_A", "beta_A", "J_X", "EM_Poynting"])),
        ("no_formalization_leak", "no 3730 files in formalization-workbench", len(formal_files) == 0),
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
        "# 3730 - Coupling Source-Norm Derivation Hunt",
        "",
        "## Status",
        "- `COUPLING_SOURCE_NORM_CONTRACT_ADVANCED_VALUES_MISSING`",
        "- Main split: `sigma_A` is the parent source-current norm; `beta_A` is the arena observable response norm.",
        "- This is progress over a vague coupling gap: it tells us exactly what must be derived next.",
        "",
        "## Core Derivation",
    ]
    for row in grouped["derivations"]:
        lines.append(f"- `{row['derivation_id']}` `{row['status']}`: {row['formula_or_clause']} | {row['meaning']}")
    lines.extend(["", "## Route Split"])
    for row in grouped["routes"]:
        lines.append(f"- `{row['route_id']}` `{row['current_status']}`: {row['quantity_or_formula']} | {row['route']}")
    lines.extend(["", "## Arena Couplings"])
    for row in grouped["arena_couplings"]:
        lines.append(f"- `{row['arena']}`: sigma route `{row['sigma_A_route']}`; beta route `{row['beta_A_route']}`")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Refusals"])
    for row in grouped["refusals"]:
        lines.append(f"- `{row['refusal_id']}` `{row['quantity']}`: {row['reason']} | fix: {row['required_fix']}")
    lines.extend(["", "## Next Target"])
    lines.append("- `3731-Y5-R2FR-parent-JX-current-and-arena-response-matrix.md`")
    lines.append("- Objective: derive parent `J_X` and write finite `B_A/W_A` response-matrix templates, so at least one arena can feed real `sigma_A` and `beta_A` into 3729.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3730_SOURCE_REGISTER.csv",
        "derivations": RESIDUALS / "P8_Y5_R2FR_3730_COUPLING_DERIVATION_ROWS.csv",
        "routes": RESIDUALS / "P8_Y5_R2FR_3730_SIGMA_BETA_ROUTE_ROWS.csv",
        "arena_couplings": RESIDUALS / "P8_Y5_R2FR_3730_ARENA_COUPLING_ROWS.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3730_RUNNER_STATUS.csv",
        "refusals": RESIDUALS / "P8_Y5_R2FR_3730_REFUSAL_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3730_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3730_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3730_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3730_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3730_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(ts),
        "derivations": derivation_rows(ts),
        "routes": route_rows(ts),
        "arena_couplings": arena_coupling_rows(ts),
        "runner": runner_rows(ts),
        "refusals": refusal_rows(ts),
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
        raise SystemExit(f"3730 validation failed: {failures}")
    print("wrote 3730 checkpoint: coupling split advanced into sigma_A source norms and beta_A response norms")


if __name__ == "__main__":
    main()
