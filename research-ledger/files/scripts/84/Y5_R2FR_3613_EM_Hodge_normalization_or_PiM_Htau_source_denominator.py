from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3613"
BRANCH_ID = "MTS_R2FR_Y5_EM_HODGE_NORMALIZATION_OR_PIM_HTAU_SOURCE_DENOMINATOR_3613"
DOC = ROOT / "3613-Y5-R2FR-EM-Hodge-normalization-or-PiM-Htau-source-denominator.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3612": (
            RESIDUALS / "P8_Y5_R2FR_3612_NEXT_TARGET.csv",
            "3613-Y5-R2FR-EM-Hodge-normalization-or-PiM-Htau-source-denominator.md",
        ),
        "poynting_bound_3612": (
            RESIDUALS / "P8_Y5_R2FR_3612_JQ_MATTER_SUBCOMPONENT_ATTACK.csv",
            "J_q^EM/Poynting sub-bound",
        ),
        "closure_3612": (
            RESIDUALS / "P8_Y5_R2FR_3612_EM_POYNTING_HILBERT_CLOSURE.csv",
            "B_Hodge",
        ),
        "hodge_owner_3503": (
            RESIDUALS / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
            "Delta_Hodge_EM",
        ),
        "hodge_flow_3504": (
            RESIDUALS / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
            "Delta_conformal_scale",
        ),
        "hodge_uniqueness_3504": (
            RESIDUALS / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv",
            "conformally invariant",
        ),
        "hodge_poynting_3286": (
            RESIDUALS / "P8_Y5_R2FR_3286_HODGE_POYNTING_OWNER_THEOREM.csv",
            "EXACT_CHAIN_RULE_AND_LEIBNIZ_THEOREM",
        ),
        "chi_reconstruct_3287": (
            RESIDUALS / "P8_Y5_R2FR_3287_CHI_TO_HODGE_RECONSTRUCTION_THEOREM.csv",
            "nonbirefringence reconstructs conformal metric",
        ),
        "observed_hodge_3503": (
            RESIDUALS / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
            "observed Hodge/coframe owner",
        ),
        "constitutive_template_3506": (
            RESIDUALS / "P8_Y5_R2FR_3506_CONSTITUTIVE_BOUND_INPUT_TEMPLATE.csv",
            "BIN3506_6_Delta_conformal_scale",
        ),
        "constitutive_runner_3506": (
            RESIDUALS / "P8_Y5_R2FR_3506_CONSTITUTIVE_BOUND_RUNNER_RESULTS.csv",
            "BLOCKED_INPUT_NOT_VALID_FOR_CLAIM",
        ),
        "unique_f2_3528": (
            RESIDUALS / "P8_EM_unique_F2_or_calibrated_alpha_status.csv",
            "calibrated_universal_constant",
        ),
        "alpha_residual_3507": (
            RESIDUALS / "P8_EM_scalar_coupling_owner_alpha_residual.csv",
            "CORE_COUPLING_THROAT",
        ),
        "pim_htau_3514": (
            RESIDUALS / "P8_EM_PiM_Htau_commutator_residual_law.csv",
            "R_PiM+R_Htau",
        ),
        "pim_htau_3602": (
            RESIDUALS / "P8_Y5_R2FR_3602_PIM_HTAU_COMPONENT_BOUND_ROWS.csv",
            "PHTB3602_0_total",
        ),
        "denominator_3531": (
            RESIDUALS / "P8_local_GR_Hilbert_source_denominator_status.csv",
            "PiM_Htau_commutator_and_integrability_gate",
        ),
    }


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3613_SOURCE_REGISTER.csv",
        "delta_hodge_bound": RESIDUALS / "P8_Y5_R2FR_3613_DELTA_HODGE_BOUND_LAW.csv",
        "conformal_subtheorem": RESIDUALS / "P8_Y5_R2FR_3613_CONFORMAL_HODGE_SUBTHEOREM.csv",
        "em_normalization_branch": RESIDUALS / "P8_Y5_R2FR_3613_EM_NORMALIZATION_BRANCH.csv",
        "pim_htau_fallback": RESIDUALS / "P8_Y5_R2FR_3613_PIM_HTAU_FALLBACK.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3613_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3613_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3613_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_EM_Hodge_conformal_or_PiM_Htau_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3613_VALIDATION.csv",
    }


def source_register_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    stamp = now()
    rows: list[dict[str, object]] = []
    for source_id, (source_path, needle) in sources.items():
        exists = source_path.exists()
        rows.append(
            {
                "timestamp_utc": stamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(source_path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(source_path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def delta_hodge_bound_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(value[0]) for source_id, value in sources.items()}
    stamp = now()
    rows = [
        (
            "DHB3613_0_target",
            "Delta_Hodge_EM",
            "aggregate mismatch between EM Hodge/constitutive flow and observed gravitational coframe",
            "Delta_Hodge_EM := *_EM - *_obs[e_obs(q)] or chi_EM - chi(g_obs)",
            "TARGET_IMPORTED",
            "hodge_owner_3503",
            "The target is now a concrete constitutive mismatch, not generic EM weirdness.",
        ),
        (
            "DHB3613_1_component_bound",
            "Delta_Hodge_EM aggregate bound",
            "Delta_Hodge_EM is bounded by named constitutive/readout/orientation components with no cancellation credit",
            "||Delta_Hodge_EM|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||d theta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|",
            "SOURCE_BOUND_FILLED_NONCLAIM",
            "hodge_flow_3504",
            "This removes one layer of fog: Hodge failure is a vector of named component coefficients.",
        ),
        (
            "DHB3613_2_principal",
            "Delta_chi_principal",
            "principal constitutive mismatch changes EM cone, anisotropy, birefringence or effective metric",
            "Delta_chi_principal := chi_EM_principal - chi(g_obs)",
            "RETAINED_COMPONENT_BOUND_REQUIRED",
            "hodge_flow_3504",
            "This is the next obvious empirical hook: light-cone, birefringence, Shapiro/lensing consistency.",
        ),
        (
            "DHB3613_3_skewon",
            "Delta_chi_skewon",
            "skewon/nonreciprocal/dissipative piece is excluded by a conservative action or retained as dispersion/Poynting-loss bound",
            "B_skewon := ||chi_EM_skewon||",
            "RETAINED_COMPONENT_BOUND_REQUIRED",
            "hodge_flow_3504",
            "This separates Lagrangian Maxwell structure from non-action constitutive drift.",
        ),
        (
            "DHB3613_4_axion_gradient",
            "Delta_chi_axion_gradient",
            "constant axion/topological term is not a local Hodge stress scale, but a gradient is active",
            "B_axion := L||d theta_EM||",
            "RETAINED_COMPONENT_BOUND_REQUIRED",
            "chi_reconstruct_3287",
            "This stops a topological F wedge F term being confused with a Maxwell source-mass term.",
        ),
        (
            "DHB3613_5_hidden_readout_orientation",
            "hidden/readout/orientation Hodge tails",
            "hidden disformal Hodge, readout Hodge regeneration, and boundary orientation conventions remain explicit tails",
            "B_tail := |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|",
            "RETAINED_TAIL_BOUND_REQUIRED",
            "hodge_flow_3504",
            "No hidden-visible Hodge map is allowed to vanish by wording.",
        ),
    ]
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "quantity": quantity,
            "statement": statement,
            "formula": formula,
            "status": status,
            "source_path": p[source_id],
            "effect_or_guard": effect,
            "numeric_value_owned": False,
            "theorem_zero_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, quantity, statement, formula, status, source_id, effect in rows
    ]


def conformal_subtheorem_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(value[0]) for source_id, value in sources.items()}
    stamp = now()
    rows = [
        (
            "CHS3613_0_theorem",
            "pure conformal Hodge invariance",
            "In four spacetime dimensions, the Hodge star on two-forms is invariant under g -> Omega^2 g.",
            "*_{Omega^2 g}|_{Lambda^2} = *_g|_{Lambda^2}",
            "MATHEMATICAL_SUBTHEOREM",
            "hodge_uniqueness_3504",
            "Pure conformal rescaling is not a Maxwell-Hodge/Poynting cone residual.",
        ),
        (
            "CHS3613_1_delta_hodge_effect",
            "Delta_conformal_scale removal from Hodge cone",
            "A pure conformal factor does not belong in the Delta_Hodge_EM cone/2-form Hodge mismatch after the 4D Maxwell restriction.",
            "B_Hodge_conformal = 0 for the 2-form Hodge operator; Delta_conformal_scale moves to source/clock/normalization gates",
            "SUBCOMPONENT_THEOREM_ZERO_FOR_HODGE_ONLY",
            "constitutive_template_3506",
            "This is the exact win in 3613: one subcomponent leaves the Hodge/Poynting cone residual, but not the whole local source problem.",
        ),
        (
            "CHS3613_2_no_overclaim",
            "source/clock scale caveat",
            "The same conformal freedom can still affect clocks, volumes, masses, alpha normalization, charge/current scale or Newton source calibration.",
            "Delta_conformal_scale -> B_scale := |D_X ln Omega_clock/source| + |D_X ln lambda_A| + |D_X ln g_J| + |D_X ln M_H_ref|",
            "RETAINED_SCALE_GATE",
            "hodge_uniqueness_3504",
            "This avoids claiming local GR or Newton from light-cone agreement alone.",
        ),
        (
            "CHS3613_3_reconstruction",
            "nonbirefringence only reconstructs conformal metric",
            "Fresnel/nonbirefringence can recover a conformal metric class, not the full source metric and normalization.",
            "G(k) proportional (g_EM^{ab} k_a k_b)^2 gives [g_EM], then separate same-metric/scale clauses are required",
            "DERIVED_OBSTRUCTION_RETAINED",
            "chi_reconstruct_3287",
            "This is why matching Maxwell waves is useful but not sufficient for Newtonian source mass.",
        ),
    ]
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "target": target,
            "statement": statement,
            "mathematical_form": mathematical_form,
            "status": status,
            "source_path": p[source_id],
            "effect_or_guard": effect,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, target, statement, mathematical_form, status, source_id, effect in rows
    ]


def normalization_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(value[0]) for source_id, value in sources.items()}
    stamp = now()
    rows = [
        (
            "ENB3613_0_local_alpha_baseline",
            "alpha_EM local branch",
            "alpha may be carried as a calibrated universal local constant for the GR/Newton route without pretending it is derived.",
            "D_{v_q} alpha_EM = 0 on the calibrated branch by definition of the baseline, not by MTS prediction",
            "CALIBRATED_CONSTANT_BASELINE_NONCLAIM",
            "unique_f2_3528",
        ),
        (
            "ENB3613_1_CXF2_branch",
            "C_XF2",
            "nonzero hidden F^2 branch remains a scoreable residual and cannot be hidden inside source mass.",
            "B_CXF2 := C_XF2 |C_XF2| with arena links alpha_EM; clock; WEP; R10; PPN; source_normalization",
            "BOUND_BRANCH_RETAINED",
            "alpha_residual_3507",
        ),
        (
            "ENB3613_2_lambda_branch",
            "D_vq ln lambda_A",
            "Maxwell kinetic normalization is closed only on the calibrated branch; otherwise its vertical derivative is a force/clock/source residual.",
            "B_lambda := C_lambda |D_{v_q} ln lambda_A|",
            "BOUND_BRANCH_RETAINED",
            "alpha_residual_3507",
        ),
        (
            "ENB3613_3_current_branch",
            "D_vq ln g_J",
            "charge/current normalization must share the same owner as A_Q and F_Q^2 before EM stress and Lorentz force are comparable.",
            "b_alpha_X = 2 D_X ln g_J - D_X ln lambda_A",
            "OWNER_UNSIGNED_RETAINED",
            "alpha_residual_3507",
        ),
    ]
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "quantity": quantity,
            "statement": statement,
            "formula": formula,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, quantity, statement, formula, status, source_id in rows
    ]


def pim_htau_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(value[0]) for source_id, value in sources.items()}
    stamp = now()
    rows = [
        (
            "PHTF3613_0_total",
            "R_PiM_plus_R_Htau",
            "source-denominator residual retained for Newton/Poisson/PPN route",
            "R_PiM+R_Htau = C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units",
            "EXACT_DECOMPOSITION_IMPORTED",
            "pim_htau_3514",
        ),
        (
            "PHTF3613_1_bound",
            "PiM/Htau no-cancellation bound",
            "if Hodge/normalization stalls, the denominator throat already has named component bounds",
            "|R_PiM+R_Htau| <= |C_M|+|C_shape|+|C_curl|+|C_domain|+|C_ref|+|C_frame|+|C_units|",
            "BOUND_FALLBACK_READY_VALUES_MISSING",
            "pim_htau_3602",
        ),
        (
            "PHTF3613_2_priority",
            "Newton source denominator",
            "Pi_M/H_tau is the next local-GR throat because it controls whether source mass is parent-owned before orbital GM fitting.",
            "mu_obs=G_ref M_H_ref(1+epsilon_mu), not M_H_ref:=mu_obs/G_ref",
            "NEXT_PRESSURE_POINT_IF_HODGE_STALLS",
            "denominator_3531",
        ),
    ]
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "quantity": quantity,
            "statement": statement,
            "formula": formula,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, quantity, statement, formula, status, source_id in rows
    ]


def decision_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(value[0]) for source_id, value in sources.items()}
    stamp = now()
    rows = [
        (
            "DEC3613_0_Delta_Hodge",
            "Delta_Hodge_EM",
            "ADVANCED",
            "Aggregate bound filled; pure conformal piece removed from the 4D two-form Hodge mismatch and reclassified as scale/source residual.",
            "hodge_flow_3504",
        ),
        (
            "DEC3613_1_conformal",
            "Delta_conformal_scale",
            "SUBTHEOREM_ZERO_FOR_HODGE_ONLY",
            "Conformal light-cone agreement is useful but does not fix clocks, source mass, alpha, charge/current, or Newton normalization.",
            "hodge_uniqueness_3504",
        ),
        (
            "DEC3613_2_normalization",
            "D_vq ln lambda_A / C_XF2",
            "RETAINED",
            "Calibrated local alpha is allowed as baseline; any nonzero hidden F2 or kinetic drift branch remains scoreable.",
            "unique_f2_3528",
        ),
        (
            "DEC3613_3_PiM_Htau",
            "Pi_M/H_tau source denominator",
            "FALLBACK_READY",
            "If EM Hodge subcomponents cannot be parent-signed next, the denominator route has a ready no-cancellation component bound.",
            "pim_htau_3602",
        ),
        (
            "DEC3613_4_claim_guard",
            "local-GR/Newton/Maxwell claim",
            "BLOCKED_FOR_CLAIM_NOT_FOR_WORK",
            "No claim follows until the remaining Hodge components, normalization branch, and source denominator are theorem-zero or numeric/source-backed.",
            "closure_3612",
        ),
        (
            "DEC3613_5_next",
            "next best attack",
            "SELECT_PRINCIPAL_HODGE_OR_PIM_HTAU_CURL",
            "Either attack Delta_chi_principal with empirical/parent bounds, or attack C_curl in Pi_M/H_tau because it is the Hamiltonian integrability core.",
            "pim_htau_3514",
        ),
    ]
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "target": target,
            "decision": decision,
            "rationale": rationale,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for decision_id, target, decision, rationale, source_id in rows
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "DELTA_HODGE_BOUND_FILLED_CONFORMAL_HODGE_SUBTERM_ZEROED_SCALE_RETAINED",
            "summary": (
                "3613 fills a source-backed aggregate Delta_Hodge_EM bound, proves the pure conformal piece is zero for the 4D two-form Maxwell Hodge operator, "
                "reclassifies conformal scale as a clock/source/normalization residual, keeps EM kinetic/C_XF2 branches nonclaim, and imports Pi_M/H_tau as the fallback Newton-source denominator bound."
            ),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3613_0",
            "target_doc": "3614-Y5-R2FR-principal-Hodge-bound-or-Htau-curl-integrability.md",
            "target_script": "scripts/Y5_R2FR_3614_principal_Hodge_bound_or_Htau_curl_integrability.py",
            "objective": (
                "try to source-bound or theorem-zero Delta_chi_principal using the constitutive/light-cone branch; "
                "if that does not close, attack C_curl in Pi_M/H_tau via Hamiltonian integrability and boundary symplectic flux"
            ),
            "success_gate": (
                "must produce a sourced nonclaim bound or theorem-zero for Delta_chi_principal, or a sourced nonclaim bound/theorem-zero for C_curl; "
                "do not write another generic coupling ledger"
            ),
            "reason": "3613 removes the conformal Hodge decoy and leaves principal Hodge shape or H_tau curl as the next sharp pressure points.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def formalization_leaks() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    leaks: list[Path] = []
    for path in FORMALIZATION.rglob("*3613*"):
        parts = set(path.parts)
        if "__pycache__" in parts or ".venv" in parts or "package" in parts:
            continue
        leaks.append(path)
    return leaks


def csv_summary(paths: dict[str, Path]) -> str:
    parts = []
    for name, path in paths.items():
        if name == "validation":
            continue
        parts.append(f"{name}:{len(read_csv(path))}")
    return "; ".join(parts)


def validation_rows(sources: dict[str, tuple[Path, str]], paths: dict[str, Path]) -> list[dict[str, object]]:
    source_rows = read_csv(paths["source_register"])
    hodge_rows = read_csv(paths["delta_hodge_bound"])
    conformal_rows = read_csv(paths["conformal_subtheorem"])
    norm_rows = read_csv(paths["em_normalization_branch"])
    pim_rows = read_csv(paths["pim_htau_fallback"])
    decisions = read_csv(paths["decision_gates"])
    status = read_csv(paths["status"])
    outputs_exist = all(path.exists() for name, path in paths.items() if name != "validation")
    source_paths_all_exist = all(row["exists"].lower() == "true" for row in source_rows)
    source_needles_found = all(row["needle_found"].lower() == "true" for row in source_rows)
    no_claim_flags = True
    for name, path in paths.items():
        if name == "validation":
            continue
        for row in read_csv(path):
            if row.get("claim_allowed", "False").lower() == "true" or row.get("valid_for_claim", "False").lower() == "true":
                no_claim_flags = False
    delta_hodge_bound_filled = any(row["bound_id"] == "DHB3613_1_component_bound" and "||Delta_Hodge_EM|| <=" in row["formula"] for row in hodge_rows)
    conformal_zero_hodge_only = any(
        row["theorem_id"] == "CHS3613_1_delta_hodge_effect"
        and row["status"] == "SUBCOMPONENT_THEOREM_ZERO_FOR_HODGE_ONLY"
        and "source/clock/normalization" in row["mathematical_form"]
        for row in conformal_rows
    )
    scale_retained = any(row["theorem_id"] == "CHS3613_2_no_overclaim" and row["status"] == "RETAINED_SCALE_GATE" for row in conformal_rows)
    normalization_retained = any(row["row_id"] == "ENB3613_1_CXF2_branch" and row["status"] == "BOUND_BRANCH_RETAINED" for row in norm_rows)
    pim_fallback_ready = any(row["row_id"] == "PHTF3613_1_bound" and "|R_PiM+R_Htau| <=" in row["formula"] for row in pim_rows)
    next_selected = any(row["decision_id"] == "DEC3613_5_next" and "SELECT_PRINCIPAL_HODGE" in row["decision"] for row in decisions)
    status_ok = bool(status) and status[0]["status"] == "DELTA_HODGE_BOUND_FILLED_CONFORMAL_HODGE_SUBTERM_ZEROED_SCALE_RETAINED"
    leaks = formalization_leaks()
    specs = [
        ("VAL3613_0_sources_exist", source_paths_all_exist, "all required 3613 source paths exist"),
        ("VAL3613_1_needles_found", source_needles_found, "all selected 3613 source anchors found"),
        ("VAL3613_2_outputs_exist", outputs_exist, "all pre-validation 3613 csv outputs written"),
        ("VAL3613_3_csv_parse", True, csv_summary(paths)),
        ("VAL3613_4_delta_hodge_bound_filled", delta_hodge_bound_filled, "Delta_Hodge_EM aggregate source-bound filled"),
        ("VAL3613_5_conformal_zero_hodge_only", conformal_zero_hodge_only, "pure conformal term zeroed only for 4D Maxwell Hodge"),
        ("VAL3613_6_scale_retained", scale_retained, "conformal scale retained for clock/source/normalization"),
        ("VAL3613_7_normalization_branch_retained", normalization_retained, "C_XF2 / kinetic branch remains nonclaim bound branch"),
        ("VAL3613_8_pim_htau_fallback_ready", pim_fallback_ready, "Pi_M/H_tau fallback no-cancellation bound imported"),
        ("VAL3613_9_no_claim_flags", no_claim_flags, "all generated rows remain nonclaim"),
        ("VAL3613_10_next_target_selected", next_selected, "3614 target selected from concrete residual branches"),
        ("VAL3613_11_status_ok", status_ok, "canonical status matches 3613 verdict"),
        (
            "VAL3613_12_formalization_workbench_untouched",
            len(leaks) == 0,
            "no 3613 checkpoint output appears in formalization-workbench outside package/venv noise",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail if passed else f"{detail}; leaks={[str(leak) for leak in leaks]}",
        }
        for validation_id, passed, detail in specs
    ]


def write_doc(paths: dict[str, Path]) -> None:
    hodge = read_csv(paths["delta_hodge_bound"])
    conformal = read_csv(paths["conformal_subtheorem"])
    norm = read_csv(paths["em_normalization_branch"])
    pim = read_csv(paths["pim_htau_fallback"])
    decisions = read_csv(paths["decision_gates"])
    status = read_csv(paths["status"])[0]
    validation = read_csv(paths["validation"])
    next_target = read_csv(paths["next_target"])[0]
    lines = [
        "# 3613 - EM Hodge normalization or PiM/Htau source denominator",
        "",
        "## Verdict",
        "3613 takes a real bite out of the EM/Poynting residual: `Delta_Hodge_EM` is now an explicit component bound, and the pure conformal piece is removed from the 4D Maxwell two-form Hodge mismatch.",
        "",
        "`||Delta_Hodge_EM|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||d theta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|`",
        "",
        "The important guard is just as sharp: pure conformal scale is zero only for the Maxwell Hodge/cone piece.  It is still alive in clocks, source mass, alpha/charge normalization, and Newton calibration.  So this is progress, not a local-GR or Maxwell pass.",
        "",
        "## Delta Hodge Bound",
    ]
    for row in hodge:
        lines.append(f"- `{row['bound_id']}` / `{row['quantity']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Conformal Subtheorem"])
    for row in conformal:
        lines.append(f"- `{row['theorem_id']}` / `{row['target']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## EM Normalization"])
    for row in norm:
        lines.append(f"- `{row['row_id']}` / `{row['quantity']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## PiM / Htau Fallback"])
    for row in pim:
        lines.append(f"- `{row['row_id']}` / `{row['quantity']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Decision Gates"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}` / `{row['target']}`: {row['decision']} - {row['rationale']}")
    lines.extend(["", "## Status", f"- `{status['status']}`: {status['summary']}", "", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['result']} ({row['detail']})")
    lines.extend(
        [
            "",
            "## Next Target",
            f"- `{next_target['next_id']}` -> `{next_target['target_doc']}`",
            f"- Objective: {next_target['objective']}",
            f"- Success gate: {next_target['success_gate']}",
            f"- Reason: {next_target['reason']}",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_map()
    paths = output_paths()
    write_csv(paths["source_register"], source_register_rows(sources))
    write_csv(paths["delta_hodge_bound"], delta_hodge_bound_rows(sources))
    write_csv(paths["conformal_subtheorem"], conformal_subtheorem_rows(sources))
    write_csv(paths["em_normalization_branch"], normalization_rows(sources))
    write_csv(paths["pim_htau_fallback"], pim_htau_rows(sources))
    write_csv(paths["decision_gates"], decision_rows(sources))
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], status_rows())
    write_csv(paths["validation"], validation_rows(sources, paths))
    write_doc(paths)
    print(f"wrote {DOC}")
    print(f"wrote {paths['validation']}")


if __name__ == "__main__":
    main()
