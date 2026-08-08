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

DOC = ROOT / "3323-Y5-R2FR-parent-source-normalization-and-composite-no-tadpole-gate-under-AX1090.md"

SRC_ACTION = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
SRC_GRAVITY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
SRC_COMPACT = REPO / "core-mts-framework" / "gravity" / "gravity-as-emergent-mass-geometry-scaling-in-motion-timespace.md"

SOURCES = [
    {
        "source_id": "SRC3323_0_3322_doc",
        "path": ROOT / "3322-Y5-R2FR-Ci-projection-and-composite-contact-tail-gate-for-epsilon-grad-under-AX1090.md",
        "role": "C_i decomposition, source-normalization gap, composite-tail handoff",
    },
    {
        "source_id": "SRC3323_1_3322_Ci",
        "path": OUT / "P8_Y5_R2FR_3322_CI_RESPONSE_GATE.csv",
        "role": "projection / propagator / source-normalization factor split",
    },
    {
        "source_id": "SRC3323_2_3322_composite",
        "path": OUT / "P8_Y5_R2FR_3322_COMPOSITE_TAIL_GATE.csv",
        "role": "tadpole, loop, contact, boundary, anisotropy tail split",
    },
    {
        "source_id": "SRC3323_3_action",
        "path": SRC_ACTION,
        "role": "MTS action, emergent metric, kappa, matter coupling, gamma/lambda definitions",
    },
    {
        "source_id": "SRC3323_4_gravity",
        "path": SRC_GRAVITY,
        "role": "field equation, kappa Tmunu coupling, solar PPN weak-field scale",
    },
    {
        "source_id": "SRC3323_5_compact_newton",
        "path": SRC_COMPACT,
        "role": "compact-system Newtonian inverse-square recovery",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3323_SOURCE_REGISTER.csv",
    "normalization": OUT / "P8_Y5_R2FR_3323_NEWTON_NORMALIZATION_CONTRACT.csv",
    "circularity": OUT / "P8_Y5_R2FR_3323_G_CIRCULARITY_AUDIT.csv",
    "notadpole": OUT / "P8_Y5_R2FR_3323_NO_TADPOLE_COMPOSITE_GATE.csv",
    "em": OUT / "P8_Y5_R2FR_3323_EM_POYNTING_SOURCE_GATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3323_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3323_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3323_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3323_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1200) -> str:
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


def normalization_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NORM3323_0_metric_normalization",
            "object": "g_pub[psi]",
            "derived_contract": "g_pub_mu_nu = eta_mu_nu + N_psi S_ell[partial_mu psi partial_nu psi]",
            "meaning": "N_psi is the metric-readout normalization; without it, psi-covariance has shape but not absolute gravitational strength",
            "status": "CONTRACT_ADDED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NORM3323_1_EH_coefficient",
            "object": "induced Einstein-Hilbert term",
            "derived_contract": "Gamma_eff[g_pub] contains C_EH int sqrt(-g) R, with C_EH = c^4/(16 pi G_eff) = 1/(2 kappa_eff)",
            "meaning": "local GR normalization is fixed only when the microscopic psi measure/cutoff/spectrum produces C_EH or when C_EH is explicitly calibrated to measured G",
            "status": "DERIVED_MATCHING_CONDITION",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NORM3323_2_Poisson_limit",
            "object": "Newtonian potential",
            "derived_contract": "g_00 = -(1+2 Phi/c^2) and slow weak-field local limit requires nabla^2 Phi = 4 pi G_eff rho",
            "meaning": "inverse-square shape alone is not enough; the coefficient of the Poisson equation must be inherited from the same C_EH/source normalization",
            "status": "DERIVED_LOCAL_LIMIT_REQUIREMENT",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NORM3323_3_source_universality",
            "object": "matter coupling",
            "derived_contract": "S_matter must depend on matter fields only through g_pub and local fields: delta S_matter = 1/2 int sqrt(-g_pub) T^mu_nu delta g_pub_mu_nu",
            "meaning": "if true, WEP/Maxwell/orbital source coupling is universal metric coupling; if false, each direct psi-matter coupling must be bounded as a fifth-force source",
            "status": "DERIVED_UNIVERSALITY_GATE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NORM3323_4_Ci_source_factor",
            "object": "source_normalization_i in C_i",
            "derived_contract": "source_normalization_i = functional derivative of observable_i with respect to g_pub times the same kappa_eff/Poisson normalization",
            "meaning": "the source factor in 3322 is now tied to Newton/metric normalization, not an independent adjustable coupling",
            "status": "DERIVED_DEPENDENCE",
            "valid_for_claim": "false",
        },
    ]


def circularity_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "CIRC3323_0_action_kappa",
            "corpus_fact": "the current macroscopic MTS action contains kappa = 8 pi G/c^4",
            "verdict": "MATCHED_INPUT_NOT_DERIVED_G",
            "why_it_matters": "this is acceptable at GR-equivalence stage, but it is not a derivation of Newton's constant",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CIRC3323_1_micro_constants",
            "corpus_fact": "the current gamma/lambda definitions use G together with hbar,c and Phi_G",
            "verdict": "CIRCULAR_IF_USED_TO_DERIVE_G",
            "why_it_matters": "those definitions can set Planck-scale consistency after G is calibrated, but cannot independently derive G",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CIRC3323_2_compact_newton_shape",
            "corpus_fact": "compact systems recover g(r) proportional to r^-2 when m=0",
            "verdict": "SHAPE_DERIVED_COEFFICIENT_NOT_FIXED",
            "why_it_matters": "inverse-square behavior helps local Newtonian mechanics, but the absolute coefficient still needs C_EH/G_eff matching",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CIRC3323_3_allowed_closure",
            "corpus_fact": "GR itself takes G as measured coupling; an MTS local-GR reduction may also calibrate G while trying to derive deeper structure later",
            "verdict": "SAFE_CLOSURE_IF_DECLARED",
            "why_it_matters": "the honest near-term win is 'MTS reduces to GR/Newton with measured G', not 'MTS derives G' unless C_EH is computed from psi spectrum",
            "valid_for_claim": "false",
        },
    ]


def no_tadpole_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "TAD3323_0_stationary_background",
            "condition": "delta S_parent/delta psi evaluated at psi_bar equals zero after local constraints",
            "derived_effect": "kills the linear pi tadpole generated by expanding the parent action",
            "if_failed": "composite readout can mix back into a one-particle pole and local branch is not closed",
            "current_status": "CONDITION_DERIVED_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "TAD3323_1_one_point_silence",
            "condition": "<pi>_local = 0 and the one-particle projection P1 S_ell[grad pi grad pi] vanishes",
            "derived_effect": "prevents the quadratic public readout from acting like a hidden linear source",
            "if_failed": "epsilon_composite contains a finite single-pole residue",
            "current_status": "CONDITION_DERIVED_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "TAD3323_2_symmetry_or_selection_rule",
            "condition": "local fluctuation measure has pi -> -pi symmetry, Gaussian central limit symmetry, or an equivalent projection selection rule",
            "derived_effect": "sets odd correlators and one-particle composite overlap to zero",
            "if_failed": "interactions can permit composite/operator mixing and must be bounded",
            "current_status": "POSSIBLE_ROUTE_NOT_CLAIMED",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "TAD3323_3_two_particle_gap",
            "condition": "two-pi spectral branch is gapped or projected outside the finite-range local arena",
            "derived_effect": "turns loop/composite exchange into short-range or sub-threshold residue",
            "if_failed": "massless composite tail can be long-range and compete with PPN/R10/WEP tests",
            "current_status": "MASS_GAP_OR_PROJECTION_NOT_YET_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "TAD3323_4_contact_absorption",
            "condition": "contact terms are delta-supported inside source support and universally renormalize masses/G rather than producing finite external force",
            "derived_effect": "moves local coincident terms into calibration instead of fifth-force residuals",
            "if_failed": "R10/lab tests see an unbounded contact-like residual",
            "current_status": "COUNTERTERM_RULE_DERIVED_AS_GATE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def em_poynting_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EM3323_0_metric_Maxwell_route",
            "claim": "if EM uses only the universal metric action S_EM = -1/4 int sqrt(-g_pub) F_mu_nu F^mu_nu, the Poynting vector contributes through T_mu_nu",
            "effect": "EM energy flux is then part of T_mu_nu source/stress in the same metric coupling, not a separate hand-added force",
            "status": "GOOD_ROUTE_TO_TEST",
            "valid_for_claim": "false",
        },
        {
            "row_id": "EM3323_1_direct_psi_EM_coupling",
            "claim": "any term f(psi) F^2, J^mu A_mu psi, or nonmetric Poynting-background coupling is a new direct coupling",
            "effect": "must be put into C_i or epsilon_EM_Poynting_tail and bounded by clocks, WEP, optics, and lab EM tests",
            "status": "DANGER_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "EM3323_2_best_near_term_rule",
            "claim": "keep Poynting/EM in T_mu_nu unless a parent action explicitly derives a direct psi-EM vertex",
            "effect": "this is the least-scrutiny route because it preserves Maxwell/GR equivalence while still letting MTS explain the metric background",
            "status": "RECOMMENDED_DISCIPLINE",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3323_0_Newton_contract",
            "claim": "Newton/Poisson source-normalization contract is explicit",
            "passed": "true",
            "reason": "C_EH, kappa_eff, Poisson limit, and universal matter coupling are all stated as the required matching theorem",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3323_1_G_derived",
            "claim": "MTS derives Newton's constant from the parent psi action",
            "passed": "false",
            "reason": "current corpus uses G in kappa and in gamma/lambda definitions; deriving G requires an independent induced C_EH calculation",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3323_2_no_tadpole_closed",
            "claim": "composite one-particle tail is killed by parent stationarity/selection rule",
            "passed": "false",
            "reason": "the no-tadpole, one-point silence, selection-rule, gap/projection, and contact clauses are derived as gates but not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3323_3_EM_clean",
            "claim": "EM/Poynting contributes only through universal metric stress",
            "passed": "false",
            "reason": "recommended route is stated, but the parent matter action has not yet explicitly excluded direct psi-EM vertices",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3323_4_local_GR_claim",
            "claim": "local GR/Newton/Maxwell branch is claim-ready",
            "passed": "false",
            "reason": "normalization closure and no-tadpole/EM exclusions are not signed yet",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3323_0",
            "question": "Can MTS currently derive G rather than use it?",
            "answer": "not yet",
            "reason": "the current action and microscopic constants already contain G, so using them to derive G would be circular",
            "next_action": "either declare measured-G closure for the GR-limit paper or compute induced C_EH from psi spectrum/cutoff",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3323_1",
            "question": "Did we still move forward?",
            "answer": "yes",
            "reason": "the coupling problem is now a precise matching theorem: calculate C_EH and prove universal source coupling/no-tadpole, or mark them as explicit closures",
            "next_action": "attack C_EH induced-gravity coefficient or write closure-grade local-GR theorem",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3323_2",
            "question": "Where should EM/Poynting live?",
            "answer": "inside T_munu unless a parent direct vertex is derived",
            "reason": "this preserves Maxwell/GR equivalence and avoids creating an unconstrained fifth-force channel",
            "next_action": "add a matter-action exclusion gate for direct psi-EM couplings",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3324-Y5-R2FR-induced-EH-coefficient-or-measured-G-closure-local-GR-theorem-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3324_induced_EH_coefficient_or_measured_G_closure_local_GR_theorem.py",
            "objective": "choose the less fragile route: either derive an induced Einstein-Hilbert coefficient C_EH from psi covariance, or formalize measured-G closure as the honest local-GR reduction theorem",
            "must_include": "weak-field Poisson matching; kappa_eff; source universality; no direct psi-EM vertex; no-tadpole assumptions; explicit statement that G is calibrated unless C_EH is computed",
            "fallback_if_failed": "local-GR route remains closure-only with measured G and explicit C_i/epsilon_composite nuisance bounds",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    normalization = normalization_contract_rows()
    circularity = circularity_rows()
    tadpole = no_tadpole_rows()
    em_rows = em_poynting_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3323_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3323_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3323_2_outputs_parse",
            "check": "all 3323 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3323_3_Newton_contract",
            "check": "normalization rows include C_EH, Poisson, and universal matter coupling",
            "passed": {"induced Einstein-Hilbert term", "Newtonian potential", "matter coupling"}.issubset(
                {row["object"] for row in normalization}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3323_4_G_circularity",
            "check": "G circularity audit identifies input kappa and gamma/lambda risk",
            "passed": any(row["audit_id"] == "CIRC3323_0_action_kappa" for row in circularity)
            and any(row["verdict"] == "CIRCULAR_IF_USED_TO_DERIVE_G" for row in circularity),
            "detail": "",
        },
        {
            "check_id": "VAL3323_5_no_tadpole_conditions",
            "check": "no-tadpole gate includes stationarity, one-point silence, selection rule, two-particle gap, and contact absorption",
            "passed": {"TAD3323_0_stationary_background", "TAD3323_1_one_point_silence", "TAD3323_2_symmetry_or_selection_rule", "TAD3323_3_two_particle_gap", "TAD3323_4_contact_absorption"}.issubset(
                {row["gate_id"] for row in tadpole}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3323_6_EM_Poynting",
            "check": "EM/Poynting gate distinguishes metric stress from direct psi-EM coupling",
            "passed": any("Poynting" in row["claim"] and "T_mu_nu" in row["effect"] for row in em_rows)
            and any("direct psi-EM" in row["claim"] for row in em_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3323_7_no_full_claim",
            "check": "G-derived, no-tadpole, EM-clean, and local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3323_1_G_derived", "GATE3323_2_no_tadpole_closed", "GATE3323_3_EM_clean", "GATE3323_4_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3323_8_next_CEH_or_closure",
            "check": "next target is induced EH coefficient or measured-G closure theorem",
            "passed": any("induced Einstein-Hilbert coefficient" in row["objective"] and "measured-G closure" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3323_9_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3323_10_overall",
            "check": "3323 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3323 - Parent source-normalization and composite no-tadpole gate under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3323 pins the coupling problem down to a theorem, not a vibe.",
        "",
        "The local-GR/Newton branch needs two separate facts:",
        "",
        "1. Source normalization: `g_pub = eta + N_psi S[grad psi grad psi]` must induce or calibrate an Einstein-Hilbert coefficient",
        "",
        "`C_EH = c^4/(16 pi G_eff) = 1/(2 kappa_eff)`,",
        "",
        "so the weak-field metric `g_00 = -(1+2 Phi/c^2)` obeys",
        "",
        "`nabla^2 Phi = 4 pi G_eff rho`.",
        "",
        "2. Composite silence: the quadratic public readout `S[grad pi grad pi]` must not hide a one-particle tadpole, and any two-particle/contact/boundary residue must be short-range, absorbed, or explicitly bounded.",
        "",
        "The current corpus already contains `kappa = 8 pi G/c^4`, and the microscopic `gamma/lambda` definitions also use `G`. Therefore MTS has not yet derived Newton's constant. It can honestly claim a GR-limit closure with measured `G`, or it must compute `C_EH` independently from the psi spectrum/cutoff. That is the next fork.",
        "",
        "For EM/Poynting: the clean route is to keep EM energy flux inside `T_munu` through the universal Maxwell action on `g_pub`. Any direct `psi`-EM/Poynting vertex is a new coupling and must be bounded separately.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Newton Normalization Contract", normalization_contract_rows(), "row_id"),
        ("G Circularity Audit", circularity_rows(), "audit_id"),
        ("No-Tadpole Composite Gate", no_tadpole_rows(), "gate_id"),
        ("EM/Poynting Source Gate", em_poynting_rows(), "row_id"),
        ("Promotion Gates", promotion_gate_rows(), "gate_id"),
        ("Decision Ledger", decision_rows(), "decision_id"),
        ("Next Target", next_target_rows(), "target_doc"),
    ]
    for title, rows, key_name in sections:
        lines.extend(["", f"## {title}", ""])
        for row in rows:
            label = row.get(key_name, "")
            body = "; ".join(f"{key}={value}" for key, value in row.items() if key != key_name)
            lines.append(f"- `{label}`: {body}")
    lines.extend(
        [
            "",
            "## Test Notes",
            "",
            "- This checkpoint is private and nonclaim.",
            "- It advances the derivation by turning source coupling into an explicit `C_EH/kappa_eff/Poisson` matching condition.",
            "- It rejects deriving `G` from current `gamma/lambda` definitions because those already contain `G`.",
            "- It gives a clear no-tadpole route for the composite term, but does not claim it is parent-signed.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["normalization"], normalization_contract_rows())
    write_csv(OUTPUTS["circularity"], circularity_rows())
    write_csv(OUTPUTS["notadpole"], no_tadpole_rows())
    write_csv(OUTPUTS["em"], em_poynting_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
