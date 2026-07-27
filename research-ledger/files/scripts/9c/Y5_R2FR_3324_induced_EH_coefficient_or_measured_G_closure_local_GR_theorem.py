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

DOC = ROOT / "3324-Y5-R2FR-induced-EH-coefficient-or-measured-G-closure-local-GR-theorem-under-AX1090.md"

SRC_ACTION = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
SRC_GRAVITY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
SRC_COMPACT = REPO / "core-mts-framework" / "gravity" / "gravity-as-emergent-mass-geometry-scaling-in-motion-timespace.md"

SOURCES = [
    {
        "source_id": "SRC3324_0_3323_doc",
        "path": ROOT / "3323-Y5-R2FR-parent-source-normalization-and-composite-no-tadpole-gate-under-AX1090.md",
        "role": "source normalization, G circularity, no-tadpole, EM/Poynting handoff",
    },
    {
        "source_id": "SRC3324_1_3323_norm",
        "path": OUT / "P8_Y5_R2FR_3323_NEWTON_NORMALIZATION_CONTRACT.csv",
        "role": "C_EH/kappa_eff/Poisson matching contract",
    },
    {
        "source_id": "SRC3324_2_3323_circularity",
        "path": OUT / "P8_Y5_R2FR_3323_G_CIRCULARITY_AUDIT.csv",
        "role": "why current corpus does not derive G",
    },
    {
        "source_id": "SRC3324_3_3323_tadpole",
        "path": OUT / "P8_Y5_R2FR_3323_NO_TADPOLE_COMPOSITE_GATE.csv",
        "role": "stationarity/no-tadpole/contact requirements",
    },
    {
        "source_id": "SRC3324_4_3323_em",
        "path": OUT / "P8_Y5_R2FR_3323_EM_POYNTING_SOURCE_GATE.csv",
        "role": "EM/Poynting metric-stress route",
    },
    {
        "source_id": "SRC3324_5_action",
        "path": SRC_ACTION,
        "role": "emergent metric, Sakharov analogy, EH action, kappa, matter action",
    },
    {
        "source_id": "SRC3324_6_gravity",
        "path": SRC_GRAVITY,
        "role": "MTS extended Einstein equation, kappa Tmunu, solar PPN suppression",
    },
    {
        "source_id": "SRC3324_7_compact_newton",
        "path": SRC_COMPACT,
        "role": "compact-system inverse-square/Newtonian shape recovery",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3324_SOURCE_REGISTER.csv",
    "induced": OUT / "P8_Y5_R2FR_3324_INDUCED_EH_ATTEMPT.csv",
    "closure": OUT / "P8_Y5_R2FR_3324_MEASURED_G_CLOSURE_THEOREM.csv",
    "poisson": OUT / "P8_Y5_R2FR_3324_POISSON_LIMIT_DERIVATION.csv",
    "em": OUT / "P8_Y5_R2FR_3324_MAXWELL_EM_STRESS_CLEAN_ROUTE.csv",
    "assumptions": OUT / "P8_Y5_R2FR_3324_CLOSURE_ASSUMPTION_LEDGER.csv",
    "gates": OUT / "P8_Y5_R2FR_3324_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3324_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3324_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3324_VALIDATION.csv",
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


def induced_eh_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "IEH3324_0_structural_route",
            "target": "induced Einstein-Hilbert coefficient",
            "formula": "Gamma_eff[g_pub] = Gamma_0 + C_EH^ind int sqrt(-g_pub) R[g_pub] + higher-derivative terms",
            "derived_status": "STRUCTURAL_ROUTE_PRESENT",
            "missing_for_numeric": "spectral measure, cutoff, readout normalization, sign/stability, counterterm rule",
            "valid_for_claim": "false",
        },
        {
            "row_id": "IEH3324_1_dimensional_coefficient",
            "target": "C_EH^ind",
            "formula": "C_EH^ind = eta_EH N_eff Lambda_eff^2 + C_EH^bare, with eta_EH set by the fluctuation measure/heat-kernel content",
            "derived_status": "DIMENSIONAL_AND_HEAT_KERNEL_CONTRACT",
            "missing_for_numeric": "eta_EH, N_eff, Lambda_eff=1/ell_s or other parent cutoff, and whether C_EH^bare is zero",
            "valid_for_claim": "false",
        },
        {
            "row_id": "IEH3324_2_G_relation",
            "target": "G_eff",
            "formula": "G_eff = c^4/(16 pi C_EH^ind) and kappa_eff = 1/(2 C_EH^ind)",
            "derived_status": "MATCHING_RELATION_DERIVED",
            "missing_for_numeric": "C_EH^ind is not computed from parent psi spectrum",
            "valid_for_claim": "false",
        },
        {
            "row_id": "IEH3324_3_no_G_derivation",
            "target": "derive Newton constant",
            "formula": "current gamma/lambda definitions cannot be used to derive G because G already appears in them",
            "derived_status": "REJECTED_AS_CIRCULAR",
            "missing_for_numeric": "independent parent spectral calculation not containing measured G",
            "valid_for_claim": "false",
        },
    ]


def measured_g_closure_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "MGC3324_0_conditional_local_GR",
            "assumptions": "Lorentzian g_pub from psi covariance; measured kappa_eff=8 pi G_N/c^4; universal matter action S_matter[g_pub,Psi]; local Gamma_G/saturation and finite psi residues suppressed by 3319-3323 gates",
            "conclusion": "field equations reduce locally to G_munu[g_pub] = kappa_eff T_munu + subthreshold residuals",
            "status": "CONDITIONAL_THEOREM_FORMALIZED",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MGC3324_1_Newton_limit",
            "assumptions": "weak field g_00=-(1+2 Phi/c^2), slow sources, pressure negligible, local residuals below threshold",
            "conclusion": "00 equation gives nabla^2 Phi = 4 pi G_N rho plus bounded MTS residual",
            "status": "CONDITIONAL_NEWTON_LIMIT",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MGC3324_2_Maxwell_limit",
            "assumptions": "EM enters through S_EM[g_pub,A] only, with no f(psi)F^2 or nonmetric Poynting vertex",
            "conclusion": "Maxwell stress and Poynting flux contribute through T_munu^EM and obey the same local-GR coupling",
            "status": "CONDITIONAL_MAXWELL_STRESS_LIMIT",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "MGC3324_3_closure_scope",
            "assumptions": "G_N is calibrated from experiment rather than derived from psi spectrum",
            "conclusion": "this is a serious local-GR reduction route, but not a derivation of Newton's constant",
            "status": "HONEST_MEASURED_G_CLOSURE",
            "valid_for_claim": "false",
        },
    ]


def poisson_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "POI3324_0_metric",
            "statement": "take g_00 = -(1+2 Phi/c^2), g_ij=(1-2 Phi/c^2) delta_ij, slow weak-field local branch",
            "result": "curvature is first order in Phi/c^2",
            "valid_for_claim": "false",
        },
        {
            "step_id": "POI3324_1_equation",
            "statement": "with Gamma_G and psi residuals suppressed, local equation is G_munu = 8 pi G_N T_munu/c^4",
            "result": "the 00 component is controlled by mass density rho",
            "valid_for_claim": "false",
        },
        {
            "step_id": "POI3324_2_poisson",
            "statement": "standard weak-field reduction gives G_00 approximately 2 nabla^2 Phi/c^2 and T_00 approximately rho c^2",
            "result": "nabla^2 Phi = 4 pi G_N rho",
            "valid_for_claim": "false",
        },
        {
            "step_id": "POI3324_3_mts_residual",
            "statement": "MTS corrections enter as delta_Phi satisfying |delta local observable| <= C_i epsilon_eff^2 + epsilon_composite_i",
            "result": "Newtonian limit is recovered up to the already bounded 3319-3323 residual envelope",
            "valid_for_claim": "false",
        },
    ]


def maxwell_em_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MEM3324_0_universal_action",
            "route": "S_EM[g_pub,A] = -1/4 int sqrt(-g_pub) F_munu F^munu",
            "consequence": "EM stress tensor is obtained by variation with respect to g_pub; Poynting flux is part of T_munu^EM",
            "status": "CLEAN_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "MEM3324_1_forbidden_direct_vertices",
            "route": "exclude f(psi)F^2, psi J^mu A_mu, or Poynting-background force terms unless derived from parent symmetry",
            "consequence": "direct vertices would be fifth-force/clock/optics channels and must be separately bounded",
            "status": "EXCLUSION_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "MEM3324_2_test_mapping",
            "route": "if only universal metric coupling exists, EM tests inherit the same PPN/local-GR residual envelope",
            "consequence": "clock/EM/Poynting arena uses C_clock epsilon_eff^2 + epsilon_EM_composite_tail",
            "status": "TEST_ROUTING_READY",
            "valid_for_claim": "false",
        },
    ]


def closure_assumption_rows() -> list[dict[str, Any]]:
    return [
        {
            "assumption_id": "ASS3324_0_metric_readout",
            "assumption": "g_pub is Lorentzian and equals eta + N_psi S[grad psi grad psi] in the local branch",
            "status": "PARTIAL_PARENT_SUPPORT",
            "needed_to_claim": "fix N_psi or absorb it into measured-G closure",
            "valid_for_claim": "false",
        },
        {
            "assumption_id": "ASS3324_1_kappa_closure",
            "assumption": "kappa_eff is calibrated to measured G_N unless C_EH^ind is computed",
            "status": "HONEST_CLOSURE_ALLOWED",
            "needed_to_claim": "state explicitly in any public theorem",
            "valid_for_claim": "false",
        },
        {
            "assumption_id": "ASS3324_2_universal_matter",
            "assumption": "matter, including EM, couples through g_pub only",
            "status": "NOT_PARENT_SIGNED",
            "needed_to_claim": "matter action descent/no-direct-psi-vertex proof",
            "valid_for_claim": "false",
        },
        {
            "assumption_id": "ASS3324_3_local_residual_suppression",
            "assumption": "Gamma_G/saturation, psi tree residue, and composite tail are suppressed below local bounds",
            "status": "BOUNDED_CONTRACT_NOT_NUMERICALLY_CLOSED",
            "needed_to_claim": "complete C_i, epsilon_composite, and local projection/source bounds",
            "valid_for_claim": "false",
        },
        {
            "assumption_id": "ASS3324_4_no_tadpole",
            "assumption": "parent local vacuum is stationary and quadratic readout has no one-particle projection",
            "status": "NOT_PARENT_SIGNED",
            "needed_to_claim": "stationarity/selection-rule proof",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3324_0_induced_attempt",
            "claim": "induced-EH route has been attempted and reduced to explicit missing parent inputs",
            "passed": "true",
            "reason": "C_EH^ind contract and required spectral/cutoff inputs are written explicitly",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3324_1_induced_CEH_numeric",
            "claim": "C_EH is numerically derived from psi parent spectrum",
            "passed": "false",
            "reason": "spectral measure, cutoff/readout normalization, sign, and counterterm rule are absent",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3324_2_measured_G_theorem",
            "claim": "conditional measured-G local-GR/Newton/Maxwell closure theorem is formalized",
            "passed": "true",
            "reason": "field equation, Poisson limit, Maxwell stress route, and residual envelope are stated as a conditional theorem",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3324_3_parent_assumptions_signed",
            "claim": "all closure assumptions are parent-signed",
            "passed": "false",
            "reason": "universal matter/no direct psi-EM, no-tadpole, and numeric residual bounds remain open",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3324_4_unconditional_local_GR",
            "claim": "MTS unconditionally reduces to local GR/Newton/Maxwell",
            "passed": "false",
            "reason": "the theorem is conditional and measured-G closure is not a derivation of G",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3324_0",
            "question": "Can 3324 derive C_EH/G from current files?",
            "answer": "no",
            "reason": "the corpus references Sakharov-like emergence but does not supply the spectral measure/cutoff coefficient, and it already uses G in kappa and microscopic constants",
            "next_action": "do not claim derived G; keep induced C_EH as a future parent calculation",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3324_1",
            "question": "What can be claimed internally now?",
            "answer": "a conditional measured-G local-GR closure theorem",
            "reason": "this matches what GR itself does with G while letting MTS focus on deriving metric emergence, residual suppression, and source universality",
            "next_action": "parent-sign universal matter/no-direct-psi-vertex and no-tadpole assumptions",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3324_2",
            "question": "Is this a retreat?",
            "answer": "no",
            "reason": "it separates two wins: local-GR equivalence with measured G now, deeper derivation of G later if induced C_EH can be computed",
            "next_action": "write the closure theorem into the spine only after assumptions are signed",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3325-Y5-R2FR-universal-matter-no-direct-psi-vertex-and-no-tadpole-signature-gate-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3325_universal_matter_no_direct_psi_vertex_and_no_tadpole_signature_gate.py",
            "objective": "parent-sign the assumptions needed by the measured-G local-GR theorem: universal metric matter coupling, no direct psi-EM/Poynting vertex, and no composite one-particle tadpole",
            "must_include": "matter action descent; EM Maxwell stress route; direct vertex exclusion; local vacuum stationarity; pi -> -pi or projection selection rule; residual bound routing",
            "fallback_if_failed": "local-GR route remains a conditional closure theorem rather than a parent-derived branch",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    induced = induced_eh_attempt_rows()
    closure = measured_g_closure_rows()
    poisson = poisson_derivation_rows()
    em_rows = maxwell_em_rows()
    assumptions = closure_assumption_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3324_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3324_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3324_2_outputs_parse",
            "check": "all 3324 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3324_3_induced_inputs_explicit",
            "check": "induced EH attempt records missing spectral/cutoff inputs and G relation",
            "passed": any("spectral measure" in row["missing_for_numeric"] for row in induced)
            and any("G_eff" in row["target"] for row in induced),
            "detail": "",
        },
        {
            "check_id": "VAL3324_4_measured_G_theorem",
            "check": "measured-G theorem includes local GR, Newton, Maxwell, and closure scope",
            "passed": {"MGC3324_0_conditional_local_GR", "MGC3324_1_Newton_limit", "MGC3324_2_Maxwell_limit", "MGC3324_3_closure_scope"}.issubset(
                {row["theorem_id"] for row in closure}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3324_5_poisson_derivation",
            "check": "Poisson derivation includes metric ansatz, local equation, Poisson result, and MTS residual",
            "passed": {"POI3324_0_metric", "POI3324_1_equation", "POI3324_2_poisson", "POI3324_3_mts_residual"}.issubset(
                {row["step_id"] for row in poisson}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3324_6_EM_route",
            "check": "EM route includes universal Maxwell action and direct vertex exclusion",
            "passed": any("S_EM" in row["route"] for row in em_rows)
            and any("exclude" in row["route"] for row in em_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3324_7_assumption_ledger",
            "check": "assumption ledger includes metric readout, kappa closure, universal matter, residual suppression, and no-tadpole",
            "passed": {"ASS3324_0_metric_readout", "ASS3324_1_kappa_closure", "ASS3324_2_universal_matter", "ASS3324_3_local_residual_suppression", "ASS3324_4_no_tadpole"}.issubset(
                {row["assumption_id"] for row in assumptions}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3324_8_no_unconditional_claim",
            "check": "induced numeric, parent assumptions, and unconditional local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3324_1_induced_CEH_numeric", "GATE3324_3_parent_assumptions_signed", "GATE3324_4_unconditional_local_GR"}
            )
            and any(row["gate_id"] == "GATE3324_2_measured_G_theorem" and row["passed"] == "true" for row in gates),
            "detail": "",
        },
        {
            "check_id": "VAL3324_9_next_signature_gate",
            "check": "next target is universal matter/no direct psi vertex/no-tadpole signature gate",
            "passed": any("universal metric matter coupling" in row["objective"] and "no direct psi-EM" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3324_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3324_11_overall",
            "check": "3324 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3324 - Induced EH coefficient or measured-G closure local-GR theorem under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3324 tries the stronger route first: derive the Einstein-Hilbert coefficient from the parent psi sector.",
        "",
        "The structural induced-gravity form is",
        "",
        "`Gamma_eff[g_pub] = Gamma_0 + C_EH^ind int sqrt(-g_pub) R[g_pub] + ...`,",
        "",
        "with",
        "",
        "`G_eff = c^4/(16 pi C_EH^ind)` and `kappa_eff = 1/(2 C_EH^ind)`.",
        "",
        "But the current corpus does not supply the spectral measure, cutoff/readout normalization, sign, or counterterm rule needed to compute `C_EH^ind`. Also, the existing macroscopic action and microscopic constants already contain `G`, so using those to derive `G` would be circular.",
        "",
        "Therefore 3324 adopts the honest near-term theorem: MTS may reduce to local GR/Newton/Maxwell with measured `G_N`, exactly as GR itself does, provided source universality, no direct `psi`-matter/EM vertices, no-tadpole composite silence, and residual suppression are parent-signed.",
        "",
        "In the weak-field branch this gives",
        "",
        "`nabla^2 Phi = 4 pi G_N rho + bounded MTS residual`.",
        "",
        "This is not a retreat. It separates the achievable local-GR closure from the deeper future problem of deriving `G` from an induced `C_EH` calculation.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Induced EH Attempt", induced_eh_attempt_rows(), "row_id"),
        ("Measured-G Closure Theorem", measured_g_closure_rows(), "theorem_id"),
        ("Poisson Limit Derivation", poisson_derivation_rows(), "step_id"),
        ("Maxwell/EM Stress Clean Route", maxwell_em_rows(), "row_id"),
        ("Closure Assumption Ledger", closure_assumption_rows(), "assumption_id"),
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
            "- It explicitly rejects a circular derivation of `G` from equations that already contain `G`.",
            "- It formalizes a conditional measured-`G` local-GR/Newton/Maxwell theorem.",
            "- The theorem is not yet unconditional because universal matter descent, no direct `psi`-EM vertex, no-tadpole, and numeric residual bounds are not parent-signed.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["induced"], induced_eh_attempt_rows())
    write_csv(OUTPUTS["closure"], measured_g_closure_rows())
    write_csv(OUTPUTS["poisson"], poisson_derivation_rows())
    write_csv(OUTPUTS["em"], maxwell_em_rows())
    write_csv(OUTPUTS["assumptions"], closure_assumption_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
