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

DOC = ROOT / "3319-Y5-R2FR-psi-coarse-graining-no-finite-public-residue-or-Bi-bound-under-AX1090.md"

SRC_ACTION_FUND = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
SRC_ACTION_MOTION = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"

SOURCES = [
    {
        "source_id": "SRC3319_0_3318_doc",
        "path": ROOT / "3318-Y5-R2FR-Gamma-extra-sector-nonpropagation-proof-or-Bi-envelope-under-AX1090.md",
        "role": "3318 handoff to psi coarse-graining theorem",
    },
    {
        "source_id": "SRC3319_1_3318_theorem",
        "path": OUT / "P8_Y5_R2FR_3318_NONPROPAGATION_THEOREM_ATTEMPT.csv",
        "role": "Gamma no-pole and psi caveat",
    },
    {
        "source_id": "SRC3319_2_3318_fallback",
        "path": OUT / "P8_Y5_R2FR_3318_BI_ENVELOPE_FALLBACK.csv",
        "role": "B_i envelope fallback rows",
    },
    {
        "source_id": "SRC3319_3_fundamental_action",
        "path": SRC_ACTION_FUND,
        "role": "g_pub covariance map and psi derivative action",
    },
    {
        "source_id": "SRC3319_4_motion_action",
        "path": SRC_ACTION_MOTION,
        "role": "smoothed gradient covariance construction",
    },
    {
        "source_id": "SRC3319_5_3316_factor",
        "path": OUT / "P8_Y5_R2FR_3316_A_FACTOR_UPDATE.csv",
        "role": "B_i invariant residue law",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3319_SOURCE_REGISTER.csv",
    "evidence": OUT / "P8_Y5_R2FR_3319_PSI_EVIDENCE_EXTRACT.csv",
    "linearization": OUT / "P8_Y5_R2FR_3319_PSI_READOUT_LINEARIZATION.csv",
    "pole": OUT / "P8_Y5_R2FR_3319_POLE_CLASSIFICATION.csv",
    "fallback": OUT / "P8_Y5_R2FR_3319_BI_GRADIENT_ENVELOPE_FALLBACK.csv",
    "gates": OUT / "P8_Y5_R2FR_3319_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3319_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3319_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3319_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

PATTERNS = [
    "g_{μν}",
    "g_{Î¼Î½}",
    "smoothed covariance",
    "∂_μ",
    "âˆ‚_Î¼",
    "∂_t",
    "âˆ‚_t",
    "∇",
    "âˆ‡",
    "A_MTS",
    "L_MTS",
    "ψ",
    "Ïˆ",
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
    hits: list[str] = []
    lowers = [pattern.lower() for pattern in patterns]
    for index, line in enumerate(text.splitlines(), start=1):
        lower_line = line.lower()
        if any(pattern in lower_line for pattern in lowers):
            hits.append(f"L{index}:{line.strip()}")
        if len(hits) >= max_hits:
            break
    return " | ".join(hits)


def evidence_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        text = text_for(path)
        rows.append(
            {
                "evidence_id": f"EVID3319_{len(rows)}",
                "source_id": source["source_id"],
                "path": str(path),
                "has_metric_covariance_map": bool_str("smoothed covariance" in text or "∂_μψ" in text or "âˆ‚_Î¼Ïˆ" in text or "<partial psi partial psi>" in text),
                "has_psi_derivative_kinetic": bool_str(("A_MTS" in text or "L_MTS" in text) and ("∂_t" in text or "âˆ‚_t" in text or "∇" in text or "âˆ‡" in text)),
                "has_Bi_fallback": bool_str("B_0" in text or "B_2" in text or "B_i" in text),
                "hits": find_hits(path, PATTERNS),
                "valid_for_claim": "false",
            }
        )
    return rows


def linearization_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "LIN3319_0_define_map",
            "claim": "The public metric is a smoothed derivative covariance of psi.",
            "formula": "g_pub_mu_nu = eta_mu_nu + S[partial_mu psi partial_nu psi]",
            "derivation": "This is the map stated by the action corpus; S denotes the smoothing/coarse-graining operation.",
            "status": "SOURCE_BACKED_MAP",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LIN3319_1_split_field",
            "claim": "Linearize around a local background psi_bar.",
            "formula": "psi = psi_bar + pi",
            "derivation": "pi is the microscopic fluctuation whose public finite residue would become B_i if it couples linearly to g_pub.",
            "status": "DERIVATION_SETUP",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LIN3319_2_first_variation",
            "claim": "The first public readout variation is proportional to the background gradient.",
            "formula": "delta g_pub_mu_nu = S[partial_mu psi_bar partial_nu pi + partial_mu pi partial_nu psi_bar]",
            "derivation": "Differentiate the quadratic covariance map. No term linear in pi survives unless a background gradient/readout is present.",
            "status": "DERIVED",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LIN3319_3_stationary_zero",
            "claim": "A zero-gradient or first-gradient-silent local vacuum has no linear single-pi public readout.",
            "formula": "if S[partial_(mu psi_bar partial_{nu)} pi]=0 for all allowed pi, then R_pi=delta g_pub/delta pi=0",
            "derivation": "The readout vector R in G_pub=R H^{-1} R^T vanishes for the microscopic psi fluctuation at tree level.",
            "status": "CONDITIONAL_TREE_LEVEL_NO_POLE",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LIN3319_4_nonzero_gradient",
            "claim": "Nonzero coherent background gradient revives the finite residue channel.",
            "formula": "R_pi_mu_nu ~ S[partial_(mu psi_bar partial_{nu)} .], so B_pi scales with the squared local gradient/readout overlap",
            "derivation": "If local memory/cosmological/galactic gradients survive smoothing, psi fluctuations can feed a public finite residue and must be bounded.",
            "status": "BOUND_BRANCH",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LIN3319_5_second_order",
            "claim": "The quadratic pi-pi term is not a tree-level single-pole public readout.",
            "formula": "delta^2 g_pub_mu_nu = 2 S[partial_mu pi partial_nu pi]",
            "derivation": "This can renormalize the EH/contact sector or produce composite/loop effects, but it is not the linear R_pi that creates a classical single-exchange fifth-force pole.",
            "status": "CONTACT_OR_COMPOSITE_CAVEAT",
            "valid_for_claim": "false",
        },
    ]


def pole_rows() -> list[dict[str, Any]]:
    return [
        {
            "pole_id": "POLE3319_0_tree_single_pi",
            "branch": "stationary local vacuum",
            "readout": "R_pi=0",
            "result_for_Bi": "B_pi_tree=0",
            "proof_status": "CONDITIONAL_ON_FIRST_GRADIENT_SILENCE",
            "claim_scope": "kills tree-level single-psi finite public pole only",
            "valid_for_claim": "false",
        },
        {
            "pole_id": "POLE3319_1_background_gradient",
            "branch": "nonzero local/cosmological/galactic memory gradient",
            "readout": "R_pi != 0",
            "result_for_Bi": "B_pi <= C_smooth |grad psi_bar|^2 |G_pi| with projector factors",
            "proof_status": "ENVELOPE_REQUIRED",
            "claim_scope": "finite public residue must be bounded against local tests",
            "valid_for_claim": "false",
        },
        {
            "pole_id": "POLE3319_2_composite_pi_pi",
            "branch": "quadratic public readout",
            "readout": "delta^2 g_pub ~ S[partial pi partial pi]",
            "result_for_Bi": "not a classical linear Yukawa pole unless composite channel has long-range coherent support",
            "proof_status": "CONTACT_OR_COMPOSITE_NOT_FULLY_CLASSIFIED",
            "claim_scope": "requires induced-EH/contact split",
            "valid_for_claim": "false",
        },
        {
            "pole_id": "POLE3319_3_EH_emergence",
            "branch": "massless GR channel",
            "readout": "coarse-grained covariance collective mode",
            "result_for_Bi": "not evaluated here",
            "proof_status": "MASSLESS_EH_NORMALIZATION_REMAINS",
            "claim_scope": "local GR still needs induced EH/Newton normalization",
            "valid_for_claim": "false",
        },
    ]


def fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PGE3319_0_gradient_envelope",
            "quantity": "epsilon_grad",
            "definition": "dimensionless local first-gradient readout envelope for S[partial psi_bar partial pi]",
            "bound_law": "|B_i^psi| <= C_i(lambda,S,H_pi) epsilon_grad^2 + composite_tail",
            "needed_input": "local vacuum/solar/system gradient bound or theorem zero",
            "valid_for_claim": "false",
        },
        {
            "row_id": "PGE3319_1_smoothing_kernel",
            "quantity": "C_i(lambda,S,H_pi)",
            "definition": "smoothing-kernel and psi-propagator projection from microscopic pi to public metric residue",
            "bound_law": "compute from S kernel, H_pi inverse, and spin/projector extraction",
            "needed_input": "explicit smoothing kernel or conservative scale separation bound",
            "valid_for_claim": "false",
        },
        {
            "row_id": "PGE3319_2_composite_tail",
            "quantity": "epsilon_composite",
            "definition": "quadratic pi-pi contact/loop/composite public readout tail",
            "bound_law": "separate local contact renormalization from any long-range coherent composite mode",
            "needed_input": "two-point/four-point covariance or induced-gravity effective action",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3319_0_linearization",
            "claim": "first variation of g_pub covariance map is derived",
            "passed": "true",
            "reason": "delta g_pub = S[partial psi_bar partial pi + partial pi partial psi_bar]",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3319_1_tree_no_pole_condition",
            "claim": "tree-level single-psi finite public pole vanishes if first-gradient readout is silent",
            "passed": "true",
            "reason": "R_pi=0 implies R H^{-1} R^T has no single-pi public pole",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3319_2_parent_gradient_silence",
            "claim": "MTS parent action proves first-gradient silence in the real local branch",
            "passed": "false",
            "reason": "local stationary/zero-gradient condition is not yet parent-signed across matter, clocks, and boundaries",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3319_3_full_local_GR",
            "claim": "local GR/Newtonian limit is fully derived",
            "passed": "false",
            "reason": "massless EH normalization, composite/contact split, and gradient envelope remain",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3319_0",
            "question": "Did 3319 make a real derivation?",
            "answer": "yes: it derives the linear public readout of psi and shows the tree-level finite residue vanishes when the local first-gradient readout is silent",
            "reason": "the public metric map is quadratic in psi gradients, so its first variation is proportional to the background gradient",
            "next_action": "prove or bound local first-gradient silence instead of treating B_i as primary",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3319_1",
            "question": "What is not solved?",
            "answer": "full local GR",
            "reason": "we still need parent-signed local gradient silence, induced EH/Newton normalization, and the composite/contact split",
            "next_action": "attack local first-gradient silence and scale-separation smoothing",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3319_2",
            "question": "How does this change testing?",
            "answer": "finite B_i is now a background-gradient/composite-tail envelope, not the default tree-level coupling",
            "reason": "if R_pi=0, the direct Yukawa-like residue is absent; nonzero gradients revive it with a calculable envelope",
            "next_action": "build epsilon_grad rows and connect them to local/solar/cosmological environments",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3320-Y5-R2FR-local-first-gradient-silence-or-gradient-envelope-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3320_local_first_gradient_silence_or_gradient_envelope.py",
            "objective": "prove or bound the local first-gradient readout S[partial_(mu) psi_bar partial_(nu) pi] in solar/lab vacuum so the 3319 tree-level no-pole condition becomes parent-signed or becomes an explicit epsilon_grad envelope",
            "must_include": "local vacuum/stationary branch; smoothing kernel assumptions; matter boundary/source terms; cosmological/galactic gradient leakage; epsilon_grad units; WEP/R10/PPN routing",
            "fallback_if_failed": "retain B_i^psi <= C_i epsilon_grad^2 + composite_tail and score it empirically",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    evidence = evidence_rows()
    lin = linearization_rows()
    poles = pole_rows()
    gates = gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3319_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3319_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3319_2_outputs_parse",
            "check": "all 3319 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3319_3_evidence_covariance_kinetic",
            "check": "evidence includes covariance map and psi derivative kinetic action",
            "passed": any(row["has_metric_covariance_map"] == "true" for row in evidence)
            and any(row["has_psi_derivative_kinetic"] == "true" for row in evidence),
            "detail": "",
        },
        {
            "check_id": "VAL3319_4_first_variation",
            "check": "first variation formula is present",
            "passed": any("delta g_pub_mu_nu" in row["formula"] and "psi_bar" in row["formula"] for row in lin),
            "detail": "",
        },
        {
            "check_id": "VAL3319_5_tree_zero",
            "check": "tree-level no-pole condition is present",
            "passed": any(row["result_for_Bi"] == "B_pi_tree=0" for row in poles),
            "detail": "",
        },
        {
            "check_id": "VAL3319_6_gradient_fallback",
            "check": "nonzero gradient fallback envelope is present",
            "passed": any("gradient" in row["branch"] and row["proof_status"] == "ENVELOPE_REQUIRED" for row in poles),
            "detail": "",
        },
        {
            "check_id": "VAL3319_7_no_full_local_GR_claim",
            "check": "parent gradient silence and full local-GR gates remain false",
            "passed": all(row["passed"] == "false" for row in gates if row["gate_id"] in {"GATE3319_2_parent_gradient_silence", "GATE3319_3_full_local_GR"}),
            "detail": "",
        },
        {
            "check_id": "VAL3319_8_next_gradient",
            "check": "next target is local first-gradient silence/envelope",
            "passed": any("local-first-gradient-silence" in row["target_doc"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3319_9_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(row["passed"]) for row in checks)
    checks.append(
        {
            "check_id": "VAL3319_10_overall",
            "check": "3319 validation overall",
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
    lin = linearization_rows()
    poles = pole_rows()
    fallback = fallback_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    lines: list[str] = [
        "# 3319 - Psi coarse-graining no finite public residue or Bi bound under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3319 derives the key public-readout fact for the microscopic `psi` route.",
        "",
        "The source map is",
        "",
        "`g_pub_mu_nu = eta_mu_nu + S[partial_mu psi partial_nu psi]`.",
        "",
        "Writing `psi = psi_bar + pi`, the first variation is",
        "",
        "`delta g_pub_mu_nu = S[partial_mu psi_bar partial_nu pi + partial_mu pi partial_nu psi_bar]`.",
        "",
        "Therefore, in a local vacuum branch where the first-gradient readout is silent, `R_pi = 0` and the tree-level single-`pi` public finite residue vanishes:",
        "",
        "`B_pi_tree = 0`.",
        "",
        "This is a real structural advance. The remaining problem is no longer a generic finite coupling; it is the local first-gradient silence theorem or an explicit `epsilon_grad` envelope. Full local GR is still not claimed because EH/Newton normalization, composite/contact terms, and background-gradient leakage remain.",
        "",
        "## Source Register",
        "",
    ]
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` - exists={row['exists']}; parse_ok={row['parse_ok']}; role={row['role']}")
    lines.extend(["", "## Psi Evidence Extract", ""])
    for row in evidence:
        lines.append(
            f"- `{row['evidence_id']}` `{row['source_id']}`: covariance={row['has_metric_covariance_map']}; kinetic={row['has_psi_derivative_kinetic']}; Bfallback={row['has_Bi_fallback']}; hits={row['hits']}"
        )
    lines.extend(["", "## Psi Readout Linearization", ""])
    for row in lin:
        lines.append(f"- `{row['step_id']}` `{row['status']}`: {row['claim']} Formula: `{row['formula']}` {row['derivation']}")
    lines.extend(["", "## Pole Classification", ""])
    for row in poles:
        lines.append(
            f"- `{row['pole_id']}` `{row['branch']}`: readout={row['readout']}; result={row['result_for_Bi']}; status={row['proof_status']}; scope={row['claim_scope']}."
        )
    lines.extend(["", "## Bi Gradient Envelope Fallback", ""])
    for row in fallback:
        lines.append(f"- `{row['row_id']}` `{row['quantity']}`: {row['definition']} Law: {row['bound_law']}. Needed: {row['needed_input']}.")
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
    write_csv(OUTPUTS["linearization"], linearization_rows())
    write_csv(OUTPUTS["pole"], pole_rows())
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
