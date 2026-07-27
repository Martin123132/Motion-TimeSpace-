from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "956-Y5-R10-source-side-GR-reduction-spine-and-left-hand-EH-gate-map.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "955_doc",
            "path": "955-Y5-R10-minimal-matter-action-source-coupling-lemma-or-species-weight-residual-runner.md",
            "role": "handoff: conditional source-side spine and relative w_A obstruction",
            "needle": "minimal matter action lemma",
        },
        {
            "source_id": "955_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_955_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V955_13_validation_rows_ready",
        },
        {
            "source_id": "955_minimal_matter",
            "path": "source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
            "role": "minimal matter/source coupling lemma",
            "needle": "MMA955_6_verdict",
        },
        {
            "source_id": "955_prefactor_classification",
            "path": "source-intake/mts_residuals/P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv",
            "role": "common-mode vs relative species source prefactors",
            "needle": "SPC955_2_relative_species_weight",
        },
        {
            "source_id": "953_source_functor_theorem",
            "path": "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
            "role": "conditional no-species-label uniqueness theorem",
            "needle": "NSF953_5_verdict",
        },
        {
            "source_id": "954_label_forgetting",
            "path": "source-intake/mts_residuals/P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv",
            "role": "label-forgetting by total Hilbert variation",
            "needle": "PLF954_5_verdict",
        },
        {
            "source_id": "912_EH_baseline",
            "path": "source-intake/mts_residuals/P8_Y5_R10_912_EH_CORE_BASELINE.csv",
            "role": "EH metric-core baseline and extra-omega warning",
            "needle": "EHB912_3_EH_does_not_silence_extras",
        },
        {
            "source_id": "529_source_calibrated_EH_stack",
            "path": "source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK.csv",
            "role": "source-calibrated EH/PPN proof-stack rungs",
            "needle": "SCEH529_7_beta_local_GR_gate",
        },
        {
            "source_id": "529_source_calibrated_EH_blockers",
            "path": "source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_BLOCKERS.csv",
            "role": "highest-priority EH/source-normalization blockers",
            "needle": "BL529_0_R11_operator",
        },
        {
            "source_id": "482_local_GR_promotion_gates",
            "path": "source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_PROMOTION_GATES.csv",
            "role": "local GR residual promotion gates",
            "needle": "G482_local_GR_vector",
        },
        {
            "source_id": "505_EH_requirements",
            "path": "source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv",
            "role": "local EH reduction requirements",
            "needle": "EH505_0_operator_reduction",
        },
        {
            "source_id": "655_EH_premise_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
            "role": "EH-only premise audit",
            "needle": "EHP655_P6_second_order",
        },
    ]
    rows = []
    for spec in specs:
        path = source_path(spec["path"])
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def source_side_spine() -> list[dict[str, str]]:
    return [
        {
            "spine_id": "SSG956_0_observed_coframe",
            "condition": "one observed coframe/metric used by matter, source variation, clocks, photons, and readout",
            "mathematical_form": "e_obs = e_matter = e_source = e_readout through tested PPN order",
            "current_status": "conditional_from_prior_contracts",
            "if_closed": "ordinary source and observables refer to the same geometry",
            "remaining_blocker": "readout-frame and hidden-sector variations still need parent closure through PPN order",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "spine_id": "SSG956_1_no_species_source_functor",
            "condition": "source functor has no species-label argument",
            "mathematical_form": "F_src(T_total)=kappa_univ T_total, not F_src({(T_A,A)})=sum_A kappa_A T_A",
            "current_status": "conditional_theorem_from_953",
            "if_closed": "relative source couplings cannot be formed",
            "remaining_blocker": "parent label-forgetting/source-domain clause unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "spine_id": "SSG956_2_total_Hilbert_source",
            "condition": "active ordinary source is total Hilbert/coframe derivative of one matter action",
            "mathematical_form": "T_total := delta S_matter/delta e_obs = sum_A delta S_A/delta e_obs",
            "current_status": "conditional_variational_mechanism_from_954",
            "if_closed": "species decomposition is bookkeeping rather than separate source channels",
            "remaining_blocker": "source-only species prefactors w_A must be absent or bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "spine_id": "SSG956_3_minimal_matter_action",
            "condition": "matter dynamics and active source come from the same minimal matter functional",
            "mathematical_form": "S_matter=sum_A S_A[Psi_A,e_obs,theta_A], no independent source-only w_A slot",
            "current_status": "exact_contract_not_parent_signed_from_955",
            "if_closed": "relative w_A/w_B source residual is removed by construction",
            "remaining_blocker": "schema has not been derived from deeper quotient/no-extra-slot principle",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "spine_id": "SSG956_4_common_kappa_calibration",
            "condition": "one common coupling is calibrated to measured Newton G",
            "mathematical_form": "kappa_univ -> 8 pi G_ref/c^4 after source-measure/Gauss calibration",
            "current_status": "common_mode_harmless_but_measured_GM_chain_open",
            "if_closed": "common normalization becomes units rather than a new composition force",
            "remaining_blocker": "measured-GM/worldtube/source-normalization chain remains open in older gates",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "spine_id": "SSG956_5_source_side_verdict",
            "condition": "source-side GR/Newton matter term",
            "mathematical_form": "source side = kappa_univ T_total + DeltaJ_hidden + DeltaJ_species",
            "current_status": "conditional_spine_sharp_not_claimable",
            "if_closed": "right-hand side of local GR/Newton limit is structurally standard",
            "remaining_blocker": "DeltaJ_hidden and DeltaJ_species must be theorem-zero or bounded; left-hand EH still separate",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def left_hand_gate_map() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "LHG956_0_EH_core_selection",
            "required_condition": "local exterior metric/coframe operator reduces to Einstein-Hilbert plus harmless Lambda/background",
            "mathematical_form": "E_MTS[g,...] = G_munu + Lambda g_munu + DeltaE_extra; require DeltaE_extra=0 or bounded",
            "prior_evidence": "P8_LOCAL_EH_REDUCTION_REQUIREMENTS EH505_0 and P8_Y5_R10_655 premise audit",
            "current_status": "not_parent_derived",
            "blocks": "EH-only local GR claim and Newtonian source-normalized promotion",
            "next_action": "derive metric-only second-order EH selection or retain executable R11/nonEH vector",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "LHG956_1_extra_sector_silence",
            "required_condition": "motion/time/domain/memory/projector/boundary/connection sectors have no projected local exterior stress/charge",
            "mathematical_form": "DeltaE_extra = DeltaE_X + DeltaE_D + DeltaE_boundary + DeltaE_connection + ... = 0",
            "prior_evidence": "P8_Y5_R10_912 EHB912_3 and P8_Y5_SOURCE_CALIBRATED_EH_BLOCKERS",
            "current_status": "active_primary_obstruction",
            "blocks": "Hamiltonian charge integrability, PPN vector, and local no-hair family",
            "next_action": "prove gauge/topological/no-hair silence or retain each residual with sourced bounds",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "LHG956_2_one_parameter_nohair",
            "required_condition": "compact exterior is a one-parameter mass family with no independent scalar/vector/domain/boundary hair",
            "mathematical_form": "metric exterior = Schwarzschild/SdS(mu) + background; no independent hair charges",
            "prior_evidence": "P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK SCEH529_2",
            "current_status": "not_derived",
            "blocks": "Newtonian potential and PPN beta/gamma source identification",
            "next_action": "derive sector no-hair theorems or fill residual vector rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "LHG956_3_measured_GM_calibration",
            "required_condition": "EH mass parameter equals measured orbital GM and Hilbert/projected source charge",
            "mathematical_form": "mu_EH = mu_obs = G_ref M_H[Pi_M J_H]",
            "prior_evidence": "P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK SCEH529_3 and blockers BL529_1",
            "current_status": "not_derived",
            "blocks": "Newtonian mechanics reduction even if EH operator is selected",
            "next_action": "derive Gauss/Poisson/worldtube source-measure calibration or keep M_eff residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "LHG956_4_constant_source_normalization",
            "required_condition": "mass/source normalization has no time/radius/species/range/frame/domain derivative",
            "mathematical_form": "partial_{t,r,A,lambda,frame,domain} mu_EH = 0 and mu_extra=0",
            "prior_evidence": "P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK SCEH529_4 and source-normalization missing ledgers",
            "current_status": "not_derived",
            "blocks": "fifth-force, Gdot, WEP/source normalization, and radial-hair claims",
            "next_action": "combine source-side 953-955 with radial/domain/boundary no-hair gates",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "LHG956_5_PPN_completion",
            "required_condition": "observed weak-field expansion reaches GR PPN values with no quadratic leakage",
            "mathematical_form": "gamma=1, beta=1, alpha_i=0, xi=0, Delta_beta_R11=Delta_beta_q_loc=...=0",
            "prior_evidence": "P8_LOCAL_GR_RESIDUAL_PROMOTION_GATES and SCEH529_6/SCEH529_7",
            "current_status": "failed_for_claim_current_vector",
            "blocks": "local GR claim even if leading Newtonian order looks good",
            "next_action": "fill or theorem-zero every local residual vector component without cancellation",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def hidden_current_gate_map() -> list[dict[str, str]]:
    return [
        {
            "hidden_id": "HCG956_0_relative_species_prefactor",
            "channel": "relative w_A/w_B or kappa_A/kappa_B source weight",
            "risk": "composition-dependent source normalization",
            "current_status": "live_residual_from_955",
            "required_closure": "parent no-source-prefactor theorem or sourced epsilon_A bound",
            "feeds_gate": "SSG956_3; LHG956_4; PPN/WEP source channels",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hidden_id": "HCG956_1_marker_domain_boundary_weight",
            "channel": "marker/domain/boundary/post-readout disguised source prefactor",
            "risk": "kappa_A returns after apparent label-forgetting",
            "current_status": "hidden_spurion_channel_from_955",
            "required_closure": "no-spurion theorem or explicit residual vector rows",
            "feeds_gate": "SSG956_5; LHG956_1; LHG956_4",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hidden_id": "HCG956_2_nonHilbert_current",
            "channel": "spin/torsion/boundary/non-Hilbert active current",
            "risk": "bypasses Hilbert-current uniqueness and changes source or PPN charges",
            "current_status": "parallel_open_gate_from_955_and_912",
            "required_closure": "absent/exact/projected silent theorem or retained bound row",
            "feeds_gate": "SSG956_5; LHG956_1; LHG956_5",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hidden_id": "HCG956_3_omega_extra",
            "channel": "extra-sector symplectic flux",
            "risk": "EH baseline charge form does not integrate to full MTS Hamiltonian charge",
            "current_status": "active_obstruction_from_911_912",
            "required_closure": "omega_extra=0/gauge/topological/no-flux or bounded charge residual",
            "feeds_gate": "LHG956_1; LHG956_2; LHG956_5",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hidden_id": "HCG956_4_R11_nonEH_operator",
            "channel": "non-EH/R11 operator vector",
            "risk": "conserved non-EH tensors alter beta/gamma/preferred-frame observables",
            "current_status": "template_or_unfilled_in_prior_gates",
            "required_closure": "EH-only theorem or executable nonEH coefficient vector with bounds",
            "feeds_gate": "LHG956_0; LHG956_5",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "hidden_id": "HCG956_5_worldtube_source_measure",
            "channel": "source-measure/worldtube/Gauss calibration",
            "risk": "metric mass parameter not equal to measured orbital GM",
            "current_status": "open_high_priority_blocker",
            "required_closure": "derive worldtube source law and measured-GM calibration",
            "feeds_gate": "SSG956_4; LHG956_3; Newtonian reduction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def reduction_equation_spine() -> list[dict[str, str]]:
    return [
        {
            "equation_id": "REQ956_0_full_local_equation",
            "equation": "E_MTS[g,e_obs,X,D,...] = kappa_univ T_total + DeltaJ_species + DeltaJ_hidden",
            "GR_limit_condition": "E_MTS -> G_munu+Lambda g_munu and DeltaJ_species=DeltaJ_hidden=0",
            "Newton_limit_condition": "weak-field 00 equation gives nabla^2 U = 4 pi G_ref rho_obs with mu_EH=G_ref M_obs",
            "current_status": "framework_spine_only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "equation_id": "REQ956_1_left_hand_residual_split",
            "equation": "E_MTS = E_EH + DeltaE_R11 + DeltaE_q_loc + DeltaE_boundary + DeltaE_domain + DeltaE_connection + ...",
            "GR_limit_condition": "each DeltaE term theorem-zero/gauge/topological/no-hair or separately bounded",
            "Newton_limit_condition": "no extra Poisson source, no radial hair, no range dependence",
            "current_status": "residual_split_required_not_closed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "equation_id": "REQ956_2_source_residual_split",
            "equation": "T_source = T_total + DeltaT_w + DeltaT_NH + DeltaT_boundary",
            "GR_limit_condition": "DeltaT_w=DeltaT_NH=DeltaT_boundary=0 or retained below bounds",
            "Newton_limit_condition": "source mass is conserved, universal, and calibrated to measured GM",
            "current_status": "source_side_conditional_from_953_955",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "equation_id": "REQ956_3_PPN_vector_condition",
            "equation": "Delta_PPN = (gamma-1, beta-1, alpha1, alpha2, alpha3, xi, Gdot/G, range_terms, ...)",
            "GR_limit_condition": "every component is zero/theorem-derived or scored below bound without cancellation",
            "Newton_limit_condition": "leading Newtonian piece is not promoted until source normalization and local residual vector pass",
            "current_status": "promotion_gates_fail_for_claim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC956_0_source_side",
            "topic": "source-side GR/Newton spine",
            "result": "conditional_spine_consolidated",
            "reason": "953-955 now give a coherent route from one matter action to one total Hilbert source with common kappa",
            "next_action": "do not claim source closure until no-source-prefactor and hidden-current clauses are parent-signed or bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC956_1_left_hand",
            "topic": "left-hand EH/Newton gate",
            "result": "still_open_high_pressure",
            "reason": "EH baseline exists, but EH selection, extra-sector silence, one-parameter no-hair, measured GM, and PPN completion remain open",
            "next_action": "attack left-hand EH parent selection or produce executable residual vector rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC956_2_project_overview",
            "topic": "overall local GR bridge",
            "result": "not_claimable_but_structurally_clearer",
            "reason": "the bridge is now split into exact source-side clauses and left-hand operator/no-hair/calibration gates",
            "next_action": "write a parent-local-GR spine ledger and choose the next highest-leverage derivation: EH selection vs measured-GM calibration",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE956_0_source_side_GR",
            "claim": "source side reduces to GR/Newton matter source",
            "required_condition": "953 no-species theorem + 954 label-forgetting + 955 no-prefactor/minimal matter schema + hidden current silence",
            "current_evidence": "conditional spine only; relative w_A and hidden currents remain open",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE956_1_left_hand_EH",
            "claim": "left-hand local field equation is EH in observed frame",
            "required_condition": "metric-only second-order EH selection and all nonEH/R11/extra sectors silent or bounded",
            "current_evidence": "EH baseline conditional; extra-sector and R11 blockers active",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE956_2_Newtonian_limit",
            "claim": "MTS derives Newtonian mechanics locally",
            "required_condition": "EH/source equation weak-field 00 limit plus measured-GM/worldtube calibration and no extra Poisson hair",
            "current_evidence": "source-side structure sharpened but measured-GM/no-hair gates open",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE956_3_full_local_GR_PPN",
            "claim": "local GR/PPN vector passes",
            "required_condition": "gamma, beta, alpha_i, xi, Gdot/range/source-normalization rows zero or scored without cancellation",
            "current_evidence": "promotion gates fail for claim and residual vector rows remain unfilled",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "957-Y5-R10-parent-local-GR-spine-ledger-and-EH-vs-GM-next-derivation-choice.md",
            "objective": "turn the 956 map into a parent-local-GR spine ledger and select the next high-leverage derivation branch: EH-only operator selection or measured-GM/worldtube calibration",
            "include": "source-side clauses, left-hand EH gates, Newtonian weak-field conditions, measured-GM chain, residual-vector blockers, next derivation decision",
            "exclude": "invented coefficients, local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    source_spine_rows: list[dict[str, str]],
    left_gate_rows: list[dict[str, str]],
    hidden_rows: list[dict[str, str]],
    equation_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_955_VALIDATION.csv"))
    source_spine_ready = len(source_spine_rows) == 6 and any(row["spine_id"] == "SSG956_5_source_side_verdict" for row in source_spine_rows)
    source_spine_nonclaim = all(row["claim_allowed"] == "false" for row in source_spine_rows)
    left_gates_mapped = len(left_gate_rows) == 6 and all(row["claim_allowed"] == "false" for row in left_gate_rows)
    hidden_gates_mapped = len(hidden_rows) == 6 and all(row["valid_for_claim"] == "false" for row in hidden_rows)
    equation_spine_mapped = len(equation_rows) == 4 and all(row["claim_allowed"] == "false" for row in equation_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = bool(target_rows) and target_rows[0]["next_target"].startswith("957-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, source_spine_rows, left_gate_rows, hidden_rows, equation_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V956_0_sources_exist_and_needles", sources_ok, "all 956 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V956_1_prior_955_clean", prior_clean, "P8_Y5_BRR545_955_VALIDATION.csv clean")
    add("V956_2_source_spine_ready", source_spine_ready, "source-side GR/Newton conditional spine consolidated")
    add("V956_3_source_spine_nonclaim", source_spine_nonclaim, "source-side spine remains nonclaim")
    add("V956_4_left_hand_gates_mapped", left_gates_mapped, "left-hand EH/Newton gates mapped")
    add("V956_5_hidden_current_gates_mapped", hidden_gates_mapped, "hidden-current bypass gates mapped")
    add("V956_6_reduction_equation_spine_mapped", equation_spine_mapped, "reduction equation residual split mapped")
    add("V956_7_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V956_8_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V956_9_next_target_selected", target_selected, "957 parent-local-GR spine ledger selected")
    add("V956_10_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V956_11_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V956_12_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    source_spine_rows: list[dict[str, str]],
    left_gate_rows: list[dict[str, str]],
    hidden_rows: list[dict[str, str]],
    equation_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 956 Y5 R10: Source-Side GR Reduction Spine And Left-Hand EH Gate Map

Status: `Y5_R10_956_source_side_spine_consolidated_left_hand_EH_Newton_gates_mapped_nonclaim`

Claim ceiling: `structural_map_only_no_source_side_claim_no_EH_claim_no_Newton_claim_no_local_GR_claim`

## Result

This checkpoint gives the cleanest local-GR bridge map so far.

The source side is no longer foggy. The conditional route is: one observed coframe, no species-label source functor, total Hilbert variation of one matter action, no source-only relative `w_A`, and one common `kappa_univ` calibrated to measured `G`. If those parent clauses are signed, the right-hand side becomes the ordinary GR/Newton matter source.

But that is only half the bridge. The left-hand side still needs EH/operator selection, extra-sector silence, one-parameter no-hair, measured-GM/worldtube calibration, constant source normalization, and full PPN vector completion. EH baseline machinery exists, but it does not silence MTS extra sectors by itself.

So the honest state is: source-side spine sharpened; full GR/Newton reduction not claimable yet.

```text
RHS route: kappa_univ T_total, conditional but sharp.
LHS route: EH + zero/bounded residuals, still open.
Newton route: needs measured-GM/worldtube calibration plus no extra Poisson hair.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Source-Side GR/Newton Spine

{md_table(source_spine_rows, ["spine_id", "condition", "current_status", "if_closed", "remaining_blocker"])}

## Left-Hand EH/Newton Gate Map

{md_table(left_gate_rows, ["gate_id", "required_condition", "current_status", "blocks", "next_action"])}

## Hidden-Current Bypass Gates

{md_table(hidden_rows, ["hidden_id", "channel", "risk", "current_status", "required_closure", "feeds_gate"])}

## Reduction Equation Spine

{md_table(equation_rows, ["equation_id", "equation", "GR_limit_condition", "Newton_limit_condition", "current_status"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    source_spine_rows = source_side_spine()
    left_gate_rows = left_hand_gate_map()
    hidden_rows = hidden_current_gate_map()
    equation_rows = reduction_equation_spine()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        source_spine_rows,
        left_gate_rows,
        hidden_rows,
        equation_rows,
        decision_rows,
        claim_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_956_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv",
        source_spine_rows,
        [
            "spine_id",
            "condition",
            "mathematical_form",
            "current_status",
            "if_closed",
            "remaining_blocker",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv",
        left_gate_rows,
        [
            "gate_id",
            "required_condition",
            "mathematical_form",
            "prior_evidence",
            "current_status",
            "blocks",
            "next_action",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_956_HIDDEN_CURRENT_BYPASS_GATES.csv",
        hidden_rows,
        ["hidden_id", "channel", "risk", "current_status", "required_closure", "feeds_gate", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_956_REDUCTION_EQUATION_SPINE.csv",
        equation_rows,
        [
            "equation_id",
            "equation",
            "GR_limit_condition",
            "Newton_limit_condition",
            "current_status",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_956_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_956_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_956_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_956_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, source_spine_rows, left_gate_rows, hidden_rows, equation_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()
