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
DOC_PATH = ROOT / "4034-Y5-R2FR-no-linear-source-leak-proof-or-Qphi-coefficient-fill.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4034_SOURCE_REGISTER.csv",
    "leak_decomposition": SOURCE_DIR / "P8_Y5_R2FR_4034_F_SOURCE_LEAK_DECOMPOSITION.csv",
    "no_linear_gate": SOURCE_DIR / "P8_Y5_R2FR_4034_NO_LINEAR_SOURCE_LEAK_GATE.csv",
    "qphi_coefficients": SOURCE_DIR / "P8_Y5_R2FR_4034_QPHI_COEFFICIENT_FILL.csv",
    "evaluator_cases": SOURCE_DIR / "P8_Y5_R2FR_4034_EVALUATOR_CASES.csv",
    "evaluator_results": SOURCE_DIR / "P8_Y5_R2FR_4034_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4034_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4034_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4034_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4034_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4034_VALIDATION.csv",
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
            "source_id": "SRC4034_0_4033_doc",
            "path": "4033-Y5-R2FR-source-neutral-F-proof-or-alpha-lambda-curve-row.md",
            "needle": "F_source_leak=0",
            "role": "selects no-linear-source-leak as the next obstruction",
        },
        {
            "source_id": "SRC4034_1_4033_decomp",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4033_SOURCE_NEUTRAL_F_DECOMPOSITION.csv",
            "needle": "F_source_leak",
            "role": "defines the retained leak term",
        },
        {
            "source_id": "SRC4034_2_gamma_owner",
            "path": "source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            "needle": "exchange-odd residuals",
            "role": "supports exchange-even quadratic owner route",
        },
        {
            "source_id": "SRC4034_3_gamma_quad",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4026_EXPLICIT_GAMMA_DENSITY_CANDIDATE.csv",
            "needle": "Gamma_quad",
            "role": "provides explicit quadratic Gamma density candidate",
        },
        {
            "source_id": "SRC4034_4_local_action",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4021_PARENT_LOCAL_ACTION_WITNESS.csv",
            "needle": "S_matter[psi,g_obs,theta]",
            "role": "provides same-source local action witness",
        },
        {
            "source_id": "SRC4034_5_source_once",
            "path": "source-intake/mts_residuals/P8_Y5_R2FR_4021_DERIVED_ZERO_LEMMAS.csv",
            "needle": "source is single-counted",
            "role": "supports EM/matter included once in Hilbert source",
        },
        {
            "source_id": "SRC4034_6_EM_flux",
            "path": "source-intake/mts_residuals/P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
            "needle": "Poynting_flux",
            "role": "keeps EM flux/cross-term residuals visible",
        },
        {
            "source_id": "SRC4034_7_odd_warning",
            "path": "source-intake/mts_residuals/P8_ODD_RESIDUAL_COMPONENT_MAP.csv",
            "needle": "matter trace can be exchange-even",
            "role": "prevents overclaiming exchange parity against ordinary matter trace",
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


def build_leak_decomposition(ts: str) -> list[dict[str, object]]:
    return [
        {
            "leak_id": "LEAK4034_0_master",
            "term": "F_source_leak",
            "formula": "F_source_leak=c_T*T_H + c_EM*F_EM^2 + c_Poynting*divS_EM + c_B*B_boundary + c_Z*J_Z + c_norm*Delta_source_norm + c_nonEH*O_nonEH",
            "meaning": "all possible linear source leak channels are explicit coefficients",
            "status": "LEAK_VECTOR_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "leak_id": "LEAK4034_1_matter_trace",
            "term": "c_T*T_H",
            "formula": "ordinary matter trace or Hilbert source coupling directly into F",
            "meaning": "danger channel because matter trace can be exchange-even",
            "status": "RETAINED_UNLESS_SOURCE_DOMAIN_EXCLUSION_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "leak_id": "LEAK4034_2_EM",
            "term": "c_EM*F_EM^2 + c_Poynting*divS_EM",
            "formula": "nonminimal EM cross term or radiative/background Poynting flux outside M_H",
            "meaning": "ordinary bound EM stress belongs in Hilbert source; nonminimal/background flux is retained",
            "status": "PARTLY_CONDITIONAL_PARTLY_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "leak_id": "LEAK4034_3_boundary_odd",
            "term": "c_B*B_boundary + c_Z*J_Z",
            "formula": "exchange-odd boundary/source class charge",
            "meaning": "quadratic exchange route works only if local odd charge is zero",
            "status": "RETAINED_UNTIL_BOUNDARY_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "leak_id": "LEAK4034_4_source_norm",
            "term": "c_norm*Delta_source_norm + c_nonEH*O_nonEH",
            "formula": "source-normalization or non-EH operator contribution after EH/Newton routing",
            "meaning": "feeds measured-GM/Newton/R11 if not zeroed",
            "status": "RETAINED_R11_SOURCE_NORMALIZATION",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_no_linear_gate(ts: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "NLL4034_0_action_separation",
            "clause": "I_Gamma depends on response fields and observed geometry, while ordinary matter/EM enter only S_matter+S_EM+S_binding",
            "current_result": "witness clause exists but is not corpus-adopted",
            "zeroes_coefficients": "c_T,c_EM,c_norm if live-signed",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "NLL4034_1_exchange_even",
            "clause": "Gamma_eff-Gamma0 is exchange-even/quadratic in odd residuals Z, so first variation at Z=0 vanishes",
            "current_result": "best candidate exists; component map not fully parent-owned",
            "zeroes_coefficients": "linear Z source terms",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "NLL4034_2_no_source_only_vertices",
            "clause": "parent object language forbids source-only vertices Z*T_H, Z*F_EM^2, Z*J_H, f(Z)R_matter, and source prefactors",
            "current_result": "not yet proven; main remaining proof obligation",
            "zeroes_coefficients": "c_T,c_EM,c_norm,c_nonEH",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "NLL4034_3_EM_once",
            "clause": "minimal Maxwell stress and bound fields are counted once in T_total; radiative/background Poynting flux is zero or explicitly bounded",
            "current_result": "ordinary EM route conditional; flux/cross coefficients retained",
            "zeroes_coefficients": "ordinary c_EM, not c_Poynting unless stationary/no-flux signed",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "NLL4034_4_boundary",
            "clause": "local exchange-odd boundary/source charge J_Z and B_boundary vanish",
            "current_result": "not proven",
            "zeroes_coefficients": "c_B,c_Z",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "NLL4034_5_if_all_signed",
            "clause": "NLL4034_0 through NLL4034_4 all hold",
            "current_result": "conditional theorem: F_source_leak=0",
            "zeroes_coefficients": "all linear source leak coefficients",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_qphi_coefficients(ts: str) -> list[dict[str, object]]:
    terms = [
        ("QPHIC4034_0_cT", "c_T", "matter trace/Hilbert source", "MISSING_SOURCE_DOMAIN_EXCLUSION_OR_COEFFICIENT"),
        ("QPHIC4034_1_cEM", "c_EM", "nonminimal EM scalar cross term", "MISSING_UNIQUE_EM_ACTION_DOMAIN_OR_COEFFICIENT"),
        ("QPHIC4034_2_cPoynting", "c_Poynting", "radiative/background Poynting flux", "MISSING_STATIONARY_NO_FLUX_OR_FLUX_BOUND"),
        ("QPHIC4034_3_cB", "c_B", "boundary/source class charge", "MISSING_BOUNDARY_ZERO_OR_COEFFICIENT"),
        ("QPHIC4034_4_cZ", "c_Z", "exchange-odd local source current", "MISSING_ODD_CHARGE_ZERO_OR_COEFFICIENT"),
        ("QPHIC4034_5_cnorm", "c_norm", "source-normalization/non-EH residue", "MISSING_R11_SOURCE_NORMALIZATION_ZERO_OR_VECTOR"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, symbol, channel, status in terms:
        rows.append(
            {
                "coefficient_id": row_id,
                "symbol": symbol,
                "channel": channel,
                "Q_phi_contribution": f"(2/3)*{symbol}*I_{symbol}",
                "alpha_lambda_impact": f"alpha_phi += C_alpha_phi*((2/3)*{symbol}*I_{symbol}/M_H)*(q_test/m_test)",
                "current_status": status,
                "score_ready": False,
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def build_evaluator_cases(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4034_0_all_signed",
            "input_condition": "action separation, exchange-even quadratic owner, no source-only vertices, EM once/no flux, boundary odd charge zero",
            "expected_verdict": "NO_LINEAR_SOURCE_LEAK_IF_PARENT_SIGNED",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4034_1_current",
            "input_condition": "current source hierarchy after 4034",
            "expected_verdict": "NO_LINEAR_SOURCE_LEAK_CONDITIONAL_QPHI_COEFFICIENTS_RETAINED",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4034_2_fail",
            "input_condition": "one or more direct/source-only coefficients survives",
            "expected_verdict": "QPHI_COEFFICIENT_VECTOR_REQUIRED",
            "timestamp_utc": ts,
        },
    ]


def build_evaluator_results(ts: str) -> list[dict[str, object]]:
    return [
        {
            "case_id": "CASE4034_0_all_signed",
            "verdict": "NO_LINEAR_SOURCE_LEAK_IF_PARENT_SIGNED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4034",
            "next_action": "then return to fixed-branch/no-flux clauses for Q_phi=0",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4034_1_current",
            "verdict": "NO_LINEAR_SOURCE_LEAK_CONDITIONAL_QPHI_COEFFICIENTS_RETAINED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4034",
            "next_action": "4035 should attack source-only vertex exclusion as the cleanest proof target",
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4034_2_fail",
            "verdict": "QPHI_COEFFICIENT_VECTOR_REQUIRED",
            "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4034",
            "next_action": "fill c_T,c_EM,c_Poynting,c_B,c_Z,c_norm with source paths and units before alpha scoring",
            "timestamp_utc": ts,
        },
    ]


def build_decisions(ts: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC4034_0_proof_route",
            "decision": "no-linear-source-leak can be proven by action-domain separation plus exchange-even quadratic Gamma owner plus no source-only vertices",
            "status": "PROOF_ROUTE_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4034_1_current",
            "decision": "current corpus has conditional support but not live adoption; coefficient vector remains active",
            "status": "PRIVATE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4034_2_poynting",
            "decision": "ordinary EM stress belongs inside total Hilbert source; radiative/background Poynting flux remains a separate coefficient unless stationary no-flux is signed",
            "status": "EM_Poynting_PLACED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4034_3_next",
            "decision": "move to 4035-Y5-R2FR-source-only-vertex-exclusion-or-cT-cEM-fill.md",
            "status": "NEXT_TARGET_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def build_claims(ts: str) -> list[dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4034_0_no_leak",
            "claim": "F_source_leak=0 in the live theory",
            "allowed": False,
            "reason": "source-only vertex exclusion and boundary odd charge zero are not parent-signed",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4034_1_Qphi_zero",
            "claim": "Q_phi=0",
            "allowed": False,
            "reason": "no-linear-leak is conditional and fixed/no-flux clauses remain open",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4034_2_alpha_score",
            "claim": "alpha(lambda) is numerically scoreable",
            "allowed": False,
            "reason": "Q_phi coefficient vector is symbolic and not source-backed",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4034_3_local_GR",
            "claim": "local-GR branch passes",
            "allowed": False,
            "reason": "scalar/source/boundary/adoption gates remain open",
            "timestamp_utc": ts,
        },
    ]


def build_next_target(ts: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "NEXT4034_0",
            "next_doc": "4035-Y5-R2FR-source-only-vertex-exclusion-or-cT-cEM-fill.md",
            "next_script": "scripts/Y5_R2FR_4035_source_only_vertex_exclusion_or_cT_cEM_fill.py",
            "why": "source-only vertices Z*T_H and Z*F_EM^2 are the first concrete leak channels to kill or score",
            "fallback": "if exclusion fails, fill c_T and c_EM first because they dominate scalar charge and WEP/R10 risk",
            "timestamp_utc": ts,
        }
    ]


def build_status(ts: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS4034_0",
            "checkpoint": "4034",
            "headline": "no-linear-source-leak route written; Q_phi coefficient vector retained",
            "verdict": "NO_LINEAR_SOURCE_LEAK_CONDITIONAL_QPHI_COEFFICIENTS_RETAINED",
            "claim_allowed": False,
            "formalization_workbench_modified": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: list[dict[str, object]]) -> str:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    return f"""# 4034 - No Linear Source Leak Proof Or Qphi Coefficient Fill

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

4034 decomposes the leak term:

`F_source_leak=c_T*T_H + c_EM*F_EM^2 + c_Poynting*divS_EM + c_B*B_boundary + c_Z*J_Z + c_norm*Delta_source_norm + c_nonEH*O_nonEH`.

The proof route is now explicit:

1. ordinary matter and EM enter only `S_matter+S_EM+S_binding`;
2. `Gamma_eff-Gamma_0` is exchange-even/quadratic in local residuals;
3. source-only vertices such as `Z*T_H` and `Z*F_EM^2` are forbidden by the parent object language;
4. ordinary EM stress is counted once in the total Hilbert source;
5. radiative/background Poynting flux and boundary odd charge are either zero or scored.

If all clauses are signed, `F_source_leak=0`.

## Current Obstruction

The dangerous terms are now concrete:

`c_T`, `c_EM`, `c_Poynting`, `c_B`, `c_Z`, and `c_norm`.

The largest immediate proof target is source-only vertex exclusion. Matter trace can be exchange-even, so exchange parity alone is not enough.

## Current Verdict

- Current evaluator result: `NO_LINEAR_SOURCE_LEAK_CONDITIONAL_QPHI_COEFFICIENTS_RETAINED`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4034`.
- Source needles found: `{found}/{len(sources)}`.

## Next Target

- `4035-Y5-R2FR-source-only-vertex-exclusion-or-cT-cEM-fill.md`
- `scripts/Y5_R2FR_4035_source_only_vertex_exclusion_or_cT_cEM_fill.py`
"""


def add_validation(rows: list[dict[str, object]], check_id: str, passed: bool, detail: str, ts: str) -> None:
    rows.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": ts})


def build_validation_rows(
    ts: str,
    sources: list[dict[str, object]],
    leaks: list[dict[str, object]],
    gates: list[dict[str, object]],
    coeffs: list[dict[str, object]],
    results: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_target: list[dict[str, object]],
    compile_ok: bool,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    leak_ids = {str(row["leak_id"]) for row in leaks}
    gate_ids = {str(row["gate_id"]) for row in gates}
    coeff_symbols = {str(row["symbol"]) for row in coeffs}
    verdicts = {str(row["verdict"]) for row in results}

    add_validation(rows, "VAL4034_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", ts)
    add_validation(rows, "VAL4034_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found", ts)
    add_validation(rows, "VAL4034_02_master_leak", "LEAK4034_0_master" in leak_ids, "master leak decomposition row present", ts)
    add_validation(rows, "VAL4034_03_matter_trace", "LEAK4034_1_matter_trace" in leak_ids, "matter-trace danger row present", ts)
    add_validation(rows, "VAL4034_04_EM", "LEAK4034_2_EM" in leak_ids, "EM/Poynting leak row present", ts)
    add_validation(rows, "VAL4034_05_action_gate", "NLL4034_0_action_separation" in gate_ids, "action separation gate present", ts)
    add_validation(rows, "VAL4034_06_source_vertex_gate", "NLL4034_2_no_source_only_vertices" in gate_ids, "source-only vertex gate present", ts)
    add_validation(rows, "VAL4034_07_all_signed_gate", "NLL4034_5_if_all_signed" in gate_ids, "all-signed no-leak gate present", ts)
    add_validation(rows, "VAL4034_08_coeffs", {"c_T", "c_EM", "c_Poynting", "c_B", "c_Z", "c_norm"}.issubset(coeff_symbols), "Q_phi coefficient vector complete", ts)
    add_validation(rows, "VAL4034_09_no_score_ready", all(str(row.get("score_ready", "False")) == "False" for row in coeffs), "coefficient rows not score-ready", ts)
    add_validation(rows, "VAL4034_10_current_verdict", "NO_LINEAR_SOURCE_LEAK_CONDITIONAL_QPHI_COEFFICIENTS_RETAINED" in verdicts, "current evaluator verdict present", ts)
    add_validation(rows, "VAL4034_11_no_claims", all(str(row.get("allowed", "False")) == "False" for row in claims), "all claim gates remain false", ts)
    add_validation(rows, "VAL4034_12_next_decision", any("4035" in str(row["decision"]) for row in decisions), "4035 next decision present", ts)
    add_validation(rows, "VAL4034_13_next_target", bool(next_target and "4035" in str(next_target[0]["next_doc"])), "next target row present", ts)
    add_validation(rows, "VAL4034_14_doc_written", DOC_PATH.exists() and "What Actually Moved" in read_text(DOC_PATH), "checkpoint doc written", ts)
    add_validation(rows, "VAL4034_15_no_formalization_output", "formalization-workbench" not in str(DOC_PATH) and all("formalization-workbench" not in str(path) for path in OUTPUTS.values()), "no output targets formalization-workbench", ts)
    add_validation(rows, "VAL4034_16_script_compiles", compile_ok, "script compiles", ts)
    add_validation(rows, "VAL4034_17_private_nonclaim", all(str(row.get("valid_for_claim", "False")) == "False" for row in leaks + gates + coeffs + decisions), "all rows remain nonclaim", ts)
    return rows


def main() -> None:
    ts = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = build_source_register(ts)
    leaks = build_leak_decomposition(ts)
    gates = build_no_linear_gate(ts)
    coeffs = build_qphi_coefficients(ts)
    cases = build_evaluator_cases(ts)
    results = build_evaluator_results(ts)
    decisions = build_decisions(ts)
    claims = build_claims(ts)
    next_target = build_next_target(ts)
    status = build_status(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["leak_decomposition"], leaks)
    write_csv(OUTPUTS["no_linear_gate"], gates)
    write_csv(OUTPUTS["qphi_coefficients"], coeffs)
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

    validation = build_validation_rows(ts, sources, leaks, gates, coeffs, results, decisions, claims, next_target, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4034 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
