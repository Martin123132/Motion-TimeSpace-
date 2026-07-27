from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3360-Y5-R2FR-Yloc-Euler-equations-or-R11-coefficient-bound-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

LOCAL_SOURCES = [
    ("LSRC3360_0_3359_doc", ROOT / "3359-Y5-R2FR-left-hand-EH-Newton-operator-recovery-under-AX1090.md", "3359 handoff"),
    ("LSRC3360_1_3359_next", OUT / "P8_Y5_R2FR_3359_NEXT_TARGET.csv", "3359 next target"),
    ("LSRC3360_2_3359_double_zero", OUT / "P8_Y5_R2FR_3359_DOUBLE_ZERO_SELECTOR_PACKET.csv", "double-zero packet"),
    ("LSRC3360_3_3359_operator_matrix", OUT / "P8_Y5_R2FR_3359_NON_EH_OPERATOR_FAMILY_MATRIX.csv", "non-EH operator family matrix"),
    ("LSRC3360_4_3359_bounds", OUT / "P8_Y5_R2FR_3359_OPERATOR_RESIDUAL_BOUND_SCHEMA.csv", "operator residual bound schema"),
    ("LSRC3360_5_Yloc_euler", OUT / "P8_YLOC_EULER_SYSTEM.csv", "old Yloc Euler component system"),
    ("LSRC3360_6_Yloc_no_source", OUT / "P8_YLOC_NO_SOURCE_THEOREM.csv", "old positive-operator no-source theorem"),
    ("LSRC3360_7_Yloc_source_debt", OUT / "P8_YLOC_SOURCE_DEBT_LEDGER.csv", "old Yloc source debt ledger"),
    ("LSRC3360_8_Yloc_no_linear", OUT / "P8_YLOC_NO_LINEAR_SOURCE_PARENT_CONTRACT.csv", "old no-linear-source parent contract"),
    ("LSRC3360_9_Yloc_aux_result", OUT / "P8_YLOC_AUX_PARENT_COMPONENT_RESULT.csv", "old auxiliary parent component result"),
    ("LSRC3360_10_energy_identity", OUT / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv", "positive-operator energy identity"),
    ("LSRC3360_11_response_variation", OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv", "response-doublet variation and source-current obstruction"),
    ("LSRC3360_12_GK_contract", OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv", "GK/q_loc first variation contract"),
    ("LSRC3360_13_3357_scope", OUT / "P8_Y5_R2FR_3357_CLAIM_SCOPE_SEPARATION.csv", "AX1090 source-side theorem scope"),
    ("LSRC3360_14_3358_surface", OUT / "P8_Y5_R2FR_3358_EPSILON_SURFACE_SOURCE_UPDATE.csv", "surface/source residual update"),
]

OUTPUTS = {
    "local_sources": OUT / "P8_Y5_R2FR_3360_LOCAL_SOURCE_REGISTER.csv",
    "euler_packet": OUT / "P8_Y5_R2FR_3360_YLOC_EULER_ZERO_PACKET.csv",
    "component_audit": OUT / "P8_Y5_R2FR_3360_YLOC_COMPONENT_CLOSURE_AUDIT.csv",
    "r11_link": OUT / "P8_Y5_R2FR_3360_R11_FACTORISATION_LINK_AUDIT.csv",
    "bound_rows": OUT / "P8_Y5_R2FR_3360_FIRST_R11_BOUND_ROW_ATTEMPT.csv",
    "gates": OUT / "P8_Y5_R2FR_3360_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3360_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3360_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3360_VALIDATION.csv",
}


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parseable(path: Path) -> bool:
    try:
        if path.suffix.lower() == ".csv":
            read_csv(path)
        else:
            path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(compact(row.get(key, ""), 260).replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines) + "\n"


def local_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_str(path.exists()),
            "parseable": bool_str(path.exists() and parseable(path)),
            "usage": usage,
            "valid_for_claim": "false",
        }
        for source_id, path, usage in LOCAL_SOURCES
    ]


def euler_packet_rows() -> list[dict[str, Any]]:
    return [
        {
            "packet_id": "YE3360_0_positive_operator_identity",
            "claim": "For each local-silence component Y^A, a positive self-adjoint Euler operator L_A gives an energy identity.",
            "math_form": "L_A Y^A = J_A with boundary B_A; integral <Y,L_A Y> = positive_norm[Y] = integral Y J_A + boundary_flux",
            "current_result": "EXACT_CONDITIONAL_SUFFICIENCY",
            "gap": "operator positivity and parent ownership must be shown componentwise",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "YE3360_1_zero_source_boundary",
            "claim": "If J_A=0 and B_A=0 for every component, positivity forces Y_loc^A=0.",
            "math_form": "positive_norm[Y]=0 => Y^A=0 modulo pure gauge/topological classes",
            "current_result": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "gap": "J_A/B_A zero not parent-signed for Y2-Y6",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "YE3360_2_no_linear_source_contract",
            "claim": "A true parent evenness/selection symmetry can forbid linear J_A Y^A source terms.",
            "math_form": "y^A -> -y^A as a parent symmetry, not a notation flip on composite residuals",
            "current_result": "ROUTE_AVAILABLE_NOT_DERIVED",
            "gap": "physical residuals are not yet parentized as odd variables with matter/boundary neutrality",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "YE3360_3_physical_lock",
            "claim": "The zeroed Y variables must equal actual q_loc/PPN/R11/source-normalization residuals, not bookkeeping auxiliaries.",
            "math_form": "Y_loc^A = {X_D,Qcoh_D,Phi_boundary,V_domain,S_TF_domain,Delta_mu_source,nabla T_extra,...} through the local PPN gate",
            "current_result": "MAIN_BLOCKER",
            "gap": "composite residual lock and PPN lock remain unsigned",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "YE3360_4_AX1090_update",
            "claim": "The 3357/3358 source-side packet improves the ordinary Hilbert source and surface/contact classification, but does not zero every Y source current.",
            "math_form": "ordinary matter+EM source is cleaner; nonordinary boundary/domain/source-normalization/stress currents remain retained",
            "current_result": "PARTIAL_IMPROVEMENT_NOT_CLOSURE",
            "gap": "Y5 source normalization and Y6 extra stress remain hard rows",
            "valid_for_claim": "false",
        },
    ]


def component_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "Y0_trace_expansion",
            "component": "X_D",
            "euler_route": "positive scalar/trace operator with no source and zero boundary flux",
            "AX1090_update": "ordinary Hilbert source cleaned; exterior/vacuum trace route improved",
            "current_status": "PARTIAL_CONDITIONAL_NOT_LOCKED",
            "blocks": "parent branch/domain selector and physical residual lock",
            "valid_for_claim": "false",
        },
        {
            "component_id": "Y1_coherent_projector",
            "component": "Qcoh_D - h X_D/3",
            "euler_route": "algebraic constraint plus positive STF penalty",
            "AX1090_update": "projector/source-shadow aliases reduced, but projector stress ownership remains",
            "current_status": "PARTIAL_CLAUSE_STRESS_OPEN",
            "blocks": "topological/projector ownership and metric-stress accounting",
            "valid_for_claim": "false",
        },
        {
            "component_id": "Y2_boundary_flux",
            "component": "Phi_boundary^i",
            "euler_route": "boundary/collar elliptic equation with scalar stationary no-flux conditions",
            "AX1090_update": "3355/3356 kill pointwise bulk boundary/contact; 3358 trichotomy isolates surface multipoles",
            "current_status": "IMPROVED_BUT_SURFACE_BRANCH_OPEN",
            "blocks": "surface/contact owner, universal monopole certificate, or multipole bound",
            "valid_for_claim": "false",
        },
        {
            "component_id": "Y3_domain_vector",
            "component": "V_domain^i",
            "euler_route": "positive vector operator with no preferred-frame source",
            "AX1090_update": "hidden-frame/readout aliases reduced but actual no-vector domain theorem absent",
            "current_status": "RETAINED_UNFILLED",
            "blocks": "domain selector no-vector Euler theorem or R5/R6/R7 coefficient products",
            "valid_for_claim": "false",
        },
        {
            "component_id": "Y4_domain_STF_stress",
            "component": "S_TF_domain^{ij}",
            "euler_route": "positive STF stress operator or topological/isotropic trace-only projector stress",
            "AX1090_update": "source side cleaner, but Bianchi-owned STF stress can remain conserved and nonzero",
            "current_status": "RETAINED_DEBT",
            "blocks": "topological/isotropic stress theorem or xi/T_extra residual scoring",
            "valid_for_claim": "false",
        },
        {
            "component_id": "Y5_source_normalization",
            "component": "Delta_mu_source",
            "euler_route": "constant measured-GM/source-normalization Noether theorem or double-zero source-normalization coefficient",
            "AX1090_update": "surface/contact trichotomy helps, but measured-GM calibration is still not parent-owned",
            "current_status": "FAILED_CURRENT_HARD_ROW",
            "blocks": "constant kappa, same-frame mass flux, no extra mu channels, source-normalization operator",
            "valid_for_claim": "false",
        },
        {
            "component_id": "Y6_stress_Bianchi",
            "component": "nabla_mu T_extra^{mu nu}",
            "euler_route": "Ward/Bianchi stress ledger plus zero/topological/invisible extra stress",
            "AX1090_update": "ordinary Hilbert source owner cleaned, but conserved extra stress can still exist",
            "current_status": "RETAINED_DEBT",
            "blocks": "topological/invisible T_extra theorem or explicit residual vector scoring",
            "valid_for_claim": "false",
        },
    ]


def r11_link_rows() -> list[dict[str, Any]]:
    return [
        {
            "link_id": "R11L3360_0_boundary_topological",
            "R11_family": "boundary/topological terms",
            "needed_Y_control": "Y2 boundary flux plus topological/scalar no-flux route",
            "factorisation_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "fallback": "boundary/topological coefficient or contact multipole bound",
            "valid_for_claim": "false",
        },
        {
            "link_id": "R11L3360_1_R2_fR_scalar",
            "R11_family": "R^2/f(R) scalar mode",
            "needed_Y_control": "Y0 trace/scalar silence plus actual c_R2(Sigma_loc)=O(Sigma_loc^2)",
            "factorisation_status": "MISSING_ACTUAL_COEFFICIENT_FACTORISATION",
            "fallback": "R2/fR coefficient and scalar mass/range bound",
            "valid_for_claim": "false",
        },
        {
            "link_id": "R11L3360_2_Ricci_Weyl_squared",
            "R11_family": "Ricci^2/Weyl^2",
            "needed_Y_control": "topological Gauss-Bonnet route or Y4 shear/STF silence",
            "factorisation_status": "MISSING_TOPOLOGICAL_OR_DOUBLE_ZERO_CERTIFICATE",
            "fallback": "quadratic curvature coefficient bound",
            "valid_for_claim": "false",
        },
        {
            "link_id": "R11L3360_3_scalar_tensor",
            "R11_family": "scalar-tensor/class-metric coupling",
            "needed_Y_control": "scalar field local fixed point plus derivative silence",
            "factorisation_status": "MISSING_LOCAL_SCALAR_SILENCE",
            "fallback": "scalar coupling/range/Gdot bound",
            "valid_for_claim": "false",
        },
        {
            "link_id": "R11L3360_4_vector_preferred_frame",
            "R11_family": "vector/preferred-frame selector",
            "needed_Y_control": "Y3 domain vector no-source theorem",
            "factorisation_status": "RETAINED_UNFILLED",
            "fallback": "alpha1/alpha2/alpha3/xi vector coefficient products",
            "valid_for_claim": "false",
        },
        {
            "link_id": "R11L3360_5_torsion_nonmetricity",
            "R11_family": "torsion/nonmetricity",
            "needed_Y_control": "Levi-Civita branch or positive connection-mode silence",
            "factorisation_status": "MISSING_CONNECTION_ZERO",
            "fallback": "connection/torsion/nonmetricity coefficient bound",
            "valid_for_claim": "false",
        },
        {
            "link_id": "R11L3360_6_bulk_X_force",
            "R11_family": "bulk X force/range field",
            "needed_Y_control": "source charge zero plus positive no-hair operator",
            "factorisation_status": "MISSING_SOURCE_CHARGE_ZERO",
            "fallback": "R10 alpha(lambda) curve map or finite-range coefficient",
            "valid_for_claim": "false",
        },
        {
            "link_id": "R11L3360_7_nonlocal_memory",
            "R11_family": "nonlocal/memory kernel",
            "needed_Y_control": "compact-local kernel silence and no history injection",
            "factorisation_status": "MISSING_KERNEL_LOCALITY_BOUND",
            "fallback": "kernel norm/locality/Gdot/R10 bound",
            "valid_for_claim": "false",
        },
        {
            "link_id": "R11L3360_8_source_normalization",
            "R11_family": "source-normalization operator",
            "needed_Y_control": "Y5 measured-GM/source normalization owner theorem",
            "factorisation_status": "OPEN_HARD_ROW",
            "fallback": "c_domain_source_normalization_operator bound",
            "valid_for_claim": "false",
        },
        {
            "link_id": "R11L3360_9_projector_domain_stress",
            "R11_family": "projector/domain stress",
            "needed_Y_control": "Y1/Y4/Y6 projector stress topological or double-zero",
            "factorisation_status": "CONDITIONAL_ZERO_NOT_PARENT_OWNED",
            "fallback": "projector stress coefficient bound",
            "valid_for_claim": "false",
        },
    ]


def bound_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "RB3360_0_first_real_R11_bound_attempt",
            "target": "epsilon_nonEH_operator_abs",
            "attempted_route": "source-backed absolute R11 coefficient row",
            "candidate_formula": "sum_A |c_A| |W_A| with no cancellation; first scored row may be c_domain_source_normalization_operator or vector_preferred_frame coefficient",
            "available_sources": "R11_nonEH_operator_vector_executable.csv; P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv; P8_YLOC_EULER_SYSTEM.csv",
            "current_value": "NOT_FILLED_NUMERICALLY",
            "why_not_source_backed_claim": "no coefficient value, units, weak-field map, or source path for a numeric bound is present",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "RB3360_1_zero_switch_attempt",
            "target": "epsilon_nonEH_operator_abs",
            "attempted_route": "derive zero via Yloc Euler + actual R11 factorisation",
            "candidate_formula": "0 if every Yloc component is parent-zero and every R11 family is absent/topological/double-zero selected",
            "available_sources": "P8_YLOC_NO_SOURCE_THEOREM.csv; P8_DOUBLE_ZERO_R11_VARIATION_PROOF.csv",
            "current_value": "BLOCKED_BY_YLOC_SOURCE_CURRENTS_AND_FACTORISATION",
            "why_not_source_backed_claim": "Y2-Y6 source/boundary currents and actual R11 factorisation remain unsigned",
            "valid_for_component_bound": "false",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3360_0_positive_Euler_zero_theorem",
            "claim": "positive Euler operator plus zero source/boundary currents forces Y_loc=0",
            "passed": "true",
            "reason": "energy identity sufficiency is already present and consolidated",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3360_1_all_Yloc_sources_zero",
            "claim": "all Yloc source and boundary currents vanish in the current MTS corpus",
            "passed": "false",
            "reason": "Y2-Y6 source/boundary/stress currents remain open or retained",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3360_2_physical_residual_lock",
            "claim": "Yloc variables equal the actual q_loc/PPN/R11/source-normalization residuals",
            "passed": "false",
            "reason": "old no-linear-source and aux-parent audits say physical lock is not derived",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3360_3_actual_R11_factorisation",
            "claim": "every actual R11 family is absent/topological/double-zero factorized",
            "passed": "false",
            "reason": "factorisation contracts exist but actual coefficient/vector rows are unfilled",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3360_4_first_R11_numeric_bound",
            "claim": "a source-backed absolute R11 coefficient bound row is claim-ready",
            "passed": "false",
            "reason": "no numeric coefficient, units, weak-field map, and source path are all present for a scored row",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3360_5_local_GR_claim",
            "claim": "local GR/Newton branch is claim-ready",
            "passed": "false",
            "reason": "Yloc source currents, physical lock, R11 factorisation, and source calibration remain open",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3360_0",
            "question": "Did 3360 prove Y_loc=0?",
            "answer": "no, but it upgrades the proof target into a componentwise Euler/source-current closure problem",
            "reason": "positive-operator zero theorem is sound; failures are now specifically Y2-Y6 currents, physical lock, and R11 factorisation",
            "next_action": "attack Y5 source-normalization first or derive odd residual parentization/physical lock",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3360_1",
            "question": "What is the best route after this?",
            "answer": "derive physical-lock/odd-residual parentization before numeric R11 fitting",
            "reason": "without physical lock, a positive auxiliary action can zero bookkeeping fields while R11/PPN residuals survive",
            "next_action": "3361 odd-residual parentization and physical lock, with Y5 as the pressure row",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3361-Y5-R2FR-odd-residual-parentization-and-physical-lock-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3361_odd_residual_parentization_and_physical_lock.py",
            "objective": "derive actual physical residuals as parent odd variables with matter/boundary neutrality and lock them to q_loc/PPN/R11 rows, or demote Yloc zero to auxiliary closure only",
            "why_next": "3360 shows positive Euler equations are not enough unless Yloc variables are physical and source-free",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3362-Y5-R2FR-Y5-source-normalization-owner-or-first-R11-bound-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3362_Y5_source_normalization_owner_or_first_R11_bound_row.py",
            "objective": "attack the hardest row: derive measured-GM/source-normalization owner theorem or build the first numeric/source-backed c_domain_source_normalization_operator bound",
            "why_next": "Y5 is the hard row blocking Newton/source-normalized GR recovery",
            "valid_for_claim": "false",
        },
    ]


def render_doc() -> str:
    return "\n".join(
        [
            "# 3360 — Yloc Euler Equations Or R11 Coefficient Bound Under AX1090",
            "",
            f"Generated: `{RUN_UTC}`",
            "",
            "## Summary",
            "- This checkpoint attacks the blocker named by 3359: deriving `Y_loc^A=0` or filling a real R11 coefficient bound.",
            "- Real gain: the positive-operator Euler theorem is cleanly consolidated. If every `Y` component has a positive operator, zero source current, and zero boundary flux, then `Y_loc=0` follows.",
            "- The failure is now exact, not foggy: `Y2` boundary, `Y3` vector, `Y4` STF stress, `Y5` source normalization, and `Y6` extra stress are still not zeroed; physical residual lock is also missing.",
            "- No numeric/source-backed R11 coefficient bound was legitimately filled because coefficient values, units, and weak-field maps are still missing.",
            "- Therefore local GR/Newton remains unpromoted, but the next derivation target is sharper: odd-residual parentization / physical lock, especially for `Y5`.",
            "",
            "## Local Source Register",
            table(local_source_rows()),
            "## Yloc Euler Zero Packet",
            table(euler_packet_rows()),
            "## Yloc Component Closure Audit",
            table(component_audit_rows()),
            "## R11 Factorisation Link Audit",
            table(r11_link_rows()),
            "## First R11 Bound Row Attempt",
            table(bound_attempt_rows()),
            "## Promotion Gates",
            table(promotion_gate_rows()),
            "## Decision Ledger",
            table(decision_rows()),
            "## Next Target",
            table(next_target_rows()),
        ]
    )


def validate_outputs() -> list[dict[str, Any]]:
    local_sources = local_source_rows()
    packet = euler_packet_rows()
    components = component_audit_rows()
    r11 = r11_link_rows()
    bounds = bound_attempt_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    write_targets_outside_fw = all(not path.resolve().is_relative_to(FW.resolve()) for path in output_paths + [DOC])
    checks: list[dict[str, Any]] = [
        {
            "check_id": "VAL3360_0_local_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3360_1_local_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parseable"] == "true" for row in local_sources),
            "detail": "",
        },
        {
            "check_id": "VAL3360_2_outputs_parse",
            "check": "all 3360 non-validation outputs parse",
            "passed": all(path.exists() and parseable(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3360_3_euler_packet_complete",
            "check": "Euler packet includes positivity, zero source/boundary, no-linear-source, physical lock, and AX1090 update",
            "passed": {row["packet_id"] for row in packet}
            == {"YE3360_0_positive_operator_identity", "YE3360_1_zero_source_boundary", "YE3360_2_no_linear_source_contract", "YE3360_3_physical_lock", "YE3360_4_AX1090_update"},
            "detail": "",
        },
        {
            "check_id": "VAL3360_4_component_coverage",
            "check": "component audit covers Y0 through Y6",
            "passed": {row["component_id"] for row in components}
            == {"Y0_trace_expansion", "Y1_coherent_projector", "Y2_boundary_flux", "Y3_domain_vector", "Y4_domain_STF_stress", "Y5_source_normalization", "Y6_stress_Bianchi"},
            "detail": "",
        },
        {
            "check_id": "VAL3360_5_R11_family_coverage",
            "check": "R11 link audit covers ten operator families",
            "passed": len(r11) == 10 and all(row["valid_for_claim"] == "false" for row in r11),
            "detail": f"r11_rows={len(r11)}",
        },
        {
            "check_id": "VAL3360_6_no_fake_numeric_bound",
            "check": "first R11 bound attempts remain nonclaim and not numerically filled",
            "passed": all(row["valid_for_claim"] == "false" and ("NOT_FILLED" in row["current_value"] or "BLOCKED" in row["current_value"]) for row in bounds),
            "detail": "",
        },
        {
            "check_id": "VAL3360_7_no_overclaim",
            "check": "Yloc, physical lock, R11, numeric bound, and local GR claims remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3360_1_all_Yloc_sources_zero", "GATE3360_2_physical_residual_lock", "GATE3360_3_actual_R11_factorisation", "GATE3360_4_first_R11_numeric_bound", "GATE3360_5_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3360_8_next_targets_physical_lock_and_Y5",
            "check": "next targets attack physical lock and Y5 source normalization",
            "passed": any("physical residuals" in row["objective"] for row in next_target_rows())
            and any("source-normalization" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3360_9_write_scope_outside_formalization",
            "check": "all 3360 write targets are outside formalization-workbench",
            "passed": write_targets_outside_fw,
            "detail": f"write_targets={len(output_paths) + 1}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3360_10_overall",
            "check": "3360 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["local_sources"], local_source_rows())
    write_csv(OUTPUTS["euler_packet"], euler_packet_rows())
    write_csv(OUTPUTS["component_audit"], component_audit_rows())
    write_csv(OUTPUTS["r11_link"], r11_link_rows())
    write_csv(OUTPUTS["bound_rows"], bound_attempt_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs())
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
