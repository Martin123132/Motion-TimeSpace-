from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "993-Y5-R10-parent-Lagrangian-current-extraction-theta-Qtau-or-deltaH-curl-input.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "992_doc",
            "path": "992-Y5-R10-Hamiltonian-PiM-source-current-descent-or-FB5540-component-bound-pack.md",
            "role": "immediate handoff selecting parent Lagrangian current extraction",
            "needle": "DEC992_2_next_target",
        },
        {
            "source_id": "992_theorem",
            "path": "source-intake/mts_residuals/P8_Y5_R10_992_SOURCE_CURRENT_DESCENT_THEOREM_GATE.csv",
            "role": "source-current descent gate requiring parent current first",
            "needle": "SCD992_0_parent_action_current",
        },
        {
            "source_id": "770_parent_certificate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_770_PARENT_ACTION_CERTIFICATE_AUDIT.csv",
            "role": "parent action certificate audit",
            "needle": "HIC770_1_variation_owner",
        },
        {
            "source_id": "771_theta_Qtau",
            "path": "source-intake/mts_residuals/P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
            "role": "theta/Q_tau current owner audit",
            "needle": "TQ771_1_Noether_current",
        },
        {
            "source_id": "772_hybrid_current",
            "path": "source-intake/mts_residuals/P8_Y5_R10_772_HYBRID_CURRENT_OWNER_AUDIT.csv",
            "role": "hybrid EH plus quotient current owner status",
            "needle": "HCO772_0_observed_EH_current",
        },
        {
            "source_id": "p8_parent_terms",
            "path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "role": "parent action term inventory",
            "needle": "A0_total_covariant_parent",
        },
        {
            "source_id": "p8_min_local_GR_blocks",
            "path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "role": "minimal local-GR action blocks",
            "needle": "A511_0_EH_core",
        },
        {
            "source_id": "p8_symbol_map",
            "path": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            "role": "MTS symbol to local GR action-block map",
            "needle": "Pi_M",
        },
        {
            "source_id": "p8_noether_chain",
            "path": "source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
            "role": "parent Noether closure chain",
            "needle": "D505_0_local_parent_action_form",
        },
        {
            "source_id": "p8_worldtube_noether",
            "path": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_NOETHER_CHAIN.csv",
            "role": "worldtube Noether chain",
            "needle": "N504_0_variation",
        },
        {
            "source_id": "brr545_parent_zero",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_PARENT_ACTION_ZERO_THEOREM_CONTRACT.csv",
            "role": "BRR545 parent-action zero theorem contract",
            "needle": "BZTC552_0_covariant_phase_space_parent",
        },
        {
            "source_id": "boundary_reference_contract",
            "path": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
            "role": "boundary/reference minimal action contract",
            "needle": "MAC545_0_covariant_parent_action",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                "source_id": spec["source_id"],
                "role": spec["role"],
                "path": spec["path"],
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "needle": spec["needle"],
                "valid_for_claim": "false",
            }
        )
    return rows


def current_extraction_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CEG993_0_action_inventory",
            "gate": "one parent Lagrangian inventory exists",
            "required_form": "L_parent = L_EH + L_kappa/top + L_matter + L_extra + L_selector + L_boundary + L_readout/source",
            "current_result": "structural_inventory_exists",
            "why_not_enough": "inventory is not a full variational current extraction",
            "next_requirement": "sector-by-sector theta_s, Q_tau_s, C_tau_s, and boundary terms",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CEG993_1_variation_owner",
            "gate": "delta L_parent=E_A delta Phi^A+dtheta_total",
            "required_form": "theta_total=sum_s theta_s with all hidden/projector/domain/boundary/source variables varied before readout",
            "current_result": "not_extracted",
            "why_not_enough": "770/771 say explicit L_X, coupling owner, and boundary/reference terms are missing",
            "next_requirement": "write or source every theta_s term",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CEG993_2_Noether_charge",
            "gate": "J_tau=theta_total(L_tau Phi)-i_tau L_parent=dQ_tau+C_tau",
            "required_form": "Q_tau^MTS=sum_s Q_tau_s plus named constraints C_tau_s",
            "current_result": "formal_shape_only",
            "why_not_enough": "EH part is a reference, but extra/projector/boundary/source pieces are not extracted",
            "next_requirement": "decompose Q_tau and C_tau sector by sector",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CEG993_3_deltaH_curl",
            "gate": "deltaH curl evaluable",
            "required_form": "curl(delta H_tau)=int_S i_tau omega_total + delta_tau + delta_surface + delta_ref terms",
            "current_result": "not_evaluable",
            "why_not_enough": "omega_total requires theta_total and boundary/reference/tau ownership first",
            "next_requirement": "stage deltaH curl input schema if extraction fails",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CEG993_4_verdict",
            "gate": "accept parent current owner",
            "required_form": "CEG993_0 through CEG993_3 pass with source paths and no placeholders",
            "current_result": "not_promoted",
            "why_not_enough": "only the EH baseline current is conditionally available",
            "next_requirement": "use EH baseline as comparator and residualize every non-EH/current piece",
            "valid_for_claim": "false",
        },
    ]


def sector_extraction_rows() -> list[dict[str, str]]:
    return [
        {
            "sector_id": "SEC993_0_EH_core",
            "candidate_L_term": "(16*pi*G_ref)^-1 (R[g_obs]-2Lambda0) epsilon",
            "theta_status": "standard_EH_reference_available",
            "Qtau_status": "standard_EH_Qtau_reference_available",
            "constraint_status": "EH_constraint_reference_available",
            "extraction_result": "conditional_baseline_only",
            "missing_for_MTS_claim": "EH-only operator selection, fixed boundary/reference, same tau, and extra-sector silence",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "SEC993_1_kappa_topological",
            "candidate_L_term": "kappa_eff dA_3 or equivalent global coupling lock",
            "theta_status": "formal_boundary_variation_possible",
            "Qtau_status": "not_mass_charge_without_glue",
            "constraint_status": "d kappa_eff=0 conditional",
            "extraction_result": "coupling_constant_lock_only",
            "missing_for_MTS_claim": "proof it fixes G_ref for source charge and carries no local boundary mass flux",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "SEC993_2_universal_matter",
            "candidate_L_term": "L_matter[psi,g_obs] with species-blind observed coframe",
            "theta_status": "conditional_standard_matter_theta",
            "Qtau_status": "enters constraints/Hilbert current, not standalone exterior charge",
            "constraint_status": "Hilbert current conditional on parent matter functor",
            "extraction_result": "source_current_reference_only",
            "missing_for_MTS_claim": "parent-signed matter functor, no hidden source/readout map, charge/current descent",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "SEC993_3_extra_motion_time_memory",
            "candidate_L_term": "L_extra[g_obs,Phi]=sqrt(-g)(-1/2 G_AB grad Phi^A grad Phi^B - V(Phi)+C(Phi)R+...)",
            "theta_status": "not_extracted_current_MTS",
            "Qtau_status": "not_extracted_current_MTS",
            "constraint_status": "positive/no-source silence not signed",
            "extraction_result": "blocked",
            "missing_for_MTS_claim": "explicit fields, kinetic matrix, potential, signs, source laws, and boundary conditions",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "SEC993_4_domain_projector_selector",
            "candidate_L_term": "L_selector[u,h,X,Qcoh,chi_D] as constraint/topological/positive sector",
            "theta_status": "not_extracted_current_MTS",
            "Qtau_status": "not_extracted_current_MTS",
            "constraint_status": "projector/domain commutators retained",
            "extraction_result": "blocked",
            "missing_for_MTS_claim": "parent-owned Pi_M/P_loc algebra, covariant constancy, domain/homology policy",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "SEC993_5_boundary_reference",
            "candidate_L_term": "L_boundary = L_GHY + exact/topological B_ref and boundary class terms",
            "theta_status": "not_fixed_beyond_EH_reference",
            "Qtau_status": "reference/boundary charge not fixed",
            "constraint_status": "boundary no-flux and reference lock fail current corpus",
            "extraction_result": "blocked",
            "missing_for_MTS_claim": "fixed B_ref, relative cohomology/nohair theorem, no vector/tensor/radial boundary flux",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "SEC993_6_metric_readout_PiM",
            "candidate_L_term": "g_readout=g_obs+O((Phi-Phi0)^2), Pi_M=Pi_EH+O((Phi-Phi0)^2)",
            "theta_status": "readout_not_action_variation",
            "Qtau_status": "Pi_M^H repair candidate only",
            "constraint_status": "delta Pi_M and [d,Pi_M]J_H not zero",
            "extraction_result": "blocked",
            "missing_for_MTS_claim": "Hamiltonian mass projector equality to Hilbert/source current",
            "valid_for_claim": "false",
        },
        {
            "sector_id": "SEC993_7_EM_charge_coupling",
            "candidate_L_term": "L_EM and source/readout charge sector",
            "theta_status": "not_part_of_mass_current_extraction_yet",
            "Qtau_status": "charge normalization not tied to Hamiltonian mass",
            "constraint_status": "EM-lock/no-alpha/source normalization unsigned",
            "extraction_result": "coupling_guard_only",
            "missing_for_MTS_claim": "prevents hidden WEP/clock/EM leakage but does not derive Newton source charge",
            "valid_for_claim": "false",
        },
    ]


def qtau_decomposition_rows() -> list[dict[str, str]]:
    return [
        {
            "piece_id": "QDEC993_0_EH",
            "Q_piece": "Q_tau^EH[g_obs,tau]",
            "status": "conditional_GR_reference",
            "role": "baseline Hamiltonian charge shape",
            "not_enough_because": "does not include MTS extra, projector, boundary/reference, or coupling sectors",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QDEC993_1_boundary_reference",
            "Q_piece": "Q_tau^boundary + delta B_ref",
            "status": "not_parent_fixed",
            "role": "finite charge and reference subtraction",
            "not_enough_because": "reference can absorb source normalization unless fixed before readout",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QDEC993_2_extra",
            "Q_piece": "Q_tau^extra + C_extra",
            "status": "not_extracted",
            "role": "motion/time/domain/memory/range charge leakage",
            "not_enough_because": "extra-sector theta/Q and no-source operators are missing",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QDEC993_3_projector",
            "Q_piece": "Q_tau^projector + C_projector + [d,Pi_M]J_H",
            "status": "not_extracted",
            "role": "mass projector/source-current channel",
            "not_enough_because": "Pi_M chain map and variation terms remain retained residuals",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QDEC993_4_matter_source",
            "Q_piece": "C_tau^matter[J_H] and worldtube source glue",
            "status": "conditional_not_glued",
            "role": "links charge to observed source mass",
            "not_enough_because": "Hilbert current equality and worldtube denominator glue are downstream and unsigned",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QDEC993_5_total",
            "Q_piece": "Q_tau^MTS=sum pieces above",
            "status": "not_promoted",
            "role": "candidate physical Hamiltonian mass charge",
            "not_enough_because": "only Q_EH is conditionally available; total Q_tau cannot be evaluated",
            "valid_for_claim": "false",
        },
    ]


def deltaH_curl_schema_rows() -> list[dict[str, str]]:
    base = "source-intake/mts_residuals"
    return [
        {
            "schema_id": "DHC993_0_sector_current_extraction",
            "target": "theta_s_and_Qtau_s_by_sector",
            "candidate_artifact": f"{base}/P8_Y5_R10_993_SECTOR_CURRENT_INPUT_CANDIDATE.csv",
            "required_columns": "sector;L_term;theta_term;Qtau_term;constraint_term;boundary_term;source_path;valid_for_claim",
            "current_status": "MISSING_SECTOR_CURRENT_EXTRACTION",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "DHC993_1_symplectic_current",
            "target": "omega_total(delta1,delta2)",
            "candidate_artifact": f"{base}/P8_Y5_R10_993_SYMPLECTIC_CURRENT_INPUT_CANDIDATE.csv",
            "required_columns": "sector;omega_term;boundary_pullback;tau_contraction;units;source_path;valid_for_claim",
            "current_status": "MISSING_OMEGA_TOTAL",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "DHC993_2_tau_surface_reference",
            "target": "delta_tau_delta_surface_delta_ref_terms",
            "candidate_artifact": f"{base}/P8_Y5_R10_993_TAU_SURFACE_REFERENCE_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;tau_owner;surface_class;B_ref_owner;delta_tau;delta_surface;delta_ref;source_path;valid_for_claim",
            "current_status": "MISSING_TAU_SURFACE_REFERENCE_LOCK",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "DHC993_3_deltaH_curl_value",
            "target": "curl(delta H_tau)/M_H_ref",
            "candidate_artifact": f"{base}/P8_Y5_R10_993_DELTAH_CURL_VALUE_INPUT_CANDIDATE.csv",
            "required_columns": "system_id;surface_id;curl_value;M_H_ref;units;zero_theorem_or_bound;source_path;valid_for_claim",
            "current_status": "MISSING_DELTAH_CURL_VALUE",
            "valid_for_claim": "false",
        },
    ]


def eh_credit_rows() -> list[dict[str, str]]:
    return [
        {
            "credit_id": "EHC993_0_EH_current_shape",
            "credit_allowed": "use standard EH covariant phase-space current as a reference baseline",
            "credit_forbidden": "claim total MTS Q_tau or Newton source equality from EH alone",
            "reason": "772 allowed EH current as baseline but explicitly left MTS extra/source/projector terms open",
            "valid_for_claim": "false",
        },
        {
            "credit_id": "EHC993_1_EH_weak_field",
            "credit_allowed": "use GR Poisson/Gauss relation as downstream comparator after source charge closes",
            "credit_forbidden": "substitute orbital GM or GR ADM mass for parent-owned MTS source mass",
            "reason": "992 rejects direct substitution and keeps Delta_cal residual",
            "valid_for_claim": "false",
        },
        {
            "credit_id": "EHC993_2_EH_boundary_terms",
            "credit_allowed": "use GHY/reference discipline as the shape of the boundary problem",
            "credit_forbidden": "declare MTS B_ref fixed unless parent branch selects it",
            "reason": "boundary reference contracts remain false for parent_owned_now",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG993_0_parent_current_owner",
            "claim": "theta_total and Q_tau^MTS are extracted from parent L",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "only an EH baseline is conditionally extractable; non-EH/projector/boundary/coupling sectors remain missing",
        },
        {
            "gate_id": "CG993_1_deltaH_curl",
            "claim": "deltaH curl is evaluated or zero",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "omega_total, tau/surface/reference locks, and M_H_ref are not all owned",
        },
        {
            "gate_id": "CG993_2_FB5540",
            "claim": "FB554_0=0 or Hamiltonian Pi_M source mass is derived",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "parent current extraction fails before source equality",
        },
        {
            "gate_id": "CG993_3_Newton_PPN_local_GR",
            "claim": "Newton, PPN, R10, R11, Gdot, orbit, or local-GR pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "these remain downstream of source charge and weak-field operator ownership",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC993_0_extraction_attempt",
            "decision": "do not accept full parent current extraction",
            "reason": "sector ledger shows only EH reference credit; total Q_tau^MTS is not constructed",
            "effect": "deltaH curl remains an input/theorem target, not a result",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC993_1_EH_baseline_policy",
            "decision": "keep EH current as comparator, not proof",
            "reason": "this gives the right GR/Newton target shape without smuggling GR into MTS",
            "effect": "future residual currents can be measured against EH baseline",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC993_2_next_target",
            "decision": "build EH-baseline plus residual-current pack next",
            "reason": "the most concrete progress is to separate Q_EH from every missing MTS current piece",
            "effect": "turn total-current fog into sector residual rows suitable for derivation or bounds",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "994-Y5-R10-EH-baseline-current-plus-MTS-residual-current-pack.md",
            "objective": "write the EH baseline current explicitly as comparator and build a sector residual-current pack for every non-EH/projector/boundary/source term",
            "include": "Q_EH baseline, theta_EH baseline, Q_residual sectors, C_extra/C_projector/C_boundary/C_ref rows, no-cancellation deltaH curl envelope",
            "exclude": "FB554_0 pass, Newton/PPN/R10/local-GR pass, orbital GM substitution, hidden EH import, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_timestamp:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    gate: list[dict[str, str]],
    sectors: list[dict[str, str]],
    qtau: list[dict[str, str]],
    schemas: list[dict[str, str]],
    eh_credit: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    gate_ok = all(row["valid_for_claim"] == "false" for row in gate) and gate[-1]["current_result"] == "not_promoted"
    sectors_ok = len(sectors) >= 8 and all(row["valid_for_claim"] == "false" for row in sectors) and any(row["sector_id"] == "SEC993_0_EH_core" for row in sectors)
    qtau_ok = any(row["piece_id"] == "QDEC993_5_total" and row["status"] == "not_promoted" for row in qtau)
    schema_ok = all(row["valid_for_claim"] == "false" and "MISSING" in row["current_status"] for row in schemas)
    eh_credit_ok = all(row["valid_for_claim"] == "false" and row["credit_forbidden"] for row in eh_credit)
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    decision_ok = any(row["decision_id"] == "DEC993_2_next_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V993_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all cited local source files exist and expected needles are found"},
        {"check_id": "V993_1_current_gate_nonclaim", "result": "pass" if gate_ok else "fail", "detail": "current extraction gate is written and not promoted"},
        {"check_id": "V993_2_sector_ledger_complete", "result": "pass" if sectors_ok else "fail", "detail": "sector ledger includes EH baseline and all MTS sectors as nonclaim"},
        {"check_id": "V993_3_Qtau_total_not_promoted", "result": "pass" if qtau_ok else "fail", "detail": "total Q_tau^MTS is not promoted"},
        {"check_id": "V993_4_deltaH_schema_fail_closed", "result": "pass" if schema_ok else "fail", "detail": "deltaH curl schemas remain MISSING and valid_for_claim=false"},
        {"check_id": "V993_5_EH_credit_limited", "result": "pass" if eh_credit_ok else "fail", "detail": "EH baseline credit is limited to comparator/reference use"},
        {"check_id": "V993_6_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "parent current, deltaH curl, FB5540, and local-GR claims are blocked"},
        {"check_id": "V993_7_next_decision", "result": "pass" if decision_ok else "fail", "detail": "994 EH-baseline residual-current pack is selected"},
        {"check_id": "V993_8_next_target_written", "result": "pass" if next_ok else "fail", "detail": "next target row is present and nonclaim"},
        {"check_id": "V993_9_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V993_READY",
            "result": "pass" if ready else "fail",
            "detail": "993 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    gate: list[dict[str, str]],
    sectors: list[dict[str, str]],
    qtau: list[dict[str, str]],
    schemas: list[dict[str, str]],
    eh_credit: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 993 Y5 R10: Parent Lagrangian Current Extraction, Theta/Q_tau, Or DeltaH Curl Input",
        "",
        "Status: `Y5_R10_993_parent_current_extraction_not_promoted_EH_baseline_credit_only_deltaH_curl_schema_staged_nonclaim`",
        "",
        "Claim ceiling: no parent-current owner, no `deltaH` curl zero/evaluation, no `FB554_0=0`, no Newton/PPN/R10/R11/Gdot/orbit/local-GR pass.",
        "",
        "## Readout",
        "",
        "993 goes to the source of the source: if MTS is going to reduce to GR/Newton honestly, `theta_total` and `Q_tau^MTS` have to come from a parent Lagrangian, not from a hand-named mass current.",
        "",
        "The extraction attempt does not close. The EH current can be used as a clean comparator, but the full MTS current is not extracted because the extra, projector/domain, boundary/reference, readout/Pi_M, and coupling sectors are not yet explicit variational objects. That is not a knockout against the programme; it is the guardrail that prevents an EH-looking shortcut from pretending to be a derivation.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Current Extraction Gate",
        "",
        md_table(gate, ["gate_id", "gate", "required_form", "current_result", "why_not_enough", "next_requirement", "valid_for_claim"]),
        "",
        "## Sector Current Extraction Ledger",
        "",
        md_table(sectors, ["sector_id", "candidate_L_term", "theta_status", "Qtau_status", "constraint_status", "extraction_result", "missing_for_MTS_claim", "valid_for_claim"]),
        "",
        "## Q_tau Decomposition Ledger",
        "",
        md_table(qtau, ["piece_id", "Q_piece", "status", "role", "not_enough_because", "valid_for_claim"]),
        "",
        "## DeltaH Curl Input Schema",
        "",
        md_table(schemas, ["schema_id", "target", "candidate_artifact", "required_columns", "current_status", "valid_for_claim"]),
        "",
        "## EH Baseline Credit Ledger",
        "",
        md_table(eh_credit, ["credit_id", "credit_allowed", "credit_forbidden", "reason", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    gate = current_extraction_gate_rows()
    sectors = sector_extraction_rows()
    qtau = qtau_decomposition_rows()
    schemas = deltaH_curl_schema_rows()
    eh_credit = eh_credit_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, gate, sectors, qtau, schemas, eh_credit, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_993_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_993_CURRENT_EXTRACTION_GATE.csv", gate)
    write_csv(OUT / "P8_Y5_R10_993_SECTOR_CURRENT_EXTRACTION_LEDGER.csv", sectors)
    write_csv(OUT / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv", qtau)
    write_csv(OUT / "P8_Y5_R10_993_DELTAH_CURL_INPUT_SCHEMA.csv", schemas)
    write_csv(OUT / "P8_Y5_R10_993_EH_BASELINE_CREDIT_LEDGER.csv", eh_credit)
    write_csv(OUT / "P8_Y5_R10_993_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_993_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_993_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_993_VALIDATION.csv", validation)
    write_doc(sources, gate, sectors, qtau, schemas, eh_credit, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
