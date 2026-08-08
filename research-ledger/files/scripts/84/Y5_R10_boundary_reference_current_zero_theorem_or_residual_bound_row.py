from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "995-Y5-R10-boundary-reference-current-zero-theorem-or-residual-bound-row.md"
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
            "source_id": "994_doc",
            "path": "994-Y5-R10-EH-baseline-current-plus-MTS-residual-current-pack.md",
            "role": "immediate handoff isolating RC994_0 boundary/reference current",
            "needle": "RC994_0_reference_boundary",
        },
        {
            "source_id": "994_residual_pack",
            "path": "source-intake/mts_residuals/P8_Y5_R10_994_MTS_RESIDUAL_CURRENT_PACK.csv",
            "role": "machine-readable residual-current pack",
            "needle": "RC994_0_reference_boundary",
        },
        {
            "source_id": "994_deltaH_envelope",
            "path": "source-intake/mts_residuals/P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv",
            "role": "no-cancellation envelope for deltaH curl",
            "needle": "DHE994_1_no_cancellation",
        },
        {
            "source_id": "545_doc",
            "path": "545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md",
            "role": "minimal action contract for boundary/reference zero route",
            "needle": "MAC545_2_reference_lock",
        },
        {
            "source_id": "545_minimal_contract",
            "path": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
            "role": "contract clauses for B_ref, cohomology, no-hair, projector silence, and M_H_ref",
            "needle": "MAC545_3_boundary_exact_cohomology_zero",
        },
        {
            "source_id": "545_parent_ownership",
            "path": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_PARENT_OWNERSHIP_AUDIT.csv",
            "role": "ownership audit proving 545 clauses are not parent-owned",
            "needle": "POA545_3_boundary",
        },
        {
            "source_id": "549_doc",
            "path": "549-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill.md",
            "role": "boundary cohomology/nohair certificate attempt",
            "needle": "BCT549_6_certificate_verdict",
        },
        {
            "source_id": "549_theorem_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv",
            "role": "machine-readable boundary cohomology/nohair theorem attempt",
            "needle": "BCT549_6_certificate_verdict",
        },
        {
            "source_id": "549_obstructions",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_OBSTRUCTION_LEDGER.csv",
            "role": "obstruction ledger for finite charge and boundary hair",
            "needle": "BCO549_2_vector_tensor_hair",
        },
        {
            "source_id": "549_flux_fill_row",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv",
            "role": "fallback boundary flux bound row",
            "needle": "FB549_0_boundary_flux_bound",
        },
        {
            "source_id": "552_doc",
            "path": "552-Y5-parent-action-BRR545-zero-theorem-contract-or-first-repair-attempt.md",
            "role": "BRR545 parent-action zero theorem contract",
            "needle": "HPR552_1_reference_boundary_pairing",
        },
        {
            "source_id": "552_zero_contract",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_PARENT_ACTION_ZERO_THEOREM_CONTRACT.csv",
            "role": "parent action clauses for reference superselection and boundary relative nohair",
            "needle": "BZTC552_3_boundary_relative_nohair",
        },
        {
            "source_id": "552_clause_tests",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_PARENT_ACTION_CLAUSE_TESTS.csv",
            "role": "clause tests showing reference and boundary flux fail current claim",
            "needle": "CT552_1_boundary_flux",
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


def zero_theorem_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "ZT995_0_parent_boundary_phase_space",
            "zero_clause": "the parent action supplies L, B_ref, Theta, Q_tau, and C_tau for the MTS branch",
            "mathematical_requirement": "S=int_M L[Phi]+int_dM B_ref; delta L=E_A delta Phi^A+dTheta; J_tau=Theta(Phi,L_tau Phi)-i_tau L=dQ_tau+C_tau",
            "current_result": "blocked",
            "blocker": "545/552 contain the covariant phase-space template, but not a fully varied MTS parent Lagrangian and boundary term",
            "accepted_for_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZT995_1_Bref_superselection",
            "zero_clause": "B_ref is fixed by the parent branch and cannot depend on source, surface, frame, radius, or fit choice",
            "mathematical_requirement": "partial_t Delta_ref=partial_r Delta_ref=partial_source Delta_ref=partial_frame Delta_ref=0",
            "current_result": "blocked",
            "blocker": "reference lock remains a contract; 544/545/552 do not parent-select the subtraction",
            "accepted_for_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZT995_2_EH_GHY_not_imported",
            "zero_clause": "GHY/reference machinery may be used only as an EH comparator unless MTS derives the same boundary pair",
            "mathematical_requirement": "B_ref^MTS=B_GHY+constant/topological class by parent variation, not by analogy",
            "current_result": "comparator_only",
            "blocker": "EH/GHY gives the target shape, but importing it would hide the MTS boundary proof inside GR",
            "accepted_for_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZT995_3_relative_cohomology_exactness",
            "zero_clause": "the improvement/exact boundary form is trivial in the relevant relative cohomology class",
            "mathematical_requirement": "B_imp=dC and int_S2 B_imp-int_S1 B_imp=int_A dB_imp=0 with parent-selected relative class",
            "current_result": "blocked",
            "blocker": "549 says exact/topological labels can still carry finite linked-sphere charges unless the relative class is owned",
            "accepted_for_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZT995_4_no_vector_tensor_radial_hair",
            "zero_clause": "boundary stress has no vector, trace-free tensor, shear, marker, normal-exchange, time, radial, or frame hair",
            "mathematical_requirement": "n_mu P_loc_nu T_B^{mu nu}=0; T_B^TF=T_B^vector=0; partial_t,r,frame T_B=0",
            "current_result": "blocked",
            "blocker": "scalar/trace no-flux does not remove vector/tensor/derivative hair without a parent-owned boundary action",
            "accepted_for_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZT995_5_projector_symplectic_silence",
            "zero_clause": "projector variation does not create a boundary-supported symplectic residual",
            "mathematical_requirement": "delta Pi_M=0 and [d,Pi_M]J_H=0 on the fixed charge branch, or a source-backed boundary commutator bound exists",
            "current_result": "blocked",
            "blocker": "Pi_M/projector stress remains retained in 545/552 and feeds Delta_symp",
            "accepted_for_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZT995_6_positive_same_frame_MHref",
            "zero_clause": "M_H_ref is positive and tied to the same observed-frame mass normalization",
            "mathematical_requirement": "M_H_ref>0 and G_ref M_H_ref=GM_observed in the same frame used by Q_tau",
            "current_result": "blocked",
            "blocker": "same-frame measured-GM/worldtube denominator glue is still conditional",
            "accepted_for_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZT995_7_zero_theorem_verdict",
            "zero_clause": "RC994_0_reference_boundary=0 can be signed for current MTS",
            "mathematical_requirement": "Delta_ref=0, Delta_symp_boundary=0, B_zero_flux=0, projector boundary tail=0, and M_H_ref>0",
            "current_result": "fail_current_claim",
            "blocker": "at least six upstream clauses are unsigned, so the zero proof is not available yet",
            "accepted_for_zero": "false",
            "valid_for_claim": "false",
        },
    ]


def clause_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "CA995_0_Bref_lock",
            "source_clause": "MAC545_2;BZTC552_2",
            "question": "is the reference subtraction parent-selected rather than chosen?",
            "answer": "no",
            "needed_exit": "derive B_ref from the parent action, topology, or stationarity rule with no source/surface/frame dependence",
            "residual_if_open": "Delta_ref_over_MH",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CA995_1_GHY_reference_pair",
            "source_clause": "EHB994_0;HPR552_1",
            "question": "can the EH GHY/reference pair be reused as proof?",
            "answer": "no; comparator only",
            "needed_exit": "show the MTS parent variation produces the same boundary pair or a source-backed difference",
            "residual_if_open": "Delta_symp_boundary_over_MH",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CA995_2_exact_cohomology",
            "source_clause": "MAC545_3;BCT549_1;BCT549_2",
            "question": "does exact/cohomology language itself kill the boundary charge?",
            "answer": "no",
            "needed_exit": "parent-selected relative class with linked-sphere flux zero, or a numeric/profile bound",
            "residual_if_open": "B_zero_flux_over_MH",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CA995_3_boundary_hair",
            "source_clause": "MAC545_4;BCT549_3;BCO549_2;BCO549_3",
            "question": "are vector/tensor/radial/frame/source boundary hair channels eliminated?",
            "answer": "no",
            "needed_exit": "parent-owned marker-free homogeneous boundary action or source-backed hair coefficient rows",
            "residual_if_open": "B_TF_vector_radial_hair_over_MH",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CA995_4_projector_silence",
            "source_clause": "MAC545_5;BCO549_4;CT552_2;CT552_3",
            "question": "does the boundary route silence Pi_M/projector symplectic stress?",
            "answer": "no",
            "needed_exit": "Hamiltonian charge projector proof or finite boundary projector commutator row",
            "residual_if_open": "projector_boundary_commutator_over_MH",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CA995_5_denominator",
            "source_clause": "MAC545_6;CT552_4",
            "question": "is the denominator positive and calibrated in the same observed frame?",
            "answer": "not yet",
            "needed_exit": "M_H_ref owner tied to same-frame measured-GM/worldtube glue",
            "residual_if_open": "all_RC9940_ratios",
            "valid_for_claim": "false",
        },
    ]


def eh_ghy_comparator_rows() -> list[dict[str, str]]:
    return [
        {
            "comparator_id": "EHG995_0_GHY_variation",
            "object": "Einstein-Hilbert plus GHY/reference boundary pair",
            "allowed_use": "well-posed GR comparator for what an owned local-GR boundary current should reduce to",
            "forbidden_use": "declare MTS B_ref=B_GHY without deriving it from the MTS parent variation",
            "status": "comparator_only",
            "valid_for_claim": "false",
        },
        {
            "comparator_id": "EHG995_1_reference_background",
            "object": "GR reference subtraction / background choice",
            "allowed_use": "name the reference-lock target and test whether MTS makes it source independent",
            "forbidden_use": "choose a reference after seeing the source/readout residual",
            "status": "comparator_only",
            "valid_for_claim": "false",
        },
        {
            "comparator_id": "EHG995_2_Komar_ADM_shape",
            "object": "standard GR boundary mass-charge shape",
            "allowed_use": "downstream target for Q_tau once parent current and M_H_ref are owned",
            "forbidden_use": "replace missing MTS source current by orbital GM or an EH charge",
            "status": "comparator_only",
            "valid_for_claim": "false",
        },
    ]


def residual_bound_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BR995_0_Delta_ref",
            "target": "Delta_ref_over_MH",
            "formula": "abs(Delta_ref)/M_H_ref",
            "numerator_status": "MISSING_BREF_SUPERSELECTION_OR_SOURCE_VALUE",
            "denominator_status": "MISSING_SAME_FRAME_POSITIVE_MHREF",
            "units": "dimensionless",
            "required_source_columns": "system_id;surface_pair;Delta_ref;M_H_ref;units;B_ref_rule;source_path;valid_for_claim",
            "current_value": "",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BR995_1_Delta_symp_boundary",
            "target": "Delta_symp_boundary_over_MH",
            "formula": "abs(Delta_symp_boundary)/M_H_ref",
            "numerator_status": "MISSING_SYMPLECTIC_REFERENCE_BOUNDARY_VALUE",
            "denominator_status": "MISSING_SAME_FRAME_POSITIVE_MHREF",
            "units": "dimensionless",
            "required_source_columns": "system_id;surface_pair;Delta_symp_boundary;Theta_rule;projector_rule;M_H_ref;source_path;valid_for_claim",
            "current_value": "",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BR995_2_B_zero_flux",
            "target": "B_zero_flux_over_MH",
            "formula": "abs(int_S2 B_imp-int_S1 B_imp)/M_H_ref",
            "numerator_status": "MISSING_RELATIVE_COHOMOLOGY_ZERO_OR_BOUNDARY_FLUX_PROFILE",
            "denominator_status": "MISSING_SAME_FRAME_POSITIVE_MHREF",
            "units": "dimensionless",
            "required_source_columns": "system_id;surface_pair;B_zero_flux;relative_class_rule;flux_profile;M_H_ref;source_path;valid_for_claim",
            "current_value": "",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BR995_3_boundary_hair",
            "target": "B_TF_vector_radial_hair_over_MH",
            "formula": "sum_abs(B_TF,B_vector,B_shear,B_normal_exchange,partial_tB,partial_rB,partial_frameB)/M_H_ref",
            "numerator_status": "MISSING_VECTOR_TENSOR_RADIAL_HAIR_COEFFICIENTS",
            "denominator_status": "MISSING_SAME_FRAME_POSITIVE_MHREF",
            "units": "dimensionless",
            "required_source_columns": "system_id;hair_channel;coefficient;profile;bound;M_H_ref;mapped_lock_row;source_path;valid_for_claim",
            "current_value": "",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BR995_4_projector_boundary",
            "target": "projector_boundary_commutator_over_MH",
            "formula": "abs(Delta_PiM_boundary+[d,Pi_M]J_H_boundary+deltaPi_M_boundary)/M_H_ref",
            "numerator_status": "MISSING_PROJECTOR_BOUNDARY_COMMUTATOR_VALUE",
            "denominator_status": "MISSING_SAME_FRAME_POSITIVE_MHREF",
            "units": "dimensionless",
            "required_source_columns": "system_id;surface_pair;projector_commutator;deltaPiM_boundary;M_H_ref;source_path;valid_for_claim",
            "current_value": "",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BR995_5_RC9940_total_abs",
            "target": "RC994_0_reference_boundary_over_MH",
            "formula": "BR995_0+BR995_1+BR995_2+BR995_3+BR995_4",
            "numerator_status": "MISSING_COMPONENT_VALUES_NO_CANCELLATION_ALLOWED",
            "denominator_status": "MISSING_SAME_FRAME_POSITIVE_MHREF",
            "units": "dimensionless",
            "required_source_columns": "all component rows valid, numeric, sourced, same-frame, no MISSING markers",
            "current_value": "",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def delta_ref_symp_map_rows() -> list[dict[str, str]]:
    return [
        {
            "map_id": "MAP995_0_reference",
            "source_piece": "delta B_ref + reference subtraction",
            "mapped_residual": "Delta_ref",
            "expression": "Delta_ref[S2,S1]=Delta_Bref[S2]-Delta_Bref[S1]",
            "current_status": "MISSING_BREF_LOCK",
            "blocks": "RC994_0, DeltaH envelope, FB554_0",
            "valid_for_claim": "false",
        },
        {
            "map_id": "MAP995_1_symplectic",
            "source_piece": "boundary symplectic/reference flux",
            "mapped_residual": "Delta_symp_boundary",
            "expression": "Delta_symp_boundary=int_A omega_boundary+omega_ref+omega_projector_tail",
            "current_status": "MISSING_THETA_BREF_PROJECTOR_SILENCE",
            "blocks": "RC994_0, Hamiltonian integrability",
            "valid_for_claim": "false",
        },
        {
            "map_id": "MAP995_2_boundary_flux",
            "source_piece": "exact/cohomology boundary improvement",
            "mapped_residual": "B_zero_flux",
            "expression": "B_zero_flux=int_S2 B_imp-int_S1 B_imp",
            "current_status": "MISSING_RELATIVE_CLASS_OR_FLUX_BOUND",
            "blocks": "boundary alpha3/xi/beta/Gdot/R11 rows",
            "valid_for_claim": "false",
        },
        {
            "map_id": "MAP995_3_no_cancellation_total",
            "source_piece": "RC994_0 boundary/reference total",
            "mapped_residual": "RC994_0_reference_boundary_over_MH",
            "expression": "abs(Delta_ref)/M_H_ref+abs(Delta_symp_boundary)/M_H_ref+abs(B_zero_flux)/M_H_ref+abs(hair/projector terms)/M_H_ref",
            "current_status": "MISSING_COMPONENT_VALUES",
            "blocks": "deltaH curl bound and local-GR reduction",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG995_0_RC9940_zero",
            "claim": "RC994_0_reference_boundary=0",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "B_ref, relative cohomology/nohair, projector silence, and M_H_ref clauses remain unsigned",
        },
        {
            "gate_id": "CG995_1_RC9940_bound",
            "claim": "RC994_0 has a source-backed finite bound",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "bound rows are schema-only and contain MISSING source/value markers",
        },
        {
            "gate_id": "CG995_2_deltaH_FB5540",
            "claim": "deltaH curl or FB554_0 is closed by the boundary/reference route",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "RC994_0 still contributes to the 994 no-cancellation envelope",
        },
        {
            "gate_id": "CG995_3_Newton_PPN_R10_localGR",
            "claim": "Newton, PPN, R10, R11, orbital, or local-GR pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "this checkpoint only audits one residual-current family and does not supply source-current equality",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC995_0_zero_attempt",
            "decision": "do not promote the boundary/reference zero theorem",
            "reason": "the required B_ref lock, relative boundary class, no-hair, projector silence, and denominator clauses are not parent-owned",
            "effect": "RC994_0 remains live in the deltaH no-cancellation envelope",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC995_1_EH_comparator",
            "decision": "keep EH/GHY as comparator only",
            "reason": "using it directly would smuggle GR into MTS instead of deriving the local-GR limit",
            "effect": "the target shape is useful but carries no claim credit",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC995_2_bound_schema",
            "decision": "stage source-ready RC994_0 bound rows",
            "reason": "if the zero theorem remains unavailable, the next honest route is sourced component bounds",
            "effect": "future work has exact rows to fill without cancellation bookkeeping",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "996-Y5-R10-relative-boundary-class-owner-or-Bref-source-bound-pack.md",
            "objective": "either parent-own the relative boundary class and B_ref superselection, or fill source-backed RC994_0 boundary/reference bound inputs",
            "include": "B_ref lock, parent-selected relative cohomology class, boundary no-hair coefficients, projector boundary commutator, positive same-frame M_H_ref",
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
    zero_gates: list[dict[str, str]],
    clause_audit: list[dict[str, str]],
    eh_ghy: list[dict[str, str]],
    residual_bounds: list[dict[str, str]],
    maps: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    zero_ok = (
        len(zero_gates) >= 8
        and any(row["gate_id"] == "ZT995_7_zero_theorem_verdict" and row["current_result"] == "fail_current_claim" for row in zero_gates)
        and all(row["accepted_for_zero"] == "false" and row["valid_for_claim"] == "false" for row in zero_gates)
    )
    clause_ok = all(row["valid_for_claim"] == "false" and row["residual_if_open"] for row in clause_audit)
    eh_ok = all(row["status"] == "comparator_only" and row["valid_for_claim"] == "false" and row["forbidden_use"] for row in eh_ghy)
    bounds_ok = (
        len(residual_bounds) >= 6
        and all(row["valid_for_claim"] == "false" for row in residual_bounds)
        and all("MISSING" in row["numerator_status"] or "MISSING" in row["denominator_status"] for row in residual_bounds)
        and any(row["bound_id"] == "BR995_5_RC9940_total_abs" and "+" in row["formula"] for row in residual_bounds)
    )
    maps_ok = all(row["valid_for_claim"] == "false" and "MISSING" in row["current_status"] for row in maps)
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC995_0_zero_attempt" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V995_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all cited local source files exist and expected needles are found"},
        {"check_id": "V995_1_zero_theorem_fail_closed", "result": "pass" if zero_ok else "fail", "detail": "zero theorem is explicitly blocked and not promoted"},
        {"check_id": "V995_2_clause_audit_residualized", "result": "pass" if clause_ok else "fail", "detail": "each unsigned clause maps to a retained residual"},
        {"check_id": "V995_3_EH_GHY_comparator_limited", "result": "pass" if eh_ok else "fail", "detail": "EH/GHY is comparator-only with forbidden import use recorded"},
        {"check_id": "V995_4_residual_bound_rows_fail_closed", "result": "pass" if bounds_ok else "fail", "detail": "RC994_0 bound rows are source-ready but MISSING and valid_for_claim=false"},
        {"check_id": "V995_5_delta_ref_symp_map_safe", "result": "pass" if maps_ok else "fail", "detail": "Delta_ref/Delta_symp/B_flux map remains nonclaim and missing-valued"},
        {"check_id": "V995_6_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "RC994_0, deltaH, FB5540, and local-GR claims are blocked"},
        {"check_id": "V995_7_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "zero attempt decision is recorded"},
        {"check_id": "V995_8_next_target_written", "result": "pass" if next_ok else "fail", "detail": "996 target row is present and nonclaim"},
        {"check_id": "V995_9_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V995_READY",
            "result": "pass" if ready else "fail",
            "detail": "995 boundary/reference gate validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    zero_gates: list[dict[str, str]],
    clause_audit: list[dict[str, str]],
    eh_ghy: list[dict[str, str]],
    residual_bounds: list[dict[str, str]],
    maps: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 995 Y5 R10: Boundary/Reference Current Zero Theorem or Residual Bound Row",
        "",
        "Status: `Y5_R10_995_boundary_reference_zero_theorem_failed_source_ready_RC9940_bound_rows_staged_nonclaim`",
        "",
        "Claim ceiling: no `RC994_0=0`, no source-backed `RC994_0` bound, no `deltaH` curl closure, no `FB554_0=0`, no Newton/PPN/R10/R11/orbit/local-GR pass.",
        "",
        "## Readout",
        "",
        "995 takes the first residual-current family from 994 and tries the clean route first: prove the boundary/reference current is zero. That proof does not close. The missing piece is not a vibe problem; it is a precise ownership problem. `B_ref`, the relative boundary class, boundary no-hair, projector symplectic silence, and the positive same-frame denominator are not yet parent-signed.",
        "",
        "So the branch stays honest: EH/GHY is retained as a comparator only, and `RC994_0` becomes a source-ready residual vector rather than a hidden GR import. Tiny grimace, useful map.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Boundary/Reference Zero-Theorem Gate",
        "",
        md_table(zero_gates, ["gate_id", "zero_clause", "mathematical_requirement", "current_result", "blocker", "accepted_for_zero", "valid_for_claim"]),
        "",
        "## Clause Audit",
        "",
        md_table(clause_audit, ["audit_id", "source_clause", "question", "answer", "needed_exit", "residual_if_open", "valid_for_claim"]),
        "",
        "## EH/GHY Comparator Ledger",
        "",
        md_table(eh_ghy, ["comparator_id", "object", "allowed_use", "forbidden_use", "status", "valid_for_claim"]),
        "",
        "## RC994_0 Residual Bound Row Schema",
        "",
        md_table(residual_bounds, ["bound_id", "target", "formula", "numerator_status", "denominator_status", "units", "required_source_columns", "source_path", "status", "valid_for_claim"]),
        "",
        "## Delta_ref / Delta_symp Map",
        "",
        md_table(maps, ["map_id", "source_piece", "mapped_residual", "expression", "current_status", "blocks", "valid_for_claim"]),
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
    zero_gates = zero_theorem_gate_rows()
    clause_audit = clause_audit_rows()
    eh_ghy = eh_ghy_comparator_rows()
    residual_bounds = residual_bound_schema_rows()
    maps = delta_ref_symp_map_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, zero_gates, clause_audit, eh_ghy, residual_bounds, maps, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_995_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_995_BOUNDARY_REFERENCE_ZERO_THEOREM_GATE.csv", zero_gates)
    write_csv(OUT / "P8_Y5_R10_995_CLAUSE_AUDIT.csv", clause_audit)
    write_csv(OUT / "P8_Y5_R10_995_EH_GHY_COMPARATOR_LEDGER.csv", eh_ghy)
    write_csv(OUT / "P8_Y5_R10_995_RC9940_RESIDUAL_BOUND_ROW_SCHEMA.csv", residual_bounds)
    write_csv(OUT / "P8_Y5_R10_995_DELTA_REF_SYMP_MAP.csv", maps)
    write_csv(OUT / "P8_Y5_R10_995_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_995_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_995_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_995_VALIDATION.csv", validation)
    write_doc(sources, zero_gates, clause_audit, eh_ghy, residual_bounds, maps, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
