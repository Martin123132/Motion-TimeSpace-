from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3318-Y5-R2FR-Gamma-extra-sector-nonpropagation-proof-or-Bi-envelope-under-AX1090.md"

SRC_ACTION_FUND = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
SRC_ACTION_MOTION = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"

SOURCES = [
    {
        "source_id": "SRC3318_0_3317_doc",
        "path": ROOT / "3317-Y5-R2FR-minimal-symbolic-hessian-no-pole-or-finite-residue-branch-under-AX1090.md",
        "role": "3317 exact no-pole algebra and target",
    },
    {
        "source_id": "SRC3318_1_3317_conditions",
        "path": OUT / "P8_Y5_R2FR_3317_NO_POLE_CONDITIONS.csv",
        "role": "b0/z/b1 no-pole condition table",
    },
    {
        "source_id": "SRC3318_2_3317_action",
        "path": OUT / "P8_Y5_R2FR_3317_ACTION_COMPATIBILITY_TEST.csv",
        "role": "action compatibility/caveat rows",
    },
    {
        "source_id": "SRC3318_3_fundamental_action",
        "path": SRC_ACTION_FUND,
        "role": "MTS-Einstein action and microscopic psi action",
    },
    {
        "source_id": "SRC3318_4_motion_action",
        "path": SRC_ACTION_MOTION,
        "role": "Gamma_G potential and metric variation convention",
    },
    {
        "source_id": "SRC3318_5_3316_factor",
        "path": OUT / "P8_Y5_R2FR_3316_A_FACTOR_UPDATE.csv",
        "role": "B_i invariant amplitude update",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3318_SOURCE_REGISTER.csv",
    "evidence": OUT / "P8_Y5_R2FR_3318_ACTION_EVIDENCE_EXTRACT.csv",
    "branch": OUT / "P8_Y5_R2FR_3318_GAMMA_BRANCH_AUDIT.csv",
    "theorem": OUT / "P8_Y5_R2FR_3318_NONPROPAGATION_THEOREM_ATTEMPT.csv",
    "fallback": OUT / "P8_Y5_R2FR_3318_BI_ENVELOPE_FALLBACK.csv",
    "gates": OUT / "P8_Y5_R2FR_3318_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3318_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3318_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3318_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

PATTERNS = [
    "L_{Λκ}",
    "Gamma",
    "Γ_G",
    "scalar independent of metric variation",
    "δ(Γ_G",
    "curvature-exchange potential",
    "A_MTS",
    "∂_t",
    "∇",
    "ψ",
    "smoothed covariance",
]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1100) -> str:
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
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def text_for(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_hits(path: Path, patterns: list[str], max_hits: int = 10) -> str:
    text = text_for(path)
    lines = text.splitlines()
    hits: list[str] = []
    pattern_lowers = [pattern.lower() for pattern in patterns]
    for index, line in enumerate(lines, start=1):
        lower_line = line.lower()
        if any(pattern in lower_line for pattern in pattern_lowers):
            hits.append(f"L{index}:{line.strip()}")
        if len(hits) >= max_hits:
            break
    return " | ".join(hits)


def evidence_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        if path.suffix.lower() not in {".md", ".txt", ".csv"}:
            continue
        text = text_for(path)
        rows.append(
            {
                "evidence_id": f"EVID3318_{len(rows)}",
                "source_id": source["source_id"],
                "path": str(path),
                "has_Gamma_potential_language": bool_str("curvature-exchange potential" in text or "L_{Λκ}" in text or "L_{Î›Îº}" in text),
                "has_metric_independence_statement": bool_str("independent of metric variation" in text),
                "has_psi_derivative_action": bool_str(("A_MTS" in text or "L_MTS" in text) and ("∂" in text or "âˆ‚" in text or "nabla" in text or "∇" in text or "âˆ‡" in text)),
                "hits": find_hits(path, PATTERNS),
                "valid_for_claim": "false",
            }
        )
    return rows


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "GB3318_0_readout_background_Gamma",
            "branch": "Gamma_G is a local readout/background scalar, not an independent local variational field",
            "3317_coefficients": "x absent from Phi; equivalently b0=0, b1=0, z=0 in the local propagating Hessian",
            "derivation_status": "CONDITIONAL_NO_POLE_THEOREM",
            "supporting_source": "action text states Gamma_G enters as scalar potential and is independent of metric variation",
            "failure_mode": "must still prove microscopic psi coarse graining does not reintroduce public finite poles",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "GB3318_1_independent_algebraic_Gamma",
            "branch": "Gamma_G is promoted to independent local algebraic perturbation x in int sqrt(-g) x",
            "3317_coefficients": "z=0 and b1=0, but generic sqrt(-g) x expansion gives h-x algebraic mixing/tadpole rather than a clean GR pole unless stationarity/constraint is supplied",
            "derivation_status": "REJECT_AS_DIRECT_LOCAL_GR_PROOF",
            "supporting_source": "the source action does not provide an x variation equation, x^2 potential, or stationarity condition",
            "failure_mode": "an independent x is a constraint/tadpole problem, not a signed no-pole theorem",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "GB3318_2_microscopic_psi_reduction",
            "branch": "psi is the true microscopic field and g_pub emerges from smoothed derivative covariance",
            "3317_coefficients": "z_psi is nonzero before coarse graining because the psi action contains derivative kinetic terms",
            "derivation_status": "OPEN_PARENT_REDUCTION_REQUIRED",
            "supporting_source": "fundamental action contains psi time/spatial derivative terms and g_mu_nu = eta + <partial psi partial psi>",
            "failure_mode": "integrating or averaging psi could induce a finite public residue B_i unless a reduction theorem kills it",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "GB3318_3_empirical_Bi_envelope",
            "branch": "finite public residue retained",
            "3317_coefficients": "b0=0 for Newton pole, but a z-b1^2 != 0 and N(p_f) != 0",
            "derivation_status": "FALLBACK_SCOREABLE_BRANCH",
            "supporting_source": "3316/3317 provide the B_i residue formula and no-pole alternatives",
            "failure_mode": "must face R10/WEP/PPN/clock/orbital bounds with no cancellation",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "NPT3318_0_absence_lemma",
            "claim": "If Gamma_G is not an independent local field in Phi, then it contributes no x row to H_AB.",
            "derivation": "The local propagator is built from fields varied in S_2. A prescribed scalar readout/background Gamma_G has delta Gamma_G=0 in the local metric variation and no independent delta x. Therefore the public Hessian contains no x kinetic row and no h-x derivative mixing.",
            "3317_condition_effect": "b0=b1=z=0 by absence, not by tuning",
            "status": "CONDITIONAL_THEOREM_VALID",
            "valid_for_claim": "false",
        },
        {
            "step_id": "NPT3318_1_local_GR_effect",
            "claim": "In the readout/background Gamma branch with Gamma_0 -> 0 locally, the finite Gamma pole is absent.",
            "derivation": "With x absent and Gamma_0 locally zero/constant, D(p) reduces to the EH massless channel plus at most cosmological constant background curvature. There is no finite Gamma exchange pole B_Gamma to couple to WEP/R10/PPN.",
            "3317_condition_effect": "supports the algebraic-decoupled branch",
            "status": "CONDITIONAL_NO_POLE",
            "valid_for_claim": "false",
        },
        {
            "step_id": "NPT3318_2_independent_x_countercheck",
            "claim": "Promoting Gamma_G to an independent algebraic x does not by itself prove local GR.",
            "derivation": "S_x=int sqrt(-g) x expands as x + 1/2 h x + ..., so without a parent stationarity condition or x^2 potential it gives a tadpole/constraint-style term. This does not match the clean b0=0 branch.",
            "3317_condition_effect": "rejects the naive independent algebraic Gamma proof",
            "status": "COUNTERMODEL_GUARD",
            "valid_for_claim": "false",
        },
        {
            "step_id": "NPT3318_3_psi_caveat",
            "claim": "The microscopic psi action blocks a full parent no-pole claim unless coarse-grained reduction is proved.",
            "derivation": "The source action gives psi derivative dynamics and the metric as smoothed covariance of partial psi. A derivative microscopic field can generate public metric fluctuations after averaging unless a theorem projects them only into the massless EH channel/contact terms.",
            "3317_condition_effect": "keeps local-GR gate false",
            "status": "OPEN_REDUCTION_GAP",
            "valid_for_claim": "false",
        },
    ]


def fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BIE3318_0_scalar",
            "mode": "scalar_public_residue",
            "amplitude": "B_0",
            "law": "A_0=(1/3) B_0 [1+epsilon_0(Earth)]",
            "status": "ZERO_IF_READOUT_GAMMA_BRANCH_PARENT_SIGNED_ELSE_BOUND",
            "needed_for_claim": "psi reduction theorem or numeric/sourced B_0(lambda) bound",
            "valid_for_claim": "false",
        },
        {
            "row_id": "BIE3318_1_spin2",
            "mode": "massive_spin2_public_residue",
            "amplitude": "B_2",
            "law": "A_2=(-4/3) B_2 [1+epsilon_2(Earth)]",
            "status": "ZERO_IF_READOUT_GAMMA_BRANCH_PARENT_SIGNED_ELSE_BOUND",
            "needed_for_claim": "psi reduction theorem or numeric/sourced B_2(lambda) bound",
            "valid_for_claim": "false",
        },
        {
            "row_id": "BIE3318_2_no_cancellation",
            "mode": "absolute_envelope",
            "amplitude": "|B_0 Delta epsilon_0| + |B_2 Delta epsilon_2| + tails",
            "law": "WEP/R10/PPN/clock/orbital residuals must be bounded as absolute components unless a parent sign/cancellation relation is derived",
            "status": "FALLBACK_POLICY",
            "needed_for_claim": "arena-specific kernels and residual epsilon bounds",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3318_0_readout_branch_theorem",
            "claim": "readout/background Gamma has no independent local finite pole",
            "passed": "true",
            "reason": "if Gamma_G is absent from the local varied field vector, b0=b1=z=0 by absence",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3318_1_parent_signed_branch",
            "claim": "the parent theory signs readout/background Gamma as the actual local branch",
            "passed": "false",
            "reason": "microscopic psi derivative reduction is not proved",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3318_2_independent_Gamma_safe",
            "claim": "independent local algebraic Gamma is automatically safe",
            "passed": "false",
            "reason": "sqrt(-g) x creates tadpole/mixing unless stationarity/constraint is owned",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3318_3_local_GR",
            "claim": "local GR/Newtonian limit is fully derived",
            "passed": "false",
            "reason": "needs parent psi-to-public-metric no-finite-residue theorem or finite B_i bounds",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3318_0",
            "question": "Did 3318 prove anything useful?",
            "answer": "yes: it proves the conditional no-pole lemma for the readout/background Gamma branch",
            "reason": "a quantity not present in the local varied field vector cannot have a local propagator pole",
            "next_action": "try to parent-sign that this is the actual local branch after psi coarse graining",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3318_1",
            "question": "What route is rejected?",
            "answer": "independent algebraic Gamma as an automatic local-GR proof",
            "reason": "int sqrt(-g) x has tadpole/mixing without a stationarity equation or x^2 potential",
            "next_action": "do not use independent Gamma as a shortcut",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3318_2",
            "question": "What is the real next derivation?",
            "answer": "psi coarse-graining/no-finite-public-residue theorem",
            "reason": "psi is the derivative microscopic field that could reintroduce finite poles even if macroscopic Gamma is a readout",
            "next_action": "derive whether delta g_pub=<partial psi partial psi> has only EH/contact terms in the local branch or retains B_i",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3319-Y5-R2FR-psi-coarse-graining-no-finite-public-residue-or-Bi-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3319_psi_coarse_graining_no_finite_public_residue_or_Bi_bound.py",
            "objective": "prove or reject that the microscopic psi derivative action, after smoothing into g_pub=eta+<partial psi partial psi>, produces only the EH massless channel/contact renormalizations locally and no finite public B_i pole",
            "must_include": "psi quadratic action; smoothing kernel; public metric covariance map; two-point function; contact versus finite pole split; B_i extraction; fallback bound rows",
            "fallback_if_failed": "retain B_0/B_2 finite residue envelopes for R10/WEP/PPN/clock/orbital scoring",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    evidence = evidence_rows()
    branches = branch_rows()
    theorem = theorem_rows()
    gates = gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3318_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3318_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3318_2_outputs_parse",
            "check": "all 3318 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3318_3_evidence_has_Gamma_and_psi",
            "check": "evidence extract includes Gamma potential and psi derivative action",
            "passed": any(row["has_metric_independence_statement"] == "true" for row in evidence)
            and any(row["has_psi_derivative_action"] == "true" for row in evidence),
            "detail": "",
        },
        {
            "check_id": "VAL3318_4_branch_split",
            "check": "readout, independent, psi, and fallback branches are present",
            "passed": {"GB3318_0_readout_background_Gamma", "GB3318_1_independent_algebraic_Gamma", "GB3318_2_microscopic_psi_reduction", "GB3318_3_empirical_Bi_envelope"}.issubset(
                {row["branch_id"] for row in branches}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3318_5_conditional_no_pole",
            "check": "conditional readout Gamma no-pole theorem is present",
            "passed": any(row["step_id"] == "NPT3318_0_absence_lemma" and "b0=b1=z=0" in row["3317_condition_effect"] for row in theorem),
            "detail": "",
        },
        {
            "check_id": "VAL3318_6_reject_independent_shortcut",
            "check": "independent algebraic Gamma shortcut is rejected",
            "passed": any(row["step_id"] == "NPT3318_2_independent_x_countercheck" and row["status"] == "COUNTERMODEL_GUARD" for row in theorem),
            "detail": "",
        },
        {
            "check_id": "VAL3318_7_no_full_local_GR_claim",
            "check": "parent-signed and full local-GR gates remain false",
            "passed": all(row["passed"] == "false" for row in gates if row["gate_id"] in {"GATE3318_1_parent_signed_branch", "GATE3318_3_local_GR"}),
            "detail": "",
        },
        {
            "check_id": "VAL3318_8_next_psi",
            "check": "next target is psi coarse-graining/no finite residue",
            "passed": any("psi-coarse-graining" in row["target_doc"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3318_9_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3318_10_overall",
            "check": "3318 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for row in checks:
        row["passed"] = bool_str(bool(row["passed"]))
    return checks


def render_doc() -> str:
    sources = source_register_rows()
    evidence = evidence_rows()
    branches = branch_rows()
    theorem = theorem_rows()
    fallback = fallback_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    lines: list[str] = [
        "# 3318 - Gamma extra-sector nonpropagation proof or Bi envelope under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3318 gets one clean conditional theorem and rejects one tempting shortcut.",
        "",
        "If `Γ_G` is a readout/background scalar and is not an independent local variable in the field vector `Phi`, then it has no local Hessian row. In the 3317 language this gives",
        "",
        "`b0 = b1 = z = 0`",
        "",
        "by absence rather than tuning, so there is no finite `Γ_G` pole.",
        "",
        "But this is not yet a full local-GR proof, because the microscopic `ψ` action is derivative-dynamical and `g_pub` is built from smoothed `∂ψ ∂ψ`. A coarse-graining theorem is still needed to show that `ψ` produces only the EH massless channel/contact renormalizations locally, not finite public residues `B_i`.",
        "",
        "Also rejected: treating `Γ_G` as an independent algebraic local field automatically. Expanding `int sqrt(-g) x` gives tadpole/mixing unless a parent stationarity/constraint equation is supplied.",
        "",
        "## Source Register",
        "",
    ]
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` - exists={row['exists']}; parse_ok={row['parse_ok']}; role={row['role']}")
    lines.extend(["", "## Action Evidence Extract", ""])
    for row in evidence:
        lines.append(
            f"- `{row['evidence_id']}` `{row['source_id']}`: GammaPotential={row['has_Gamma_potential_language']}; MetricIndependent={row['has_metric_independence_statement']}; PsiDerivative={row['has_psi_derivative_action']}; hits={row['hits']}"
        )
    lines.extend(["", "## Gamma Branch Audit", ""])
    for row in branches:
        lines.append(
            f"- `{row['branch_id']}` `{row['derivation_status']}`: {row['branch']} Coefficients: {row['3317_coefficients']}. Failure mode: {row['failure_mode']}."
        )
    lines.extend(["", "## Nonpropagation Theorem Attempt", ""])
    for row in theorem:
        lines.append(
            f"- `{row['step_id']}` `{row['status']}`: {row['claim']} {row['derivation']} 3317 effect: {row['3317_condition_effect']}."
        )
    lines.extend(["", "## Bi Envelope Fallback", ""])
    for row in fallback:
        lines.append(f"- `{row['row_id']}` `{row['mode']}`: {row['law']} Status: {row['status']}. Needed: {row['needed_for_claim']}.")
    lines.extend(["", "## Promotion Gates", ""])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: passed={row['passed']}; claim={row['claim']}; reason={row['reason']}")
    lines.extend(["", "## Decision", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['answer']} - {row['reason']} Next: {row['next_action']}.")
    lines.extend(["", "## Next Target", ""])
    for row in next_rows:
        lines.append(f"- `{row['target_doc']}`")
        lines.append(f"- `{row['target_script']}`")
        lines.append(f"- Objective: {row['objective']}")
        lines.append(f"- Fallback: {row['fallback_if_failed']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["evidence"], evidence_rows())
    write_csv(OUTPUTS["branch"], branch_rows())
    write_csv(OUTPUTS["theorem"], theorem_rows())
    write_csv(OUTPUTS["fallback"], fallback_rows())
    write_csv(OUTPUTS["gates"], gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
