from __future__ import annotations

import csv
import hashlib
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main\post-checkpoint-work"
)
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4035-Y5-R2FR-source-only-vertex-exclusion-or-cT-cEM-fill.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4035_SOURCE_REGISTER.csv",
    "normal_form": SOURCE_DIR / "P8_Y5_R2FR_4035_SOURCE_ONLY_VERTEX_NORMAL_FORM.csv",
    "exclusion_gate": SOURCE_DIR / "P8_Y5_R2FR_4035_SOURCE_ONLY_VERTEX_EXCLUSION_GATE.csv",
    "ct_cem_fill": SOURCE_DIR / "P8_Y5_R2FR_4035_cT_cEM_COEFFICIENT_FILL.csv",
    "evaluator_cases": SOURCE_DIR / "P8_Y5_R2FR_4035_EVALUATOR_CASES.csv",
    "evaluator_results": SOURCE_DIR / "P8_Y5_R2FR_4035_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4035_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4035_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4035_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4035_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4035_VALIDATION.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def short_hash(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "SRC4035_0_4034_doc",
            "path": "4034-Y5-R2FR-no-linear-source-leak-proof-or-Qphi-coefficient-fill.md",
            "needle": "source-only vertices",
            "role": "selects source-only vertex exclusion as next target",
        },
        {
            "source_id": "SRC4035_1_4034_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4034_NO_LINEAR_SOURCE_LEAK_GATE.csv",
            "needle": "NLL4034_2_no_source_only_vertices",
            "role": "upstream source-only vertex gate",
        },
        {
            "source_id": "SRC4035_2_4034_coeffs",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4034_QPHI_COEFFICIENT_FILL.csv",
            "needle": "c_EM",
            "role": "upstream c_T/c_EM coefficient rows",
        },
        {
            "source_id": "SRC4035_3_normal_form",
            "path": "source-intake/mts_residuals/P8_EM_vq_parent_object_language_normal_form_candidate.csv",
            "needle": "S_A[psi_A,Qvis,theta_A,A_obs]",
            "role": "typed matter normal form forbidding private source slots",
        },
        {
            "source_id": "SRC4035_4_no_source_functor",
            "path": "source-intake/mts_residuals/P8_EM_no_source_only_matter_functor_residual.csv",
            "needle": "source-only active coupling",
            "role": "existing no-source-only residual audit",
        },
        {
            "source_id": "SRC4035_5_min_action",
            "path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "needle": "S_matter[psi, g_obs]",
            "role": "minimal parent action block with universal matter",
        },
        {
            "source_id": "SRC4035_6_EM_flux",
            "path": "source-intake/mts_residuals/P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
            "needle": "nonminimal_MTS_EM_cross_term",
            "role": "keeps EM cross-term coefficient visible",
        },
        {
            "source_id": "SRC4035_7_matter_trace_warning",
            "path": "source-intake/mts_residuals/P8_ODD_RESIDUAL_COMPONENT_MAP.csv",
            "needle": "matter trace can be exchange-even",
            "role": "prevents exchange-parity-only overclaim",
        },
    ]


def build_source_register(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        full = ROOT / spec["path"]
        text = read_text(full)
        rows.append(
            {
                **spec,
                "absolute_path": str(full),
                "exists": full.exists(),
                "needle_found": spec["needle"] in text,
                "sha256_16": short_hash(full),
                "timestamp_utc": ts,
            }
        )
    return rows


def build_normal_form(ts: str) -> list[dict[str, object]]:
    return [
        {
            "rule_id": "NF4035_0_action_domain",
            "rule": "S_total=S_EH[g_obs]+I_Gamma[g_obs,Z,R_even,D]+S_matter[psi,Qvis,theta]+S_EM[A,Qvis,J]+S_binding+dB",
            "forbids": "post-readout source labels or fitted source weights entering the action domain",
            "kills": "late source-only scalar couplings",
            "status": "NORMAL_FORM_WRITTEN_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "rule_id": "NF4035_1_matter_functor",
            "rule": "S_matter=sum_A S_A[psi_A,Qvis,theta_A,A_obs]",
            "forbids": "Z*T_A, Z*L_matter, w_A(Z)S_A, species-dependent private source prefactors",
            "kills": "c_T from ordinary matter trace if live-signed",
            "status": "CONDITIONAL_VERTEX_EXCLUSION",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "rule_id": "NF4035_2_EM_functor",
            "rule": "S_EM=-(1/(4*mu0))int F wedge *obs F + int A wedge J with no hidden multiplier",
            "forbids": "Z*F_EM^2, f_Z(Phi)F_EM^2, independent EM action multiplier, hidden Hodge source slot",
            "kills": "ordinary c_EM if unique EM owner/live observed Hodge are signed",
            "status": "CONDITIONAL_EM_VERTEX_EXCLUSION",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "rule_id": "NF4035_3_gamma_owner",
            "rule": "I_Gamma is even/quadratic in response fields Z and may depend on Qvis but not on T_H or F_EM^2 as source objects",
            "forbids": "linear response-source vertices that would turn ordinary stress into scalar charge",
            "kills": "linear Z-source terms, not every source-normalization residual",
            "status": "CONDITIONAL_GAMMA_DOMAIN_RULE",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "rule_id": "NF4035_4_readout_firewall",
            "rule": "PPN/R10/orbital readouts occur after variation and cannot re-enter I_Gamma or S_matter as source selectors",
            "forbids": "calibrated-GM/source-mask feedback into the parent action",
            "kills": "source-only post-fit vertices",
            "status": "FIREWALL_RULE_DEFINED_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_exclusion_gate(ts: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "VX4035_0_typed_domain",
            "clause": "visible matter/EM actions are typed over Qvis only, not hidden response variables Z",
            "current_result": "normal form exists, parent signing missing",
            "sets_to_zero": "c_T,c_EM from direct source-only vertices",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "VX4035_1_no_Hom",
            "clause": "Hom_parent(Z_source_slot, MatterActionScalar)=0 and Hom_parent(Z_source_slot, EMActionScalar)=0 except common constants already in Qvis",
            "current_result": "no-Hom theorem not proven",
            "sets_to_zero": "Z*T_H and Z*F_EM^2 vertices",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "VX4035_2_Gamma_domain",
            "clause": "I_Gamma uses response variables and geometry, not matter/EM Lagrangian densities as independent source arguments",
            "current_result": "candidate route only",
            "sets_to_zero": "c_T,c_EM inside F_source_leak",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "VX4035_3_EM_unique_owner",
            "clause": "Maxwell action has one observed Hodge/normalization owner; nonminimal hidden F^2 terms are absent",
            "current_result": "ordinary EM stress conditional; nonminimal C_XF2 retained",
            "sets_to_zero": "ordinary c_EM only; C_XF2 remains if not excluded",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "VX4035_4_trace_warning",
            "clause": "exchange parity alone is insufficient because ordinary matter trace can be exchange-even",
            "current_result": "guard active",
            "sets_to_zero": "nothing by itself",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "VX4035_5_if_signed",
            "clause": "VX4035_0 through VX4035_3 hold with the trace warning respected",
            "current_result": "conditional theorem: c_T=c_EM=0 for source-only vertices",
            "sets_to_zero": "c_T,c_EM direct vertices",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_ct_cem_fill(ts: str) -> list[dict[str, object]]:
    return [
        {
            "coefficient_id": "CT4035_0",
            "symbol": "c_T",
            "vertex": "Z*T_H or gamma*T_H",
            "zero_theorem": "typed matter functor plus no-Hom source slot exclusion",
            "if_not_zero": "Q_phi_T=(2/3)c_T int_W T_H dV",
            "units_required": "units making c_T*T_H match F=Gamma_eff-Gamma0",
            "first_score_link": "alpha_phi_T=C_alpha_phi*(Q_phi_T/M_H)*(q_test/m_test)",
            "current_status": "MISSING_PARENT_NO_HOM_OR_NUMERIC_COEFFICIENT",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "coefficient_id": "CEM4035_0",
            "symbol": "c_EM",
            "vertex": "Z*F_EM^2 or gamma*F_EM^2",
            "zero_theorem": "unique observed Maxwell owner plus hidden-visible EM vertex exclusion",
            "if_not_zero": "Q_phi_EM=(2/3)c_EM int_W F_EM^2 dV",
            "units_required": "units making c_EM*F_EM^2 match F=Gamma_eff-Gamma0",
            "first_score_link": "alpha_phi_EM=C_alpha_phi*(Q_phi_EM/M_H)*(q_test/m_test)",
            "current_status": "MISSING_EM_VERTEX_EXCLUSION_OR_NUMERIC_COEFFICIENT",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "coefficient_id": "CEM4035_1_flux",
            "symbol": "c_Poynting",
            "vertex": "radiative/background Poynting flux through collar boundary",
            "zero_theorem": "stationary isolated local branch with no net external/background flux",
            "if_not_zero": "Q_phi_flux=(2/3)c_Poynting int_dt int_boundary S_EM.n dA",
            "units_required": "flux-window normalization relative to M_H and F",
            "first_score_link": "time/radial source hair plus possible alpha(lambda) if finite-range scalar response is sourced",
            "current_status": "DEFERRED_AFTER_cT_cEM",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_cases(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4035_0_all_signed",
            "input_condition": "typed Qvis matter/EM domain, no-Hom theorem, Gamma domain separation, unique EM owner",
            "expected_verdict": "SOURCE_ONLY_VERTICES_EXCLUDED_IF_PARENT_SIGNED",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4035_1_current",
            "input_condition": "current source hierarchy after 4035",
            "expected_verdict": "VERTEX_EXCLUSION_CONDITIONAL_cT_cEM_RETAINED",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4035_2_fail",
            "input_condition": "source-only vertices allowed or no-Hom theorem fails",
            "expected_verdict": "cT_cEM_NUMERIC_FILL_REQUIRED",
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_results(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4035_0_all_signed",
            "verdict": "SOURCE_ONLY_VERTICES_EXCLUDED_IF_PARENT_SIGNED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4035",
            "next_action": "then move to c_Poynting/boundary odd charge and source-current closure",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4035_1_current",
            "verdict": "VERTEX_EXCLUSION_CONDITIONAL_cT_cEM_RETAINED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4035",
            "next_action": "4036 should prove the no-Hom/source-slot theorem or fill c_T,c_EM units",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4035_2_fail",
            "verdict": "cT_cEM_NUMERIC_FILL_REQUIRED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4035",
            "next_action": "source c_T and c_EM before any Q_phi/alpha(lambda) score",
            "timestamp_utc": ts,
        },
    ]


def build_decisions(ts: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC4035_0_proof",
            "decision": "source-only vertices are excluded by typed parent object-language plus no-Hom theorem, if parent-signed",
            "status": "PROOF_ROUTE_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4035_1_guard",
            "decision": "exchange parity alone is not enough; matter trace can be exchange-even, so typed-domain exclusion is required",
            "status": "OVERCLAIM_GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4035_2_coefficients",
            "decision": "c_T and c_EM are now first-fill coefficients if the theorem fails",
            "status": "FALLBACK_SCORING_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4035_3_next",
            "decision": "move to 4036-Y5-R2FR-no-Hom-source-slot-theorem-or-cT-cEM-units.md",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_claims(ts: str) -> list[dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4035_0_vertices_excluded",
            "claim": "source-only vertices are excluded in the live parent action",
            "allowed": False,
            "reason": "normal form and no-Hom theorem are conditional, not parent-signed",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4035_1_cT_cEM_zero",
            "claim": "c_T=c_EM=0",
            "allowed": False,
            "reason": "zero follows only if source-slot exclusion and unique EM owner are signed",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4035_2_Qphi_zero",
            "claim": "Q_phi=0",
            "allowed": False,
            "reason": "c_T/c_EM plus remaining flux/boundary/source clauses are still open",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4035_3_local_GR",
            "claim": "local-GR branch passes",
            "allowed": False,
            "reason": "source-only vertex exclusion is conditional and not all local-GR gates are closed",
            "timestamp_utc": ts,
        },
    ]


def build_next_target(ts: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "NEXT4035_0",
            "next_doc": "4036-Y5-R2FR-no-Hom-source-slot-theorem-or-cT-cEM-units.md",
            "next_script": "scripts/Y5_R2FR_4036_no_Hom_source_slot_theorem_or_cT_cEM_units.py",
            "why": "no-Hom/source-slot theorem is the exact parent-language clause needed to turn c_T,c_EM off",
            "fallback": "if no-Hom fails, assign units and source paths for c_T,c_EM coefficient rows",
            "timestamp_utc": ts,
        }
    ]


def build_status(ts: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS4035_0",
            "checkpoint": "4035",
            "headline": "source-only vertex exclusion route written; c_T/c_EM retained as first-fill coefficients",
            "verdict": "VERTEX_EXCLUSION_CONDITIONAL_cT_cEM_RETAINED",
            "claim_allowed": False,
            "formalization_workbench_modified": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: list[dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    return f"""# 4035 - Source Only Vertex Exclusion Or cT cEM Fill

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

4035 attacks the first two source-leak coefficients:

`c_T` from `Z*T_H` or `gamma*T_H`, and `c_EM` from `Z*F_EM^2` or `gamma*F_EM^2`.

The clean theorem route is a typed parent normal form:

`S_total=S_EH[g_obs]+I_Gamma[g_obs,Z,R_even,D]+S_matter[psi,Qvis,theta]+S_EM[A,Qvis,J]+S_binding+dB`.

If matter and EM are functors only of `Qvis`, and if there is no parent morphism from hidden/source slots into matter or EM action scalars, then source-only vertices are forbidden.

## Guardrail

Exchange parity alone is not enough. Ordinary matter trace can be exchange-even. The proof needs typed-domain/source-slot exclusion, not just "odd things vanish".

## If The Theorem Fails

The first coefficient rows are:

- `Q_phi_T=(2/3)c_T int_W T_H dV`;
- `Q_phi_EM=(2/3)c_EM int_W F_EM^2 dV`.

Those feed `alpha_phi(lambda)` and source-WEP rows before any R10/local-GR claim.

## Current Verdict

- Current evaluator result: `VERTEX_EXCLUSION_CONDITIONAL_cT_cEM_RETAINED`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4035`.
- Source needles found: `{found}/{len(sources)}`.

## Next Target

- `4036-Y5-R2FR-no-Hom-source-slot-theorem-or-cT-cEM-units.md`
- `scripts/Y5_R2FR_4036_no_Hom_source_slot_theorem_or_cT_cEM_units.py`
"""


def add_validation(rows: list[dict[str, object]], check_id: str, passed: bool, detail: str, ts: str) -> None:
    rows.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts})


def build_validation_rows(
    ts: str,
    sources: list[dict[str, object]],
    normal: list[dict[str, object]],
    gates: list[dict[str, object]],
    coeffs: list[dict[str, object]],
    results: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_target: list[dict[str, object]],
    compile_ok: bool,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    normal_ids = {str(row["rule_id"]) for row in normal}
    gate_ids = {str(row["gate_id"]) for row in gates}
    coeff_ids = {str(row["coefficient_id"]) for row in coeffs}
    verdicts = {str(row["verdict"]) for row in results}

    add_validation(rows, "VAL4035_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", ts)
    add_validation(rows, "VAL4035_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found", ts)
    add_validation(rows, "VAL4035_02_action_domain", "NF4035_0_action_domain" in normal_ids, "action normal form row present", ts)
    add_validation(rows, "VAL4035_03_matter_functor", "NF4035_1_matter_functor" in normal_ids, "matter functor row present", ts)
    add_validation(rows, "VAL4035_04_EM_functor", "NF4035_2_EM_functor" in normal_ids, "EM functor row present", ts)
    add_validation(rows, "VAL4035_05_noHom", "VX4035_1_no_Hom" in gate_ids, "no-Hom gate present", ts)
    add_validation(rows, "VAL4035_06_trace_guard", "VX4035_4_trace_warning" in gate_ids, "matter trace guard present", ts)
    add_validation(rows, "VAL4035_07_all_signed", "VX4035_5_if_signed" in gate_ids, "all-signed vertex gate present", ts)
    add_validation(rows, "VAL4035_08_cT", "CT4035_0" in coeff_ids, "c_T fill row present", ts)
    add_validation(rows, "VAL4035_09_cEM", "CEM4035_0" in coeff_ids, "c_EM fill row present", ts)
    add_validation(rows, "VAL4035_10_no_score_ready", all(str(row.get("score_ready", "False")) == "False" for row in coeffs), "coefficient rows are not score-ready", ts)
    add_validation(rows, "VAL4035_11_current_verdict", "VERTEX_EXCLUSION_CONDITIONAL_cT_cEM_RETAINED" in verdicts, "current evaluator verdict present", ts)
    add_validation(rows, "VAL4035_12_no_claims", all(str(row.get("allowed", "False")) == "False" for row in claims), "all claim gates remain false", ts)
    add_validation(rows, "VAL4035_13_next_decision", any("4036" in str(row["decision"]) for row in decisions), "4036 next decision present", ts)
    add_validation(rows, "VAL4035_14_next_target", bool(next_target and "4036" in str(next_target[0]["next_doc"])), "next target row present", ts)
    add_validation(rows, "VAL4035_15_doc_written", DOC_PATH.exists() and "What Actually Moved" in read_text(DOC_PATH), "checkpoint doc written", ts)
    add_validation(rows, "VAL4035_16_no_formalization_output", "formalization-workbench" not in str(DOC_PATH) and all("formalization-workbench" not in str(path) for path in OUTPUTS.values()), "no output targets formalization-workbench", ts)
    add_validation(rows, "VAL4035_17_script_compiles", compile_ok, "script compiles", ts)
    add_validation(rows, "VAL4035_18_private_nonclaim", all(str(row.get("valid_for_claim", "False")) == "False" for row in normal + gates + coeffs + decisions), "all rows remain nonclaim", ts)
    return rows


def main() -> None:
    ts = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = build_source_register(ts)
    normal = build_normal_form(ts)
    gates = build_exclusion_gate(ts)
    coeffs = build_ct_cem_fill(ts)
    cases = build_evaluator_cases(ts)
    results = build_evaluator_results(ts)
    decisions = build_decisions(ts)
    claims = build_claims(ts)
    next_target = build_next_target(ts)
    status = build_status(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["normal_form"], normal)
    write_csv(OUTPUTS["exclusion_gate"], gates)
    write_csv(OUTPUTS["ct_cem_fill"], coeffs)
    write_csv(OUTPUTS["evaluator_cases"], cases)
    write_csv(OUTPUTS["evaluator_results"], results)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(ts, sources, normal, gates, coeffs, results, decisions, claims, next_target, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4035 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
