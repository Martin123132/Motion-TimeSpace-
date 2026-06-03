from __future__ import annotations

import argparse
import csv
import importlib
import importlib.metadata
import importlib.util
import json
import math
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
WORKBENCH = PROJECT_ROOT / "formalization-workbench"
RUN_SLUG = "official-CMB-likelihood-preflight"
STATUS = "official_CMB_preflight_CAMB_engine_smoke_passed_official_likelihood_assets_missing_no_CMB_claim"
STATUS_NO_ENGINE = "official_CMB_preflight_no_engine_no_likelihood_no_CMB_claim"
CLAIM_CEILING = "official_CMB_preflight_only_no_likelihood_score_no_MTS_CMB_claim"
B_MEM_FIXED = 2.0 / 27.0


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return ""


def module_origin(name: str) -> str:
    spec = importlib.util.find_spec(name)
    if spec is None:
        return ""
    return str(spec.origin or "")


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "263-post-scale-lock-CMB-bridge-readiness-gate.md", "post-scale-lock CMB readiness gate"),
        (ROOT / "182-CMB-engine-install-or-external-run-plan.md", "previous CAMB engine install/readiness checkpoint"),
        (ROOT / "181-CMB-engine-readiness-and-dryrun-wrapper.md", "CMB dry-run wrapper checkpoint"),
        (ROOT / "scripts" / "cmb_kill_screen_long_run.py", "locked CMB dry-run wrapper"),
        (ROOT / "scripts" / "official_CMB_likelihood_preflight.py", "this official preflight runner"),
        (WORKBENCH / "data" / "cosmology", "local cosmology data root"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
            "is_dir": "yes" if path.exists() and path.is_dir() else "no",
        }
        for path, role in sources
    ]


def engine_inventory_rows() -> list[dict[str, Any]]:
    class_exe = shutil.which("class")
    rows = [
        {
            "engine_or_tool": "camb_python_module",
            "available": "yes" if module_available("camb") else "no",
            "version": package_version("camb"),
            "origin_or_path": module_origin("camb"),
            "role": "Boltzmann spectra engine",
        },
        {
            "engine_or_tool": "classy_python_module",
            "available": "yes" if module_available("classy") else "no",
            "version": package_version("classy"),
            "origin_or_path": module_origin("classy"),
            "role": "CLASS Python Boltzmann engine",
        },
        {
            "engine_or_tool": "class_executable",
            "available": "yes" if class_exe else "no",
            "version": "",
            "origin_or_path": class_exe or "",
            "role": "standalone CLASS executable",
        },
        {
            "engine_or_tool": "cobaya_python_module",
            "available": "yes" if module_available("cobaya") else "no",
            "version": package_version("cobaya"),
            "origin_or_path": module_origin("cobaya"),
            "role": "official likelihood/evaluation plumbing",
        },
        {
            "engine_or_tool": "clik_python_module",
            "available": "yes" if module_available("clik") else "no",
            "version": package_version("clik"),
            "origin_or_path": module_origin("clik"),
            "role": "Planck likelihood interface candidate",
        },
        {
            "engine_or_tool": "candl_python_module",
            "available": "yes" if module_available("candl") else "no",
            "version": package_version("candl"),
            "origin_or_path": module_origin("candl"),
            "role": "ACT/SPT likelihood interface candidate",
        },
        {
            "engine_or_tool": "montepython_python_module",
            "available": "yes" if module_available("montepython") else "no",
            "version": package_version("montepython"),
            "origin_or_path": module_origin("montepython"),
            "role": "CLASS likelihood runner candidate",
        },
    ]
    return rows


def official_asset_roots() -> list[Path]:
    return [
        WORKBENCH / "data" / "cosmology" / "cmb",
        WORKBENCH / "data" / "cosmology" / "planck",
        WORKBENCH / "data" / "cmb",
        WORKBENCH / "data" / "planck",
        PROJECT_ROOT / "data" / "cmb",
        PROJECT_ROOT / "data" / "planck",
        ROOT / "data" / "cmb",
        ROOT / "likelihoods",
        PROJECT_ROOT / "likelihoods",
    ]


def likelihood_asset_inventory_rows(max_matches: int = 80) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    patterns = [
        "plik",
        "commander",
        "simall",
        "low_l",
        "lowell",
        "clik",
        "planck",
        "act_dr",
        "spt",
        "candl",
        "lensing",
    ]
    for root in official_asset_roots():
        rows.append(
            {
                "asset_kind": "candidate_root",
                "path": str(root),
                "exists": "yes" if root.exists() else "no",
                "match_reason": "configured official-likelihood search root",
                "bytes": root.stat().st_size if root.exists() and root.is_file() else "",
            }
        )
        if not root.exists() or not root.is_dir():
            continue
        match_count = 0
        for path in root.rglob("*"):
            if match_count >= max_matches:
                break
            lowered = path.name.lower()
            if any(pattern in lowered for pattern in patterns):
                rows.append(
                    {
                        "asset_kind": "candidate_asset",
                        "path": str(path),
                        "exists": "yes",
                        "match_reason": "name_pattern",
                        "bytes": path.stat().st_size if path.is_file() else "",
                    }
                )
                match_count += 1
    return rows


def has_likelihood_assets(rows: list[dict[str, Any]]) -> bool:
    return any(row["asset_kind"] == "candidate_asset" and row["exists"] == "yes" for row in rows)


def run_camb_engine_smoke(lmax: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    if not module_available("camb"):
        return (
            [
                {
                    "check": "CAMB_engine_smoke",
                    "status": "not_run",
                    "evidence": "camb module unavailable",
                }
            ],
            [],
            {"smoke_run": False, "smoke_status": "not_run_no_camb"},
        )
    start = time.time()
    try:
        camb = importlib.import_module("camb")
        params = camb.CAMBparams()
        params.set_cosmology(H0=67.5, ombh2=0.02237, omch2=0.12, tau=0.0544)
        params.InitPower.set_params(As=2.1e-9, ns=0.965)
        params.set_for_lmax(lmax, lens_potential_accuracy=0)
        results = camb.get_results(params)
        powers = results.get_cmb_power_spectra(params, CMB_unit="muK")
        total = powers["total"]
        elapsed = time.time() - start
        finite = all(math.isfinite(float(total[ell, col])) for ell in range(2, min(lmax, total.shape[0] - 1) + 1) for col in range(min(4, total.shape[1])))
        summary_rows = [
            {
                "check": "CAMB_engine_smoke",
                "status": "pass" if finite else "fail",
                "evidence": f"version={getattr(camb, '__version__', '')}; lmax={lmax}; shape={total.shape}; elapsed_s={elapsed:.3f}",
            },
            {
                "check": "LCDM_parameters_declared",
                "status": "pass",
                "evidence": "H0=67.5, ombh2=0.02237, omch2=0.12, tau=0.0544, As=2.1e-9, ns=0.965",
            },
            {
                "check": "official_baseline_reproduction",
                "status": "not_attempted",
                "evidence": "engine smoke has no official Planck/ACT/SPT reference likelihood or covariance",
            },
        ]
        sample_rows: list[dict[str, Any]] = []
        for ell in range(2, min(12, total.shape[0] - 1) + 1):
            sample_rows.append(
                {
                    "ell": ell,
                    "TT": float(total[ell, 0]),
                    "EE": float(total[ell, 1]),
                    "BB": float(total[ell, 2]),
                    "TE": float(total[ell, 3]),
                    "unit": "muK^2 Dl",
                    "role": "engine_smoke_sample_not_official_reference",
                }
            )
        payload = {
            "smoke_run": True,
            "smoke_status": "pass" if finite else "fail",
            "elapsed_s": elapsed,
            "lmax": lmax,
            "camb_version": getattr(camb, "__version__", ""),
        }
        return summary_rows, sample_rows, payload
    except Exception as exc:
        elapsed = time.time() - start
        return (
            [
                {
                    "check": "CAMB_engine_smoke",
                    "status": "fail",
                    "evidence": f"{exc.__class__.__name__}: {exc}; elapsed_s={elapsed:.3f}",
                }
            ],
            [],
            {"smoke_run": True, "smoke_status": "fail", "error": f"{exc.__class__.__name__}: {exc}", "elapsed_s": elapsed},
        )


def baseline_reproduction_gate_rows(engine_smoke: list[dict[str, Any]], official_assets: bool) -> list[dict[str, Any]]:
    camb_smoke_pass = any(row["check"] == "CAMB_engine_smoke" and row["status"] == "pass" for row in engine_smoke)
    return [
        {
            "gate": "Boltzmann_engine_available",
            "status": "pass" if camb_smoke_pass or module_available("classy") or shutil.which("class") else "fail",
            "evidence": "CAMB smoke pass" if camb_smoke_pass else "no working spectra engine smoke",
        },
        {
            "gate": "official_likelihood_assets_available",
            "status": "pass" if official_assets else "fail",
            "evidence": "candidate official assets found" if official_assets else "no Planck/ACT/SPT likelihood assets found in configured roots",
        },
        {
            "gate": "LCDM_official_baseline_reproduction",
            "status": "not_attempted",
            "evidence": "requires official likelihood assets and reference target before MTS scoring",
        },
        {
            "gate": "MTS_CMB_score_allowed",
            "status": "blocked",
            "evidence": "official baseline reproduction not complete",
        },
    ]


def official_likelihood_readiness_rows(
    engine_rows: list[dict[str, Any]],
    asset_rows: list[dict[str, Any]],
    camb_smoke_payload: dict[str, Any],
    official_assets: bool,
) -> list[dict[str, Any]]:
    availability = {row["engine_or_tool"]: row["available"] for row in engine_rows}
    asset_roots_checked = sum(1 for row in asset_rows if row["asset_kind"] == "candidate_root")
    candidate_assets = sum(1 for row in asset_rows if row["asset_kind"] == "candidate_asset")
    camb_smoke_pass = camb_smoke_payload.get("smoke_status") == "pass"
    planck_interface_ready = availability.get("clik_python_module") == "yes" or availability.get("cobaya_python_module") == "yes"
    act_spt_interface_ready = availability.get("candl_python_module") == "yes" or availability.get("cobaya_python_module") == "yes"
    return [
        {
            "component": "CAMB_spectra_engine",
            "status": "ready" if camb_smoke_pass else "blocked",
            "evidence": f"tiny LCDM spectra smoke status={camb_smoke_payload.get('smoke_status', 'not_run')}; version={camb_smoke_payload.get('camb_version', '')}",
            "next_action": "use only for engine/matched-mock work until official likelihood baseline exists",
        },
        {
            "component": "CLASS_alternative_engine",
            "status": "available" if availability.get("classy_python_module") == "yes" or availability.get("class_executable") == "yes" else "missing",
            "evidence": f"classy={availability.get('classy_python_module')}; class_executable={availability.get('class_executable')}",
            "next_action": "optional; not required while CAMB smoke works",
        },
        {
            "component": "Planck_likelihood_interface",
            "status": "partial" if planck_interface_ready else "missing",
            "evidence": f"clik={availability.get('clik_python_module')}; cobaya={availability.get('cobaya_python_module')}",
            "next_action": "install/configure official interface before LCDM baseline reproduction",
        },
        {
            "component": "ACT_SPT_likelihood_interface",
            "status": "partial" if act_spt_interface_ready else "missing",
            "evidence": f"candl={availability.get('candl_python_module')}; cobaya={availability.get('cobaya_python_module')}",
            "next_action": "optional after Planck route; still needs official assets",
        },
        {
            "component": "official_likelihood_assets",
            "status": "found" if official_assets else "missing",
            "evidence": f"candidate_roots_checked={asset_roots_checked}; candidate_assets_found={candidate_assets}",
            "next_action": "add official Planck/ACT/SPT likelihood data or keep CMB work labelled proxy",
        },
        {
            "component": "LCDM_official_baseline_reproduction",
            "status": "blocked",
            "evidence": "not attempted in this checkpoint; requires official likelihood assets and reference target",
            "next_action": "run LCDM baseline before any MTS CMB branch readout",
        },
        {
            "component": "MTS_CMB_branch_readout",
            "status": "blocked",
            "evidence": "official baseline reproduction incomplete",
            "next_action": "do not score or promote MTS on CMB yet",
        },
    ]


def command_plan_rows() -> list[dict[str, Any]]:
    return [
        {
            "phase": "official_preflight",
            "command": "python scripts/official_CMB_likelihood_preflight.py --timestamp <timestamp>",
            "allowed_now": "yes",
            "outputs": "engine inventory, likelihood asset inventory, tiny CAMB smoke if available",
        },
        {
            "phase": "official_baseline_reproduction",
            "command": "deferred until official likelihood assets/reference target exist",
            "allowed_now": "no",
            "outputs": "LCDM baseline likelihood score before any MTS CMB readout",
        },
        {
            "phase": "matched_mock_refresh",
            "command": "allowed as proxy if official assets remain missing",
            "allowed_now": "yes_with_proxy_labels",
            "outputs": "matched mock likelihood refresh under post-scale-lock claim gates",
        },
    ]


def claim_gate_rows(camb_smoke_payload: dict[str, Any], official_assets: bool) -> list[dict[str, Any]]:
    return [
        {
            "gate": "CAMB_engine_smoke",
            "result": camb_smoke_payload.get("smoke_status", "not_run"),
            "evidence": f"lmax={camb_smoke_payload.get('lmax', '')}; version={camb_smoke_payload.get('camb_version', '')}",
            "claim_effect": "engine readiness only",
        },
        {
            "gate": "official_likelihood_assets",
            "result": "pass" if official_assets else "fail",
            "evidence": "candidate assets found" if official_assets else "missing configured official likelihood assets",
            "claim_effect": "official score blocked if fail",
        },
        {
            "gate": "official_CMB_score",
            "result": "not_run",
            "evidence": "no official likelihood invocation in this checkpoint",
            "claim_effect": "no CMB support claim",
        },
        {
            "gate": "MTS_branch_readout",
            "result": "blocked",
            "evidence": "LCDM official baseline reproduction not complete",
            "claim_effect": "do not inspect MTS CMB likelihood yet",
        },
        {
            "gate": "post_scale_lock_claim_policy",
            "result": "pass",
            "evidence": "B_mem/Hstar/half-memory bridge remain closure/theorem-target only",
            "claim_effect": "no parent promotion",
        },
    ]


def decision_rows(camb_smoke_payload: dict[str, Any], official_assets: bool) -> list[dict[str, Any]]:
    if camb_smoke_payload.get("smoke_status") == "pass" and not official_assets:
        decision = STATUS
        meaning = (
            "CAMB is usable for tiny spectra smoke, but official likelihood assets/plumbing are missing. "
            "The official CMB route is not score-ready; use matched mock refresh as proxy or add official likelihood assets first."
        )
    elif camb_smoke_payload.get("smoke_status") == "pass" and official_assets:
        decision = "official_CMB_preflight_engine_and_candidate_assets_ready_baseline_reproduction_next_no_CMB_claim"
        meaning = (
            "A spectra engine and candidate likelihood assets exist. The next step is LCDM official baseline reproduction before any MTS CMB branch is read."
        )
    else:
        decision = STATUS_NO_ENGINE
        meaning = "No working spectra engine smoke passed; official CMB likelihood route remains blocked."
    return [
        {
            "decision": decision,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "meaning": meaning,
            "next_target": "post_scale_lock_matched_mock_refresh_if_assets_missing_else_LCDM_official_baseline_reproduction",
        }
    ]


def build_outputs(timestamp: str, lmax: int) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    engine_rows = engine_inventory_rows()
    asset_rows = likelihood_asset_inventory_rows()
    official_assets = has_likelihood_assets(asset_rows)
    smoke_rows, spectra_sample_rows, smoke_payload = run_camb_engine_smoke(lmax)
    gate_rows = baseline_reproduction_gate_rows(smoke_rows, official_assets)
    readiness_rows = official_likelihood_readiness_rows(engine_rows, asset_rows, smoke_payload, official_assets)
    decision = decision_rows(smoke_payload, official_assets)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists", "is_dir"]),
        "engine_inventory.csv": (engine_rows, ["engine_or_tool", "available", "version", "origin_or_path", "role"]),
        "official_likelihood_asset_inventory.csv": (asset_rows, ["asset_kind", "path", "exists", "match_reason", "bytes"]),
        "official_likelihood_readiness.csv": (readiness_rows, ["component", "status", "evidence", "next_action"]),
        "LCDM_engine_smoke.csv": (smoke_rows, ["check", "status", "evidence"]),
        "LCDM_engine_smoke_summary.csv": (smoke_rows, ["check", "status", "evidence"]),
        "LCDM_spectra_sample.csv": (spectra_sample_rows, ["ell", "TT", "EE", "BB", "TE", "unit", "role"]),
        "LCDM_engine_smoke_spectra_sample.csv": (spectra_sample_rows, ["ell", "TT", "EE", "BB", "TE", "unit", "role"]),
        "baseline_reproduction_gate.csv": (gate_rows, ["gate", "status", "evidence"]),
        "baseline_reproduction_gates.csv": (gate_rows, ["gate", "status", "evidence"]),
        "next_command_plan.csv": (command_plan_rows(), ["phase", "command", "allowed_now", "outputs"]),
        "command_plan.csv": (command_plan_rows(), ["phase", "command", "allowed_now", "outputs"]),
        "claim_gate_results.csv": (claim_gate_rows(smoke_payload, official_assets), ["gate", "result", "evidence", "claim_effect"]),
        "decision.csv": (decision, ["decision", "claim_ceiling", "lead_branch", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status = decision[0]["decision"]
    payload = {
        "status": status,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "CAMB_engine_smoke_status": smoke_payload.get("smoke_status", "not_run"),
        "official_likelihood_assets_found": official_assets,
        "official_likelihood_run": False,
        "LCDM_official_baseline_reproduced": False,
        "MTS_CMB_score_allowed": False,
        "B_mem_fixed": B_MEM_FIXED,
        "next_target": "post_scale_lock_matched_mock_refresh_if_assets_missing_else_LCDM_official_baseline_reproduction",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(status + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Official CMB likelihood preflight: engine, assets, and baseline gates.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    parser.add_argument("--lmax", type=int, default=64)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp, args.lmax)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
