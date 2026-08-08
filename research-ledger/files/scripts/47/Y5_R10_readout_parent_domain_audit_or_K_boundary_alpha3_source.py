from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "976-Y5-R10-readout-parent-domain-audit-or-K-boundary-alpha3-source.md"
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
            "source_id": "975_doc",
            "path": "975-Y5-R10-no-linear-marker-covector-proof-or-boundary-flux-source-acquisition.md",
            "role": "handoff selecting readout parent-domain audit or K_boundary_alpha3 source",
            "needle": "976-Y5-R10-readout-parent-domain-audit-or-K-boundary-alpha3-source.md",
        },
        {
            "source_id": "975_next",
            "path": "source-intake/mts_residuals/P8_Y5_R10_975_NEXT_TARGET.csv",
            "role": "976 next-target row from invariant-covector checkpoint",
            "needle": "976-Y5-R10-readout-parent-domain-audit-or-K-boundary-alpha3-source.md",
        },
        {
            "source_id": "975_alpha3",
            "path": "source-intake/mts_residuals/P8_Y5_R10_975_ALPHA3_COEFFICIENT_ACQUISITION.csv",
            "role": "alpha3 formula stub and coefficient-acquisition fallback",
            "needle": "ACQ975_0_prediction_formula",
        },
        {
            "source_id": "575_readout_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_575_READOUT_LOCK_CONTRACT.csv",
            "role": "readout-after-variation contract rows",
            "needle": "RL575_2_no_backreaction",
        },
        {
            "source_id": "575_constant_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_575_CONSTANT_SOURCE_LOCK_CONTRACT.csv",
            "role": "constant/source locks that remain after readout hygiene",
            "needle": "CL575_1_trivial_MTS_action",
        },
        {
            "source_id": "422_doc",
            "path": "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
            "role": "matter functor and readout-after-variation theorem attempt",
            "needle": "readout_after_variation_contract_written",
        },
        {
            "source_id": "422_variation_order",
            "path": "runs/20260602-081000-matter-functor-blindness-readout-after-variation-theorem-attempt/results/variation_order_contract.csv",
            "role": "variation-order contract and forbidden post-readout objects",
            "needle": "variation of readout-selected reduced blocks",
        },
        {
            "source_id": "422_counterexamples",
            "path": "runs/20260602-081000-matter-functor-blindness-readout-after-variation-theorem-attempt/results/counterexample_leaks.csv",
            "role": "post-readout EFT and domain-scored matter counterexamples",
            "needle": "post_readout_EFT_action",
        },
        {
            "source_id": "621_doc",
            "path": "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
            "role": "post-readout EFT excluded as branch policy but not positive theorem evidence",
            "needle": "NMF621_6_no_post_readout_EFT",
        },
        {
            "source_id": "622_doc",
            "path": "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
            "role": "branch purity accepted as nonclaim prior runner row",
            "needle": "SP622_6_EFT",
        },
        {
            "source_id": "456_doc",
            "path": "456-PiM-projector-variation-stress-ledger.md",
            "role": "readout mask backreaction rejection and Pi_M stress warning",
            "needle": "PV7_readout_masks_after_variation_only",
        },
        {
            "source_id": "595_doc",
            "path": "595-Y5-R10-construct-pi-observed-quotient-map-or-demote-to-diffeo-current.md",
            "role": "readout cheat rejection in quotient-map construction",
            "needle": "NCR595_5_post_readout_cheat",
        },
        {
            "source_id": "423_doc",
            "path": "423-parent-action-minimality-no-extension-theorem-attempt.md",
            "role": "no-extension blocker after readout hygiene",
            "needle": "post_readout_reduced_action",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "alpha3 pressure anchor for K_boundary fallback",
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


def readout_parent_domain_audit() -> list[dict[str, str]]:
    specs = [
        {
            "audit_id": "RDA976_0_parent_domain_before_readout",
            "domain_clause": "S_parent is defined on parent fields before observational readout",
            "mathematical_form": "S_parent=S[Phi in C_parent; Psi; universal constants]",
            "audit_result": "FORMAL_DOMAIN_RULE_ACCEPTED",
            "claim_effect": "post-readout objects are not variational parent arguments",
            "remaining_gap": "does not prove matter factorization, constants, or source current universality",
        },
        {
            "audit_id": "RDA976_1_solution_space_readout",
            "domain_clause": "readout maps solutions to observables",
            "mathematical_form": "R_read: Sol(S_parent)/G -> Obs",
            "audit_result": "RELATIVE_THEOREM_VALID",
            "claim_effect": "delta S_parent/delta R_read=0 by absence when the branch obeys the domain rule",
            "remaining_gap": "full parent-action inventory is not globally exhausted by this checkpoint",
        },
        {
            "audit_id": "RDA976_2_no_reduced_action_backreaction",
            "domain_clause": "readout-selected reduced blocks are not varied as fundamental actions",
            "mathematical_form": "no variation of S_red[P_read, P_active, fitted masks, e_obs] as S_parent",
            "audit_result": "BRANCH_POLICY_PASS_NOT_POSITIVE_THEOREM",
            "claim_effect": "post-readout EFT cannot be used for parent-derived theorem credit",
            "remaining_gap": "policy excludes fake proof credit but does not prove all physical marker couplings absent",
        },
        {
            "audit_id": "RDA976_3_qbar_effect",
            "domain_clause": "readout projector contributes no direct parent X source if absent from S_parent",
            "mathematical_form": "partial_X P_read terms are absent from delta_X S_parent",
            "audit_result": "CONDITIONAL_PASS_FOR_READOUT_COMPONENT_ONLY",
            "claim_effect": "b_EFT/post_readout_counterterm_projection stays absent from parent-derived branch",
            "remaining_gap": "qbar_XT still has b_g, b_theta, b_m, b_kappa, b_NH components open",
        },
        {
            "audit_id": "RDA976_4_domain_scoring_guard",
            "domain_clause": "candidate domains/projectors must be generated before scoring or treated as readout only",
            "mathematical_form": "D_candidate in parent equations or D_read in R_read, never post-score D fed into S_parent",
            "audit_result": "GUARDRAIL_WRITTEN",
            "claim_effect": "prevents domain-scored matter coupling from masquerading as derivation",
            "remaining_gap": "does not derive Bianchi-safe domain selector or boundary no-flux",
        },
        {
            "audit_id": "RDA976_5_verdict",
            "domain_clause": "readout parent-domain absence certificate",
            "mathematical_form": "P_read, P_active, fitted masks, closure flags, and post-readout counterterms notin Args(S_parent)",
            "audit_result": "BRANCH_EXCLUSION_CERTIFICATE_WRITTEN_NONCLAIM",
            "claim_effect": "one fake-zero route is excluded from the private parent-derived branch",
            "remaining_gap": "not enough for qbar_XT=0, p>=2 promotion, R10 pass, PPN pass, or local-GR reduction",
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


def args_sparent_inventory() -> list[dict[str, str]]:
    specs = [
        {
            "arg_id": "ARG976_0_parent_fields",
            "object_class": "Phi_parent/Q_MTS",
            "domain_status": "ALLOWED_PARENT_ARGUMENT",
            "reason": "parent equations are varied on primitive fields/quotient variables",
            "risk_if_wrong": "none; this is the actual parent domain",
            "claim_use": "structural setup only",
        },
        {
            "arg_id": "ARG976_1_matter_fields",
            "object_class": "Psi ordinary matter fields",
            "domain_status": "ALLOWED_PARENT_ARGUMENT_WITH_FACTORISATION_DEBT",
            "reason": "matter can be a parent argument, but must factor through observed geometry and universal constants",
            "risk_if_wrong": "selector-dependent matter vertices reopen qbar_XT",
            "claim_use": "not enough for matter blindness",
        },
        {
            "arg_id": "ARG976_2_universal_constants",
            "object_class": "theta_A/kappa universal representation data",
            "domain_status": "ALLOWED_ONLY_IF_CONSTANT_SECTOR_TRIVIAL",
            "reason": "constants may be parameters but not MTS fields or marker functions",
            "risk_if_wrong": "theta_A(I_Q,m) and kappa_A source weights survive",
            "claim_use": "next theorem lock",
        },
        {
            "arg_id": "ARG976_3_readout_maps",
            "object_class": "R_read, Obs comparison maps",
            "domain_status": "FORBIDDEN_AS_VARIATIONAL_ARGUMENT",
            "reason": "readout is a map on solution space after variation",
            "risk_if_wrong": "closure-zero can be baked into reduced action",
            "claim_use": "branch exclusion only",
        },
        {
            "arg_id": "ARG976_4_projector_masks",
            "object_class": "P_read, P_active, fitted Pi_M, fitted selector masks",
            "domain_status": "FORBIDDEN_AS_PARENT_SOURCE",
            "reason": "post-fit/readout masks are not primitive parent fields",
            "risk_if_wrong": "preferred-frame/location/source-normalization cheat",
            "claim_use": "reject proof credit if present",
        },
        {
            "arg_id": "ARG976_5_closure_flags",
            "object_class": "closure-zero labels and score-selected branches",
            "domain_status": "FORBIDDEN_AS_PARENT_SOURCE",
            "reason": "closure labels classify branches; they do not vary the parent action",
            "risk_if_wrong": "local-GR pass is inserted by definition",
            "claim_use": "guardrail only",
        },
        {
            "arg_id": "ARG976_6_boundary_flux",
            "object_class": "boundary/local projection flux",
            "domain_status": "NOT_RESOLVED_BY_READOUT_RULE",
            "reason": "boundary flux may be an actual parent/boundary term, not merely readout",
            "risk_if_wrong": "alpha3/Gdot/PPN residual source remains",
            "claim_use": "derive no-flux or source K_boundary_alpha3",
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


def residual_component_update() -> list[dict[str, str]]:
    specs = [
        {
            "component_id": "RCU976_0_b_EFT",
            "component": "post_readout_counterterm_projection",
            "status_after_976": "ABSENT_FROM_PARENT_DERIVED_BRANCH",
            "reason": "readout/reduced counterterms are outside Args(S_parent) by branch definition",
            "zero_credit": "false",
            "next_action": "keep absent unless explicitly demoted to phenomenology",
        },
        {
            "component_id": "RCU976_1_b_g",
            "component": "common_frame_log_derivative",
            "status_after_976": "OPEN",
            "reason": "readout hygiene does not prove observed coframe/metric factorization",
            "zero_credit": "false",
            "next_action": "derive matter geometry functor through one observed coframe",
        },
        {
            "component_id": "RCU976_2_b_theta",
            "component": "d_ln_alpha_EM_dXhat;d_ln_mass_ratio_dXhat",
            "status_after_976": "OPEN",
            "reason": "constant-sector trivial MTS action is not parent-derived",
            "zero_credit": "false",
            "next_action": "derive constants as representation/superselection data",
        },
        {
            "component_id": "RCU976_3_b_m",
            "component": "marker_coupling_projection",
            "status_after_976": "OPEN",
            "reason": "co-moving material/domain marker extensions remain legal",
            "zero_credit": "false",
            "next_action": "derive no-extension/minimality or retain finite coefficient",
        },
        {
            "component_id": "RCU976_4_b_kappa",
            "component": "species_source_weight_splitting",
            "status_after_976": "OPEN",
            "reason": "universal source-current/coupling theorem is not parent-derived",
            "zero_credit": "false",
            "next_action": "derive Hilbert source universality and single kappa",
        },
        {
            "component_id": "RCU976_5_boundary_alpha3",
            "component": "K_boundary_alpha3 * Phi_boundary_local",
            "status_after_976": "OPEN_NON_SCOREABLE",
            "reason": "boundary flux is not removed by readout-after-variation",
            "zero_credit": "false",
            "next_action": "derive boundary no-flux or source K_boundary_alpha3",
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


def k_boundary_alpha3_source_acquisition() -> list[dict[str, str]]:
    specs = [
        {
            "row_id": "KBA976_0_formula",
            "coefficient": "K_boundary_alpha3",
            "required_value": "numeric dimensionless projection coefficient or theorem-zero",
            "observable_map": "alpha3_MTS=K_boundary_alpha3*Phi_boundary_local",
            "bound_or_anchor": "abs(alpha3_MTS)<=4.000e-20",
            "source_status": "MISSING",
            "missing_inputs": "MISSING_K_BOUNDARY_ALPHA3;MISSING_DERIVATION_OR_SOURCE_PATH",
        },
        {
            "row_id": "KBA976_1_flux_amplitude",
            "coefficient": "Phi_boundary_local",
            "required_value": "numeric local boundary/memory flux amplitude with units",
            "observable_map": "normalizes K_boundary_alpha3 prediction",
            "bound_or_anchor": "same alpha3 anchor",
            "source_status": "MISSING",
            "missing_inputs": "MISSING_PHI_BOUNDARY_LOCAL;MISSING_BOUNDARY_NORM;MISSING_UNITS",
        },
        {
            "row_id": "KBA976_2_anchor",
            "coefficient": "alpha3_flux_bound_anchor",
            "required_value": "4.000e-20 dimensionless",
            "observable_map": "PPN preferred-frame pressure anchor",
            "bound_or_anchor": "417 alpha3_flux",
            "source_status": "SOURCE_BACKED_ANCHOR_ONLY",
            "missing_inputs": "MISSING_CLAIM_GRADE_MTS_PREDICTION",
        },
        {
            "row_id": "KBA976_3_decision",
            "coefficient": "K_boundary_alpha3_row",
            "required_value": "not executable",
            "observable_map": "runner must reject until K and Phi are sourced or theorem-zero closes",
            "bound_or_anchor": "G507 theorem-zero/numeric-bound policy",
            "source_status": "NONCLAIM",
            "missing_inputs": "MISSING_THEOREM_ZERO_OR_EXECUTABLE_NUMERIC_BOUND_PASS",
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
            "gate_id": "CGATE976_0_readout_branch_exclusion",
            "claim": "post-readout EFT is excluded from parent-derived branch",
            "current_evidence": "branch-domain rule and prior 621/622 policy support exclusion",
            "gate_pass": "true",
            "claim_allowed": "false",
            "why_not_claim": "it is hygiene/branch exclusion, not positive proof that physical qbar_XT vanishes",
        },
        {
            "gate_id": "CGATE976_1_qbarXT_zero",
            "claim": "ordinary test-body qbar_XT is zero",
            "current_evidence": "b_EFT excluded, but b_g/b_theta/b_m/b_kappa/b_NH remain open",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not_claim": "matter factorization and constant/source universality are not parent-derived",
        },
        {
            "gate_id": "CGATE976_2_no_linear_marker",
            "claim": "all marker covectors are excluded",
            "current_evidence": "readout marker hygiene only; material/domain/constant markers survive",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not_claim": "no-extension and invariant algebra triviality remain unsigned",
        },
        {
            "gate_id": "CGATE976_3_alpha3_executable",
            "claim": "K_boundary_alpha3 alpha3 row is scoreable",
            "current_evidence": "anchor exists; K_boundary_alpha3 and Phi_boundary_local missing",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not_claim": "no MTS prediction exists",
        },
        {
            "gate_id": "CGATE976_4_local_GR",
            "claim": "local GR/Newton reduction follows",
            "current_evidence": "only one fake-zero channel excluded",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not_claim": "local operator, source, boundary, and marker gates remain open",
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


def decisions() -> list[dict[str, str]]:
    specs = [
        {
            "decision_id": "DEC976_0_readout_result",
            "topic": "readout parent-domain audit",
            "result": "branch_exclusion_certificate_written",
            "reason": "P_read/P_active/fitted masks/post-readout counterterms are outside Args(S_parent) in the parent-derived branch",
            "next_action": "use this as hygiene only; do not count it as qbarXT theorem-zero",
        },
        {
            "decision_id": "DEC976_1_remaining_marker_problem",
            "topic": "no-linear-marker route",
            "result": "readout_marker_reduced_material_constant_markers_remain",
            "reason": "co-moving material markers, domain/class scalars, constants, and universal source weights are not removed by readout hygiene",
            "next_action": "attack constant/source universality next",
        },
        {
            "decision_id": "DEC976_2_alpha3_fallback",
            "topic": "K_boundary_alpha3",
            "result": "source_acquisition_contract_tightened_nonclaim",
            "reason": "formula and anchor are known, but no K/Phi prediction exists",
            "next_action": "keep K_boundary_alpha3 as fallback if derivation branch stalls",
        },
        {
            "decision_id": "DEC976_3_best_next",
            "topic": "next checkpoint",
            "result": "constant_source_universality_or_K_boundary_alpha3",
            "reason": "after readout hygiene, the shortest live source-side lock is constants and universal Hilbert source current",
            "next_action": "try constant/source universality parent certificate; if it fails, fill finite residual priors or K_boundary_alpha3",
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
            "next_target": "977-Y5-R10-constant-source-universality-certificate-or-K-boundary-alpha3-source.md",
            "objective": "try to parent-sign constant-sector trivial MTS action and universal Hilbert source current; if not, keep finite qbar/source priors and K_boundary_alpha3 acquisition active",
            "include": "theta_A representation data, Lie_X theta_A=0, single universal kappa, Hilbert source current, species/source-weight split, K_boundary_alpha3 fallback",
            "exclude": "qbarXT theorem-zero from readout hygiene alone, local-GR claim, invented coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    args_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    k_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    formalization_count = formalization_changed_after_start()
    rows = [
        {
            "check_id": "V976_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail",
            "detail": "all cited local source paths exist",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V976_1_source_needles_found",
            "result": "pass" if all(row["needle_found"] == "true" for row in sources) else "fail",
            "detail": "all source needles found",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V976_2_readout_branch_exclusion_written",
            "result": "pass"
            if any(row["audit_id"] == "RDA976_5_verdict" and row["audit_result"] == "BRANCH_EXCLUSION_CERTIFICATE_WRITTEN_NONCLAIM" for row in readout_rows)
            else "fail",
            "detail": "readout branch exclusion certificate is written as nonclaim hygiene",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V976_3_forbidden_args_listed",
            "result": "pass"
            if any(row["arg_id"] == "ARG976_4_projector_masks" and row["domain_status"] == "FORBIDDEN_AS_PARENT_SOURCE" for row in args_rows)
            else "fail",
            "detail": "P_read/P_active/fitted masks are forbidden as parent sources",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V976_4_qbar_components_remain_open",
            "result": "pass"
            if any(row["component_id"] == "RCU976_2_b_theta" and row["status_after_976"] == "OPEN" for row in residual_rows)
            else "fail",
            "detail": "constant-sector and related qbar components remain open",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V976_5_K_alpha3_rows_nonclaim",
            "result": "pass" if all(row["valid_for_claim"] == "false" and "MISSING_" in row["missing_inputs"] for row in k_rows) else "fail",
            "detail": "K_boundary_alpha3 rows remain non-scoreable until K/Phi inputs exist",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V976_6_no_positive_claim_credit",
            "result": "pass"
            if all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
            else "fail",
            "detail": "even the readout exclusion pass gives no positive local-GR/R10 claim credit",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V976_7_decisions_nonclaim",
            "result": "pass" if all(row["claim_allowed"] == "false" for row in decision_rows) else "fail",
            "detail": "decision ledger remains nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V976_8_next_target_written",
            "result": "pass" if len(target_rows) == 1 and target_rows[0]["valid_for_claim"] == "false" else "fail",
            "detail": "977 constant/source universality or K_boundary_alpha3 target selected",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V976_9_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
            "generated_utc": stamp(),
        },
    ]
    rows.append(
        {
            "check_id": "V976_READY",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "976 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    args_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    k_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 976 Y5 R10: Readout Parent-Domain Audit Or K Boundary Alpha3 Source

Status: `Y5_R10_976_readout_branch_exclusion_certificate_written_nonclaim_qbar_components_open_Kboundary_alpha3_missing`

Claim ceiling: post-readout EFT is excluded from the parent-derived branch, but no `qbar_XT=0`, no no-linear-marker theorem, no `p>=2` promotion, no alpha3 coefficient pass, no R10/PPN pass, and no EH/Newton/local-GR claim is made.

## Readout

976 closes one cheat door, not the whole house.

The parent-derived branch now carries a clean domain rule:

`S_parent` is varied on parent fields before observation, and `R_read: Sol(S_parent)/G -> Obs` is applied only after the parent equations are solved.

Therefore `P_read`, `P_active`, fitted masks, post-score projectors, closure labels, and after-the-fact EFT counterterms are not in `Args(S_parent)`. If a branch uses them as variational sources, it is rejected for parent-theorem credit.

That is useful hygiene. It removes the post-readout fake-zero channel and keeps `b_EFT` absent from the parent-derived branch.

But it is not positive evidence for local GR. It does not prove ordinary matter sees only one observed coframe, does not prove `theta_A` and `kappa` are MTS-trivial representation data, does not kill co-moving material markers, and does not zero boundary flux. So `qbar_XT`, no-linear-marker, alpha3, and local-GR gates remain blocked.

The next best derivation target is constants and universal source current. If that route fails, the finite residual wall stays live, especially `K_boundary_alpha3`.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Readout Parent-Domain Audit

{md_table(readout_rows, ["audit_id", "domain_clause", "audit_result", "claim_effect", "remaining_gap"])}

## Args(S_parent) Inventory

{md_table(args_rows, ["arg_id", "object_class", "domain_status", "reason", "risk_if_wrong", "claim_use"])}

## Residual Component Update

{md_table(residual_rows, ["component_id", "component", "status_after_976", "reason", "zero_credit", "next_action"])}

## K Boundary Alpha3 Source Acquisition

{md_table(k_rows, ["row_id", "coefficient", "required_value", "observable_map", "bound_or_anchor", "source_status", "missing_inputs", "valid_for_claim"])}

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
    readout_rows = readout_parent_domain_audit()
    args_rows = args_sparent_inventory()
    residual_rows = residual_component_update()
    k_rows = k_boundary_alpha3_source_acquisition()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        readout_rows,
        args_rows,
        residual_rows,
        k_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_976_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_976_READOUT_PARENT_DOMAIN_AUDIT.csv",
        readout_rows,
        ["audit_id", "domain_clause", "mathematical_form", "audit_result", "claim_effect", "remaining_gap", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_976_ARGS_SPARENT_INVENTORY.csv",
        args_rows,
        ["arg_id", "object_class", "domain_status", "reason", "risk_if_wrong", "claim_use", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_976_RESIDUAL_COMPONENT_UPDATE.csv",
        residual_rows,
        ["component_id", "component", "status_after_976", "reason", "zero_credit", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_976_K_BOUNDARY_ALPHA3_SOURCE_ACQUISITION.csv",
        k_rows,
        ["row_id", "coefficient", "required_value", "observable_map", "bound_or_anchor", "source_status", "missing_inputs", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_976_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed", "why_not_claim", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_976_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_976_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_976_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(
        sources,
        readout_rows,
        args_rows,
        residual_rows,
        k_rows,
        claim_rows,
        decision_rows,
        target_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()
