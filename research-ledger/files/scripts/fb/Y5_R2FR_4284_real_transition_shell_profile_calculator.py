from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4284"
CLAIM_ID = "L-125"
BRANCH = "MTS_R2FR_Y5_REAL_TRANSITION_SHELL_PROFILE_CALCULATOR_4284"
DECISION = "SOURCE_MODEL_DIRECT_TRANSITION_SHELL_PROFILE_FAILS_BY_LARGE_FACTOR_NONLOCAL_OWNER_OR_EXPLICIT_CLOSURE_REQUIRED_NONCLAIM"
MARKER = "PPC4161_REAL_TRANSITION_SHELL_PROFILE_CALCULATOR_4284"
PACKET_MARKER = "PPC4161_PACKET_REAL_TRANSITION_SHELL_PROFILE_CALCULATOR_4284"
NEXT_TARGET = "4285-Y5-R2FR-transition-nonlocal-owner-kernel-or-explicit-local-closure-lock.md"

FORMAL_PATH = FORMAL / "300-PPC4161-real-transition-shell-profile-calculator.md"
DOC_PATH = POST / "4284-Y5-R2FR-real-transition-shell-profile-calculator-and-threshold-comparator.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4284_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SHELL = {
    "r_m": 3.3700091957845725e14,
    "L_cg_m": 3.3700091963391706e14,
    "A_curv": 1.718281828615257,
    "B_env": 1.0000000000574671,
    "Pi_B": 0.5000000000287336,
    "U_B": 0.49999999997126643,
    "trace_gradient_proxy": 0.9999704774230199,
    "u_shell": 4.381797215510729e-12,
}
BARE_S_PPN = 228210122029.09586
BARE_RATIO = 2.2821012202909584e16
BARE_REQUIRED = 4.3819265819966744e-17
U2_S_PPN = 237379306246.21347
U2_RATIO = 2.3737930624621344e16
U2_REQUIRED = 4.212667126774669e-17
WIDE_S_PPN = 23737930624621.348
WIDE_RATIO = 2.373793062462135e18
SECTOR_TUNED_RATIO = 0.5
AJ_REQUIREMENT = "0.1678939074330212*(mu_Xi T_res)/|c_Gamma|"

SOURCES = {
    "SRC4284_00_4283_runner": (
        FORMAL / "299-PPC4161-transition-boundary-topological-superpotential-or-shell-profile-runner.md",
        "The live route is now a real shell-profile calculator.",
        "4283 installs the shell-profile runner interface.",
    ),
    "SRC4284_01_92_shell_row": (
        FORMAL / "92-solar-transition-current-ppn-gate.md",
        "case = solar_transition_shell_point_mass",
        "92 provides the Solar transition shell source-model row.",
    ),
    "SRC4284_02_92_bare": (
        FORMAL / "92-solar-transition-current-ppn-gate.md",
        "PPN_ratio_to_budget = 2.2821012202909584e16",
        "92 provides the bare transition failure ratio.",
    ),
    "SRC4284_03_92_U2": (
        FORMAL / "92-solar-transition-current-ppn-gate.md",
        "PPN_ratio_to_budget = 2.3737930624621344e16",
        "92 provides the U_B^2 transition failure ratio.",
    ),
    "SRC4284_04_92_wide": (
        FORMAL / "92-solar-transition-current-ppn-gate.md",
        "PPN_ratio_to_budget = 2.373793062462135e18",
        "92 provides the wide-shell failure ratio.",
    ),
    "SRC4284_05_92_quarantine": (
        FORMAL / "92-solar-transition-current-ppn-gate.md",
        "the transition may survive only if it is not directly projected as a local metric source.",
        "92 states the nonlocal/quarantine survival condition.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if f"{CLAIM_ID}," in text:
        return
    row = (
        f'{CLAIM_ID},local_gr,'
        f'"4284 promotes the transition shell from a prose blocker to a scored source-model comparator. The imported Solar transition shell fails if treated as a direct local metric source: bare projection fails by 2.2821e16, U_B^2 projection fails by 2.3738e16, and wide-shell scaling fails by 2.3738e18. Therefore the transition branch needs a parent nonlocal owner/kernel theorem or must remain an explicit local closure; direct local projection is not viable.",'
        f'"4284 source register, Solar shell inputs, direct-profile comparator results, suppression requirements, AJ interface rows, decision and firewall.",'
        f'private_transition_shell_direct_metric_profile_fails_nonlocal_owner_or_closure_required_nonclaim,'
        f'"Derive a nonlocal owner/kernel law that removes the shell from direct local metric projection, or lock the transition branch as explicit closure and keep testing nonlocal/galaxy/cosmology sectors separately.",'
        f'"Treating direct shell projection as local-GR safe, counting sector-tuned suppression as evidence, or using U_B^2/wide-shell scaling as a transition rescue."\n'
    )
    path.write_text(text.rstrip() + "\n" + row, encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def shell_input_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for key, value in SHELL.items():
        rows.append(
            {
                **common(),
                "input_id": f"SHELL4284_{key}",
                "quantity": key,
                "value": repr(value),
                "source_path": str(FORMAL / "92-solar-transition-current-ppn-gate.md"),
                "status": "SOURCE_MODEL_IMPORTED",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def comparator_rows() -> List[Dict[str, str]]:
    raw = [
        ("COMP4284_0_bare", "bare_transition_shell", BARE_S_PPN, BARE_RATIO, BARE_REQUIRED, "FAIL_DIRECT_LOCAL_METRIC_SOURCE"),
        ("COMP4284_1_U2", "U_B2_transition_shell", U2_S_PPN, U2_RATIO, U2_REQUIRED, "FAIL_U_B2_TRANSITION_SUPPRESSION"),
        ("COMP4284_2_wide", "wide_transition_shell_width_100", WIDE_S_PPN, WIDE_RATIO, 1.0 / WIDE_RATIO, "FAIL_WIDE_SHELL_SCALING"),
        ("COMP4284_3_sector_tuned", "sector_tuned_budget_row", 5.0e-6, SECTOR_TUNED_RATIO, 2.0, "FORBIDDEN_TUNED_CONTROL_NOT_EVIDENCE"),
        ("COMP4284_4_exact_zero", "exact_theorem_zero_control", 0.0, 0.0, 1.0, "CONTROL_PASS_IF_PARENT_THEOREM_EXISTS"),
    ]
    rows: List[Dict[str, str]] = []
    for comparator_id, scenario, s_ppn, ratio, required, verdict in raw:
        rows.append(
            {
                **common(),
                "comparator_id": comparator_id,
                "scenario": scenario,
                "S_PPN": f"{s_ppn:.15g}",
                "PPN_ratio_to_budget": f"{ratio:.15g}",
                "required_suppression_factor": f"{required:.15g}",
                "verdict": verdict,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def suppression_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "requirement_id": "REQ4284_0_bare",
            "quantity": "bare_shell_suppression",
            "required_value": f"<= {BARE_REQUIRED:.15g}",
            "meaning": "Direct bare local projection must be suppressed by this factor to meet the proxy budget.",
            "status": "NOT_MET_BY_DIRECT_PROFILE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "requirement_id": "REQ4284_1_U2",
            "quantity": "U_B2_shell_suppression",
            "required_value": f"<= {U2_REQUIRED:.15g}",
            "meaning": "U_B^2 does not supply this at transition where U_B~1/2.",
            "status": "NOT_MET_BY_U_B2_TRANSITION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "requirement_id": "REQ4284_2_nonlocal",
            "quantity": "P_metric_loc_q_tr",
            "required_value": "0 or <= sourced shell threshold by parent theorem",
            "meaning": "The shell survives local tests only if removed from direct local metric projection or explicitly profile-bounded.",
            "status": "THEOREM_OR_CLOSURE_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def aj_interface_rows() -> List[Dict[str, str]]:
    raw = [
        ("AJI4284_0", "R_transport_to_local", "MISSING_REAL_CGAMMA_AJ_PROFILE", AJ_REQUIREMENT, "PROFILE_STILL_REQUIRED"),
        ("AJI4284_1", "R_Bgrad_to_local", "MISSING_REAL_CGAMMA_AJ_PROFILE", AJ_REQUIREMENT, "PROFILE_STILL_REQUIRED"),
        ("AJI4284_2", "T_res/tau_L", "MISSING_PARENT_NORMALIZATION", "needed for AJ conversion", "PROFILE_STILL_REQUIRED"),
        ("AJI4284_3", "c_Gamma", "MISSING_PARENT_COEFFICIENT", "needed for AJ conversion", "PROFILE_STILL_REQUIRED"),
    ]
    return [
        {
            **common(),
            "interface_id": interface_id,
            "quantity": quantity,
            "value": value,
            "requirement": requirement,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for interface_id, quantity, value, requirement, status in raw
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4284_0",
            "selected_route": "NONLOCAL_OWNER_KERNEL_OR_EXPLICIT_CLOSURE_LOCK",
            "meaning": "Direct local metric projection of the source-model shell fails; derive a parent nonlocal owner/kernel or lock transition safety as explicit closure.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4284_0", "Do not use direct transition-shell local metric projection as a local-GR pass."),
        ("FW4284_1", "Do not count U_B^2 as transition-shell suppression; it fails where U_B is about one half."),
        ("FW4284_2", "Do not count wide-shell scaling as rescue; the source-model proxy worsens."),
        ("FW4284_3", "Do not use sector-tuned suppression as evidence."),
        ("FW4284_4", "Do not infer cGamma/AJ profile pass from the trace-shell comparator alone."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4284_0",
            "status": "DIRECT_TRANSITION_SHELL_PROFILE_FAILS_NONLOCAL_OWNER_OR_CLOSURE_REQUIRED",
            "summary": "The transition shell is now a scored failure under direct local projection, not an undefined gap.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NEXT4284_0",
            "target_file": NEXT_TARGET,
            "task": "Try to derive a parent nonlocal owner/kernel law with zero local metric projection; otherwise lock transition safety as explicit closure and keep the finite cGamma/AJ rows open.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 300 Real Transition-Shell Profile Calculator

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4284 turns the transition shell into a scored object.

Imported source-model shell:

```text
r = {SHELL["r_m"]} m
L_cg = {SHELL["L_cg_m"]} m
B_env = {SHELL["B_env"]}
Pi_B = {SHELL["Pi_B"]}
U_B = {SHELL["U_B"]}
trace_gradient_proxy = {SHELL["trace_gradient_proxy"]}
u_shell = {SHELL["u_shell"]}
```

Direct local projection fails:

```text
bare PPN_ratio_to_budget = {BARE_RATIO}
required_suppression_factor = {BARE_REQUIRED}
```

The `U_B^2` transition row also fails:

```text
U_B2 PPN_ratio_to_budget = {U2_RATIO}
required_suppression_factor = {U2_REQUIRED}
```

Wide-shell scaling also fails:

```text
wide-shell PPN_ratio_to_budget = {WIDE_RATIO}.
```

So the transition shell cannot be treated as a direct local metric source.

## What This Means

The next physics fork is now sharp:

```text
derive P_metric,loc q_tr = 0 from a parent nonlocal owner/kernel law,
or keep transition local safety as an explicit closure/guardrail.
```

This does not kill the wider MTS framework. It says the local transition shell cannot be one of the places where MTS claims derived GR unless the nonlocal owner theorem appears.

## Still Open

The trace-shell comparator does not fill the cGamma AJ rows. Those still require:

```text
R_transport_to_local,
R_Bgrad_to_local,
T_res/tau_L,
c_Gamma.
```

## No-Claim Guard

No public local-GR claim is made.

## Next Target

`{NEXT_TARGET}` should either derive the parent nonlocal owner/kernel law or lock the transition branch as explicit local closure.
"""


def checkpoint_doc() -> str:
    return f"""
# 4284 - real transition-shell profile calculator and threshold comparator

Marker: `{MARKER}`

Decision: `{DECISION}`

4284 imports the Solar transition source-model row and records:

```text
bare direct projection fails by {BARE_RATIO};
U_B^2 transition projection fails by {U2_RATIO};
wide-shell scaling fails by {WIDE_RATIO}.
```

Direct local transition projection is therefore not viable without a parent nonlocal owner/kernel theorem.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    shell = csv_rows(paths["shell"])
    comparator = csv_rows(paths["comparator"])
    suppression = csv_rows(paths["suppression"])
    aj = csv_rows(paths["aj"])
    generated_rows: Iterable[Dict[str, str]] = (
        sources
        + shell
        + comparator
        + suppression
        + aj
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4284_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4284_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4284_2_shell_inputs",
            {"B_env", "Pi_B", "U_B", "trace_gradient_proxy", "u_shell"}.issubset({row["quantity"] for row in shell}),
            "shell input row imported",
        ),
        (
            "VAL4284_3_direct_failures",
            {"FAIL_DIRECT_LOCAL_METRIC_SOURCE", "FAIL_U_B2_TRANSITION_SUPPRESSION", "FAIL_WIDE_SHELL_SCALING"}.issubset(
                {row["verdict"] for row in comparator}
            ),
            "direct projection failures recorded",
        ),
        (
            "VAL4284_4_forbidden_control",
            any(row["verdict"] == "FORBIDDEN_TUNED_CONTROL_NOT_EVIDENCE" for row in comparator),
            "sector-tuned control is forbidden",
        ),
        (
            "VAL4284_5_nonlocal_required",
            any(row["status"] == "THEOREM_OR_CLOSURE_REQUIRED" for row in suppression),
            "nonlocal owner/kernel or closure requirement emitted",
        ),
        (
            "VAL4284_6_aj_open",
            {"R_transport_to_local", "R_Bgrad_to_local", "c_Gamma"}.issubset({row["quantity"] for row in aj}),
            "cGamma AJ interface still explicit",
        ),
        ("VAL4284_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4284_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4284_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        (
            "VAL4284_10_no_claim_rows",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in generated_rows),
            "all generated rows remain nonclaim",
        ),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4284_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4284_SOURCE_REGISTER.csv",
        "shell": SOURCE_DIR / "P8_Y5_R2FR_4284_SOLAR_SHELL_INPUTS.csv",
        "comparator": SOURCE_DIR / "P8_Y5_R2FR_4284_PROFILE_COMPARATOR_RESULTS.csv",
        "suppression": SOURCE_DIR / "P8_Y5_R2FR_4284_SUPPRESSION_REQUIREMENTS.csv",
        "aj": SOURCE_DIR / "P8_Y5_R2FR_4284_CGAMMA_AJ_PROFILE_INTERFACE.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4284_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4284_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4284_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4284_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["shell"], shell_input_rows())
    write_csv(paths["comparator"], comparator_rows())
    write_csv(paths["suppression"], suppression_rows())
    write_csv(paths["aj"], aj_interface_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4284 transition shell scored",
        "4284 imports the Solar transition source-model row and records direct local projection as a large scored failure: bare, U_B^2 and wide-shell transition variants all miss the proxy budget by enormous factors. The next legitimate route is parent nonlocal owner/kernel derivation or explicit transition-local closure.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4284 packet transition shell comparator",
        "Packet update: direct local transition projection is now scored and fails. The transition branch must be nonlocal-owner/theorem based or closure-locked; cGamma AJ profile rows remain explicit.",
    )
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(VALIDATION_PATH))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
