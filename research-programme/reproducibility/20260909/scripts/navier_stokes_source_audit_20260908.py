import argparse
import ctypes
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
from datetime import datetime, timezone
import urllib.request
import zipfile


ROOT = Path(__file__).resolve().parents[1]
COMMIT = "8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538"
ARCHIVE_URL = f"https://codeload.github.com/openai/NavierStokesAndEuler/zip/{COMMIT}"
PAPER_URL = "https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf"
DESTINATION = ROOT / "source-intake" / "navier-stokes" / "20260908"


def limit_process():
    if os.name == "nt":
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        kernel.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
        handle = kernel.GetCurrentProcess()
        if not kernel.SetPriorityClass(handle, 0x00004000):
            raise ctypes.WinError(ctypes.get_last_error())
        if not kernel.SetProcessAffinityMask(handle, 1):
            raise ctypes.WinError(ctypes.get_last_error())


def acquire(url, path):
    if path.exists():
        return path.read_bytes()
    request = urllib.request.Request(url, headers={"User-Agent": "MTS-private-static-audit"})
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()
    with path.open("xb") as output:
        output.write(payload)
    return payload


def code_only(source):
    result = []
    position = 0
    delimiter = re.compile(r'/-|--|"')
    nesting = re.compile(r'/-|-/')
    quoted = re.compile(r'"(?:\\.|[^"\\])*"', re.DOTALL)
    while matched := delimiter.search(source, position):
        result.append(source[position:matched.start()])
        if matched.group() == "/-":
            depth = 1
            ending = matched.end()
            while depth:
                nested = nesting.search(source, ending)
                if nested is None:
                    raise ValueError("Unclosed Lean block comment")
                depth += 1 if nested.group() == "/-" else -1
                ending = nested.end()
        elif matched.group() == "--":
            ending = source.find("\n", matched.end())
            ending = len(source) if ending < 0 else ending
        else:
            string_match = quoted.match(source, matched.start())
            if string_match is None:
                raise ValueError("Unclosed Lean string")
            ending = string_match.end()
        result.append(re.sub(r"[^\n]", " ", source[matched.start():ending]))
        position = ending
    result.append(source[position:])
    return "".join(result)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--acquire", action="store_true")
    arguments = parser.parse_args()
    limit_process()
    print("Static source audit only; no downloaded code execution or Lean build.", flush=True)
    fixture = 'import Mathlib\n/- outer /- sorry -/ axiom -/\ntheorem proof : True := by trivial -- sorry\n#check "axiom\\\" sorry"\n'
    fixture_code = code_only(fixture)
    assert "sorry" not in fixture_code and "axiom" not in fixture_code
    assert fixture_code.count("\n") == fixture.count("\n")
    DESTINATION.mkdir(parents=True, exist_ok=True)
    archive_path = DESTINATION / f"NavierStokesAndEuler-{COMMIT}.zip"
    paper_path = DESTINATION / "navier-stokes.pdf"
    if arguments.acquire:
        archive_bytes = acquire(ARCHIVE_URL, archive_path)
        paper_bytes = acquire(PAPER_URL, paper_path)
    else:
        archive_bytes = archive_path.read_bytes()
        paper_bytes = paper_path.read_bytes()
    if not paper_bytes.startswith(b"%PDF"):
        raise ValueError("Paper response is not PDF")
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        files = {}
        for member in archive.infolist():
            if member.is_dir():
                continue
            relative = member.filename.split("/", 1)[1]
            if ".." in Path(relative).parts:
                raise ValueError("Unsafe archive member")
            files[relative] = archive.read(member)
    print(f"Read {len(files)} archived sources; starting lexical import audit.", flush=True)
    modules = {
        name[:-5].replace("/", "."): name
        for name in files if name.endswith(".lean")
    }
    stripped = {name: code_only(payload.decode("utf-8")) for name, payload in files.items() if name.endswith(".lean")}
    imports = {}
    for name, source in stripped.items():
        imports[name] = []
        for line in source.splitlines():
            matched = re.match(r"\s*import\s+(.+)", line)
            if matched:
                imports[name].extend(matched.group(1).split())
    reachable = set()
    external = set()
    pending = ["NavierStokes/ComparatorSolution.lean"]
    while pending:
        name = pending.pop()
        if name in reachable:
            continue
        reachable.add(name)
        for module in imports[name]:
            if module in modules:
                pending.append(modules[module])
            else:
                external.add(module)
    token_pattern = re.compile(r"\b(?:sorry|sorryAx|admit|axiom|native_decide|unsafe|implemented_by|run_tac|elab|macro)\b")
    findings = []
    for name in sorted(reachable):
        for line_number, line in enumerate(stripped[name].splitlines(), 1):
            for matched in token_pattern.finditer(line):
                findings.append({"file": name, "line": line_number, "token": matched.group(), "code": line.strip()})
    definitions = stripped["NavierStokes/ComparatorDefinitions.lean"]
    challenge = stripped["ComparatorChallenges/NavierStokes.lean"]
    beginning = "open ContDiff Set InnerProductSpace MeasureTheory"
    ending = "end NavierStokes.Comparator"
    definitions_body = definitions.split(beginning, 1)[1].rsplit(ending, 1)[0]
    challenge_body = challenge.split(beginning, 1)[1].split("theorem navier_stokes_breakdown_R3", 1)[0]
    normalized = lambda value: re.sub(r"\s+", "", value)
    same_definitions = normalized(definitions_body) == normalized(challenge_body)
    report = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "commit": COMMIT,
        "repository_files": len(files),
        "repository_lean_files": len(modules),
        "reachable_lean_files": len(reachable),
        "reachable": sorted(reachable),
        "external_imports_not_inspected": sorted(external),
        "lexical_review_findings": findings,
        "challenge_imported_by_submission": "ComparatorChallenges/NavierStokes.lean" in reachable,
        "definition_bodies_equal_after_comment_and_whitespace_removal": same_definitions,
        "independent_kernel_build_performed": False,
        "comparator_executed": False,
        "valid_for_mts_claim": False,
        "limitations": "Lexical import/token audit only; not a Lean parser, kernel checker, transitive constant-axiom proof, or audit of Mathlib/compiler/comparator tooling.",
        "sources": [
            {"url": ARCHIVE_URL, "local_path": str(archive_path), "sha256": hashlib.sha256(archive_bytes).hexdigest(), "bytes": len(archive_bytes)},
            {"url": PAPER_URL, "local_path": str(paper_path), "sha256": hashlib.sha256(paper_bytes).hexdigest(), "bytes": len(paper_bytes)},
        ],
        "file_manifest": [{"path": name, "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload)} for name, payload in sorted(files.items())],
    }
    output_path = DESTINATION / "static-audit.json"
    if output_path.exists():
        raise FileExistsError("Preserve prior audit; choose a new version before regenerating")
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    extracts = DESTINATION / "selected-source"
    extracts.mkdir(exist_ok=True)
    selected = ["NavierStokes/ComparatorSolution.lean", "NavierStokes/ComparatorR3Theorem.lean", "NavierStokes/ComparatorR3Bridge.lean", "NavierStokes/ComparatorTheorem.lean", "NavierStokes/ComparatorDefinitions.lean", "ComparatorChallenges/NavierStokes.lean", "ComparatorChallenges/NavierStokes.json", "NavierStokes/BlowupImplication.lean", "formalization.yaml", "lakefile.toml", "lake-manifest.json", "lean-toolchain", "LICENSE"]
    for name in selected:
        if name in files:
            target = extracts / name.replace("/", "__")
            with target.open("xb") as output:
                output.write(files[name])
    summary = {key: value for key, value in report.items() if key not in {"reachable", "file_manifest"}}
    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    run()
