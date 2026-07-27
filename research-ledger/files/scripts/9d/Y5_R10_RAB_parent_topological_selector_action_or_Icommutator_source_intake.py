from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1359"
TITLE = "1359-Y5-R10-RAB-parent-topological-selector-action-or-Icommutator-source-intake"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ACTION_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_SELECTOR_ACTION_ATTEMPT.csv"
OBSTRUCTION_PATH = OUT_DIR / f"{PACK_ID}_SELECTOR_ACTION_OBSTRUCTION_LEDGER.csv"
SOURCE_INTAKE_PATH = OUT_DIR / f"{PACK_ID}_ICOMMUTATOR_SOURCE_INTAKE_LEDGER.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1359_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1359_0_1358_doc",
            "source_path": "1358-Y5-R10-RAB-PiM-fixed-chainmap-parent-signature-or-Icommutator-first-profile-row.md",
            "required_anchor": "PCC1358_0_selector_field_or_constraint",
            "purpose": "1358 identifies parent selector as the first missing fixed-chainmap clause.",
        },
        {
            "source_id": "SRC1359_1_1358_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1358_NEXT_TARGET.csv",
            "required_anchor": "NEXT1358_0_1359",
            "purpose": "handoff to parent topological selector action or source-intake ledger.",
        },
        {
            "source_id": "SRC1359_2_1358_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1358_PARENT_CHAINMAP_CONTRACT.csv",
            "required_anchor": "PCC1358_0_selector_field_or_constraint",
            "purpose": "current parent chain-map contract rows.",
        },
        {
            "source_id": "SRC1359_3_1358_schema",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1358_ICOMMUTATOR_FIRST_PROFILE_ROW_SCHEMA.csv",
            "required_anchor": "IFR1358_0_Icommutator_domain_first_profile",
            "purpose": "first I_commutator profile row schema to turn into source-intake ledger.",
        },
        {
            "source_id": "SRC1359_4_1016_doc",
            "source_path": "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            "required_anchor": "PSC1016_0_parent_action",
            "purpose": "legal source-worldtube selector contract.",
        },
        {
            "source_id": "SRC1359_5_1017_doc",
            "source_path": "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
            "required_anchor": "HRL1017_5_MHref_denominator",
            "purpose": "same-frame Hamiltonian denominator remains blocked.",
        },
        {
            "source_id": "SRC1359_6_1018_doc",
            "source_path": "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
            "required_anchor": "LOC1018_0_LX_owner",
            "purpose": "sector Lagrangian and boundary owner map remains unsigned.",
        },
        {
            "source_id": "SRC1359_7_topo_certificate",
            "source_path": "source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv",
            "required_anchor": "PTEC534_0_fixed_parent_domain",
            "purpose": "topological PiM certificate requirements.",
        },
        {
            "source_id": "SRC1359_8_input_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
            "required_anchor": "PIF537_1_I_commutator",
            "purpose": "required source-intake columns for I_commutator.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def action_attempt() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "PSA1359_0_parent_selector_sector",
            "object": "S_selector",
            "candidate_form": "S_parent = S_MTS[g,Phi] + S_matter[e_obs,psi] + S_selector[chi_M,W_M,omega_M_top,ell_M,lambda_i]",
            "intended_job": "make the mass/source selector part of the parent variational problem before any readout or orbital fit",
            "derivation_status": "CANDIDATE_CONTRACT_ONLY",
            "why_not_claim": "the current corpus has no parent term or principle that requires this selector sector",
        },
        {
            "attempt_id": "PSA1359_1_support_selector",
            "object": "chi_M and W_M",
            "candidate_form": "chi_M is a compact support selector with W_M=supp(chi_M); constraints force (1-chi_M)J_H[tau]=0 and delta_readout W_M=0",
            "intended_job": "select the source worldtube from Hilbert current support before readout",
            "derivation_status": "CONDITIONAL_BUT_NONSIGNED",
            "why_not_claim": "support of J_H[tau] requires e_obs, tau, compactness, regularity, and source-frame ownership first",
        },
        {
            "attempt_id": "PSA1359_2_closed_representative",
            "object": "omega_M_top",
            "candidate_form": "lambda_d wedge d omega_M_top + lambda_N (integral_link omega_M_top - 1)",
            "intended_job": "provide a closed normalized topological representative for the selected worldtube/linking class",
            "derivation_status": "AUXILIARY_CONSTRAINT_ONLY",
            "why_not_claim": "a multiplier can impose closure but does not prove the representative is the observed Hilbert mass channel",
        },
        {
            "attempt_id": "PSA1359_3_mass_functional",
            "object": "ell_M[J_H]",
            "candidate_form": "ell_M[J_H;tau,S] := M_H_ref^-1 integral_S Q_tau^MTS or an equivalent parent Hamiltonian mass functional",
            "intended_job": "turn Pi_M J = ell_M[J] omega_M_top into a source-normalized projection",
            "derivation_status": "BLOCKED_BY_MHREF",
            "why_not_claim": "M_H_ref, Q_tau, H_ref, tau lock, and integrability are not source-backed",
        },
        {
            "attempt_id": "PSA1359_4_projector_definition",
            "object": "Pi_M",
            "candidate_form": "Pi_M J := ell_M[J] omega_M_top on the parent-owned Hilbert-current complex C_H(W_M,A_ext)",
            "intended_job": "make Pi_M a fixed chain-map instead of an empirical mass selector",
            "derivation_status": "CONDITIONAL_CHAINMAP_IF_PRIORS_PASS",
            "why_not_claim": "C_H membership and parent ownership of omega_M_top/ell_M are not proved",
        },
        {
            "attempt_id": "PSA1359_5_chainmap_identity",
            "object": "d Pi_M = Pi_M d",
            "candidate_form": "if d omega_M_top=0, d ell_M[J]=ell_M[dJ] on C_H, and the domain is fixed, then d(Pi_M J)=Pi_M dJ",
            "intended_job": "kill I_commutator by theorem rather than by fit",
            "derivation_status": "CONDITIONAL_LEMMA_ONLY",
            "why_not_claim": "d ell_M[J]=ell_M[dJ] is exactly the source-measure/Hamiltonian lock, not yet derived",
        },
        {
            "attempt_id": "PSA1359_6_no_extra_stress",
            "object": "selector stress and boundary terms",
            "candidate_form": "delta_g S_selector=0 or T_selector is included and bounded; boundary variations of omega_M_top and W_M vanish",
            "intended_job": "avoid creating a new projector stress while trying to solve the old one",
            "derivation_status": "NOT_DERIVED",
            "why_not_claim": "the candidate selector sector can itself create metric/domain/boundary stress",
        },
        {
            "attempt_id": "PSA1359_7_verdict",
            "object": "parent topological selector action",
            "candidate_form": "PSA1359_0 through PSA1359_6 all source-backed by the current MTS parent action",
            "intended_job": "parent-sign chi_M, W_M, omega_M_top, ell_M, and Pi_M before readout",
            "derivation_status": "PARENT_SELECTOR_ACTION_NOT_DERIVED",
            "why_not_claim": "the candidate action is a useful contract, but adding multipliers would be a new closure sector unless justified by the parent theory",
        },
    ]
    return mark_nonclaim(rows)


def obstruction_rows() -> list[dict[str, object]]:
    rows = [
        {
            "obstruction_id": "PSO1359_0_new_auxiliary_sector",
            "obstruction": "selector action may add new auxiliary variables rather than derive them from MTS",
            "risk": "closure axiom masquerades as field-theory derivation",
            "repair": "derive chi_M/omega_M_top/ell_M from existing parent variables or label the selector sector as an explicit extension",
            "status": "OPEN",
        },
        {
            "obstruction_id": "PSO1359_1_nonlocal_support",
            "obstruction": "W_M=closure(supp J_H[tau]) is nonlocal and can be nonsmooth",
            "risk": "variation of support produces domain terms and delta-function boundary stress",
            "repair": "prove compact regular support and differentiable worldtube class, or retain domain I_commutator row",
            "status": "OPEN",
        },
        {
            "obstruction_id": "PSO1359_2_wrong_charge",
            "obstruction": "closed omega_M_top can conserve the wrong object",
            "risk": "topological charge is not the observed Hilbert/Hamiltonian source mass",
            "repair": "prove ell_M is the same-frame Hamiltonian source charge with M_H_ref",
            "status": "OPEN",
        },
        {
            "obstruction_id": "PSO1359_3_chainmap_functional",
            "obstruction": "d ell_M[J]=ell_M[dJ] is not automatic",
            "risk": "I_commutator survives through scalar functional/domain dependence",
            "repair": "derive the Hamiltonian/source-measure lock or keep numerator source-intake row",
            "status": "OPEN",
        },
        {
            "obstruction_id": "PSO1359_4_selector_stress",
            "obstruction": "selector constraints can generate their own stress/boundary response",
            "risk": "fixing Pi_M creates a new local-GR/PPN residual",
            "repair": "compute delta_g S_selector or prove topological metric independence with no boundary variation",
            "status": "OPEN",
        },
        {
            "obstruction_id": "PSO1359_5_denominator_absent",
            "obstruction": "M_H_ref is missing",
            "risk": "I_commutator and R_eq cannot be normalized without borrowing orbital GM",
            "repair": "source or derive same-frame Hamiltonian denominator before scoring",
            "status": "OPEN",
        },
    ]
    return mark_nonclaim(rows)


def source_intake_rows() -> list[dict[str, object]]:
    rows = [
        {
            "intake_id": "ISI1359_0_surface_inner",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "required_item": "inner linking surface S1 or radius r1",
            "required_columns": "system_id;surface_inner_id;r1;surface_definition;links_W_M;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_INNER_RADIUS_OR_SURFACE",
            "acceptance_rule": "must be fixed before readout and linked to W_M",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "ISI1359_1_surface_outer",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "required_item": "outer linking surface S2 or radius r2",
            "required_columns": "system_id;surface_outer_id;r2;surface_definition;homology_class;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_OUTER_RADIUS_OR_SURFACE",
            "acceptance_rule": "must be homologous to S1 in the compact exterior annulus",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "ISI1359_2_numerator",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "required_item": "finite-annulus numerator",
            "required_columns": "system_id;annulus_A;dPiM_domain;J_H_source;integral_value;sign_convention;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_INT_A_DPiM_DOMAIN_JH",
            "acceptance_rule": "numeric value or theorem-zero certificate; no cancellation with other missing components",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "ISI1359_3_denominator",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "required_item": "same-frame source denominator M_H_ref",
            "required_columns": "system_id;tau_id;surface_outer;Q_tau_integral;G_ref;H_ref;M_H_ref;units;reference_rule;source_path;source_anchor;valid_for_claim",
            "current_value": "MISSING_M_H_REF",
            "acceptance_rule": "positive Hamiltonian/Hilbert source denominator; not orbital GM, bare mass, or reference-only 1",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "ISI1359_4_units_normalization",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "required_item": "units and normalization convention",
            "required_columns": "system_id;numerator_units;denominator_units;epsilon_units;normalization;source_path;source_anchor;valid_for_claim",
            "current_value": "dimensionless_after_M_H_ref_normalization",
            "acceptance_rule": "must show numerator/denominator unit compatibility and dimensionless epsilon",
            "status": "SCHEMA_ONLY_NOT_SOURCED",
        },
        {
            "intake_id": "ISI1359_5_source_path",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "required_item": "source path and anchor for every numeric/theorem value",
            "required_columns": "source_path;source_anchor;extraction_method;confidence;valid_for_claim",
            "current_value": "MISSING_SOURCE_PATH;MISSING_SOURCE_ANCHOR",
            "acceptance_rule": "local path must exist or public source must be recorded; anchor must verify the exact value/theorem",
            "status": "MISSING_SOURCE_INPUT",
        },
        {
            "intake_id": "ISI1359_6_no_cheat_flags",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "required_item": "anti-cheat assumptions",
            "required_columns": "no_post_readout_mask;no_fitted_G_absorption;no_orbital_GM_denominator;no_reference_zero;valid_for_claim",
            "current_value": "guardrails_written_but_not_source_backed",
            "acceptance_rule": "all guard flags true before scoring",
            "status": "GUARDRAIL_ONLY",
        },
        {
            "intake_id": "ISI1359_7_acceptance_gate",
            "row_ref": "IFR1358_0_Icommutator_domain_first_profile",
            "required_item": "promotion gate from schema to evidence",
            "required_columns": "all_required_items_present;no_MISSING_markers;all_sources_verified;valid_for_claim",
            "current_value": "BLOCKED",
            "acceptance_rule": "valid_for_claim can only become true after ISI1359_0 through ISI1359_6 pass",
            "status": "CLAIM_BLOCKED",
        },
    ]
    return mark_nonclaim(rows)


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1359_0_selector_contract_written",
            "claim": "minimal parent selector action contract is written",
            "gate_pass": True,
            "reason": "candidate terms for chi_M, W_M, omega_M_top, ell_M, and Pi_M are explicit",
        },
        {
            "gate_id": "GATE1359_1_selector_action_derived",
            "claim": "current MTS derives the parent selector action",
            "gate_pass": False,
            "reason": "candidate selector sector is not sourced by existing parent variables/action",
        },
        {
            "gate_id": "GATE1359_2_chainmap_signed",
            "claim": "Pi_M is parent-signed as a fixed chain-map",
            "gate_pass": False,
            "reason": "support, charge functional, denominator, and selector stress remain open",
        },
        {
            "gate_id": "GATE1359_3_first_Icommutator_row_ready",
            "claim": "first I_commutator source row can be scored",
            "gate_pass": False,
            "reason": "surfaces, numerator, M_H_ref, units provenance, and source path remain missing or schema-only",
        },
        {
            "gate_id": "GATE1359_4_Newton_local_GR",
            "claim": "Newton/local-GR gates can reopen",
            "gate_pass": False,
            "reason": "selector action, chain-map, M_H_ref, R_eq, B_zero, and calibration remain blocked",
        },
    ]
    return mark_nonclaim(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1359_0_action_contract_useful",
            "decision": "The parent selector action can be written as a precise contract.",
            "why": "it identifies the exact objects a future parent action must own: chi_M, W_M, omega_M_top, ell_M, Pi_M, and selector stress",
            "next_action": "test whether the selector sector is local, differentiable, and already implicit in MTS rather than a new closure axiom",
        },
        {
            "decision_id": "DEC1359_1_no_current_derivation",
            "decision": "Current MTS does not derive the selector action.",
            "why": "the candidate uses auxiliary constraints and still lacks M_H_ref/source-measure lock",
            "next_action": "keep chain-map and Newton/local-GR claims blocked",
        },
        {
            "decision_id": "DEC1359_2_source_intake_ready",
            "decision": "The first I_commutator source-intake ledger is ready.",
            "why": "if derivation fails, we now know exactly what data/theorem fields must be filled before any score",
            "next_action": "source M_H_ref and annulus/surface/numerator inputs, or prove them theorem-zero",
        },
    ]
    return mark_nonclaim(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1359_0_1360",
            "target_file": "1360-Y5-R10-RAB-selector-action-locality-differentiability-or-MHref-surface-intake.md",
            "target_script": "scripts/Y5_R10_RAB_selector_action_locality_differentiability_or_MHref_surface_intake.py",
            "task": "test whether the selector action can be made local/covariant/differentiable without new stress; if not, start M_H_ref and S1/S2 source-intake rows for IFR1358_0",
            "success_condition": "selector action locality/differentiability/no-stress certificate, or nonclaim M_H_ref and surface source-intake rows with missing fields explicit",
            "do_not": "do not treat auxiliary multipliers as derivation; do not normalize by orbital GM; do not use post-readout masks; do not edit formalization-workbench or use GitHub",
        }
    ]
    return mark_nonclaim(rows)


def validate_outputs(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    intake: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append({"check_id": check_id, "check": check, "status": "PASS" if status else "FAIL", "details": details})

    add(
        "VAL1359_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in attempts if row["attempt_id"] == "PSA1359_7_verdict")
    add(
        "VAL1359_1_selector_action_not_promoted",
        "parent selector action is a contract, not a current-MTS derivation",
        verdict["derivation_status"] == "PARENT_SELECTOR_ACTION_NOT_DERIVED" and not verdict["claim_allowed"],
        str(verdict["why_not_claim"]),
    )

    add(
        "VAL1359_2_obstructions_open",
        "selector action obstruction ledger stays open",
        len(obstructions) == 6 and all(row["status"] == "OPEN" and not row["claim_allowed"] for row in obstructions),
        f"obstruction_rows={len(obstructions)}",
    )

    required_intake = {
        "ISI1359_0_surface_inner",
        "ISI1359_1_surface_outer",
        "ISI1359_2_numerator",
        "ISI1359_3_denominator",
        "ISI1359_4_units_normalization",
        "ISI1359_5_source_path",
        "ISI1359_6_no_cheat_flags",
        "ISI1359_7_acceptance_gate",
    }
    add(
        "VAL1359_3_intake_ledger_complete",
        "I_commutator source-intake ledger covers surfaces, numerator, denominator, units, sources, guard flags, and acceptance",
        required_intake.issubset({str(row["intake_id"]) for row in intake}),
        f"intake_rows={len(intake)}",
    )

    add(
        "VAL1359_4_intake_nonclaim_missing",
        "intake rows remain missing/schema-only/nonclaim",
        all(not row["claim_allowed"] and str(row["status"]) in {"MISSING_SOURCE_INPUT", "SCHEMA_ONLY_NOT_SOURCED", "GUARDRAIL_ONLY", "CLAIM_BLOCKED"} for row in intake),
        "no intake row can score",
    )

    add(
        "VAL1359_5_claim_gates_block_claim",
        "selector derivation, chainmap, source-row, and Newton claims remain blocked",
        all((row["gate_pass"] is False or row["gate_id"] == "GATE1359_0_selector_contract_written") and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + attempts + obstructions + intake + gates + decisions + next_target
    add(
        "VAL1359_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1359*", "*1359-Y5-R10-RAB-parent-topological-selector*", "*Y5_R10_RAB_parent_topological_selector*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1359_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1359_8_next_target_1360",
        "next target routes to selector-action locality/differentiability or MHref/surface intake",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1360-Y5-R10-RAB-selector-action-locality"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1359_9_overall",
        "overall 1359 validation",
        all(row["status"] == "PASS" for row in validations),
        "1359 writes selector-action contract, blocks derivation claim, and creates I_commutator intake ledger",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    intake: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1359 can write a minimal parent-selector action contract, but current MTS does not derive it. The candidate sector would introduce `chi_M`, `W_M`, `omega_M_top`, `ell_M`, and `Pi_M` constraints; without a parent principle this is closure machinery, not yet a field-theory derivation.",
            "**Main progress:** the route is now boxed in. Either the selector sector must be shown local/covariant/differentiable and already parent-owned, or the fallback is source intake for the first `I_commutator` row: S1/S2 surfaces, numerator, `M_H_ref`, units, provenance, and anti-cheat flags.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Parent selector action attempt",
            table(["attempt_id", "object", "candidate_form", "intended_job", "derivation_status", "why_not_claim"], attempts),
            "## Selector action obstruction ledger",
            table(["obstruction_id", "obstruction", "risk", "repair", "status"], obstructions),
            "## I_commutator source-intake ledger",
            table(["intake_id", "row_ref", "required_item", "required_columns", "current_value", "acceptance_rule", "status"], intake),
            "## Claim gates",
            table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates),
            "## Decision ledger",
            table(["decision_id", "decision", "why", "next_action"], decisions),
            "## Next target",
            table(["next_id", "target_file", "target_script", "task", "success_condition", "do_not"], next_target),
            "## Validation",
            table(["check_id", "check", "status", "details"], validations),
        ]
    ) + "\n"


def main() -> None:
    sources = source_register()
    attempts = action_attempt()
    obstructions = obstruction_rows()
    intake = source_intake_rows()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, attempts, obstructions, intake, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(ACTION_ATTEMPT_PATH, attempts)
    write_csv(OBSTRUCTION_PATH, obstructions)
    write_csv(SOURCE_INTAKE_PATH, intake)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, attempts, obstructions, intake, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
