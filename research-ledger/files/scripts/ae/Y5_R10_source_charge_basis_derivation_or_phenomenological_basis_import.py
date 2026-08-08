from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "984-Y5-R10-source-charge-basis-derivation-or-phenomenological-basis-import.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "983_doc",
            "path": "983-Y5-R10-WEP-source-charge-projection-matrix-MICROSCOPE-TiPt.md",
            "role": "handoff selecting source-charge basis derivation/import",
            "needle": "DEC983_2_best_next",
        },
        {
            "source_id": "983_projection_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_R10_983_PROJECTION_ATTEMPT.csv",
            "role": "WEP projection skeleton with missing C-source coefficients",
            "needle": "WEP983_0_vector_projection",
        },
        {
            "source_id": "983_delta_vector",
            "path": "source-intake/mts_residuals/P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv",
            "role": "MICROSCOPE alloy differential proxy vector",
            "needle": "DEL983_neutron_excess_proxy",
        },
        {
            "source_id": "983_identity_bounds",
            "path": "source-intake/mts_residuals/P8_Y5_R10_983_IDENTITY_DEBUG_BOUNDS.csv",
            "role": "debug-only single-proxy bounds",
            "needle": "IB983_coulomb_proxy",
        },
        {
            "source_id": "575_constant_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_575_CONSTANT_SOURCE_LOCK_CONTRACT.csv",
            "role": "constant/source lock contract",
            "needle": "CL575_4_universal_coupling",
        },
        {
            "source_id": "622_doc",
            "path": "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
            "role": "parent matter sector and source-weight slot definitions",
            "needle": "PMC622_5_universal_source",
        },
        {
            "source_id": "447_doc",
            "path": "447-no-species-source-charge-one-coframe-theorem-attempt.md",
            "role": "one-coframe not enough; source-charge theorem gap",
            "needle": "species_source_charge",
        },
        {
            "source_id": "448_doc",
            "path": "448-constant-sector-universality-theorem-attempt.md",
            "role": "constant-sector universality and theta_A(I_Q) warning",
            "needle": "theta_A(I_Q)",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "generated_utc": stamp(),
            }
        )
    return rows


def web_source_rows() -> list[dict[str, str]]:
    return [
        {
            "web_source_id": "WEB984_0_DAMOUR_DONOGHUE_DILATON_COUPLINGS",
            "title": "Phenomenology of the Equivalence Principle with Light Scalars",
            "authors": "Damour and Donoghue",
            "year": "2010",
            "url": "https://arxiv.org/abs/1007.2790",
            "role": "phenomenological scalar-composition charge basis; five dilaton parameters with dominant nuclear/electromagnetic directions",
            "use_in_984": "source for imported nonclaim charge-basis scaffold",
            "valid_for_claim": "false",
        },
        {
            "web_source_id": "WEB984_1_DAMOUR_DONOGHUE_EPV",
            "title": "Equivalence Principle Violations and Couplings of a Light Dilaton",
            "authors": "Damour and Donoghue",
            "year": "2010",
            "url": "https://arxiv.org/abs/1007.2792",
            "role": "explicit EP-violation parameterization and dominant charge directions",
            "use_in_984": "source for C_hatm/C_e-style phenomenological rows",
            "valid_for_claim": "false",
        },
        {
            "web_source_id": "WEB984_2_MICROSCOPE_DILATON_CONSTRAINTS",
            "title": "MICROSCOPE mission: first constraints on the violation of the weak equivalence principle by a light scalar dilaton",
            "authors": "Berge et al.",
            "year": "2018",
            "url": "https://arxiv.org/abs/1712.00483",
            "role": "MICROSCOPE use of scalar/dilaton WEP projection language",
            "use_in_984": "confirms that MICROSCOPE WEP bounds require model-specific projection assumptions",
            "valid_for_claim": "false",
        },
        {
            "web_source_id": "WEB984_3_DAMOUR_THEORETICAL_EP_REVIEW",
            "title": "Theoretical Aspects of the Equivalence Principle",
            "authors": "Damour",
            "year": "2012",
            "url": "https://arxiv.org/abs/1202.6311",
            "role": "review of EP-violation phenomenology dominated by Coulomb and nuclear binding effects",
            "use_in_984": "context source for splitting derivation route from phenomenological import",
            "valid_for_claim": "false",
        },
    ]


def derivation_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "SCB984_0_universal_Hilbert_source",
            "claim": "If one observed coframe and one universal kappa couple to the Hilbert stress current of all ordinary matter, no composition-dependent source charge appears.",
            "math_form": "E_munu = kappa*T_munu; T_munu=sum_A T_A_munu from the same S_m[e_obs,Psi_A,theta_A]",
            "result": "RELATIVE_ZERO_THEOREM",
            "reason": "all test bodies source the same metric current; differential free fall needs an extra non-universal channel",
            "missing_for_MTS_derivation": "parent proof of one kappa, one observed coframe, constant-sector trivial action, and measured-GM calibration",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "SCB984_1_source_charge_basis_not_from_universal_source",
            "claim": "A nonzero source-charge basis cannot be derived from strict universal Hilbert-source coupling alone.",
            "math_form": "universal source => C_e=C_N=C_C=C_A=S_source=0 for WEP residuals",
            "result": "NO_NONZERO_BASIS_FROM_UNIVERSAL_SOURCE",
            "reason": "the very purpose of a source-charge basis is to parameterize deviations from universal source coupling",
            "missing_for_MTS_derivation": "parent term that couples MTS residuals to nuclear/EM mass contributions",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "SCB984_2_MTS_specific_basis_requirement",
            "claim": "An MTS-derived basis must say which parent field changes which part of rest mass/source normalization.",
            "math_form": "delta ln m_A = C_g d_g + C_hatm d_hatm*Q_hatm(A,Z)+C_e d_e*Q_e(A,Z)+... mapped to b_kappa,b_theta,b_m",
            "result": "MTS_PARENT_TERM_MISSING",
            "reason": "current MTS corpus has coefficient slots, but not a parent Lagrangian term identifying nuclear/EM sensitivities",
            "missing_for_MTS_derivation": "explicit parent coupling to QCD scale, quark-mass, EM/Coulomb, electron-mass, or marker source terms",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "SCB984_3_import_policy",
            "claim": "Use an external phenomenological charge basis only as a nonclaim scaffold.",
            "math_form": "eta_AB = sum_i DeltaQ_i(A,B)*C_i with imported Q_i and unsourced C_i",
            "result": "PHENOMENOLOGICAL_IMPORT_ALLOWED_NONCLAIM",
            "reason": "this permits screening/debugging without pretending the basis is MTS-derived",
            "missing_for_MTS_derivation": "derive or source the C_i-to-MTS coefficient map",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "SCB984_4_verdict",
            "claim": "984 source-charge basis status.",
            "math_form": "universal Hilbert source gives zero WEP branch conditionally; nonzero composition basis is imported phenomenology",
            "result": "DERIVED_ZERO_OR_IMPORTED_NONCLAIM_BASIS_ONLY",
            "reason": "we can derive the condition under which source charges vanish, but not the nonzero basis coefficients",
            "missing_for_MTS_derivation": "parent source-charge deformation term or theorem-zero closure",
            "valid_for_claim": "false",
        },
    ]


def imported_basis_rows() -> list[dict[str, str]]:
    return [
        {
            "basis_id": "IMP984_0_universal_part",
            "imported_charge": "universal mass/source component",
            "proxy_in_983": "none; cancels in eta_AB",
            "phenomenological_role": "common coupling does not produce WEP contrast",
            "maps_to_MTS_slot": "universal kappa baseline, not b_kappa residual",
            "source": "WEB984_0_DAMOUR_DONOGHUE_DILATON_COUPLINGS",
            "import_status": "background_only",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "IMP984_1_nuclear_surface_light_quark",
            "imported_charge": "dominant nuclear binding/light-quark-mass direction",
            "proxy_in_983": "neutron_excess_proxy plus A_bar/A_surface proxy placeholders",
            "phenomenological_role": "composition-dependent nuclear binding sensitivity",
            "maps_to_MTS_slot": "b_theta if MTS changes matter constants; b_kappa only if source normalization becomes composition dependent",
            "source": "WEB984_0_DAMOUR_DONOGHUE_DILATON_COUPLINGS",
            "import_status": "phenomenological_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "IMP984_2_electromagnetic_Coulomb",
            "imported_charge": "electromagnetic/Coulomb direction",
            "proxy_in_983": "coulomb_proxy",
            "phenomenological_role": "fine-structure/Coulomb contribution to composition-dependent mass",
            "maps_to_MTS_slot": "b_theta/alpha_EM first; b_kappa only after source-normalization projection",
            "source": "WEB984_1_DAMOUR_DONOGHUE_EPV",
            "import_status": "phenomenological_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "IMP984_3_electron_fraction",
            "imported_charge": "electron/electromagnetic matter fraction proxy",
            "proxy_in_983": "Y_e_proxy",
            "phenomenological_role": "rough electron/proton fraction sensitivity; not full DD charge formula",
            "maps_to_MTS_slot": "b_theta or b_m only with explicit matter-sector coupling",
            "source": "WEB984_0_DAMOUR_DONOGHUE_DILATON_COUPLINGS",
            "import_status": "debug_proxy_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "basis_id": "IMP984_4_marker_or_material_charge",
            "imported_charge": "unclassified material marker/source-normalization charge",
            "proxy_in_983": "A_bar_proxy or user-defined material marker",
            "phenomenological_role": "captures non-standard composition/source weighting not in known charge basis",
            "maps_to_MTS_slot": "b_m or b_kappa",
            "source": "MTS_internal_gap_from_983",
            "import_status": "MTS_placeholder_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def basis_to_slot_rows() -> list[dict[str, str]]:
    return [
        {
            "map_id": "BMAP984_0_universal_kappa",
            "basis_id": "IMP984_0_universal_part",
            "MTS_slot": "baseline kappa",
            "status": "cancels_in_WEP",
            "claim_effect": "does not bound b_kappa",
            "missing": "none for cancellation; parent derivation still needed for local GR",
            "valid_for_claim": "false",
        },
        {
            "map_id": "BMAP984_1_nuclear_to_btheta",
            "basis_id": "IMP984_1_nuclear_surface_light_quark",
            "MTS_slot": "b_theta",
            "status": "phenomenological_route",
            "claim_effect": "would bound matter-constant sensitivity, not source kappa directly",
            "missing": "parent link between MTS field and quark/nuclear binding parameters",
            "valid_for_claim": "false",
        },
        {
            "map_id": "BMAP984_2_coulomb_to_btheta",
            "basis_id": "IMP984_2_electromagnetic_Coulomb",
            "MTS_slot": "b_theta",
            "status": "phenomenological_route",
            "claim_effect": "would bound alpha_EM-like sensitivity",
            "missing": "parent EM/fine-structure coupling normal form",
            "valid_for_claim": "false",
        },
        {
            "map_id": "BMAP984_3_basis_to_bkappa",
            "basis_id": "IMP984_1_nuclear_surface_light_quark;IMP984_2_electromagnetic_Coulomb;IMP984_4_marker_or_material_charge",
            "MTS_slot": "b_kappa",
            "status": "not_derived",
            "claim_effect": "cannot bound source-weight splitting yet",
            "missing": "source-normalization theorem or explicit non-universal gravitational charge term",
            "valid_for_claim": "false",
        },
        {
            "map_id": "BMAP984_4_marker_to_bm",
            "basis_id": "IMP984_4_marker_or_material_charge",
            "MTS_slot": "b_m",
            "status": "placeholder_only",
            "claim_effect": "marks unclassified material marker channel",
            "missing": "marker taxonomy and no-extension theorem",
            "valid_for_claim": "false",
        },
    ]


def screening_policy_rows() -> list[dict[str, str]]:
    return [
        {
            "policy_id": "SPOL984_0_theorem_zero_branch",
            "branch": "parent-derived universal Hilbert source",
            "allowed_action": "set WEP source-charge basis to zero only if 575/622/979 source-universality gates are parent-signed",
            "current_status": "not_signed",
            "claim_allowed": "false",
        },
        {
            "policy_id": "SPOL984_1_phenomenological_branch",
            "branch": "imported Damour-Donoghue-like charge basis",
            "allowed_action": "screen eta_AB against proxy charge deltas using labelled C_i coefficients",
            "current_status": "allowed_nonclaim_scaffold",
            "claim_allowed": "false",
        },
        {
            "policy_id": "SPOL984_2_identity_debug",
            "branch": "single-proxy identity assumption",
            "allowed_action": "use 983 identity bounds only for debugging scale intuition",
            "current_status": "debug_only",
            "claim_allowed": "false",
        },
        {
            "policy_id": "SPOL984_3_MTS_claim",
            "branch": "MTS coefficient bound",
            "allowed_action": "requires explicit C_i-to-b_slot map or theorem-zero proof",
            "current_status": "blocked",
            "claim_allowed": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE984_0_universal_source_zero",
            "claim": "universal Hilbert source would zero WEP source charges",
            "gate_pass": "relative_only",
            "claim_allowed": "false",
            "why_not": "the parent source-universality gates are not signed",
        },
        {
            "gate_id": "CGATE984_1_imported_basis_ready",
            "claim": "phenomenological charge basis is available for nonclaim screening",
            "gate_pass": "true",
            "claim_allowed": "false",
            "why_not": "available scaffold is not an MTS derivation",
        },
        {
            "gate_id": "CGATE984_2_bkappa_bound",
            "claim": "MICROSCOPE bounds MTS b_kappa",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "C_i-to-b_kappa source-normalization projection is missing",
        },
        {
            "gate_id": "CGATE984_3_btheta_bound",
            "claim": "MICROSCOPE bounds MTS b_theta",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "MTS-to-matter-constant coupling normal form is missing",
        },
        {
            "gate_id": "CGATE984_4_WEP_local_GR",
            "claim": "WEP/local-GR branch passes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "984 is basis discipline only; no scored MTS coefficient",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC984_0_derivation",
            "topic": "Hilbert-source derivation",
            "result": "zero_theorem_conditional_nonzero_basis_not_derived",
            "reason": "universal Hilbert source removes composition dependence rather than producing a finite source-charge basis",
            "next_action": "separate theorem-zero branch from phenomenological finite branch",
        },
        {
            "decision_id": "DEC984_1_import",
            "topic": "phenomenological basis",
            "result": "Damour_Donoghue_style_basis_imported_nonclaim",
            "reason": "known EP phenomenology supplies charge directions for screening, but not MTS coefficients",
            "next_action": "wire imported C_i scaffold into a screening-only WEP runner",
        },
        {
            "decision_id": "DEC984_2_best_next",
            "topic": "next checkpoint",
            "result": "WEP_screening_runner_with_imported_basis",
            "reason": "we now have composition deltas plus imported nonclaim charge basis; next step is a runner that refuses claims unless C_i-to-b_slot map is supplied",
            "next_action": "write 985 WEP imported-basis screening runner for MICROSCOPE Ti/Pt",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "985-Y5-R10-WEP-imported-basis-screening-runner-MICROSCOPE-TiPt.md",
            "objective": "build a nonclaim WEP screening runner using the imported phenomenological charge basis and MICROSCOPE alloy proxy deltas",
            "include": "C_i placeholder vector, eta prediction formula, identity/debug scenarios, hard claim gates for missing C_i-to-MTS map",
            "exclude": "WEP pass, b_kappa/b_theta bound claim, invented coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_ts = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_ts:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    web_sources: list[dict[str, str]],
    attempts: list[dict[str, str]],
    imports: list[dict[str, str]],
    maps: list[dict[str, str]],
    policies: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    web_ok = all(row["url"].startswith("https://") and row["valid_for_claim"] == "false" for row in web_sources)
    verdict_ok = any(row["attempt_id"] == "SCB984_4_verdict" and row["result"] == "DERIVED_ZERO_OR_IMPORTED_NONCLAIM_BASIS_ONLY" for row in attempts)
    imports_nonclaim_ok = all(row["valid_for_claim"] == "false" and "nonclaim" in row["import_status"] or row["import_status"] == "background_only" for row in imports)
    maps_nonclaim_ok = all(row["valid_for_claim"] == "false" for row in maps)
    policies_safe_ok = all(row["claim_allowed"] == "false" for row in policies)
    claims_safe_ok = all(row["claim_allowed"] == "false" for row in claims)
    next_decision_ok = any(row["decision_id"] == "DEC984_2_best_next" and row["result"] == "WEP_screening_runner_with_imported_basis" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V984_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all local sources exist and needles are found"},
        {"check_id": "V984_1_web_sources", "result": "pass" if web_ok else "fail", "detail": "phenomenological web source rows are recorded and nonclaim"},
        {"check_id": "V984_2_derivation_verdict", "result": "pass" if verdict_ok else "fail", "detail": "zero theorem/import-only verdict is recorded"},
        {"check_id": "V984_3_imports_nonclaim", "result": "pass" if imports_nonclaim_ok else "fail", "detail": "imported basis rows are nonclaim scaffolds"},
        {"check_id": "V984_4_maps_nonclaim", "result": "pass" if maps_nonclaim_ok else "fail", "detail": "basis-to-slot maps are nonclaim rows"},
        {"check_id": "V984_5_policy_safe", "result": "pass" if policies_safe_ok else "fail", "detail": "screening policies do not allow claims"},
        {"check_id": "V984_6_claim_gates_safe", "result": "pass" if claims_safe_ok else "fail", "detail": "claim gates block WEP/local-GR claims"},
        {"check_id": "V984_7_next_decision", "result": "pass" if next_decision_ok else "fail", "detail": "985 imported-basis screening runner selected"},
        {"check_id": "V984_8_next_target_written", "result": "pass" if next_ok else "fail", "detail": "next target row is present and nonclaim"},
        {"check_id": "V984_9_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {"check_id": "V984_READY", "result": "pass" if ready else "fail", "detail": "984 checkpoint pack validation summary", "generated_utc": stamp()}
    ]


def write_doc(
    sources: list[dict[str, str]],
    web_sources: list[dict[str, str]],
    attempts: list[dict[str, str]],
    imports: list[dict[str, str]],
    maps: list[dict[str, str]],
    policies: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 984 Y5 R10: Source-Charge Basis Derivation Or Phenomenological Basis Import",
        "",
        "Status: `Y5_R10_984_universal_Hilbert_source_gives_conditional_zero_nonzero_charge_basis_imported_nonclaim`",
        "",
        "Claim ceiling: no WEP pass, no `b_kappa` bound, no `b_theta` bound, no source-charge theorem-zero promotion, and no local-GR claim.",
        "",
        "## Readout",
        "",
        "984 separates two things that must not be blurred. If the parent action truly has one observed coframe, one universal `kappa`, and one Hilbert stress current for all ordinary matter, then WEP source-charge residuals vanish conditionally. That is a zero theorem route.",
        "",
        "But a nonzero source-charge basis is not derived by that universal-source theorem. A nonzero basis is a parameterization of deviations from universal source coupling. Therefore the finite branch can import a Damour-Donoghue-style phenomenological charge basis only as nonclaim scaffolding.",
        "",
        "In blunt terms: either derive zero, or import a basis. Do not pretend the imported basis is MTS-derived.",
        "",
        "## Local Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Web Source Register",
        "",
        md_table(web_sources, ["web_source_id", "title", "authors", "year", "url", "role", "valid_for_claim"]),
        "",
        "## Derivation Attempt",
        "",
        md_table(attempts, ["attempt_id", "claim", "result", "reason", "missing_for_MTS_derivation", "valid_for_claim"]),
        "",
        "## Imported Phenomenological Basis",
        "",
        md_table(imports, ["basis_id", "imported_charge", "proxy_in_983", "phenomenological_role", "maps_to_MTS_slot", "source", "import_status", "valid_for_claim"]),
        "",
        "## Basis To MTS Slot Map",
        "",
        md_table(maps, ["map_id", "basis_id", "MTS_slot", "status", "claim_effect", "missing", "valid_for_claim"]),
        "",
        "## Screening Policy",
        "",
        md_table(policies, ["policy_id", "branch", "allowed_action", "current_status", "claim_allowed"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "topic", "result", "reason", "next_action"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    web_sources = web_source_rows()
    attempts = derivation_attempt_rows()
    imports = imported_basis_rows()
    maps = basis_to_slot_rows()
    policies = screening_policy_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, web_sources, attempts, imports, maps, policies, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_984_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_984_WEB_SOURCE_REGISTER.csv", web_sources)
    write_csv(OUT / "P8_Y5_R10_984_DERIVATION_ATTEMPT.csv", attempts)
    write_csv(OUT / "P8_Y5_R10_984_IMPORTED_PHENOMENOLOGICAL_BASIS.csv", imports)
    write_csv(OUT / "P8_Y5_R10_984_BASIS_TO_MTS_SLOT_MAP.csv", maps)
    write_csv(OUT / "P8_Y5_R10_984_SCREENING_POLICY.csv", policies)
    write_csv(OUT / "P8_Y5_R10_984_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_984_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_984_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_984_VALIDATION.csv", validation)
    write_doc(sources, web_sources, attempts, imports, maps, policies, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
