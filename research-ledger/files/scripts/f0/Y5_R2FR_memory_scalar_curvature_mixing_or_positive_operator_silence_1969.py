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

DOC_PATH = ROOT / "1969-Y5-R2FR-memory-scalar-curvature-mixing-or-positive-operator-silence.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1969_VALIDATION.csv"

SOURCES = {
    "1968_doc": {
        "path": ROOT / "1968-Y5-R2FR-no-integrated-out-curvature-tower-or-Xi-mixing-coefficient.md",
        "needles": ["XI1968_1_memory_m", "XI1968_4_zero_by_positive_operator", "NEXT1968_0_primary"],
    },
    "1968_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1968_VALIDATION.csv",
        "needles": ["VAL1968_OVERALL", "PASS"],
    },
    "826_parent_action": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
        "needles": ["AA826_1_memory_sector", "AA826_2_trace_projection_lock"],
    },
    "1302_memory_stress": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
        "needles": ["MSR1302_0_canonical_scalar_stress_form", "MSR1302_2_constant_nohair_safe_case", "MSR1302_3_metric_composite_fallback"],
    },
    "967_positive_operator": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
        "needles": ["MPO967_1_operator", "MPO967_3_zero_source", "MPO967_4_energy_identity", "MPO967_6_verdict"],
    },
    "1965_doc": {
        "path": ROOT / "1965-Y5-R2FR-R2-fR-zero-proof-or-executable-R11-bound-row.md",
        "needles": ["SM1965_1_scalar_mass", "ZP1965_6_verdict"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


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
                "purpose": "1969 memory scalar curvature mixing or positive-operator silence",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def memory_derivation_rows() -> list[dict[str, object]]:
    entries = [
        (
            "MEM1969_0_target",
            "derive B_mR and H_m for the memory scalar, or prove the memory scalar cannot generate R2/fR",
            "Delta c_R2[m] ~ -1/2 B_mR H_m^{-1} B_mR",
            "TARGET_EXACT",
            "This is the first concrete hidden-sector coefficient calculation target.",
            "need parent action dependence of Z_m, V_R, X_B, source/bath terms, and boundary",
        ),
        (
            "MEM1969_1_notation_guard",
            "Distinguish Ricci scalar curvature R_geom from the memory response symbol R(m;X_B) used in 826.",
            "B_mR := delta^2 S/(delta m delta R_geom), not derivative of the named memory response R(m;X_B) unless that response is explicitly curvature-valued",
            "NOTATION_GUARD_INSTALLED",
            "Prevents a false R2/fR derivation from overloaded R notation.",
            "keep R_geom and R_mem separate in later files",
        ),
        (
            "MEM1969_2_written_branch_direct_mixing",
            "The written 826 memory kinetic/potential branch has no explicit m R_geom term as written.",
            "L_m=-1/2 Z_m(X_B) grad m grad m - V_R(m;X_B); direct B_mR=0 if Z_m,V_R,X_B,source/bath are curvature-independent",
            "CONDITIONAL_DIRECT_MIXING_ZERO",
            "This is a real partial simplification: the obvious direct curvature-mixing term is absent in the displayed ansatz.",
            "must parent-sign curvature independence of Z_m,V_R,X_B and all hidden terms",
        ),
        (
            "MEM1969_3_hessian",
            "Around a constant local background m_*, the memory Hessian is an elliptic/relativistic scalar operator with mass from V_R'' plus hidden response terms.",
            "H_m approx -nabla_mu(Z_m nabla^mu) + partial_m^2 V_R(m_*;X_B) + Delta H_XB/source/bath/boundary",
            "HESSIAN_TEMPLATE_DERIVED",
            "This gives the denominator for any generated c_R2 coefficient.",
            "need Z_m sign/value, V_R'', X_B response, source/bath/boundary corrections",
        ),
        (
            "MEM1969_4_indirect_mixing_channels",
            "Curvature mixing can re-enter through X_B metric response, curvature dependence of V_R/Z_m, metric-composite m[g,...], source/bath terms, or boundary counterterms.",
            "B_mR = B_direct + B_XB + B_metric_composite + B_source_bath + B_boundary",
            "INDIRECT_MIXING_LIVE",
            "The direct ansatz helps, but does not close the no-tower theorem.",
            "need each B component zeroed or bounded",
        ),
        (
            "MEM1969_5_trace_projection_channel",
            "The 826 trace projection channel may be harmless if the memory response has a local extremum F1=0, but it is not yet a curvature-mixing coefficient proof.",
            "Gamma_eff=L_cg^-2[F_L(X_B)+a_F(R_mem(m;X_B)-R_mem(m_L;X_B))]",
            "CONDITIONAL_EXTREMUM_ROUTE_SEPARATE",
            "Useful for local source suppression, but do not confuse it with Ricci R2/fR unless projection owner maps it to curvature.",
            "derive projection owner and F1=0; keep separate from B_mR",
        ),
        (
            "MEM1969_6_verdict",
            "Memory scalar direct Ricci mixing is conditionally zero in the displayed branch, but total B_mR is not parent-zeroed.",
            "B_direct=0 under assumptions; B_total remains open through X_B/source/bath/boundary/metric-composite channels",
            "PARTIAL_ZERO_TOTAL_MIXING_NOT_CLOSED",
            "Progress: the coefficient problem is narrowed to indirect channels and H_m inputs.",
            "stage B-component ledger and positive-operator silence gate",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, math_form, status, implication, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "math_form": math_form,
                "status": status,
                "implication": implication,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def b_component_rows() -> list[dict[str, object]]:
    entries = [
        (
            "BMR1969_0_direct",
            "B_direct",
            "explicit m R_geom or F(m)R_geom term in L_m",
            "0 if 826 displayed branch is complete and curvature-independent",
            "CONDITIONAL_ZERO",
            "needs parent-completeness certificate",
        ),
        (
            "BMR1969_1_XB_response",
            "B_XB",
            "X_B depends on metric curvature or carries metric response that couples m to R_geom",
            "delta X_B/delta R_geom times partial_m partial_XB L_m",
            "MISSING_XB_METRIC_RESPONSE",
            "1302 already flags X_B metric response missing",
        ),
        (
            "BMR1969_2_metric_composite",
            "B_metric_composite",
            "m=m[g,Phi,D,P] rather than independent scalar",
            "delta m/delta R_geom induced by parent composite definition",
            "MISSING_PARENT_DEFINITION_OF_m",
            "1302 metric-composite fallback remains live",
        ),
        (
            "BMR1969_3_source_bath",
            "B_source_bath",
            "source, bath, or irreversible terms couple memory to curvature/readout",
            "partial_m partial_Rgeom L_source_bath",
            "MISSING_SOURCE_BATH_TERMS",
            "826 warns bath/open-system terms may be required",
        ),
        (
            "BMR1969_4_boundary",
            "B_boundary",
            "boundary/counterterm response couples memory to local curvature",
            "partial_m partial_Rgeom S_boundary",
            "MISSING_BOUNDARY_TERMS",
            "boundary flux/counterterm must be zeroed or retained",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, component, channel, formula, status, note in entries:
        row = base(row_id)
        row.update(
            {
                "component": component,
                "channel": channel,
                "formula": formula,
                "status": status,
                "note": note,
            }
        )
        rows.append(row)
    return rows


def positive_operator_rows() -> list[dict[str, object]]:
    entries = [
        (
            "POS1969_0_operator",
            "H_m positive in the local branch",
            "Z_m>0 and V_R''(m_*;X_B)>=0 or a positive operator L_m with gap/zero-mode control",
            "UNSIGNED_INPUTS",
            "needed for silence and for a healthy scalar coefficient denominator",
        ),
        (
            "POS1969_1_source_silence",
            "J_m=0 in the ordinary compact exterior",
            "no matter vertex, no wall/domain source, no readout source, no bath drive",
            "UNSIGNED_INPUTS",
            "without this the scalar can carry local hair even if B_mR=0",
        ),
        (
            "POS1969_2_boundary",
            "boundary removes flux and zero modes",
            "Dirichlet/zero flux plus zero mean/topological control",
            "UNSIGNED_INPUTS",
            "constant mode must be universal/source-independent or retained",
        ),
        (
            "POS1969_3_curvature_mixing_zero",
            "B_mR=0 for all direct and indirect channels",
            "B_direct+B_XB+B_metric+B_source_bath+B_boundary=0",
            "UNSIGNED_INPUTS",
            "positive operator silence alone does not remove generated R2 if B_mR survives",
        ),
        (
            "POS1969_4_relative_theorem",
            "If POS1969_0..3 pass, memory scalar generates no local R2/fR scalar tower.",
            "H_m positive, J_m=0, boundary silent, B_mR=0 => no scalar pole and no Schur R2 term",
            "RELATIVE_THEOREM_CLEAN",
            "This is the best current theorem route for the memory branch.",
        ),
        (
            "POS1969_5_verdict",
            "Positive-operator memory silence is not parent-signed yet.",
            "POS1969_0..3 unsigned",
            "SILENCE_NOT_CLAIMED",
            "Retain B-component and H_m rows as required inputs.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, math_form, status, implication in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "math_form": math_form,
                "status": status,
                "implication": implication,
            }
        )
        rows.append(row)
    return rows


def coefficient_schema_rows() -> list[dict[str, object]]:
    entries = [
        (
            "MCS1969_0_Hm",
            "memory_hessian",
            "Z_m;V_R_second_derivative;X_B_response_terms;source_bath_terms;boundary_terms;operator_domain;units;source_path",
            "MISSING_H_M_INPUTS",
            "REJECT_FOR_CLAIM",
        ),
        (
            "MCS1969_1_BmR_total",
            "memory_curvature_mixing",
            "B_direct;B_XB;B_metric_composite;B_source_bath;B_boundary;normalization;units;source_path",
            "MISSING_B_MR_COMPONENTS",
            "REJECT_FOR_CLAIM",
        ),
        (
            "MCS1969_2_cR2_memory",
            "generated_memory_coefficient",
            "c_R2_memory=-1/2 B_mR H_m^-1 B_mR;sign;units;validity_scale;locality_regime;source_path",
            "MISSING_C_R2_MEMORY",
            "REJECT_FOR_CLAIM",
        ),
        (
            "MCS1969_3_zero_certificate",
            "memory_no_tower_zero",
            "H_m_positive;J_m_zero;boundary_silent;B_mR_zero;constant_mode_harmless;source_path",
            "MISSING_MEMORY_ZERO_CERTIFICATE",
            "REJECT_FOR_CLAIM",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, row_type, required_fields, missing_now, runner_status in entries:
        row = base(row_id)
        row.update(
            {
                "row_type": row_type,
                "required_fields": required_fields,
                "missing_now": missing_now,
                "runner_status": runner_status,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        ("MRUN1969_0_direct_zero", "BMR1969_0_direct", "PASS_NONCLAIM_CONDITIONAL", "direct mixing zero only if displayed branch is complete and curvature-independent"),
        ("MRUN1969_1_total_B", "MCS1969_1_BmR_total", "REJECTED_MISSING_B_MR_COMPONENTS", "indirect channels remain open"),
        ("MRUN1969_2_Hm", "MCS1969_0_Hm", "REJECTED_MISSING_H_M_INPUTS", "Z_m,V_R'',X_B/source/boundary corrections missing"),
        ("MRUN1969_3_positive_operator", "POS1969_4_relative_theorem", "REJECTED_RELATIVE_ROUTE_UNSIGNED", "operator/source/boundary/B_mR premises missing"),
        ("MRUN1969_VERDICT", "all_rows", "MEMORY_MIXING_PARTIAL_ZERO_TOTAL_BLOCKED_NONCLAIM", "direct branch helps, but total memory no-tower proof is not closed"),
    ]
    rows: list[dict[str, object]] = []
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
        ("CG1969_0_direct_mixing", "Direct memory-Ricci mixing is absent in displayed branch.", "PASS_NONCLAIM", "conditional on branch completeness/curvature independence"),
        ("CG1969_1_total_BmR_zero", "Total B_mR is zero.", "FAIL_BLOCKED", "indirect channels not zeroed"),
        ("CG1969_2_Hm_known", "H_m is parent-sourced and positive.", "FAIL_BLOCKED", "Z_m,V_R'',boundary/source inputs missing"),
        ("CG1969_3_memory_no_tower", "Memory scalar cannot generate R2/fR.", "FAIL_BLOCKED", "positive-operator and B_mR premises unsigned"),
        ("CG1969_4_EH_second_order", "EH second-order premise cleared.", "FAIL_BLOCKED", "memory/no-tower and other R11 families remain"),
        ("CG1969_5_local_GR", "local GR/Newton derived.", "FAIL_BLOCKED", "EH/GM/PPN gates remain"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1969_0_verdict",
            "DIRECT_MEMORY_RICCI_MIXING_CONDITIONALLY_ZERO_TOTAL_MIXING_OPEN",
            "The displayed 826 memory branch does not itself contain an m R_geom term, but X_B response, source/bath, boundary, and metric-composite channels remain open.",
            "do not claim no-tower; audit indirect B_mR components next",
        ),
        (
            "DEC1969_1_best_next",
            "X_B_METRIC_RESPONSE_AND_SOURCE_BATH_AUDIT",
            "The highest-risk indirect terms are exactly the ones 1302 flags as missing: X_B metric response, source/bath terms, and boundary terms.",
            "derive or bound B_XB, B_source_bath, and B_boundary before trying to score c_R2_memory",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1969_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1970-Y5-R2FR-XB-source-bath-boundary-curvature-mixing-audit.md",
            "target_script": "scripts/Y5_R2FR_XB_source_bath_boundary_curvature_mixing_audit_1970.py",
            "objective": "audit indirect memory curvature-mixing channels B_XB, B_source_bath, B_boundary, and metric-composite m[g] response",
            "acceptance_output": "zero certificates or coefficient rows for each indirect B_mR component",
            "nonclaim_rule": "no memory no-tower or EH claim while any indirect B_mR component is missing",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1969_0_project_position")
    row.update(
        {
            "strongest_result": "The displayed memory scalar action has conditional direct B_mR=0 with respect to Ricci curvature; the blocker is now indirect metric/source/bath/boundary mixing.",
            "what_improved": "The memory scalar coefficient target split into concrete B components and H_m inputs.",
            "still_missing": "curvature independence of Z_m/V_R/X_B, X_B metric response, source/bath terms, boundary terms, H_m positivity, J_m silence, full R2/fR bound curve, GM/PPN completion",
            "claim_status": "partial nonclaim simplification only; no memory no-tower/EH/Newton/local-GR claim",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1969_SOURCE_REGISTER.csv",
    "memory_derivation": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1969_MEMORY_DERIVATION.csv",
    "b_components": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1969_BMR_COMPONENT_LEDGER.csv",
    "positive_operator": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1969_POSITIVE_OPERATOR_SILENCE.csv",
    "coefficient_schema": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1969_MEMORY_COEFFICIENT_SCHEMA.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1969_MEMORY_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1969_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1969_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1969_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1969_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MEMORY_SCALAR_MIXING_1969_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1969_INDIRECT_MEMORY_MIXING_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1969_0_nonclaim_weight"),
            "artifact": "1969 memory scalar curvature mixing or positive operator silence",
            "weight": "PARTIAL_DIRECT_ZERO_INDIRECTS_OPEN",
            "reason": "direct curvature mixing absent only conditionally; indirect channels remain open",
        }
    ]
    queue = [
        {
            **base("AQ1969_0_XB_response"),
            "target": "X_B metric/curvature response",
            "needed_inputs": "definition of X_B; delta X_B/delta R_geom; partial_m partial_XB L_m; source path",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1969_1_source_bath_boundary"),
            "target": "source/bath/boundary memory-curvature mixing",
            "needed_inputs": "source terms; bath variables; boundary counterterms; curvature dependence; zero or coefficient",
            "priority": "HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "memory_derivation": memory_derivation_rows(),
        "b_components": b_component_rows(),
        "positive_operator": positive_operator_rows(),
        "coefficient_schema": coefficient_schema_rows(),
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
    patterns = ("1969-", "*_1969_*", "*Y5*1969*", "*VAL1969*", "*P8*1969*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1969_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    notation_ok = any(row["row_id"] == "MEM1969_1_notation_guard" and row["status"] == "NOTATION_GUARD_INSTALLED" for row in tables["memory_derivation"])
    partial_ok = any(row["row_id"] == "MEM1969_6_verdict" and row["status"] == "PARTIAL_ZERO_TOTAL_MIXING_NOT_CLOSED" for row in tables["memory_derivation"])
    rows.append(validation_row("VAL1969_01_memory_derivation", "PASS" if notation_ok and partial_ok else "FAIL", "notation guard and partial direct-zero verdict recorded"))

    direct_ok = any(row["row_id"] == "BMR1969_0_direct" and row["status"] == "CONDITIONAL_ZERO" for row in tables["b_components"])
    indirect_ok = any(row["row_id"] == "BMR1969_1_XB_response" and row["status"] == "MISSING_XB_METRIC_RESPONSE" for row in tables["b_components"])
    rows.append(validation_row("VAL1969_02_B_components", "PASS" if direct_ok and indirect_ok else "FAIL", "direct and indirect B_mR components separated"))

    positive_ok = any(row["row_id"] == "POS1969_4_relative_theorem" and row["status"] == "RELATIVE_THEOREM_CLEAN" for row in tables["positive_operator"])
    silence_not_claimed = any(row["row_id"] == "POS1969_5_verdict" and row["status"] == "SILENCE_NOT_CLAIMED" for row in tables["positive_operator"])
    rows.append(validation_row("VAL1969_03_positive_operator", "PASS" if positive_ok and silence_not_claimed else "FAIL", "positive-operator route retained without claim"))

    schema_ok = any(row["row_id"] == "MCS1969_1_BmR_total" and row["runner_status"] == "REJECT_FOR_CLAIM" for row in tables["coefficient_schema"])
    rows.append(validation_row("VAL1969_04_schema", "PASS" if schema_ok else "FAIL", "memory coefficient schema rejects missing B components"))

    runner_ok = any(row["row_id"] == "MRUN1969_VERDICT" and row["runner_status"] == "MEMORY_MIXING_PARTIAL_ZERO_TOTAL_BLOCKED_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1969_05_runner", "PASS" if runner_ok else "FAIL", "runner blocks memory no-tower claim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1969_4_EH_second_order" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1969_06_claim_gates", "PASS" if gate_ok else "FAIL", "EH/local-GR claims remain blocked"))

    decision_ok = any(row["decision"] == "X_B_METRIC_RESPONSE_AND_SOURCE_BATH_AUDIT" for row in tables["decision"])
    rows.append(validation_row("VAL1969_07_decision", "PASS" if decision_ok else "FAIL", "indirect B_mR audit selected"))

    next_ok = tables["next"][0]["target_doc"] == "1970-Y5-R2FR-XB-source-bath-boundary-curvature-mixing-audit.md"
    rows.append(validation_row("VAL1969_08_next_target", "PASS" if next_ok else "FAIL", "1970 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1969_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1969_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1969_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1969_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1969_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1969_OVERALL", overall, "1969 memory scalar curvature mixing or positive-operator silence"))
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
        ("Memory Derivation", tables["memory_derivation"]),
        ("B_mR Component Ledger", tables["b_components"]),
        ("Positive Operator Silence", tables["positive_operator"]),
        ("Coefficient Schema", tables["coefficient_schema"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1969 Y5 R2FR: Memory Scalar Curvature Mixing Or Positive-Operator Silence",
        "",
        "Private checkpoint. This derives the memory scalar contribution to the `R2/fR` coefficient as far as the current parent ansatz allows.",
        "",
        "Verdict: the displayed 826 memory scalar branch has conditional direct Ricci-mixing zero, because it contains no explicit `m R_geom` term as written. The total memory mixing is not closed because `X_B` metric response, source/bath terms, boundary terms, and metric-composite definitions remain open.",
        "",
        "No R2/fR, EH, Newton, or local-GR claim follows from this checkpoint.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
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
    print(f"VAL1969_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
