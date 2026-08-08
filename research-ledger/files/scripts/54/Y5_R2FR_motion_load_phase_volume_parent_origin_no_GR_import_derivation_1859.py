from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1859"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1859_SOURCE_REGISTER.csv",
    "derivation_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1859_MOTION_PHASE_DERIVATION_AUDIT.csv",
    "no_go": RESIDUALS / "P8_Y5_PARENT_QLOC_1859_NO_GO_LEDGER.csv",
    "route_selection": RESIDUALS / "P8_Y5_PARENT_QLOC_1859_FIELD_EQUATION_ROUTE_SELECTION.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1859_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1859_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1859_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1859_VALIDATION.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def source_path(relative_path: str) -> str:
    return rel(ROOT / relative_path)


def ensure_dirs() -> None:
    for path in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    source_rows = [
        {
            "source_id": "SRC1859_0_1858_handoff",
            "source_path": source_path("1858-Y5-R2FR-parent-constraint-package-no-GR-import-gate.md"),
            "needle": "NEXT1858_0_primary",
            "role": "handoff into motion-load/phase-volume parent-origin attempt",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1859_1_phase_volume",
            "source_path": source_path("08-phase-volume-reciprocity-origin.md"),
            "needle": "phase_volume_reciprocity_motivated_not_parent_derived",
            "role": "phase-volume route status",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1859_2_hamiltonian_cell",
            "source_path": source_path("09-hamiltonian-radial-cell-derivation.md"),
            "needle": "generic symplectic or Liouville phase-volume preservation does not derive p=1",
            "role": "Hamiltonian/Liouville obstruction",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1859_3_observer_contract",
            "source_path": source_path("10-observer-map-symplectic-contract.md"),
            "needle": "That is the exact missing theorem",
            "role": "observer-cell contract",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1859_4_cell_current",
            "source_path": source_path("11-cell-current-origin-attempt.md"),
            "needle": "cell_current_origin_no_charge_obstruction",
            "role": "ordinary cell-current no-charge obstruction",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1859_5_gauge_noether",
            "source_path": source_path("12-gauge-noether-origin-audit.md"),
            "needle": "gauge_noether_origin_not_derived_closure_only",
            "role": "gauge/Noether obstruction",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1859_6_unimodular_cell",
            "source_path": source_path("1274-Y5-R10-RAB-unimodular-radial-cell-constraint-origin-or-finite-residual-intake.md"),
            "needle": "CLOSURE_ONLY_NOT_DERIVED",
            "role": "unimodular radial-cell closure status",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1859_7_equation_difference",
            "source_path": source_path("1275-Y5-R10-RAB-GR-style-radial-field-equation-difference-or-local-closure-baseline.md"),
            "needle": "D_R[MTS] := E_time - E_radial",
            "role": "GR-style equation-difference contract",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1859_8_parent_euler_contract",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_1276_PARENT_EULER_SOURCE_CONTRACT.csv"),
            "needle": "ESC1276_9_verdict",
            "role": "parent Euler/source-map contract",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1859_9_extra_silence",
            "source_path": source_path("1279-Y5-R10-RAB-A511-extra-sector-silence-double-zero-or-residual-vector.md"),
            "needle": "Gamma_eff/K_hat/q_loc",
            "role": "sharpest extra-sector blocker for EH/local-GR inheritance",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1859_10_finite_backstop",
            "source_path": source_path("1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md"),
            "needle": "RADIAL_CURRENT_NO_CHARGE_THEOREM_FAILS_CURRENT_CORPUS",
            "role": "finite fallback after current/no-charge failure",
            "status": "FOUND",
            "valid_for_claim": False,
        },
    ]

    derivation_rows = [
        {
            "audit_id": "MPD1859_0_definitions",
            "object": "radial observer-cell variable",
            "derivation_or_test": "J_q := T sqrt(S); C_R := ln(T^2 S)=2 ln(J_q)",
            "result": "EXACT_IDENTITY",
            "claim_impact": "defines the same reciprocal variable used by earlier R_AB/u rows",
            "status": "PASS_DEFINITION_ONLY",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPD1859_1_if_Jq_fixed",
            "object": "separate radial observer-cell conservation",
            "derivation_or_test": "J_q=1 -> T sqrt(S)=1 -> T^2 S=1 -> C_R=0; with T^2=1-L and S=(1-L)^(-p), this gives p=1",
            "result": "EXACT_CONDITIONAL",
            "claim_impact": "the algebraic lane to local GR reciprocity is clean if the parent law owns J_q=1",
            "status": "CONDITIONAL_NOT_PARENT_ORIGIN",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPD1859_2_motion_load_balance",
            "object": "motion-load phase-volume story",
            "derivation_or_test": "load reduces clock capacity while radial routing compensates so delta ln(T)+delta ln(sqrt(S))=0",
            "result": "MOTIVATES_JQ_CONSTANT",
            "claim_impact": "good physical interpretation but not an Euler/Dirac equation",
            "status": "MOTIVATION_NOT_DERIVATION",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPD1859_3_cell_current",
            "object": "ordinary conserved cell-current",
            "derivation_or_test": "partial_r(W_R partial_r C_R)=0 -> W_R partial_r C_R=Q_R",
            "result": "DERIVES_QR_CONSTANT_NOT_ZERO",
            "claim_impact": "leaves reciprocal hair unless Q_R=0 is separately proven",
            "status": "FAILS_AS_EXACT_LOCAL_GR_DERIVATION",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPD1859_4_no_charge_needed",
            "object": "boundary/no-charge theorem",
            "derivation_or_test": "Q_R=0 plus C_R(infinity)=0 would imply C_R=0 for the current/equation-difference branch",
            "result": "SUFFICIENT_CONDITIONAL",
            "claim_impact": "moves the proof burden to source-neutral boundary or auxiliary elimination",
            "status": "NO_CHARGE_THEOREM_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPD1859_5_direct_phase_volume_verdict",
            "object": "phase-volume parent-origin derivation",
            "derivation_or_test": "Can motion-load/phase-volume alone supply C_R=0 without a parent current, Euler equation, gauge constraint, or no-charge theorem?",
            "result": "NO",
            "claim_impact": "do not promote local GR from the phase-volume story alone",
            "status": "REJECT_DIRECT_PARENT_DERIVATION_CURRENT_CORPUS",
            "valid_for_claim": False,
        },
        {
            "audit_id": "MPD1859_6_best_surviving_route",
            "object": "MTS-owned time/radial equation-difference",
            "derivation_or_test": "derive E_time and E_radial from S_parent, form D_R[MTS]=E_time-E_radial=partial_r C_R-S_R=0, then prove S_R=0 and Q_R=0 on local vacuum/source-balanced branch",
            "result": "BEST_NONCIRCULAR_ROUTE",
            "claim_impact": "more defensible than imposing J_q=1 because it mirrors field-equation logic while forbidding EH import",
            "status": "SELECT_FOR_NEXT_PROOF_CHAIN",
            "valid_for_claim": False,
        },
    ]

    no_go_rows = [
        {
            "no_go_id": "NG1859_0_generic_volume",
            "candidate": "generic four-volume or broad volume preservation",
            "why_it_fails": "selects wrong exponents or is underdetermined; previous audit gives p=1/3 or other non-GR lanes",
            "survives_as": "discarded shortcut",
            "status": "REJECT",
            "valid_for_claim": False,
        },
        {
            "no_go_id": "NG1859_1_liouville",
            "candidate": "canonical Liouville/symplectic phase-volume preservation",
            "why_it_fails": "(T sqrt(S))*(1/(T sqrt(S)))=1 for every p",
            "survives_as": "background consistency only",
            "status": "REJECT_AS_SELECTOR",
            "valid_for_claim": False,
        },
        {
            "no_go_id": "NG1859_2_null_propagation",
            "candidate": "radial null propagation",
            "why_it_fails": "dr/dt=cT/sqrt(S) is defined for any p; it does not force T sqrt(S)=1",
            "survives_as": "readout constraint after metric is known",
            "status": "REJECT_AS_SELECTOR",
            "valid_for_claim": False,
        },
        {
            "no_go_id": "NG1859_3_unimodular_cell",
            "candidate": "impose theta_0 wedge theta_1 equals flat/reference radial cell",
            "why_it_fails": "exactly gives C_R=0, but as an imposed cell determinant it is closure-only unless parent dynamics force it",
            "survives_as": "explicit local closure baseline",
            "status": "CLOSURE_ONLY",
            "valid_for_claim": False,
        },
        {
            "no_go_id": "NG1859_4_ordinary_current",
            "candidate": "conserved radial observer-cell current",
            "why_it_fails": "ordinary conservation preserves Q_R hair instead of setting Q_R=0",
            "survives_as": "finite residual or no-charge theorem target",
            "status": "REJECT_AS_ZERO_PROOF",
            "valid_for_claim": False,
        },
        {
            "no_go_id": "NG1859_5_gauge_noether",
            "candidate": "Noether/gauge language alone",
            "why_it_fails": "Noether identities relate equations after a parent action exists; they do not conjure R_AB=0 from nothing",
            "survives_as": "constraint algebra requirement after parent action is written",
            "status": "REJECT_AS_ORIGIN",
            "valid_for_claim": False,
        },
    ]

    route_rows = [
        {
            "route_id": "FRS1859_0_direct_phase_volume",
            "route": "direct motion-load/phase-volume derivation of J_q=1",
            "best_case": "clean intuitive MTS explanation of reciprocal clock/radial routing",
            "current_blocker": "specific cell preservation is not parent-owned",
            "decision": "DEMOTE_TO_MOTIVATION_OR_CLOSURE",
            "selected": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "FRS1859_1_cell_current_no_charge",
            "route": "radial cell current plus Q_R=0 theorem",
            "best_case": "derives C_R=0 by conservation plus no-charge boundary/source theorem",
            "current_blocker": "current conservation gives Q_R constant; Q_R=0 theorem missing",
            "decision": "HELD_AS_SUBROUTE",
            "selected": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "FRS1859_2_parent_Euler_difference",
            "route": "MTS-owned E_time-E_radial field-equation difference",
            "best_case": "D_R[MTS]=partial_r C_R-S_R=0; local source-balance and boundary/no-charge give C_R=0",
            "current_blocker": "parent Euler pair, source map, boundary class and extra-sector silence are unsigned",
            "decision": "SELECT_PRIMARY",
            "selected": True,
            "valid_for_claim": False,
        },
        {
            "route_id": "FRS1859_3_EH_fixed_point_inheritance",
            "route": "derive local EH fixed point then inherit the GR-style radial difference",
            "best_case": "legitimate inheritance after A511 blocks are parent-signed and extras are silent",
            "current_blocker": "A511 scaffold is not proof; Gamma/Khat/q_loc and other extra sectors leak",
            "decision": "SELECT_AS_PARENT_EULER_BRIDGE",
            "selected": True,
            "valid_for_claim": False,
        },
        {
            "route_id": "FRS1859_4_finite_residual_backstop",
            "route": "retain finite R_AB/q_R residuals and source-bound them",
            "best_case": "testable fallback against R10/PPN/clock/orbital data",
            "current_blocker": "not a derivation of GR; internal coefficients and arena projections missing",
            "decision": "BACKSTOP_ONLY",
            "selected": False,
            "valid_for_claim": False,
        },
    ]

    claim_gate_rows = [
        {
            "gate_id": "CG1859_0_definitions",
            "claim": "J_q and C_R identities are defined",
            "gate_pass": True,
            "reason": "C_R=ln(T^2S)=2ln(J_q) is exact bookkeeping",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1859_1_direct_phase_volume",
            "claim": "motion-load/phase-volume derives local GR reciprocity",
            "gate_pass": False,
            "reason": "specific radial cell preservation is not parent-derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1859_2_current_no_charge",
            "claim": "cell current proves Q_R=0",
            "gate_pass": False,
            "reason": "ordinary current conservation gives Q_R constant, not zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1859_3_equation_difference",
            "claim": "MTS parent Euler difference derives C_R=0",
            "gate_pass": False,
            "reason": "E_time/E_radial/source/boundary/extra-silence certificates remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1859_4_local_GR",
            "claim": "MTS derives local GR/Newton branch",
            "gate_pass": False,
            "reason": "1859 selects the right proof chain but does not close it",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1859_0_phase_volume_result",
            "decision": "reject direct phase-volume as a current parent derivation",
            "because": "it identifies the right condition, but does not supply the parent Euler/constraint/no-charge machinery",
            "consequence": "do not claim local GR from J_q=1 unless it is labelled closure-only or parent-derived later",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1859_1_best_derivation_route",
            "decision": "select parent Euler/source-map equation-difference route",
            "because": "it is less axiom-like than unimodular cell imposition and matches how a serious field theory should earn AB=1",
            "consequence": "attack E_time/E_radial/source/boundary/extra-sector certificates rather than re-running volume arguments",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1859_2_next_blocker",
            "decision": "bridge 1858/1859 into the A511 extra-sector silence chain",
            "because": "1276/1279 show EH/local-GR inheritance is blocked first by unsigned extra-sector silence, especially Gamma_eff/K_hat/q_loc",
            "consequence": "next proof target should attempt GK/q_loc action-existence/Euler/double-zero or retain an explicit residual",
            "valid_for_claim": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1859_0_primary",
            "target_file": "1860-Y5-R2FR-Gamma-Khat-q-loc-action-existence-bridge-to-local-EH-fixed-point.md",
            "target_script": "scripts/Y5_R2FR_Gamma_Khat_qloc_action_existence_bridge_to_local_EH_fixed_point_1860.py",
            "task": "try to close the concrete Gamma_eff/K_hat/q_loc extra-sector silence blocker: action existence, Helmholtz/integrability, Euler closure, double-zero, boundary silence, and readout projection; otherwise retain epsilon_GK_q_loc as an explicit residual",
            "success_condition": "q_loc is parent-zero on the local branch without plateau/closure/EH import, or the residual vector is source-bound and claim-blocked",
            "do_not": "do not use phase-volume closure, A511 EH anchor, or local test success as proof of derived GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1859_1_secondary",
            "target_file": "1860b-Y5-R2FR-parent-Euler-source-map-local-reciprocity-contract.md",
            "target_script": "scripts/Y5_R2FR_parent_Euler_source_map_local_reciprocity_contract_1860b.py",
            "task": "assemble E_time, E_radial, S_R, Q_R and boundary normalization certificates into one R2FR contract after extra-sector silence is narrowed",
            "success_condition": "D_R[MTS]=partial_r C_R-S_R is derived from parent variations or remains closure-only",
            "do_not": "do not copy Einstein equations as MTS equations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    return {
        "source_register": source_rows,
        "derivation_audit": derivation_rows,
        "no_go": no_go_rows,
        "route_selection": route_rows,
        "claim_gate": claim_gate_rows,
        "decision": decision_rows,
        "next_target": next_rows,
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        for dst_dir in [MICROSCOPE_RESIDUALS, QUARANTINE]:
            shutil.copy2(src, dst_dir / src.name)
        shutil.copy2(src, RAB_QUEUE / f"JR1859_{src.name}")


def check_sources(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        if not path.exists():
            missing.append(str(row["source_path"]))
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source paths exist"


def check_needles(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        needle = str(row["needle"])
        if path.exists() and needle not in path.read_text(encoding="utf-8", errors="ignore"):
            missing.append(f"{row['source_path']}::{needle}")
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source needles are present"


def check_csv_parse() -> tuple[bool, str]:
    malformed: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            malformed.append(f"{path.name}: {exc}")
    return not malformed, "malformed: " + "; ".join(malformed) if malformed else "all generated 1859 CSVs parse"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1859_{path.name}",
        ]
        for item in expected:
            if not item.exists():
                missing.append(str(item))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1859_0_sources_exist", ok, detail))
    ok, detail = check_needles(rows_map["source_register"])
    checks.append(("VAL1859_1_needles_present", ok, detail))
    checks.append(
        (
            "VAL1859_2_conditional_identity",
            any(row["audit_id"] == "MPD1859_1_if_Jq_fixed" and row["result"] == "EXACT_CONDITIONAL" for row in rows_map["derivation_audit"]),
            "J_q=1 condition exactly implies C_R=0 and p=1",
        )
    )
    checks.append(
        (
            "VAL1859_3_direct_phase_volume_rejected",
            any(row["audit_id"] == "MPD1859_5_direct_phase_volume_verdict" and row["status"] == "REJECT_DIRECT_PARENT_DERIVATION_CURRENT_CORPUS" for row in rows_map["derivation_audit"]),
            "direct phase-volume parent derivation is rejected for current corpus",
        )
    )
    checks.append(
        (
            "VAL1859_4_no_go_routes_recorded",
            all(any(row["no_go_id"] == no_go_id for row in rows_map["no_go"]) for no_go_id in ["NG1859_1_liouville", "NG1859_4_ordinary_current", "NG1859_5_gauge_noether"]),
            "Liouville/current/Noether no-go rows are present",
        )
    )
    checks.append(
        (
            "VAL1859_5_equation_difference_selected",
            any(row["route_id"] == "FRS1859_2_parent_Euler_difference" and boolish(row["selected"]) for row in rows_map["route_selection"]),
            "parent Euler/source-map equation-difference route selected",
        )
    )
    checks.append(
        (
            "VAL1859_6_claim_gates_safe",
            any(row["gate_id"] == "CG1859_0_definitions" and boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and any(row["gate_id"] == "CG1859_4_local_GR" and not boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and all(not boolish(row["claim_allowed"]) for row in rows_map["claim_gate"]),
            "only definitions pass; local-GR claim remains blocked",
        )
    )
    checks.append(
        (
            "VAL1859_7_next_target_selected",
            any(row["next_id"] == "NEXT1859_0_primary" for row in rows_map["next_target"]),
            "1860 GK/q_loc bridge target selected",
        )
    )
    checks.append(
        (
            "VAL1859_8_no_claim_flags",
            all(not boolish(row.get("valid_for_claim", False)) for rows in rows_map.values() for row in rows),
            "no valid_for_claim flags are true",
        )
    )
    ok, detail = check_csv_parse()
    checks.append(("VAL1859_9_csv_parse", ok, detail))
    ok, detail = check_branch_copies()
    checks.append(("VAL1859_10_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1859_11_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in [
            "*P8_Y5*1859*",
            "*1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation*",
            "*Y5_R2FR_motion_load_phase_volume_parent_origin_no_GR_import_derivation_1859.py",
        ]:
            formalization_outputs.extend(FORMALIZATION.rglob(pattern))
    formalization_detail = (
        "found generated outputs: " + "; ".join(str(path) for path in formalization_outputs)
        if formalization_outputs
        else "no generated 1859 outputs found under formalization-workbench"
    )
    checks.append(("VAL1859_12_formalization_untouched", not formalization_outputs, formalization_detail))
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1859_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1859 motion-load/phase-volume parent-origin no-GR-import derivation attempt",
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1859: Motion-Load Phase-Volume Parent-Origin No-GR-Import Derivation",
            "",
            "**Current verdict:** direct motion-load/phase-volume does not yet derive the local GR reciprocity constraint. It identifies the right condition, `J_q=T sqrt(S)=1`, and that condition exactly gives `C_R=ln(T^2S)=0` and `p=1`. But ordinary phase volume, Liouville preservation, null propagation, cell-current conservation, gauge/Noether language, and unimodular cell imposition all fail as parent derivations in the current corpus. The best surviving route is an MTS-owned time/radial parent Euler difference plus source/boundary/no-charge certificates.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_path", "needle", "role", "status", "valid_for_claim"]),
            "",
            "## Motion-Phase Derivation Audit",
            markdown_table(rows_map["derivation_audit"], ["audit_id", "object", "derivation_or_test", "result", "claim_impact", "status", "valid_for_claim"]),
            "",
            "## No-Go Ledger",
            markdown_table(rows_map["no_go"], ["no_go_id", "candidate", "why_it_fails", "survives_as", "status", "valid_for_claim"]),
            "",
            "## Field-Equation Route Selection",
            markdown_table(rows_map["route_selection"], ["route_id", "route", "best_case", "current_blocker", "decision", "selected", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "consequence", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is progress, not a defeat. We have stopped asking a vague phase-volume principle to do too much. The exact local-GR gate is now: derive parent-owned `E_time` and `E_radial`, prove their difference controls `C_R`, prove the source/residual side vanishes in the local branch, and prevent `Q_R`/boundary/readout hair. The concrete next blocker is the extra-sector silence needed for local EH/Euler inheritance, especially `Gamma_eff/K_hat/q_loc`.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1859 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
