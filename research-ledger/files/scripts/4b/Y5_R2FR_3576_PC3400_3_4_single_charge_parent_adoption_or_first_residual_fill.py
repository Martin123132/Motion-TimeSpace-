from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3576-Y5-R2FR-PC3400-3-4-single-charge-parent-adoption-or-first-residual-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_PC3400_SINGLE_CHARGE_ADOPTION_3576"
CHECKPOINT_ID = "3576"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def sources() -> dict[str, Path]:
    return {
        "handoff_3575": RESIDUALS / "P8_Y5_R2FR_3575_NEXT_TARGET.csv",
        "theorem_3575": RESIDUALS / "P8_Y5_R2FR_3575_SINGLE_CHARGE_THEOREM.csv",
        "req_derivation_3575": RESIDUALS / "P8_Y5_R2FR_3575_REQ_ZERO_DERIVATION.csv",
        "selector_3575": RESIDUALS / "P8_Y5_R2FR_3575_BRANCH_SELECTOR_AND_RESIDUAL_ENVELOPE.csv",
        "hgm_gates_3575": RESIDUALS / "P8_Y5_R2FR_3575_HAMILTONIAN_GM_GLUE_GATES.csv",
        "residual_rows_3575": RESIDUALS / "P8_Y5_R2FR_3575_RESIDUAL_FILL_ROWS.csv",
        "status_3575": RESIDUALS / "P8_Y5_R2FR_3575_STATUS.csv",
        "pc3400_patch": RESIDUALS / "P8_Y5_R2FR_3400_ADOPTION_PATCH_PACKET_NONCLAIM.csv",
        "pc3400_clauses": RESIDUALS / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
        "pc3400_adoption": RESIDUALS / "P8_Y5_R2FR_3424_PC3400_ADOPTION_AUDIT.csv",
        "pc3400_lock": RESIDUALS / "P8_Y5_R2FR_3425_PC3400_3_LOCK_AUDIT.csv",
        "pc3400_update": RESIDUALS / "P8_Y5_R2FR_3426_PC3400_3_UPDATE.csv",
        "source_coupling_update": RESIDUALS / "P8_Y5_R2FR_3433_PC3400_SOURCE_COUPLING_UPDATE.csv",
        "newton_ppn_update": RESIDUALS / "P8_Y5_R2FR_3434_PC3400_NEWTON_PPN_UPDATE.csv",
        "htau_update": RESIDUALS / "P8_Y5_R2FR_3446_PC3400_3_HTAU_UPDATE.csv",
        "pim_chainmap": RESIDUALS / "P8_Y5_R2FR_3426_PIM_CHAIN_MAP_THEOREM.csv",
        "source_descent": RESIDUALS / "P8_EM_quotient_source_coordinate_descent_certificate.csv",
        "mass_flat_zero": RESIDUALS / "P8_Y5_R2FR_3550_MASS_FLAT_ZERO_PROOF_ATTEMPT.csv",
        "ham_contract": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "poynting_bound": RESIDUALS / "P8_Y5_R2FR_3249_SOURCE_WORLDTUBE_POYNTING_BOUND_ROW.csv",
        "newton_zero": RESIDUALS / "P8_Y5_R2FR_3399_FIRST_ORDER_NEWTON_ZERO_THEOREM.csv",
        "newton_chain": RESIDUALS / "P8_Y5_R2FR_3399_NEWTON_CLOSURE_CHAIN.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": "3576 parent-branch adoption/source-coupling input",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def candidate_parent_branch_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "ADOPT3576_0_branch",
            "single local weak-field branch",
            "Fix g_obs/e_obs, q(Phi), tau, H_tau, H_ref, Pi_M^H, kappa_MTS and source support before Newton/PPN scoring.",
            "PC3400_0",
            "INTERNAL_CANDIDATE_SIGNED",
            "pc3400_clauses",
            "This blocks fitted-G/source-mask backfill inside the private candidate branch.",
        ),
        (
            "ADOPT3576_1_kappa",
            "constant universal coupling",
            "Set kappa_MTS=8*pi*G_ref/c^4 as a branch constant with no source/species/range/frame/domain labels.",
            "PC3400_1",
            "INTERNAL_CANDIDATE_SIGNED_NOT_SI_DERIVED",
            "pc3400_adoption",
            "This follows the GR-style rule: derive no drift, do not pretend to derive the measured SI value of G.",
        ),
        (
            "ADOPT3576_2_same_matter_source",
            "same Hilbert matter source",
            "S_matter depends on parent geometry only through e_obs(q(Phi)); J_H[tau], T_H, M_H and source density come from the same variation.",
            "PC3400_2",
            "INTERNAL_CANDIDATE_SIGNED_FOR_PUBLIC_MATTER_EM",
            "pc3400_adoption",
            "Hidden/constitutive matter sectors would reopen as residuals.",
        ),
        (
            "ADOPT3576_3_PiM_identity",
            "Pi_M^H identity/inclusion branch",
            "Pi_M:=Pi_M^H on the Hilbert mass-current complex, so Pi_M J_H=J_H, [d,Pi_M]J_H=0, and delta_g Pi_M has no independent projector stress.",
            "PC3400_3",
            "INTERNAL_CANDIDATE_SIGNED_BY_3426_3575",
            "theorem_3575",
            "This is the main 3576 adoption: old independent topological Pi_M stays demoted.",
        ),
        (
            "ADOPT3576_4_R_eq_Bzero",
            "same-worldtube R_eq/B_zero flux closure",
            "Choose J_M^top from the same Hilbert worldtube charge and B_zero from the exact difference; then R_eq=0 and int_boundary dB_zero=0 at flux/cohomology level.",
            "PC3400_4_partial",
            "INTERNAL_CANDIDATE_SIGNED_BY_3575_IF_NO_HARMONIC_REMAINDER",
            "req_derivation_3575",
            "This signs only the wrong-object/boundary-exact piece, not every extra mass channel.",
        ),
        (
            "ADOPT3576_5_Htau_Href",
            "H_tau/H_ref source denominator",
            "M_H:=H_tau[S_outer]-H_ref with H_ref fixed/source-blind on the branch and tau shared by source, charge, clocks and orbit readout.",
            "PC3400_3",
            "CANDIDATE_DEFINITION_READY_REQUIRES_INTEGRABILITY_AND_POSITIVITY_CHECK",
            "htau_update",
            "This is not fully signed because H_tau curls, H_ref selection and positive denominator still need a theorem or row.",
        ),
        (
            "ADOPT3576_6_no_extra_mass",
            "no unowned compact-source mass",
            "Q_nonEH+Q_boundary+Q_domain+Q_memory+Q_range+Q_delta_kappa+Q_Poynting=0 or retained with explicit bounds.",
            "PC3400_4_remaining",
            "NOT_SIGNED_RETAIN_ROWS_ACTIVE",
            "ham_contract",
            "This is the hard leftover; do not collapse it into the adoption packet.",
        ),
        (
            "ADOPT3576_7_v_ratio_and_PPN_guard",
            "Newton transfer only",
            "Use the existing v-ratio/EH metric-potential fork only for first-order source normalization; beta/full PPN remain downstream.",
            "PC3400_5_6",
            "CONDITIONAL_TRANSFER_ONLY",
            "newton_ppn_update",
            "3576 is source coupling progress, not a local-GR declaration.",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "adoption_id": adoption_id,
            "clause": clause,
            "candidate_parent_statement": statement,
            "pc3400_target": target,
            "adoption_status": status,
            "source_path": str(source_paths[source_key]),
            "consequence": consequence,
            "apply_to_core_now": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for adoption_id, clause, statement, target, status, source_key, consequence in specs
    ]


def pc3400_update_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "PCU3576_0_PC3400_0",
            "PC3400_0_single_branch",
            "STAGED_NOT_ADOPTED",
            "INTERNAL_CANDIDATE_SIGNED",
            "No public claim; branch variables fixed before readout.",
            "pc3400_clauses",
        ),
        (
            "PCU3576_1_PC3400_1",
            "PC3400_1_constant_kappa",
            "CORE_KAPPA_COMPATIBLE_GLOBAL_CLAUSE_NOT_ADOPTED",
            "INTERNAL_CANDIDATE_SIGNED_NOT_SI_DERIVED",
            "G_ref is a universal coupling constant; source/range/species drift is forbidden in branch.",
            "pc3400_adoption",
        ),
        (
            "PCU3576_2_PC3400_2",
            "PC3400_2_same_matter_source",
            "MATTER_ACTION_COMPATIBLE_OBSERVED_COFRAME_AND_ELLJ_NOT_ADOPTED",
            "INTERNAL_CANDIDATE_SIGNED_FOR_PUBLIC_MATTER_EM",
            "Same Hilbert variation supplies source current and EM stress in the public matter branch.",
            "pc3400_adoption",
        ),
        (
            "PCU3576_3_PC3400_3_PiM",
            "PC3400_3_Htau_PiM_chain/PiM",
            "PiM chain map open",
            "SIGNED_IN_INTERNAL_SINGLE_CHARGE_BRANCH",
            "Pi_M^H identity/inclusion kills commutator and independent projector stress.",
            "pim_chainmap",
        ),
        (
            "PCU3576_4_PC3400_3_Htau",
            "PC3400_3_Htau_PiM_chain/Htau_Href",
            "reference/boundary/tau/MHref not claim-ready",
            "CANDIDATE_DEFINITION_RETAINED_ROWS",
            "H_tau/H_ref branch definition is written, but integrability, reference and positivity rows remain.",
            "htau_update",
        ),
        (
            "PCU3576_5_PC3400_4_R_eq",
            "PC3400_4_no_boundary_extra_mass/R_eq_Bzero_commutator",
            "NO_EXTRA_MASS_CLAUSE_NOT_ADOPTED",
            "R_EQ_BZERO_COMMUTATOR_SIGNED_CONDITIONALLY",
            "R_eq=0, Bzero flux=0 and [d,Pi_M]J_H=0 in Hilbert identity single-charge branch.",
            "req_derivation_3575",
        ),
        (
            "PCU3576_6_PC3400_4_extra",
            "PC3400_4_no_boundary_extra_mass/extra_channels",
            "NO_EXTRA_MASS_CLAUSE_NOT_ADOPTED",
            "NOT_SIGNED_RESIDUAL_ROWS_ACTIVE",
            "Poynting, nonEH, domain, memory, range, boundary and coupling extra charges are still explicit rows.",
            "source_coupling_update",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "update_id": update_id,
            "pc_clause": pc_clause,
            "before": before,
            "after": after,
            "delta": delta,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for update_id, pc_clause, before, after, delta, source_key in specs
    ]


def first_residual_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "FR3576_0_epsilon_Req_annulus",
            "epsilon_Req_annulus",
            "0 in B_SC candidate branch; else epsilon_Req_input",
            "dimensionless",
            "CANDIDATE_ZERO_OR_INPUT",
            "selector_3575",
            "wrong-object flux residual",
        ),
        (
            "FR3576_1_epsilon_Bzero_flux",
            "epsilon_Bzero_flux",
            "0 if B_zero is global exact difference with no compact-boundary period; else |int_boundary dB_zero|/|M_eff|",
            "dimensionless",
            "CANDIDATE_ZERO_OR_BOUNDARY_INPUT",
            "req_derivation_3575",
            "boundary exact-term monopole shift",
        ),
        (
            "FR3576_2_epsilon_Href_lock",
            "epsilon_Href_lock",
            "|D_X H_ref|/|M_eff| plus H_tau field-space curl/positivity failure envelope",
            "dimensionless or derivative-normalized",
            "RETAINED_FIRST_ROW_INPUT_MISSING",
            "hgm_gates_3575",
            "Hamiltonian reference/source denominator drift",
        ),
        (
            "FR3576_3_epsilon_extra_mass",
            "epsilon_extra_mass",
            "|Q_nonEH+Q_boundary+Q_domain+Q_memory+Q_range+Q_delta_kappa|/|M_eff|",
            "dimensionless",
            "RETAINED_FIRST_ROW_INPUT_MISSING",
            "ham_contract",
            "unowned compact-source mass channels",
        ),
        (
            "FR3576_4_epsilon_Poynting_worldtube",
            "epsilon_Poynting_worldtube",
            "|int_W Pi_M dJ_Poynting|/|M_eff| or source-collar flux bound",
            "dimensionless",
            "BOUND_FORMULA_READY_INPUTS_MISSING",
            "poynting_bound",
            "EM/wave source-owner flux",
        ),
        (
            "FR3576_5_epsilon_source_coordinate",
            "epsilon_source_coordinate",
            "|A_X^M|+|A_X^shape| unless M_H_ref and sigma^a descend through q",
            "branch/source-coordinate units",
            "RETAINED_UNTIL_Q_MAP_AND_VERTICAL_BASIS",
            "source_descent",
            "source-coordinate leakage under residual directions",
        ),
        (
            "FR3576_6_epsilon_M_total",
            "epsilon_M_total",
            "epsilon_Href_lock+epsilon_extra_mass+epsilon_Poynting_worldtube+epsilon_source_coordinate after R_eq/Bzero/PiM candidate zeroes",
            "dimensionless envelope",
            "EXECUTABLE_NO_CANCELLATION_ENVELOPE",
            "selector_3575",
            "first-order Newton source normalization envelope",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "observable_link": observable,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, formula, units, status, source_key, observable in specs
    ]


def gates_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("GATE3576_0_sources", "source audit", "PASS", "all required 3576 source paths exist"),
        ("GATE3576_1_PC3400_3_PiM", "PC3400_3 Pi_M component", "PASS_INTERNAL_CANDIDATE", "Pi_M^H identity/inclusion branch signed internally; no public claim"),
        ("GATE3576_2_PC3400_3_Htau", "PC3400_3 H_tau/H_ref component", "PARTIAL_RETAIN_ROWS", "candidate definition written, but H_tau curl, H_ref and positivity still need theorem/data"),
        ("GATE3576_3_PC3400_4_Req_Bzero", "PC3400_4 R_eq/Bzero/commutator", "PASS_INTERNAL_CANDIDATE", "R_eq, Bzero flux and commutator zero in single-charge branch under 3575 conditions"),
        ("GATE3576_4_PC3400_4_extra", "PC3400_4 extra mass channels", "FAIL_CURRENT_CLAIM", "Poynting/nonEH/domain/memory/range/coupling channels remain residual rows"),
        ("GATE3576_5_Newton", "first-order Newton", "PARTIAL_NOT_PROMOTED", "epsilon_M narrowed, but full product also needs v ratio and retained residual values"),
        ("GATE3576_6_local_GR", "local GR/PPN", "FAIL_CURRENT_CLAIM", "full PPN/R10/clock/orbital residual vector still open"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths["status_3575"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decisions_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3576_0_candidate_adoption",
            "adopt Hilbert-identity single-charge branch internally",
            "3575 earned enough to sign Pi_M^H/R_eq/Bzero as a private candidate branch, not just leave it as a theorem note.",
            "Future work should test this branch rather than circling generic topological Pi_M.",
            "ADOPTED_INTERNAL_NONCLAIM",
            "theorem_3575",
        ),
        (
            "DEC3576_1_partial_PC3400_4",
            "narrow PC3400_4 instead of falsely closing it",
            "The wrong-object/projector piece is fixed in the branch; Poynting/extra mass is not.",
            "epsilon_M_total is now shorter and more executable.",
            "ADOPTED",
            "selector_3575",
        ),
        (
            "DEC3576_2_next_target",
            "derive or fill the first retained residuals",
            "The next real obstacle is no longer R_eq; it is H_ref/H_tau and extra compact-source mass, especially Poynting/source-worldtube flux.",
            "3577 should attack H_ref/Htau q-basic reference lock first, then Poynting/extra-mass rows.",
            "NEXT_TARGET_SELECTED",
            "hgm_gates_3575",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "valid_for_claim": False,
        }
        for decision_id, decision, reason, consequence, status, source_key in specs
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "SINGLE_CHARGE_BRANCH_INTERNALLY_ADOPTED_FOR_PIM_REQ_BZERO_PC3400_4_NARROWED",
            "strongest_result": "PC3400_3 Pi_M and the PC3400_4 R_eq/Bzero/commutator pieces are internally signed in the Hilbert-identity single-charge branch; PC3400_4 extra-mass and H_tau/H_ref pieces remain explicit residual rows.",
            "still_missing": "H_tau integrability, fixed positive H_ref/M_H denominator, q-basic source-coordinate proof, Poynting/worldtube flux bound or zero theorem, no-extra-mass theorem, v coefficient signature and PPN residual closure",
            "public_claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3576_0",
            "target_doc": "3577-Y5-R2FR-Htau-Href-qbasic-reference-lock-or-source-residual-first-fill.md",
            "target_script": "scripts/Y5_R2FR_3577_Htau_Href_qbasic_reference_lock_or_source_residual_first_fill.py",
            "objective": "derive H_tau/H_ref q-basic reference lock and positive same-frame M_H denominator in the single-charge branch; if not, fill epsilon_Href_lock as the first retained source residual row",
            "success_gate": "H_ref source-blind derivative and H_tau integrability/positivity signed, or epsilon_Href_lock gets source-backed units/formula/first inputs",
            "reason": "3576 narrowed R_eq/PiM; H_tau/H_ref is now the leading PC3400_3 blocker before extra-mass/Poynting rows",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "PC3400_3_4_single_charge_candidate_adoption",
            "status": "PIM_REQ_BZERO_SIGNED_INTERNAL_EXTRA_MASS_HTAU_RETAINED",
            "adopted_zeroes": "Pi_M^H identity; [d,Pi_M]J_H=0; projector stress=0; R_eq=0; B_zero_flux=0 in single-charge branch",
            "retained_rows": "epsilon_Href_lock; epsilon_extra_mass; epsilon_Poynting_worldtube; epsilon_source_coordinate",
            "next_action": "derive H_tau/H_ref q-basic reference lock or fill epsilon_Href_lock",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    adoption: list[dict[str, object]],
    updates: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3576_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3576 source paths exist"))
    needles = {
        "handoff_3575": "NEXT3575_0",
        "theorem_3575": "SCT3575_4_Req_zero_flux",
        "req_derivation_3575": "REQ3575_4_absorb_C",
        "selector_3575": "BSC3575_4_mass_envelope",
        "hgm_gates_3575": "HGM3575_2_Href_lock",
        "residual_rows_3575": "RF3575_4_epsilon_Href_lock",
        "status_3575": "REQ_FLUX_ZERO_CONDITIONAL_THEOREM",
        "pc3400_patch": "PATCH3400_1_formula",
        "pc3400_clauses": "PC3400_4_no_boundary_extra_mass",
        "pc3400_adoption": "PC3400_VERDICT",
        "pc3400_lock": "P3L3425_5_verdict",
        "pc3400_update": "PC3400_3_verdict",
        "source_coupling_update": "PC3400_4",
        "newton_ppn_update": "PC3400_Newton",
        "htau_update": "PCU3446_0_PC3400_3",
        "pim_chainmap": "PCM3426_1_identity_chain_map",
        "source_descent": "QSC3516_1_MHref_descent",
        "mass_flat_zero": "ZP3550_1_MHref_qbasic",
        "ham_contract": "HC5_no_extra_hidden_charge",
        "poynting_bound": "SWP3249_0_source_worldtube_Poynting_bound",
        "newton_zero": "T3399_D2_newton_zero",
        "newton_chain": "NC3399_4_epsilon_M",
    }
    validations.append(("VAL3576_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3576 adoption needles found"))
    validations.append(("VAL3576_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3576 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3576_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3576_4_PiM_adopted_internal", any(row["adoption_id"] == "ADOPT3576_3_PiM_identity" and "INTERNAL_CANDIDATE_SIGNED" in str(row["adoption_status"]) for row in adoption), "Pi_M^H internal candidate adoption present"))
    validations.append(("VAL3576_5_Req_Bzero_adopted_internal", any(row["adoption_id"] == "ADOPT3576_4_R_eq_Bzero" and "R_eq=0" in str(row["candidate_parent_statement"]) for row in adoption), "R_eq/Bzero candidate adoption present"))
    validations.append(("VAL3576_6_extra_mass_retained", any(row["adoption_id"] == "ADOPT3576_6_no_extra_mass" and "NOT_SIGNED" in str(row["adoption_status"]) for row in adoption), "extra mass channels remain retained"))
    validations.append(("VAL3576_7_PC3400_update_present", {"PCU3576_3_PC3400_3_PiM", "PCU3576_5_PC3400_4_R_eq", "PCU3576_6_PC3400_4_extra"}.issubset({str(row["update_id"]) for row in updates}), "PC3400_3/4 update rows present"))
    validations.append(("VAL3576_8_first_residual_rows_present", {"epsilon_Href_lock", "epsilon_extra_mass", "epsilon_Poynting_worldtube", "epsilon_source_coordinate"}.issubset({str(row["symbol"]) for row in residuals}), "first retained residual rows present"))
    validations.append(("VAL3576_9_no_public_promotion", any(row["gate_id"] == "GATE3576_6_local_GR" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "local GR remains unclaimed"))
    validations.append(("VAL3576_10_next_target_selected", any(row["decision_id"] == "DEC3576_2_next_target" for row in decisions), "Htau/Href next target selected"))
    validations.append(("VAL3576_11_no_claim_flags", all(str(row["valid_for_claim"]).lower() == "false" for row in adoption + updates + residuals + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in adoption + updates + residuals + gates + decisions)
    validations.append(("VAL3576_12_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3576*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3576_13_formalization_workbench_untouched", not formalization_touched, "no 3576 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    outputs: dict[str, Path],
    adoption: list[dict[str, object]],
    updates: list[dict[str, object]],
    residuals: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3576 - PC3400_3/4 single-charge parent adoption or first residual fill",
        "",
        "## Verdict",
        "3576 makes the private leap that 3575 earned.  Inside a non-public candidate parent branch, `Pi_M` is adopted as the Hilbert identity/inclusion `Pi_M^H`, and the same-worldtube construction signs the `R_eq/B_zero/[d,Pi_M]` part of `PC3400_4`.",
        "",
        "That means the old wrong-object coupling problem is not the leading blocker anymore in this branch.  The branch now carries these candidate zeroes: `Pi_M^H J_H=J_H`, `[d,Pi_M]J_H=0`, projector stress `=0`, `R_eq=0`, and compact `B_zero` flux `=0`.",
        "",
        "The branch is still not a Newton/local-GR claim.  `H_tau/H_ref` is only a candidate definition, and `epsilon_Href_lock`, `epsilon_extra_mass`, `epsilon_Poynting_worldtube`, and `epsilon_source_coordinate` remain live residual rows.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Candidate adoption"])
    for row in adoption:
        lines.append(f"- `{row['adoption_id']}` `{row['pc3400_target']}`: {row['adoption_status']} — {row['candidate_parent_statement']}")
    lines.extend(["", "## PC3400 update"])
    for row in updates:
        lines.append(f"- `{row['update_id']}` `{row['pc_clause']}`: {row['before']} -> {row['after']} ({row['delta']})")
    lines.extend(["", "## First residual rows"])
    for row in residuals:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} -> {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target", f"- `{next_target[0]['target_doc']}`", f"- Objective: {next_target[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    register = source_register(source_paths)
    adoption = candidate_parent_branch_rows(source_paths)
    updates = pc3400_update_rows(source_paths)
    residuals = first_residual_rows(source_paths)
    gates = gates_rows(source_paths)
    decisions = decisions_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3576_SOURCE_REGISTER.csv",
        "candidate_parent_branch": RESIDUALS / "P8_Y5_R2FR_3576_CANDIDATE_PARENT_BRANCH_ADOPTION_PACKET.csv",
        "pc3400_update": RESIDUALS / "P8_Y5_R2FR_3576_PC3400_3_4_UPDATE.csv",
        "first_residual_rows": RESIDUALS / "P8_Y5_R2FR_3576_FIRST_RETAINED_RESIDUAL_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3576_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3576_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3576_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3576_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_PC3400_single_charge_adoption_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3576_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["candidate_parent_branch"], adoption)
    write_csv(outputs["pc3400_update"], updates)
    write_csv(outputs["first_residual_rows"], residuals)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, adoption, updates, residuals, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, adoption, updates, residuals, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3576 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
