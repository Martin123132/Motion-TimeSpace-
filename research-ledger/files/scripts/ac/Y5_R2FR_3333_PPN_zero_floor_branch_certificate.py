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

DOC = ROOT / "3333-Y5-R2FR-PPN-zero-floor-branch-certificate-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3333_0_3332_doc",
        "path": ROOT / "3332-Y5-R2FR-PPN-epsilon-eff-and-floor-specialization-under-AX1090.md",
        "role": "3332 zero-floor handoff",
    },
    {
        "source_id": "SRC3333_1_3332_direct_g",
        "path": OUT / "P8_Y5_R2FR_3332_DIRECT_AND_G_CLOSURE_FLOORS.csv",
        "role": "direct and measured-G floor formulas",
    },
    {
        "source_id": "SRC3333_2_3332_gamma",
        "path": OUT / "P8_Y5_R2FR_3332_GAMMA_FLOOR_BRANCHES.csv",
        "role": "Gamma floor branch formulas",
    },
    {
        "source_id": "SRC3333_3_3332_budget",
        "path": OUT / "P8_Y5_R2FR_3332_NORMALIZED_PPN_BUDGET.csv",
        "role": "normalized PPN residual budget",
    },
    {
        "source_id": "SRC3333_4_3324_measured_G",
        "path": OUT / "P8_Y5_R2FR_3324_MEASURED_G_CLOSURE_THEOREM.csv",
        "role": "measured-G local GR/Newton/Maxwell theorem",
    },
    {
        "source_id": "SRC3333_5_3324_poisson",
        "path": OUT / "P8_Y5_R2FR_3324_POISSON_LIMIT_DERIVATION.csv",
        "role": "Poisson/Newton limit support",
    },
    {
        "source_id": "SRC3333_6_3324_em",
        "path": OUT / "P8_Y5_R2FR_3324_MAXWELL_EM_STRESS_CLEAN_ROUTE.csv",
        "role": "Maxwell stress/Poynting metric route",
    },
    {
        "source_id": "SRC3333_7_3325_matter_signature",
        "path": OUT / "P8_Y5_R2FR_3325_MATTER_SIGNATURE_CONTRACT.csv",
        "role": "metric matter and forbidden direct-vertex signature",
    },
    {
        "source_id": "SRC3333_8_3325_direct_audit",
        "path": OUT / "P8_Y5_R2FR_3325_DIRECT_VERTEX_AUDIT.csv",
        "role": "direct vertex audit and branch guard",
    },
    {
        "source_id": "SRC3333_9_3318_gamma_no_pole",
        "path": OUT / "P8_Y5_R2FR_3318_NONPROPAGATION_THEOREM_ATTEMPT.csv",
        "role": "Gamma readout/background no-pole theorem attempt",
    },
    {
        "source_id": "SRC3333_10_3318_gamma_branch",
        "path": OUT / "P8_Y5_R2FR_3318_GAMMA_BRANCH_AUDIT.csv",
        "role": "Gamma branch classification",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3333_SOURCE_REGISTER.csv",
    "certificate": OUT / "P8_Y5_R2FR_3333_ZERO_FLOOR_CERTIFICATE.csv",
    "direct": OUT / "P8_Y5_R2FR_3333_DIRECT_VERTEX_CERTIFICATE.csv",
    "measured_g": OUT / "P8_Y5_R2FR_3333_MEASURED_G_CERTIFICATE.csv",
    "gamma": OUT / "P8_Y5_R2FR_3333_GAMMA_BRANCH_CERTIFICATE.csv",
    "fallback": OUT / "P8_Y5_R2FR_3333_RESIDUAL_FALLBACKS.csv",
    "reduced_budget": OUT / "P8_Y5_R2FR_3333_REDUCED_PPN_BUDGET.csv",
    "gates": OUT / "P8_Y5_R2FR_3333_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3333_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3333_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3333_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
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


def direct_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "DIR3333_0_metric_matter_only",
            "certificate_clause": "S_matter and S_EM enter the local branch only through g_pub",
            "evidence": "3325 metric matter signature and 3324 Maxwell stress route",
            "derivation": "If matter has no independent psi charge and EM is S_EM[g_pub,A], then variation gives metric T_munu sources only; Poynting flux is in T_munu^EM rather than a separate background-force vertex.",
            "branch_effect": "supports epsilon_direct_PPN=0 for the clean local-GR branch",
            "certificate_status": "BRANCH_SIGNED_NOT_PARENT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "DIR3333_1_forbidden_vertices",
            "certificate_clause": "Delta S_direct[psi,Psi_m,A]=0 for f(psi)L_matter, f(psi)F^2, psi J^mu A_mu, and nonmetric Poynting-background terms",
            "evidence": "3325 forbidden direct vertex signature",
            "derivation": "These terms would create nonmetric fifth-force, optical, or clock channels. Excluding them is not optional in the clean local-GR theorem; it is the definition of that branch.",
            "branch_effect": "epsilon_direct_PPN=0 only inside the branch; nonzero Delta S_direct exits the branch",
            "certificate_status": "BRANCH_SIGNATURE_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "DIR3333_2_audit_scope",
            "certificate_clause": "absence in current core files is not a microscopic no-go theorem",
            "evidence": "3325 direct vertex audit",
            "derivation": "The corpus supports a macroscopic metric-matter closure, but a future microscopic parent matter action could reintroduce representative-dependent direct couplings unless it proves descent.",
            "branch_effect": "parent-level epsilon_direct_PPN=0 remains unproved",
            "certificate_status": "PARENT_DESCENT_OPEN",
            "valid_for_claim": "false",
        },
    ]


def measured_g_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "GCL3333_0_measured_kappa",
            "certificate_clause": "kappa_eff is calibrated as 8 pi G_N/c^4 in the local closure branch",
            "evidence": "3324 measured-G closure theorem",
            "derivation": "The Einstein/Newton leading slot is not scored as an MTS residual when the branch explicitly adopts measured G_N; only departures after that calibration enter R_PPN.",
            "branch_effect": "epsilon_G_closure_PPN=0 for measured-G closure",
            "certificate_status": "BRANCH_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "GCL3333_1_Newton_slot",
            "certificate_clause": "GM/source mass calibration is completed before residual scoring",
            "evidence": "3324 Poisson/Newton limit plus 3331 q_U normalization",
            "derivation": "PPN first-order time-potential normalization defines the source mass. Residual metric pieces are compared only after pure GM redefinition has been absorbed.",
            "branch_effect": "prevents a Newtonian source-normalization mismatch being double-counted as MTS physics",
            "certificate_status": "CALIBRATION_GUARD_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "GCL3333_2_no_derived_G_claim",
            "certificate_clause": "the branch does not claim to derive Newton's constant",
            "evidence": "3324 closure scope",
            "derivation": "If the theory instead claims induced C_EH or derived kappa_ind, the residual floor reopens as |kappa_ind/kappa_N-1| plus source-normalization mismatch.",
            "branch_effect": "derived-G branch remains blocked, but measured-G local-GR branch is internally clean",
            "certificate_status": "CLAIM_SCOPE_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def gamma_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "GAM3333_0_no_independent_x",
            "certificate_clause": "Gamma_G is treated as readout/background, not as an independent local fluctuating field x",
            "evidence": "3318 absence lemma",
            "derivation": "The local propagator is built from varied fields in S_2. If delta Gamma_G is absent, the Hessian has no x row, no h-x derivative mixing, and no finite Gamma exchange pole.",
            "branch_effect": "R_Gamma_PPN^pole=0",
            "certificate_status": "CONDITIONAL_NO_POLE_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "GAM3333_1_background_subtraction",
            "certificate_clause": "local Gamma_0 is zero/constant after measured-G/cosmological-background subtraction",
            "evidence": "3318 local GR effect and 3332 Gamma branch",
            "derivation": "A constant scalar background can contribute only as a cosmological-constant-like curvature floor, not a finite exchange pole. It must still be bounded as A_Gamma |Gamma_local| L_PPN^2 unless proved negligible.",
            "branch_effect": "finite pole closed; constant-curvature floor remains explicit",
            "certificate_status": "PARTIAL_GAMMA_CERTIFICATE",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "GAM3333_2_proxy_not_promoted",
            "certificate_clause": "K_solar^m proxy is not promoted to a PPN pass without a parent map",
            "evidence": "3321 solar proxy and 3330/3332 Gamma proxy rows",
            "derivation": "K_solar^m <= 1e-122 is an encouraging internal scale only if the local Gamma residual is parent-linked to curvature-saturation response; it cannot bound psi/composite tails.",
            "branch_effect": "Gamma proxy stays nonclaim until mapped or replaced by constant-curvature bound",
            "certificate_status": "PROXY_GUARD_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "GAM3333_3_independent_x_countermodel",
            "certificate_clause": "independent algebraic Gamma x is rejected as a shortcut local-GR proof",
            "evidence": "3318 independent-x countercheck",
            "derivation": "Without stationarity, an x^2 potential, or a constraint equation, sqrt(-g)x generates tadpole/constraint behavior rather than a clean no-pole theorem.",
            "branch_effect": "prevents smuggling Gamma silence by an unsourced algebraic field",
            "certificate_status": "COUNTERMODEL_GUARD_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def zero_floor_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "certificate_id": "ZFC3333_0_direct",
            "floor": "epsilon_direct_PPN",
            "result": "epsilon_direct_PPN=0 is branch-certified for the clean metric-matter/metric-Maxwell local-GR closure",
            "status": "ZERO_AT_BRANCH_LEVEL",
            "not_proved": "microscopic parent matter descent with no representative dependence",
            "fallback_if_unsigned": "epsilon_direct_PPN >= ||delta S_direct/delta g_PPN|| and the branch must face PPN/WEP/clock/optics constraints",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "ZFC3333_1_measured_G",
            "floor": "epsilon_G_closure_PPN",
            "result": "epsilon_G_closure_PPN=0 is branch-certified for measured-G closure with calibrated kappa_eff and GM absorption",
            "status": "ZERO_AT_BRANCH_LEVEL",
            "not_proved": "derivation of G_N or induced C_EH from psi spectrum",
            "fallback_if_unsigned": "epsilon_G_closure_PPN >= |kappa_ind/kappa_N-1| plus source-normalization mismatch",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "ZFC3333_2_Gamma_pole",
            "floor": "R_Gamma_PPN^pole",
            "result": "finite Gamma exchange pole is zero if Gamma_G is readout/background and not an independent local field",
            "status": "CONDITIONAL_ZERO_POLE",
            "not_proved": "full microscopic psi reduction and universal mapping of Gamma residual to K_solar^m",
            "fallback_if_unsigned": "R_Gamma_PPN <= A_Gamma |Gamma_local| L_PPN^2 or a finite-pole residual bound",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "ZFC3333_3_full_Gamma",
            "floor": "R_Gamma_PPN total",
            "result": "not fully zero yet because constant-curvature/proxy mapping remains explicit",
            "status": "PARTIAL_ONLY",
            "not_proved": "Gamma_local=0 or source-owned constant-curvature/proxy bound",
            "fallback_if_unsigned": "retain R_Gamma_PPN in the reduced PPN budget",
            "valid_for_claim": "false",
        },
    ]


def residual_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "fallback_id": "FB3333_0_direct_nonzero",
            "trigger": "any forbidden direct psi-matter/psi-EM/Poynting-background vertex is present",
            "residual_formula": "epsilon_direct_PPN >= ||delta S_direct/delta g_PPN|| or observable fifth-force/clock/optics response norm",
            "consequence": "clean local-GR branch fails; direct vertex must be bounded in PPN, WEP, clock, and optics arenas",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "FB3333_1_derived_G_claim",
            "trigger": "the theory claims to derive G_N rather than use measured-G closure",
            "residual_formula": "epsilon_G_closure_PPN >= |kappa_ind/kappa_N-1| + source_normalization_mismatch",
            "consequence": "local-GR reduction must wait for induced EH coefficient and source calibration",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "FB3333_2_Gamma_constant",
            "trigger": "Gamma is readout/background but local constant curvature is not proved negligible",
            "residual_formula": "R_Gamma_PPN <= A_Gamma_PPN |Gamma_local| L_PPN^2",
            "consequence": "no finite Gamma pole, but constant-curvature floor must be sourced or bounded",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "FB3333_3_Gamma_independent",
            "trigger": "Gamma is promoted to an independent local field",
            "residual_formula": "retain finite-pole/tadpole/constraint residual until stationarity, x^2 potential, and Hessian row are supplied",
            "consequence": "Gamma no-pole certificate is void",
            "valid_for_claim": "false",
        },
    ]


def reduced_budget_rows() -> list[dict[str, Any]]:
    return [
        {
            "budget_id": "RB3333_0_clean_branch",
            "formula": "R_PPN <= |R_Gamma_const_or_proxy| + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN",
            "conditions": "epsilon_direct_PPN=0 by metric matter/Maxwell branch; epsilon_G_closure_PPN=0 by measured-G closure; Gamma finite pole absent by readout/background branch",
            "meaning": "3333 reduces the clean local PPN problem to Gamma constant/proxy, tree leakage, and composite tail",
            "status": "REDUCED_CLEAN_BRANCH_BUDGET",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "RB3333_1_if_Gamma_bound_signed",
            "formula": "R_PPN <= A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN + A_Gamma |Gamma_local| L_PPN^2",
            "conditions": "Gamma finite pole absent but constant curvature remains bounded rather than zero",
            "meaning": "this is the realistic next budget if Gamma_local can be sourced or shown negligible",
            "status": "GAMMA_CONSTANT_BRANCH",
            "valid_for_claim": "false",
        },
        {
            "budget_id": "RB3333_2_if_Gamma_proxy_signed",
            "formula": "R_PPN <= A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN + A_K K_solar^m",
            "conditions": "parent map signs local Gamma residual to curvature-saturation proxy",
            "meaning": "the proxy would make Gamma likely harmless, leaving tree and composite as dominant floors",
            "status": "GAMMA_PROXY_BRANCH_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3333_0_direct_branch_zero",
            "claim": "epsilon_direct_PPN=0 is certified for the clean local branch",
            "passed": "true",
            "reason": "metric matter/Maxwell signature excludes direct psi-matter/psi-EM/Poynting-background vertices in this branch",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3333_1_measured_G_branch_zero",
            "claim": "epsilon_G_closure_PPN=0 is certified for measured-G closure",
            "passed": "true",
            "reason": "kappa_eff and GM are calibrated before residual scoring, with no derived-G claim",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3333_2_Gamma_pole_zero",
            "claim": "finite Gamma exchange pole is absent in the readout/background branch",
            "passed": "true",
            "reason": "delta Gamma_G is not an independent local Hessian row in the conditional 3318 theorem",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3333_3_Gamma_total_zero",
            "claim": "total R_Gamma_PPN is zero",
            "passed": "false",
            "reason": "constant-curvature/proxy mapping remains explicit and unsourced",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3333_4_parent_matter_descent",
            "claim": "microscopic parent matter descent proves no direct vertices",
            "passed": "false",
            "reason": "current corpus supports branch signature but not parent-level matter descent",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3333_5_local_GR_claim",
            "claim": "local GR/PPN pass is claim-ready",
            "passed": "false",
            "reason": "tree leakage, composite, Gamma constant/proxy, A_PPN, C_metric, and real B_PPN still need source-grade bounds",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3333_0",
            "question": "Did 3333 close any floors?",
            "answer": "yes, at branch level",
            "reason": "epsilon_direct_PPN and epsilon_G_closure_PPN can be set to zero inside the clean measured-G metric-matter branch without claiming microscopic descent or derived G",
            "next_action": "work the remaining reduced budget: Gamma constant/proxy, tree leakage, and composite tail",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3333_1",
            "question": "Is Gamma fully closed?",
            "answer": "not fully",
            "reason": "finite Gamma pole is conditionally absent, but constant-curvature/proxy mapping is still a residual floor",
            "next_action": "derive or bound Gamma_local in the PPN patch, or parent-map it to K_solar^m",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3333_2",
            "question": "What remains the serious local-GR risk?",
            "answer": "composite tail and tree leakage after q_U normalization",
            "reason": "once direct/G closure are branch-zero and Gamma pole is absent, the remaining hard problem is suppressing psi public residues in PPN units",
            "next_action": "attack Gamma constant/proxy first because it is cheaper; then composite/tree numeric envelopes",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3334-Y5-R2FR-Gamma-constant-curvature-or-Ksolar-proxy-map-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3334_Gamma_constant_curvature_or_Ksolar_proxy_map.py",
            "objective": "try to remove the remaining Gamma floor by either bounding Gamma_local L_PPN^2 or parent-mapping the local Gamma residual to the K_solar^m saturation proxy",
            "must_include": "distinguish finite pole zero from constant curvature; derive R_Gamma <= A_Gamma |Gamma_local| L_PPN^2; attempt K_solar^m map; keep proxy nonclaim unless parent-signed; update reduced PPN budget",
            "fallback_if_failed": "retain explicit Gamma floor and move to composite/tree PPN envelope acquisition",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    certificate = zero_floor_certificate_rows()
    direct = direct_certificate_rows()
    measured_g = measured_g_certificate_rows()
    gamma = gamma_certificate_rows()
    fallback = residual_fallback_rows()
    reduced = reduced_budget_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3333_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3333_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3333_2_outputs_parse",
            "check": "all 3333 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3333_3_direct_zero",
            "check": "direct certificate signs branch-level zero and keeps parent descent open",
            "passed": any("epsilon_direct_PPN=0" in row["branch_effect"] for row in direct)
            and any(row["certificate_status"] == "PARENT_DESCENT_OPEN" for row in direct)
            and any(row["floor"] == "epsilon_direct_PPN" and row["status"] == "ZERO_AT_BRANCH_LEVEL" for row in certificate),
            "detail": "",
        },
        {
            "check_id": "VAL3333_4_measured_G_zero",
            "check": "measured-G certificate signs branch-level zero and blocks derived-G claim",
            "passed": any("epsilon_G_closure_PPN=0" in row["branch_effect"] for row in measured_g)
            and any("does not claim" in row["certificate_clause"] for row in measured_g)
            and any(row["floor"] == "epsilon_G_closure_PPN" and row["status"] == "ZERO_AT_BRANCH_LEVEL" for row in certificate),
            "detail": "",
        },
        {
            "check_id": "VAL3333_5_gamma_partial",
            "check": "Gamma certificate closes finite pole but not total Gamma floor",
            "passed": any("R_Gamma_PPN^pole=0" in row["branch_effect"] for row in gamma)
            and any(row["floor"] == "R_Gamma_PPN total" and row["status"] == "PARTIAL_ONLY" for row in certificate),
            "detail": "",
        },
        {
            "check_id": "VAL3333_6_fallbacks",
            "check": "fallback rows exist for direct, derived-G, Gamma constant, and Gamma independent cases",
            "passed": {"FB3333_0_direct_nonzero", "FB3333_1_derived_G_claim", "FB3333_2_Gamma_constant", "FB3333_3_Gamma_independent"}.issubset(
                {row["fallback_id"] for row in fallback}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3333_7_reduced_budget",
            "check": "reduced clean branch budget keeps Gamma/tree/composite only",
            "passed": any("R_Gamma_const_or_proxy" in row["formula"] and "epsilon_composite_PPN" in row["formula"] and "epsilon_direct" not in row["formula"] for row in reduced),
            "detail": "",
        },
        {
            "check_id": "VAL3333_8_gate_pattern",
            "check": "branch zero gates pass while parent/full/local claim gates remain false",
            "passed": all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3333_0_direct_branch_zero", "GATE3333_1_measured_G_branch_zero", "GATE3333_2_Gamma_pole_zero"}
            )
            and all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3333_3_Gamma_total_zero", "GATE3333_4_parent_matter_descent", "GATE3333_5_local_GR_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3333_9_next_3334",
            "check": "next target attacks remaining Gamma floor",
            "passed": any("Gamma_local" in row["objective"] and "K_solar" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3333_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3333_11_overall",
            "check": "3333 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3333 - PPN zero-floor branch certificate under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3333 closes two cheap floors at branch level and partially closes Gamma.",
        "",
        "Inside the clean measured-G metric-matter local-GR branch:",
        "",
        "`epsilon_direct_PPN = 0`",
        "",
        "because matter and Maxwell/EM stress are coupled only through `g_pub`, with forbidden direct vertices explicitly excluded.",
        "",
        "`epsilon_G_closure_PPN = 0`",
        "",
        "because this branch calibrates `kappa_eff=8 pi G_N/c^4` and absorbs `GM` before residual scoring. This is not a derivation of Newton's constant.",
        "",
        "For Gamma, the finite exchange pole is conditionally absent:",
        "",
        "`R_Gamma_PPN^pole = 0`",
        "",
        "if `Gamma_G` is readout/background and `delta Gamma_G` is not an independent local Hessian row.",
        "",
        "But total `R_Gamma_PPN` is not fully zero yet. A constant-curvature floor or the `K_solar^m` proxy map still has to be signed.",
        "",
        "So the reduced clean-branch PPN budget is",
        "",
        "`R_PPN <= |R_Gamma_const_or_proxy| + A_PPN C_metric epsilon_eff_PPN^2 + epsilon_composite_PPN`.",
        "",
        "This is a genuine narrowing: direct-vertex fog and measured-G closure fog are no longer carried as open local PPN floors, as long as the branch is stated honestly.",
        "",
        "No PPN/local-GR pass is claimed.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Zero Floor Certificate", zero_floor_certificate_rows(), "certificate_id"),
        ("Direct Vertex Certificate", direct_certificate_rows(), "clause_id"),
        ("Measured G Certificate", measured_g_certificate_rows(), "clause_id"),
        ("Gamma Branch Certificate", gamma_certificate_rows(), "clause_id"),
        ("Residual Fallbacks", residual_fallback_rows(), "fallback_id"),
        ("Reduced PPN Budget", reduced_budget_rows(), "budget_id"),
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
            "- It distinguishes branch-level closure from parent-level derivation.",
            "- It allows the local-GR branch to use measured `G_N` honestly without claiming to derive it.",
            "- It keeps Maxwell/Poynting in metric `T_munu^EM` and quarantines direct background-force vertices.",
            "- It does not close composite or tree leakage.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["certificate"], zero_floor_certificate_rows())
    write_csv(OUTPUTS["direct"], direct_certificate_rows())
    write_csv(OUTPUTS["measured_g"], measured_g_certificate_rows())
    write_csv(OUTPUTS["gamma"], gamma_certificate_rows())
    write_csv(OUTPUTS["fallback"], residual_fallback_rows())
    write_csv(OUTPUTS["reduced_budget"], reduced_budget_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
