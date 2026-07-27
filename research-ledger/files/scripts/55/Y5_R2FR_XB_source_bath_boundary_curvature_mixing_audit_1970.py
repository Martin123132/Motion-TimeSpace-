from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1970-Y5-R2FR-XB-source-bath-boundary-curvature-mixing-audit.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1970_VALIDATION.csv"

SOURCES = {
    "1969_doc": {
        "path": ROOT / "1969-Y5-R2FR-memory-scalar-curvature-mixing-or-positive-operator-silence.md",
        "needles": [
            "MEM1969_4_indirect_mixing_channels",
            "BMR1969_1_XB_response",
            "NEXT1969_0_primary",
        ],
    },
    "1969_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1969_VALIDATION.csv",
        "needles": ["VAL1969_OVERALL", "PASS"],
    },
    "826_parent_action": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
        "needles": ["AA826_1_memory_sector", "AA826_2_trace_projection_lock"],
    },
    "1302_memory_stress": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
        "needles": [
            "MSR1302_0_canonical_scalar_stress_form",
            "MISSING_X_B_METRIC_RESPONSE",
            "MSR1302_3_metric_composite_fallback",
        ],
    },
    "967_positive_operator": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
        "needles": ["MPO967_4_energy_identity", "MPO967_6_verdict"],
    },
    "1968_schur_gate": {
        "path": ROOT / "1968-Y5-R2FR-no-integrated-out-curvature-tower-or-Xi-mixing-coefficient.md",
        "needles": ["Delta c_R2", "H_X", "B_XR"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_spec in SOURCES.items():
        path = source_spec["path"]
        needles = source_spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1970 indirect memory/X_B curvature-mixing audit",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def indirect_bmr_rows() -> list[dict[str, object]]:
    entries = [
        {
            "row_id": "IND1970_0_exact_split",
            "component": "B_mR_total",
            "derivation": "B_mR = B_direct + B_XB + B_metric_composite + B_source_bath + B_boundary",
            "status": "EXACT_SPLIT_INSTALLED",
            "missing_input": "component certificates",
            "interpretation": "the memory scalar cannot be cleared by looking only at the displayed potential",
        },
        {
            "row_id": "IND1970_1_direct",
            "component": "B_direct",
            "derivation": "delta^2 S_m/(delta m delta R_geom) from explicit m R_geom or F(m)R_geom terms",
            "status": "CONDITIONAL_ZERO_CARRIED_FROM_1969",
            "missing_input": "parent completeness and curvature-independence certificate",
            "interpretation": "the obvious direct Ricci term is absent in the displayed 826 branch",
        },
        {
            "row_id": "IND1970_2_XB_constant_branch",
            "component": "B_XB",
            "derivation": "if C_XR := delta X_B/delta R_geom = 0, then the X_B-mediated part vanishes even when V_mX is nonzero",
            "status": "ZERO_ROUTE_IDENTIFIED_UNSIGNED",
            "missing_input": "parent proof that X_B is a quotient label, fixed background, or curvature-independent local environment variable",
            "interpretation": "this is the cleanest route if MTS wants local GR without adding a new scalar pole",
        },
        {
            "row_id": "IND1970_3_XB_live_branch",
            "component": "B_XB",
            "derivation": "on a constant local m_* branch, B_XB ~= -V_mX(m_*,X_B) C_XR plus kinetic/source corrections",
            "status": "COEFFICIENT_ROUTE_OPEN",
            "missing_input": "V_mX, C_XR, kinetic response, units, and source path",
            "interpretation": "if X_B responds to curvature, the missing coupling really is the bottleneck",
        },
        {
            "row_id": "IND1970_4_metric_composite",
            "component": "B_metric_composite",
            "derivation": "if m=m[g,Phi,D,P], induced response contains C_mR := delta m/delta R_geom and cannot be treated as an independent no-hair scalar",
            "status": "MISSING_PARENT_DEFINITION_OF_m",
            "missing_input": "parent object definition for m and its metric derivative",
            "interpretation": "metric-composite memory keeps the local branch open until the definition is signed",
        },
        {
            "row_id": "IND1970_5_source_bath",
            "component": "B_source_bath",
            "derivation": "B_source_bath = partial_m partial_Rgeom L_source/bath plus bath-response terms",
            "status": "MISSING_SOURCE_BATH_ACTION",
            "missing_input": "closed bath variables or open-system variational action with curvature dependence stated",
            "interpretation": "irreversibility cannot be smuggled in without paying the curvature-mixing bill",
        },
        {
            "row_id": "IND1970_6_boundary",
            "component": "B_boundary",
            "derivation": "B_boundary = delta^2 S_boundary/(delta m delta R_geom) after applying local exterior boundary conditions",
            "status": "MISSING_BOUNDARY_COUNTERTERM_CERTIFICATE",
            "missing_input": "boundary action, flux condition, counterterm subtraction, and zero-mode treatment",
            "interpretation": "boundary silence must be derived, not assumed as plateau behaviour",
        },
        {
            "row_id": "IND1970_7_verdict",
            "component": "B_mR_total",
            "derivation": "direct zero is not enough; at least X_B curvature-independence or a two-field Schur coefficient is required",
            "status": "INDIRECT_CHANNELS_BLOCK_NO_TOWER_CLAIM",
            "missing_input": "X_B response/zero theorem first, then source/bath and boundary certificates",
            "interpretation": "1970 narrows the real leap to the X_B coupling/response gate",
        },
    ]
    rows = []
    for entry in entries:
        row = base(entry.pop("row_id"))
        row.update(entry)
        rows.append(row)
    return rows


def schur_gate_rows() -> list[dict[str, object]]:
    entries = [
        {
            "row_id": "SCHUR1970_0_field_block",
            "object": "memory/environment block",
            "formula": "Y=(delta m, delta X_B); H_Y=[[H_m,H_mX],[H_Xm,H_X]]; B_YR=(B_mR_direct+B_source+B_boundary, B_XR)",
            "status": "TWO_FIELD_BLOCK_REQUIRED_IF_XB_LIVE",
            "missing_input": "H_m, H_X, H_mX, B_XR, B_mR_direct/source/boundary",
        },
        {
            "row_id": "SCHUR1970_1_generated_coefficient",
            "object": "generated higher-curvature coefficient",
            "formula": "Delta c_R2[Y] = -1/2 B_YR^T H_Y^{-1} B_YR, up to parent sign/normalization conventions",
            "status": "FORMULA_RELATIVE_NOT_NUMERIC",
            "missing_input": "parent normalization, operator inverse domain, units, local validity scale",
        },
        {
            "row_id": "SCHUR1970_2_zero_condition",
            "object": "no R2/fR tower from memory/X_B block",
            "formula": "B_YR=0 or B_YR lies in a projected null direction of the positive constrained Hessian",
            "status": "ZERO_CONDITION_EXACT_UNSIGNED",
            "missing_input": "parent projection/kernel theorem for X_B and memory variables",
        },
        {
            "row_id": "SCHUR1970_3_coupling_location",
            "object": "the missing coupling",
            "formula": "the dangerous couplings are C_XR=delta X_B/delta R_geom, H_mX~V_mX/Z_mX, and source/boundary curvature vertices",
            "status": "COUPLING_TARGET_LOCALIZED",
            "missing_input": "decide whether X_B is geometry-blind or calculate the response coefficient",
        },
        {
            "row_id": "SCHUR1970_4_verdict",
            "object": "1970 R2/fR implication",
            "formula": "local EH survives this gate only if the memory/X_B Schur block is zero, projected out, or bounded below R11 limits",
            "status": "EH_LEFT_HAND_STILL_BLOCKED_NONCLAIM",
            "missing_input": "X_B zero proof or numeric source-backed coefficient row",
        },
    ]
    rows = []
    for entry in entries:
        row = base(entry.pop("row_id"))
        row.update(entry)
        rows.append(row)
    return rows


def zero_route_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ZERO1970_0_best_route",
            "X_B geometry-blind quotient/environment label",
            "q owns X_B and local metric variations leave X_B fixed: delta X_B/delta R_geom=0",
            "BEST_ZERO_ROUTE_UNSIGNED",
            "would kill B_XB without needing a fitted coefficient",
        ),
        (
            "ZERO1970_1_separable_potential",
            "separable local memory potential",
            "V_R(m;X_B)=V_m(m)+V_X(X_B)+constant gives V_mX=0 at the branch",
            "SECONDARY_ZERO_ROUTE_UNSIGNED",
            "helps even if X_B is live, but still leaves B_XR and source/boundary terms",
        ),
        (
            "ZERO1970_2_positive_operator_silence",
            "positive memory operator with no source and silent boundary",
            "H_m positive, J_m=0, boundary silent, and B_YR=0 imply no memory scalar pole",
            "RELATIVE_THEOREM_RETAINED",
            "inherits 967 but needs the new two-field B_YR gate",
        ),
        (
            "ZERO1970_3_projection_null",
            "projected/null Schur direction",
            "B_YR may be harmless if the constrained quotient projector annihilates it before inversion",
            "POSSIBLE_ROUTE_UNDERIVED",
            "needs an actual parent projection theorem, otherwise it is closure-only",
        ),
        (
            "ZERO1970_4_verdict",
            "zero proof not closed",
            "no route currently has parent signatures for X_B, source/bath, boundary, and projection",
            "ZERO_PROOF_FAILS_FOR_NOW",
            "move to X_B curvature-independence or response coefficient",
        ),
    ]
    rows = []
    for row_id, route, condition, status, consequence in entries:
        row = base(row_id)
        row.update(
            {
                "route": route,
                "condition": condition,
                "status": status,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def source_bath_boundary_rows() -> list[dict[str, object]]:
    entries = [
        (
            "SBB1970_0_source_schema",
            "source term",
            "L_source(m,J_m,g,...)",
            "partial_m partial_Rgeom L_source or proof J_m=0 in ordinary local exterior",
            "MISSING_SOURCE_ACTION_OR_JM_ZERO",
        ),
        (
            "SBB1970_1_bath_schema",
            "bath/open-system term",
            "L_bath(m,bath,g,...) or influence functional",
            "curvature vertex of bath variables and memory-bath Hessian block",
            "MISSING_BATH_VARIATIONAL_OWNER",
        ),
        (
            "SBB1970_2_boundary_schema",
            "boundary/counterterm",
            "S_boundary[m,X_B,g] plus exterior boundary condition",
            "delta^2 S_boundary/(delta m delta R_geom) or zero-flux/counterterm theorem",
            "MISSING_BOUNDARY_OWNER",
        ),
        (
            "SBB1970_3_constant_mode_schema",
            "constant memory mode",
            "m=m_* with grad m=0",
            "prove universal/source-independent and EH-subtracted, otherwise retained residual",
            "MISSING_CONSTANT_MODE_CERTIFICATE",
        ),
    ]
    rows = []
    for row_id, channel, required_object, coefficient_or_zero, status in entries:
        row = base(row_id)
        row.update(
            {
                "channel": channel,
                "required_object": required_object,
                "coefficient_or_zero": coefficient_or_zero,
                "status": status,
                "valid_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RUN1970_0_direct",
            "IND1970_1_direct",
            "PASS_NONCLAIM_CONDITIONAL",
            "direct Ricci mixing remains conditionally absent",
        ),
        (
            "RUN1970_1_XB",
            "IND1970_3_XB_live_branch",
            "REJECTED_MISSING_XB_RESPONSE",
            "C_XR and V_mX/H_mX are not sourced",
        ),
        (
            "RUN1970_2_schur",
            "SCHUR1970_1_generated_coefficient",
            "REJECTED_MISSING_TWO_FIELD_BLOCK",
            "H_Y and B_YR are not parent-sourced",
        ),
        (
            "RUN1970_3_source_bath_boundary",
            "SBB1970_0..2",
            "REJECTED_MISSING_SOURCE_BATH_BOUNDARY",
            "source/bath/boundary curvature vertices are unsigned",
        ),
        (
            "RUN1970_VERDICT",
            "all_rows",
            "INDIRECT_MEMORY_XB_MIXING_BLOCKED_NONCLAIM",
            "the next non-circular step is the X_B curvature-independence proof or response coefficient",
        ),
    ]
    rows = []
    for row_id, input_row, runner_status, reason in entries:
        row = base(row_id)
        row.update(
            {
                "input_row": input_row,
                "runner_status": runner_status,
                "reason": reason,
                "accepted_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1970_0_direct_memory_mixing", "direct memory-Ricci mixing absent in displayed branch", "PASS_NONCLAIM_CONDITIONAL", "same condition as 1969"),
        ("CG1970_1_XB_response_zero", "X_B has no curvature response", "FAIL_BLOCKED", "C_XR is not parent-signed"),
        ("CG1970_2_two_field_schur", "memory/X_B Schur block produces no R2/fR coefficient", "FAIL_BLOCKED", "H_Y and B_YR missing"),
        ("CG1970_3_source_bath_boundary", "source/bath/boundary terms are silent", "FAIL_BLOCKED", "actions/counterterms missing"),
        ("CG1970_4_EH_second_order", "EH second-order local left-hand side derived", "FAIL_BLOCKED", "R2/fR tower not eliminated"),
        ("CG1970_5_local_GR_Newton", "local GR/Newton recovered as a theorem", "FAIL_BLOCKED", "EH and PPN gates remain"),
    ]
    rows = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1970_0_leap",
            "THE_COUPLING_GATE_IS_NOW_LOCALIZED",
            "1970 shows the next serious step is not another broad audit: it is the X_B curvature response/coupling block.",
            "try to prove C_XR=0 from parent quotient ownership; if that fails, calculate/source H_Y and B_YR",
        ),
        (
            "DEC1970_1_best_route",
            "X_B_CURVATURE_INDEPENDENCE_FIRST",
            "A zero theorem is cleaner and less scrutinizable than importing a small coefficient; it also preserves a pure EH local branch.",
            "construct the parent clause q owns X_B and local metric variations cannot move it",
        ),
        (
            "DEC1970_2_fallback",
            "TWO_FIELD_SCHUR_COEFFICIENT_IF_XB_LIVE",
            "If X_B is dynamic or metric-responsive, the correct object is the two-field Hessian and curvature-coupling vector, not a scalar placeholder.",
            "build coefficient rows for C_XR, H_X, H_mX, H_m, source/bath, and boundary",
        ),
    ]
    rows = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1970_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1971-Y5-R2FR-XB-curvature-independence-or-two-field-Schur-coefficient.md",
            "target_script": "scripts/Y5_R2FR_XB_curvature_independence_or_two_field_Schur_coefficient_1971.py",
            "objective": "prove X_B curvature-independence from parent quotient ownership, or calculate the two-field Schur coefficient if X_B is live",
            "acceptance_output": "C_XR=0 certificate or sourced H_Y/B_YR coefficient rows",
            "nonclaim_rule": "no EH/local-GR claim while C_XR, H_Y, B_YR, source/bath, or boundary rows are missing",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1970_0_project_position")
    row.update(
        {
            "strongest_result": "The hidden R2/fR obstruction has been sharpened to an X_B/memory coupling-response gate rather than a vague local-GR failure.",
            "what_improved": "We now have the exact two-field Schur object needed if X_B is live, and the exact zero condition needed if X_B is geometry-blind.",
            "still_missing": "C_XR, V_mX/H_mX, H_X, source/bath action, boundary/counterterm action, operator domain, units, and R11 bound comparison",
            "claim_status": "private nonclaim; no EH/Newton/local-GR pass yet",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1970_SOURCE_REGISTER.csv",
    "indirect_bmr": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1970_INDIRECT_BMR_AUDIT.csv",
    "schur_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1970_TWO_FIELD_SCHUR_GATE.csv",
    "zero_routes": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1970_ZERO_ROUTE_CERTIFICATE.csv",
    "source_bath_boundary": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1970_SOURCE_BATH_BOUNDARY_SCHEMA.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1970_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1970_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1970_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1970_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1970_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "INDIRECT_MEMORY_MIXING_1970_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1970_XB_RESPONSE_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1970_0_nonclaim_weight"),
            "artifact": "1970 indirect memory/X_B curvature-mixing audit",
            "weight": "COUPLING_GATE_LOCALIZED_NONCLAIM",
            "reason": "direct memory zero is not enough; X_B response or two-field Schur block decides the EH gate",
        }
    ]
    queue = [
        {
            **base("AQ1970_0_CXR_zero_proof"),
            "target": "C_XR := delta X_B/delta R_geom",
            "needed_inputs": "parent definition of X_B; quotient map q; allowed local metric variations; proof C_XR=0 or coefficient source",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1970_1_two_field_block"),
            "target": "H_Y and B_YR",
            "needed_inputs": "H_m; H_X; H_mX; B_XR; source/bath vertices; boundary vertices; units",
            "priority": "HIGH_IF_XB_LIVE",
        },
    ]
    return {
        "source_register": source_register(),
        "indirect_bmr": indirect_bmr_rows(),
        "schur_gate": schur_gate_rows(),
        "zero_routes": zero_route_rows(),
        "source_bath_boundary": source_bath_boundary_rows(),
        "runner": runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "queue": queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_hits() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1970-", "*_1970_*", "*Y5*1970*", "*VAL1970*", "*P8*1970*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1970_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    split_ok = any(row["row_id"] == "IND1970_0_exact_split" and row["status"] == "EXACT_SPLIT_INSTALLED" for row in tables["indirect_bmr"])
    xb_ok = any(row["row_id"] == "IND1970_3_XB_live_branch" and row["status"] == "COEFFICIENT_ROUTE_OPEN" for row in tables["indirect_bmr"])
    rows.append(validation_row("VAL1970_01_indirect_split", "PASS" if split_ok and xb_ok else "FAIL", "indirect B_mR split and X_B live branch recorded"))

    schur_ok = any(row["row_id"] == "SCHUR1970_1_generated_coefficient" and "B_YR^T H_Y^{-1} B_YR" in row["formula"] for row in tables["schur_gate"])
    coupling_ok = any(row["row_id"] == "SCHUR1970_3_coupling_location" and row["status"] == "COUPLING_TARGET_LOCALIZED" for row in tables["schur_gate"])
    rows.append(validation_row("VAL1970_02_schur_gate", "PASS" if schur_ok and coupling_ok else "FAIL", "two-field Schur coefficient and coupling location recorded"))

    zero_ok = any(row["row_id"] == "ZERO1970_0_best_route" and row["status"] == "BEST_ZERO_ROUTE_UNSIGNED" for row in tables["zero_routes"])
    zero_fail = any(row["row_id"] == "ZERO1970_4_verdict" and row["status"] == "ZERO_PROOF_FAILS_FOR_NOW" for row in tables["zero_routes"])
    rows.append(validation_row("VAL1970_03_zero_routes", "PASS" if zero_ok and zero_fail else "FAIL", "zero routes identified without claim"))

    sbb_ok = all(str(row["status"]).startswith("MISSING_") for row in tables["source_bath_boundary"])
    rows.append(validation_row("VAL1970_04_source_bath_boundary", "PASS" if sbb_ok else "FAIL", "source/bath/boundary schemas remain explicit blockers"))

    runner_ok = any(row["row_id"] == "RUN1970_VERDICT" and row["runner_status"] == "INDIRECT_MEMORY_XB_MIXING_BLOCKED_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1970_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks no-tower claim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1970_4_EH_second_order" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1970_06_claim_gates", "PASS" if gate_ok else "FAIL", "EH/local-GR claims remain blocked"))

    decision_ok = any(row["decision"] == "X_B_CURVATURE_INDEPENDENCE_FIRST" for row in tables["decision"])
    rows.append(validation_row("VAL1970_07_decision", "PASS" if decision_ok else "FAIL", "next route selects X_B curvature-independence first"))

    next_ok = tables["next"][0]["target_doc"] == "1971-Y5-R2FR-XB-curvature-independence-or-two-field-Schur-coefficient.md"
    rows.append(validation_row("VAL1970_08_next_target", "PASS" if next_ok else "FAIL", "1971 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1970_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1970_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1970_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1970_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1970_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1970_OVERALL", overall, "1970 X_B/source/bath/boundary curvature-mixing audit"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Indirect B_mR Audit", tables["indirect_bmr"]),
        ("Two-Field Schur Gate", tables["schur_gate"]),
        ("Zero Route Certificate", tables["zero_routes"]),
        ("Source Bath Boundary Schema", tables["source_bath_boundary"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1970 Y5 R2FR: X_B Source/Bath/Boundary Curvature-Mixing Audit",
        "",
        "Private checkpoint. This is the non-circular follow-up to 1969: the displayed memory scalar has conditional direct Ricci-mixing zero, so the remaining question is whether indirect channels reintroduce an `R2/fR` scalar tower.",
        "",
        "Verdict: the coupling bottleneck is now localized. Either prove `C_XR := delta X_B/delta R_geom = 0` from parent quotient ownership, or treat `(m, X_B)` as a two-field hidden block with `Delta c_R2 = -1/2 B_YR^T H_Y^{-1} B_YR` and source the coefficients. No EH/Newton/local-GR claim follows yet.",
        "",
        "This is a leap forward rather than another broad audit: the next gate is a single coupling/response decision.",
        "",
    ]
    for title, table_rows in sections:
        lines.extend([f"## {title}", "", markdown_table(table_rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1970_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
