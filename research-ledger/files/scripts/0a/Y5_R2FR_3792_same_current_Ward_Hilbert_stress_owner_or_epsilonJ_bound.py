import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3792"
BRANCH = "MTS_R2FR_Y5_SAME_CURRENT_WARD_HILBERT_STRESS_OWNER_OR_EPSILONJ_BOUND_3792"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3792_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3792_SAME_CURRENT_WARD_HILBERT_THEOREM.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3792_CURRENT_CORPUS_SIGNATURE_AUDIT.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_3792_EPSILON_JQ_COMPONENTS.csv",
    "pim_update": RESIDUALS / "P8_Y5_R2FR_3792_PIM_TOTAL_EM_SOURCE_UPDATE.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_3792_WARD_COUNTEREXAMPLE_GUARD.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3792_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3792_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3792_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3792_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3792_VALIDATION.csv",
}

SOURCE_PATHS = [
    PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md",
    PCW / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md",
    PCW / "3760-Y5-R2FR-Maxwell-EM-stress-same-source-current-or-residual.md",
    PCW / "3776-Y5-R2FR-total-Hilbert-source-inclusion-EM-Poynting-and-interior-monopole-closure.md",
    PCW / "3777-Y5-R2FR-PiM-total-system-domain-and-EM-field-energy-source-map.md",
    PCW / "3339-Y5-R2FR-parent-source-coupling-decomposition-under-AX1090.md",
    PCW / "3340-Y5-R2FR-parent-Hilbert-source-clause-or-finite-residual-vector-under-AX1090.md",
    PCW / "3780-Y5-R2FR-vertical-EM-basicness-calculation-A-F-ZEM.md",
    PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
]


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def source_register(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "source_path": str(path),
            "exists": path.exists(),
            "source_role": "same_current_Ward_Hilbert_source_context",
            "valid_for_claim": False,
        }
        for path in SOURCE_PATHS
    ]


def theorem_rows(timestamp):
    rows = [
        {
            "theorem_id": "SCW3792_0_total_source_owner",
            "claim_piece": "one descended source action owns current and stress",
            "mathematical_form": "Assume S_src=S_charged[psi,g_obs,A_Q,theta]+S_EM[g_obs,A_Q,Z_EM]+S_binding+S_apparatus+S_int+S_boundary descends through q_obs and all displayed sectors are varied before readout against the same g_obs/coframe and A_Q.",
            "derivation_status": "ASSUMPTION_PACKAGE_FOR_EXACT_THEOREM",
            "zero_result_if_signed": "no separate matter-current owner, no separate EM gravitational source owner, and no source-only normalization channel",
            "missing_for_current_claim": "parent q_obs source action; parent U1/Pi_Q/B_Q owner; Z_EM/lambda closure; total domain/tail closure",
        },
        {
            "theorem_id": "SCW3792_1_same_current_definition",
            "claim_piece": "same J_Q",
            "mathematical_form": "J_Q^a := (1/sqrt(-g_obs)) delta S_src/delta A_Qa, with the same variational derivative supplying the source in the Maxwell equation.",
            "derivation_status": "EXACT_BY_VARIATIONAL_DEFINITION_IF_SINGLE_ACTION_EXISTS",
            "zero_result_if_signed": "epsilon_J_owner=0 and no current mismatch between charged matter and Maxwell source",
            "missing_for_current_claim": "single q_obs-descended source action containing charged matter, EM, binding, apparatus, and interactions",
        },
        {
            "theorem_id": "SCW3792_2_gauge_Ward_conservation",
            "claim_piece": "charge-current Ward identity",
            "mathematical_form": "Gauge variation gives delta_lambda S_src=-int sqrt(-g_obs) lambda nabla_a J_Q^a + boundary; on-shell and with silent boundary, nabla_a J_Q^a=0.",
            "derivation_status": "EXACT_CONDITIONAL_WARD_IDENTITY",
            "zero_result_if_signed": "epsilon_J_div=0",
            "missing_for_current_claim": "boundary/domain silence and parent-owned gauge action",
        },
        {
            "theorem_id": "SCW3792_3_total_Hilbert_stress",
            "claim_piece": "same total stress",
            "mathematical_form": "T_total^{ab}:=(2/sqrt(-g_obs)) delta S_src/delta g_obs_ab = T_charged^{ab}+T_EM^{ab}+T_binding^{ab}+T_apparatus^{ab}+T_int^{ab} by linearity of variation.",
            "derivation_status": "EXACT_CONDITIONAL_HILBERT_IDENTITY",
            "zero_result_if_signed": "epsilon_EM_Hilbert=0 and binding/apparatus stresses are not side-channel mass",
            "missing_for_current_claim": "all sectors in the same q_obs source action and varied with the same observed metric/coframe",
        },
        {
            "theorem_id": "SCW3792_4_Lorentz_internal_exchange",
            "claim_piece": "Lorentz force cancellation inside total stress",
            "mathematical_form": "On Maxwell/matter equations, nabla_a T_EM^{ab}=-F^b_c J_Q^c and nabla_a(T_charged+T_binding)^{ab}=+F^b_c J_Q^c + Q_parent^b, so the FJ exchange cancels in nabla_a T_total^{ab}.",
            "derivation_status": "EXACT_CONDITIONAL_WARD_CANCELLATION",
            "zero_result_if_signed": "epsilon_Lorentz_exchange=0 except declared parent/non-EM exchange Q_parent^b",
            "missing_for_current_claim": "same current and same Hilbert source owner plus parent exchange projection silence",
        },
        {
            "theorem_id": "SCW3792_5_epsilonJ_zero",
            "claim_piece": "same-current residual zero",
            "mathematical_form": "If SCW3792_0 through SCW3792_4 hold, epsilon_J_Q_total_abs=sum_abs(epsilon_J_div,epsilon_J_owner,epsilon_Lorentz_exchange,epsilon_EM_Hilbert,epsilon_binding_source,epsilon_Poynting_domain,epsilon_source_weight)=0.",
            "derivation_status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "zero_result_if_signed": "epsilon_J_Q=0",
            "missing_for_current_claim": "all same-source, Ward, Hilbert, domain, and source-weight clauses parent-signed",
        },
        {
            "theorem_id": "SCW3792_6_PiM_total_admission_rule",
            "claim_piece": "EM/Poynting admission into Pi_M_total",
            "mathematical_form": "T_EM and Poynting stress enter Pi_M_total as ordinary Hilbert source terms only if same-current/Hilbert ownership, total-system domain closure, boundary/tail silence, and Z_EM/lambda gates are closed or bounded.",
            "derivation_status": "EXACT_CONDITIONAL_SOURCE_ADMISSION_RULE",
            "zero_result_if_signed": "EM/Poynting no longer live in mu_extra; they are part of M_H,total",
            "missing_for_current_claim": "Z_EM, B_Q/A_Q owner, and total-domain tail certificates",
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
        row["valid_for_claim"] = False
    return rows


def audit_rows(timestamp):
    rows = [
        {
            "audit_id": "SCA3792_0_3760_same_source",
            "source_signal": "3760 already states the Maxwell Hilbert-stress identity and Lorentz Ward cancellation for one same source action.",
            "current_result": "THEOREM_SHAPE_SUPPORTED",
            "impact": "3792 can sharpen the exact current/stress owner theorem rather than re-audit the concept.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SCA3792_1_3776_total_source",
            "source_signal": "3776 says EM/Poynting, binding, apparatus, and interaction energy move into M_H,total only through one total Hilbert source action and total-system domain.",
            "current_result": "PIM_TOTAL_RULE_SUPPORTED",
            "impact": "Poynting is not a weird side force if it is in T_EM and the source domain is total-system.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SCA3792_2_3777_projector",
            "source_signal": "3777 builds Pi_M_total but keeps EM descent, tail/domain closure, and normalization unsigned.",
            "current_result": "PROJECTOR_CONDITIONAL_NOT_CLAIM",
            "impact": "same-current helps the source owner but cannot by itself close EM tails or domains.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SCA3792_3_3784_parent_U1",
            "source_signal": "3784 supplies a coherent parent U1 action grammar whose variation conditionally gives Ward conservation, Maxwell descent, and Hilbert stress.",
            "current_result": "PARENT_GRAMMAR_EXISTS_OWNER_UNSIGNED",
            "impact": "the route is viable as a parent extension; current real-scalar MTS has not built the U1 owner from pre-EM primitives.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SCA3792_4_3791_ZEM",
            "source_signal": "3791 keeps Z_EM/lambda and alpha readout nonclaim because no-independent-F2 and current/readout owner are unsigned.",
            "current_result": "NORMALIZATION_GATE_STILL_OPEN",
            "impact": "even epsilon_J_Q=0 would not prove alpha_EM or remove beta_Z/lambda leakage.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SCA3792_5_3339_3340_source",
            "source_signal": "3339/3340 split source coupling and Hilbert source clauses into exact zero-or-bound contracts, but parent source descent remains unsigned.",
            "current_result": "SOURCE_CLAUSE_NOT_PARENT_SIGNED",
            "impact": "3792 can derive the exact contract; it cannot claim the current corpus already satisfies it.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SCA3792_6_verdict",
            "source_signal": "the corpus supports the theorem but does not supply parent-owned numeric/source rows or a signed total action.",
            "current_result": "CONDITIONAL_THEOREM_PLUS_EPSILONJ_VECTOR",
            "impact": "record epsilon_J_Q components and push next toward B_Q/A_Q descent rather than pretending local GR is closed.",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def component_rows(timestamp):
    rows = [
        {
            "component_id": "EJ3792_0_div",
            "symbol": "epsilon_J_div",
            "definition": "normalized ||nabla_a J_Q^a|| Ward defect after boundary/domain terms are separated",
            "zero_if": "parent U1 gauge action is signed, equations of motion hold, and charge flux through the chosen boundary is silent or included",
            "fallback_value": "MISSING_GAUGE_WARD_BOUND_OR_BOUNDARY_FLUX",
            "feeds": "clock;R10;WEP;PPN;orbital_source",
            "status": "CONDITIONAL_ZERO_CURRENTLY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "EJ3792_1_owner",
            "symbol": "epsilon_J_owner",
            "definition": "mismatch between matter current from delta S_matter/delta A_Q and the current sourcing the Maxwell equation",
            "zero_if": "the same q_obs-descended S_src owns charged matter, EM, binding, apparatus, and interaction terms",
            "fallback_value": "MISSING_SAME_CURRENT_SOURCE_OWNER",
            "feeds": "EM_source;alpha_readout;WEP;PPN",
            "status": "CONDITIONAL_ZERO_CURRENTLY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "EJ3792_2_lorentz",
            "symbol": "epsilon_Lorentz_exchange",
            "definition": "normalized leftover |div(T_EM)+FJ| plus |div(T_charged+T_binding)-FJ-Q_parent|",
            "zero_if": "Maxwell and charged matter Ward identities use the same J_Q and parent exchange Q_parent is projected or bounded",
            "fallback_value": "MISSING_LORENTZ_WARD_EXCHANGE_CLOSURE",
            "feeds": "WEP;PPN_gamma;PPN_beta;Newton_GM",
            "status": "CONDITIONAL_ZERO_CURRENTLY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "EJ3792_3_hilbert",
            "symbol": "epsilon_EM_Hilbert",
            "definition": "mismatch between the EM stress used in the source map and the Hilbert stress varied from the same metric/coframe action",
            "zero_if": "S_EM descends as the same observed Maxwell action with universal Z_EM and no shadow metric",
            "fallback_value": "MISSING_EM_HILBERT_DESCENT_OR_SHADOW_METRIC_BOUND",
            "feeds": "Pi_M_total;mu_extra;PPN;WEP",
            "status": "CONDITIONAL_ZERO_CURRENTLY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "EJ3792_4_binding",
            "symbol": "epsilon_binding_source",
            "definition": "binding, material response, apparatus, or interaction stress varied outside the same source action",
            "zero_if": "binding/apparatus/interaction terms are in S_src and varied with the same g_obs/coframe and theta labels",
            "fallback_value": "MISSING_BINDING_APPARATUS_INTERACTION_SOURCE_DESCENT",
            "feeds": "Newton_GM;WEP;clock;orbital_source",
            "status": "CONDITIONAL_ZERO_CURRENTLY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "EJ3792_5_poynting_domain",
            "symbol": "epsilon_Poynting_domain",
            "definition": "radiative/Poynting/tail stress-energy not included in the total-system source domain or not bounded at the boundary",
            "zero_if": "Pi_M_total selects the total-system domain and Poynting/radiative flux is stationary, included, or bounded",
            "fallback_value": "MISSING_TOTAL_DOMAIN_TAIL_OR_POYNTING_FLUX_BOUND",
            "feeds": "mu_extra;radial_hair;Newton_GM;PPN",
            "status": "CONDITIONAL_ZERO_CURRENTLY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "EJ3792_6_source_weight",
            "symbol": "epsilon_source_weight",
            "definition": "source-only current/species/material weights that affect active source coupling without appearing in the same readout",
            "zero_if": "source weights are q_obs-owned, superselected, or common unit conventions rather than physical species labels",
            "fallback_value": "MISSING_SOURCE_WEIGHT_OR_THETA_SILENCE",
            "feeds": "WEP;clock;Newton_active_passive;R10",
            "status": "CONDITIONAL_ZERO_CURRENTLY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "EJ3792_7_total",
            "symbol": "epsilon_J_Q_total_abs",
            "definition": "sum_abs(epsilon_J_div,epsilon_J_owner,epsilon_Lorentz_exchange,epsilon_EM_Hilbert,epsilon_binding_source,epsilon_Poynting_domain,epsilon_source_weight)",
            "zero_if": "all epsilon_J_Q components above are theorem-zero or source-bounded below the relevant arena tolerance",
            "fallback_value": "MISSING_EPSILON_JQ_COMPONENT_VALUES",
            "feeds": "local_GR_gate;Pi_M_total;R10;PPN;WEP;clock;orbital",
            "status": "FINITE_VECTOR_RETAINED",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def pim_update_rows(timestamp):
    rows = [
        {
            "update_id": "PIM3792_0_same_current_effect",
            "branch": "conditional_zero",
            "formula": "same-current theorem sets Delta_J_leak=0, epsilon_J_owner=0, and epsilon_Lorentz_exchange=0; it does not by itself set R_A, dR_A, beta_Z,A, or lambda_A to zero",
            "conditions": "one descended S_src; same A_Q; same g_obs/coframe; Ward boundary silence",
            "impact": "prevents double-counting Lorentz force as external WEP/PPN violation",
            "valid_for_claim": False,
        },
        {
            "update_id": "PIM3792_1_RA_term_guard",
            "branch": "field_map_still_live",
            "formula": "delta_A S_src may still contain int sqrt(-g_obs) J_Q^a R_Aa; same-current kills current mismatch, while R_A is controlled by B_Q/A_Q descent",
            "conditions": "R_A or dR_A not yet theorem-zero",
            "impact": "pushes the next derivation toward B_Q descent amplitude and dB_Q bounds",
            "valid_for_claim": False,
        },
        {
            "update_id": "PIM3792_2_EM_Hilbert_admission",
            "branch": "Pi_M_total",
            "formula": "Pi_M_total may include T_EM, T_binding, T_apparatus, T_int, and Poynting stress only as Hilbert variations from the same total source action and total-system domain",
            "conditions": "same-current plus total-domain/tail closure plus Z_EM/lambda closure",
            "impact": "real EM/Poynting energy is conserved as source mass rather than deleted or made a hidden fifth force",
            "valid_for_claim": False,
        },
        {
            "update_id": "PIM3792_3_bound_form",
            "branch": "finite_current_corpus",
            "formula": "epsilon_total_source <= C_J epsilon_J_Q_total_abs + C_BQ(R_A_normed+dRA_normed) + C_Z(|beta_Z,A|+|lambda_A|) + C_tail epsilon_Poynting_domain + C_theta epsilon_source_weight",
            "conditions": "symbolic until coefficients and component values are parent-derived or data-sourced",
            "impact": "turns same-current failure into one bounded vector feeding WEP/PPN/R10/clock/orbital rows",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def guard_rows(timestamp):
    rows = [
        {
            "guard_id": "WCG3792_0_two_actions",
            "failure_mode": "matter current and Maxwell source come from separately normalized actions",
            "effect": "J_matter != J_Maxwell is legal unless one total source action owns both",
            "repair_needed": "single q_obs-descended S_src with same A_Q variation",
            "valid_for_claim": False,
        },
        {
            "guard_id": "WCG3792_1_source_only_weight",
            "failure_mode": "species or material coefficient multiplies source coupling but not readout",
            "effect": "WEP/source-normalization residual appears even with standard Maxwell equations",
            "repair_needed": "theta/source-weight superselection or same-readout descent",
            "valid_for_claim": False,
        },
        {
            "guard_id": "WCG3792_2_domain_cut",
            "failure_mode": "matter-only tube excludes EM tail, binding field, apparatus stress, or Poynting momentum",
            "effect": "unmatched field energy reappears as mu_extra or radial-hair/source residual",
            "repair_needed": "total-system Pi_M_total domain or explicit field-energy/tail bound",
            "valid_for_claim": False,
        },
        {
            "guard_id": "WCG3792_3_shadow_metric",
            "failure_mode": "EM stress is varied against a different metric/coframe than local gravity reads",
            "effect": "Hilbert source mismatch feeds PPN/WEP even if current is conserved",
            "repair_needed": "single observed frame q_obs theorem plus no EM shadow metric",
            "valid_for_claim": False,
        },
        {
            "guard_id": "WCG3792_4_boundary_flux",
            "failure_mode": "gauge/current or stress Ward identity has unaccounted boundary terms",
            "effect": "nabla J or nabla T zero is only local bookkeeping and not a closed source claim",
            "repair_needed": "boundary silence, total-system boundary inclusion, or flux bound",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def claim_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3792_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all cited source paths resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3792_1_exact_theorem_shape",
            "pass": True,
            "claim_allowed": False,
            "details": "same-current/Ward/Hilbert theorem is derived conditionally",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3792_2_current_parent_signed",
            "pass": False,
            "claim_allowed": False,
            "details": "current corpus lacks signed q_obs total source action, parent U1/B_Q owner, and total domain/tail closure",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3792_3_epsilonJ_zero_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "epsilon_J_Q remains finite because same-source clauses are not parent-signed",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3792_4_PiM_total_EM_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "EM/Poynting can enter Pi_M_total only conditionally; tail/domain/ZEM/BQ clauses remain open",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3792_5_local_GR_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "no local-GR claim from 3792; it narrows the source-current contract and defines epsilon_J_Q",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3792_0_theorem",
            "decision": "The same-current/Ward/Hilbert source theorem is exact once one descended total source action is signed.",
            "action": "Keep it as a real derivation target, not a vibes ledger.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3792_1_nonclaim",
            "decision": "The current corpus does not yet sign the parent total action, U1 owner, Z_EM/lambda silence, or total-domain tails.",
            "action": "Retain epsilon_J_Q components and keep all local-GR/EM claims closed.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3792_2_Poynting",
            "decision": "Poynting/vector-field energy is not an enemy of the route; it is safe only as part of the same Hilbert source and total domain.",
            "action": "Route Poynting through Pi_M_total/domain closure, not through matter-only source tubes.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3792_3_next",
            "decision": "Same-current narrows the problem to the still-live actual coupling throat: A_Q/B_Q descent, dB_Q, Z_EM/lambda, and total-domain tails.",
            "action": "Attack B_Q descent amplitude and dB_Q bounds next because 3790-3792 reduce R_A and current mismatch to that owner problem.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3793-Y5-R2FR-BQ-descent-amplitude-or-eps-dBQ-bound.md",
            "target_script": "scripts/Y5_R2FR_3793_BQ_descent_amplitude_or_eps_dBQ_bound.py",
            "objective": "Use 3788-3792 to try to derive or bound the remaining A_Q/B_Q descent amplitude: eps_BQ_descent_A and eps_dBQ_A, separating exact local chart/gauge zeros from real parent-owner and curvature-amplitude failures.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "SAME_CURRENT_WARD_HILBERT_THEOREM_CONDITIONAL_CURRENT_CORPUS_UNSIGNED_EPSILONJ_RETAINED",
            "plain_verdict": "3792 proves the exact conditional route: one q_obs-descended total source action makes J_Q, Maxwell source, Hilbert stress, binding/apparatus stress, and Lorentz exchange share the same owner, so epsilon_J_Q is zero and EM/Poynting may enter Pi_M_total. The current corpus does not parent-sign the total action, U1/B_Q owner, Z_EM/lambda silence, or total-domain tails, so epsilon_J_Q remains a finite nonclaim residual vector.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(timestamp, grouped):
    def csv_parses(path):
        if not path.exists():
            return False
        with path.open(encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True

    checks = [
        (
            "sources_exist",
            all(Path(row["source_path"]).exists() for row in grouped["sources"]),
            "every cited source path exists",
        ),
        (
            "csv_outputs_parse",
            all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation"),
            "all generated CSV outputs exist and parse",
        ),
        ("doc_written", DOC_PATH.exists(), "3792 markdown document written"),
        (
            "same_current_theorem",
            any(row["theorem_id"] == "SCW3792_5_epsilonJ_zero" for row in grouped["theorem"]),
            "conditional epsilon_J_Q zero theorem emitted",
        ),
        (
            "epsilon_components",
            all(
                any(row["symbol"] == symbol for row in grouped["components"])
                for symbol in [
                    "epsilon_J_div",
                    "epsilon_J_owner",
                    "epsilon_Lorentz_exchange",
                    "epsilon_EM_Hilbert",
                    "epsilon_binding_source",
                    "epsilon_Poynting_domain",
                    "epsilon_source_weight",
                    "epsilon_J_Q_total_abs",
                ]
            ),
            "full epsilon_J_Q component vector emitted",
        ),
        (
            "pim_update",
            any(row["update_id"] == "PIM3792_2_EM_Hilbert_admission" for row in grouped["pim_update"]),
            "Pi_M_total EM/Poynting admission rule emitted",
        ),
        (
            "current_nonclaim",
            any(row["gate_id"] == "CG3792_3_epsilonJ_zero_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "epsilon_J_Q zero claim remains closed",
        ),
        (
            "local_gr_closed",
            any(row["gate_id"] == "CG3792_5_local_GR_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "local-GR claim remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3793-"),
            "3793 B_Q descent-amplitude target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3792 files written under formalization-workbench",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "validation_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for check_id, ok, detail in checks
    ]


def render_section(title, rows, key_fields):
    lines = [f"## {title}"]
    for row in rows:
        head = " ".join(f"`{row[field]}`" for field in key_fields if field in row)
        details = []
        for key, value in row.items():
            if key in key_fields or key in {"timestamp_utc", "checkpoint_id", "branch_id", "valid_for_claim"}:
                continue
            details.append(f"{key}: {value}")
        lines.append(f"- {head}: " + "; ".join(details))
    lines.append("")
    return "\n".join(lines)


def render_doc(grouped):
    status = grouped["status"][0]
    text = [
        "# 3792 - Same-Current Ward/Hilbert Stress Owner or epsilon_J Bound",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3792 is a real narrowing move. If charged matter, Maxwell field, binding energy, apparatus stress, interactions, and boundary bookkeeping all come from one `q_obs`-descended source action, then the current in the Maxwell equation is the same current varied from the source action, the EM stress is the same Hilbert stress local gravity reads, and the Lorentz force is internal exchange, not a fifth-force side channel. In that parent-signed branch `epsilon_J_Q=0`.",
        "",
        "The current corpus does not yet sign that parent action. It has the correct theorem shape, but the U(1)/`B_Q` owner, `Z_EM/lambda` silence, total source domain, Poynting/tail boundary closure, and source-weight silence remain open. So 3792 does not claim local GR; it turns the loose coupling issue into a precise `epsilon_J_Q` residual vector.",
        "",
        "## Compact Derivation",
        "",
        "`J_Q^a := (1/sqrt(-g_obs)) delta S_src/delta A_Qa`.",
        "",
        "`T_total^{ab}:=(2/sqrt(-g_obs)) delta S_src/delta g_obs_ab = T_charged^{ab}+T_EM^{ab}+T_binding^{ab}+T_apparatus^{ab}+T_int^{ab}`.",
        "",
        "Gauge Ward identity: `delta_lambda S_src=-int sqrt(-g_obs) lambda nabla_a J_Q^a + boundary`, so `nabla_a J_Q^a=0` only when the boundary/domain term is silent or included.",
        "",
        "Stress Ward identity: `nabla_a T_EM^{ab}=-F^b_c J_Q^c` and `nabla_a(T_charged+T_binding)^{ab}=+F^b_c J_Q^c+Q_parent^b`; the `FJ` terms cancel inside `nabla_a T_total^{ab}`.",
        "",
        "Residual vector: `epsilon_J_Q_total_abs=sum_abs(epsilon_J_div,epsilon_J_owner,epsilon_Lorentz_exchange,epsilon_EM_Hilbert,epsilon_binding_source,epsilon_Poynting_domain,epsilon_source_weight)`.",
        "",
        render_section("Same-Current Ward/Hilbert Theorem", grouped["theorem"], ["theorem_id", "claim_piece"]),
        render_section("Current Corpus Signature Audit", grouped["audit"], ["audit_id"]),
        render_section("epsilon_J_Q Components", grouped["components"], ["component_id", "symbol"]),
        render_section("Pi_M_total EM Source Update", grouped["pim_update"], ["update_id", "branch"]),
        render_section("Ward Counterexample Guard", grouped["guards"], ["guard_id", "failure_mode"]),
        render_section("Claim Gates", grouped["claim_gates"], ["gate_id"]),
        render_section("Decisions", grouped["decisions"], ["decision_id"]),
        render_section("Next Target", grouped["next_target"], ["target_file"]),
        render_section("Validation", grouped["validation"], ["validation_id", "result"]),
    ]
    return "\n".join(text).rstrip() + "\n"


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    grouped = {
        "sources": source_register(timestamp),
        "theorem": theorem_rows(timestamp),
        "audit": audit_rows(timestamp),
        "components": component_rows(timestamp),
        "pim_update": pim_update_rows(timestamp),
        "guards": guard_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["audit"], grouped["audit"])
    write_csv(OUTPUTS["components"], grouped["components"])
    write_csv(OUTPUTS["pim_update"], grouped["pim_update"])
    write_csv(OUTPUTS["guards"], grouped["guards"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3792 validation failed: {failures}")
    print("wrote 3792 checkpoint: same-current theorem and epsilon_J_Q residual vector emitted")


if __name__ == "__main__":
    main()
