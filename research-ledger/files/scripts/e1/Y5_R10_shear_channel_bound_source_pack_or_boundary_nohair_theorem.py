from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_shear_channel_nohair_attempt_failed_metric_shear_bound_source_pack_written_nonclaim"
CLAIM_CEILING = "boundary_nohair_attempt_and_metric_shear_bound_pack_only_no_sigma_zero_no_epsilon_tau_no_MH_ref_no_Qbar_no_R10_no_PPN_no_local_GR_claim"
NEXT_TARGET = "692-Y5-R10-metric-shear-bound-runner-from-PPN-slip-source-lock.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "691-Y5-R10-shear-channel-bound-source-pack-or-boundary-nohair-theorem.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "232_doc": ROOT / "232-parent-Pmem-projector-or-source-identity-variation.md",
    "233_doc": ROOT / "233-boundary-symplectic-metric-or-local-EH-operator.md",
    "234_doc": ROOT / "234-boundary-metric-variation-and-Bianchi-ledger.md",
    "235_doc": ROOT / "235-projector-stress-variation-or-nohair-constraint-algebra.md",
    "247_doc": ROOT / "247-local-EH-exterior-sufficiency-stack-no-promotion.md",
    "347_doc": ROOT / "347-local-GR-parent-reduction-theorem-attempt.md",
    "352_doc": ROOT / "352-boundary-nohair-and-PPN-residual-vector-gate.md",
    "353_doc": ROOT / "353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md",
    "354_doc": ROOT / "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
    "357_doc": ROOT / "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
    "549_doc": ROOT / "549-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill.md",
    "678_doc": ROOT / "678-Y5-R10-boundary-class-nohair-projector-silence-or-BX-source-row.md",
    "690_doc": ROOT / "690-Y5-R10-trace-shear-first-component-zero-theorem-or-source-bound-fill.md",
    "549_validation": RESIDUALS / "P8_Y5_BRR545_549_VALIDATION.csv",
    "655_eh_audit": RESIDUALS / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
    "655_validation": RESIDUALS / "P8_Y5_BRR545_655_VALIDATION.csv",
    "678_validation": RESIDUALS / "P8_Y5_BRR545_678_VALIDATION.csv",
    "678_silence_stack": RESIDUALS / "P8_Y5_R10_678_SILENCE_STACK_AUDIT.csv",
    "689_validation": RESIDUALS / "P8_Y5_BRR545_689_VALIDATION.csv",
    "690_validation": RESIDUALS / "P8_Y5_BRR545_690_VALIDATION.csv",
    "690_shear_audit": RESIDUALS / "P8_Y5_R10_690_SHEAR_ZERO_THEOREM_AUDIT.csv",
    "690_bound_template": RESIDUALS / "P8_Y5_R10_690_TRACE_SHEAR_SOURCE_BOUND_TEMPLATE.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate_path.is_file()
        and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "232_doc": "P_mem decomposition names Pi_TF as trace-free/tangential shear projector",
        "233_doc": "boundary symplectic/metric ledger links trace-free shell tensor to anisotropic shear/slip",
        "234_doc": "Bianchi ledger requires Pi_TF sector to vanish or be carried explicitly",
        "235_doc": "projector stress/nohair constraint algebra leaves Pi_TF zero conditional",
        "247_doc": "EH exterior sufficiency stack keeps trace-free shear zero under conditional N2",
        "347_doc": "local GR reduction maps trace-free residual to gamma/slip and keeps N2 conditional",
        "352_doc": "boundary no-hair and symbolic PPN vector; B_TF remains open",
        "353_doc": "boundary no-hair contract A1-A7 attempted but A3-A7 unsigned",
        "354_doc": "source-locked PPN scales and no-hair debts sharpened",
        "357_doc": "Ward-owned nohair map and retained PPN residual vector",
        "549_doc": "boundary cohomology/nohair certificate failure and boundary flux bound row",
        "678_doc": "boundary-class/nohair/projector silence stack not derived",
        "690_doc": "immediate trace/shear split predecessor",
        "549_validation": "549 validation gate",
        "655_eh_audit": "EH-only premise audit",
        "655_validation": "655 validation gate",
        "678_validation": "678 validation gate",
        "678_silence_stack": "678 silence-stack audit rows",
        "689_validation": "689 validation gate",
        "690_validation": "690 validation gate",
        "690_shear_audit": "690 shear zero-theorem audit",
        "690_bound_template": "690 trace/shear source-bound template",
        "boundary_reference_status": "M_H_ref denominator status",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def boundary_nohair_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "audit_id": "NH691_0_target",
            "theorem_clause": "physical metric shear target",
            "mathematical_form": "sigma_mu_nu=0 or equivalently no observed trace-free/tangential boundary stress feeding local metric slip",
            "current_status": "target_defined",
            "blocker": "target definition is not a parent theorem",
            "if_passes": "B_shear_metric can be theorem-zero and metric shear drops from epsilon_tau numerator",
            "fallback_row": "SB691_0_sigma_metric",
            "valid_for_claim": "false",
            "source_paths": source_list("690_doc", "690_shear_audit"),
            "generated_utc": now,
        },
        {
            "audit_id": "NH691_1_class_only_boundary_action",
            "theorem_clause": "boundary action is class-only and marker-free",
            "mathematical_form": "S_boundary=S_boundary(total relative class,total charge,induced scalar volume) with no angular representatives",
            "current_status": "conditional_lemma_not_parent_signed",
            "blocker": "353/354 state the right condition but do not derive it from the parent action",
            "if_passes": "trace-free shell stress has no allowed source in the boundary action",
            "fallback_row": "SB691_1_B_TF_boundary",
            "valid_for_claim": "false",
            "source_paths": source_list("353_doc", "354_doc", "678_silence_stack"),
            "generated_utc": now,
        },
        {
            "audit_id": "NH691_2_relative_boundary_class",
            "theorem_clause": "relative boundary class is trivial or parent-selected",
            "mathematical_form": "[B_edge]_{H_rel}=0 before local readout, with proper charge/reference guard",
            "current_status": "not_signed",
            "blocker": "549/678 leave relative class selection as a contract rather than a parent result",
            "if_passes": "exact boundary/improvement terms cannot carry linked trace-free local hair",
            "fallback_row": "SB691_1_B_TF_boundary",
            "valid_for_claim": "false",
            "source_paths": source_list("549_doc", "678_doc", "678_silence_stack"),
            "generated_utc": now,
        },
        {
            "audit_id": "NH691_3_projector_TF_stress",
            "theorem_clause": "projector variation creates no trace-free local stress",
            "mathematical_form": "delta Pi_TF either vanishes, is pure gauge/topological, or is retained in a conserved explicit stress row",
            "current_status": "not_derived",
            "blocker": "232-235 name Pi_TF/projector stress but do not prove it harmless",
            "if_passes": "projector stress cannot source gamma/lensing slip through the shear channel",
            "fallback_row": "SB691_2_Pi_TF_projector",
            "valid_for_claim": "false",
            "source_paths": source_list("232_doc", "233_doc", "234_doc", "235_doc"),
            "generated_utc": now,
        },
        {
            "audit_id": "NH691_4_no_vector_tensor_marker_hair",
            "theorem_clause": "no physical boundary markers or preferred tangential frames",
            "mathematical_form": "Pi_vector=Pi_TF=Pi_shear=Pi_radial=Pi_time=0 on allowed compact local shell",
            "current_status": "not_derived",
            "blocker": "marker-free/no-vector/no-tensor hair is stated as a needed clause, not proved",
            "if_passes": "preferred-frame, anisotropy, and shear residuals are forbidden by parent symmetry",
            "fallback_row": "SB691_3_TF_to_PPN_coefficients",
            "valid_for_claim": "false",
            "source_paths": source_list("353_doc", "354_doc", "357_doc", "678_doc"),
            "generated_utc": now,
        },
        {
            "audit_id": "NH691_5_Ward_Bianchi_flux_closure",
            "theorem_clause": "boundary Ward/Bianchi flux closure",
            "mathematical_form": "F_boundary^nu is zero, conserved monopole only, or exactly balanced by owned boundary charge",
            "current_status": "conditional_open",
            "blocker": "Ward maps exist, but signs/couplings and local boundary flux equations are not parent-derived",
            "if_passes": "no shear/vector momentum leaks into local exterior field equations",
            "fallback_row": "SB691_4_boundary_flux_profile",
            "valid_for_claim": "false",
            "source_paths": source_list("234_doc", "352_doc", "357_doc", "549_doc"),
            "generated_utc": now,
        },
        {
            "audit_id": "NH691_6_EH_metric_only_exterior",
            "theorem_clause": "EH-only metric exterior selection",
            "mathematical_form": "extra sectors absent/gauge/topological/no-haired and surviving exterior equations are metric-only EH through PPN order",
            "current_status": "blocked",
            "blocker": "247/347/655 keep EH-only route conditional or failed for claim",
            "if_passes": "local GR handles shear/PPN in the normal GR way",
            "fallback_row": "SB691_5_EH_R11_shear_family",
            "valid_for_claim": "false",
            "source_paths": source_list("247_doc", "347_doc", "655_eh_audit"),
            "generated_utc": now,
        },
        {
            "audit_id": "NH691_7_denominator_charge_guard",
            "theorem_clause": "proper charge and same-frame denominator guard",
            "mathematical_form": "boundary exactness does not subtract physical ADM/H_tau/source mass; M_H_ref or same-frame denominator is fixed",
            "current_status": "blocked",
            "blocker": "M_H_ref/source-normalization/reference branch remains unclosed",
            "if_passes": "dimensionless shear residuals become meaningful",
            "fallback_row": "SB691_6_same_frame_denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("678_doc", "boundary_reference_status", "690_bound_template"),
            "generated_utc": now,
        },
        {
            "audit_id": "NH691_8_verdict",
            "theorem_clause": "boundary no-hair proves physical metric shear zero",
            "mathematical_form": "NH691_1 through NH691_7 all parent-signed",
            "current_status": "fail_current_corpus",
            "blocker": "class-only action, relative class, projector TF stress, Ward flux, EH exterior, and denominator are not jointly signed",
            "if_passes": "local metric shear branch can be removed from R10/PPN/clock/orbital residuals",
            "fallback_row": "SB691_source_pack_required",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "353_doc", "549_doc", "678_doc", "690_bound_template"),
            "generated_utc": now,
        },
    ]


def shear_bound_source_pack_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "SB691_0_sigma_metric",
            "sigma_mu_nu",
            "B_shear_metric",
            "metric shear norm bound or theorem-zero certificate",
            "MISSING_METRIC_SHEAR_SOURCE_BOUND",
            "physical metric residual; cannot be filled by P_coh/J_C projector silence",
            "690_shear_audit;690_bound_template",
        ),
        (
            "SB691_1_B_TF_boundary",
            "trace_free_boundary_stress",
            "B_TF_over_MH",
            "trace-free boundary stress amplitude divided by same-frame mass scale",
            "MISSING_B_TF_OVER_MH_VALUE_OR_THEOREM_ZERO",
            "feeds gamma/lensing slip and anisotropic local potentials",
            "352_doc;353_doc;354_doc",
        ),
        (
            "SB691_2_Pi_TF_projector",
            "projector_trace_free_stress",
            "T_projector_TF_over_MH",
            "projector variation trace-free stress coefficient or topological silence theorem",
            "MISSING_PROJECTOR_TF_STRESS_COEFFICIENT",
            "prevents hidden projector stress from masquerading as no-hair",
            "232_doc;233_doc;234_doc;235_doc",
        ),
        (
            "SB691_3_TF_to_PPN_coefficients",
            "observable_conversion",
            "C_gamma_TF;C_slip_TF;C_xi_TF",
            "linearized map from shear/boundary TF residual to gamma, lensing slip, and l>=2 anisotropy",
            "MISSING_TF_TO_PPN_COEFFICIENTS",
            "needed before comparing with source-locked PPN guardrails",
            "352_doc;354_doc;357_doc;347_doc",
        ),
        (
            "SB691_4_boundary_flux_profile",
            "boundary_flux_profile",
            "partial_t_B_TF;partial_r_B_TF;frame_profile",
            "time/radial/frame profile or theorem-zero derivative silence",
            "MISSING_SHEAR_BOUNDARY_PROFILE",
            "prevents Gdot, beta, radial-source, and preferred-frame leakage",
            "357_doc;549_doc;678_doc",
        ),
        (
            "SB691_5_EH_R11_shear_family",
            "EH_or_R11_operator_family",
            "R11_TF_or_EH_nohair_clause",
            "EH no-hair proof or retained R11 shear operator coefficients",
            "MISSING_EH_OR_R11_SHEAR_OPERATOR_ROW",
            "fallback if physical shear is not theorem-zero",
            "247_doc;347_doc;655_eh_audit",
        ),
        (
            "SB691_6_same_frame_denominator",
            "same_frame_denominator",
            "M_H_ref_or_M_ref_candidate",
            "claim-ready denominator with same frame/convention as shear numerator",
            "MISSING_CLAIM_READY_M_REF_CANDIDATE",
            "needed for dimensionless epsilon_TF/epsilon_tau",
            "boundary_reference_status;690_bound_template",
        ),
        (
            "SB691_7_no_shortcut_guard",
            "trace_projected_shear_nonimplication_guard",
            "logic_guard",
            "runner must reject projected-channel shear silence as physical metric shear zero",
            "SCHEMA_ONLY_NONCLAIM_TRACE_SHEAR_GUARD",
            "prevents false R10/PPN/local-GR promotion",
            "690_doc;690_shear_audit;690_bound_template",
        ),
    ]
    output_rows = []
    for row_id, residual, symbol, required, status, arena_role, source_ids_text in rows:
        source_ids = source_ids_text.split(";")
        output_rows.append(
            {
                "pack_id": row_id,
                "residual_component": residual,
                "bound_symbol": symbol,
                "required_evidence": required,
                "current_status": status,
                "arena_role": arena_role,
                "valid_for_claim": "false",
                "source_paths": source_list(*source_ids),
                "generated_utc": now,
            }
        )
    return output_rows


def observable_map_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "map_id": "OM691_0_gamma_slip",
            "observable_arena": "PPN_gamma_and_lensing_slip",
            "symbolic_map": "abs(gamma-1), abs(Phi-Psi) <= C_gamma_TF*epsilon_TF + other retained residuals",
            "needed_inputs": "B_TF_over_MH;C_gamma_TF;same_frame_denominator",
            "current_status": "blocked_missing_coefficients",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "354_doc", "357_doc"),
            "generated_utc": now,
        },
        {
            "map_id": "OM691_1_xi_anisotropy",
            "observable_arena": "preferred_location_l_ge_2_anisotropy",
            "symbolic_map": "abs(xi) <= C_xi_TF*epsilon_TF_lge2 + domain/external anisotropy rows",
            "needed_inputs": "l>=2 shear profile;C_xi_TF;domain anisotropy map",
            "current_status": "blocked_missing_l_ge_2_profile",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "357_doc", "678_doc"),
            "generated_utc": now,
        },
        {
            "map_id": "OM691_2_beta_radial",
            "observable_arena": "PPN_beta_and_radial_source_hair",
            "symbolic_map": "abs(beta-1) <= C_rad2*epsilon_rad + C_boundary_nl*epsilon_TF_profile + nonlinear retained rows",
            "needed_inputs": "radial/time shear-boundary profile;nonlinear coefficients",
            "current_status": "blocked_missing_profile_and_coefficients",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "357_doc", "549_doc"),
            "generated_utc": now,
        },
        {
            "map_id": "OM691_3_R10",
            "observable_arena": "R10_short_range_alpha_lambda",
            "symbolic_map": "alpha_TF(lambda) requires a range kernel and source-normalized TF operator coefficient",
            "needed_inputs": "lambda_TF;operator coefficient;source normalization;M_H_ref",
            "current_status": "blocked_no_range_kernel_or_operator_row",
            "valid_for_claim": "false",
            "source_paths": source_list("655_eh_audit", "690_bound_template"),
            "generated_utc": now,
        },
        {
            "map_id": "OM691_4_clock_orbit",
            "observable_arena": "clocks_orbital_systems",
            "symbolic_map": "clock/orbital residuals inherit metric shear only after tau/frame and same-metric map are fixed",
            "needed_inputs": "same tau/frame;metric residual map;source mass denominator",
            "current_status": "blocked_by_tau_frame_and_denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("690_doc", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "map_id": "OM691_5_local_GR",
            "observable_arena": "local_GR_reduction",
            "symbolic_map": "local GR follows only if shear/nohair, EH metric-only exterior, source normalization, and PPN completion close together",
            "needed_inputs": "NH691_1_to_NH691_7 all pass or retained residual runner beats bounds",
            "current_status": "blocked_no_local_GR_promotion",
            "valid_for_claim": "false",
            "source_paths": source_list("247_doc", "347_doc", "655_eh_audit", "690_doc"),
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "CG691_0_nohair_theorem",
            "gate": "boundary no-hair theorem",
            "required_state": "class-only boundary action, trivial relative class, no projector TF stress, Ward closure, EH exterior, and denominator all parent-signed",
            "observed_state": "multiple clauses conditional or failed for claim",
            "result": "fail_blocked",
            "claim_effect": "sigma_mu_nu cannot be theorem-zeroed",
            "valid_for_claim": "false",
            "source_paths": source_list("353_doc", "549_doc", "678_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG691_1_source_pack",
            "gate": "metric shear source pack",
            "required_state": "numeric/theorem rows with units, source paths, coefficients, profiles, and same-frame denominator",
            "observed_state": "pack written but every physical row is missing or schema-only",
            "result": "staged_nonclaim",
            "claim_effect": "future runner has exact inputs but no pass now",
            "valid_for_claim": "false",
            "source_paths": source_list("690_bound_template"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG691_2_observable_map",
            "gate": "PPN/R10/clock/orbit map",
            "required_state": "coefficients and range/profile maps exist",
            "observed_state": "observable equations are symbolic and missing coefficients",
            "result": "fail_blocked",
            "claim_effect": "no PPN, R10, clock, orbital, or local-GR evidence",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "357_doc", "655_eh_audit"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG691_3_denominator",
            "gate": "same-frame denominator",
            "required_state": "M_H_ref or same-frame denominator valid for shear numerator",
            "observed_state": "boundary/reference status remains unclaimable",
            "result": "fail_blocked",
            "claim_effect": "epsilon_TF and epsilon_tau remain nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG691_4_no_shortcut",
            "gate": "projected shear shortcut guard",
            "required_state": "projected-channel silence never promoted to metric shear zero",
            "observed_state": "guard retained from 690 and restated in SB691_7",
            "result": "pass_guard_only",
            "claim_effect": "prevents false local-GR promotion",
            "valid_for_claim": "false",
            "source_paths": source_list("690_doc", "690_shear_audit"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG691_5_next",
            "gate": "next target selection",
            "required_state": "choose executable follow-up after nohair failure",
            "observed_state": NEXT_TARGET,
            "result": "selected",
            "claim_effect": "build metric-shear bound runner from source-locked PPN/slip guardrails",
            "valid_for_claim": "false",
            "source_paths": source_list("354_doc", "357_doc"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D691_0_nohair",
            "target": "boundary no-hair theorem",
            "result": "attempted_failed_current_corpus",
            "reason": "conditional no-hair route is structurally clean, but class-only boundary action, relative class, projector stress, Ward closure, EH exterior, and denominator are not jointly signed",
            "next_action": "do not claim sigma_mu_nu=0",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D691_1_source_pack",
            "target": "metric shear bound source pack",
            "result": "written_nonclaim",
            "reason": "the exact rows needed to bound physical metric shear are now separated from projected-channel silence",
            "next_action": "fill coefficients/profiles/denominator or theorem-zero rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D691_2_next",
            "target": "metric shear bound runner",
            "result": "selected",
            "reason": "after no-hair fails, the least handwavy route is a source-locked PPN/slip runner for the shear residual",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S691_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "boundary no-hair theorem is a clean sufficient route but fails for current corpus; metric shear bound source pack is written",
            "hardest_blocker": "no parent-signed class-only boundary action plus projector-TF stress silence plus same-frame denominator",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def all_valid_for_claim_false(rows_by_name: dict[str, list[dict[str, str]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("valid_for_claim") == "true":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, str]],
    nohair_rows: list[dict[str, str]],
    pack_rows: list[dict[str, str]],
    observable_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "nohair": nohair_rows,
        "pack": pack_rows,
        "observable": observable_rows,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["549_validation", "655_validation", "678_validation", "689_validation", "690_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    nohair_complete = len(nohair_rows) == 9 and all(row["valid_for_claim"] == "false" for row in nohair_rows)
    nohair_not_promoted = not any(row["current_status"] in {"proved", "pass", "theorem_zero"} for row in nohair_rows)
    pack_complete = len(pack_rows) == 8 and all(row["valid_for_claim"] == "false" for row in pack_rows)
    missing_or_schema_retained = all(
        "MISSING_" in row["current_status"] or row["current_status"].startswith("SCHEMA_ONLY") for row in pack_rows
    )
    observable_complete = len(observable_rows) == 6 and all(row["valid_for_claim"] == "false" for row in observable_rows)
    projected_guard = any(row["pack_id"] == "SB691_7_no_shortcut_guard" for row in pack_rows) and any(
        row["gate_id"] == "CG691_4_no_shortcut" and row["result"] == "pass_guard_only" for row in gate_rows
    )
    gates_block = all(row["valid_for_claim"] == "false" for row in gate_rows) and any(row["result"].startswith("fail") for row in gate_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_) and any(
        row["next_target"] == NEXT_TARGET for row in summary_rows
    )
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_691_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_691_BOUNDARY_NOHAIR_THEOREM_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_691_SHEAR_CHANNEL_BOUND_SOURCE_PACK.csv",
        RESIDUALS / "P8_Y5_R10_691_OBSERVABLE_MAP.csv",
        RESIDUALS / "P8_Y5_R10_691_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_691_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_691_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_691_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V691_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V691_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{key}={value}" for key, value in prior_failure_counts.items())),
        ("V691_2_nohair_audit_complete", nohair_complete, f"nohair_rows={len(nohair_rows)}"),
        ("V691_3_nohair_not_promoted", nohair_not_promoted, "no theorem-zero or pass status assigned to boundary no-hair"),
        ("V691_4_shear_source_pack_complete", pack_complete, f"pack_rows={len(pack_rows)}"),
        ("V691_5_missing_markers_retained", missing_or_schema_retained, "pack rows retain MISSING or SCHEMA_ONLY status"),
        ("V691_6_observable_map_complete", observable_complete, f"observable_rows={len(observable_rows)}"),
        ("V691_7_projected_shear_guard_retained", projected_guard, "SB691_7 and CG691_4 prevent projected-channel shortcut"),
        ("V691_8_claim_gates_block", gates_block, "claim gates block nohair/sourcepack/observable/denominator/local promotion"),
        ("V691_9_no_claim_rows_promoted", no_claim_rows, "all generated 691 rows remain valid_for_claim=false"),
        ("V691_10_next_target_selected", next_selected, NEXT_TARGET),
        ("V691_11_generated_outputs_scoped", scoped_outputs, "all 691 outputs target post-checkpoint-work"),
        ("V691_12_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V691_13_status_nonclaim", "no_sigma_zero" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now,
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(
    source_rows: list[dict[str, str]],
    nohair_rows: list[dict[str, str]],
    pack_rows: list[dict[str, str]],
    observable_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 691 - Y5 R10 Shear Channel Bound Source Pack Or Boundary Nohair Theorem

## Verdict

691 tries the cleanest derivation route for physical metric shear:

```text
boundary no-hair + projector trace-free silence + Ward closure
=> sigma_mu_nu = 0
```

The route is mathematically sensible, but it is not signed by the current parent corpus. The blocker is not one vague missing miracle. It is a specific stack: class-only boundary action, parent-selected relative class, no projector trace-free stress, marker-free/no-vector/no-tensor boundary data, Ward/Bianchi flux closure, metric-only EH exterior, and a same-frame denominator.

So 691 does not claim `sigma_mu_nu=0`. It writes the metric-shear source pack that a future runner must fill if the no-hair theorem is not derived.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Boundary Nohair Theorem Audit

{markdown_table(nohair_rows, ["audit_id", "theorem_clause", "current_status", "blocker", "fallback_row", "valid_for_claim"])}

## Shear Channel Bound Source Pack

{markdown_table(pack_rows, ["pack_id", "residual_component", "bound_symbol", "required_evidence", "current_status", "arena_role", "valid_for_claim"])}

## Observable Map

{markdown_table(observable_rows, ["map_id", "observable_arena", "symbolic_map", "needed_inputs", "current_status", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows_, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    nohair_rows = boundary_nohair_audit_rows()
    pack_rows = shear_bound_source_pack_rows()
    observable_rows = observable_map_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(source_rows, nohair_rows, pack_rows, observable_rows, gate_rows, decision_rows_, summary_rows)

    write_csv(RESIDUALS / "P8_Y5_R10_691_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_691_BOUNDARY_NOHAIR_THEOREM_AUDIT.csv", nohair_rows, ["audit_id", "theorem_clause", "mathematical_form", "current_status", "blocker", "if_passes", "fallback_row", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_691_SHEAR_CHANNEL_BOUND_SOURCE_PACK.csv", pack_rows, ["pack_id", "residual_component", "bound_symbol", "required_evidence", "current_status", "arena_role", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_691_OBSERVABLE_MAP.csv", observable_rows, ["map_id", "observable_arena", "symbolic_map", "needed_inputs", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_691_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_691_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_691_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_691_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_rows, nohair_rows, pack_rows, observable_rows, gate_rows, decision_rows_, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"nohair_rows={len(nohair_rows)}")
    print(f"pack_rows={len(pack_rows)}")
    print(f"observable_rows={len(observable_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
