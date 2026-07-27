from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_GK_STRESS_SILENCE_AND_LOCAL_METRIC_EQUATION_GATE_2469"
CHECKPOINT_ID = "2469"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2469-Y5-R2FR-GK-stress-silence-and-local-metric-equation-gate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_GK_STRESS_2469_SOURCE_REGISTER.csv",
    "stress_exposure": OUT / "P8_Y5_GK_STRESS_2469_STRESS_EXPOSURE.csv",
    "stealth_branch": OUT / "P8_Y5_GK_STRESS_2469_STEALTH_BRANCH_CONDITIONS.csv",
    "metric_gate": OUT / "P8_Y5_GK_STRESS_2469_LOCAL_METRIC_EQUATION_GATE.csv",
    "ppn_residual": OUT / "P8_Y5_GK_STRESS_2469_PPN_RESIDUAL_LEDGER.csv",
    "promotion_verdict": OUT / "P8_Y5_GK_STRESS_2469_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_GK_STRESS_2469_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_GK_STRESS_2469_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_GK_STRESS_2469_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_GK_STRESS_2469_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2469_VALIDATION.csv",
}

COPY_TARGETS = {
    "stress_silence_contract": LOCAL_BOUNDS / "GK_stress_silence_contract_2469_NONCLAIM.csv",
    "ppn_residual_ledger": LOCAL_BOUNDS / "GK_PPN_residual_ledger_2469_NONCLAIM.csv",
    "stealth_branch_queue": QUEUE / "JR2469_GK_STEALTH_BRANCH_REQUIREMENTS_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2469_00_2468_doc",
        "source_path": ROOT / "2468-Y5-R2FR-stationary-local-source-theorem-or-dynamic-exchange-current.md",
        "needles": ["PRF2468_4_projected_q_zero", "SCP2468_1_GK_stress", "NEXT2468_0_selected", "VAL2468_OVERALL"],
        "role": "handoff showing q_loc zero but stress gate open",
    },
    {
        "source_id": "SRC2469_01_2468_scope",
        "source_path": OUT / "P8_Y5_STATIONARY_SOURCE_2468_SCOPE_LIMITS.csv",
        "needles": ["SCP2468_1_GK_stress", "q_loc=0 does not imply T_GK"],
        "role": "machine-readable stress blocker",
    },
    {
        "source_id": "SRC2469_02_2465_stress",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2465_STRESS_TENSOR_EXPOSURE.csv",
        "needles": ["STR2465_0_metric_variation_exists", "STR2465_4_GR_limit_gate", "q_loc Euler equation alone is not enough"],
        "role": "initial stress tensor exposure",
    },
    {
        "source_id": "SRC2469_03_2464_candidate_action",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2464_CANDIDATE_ACTIONS.csv",
        "needles": ["ACT2464_A_vertical_generator_current_law", "L_K", "L_Gamma"],
        "role": "candidate GK action whose stress must be tested",
    },
    {
        "source_id": "SRC2469_04_2465_variation",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2465_VARIATION_AUDIT.csv",
        "needles": ["VAR2465_2_delta_A_bulk", "VAR2465_4_delta_Gamma_bulk", "NONCLAIM"],
        "role": "A and Gamma variation equations",
    },
    {
        "source_id": "SRC2469_05_2468_exterior",
        "source_path": OUT / "P8_Y5_STATIONARY_SOURCE_2468_EXTERIOR_QLOC_RESULT.csv",
        "needles": ["EXT2468_0_stationary_q_zero", "EXT2468_1_F1_zero", "EXT2468_4_claim_limit"],
        "role": "stationary exterior q_loc/F1 result",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {"timestamp_utc": stamp(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append({**base_row(), "source_id": source["source_id"], "source_path": str(path), "exists": exists, "missing_needles": ";".join(missing), "source_pass": exists and not missing, "role": source["role"]})
    return rows


def stress_exposure_rows() -> list[dict[str, Any]]:
    rows = [
        ("STR2469_0_definition", "T_GK^{mu nu}=-(2/sqrt(-g))delta S_GK/delta g_mu_nu", "metric variation of ACT2464_A", "stress object exists symbolically", "PASS_AS_FORMAL_DEFINITION"),
        ("STR2469_1_LK", "T_K from L_K(g,tau,nabla A)", "explicit metric contractions and covariant derivative dependence", "generically nonzero if nabla A or A modes are present", "EXPOSED_NONZERO_RISK"),
        ("STR2469_2_AGamma", "T_{A Gamma} from A_nu nabla^nu Gamma_eff", "metric raises derivative/index and sqrt(-g)", "generically nonzero if A or grad Gamma persists", "EXPOSED_NONZERO_RISK"),
        ("STR2469_3_AJ", "T_{AJ} from -A_nu J_M^nu", "source coupling and metric dependence of J_M", "zero in exterior only if J_M=0 and A does not enter hidden source readout", "CONDITIONAL_ZERO"),
        ("STR2469_4_LGamma", "T_Gamma from L_Gamma(Gamma_eff,g,tau)", "potential/gap/vacuum energy term", "acts like local cosmological/stress term unless vacuum value and derivative are fixed", "EXPOSED_VACUUM_ENERGY_RISK"),
        ("STR2469_5_improvement_boundary", "boundary/improvement stress from integrations by parts", "well-posed variational principle", "can leak into local metric unless boundary terms fixed or bounded", "MISSING_BOUNDARY_STRESS"),
        ("STR2469_6_key_lesson", "q_loc=0 constrains Euler residual, not all field amplitudes", "homogeneous GK modes can carry stress", "stress silence needs a vacuum/stealth branch, not just current-law silence", "PASS_RED_TEAM"),
    ]
    return [{**base_row(), "stress_id": i, "stress_component": comp, "basis": basis, "local_effect": effect, "status": st} for i, comp, basis, effect, st in rows]


def stealth_branch_rows() -> list[dict[str, Any]]:
    rows = [
        ("STL2469_0_source_exterior", "J_M=0 outside compact stationary source", "from 2468 stationary theorem", "available condition", "CONDITIONAL_INPUT"),
        ("STL2469_1_q_zero", "q_loc=0 in exterior", "from 2468", "removes force-current residual", "CONDITIONAL_INPUT"),
        ("STL2469_2_field_vacuum", "A_nu=0 or pure gauge, nabla_mu A_nu=0, Gamma_eff=Gamma_0 with nabla Gamma=0", "strong stealth/vacuum branch", "makes L_K and A.Gamma stress vanish", "REQUIRED_NOT_DERIVED"),
        ("STL2469_3_potential_minimum", "dL_Gamma/dGamma|Gamma_0=0 and L_Gamma(Gamma_0)=0 or absorbed into fixed cosmological term", "avoid vacuum energy/local cosmological stress", "needed for metric silence", "REQUIRED_NOT_DERIVED"),
        ("STL2469_4_positive_gap", "L_K/L_Gamma have positive energy/gap so boundary zero selects the trivial exterior mode", "excludes homogeneous hair", "needed for uniqueness/no-hair", "REQUIRED_NOT_DERIVED"),
        ("STL2469_5_boundary_no_hair", "stationary exterior boundary data forbids incoming GK hair/topological modes", "prevents q_loc=0 but T_GK!=0 solutions", "needed for local PPN safety", "REQUIRED_NOT_DERIVED"),
        ("STL2469_6_conditional_result", "If STL2469_0-5 hold, T_GK^{mu nu}=0 or pure fixed Lambda in the local exterior", "conditional stress-silence theorem", "would let metric equation reduce to GR locally", "CONDITIONAL_CONTRACT_ONLY"),
    ]
    return [{**base_row(), "stealth_id": i, "condition": cond, "basis": basis, "effect": effect, "status": st} for i, cond, basis, effect, st in rows]


def metric_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("MET2469_0_parent_metric_equation", "E_GR^{mu nu}=8piG T_matter^{mu nu}+T_GK^{mu nu}+T_tau/P^{mu nu}+boundary", "generic local metric equation", "extra sector stress appears unless silenced", "FORMAL_GATE"),
        ("MET2469_1_stationary_exterior", "Outside matter, T_matter=0 and q_loc=0", "2468 theorem", "metric still differs from GR if T_GK or projector/tau stress survives", "BLOCKED_UNTIL_STRESS_SILENCE"),
        ("MET2469_2_stealth_reduction", "If T_GK=0 and other retained sector stresses vanish/bound, local metric equation reduces to vacuum GR plus fixed Lambda", "stealth branch", "conditional GR exterior route", "CONDITIONAL_CONTRACT_ONLY"),
        ("MET2469_3_current_corpus", "Current corpus does not prove T_GK=0", "missing explicit L_K/L_Gamma/gap/boundary/no-hair", "local GR/PPN not promoted", "BLOCKED_CURRENT_CLAIM"),
        ("MET2469_4_next_mathematical_target", "derive energy positivity/no-hair for GK exterior modes", "needed to turn q_loc=0 into T_GK=0", "next step must attack vacuum branch", "SELECT_NEXT"),
    ]
    return [{**base_row(), "metric_gate_id": i, "statement": s, "basis": b, "effect": e, "status": st} for i, s, b, e, st in rows]


def ppn_residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("PPN2469_0_residual_source", "delta G^{mu nu}=T_GK^{mu nu}+T_tau/P^{mu nu}+boundary", "local metric residual source", "PPN deviations source", "FORMAL_LEDGER"),
        ("PPN2469_1_q_zero_not_enough", "q_loc=0 removes current residual but not homogeneous stress", "stationary q theorem", "PPN residual can remain", "BLOCKED"),
        ("PPN2469_2_hair_bound", "||delta g_PPN|| <= C_metric ||T_GK+T_tau/P+boundary||", "linearized metric response", "requires stress norm and Green function scale", "BOUND_FORM_ONLY"),
        ("PPN2469_3_stealth_pass", "If stealth branch gives T_GK=0 and other sector stresses zero/bounded below arena limits, PPN residual passes conditionally", "conditional exterior branch", "not current claim", "CONDITIONAL_ONLY"),
        ("PPN2469_4_empirical_needed_later", "R10/PPN/clocks/orbital tests need numeric stress residual coefficients", "future empirical gate", "not ready until L_K/L_Gamma fixed", "DEFER_NUMERIC_TEST"),
    ]
    return [{**base_row(), "ppn_id": i, "residual": r, "basis": b, "effect": e, "status": st} for i, r, b, e, st in rows]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("PV2469_0_stress_exposed", "Is the GK stress gate now explicit?", "YES", "stress components and risks listed", "progress"),
        ("PV2469_1_q_zero_to_stress_zero", "Does q_loc=0 imply T_GK=0?", "NO", "homogeneous GK modes/vacuum energy can carry stress", "do not overclaim"),
        ("PV2469_2_conditional_stealth", "Is there a clean conditional stress-silence route?", "YES_CONDITIONAL", "trivial/gapped vacuum branch plus no-hair boundary would silence T_GK", "contract only"),
        ("PV2469_3_current_local_GR", "Does current MTS pass local GR/PPN?", "NO", "stealth/no-hair/gap and explicit stress tensor not derived", "blocked"),
        ("PV2469_4_overall", "Overall 2469 verdict", "STRESS_GATE_SHARPENED_STEALTH_CONTRACT_WRITTEN_NOT_PROMOTED", "next target is GK vacuum/no-hair positivity", "continue derivation"),
    ]
    return [{**base_row(), "verdict_id": i, "question": q, "result": r, "evidence": e, "effect": eff} for i, q, r, e, eff in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2469_0_stress_exposure", "GK stress tensor exposure is written.", "PASS_AS_AUDIT", "symbolic stress components identified", True, False),
        ("GATE2469_1_conditional_stealth", "A conditional stress-silence branch is stated.", "PASS_AS_CONTRACT", "requires vacuum/gap/no-hair hypotheses", True, False),
        ("GATE2469_2_current_stress_silence", "Current corpus proves T_GK=0 in local exterior.", "BLOCKED", "explicit stress/no-hair/gap branch missing", False, False),
        ("GATE2469_3_PPN_GR", "PPN/local GR branch passes.", "BLOCKED", "stress residual not yet zero or bounded numerically", False, False),
        ("GATE2469_4_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", True, False),
    ]
    return [{**base_row(), "gate_id": i, "claim": c, "gate_status": st, "reason": r, "gate_pass": gp, "claim_allowed": ca} for i, c, st, r, gp, ca in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2469_0_no_q_to_stress_shortcut", "Reject q_loc=0 => T_GK=0 as a shortcut.", "Euler residual silence is weaker than stress silence", "keeps local GR route honest"),
        ("DEC2469_1_keep_stealth_contract", "Keep the stealth/no-hair branch as the right next contract.", "it is the least-scrutiny path to local GR: source exterior plus vacuum uniqueness", "next work targets no-hair/positivity"),
        ("DEC2469_2_no_claim", "Do not claim local GR/PPN.", "current corpus lacks explicit stress tensor and no-hair proof", "private nonclaim status retained"),
    ]
    return [{**base_row(), "decision_id": i, "decision": d, "reason": r, "effect": e} for i, d, r, e in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2469_0_selected",
            "selection_status": "selected",
            "target_file": "2470-Y5-R2FR-GK-vacuum-no-hair-positivity-or-stress-bound.md",
            "target_script": "scripts/Y5_R2FR_GK_vacuum_no_hair_positivity_or_stress_bound_2470.py",
            "task": "derive or reject a GK vacuum/no-hair positivity theorem showing stationary exterior q_loc=0 selects trivial stress, or else build the stress-bound fallback",
            "acceptance_target": "candidate L_K/L_Gamma positivity clauses, boundary no-hair proof attempt, stress residual bound form, and claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["stealth_branch"], COPY_TARGETS["stress_silence_contract"])
    shutil.copyfile(OUTPUTS["ppn_residual"], COPY_TARGETS["ppn_residual_ledger"])
    shutil.copyfile(OUTPUTS["stealth_branch"], COPY_TARGETS["stealth_branch_queue"])
    source_map = {
        "stress_silence_contract": OUTPUTS["stealth_branch"],
        "ppn_residual_ledger": OUTPUTS["ppn_residual"],
        "stealth_branch_queue": OUTPUTS["stealth_branch"],
    }
    return [{**base_row(), "copy_id": cid, "source_path": str(source_map[cid]), "target_path": str(target), "source_exists": source_map[cid].exists(), "target_exists": target.exists()} for cid, target in COPY_TARGETS.items()]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    add("VAL2469_00_sources_exist", all(row["source_pass"] is True or str(row["source_pass"]) == "True" for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2469_01_stress_exposed", any(row["stress_id"] == "STR2469_0_definition" for row in data["stress"]), "GK stress definition exposed")
    add("VAL2469_02_q_not_stress", any(row["stress_id"] == "STR2469_6_key_lesson" and row["status"] == "PASS_RED_TEAM" for row in data["stress"]), "q_loc zero not treated as stress zero")
    add("VAL2469_03_stealth_conditions", any(row["stealth_id"] == "STL2469_6_conditional_result" and row["status"] == "CONDITIONAL_CONTRACT_ONLY" for row in data["stealth"]), "conditional stress-silence branch written")
    add("VAL2469_04_metric_blocked", any(row["metric_gate_id"] == "MET2469_3_current_corpus" and row["status"] == "BLOCKED_CURRENT_CLAIM" for row in data["metric"]), "current local metric claim blocked")
    add("VAL2469_05_ppn_bound_form", any(row["ppn_id"] == "PPN2469_2_hair_bound" and row["status"] == "BOUND_FORM_ONLY" for row in data["ppn"]), "PPN residual bound form written")
    add("VAL2469_06_overall_nonclaim", any(row["verdict_id"] == "PV2469_4_overall" and row["result"] == "STRESS_GATE_SHARPENED_STEALTH_CONTRACT_WRITTEN_NOT_PROMOTED" for row in data["verdicts"]), "overall verdict is nonclaim")
    add("VAL2469_07_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR/PPN claim")
    add("VAL2469_08_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2469_0_selected", "2470 no-hair/positivity target selected")
    add("VAL2469_09_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2469-Y5", "P8_Y5_GK_STRESS_2469", "P8_Y5_BRR545_2469", "JR2469")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2469_10_no_formalization_artifacts", not formal_hits, "no 2469 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2469_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2469_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2469_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2469_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2469_OVERALL", all(row["status"] == "PASS" for row in rows), "2469 exposes GK stress, writes conditional stealth contract, and keeps local GR blocked pending no-hair/positivity")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2469 Y5 R2FR GK Stress Silence And Local Metric Equation Gate",
        "",
        "**Status:** stress gate sharpened, not closed. The stationary source theorem gives exterior `q_loc=0`, but that only silences a current residual. It does not automatically silence the stress carried by `A`, `Gamma_eff`, `K_hat`, boundary terms, or vacuum energy.",
        "",
        "**Main result:** a clean conditional route now exists: if the exterior GK sector sits on a genuine trivial/gapped vacuum branch with no homogeneous hair, then `T_GK^{mu nu}=0` or a fixed absorbed Lambda and the local metric equation can reduce to GR. Current MTS does not yet prove those no-hair/positivity conditions, so the GR/PPN claim remains blocked.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Stress Exposure",
        markdown_table(data["stress"], ["stress_id", "stress_component", "basis", "local_effect", "status"]),
        "",
        "## Stealth Branch Conditions",
        markdown_table(data["stealth"], ["stealth_id", "condition", "basis", "effect", "status"]),
        "",
        "## Local Metric Equation Gate",
        markdown_table(data["metric"], ["metric_gate_id", "statement", "basis", "effect", "status"]),
        "",
        "## PPN Residual Ledger",
        markdown_table(data["ppn"], ["ppn_id", "residual", "basis", "effect", "status"]),
        "",
        "## Promotion Verdict",
        markdown_table(data["verdicts"], ["verdict_id", "question", "result", "evidence", "effect"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register(),
        "stress": stress_exposure_rows(),
        "stealth": stealth_branch_rows(),
        "metric": metric_gate_rows(),
        "ppn": ppn_residual_rows(),
        "verdicts": promotion_verdict_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["stress_exposure"], data["stress"])
    write_csv(OUTPUTS["stealth_branch"], data["stealth"])
    write_csv(OUTPUTS["metric_gate"], data["metric"])
    write_csv(OUTPUTS["ppn_residual"], data["ppn"])
    write_csv(OUTPUTS["promotion_verdict"], data["verdicts"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
