from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4933"
EXTRACTED_INPUT = SOURCE_DIR / "Flow_mendeley_input_extracted.wl"
MATHICS = POST / ".venv-score" / "Scripts" / "mathics.exe"
RUN_DIR = POST / "runs" / "4933-c3-flow"
MARKER = "MTS_4933_C3_FLOW_EXECUTION"

EXPECTED_EXTRACTED_HASH = "7a6ce0ad809f1c8932511d4652542599ea30499805d8b71a5b758443a0e797d1"
RHO_MODES = {
    "source": "1/(8*Pi)",
    "photon": "1/(4*Pi)",
}

SYMBOL_REPLACEMENTS = {
    "Subscript[WLGamma,((R)^(2))]": "gammaR2",
    "Subscript[WLGamma,((S)^(2))]": "gammaS2",
    "Subscript[WLGamma,((C)^(2))]": "gammaC2",
    "Subscript[WLGamma,WLCapitalDeltaR]": "gammaDeltaR",
    "Subscript[WLGamma,WLCapitalDeltaS]": "gammaDeltaS",
    "Subscript[WLGamma,SSTL]": "gammaSSTL",
    "Subscript[WLGamma,DDR]": "gammaDDR",
    "Subscript[WLGamma,RS]": "gammaRS",
    "Subscript[WLGamma,CS]": "gammaCS",
    "Subscript[WLGamma,g]": "gammaG",
    "Subscript[WLGamma,R]": "gammaR",
    "Subscript[WLGamma,S]": "gammaS",
    "Subscript[WLSigma,Euler]": "SigmaEuler",
    "Subscript[G,GS]": "GGS",
    "Subscript[G,N]": "GN",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def extracted_cells(text: str) -> dict[int, str]:
    pattern = re.compile(r"(?m)^\(\* INPUT_CELL_(\d+) \*\)\r?$")
    matches = list(pattern.finditer(text))
    cells: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        cells[int(match.group(1))] = text[match.end() : end].strip()
    return cells


def flatten_q_heads(text: str) -> str:
    marker = "Subscript[Q,"
    cursor = text.find(marker)
    while cursor >= 0:
        index_end = text.find("]", cursor + len(marker))
        if index_end < 0 or index_end + 1 >= len(text) or text[index_end + 1] != "[":
            raise ValueError(f"malformed Q head near offset {cursor}")
        argument_start = index_end + 2
        depth = 1
        position = argument_start
        while position < len(text) and depth:
            if text[position] == "[":
                depth += 1
            elif text[position] == "]":
                depth -= 1
            position += 1
        if depth:
            raise ValueError(f"unterminated Q argument near offset {cursor}")
        index_text = text[cursor + len(marker) : index_end]
        argument_text = flatten_q_heads(text[argument_start : position - 1])
        text = text[:cursor] + f"Q[{index_text},{argument_text}]" + text[position:]
        cursor = text.find(marker, cursor)
    return text


def normalize_mathics_symbols(text: str) -> str:
    for source, target in SYMBOL_REPLACEMENTS.items():
        text = text.replace(source, target)
    text = text.replace("Litim[1]", "Litim1")
    return flatten_q_heads(text)


def wolfram_program(flow_cell: str, litim_cell: str, rho: str, mode: str) -> str:
    unknowns = (
        "{GN'[t],GGS'[t],SigmaEuler'[t],gammaG,gammaR,gammaS,gammaR2,gammaC2,"
        "gammaSSTL,gammaRS,gammaCS,gammaDeltaR,gammaDeltaS}"
    )
    zero_rules = (
        "{gammaDDR->0,gammaS2->0,"
        "WLBeta->1,WLRho->((" + rho + ")&)}"
    )
    flow_cell = normalize_mathics_symbols(flow_cell)
    litim_cell = normalize_mathics_symbols(litim_cell)
    program = """(* __MARKER__; mode=__MODE__; rho=__RHO__ *)
$HistoryLength=0;
$IterationLimit=50000;
$RecursionLimit=10000;
__FLOW_CELL__
Print[\"__MARKER___FLOW_LOADED=\",Length[Flow]];
__LITIM_CELL__
Print[\"__MARKER___LITIM_READY=\",Length[FlowLitim]];
MTS4933Unknowns=__UNKNOWNS__;
MTS4933Equations=FlowLitim/.__ZERO_RULES__;
Print[\"__MARKER___LINEAR_SOLVE_START\"];
MTS4933SolveTiming=AbsoluteTiming[MTS4933FlowRules=Solve[MTS4933Equations==0,MTS4933Unknowns][[1]];];
Print[\"__MARKER___LINEAR_SOLVE_SECONDS=\",N[MTS4933SolveTiming[[1]],12]];
Print[\"__MARKER___RULE_COUNT=\",Length[MTS4933FlowRules]];
MTS4933Betas={MTS4933FlowRules[[1,2]],MTS4933FlowRules[[2,2]]};
Print[\"__MARKER___BETA_G=\",InputForm[MTS4933Betas[[1]]]];
Print[\"__MARKER___BETA_H=\",InputForm[MTS4933Betas[[2]]]];
Print[\"__MARKER___FIND_ROOT_START\"];
MTS4933RootTiming=AbsoluteTiming[MTS4933FixedPoint=FindRoot[Thread[MTS4933Betas==0],{{GN[t],0.35},{GGS[t],0}},WorkingPrecision->40,AccuracyGoal->24,PrecisionGoal->24,MaxIterations->300];];
Print[\"__MARKER___FIND_ROOT_SECONDS=\",N[MTS4933RootTiming[[1]],12]];
Print[\"__MARKER___FIXED_POINT=\",InputForm[MTS4933FixedPoint]];
MTS4933Residual=N[MTS4933Betas/.MTS4933FixedPoint,30];
Print[\"__MARKER___RESIDUAL=\",InputForm[MTS4933Residual]];
MTS4933Stability=N[D[MTS4933Betas,{{GN[t],GGS[t]}}]/.MTS4933FixedPoint,30];
MTS4933Exponents=-Eigenvalues[MTS4933Stability];
Print[\"__MARKER___STABILITY=\",InputForm[MTS4933Stability]];
Print[\"__MARKER___EXPONENTS=\",InputForm[MTS4933Exponents]];
MTS4933GammaRules=MTS4933FlowRules[[3;;]]/.MTS4933FixedPoint;
Print[\"__MARKER___GAMMA_RULES=\",InputForm[N[MTS4933GammaRules,24]]];
Print[\"__MARKER___PASS\"];
"""
    return (
        program.replace("__MARKER__", MARKER)
        .replace("__MODE__", mode)
        .replace("__RHO__", rho)
        .replace("__FLOW_CELL__", flow_cell)
        .replace("__LITIM_CELL__", litim_cell)
        .replace("__UNKNOWNS__", unknowns)
        .replace("__ZERO_RULES__", zero_rules)
    )


def run_mode(mode: str, timeout_seconds: int, prepare_only: bool) -> dict[str, object]:
    if digest(EXTRACTED_INPUT) != EXPECTED_EXTRACTED_HASH:
        raise RuntimeError("extracted C3 input hash changed; rerun and audit extraction first")
    cells = extracted_cells(EXTRACTED_INPUT.read_text(encoding="utf-8"))
    missing = sorted({3, 5} - set(cells))
    if missing:
        raise RuntimeError(f"missing extracted input cells: {missing}")

    RUN_DIR.mkdir(parents=True, exist_ok=True)
    program_path = RUN_DIR / f"c3_flow_{mode}.wl"
    log_path = RUN_DIR / f"c3_flow_{mode}.log"
    status_path = RUN_DIR / f"c3_flow_{mode}_status.json"
    program = wolfram_program(cells[3], cells[5], RHO_MODES[mode], mode)
    program_path.write_text(program, encoding="utf-8")

    status: dict[str, object] = {
        "marker": MARKER,
        "mode": mode,
        "rho": RHO_MODES[mode],
        "source": EXTRACTED_INPUT.relative_to(ROOT).as_posix(),
        "source_sha256": digest(EXTRACTED_INPUT),
        "program": program_path.relative_to(ROOT).as_posix(),
        "program_sha256": digest(program_path),
        "log": log_path.relative_to(ROOT).as_posix(),
        "prepared": True,
        "executed": False,
        "passed": False,
    }
    if prepare_only:
        status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
        return status

    if not MATHICS.exists():
        raise FileNotFoundError(MATHICS)
    start = time.monotonic()
    try:
        result = subprocess.run(
            [str(MATHICS), "--no-readline", "--quiet", "-f", str(program_path)],
            cwd=POST,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            timeout=timeout_seconds,
            check=False,
        )
        output = result.stdout + ("\n[STDERR]\n" + result.stderr if result.stderr else "")
        log_path.write_text(output, encoding="utf-8")
        status.update(
            {
                "executed": True,
                "returncode": result.returncode,
                "elapsed_seconds": time.monotonic() - start,
                "passed": result.returncode == 0 and f"{MARKER}_PASS" in output,
            }
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode("utf-8", "replace") if isinstance(error.stdout, bytes) else error.stdout or ""
        stderr = error.stderr.decode("utf-8", "replace") if isinstance(error.stderr, bytes) else error.stderr or ""
        log_path.write_text(stdout + ("\n[STDERR]\n" + stderr if stderr else ""), encoding="utf-8")
        status.update(
            {
                "executed": True,
                "timed_out": True,
                "elapsed_seconds": time.monotonic() - start,
                "passed": False,
            }
        )
    status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["source", "photon", "both"], default="source")
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()

    modes = tuple(RHO_MODES) if args.mode == "both" else (args.mode,)
    statuses = [run_mode(mode, args.timeout_seconds, args.prepare_only) for mode in modes]
    print(json.dumps(statuses, indent=2))
    return 0 if all(status["prepared"] and (args.prepare_only or status["passed"]) for status in statuses) else 1


if __name__ == "__main__":
    raise SystemExit(main())
