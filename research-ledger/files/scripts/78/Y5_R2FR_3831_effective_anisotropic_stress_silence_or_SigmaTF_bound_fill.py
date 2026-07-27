from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3831"
BRANCH = "MTS_R2FR_Y5_EFFECTIVE_ANISOTROPIC_STRESS_SILENCE_OR_SIGMATF_BOUND_FILL_3831"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3831-Y5-R2FR-effective-anisotropic-stress-silence-or-SigmaTF-bound-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3830 = PCW / "3830-Y5-R2FR-no-slip-traceless-ij-source-condition-or-gamma-bound-source.md"
CSV_3830_OPERATOR = OUT / "P8_Y5_R2FR_3830_NO_SLIP_OPERATOR_THEOREM.csv"
CSV_3830_DECOMP = OUT / "P8_Y5_R2FR_3830_SLIP_SOURCE_DECOMPOSITION.csv"
CSV_3830_GAMMA = OUT / "P8_Y5_R2FR_3830_GAMMA_BOUND_SOURCE_ROWS.csv"
CSV_3830_VALIDATION = OUT / "P8_Y5_BRR545_3830_VALIDATION.csv"
CSV_3821_STRESS_ROWS = OUT / "P8_Y5_R2FR_3821_STRESS_VIRIAL_RESIDUAL_ROWS.csv"
CSV_3821_STRESS_THEOREM = OUT / "P8_Y5_R2FR_3821_STRESS_VIRIAL_THEOREM.csv"
CSV_3820_KOMAR = OUT / "P8_Y5_R2FR_3820_KOMAR_TOLMAN_ACTIVE_MASS_DERIVATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3831_SOURCE_REGISTER.csv",
    "tf_theorem": OUT / "P8_Y5_R2FR_3831_TRACeless_STRESS_OPERATOR_THEOREM.csv",
    "decomposition": OUT / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv",
    "tensor_virial": OUT / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv",
    "bounds": OUT / "P8_Y5_R2FR_3831_SIGMATF_BOUND_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3831_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3831_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3831_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3831_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3831_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3831_0_3830_doc", P_3830, "No-Slip Traceless-ij Source Condition Or Gamma Bound Source"),
    ("SRC3831_1_3830_operator", CSV_3830_OPERATOR, "NS3830_2_effective_source_equation"),
    ("SRC3831_2_3830_decomp", CSV_3830_DECOMP, "SLIP3830_0_matter_anisotropic"),
    ("SRC3831_3_3830_gamma_bound", CSV_3830_GAMMA, "GB3830_1_gamma_total"),
    ("SRC3831_4_3830_validation", CSV_3830_VALIDATION, "VAL3830_2_source_decomposition"),
    ("SRC3831_5_3821_stress_rows", CSV_3821_STRESS_ROWS, "R3821_5_total"),
    ("SRC3831_6_3821_stress_theorem", CSV_3821_STRESS_THEOREM, "SVT3821_2_trace_cancellation"),
    ("SRC3831_7_3820_komar", CSV_3820_KOMAR, "KT3820_4_slow_weak_Newton_limit"),
]


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
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle in SOURCE_SPECS:
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
                "role": "input_for_effective_anisotropic_stress_silence_or_bound",
                "claim_use": "conditional_tensor_virial_and_bound_contract_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def tf_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "TF3831_0_trace_not_traceless",
            "statement": "The 3821 trace/virial cancellation is not sufficient for gamma: no-slip needs the traceless spatial source.",
            "equation": "Sigma_TF_matter = P_TF[T_ij^matter + T_ij^apparatus + T_ij^EM/radiation + T_ij^binding]",
            "zero_condition": "each projected traceless term vanishes or is outside the local exterior order being claimed",
            "status": "CLARIFICATION_GATE_PASS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "TF3831_1_exterior_vacuum_silence",
            "statement": "On a true matter-vacuum exterior annulus, ordinary material stress contributes no local Sigma_TF_matter density.",
            "equation": "T_ij^matter|Omega_ext = 0 => P_TF T_ij^matter|Omega_ext = 0",
            "zero_condition": "fixed exterior domain has no matter/apparatus/radiation support crossing it",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "TF3831_2_tensor_virial_average",
            "statement": "For a closed stationary bound source, the tensor virial identity can suppress the integrated TF stress moment, but this is stronger than trace cancellation.",
            "equation": "d2I_ij^TF/dt2 = 2 int T_ij^TF d3x + surface/exchange terms",
            "zero_condition": "stationary closed total source, fixed surface, no exchange, and no unresolved quadrupole/radiative TF term",
            "status": "CONDITIONAL_AVERAGE_ZERO_NOT_POINTWISE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "TF3831_3_gamma_bound_from_TF_source",
            "statement": "If TF stress is not zero-signed, gamma survives only as a finite source bound.",
            "equation": "B_gamma_matter_TF <= K_TF*(epsilon_ext_TF + epsilon_tensor_virial_TF + epsilon_quad_TF + epsilon_EM_Poynting_TF + epsilon_apparatus_TF)",
            "zero_condition": "all epsilon terms vanish or fall below the declared gamma threshold",
            "status": "FIRST_TF_BOUND_CONTRACT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decomposition_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "SIGMATF3831_0_exterior_material",
            "component": "epsilon_ext_TF",
            "definition": "ordinary matter stress physically present inside the exterior test annulus",
            "zero_route": "true exterior vacuum/support separation",
            "bound_formula": "epsilon_ext_TF <= sup_Omega_ext norm(P_TF T_ij^matter)/(rho_source c^2)",
            "status": "ZERO_IF_EXTERIOR_VACUUM_ELSE_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SIGMATF3831_1_tensor_virial",
            "component": "epsilon_tensor_virial_TF",
            "definition": "unbalanced integrated TF stress moment of the closed source",
            "zero_route": "tensor virial stationary closed source with surface/exchange silence",
            "bound_formula": "epsilon_tensor_virial_TF <= norm(d2I_TF/dt2 + surface_TF + exchange_TF)/(M c^2)",
            "status": "REQUIRES_TENSOR_VIRIAL_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SIGMATF3831_2_quadrupole_multipole",
            "component": "epsilon_quad_TF",
            "definition": "finite multipole/quadrupole leakage from the compact source into the local exterior readout",
            "zero_route": "spherical/monopole projection or explicit quadrupole outside claimed order",
            "bound_formula": "epsilon_quad_TF <= C_Q abs(Q_TF)/(M r^2)",
            "status": "MULTIPOLE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SIGMATF3831_3_EM_Poynting",
            "component": "epsilon_EM_Poynting_TF",
            "definition": "traceless stress from electromagnetic fields, radiation, or Poynting momentum flux",
            "zero_route": "no EM/radiative flux in local exterior or parent coupling cancels/sequesters its TF part",
            "bound_formula": "epsilon_EM_Poynting_TF <= sup norm(P_TF T_ij^EM + S_i S_j/c^2)/(rho_source c^2)",
            "status": "EM_POYNTING_SOURCE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "SIGMATF3831_4_apparatus_binding",
            "component": "epsilon_apparatus_TF",
            "definition": "lab apparatus, binding, material, or frame stress not included in the isolated compact source",
            "zero_route": "apparatus stress outside projection or explicitly included in closed total source",
            "bound_formula": "epsilon_apparatus_TF <= norm(P_TF T_ij^apparatus)/(M_source c^2)",
            "status": "ARENA_SOURCE_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def tensor_virial_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "condition_id": "TV3831_0_closed_total_source",
            "condition": "source is a closed total system, not a partial matter subset",
            "why_needed": "otherwise hidden support/exchange stress can carry TF source",
            "current_status": "UNSIGNED_FOR_LOCAL_ARENAS",
            "if_unsigned": "retain epsilon_apparatus_TF + epsilon_tensor_virial_TF",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "condition_id": "TV3831_1_stationary_TF_inertia",
            "condition": "d2I_ij^TF/dt2=0 after averaging on the claimed timescale",
            "why_needed": "tensor virial zero is an averaged TF statement, not merely static-looking prose",
            "current_status": "UNSIGNED",
            "if_unsigned": "retain epsilon_tensor_virial_TF",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "condition_id": "TV3831_2_surface_exchange_silence",
            "condition": "surface_TF=0 and exchange_TF=0 on the fixed compact boundary",
            "why_needed": "surface/exchange terms can mimic anisotropic stress in the no-slip equation",
            "current_status": "PARTIAL_FROM_3825_BOUNDARY_ROUTE",
            "if_unsigned": "retain epsilon_boundary_TF",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "condition_id": "TV3831_3_EM_radiation_separation",
            "condition": "Poynting/radiation/field stress is either absent, included in the total closed source, or separately bounded",
            "why_needed": "EM wave stress is naturally traceless/anisotropic and can source slip",
            "current_status": "UNSIGNED_AND_SELECTED_NEXT",
            "if_unsigned": "retain epsilon_EM_Poynting_TF",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "BTF3831_0_matter_total",
            "observable": "B_gamma_matter_TF",
            "bound_formula": "B_gamma_matter_TF <= K_TF*(epsilon_ext_TF + epsilon_tensor_virial_TF + epsilon_quad_TF + epsilon_EM_Poynting_TF + epsilon_apparatus_TF)",
            "source_rows_needed": "exterior support; tensor virial; quadrupole; EM/Poynting; apparatus stress",
            "status": "FIRST_SIGMATF_MATTER_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BTF3831_1_zero_route",
            "observable": "Sigma_TF_matter zero",
            "bound_formula": "if all five epsilon_TF terms vanish then Sigma_TF_matter=0",
            "source_rows_needed": "closed stationary exterior-vacuum no-radiation source signature",
            "status": "CONDITIONAL_ZERO_NOT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BTF3831_2_gamma_update",
            "observable": "gamma-1",
            "bound_formula": "abs(gamma-1) <= B_gamma_matter_TF + B_gamma_parent_extra + B_gamma_boundary + B_gamma_readout + abs(eps_spatial/Phi)",
            "source_rows_needed": "3831 matter row plus remaining 3830 parent/boundary/readout rows",
            "status": "UPDATED_GAMMA_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3831_0_trace_guard",
            "gate": "trace/virial does not imply no-slip",
            "status": "PASS_GUARD",
            "claim_allowed": False,
            "reason": "3831 separates trace cancellation from traceless anisotropic stress silence",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3831_1_SigmaTF_zero",
            "gate": "Sigma_TF_matter zero claim",
            "status": "BLOCKED_TENSOR_VIRIAL_AND_EM_BOUND_REQUIRED",
            "claim_allowed": False,
            "reason": "tensor virial, quadrupole, EM/Poynting, and apparatus TF rows are not signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3831_2_gamma_bound",
            "gate": "gamma matter-source bound",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "first Sigma_TF_matter bound formula exists but lacks numeric/source-backed rows",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3831_3_local_GR",
            "gate": "local GR/no-slip claim",
            "status": "BLOCKED",
            "claim_allowed": False,
            "reason": "matter TF, parent extra, boundary, readout, and beta residuals remain open",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3831_4_next_target",
            "gate": "next target attacks EM/Poynting and tensor-virial TF separation",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "EM/Poynting stress is the highest-risk TF source and matches the framework's EM route",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3831_0_no_trace_shortcut",
            "decision": "do not use stress-virial trace cancellation as a gamma/no-slip proof",
            "basis": "gamma is controlled by traceless anisotropic stress, while 3821 mainly guards active mass/trace routes",
            "consequence": "local GR remains honest and harder to break under scrutiny",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3831_1_tensor_virial_possible",
            "decision": "a stronger tensor-virial route may suppress integrated TF stress for closed stationary sources",
            "basis": "d2I_ij^TF/dt2 identity can zero averaged TF stress only with closed source, surface, exchange, and radiation clauses",
            "consequence": "this is a derivation path, but not yet parent/source signed",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3831_2_poynting_relevance",
            "decision": "Poynting/vector-wave stress is genuinely relevant but dangerous",
            "basis": "EM/radiation stress naturally contributes to TF anisotropic source terms",
            "consequence": "next step should separate/cancel/bound EM-Poynting TF stress rather than treating it as motivational prose",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3831_0",
            "next_checkpoint": "3832-Y5-R2FR-tensor-virial-TF-stress-and-EM-Poynting-separation-or-bound.md",
            "script": "scripts/Y5_R2FR_3832_tensor_virial_TF_stress_and_EM_Poynting_separation_or_bound.py",
            "objective": "separate tensor-virial TF stress from EM/Poynting/radiative TF stress, then try to prove cancellation/sequestration or emit source-bound rows for epsilon_EM_Poynting_TF and epsilon_tensor_virial_TF",
            "reason": "3831 shows Sigma_TF_matter is the first no-slip blocker and that EM/Poynting stress is a real possible source term, not a shortcut",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_SIGMATF_MATTER_BOUND_FORM",
            "claim": "no gamma/no-slip/local-GR claim",
            "summary": "3831 separates trace virial cancellation from traceless anisotropic stress silence and emits first Sigma_TF_matter/gamma bound rows.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    tf_theorems: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    tensor_virial: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3831 — Effective Anisotropic Stress Silence Or SigmaTF Bound Fill

Private checkpoint. This attacks `Sigma_TF_matter`, the first source term in the 3830 no-slip equation. It does not claim `gamma=1`.

Generated: `{timestamp}`

## Result

3831 makes an important distinction:

`trace/virial cancellation != traceless anisotropic stress silence`.

The no-slip source is

`Sigma_TF_matter = P_TF[T_ij^matter + T_ij^apparatus + T_ij^EM/radiation + T_ij^binding]`.

The useful bound is

`B_gamma_matter_TF <= K_TF*(epsilon_ext_TF + epsilon_tensor_virial_TF + epsilon_quad_TF + epsilon_EM_Poynting_TF + epsilon_apparatus_TF)`.

So `gamma` is not closed, but the matter-side source of slip is now a concrete source-bound problem.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Traceless Stress Operator Theorem

{markdown_table(tf_theorems, ["theorem_id", "statement", "equation", "zero_condition", "status"])}

## SigmaTF Matter Decomposition

{markdown_table(decomposition, ["component_id", "component", "definition", "zero_route", "status"])}

## Tensor-Virial Conditions

{markdown_table(tensor_virial, ["condition_id", "condition", "why_needed", "current_status", "if_unsigned"])}

## SigmaTF Bound Rows

{markdown_table(bounds, ["bound_id", "observable", "bound_formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This is not a public win, but it is a proper derivation step. We now know exactly why a lazy trace argument would fail: `gamma` cares about traceless stress. The next clean target is to separate tensor-virial TF stress from EM/Poynting/radiative TF stress. If Poynting is part of the background/source story, it must enter here as a controlled source term, not as a shortcut.

Next target: `3832-Y5-R2FR-tensor-virial-TF-stress-and-EM-Poynting-separation-or-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3830", "Current State After 3831", 1)
    paragraph = (
        "`3831` separates trace/virial cancellation from the traceless anisotropic stress silence required for `gamma`. "
        "The matter-side no-slip source is now `Sigma_TF_matter=P_TF[T_ij^matter+T_ij^apparatus+T_ij^EM/radiation+T_ij^binding]`, with "
        "`B_gamma_matter_TF <= K_TF*(epsilon_ext_TF+epsilon_tensor_virial_TF+epsilon_quad_TF+epsilon_EM_Poynting_TF+epsilon_apparatus_TF)`. "
        "This blocks any shortcut from active-mass trace work to `gamma=1`, but gives a concrete tensor-virial/EM-Poynting source-bound route.\n\n"
    )
    anchor = "`3830` formulates"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3831-Y5-R2FR-effective-anisotropic-stress-silence-or-SigmaTF-bound-fill.md`

Target: try to prove `Sigma_TF_matter=0` or source-bound it for compact exterior local tests, distinguishing stress trace/virial cancellation from traceless anisotropic stress silence.

This is the best next move because 3830 shows no-slip/gamma recovery fails or survives on the effective traceless stress source first."""
    new_gate = """`3832-Y5-R2FR-tensor-virial-TF-stress-and-EM-Poynting-separation-or-bound.md`

Target: separate tensor-virial TF stress from EM/Poynting/radiative TF stress, then try to prove cancellation/sequestration or emit source-bound rows for `epsilon_EM_Poynting_TF` and `epsilon_tensor_virial_TF`.

This is the best next move because 3831 shows `Sigma_TF_matter` is the first no-slip blocker and that EM/Poynting stress is a real possible source term, not a shortcut."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3831_TRACeless_STRESS_OPERATOR_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3831_SIGMATF_BOUND_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3831_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3831_SIGMATF_BOUND_ROWS.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3831 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3831 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    tf_theorems: list[dict[str, object]],
    decomposition: list[dict[str, object]],
    tensor_virial: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in tf_theorems + decomposition + tensor_virial + bounds + gates)
    add(
        "VAL3831_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3831_1_trace_guard",
        "trace/virial cancellation is explicitly not used as no-slip proof",
        "trace/virial cancellation != traceless anisotropic stress silence" in read_text(DOC_PATH),
        "doc contains trace/traceless guard",
    )
    add(
        "VAL3831_2_components",
        "SigmaTF matter bound includes exterior, tensor virial, quadrupole, EM/Poynting, and apparatus components",
        all(token in all_text for token in ["epsilon_ext_TF", "epsilon_tensor_virial_TF", "epsilon_quad_TF", "epsilon_EM_Poynting_TF", "epsilon_apparatus_TF"]),
        "five epsilon components present",
    )
    add(
        "VAL3831_3_nonclaim",
        "all SigmaTF rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in tf_theorems + decomposition + tensor_virial + bounds + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3831_4_gamma_bound",
        "gamma matter TF bound row exists",
        any(row["bound_id"] == "BTF3831_0_matter_total" for row in bounds),
        f"{len(bounds)} bound rows",
    )
    add(
        "VAL3831_5_zero_blocked",
        "Sigma_TF_matter zero claim remains blocked",
        any(row["gate_id"] == "GATE3831_1_SigmaTF_zero" and row["status"] == "BLOCKED_TENSOR_VIRIAL_AND_EM_BOUND_REQUIRED" for row in gates),
        "Sigma_TF_matter zero blocked",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3831_6_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3831_7_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "epsilon_EM_Poynting_TF" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3831*", "P8_Y5_BRR545_3831*", "*Y5_R2FR_3831*", "3831-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3831_8_formalization_clean",
        "formalization-workbench has no 3831 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3831 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3831_9_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    tf_theorems = tf_theorem_rows(timestamp)
    decomposition = decomposition_rows(timestamp)
    tensor_virial = tensor_virial_rows(timestamp)
    bounds = bound_rows(timestamp)
    gates = claim_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["tf_theorem"], tf_theorems)
    write_csv(OUTPUTS["decomposition"], decomposition)
    write_csv(OUTPUTS["tensor_virial"], tensor_virial)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, tf_theorems, decomposition, tensor_virial, bounds, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, tf_theorems, decomposition, tensor_virial, bounds, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_SIGMATF_MATTER_BOUND_FORM")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
