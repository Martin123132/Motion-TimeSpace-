from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3893"
BRANCH = "MTS_R2FR_Y5_MEMORY_R11_FACTORIZATION_OR_BOUNDARY_PROJECTOR_NUMERIC_SOURCE_FILL_3893"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3893-Y5-R2FR-memory-R11-factorization-or-boundary-projector-numeric-source-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3892_NEXT = OUT / "P8_Y5_R2FR_3892_NEXT_TARGET.csv"
CSV_3892_FILL = OUT / "P8_Y5_R2FR_3892_ALPHA3_PROJECTOR_NUMERIC_FILL_ROWS.csv"
CSV_3892_GATE = OUT / "P8_Y5_R2FR_3892_LOCAL_GR_DECISION_GATE.csv"
CSV_3892_VALIDATION = OUT / "P8_Y5_BRR545_3892_VALIDATION.csv"
CSV_MEM_OWNER = OUT / "P8_Y5_MEMORY_OWNER_GATE_2626_PARENT_MEMORY_OPERATOR_OWNER_AUDIT.csv"
CSV_MEM_POS = OUT / "P8_Y5_MEMORY_OWNER_GATE_2626_POSITIVE_OPERATOR_ZERO_THEOREM_ATTEMPT.csv"
CSV_MEM_JX = OUT / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_JX_COMPONENT_ZERO_GATE.csv"
CSV_MEM_BOUND = OUT / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv"
CSV_DZ_R11_MAP = OUT / "P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv"
CSV_DZ_R11_PARENT = OUT / "P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv"
CSV_3886_R11 = OUT / "P8_Y5_R2FR_3886_R11_FAMILY_SELECTOR_OR_FILL_MATRIX.csv"
CSV_3887_YLOC = OUT / "P8_Y5_R2FR_3887_YLOC_COMPONENT_CLOSURE_MATRIX.csv"
CSV_3890_INSERT = OUT / "P8_Y5_R2FR_3890_PARENT_ACTION_GRAMMAR_INSERTION.csv"
CSV_3891_LOCK = OUT / "P8_Y5_R2FR_3891_RESIDUAL_LOCK_MAP.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3893_SOURCE_REGISTER.csv",
    "memory": OUT / "P8_Y5_R2FR_3893_MEMORY_SILENCE_THEOREM_OR_BOUND.csv",
    "r11": OUT / "P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv",
    "fill": OUT / "P8_Y5_R2FR_3893_NUMERIC_SOURCE_FILL_QUEUE.csv",
    "gate": OUT / "P8_Y5_R2FR_3893_LOCAL_GR_DECISION_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3893_RUNNER_UPDATE.csv",
    "next": OUT / "P8_Y5_R2FR_3893_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3893_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3893_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3893_00_next", CSV_3892_NEXT, "NEXT3892_0", "3892 selected memory/R11 target"),
    ("SRC3893_01_fill", CSV_3892_FILL, "AF3892_0_alpha3_boundary", "boundary/projector numeric formulas"),
    ("SRC3893_02_gate", CSV_3892_GATE, "LGG3892_5_local_GR", "3892 local-GR gate"),
    ("SRC3893_03_validation", CSV_3892_VALIDATION, "VAL3892_14_next_target", "3892 validation"),
    ("SRC3893_04_mem_owner", CSV_MEM_OWNER, "MOA2626_9_verdict", "memory operator owner audit"),
    ("SRC3893_05_mem_pos", CSV_MEM_POS, "ZPT2626_1_energy_identity", "memory positive-operator theorem"),
    ("SRC3893_06_mem_jx", CSV_MEM_JX, "JX2627_6_total_verdict", "memory source component zero gate"),
    ("SRC3893_07_mem_bound", CSV_MEM_BOUND, "RBP2627_4_local_projection", "memory finite residual bound pack"),
    ("SRC3893_08_R11_map", CSV_DZ_R11_MAP, "nonlocal_memory_kernel", "R11 family mapping"),
    ("SRC3893_09_R11_parent", CSV_DZ_R11_PARENT, "C2_R11_factorization", "R11 parent clause"),
    ("SRC3893_10_R11_3886", CSV_3886_R11, "R11F3886_07_nonlocal_memory_kernel", "3886 R11 matrix"),
    ("SRC3893_11_Yloc_3887", CSV_3887_YLOC, "YLC3887_5_nonlocal_memory", "3897 Yloc memory component"),
    ("SRC3893_12_3890_action", CSV_3890_INSERT, "INS3890_0_action", "candidate parent action grammar"),
    ("SRC3893_13_3891_lock", CSV_3891_LOCK, "RLM3891_4_memory", "memory residual retained"),
]

MEMORY_IDENTITY = "int_D (A^ij grad_i X grad_j X + m_X^2 X^2) = int_D X J_X + boundary_X"
MEMORY_ZERO = "If X is parent-owned, A^ij>0, m_X^2+lambda_1(D)>0 after gauge/zero-mode removal, J_X=0, and boundary_X=0, then X=0 and K_history is locally silent"
R11_ACTION = "S_R11^3893 = int sqrt(-g_obs) Sigma_loc(Y)^2? no: int sqrt(-g_obs) Sigma_loc(Y) sum_F c_F O_F[g_obs,Psi] + S_top"
R11_ZERO = "Because Sigma_loc=G_AB Y^A Y^B and delta Sigma_loc=0 at Y=0, every finite non-topological R11 term multiplied by Sigma_loc has zero first variation on the local-zero branch"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        cells = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_memory_R11_factorization_or_numeric_fill",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def memory_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("MEM3893_0_identity", "positive memory operator identity", MEMORY_IDENTITY, "RELATIVE_THEOREM_READY", "operator owner/sign/source/boundary inputs unsigned"),
        ("MEM3893_1_zero", "compact-local memory silence", MEMORY_ZERO, "PASS_IF_ALL_INPUTS_SIGNED_ONLY", "current corpus lacks X owner, sign/gap, J_X=0, boundary zero and projection maps"),
        ("MEM3893_2_JX_split", "memory source split", "J_X=J_kin_affine+J_matter+J_obs+J_chi_wall+J_boundary+J_history", "SOURCE_SPLIT_RETAINED", "J_boundary and J_history remain not derived zero"),
        ("MEM3893_3_constant", "constant-mode exception", "if m_X=0 and zero mode not removed, X may be a universal constant calibration rather than zero", "EXCEPTION_RETAINED", "must prove universality/source independence or bound drift"),
        ("MEM3893_4_bound", "finite memory residual bound", "||X|| <= (||J_X||+boundary_lift_norm)/lambda_gap; Delta O_i <= K_i||X||+K_i_grad||grad X||", "BOUND_FORMULA_READY_NONCLAIM", "all numeric/source inputs missing"),
        ("MEM3893_5_verdict", "memory status", "memory silence is not activated; it remains theorem-zero if inputs sign, otherwise finite residual to score", "NO_MEMORY_CLAIM", "Gdot/clock/R10/PPN memory rows remain active"),
    ]
    return [
        {
            "memory_id": row_id,
            "piece": piece,
            "statement_or_math": statement,
            "status": status,
            "remaining_failure": failure,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, failure in raw_rows
    ]


def r11_rows(timestamp: str) -> list[dict[str, object]]:
    source_rows = read_csv_rows(CSV_DZ_R11_MAP)
    rows = [
        {
            "r11_id": "R11S3893_00_candidate_action",
            "operator_family": "ALL_NONTOPOLOGICAL_R11",
            "candidate_factorized_form": R11_ACTION,
            "candidate_branch_status": "SIGNED_IN_3893_CANDIDATE_ACTION",
            "local_zero_effect": R11_ZERO,
            "remaining_failure": "requires Y_loc=0 and finite operator coefficients; topological/boundary escapes still need certificates",
            "candidate_branch_signed": True,
            "global_corpus_adopted": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    for index, source in enumerate(source_rows):
        family = source["operator_family"]
        if family in {"boundary_topological_terms", "projector_domain_stress"}:
            status = "REQUIRES_3892_CERTIFICATE_OR_FILL"
            failure = "not killed by generic Sigma factor unless boundary/projector component is included in Yloc or topological certificate signs"
        else:
            status = "CANDIDATE_SIGMA_FACTOR_SIGNED"
            failure = "still requires Y_loc=0; if Yloc/memory source fails, fill numeric coefficients"
        rows.append(
            {
                "r11_id": f"R11S3893_{index+1:02d}_{family}",
                "operator_family": family,
                "candidate_factorized_form": source["candidate_factorized_form"],
                "candidate_branch_status": status,
                "local_zero_effect": "delta[Sigma_loc c_F O_F]=0 on Y_loc=0 branch" if status == "CANDIDATE_SIGMA_FACTOR_SIGNED" else "certificate_or_fill_required",
                "remaining_failure": failure,
                "candidate_branch_signed": status == "CANDIDATE_SIGMA_FACTOR_SIGNED",
                "global_corpus_adopted": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def fill_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("SRCF3893_0_memory_gap", "lambda_gap;m_X^2;lambda_1(D)", "1/length^2", "memory positive operator", "source parent operator sign/gap or retain finite memory residual", "MISSING_A_MIN;MISSING_LAMBDA1_D;MISSING_MX2"),
        ("SRCF3893_1_memory_source", "||J_X|| components", "operator-normalized source units", "memory source", "source J_kin,J_matter,J_boundary,J_history or theorem-zero each", "MISSING_COMPONENT_NORMS"),
        ("SRCF3893_2_memory_projection", "K_R10;K_PPN;K_clock;K_Gdot;K_orbital;K_WEP", "arena-specific", "memory observable map", "map ||X|| bound to each arena", "MISSING_PROJECTION_COEFFICIENTS"),
        ("SRCF3893_3_boundary_alpha3", "c_B_flux_to_alpha3;epsilon_B_flux_abs", "dimensionless", "boundary alpha3", "abs(c_B_flux_to_alpha3*epsilon_B_flux_abs)<=4e-20", "MISSING_BOUNDARY_PRODUCT"),
        ("SRCF3893_4_projector_PPN", "P_PPN[T_extra_munu^Pi]", "dimensionless_vector", "projector PPN", "each gamma,beta,alpha_i,xi,zeta_i component below bound", "MISSING_PROJECTOR_COMPONENT_MAP"),
        ("SRCF3893_5_R11_gamma_beta", "C_gamma^F;c_F;C_beta^F", "dimensionless", "R11 weak-field", "gamma and beta rows pass individually", "MISSING_R11_WEAK_FIELD_COEFFICIENTS"),
        ("SRCF3893_6_R10_range", "K_X(lambda);Q_X^H;q_X^test;alpha_bound(lambda)", "range-dependent", "R10/R11 finite range", "abs(alpha_pred(lambda))<=alpha_bound(lambda)", "MISSING_SOURCE_CHARGES_AND_BOUND_CURVE"),
    ]
    return [
        {
            "fill_id": row_id,
            "needed_input": needed,
            "units": units,
            "residual_channel": channel,
            "pass_rule": rule,
            "current_input_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, needed, units, channel, rule, status in raw_rows
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("LGG3893_0_memory_identity", "memory positive-operator identity", MEMORY_IDENTITY, "PASS_RELATIVE_THEOREM"),
        ("LGG3893_1_memory_zero", "memory theorem-zero", MEMORY_ZERO, "FAIL_INPUTS_UNSIGNED"),
        ("LGG3893_2_R11_factorization", "universal R11 Sigma factorization", R11_ACTION, "PASS_CANDIDATE_BRANCH_NONCLAIM"),
        ("LGG3893_3_R11_local_zero", "R11 first variation zero", R11_ZERO, "PASS_IF_YLOC_ZERO"),
        ("LGG3893_4_boundary_projector", "boundary/projector certificates", "3892 certificates or fill rows required", "FAIL_OPEN"),
        ("LGG3893_5_numeric_fill", "numeric source fill queue", "memory, boundary, projector, R11 and R10 rows emitted", "PASS_QUEUE_READY_NONCLAIM"),
        ("LGG3893_6_local_GR", "local-GR promotion", "memory zero or bounds plus R11, boundary/projector, residual-lock all close", "BLOCKED_NO_CLAIM"),
    ]
    return [
        {
            "gate_id": row_id,
            "gate": gate,
            "requirement": req,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, req, status in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3893_0_memory", "memory_zero_guard", "do not set K_history or X to zero unless owner, sign/gap, J_X and boundary gates all pass", "NO_MEMORY_SHORTCUT"),
        ("RUNU3893_1_R11", "R11_sigma_guard", "R11 operators are candidate Sigma-selected, but they vanish only on the proven Y_loc=0 branch", "NO_R11_WITHOUT_YLOC"),
        ("RUNU3893_2_fill", "source_fill", "if memory/R11/boundary/projector certificates fail, fill emitted numeric inputs with source paths", "QUEUE_READY"),
        ("RUNU3893_3_claim", "local_GR_claim", "false until all remaining gates pass or bounded residuals beat local locks", "NO_LOCAL_GR_CLAIM"),
        ("RUNU3893_4_next", "next_attack", "attempt parent ownership/sign/gap/JX closure for memory; otherwise start numeric source acquisition", "NEXT_3894"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, status in raw_rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3893_0",
            "target_checkpoint": "3894-Y5-R2FR-memory-parent-owner-gap-JX-closure-or-numeric-source-acquisition.md",
            "script": "scripts/Y5_R2FR_3894_memory_parent_owner_gap_JX_closure_or_numeric_source_acquisition.py",
            "objective": "try to parent-own the memory operator X, prove positive sign/gap and J_X/boundary zero; if that fails, begin numeric source acquisition for memory, boundary, projector, R11 and R10 fill inputs",
            "why_next": "3893 candidate-signs universal R11 Sigma factorization, so memory activation and numeric source inputs are now the main non-closed local-GR blockers",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3893_0",
            "branch": BRANCH,
            "summary": "R11 Sigma factorization inserted into candidate branch; memory silence remains a relative positive-operator theorem with unsigned owner/sign/JX/boundary inputs; numeric source fill queue emitted",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    memory: list[dict[str, object]],
    r11: list[dict[str, object]],
    fill: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3893 - Memory/R11 Factorization or Boundary/Projector Numeric Source Fill

Generated: `{timestamp}`

## Result

3893 separates two different issues.

Memory identity:

`{MEMORY_IDENTITY}`

Memory zero theorem:

`{MEMORY_ZERO}`

R11 candidate action:

`{R11_ACTION}`

R11 zero theorem:

`{R11_ZERO}`

The useful win is R11 factorization: in the candidate branch, ordinary non-topological R11 operators are now explicitly Sigma-selected. The hard failure remains memory activation: the positive operator identity is good mathematics, but the current branch still lacks the parent owner, sign/gap, source-zero, boundary-zero, and projection coefficients needed to use it as local-GR evidence.

## Memory Silence Theorem or Bound

{markdown_table(memory, ["memory_id", "piece", "statement_or_math", "status", "remaining_failure"])}

## R11 Sigma Factorization Insertion

{markdown_table(r11, ["r11_id", "operator_family", "candidate_factorized_form", "candidate_branch_status", "local_zero_effect", "remaining_failure"])}

## Numeric Source Fill Queue

{markdown_table(fill, ["fill_id", "needed_input", "units", "residual_channel", "pass_rule", "current_input_status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "requirement", "status", "claim_allowed"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

R11 is no longer just floating as a vague open family in the candidate branch: it has a Sigma-selected parent-action home. But that does not promote local GR until `Y_loc=0` is actually activated. The most concrete remaining derivation target is now memory parent ownership plus sign/gap/source/boundary zero; otherwise the numeric fill queue becomes the honest path.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3893 MEMORY R11 FACTORIZATION -->"
    end = "<!-- END 3893 MEMORY R11 FACTORIZATION -->"
    block = f"""{start}

## 3893 - Memory positive theorem and R11 Sigma factorization

Memory zero theorem:

`{MEMORY_ZERO}`

R11 candidate action:

`{R11_ACTION}`

R11 zero theorem:

`{R11_ZERO}`

Status: R11 Sigma factorization is inserted into the candidate branch. Memory silence remains a relative theorem because parent owner, sign/gap, J_X=0, boundary zero and projection coefficients are unsigned. Numeric source fill rows now cover memory, boundary, projector, R11 and R10.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3893_MEMORY_SILENCE_THEOREM_OR_BOUND.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3893_NUMERIC_SOURCE_FILL_QUEUE.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3893_VALIDATION.csv`

Next gate: `3894`, memory parent owner/gap/JX closure or numeric source acquisition.

<!-- Generated by 3893 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    memory: list[dict[str, object]],
    r11: list[dict[str, object]],
    fill: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks.append(("VAL3893_0_sources", "all cited source paths exist and needles are found", resolved == len(sources), f"{resolved}/{len(sources)} sources resolved"))
    checks.append(("VAL3893_1_memory_identity", "memory identity is explicit", any("int_D" in str(row["statement_or_math"]) and "J_X" in str(row["statement_or_math"]) for row in memory), "MEM3893_0"))
    checks.append(("VAL3893_2_memory_no_claim", "memory theorem remains input-unsigned", any(row["memory_id"] == "MEM3893_5_verdict" and "NO_MEMORY_CLAIM" in str(row["status"]) for row in memory), "MEM3893_5"))
    checks.append(("VAL3893_3_R11_action", "R11 Sigma action is candidate-signed", any(row["r11_id"] == "R11S3893_00_candidate_action" and row["candidate_branch_signed"] for row in r11), "R11S3893_00"))
    required_families = {"R2_fR_scalar_mode", "Ricci_Weyl_squared", "scalar_tensor_class_metric", "vector_preferred_frame", "torsion_nonmetricity", "bulk_X_force_law", "nonlocal_memory_kernel", "source_normalization_operator"}
    signed_families = {str(row["operator_family"]) for row in r11 if str(row["candidate_branch_status"]) == "CANDIDATE_SIGMA_FACTOR_SIGNED"}
    checks.append(("VAL3893_4_R11_family_coverage", "ordinary non-topological R11 families are Sigma candidate-signed", required_families.issubset(signed_families), f"{len(signed_families)} signed families"))
    required_fill = {"lambda_gap;m_X^2;lambda_1(D)", "||J_X|| components", "K_R10;K_PPN;K_clock;K_Gdot;K_orbital;K_WEP", "c_B_flux_to_alpha3;epsilon_B_flux_abs", "P_PPN[T_extra_munu^Pi]", "C_gamma^F;c_F;C_beta^F", "K_X(lambda);Q_X^H;q_X^test;alpha_bound(lambda)"}
    found_fill = {str(row["needed_input"]) for row in fill}
    checks.append(("VAL3893_5_fill_queue", "numeric source fill queue covers memory/boundary/projector/R11/R10", required_fill.issubset(found_fill), f"{len(found_fill)} fill rows"))
    checks.append(("VAL3893_6_local_gr_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3893_6_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3893_6"))
    checks.append(("VAL3893_7_all_nonclaim", "all generated analytic rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [memory, r11, fill, gate, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3893_8_runner", "runner forbids R11 zero without Yloc", any(row["runner_field"] == "R11_sigma_guard" and "Y_loc=0" in str(row["rule"]) for row in runner), "RUNU3893_1"))
    checks.append(("VAL3893_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "R11 is no longer just floating" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3893_10_spine", "spine updated with 3893 block", SPINE_PATH.exists() and "BEGIN 3893 MEMORY R11 FACTORIZATION" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3893_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3893*") if path.is_file() and ("3893-Y5" in path.name or "P8_Y5_R2FR_3893" in path.name or "P8_Y5_BRR545_3893" in path.name)]
    checks.append(("VAL3893_12_formalization_untouched", "no generated 3893 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3893_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3893_14_next_target", "next target attacks memory owner/gap/JX or numeric source acquisition", any("memory-parent-owner-gap" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3894 memory owner/gap"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    memory = memory_rows(timestamp)
    r11 = r11_rows(timestamp)
    fill = fill_rows(timestamp)
    gate = gate_rows(timestamp)
    runner = runner_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["memory"], memory)
    write_csv(OUTPUTS["r11"], r11)
    write_csv(OUTPUTS["fill"], fill)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, memory, r11, fill, gate, runner, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, memory, r11, fill, gate, runner, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_MEMORY_RELATIVE_R11_SIGMA_CANDIDATE")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
