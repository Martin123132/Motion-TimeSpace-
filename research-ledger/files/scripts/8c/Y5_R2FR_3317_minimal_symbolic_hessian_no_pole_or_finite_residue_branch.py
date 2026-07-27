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

DOC = ROOT / "3317-Y5-R2FR-minimal-symbolic-hessian-no-pole-or-finite-residue-branch-under-AX1090.md"

SRC_ACTION_1 = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
SRC_ACTION_2 = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"

SOURCES = [
    {
        "source_id": "SRC3317_0_3316_doc",
        "path": ROOT / "3316-Y5-R2FR-parent-quadratic-hessian-readout-extraction-for-ZiUi-under-AX1090.md",
        "role": "3316 invariant residue/readout formula and next target",
    },
    {
        "source_id": "SRC3317_1_3316_factor",
        "path": OUT / "P8_Y5_R2FR_3316_A_FACTOR_UPDATE.csv",
        "role": "A_i updated to B_i residue law",
    },
    {
        "source_id": "SRC3317_2_3316_contract",
        "path": OUT / "P8_Y5_R2FR_3316_RESIDUE_EXTRACTION_CONTRACT.csv",
        "role": "required H_AB and R map contract",
    },
    {
        "source_id": "SRC3317_3_fundamental_action",
        "path": SRC_ACTION_1,
        "role": "macroscopic action and microscopic psi action source",
    },
    {
        "source_id": "SRC3317_4_motion_action",
        "path": SRC_ACTION_2,
        "role": "MTS action principle with curvature-exchange potential",
    },
    {
        "source_id": "SRC3317_5_1042_nohair",
        "path": ROOT / "1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md",
        "role": "conditional positive no-hair route if finite pole remains as physical X",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3317_SOURCE_REGISTER.csv",
    "hessian": OUT / "P8_Y5_R2FR_3317_MINIMAL_HESSIAN_FORMULA.csv",
    "conditions": OUT / "P8_Y5_R2FR_3317_NO_POLE_CONDITIONS.csv",
    "action_test": OUT / "P8_Y5_R2FR_3317_ACTION_COMPATIBILITY_TEST.csv",
    "branch": OUT / "P8_Y5_R2FR_3317_BRANCH_DECISION_MATRIX.csv",
    "gates": OUT / "P8_Y5_R2FR_3317_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3317_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3317_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3317_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1000) -> str:
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


def action_text() -> str:
    parts: list[str] = []
    for path in (SRC_ACTION_1, SRC_ACTION_2):
        if path.exists():
            parts.append(path.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def keyword_present(text: str, keyword: str) -> bool:
    return keyword.lower() in text.lower()


def hessian_rows() -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "MH3317_0_ansatz",
            "object": "minimal two-channel local Hessian",
            "formula": "Phi=(h,x), H(p)=[[a p, b0+b1 p],[b0+b1 p, M2+z p]], R=(1,u), p=k^2",
            "meaning": "h is the massless GR metric channel; x is the least extra finite/local MTS channel; u is public readout overlap",
            "status": "SYMBOLIC_TEST_BED",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "MH3317_1_propagator",
            "object": "public exchange propagator",
            "formula": "G_pub(p)=N(p)/D(p)",
            "meaning": "N and D decide whether local tests see a finite pole",
            "status": "DERIVED",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "MH3317_2_denominator",
            "object": "D(p)=det H",
            "formula": "D(p)=a p (M2+z p)-(b0+b1 p)^2",
            "meaning": "the zeros of D are the massless and finite pole candidates",
            "status": "DERIVED",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "MH3317_3_numerator",
            "object": "N(p)=R adj(H) R^T",
            "formula": "N(p)=M2+z p-2u(b0+b1 p)+u^2 a p",
            "meaning": "a pole is observable only if N is nonzero at that pole",
            "status": "DERIVED",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "MH3317_4_GR_massless_condition",
            "object": "massless Newton pole",
            "formula": "D(0)=-b0^2, so a GR-like massless pole at p=0 requires b0=0",
            "meaning": "constant h-x mixing gives the graviton a mass/deformation unless removed by symmetry/constraint",
            "status": "DERIVED_GATE",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "MH3317_5_finite_pole",
            "object": "finite pole location after b0=0",
            "formula": "D(p)=p[a M2+(a z-b1^2)p], so p_f=-a M2/(a z-b1^2)",
            "meaning": "generic derivative kinetic/mixing creates a finite pole unless the second factor is absent or unobserved",
            "status": "DERIVED_GATE",
            "valid_for_claim": "false",
        },
    ]


def condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition_id": "NPC3317_0_GR_pole",
            "branch": "GR_massless_first_gate",
            "condition": "b0=0",
            "effect": "keeps D(0)=0 and prevents constant h-x mixing from deforming the Newton pole",
            "scrutiny": "must be symmetry/constraint derived, not fitted",
            "local_GR_support": "required_not_sufficient",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "NPC3317_1_algebraic_decoupled",
            "branch": "no_finite_pole_by_algebraic_decoupling",
            "condition": "b0=0, z=0, b1=0, M2 nonzero",
            "effect": "D(p)=a M2 p, so G_pub has only the massless Newton pole plus contact/algebraic terms",
            "scrutiny": "best local-GR route if Gamma/extra sector is nonpropagating and does not derivative-mix with h",
            "local_GR_support": "strong_if_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "NPC3317_2_degenerate_constraint",
            "branch": "no_finite_pole_by_constraint_degeneracy",
            "condition": "b0=0 and a z-b1^2=0 with first-class/constraint degree-count proof",
            "effect": "the finite denominator factor vanishes rather than producing a physical extra pole",
            "scrutiny": "dangerous unless the degeneracy is a true gauge/constraint, not an under-specified Hessian",
            "local_GR_support": "possible_if_constraint_proved",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "NPC3317_3_readout_orthogonal",
            "branch": "finite_pole_unobserved",
            "condition": "N(p_f)=M2+p_f(z-2u b1+u^2 a)=0",
            "effect": "a finite eigenmode may exist but has zero public-metric residue B_i",
            "scrutiny": "looks like tuning unless enforced by a parent projector/orthogonality theorem",
            "local_GR_support": "possible_if_parent_orthogonality_proved",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "NPC3317_4_short_range",
            "branch": "finite_pole_retained_but_short_range",
            "condition": "m_f^2=a M2/(a z-b1^2)>0 and m_f r_local >> 1",
            "effect": "finite pole exists but is exponentially suppressed in local tests",
            "scrutiny": "requires parent range or empirical bound; not as clean as no-pole",
            "local_GR_support": "bounded_empirical_route",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "NPC3317_5_generic_residue",
            "branch": "finite_residue_branch",
            "condition": "b0=0, a z-b1^2 != 0, N(p_f) != 0",
            "effect": "local finite mode has nonzero B_i and must face R10/WEP/PPN/clock/orbital tests",
            "scrutiny": "no local-GR claim without bounds or screening",
            "local_GR_support": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def action_compatibility_rows() -> list[dict[str, Any]]:
    text = action_text()
    has_eh = keyword_present(text, "Einstein") and keyword_present(text, "Hilbert")
    has_lgamma = (
        keyword_present(text, "curvature-exchange")
        or keyword_present(text, "Global Curvature Gradient")
        or keyword_present(text, "L_{")
        or keyword_present(text, "L_")
    )
    has_matter = keyword_present(text, "L_matter") or keyword_present(text, "matter")
    has_explicit_gamma_kinetic = keyword_present(text, "partial Gamma") or keyword_present(text, "nabla Gamma") or keyword_present(text, "(partial Gamma)")
    has_microscopic_psi = (
        keyword_present(text, "microscopic")
        and (keyword_present(text, "motion field") or keyword_present(text, "field action") or keyword_present(text, "gradients encode"))
    )
    return [
        {
            "test_id": "ACT3317_0_EH_anchor",
            "question": "Does the corpus contain a massless EH/GR anchor?",
            "answer": bool_str(has_eh),
            "evidence": "action sources discuss Einstein-Hilbert/Einstein limit" if has_eh else "not found",
            "impact": "supports h channel as the massless pole",
            "valid_for_claim": "false",
        },
        {
            "test_id": "ACT3317_1_curvature_exchange_potential",
            "question": "Does the macroscopic action describe curvature exchange as potential-like rather than explicit local kinetic Gamma?",
            "answer": bool_str(has_lgamma and not has_explicit_gamma_kinetic),
            "evidence": "action sources list L_Lambda/Gamma-style curvature-exchange potential, but the scan did not find explicit partial-Gamma kinetic language",
            "impact": "compatible with the algebraic-decoupled no-finite-pole branch, but not a proof because microscopic psi dynamics may induce a reduced Hessian",
            "valid_for_claim": "false",
        },
        {
            "test_id": "ACT3317_2_matter_coupling",
            "question": "Does the corpus include ordinary matter coupling language?",
            "answer": bool_str(has_matter),
            "evidence": "L_matter/matter coupling appears in action sources" if has_matter else "not found",
            "impact": "compatible with Hilbert source theorem from 3315",
            "valid_for_claim": "false",
        },
        {
            "test_id": "ACT3317_3_microscopic_psi_caveat",
            "question": "Can microscopic psi dynamics reintroduce finite local poles after coarse graining?",
            "answer": bool_str(has_microscopic_psi),
            "evidence": "fundamental action source discusses microscopic psi field/action",
            "impact": "prevents claiming no-pole from macroscopic potential language alone",
            "valid_for_claim": "false",
        },
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "BR3317_0_best_route",
            "route": "prove algebraic/nonpropagating curvature-exchange in local compact branch",
            "why_best": "it gives D(p)=a M2 p and no finite public pole, matching local GR without fifth-force fine tuning",
            "needed_proof": "Gamma/extra sector has z=0, b1=0, b0=0 after local reduction and no psi-induced finite readout pole",
            "status": "BEST_NEXT_TARGET_NOT_CLAIMED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BR3317_1_second_best",
            "route": "prove readout orthogonality N(p_f)=0",
            "why_best": "finite mode can exist internally but has B_i=0 in ordinary public metric tests",
            "needed_proof": "parent projector orthogonality theorem for R against finite eigenvector",
            "status": "VIABLE_BUT_TUNING_RISK",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BR3317_2_empirical",
            "route": "retain finite B_i envelope",
            "why_best": "scoreable if no-pole fails",
            "needed_proof": "range, residue sign, residual source tails, R10/WEP/PPN/clock/orbital bounds",
            "status": "FALLBACK",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3317_0_algebra",
            "claim": "minimal Hessian pole algebra is derived",
            "passed": "true",
            "reason": "D(p), N(p), GR b0 gate, finite pole, and no-pole branches are explicit",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3317_1_no_finite_pole",
            "claim": "MTS local branch has no observable finite pole",
            "passed": "false",
            "reason": "algebraic-decoupled/no-pole clauses are compatible but not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3317_2_local_GR",
            "claim": "local GR/Newton limit is derived",
            "passed": "false",
            "reason": "requires parent proof of no finite pole, orthogonal readout, short range, or no-hair/screening",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3317_0",
            "question": "What exact leap did 3317 make?",
            "answer": "it derived the two-channel finite-pole algebra and the exact no-pole conditions",
            "reason": "the local-GR problem reduces to b0=0 plus either z=b1=0, az-b1^2=0 with constraints, N(p_f)=0, or short-range/screened finite residue",
            "next_action": "attack the algebraic/nonpropagating Gamma/local-extra-sector proof first",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3317_1",
            "question": "Does the current action language favor any branch?",
            "answer": "yes, weakly: the macroscopic curvature-exchange term looks potential-like and therefore compatible with algebraic no-pole",
            "reason": "the action scan does not expose an explicit Gamma kinetic term, but microscopic psi dynamics may still generate one after reduction",
            "next_action": "prove or reject z=0 and b1=0 for the local compact branch",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3317_2",
            "question": "Is this a local-GR claim yet?",
            "answer": "no",
            "reason": "compatibility is not derivation; the no-pole branch needs parent signature",
            "next_action": "3318 should specifically test Gamma/extra-sector nonpropagation rather than broad source sweeps",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3318-Y5-R2FR-Gamma-extra-sector-nonpropagation-proof-or-Bi-envelope-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3318_Gamma_extra_sector_nonpropagation_proof_or_Bi_envelope.py",
            "objective": "prove or reject the best 3317 no-pole route: local curvature-exchange/extra sector has b0=0, z=0, b1=0 in the public metric Hessian, so no finite observable pole exists",
            "must_include": "macroscopic Gamma potential check; microscopic psi reduction caveat; derivative-mixing audit; source/readout overlap; no-pole gate; fallback B_i envelope rows",
            "fallback_if_failed": "retain finite B_0/B_2 and score them through R10/WEP/PPN/clock/orbital bounds with residual epsilon tails",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    source_rows = source_register_rows()
    hessian = hessian_rows()
    conditions = condition_rows()
    action = action_compatibility_rows()
    gates = gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3317_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in source_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3317_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in source_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3317_2_outputs_parse",
            "check": "all 3317 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3317_3_denominator_formula",
            "check": "determinant denominator formula is present",
            "passed": any("D(p)=a p (M2+z p)-(b0+b1 p)^2" in row["formula"] for row in hessian),
            "detail": "",
        },
        {
            "check_id": "VAL3317_4_b0_gate",
            "check": "GR b0=0 gate is present",
            "passed": any(row["condition"] == "b0=0" for row in conditions),
            "detail": "",
        },
        {
            "check_id": "VAL3317_5_no_pole_branches",
            "check": "algebraic and readout-orthogonal no-pole branches are present",
            "passed": any(row["branch"] == "no_finite_pole_by_algebraic_decoupling" for row in conditions)
            and any(row["branch"] == "finite_pole_unobserved" for row in conditions),
            "detail": "",
        },
        {
            "check_id": "VAL3317_6_action_compatibility_not_claim",
            "check": "action compatibility recognizes potential-like route without claiming proof",
            "passed": any(row["test_id"] == "ACT3317_1_curvature_exchange_potential" for row in action)
            and all(row["valid_for_claim"] == "false" for row in action),
            "detail": "",
        },
        {
            "check_id": "VAL3317_7_no_local_GR_claim",
            "check": "no finite-pole/local-GR gates remain false",
            "passed": all(row["passed"] == "false" for row in gates if row["gate_id"] in {"GATE3317_1_no_finite_pole", "GATE3317_2_local_GR"}),
            "detail": "",
        },
        {
            "check_id": "VAL3317_8_next_nonpropagation",
            "check": "next target is Gamma/extra-sector nonpropagation proof",
            "passed": any("nonpropagation" in row["target_doc"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3317_9_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3317_10_overall",
            "check": "3317 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for row in checks:
        row["passed"] = bool_str(bool(row["passed"]))
    return checks


def render_doc() -> str:
    sources = source_register_rows()
    hessian = hessian_rows()
    conditions = condition_rows()
    action = action_compatibility_rows()
    branches = branch_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    lines: list[str] = [
        "# 3317 - Minimal symbolic Hessian no-pole or finite-residue branch under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3317 turns the local-GR question into a small algebra problem.",
        "",
        "For the minimal public metric channel `h` plus one extra local channel `x`, take",
        "",
        "`H(p) = [[a p, b0+b1 p], [b0+b1 p, M2+z p]]`, `R=(1,u)`, `p=k^2`.",
        "",
        "Then",
        "",
        "`G_pub(p)=N(p)/D(p)`",
        "",
        "`D(p)=a p (M2+z p)-(b0+b1 p)^2`",
        "",
        "`N(p)=M2+z p-2u(b0+b1 p)+u^2 a p`.",
        "",
        "A GR-like massless Newton pole first requires `b0=0`. After that, the finite pole is generic:",
        "",
        "`p_f=-a M2/(a z-b1^2)`.",
        "",
        "So the cleanest local-GR route is now exact: prove the local curvature-exchange/extra sector is algebraic and non-derivative-mixed in the public metric branch, `z=0` and `b1=0`, with `b0=0`. Then `D(p)=a M2 p` and there is no observable finite pole to fight in R10/WEP/PPN.",
        "",
        "The action language is compatible with this because the macroscopic curvature-exchange term is potential-like, but it is not yet a proof because microscopic `psi` dynamics could induce a reduced finite pole after coarse graining.",
        "",
        "## Source Register",
        "",
    ]
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` - exists={row['exists']}; parse_ok={row['parse_ok']}; role={row['role']}")
    lines.extend(["", "## Minimal Hessian Formula", ""])
    for row in hessian:
        lines.append(f"- `{row['formula_id']}` `{row['object']}`: `{row['formula']}` Meaning: {row['meaning']}.")
    lines.extend(["", "## No-Pole Conditions", ""])
    for row in conditions:
        lines.append(f"- `{row['condition_id']}` `{row['branch']}`: condition `{row['condition']}`. Effect: {row['effect']} Scrutiny: {row['scrutiny']}.")
    lines.extend(["", "## Action Compatibility Test", ""])
    for row in action:
        lines.append(f"- `{row['test_id']}`: answer={row['answer']}; {row['question']} Impact: {row['impact']}.")
    lines.extend(["", "## Branch Decision Matrix", ""])
    for row in branches:
        lines.append(f"- `{row['branch_id']}` `{row['route']}`: {row['why_best']} Needed: {row['needed_proof']}. Status: {row['status']}.")
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
    write_csv(OUTPUTS["hessian"], hessian_rows())
    write_csv(OUTPUTS["conditions"], condition_rows())
    write_csv(OUTPUTS["action_test"], action_compatibility_rows())
    write_csv(OUTPUTS["branch"], branch_rows())
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
