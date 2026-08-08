from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3683"
BRANCH_ID = "MTS_R2FR_Y5_HILBERT_WORLDTUBE_CHARGE_IDENTITY_OR_RHSRC_BOUND_3683"
DOC = ROOT / "3683-Y5-R2FR-Hilbert-worldtube-charge-identity-or-RHsrc-bound-row.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        rows = load_csv(path)
        return True, len(rows)
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3682", RESIDUALS / "P8_Y5_R2FR_3682_NEXT_TARGET.csv", "R_Hsrc", "3682 selected Hilbert-worldtube charge identity as the next throat"),
        ("identity_1818", RESIDUALS / "P8_Y5_PARENT_QLOC_1818_HILBERT_WORLDTUBE_CHARGE_IDENTITY_THEOREM.csv", "HCI1818_5_residual_decomposition", "1818 gives the target identity and residual decomposition"),
        ("closure_3558", RESIDUALS / "P8_Y5_R2FR_3558_HILBERT_CURRENT_CLOSURE_THEOREM.csv", "HC3558_1_projected_flux_obstruction_identity", "Hilbert flux obstruction identity"),
        ("adoption_3559", RESIDUALS / "P8_Y5_R2FR_3559_HILBERT_IDENTITY_PIM_ADOPTION_THEOREM.csv", "PIA3559_1_identity_chainmap_zero", "identity Pi_M^H chainmap removes the independent projector-operator piece"),
        ("density_3561", RESIDUALS / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv", "HDQ3561_5_live_density_verdict", "density q-basic theorem is clean but not fully live"),
        ("equality_3592", RESIDUALS / "P8_Y5_R2FR_3592_PIM_HILBERT_EQUALITY_ATTEMPT.csv", "PHE3592_7_verdict", "Pi_M/Hilbert equality is not parent-signed"),
        ("worldtube_3596", RESIDUALS / "P8_Y5_R2FR_3596_WORLDTUBE_HILBERT_SOURCE_MEASURE_LOCK.csv", "WSL3596_6_conditional_lock_theorem", "worldtube-Hilbert-source lock theorem is conditional"),
        ("poynting_3612", RESIDUALS / "P8_Y5_R2FR_3612_EM_POYNTING_HILBERT_CLOSURE.csv", "EPC3612_6_closure_rule", "Poynting/EM stress belongs inside Hilbert source only under exact local branch rule"),
        ("hamiltonian_contract", RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC4_charge_equals_PiM_Hilbert_mass", "Hamiltonian boundary charge contract identifies source-current equality as required"),
        ("poisson_contract", RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG1_charge_equals_projected_Hilbert_source", "Poisson/Gauss calibration needs the same charge equals source current"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def identity_audit_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "HCI3683_0_target",
            "prove the Hilbert-worldtube charge identity",
            "G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc with R_Hsrc=0",
            "TARGET_NOT_PROVED",
            "the target is exact, but current corpus only supports subslot reductions",
            False,
        ),
        (
            "HCI3683_1_identity_PiM_operator",
            "independent Pi_M operator commutator vanishes on the typed identity branch",
            "On C_H^M, Pi_M^H is identity/inclusion, so [d,Pi_M^H]J_H^dress = 0 and delta(Pi_M^H J_H^dress)=Pi_M^H delta J_H^dress.",
            "EXACT_TYPED_OPERATOR_ZERO",
            "R_PiMop = 0 on the preferred Hilbert mass-current complex",
            True,
        ),
        (
            "HCI3683_2_static_EM_dressing",
            "minimal stationary EM/Poynting stress is part of dressed Hilbert source",
            "For a common observed Hodge/current and stationary isolated support, bound EM energy and matter-EM exchange sit inside J_H^dress once, not in a separate source residual.",
            "EXACT_CONDITIONAL_ONCE_ONLY_DRESSING",
            "R_EM_bound_duplicate = 0 under the same-denominator branch",
            True,
        ),
        (
            "HCI3683_3_Qtau_equality_gap",
            "Q_tau is not yet proved equal to the dressed Hilbert source charge",
            "The parent Noether/Hamiltonian charge must be extracted and integrated with fixed tau/reference before G_ref^-1 Q_tau can be identified with Pi_M^H J_H^dress + dB_H.",
            "NOETHER_HAMILTONIAN_EQUALITY_MISSING",
            "R_Qtau_owner remains the dominant bridge residual",
            False,
        ),
        (
            "HCI3683_4_support_qbasic_gap",
            "source worldtube/support is not fully q-basic and fixed",
            "The support theorem needs actual q map, vertical basis, q-basic M_H_ref/worldtube coordinates, and no readout-defined source mass.",
            "SUPPORT_QBASIC_RESIDUAL_RETAINED",
            "R_support remains live",
            False,
        ),
        (
            "HCI3683_5_extra_sector_gap",
            "extra/non-Hilbert mass charge is not zeroed",
            "Projected extra current, non-EH charge, projector/domain terms and parent anomaly must be zero or bounded before the Hilbert charge identity is live.",
            "EXTRA_SECTOR_RESIDUAL_RETAINED",
            "R_extra remains live",
            False,
        ),
        (
            "HCI3683_6_boundary_calibration_gap",
            "boundary/reference and absolute calibration remain unowned",
            "Fixed reference, boundary zero flux, G_ref normalization, Poisson/Gauss coefficient and orbital readout cannot be borrowed from measured GM.",
            "BOUNDARY_CALIBRATION_RESIDUAL_RETAINED",
            "R_boundary and R_cal remain live",
            False,
        ),
        (
            "HCI3683_7_verdict",
            "current corpus proves R_Hsrc=0",
            "R_PiMop and duplicate bound EM/Poynting source accounting are removed, but Q_tau ownership, support, extra sectors, boundary/reference, calibration and radiative/nonminimal EM flux remain.",
            "RHSRC_ZERO_NOT_PROVED_TWO_SUBSLOTS_REMOVED",
            "move next to R_Qtau_owner rather than circling generic coupling",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "audit_id": audit_id,
            "claim": claim,
            "mathematical_statement": mathematical_statement,
            "status": status,
            "consequence": consequence,
            "zero_subslot": zero_subslot,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for audit_id, claim, mathematical_statement, status, consequence, zero_subslot in specs
    ]


def rhsrc_split_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "RHS3683_0_identity_definition",
            "R_Hsrc",
            "G_ref^-1 Q_tau - Pi_M^H J_H^dress - dB_H",
            "exact residual defining the Hilbert-worldtube charge bridge",
            "DEFINITION_NONCLAIM",
            "same arena source-current units as Q_tau/G_ref",
            "HCI1818_0_target;KCB3682_4_RHsrc_identity",
            "zeroing this is the local GR/Newton source bridge",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RHS3683_1_PiM_operator",
            "R_PiMop",
            "0",
            "independent projector-operator commutator on typed Hilbert mass-current complex",
            "EXACT_TYPED_OPERATOR_ZERO",
            "source-current units after projection",
            "PIA3559_1_identity_chainmap_zero",
            "do not reintroduce old Hodge/topological Pi_M stress when using Pi_M^H identity/inclusion",
            0,
        ),
        (
            "RHS3683_2_EM_bound_duplicate",
            "R_EM_bound_duplicate",
            "0",
            "duplicate source residual for stationary bound minimal EM/Poynting energy already inside J_H^dress",
            "CONDITIONAL_ONCE_ONLY_ZERO",
            "source-current units",
            "EPC3612_1_bound_fields;EPC3612_2_exchange",
            "Poynting is not ignored; it is counted in Hilbert stress once",
            0,
        ),
        (
            "RHS3683_3_Qtau_owner",
            "R_Qtau_owner",
            "G_ref^-1 Q_tau^MTS - ell_M(Pi_M^H J_H^dress) - dB_H",
            "Noether/Hamiltonian charge equality gap",
            "MISSING_PARENT_NOETHER_HAMILTONIAN_EQUALITY",
            "source-current or mass-charge units",
            "HCI1818_1_noether_charge;PHE3592_1_phase_space_start",
            "dominant next residual: extract Q_tau from parent action or bound this mismatch",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RHS3683_4_support",
            "R_support",
            "Delta_Wsource + Delta_frame + Delta_qbasic",
            "worldtube support, source frame and q-basic source-coordinate mismatch",
            "MISSING_SUPPORT_QBASIC_LOCK",
            "source-current units",
            "HDQ3561_5_live_density_verdict;WSL3596_7_current_MTS_verdict",
            "prevents source selection becoming an orbital/readout fit",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RHS3683_5_extra",
            "R_extra",
            "Pi_M^H J_extra + Q_nonEH + A_parent",
            "non-Hilbert, non-EH, parent-anomaly or hidden mass-charge leakage",
            "MISSING_EXTRA_SECTOR_SILENCE",
            "source-current units",
            "HC3558_1_projected_flux_obstruction_identity;HCI1818_5_residual_decomposition",
            "must be zero or bounded, not absorbed into measured GM",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RHS3683_6_boundary",
            "R_boundary",
            "Delta_ref + Delta_symp + B_flux + dB_H_mismatch",
            "fixed-reference, symplectic and boundary flux residual",
            "MISSING_BOUNDARY_REFERENCE_ZERO_FLUX",
            "source-current or mass-charge units",
            "HC2_differentiable_integrable_Hxi;HCI1818_5_residual_decomposition",
            "boundary terms may be harmless constants only after fixed-before-readout proof",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RHS3683_7_calibration",
            "R_cal",
            "Delta_Gref + Delta_PoissonGauss + Delta_orbital_readout",
            "absolute G_ref/Poisson/Gauss/orbital calibration mismatch",
            "MISSING_ABSOLUTE_CALIBRATION_BRIDGE",
            "source-current or mass-charge units",
            "PG1_charge_equals_projected_Hilbert_source;PG5_orbital_inverse_square_readout",
            "do not borrow Newtonian GM to prove Newtonian GM",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RHS3683_8_EM_flux",
            "R_EM_flux",
            "Phi_EM_rad + Delta_Hodge_EM + Delta_EM_norm + C_EM_readout",
            "radiative/background/nonminimal EM flux and constitutive mismatch not inside stationary Hilbert source",
            "MISSING_EM_FLUX_OR_CONSTITUTIVE_BOUND",
            "source-current units or dimensionless after normalizing by G_ref M_H",
            "EPC3612_3_radiative_flux;EPC3612_4_constitutive;EPC3612_5_action_scale",
            "the user's Poynting intuition belongs here, not as a vague extra force",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RHS3683_9_reduced_RHsrc",
            "R_Hsrc",
            "R_Qtau_owner + R_support + R_extra + R_boundary + R_cal + R_EM_flux",
            "R_Hsrc after R_PiMop=0 and R_EM_bound_duplicate=0",
            "REDUCED_NO_CANCELLATION_VECTOR",
            "source-current or mass-charge units",
            "RHS3683_3_Qtau_owner;RHS3683_4_support;RHS3683_5_extra;RHS3683_6_boundary;RHS3683_7_calibration;RHS3683_8_EM_flux",
            "this is the real source bridge debt now",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RHS3683_10_normalized_bound",
            "abs(z_RHsrc,A)",
            "(|R_Qtau_owner|+|R_support|+|R_extra|+|R_boundary|+|R_cal|+|R_EM_flux|)/N_H",
            "finite no-cancellation envelope with N_H=||Pi_M^H J_H^dress|| on the same worldtube/frame",
            "FORMULA_READY_INPUTS_MISSING",
            "dimensionless source-identity fraction",
            "RHS3683_9_reduced_RHsrc",
            "requires positive same-frame N_H and component norms before scoring",
            "MISSING_COMPONENT_VALUE",
        ),
    ]
    rows: list[dict[str, object]] = []
    for split_id, symbol, formula_or_value, meaning, status, units, source_anchor, interpretation, numeric_value in specs:
        rows.append(
            {
                **base(ts),
                "split_id": split_id,
                "symbol": symbol,
                "formula_or_value": formula_or_value,
                "meaning": meaning,
                "status": status,
                "units": units,
                "source_anchor": source_anchor,
                "interpretation": interpretation,
                "numeric_value": numeric_value,
                "valid_for_claim": False,
                "claim_allowed": False,
                "score_ready": False,
            }
        )
    return rows


def bound_schema_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "RHB3683_0_identity_row",
            "R_Hsrc",
            "G_ref^-1 Q_tau - Pi_M^H J_H^dress - dB_H",
            "source-current residual units",
            "exact source-bridge residual definition",
            "P8_Y5_PARENT_QLOC_1818_HILBERT_WORLDTUBE_CHARGE_IDENTITY_THEOREM.csv",
            "identity is defined, not zeroed",
        ),
        (
            "RHB3683_1_operator_zero",
            "R_PiMop",
            "0",
            "source-current units",
            "typed identity/inclusion Pi_M^H kills independent projector operator commutator",
            "P8_Y5_R2FR_3559_HILBERT_IDENTITY_PIM_ADOPTION_THEOREM.csv",
            "zero subslot, no local-GR claim",
        ),
        (
            "RHB3683_2_bound_EM_duplicate_zero",
            "R_EM_bound_duplicate",
            "0",
            "source-current units",
            "stationary bound minimal EM stress is already in J_H^dress",
            "P8_Y5_R2FR_3612_EM_POYNTING_HILBERT_CLOSURE.csv",
            "radiative/nonminimal/Hodge terms still live",
        ),
        (
            "RHB3683_3_Qtau_owner_bound",
            "abs(R_Qtau_owner)/N_H",
            "MISSING_RQTAU_OWNER_BOUND_VALUE",
            "dimensionless",
            "needs parent Noether charge extraction, integrable H_tau, fixed reference and same-frame source pairing",
            "MISSING_PARENT_QTAU_HILBERT_BRIDGE_SOURCE_PATH",
            "main next bound/theorem target",
        ),
        (
            "RHB3683_4_support_bound",
            "abs(R_support)/N_H",
            "MISSING_SUPPORT_QBASIC_BOUND_VALUE",
            "dimensionless",
            "needs q-basic worldtube/support coordinates and fixed source frame",
            "MISSING_QBASIC_WORLDTUBE_SOURCE_PATH",
            "support readout cannot be fitted after the fact",
        ),
        (
            "RHB3683_5_extra_bound",
            "abs(R_extra)/N_H",
            "MISSING_EXTRA_SECTOR_BOUND_VALUE",
            "dimensionless",
            "needs non-Hilbert/non-EH/projector/domain mass charge silence or finite coefficient rows",
            "MISSING_EXTRA_SECTOR_SILENCE_SOURCE_PATH",
            "hidden mass charge remains explicit",
        ),
        (
            "RHB3683_6_boundary_bound",
            "abs(R_boundary)/N_H",
            "MISSING_BOUNDARY_REFERENCE_BOUND_VALUE",
            "dimensionless",
            "needs fixed reference, zero symplectic/reference flux, and boundary convention",
            "MISSING_BOUNDARY_REFERENCE_SOURCE_PATH",
            "boundary constants are harmless only if fixed before readout",
        ),
        (
            "RHB3683_7_calibration_bound",
            "abs(R_cal)/N_H",
            "MISSING_CALIBRATION_BOUND_VALUE",
            "dimensionless",
            "needs G_ref ownership, Poisson/Gauss coefficient and orbital readout derivation",
            "MISSING_POISSON_GAUSS_CALIBRATION_SOURCE_PATH",
            "prevents orbital GM laundering",
        ),
        (
            "RHB3683_8_EM_flux_bound",
            "abs(R_EM_flux)/N_H",
            "MISSING_EM_FLUX_BOUND_VALUE",
            "dimensionless",
            "needs radiative Poynting flux/Hodge/action-scale/readout bounds",
            "MISSING_EM_FLUX_BOUND_SOURCE_PATH",
            "Poynting-style residual kept as a real coefficient",
        ),
        (
            "RHB3683_9_total_bound",
            "abs(z_RHsrc,A)",
            "(abs(R_Qtau_owner)+abs(R_support)+abs(R_extra)+abs(R_boundary)+abs(R_cal)+abs(R_EM_flux))/N_H",
            "dimensionless no-cancellation envelope",
            "source-ready finite envelope; not numeric or claim-valid until N_H and every component norm are sourced",
            "RHS3683_10_normalized_bound",
            "the residual is now executable rather than vague",
        ),
    ]
    return [
        {
            **base(ts),
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_or_formula": bound_or_formula,
            "units": units,
            "status": "THEOREM_ZERO_SUBSLOT_NONCLAIM" if bound_or_formula == "0" else "FORMULA_READY_INPUTS_MISSING",
            "interpretation": interpretation,
            "source_path_or_missing": source_path_or_missing,
            "next_input_needed": next_input_needed,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for bound_id, quantity, bound_or_formula, units, interpretation, source_path_or_missing, next_input_needed in specs
    ]


def dressed_source_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "DSA3683_0_dressed_source",
            "J_H^dress",
            "J_matter + J_EM(bound) + J_binding + J_pressure + exact_improvements",
            "DEFINITION_BRANCH_NONCLAIM",
            "dressed Hilbert source includes ordinary stress, stationary EM stress, pressure and binding once",
            "source denominator, not measured orbital GM",
        ),
        (
            "DSA3683_1_matter_EM_exchange",
            "nabla_mu(T_matter+T_EM)^{mu nu}",
            "0 under common current plus Lorentz exchange cancellation",
            "CONDITIONAL_EXCHANGE_ZERO",
            "matter-only and EM-only are not separately conserved; total Hilbert stress is the object",
            "same current and common observed Hodge required",
        ),
        (
            "DSA3683_2_static_bound_EM",
            "Delta M_EM_bound",
            "integral_Sigma T_EM(u,u) dV_obs inside M_H",
            "CONDITIONAL_INSIDE_MH",
            "static Coulomb/magnetic energy is not a separate fifth-force coefficient if same denominator is used",
            "stationary isolated support required",
        ),
        (
            "DSA3683_3_radiative_flux",
            "Phi_EM_rad",
            "integral_boundary S_Poynting dot n dA",
            "RETAINED_BOUND_INPUT",
            "non-stationary/background Poynting flux is source time-hair, not silently zero",
            "requires time window and boundary surface",
        ),
        (
            "DSA3683_4_Hodge_mismatch",
            "Delta_Hodge_EM",
            "||*_EM - *_obs[e_obs(q)]|| plus constitutive sub-bounds",
            "RETAINED_BOUND_INPUT",
            "EM follows the same geometry only if the observed Hodge/constitutive tensor is owned",
            "requires EM owner and constitutive source rows",
        ),
        (
            "DSA3683_5_EM_normalization",
            "Delta_EM_norm",
            "D_X ln lambda_A plus C_XF2/action-scale terms",
            "RETAINED_ALPHA_SOURCE_LINK",
            "EM action normalization links back to alpha/clock/WEP gates",
            "requires s_XF2/z_g bookkeeping from 3679-3680",
        ),
    ]
    return [
        {
            **base(ts),
            "accounting_id": accounting_id,
            "object": obj,
            "formula": formula,
            "status": status,
            "meaning": meaning,
            "required_guard": required_guard,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for accounting_id, obj, formula, status, meaning, required_guard in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3683_0_reduction",
            "identity Pi_M^H removes independent projector-operator debt",
            "REAL_REDUCTION",
            "the preferred branch uses Pi_M^H as identity/inclusion on the Hilbert mass-current complex",
            "remove R_PiMop from R_Hsrc",
        ),
        (
            "DEC3683_1_poynting_accounting",
            "static EM/Poynting source accounting is now once-only",
            "REAL_REDUCTION_WITH_GUARDS",
            "bound minimal EM stress belongs inside J_H^dress; radiative/Hodge/action-scale pieces remain explicit",
            "do not double-count static EM as a separate source residual",
        ),
        (
            "DEC3683_2_not_full_identity",
            "R_Hsrc=0 is not proved",
            "QTAU_SUPPORT_EXTRA_BOUNDARY_CALIBRATION_RETAINED",
            "the parent Noether/Hamiltonian charge equality and source/calibration locks remain unsigned",
            "carry reduced residual vector forward",
        ),
        (
            "DEC3683_3_next_route",
            "Q_tau-to-Hilbert source equality is now the best next throat",
            "NEXT_BEST_TARGET",
            "R_Qtau_owner is upstream of support/calibration scoring and decides whether the charge is derived or imported",
            "derive R_Qtau_owner=0 or source its bound row",
        ),
        (
            "DEC3683_4_claim_discipline",
            "no Newton/local-GR/PPN/R10/WEP claim",
            "PRIVATE_NONCLAIM",
            "two subslot reductions do not close the full source bridge",
            "continue privately",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, decision, status, reason, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3683_0_RHsrc_zero", "claim R_Hsrc=0", "BLOCKED_REDUCED_RESIDUALS_LIVE", "R_Qtau_owner, support, extra, boundary, calibration and EM flux terms remain unsigned"),
        ("CG3683_1_Newton_GR_source", "claim Newton/GR source bridge", "BLOCKED_QTAU_AND_CALIBRATION", "Noether charge equality and Poisson/Gauss/orbital calibration are not derived"),
        ("CG3683_2_static_EM_overclaim", "claim all EM/Poynting effects vanish", "BLOCKED_EM_FLUX_HODGE_NORM", "only stationary bound minimal EM duplicate accounting is zero; radiative/Hodge/normalization terms remain"),
        ("CG3683_3_zg_or_alpha_direct", "treat alpha/clock as direct s_XF2 evidence", "BLOCKED_SOURCE_CURRENT_STILL_LIVE", "source current bridge still includes R_Hsrc residuals"),
        ("CG3683_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private derivation checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "RHSRC_OPERATOR_AND_BOUND_EM_SUBSLOTS_ZERO_FULL_SOURCE_IDENTITY_BLOCKED_NONCLAIM",
            "summary": "3683 removes two real subslots from the Hilbert-worldtube source bridge: the independent Pi_M operator commutator is zero on the typed identity Pi_M^H branch, and stationary bound minimal EM/Poynting stress is inside J_H^dress once. The full R_Hsrc=0 identity remains unproved.",
            "claim_ceiling": "no R_Hsrc zero, Newton/GR source bridge, PPN/orbital calibration, WEP/R10/clock pass, direct alpha route, or public claim is made",
            "useful_result": "R_Hsrc reduces to R_Qtau_owner + R_support + R_extra + R_boundary + R_cal + R_EM_flux, with a source-ready no-cancellation envelope normalized by N_H",
            "next_missing_piece": "derive G_ref^-1 Q_tau^MTS = ell_M(Pi_M^H J_H^dress)+dB_H or source-bound R_Qtau_owner",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3683_0",
            "target_doc": "3684-Y5-R2FR-Qtau-Hilbert-Noether-bridge-or-RQtau-bound-row.md",
            "target_script": "scripts/Y5_R2FR_3684_Qtau_Hilbert_Noether_bridge_or_RQtau_bound_row.py",
            "objective": "derive G_ref^-1 Q_tau^MTS = ell_M(Pi_M^H J_H^dress)+dB_H from the parent Noether/Hamiltonian constraint with fixed tau/reference, or produce a nonclaim R_Qtau_owner bound row with N_H, boundary flux, units and source paths",
            "success_gate": "R_Qtau_owner is theorem-zero from parent Noether/Hamiltonian source equality, or a source-backed nonclaim residual/bound row exists and R_Hsrc has only support/extra/boundary/calibration/EM-flux residuals",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    split: list[dict[str, object]],
    bounds: list[dict[str, object]],
    accounting: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3683 - Hilbert-worldtube charge identity or R_Hsrc bound row",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint attacks the source bridge itself. It does not prove `R_Hsrc=0`, but it removes two genuine non-dynamical pieces: the independent `Pi_M` operator commutator on the typed identity branch, and duplicate stationary bound EM/Poynting source accounting.",
        "",
        "## Main result",
        "",
        "`R_Hsrc = G_ref^-1 Q_tau - Pi_M^H J_H^dress - dB_H`.",
        "",
        "On the preferred typed Hilbert current branch:",
        "",
        "`R_PiMop = 0`.",
        "",
        "For stationary bound minimal EM/Poynting stress using the same observed Hodge/current and Hilbert denominator:",
        "",
        "`R_EM_bound_duplicate = 0`.",
        "",
        "The reduced source-bridge residual is:",
        "",
        "`R_Hsrc = R_Qtau_owner + R_support + R_extra + R_boundary + R_cal + R_EM_flux`.",
        "",
        "The source-ready normalized envelope is:",
        "",
        "`abs(z_RHsrc,A) <= (|R_Qtau_owner|+|R_support|+|R_extra|+|R_boundary|+|R_cal|+|R_EM_flux|)/N_H`.",
        "",
        "So the next attack is precise: prove or bound `R_Qtau_owner`, not generic coupling.",
        "",
        "## Identity audit rows",
    ]
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: {row['status']} - {row['claim']} -> {row['consequence']}")
    lines.extend(["", "## R_Hsrc split rows"])
    for row in split:
        lines.append(f"- `{row['split_id']}`: {row['status']} - `{row['symbol']}` -> `{row['formula_or_value']}`")
    lines.extend(["", "## Bound schema rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: {row['status']} - `{row['quantity']}` -> `{row['bound_or_formula']}`; {row['interpretation']}")
    lines.extend(["", "## Dressed source accounting"])
    for row in accounting:
        lines.append(f"- `{row['accounting_id']}`: {row['status']} - `{row['object']}` -> `{row['formula']}`")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.",
            "",
            "## Sources",
        ]
    )
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    split: list[dict[str, object]],
    bounds: list[dict[str, object]],
    accounting: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + audit + split + bounds + accounting + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3683*", "3683-Y5-R2FR-*", "P8_Y5*3683*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    audit_by_id = {str(row["audit_id"]): row for row in audit}
    split_by_id = {str(row["split_id"]): row for row in split}
    bound_by_id = {str(row["bound_id"]): row for row in bounds}
    accounting_by_id = {str(row["accounting_id"]): row for row in accounting}

    add("VAL3683_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3683_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3683_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3683 outputs written")
    add("VAL3683_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3683_4_PiM_operator_zero", audit_by_id["HCI3683_1_identity_PiM_operator"]["status"] == "EXACT_TYPED_OPERATOR_ZERO" and split_by_id["RHS3683_1_PiM_operator"]["numeric_value"] == 0, "Pi_M^H operator subslot is zero")
    add("VAL3683_5_EM_bound_duplicate_zero", audit_by_id["HCI3683_2_static_EM_dressing"]["status"] == "EXACT_CONDITIONAL_ONCE_ONLY_DRESSING" and split_by_id["RHS3683_2_EM_bound_duplicate"]["numeric_value"] == 0, "stationary bound EM duplicate source residual is zero")
    add("VAL3683_6_not_full_RHsrc_zero", audit_by_id["HCI3683_7_verdict"]["status"] == "RHSRC_ZERO_NOT_PROVED_TWO_SUBSLOTS_REMOVED", "full R_Hsrc zero is not claimed")
    add("VAL3683_7_reduced_RHsrc_formula", split_by_id["RHS3683_9_reduced_RHsrc"]["formula_or_value"] == "R_Qtau_owner + R_support + R_extra + R_boundary + R_cal + R_EM_flux", "R_Hsrc reduced to live residuals")
    add("VAL3683_8_normalized_bound_formula", "N_H" in str(split_by_id["RHS3683_10_normalized_bound"]["formula_or_value"]) and "R_Qtau_owner" in str(bound_by_id["RHB3683_9_total_bound"]["bound_or_formula"]), "normalized source envelope is recorded")
    add("VAL3683_9_poynting_retained", accounting_by_id["DSA3683_3_radiative_flux"]["status"] == "RETAINED_BOUND_INPUT" and "Poynting" in accounting_by_id["DSA3683_3_radiative_flux"]["meaning"], "radiative/background Poynting flux remains a bound input")
    add("VAL3683_10_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates), "claim gates remain blocked")
    add("VAL3683_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3683_12_doc_written", "R_PiMop = 0" in doc_text and "R_EM_bound_duplicate = 0" in doc_text and "R_Hsrc = R_Qtau_owner + R_support + R_extra + R_boundary + R_cal + R_EM_flux" in doc_text, "doc records two zero subslots and reduced R_Hsrc")
    add("VAL3683_13_next_target", next_target[0]["target_doc"].startswith("3684-") and "R_Qtau_owner" in next_target[0]["objective"], "3684 targets Q_tau/Hilbert source bridge")
    add("VAL3683_14_no_formalization_leak", not leaks, "no 3683 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    audit = identity_audit_rows(ts)
    split = rhsrc_split_rows(ts)
    bounds = bound_schema_rows(ts)
    accounting = dressed_source_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3683_SOURCE_REGISTER.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3683_HILBERT_CHARGE_IDENTITY_AUDIT.csv",
        "split": RESIDUALS / "P8_Y5_R2FR_3683_RHSRC_COMPONENT_SPLIT_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3683_RHSRC_BOUND_SCHEMA_ROWS.csv",
        "accounting": RESIDUALS / "P8_Y5_R2FR_3683_DRESSED_SOURCE_ACCOUNTING_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3683_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3683_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3683_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3683_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3683_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["split"], split)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["accounting"], accounting)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, audit, split, bounds, accounting, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, audit, split, bounds, accounting, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3683 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3683 checkpoint: PiM operator and bound EM duplicate subslots zero; R_Qtau_owner next")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
