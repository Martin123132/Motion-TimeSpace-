from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2910"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2910-Y5-R2FR-Qvis-object-language-no-source-slot-or-finite-JH-DqZ-Y5Y6-vector-under-AX1090.md"

SRC_2909_DOC = ROOT / "2909-Y5-R2FR-source-current-descent-and-Y5Y6-coupling-zero-or-residual-vector-under-AX1090.md"
SRC_2909_NEXT = RESIDUALS / "P8_Y5_R2FR_2909_NEXT_TARGET.csv"
SRC_2909_PROOF = RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_CURRENT_DESCENT_PROOF_ATTEMPT.csv"
SRC_2909_RESIDUAL = RESIDUALS / "P8_Y5_R2FR_2909_SOURCE_CURRENT_Y5Y6_RESIDUAL_VECTOR.csv"
SRC_2644_DOC = ROOT / "2644-Y5-R2FR-Qvis-object-language-no-source-slot-or-finite-JH-DqZ-vector.md"
SRC_2644_GATE = RESIDUALS / "P8_Y5_QVIS_OBJECT_LANGUAGE_2644_OBJECT_LANGUAGE_GATE.csv"
SRC_2644_VECTOR = RESIDUALS / "P8_Y5_QVIS_OBJECT_LANGUAGE_2644_FINITE_JH_DQZ_VECTOR_CONTRACT.csv"
SRC_2644_NEXT = RESIDUALS / "P8_Y5_QVIS_OBJECT_LANGUAGE_2644_NEXT_TARGET.csv"
SRC_2650_PREF = RESIDUALS / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv"
SRC_2508_NOSLOT = RESIDUALS / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv"
SRC_2677_OBJECT = RESIDUALS / "P8_Y5_R2FR_2677_NO_SPECIES_ACTION_WEIGHT_OBJECT_LANGUAGE_AUDIT.csv"
SRC_2611_PREMISE = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv"
SRC_2611_CHAIN = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv"
SRC_2611_WORLD = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv"
SRC_2612_DIRECT = RESIDUALS / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_DIRECT_VERTEX_AND_NO_MARKER_AUDIT.csv"
SRC_2602_DESCENT = RESIDUALS / "P8_Y5_CURRENT_DESCENT_REBASE_2602_DESCENT_GATE_STATUS.csv"
SRC_2602_BG = RESIDUALS / "P8_Y5_CURRENT_DESCENT_REBASE_2602_BG_RESPONSE_BRIDGE.csv"
SRC_1415_OWNER = RESIDUALS / "P8_Y5_R10_1415_SOURCE_CURRENT_OWNER_ATTEMPT.csv"
SRC_1416_BAN = RESIDUALS / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv"
SRC_1416_COUNTER = RESIDUALS / "P8_Y5_R10_1416_SOURCE_SLOT_COUNTERMODEL_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2910_SOURCE_REGISTER.csv",
    "qvis_gate": RESIDUALS / "P8_Y5_R2FR_2910_QVIS_OBJECT_LANGUAGE_GATE.csv",
    "no_source": RESIDUALS / "P8_Y5_R2FR_2910_NO_SOURCE_SLOT_AUDIT.csv",
    "finite_vector": RESIDUALS / "P8_Y5_R2FR_2910_FINITE_JH_DQZ_Y5Y6_VECTOR.csv",
    "arenas": RESIDUALS / "P8_Y5_R2FR_2910_ARENA_VECTOR_MAP.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2910_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2910_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2910_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2910_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2910_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2910_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "qvis_gate_copy": RAB_QUEUE / "JR2910_QVIS_OBJECT_LANGUAGE_GATE_NONCLAIM.csv",
    "finite_vector_copy": LOCAL_BOUNDS / "Qvis_JH_DqZ_Y5Y6_vector_2910_NONCLAIM.csv",
    "next_copy": PARENT_ACTION / "Parent_field_chart_qmap_kernel_next_2910_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2910_00_2909_doc", SRC_2909_DOC, "NEXT2909_0_2910;Q_vis object-language/no-source-slot", "handoff from source-current descent to Q_vis grammar"),
        ("SRC2910_01_2909_next", SRC_2909_NEXT, "NEXT2909_0_2910;Q_vis grammar makes DqZ/JH leaks", "machine-readable 2910 target"),
        ("SRC2910_02_2909_proof", SRC_2909_PROOF, "PROOF2909_0_JZ_chain_rule_identity;PROOF2909_7_verdict", "conditional J_Z chain-rule theorem and blocked application"),
        ("SRC2910_03_2909_residual", SRC_2909_RESIDUAL, "RES2909_2_DqZ;RES2909_TOTAL", "source-current/Y5Y6 residual vector handed into 2910"),
        ("SRC2910_04_2644_doc", SRC_2644_DOC, "QOL2644_8_verdict;FJV2644_0_master_vector", "earlier Q_vis object-language gate and finite-vector contract"),
        ("SRC2910_05_2644_gate", SRC_2644_GATE, "QOL2644_0_target_signature;QOL2644_8_verdict", "Q_vis object-language source-side zero gate"),
        ("SRC2910_06_2644_vector", SRC_2644_VECTOR, "FJV2644_0_master_vector;FJV2644_8_policy", "finite JH/DqZ source/readout vector schema"),
        ("SRC2910_07_2644_next", SRC_2644_NEXT, "NEXT2644_0_selected;no-source-prefactor", "earlier no-source-prefactor bottleneck decision"),
        ("SRC2910_08_2650_prefactor", SRC_2650_PREF, "NSP2650_1_exact_if_grammar_signed;NSP2650_6_verdict", "typed no-source-prefactor theorem attempt"),
        ("SRC2910_09_2508_noslot", SRC_2508_NOSLOT, "NSP2508_6_counterexample;NSP2508_7_verdict", "surviving no-source-only slot counterexample"),
        ("SRC2910_10_2677_object", SRC_2677_OBJECT, "OL2677_1_eom_rejection;OL2677_5_verdict", "species action-weight object-language audit"),
        ("SRC2910_11_2611_premise", SRC_2611_PREMISE, "PRE2611_0_q_map;PRE2611_8_verdict", "matter descent premise audit"),
        ("SRC2910_12_2611_chain", SRC_2611_CHAIN, "CR2611_0_variation_identity;CR2611_6_direct_vertex", "matter descent chain-rule decomposition"),
        ("SRC2910_13_2611_world", SRC_2611_WORLD, "MWD2611_1_conditional_theorem;MWD2611_4_current_verdict", "matter/worldtube descent attempt"),
        ("SRC2910_14_2612_direct", SRC_2612_DIRECT, "DV2612_1_wA;DV2612_5_verdict", "direct matter/source vertex and marker audit"),
        ("SRC2910_15_2602_descent", SRC_2602_DESCENT, "DGR2602_2_coframe_kernel;DGR2602_3_no_shadow_frame", "observed coframe descent and shadow-frame gate"),
        ("SRC2910_16_2602_bg", SRC_2602_BG, "BGB2602_1_b_g;BGB2602_3_gamma_response", "finite observed-frame leak response rows"),
        ("SRC2910_17_1415_owner", SRC_1415_OWNER, "SCO1415_1_object_language;SCO1415_6_verdict", "source-current owner attempt"),
        ("SRC2910_18_1416_ban", SRC_1416_BAN, "BAN1416_1_locality_covariance;BAN1416_6_verdict", "source-slot/current-rescaling ban attempt"),
        ("SRC2910_19_1416_counter", SRC_1416_COUNTER, "CM1416_0_wA_action;CM1416_4_readout_current", "live source-slot countermodels"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def qvis_gate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "QVIS2910_0_visible_object_set",
            "visible quotient object Q_vis",
            "Q_vis=(e_obs,g_obs,mu_m,D_m,J_H/source/readout data,theta_rep,A_owned) is the only ordinary-matter/readout argument set.",
            "TARGET_EXACT_NOT_PARENT_OWNED",
            "parent field chart and q(Phi) image are not explicitly derived",
            "ordinary matter cannot see residual directions except through q",
            "Dq_Z_norm and observed descent leaks remain finite rows",
            SRC_2644_GATE,
        ),
        (
            "QVIS2910_1_parent_q_map",
            "parent quotient map q",
            "There is a declared smooth q: Phi_parent -> Q_vis before readout, fitting, boundary projection, or source normalization.",
            "MISSING_PARENT_FIELD_CHART_AND_Q_MAP",
            "the corpus has contracts and candidate skeletons, not a typed parent map with derivative matrix",
            "all vertical/null directions become checkable rather than asserted",
            "Dq_Z_norm cannot be theorem-zero",
            SRC_2611_PREMISE,
        ),
        (
            "QVIS2910_2_vertical_kernel_basis",
            "residual generator verticality",
            "For every retained local residual generator v_Z, Dq[v_Z]=0 in the declared q-map basis.",
            "MISSING_KERNEL_BASIS",
            "no parent-coordinate basis lists v_Z and no normed Dq matrix exists",
            "DObs(v_Z)=0 follows by chain rule for Q_vis functors",
            "E_DqZ_A must remain a finite arena vector",
            SRC_2644_VECTOR,
        ),
        (
            "QVIS2910_3_no_direct_Z_slot",
            "no direct residual slot in matter",
            "S_matter=sum_A S_A[Psi_A,Q_vis,theta_A,A_owned] and has no independent Z, R_AB, Gamma_mem, chi, support-mask, or source-worldtube argument.",
            "DIRECT_SLOT_EXCLUSION_UNSIGNED",
            "absence from legacy formulas is weaker than a parent constructor ban",
            "A_direct_matter=0 and direct J_Z vertices vanish",
            "direct-vertex row remains live",
            SRC_2612_DIRECT,
        ),
        (
            "QVIS2910_4_no_source_only_weight",
            "no pre-action source-only/species weight",
            "The parent grammar forbids relative w_A(Z)S_A, kappa_A(Z)T_A, hbar_A, species Jacobians, and active-source-only current rescalings before variation.",
            "COUNTERMODEL_SURVIVES",
            "local/covariant/additive weights preserve matter EOM while changing Hilbert source",
            "Delta_w_abs and current-rescaling seams become theorem-zero",
            "Delta_w_abs remains the core finite coupling row",
            SRC_1416_COUNTER,
        ),
        (
            "QVIS2910_5_theta_marker_silence",
            "theta/material/marker silence",
            "Masses, charges, alpha_EM, clocks, material labels, and readout markers are representation/superselection data with Lie_vZ(theta)=0.",
            "NO_MARKER_THEOREM_UNSIGNED",
            "marker and radiative/readout re-entry maps are not parent-exhausted",
            "epsilon_theta_marker=0 and clock/EM/WEP marker tails vanish",
            "theta/marker leak remains arena-specific",
            SRC_2611_CHAIN,
        ),
        (
            "QVIS2910_6_source_worldtube_descent",
            "Hilbert source and worldtube ownership",
            "J_M is the parent Hilbert/coframe current and W_source=closure(supp J_H[tau]) before source/readout fitting.",
            "SOURCE_WORLDTUBE_OWNER_UNSIGNED",
            "source current owner, Pi_M equality, tau frame and source support are not signed together",
            "J_M exterior source is zero up to declared boundary tails",
            "epsilon_JM_descent_abs and boundary/worldtube flux remain live",
            SRC_1415_OWNER,
        ),
        (
            "QVIS2910_7_boundary_projector_silence",
            "boundary/projector silence",
            "Matter/worldtube boundary terms and local projectors are zero, exact/proper, or explicitly bounded before local arena scoring.",
            "BOUNDARY_PROJECTOR_OPEN",
            "boundary charge and projector variation are contracts rather than computed parent terms",
            "bulk descent transfers to Newton/PPN/R10/clock/orbital arenas",
            "boundary and projector stress stay in the total vector",
            SRC_2611_WORLD,
        ),
        (
            "QVIS2910_8_Ward_owner",
            "Ward/current owner is support not proof",
            "Ward conservation may preserve a signed Hilbert current, but it cannot by itself ban source weights or hidden readout currents.",
            "GUARDRAIL_PASS_NOT_CLAIM",
            "conservation does not identify the unique source normalization or object language",
            "prevents a false coupling-zero proof",
            "no direct zero; it only protects the decision logic",
            SRC_1415_OWNER,
        ),
        (
            "QVIS2910_9_verdict",
            "Q_vis/no-source-slot theorem for current MTS",
            "QVIS2910_0 through QVIS2910_7 all close in one parent branch, so JH/DqZ/source-weight/Y5Y6 couplings are theorem-zero.",
            "NOT_PARENT_SIGNED_FINITE_VECTOR_REQUIRED",
            "q map, kernel basis, no-source-only slot, no-marker, source-worldtube and boundary/projector clauses do not close together",
            "local source side could move toward GR/Newton reduction",
            "finite JH/DqZ/Y5Y6 vector remains mandatory",
            SRC_2909_NEXT,
        ),
    ]
    rows: list[dict[str, Any]] = []
    for gate_id, clause, statement, status, gap, signed_effect, unsigned_effect, source_path in specs:
        rows.append(
            add_common(
                {
                    "gate_id": gate_id,
                    "clause": clause,
                    "theorem_or_contract": statement,
                    "current_status": status,
                    "blocking_gap": gap,
                    "consequence_if_signed": signed_effect,
                    "residual_if_unsigned": unsigned_effect,
                    "source_path": str(source_path),
                    "signed_now": False,
                }
            )
        )
    return rows


def no_source_slot_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NSS2910_0_exact_conditional",
            "typed no-source-slot theorem",
            "If Hom_parent(SpeciesLabel or Marker, Coeff_active_source)=empty, one action-density line owns all ordinary sectors, and readout cannot re-enter, then relative source-only weights are ill-typed.",
            "EXACT_CONDITIONAL_THEOREM",
            "would kill Delta_w_abs, beta_source/test and current-rescaling source seams",
            "not active until parent constructor list and common measure owner are signed",
        ),
        (
            "NSS2910_1_EOM_rejection",
            "matter EOM equivalence is not source equivalence",
            "delta(w_A S_A)/delta Psi_A can share classical matter equations, while delta(w_A S_A)/delta g_obs = w_A T_A changes the gravitational source.",
            "REJECTION_LEMMA_CONFIRMED",
            "prevents a fake proof of coupling zero",
            "w_A remains dangerous specifically because the coupling/source equation changes",
        ),
        (
            "NSS2910_2_local_covariant_countermodel",
            "local/covariant/additive weights survive symmetry",
            "w_A(Z) can be a scalar and preserve diffeomorphism covariance/additivity, so basic symmetry alone does not ban it.",
            "LIVE_COUNTERMODEL",
            "forces parent grammar proof rather than symmetry rhetoric",
            "Delta_w_abs finite row required",
        ),
        (
            "NSS2910_3_common_mode_guard",
            "common-mode weights are not a WEP/source proof",
            "A universal common weight may be calibration-like only after its derivative is source/test/readout silent and cannot absorb relative components into G_N or GM.",
            "GUARDRAIL_ACTIVE",
            "blocks G_N/GM laundering",
            "all relative rows stay absolute-summed",
        ),
        (
            "NSS2910_4_connected_category_route",
            "connected ordinary-matter category route",
            "Naturality can collapse weights only if the parent owns nonzero morphisms linking ordinary matter sectors and source/readout forgets labels.",
            "CONDITIONAL_ROUTE_CLEAN_NOT_SIGNED",
            "could remove species weights without a closure axiom",
            "connected graph owner and source-label forgetting are missing",
        ),
        (
            "NSS2910_5_quantum_measure_route",
            "single path/statistical measure route",
            "A single parent hbar/action measure would forbid independent exp(i w_A S_A/hbar) sector weights.",
            "CONDITIONAL_ROUTE_CLEAN_NOT_SIGNED",
            "could remove action-scale loopholes",
            "parent measure/action-scale owner is unsigned",
        ),
        (
            "NSS2910_6_readout_radiative_return",
            "post-variation source/readout return",
            "Even after a grammar ban, readout, EFT thresholds, clocks, boundaries, or conserved added currents must not regenerate source-only coefficients.",
            "READOUT_RADIATIVE_CLOSURE_UNSIGNED",
            "would protect WEP/PPN/R10/clock projections",
            "marker/readout tail remains finite",
        ),
        (
            "NSS2910_7_verdict",
            "no-source-slot proof for current MTS",
            "The parent object language forbids source-only weights, direct source slots, markers and current rescalings from primitives alone.",
            "NOT_DERIVED_CURRENT_MTS",
            "would zero the coupling bottleneck row set",
            "stage finite rows and move upstream to parent field chart/q-map/kernel basis",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for audit_id, clause, statement, status, effect, blocker in specs:
        rows.append(
            add_common(
                {
                    "audit_id": audit_id,
                    "clause": clause,
                    "statement": statement,
                    "current_status": status,
                    "what_it_would_kill": effect,
                    "blocker_or_guard": blocker,
                    "signed_now": False,
                }
            )
        )
    return rows


def finite_vector_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FV2910_0_DqZ",
            "Dq_Z_norm",
            "quotient derivative leakage of residual directions into visible variables",
            "operator_norm",
            "Dq_Z_norm := ||Dq[v_Z]||_q / ||v_Z||_Z",
            "MISSING_PARENT_FIELD_CHART_Q_MAP_DQ_MATRIX_AND_KERNEL_BASIS",
            "Newton;PPN;WEP;R10;clock;orbital",
        ),
        (
            "FV2910_1_eps_JH",
            "eps_JH_Z_abs",
            "ordinary Hilbert source leak under residual variation",
            "source-current-normalized",
            "eps_JH_Z_abs <= C_matter*Dq_Z_norm + eps_theta_marker + A_direct_matter + Delta_w_abs + epsilon_boundary_worldtube_flux",
            "MISSING_QVIS_GRAMMAR_OR_FINITE_COMPONENT_COEFFICIENTS",
            "Newton;PPN;WEP;R10",
        ),
        (
            "FV2910_2_E_DqZ_A",
            "E_DqZ_A",
            "observed arena descent leak from DqZ into readout variables",
            "arena_projection_units",
            "E_DqZ_A <= C_A_obs*Dq_Z_norm*N_Z + E_theta_A + E_readout_A + E_boundary_A",
            "MISSING_OBSERVED_FUNCTOR_AND_ARENA_PROJECTION_COEFFICIENTS",
            "Newton;PPN;WEP;clock;EM;orbital",
        ),
        (
            "FV2910_3_Delta_w",
            "Delta_w_abs",
            "relative pre-action source/species/action weight seam",
            "dimensionless",
            "Delta_w_abs := max_AB |w_A-w_B| after common-mode projection guard",
            "MISSING_NO_SOURCE_ONLY_SLOT_THEOREM_OR_NUMERIC_SOURCE_WEIGHT_ROWS",
            "WEP;PPN;R10;source_mass",
        ),
        (
            "FV2910_4_theta_marker",
            "epsilon_theta_marker",
            "theta/material/clock/EM/readout marker leak",
            "source-normalized_or_arena_specific",
            "epsilon_theta_marker <= ||J_theta Lie_vZ(theta)||/||J_ref|| plus marker/readout tail",
            "MISSING_NO_MARKER_THEOREM_AND_READOUT_RADIATIVE_CLOSURE",
            "WEP;clock;EM;R10",
        ),
        (
            "FV2910_5_direct_vertex",
            "A_direct_matter",
            "direct matter/source/worldtube vertex depending on residual variables outside q",
            "action_variation_units",
            "A_direct_matter := ||delta_Z V_matter[source,Z]||",
            "MISSING_DIRECT_SLOT_EXCLUSION_FROM_PARENT_GRAMMAR",
            "source_mass;WEP;PPN",
        ),
        (
            "FV2910_6_boundary_flux",
            "epsilon_boundary_worldtube_flux",
            "matter/worldtube/boundary flux under residual variation",
            "flux_or_action_boundary_units",
            "epsilon_boundary_worldtube_flux := ||Pi_local delta_Z B_matter/worldtube||/||J_ref||",
            "MISSING_BOUNDARY_NOFLUX_OR_ABSOLUTE_TAIL_BOUND",
            "Newton;PPN;R10;orbital",
        ),
        (
            "FV2910_7_JM_descent",
            "epsilon_JM_descent_abs",
            "failure of q_loc source current to be parent Hilbert/worldtube current",
            "source-current-normalized",
            "epsilon_JM_descent_abs := ||J_M-J_H[worldtube]||/||J_ref|| plus Pi_M/source-support mismatch",
            "MISSING_SOURCE_CURRENT_OWNER_WORLDTUBE_PIM_EQUALITY",
            "Newton;PPN;orbital;R10",
        ),
        (
            "FV2910_8_Y5_GM",
            "epsilon_Y5_GM_transfer",
            "Y5 source-normalization transfer through fitted GM/source-current mismatch",
            "dimensionless_after_true_source_norm",
            "epsilon_Y5_GM_transfer <= Pi_GM(epsilon_JM_descent_abs + Delta_w_abs + boundary + readout)",
            "MISSING_COMMON_MODE_GM_THEOREM_AND_ORBITAL_OUTPUT_GUARD",
            "Newton;orbital;galaxy_reference_only",
        ),
        (
            "FV2910_9_Y5_mu",
            "epsilon_Y5_mu_extra_vector",
            "Y5 extra source offsets from non-EH/boundary/radial/time/species/calibration channels",
            "dimensionless_after_true_source_norm",
            "epsilon_Y5_mu_extra_vector := absolute component vector, no cancellation",
            "MISSING_Y5_SOURCE_NORMALIZATION_CHANNEL_OWNERS",
            "Newton;PPN;WEP;R10",
        ),
        (
            "FV2910_10_Y6_stress",
            "epsilon_extra_odd_source_Y6",
            "Y6 extra-stress/source coupling that can survive source-current descent",
            "dimensionless_after_true_source_norm",
            "epsilon_extra_odd_source_Y6 <= Pi_stress(eps_JH_Z_abs + E_DqZ_A + boundary + projector)",
            "MISSING_Y6_STRESS_PARENT_SIGNATURE",
            "PPN;clock;orbital;local_GR",
        ),
        (
            "FV2910_11_projector",
            "epsilon_Y6_projector_stress",
            "projector/readout stress and Pi_M variation leakage",
            "dimensionless_source_stress_leakage",
            "epsilon_Y6_projector_stress := ||delta_Z Pi_M|| + ||delta_Z P_loc|| projected into source stress",
            "MISSING_PROJECTOR_VARIATION_ZERO_OR_BOUND",
            "PPN;orbital;local_GR",
        ),
        (
            "FV2910_12_observable",
            "epsilon_Y5Y6_observable_projection",
            "missing arena projection and units for q_loc/Z/Y5/Y6 residuals",
            "mixed_projection_units",
            "epsilon_Y5Y6_observable_projection := absolute projection error into Newton/PPN/R10/clock/orbital maps",
            "MISSING_OBSERVABLE_PROJECTION_AND_UNITS",
            "Newton;PPN;R10;clock;orbital",
        ),
        (
            "FV2910_TOTAL",
            "epsilon_Qvis_JH_DqZ_Y5Y6_total",
            "absolute no-cancellation envelope over Q_vis, source-current, Y5, Y6, boundary, projector and observable leaks",
            "dimensionless_gate_after_declared_normalization",
            "sum_abs(FV2910_0..FV2910_12) with common-mode and G_N/GM absorption guards",
            "COMPONENTS_MISSING_NONCLAIM",
            "all_local_arenas",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for vector_id, symbol, definition, units, formula, missing, arenas in specs:
        rows.append(
            add_common(
                {
                    "vector_id": vector_id,
                    "symbol": symbol,
                    "definition": definition,
                    "units": units,
                    "formula_or_bound": formula,
                    "current_value": missing,
                    "required_parent_input": missing,
                    "arena_targets": arenas,
                    "source_paths": ";".join(
                        str(path)
                        for path in [
                            SRC_2909_RESIDUAL,
                            SRC_2644_VECTOR,
                            SRC_2611_CHAIN,
                            SRC_1416_COUNTER,
                        ]
                    ),
                    "theorem_zero_condition": "all relevant QVIS2910 clauses close in one parent branch",
                    "current_status": "STAGED_NONCLAIM_ROW",
                }
            )
        )
    return rows


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ARENA2910_0_Newton",
            "Newton/local GM/orbital",
            "Delta_GM <= Pi_GM(eps_JH_Z_abs + E_DqZ_GM + Delta_w_abs + epsilon_JM_descent_abs + boundary)",
            "COMMON_MODE_GM_AND_SOURCE_CURRENT_OWNER_UNSIGNED",
            "do not absorb finite vector into fitted GM; orbital GM remains output only",
        ),
        (
            "ARENA2910_1_PPN",
            "PPN gamma/beta/preferred-frame",
            "Delta_PPN <= Pi_PPN(eps_JH_Z_abs + E_DqZ_PPN + epsilon_extra_odd_source_Y6 + projector)",
            "PPN_PROJECTION_AND_Y6_STRESS_UNSIGNED",
            "PPN branch remains blocked until finite vector components are zero/bounded",
        ),
        (
            "ARENA2910_2_WEP",
            "WEP/composition",
            "eta_AB <= Pi_WEP(Delta_w_abs + epsilon_theta_marker + E_DqZ_WEP + source-label/readout marker tail)",
            "NO_SOURCE_SLOT_AND_NO_MARKER_UNSIGNED",
            "composition tests are sensitive to the coupling throat rather than a side issue",
        ),
        (
            "ARENA2910_3_R10",
            "R10/contact/source-test branch",
            "alpha_pred(lambda) cannot be claimed until source coefficients and local projection are real, sourced and unit-locked",
            "BOUND_INPUTS_AND_PARENT_COEFFICIENTS_MISSING",
            "R10 remains a plumbing/smoke arena, not proof of local GR",
        ),
        (
            "ARENA2910_4_clock_EM",
            "clock/time/EM",
            "Delta_clock/alpha_EM <= Pi_theta(epsilon_theta_marker + E_DqZ_clock/EM + readout/radiative return)",
            "THETA_MARKER_AND_READOUT_CLOSURE_UNSIGNED",
            "charge/clock route must be cited and kept separate from local-GR claim",
        ),
        (
            "ARENA2910_5_orbital",
            "orbital systems",
            "Delta_orbit <= Pi_orbit(epsilon_JM_descent_abs + boundary + E_DqZ_orbit + source support)",
            "SOURCE_WORLDTUBE_AND_BOUNDARY_OWNER_UNSIGNED",
            "perihelion/binary/orbital work cannot be scored until source support is owned",
        ),
        (
            "ARENA2910_6_local_GR",
            "local GR/Newton reduction",
            "local GR follows only if Q_vis/no-source-slot signs or the finite vector is zero/bounded below arena tolerance with no cancellation",
            "BLOCKED_NONCLAIM",
            "2910 does not prove local GR; it names the residual vector that must be killed",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for arena_id, arena, projection, status, guardrail in specs:
        rows.append(
            add_common(
                {
                    "arena_id": arena_id,
                    "arena": arena,
                    "projection_or_gate": projection,
                    "current_status": status,
                    "guardrail": guardrail,
                    "missing_inputs": "parent q-map; kernel basis; no-source-slot theorem; source-current owner; boundary/projector map; units",
                }
            )
        )
    return rows


def runner_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_sources_ready = all(row["path_exists"] and row["anchors_found"] for row in source_rows)
    specs = [
        ("RUN2910_0_sources", "SOURCE_AUDIT_COMPLETE" if all_sources_ready else "SOURCE_AUDIT_HAS_BLOCKERS", "all cited source paths and anchors", all_sources_ready, "used as evidence only, not claim"),
        ("RUN2910_1_qvis_theorem", "QVIS_THEOREM_ATTEMPTED_NOT_SIGNED", "Q_vis constructor list, q map, Dq kernel, matter/readout functor", False, "parent field chart/q map/kernel basis missing"),
        ("RUN2910_2_no_source_slot", "NO_SOURCE_SLOT_PROOF_ATTEMPTED_COUNTERMODEL_LIVE", "typed no-Hom, common action measure, source-label forgetting, readout closure", False, "w_A/kappa_A/current-rescaling countermodels survive basic symmetry"),
        ("RUN2910_3_finite_vector", "FINITE_VECTOR_STAGED_NONCLAIM", "DqZ/JH/Delta_w/theta/direct/boundary/Y5/Y6/projector/observable rows", False, "rows have schemas and units but no parent coefficients"),
        ("RUN2910_4_local_claims", "LOCAL_GR_NEWTON_REMAINS_BLOCKED", "all local claim gates", False, "object-language/source-current/coupling residual vector is unfilled"),
        ("RUN2910_5_next", "NEXT_PARENT_QMAP_KERNEL_SELECTED", "2911 target", False, "upstream parent field chart/q-map/kernel basis is the shortest real lock"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required,
                "components_evaluable": evaluable,
                "reason": reason,
            }
        )
        for runner_id, status, required, evaluable, reason in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2910_0_conditional_chain_rule", "conditional J_Z chain-rule theorem exists", "PASS_CONDITIONAL_ONLY", "2909/2643 chain-rule theorem is exact if Q_vis clauses close", True),
        ("CG2910_1_Qvis_current", "ordinary matter/readouts are Q_vis-only for current MTS", "BLOCKED_NONCLAIM", "parent field chart, q map, kernel basis and constructor list are unsigned", False),
        ("CG2910_2_no_source_slot", "no source-only/species/current-rescaling slot exists", "BLOCKED_NONCLAIM", "w_A/kappa_A/current-rescaling countermodels remain legal without parent grammar", False),
        ("CG2910_3_DqZ_JH_zero", "Dq_Z_norm=eps_JH_Z_abs=E_DqZ_A=0", "BLOCKED_NONCLAIM", "Q_vis theorem does not fire in current corpus", False),
        ("CG2910_4_JM_source_owner", "J_M is parent Hilbert/worldtube current", "BLOCKED_NONCLAIM", "source current owner, Pi_M equality and worldtube support remain unsigned", False),
        ("CG2910_5_Y5Y6_zero", "Y5/Y6 coupling residuals are theorem-zero", "BLOCKED_NONCLAIM", "Y5 source normalization and Y6 stress still depend on the source-current/object-language lock", False),
        ("CG2910_6_finite_vector_score", "finite vector is score-ready against arenas", "BLOCKED_NONCLAIM", "component values, coefficients, units and arena projections are missing", False),
        ("CG2910_7_local_GR_Newton", "local GR/Newton follows after 2910", "BLOCKED_NONCLAIM", "2910 stages the coupling vector; it does not close it", False),
    ]
    rows: list[dict[str, Any]] = []
    for gate_id, claim, status, reason, gate_pass in specs:
        rows.append(
            add_common(
                {
                    "gate_id": gate_id,
                    "claim": claim,
                    "gate_status": status,
                    "reason": reason,
                    "gate_pass": gate_pass,
                }
            )
        )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2910_0_result",
            "QVIS_OBJECT_LANGUAGE_NOT_PARENT_SIGNED",
            "The exact object-language theorem is now restated for the 2908-2909 parent-action route, but current evidence does not sign q, Dq kernel, no-source-slot, no-marker, worldtube and boundary clauses together.",
            "do not promote JH/DqZ/Y5/Y6 zero",
        ),
        (
            "DEC2910_1_coupling_read",
            "COUPLING_BOTTLENECK_CONFIRMED",
            "The source/coupling issue is not an embarrassment; it is the live mathematical throat: source-only weights can preserve familiar motion equations while changing gravitational source terms.",
            "attack parent grammar/q-map, not empirical patching",
        ),
        (
            "DEC2910_2_guard",
            "NO_GM_OR_GN_ABSORPTION",
            "Finite source rows cannot be hidden in fitted G_N, orbital GM, common-mode calibration, or cancellation-only vector sums.",
            "keep all finite vector components absolute and nonclaim",
        ),
        (
            "DEC2910_3_next",
            "NEXT_2911_PARENT_FIELD_CHART_QMAP_KERNEL_BASIS",
            "Q_vis/no-source-slot cannot sign until a parent field chart, q-map derivative and residual kernel basis exist.",
            "construct q and Dq first; if it fails, compute/bound Dq_Z_norm",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2910_0_2911",
                "selection_status": "selected_primary",
                "target_file": "2911-Y5-R2FR-parent-field-chart-q-map-kernel-basis-or-finite-DqZ-norm-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_field_chart_q_map_kernel_basis_or_finite_DqZ_norm_under_AX1090_2911.py",
                "task": "construct the parent field chart, q:Phi_parent->Q_vis, Dq matrix and residual kernel basis that would make Dq[v_Z]=0 an actual theorem; if it fails, stage finite Dq_Z_norm rows with norms and arena projections",
                "success_condition": "explicit variables, q-map, derivative matrix, vertical basis, norm convention and source/readout functor domain list are all parent-signed in one branch",
                "fallback_condition": "Dq_Z_norm and E_DqZ_A become finite nonclaim rows with units, coefficients, source paths and arena maps",
                "guardrails": "no closure axiom; no plateau axiom; no empirical scoring; no GM/G_N absorption; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copy_specs = [
        ("qvis_gate_copy", OUTPUTS["qvis_gate"], BRANCH_OUTPUTS["qvis_gate_copy"]),
        ("finite_vector_copy", OUTPUTS["finite_vector"], BRANCH_OUTPUTS["finite_vector_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination in copy_specs:
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "source_exists": source.exists(),
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination),
                }
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    qvis_rows: list[dict[str, Any]],
    no_source_rows_: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_outputs_with_validation = [*csv_outputs, OUTPUTS["validation"]]
    required_symbols = {
        "Dq_Z_norm",
        "eps_JH_Z_abs",
        "E_DqZ_A",
        "Delta_w_abs",
        "epsilon_theta_marker",
        "A_direct_matter",
        "epsilon_boundary_worldtube_flux",
        "epsilon_JM_descent_abs",
        "epsilon_Y5_GM_transfer",
        "epsilon_Y5_mu_extra_vector",
        "epsilon_extra_odd_source_Y6",
        "epsilon_Y6_projector_stress",
        "epsilon_Y5Y6_observable_projection",
        "epsilon_Qvis_JH_DqZ_Y5Y6_total",
    }
    finite_symbols = {str(row["symbol"]) for row in finite_rows}
    local_claim = next(row for row in claim_rows_ if row["gate_id"] == "CG2910_7_local_GR_Newton")
    qvis_verdict = next(row for row in qvis_rows if row["gate_id"] == "QVIS2910_9_verdict")
    no_source_verdict = next(row for row in no_source_rows_ if row["audit_id"] == "NSS2910_7_verdict")

    checks = [
        (
            "VAL2910_0_source_paths_exist",
            all(bool(row["path_exists"]) for row in source_rows),
            "all cited source paths exist",
        ),
        (
            "VAL2910_1_source_anchors_found",
            all(bool(row["anchors_found"]) for row in source_rows),
            "all source anchors found in cited files",
        ),
        (
            "VAL2910_2_csv_outputs_parse",
            all(csv_parses(path) for path in csv_outputs_with_validation if path.exists()),
            "generated CSV outputs parse cleanly",
        ),
        (
            "VAL2910_3_qvis_not_promoted",
            qvis_verdict["current_status"] == "NOT_PARENT_SIGNED_FINITE_VECTOR_REQUIRED" and not bool(qvis_verdict["signed_now"]),
            "Q_vis theorem remains unpromoted for current MTS",
        ),
        (
            "VAL2910_4_no_source_countermodel_live",
            no_source_verdict["current_status"] == "NOT_DERIVED_CURRENT_MTS" and not bool(no_source_verdict["signed_now"]),
            "no-source-slot proof fails honestly and keeps countermodel rows live",
        ),
        (
            "VAL2910_5_finite_vector_complete",
            required_symbols.issubset(finite_symbols),
            "finite vector includes all Qvis/JH/DqZ/Y5Y6 components",
        ),
        (
            "VAL2910_6_claim_gates_safe",
            local_claim["gate_status"] == "BLOCKED_NONCLAIM"
            and all(not bool(row["claim_allowed"]) and not bool(row["valid_for_claim"]) for row in claim_rows_),
            "local GR/Newton and empirical claims remain blocked",
        ),
        (
            "VAL2910_7_next_target_selected",
            next_rows_[0]["route_id"] == "NEXT2910_0_2911" and bool(next_rows_[0]["selected"]),
            "2911 parent q-map/kernel target selected",
        ),
        (
            "VAL2910_8_branch_copies_parse",
            all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_),
            "branch copies exist and parse",
        ),
        (
            "VAL2910_9_no_formalization_outputs",
            not any(is_under(path, FORMALIZATION) for path in [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]),
            "no generated output path is inside formalization-workbench",
        ),
        (
            "VAL2910_10_doc_written",
            DOC.exists() if include_doc_check else True,
            "markdown checkpoint exists",
        ),
    ]

    rows: list[dict[str, Any]] = [
        {
            "validation_id": validation_id,
            "status": bool(status),
            "detail": detail,
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
        for validation_id, status, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2910_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2910 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    qvis_rows: list[dict[str, Any]],
    no_source_rows_: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    arena_rows_: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2910_OVERALL")
    text = f"""# 2910 - Y5/R2FR Qvis Object-Language No-Source-Slot Or Finite JH/DqZ/Y5Y6 Vector Under AX1090

Status: `Y5_R2FR_2910_Qvis_no_source_slot_not_parent_signed_finite_vector_staged_2911_next`

Claim ceiling: `object_language_and_coupling_residual_vector_nonclaim_only_no_Qvis_zero_no_DqZ_zero_no_JH_zero_no_Y5Y6_zero_no_Newton_no_PPN_no_R10_no_local_GR_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2910 takes the lock named by 2909 seriously: try to make ordinary matter and readouts depend only on the visible quotient object `Q_vis`, with no direct residual slot, no source-only weight, no marker/theta leak, and no source/readout re-entry. The useful mathematical statement is clean:

`delta_v S_matter = D Sbar[Dq(v)] + J_theta Lie_v(theta) + J_direct[v] + delta_v B`.

If `v=v_Z` sits in `ker(Dq)`, theta/markers are silent, direct slots are illegal, and boundary/worldtube terms are zero or bounded, then the Hilbert/source leak is zero by chain rule. That is a real conditional theorem. Current MTS still does not sign the needed parent object language, so 2910 does not claim local GR. It stages the finite `Q_vis/JH/DqZ/Y5Y6` vector and selects the upstream parent field chart/q-map/kernel basis as 2911.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Qvis Object-Language Gate

{md_table(qvis_rows, ["gate_id", "clause", "current_status", "theorem_or_contract", "blocking_gap", "residual_if_unsigned", "signed_now", "valid_for_claim"])}

## No-Source-Slot Audit

{md_table(no_source_rows_, ["audit_id", "clause", "current_status", "statement", "blocker_or_guard", "signed_now", "valid_for_claim"])}

## Finite JH/DqZ/Y5Y6 Vector

{md_table(finite_rows, ["vector_id", "symbol", "definition", "units", "formula_or_bound", "current_value", "arena_targets", "current_status", "valid_for_claim"])}

## Arena Map

{md_table(arena_rows_, ["arena_id", "arena", "projection_or_gate", "current_status", "guardrail", "valid_for_claim"])}

## Runner Status

{md_table(runner_rows_, ["runner_id", "status", "required_components", "components_evaluable", "reason", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows_, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows_, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows_, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall["status"]}`.

## Interpretation

This is progress in the exact place that matters. The coupling problem has now been reduced to a typed source-language problem rather than a vague worry. If the parent action supplies the field chart, the quotient map, and the kernel basis, then the source-current zero route can become theorem-shaped. If it does not, the theory can still be tested honestly by carrying the finite vector into Newton, PPN, WEP, R10, clock/EM and orbital arenas.

The main blocker is not "MTS failed"; it is narrower: current MTS has not yet derived the object language that forbids `w_A(Z) S_A`, `kappa_A(Z) T_A`, source current rescalings, marker tails, and boundary/projector re-entry before variation. That is why the next useful attack is upstream, not another empirical scorecard.

## Not Claimed

- `Q_vis` object-language source-side zero is not proved for current MTS.
- `Dq_Z_norm`, `eps_JH_Z_abs`, `E_DqZ_A`, `Delta_w_abs`, `J_M`, `J_Z`, Y5 or Y6 residuals are not theorem-zero.
- Newton, PPN, R10, WEP, clock/EM, orbital or local-GR reduction is not claimed.
- No public/GitHub action is implied.
- No file in `formalization-workbench` is modified by this checkpoint.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    qvis_rows = qvis_gate_rows()
    no_source_rows_ = no_source_slot_rows()
    finite_rows = finite_vector_rows()
    arena_rows_ = arena_rows()
    runner_rows_ = runner_rows(source_rows)
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["qvis_gate"], qvis_rows)
    write_csv(OUTPUTS["no_source"], no_source_rows_)
    write_csv(OUTPUTS["finite_vector"], finite_rows)
    write_csv(OUTPUTS["arenas"], arena_rows_)
    write_csv(OUTPUTS["runner"], runner_rows_)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        qvis_rows,
        no_source_rows_,
        finite_rows,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        qvis_rows,
        no_source_rows_,
        finite_rows,
        arena_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        qvis_rows,
        no_source_rows_,
        finite_rows,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        qvis_rows,
        no_source_rows_,
        finite_rows,
        arena_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2910_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
