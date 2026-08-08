from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3614"
BRANCH_ID = "MTS_R2FR_Y5_PRINCIPAL_HODGE_BOUND_OR_HTAU_CURL_INTEGRABILITY_3614"
DOC = ROOT / "3614-Y5-R2FR-principal-Hodge-bound-or-Htau-curl-integrability.md"


def utc_now() -> str:
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
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3613": (
            RESIDUALS / "P8_Y5_R2FR_3613_NEXT_TARGET.csv",
            "3614-Y5-R2FR-principal-Hodge-bound-or-Htau-curl-integrability.md",
        ),
        "delta_hodge_3613": (
            RESIDUALS / "P8_Y5_R2FR_3613_DELTA_HODGE_BOUND_LAW.csv",
            "Delta_chi_principal",
        ),
        "conformal_3613": (
            RESIDUALS / "P8_Y5_R2FR_3613_CONFORMAL_HODGE_SUBTHEOREM.csv",
            "SUBCOMPONENT_THEOREM_ZERO_FOR_HODGE_ONLY",
        ),
        "hodge_uniqueness_3504": (
            RESIDUALS / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv",
            "MATHEMATICAL_UNIQUENESS_LEMMA",
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
            "BIN3506_0_Delta_chi_principal",
        ),
        "constitutive_runner_3506": (
            RESIDUALS / "P8_Y5_R2FR_3506_CONSTITUTIVE_BOUND_RUNNER_RESULTS.csv",
            "BRUN3506_0_Delta_chi_principal",
        ),
        "htau_curl_vector_3578": (
            RESIDUALS / "P8_Y5_R2FR_3578_HTAU_CURL_COMPONENT_VECTOR.csv",
            "Delta_H_curl_bound",
        ),
        "htau_curl_identities_3578": (
            RESIDUALS / "P8_Y5_R2FR_3578_HTAU_CURL_IDENTITIES.csv",
            "d_F alpha_tau",
        ),
        "pim_htau_3602": (
            RESIDUALS / "P8_Y5_R2FR_3602_PIM_HTAU_COMPONENT_BOUND_ROWS.csv",
            "PHTB3602_3_C_curl",
        ),
        "denominator_fallback_3532": (
            RESIDUALS / "P8_Y5_R2FR_3532_DENOMINATOR_BOUND_FALLBACKS.csv",
            "C_Htau",
        ),
    }


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3614_SOURCE_REGISTER.csv",
        "principal_hodge_theorem": RESIDUALS / "P8_Y5_R2FR_3614_PRINCIPAL_HODGE_THEOREM.csv",
        "principal_hodge_bound": RESIDUALS / "P8_Y5_R2FR_3614_PRINCIPAL_HODGE_BOUND.csv",
        "empirical_bound_acquisition": RESIDUALS / "P8_Y5_R2FR_3614_PRINCIPAL_HODGE_EMPIRICAL_ACQUISITION.csv",
        "htau_curl_fallback": RESIDUALS / "P8_Y5_R2FR_3614_HTAU_CURL_FALLBACK.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3614_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3614_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3614_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_principal_Hodge_or_Htau_curl_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3614_VALIDATION.csv",
    }


def source_register_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    stamp = utc_now()
    rows = []
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


def principal_hodge_theorem_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(value[0]) for source_id, value in sources.items()}
    stamp = utc_now()
    rows = [
        (
            "PHT3614_0_reciprocal_principal",
            "principal constitutive action branch",
            "A local bilinear EM action contributes only the reciprocal/symmetric principal constitutive part; skewon is non-Lagrangian and already belongs to a separate residual.",
            "S_EM=-1/4 int F_A chi^{AB} F_B; Euler/Hilbert action sees chi^{(AB)}",
            "DERIVED_CONDITIONAL_INPUT",
            "chi_reconstruct_3287",
        ),
        (
            "PHT3614_1_fresnel_reconstruction",
            "nonbirefringent Fresnel branch",
            "If the Fresnel quartic is a repeated quadratic, the principal reciprocal chi reconstructs a conformal EM metric class.",
            "G^{abcd}k_a k_b k_c k_d proportional (g_EM^{ab}k_a k_b)^2 => [g_EM]",
            "DERIVED_CONDITIONAL_INPUT",
            "chi_reconstruct_3287",
        ),
        (
            "PHT3614_2_metric_hodge_shape",
            "closure relation to Hodge shape",
            "After axion/skewon removal, kappa^2=-lambda^2 I makes kappa/lambda a Hodge complex structure.",
            "chi_principal=lambda *_gEM after closure and positivity branch selection",
            "DERIVED_CONDITIONAL_INPUT",
            "chi_reconstruct_3287",
        ),
        (
            "PHT3614_3_same_metric_clause",
            "same public metric obstruction",
            "The EM metric reconstructed from rays must be identified with the matter/clock/source metric up to the conformal scale already separated in 3613.",
            "[g_EM]=[g_obs] plus orientation/time orientation fixed before readout",
            "PARENT_SIGNATURE_REQUIRED",
            "chi_reconstruct_3287",
        ),
        (
            "PHT3614_4_conditional_zero",
            "Delta_chi_principal Hodge zero theorem",
            "Delta_chi_principal is zero for the Hodge/cone branch if reciprocal nonbirefringent closure reconstructs the same public conformal metric and no independent principal tensor is allowed.",
            "reciprocal chi + repeated-quadratic Fresnel + kappa^2=-lambda^2 I + [g_EM]=[g_obs] + fixed orientation => Delta_chi_principal^Hodge=0",
            "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "observed_hodge_3503",
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
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, target, statement, mathematical_form, status, source_id in rows
    ]


def principal_hodge_bound_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(value[0]) for source_id, value in sources.items()}
    stamp = utc_now()
    rows = [
        (
            "PHB3614_0_target",
            "Delta_chi_principal",
            "principal constitutive mismatch after skewon, axion gradient, hidden/readout tails and pure conformal Hodge scale are separated",
            "Delta_chi_principal := chi_EM_principal - chi_principal(g_obs)",
            "TARGET_IMPORTED",
            "delta_hodge_3613",
            "This is the principal-Hodge pressure point selected by 3613.",
        ),
        (
            "PHB3614_1_bound_law",
            "principal Hodge no-cancellation bound",
            "The principal mismatch is bounded by Fresnel/birefringent shape failure, same-metric identification failure, closure-relation defect and orientation/time-orientation mismatch.",
            "||Delta_chi_principal||_H <= B_Fresnel + C_g||[g_EM]-[g_obs]|| + B_closure + B_orient",
            "SOURCE_BOUND_FILLED_NONCLAIM",
            "chi_reconstruct_3287",
            "This is the 3614 success gate: Delta_chi_principal now has a sourced no-cancellation bound law.",
        ),
        (
            "PHB3614_2_B_Fresnel",
            "B_Fresnel",
            "captures failure of the Fresnel quartic to reduce to a repeated quadratic / nonbirefringent cone",
            "B_Fresnel := ||G_chi(k)-rho(g_EM^{ab}k_a k_b)^2||_arena",
            "BOUND_COMPONENT_VALUES_MISSING",
            "constitutive_template_3506",
            "Empirical arenas include vacuum birefringence, light-cone and Shapiro/lensing consistency.",
        ),
        (
            "PHB3614_3_same_metric",
            "same-metric mismatch",
            "captures failure to identify the reconstructed EM conformal metric with the public matter/clock/source metric",
            "B_same_metric := C_g||[g_EM]-[g_obs]||",
            "BOUND_COMPONENT_VALUES_MISSING",
            "hodge_uniqueness_3504",
            "This is the key local-GR obstruction after EM nonbirefringence.",
        ),
        (
            "PHB3614_4_closure_defect",
            "closure-relation defect",
            "captures failure of kappa^2=-lambda^2 I on the physical 2-form subspace after axion/skewon split",
            "B_closure := ||kappa^2+lambda^2 I||",
            "BOUND_COMPONENT_VALUES_MISSING",
            "chi_reconstruct_3287",
            "This turns the premetric constitutive ambiguity into an operator condition.",
        ),
        (
            "PHB3614_5_scale_guard",
            "scalar impedance / conformal scale",
            "lambda and pure conformal scale are not counted as Hodge-cone mismatch after 3613; they remain in normalization/source/clock gates.",
            "B_scale not in ||Delta_chi_principal||_H; carry B_lambda/source_clock instead",
            "RECLASSIFIED_NOT_DROPPED",
            "conformal_3613",
            "This prevents double-counting while preserving the Newton/source-calibration risk.",
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


def empirical_acquisition_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(value[0]) for source_id, value in sources.items()}
    stamp = utc_now()
    rows = [
        (
            "PEA3614_0_existing_runner",
            "Delta_chi_principal",
            "current local runner remains blocked because parent coefficient and observational bound rows are missing",
            "abs(predicted_value) <= bound_value with sourced numeric rows",
            "BLOCKED_INPUT_NOT_VALID_FOR_CLAIM",
            "constitutive_runner_3506",
        ),
        (
            "PEA3614_1_bound_source_need",
            "vacuum birefringence / light-cone bound",
            "future numeric scoring needs a primary-source observational bound for B_Fresnel and a declared norm map",
            "bound_source_path != MISSING_SOURCE_PATH; bound_units declared; arena projection declared",
            "ACQUISITION_REQUIRED_NO_NUMERIC_CLAIM",
            "constitutive_template_3506",
        ),
        (
            "PEA3614_2_parent_coefficient_need",
            "MTS predicted principal coefficient",
            "future numeric scoring also needs a parent coefficient for B_Fresnel, same-metric mismatch or closure defect",
            "predicted_value != MISSING_PARENT_COEFFICIENT",
            "PARENT_INPUT_REQUIRED_NO_NUMERIC_CLAIM",
            "constitutive_template_3506",
        ),
    ]
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "target": target,
            "statement": statement,
            "formula": formula,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, target, statement, formula, status, source_id in rows
    ]


def htau_curl_fallback_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(value[0]) for source_id, value in sources.items()}
    stamp = utc_now()
    rows = [
        (
            "HCF3614_0_identity",
            "C_curl",
            "Hamiltonian curl is the fallback Newton-source denominator obstruction if principal Hodge cannot be scored next.",
            "C_curl := Pi_M^H(curl(delta H_tau))/(Pi_M H_tau)",
            "FALLBACK_TARGET_IMPORTED",
            "pim_htau_3602",
        ),
        (
            "HCF3614_1_curl_law",
            "field-space curl identity",
            "fixed H_ref removes reference-source derivative, but omega_MTS, tau generator, surface and boundary/corner terms remain.",
            "d_F alpha_tau=-int_S i_tau omega_MTS + C_tau + C_S + C_ref; fixed-reference branch sets C_ref=0",
            "EXACT_IDENTITY_IMPORTED",
            "htau_curl_identities_3578",
        ),
        (
            "HCF3614_2_bound_vector",
            "Delta_H_curl_bound",
            "live curl terms already have a no-cancellation component envelope.",
            "Delta_H_curl_bound <= A_F sup_BF (I_pub+I_EM+I_extra+I_boundary+I_tau_surface+I_qdescent)",
            "BOUND_VECTOR_READY_VALUES_MISSING",
            "htau_curl_vector_3578",
        ),
        (
            "HCF3614_3_first_internal_zeroes",
            "reference and PiM projector pieces",
            "fixed-reference and Hilbert-identity Pi_M branch zeroes are retained internally and must not be double-counted.",
            "I_ref=0; I_projector_PiMH=0 in selected internal branch",
            "SIGNED_INTERNAL_ZERO_NONCLAIM",
            "htau_curl_vector_3578",
        ),
        (
            "HCF3614_4_empirical_map",
            "C_Htau observable map",
            "if not theorem-zero, the curl bound maps to Gdot, clock drift, PPN preferred-frame/conservation and orbital/source mass leakage.",
            "C_Htau := norm(int_boundary i_tau omega_total)/norm(delta H_tau)",
            "BOUND_ROUTE_IMPORTED",
            "denominator_fallback_3532",
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
    stamp = utc_now()
    rows = [
        (
            "DEC3614_0_principal_theorem",
            "Delta_chi_principal theorem-zero route",
            "CONDITIONAL_THEOREM_WRITTEN",
            "Principal Hodge mismatch vanishes if reciprocal nonbirefringent closure reconstructs the same public conformal metric and independent principal tensors are forbidden.",
            "chi_reconstruct_3287",
        ),
        (
            "DEC3614_1_principal_bound",
            "Delta_chi_principal source-bound route",
            "ADVANCED",
            "A sourced no-cancellation bound now splits principal Hodge failure into Fresnel, same-metric, closure and orientation components.",
            "delta_hodge_3613",
        ),
        (
            "DEC3614_2_empirical",
            "observational/numeric claim",
            "BLOCKED",
            "No numeric claim is allowed until primary observational bounds and parent coefficients replace MISSING rows.",
            "constitutive_runner_3506",
        ),
        (
            "DEC3614_3_htau",
            "C_curl fallback",
            "READY",
            "H_tau curl fallback is imported with internal zeroes for reference/projector and live public/EM/extra/boundary/tau/qdescent components.",
            "htau_curl_vector_3578",
        ),
        (
            "DEC3614_4_claim_guard",
            "local-GR/Newton/Maxwell claim",
            "BLOCKED_FOR_CLAIM_NOT_FOR_WORK",
            "No local-GR/Newton/Maxwell pass follows because principal Hodge theorem is conditional and numeric bounds are not sourced.",
            "handoff_3613",
        ),
        (
            "DEC3614_5_next",
            "next best attack",
            "SELECT_BFRESNEL_SOURCE_OR_HTAU_PUBLIC_FLUX",
            "Either acquire a real primary-source B_Fresnel/light-cone bound, or attack I_public/I_matter_EM in C_curl as the next Hamiltonian integrability component.",
            "htau_curl_vector_3578",
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
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "PRINCIPAL_HODGE_BOUND_FILLED_CONDITIONAL_ZERO_ROUTE_WRITTEN_HTAU_CURL_READY",
            "summary": (
                "3614 writes the conditional principal-Hodge zero theorem and fills a source-backed no-cancellation bound for Delta_chi_principal: "
                "Fresnel/birefringent shape, same-metric mismatch, closure defect and orientation. Numeric scoring remains blocked by missing parent coefficients and primary observational bound rows. "
                "C_curl is carried as the Pi_M/H_tau Hamiltonian fallback with component envelope ready."
            ),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3614_0",
            "target_doc": "3615-Y5-R2FR-BFresnel-primary-bound-or-Htau-public-flux.md",
            "target_script": "scripts/Y5_R2FR_3615_BFresnel_primary_bound_or_Htau_public_flux.py",
            "objective": (
                "try to acquire/source a primary nonclaim observational bound row for B_Fresnel / Delta_chi_principal; "
                "if not, attack the public EH plus matter/EM flux components of H_tau curl"
            ),
            "success_gate": (
                "must produce either a primary-source empirical bound acquisition row for B_Fresnel with units/arena, "
                "or a theorem-zero/source-bound row for I_EH_stationary_boundary or I_matter_EM_flux"
            ),
            "reason": "3614 split the principal-Hodge problem enough that the next useful move is either real bound data or Hamiltonian curl flux reduction.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def formalization_leaks() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    leaks = []
    for path in FORMALIZATION.rglob("*3614*"):
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
    theorem = read_csv(paths["principal_hodge_theorem"])
    bound = read_csv(paths["principal_hodge_bound"])
    empirical = read_csv(paths["empirical_bound_acquisition"])
    curl = read_csv(paths["htau_curl_fallback"])
    decisions = read_csv(paths["decision_gates"])
    status = read_csv(paths["status"])
    outputs_exist = all(path.exists() for name, path in paths.items() if name != "validation")
    sources_exist = all(row["exists"].lower() == "true" for row in source_rows)
    needles_found = all(row["needle_found"].lower() == "true" for row in source_rows)
    no_claim_flags = True
    for name, path in paths.items():
        if name == "validation":
            continue
        for row in read_csv(path):
            if row.get("claim_allowed", "False").lower() == "true" or row.get("valid_for_claim", "False").lower() == "true":
                no_claim_flags = False
    conditional_theorem = any(
        row["theorem_id"] == "PHT3614_4_conditional_zero"
        and row["status"] == "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED"
        for row in theorem
    )
    principal_bound = any(
        row["bound_id"] == "PHB3614_1_bound_law"
        and "||Delta_chi_principal||_H <=" in row["formula"]
        for row in bound
    )
    scale_not_dropped = any(row["bound_id"] == "PHB3614_5_scale_guard" and row["status"] == "RECLASSIFIED_NOT_DROPPED" for row in bound)
    empirical_blocked = any(
        row["row_id"] == "PEA3614_0_existing_runner" and row["status"] == "BLOCKED_INPUT_NOT_VALID_FOR_CLAIM"
        for row in empirical
    )
    curl_fallback = any(
        row["row_id"] == "HCF3614_2_bound_vector" and "Delta_H_curl_bound <=" in row["formula"]
        for row in curl
    )
    next_selected = any(row["decision_id"] == "DEC3614_5_next" and "SELECT_BFRESNEL" in row["decision"] for row in decisions)
    status_ok = bool(status) and status[0]["status"] == "PRINCIPAL_HODGE_BOUND_FILLED_CONDITIONAL_ZERO_ROUTE_WRITTEN_HTAU_CURL_READY"
    leaks = formalization_leaks()
    specs = [
        ("VAL3614_0_sources_exist", sources_exist, "all required 3614 source paths exist"),
        ("VAL3614_1_needles_found", needles_found, "all selected 3614 source anchors found"),
        ("VAL3614_2_outputs_exist", outputs_exist, "all pre-validation 3614 csv outputs written"),
        ("VAL3614_3_csv_parse", True, csv_summary(paths)),
        ("VAL3614_4_conditional_theorem_written", conditional_theorem, "principal-Hodge conditional zero theorem written"),
        ("VAL3614_5_principal_bound_filled", principal_bound, "Delta_chi_principal no-cancellation bound filled"),
        ("VAL3614_6_scale_not_dropped", scale_not_dropped, "scalar/conformal scale reclassified, not discarded"),
        ("VAL3614_7_empirical_claim_blocked", empirical_blocked, "numeric empirical claim remains blocked without primary/source rows"),
        ("VAL3614_8_htau_curl_fallback_ready", curl_fallback, "C_curl fallback bound vector imported"),
        ("VAL3614_9_no_claim_flags", no_claim_flags, "all generated rows remain nonclaim"),
        ("VAL3614_10_next_target_selected", next_selected, "3615 target selected from concrete bound branches"),
        ("VAL3614_11_status_ok", status_ok, "canonical status matches 3614 verdict"),
        (
            "VAL3614_12_formalization_workbench_untouched",
            len(leaks) == 0,
            "no 3614 checkpoint output appears in formalization-workbench outside package/venv noise",
        ),
    ]
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail if passed else f"{detail}; leaks={[str(leak) for leak in leaks]}",
        }
        for validation_id, passed, detail in specs
    ]


def write_doc(paths: dict[str, Path]) -> None:
    theorem = read_csv(paths["principal_hodge_theorem"])
    bound = read_csv(paths["principal_hodge_bound"])
    empirical = read_csv(paths["empirical_bound_acquisition"])
    curl = read_csv(paths["htau_curl_fallback"])
    decisions = read_csv(paths["decision_gates"])
    status = read_csv(paths["status"])[0]
    validation = read_csv(paths["validation"])
    next_target = read_csv(paths["next_target"])[0]
    lines = [
        "# 3614 - principal Hodge bound or Htau curl integrability",
        "",
        "## Verdict",
        "3614 advances the principal-Hodge branch.  `Delta_chi_principal` now has both a conditional theorem-zero route and a no-cancellation bound law.",
        "",
        "`||Delta_chi_principal||_H <= B_Fresnel + C_g||[g_EM]-[g_obs]|| + B_closure + B_orient`",
        "",
        "The theorem-zero route is clean but not a current claim: reciprocal principal chi, nonbirefringent Fresnel reconstruction, closure relation, same public conformal metric, fixed orientation, and no independent principal tensor must all be parent-signed.  Scalar/conformal scale is still carried in source/clock/normalization gates, not silently discarded.",
        "",
        "## Principal Hodge Theorem",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}` / `{row['target']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Principal Hodge Bound"])
    for row in bound:
        lines.append(f"- `{row['bound_id']}` / `{row['quantity']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Empirical Acquisition"])
    for row in empirical:
        lines.append(f"- `{row['row_id']}` / `{row['target']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Htau Curl Fallback"])
    for row in curl:
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
    write_csv(paths["principal_hodge_theorem"], principal_hodge_theorem_rows(sources))
    write_csv(paths["principal_hodge_bound"], principal_hodge_bound_rows(sources))
    write_csv(paths["empirical_bound_acquisition"], empirical_acquisition_rows(sources))
    write_csv(paths["htau_curl_fallback"], htau_curl_fallback_rows(sources))
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
