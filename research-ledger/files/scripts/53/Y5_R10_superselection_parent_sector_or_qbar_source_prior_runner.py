from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "978-Y5-R10-superselection-parent-sector-or-qbar-source-prior-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    since = SCRIPT_START_UTC.timestamp()
    count = 0
    try:
        for directory, _subdirs, filenames in os.walk(FORMALIZATION):
            for filename in filenames:
                path = Path(directory) / filename
                try:
                    if path.stat().st_mtime > since:
                        count += 1
                except OSError:
                    return -2
    except OSError:
        return -2
    return count


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "977_doc",
            "path": "977-Y5-R10-constant-source-universality-certificate-or-K-boundary-alpha3-source.md",
            "role": "handoff selecting superselection/topological sector or qbar prior runner",
            "needle": "978-Y5-R10-superselection-parent-sector-or-qbar-source-prior-runner.md",
        },
        {
            "source_id": "977_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_977_SUPERSELECTION_GATE.csv",
            "role": "parent superselection gate blockers",
            "needle": "SSG977_4_single_global_kappa",
        },
        {
            "source_id": "977_priors",
            "path": "source-intake/mts_residuals/P8_Y5_R10_977_RESIDUAL_PRIOR_UPDATE.csv",
            "role": "qbar/source prior status after constant-source certificate",
            "needle": "RPU977_2_b_kappa",
        },
        {
            "source_id": "977_counterexamples",
            "path": "source-intake/mts_residuals/P8_Y5_R10_977_COUNTEREXAMPLE_AUDIT.csv",
            "role": "constant/source counterexamples retained",
            "needle": "CEA977_3_running_kappa",
        },
        {
            "source_id": "453_doc",
            "path": "453-global-coupling-superselection-parent-action-contract.md",
            "role": "global kappa superselection/topological zero-form route",
            "needle": "P1_topological_zero_form",
        },
        {
            "source_id": "452_doc",
            "path": "452-constant-universal-Geff-kappa-identity-attempt.md",
            "role": "Bianchi exposes running kappa as residual",
            "needle": "Bianchi_limit",
        },
        {
            "source_id": "448_doc",
            "path": "448-constant-sector-universality-theorem-attempt.md",
            "role": "theta_A representation data and theta_A(I_Q) warning",
            "needle": "quotient_invariance_not_overclaimed",
        },
        {
            "source_id": "576_priors",
            "path": "source-intake/mts_residuals/P8_Y5_R10_576_QBAR_ENVELOPE_TRIGGER.csv",
            "role": "finite qbar envelope formula and trigger",
            "needle": "QE576_0_qbar_retained",
        },
        {
            "source_id": "576_premises",
            "path": "source-intake/mts_residuals/P8_Y5_R10_576_UNIVERSALITY_PREMISE_LEDGER.csv",
            "role": "P576 premises for qbar zero",
            "needle": "P576_8_qbar_zero_gate",
        },
        {
            "source_id": "621_doc",
            "path": "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
            "role": "matter-coupling normal-form priors",
            "needle": "CP621_6_post_readout_EFT",
        },
        {
            "source_id": "622_doc",
            "path": "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
            "role": "prior runner schema and status policy",
            "needle": "SP622_6_EFT",
        },
        {
            "source_id": "constant_sector_contract",
            "path": "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
            "role": "constant-sector contract",
            "needle": "C1_superselection_independence",
        },
        {
            "source_id": "kappa_contract",
            "path": "source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv",
            "role": "constant kappa contract",
            "needle": "CU1_global_coupling_status",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "alpha3 fallback anchor",
            "needle": "alpha3_flux",
        },
    ]
    rows = []
    for spec in specs:
        absolute_path = source_path(spec["path"])
        exists = absolute_path.exists()
        needle_found = spec["needle"] in read_text(absolute_path) if exists else False
        rows.append(
            {
                **spec,
                "absolute_path": str(absolute_path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_sector_attempt() -> list[dict[str, str]]:
    specs = [
        {
            "sector_id": "PSA978_0_sector_decomposition",
            "mechanism": "parent configuration decomposes into dynamical local fields plus global sector labels",
            "mathematical_form": "Conf_parent = disjoint_union_{Theta,kappa} Conf_dyn(Theta,kappa); local variations tangent only to Conf_dyn",
            "result": "VALID_EXPLICIT_PARENT_CONTRACT",
            "closes_if_parent_owned": "delta_local theta_A=0 and delta_local kappa=0 by domain definition",
            "remaining_gap": "this is a parent-sector clause, not derived from earlier MTS primitives",
        },
        {
            "sector_id": "PSA978_1_theta_representation_functor",
            "mechanism": "theta_A live in a matter representation/superselection category",
            "mathematical_form": "Matter_A: Rep_A x ObsGeom -> Actions, with theta_A in Rep_A and no map I_loc(Q_MTS)->Rep_A",
            "result": "CLEAN_THETA_ROUTE_CONDITIONAL",
            "closes_if_parent_owned": "L_X theta_A=L_IQ theta_A=L_m theta_A=0",
            "remaining_gap": "no parent proof forbids theta_A(I_Q,m) functors or material-marker extensions",
        },
        {
            "sector_id": "PSA978_2_kappa_global_sector",
            "mechanism": "one gravitational kappa belongs to a global coupling sector, not to matter species",
            "mathematical_form": "kappa in K_global, E_munu=kappa T_munu; no kappa_A and no kappa(Z,I_Q,A,lambda,r,t)",
            "result": "CLEAN_KAPPA_ROUTE_CONDITIONAL",
            "closes_if_parent_owned": "species/source/range/frame derivatives of kappa vanish",
            "remaining_gap": "single global kappa is still a parent choice unless generated by a deeper sector theorem",
        },
        {
            "sector_id": "PSA978_3_topological_zero_form_kappa",
            "mechanism": "topological zero-form sector forces d kappa=0",
            "mathematical_form": "S_top[kappa,A3]=int A3 wedge d kappa, so delta_A3 S_top gives d kappa=0",
            "result": "PROMISING_MECHANISM_NOT_PARENT_SIGNED",
            "closes_if_parent_owned": "spacetime/radial/time gradients of kappa vanish on connected local domains",
            "remaining_gap": "does not by itself prove species-blindness, no MTS-invariant sector dependence, boundary policy, or measured-GM calibration",
        },
        {
            "sector_id": "PSA978_4_topological_theta_zero_forms",
            "mechanism": "optional topological zero-form constants for matter parameters",
            "mathematical_form": "S_top[theta_A,B3_A]=int B3_A wedge d theta_A",
            "result": "DANGEROUS_AS_FULL_SOLUTION",
            "closes_if_parent_owned": "local gradients of theta_A vanish",
            "remaining_gap": "does not forbid species-specific constants or theta_A as marker-dependent sector labels; risks overbuilding particle physics into closure",
        },
        {
            "sector_id": "PSA978_5_no_marker_functor_needed",
            "mechanism": "superselection only works if no local marker functor selects sector labels",
            "mathematical_form": "Hom(I_loc(Q_MTS), Theta_sector)=Const only",
            "result": "KEY_UNPROVED_CLAUSE",
            "closes_if_parent_owned": "theta_A(I_Q,m) and kappa(I_Q,m) counterexamples die",
            "remaining_gap": "same no-extension/local-invariant-algebra problem remains",
        },
        {
            "sector_id": "PSA978_6_verdict",
            "mechanism": "superselection/topological parent sector",
            "mathematical_form": "global sector + topological zero-form can make constants local-invariant, but only with no-marker/no-extension and one-kappa clauses",
            "result": "MECHANISM_CONSTRUCTED_AS_CONTRACT_PARENT_UNSIGNED",
            "closes_if_parent_owned": "would support b_theta=0 and b_kappa=0 in the local branch",
            "remaining_gap": "not a qbar/local-GR claim; parent ownership and marker exclusion remain open",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def topological_kappa_audit() -> list[dict[str, str]]:
    specs = [
        {
            "audit_id": "TKA978_0_local_gradient",
            "test": "does topological zero-form kill local kappa gradients?",
            "result": "CONDITIONAL_PASS",
            "reason": "delta_A3 of int A3 wedge d kappa gives d kappa=0",
            "unclosed_risk": "requires actual parent A3 sector and boundary condition",
        },
        {
            "audit_id": "TKA978_1_species_blindness",
            "test": "does topological zero-form forbid species-weighted kappa_A?",
            "result": "FAIL_AS_STANDALONE",
            "reason": "one could add several topological constants kappa_A unless the parent has one shared gravitational coupling",
            "unclosed_risk": "source-charge residual survives",
        },
        {
            "audit_id": "TKA978_2_MTS_invariant_dependence",
            "test": "does d kappa=0 forbid kappa sector selection by I_Q or marker m?",
            "result": "FAIL_AS_STANDALONE",
            "reason": "an integration constant can still label different sectors unless no local marker functor selects sectors",
            "unclosed_risk": "theta/kappa marker dependence returns as sector dependence",
        },
        {
            "audit_id": "TKA978_3_metric_stress",
            "test": "does A3 wedge d kappa add local metric stress?",
            "result": "CONDITIONAL_PASS",
            "reason": "pure wedge topological term is metric independent",
            "unclosed_risk": "coupling kappa to EH/source still affects metric equations; must keep same-frame EH/source contract",
        },
        {
            "audit_id": "TKA978_4_boundary",
            "test": "does topological kappa close boundary alpha3 flux?",
            "result": "FAIL_AS_STANDALONE",
            "reason": "constant kappa does not prove boundary no-flux or K_boundary_alpha3=0",
            "unclosed_risk": "alpha3 fallback remains live",
        },
        {
            "audit_id": "TKA978_5_verdict",
            "test": "topological kappa route readiness",
            "result": "USEFUL_PARENT_MECHANISM_NOT_FULL_CERTIFICATE",
            "reason": "it can kill d kappa but not the full source-universality stack",
            "unclosed_risk": "one-kappa, no-marker sector, measured-GM, non-Hilbert current, and boundary flux remain",
        },
    ]
    return [
        {
            **spec,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def qbar_source_prior_runner_rows() -> list[dict[str, str]]:
    specs = [
        {
            "prior_id": "QSP978_0_common_frame",
            "parameter": "common_frame_log_derivative",
            "component": "b_g",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
            "bound_channel": "R0/R2/R11 frame/source compatibility",
            "reason": "observed coframe factorization remains unsigned",
        },
        {
            "prior_id": "QSP978_1_alpha_EM",
            "parameter": "d_ln_alpha_EM_dXhat",
            "component": "b_theta",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless per Xhat",
            "source_path": "448-constant-sector-universality-theorem-attempt.md",
            "bound_channel": "clock/fine-structure/EM spectra",
            "reason": "theta_A representation data not parent-derived",
        },
        {
            "prior_id": "QSP978_2_mass_ratio",
            "parameter": "d_ln_mass_ratio_dXhat",
            "component": "b_theta",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless per Xhat",
            "source_path": "448-constant-sector-universality-theorem-attempt.md",
            "bound_channel": "clock/WEP/mass-ratio tests",
            "reason": "matter constants may still depend on MTS invariants or markers",
        },
        {
            "prior_id": "QSP978_3_marker_coupling",
            "parameter": "marker_coupling_projection",
            "component": "b_m",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "977-Y5-R10-constant-source-universality-certificate-or-K-boundary-alpha3-source.md",
            "bound_channel": "WEP/source-charge/R10",
            "reason": "no-extension/no-marker functor remains unproved",
        },
        {
            "prior_id": "QSP978_4_species_source_weight",
            "parameter": "species_source_weight_splitting",
            "component": "b_kappa",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "452-constant-universal-Geff-kappa-identity-attempt.md",
            "bound_channel": "WEP/source-normalization",
            "reason": "single global kappa not parent-derived",
        },
        {
            "prior_id": "QSP978_5_running_kappa",
            "parameter": "d_ln_Geff_dXhat_or_dlnGdt",
            "component": "b_kappa",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless per Xhat or yr^-1",
            "source_path": "452-constant-universal-Geff-kappa-identity-attempt.md",
            "bound_channel": "Gdot/range/radial/fifth-force",
            "reason": "topological/global kappa mechanism not parent-signed",
        },
        {
            "prior_id": "QSP978_6_nonHilbert_current",
            "parameter": "nonHilbert_current_projection",
            "component": "b_NH",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless source projection",
            "source_path": "449-source-current-Ward-universality-theorem-attempt.md",
            "bound_channel": "boundary/bulk/domain/memory/source residuals",
            "reason": "Hilbert current identity does not zero retained currents",
        },
        {
            "prior_id": "QSP978_7_qbarXT_vec",
            "parameter": "P_A_qbarXT_vec",
            "component": "qbarXT_vec",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless charge per inertial mass",
            "source_path": "576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md",
            "bound_channel": "R10/WEP/local source",
            "reason": "aggregate qbar remains finite until all zero components close or are bounded",
        },
        {
            "prior_id": "QSP978_8_K_boundary_alpha3",
            "parameter": "K_boundary_alpha3",
            "component": "boundary_alpha3_flux",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless projection coefficient",
            "source_path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "bound_channel": "PPN alpha3",
            "reason": "boundary flux not affected by superselection kappa alone",
        },
    ]
    return [
        {
            **spec,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def qbar_runner_gate() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "QRG978_0_schema",
            "requirement": "all prior rows expose parameter, component, status, value, units, source_path, bound_channel",
            "gate_result": "pass",
            "blocks_claim": "false",
            "detail": "schema row written for future executable runner",
        },
        {
            "gate_id": "QRG978_1_missing_markers",
            "requirement": "symbolic rows with MISSING_PARENT_INPUT cannot be claim-ready",
            "gate_result": "pass",
            "blocks_claim": "true",
            "detail": "all finite priors are placeholders until parent theorem or numeric values exist",
        },
        {
            "gate_id": "QRG978_2_zero_return",
            "requirement": "only derived parent certificate may move a component to derive_zero",
            "gate_result": "pass",
            "blocks_claim": "true",
            "detail": "topological/superselection mechanism is not parent-signed yet",
        },
        {
            "gate_id": "QRG978_3_numeric_bound_return",
            "requirement": "numeric_bound rows require value, units, source path, observable map, and accepted bound",
            "gate_result": "pass",
            "blocks_claim": "true",
            "detail": "no numeric finite qbar/source values are supplied in 978",
        },
        {
            "gate_id": "QRG978_4_local_GR_guard",
            "requirement": "finite qbar/source runner pass would not equal local-GR pass by itself",
            "gate_result": "pass",
            "blocks_claim": "true",
            "detail": "measured-GM, PPN, operator, boundary, and conservation gates remain separate",
        },
    ]
    return [
        {
            **spec,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def claim_gates() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "CGATE978_0_superselection_parent_sector",
            "claim": "parent superselection/topological sector is derived",
            "current_evidence": "mechanism constructed as contract only",
            "gate_pass": "false",
            "why_not_claim": "parent category/no-marker functor and topological boundary policy are not signed",
        },
        {
            "gate_id": "CGATE978_1_theta_kappa_zero",
            "claim": "b_theta and b_kappa are theorem-zero",
            "current_evidence": "relative mechanism could close them if parent-owned",
            "gate_pass": "false",
            "why_not_claim": "theta(I_Q,m), kappa_A, and sector-selection counterexamples remain legal",
        },
        {
            "gate_id": "CGATE978_2_qbar_runner_claim",
            "claim": "finite qbar/source prior runner has scoreable rows",
            "current_evidence": "placeholder rows written with MISSING_PARENT_INPUT",
            "gate_pass": "false",
            "why_not_claim": "no numeric values, source-backed coefficients, or derived-zero rows",
        },
        {
            "gate_id": "CGATE978_3_K_alpha3",
            "claim": "K_boundary_alpha3 is scoreable",
            "current_evidence": "placeholder row only",
            "gate_pass": "false",
            "why_not_claim": "K/Phi/projection normalization missing",
        },
        {
            "gate_id": "CGATE978_4_local_GR",
            "claim": "local GR/Newton reduction follows",
            "current_evidence": "parent sector and qbar/source rows remain nonclaim",
            "gate_pass": "false",
            "why_not_claim": "source, measured-GM, PPN, operator, boundary, and no-marker gates remain open",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def decisions() -> list[dict[str, str]]:
    specs = [
        {
            "decision_id": "DEC978_0_mechanism",
            "topic": "superselection/topological parent sector",
            "result": "mechanism_constructed_as_contract_parent_unsigned",
            "reason": "sector decomposition and A3 wedge d kappa can explain constant kappa locally, but no-marker/no-extension and one-kappa ownership remain unproved",
            "next_action": "either parent-sign this sector in a future action spine or keep finite priors",
        },
        {
            "decision_id": "DEC978_1_theta",
            "topic": "matter constants",
            "result": "representation_functor_route_conditional",
            "reason": "theta_A as Rep_A data is clean and does not require all constants to be equal, but theta_A(I_Q,m) is still legal without no-marker functor proof",
            "next_action": "connect representation functor to parent category or source clock/EM priors",
        },
        {
            "decision_id": "DEC978_2_kappa",
            "topic": "global coupling",
            "result": "topological_zero_form_promising_but_incomplete",
            "reason": "d kappa=0 can be generated, but species-blindness and sector-selection are extra clauses",
            "next_action": "decide whether to write this as explicit parent action spine clause or demote to residual runner",
        },
        {
            "decision_id": "DEC978_3_priors",
            "topic": "finite qbar/source priors",
            "result": "placeholder_runner_rows_written_nonclaim",
            "reason": "derive-first route remains alive but not closed; finite branch now has rows ready for future numeric sourcing",
            "next_action": "if derivation stalls, source numeric bounds/coefficients for the highest-risk priors",
        },
        {
            "decision_id": "DEC978_4_best_next",
            "topic": "next checkpoint",
            "result": "parent_action_spine_clause_or_first_numeric_qbar_prior",
            "reason": "we now have the explicit coupling mechanism; the next move is either to insert it openly into the parent action spine or start numeric sourcing",
            "next_action": "write 979 parent action spine clause for superselection/topological constants, with closure label if not derived",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "979-Y5-R10-parent-action-spine-superselection-clause-or-first-qbar-prior-source.md",
            "objective": "write the explicit parent-action spine clause for theta/kappa superselection/topological constants, labelled as derived only if parent-owned; otherwise begin sourcing the first finite qbar/source prior",
            "include": "Conf_parent sector decomposition, theta_A representation functor, kappa A3 zero-form term, no-marker functor gate, qbar prior source priority",
            "exclude": "qbar theorem-zero, local-GR claim, invented numeric priors, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    sector_rows: list[dict[str, str]],
    topological_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    runner_gate_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    formalization_count = formalization_changed_after_start()
    rows = [
        {
            "check_id": "V978_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail",
            "detail": "all cited local source paths exist",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V978_1_source_needles_found",
            "result": "pass" if all(row["needle_found"] == "true" for row in sources) else "fail",
            "detail": "all source needles found",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V978_2_parent_sector_mechanism_written",
            "result": "pass"
            if any(row["sector_id"] == "PSA978_6_verdict" and row["result"] == "MECHANISM_CONSTRUCTED_AS_CONTRACT_PARENT_UNSIGNED" for row in sector_rows)
            else "fail",
            "detail": "superselection/topological mechanism is written as parent-unsigned contract",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V978_3_topological_limits_recorded",
            "result": "pass"
            if any(row["audit_id"] == "TKA978_5_verdict" and row["result"] == "USEFUL_PARENT_MECHANISM_NOT_FULL_CERTIFICATE" for row in topological_rows)
            else "fail",
            "detail": "topological kappa limitations are recorded",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V978_4_qbar_prior_rows_nonclaim",
            "result": "pass"
            if all(row["valid_for_claim"] == "false" and row["status"] == "symbolic_placeholder" and row["value"] == "MISSING_PARENT_INPUT" for row in prior_rows)
            else "fail",
            "detail": "all qbar/source prior rows are placeholders and nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V978_5_runner_gates_block_claim",
            "result": "pass" if any(row["gate_id"] == "QRG978_4_local_GR_guard" and row["blocks_claim"] == "true" for row in runner_gate_rows) else "fail",
            "detail": "runner gates block local-GR overclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V978_6_claim_gates_false",
            "result": "pass" if all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows) else "fail",
            "detail": "all superselection/qbar/local-GR claim gates remain false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V978_7_decisions_nonclaim",
            "result": "pass" if all(row["claim_allowed"] == "false" for row in decision_rows) else "fail",
            "detail": "decision ledger remains nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V978_8_next_target_written",
            "result": "pass" if len(target_rows) == 1 and target_rows[0]["valid_for_claim"] == "false" else "fail",
            "detail": "979 parent-action spine or first qbar prior source target selected",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V978_9_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
            "generated_utc": stamp(),
        },
    ]
    rows.append(
        {
            "check_id": "V978_READY",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "978 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    sector_rows: list[dict[str, str]],
    topological_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    runner_gate_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 978 Y5 R10: Superselection Parent Sector Or Qbar Source Prior Runner

Status: `Y5_R10_978_superselection_topological_mechanism_constructed_as_parent_unsigned_contract_qbar_prior_rows_written_nonclaim`

Claim ceiling: no parent superselection theorem, no `theta_A`/`kappa` zero promotion, no `qbar_XT=0`, no alpha3 pass, no R10/PPN pass, and no EH/Newton/local-GR claim is made.

## Readout

978 builds the missing coupling mechanism in explicit parent-action language.

The clean parent-sector shape is:

`Conf_parent = disjoint_union_{{Theta,kappa}} Conf_dyn(Theta,kappa)`.

Local variations are tangent to `Conf_dyn`, not to the global sector labels. If `theta_A` lives in a matter representation/superselection category and `kappa` lives in one shared gravitational coupling sector, then local MTS directions do not act on them.

For `kappa`, there is also a plausible topological zero-form mechanism:

`S_top[kappa,A3] = int A3 wedge d kappa`.

Varying `A3` gives `d kappa=0`, so local time/radius/range gradients are killed on connected local domains.

That is useful. It is not the whole theorem. It does not by itself prove one species-blind `kappa`, forbid sector selection by `I_Q` or material markers, calibrate Hilbert mass to measured `GM`, zero non-Hilbert source currents, or close boundary alpha3 flux. So the mechanism is a strong candidate parent-spine clause, not a local-GR derivation.

Because the parent ownership is still unsigned, 978 also writes finite `qbar`/source prior rows as symbolic placeholders. They are deliberately nonclaim and blocked by `MISSING_PARENT_INPUT`.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Parent Sector Attempt

{md_table(sector_rows, ["sector_id", "mechanism", "result", "closes_if_parent_owned", "remaining_gap"])}

## Topological Kappa Audit

{md_table(topological_rows, ["audit_id", "test", "result", "reason", "unclosed_risk"])}

## Qbar Source Prior Runner Rows

{md_table(prior_rows, ["prior_id", "parameter", "component", "status", "value", "units", "bound_channel", "reason", "valid_for_claim"])}

## Qbar Runner Gate

{md_table(runner_gate_rows, ["gate_id", "requirement", "gate_result", "blocks_claim", "detail"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed", "why_not_claim"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    sector_rows = parent_sector_attempt()
    topological_rows = topological_kappa_audit()
    prior_rows = qbar_source_prior_runner_rows()
    runner_gate_rows = qbar_runner_gate()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        sector_rows,
        topological_rows,
        prior_rows,
        runner_gate_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_978_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_978_PARENT_SECTOR_ATTEMPT.csv",
        sector_rows,
        ["sector_id", "mechanism", "mathematical_form", "result", "closes_if_parent_owned", "remaining_gap", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_978_TOPOLOGICAL_KAPPA_AUDIT.csv",
        topological_rows,
        ["audit_id", "test", "result", "reason", "unclosed_risk", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_978_QBAR_SOURCE_PRIOR_RUNNER_ROWS.csv",
        prior_rows,
        ["prior_id", "parameter", "component", "status", "value", "units", "source_path", "bound_channel", "reason", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_978_QBAR_RUNNER_GATE.csv",
        runner_gate_rows,
        ["gate_id", "requirement", "gate_result", "blocks_claim", "detail", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_978_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed", "why_not_claim", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_978_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_978_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_978_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(
        sources,
        sector_rows,
        topological_rows,
        prior_rows,
        runner_gate_rows,
        claim_rows,
        decision_rows,
        target_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()
