from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "977-Y5-R10-constant-source-universality-certificate-or-K-boundary-alpha3-source.md"
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
            "source_id": "976_doc",
            "path": "976-Y5-R10-readout-parent-domain-audit-or-K-boundary-alpha3-source.md",
            "role": "handoff selecting constant/source universality or K_boundary_alpha3",
            "needle": "977-Y5-R10-constant-source-universality-certificate-or-K-boundary-alpha3-source.md",
        },
        {
            "source_id": "976_residual_update",
            "path": "source-intake/mts_residuals/P8_Y5_R10_976_RESIDUAL_COMPONENT_UPDATE.csv",
            "role": "post-readout residual components still open",
            "needle": "RCU976_2_b_theta",
        },
        {
            "source_id": "575_constant_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_575_CONSTANT_SOURCE_LOCK_CONTRACT.csv",
            "role": "constant/source lock clauses after readout hygiene",
            "needle": "CL575_1_trivial_MTS_action",
        },
        {
            "source_id": "576_doc",
            "path": "576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md",
            "role": "prior constant/source-current derivation attempt",
            "needle": "Y5_R10_constant_source_current_universality_attempt_conditional_sublemma_only_qbar_XT_retained",
        },
        {
            "source_id": "576_derivation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_576_CONSTANT_SOURCE_DERIVATION_ATTEMPT.csv",
            "role": "qbar_XT zero derivation chain and blockers",
            "needle": "D576_7_verdict",
        },
        {
            "source_id": "576_premises",
            "path": "source-intake/mts_residuals/P8_Y5_R10_576_UNIVERSALITY_PREMISE_LEDGER.csv",
            "role": "constant/source universality premise ledger",
            "needle": "P576_8_qbar_zero_gate",
        },
        {
            "source_id": "576_counterexamples",
            "path": "source-intake/mts_residuals/P8_Y5_R10_576_SOURCE_CURRENT_COUNTEREXAMPLES.csv",
            "role": "theta(I_Q), species kappa, running kappa, non-Hilbert counterexamples",
            "needle": "CE576_1_species_weighted_kappa",
        },
        {
            "source_id": "448_doc",
            "path": "448-constant-sector-universality-theorem-attempt.md",
            "role": "constant-sector universality route and theta_A(I_Q) warning",
            "needle": "constant_sector_parent_derived",
        },
        {
            "source_id": "449_doc",
            "path": "449-source-current-Ward-universality-theorem-attempt.md",
            "role": "Hilbert source-current Ward universality conditional theorem",
            "needle": "species_weighted_source_equation",
        },
        {
            "source_id": "452_doc",
            "path": "452-constant-universal-Geff-kappa-identity-attempt.md",
            "role": "constant universal kappa/G_eff identity and Bianchi residual",
            "needle": "conditional_global_coupling_theorem",
        },
        {
            "source_id": "453_doc",
            "path": "453-global-coupling-superselection-parent-action-contract.md",
            "role": "global/superselection kappa parent-action contract",
            "needle": "P1_topological_zero_form",
        },
        {
            "source_id": "constant_sector_contract",
            "path": "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
            "role": "constant-sector formal contract",
            "needle": "C1_superselection_independence",
        },
        {
            "source_id": "kappa_contract",
            "path": "source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv",
            "role": "constant universal G_eff/kappa contract",
            "needle": "CU1_global_coupling_status",
        },
        {
            "source_id": "source_owner_contract",
            "path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "role": "source-owner parent action terms and constant coupling block",
            "needle": "A5_constant_universal_coupling",
        },
        {
            "source_id": "ward_owner_contract",
            "path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
            "role": "Ward/source owner identity requirements",
            "needle": "C4_constant_universal_coupling",
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


def constant_source_certificate_attempt() -> list[dict[str, str]]:
    specs = [
        {
            "step_id": "CSC977_0_chain_rule_target",
            "claim_piece": "test-body X charge vanishes",
            "mathematical_form": "qbar_XT=M_T^-1 delta_X S_T=0",
            "result": "TARGET_RESTATED",
            "proof_status": "requires observed coframe blindness plus constant/source universality",
            "gap": "qbar_XT cannot be inferred from readout hygiene alone",
        },
        {
            "step_id": "CSC977_1_theta_representation_data",
            "claim_piece": "matter constants are representation/superselection labels",
            "mathematical_form": "theta_A in Rep_A, not theta_A(X,I_Q,m,h)",
            "result": "VALID_RELATIVE_THEOREM",
            "proof_status": "if parent matter functor takes theta_A only as fixed representation data, then L_X theta_A=0",
            "gap": "current corpus does not parent-derive Rep_A independence from MTS invariants/material markers",
        },
        {
            "step_id": "CSC977_2_no_constant_vertices",
            "claim_piece": "no direct MTS-dependent matter constants",
            "mathematical_form": "no alpha_EM(X)F^2, no m_A(X), no q_A X_mu J_A^mu, no theta_A(I_Q,m)",
            "result": "CONTRACT_CLEAR_NOT_PARENT_DERIVED",
            "proof_status": "forbidden-vertex list is exact enough to audit future parent actions",
            "gap": "currently a branch policy/contract, not a theorem from primitives",
        },
        {
            "step_id": "CSC977_3_hilbert_source_current",
            "claim_piece": "ordinary active source is the Hilbert/coframe current",
            "mathematical_form": "tau_a^mu=det(e)^-1 delta S_matter/delta e_mu^a; T_munu=e_(mu)^a tau_{nu)a}",
            "result": "CONDITIONAL_STANDARD_IDENTITY",
            "proof_status": "Ward identities give a conserved source current when matter sees one observed coframe and no extra source arguments",
            "gap": "does not kill species-weighted kappa_A or non-Hilbert currents by itself",
        },
        {
            "step_id": "CSC977_4_single_universal_kappa",
            "claim_piece": "field equation uses one global/superselection coupling",
            "mathematical_form": "E_munu[g_obs]=kappa_univ sum_A T_A_munu, not sum_A kappa_A T_A_munu",
            "result": "VALID_RELATIVE_THEOREM",
            "proof_status": "if kappa is global/superselection/topological constant and species-blind, b_kappa=0",
            "gap": "current corpus has a contract, not a parent derivation of global/superselection kappa",
        },
        {
            "step_id": "CSC977_5_bianchi_limit",
            "claim_piece": "Bianchi does not automatically derive constant kappa",
            "mathematical_form": "nabla_mu E^{mu nu}=0 maps local grad kappa to T_obs^{mu nu} nabla_mu kappa residual unless separate conservation/no-exchange closes",
            "result": "OVERCLAIM_BLOCKER_RETAINED",
            "proof_status": "Bianchi can expose residuals; it cannot hide them",
            "gap": "exchange/source owner terms and boundary flux remain open",
        },
        {
            "step_id": "CSC977_6_measured_monopole_guard",
            "claim_piece": "Hilbert source universality is not measured orbital GM",
            "mathematical_form": "mu_obs=G_eff M_Hilbert + mu_extra",
            "result": "GUARDRAIL_PASS",
            "proof_status": "source-current progress stays separated from measured-GM/Newton/PPN claims",
            "gap": "mass-flux calibration, mu_extra zero, derivative hair, and beta stability remain open",
        },
        {
            "step_id": "CSC977_7_verdict",
            "claim_piece": "constant/source universality certificate",
            "mathematical_form": "theta_A fixed representation data + one global kappa + Hilbert source current => b_theta=b_kappa=0 and qbar_XT route can close if other qbar components also close",
            "result": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "proof_status": "the certificate shape is now exact",
            "gap": "not a qbar/local-GR claim; parent superselection and no marker/source extensions remain unsigned",
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


def superselection_gate() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "SSG977_0_theta_rep_data",
            "required_certificate": "theta_A are representation/superselection data, not MTS fields",
            "current_evidence": "448/575/576 state the route; no parent theorem",
            "gate_pass": "false",
            "missing_input": "MISSING_PARENT_REPRESENTATION_DATA_THEOREM",
        },
        {
            "gate_id": "SSG977_1_trivial_MTS_action",
            "required_certificate": "L_X theta_A=L_IQ theta_A=L_m theta_A=L_h theta_A=0",
            "current_evidence": "constant-sector contract C1; current status not parent-derived",
            "gate_pass": "false",
            "missing_input": "MISSING_TRIVIAL_MTS_ACTION_ON_CONSTANTS",
        },
        {
            "gate_id": "SSG977_2_no_constant_vertices",
            "required_certificate": "no direct MTS-dependent matter vertices at fixed observed coframe",
            "current_evidence": "contract/forbidden-vertex policy only",
            "gate_pass": "false",
            "missing_input": "MISSING_NO_DIRECT_CONSTANT_VERTEX_THEOREM",
        },
        {
            "gate_id": "SSG977_3_hilbert_source_owner",
            "required_certificate": "active ordinary source is the same Hilbert/coframe variation",
            "current_evidence": "Ward identity gives conditional standard current",
            "gate_pass": "false",
            "missing_input": "MISSING_PARENT_SOURCE_OWNER_CERTIFICATE",
        },
        {
            "gate_id": "SSG977_4_single_global_kappa",
            "required_certificate": "one global/superselection kappa, species/source/range/frame independent",
            "current_evidence": "452/453 contract; no parent derivation",
            "gate_pass": "false",
            "missing_input": "MISSING_GLOBAL_KAPPA_SUPERSELECTION_PROOF",
        },
        {
            "gate_id": "SSG977_5_no_nonHilbert_source",
            "required_certificate": "all non-Hilbert source currents are absent, exact-owned zero flux, or retained as scored residuals",
            "current_evidence": "source-owner contracts remain open",
            "gate_pass": "false",
            "missing_input": "MISSING_NONHILBERT_SOURCE_ZERO_OR_BOUND",
        },
        {
            "gate_id": "SSG977_6_boundary_alpha3",
            "required_certificate": "boundary alpha3 flux is theorem-zero or K_boundary_alpha3 is sourced",
            "current_evidence": "alpha3 anchor exists but K/Phi missing",
            "gate_pass": "false",
            "missing_input": "MISSING_K_BOUNDARY_ALPHA3_OR_NOFLUX_THEOREM",
        },
        {
            "gate_id": "SSG977_7_verdict",
            "required_certificate": "all constant/source superselection gates close",
            "current_evidence": "relative certificate only",
            "gate_pass": "false",
            "missing_input": "MISSING_CONSTANT_SOURCE_PARENT_CERTIFICATE",
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


def counterexample_audit() -> list[dict[str, str]]:
    specs = [
        {
            "counterexample_id": "CEA977_0_theta_IQ",
            "construction": "theta_A=theta_A0[1+epsilon_A I_Q]",
            "why_not_blocked": "quotient invariance does not imply trivial action on constants",
            "residual_activated": "clock/fine-structure/WEP/R10 constant-sector residuals",
            "required_blocker": "representation-data theorem plus no MTS constant vertices",
        },
        {
            "counterexample_id": "CEA977_1_theta_m",
            "construction": "theta_A=theta_A(m) for a co-moving material marker",
            "why_not_blocked": "material marker extension remains legal without no-extension theorem",
            "residual_activated": "species/source-charge and clock residuals",
            "required_blocker": "parent no-extension/minimality theorem",
        },
        {
            "counterexample_id": "CEA977_2_species_kappa",
            "construction": "E_munu=sum_A kappa_A T_A_munu with constant kappa_A",
            "why_not_blocked": "each T_A can be conserved, so Bianchi does not force kappa_A equality",
            "residual_activated": "source-charge/WEP/source-normalization residuals",
            "required_blocker": "single global kappa parent certificate",
        },
        {
            "counterexample_id": "CEA977_3_running_kappa",
            "construction": "kappa_eff=kappa0 F(Z,I_Q,C_D,lambda,r,t)",
            "why_not_blocked": "Bianchi maps gradients into exchange/source residuals",
            "residual_activated": "Gdot/range/radial/source hair",
            "required_blocker": "global or topological zero-form kappa derivation",
        },
        {
            "counterexample_id": "CEA977_4_nonHilbert_current",
            "construction": "q_res^nu=nabla_mu K_owner^{mu nu}+q_retained^nu with nonzero flux",
            "why_not_blocked": "total conservation does not set compact exterior flux to zero",
            "residual_activated": "boundary/bulk/domain/memory residual rows",
            "required_blocker": "source-owner zero-flux/no-hair theorem or scored residual",
        },
        {
            "counterexample_id": "CEA977_5_measured_GM_split",
            "construction": "mu_obs=G_eff M_Hilbert + mu_extra(lambda,r,A,t)",
            "why_not_blocked": "Hilbert source universality is not absolute orbital source calibration",
            "residual_activated": "measured-GM/Newton/PPN source-normalization rows",
            "required_blocker": "mass-flux calibration plus mu_extra zero",
        },
        {
            "counterexample_id": "CEA977_6_verdict",
            "construction": "all surviving constant/source branches",
            "why_not_blocked": "the parent superselection certificate is not yet derived",
            "residual_activated": "finite qbar/source envelope remains live",
            "required_blocker": "derive certificate or source finite priors",
        },
    ]
    return [
        {
            **spec,
            "counterexample_retained": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def residual_prior_update() -> list[dict[str, str]]:
    specs = [
        {
            "prior_id": "RPU977_0_b_EFT",
            "component": "post_readout_counterterm_projection",
            "status_after_977": "ABSENT_FROM_PARENT_DERIVED_BRANCH",
            "reason": "carried forward from 976 readout-domain hygiene",
            "claim_zero_now": "false",
            "required_next": "none unless phenomenology branch is intentionally opened",
        },
        {
            "prior_id": "RPU977_1_b_theta",
            "component": "constant-sector MTS derivative",
            "status_after_977": "RELATIVE_ZERO_CERTIFICATE_PARENT_UNSIGNED",
            "reason": "theta_A representation-data route would zero it, but parent theorem absent",
            "claim_zero_now": "false",
            "required_next": "derive representation/superselection parent sector or source clock/fine-structure priors",
        },
        {
            "prior_id": "RPU977_2_b_kappa",
            "component": "species/source/range kappa dependence",
            "status_after_977": "RELATIVE_ZERO_CERTIFICATE_PARENT_UNSIGNED",
            "reason": "single global/topological kappa route would zero it, but parent theorem absent",
            "claim_zero_now": "false",
            "required_next": "derive global/topological kappa or source Gdot/source/range priors",
        },
        {
            "prior_id": "RPU977_3_b_m",
            "component": "marker_coupling_projection",
            "status_after_977": "OPEN",
            "reason": "constant-source certificate does not kill material marker extension",
            "claim_zero_now": "false",
            "required_next": "no-extension/minimality theorem or finite marker coefficient",
        },
        {
            "prior_id": "RPU977_4_b_NH",
            "component": "nonHilbert_current_projection",
            "status_after_977": "OPEN",
            "reason": "Hilbert source current identity does not zero boundary/bulk/domain residual currents",
            "claim_zero_now": "false",
            "required_next": "source-owner zero-flux/no-hair theorem or coefficient row",
        },
        {
            "prior_id": "RPU977_5_K_boundary_alpha3",
            "component": "K_boundary_alpha3*Phi_boundary_local",
            "status_after_977": "OPEN_NON_SCOREABLE",
            "reason": "constant-source universality does not remove boundary alpha3 flux",
            "claim_zero_now": "false",
            "required_next": "derive boundary no-flux or source K/Phi values",
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


def k_boundary_alpha3_status() -> list[dict[str, str]]:
    specs = [
        {
            "row_id": "KBS977_0_alpha3_formula",
            "formula": "alpha3_MTS=K_boundary_alpha3*Phi_boundary_local",
            "known_input": "alpha3 bound anchor 4.000e-20 dimensionless from 417",
            "missing_input": "MISSING_K_BOUNDARY_ALPHA3;MISSING_PHI_BOUNDARY_LOCAL;MISSING_PROJECTION_NORMALIZATION",
            "status": "NON_SCOREABLE_FALLBACK",
        },
        {
            "row_id": "KBS977_1_no_effect_from_constant_source",
            "formula": "constant/source universality does not imply boundary flux zero",
            "known_input": "separate source-current and boundary-flux sectors",
            "missing_input": "MISSING_BOUNDARY_NOFLUX_THEOREM_OR_NUMERIC_BOUND_PASS",
            "status": "BOUNDARY_ROUTE_STILL_OPEN",
        },
        {
            "row_id": "KBS977_2_acceptance",
            "formula": "claim_allowed only if theorem-zero or abs(alpha3_MTS)<=4e-20 with sourced K/Phi",
            "known_input": "G507 theorem-zero/numeric-bound policy",
            "missing_input": "MISSING_EXECUTABLE_MTS_PREDICTION",
            "status": "FORCED_FALSE",
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
            "gate_id": "CGATE977_0_theta_zero",
            "claim": "constant-sector X derivatives vanish",
            "current_evidence": "relative representation-data certificate only",
            "gate_pass": "false",
            "why_not_claim": "theta_A(I_Q,m) counterexamples remain legal",
        },
        {
            "gate_id": "CGATE977_1_kappa_universal",
            "claim": "single global/superselection kappa is parent-derived",
            "current_evidence": "452/453 contract and relative theorem only",
            "gate_pass": "false",
            "why_not_claim": "species-weighted and running kappa branches remain legal",
        },
        {
            "gate_id": "CGATE977_2_qbarXT_zero",
            "claim": "qbar_XT is theorem-zero",
            "current_evidence": "b_theta/b_kappa relative routes are unsigned; b_m/b_NH/b_g also open",
            "gate_pass": "false",
            "why_not_claim": "all P576 premises do not close simultaneously",
        },
        {
            "gate_id": "CGATE977_3_alpha3_score",
            "claim": "K_boundary_alpha3 branch is scoreable",
            "current_evidence": "anchor only; K/Phi missing",
            "gate_pass": "false",
            "why_not_claim": "no executable MTS alpha3 prediction exists",
        },
        {
            "gate_id": "CGATE977_4_local_GR",
            "claim": "local GR/Newton reduction follows",
            "current_evidence": "constant/source certificate not parent-signed and boundary/source residuals open",
            "gate_pass": "false",
            "why_not_claim": "measured-GM, PPN, boundary, no-marker, and operator gates remain open",
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
            "decision_id": "DEC977_0_certificate",
            "topic": "constant/source universality",
            "result": "relative_certificate_ready_parent_unsigned",
            "reason": "theta_A as representation data plus one global/topological kappa would close b_theta and b_kappa, but parent has not derived those sectors",
            "next_action": "try to construct the parent superselection/topological sector explicitly",
        },
        {
            "decision_id": "DEC977_1_counterexamples",
            "topic": "constant/source residual branches",
            "result": "finite_qbar_source_priors_retained",
            "reason": "theta(I_Q,m), species kappa_A, running kappa, non-Hilbert currents, and measured-GM split remain legal",
            "next_action": "do not promote qbar_XT; source finite priors if derivation stalls",
        },
        {
            "decision_id": "DEC977_2_alpha3",
            "topic": "K_boundary_alpha3",
            "result": "unchanged_missing_K_and_Phi",
            "reason": "constant/source progress does not zero boundary flux",
            "next_action": "keep alpha3 fallback active",
        },
        {
            "decision_id": "DEC977_3_best_next",
            "topic": "next checkpoint",
            "result": "superselection_parent_sector_or_qbar_prior_runner",
            "reason": "the cleanest derivation attempt is now to make theta/kappa superselection/topological objects instead of assumptions",
            "next_action": "try parent superselection/topological zero-form sector; if it fails, generate finite qbar/source prior runner rows",
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
            "next_target": "978-Y5-R10-superselection-parent-sector-or-qbar-source-prior-runner.md",
            "objective": "try to construct a parent superselection/topological sector that makes theta_A and kappa nonlocal constants with trivial MTS action; if not, emit finite qbar/source prior rows",
            "include": "theta_A representation functor, kappa global sector, topological zero-form route, Bianchi residual audit, qbar finite priors, K_boundary_alpha3 fallback",
            "exclude": "declaring constants global by taste, qbarXT theorem-zero, local-GR claim, invented coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    certificate_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    counterexample_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    k_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    formalization_count = formalization_changed_after_start()
    rows = [
        {
            "check_id": "V977_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail",
            "detail": "all cited local source paths exist",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V977_1_source_needles_found",
            "result": "pass" if all(row["needle_found"] == "true" for row in sources) else "fail",
            "detail": "all source needles found",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V977_2_relative_certificate_written",
            "result": "pass"
            if any(row["step_id"] == "CSC977_7_verdict" and row["result"] == "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED" for row in certificate_rows)
            else "fail",
            "detail": "constant/source certificate is written only as parent-unsigned",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V977_3_superselection_gates_false",
            "result": "pass" if all(row["gate_pass"] == "false" and row["valid_for_claim"] == "false" for row in gate_rows) else "fail",
            "detail": "parent superselection gates remain false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V977_4_counterexamples_retained",
            "result": "pass"
            if any(row["counterexample_id"] == "CEA977_6_verdict" and row["counterexample_retained"] == "true" for row in counterexample_rows)
            else "fail",
            "detail": "constant/source counterexamples remain retained",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V977_5_qbar_priors_nonclaim",
            "result": "pass" if all(row["valid_for_claim"] == "false" and row["claim_zero_now"] == "false" for row in prior_rows) else "fail",
            "detail": "qbar/source priors remain nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V977_6_K_alpha3_rows_nonclaim",
            "result": "pass" if all(row["valid_for_claim"] == "false" and "MISSING_" in row["missing_input"] for row in k_rows) else "fail",
            "detail": "K_boundary_alpha3 fallback remains non-scoreable",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V977_7_claim_gates_false",
            "result": "pass" if all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows) else "fail",
            "detail": "all qbar/R10/PPN/local-GR claim gates remain false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V977_8_decisions_nonclaim",
            "result": "pass" if all(row["claim_allowed"] == "false" for row in decision_rows) else "fail",
            "detail": "decision ledger remains nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V977_9_next_target_written",
            "result": "pass" if len(target_rows) == 1 and target_rows[0]["valid_for_claim"] == "false" else "fail",
            "detail": "978 superselection parent sector or qbar prior runner target selected",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V977_10_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
            "generated_utc": stamp(),
        },
    ]
    rows.append(
        {
            "check_id": "V977_READY",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "977 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    certificate_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    counterexample_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    k_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 977 Y5 R10: Constant Source Universality Certificate Or K Boundary Alpha3 Source

Status: `Y5_R10_977_constant_source_relative_certificate_parent_unsigned_qbar_priors_retained_Kboundary_alpha3_missing`

Claim ceiling: no constant/source parent certificate, no `qbar_XT=0`, no no-linear-marker theorem, no `p>=2` promotion, no alpha3 coefficient pass, no R10/PPN pass, and no EH/Newton/local-GR claim is made.

## Readout

977 gets the coupling problem into its sharpest current form.

The clean route is:

`theta_A` must be representation/superselection data, not functions of `X`, `I_Q`, material markers, or fibre variables.

`kappa` must be one global/superselection or topological constant, not a species-weighted, range-dependent, memory-dependent, or source-normalization field.

If those are parent-signed, and ordinary matter sources the observed coframe through the Hilbert current, then the constant/source pieces of `qbar_XT` can genuinely vanish.

But the parent signature is still missing. Ward identities define and conserve Hilbert currents under strong premises; they do not force `kappa_A=kappa`, do not make `theta_A(I_Q,m)` illegal, and do not calibrate Hilbert mass to measured orbital `GM`. Bianchi exposes running `kappa` as a residual; it does not hide it.

So this is progress as a contract, not a claim. The next best derivation attempt is to build the actual superselection/topological parent sector for `theta_A` and `kappa`. If that cannot be done, the finite `qbar`/source prior runner is the honest route.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Constant Source Certificate Attempt

{md_table(certificate_rows, ["step_id", "claim_piece", "result", "proof_status", "gap"])}

## Superselection Gate

{md_table(gate_rows, ["gate_id", "required_certificate", "current_evidence", "gate_pass", "missing_input"])}

## Counterexample Audit

{md_table(counterexample_rows, ["counterexample_id", "construction", "why_not_blocked", "residual_activated", "required_blocker"])}

## Residual Prior Update

{md_table(prior_rows, ["prior_id", "component", "status_after_977", "reason", "claim_zero_now", "required_next"])}

## K Boundary Alpha3 Status

{md_table(k_rows, ["row_id", "formula", "known_input", "missing_input", "status", "valid_for_claim"])}

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
    certificate_rows = constant_source_certificate_attempt()
    gate_rows = superselection_gate()
    counterexample_rows = counterexample_audit()
    prior_rows = residual_prior_update()
    k_rows = k_boundary_alpha3_status()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        certificate_rows,
        gate_rows,
        counterexample_rows,
        prior_rows,
        k_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_977_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
        certificate_rows,
        ["step_id", "claim_piece", "mathematical_form", "result", "proof_status", "gap", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_977_SUPERSELECTION_GATE.csv",
        gate_rows,
        ["gate_id", "required_certificate", "current_evidence", "gate_pass", "missing_input", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_977_COUNTEREXAMPLE_AUDIT.csv",
        counterexample_rows,
        ["counterexample_id", "construction", "why_not_blocked", "residual_activated", "required_blocker", "counterexample_retained", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_977_RESIDUAL_PRIOR_UPDATE.csv",
        prior_rows,
        ["prior_id", "component", "status_after_977", "reason", "claim_zero_now", "required_next", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_977_K_BOUNDARY_ALPHA3_STATUS.csv",
        k_rows,
        ["row_id", "formula", "known_input", "missing_input", "status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_977_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed", "why_not_claim", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_977_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_977_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_977_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(
        sources,
        certificate_rows,
        gate_rows,
        counterexample_rows,
        prior_rows,
        k_rows,
        claim_rows,
        decision_rows,
        target_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()
