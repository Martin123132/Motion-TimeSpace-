from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3559-Y5-R2FR-Hilbert-identity-PiM-chainmap-source-support-adoption-or-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_HILBERT_IDENTITY_PIM_SOURCE_SUPPORT_3559"
CHECKPOINT_ID = "3559"


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


def sources() -> dict[str, Path]:
    return {
        "handoff_3558": RESIDUALS / "P8_Y5_R2FR_3558_NEXT_TARGET.csv",
        "closure_theorem_3558": RESIDUALS / "P8_Y5_R2FR_3558_HILBERT_CURRENT_CLOSURE_THEOREM.csv",
        "coefficients_3558": RESIDUALS / "P8_Y5_R2FR_3558_COEFFICIENT_FILL_ROWS.csv",
        "pim_adoption_contract_3445": RESIDUALS / "P8_Y5_R2FR_3445_HILBERT_IDENTITY_PIM_PARENT_ADOPTION_CONTRACT.csv",
        "pim_chainmap_theorem_3426": RESIDUALS / "P8_Y5_R2FR_3426_PIM_CHAIN_MAP_THEOREM.csv",
        "pim_route_compare_3550": RESIDUALS / "P8_Y5_R2FR_3550_PIM_CHAINMAP_ROUTE_COMPARE.csv",
        "pim_htau_derivation_3514": RESIDUALS / "P8_Y5_R2FR_3514_PIM_HTAU_COMMUTATOR_DERIVATION.csv",
        "pim_htau_components_3514": RESIDUALS / "P8_Y5_R2FR_3514_PIM_HTAU_RESIDUAL_COMPONENTS.csv",
        "pim_htau_zero_3532": RESIDUALS / "P8_Y5_R2FR_3532_PIM_HTAU_ZERO_PROOF.csv",
        "source_connection_law_3515": RESIDUALS / "P8_EM_source_branch_mass_connection_flatness_law.csv",
        "source_coordinate_descent_3516": RESIDUALS / "P8_EM_quotient_source_coordinate_descent_certificate.csv",
        "htau_qbasic_3552": RESIDUALS / "P8_Y5_R2FR_3552_HTAU_QBASIC_THEOREM.csv",
        "mhref_descent_3551": RESIDUALS / "P8_Y5_R2FR_3551_MHREF_DESCENT_THEOREM.csv",
        "worldtube_owner_2611": RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
        "dq_vertical_2570": RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv",
        "ellj_source_owner": RESIDUALS / "P8_EM_ellJ_source_current_owner_residual_law.csv",
        "actual_q_candidate": RESIDUALS / "P8_EM_actual_q_map_vertical_basis_candidate.csv",
        "parent_source_identity": RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3558": "declares 3559 target",
        "closure_theorem_3558": "imports exact d(Pi_M J_H) obstruction identity",
        "coefficients_3558": "imports active coefficient rows to split Pi_M operator from support drift",
        "pim_adoption_contract_3445": "preferred Hilbert identity Pi_M branch contract",
        "pim_chainmap_theorem_3426": "identity/inclusion chainmap theorem and old-topological demotion",
        "pim_route_compare_3550": "route comparison selecting Hilbert identity/inclusion as least-scrutiny path",
        "pim_htau_derivation_3514": "local coordinate commutator and source-branch bundle identity",
        "pim_htau_components_3514": "C_M/C_shape/C_domain/C_frame residual components",
        "pim_htau_zero_3532": "conditional zero mechanism for Pi_M/H_tau square",
        "source_connection_law_3515": "source-coordinate connection law A_X=dY(v_X)",
        "source_coordinate_descent_3516": "q-basic source-coordinate descent theorem",
        "htau_qbasic_3552": "H_tau q-basic theorem and integrability guard",
        "mhref_descent_3551": "M_H_ref descent through H_tau-H_ref",
        "worldtube_owner_2611": "worldtube/source-support parent ownership audit",
        "dq_vertical_2570": "actual q-map and vertical-generator ledger",
        "ellj_source_owner": "source-current owner residual law",
        "actual_q_candidate": "candidate visible q-map slots and anti-tautology guard",
        "parent_source_identity": "parent source identity and projected flux obstruction",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def adoption_theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "PIA3559_0_typed_Hilbert_mass_current_complex",
            "name": "typed Hilbert mass-current complex",
            "statement": "Define C_H^M(W,e_obs,tau) as the typed Hilbert mass-current complex built from the same observed coframe, time generator, and source collar before any orbital/R10/PPN readout.",
            "derivation": "This is a branch definition imported from the Hilbert identity Pi_M contract: the active current is not an old topological projector output and not a fitted GM object.",
            "moves_forward": "separates the mass-current object from post-fit projector choices",
            "required_premises": "same e_obs/tau; parent-owned W_source; ordinary matter+EM stress included in T_H; no readout mask",
            "current_status": "ADOPTED_AS_PRIVATE_PREFERRED_BRANCH_CONTRACT",
            "source_path": str(source_paths["pim_adoption_contract_3445"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "PIA3559_1_identity_chainmap_zero",
            "name": "identity Pi_M chainmap zero",
            "statement": "On C_H^M, take Pi_M^H as the identity/inclusion of the typed Hilbert mass-current slot. Then [d,Pi_M^H]J_H^M=0 exactly on that fixed complex.",
            "derivation": "For an identity/inclusion chain map, d(Pi_M^H J_H^M)-Pi_M^H(dJ_H^M)=dJ_H^M-dJ_H^M=0. No independent Hodge, Green, DeWitt, metric-domain, or post-fit orbital projector is being varied.",
            "moves_forward": "kills the independent Pi_M operator commutator on the preferred typed branch",
            "required_premises": "Pi_M^H is not replaced by old Pi_M; C_H^M domain fixed; all metric variation is inside T_H and Q_tau",
            "current_status": "EXACT_ON_TYPED_COMPLEX_BRANCH_ADOPTED",
            "source_path": str(source_paths["pim_chainmap_theorem_3426"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "PIA3559_2_operator_vs_support_split",
            "name": "operator/support split",
            "statement": "The old symbol [d,Pi_M]J_H must now be split into a zero operator piece [d,Pi_M^H]J_H^M and a live source-support/domain piece Delta_support when W_source, tau, frame, H_ref, or q-basic source coordinates drift.",
            "derivation": "3558 left [d,Pi_M]J_H as a combined obstruction. 3559 adopts the identity operator route, so what remains cannot be blamed on an independent Pi_M operator; it belongs to support/domain/frame/source-coordinate residual rows.",
            "moves_forward": "turns a vague projector obstruction into named live residuals",
            "required_premises": "branch adoption and no old topological Pi_M laundering",
            "current_status": "EXACT_REFACTOR_NONCLAIM",
            "source_path": str(source_paths["closure_theorem_3558"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "PIA3559_3_qbasic_source_support_zero_route",
            "name": "q-basic source-support zero route",
            "statement": "If Y=(M_H_ref,sigma^a)=Ybar(q(Phi)) and v_X is in ker(Dq), then A_X=dY(v_X)=0, so C_M=C_shape=0 and the source-coordinate part of Delta_support vanishes.",
            "derivation": "By the chain rule, dY(v_X)=dYbar(Dq(v_X))=0. Mass-flatness then follows as a corollary: partial_M A_X^M=partial_M A_X^a=0.",
            "moves_forward": "identifies the actual derivation target for the remaining coupling/source support problem",
            "required_premises": "actual q map; actual vertical basis; q-basic M_H_ref; q-basic worldtube/shape coordinates; no readout-defined source mass",
            "current_status": "EXACT_CONDITIONAL_ZERO_THEOREM_NOT_LIVE",
            "source_path": str(source_paths["source_coordinate_descent_3516"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "PIA3559_4_reduced_closure_obstruction",
            "name": "reduced closure obstruction after Pi_M^H adoption",
            "statement": "After adopting Pi_M^H on C_H^M, the local source closure gate reduces to Pi_M^H dJ_extra=0, A_parent=0, Delta_support=0, and exterior side flux=0; the independent Pi_M operator-stress branch is no longer the preferred obstruction.",
            "derivation": "Substitute [d,Pi_M^H]J_H^M=0 into the 3558 identity, while keeping support/domain changes outside the fixed complex as Delta_support rather than hiding them in Pi_M.",
            "moves_forward": "shrinks the boss fight from projector algebra to source support, extra mass current, anomaly, and side flux",
            "required_premises": "typed complex fixed before readout and all live support terms retained",
            "current_status": "REDUCED_GATE_WITH_LIVE_RESIDUALS",
            "source_path": str(source_paths["parent_source_identity"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def clause_audit(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "CLA3559_0_C_HM_branch",
            "C_H^M(W,e_obs,tau) typed Hilbert mass-current complex exists before readout",
            "ADOPTED_PRIVATE_BRANCH_CONTRACT",
            "Not a full public theorem, but safe as the preferred private branch because it is explicit and nonclaim.",
            "pim_adoption_contract_3445",
        ),
        (
            "CLA3559_1_PiMH_identity",
            "Pi_M^H is identity/inclusion on C_H^M",
            "EXACT_OPERATOR_ZERO_ON_FIXED_COMPLEX",
            "This closes the independent operator commutator, not the source-support drift.",
            "pim_chainmap_theorem_3426",
        ),
        (
            "CLA3559_2_old_PiM_demoted",
            "old topological/Hodge/readout Pi_M not used in preferred local source branch",
            "DEMOTION_LOCK_ACTIVE",
            "If old Pi_M re-enters, equality and boundary-zero rows reactivate.",
            "pim_route_compare_3550",
        ),
        (
            "CLA3559_3_worldtube_support",
            "W_source=closure(supp J_H[tau]) is parent-owned and fixed before readout",
            "UNSIGNED_REMAINS_LIVE",
            "This is now the main support-domain obstruction.",
            "worldtube_owner_2611",
        ),
        (
            "CLA3559_4_qbasic_MHref",
            "M_H_ref=H_tau-H_ref descends through q",
            "UNSIGNED_REMAINS_LIVE",
            "H_tau integrability and H_ref source-blindness remain required.",
            "mhref_descent_3551",
        ),
        (
            "CLA3559_5_qbasic_shape",
            "source shape/support coordinates sigma^a descend through q",
            "UNSIGNED_REMAINS_LIVE",
            "Worldtube selector and same-frame J_H must be parent-owned.",
            "source_coordinate_descent_3516",
        ),
        (
            "CLA3559_6_actual_vertical_basis",
            "residual directions satisfy Dq(v_X)=0 for the actual q map",
            "MISSING_ACTUAL_QMAP_AND_BASIS",
            "Cannot declare directions invisible by taste; this remains a constructive target.",
            "dq_vertical_2570",
        ),
        (
            "CLA3559_7_no_readout_laundering",
            "source mass, support, and projector are not chosen after seeing orbital GM",
            "GUARD_ACTIVE_NOT_THEOREM",
            "All surviving source/readout drift gets explicit coefficient rows.",
            "actual_q_candidate",
        ),
        (
            "CLA3559_8_tau_eobs_lock",
            "same tau/e_obs branch feeds Hilbert source, H_tau, clocks, orbit and R10 readout",
            "CONDITIONAL_UNSIGNED",
            "The same-frame rule is written, but parent branch still has to own it globally.",
            "closure_theorem_3558",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "clause_id": clause_id,
            "required_clause": required_clause,
            "status": status,
            "effect": effect,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for clause_id, required_clause, status, effect, source_key in rows
    ]


def obstruction_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "OBS3559_0_Delta_PiM_operator",
            "[d,Pi_M^H]J_H^M",
            "Pi_M operator commutator on the typed Hilbert current",
            "THEOREM_ZERO_ON_FIXED_C_HM",
            "Pi_M^H=id/inclusion and old Pi_M demoted",
            "No longer counted as an independent live obstruction on the preferred branch.",
            "pim_chainmap_theorem_3426",
        ),
        (
            "OBS3559_1_Delta_support",
            "D_X W_source; D_X sigma^a",
            "source support/domain/shape drift outside the fixed C_H^M complex",
            "LIVE_UNSIGNED",
            "W_source=closure(supp J_H[tau]) parent-owned and q-basic",
            "Cannot be killed by identity Pi_M; it is the next actual derivation target.",
            "worldtube_owner_2611",
        ),
        (
            "OBS3559_2_C_M",
            "partial_M A_X^M",
            "mass-coordinate source connection curvature",
            "LIVE_UNSIGNED",
            "M_H_ref q-basic and Dq(v_X)=0",
            "Killed if source-coordinate quotient descent fires.",
            "source_connection_law_3515",
        ),
        (
            "OBS3559_3_C_shape",
            "partial_M A_X^a",
            "shape/source-sector leakage into the mass branch",
            "LIVE_UNSIGNED",
            "sigma^a q-basic and Dq(v_X)=0",
            "Killed if worldtube shape descends through q.",
            "source_coordinate_descent_3516",
        ),
        (
            "OBS3559_4_C_domain_C_frame",
            "C_domain+C_frame",
            "surface/collar/frame drift under source readout",
            "LIVE_UNSIGNED",
            "same tau/e_obs/surface branch fixed before readout",
            "Needs a source-support adoption theorem or bound rows.",
            "pim_htau_components_3514",
        ),
        (
            "OBS3559_5_PiM_extra_mass",
            "Pi_M^H dJ_extra",
            "extra hidden/domain/memory/boundary/current mass projection",
            "LIVE_UNSIGNED",
            "zero extra mass-channel theorem or sourced mu_extra vector",
            "Survives 3559 and remains one of the true local-GR gates.",
            "coefficients_3558",
        ),
        (
            "OBS3559_6_parent_anomaly",
            "A_parent",
            "parent anomaly, multiplier, boundary, or non-EH source residue",
            "LIVE_UNSIGNED",
            "parent Ward/Euler identity with no leftover source term",
            "Survives 3559 and must not be canceled by source fitting.",
            "parent_source_identity",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "obstruction_id": obstruction_id,
            "symbol": symbol,
            "meaning": meaning,
            "status": status,
            "zero_condition": zero_condition,
            "decision_effect": decision_effect,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for obstruction_id, symbol, meaning, status, zero_condition, decision_effect, source_key in rows
    ]


def coefficient_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "CF3559_0_Delta_PiM_operator",
            "projector_operator",
            "Delta_PiM_operator",
            "[d,Pi_M^H]J_H^M on fixed typed Hilbert current complex",
            "THEOREM_ZERO_ON_PREFERRED_BRANCH",
            "dimensionless_operator_norm",
            "exact zero only inside C_H^M",
            "no numeric row needed unless old PiM branch is reintroduced",
            "pim_chainmap_theorem_3426",
            True,
        ),
        (
            "CF3559_1_Delta_PiM_old_top",
            "old_projector_equivalence",
            "R_eq_top;B_zero_flux;I_commutator_top",
            "old topological/Hodge PiM equality failure against Pi_M^H",
            "DEMOTED_TO_BOUND_BRANCH",
            "dimensionless_or_boundary_flux_units",
            "must be zero before old PiM can be used",
            "P8_old_PiM_equivalence_or_bound.csv",
            "pim_route_compare_3550",
            False,
        ),
        (
            "CF3559_2_Delta_support",
            "source_support_domain",
            "Delta_W;C_domain;C_shape",
            "worldtube/support/domain/shape drift outside fixed Hilbert current complex",
            "MISSING_SOURCE_SUPPORT_QBASIC_THEOREM_OR_BOUND",
            "dimensionless_or_length_weighted",
            "PPN;R10;orbital_GM;Gdot locks",
            "P8_source_support_qbasic_or_bound_vector.csv",
            "worldtube_owner_2611",
            False,
        ),
        (
            "CF3559_3_C_M",
            "source_mass_coordinate",
            "C_M;A_X^M;partial_M_A_XM",
            "mass-coordinate source-connection curvature",
            "MISSING_MHREF_QBASIC_DESCENT_OR_BOUND",
            "dimensionless_operator_norm",
            "Gdot/orbital/R10 denominator locks",
            "P8_source_mass_coordinate_connection_bound.csv",
            "source_connection_law_3515",
            False,
        ),
        (
            "CF3559_4_C_frame",
            "same_frame_source_readout",
            "C_frame;Delta_tau;Delta_eobs",
            "tau/coframe/frame drift between source and local readout",
            "MISSING_SAME_FRAME_PARENT_LOCK_OR_BOUND",
            "dimensionless",
            "PPN alpha_i;clock;R10;orbital",
            "P8_same_frame_source_support_bound.csv",
            "closure_theorem_3558",
            False,
        ),
        (
            "CF3559_5_E_Dq_source",
            "actual_q_vertical_basis",
            "E_Dq_source;Dq(v_X)",
            "failure of the live residual direction to be vertical for the actual q map",
            "MISSING_ACTUAL_QMAP_VERTICAL_BASIS",
            "map_norm",
            "no local invisibility claim without this",
            "P8_actual_qmap_source_vertical_basis.csv",
            "dq_vertical_2570",
            False,
        ),
        (
            "CF3559_6_mu_extra_after_PiMH",
            "extra_mass_projection",
            "Pi_M^H dJ_extra;mu_extra",
            "extra-sector mass projection after Pi_M^H operator adoption",
            "MISSING_ZERO_THEOREM_OR_CHANNEL_VECTOR_VALUES",
            "dimensionless_or_channel_declared",
            "R3/R4/R7/R8/R9/R10/R11 locks",
            "P8_mu_extra_after_PiMH_source_vector.csv",
            "coefficients_3558",
            False,
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": coefficient_id,
            "channel": channel,
            "symbol": symbol,
            "definition": definition,
            "current_value_or_theorem": current_value_or_theorem,
            "units": units,
            "bound_or_lock": bound_or_lock,
            "required_artifact": required_artifact,
            "source_path": str(source_paths[source_key]),
            "branch_theorem_zero": branch_theorem_zero,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for coefficient_id, channel, symbol, definition, current_value_or_theorem, units, bound_or_lock, required_artifact, source_key, branch_theorem_zero in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "DEC3559_0",
            "Adopt Pi_M^H as the preferred private local source branch.",
            "This is a real forward move: the independent Pi_M operator commutator is zero on the typed Hilbert current complex, instead of being left as a generic missing target.",
            "no public/local-GR claim; branch adoption only",
        ),
        (
            "DEC3559_1",
            "Move source-support drift out of the Pi_M operator bucket.",
            "The remaining problem is no longer 'the projector' in general; it is W_source/tau/e_obs/H_ref/q-basic source-support ownership.",
            "Delta_support, C_M, C_shape, C_domain and C_frame remain active rows",
        ),
        (
            "DEC3559_2",
            "Forbid old Pi_M from sneaking back into the preferred branch.",
            "Topological/Hodge/readout Pi_M can only return through an explicit equivalence theorem or a bound branch.",
            "prevents conserved-wrong-object laundering",
        ),
        (
            "DEC3559_3",
            "Next target should attack source support directly.",
            "The best next shot is q-basic W_source/M_H_ref descent: prove W_source=closure(supp J_H[tau]) and Y=Ybar(q(Phi)), or produce source-ready support coefficients.",
            "sets up 3560",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "decision": decision,
            "meaning": meaning,
            "claim_effect": claim_effect,
            "valid_for_claim": False,
        }
        for decision_id, decision, meaning, claim_effect in rows
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STAT3559_0",
            "status": "PIMH_OPERATOR_CHAINMAP_ADOPTED_SOURCE_SUPPORT_STILL_OPEN",
            "summary": "Pi_M^H identity/inclusion kills the independent operator commutator on the typed Hilbert current complex; local closure still needs source-support/q-basic descent, zero extra mass projection, zero parent anomaly, and no side flux.",
            "strongest_result": "[d,Pi_M^H]J_H^M=0 on fixed C_H^M",
            "still_missing": "W_source q-basic support, M_H_ref q-basic descent, actual q vertical basis, extra mass projection silence, parent anomaly silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3559_0",
            "target_doc": "3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md",
            "target_script": "scripts/Y5_R2FR_3560_source_support_qbasic_worldtube_descent_or_bound_vector.py",
            "objective": "try to prove W_source=closure(supp J_H[tau]) and Y=(M_H_ref,sigma^a)=Ybar(q(Phi)) on the same e_obs/tau branch; if not, fill Delta_W, C_domain, C_shape, C_frame and E_Dq_source bound rows",
            "success_gate": "source-support drift zero by q-basic descent, or source-support/domain/frame residuals become source-ready nonclaim bound rows",
            "reason": "3559 kills the independent Pi_M operator commutator on the preferred branch; the remaining commutator/source-coupling obstruction is support descent",
            "valid_for_claim": False,
        }
    ]


def validation(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    coeffs: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [str(path) for path in source_paths.values() if not path.exists()]
    parse_failures: list[str] = []
    for path in outputs.values():
        if path.suffix.lower() == ".csv":
            try:
                read_csv(path)
            except Exception as exc:
                parse_failures.append(f"{path}: {exc}")
    theorem_ids = {str(row["theorem_id"]) for row in theorem}
    clause_ids = {str(row["clause_id"]) for row in clauses}
    obstruction_status = {str(row["obstruction_id"]): str(row["status"]) for row in obstructions}
    coeff_by_id = {str(row["coefficient_id"]): row for row in coeffs}
    unsafe_claims = [
        str(row["coefficient_id"])
        for row in coeffs
        if str(row.get("valid_for_claim", "")).lower() == "true"
        or str(row.get("score_ready", "")).lower() == "true"
        or str(row.get("claim_allowed", "")).lower() == "true"
    ]
    formalization_touched = any(path == FORMALIZATION or FORMALIZATION in path.parents for path in outputs.values())
    rows = [
        (
            "VAL3559_0_sources_exist",
            not missing_sources,
            f"{len(source_paths) - len(missing_sources)}/{len(source_paths)} cited source paths exist" if not missing_sources else "; ".join(missing_sources),
        ),
        (
            "VAL3559_1_generated_csvs_parse",
            not parse_failures,
            f"{sum(1 for path in outputs.values() if path.suffix.lower() == '.csv')} generated CSV files parse" if not parse_failures else "; ".join(parse_failures),
        ),
        (
            "VAL3559_2_identity_chainmap_theorem_present",
            "PIA3559_1_identity_chainmap_zero" in theorem_ids and "PIA3559_2_operator_vs_support_split" in theorem_ids,
            "identity Pi_M chainmap and operator/support split rows present",
        ),
        (
            "VAL3559_3_old_pim_demoted",
            "CLA3559_2_old_PiM_demoted" in clause_ids,
            "old topological/Hodge/readout PiM demotion clause present",
        ),
        (
            "VAL3559_4_operator_zero_support_live_split",
            obstruction_status.get("OBS3559_0_Delta_PiM_operator") == "THEOREM_ZERO_ON_FIXED_C_HM"
            and obstruction_status.get("OBS3559_1_Delta_support") == "LIVE_UNSIGNED",
            "operator piece theorem-zero while support drift remains live",
        ),
        (
            "VAL3559_5_bound_rows_nonclaim",
            not unsafe_claims,
            "all coefficient/bound rows remain nonclaim" if not unsafe_claims else "; ".join(unsafe_claims),
        ),
        (
            "VAL3559_6_required_support_rows_present",
            all(key in coeff_by_id for key in ["CF3559_2_Delta_support", "CF3559_3_C_M", "CF3559_4_C_frame", "CF3559_5_E_Dq_source", "CF3559_6_mu_extra_after_PiMH"]),
            "support, mass-coordinate, frame, Dq and mu_extra rows present",
        ),
        (
            "VAL3559_7_formalization_workbench_untouched",
            not formalization_touched,
            "3559 generated outputs only inside post-checkpoint-work",
        ),
    ]
    return [
        {
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
        }
        for validation_id, passes, detail in rows
    ]


def write_doc(
    output_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    coeffs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    lines = [
        "# 3559 - Hilbert identity PiM chainmap source-support adoption or bound",
        "",
        "## Verdict",
        "3559 takes the branch instead of circling it: the preferred local source branch now adopts `Pi_M^H` as the identity/inclusion on the typed Hilbert mass-current complex `C_H^M(W,e_obs,tau)`. On that fixed complex, the independent operator commutator is exactly zero: `[d,Pi_M^H]J_H^M=0`.",
        "",
        "This is not a local-GR claim. The work moved the live problem out of vague projector algebra and into the real remaining places: source support, q-basic worldtube descent, `M_H_ref`, actual vertical basis, extra mass projection, and parent anomaly/side-flux silence.",
        "",
        "## Reduced obstruction",
        "Starting from 3558, `d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent`.",
        "",
        "After preferred-branch adoption, the fixed-complex operator piece is zero, so the honest reduced gate is:",
        "",
        "`d(Pi_M^H J_H^M)=0` only if `Pi_M^H dJ_extra=0`, `A_parent=0`, `Delta_support=0`, and exterior side flux is zero.",
        "",
        "Here `Delta_support` carries `W_source`, `tau/e_obs`, `H_ref`, source-shape, domain and q-basic descent drift. This is the useful separation.",
        "",
        "## What moved",
        "- `Pi_M` is no longer allowed to mean three things at once; the preferred branch uses `Pi_M^H=id/inclusion`.",
        "- Old topological/Hodge/readout `Pi_M` is demoted unless an equivalence theorem or bound branch is supplied.",
        "- The independent projector operator commutator is theorem-zero on the typed Hilbert current complex.",
        "- Source-support drift is still live and cannot be hidden inside the identity operator.",
        "- The next derivation target is now sharply `W_source`/`Y=(M_H_ref,sigma^a)` q-basic descent.",
        "",
        "## Generated outputs",
    ]
    for name, path in output_paths.items():
        lines.append(f"- `{name}`: `{path}`")
    lines.extend(["", "## Adoption theorem rows"])
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['statement']}")
    lines.extend(["", "## Clause audit"])
    for row in clauses:
        lines.append(f"- `{row['clause_id']}`: {row['required_clause']} -> {row['status']}")
    lines.extend(["", "## Obstruction split"])
    for row in obstructions:
        lines.append(f"- `{row['obstruction_id']}` `{row['symbol']}`: {row['status']} ({row['decision_effect']})")
    lines.extend(["", "## Coefficient / bound rows"])
    for row in coeffs:
        lines.append(f"- `{row['coefficient_id']}` `{row['symbol']}`: {row['current_value_or_theorem']}")
    lines.extend(["", "## Decision ledger"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} {row['meaning']}")
    lines.extend(["", "## Next target", f"- `{next_rows[0]['target_doc']}`", f"- Objective: {next_rows[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    source_rows = source_register(source_paths)
    theorem = adoption_theorem_rows(source_paths)
    clauses = clause_audit(source_paths)
    obstructions = obstruction_rows(source_paths)
    coeffs = coefficient_rows(source_paths)
    decisions = decision_rows()
    statuses = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3559_SOURCE_REGISTER.csv",
        "adoption_theorem": RESIDUALS / "P8_Y5_R2FR_3559_HILBERT_IDENTITY_PIM_ADOPTION_THEOREM.csv",
        "clause_audit": RESIDUALS / "P8_Y5_R2FR_3559_ADOPTION_CLAUSE_AUDIT.csv",
        "obstruction_split": RESIDUALS / "P8_Y5_R2FR_3559_SOURCE_SUPPORT_OBSTRUCTION_MAP.csv",
        "coefficient_bound_rows": RESIDUALS / "P8_Y5_R2FR_3559_COEFFICIENT_BOUND_ROWS.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3559_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3559_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3559_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Hilbert_identity_PiM_chainmap_source_support_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3559_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["adoption_theorem"], theorem)
    write_csv(outputs["clause_audit"], clauses)
    write_csv(outputs["obstruction_split"], obstructions)
    write_csv(outputs["coefficient_bound_rows"], coeffs)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], statuses)
    write_csv(outputs["next_target"], next_rows)
    write_csv(outputs["canonical_status"], [{
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "canonical_status": statuses[0]["status"],
        "strongest_result": statuses[0]["strongest_result"],
        "still_missing": statuses[0]["still_missing"],
        "next_target": next_rows[0]["target_doc"],
        "claim_allowed": False,
        "valid_for_claim": False,
    }])
    validation_rows = validation(source_paths, {key: path for key, path in outputs.items() if key != "validation"}, theorem, clauses, obstructions, coeffs)
    write_csv(outputs["validation"], validation_rows)
    write_doc(outputs, theorem, clauses, obstructions, coeffs, decisions, next_rows)
    for path in [DOC, *outputs.values()]:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
