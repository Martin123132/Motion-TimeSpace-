from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1356"
TITLE = "1356-Y5-R10-RAB-worldtube-Hilbert-source-equality-or-R_eq-Icommutator-fill"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
EQUALITY_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_WORLDTUBE_HILBERT_EQUALITY_ATTEMPT.csv"
RESIDUAL_ROWS_PATH = OUT_DIR / f"{PACK_ID}_REQ_ICOMMUTATOR_FILL.csv"
GUARD_PATH = OUT_DIR / f"{PACK_ID}_NO_CLOSED_WRONG_CHARGE_GUARD.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1356_VALIDATION.csv"


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
            "source_id": "SRC1356_0_1355_doc",
            "source_path": "1355-Y5-R10-RAB-Y5-source-functional-pullback-or-JZ-source-normalization-basis.md",
            "required_anchor": "Current verdict",
            "purpose": "1355 blocks Y5 source-functional pullback and selects worldtube/Hilbert equality.",
        },
        {
            "source_id": "SRC1356_1_1355_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1355_NEXT_TARGET.csv",
            "required_anchor": "NEXT1355_0_1356",
            "purpose": "handoff to 1356.",
        },
        {
            "source_id": "SRC1356_2_1355_links",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1355_Y5_OBSTRUCTION_LINKS.csv",
            "required_anchor": "LINK1355_1_worldtube_glue",
            "purpose": "worldtube glue is the core missing Y5 source-normalization piece.",
        },
        {
            "source_id": "SRC1356_3_parent_worldtube_clauses",
            "source_path": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            "required_anchor": "W504_4_worldtube_source_measure_glue",
            "purpose": "parent worldtube theorem clauses and missing source-measure glue.",
        },
        {
            "source_id": "SRC1356_4_1013_flux_doc",
            "source_path": "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
            "required_anchor": "PFC1013_8_verdict",
            "purpose": "compact-exterior closure attempt and exact measured-GM obstruction.",
        },
        {
            "source_id": "SRC1356_5_1013_vector",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
            "required_anchor": "OBS1013_3_topological_equality_residual",
            "purpose": "R_eq/topological equality residual already identified as nonclaim debt.",
        },
        {
            "source_id": "SRC1356_6_1014_commutator_doc",
            "source_path": "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            "required_anchor": "PCT1014_3_Hilbert_equality",
            "purpose": "Pi_M commutator and topological-Hilbert equality route split.",
        },
        {
            "source_id": "SRC1356_7_1014_coeffs",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1014_COEFFICIENT_BOUND_ROWS.csv",
            "required_anchor": "PCC1014_1_I_commutator",
            "purpose": "coefficient debts for R_eq, I_commutator, B_zero_flux, and projector stress.",
        },
        {
            "source_id": "SRC1356_8_1015_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1015_CLAIM_GATE.csv",
            "required_anchor": "CG1015_3_topological_Hilbert_equality",
            "purpose": "current gate says topological-Hilbert equality is not derived.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def equality_attempt() -> list[dict[str, object]]:
    rows = [
        {
            "clause_id": "WHE1356_0_worldtube_setup",
            "claim_piece": "compact source worldtube and exterior annulus are defined",
            "required_form": "W compact, A=exterior(W) between linking surfaces S1 and S2, no source support in A",
            "derivation_attempt": "Stokes can compare surface charges on S1/S2 once the charge form exists.",
            "current_evidence": "W504_0 gives the setup as allowed.",
            "status": "SETUP_AVAILABLE",
            "if_missing": "no exterior charge comparison can even be formulated",
        },
        {
            "clause_id": "WHE1356_1_parent_Noether_identity",
            "claim_piece": "diffeomorphism-covariant parent action supplies the Noether/Hamiltonian charge",
            "required_form": "delta L = E_A delta phi^A + dTheta; J_tau=Theta(phi,L_tau phi)-i_tau L; on-shell dJ_tau=0 or dQ_tau plus constraints",
            "derivation_attempt": "This is the standard covariant phase-space route, but it needs the explicit MTS parent Lagrangian, boundary term, and time-flow generator.",
            "current_evidence": "W504_1 is conditional; no full parent L, Theta, Q_M[tau] is supplied here.",
            "status": "CONDITIONAL_NOT_PARENT_SUPPLIED",
            "if_missing": "a symbolic conserved charge can be normalized incorrectly",
        },
        {
            "clause_id": "WHE1356_2_Hilbert_source_current",
            "claim_piece": "same-frame Hilbert/source current defines the observed mass density",
            "required_form": "J_H[e_obs] from the matter Hilbert variation and source measure M_source[W]=int_W Pi_M J_H",
            "derivation_attempt": "The source current must be varied in the same coframe/readout used by rods, clocks, and orbital response.",
            "current_evidence": "1355 keeps same-frame/source pullback unsigned.",
            "status": "NOT_PARENT_DERIVED",
            "if_missing": "source-normalization hair can be hidden as fitted GM",
        },
        {
            "clause_id": "WHE1356_3_topological_mass_charge",
            "claim_piece": "topological/exterior charge is the mass charge, not merely a closed current",
            "required_form": "J_M_top=dQ_M[tau] in the exterior and Q_M[tau] is the measured mass generator",
            "derivation_attempt": "Closure gives surface independence, but does not by itself identify which physical source is measured.",
            "current_evidence": "1013 and 1015 warn that a closed wrong charge cannot recover Newton.",
            "status": "CHARGE_IDENTITY_NOT_ENOUGH",
            "if_missing": "the model can conserve the wrong quantity",
        },
        {
            "clause_id": "WHE1356_4_same_object_equality",
            "claim_piece": "projected Hilbert current equals the topological mass current up to an exact boundary term",
            "required_form": "Pi_M J_H = J_M_top + dB_zero, with B_zero_flux theorem-zero on the worldtube/exterior boundary",
            "derivation_attempt": "If this equality were parent-signed, then the exterior surface charge and Hilbert source measure would be the same object.",
            "current_evidence": "PCT1014_3_Hilbert_equality and CG1015_3 remain false.",
            "status": "NOT_DERIVED_KEY_BLOCKER",
            "if_missing": "R_eq must remain as an explicit residual",
        },
        {
            "clause_id": "WHE1356_5_exterior_closure",
            "claim_piece": "compact-exterior projected mass flux closes without extra/projector/anomaly terms",
            "required_form": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H=0 after extra, boundary, projector, and parent-anomaly channels vanish",
            "derivation_attempt": "The product rule isolates the exact obstruction: projected extra current, Pi_M commutator, parent anomaly, and boundary flux.",
            "current_evidence": "PFC1013_8 says closure is not derived; OBS1013 rows are retained.",
            "status": "EXACT_OBSTRUCTION_NOT_ZERO",
            "if_missing": "I_commutator and companion rows must be scored or theorem-zeroed",
        },
        {
            "clause_id": "WHE1356_6_worldtube_glue",
            "claim_piece": "worldtube source measure equals exterior charge before fitting or calibration",
            "required_form": "M_source[W]=int_S Q_M[tau]=M_eff for any valid linking surface S",
            "derivation_attempt": "Gauss/Stokes can prove this only after the same-object equality and boundary silence are parent-signed.",
            "current_evidence": "LINK1355_1 and W504_4 identify this as not derived.",
            "status": "NOT_DERIVED_CORE_MISSING_PIECE",
            "if_missing": "Newton recovery cannot use the charge as measured source mass",
        },
        {
            "clause_id": "WHE1356_7_calibration_Newton_limit",
            "claim_piece": "the same charge reduces to Poisson/GR/Newton with fixed calibration",
            "required_form": "Q_M[tau] -> Komar/ADM/Gauss mass charge and nabla^2 Phi=4 pi G_ref rho_H without fitted-G absorption",
            "derivation_attempt": "A final normalization theorem is needed after equality; otherwise a constant or Z-dependent source offset can masquerade as G.",
            "current_evidence": "1355 no-absorption and 1015 Newton/local-GR gates remain blocked.",
            "status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "if_missing": "local-GR/Newton claim stays closed",
        },
        {
            "clause_id": "WHE1356_8_verdict",
            "claim_piece": "worldtube-Hilbert source equality theorem",
            "required_form": "WHE1356_0 through WHE1356_7 all pass with parent action, Q_M, Pi_M, boundary theorem, and fixed calibration",
            "derivation_attempt": "The attempted proof reduces the problem to a precise equality, but current MTS evidence does not sign the equality.",
            "current_evidence": "same-object equality, exterior closure, worldtube glue, and calibration all remain open.",
            "status": "EQUALITY_THEOREM_NOT_PROVED",
            "if_missing": "retain R_eq, I_commutator, B_zero_flux, projector stress, parent anomaly, and calibration rows as nonclaim",
        },
    ]
    return mark_nonclaim(rows)


def residual_rows() -> list[dict[str, object]]:
    rows = [
        {
            "residual_id": "REQ1356_0_R_eq_integral",
            "symbol": "R_eq[W,S]",
            "definition": "M_source[W] - int_S Q_M[tau]",
            "source_equation": "Pi_M J_H - J_M_top - dB_zero",
            "observable_link": "Newton source normalization; beta_minus_1; orbital GM; R10/R11 cross-checks",
            "units_required": "mass or dimensionless delta GM/GM after normalization",
            "required_to_score": "parent Q_M[tau], Pi_M J_H, B_zero_flux, calibration convention",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "residual_id": "REQ1356_1_I_commutator",
            "symbol": "I_commutator",
            "definition": "int_A [d,Pi_M] J_H",
            "source_equation": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H",
            "observable_link": "projector/source hair; PPN preferred-frame terms; radial Meff drift",
            "units_required": "mass flux or dimensionless projected GM fraction",
            "required_to_score": "explicit Pi_M, domain/topology dependence, J_H frame, exterior annulus A",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "residual_id": "REQ1356_2_B_zero_flux",
            "symbol": "B_zero_flux",
            "definition": "worldtube/exterior boundary contribution from the exact term dB_zero",
            "source_equation": "int_boundary B_zero = 0 required for Pi_M J_H and J_M_top equality",
            "observable_link": "boundary monopole; beta_minus_1; Gdot/G; orbital calibration",
            "units_required": "mass or dimensionless boundary GM fraction",
            "required_to_score": "boundary condition, asymptotic falloff, inner-worldtube matching",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "residual_id": "REQ1356_3_projector_stress_beta_equiv",
            "symbol": "beta_projector",
            "definition": "metric variation of Pi_M and equivalent projector stress in the source channel",
            "source_equation": "delta_g(Pi_M J_H) residual",
            "observable_link": "PPN beta/gamma/preferred-frame residual vector",
            "units_required": "dimensionless PPN coefficient map",
            "required_to_score": "metric response of Pi_M and same-frame source current",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "residual_id": "REQ1356_4_Delta_PiM",
            "symbol": "Delta_PiM",
            "definition": "projector/domain mismatch between topological charge selector and Hilbert source selector",
            "source_equation": "Pi_M^top - Pi_M^Hilbert",
            "observable_link": "source species/material dependence; WEP/source charge residuals",
            "units_required": "dimensionless projector mismatch",
            "required_to_score": "operator-level definition of both projectors and material/source map",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "residual_id": "REQ1356_5_epsilon_radial_Meff",
            "symbol": "epsilon_radial_Meff",
            "definition": "radial dependence of the measured effective mass in a compact exterior annulus",
            "source_equation": "partial_r ln M_eff(r)",
            "observable_link": "orbital acceleration residual; inverse-square law; alpha(lambda)",
            "units_required": "1/length or dimensionless per radial convention",
            "required_to_score": "radial profile for exterior flux leakage and normalization",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "residual_id": "REQ1356_6_parent_anomaly_A_parent",
            "symbol": "A_parent",
            "definition": "parent Noether anomaly or non-EH contribution to mass-current closure",
            "source_equation": "dJ_tau = A_parent plus constraints/off-shell source terms",
            "observable_link": "non-EH operator family; local-GR residual vector",
            "units_required": "mass-current divergence or dimensionless normalized anomaly",
            "required_to_score": "explicit parent Lagrangian and boundary symplectic potential",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
        {
            "residual_id": "REQ1356_7_calibration_PPN_tail",
            "symbol": "Delta_cal_PPN",
            "definition": "closed-charge-to-orbital-readout calibration mismatch after fixing G_ref",
            "source_equation": "G_fit M_charge - G_ref M_source",
            "observable_link": "beta_minus_1; Gdot/G; orbital GM consistency",
            "units_required": "dimensionless fractional calibration vector",
            "required_to_score": "absolute calibration theorem and no-absorption audit",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
        },
    ]
    return mark_nonclaim(rows)


def guard_rows() -> list[dict[str, object]]:
    rows = [
        {
            "guard_id": "GUARD1356_0_closed_wrong_charge",
            "guardrail": "closed exterior charge is not enough for Newton recovery",
            "forbidden_move": "use dQ_M=0 or surface independence as proof that Q_M is measured source mass",
            "allowed_replacement": "prove Pi_M J_H = J_M_top + dB_zero and B_zero_flux=0, or retain R_eq",
            "status": "INSTALLED",
        },
        {
            "guard_id": "GUARD1356_1_no_fitted_G_absorption",
            "guardrail": "do not absorb source residuals into fitted G",
            "forbidden_move": "hide radial/time/species/frame source-normalization terms by redefining G_fit",
            "allowed_replacement": "split constant calibration from Z-dependent residual rows",
            "status": "INSTALLED",
        },
        {
            "guard_id": "GUARD1356_2_no_post_readout_projector",
            "guardrail": "Pi_M must be parent/before-readout, not a mask selected after seeing observables",
            "forbidden_move": "choose Pi_M to remove the measured residual after orbital fitting",
            "allowed_replacement": "derive Pi_M from parent quotient/topological structure before scoring",
            "status": "INSTALLED",
        },
        {
            "guard_id": "GUARD1356_3_no_reference_zero",
            "guardrail": "boundary and calibration zeros require theorems or sourced bounds",
            "forbidden_move": "set B_zero_flux, I_commutator, or R_eq to zero by reference choice",
            "allowed_replacement": "supply theorem-zero certificates or nonclaim numeric source rows",
            "status": "INSTALLED",
        },
    ]
    return mark_nonclaim(rows)


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1356_0_worldtube_Hilbert_equality",
            "claim": "M_source[W]=int_S Q_M[tau]=M_eff is derived",
            "gate_pass": False,
            "reason": "same-object equality, B_zero_flux, and parent Q_M are not signed",
        },
        {
            "gate_id": "GATE1356_1_R_eq_Icomm_bound_ready",
            "claim": "R_eq and I_commutator rows are numeric/source-backed and can be scored",
            "gate_pass": False,
            "reason": "rows are explicit but remain MISSING/nonclaim",
        },
        {
            "gate_id": "GATE1356_2_Newton_GR_recovery",
            "claim": "Newton/local-GR source normalization can reopen",
            "gate_pass": False,
            "reason": "worldtube-Hilbert equality and calibration are blocked",
        },
        {
            "gate_id": "GATE1356_3_no_closed_wrong_charge_claim",
            "claim": "closed-charge guardrail permits a claim",
            "gate_pass": False,
            "reason": "guardrail is installed but forbids promotion until equality is proved",
        },
    ]
    return mark_nonclaim(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1356_0_equality_not_closed",
            "decision": "Worldtube-Hilbert source equality is not derived in this pass.",
            "why": "the proof attempt reduces to Pi_M J_H = J_M_top + dB_zero, but that equality and boundary zero are unsigned",
            "next_action": "keep R_eq and I_commutator explicit",
        },
        {
            "decision_id": "DEC1356_1_residual_rows_retained",
            "decision": "R_eq, I_commutator, boundary, projector, anomaly, radial, and calibration residuals stay nonclaim.",
            "why": "this prevents an accidental closed-wrong-charge Newton recovery",
            "next_action": "derive or source each residual before local-GR/PPN claims reopen",
        },
        {
            "decision_id": "DEC1356_2_best_next_target",
            "decision": "Best next target is the Pi_M commutator/fixed-topology route.",
            "why": "if [d,Pi_M]J_H can be theorem-zeroed, the equality obstruction shrinks to R_eq and boundary/calibration rows",
            "next_action": "try to prove [d,Pi_M]J_H=0 from fixed topology and before-readout Pi_M, or fill I_commutator profile rows",
        },
    ]
    return mark_nonclaim(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1356_0_1357",
            "target_file": "1357-Y5-R10-RAB-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md",
            "target_script": "scripts/Y5_R10_RAB_PiM_commutator_fixed_topology_or_Icommutator_source_profile.py",
            "task": "try to derive [d,Pi_M]J_H=0 from fixed topology, before-readout projector ownership, and compact-exterior source silence; if not, fill I_commutator/source-profile rows",
            "success_condition": "Pi_M commutator theorem-zero certificate, or explicit nonclaim I_commutator profile inputs with units and source paths",
            "do_not": "do not fit G to absorb I_commutator; do not use post-readout Pi_M masks; do not edit formalization-workbench or use GitHub",
        }
    ]
    return mark_nonclaim(rows)


def validate_outputs(
    sources: list[dict[str, object]],
    equality: list[dict[str, object]],
    residuals: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append({"check_id": check_id, "check": check, "status": "PASS" if status else "FAIL", "details": details})

    add(
        "VAL1356_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in equality if row["clause_id"] == "WHE1356_8_verdict")
    add(
        "VAL1356_1_equality_not_promoted",
        "worldtube-Hilbert equality theorem is not promoted",
        verdict["status"] == "EQUALITY_THEOREM_NOT_PROVED" and not verdict["claim_allowed"],
        str(verdict["if_missing"]),
    )

    residual_ids = {str(row["residual_id"]) for row in residuals}
    add(
        "VAL1356_2_required_residuals_present",
        "R_eq and I_commutator residual rows are present",
        {"REQ1356_0_R_eq_integral", "REQ1356_1_I_commutator"}.issubset(residual_ids) and len(residuals) == 8,
        f"residual_rows={len(residuals)}",
    )

    add(
        "VAL1356_3_residuals_nonclaim",
        "residual rows remain missing/unscored/nonclaim",
        all(row["value_or_theorem"] == "MISSING" and not row["accepted_for_scoring"] and not row["claim_allowed"] for row in residuals),
        "all residual rows reject scoring",
    )

    guard_ids = {str(row["guard_id"]) for row in guards}
    add(
        "VAL1356_4_closed_wrong_charge_guard",
        "closed-wrong-charge guardrail is installed",
        "GUARD1356_0_closed_wrong_charge" in guard_ids and all(row["status"] == "INSTALLED" for row in guards),
        ";".join(sorted(guard_ids)),
    )

    add(
        "VAL1356_5_claim_gates_blocked",
        "all claim gates remain blocked",
        all((row["gate_pass"] is False) and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + equality + residuals + guards + gates + decisions + next_target
    add(
        "VAL1356_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1356*", "*1356-Y5-R10-RAB-worldtube-Hilbert*", "*Y5_R10_RAB_worldtube_Hilbert*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1356_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1356_8_next_target_1357",
        "next target routes to PiM commutator/fixed-topology route",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1357-Y5-R10-RAB-PiM-commutator"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1356_9_overall",
        "overall 1356 validation",
        all(row["status"] == "PASS" for row in validations),
        "1356 blocks worldtube-Hilbert equality claim and retains R_eq/I_commutator residuals",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    equality: list[dict[str, object]],
    residuals: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1356 does not derive the worldtube-Hilbert source equality. A closed exterior/topological charge is not enough: the current proof attempt still needs `Pi_M J_H = J_M_top + dB_zero`, boundary silence, parent charge ownership, and fixed calibration.",
            "**Main progress:** the exact failure point is now cleaner. Newton/local-GR recovery cannot use a closed wrong charge; the live debts are `R_eq`, `I_commutator`, `B_zero_flux`, projector stress, parent anomaly, radial `M_eff` leakage, and calibration tails.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Worldtube-Hilbert equality attempt",
            table(["clause_id", "claim_piece", "required_form", "status", "if_missing"], equality),
            "## R_eq and I_commutator residual rows",
            table(["residual_id", "symbol", "definition", "source_equation", "observable_link", "units_required", "value_or_theorem", "accepted_for_scoring", "status"], residuals),
            "## Closed-wrong-charge guard",
            table(["guard_id", "guardrail", "forbidden_move", "allowed_replacement", "status"], guards),
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
    equality = equality_attempt()
    residuals = residual_rows()
    guards = guard_rows()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, equality, residuals, guards, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(EQUALITY_ATTEMPT_PATH, equality)
    write_csv(RESIDUAL_ROWS_PATH, residuals)
    write_csv(GUARD_PATH, guards)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, equality, residuals, guards, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
