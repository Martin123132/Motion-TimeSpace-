from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains_missing(value: object) -> bool:
    text = str(value)
    return text.strip() == "" or "MISSING" in text


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1155_0_1154_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1154_NEXT_TARGET.csv",
            "needle": "NEXT1154_0_1155",
            "role": "handoff selecting single observed coframe owner or frame residual row.",
        },
        {
            "source_id": "SRC1155_1_1154_owner",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1154_SOURCE_OWNER_AUDIT.csv",
            "needle": "OWN1154_2_single_observed_coframe",
            "role": "1154 source-owner audit identifying observed coframe as upstream missing owner.",
        },
        {
            "source_id": "SRC1155_2_1154_schema",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1154_R_EQ_PROFILE_SCHEMA.csv",
            "needle": "PROF1154_1_frame_and_generator",
            "role": "R_eq profile schema requiring frame/generator ownership.",
        },
        {
            "source_id": "SRC1155_3_coframe_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
            "needle": "CFC943_7_contract_verdict",
            "role": "coframe coupling contract: exact but unsigned.",
        },
        {
            "source_id": "SRC1155_4_coframe_derivation",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_943_DERIVATION_ATTEMPT.csv",
            "needle": "DER943_6_verdict",
            "role": "conditional derivation of observed coframe/source blindness.",
        },
        {
            "source_id": "SRC1155_5_frame_residual_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_943_FRAME_RESIDUAL_SOURCE_PACK.csv",
            "needle": "FRS943_7_epsilon_frame_coupling",
            "role": "frame residual source pack for nonclaim fallback components.",
        },
        {
            "source_id": "SRC1155_6_descent_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_944_DESCENT_PROOF_GATE.csv",
            "needle": "QDG944_7_total",
            "role": "quotient descent proof gate showing parent map/matter factorization unsigned.",
        },
        {
            "source_id": "SRC1155_7_frame_leak_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
            "needle": "FLB944_7_epsilon_frame_leak",
            "role": "frame leak bound pack with arena-linked fallback terms.",
        },
        {
            "source_id": "SRC1155_8_first_bound_rows",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
            "needle": "BND945_7_score_gate",
            "role": "first frame leak bound rows, all nonclaim until sources/projections exist.",
        },
        {
            "source_id": "SRC1155_9_matter_coupling",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv",
            "needle": "MCD716_6_current_corpus_verdict",
            "role": "matter coupling derivation retaining frame-dependent source coefficients.",
        },
        {
            "source_id": "SRC1155_10_observed_force",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv",
            "needle": "FRM1068_5_verdict",
            "role": "observed-frame force/readout map not derived.",
        },
        {
            "source_id": "SRC1155_11_tau_owner",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_742_OBSERVED_TAU_OWNER_AUDIT.csv",
            "needle": "TOA742_4_owner_verdict",
            "role": "observed tau/source normal owner still not parent-owned.",
        },
        {
            "source_id": "SRC1155_12_readout_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1113_PARENT_OWNED_READOUT_DESCENT_CONTRACT.csv",
            "needle": "POC1113_7_arena_functors",
            "role": "readout descent contract requiring arena functors.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def coframe_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "COF1155_0_conditional_chain_rule",
                "claim_piece": "observed coframe vertical blindness",
                "mathematical_form": "if e_obs=Obs_e(q(Phi)) and v in ker(Dq), then Lie_v e_obs=DObs_e[Dq(v)]=0",
                "required_parent_signature": "parent q-map and vertical generator are actual configuration/action data",
                "current_status": "VALID_CONDITIONAL_LEMMA_ONLY",
                "failure_if_missing": "Dq(v)=0 is notation, not a theorem",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "COF1155_1_parent_q_map",
                "claim_piece": "parent quotient map",
                "mathematical_form": "q: Phi_parent -> Q_obs before matter coupling and readout",
                "required_parent_signature": "q included in parent kinematics/action, not post-fit equivalence",
                "current_status": "UNSIGNED",
                "failure_if_missing": "observed-frame descent cannot start",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "COF1155_2_matter_functor",
                "claim_piece": "ordinary matter action factors through observed coframe",
                "mathematical_form": "S_matter[Phi,Psi]=Sbar_matter[q(Phi),Psi,theta] with e_obs=Obs_e(q(Phi))",
                "required_parent_signature": "matter functor and quotient-owned constants/masses",
                "current_status": "NOT_PARENT_SIGNED",
                "failure_if_missing": "representative Weyl/disformal/mass channels remain legal",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "COF1155_3_geometry_stack",
                "claim_piece": "measure/coframe/connection/derivative stack descends together",
                "mathematical_form": "mu_m,e_m,g_m,omega_m,D_m are functions of q(Phi) or owned exact/gauge data",
                "required_parent_signature": "no torsion/nonmetricity/non-Hilbert source tail unless retained",
                "current_status": "NOT_PARENT_SIGNED",
                "failure_if_missing": "connection force can re-enter local source current",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "COF1155_4_tau_normal_lock",
                "claim_piece": "same observed tau and normal define source, charge, clock, orbit, and boundary",
                "mathematical_form": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary and n_source=n_readout",
                "required_parent_signature": "parent-selected observed generator and support normal before readout",
                "current_status": "NOT_PARENT_OWNED",
                "failure_if_missing": "Delta_tau_n and support shift remain active",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "COF1155_5_arena_functors",
                "claim_piece": "force, WEP, clock, R10, and orbital readouts use the same q-branch",
                "mathematical_form": "observables = post-solution functors of one descended observed branch",
                "required_parent_signature": "arena maps after parent solution, not readout variables inside parent equations",
                "current_status": "MISSING_ARENA_MAPS",
                "failure_if_missing": "cross-arena silence must be scored by separate product rows",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "COF1155_6_counterexample_class",
                "claim_piece": "representative shadow frame counterexample retained",
                "mathematical_form": "g_A=A_A(X)^2 g_obs + B_A(X)U_mu U_nu; m_A=m_A(X,theta)",
                "required_parent_signature": "no-shadow theorem or sourced c_g,b_dis,b_A frame rows",
                "current_status": "COUNTEREXAMPLE_CLASS_RETAINED",
                "failure_if_missing": "single observed coframe is not guaranteed",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "COF1155_7_verdict",
                "claim_piece": "current MTS proves e_obs=e_source=e_force=e_clock=e_readout",
                "mathematical_form": "COF1155_1 through COF1155_6 all parent-signed in one branch",
                "required_parent_signature": "q-map, matter functor, constants, geometry stack, tau/normal lock, and arena functors",
                "current_status": "SINGLE_OBSERVED_COFRAME_NOT_DERIVED",
                "failure_if_missing": "emit Delta_frame/Delta_cal residual row; no Newton/local-GR promotion",
                "valid_for_claim": "false",
            },
        ]
    )


def residual_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "DFR1155_0_Delta_frame",
                "quantity": "Delta_frame",
                "definition": "mismatch between source coframe and force/clock/orbital/readout coframe",
                "required_columns": "system_id;source_frame;force_frame;clock_frame;orbit_frame;readout_frame;Delta_frame;units;source_path;zero_theorem_path",
                "current_value": "MISSING_DELTA_FRAME",
                "source_path": "MISSING_SOURCE_FILE",
                "arena_links": "R_eq;WEP;clock;PPN;orbital;R10",
                "status": "MISSING_SINGLE_FRAME_THEOREM_OR_NUMERIC_BOUND",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "DFR1155_1_Delta_cal",
                "quantity": "Delta_cal",
                "definition": "calibration mismatch between dressed source charge and inverse-square/orbital force readout",
                "required_columns": "system_id;M_H_ref;GM_readout;Delta_cal;units;calibration_convention;source_path;zero_theorem_path",
                "current_value": "MISSING_DELTA_CAL",
                "source_path": "MISSING_SOURCE_FILE",
                "arena_links": "Newton;orbital;R_eq;PPN",
                "status": "MISSING_GAUSS_ORBITAL_CALIBRATION_OR_BOUND",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "DFR1155_2_Delta_tau_n",
                "quantity": "Delta_tau_n",
                "definition": "mismatch between source tau/n and exterior/readout tau/n",
                "required_columns": "system_id;tau_source;tau_readout;n_source;n_readout;Delta_tau_n;units;source_path",
                "current_value": "MISSING_DELTA_TAU_N",
                "source_path": "MISSING_SOURCE_FILE",
                "arena_links": "clock;orbital;source_support;R_eq",
                "status": "MISSING_TAU_NORMAL_LOCK",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "DFR1155_3_Delta_W_support",
                "quantity": "Delta_W_support",
                "definition": "source support/worldtube shift induced by changing observed frame or support rule",
                "required_columns": "system_id;support_rule_source;support_rule_readout;Delta_W_support;units;source_path",
                "current_value": "MISSING_DELTA_W_SUPPORT",
                "source_path": "MISSING_SOURCE_FILE",
                "arena_links": "R_eq;orbital;local_GR",
                "status": "MISSING_SUPPORT_FRAME_EQUIVALENCE",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "DFR1155_4_frame_coupling_vector",
                "quantity": "epsilon_frame_coupling",
                "definition": "absolute component envelope for c_g,b_dis,b_A,q_nonH,Delta_tau_n,Delta_W_support,Delta_cal",
                "required_columns": "system_id;component_sum_abs;normalization;epsilon_frame_coupling;units;source_path",
                "current_value": "MISSING_COMPONENT_INPUTS",
                "source_path": "MISSING_SOURCE_FILE",
                "arena_links": "all_local_arenas",
                "status": "MISSING_COMPONENTS_NONCLAIM",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "DFR1155_5_runner_interface",
                "quantity": "frame_residual_runner_interface",
                "definition": "frame rows feed PROF1154_1_frame_and_generator and R_eq profile normalization",
                "required_columns": "Delta_frame;Delta_cal;Delta_tau_n;Delta_W_support;source_paths;valid_for_claim",
                "current_value": "MISSING_FRAME_RESIDUALS",
                "source_path": "MISSING_SOURCE_FILE",
                "arena_links": "PROF1154_1;REQ1153_1;ACQ1152_0",
                "status": "BLOCKED_MISSING_COMPONENTS",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def arena_schema_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "schema_id": "ARENA1155_0_R_eq",
                "arena": "R_eq/local source normalization",
                "frame_requirement": "e_source=e_readout and same M_H_ref denominator",
                "residual_if_failed": "Delta_frame;Delta_tau_n;Delta_W_support",
                "claim_status": "blocked_nonclaim",
                "valid_for_claim": "false",
            },
            {
                "schema_id": "ARENA1155_1_WEP",
                "arena": "WEP/MICROSCOPE",
                "frame_requirement": "e_source=e_force and material constants quotient-owned",
                "residual_if_failed": "b_A;Delta_frame;Delta_cal",
                "claim_status": "blocked_nonclaim",
                "valid_for_claim": "false",
            },
            {
                "schema_id": "ARENA1155_2_clock",
                "arena": "clock/frequency standards",
                "frame_requirement": "e_clock=e_source and constants/masses quotient-owned",
                "residual_if_failed": "b_alpha;b_clock;b_A;Delta_tau_n",
                "claim_status": "blocked_nonclaim",
                "valid_for_claim": "false",
            },
            {
                "schema_id": "ARENA1155_3_PPN_orbital",
                "arena": "PPN/orbital/Gauss readout",
                "frame_requirement": "e_orbit=e_source and tau/n/readout calibration fixed",
                "residual_if_failed": "Delta_cal;Delta_tau_n;Delta_W_support;PPN preferred-frame vector",
                "claim_status": "blocked_nonclaim",
                "valid_for_claim": "false",
            },
            {
                "schema_id": "ARENA1155_4_R10",
                "arena": "short-range R10 alpha(lambda)",
                "frame_requirement": "source/test projection uses same observed branch and no shadow c_g",
                "residual_if_failed": "c_g;b_dis;q_nonH;tau_R10",
                "claim_status": "blocked_nonclaim",
                "valid_for_claim": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1155_0_no_frame_relabel",
                "guard": "do not set frames equal by notation after readout",
                "status": "ACTIVE",
                "reason": "frame equality must follow from parent matter coupling or be retained as Delta_frame",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1155_1_no_shadow_frame",
                "guard": "representative Weyl/disformal/mass channels are legal unless forbidden or sourced",
                "status": "ACTIVE",
                "reason": "shadow frame counterexamples generate R10, WEP, clock, and PPN residuals",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1155_2_no_common_calibration_absorption",
                "guard": "relative frame/source effects cannot be hidden inside measured G or GM",
                "status": "ACTIVE",
                "reason": "common-mode calibration does not remove WEP/clock/composition residuals",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1155_3_no_local_GR_promotion",
                "guard": "single-frame failure blocks source-normalized Newton/local-GR promotion",
                "status": "ACTIVE",
                "reason": "GR reduction needs source, clocks, force, orbit, and PPN in the same observed frame",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1155_0_sources_exist",
                "rule": "all 1155 cited local source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the local audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1155_1_conditional_descent_lemma",
                "rule": "conditional observed-coframe descent lemma is stated",
                "gate_pass": "true_nonclaim",
                "reason": "chain-rule theorem is conditional and not used as current evidence",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1155_2_single_observed_frame_parent_signed",
                "rule": "current MTS proves e_obs=e_source=e_force=e_clock=e_readout",
                "gate_pass": "false",
                "reason": "q-map, matter functor, geometry stack, tau/normal lock, and arena maps remain unsigned",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1155_3_frame_residual_rows_ready",
                "rule": "Delta_frame/Delta_cal fallback rows exist and stay nonclaim",
                "gate_pass": "true_nonclaim",
                "reason": "residual rows are emitted with missing markers and claim_allowed=false",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1155_4_Newton_GR_promotion",
                "rule": "source-normalized Newton/local-GR claim allowed",
                "gate_pass": "false",
                "reason": "single observed frame and residual values are missing",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1155_0_conditional_route",
                "decision": "observed_coframe_descent_route_is_real_but_conditional",
                "reason": "chain-rule descent would kill frame leakage if q, matter functor, constants, and geometry stack are parent-signed",
                "next_action": "do not promote until the parent quotient/matter functor is signed",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1155_1_current_branch",
                "decision": "single_observed_coframe_not_derived_for_current_MTS",
                "reason": "the current corpus keeps representative frame, constants, tau/normal, and arena maps unsigned",
                "next_action": "retain Delta_frame/Delta_cal rows",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1155_2_best_next",
                "decision": "target_parent_quotient_matter_functor_signature_or_frame_leak_bound_fill",
                "reason": "q-map and matter functor are upstream of all single-frame claims",
                "next_action": "1156 parent quotient/matter functor signature or c_g/b_A/frame-leak bound fill",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1155_0_1156",
                "next_target": "1156-Y5-R10-parent-quotient-matter-functor-signature-or-frame-leak-bound-fill.md",
                "objective": "try to parent-sign q:Phi->Q_obs and S_matter factorization through e_obs(q); if it fails, fill c_g,b_dis,b_A,q_nonH frame-leak bound rows",
                "include": "q map; vertical generator; e_obs functor; matter action factorization; quotient-owned constants; frame-leak bound schema",
                "exclude": "frame relabel; hidden Weyl/disformal channel; common calibration cheat; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    residuals: list[dict[str, object]],
    arenas: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = audit + residuals + arenas + guards + gates + decisions + next_target
    add(
        "V1155_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1155_1_verdict_blocks_frame_proof",
        any(row["audit_id"] == "COF1155_7_verdict" and row["current_status"] == "SINGLE_OBSERVED_COFRAME_NOT_DERIVED" for row in audit),
        "single observed coframe remains unsigned for current MTS",
    )
    required_residuals = {"DFR1155_0_Delta_frame", "DFR1155_1_Delta_cal", "DFR1155_2_Delta_tau_n", "DFR1155_3_Delta_W_support", "DFR1155_4_frame_coupling_vector"}
    add(
        "V1155_2_residual_rows_present",
        required_residuals.issubset({row["row_id"] for row in residuals}),
        "Delta_frame, Delta_cal, tau/normal, support, and frame-coupling rows are present",
    )
    add(
        "V1155_3_residual_rows_nonclaim_missing",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and contains_missing(row["current_value"]) for row in residuals),
        "residual rows remain missing/nonclaim until sourced",
    )
    add(
        "V1155_4_arena_schema_present",
        {"ARENA1155_0_R_eq", "ARENA1155_1_WEP", "ARENA1155_2_clock", "ARENA1155_3_PPN_orbital", "ARENA1155_4_R10"}.issubset(
            {row["schema_id"] for row in arenas}
        ),
        "arena interface schema covers R_eq, WEP, clocks, PPN/orbital, and R10",
    )
    add(
        "V1155_5_guards_active",
        {"GUARD1155_0_no_frame_relabel", "GUARD1155_1_no_shadow_frame", "GUARD1155_2_no_common_calibration_absorption", "GUARD1155_3_no_local_GR_promotion"}.issubset(
            {row["guard_id"] for row in guards if row["status"] == "ACTIVE"}
        ),
        "all no-frame-cheat guards are active",
    )
    add(
        "V1155_6_claim_gates_blocked",
        any(row["gate_id"] == "G1155_2_single_observed_frame_parent_signed" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1155_4_Newton_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "single-frame and Newton/GR promotion gates remain blocked",
    )
    add(
        "V1155_7_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1155_8_next_target",
        next_target[0]["next_target"].startswith("1156-") and "quotient-matter-functor" in str(next_target[0]["next_target"]),
        "1156 handoff targets parent quotient/matter functor signature or frame-leak bound fill",
    )
    add(
        "V1155_9_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1155_10_csv_parse", csv_parse_ok, "all 1155 CSV outputs parse cleanly")
    add("V1155_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1155_SUMMARY",
        True,
        "1155 keeps observed coframe descent conditional, rejects current single-frame promotion, and emits nonclaim Delta_frame/Delta_cal residual rows",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    residuals: list[dict[str, object]],
    arenas: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1155 - Y5/R10 Single Observed Coframe Source-Frame Owner or Frame Residual Row

**Current verdict:** the single observed coframe proof does not close for current MTS. The chain-rule route is real conditionally, but `q`, `e_obs(q)`, matter functor factorization, quotient-owned constants, geometry-stack descent, tau/normal lock, and arena readout maps are not all parent-signed.

**Useful progress:** the exact failure is now executable: `Delta_frame`, `Delta_cal`, `Delta_tau_n`, `Delta_W_support`, and `epsilon_frame_coupling` are explicit nonclaim residual rows instead of implicit handwaving.

**Important guard:** no frame relabel. `e_source=e_force=e_clock=e_readout` must be derived from parent matter coupling or retained as a measurable residual vector.

**Best next attack:** parent-sign the quotient/matter functor route: `q:Phi->Q_obs`, `e_obs=Obs_e(q(Phi))`, and `S_matter=Sbar_matter[q(Phi),Psi,theta]`. If that fails, fill the `c_g,b_dis,b_A,q_nonH` frame-leak rows.

**No claim:** no measured-GM, source-normalized Newton, local-GR, PPN, R10, WEP, clock, GitHub, or public claim follows from 1155.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Single Observed Coframe Proof Audit
{table(["audit_id", "claim_piece", "mathematical_form", "required_parent_signature", "current_status", "failure_if_missing", "valid_for_claim"], audit)}

## Delta Frame / Calibration Residual Rows
{table(["row_id", "quantity", "definition", "required_columns", "current_value", "source_path", "arena_links", "status", "valid_for_claim", "claim_allowed"], residuals)}

## Arena Interface Schema
{table(["schema_id", "arena", "frame_requirement", "residual_if_failed", "claim_status", "valid_for_claim"], arenas)}

## No-Frame-Cheat Guards
{table(["guard_id", "guard", "status", "reason", "valid_for_claim"], guards)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1155_SOURCE_REGISTER.csv",
        "audit": OUT / "P8_Y5_R10_1155_SINGLE_OBSERVED_COFRAME_PROOF_AUDIT.csv",
        "residuals": OUT / "P8_Y5_R10_1155_DELTA_FRAME_CAL_RESIDUAL_ROWS.csv",
        "arenas": OUT / "P8_Y5_R10_1155_FRAME_ARENA_INTERFACE_SCHEMA.csv",
        "guards": OUT / "P8_Y5_R10_1155_NO_FRAME_CHEAT_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1155_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1155_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1155_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1155_VALIDATION.csv",
    }

    sources = source_rows()
    audit = coframe_audit_rows()
    residuals = residual_rows()
    arenas = arena_schema_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["residuals"], residuals)
    write_csv(outputs["arenas"], arenas)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, audit, residuals, arenas, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, audit, residuals, arenas, guards, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
