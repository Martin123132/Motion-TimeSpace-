from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "986-Y5-R10-Ci-to-MTS-slot-map-or-parent-zero-theorem.md"
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
            "source_id": "985_doc",
            "path": "985-Y5-R10-WEP-imported-basis-screening-runner-MICROSCOPE-TiPt.md",
            "role": "handoff selecting C_i-to-MTS map or parent-zero theorem",
            "needle": "DEC985_2_best_next",
        },
        {
            "source_id": "985_coefficients",
            "path": "source-intake/mts_residuals/P8_Y5_R10_985_COEFFICIENT_VECTOR_TEMPLATE.csv",
            "role": "missing C_i coefficient template",
            "needle": "C985_4_S_source",
        },
        {
            "source_id": "985_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_985_SCREENING_SCENARIOS.csv",
            "role": "debug runner scenarios",
            "needle": "SCEN985_0_parent_zero_debug",
        },
        {
            "source_id": "984_derivation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_984_DERIVATION_ATTEMPT.csv",
            "role": "zero theorem versus imported nonclaim basis",
            "needle": "SCB984_4_verdict",
        },
        {
            "source_id": "984_basis_map",
            "path": "source-intake/mts_residuals/P8_Y5_R10_984_BASIS_TO_MTS_SLOT_MAP.csv",
            "role": "existing basis-to-slot nonclaim map",
            "needle": "BMAP984_3_basis_to_bkappa",
        },
        {
            "source_id": "983_delta",
            "path": "source-intake/mts_residuals/P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv",
            "role": "MICROSCOPE alloy proxy contrast",
            "needle": "DEL983_coulomb_proxy",
        },
        {
            "source_id": "575_constant_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_575_CONSTANT_SOURCE_LOCK_CONTRACT.csv",
            "role": "constant/source lock requirements",
            "needle": "CL575_4_universal_coupling",
        },
        {
            "source_id": "622_doc",
            "path": "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
            "role": "parent matter/source slot definitions",
            "needle": "PMC622_5_universal_source",
        },
        {
            "source_id": "979_doc",
            "path": "979-Y5-R10-parent-action-spine-superselection-clause-or-first-qbar-prior-source.md",
            "role": "one-kappa/topological coupling parent-action spine",
            "needle": "PASC979_4_single_gravitational_kappa",
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


def parent_zero_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "PZT986_0_statement",
            "statement": "If matter couples only through one observed coframe, constants are sector-trivial, and one universal kappa multiplies the common Hilbert source, then WEP source-charge coefficients vanish.",
            "math_form": "S_m=sum_A S_A[Psi_A,e_obs,theta_A]; E_munu=kappa*sum_A T_A_munu; L_X theta_A=0; no marker/source-weight term",
            "result": "RELATIVE_THEOREM_VALID",
            "MTS_slot_effect": "C_i=0 for composition-dependent source charges; b_kappa source split = 0",
            "missing_for_claim": "one observed coframe, constant-sector trivial action, one kappa, measured-GM calibration, no marker/source-weight term",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PZT986_1_chain_rule",
            "statement": "Composition sensitivity enters WEP only if the local MTS direction changes body-dependent mass/source normalization.",
            "math_form": "alpha_A^X = partial_X ln m_A or partial_X ln mu_A; eta_AB ~ (alpha_A^X-alpha_B^X)*field_gradient",
            "result": "ROUTING_IDENTITY",
            "MTS_slot_effect": "routes C_i into b_theta/b_m/b_kappa only after a parent coupling says which quantity X changes",
            "missing_for_claim": "local field-gradient/profile and coefficient normalization",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PZT986_2_kappa_cancellation",
            "statement": "A universal kappa rescales all ordinary source equally and cancels from differential free fall.",
            "math_form": "kappa_A=kappa for all A => Delta(kappa_A)/kappa = 0",
            "result": "RELATIVE_CANCELLATION",
            "MTS_slot_effect": "baseline kappa is not b_kappa; b_kappa means non-universal source normalization or running",
            "missing_for_claim": "parent proof that no kappa_A or material source weight exists",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PZT986_3_verdict",
            "statement": "Parent-zero theorem status.",
            "math_form": "conditional universal-source branch is coherent; current corpus has not signed every premise",
            "result": "ZERO_THEOREM_RELATIVE_NOT_PARENT_SIGNED",
            "MTS_slot_effect": "cannot retire WEP finite basis yet",
            "missing_for_claim": "same source-universality and no-marker gates as 575/622/979",
            "valid_for_claim": "false",
        },
    ]


def ci_to_slot_map_rows() -> list[dict[str, str]]:
    return [
        {
            "map_id": "CIMAP986_0_C_C_to_btheta_alpha",
            "phenomenological_coefficient": "C_C",
            "basis_feature": "coulomb_proxy",
            "primary_MTS_slot": "b_theta_alpha_EM",
            "route_formula": "C_C = P_C_alpha * d ln alpha_EM/dXhat * profile_X",
            "derivation_status": "CLEANEST_FINITE_ROUTE_NOT_PARENT_NORMALIZED",
            "why": "Coulomb binding responds directly to fine-structure/EM-sector variation, not to universal source kappa",
            "missing_inputs": "P_C_alpha, EM normal form, profile_X/local gradient normalization",
            "valid_for_claim": "false",
        },
        {
            "map_id": "CIMAP986_1_C_N_to_btheta_nuclear",
            "phenomenological_coefficient": "C_N",
            "basis_feature": "neutron_excess_proxy",
            "primary_MTS_slot": "b_theta_nuclear_or_mass_ratio",
            "route_formula": "C_N = P_N_mq * d ln(m_q/Lambda_QCD)/dXhat * profile_X + P_N_me * d ln(m_e/Lambda_QCD)/dXhat * profile_X",
            "derivation_status": "PHENOMENOLOGICAL_ROUTE_NOT_PARENT_NORMALIZED",
            "why": "nuclear/neutron-excess sensitivity is a matter-constant channel unless MTS adds non-universal source weights",
            "missing_inputs": "nuclear sensitivity matrix, mass-ratio normal form, profile_X/local gradient normalization",
            "valid_for_claim": "false",
        },
        {
            "map_id": "CIMAP986_2_C_Ye_to_btheta_or_marker",
            "phenomenological_coefficient": "C_Ye",
            "basis_feature": "Y_e_proxy",
            "primary_MTS_slot": "b_theta_electron_or_b_m",
            "route_formula": "C_Ye = P_Ye_e * d ln(m_e/Lambda_QCD)/dXhat * profile_X + P_Ye_marker*b_m",
            "derivation_status": "AMBIGUOUS_ROUTE",
            "why": "electron/proton fraction proxy can represent ordinary matter-constant sensitivity or an unclassified material marker",
            "missing_inputs": "matter-constant sensitivity split and marker taxonomy",
            "valid_for_claim": "false",
        },
        {
            "map_id": "CIMAP986_3_C_A_to_bm",
            "phenomenological_coefficient": "C_A",
            "basis_feature": "A_bar_proxy",
            "primary_MTS_slot": "b_m_or_nonstandard_source_marker",
            "route_formula": "C_A = P_A_marker*b_m + P_A_source*b_kappa_nonuniversal",
            "derivation_status": "PLACEHOLDER_ONLY",
            "why": "A_bar is a coarse debug proxy, not a standard derived fundamental charge",
            "missing_inputs": "marker/source-normalization definition and parent permission",
            "valid_for_claim": "false",
        },
        {
            "map_id": "CIMAP986_4_S_source_to_bkappa",
            "phenomenological_coefficient": "S_source",
            "basis_feature": "source_normalization",
            "primary_MTS_slot": "b_kappa_source_split",
            "route_formula": "S_source*b_kappa = Delta sigma_source(A,B) * b_kappa_nonuniversal",
            "derivation_status": "NOT_DERIVED",
            "why": "b_kappa is only WEP-visible if kappa/source normalization carries composition or marker dependence",
            "missing_inputs": "non-universal gravitational charge term or proof it is absent",
            "valid_for_claim": "false",
        },
        {
            "map_id": "CIMAP986_5_universal_kappa",
            "phenomenological_coefficient": "none",
            "basis_feature": "universal source baseline",
            "primary_MTS_slot": "baseline_kappa_not_residual",
            "route_formula": "kappa_A=kappa => no eta_AB contribution",
            "derivation_status": "RELATIVE_CANCELLATION",
            "why": "universal coupling is part of the GR-like limit, not a WEP-violating coefficient",
            "missing_inputs": "parent proof of one-kappa universality",
            "valid_for_claim": "false",
        },
    ]


def slot_claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "SLOT986_0_btheta_alpha",
            "slot": "b_theta_alpha_EM",
            "best_current_route": "C_C/coulomb_proxy",
            "gate_result": "route_identified_not_claimable",
            "claim_allowed": "false",
            "why_not": "EM normal form and profile normalization are missing",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SLOT986_1_btheta_nuclear",
            "slot": "b_theta_nuclear_or_mass_ratio",
            "best_current_route": "C_N/neutron_excess_proxy",
            "gate_result": "route_identified_not_claimable",
            "claim_allowed": "false",
            "why_not": "nuclear sensitivity matrix and parent mass-ratio normal form are missing",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SLOT986_2_bkappa_source_split",
            "slot": "b_kappa",
            "best_current_route": "S_source/non-universal source normalization",
            "gate_result": "blocked",
            "claim_allowed": "false",
            "why_not": "universal kappa cancels; non-universal kappa/source charge is not parent-derived",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SLOT986_3_bm_marker",
            "slot": "b_m",
            "best_current_route": "C_A/Y_e marker residual",
            "gate_result": "blocked",
            "claim_allowed": "false",
            "why_not": "marker taxonomy/no-extension theorem is missing",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SLOT986_4_parent_zero",
            "slot": "all WEP source-charge residuals",
            "best_current_route": "parent universal-source theorem",
            "gate_result": "relative_only",
            "claim_allowed": "false",
            "why_not": "source-universality premises are not parent-signed",
            "valid_for_claim": "false",
        },
    ]


def proof_obligation_rows() -> list[dict[str, str]]:
    return [
        {
            "obligation_id": "OB986_0_EM_normal_form",
            "needed_for": "C_C -> b_theta_alpha_EM",
            "proof_task": "derive whether MTS local branch changes alpha_EM or EM Coulomb energy at fixed observed coframe",
            "current_status": "open",
            "next_action": "write Coulomb-to-alphaEM normal-form attempt",
        },
        {
            "obligation_id": "OB986_1_nuclear_mass_normal_form",
            "needed_for": "C_N -> b_theta_nuclear",
            "proof_task": "derive whether MTS changes quark/QCD/electron mass ratios or only geometry/source normalization",
            "current_status": "open",
            "next_action": "defer until EM route is classified",
        },
        {
            "obligation_id": "OB986_2_source_normalization",
            "needed_for": "S_source -> b_kappa",
            "proof_task": "derive or reject non-universal gravitational source charge term",
            "current_status": "open",
            "next_action": "can be attacked via parent universal-source theorem",
        },
        {
            "obligation_id": "OB986_3_profile_normalization",
            "needed_for": "all finite WEP maps",
            "proof_task": "map local MTS field/profile gradient to the scalar-force coefficient used by WEP phenomenology",
            "current_status": "open",
            "next_action": "needed before any numeric WEP score",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE986_0_map_written",
            "claim": "C_i-to-slot map skeleton exists",
            "gate_pass": "true",
            "claim_allowed": "false",
            "why_not": "skeleton is not a derived coefficient map",
        },
        {
            "gate_id": "CGATE986_1_btheta_bound",
            "claim": "MICROSCOPE bounds b_theta",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "C_C/C_N route lacks EM/nuclear normal form and profile normalization",
        },
        {
            "gate_id": "CGATE986_2_bkappa_bound",
            "claim": "MICROSCOPE bounds b_kappa",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "universal kappa cancels; non-universal source-normalization term is not derived",
        },
        {
            "gate_id": "CGATE986_3_parent_zero",
            "claim": "WEP source charges are theorem-zero",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "parent one-kappa/constant/no-marker/source gates remain unsigned",
        },
        {
            "gate_id": "CGATE986_4_WEP_local_GR",
            "claim": "WEP/local-GR branch passes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "986 is a map audit, not a scored pass",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC986_0_map",
            "topic": "C_i routing",
            "result": "Coulomb_and_nuclear_coefficients_route_to_btheta_first",
            "reason": "ordinary composition charges are matter-constant sensitivities unless a non-universal source-normalization term exists",
            "next_action": "do not use WEP to bound b_kappa without source-normalization proof",
        },
        {
            "decision_id": "DEC986_1_kappa",
            "topic": "b_kappa",
            "result": "universal_kappa_cancels_nonuniversal_kappa_not_derived",
            "reason": "baseline kappa is GR-like and composition blind; WEP-visible b_kappa requires an extra source charge",
            "next_action": "attack parent-zero theorem or keep S_source as finite placeholder",
        },
        {
            "decision_id": "DEC986_2_best_next",
            "topic": "next checkpoint",
            "result": "Coulomb_to_alphaEM_normal_form_or_parent_zero_gate",
            "reason": "C_C -> b_theta_alpha_EM is the cleanest finite route, while parent-zero remains the cleanest GR route",
            "next_action": "write 987 Coulomb-to-alphaEM normal-form attempt, with parent-zero gate retained",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "987-Y5-R10-Coulomb-to-alphaEM-normal-form-or-parent-zero-gate.md",
            "objective": "derive whether the imported Coulomb WEP coefficient maps to an MTS alpha_EM/matter-constant slot, or is zero under the parent universal-source branch",
            "include": "EM/fine-structure normal form, Coulomb proxy route, profile normalization placeholders, parent-zero gate",
            "exclude": "WEP pass, invented C_i values, b_kappa claim without source-normalization proof, GitHub action, formalization-workbench edits",
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
    parent_zero: list[dict[str, str]],
    maps: list[dict[str, str]],
    slots: list[dict[str, str]],
    obligations: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    parent_verdict_ok = any(row["theorem_id"] == "PZT986_3_verdict" and row["result"] == "ZERO_THEOREM_RELATIVE_NOT_PARENT_SIGNED" for row in parent_zero)
    maps_nonclaim_ok = all(row["valid_for_claim"] == "false" for row in maps)
    slot_gates_safe_ok = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in slots)
    obligations_ok = all(row["current_status"] == "open" for row in obligations)
    claims_safe_ok = all(row["claim_allowed"] == "false" for row in claims)
    next_decision_ok = any(row["decision_id"] == "DEC986_2_best_next" and row["result"] == "Coulomb_to_alphaEM_normal_form_or_parent_zero_gate" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V986_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all source files exist and needles are found"},
        {"check_id": "V986_1_parent_zero_verdict", "result": "pass" if parent_verdict_ok else "fail", "detail": "parent-zero theorem remains relative and unsigned"},
        {"check_id": "V986_2_maps_nonclaim", "result": "pass" if maps_nonclaim_ok else "fail", "detail": "C_i-to-slot rows are nonclaim"},
        {"check_id": "V986_3_slot_gates_safe", "result": "pass" if slot_gates_safe_ok else "fail", "detail": "slot gates do not allow claims"},
        {"check_id": "V986_4_obligations_open", "result": "pass" if obligations_ok else "fail", "detail": "proof obligations remain explicit and open"},
        {"check_id": "V986_5_claim_gates_safe", "result": "pass" if claims_safe_ok else "fail", "detail": "claim gates block WEP/local-GR claims"},
        {"check_id": "V986_6_next_decision", "result": "pass" if next_decision_ok else "fail", "detail": "987 Coulomb-to-alphaEM/parent-zero target selected"},
        {"check_id": "V986_7_next_target_written", "result": "pass" if next_ok else "fail", "detail": "next target row is present and nonclaim"},
        {"check_id": "V986_8_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {"check_id": "V986_READY", "result": "pass" if ready else "fail", "detail": "986 checkpoint pack validation summary", "generated_utc": stamp()}
    ]


def write_doc(
    sources: list[dict[str, str]],
    parent_zero: list[dict[str, str]],
    maps: list[dict[str, str]],
    slots: list[dict[str, str]],
    obligations: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 986 Y5 R10: C_i To MTS Slot Map Or Parent Zero Theorem",
        "",
        "Status: `Y5_R10_986_Ci_to_MTS_slot_map_skeleton_written_universal_kappa_cancels_bkappa_not_bound_Coulomb_to_btheta_next`",
        "",
        "Claim ceiling: no WEP pass, no `b_theta` bound, no `b_kappa` bound, no source-charge theorem-zero promotion, and no local-GR claim.",
        "",
        "## Readout",
        "",
        "986 answers the routing question. Ordinary composition-dependent WEP charges do not automatically map to `b_kappa`. A universal `kappa` cancels in differential free fall. WEP-visible `b_kappa` requires a non-universal source-normalization term, species-weighted coupling, or material marker. That is not derived.",
        "",
        "The clean finite route is instead `C_C -> b_theta_alpha_EM`: Coulomb binding is an EM/fine-structure sensitivity. Nuclear/neutron-excess directions route to matter-constant or mass-ratio slots. Marker/source-normalization routes stay as placeholders until the parent action owns them.",
        "",
        "So the boxing scorecard is: good footwork, no haymaker yet. We have the map skeleton, but not a scored WEP coefficient.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Parent Zero Theorem Gate",
        "",
        md_table(parent_zero, ["theorem_id", "statement", "result", "MTS_slot_effect", "missing_for_claim", "valid_for_claim"]),
        "",
        "## C_i To MTS Slot Map",
        "",
        md_table(maps, ["map_id", "phenomenological_coefficient", "basis_feature", "primary_MTS_slot", "route_formula", "derivation_status", "why", "missing_inputs", "valid_for_claim"]),
        "",
        "## Slot Claim Gates",
        "",
        md_table(slots, ["gate_id", "slot", "best_current_route", "gate_result", "claim_allowed", "why_not", "valid_for_claim"]),
        "",
        "## Proof Obligations",
        "",
        md_table(obligations, ["obligation_id", "needed_for", "proof_task", "current_status", "next_action"]),
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
    parent_zero = parent_zero_theorem_rows()
    maps = ci_to_slot_map_rows()
    slots = slot_claim_gate_rows()
    obligations = proof_obligation_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, parent_zero, maps, slots, obligations, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_986_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_986_PARENT_ZERO_THEOREM_GATE.csv", parent_zero)
    write_csv(OUT / "P8_Y5_R10_986_CI_TO_MTS_SLOT_MAP.csv", maps)
    write_csv(OUT / "P8_Y5_R10_986_SLOT_CLAIM_GATES.csv", slots)
    write_csv(OUT / "P8_Y5_R10_986_PROOF_OBLIGATIONS.csv", obligations)
    write_csv(OUT / "P8_Y5_R10_986_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_986_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_986_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_986_VALIDATION.csv", validation)
    write_doc(sources, parent_zero, maps, slots, obligations, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
