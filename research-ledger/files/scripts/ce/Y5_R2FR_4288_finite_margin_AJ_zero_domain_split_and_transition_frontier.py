from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4288"
CLAIM_ID = "L-129"
BRANCH = "MTS_R2FR_Y5_FINITE_MARGIN_AJ_ZERO_DOMAIN_SPLIT_AND_TRANSITION_FRONTIER_4288"
DECISION = "FINITE_MARGIN_LOCAL_AJ_ZERO_IMPORTED_TRANSITION_SHELL_REMAINS_FRONTIER_NONCLAIM"
MARKER = "PPC4161_FINITE_MARGIN_AJ_ZERO_DOMAIN_SPLIT_AND_TRANSITION_FRONTIER_4288"
PACKET_MARKER = "PPC4161_PACKET_FINITE_MARGIN_AJ_ZERO_DOMAIN_SPLIT_AND_TRANSITION_FRONTIER_4288"
NEXT_TARGET = "4289-Y5-R2FR-transition-frontier-parent-kernel-or-real-profile-row.md"

FORMAL_PATH = FORMAL / "304-PPC4161-finite-margin-AJ-zero-domain-split-and-transition-frontier.md"
DOC_PATH = POST / "4288-Y5-R2FR-finite-margin-AJ-zero-domain-split-and-transition-frontier.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4288_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
PI_B_COEFFICIENT = 0.167893843691
LOCAL_PIB = 0.9999996185074501
TRANSITION_PIB = 0.5000000000287336

SOURCES = {
    "SRC4288_00_4281_theorem_doc": (
        FORMAL / "297-PPC4161-cGamma-transport-Bgrad-routing-zero-or-profile-source-pack.md",
        "This is the finite-margin local-collar branch. It is an honest support theorem, not a fitted switch.",
        "4281 supplies the support-separated cGamma/AJ zero theorem.",
    ),
    "SRC4288_01_4281_AJ_csv": (
        SOURCE_DIR / "P8_Y5_R2FR_4281_AJ_PROFILE_BOUND_ROWS.csv",
        "AJB4281_0_zero_collar",
        "4281 machine row states finite-margin collar gives A_J,eff_private=0.",
    ),
    "SRC4288_02_4287_gate": (
        FORMAL / "303-PPC4161-cGamma-AJ-real-profile-or-parent-coefficient-derivation.md",
        "T_res/tau_L >= A_J,eff_private * abs(c_Gamma) / (0.167893843691 * Pi_B).",
        "4287 supplies the strong-window law being domain-split here.",
    ),
    "SRC4288_03_equation_register_PiB": (
        FORMAL / "05-equation-register.md",
        "local_Pi_B = 0.9999996185074501",
        "Equation register supplies the current local Pi_B anchor.",
    ),
    "SRC4288_04_equation_register_transition": (
        FORMAL / "05-equation-register.md",
        "Pi_B = 0.5000000000287336",
        "Equation register supplies the current transition-shell Pi_B anchor.",
    ),
    "SRC4288_05_4284_shell_fail": (
        FORMAL / "300-PPC4161-real-transition-shell-profile-calculator.md",
        "So the transition shell cannot be treated as a direct local metric source.",
        "4284 prevents extending the local-collar theorem through the shell by direct projection.",
    ),
    "SRC4288_06_4285_domain_status": (
        FORMAL / "301-PPC4161-transition-nonlocal-owner-kernel-or-explicit-local-closure-lock.md",
        "far-local/support-separated collars: conditionally repaired;",
        "4285 already separates far-local collars from direct transition-shell failure.",
    ),
    "SRC4288_07_4286_firewall": (
        FORMAL / "302-PPC4161-transition-closure-local-sanity-and-cGamma-AJ-interface-runner.md",
        "The closure lock cannot be used as credit for them.",
        "4286 forbids using closure to fill cGamma/AJ rows.",
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
        f'"4288 imports the 4281 finite-margin local-collar theorem into the 4287 strong-window gate. For support-separated compact local collars, R_transport_to_local=R_Bgrad_to_local=0 implies A_J,eff_private=0, so the cGamma/AJ strong-window inequality is automatically satisfied in that restricted domain. The transition shell is split out explicitly and remains unresolved because direct local projection failed and closure credit is firewalled.",'
        f'"4288 source register, domain split table, AJ zero import rows, Pi_B anchors, strong-window recalculation, transition frontier table, decision and firewall.",'
        f'private_finite_margin_local_AJ_zero_transition_frontier_split_nonclaim,'
        f'"Attack the transition frontier next: derive a parent nonlocal owner/kernel theorem, or fill real transition profile rows for R_transport_to_local, R_Bgrad_to_local, T_res/tau_L, c_Gamma, Pi_B and A_J,eff_private.",'
        f'"Promoting support-separated collar zero to global local-GR, using transition closure as AJ evidence, ignoring direct shell failure, or treating rough Pi_B anchors as public data."\n'
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


def required_ratio(a_j_eff: float, c_gamma_abs: float, pi_b: float) -> float:
    if a_j_eff == 0.0:
        return 0.0
    if pi_b <= 0.0:
        return float("inf")
    return a_j_eff * c_gamma_abs / (PI_B_COEFFICIENT * pi_b)


def capacity(pi_b: float, tres_over_tau: float, c_gamma_abs: float) -> float:
    if c_gamma_abs <= 0.0:
        return float("inf")
    return PI_B_COEFFICIENT * pi_b * tres_over_tau / c_gamma_abs


def domain_split_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DS4288_0_finite_margin_local_collar",
            "support-separated compact local collar",
            "W_loc cap supp(transport,B-gradient,transition)=empty; support-respecting projector; no boundary flux",
            "R_transport_to_local=0;R_Bgrad_to_local=0;A_J,eff_private=0",
            "closed_inside_domain_private_nonclaim",
        ),
        (
            "DS4288_1_transition_shell",
            "local collar intersects transition shell",
            "Pi_B gradient/support live; q_tr shell live; direct projection failed",
            "profile_or_parent_kernel_required",
            "frontier_unresolved",
        ),
        (
            "DS4288_2_closure_sanity",
            "explicit no-leak closure branch",
            "closure lock enforces P_metric_loc=0 as contract only",
            "does_not_fill_cGamma_AJ",
            "firewalled_from_derivation_credit",
        ),
    ]
    return [
        {
            **common(),
            "domain_id": domain_id,
            "domain": domain,
            "conditions": conditions,
            "consequence": consequence,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for domain_id, domain, conditions, consequence, status in raw
    ]


def aj_zero_import_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "AJZ4288_0_imported_theorem",
            "finite_margin_local_collar",
            0.0,
            "R_transport_to_local=0 and R_Bgrad_to_local=0",
            "imported_from_4281_AJB4281_0_zero_collar",
            "pass_by_exact_zero",
        ),
        (
            "AJZ4288_1_transition_shell",
            "transition_shell",
            float("nan"),
            "R_transport_to_local or R_Bgrad_to_local may be nonzero",
            "4284 direct shell projection failed; 4286 closure credit forbidden",
            "unresolved",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, domain, a_j, residual_condition, basis, status in raw:
        rows.append(
            {
                **common(),
                "row_id": row_id,
                "domain": domain,
                "A_J_eff_private": "MISSING" if a_j != a_j else f"{a_j:.12e}",
                "residual_condition": residual_condition,
                "basis": basis,
                "status": status,
                "score_ready": str(a_j == a_j),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def pib_anchor_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "PIB4288_0_local_anchor",
            "rough_representative_local",
            LOCAL_PIB,
            "05-equation-register.md local_Pi_B = 0.9999996185074501",
            "rough_internal_anchor_not_public_data",
        ),
        (
            "PIB4288_1_transition_anchor",
            "rough_transition_shell",
            TRANSITION_PIB,
            "05-equation-register.md Pi_B = 0.5000000000287336",
            "rough_internal_anchor_not_public_data",
        ),
        (
            "PIB4288_2_ideal_local_limit",
            "ideal_local_limit",
            1.0,
            "Pi_B -> 1 in Solar-System/lab/clock limits",
            "limit_anchor",
        ),
    ]
    return [
        {
            **common(),
            "anchor_id": anchor_id,
            "domain": domain,
            "Pi_B": f"{pi_b:.16e}",
            "source_basis": source_basis,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for anchor_id, domain, pi_b, source_basis, status in raw
    ]


def strong_window_recalc_rows() -> List[Dict[str, str]]:
    controls = [
        ("SWR4288_0_finite_margin_zero", "finite_margin_local_collar", 0.0, 1.0, LOCAL_PIB, 0.0, "PASS_BY_ZERO"),
        ("SWR4288_1_local_order_one", "rough_representative_local", 1.0, 1.0, LOCAL_PIB, 1.0, "FAIL_NEEDS_RATIO"),
        ("SWR4288_2_local_order_one_required", "rough_representative_local", 1.0, 1.0, LOCAL_PIB, required_ratio(1.0, 1.0, LOCAL_PIB), "PASS_AT_THRESHOLD"),
        ("SWR4288_3_transition_order_one", "rough_transition_shell", 1.0, 1.0, TRANSITION_PIB, 1.0, "FAIL_NEEDS_RATIO"),
        ("SWR4288_4_transition_required", "rough_transition_shell", 1.0, 1.0, TRANSITION_PIB, required_ratio(1.0, 1.0, TRANSITION_PIB), "PASS_AT_THRESHOLD"),
        ("SWR4288_5_transition_AJ_missing", "transition_shell_physical", float("nan"), 1.0, TRANSITION_PIB, 1.0, "UNSCOREABLE"),
    ]
    rows: List[Dict[str, str]] = []
    for row_id, domain, a_j, c_gamma_abs, pi_b, tres_over_tau, expected in controls:
        if a_j == a_j:
            max_aj = capacity(pi_b, tres_over_tau, c_gamma_abs)
            required = required_ratio(a_j, c_gamma_abs, pi_b)
            passes = a_j <= max_aj
            score_ready = True
        else:
            max_aj = float("nan")
            required = float("nan")
            passes = False
            score_ready = False
        rows.append(
            {
                **common(),
                "window_id": row_id,
                "domain": domain,
                "A_J_eff_private": "MISSING" if a_j != a_j else f"{a_j:.12e}",
                "abs_c_Gamma": f"{c_gamma_abs:.12e}",
                "Pi_B": f"{pi_b:.16e}",
                "T_res_over_tau_L": f"{tres_over_tau:.12e}",
                "capacity_AJ_max": "MISSING" if max_aj != max_aj else f"{max_aj:.12e}",
                "required_T_res_over_tau_L": "MISSING" if required != required else f"{required:.12e}",
                "passes_window": str(passes),
                "expected": expected,
                "score_ready": str(score_ready),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def transition_frontier_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "TF4288_0_parent_kernel",
            "derive P_metric,loc q_tr = 0 from parent nonlocal owner/kernel",
            "MISSING_PARENT_KERNEL_THEOREM",
            "would remove transition shell from direct local metric projection",
        ),
        (
            "TF4288_1_profile_fill",
            "fill R_transport_to_local and R_Bgrad_to_local profiles",
            "MISSING_REAL_TRANSITION_PROFILE_ROWS",
            "would score the shell against 4287/4288 strong-window inequality",
        ),
        (
            "TF4288_2_relaxation_fill",
            "source T_res/tau_L in the transition shell",
            "MISSING_PARENT_NORMALIZATION",
            "would decide if order-one residuals can relax fast enough",
        ),
        (
            "TF4288_3_cGamma_fill",
            "derive or source abs(c_Gamma)",
            "MISSING_PARENT_COEFFICIENT",
            "would decide if the finite product branch is naturally small",
        ),
        (
            "TF4288_4_no_closure_credit",
            "use transition no-leak closure as AJ source",
            "FORBIDDEN",
            "closure sanity stays a guardrail, not derivation evidence",
        ),
    ]
    return [
        {
            **common(),
            "frontier_id": frontier_id,
            "route": route,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for frontier_id, route, status, meaning in raw
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4288_0",
            "selected_route": "TRANSITION_FRONTIER_PARENT_KERNEL_OR_REAL_PROFILE_NEXT",
            "meaning": "The cGamma/AJ branch is no longer open everywhere: support-separated compact local collars inherit A_J=0 from 4281. The unresolved problem is specifically the transition shell.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4288_0", "Do not promote finite-margin collar zero to global local-GR."),
        ("FW4288_1", "Do not extend support-separated zero through a transition shell."),
        ("FW4288_2", "Do not use closure no-leak sanity as cGamma/AJ profile evidence."),
        ("FW4288_3", "Do not treat rough Pi_B anchors as public empirical fits."),
        ("FW4288_4", "Do not ignore the 4284 direct transition-shell failure."),
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
            "status_id": "STATUS4288_0",
            "status": "FINITE_MARGIN_LOCAL_CGAMMA_AJ_CLOSED_TRANSITION_FRONTIER_OPEN",
            "summary": "4288 converts the broad cGamma/AJ gap into a domain split: far-local/support-separated collars have A_J=0; transition shells still need parent kernel or real profile data.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NEXT4288_0",
            "target_file": NEXT_TARGET,
            "task": "Attack the transition frontier directly: parent nonlocal owner/kernel theorem first; if it fails, source real transition profile rows for the strong-window comparator.",
            "priority": "highest_remaining_local_GR_pressure_point",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    local_required = required_ratio(1.0, 1.0, LOCAL_PIB)
    transition_required = required_ratio(1.0, 1.0, TRANSITION_PIB)
    return f"""
# 304 finite-margin AJ zero domain split and transition frontier

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4288 imports the 4281 finite-margin theorem into the 4287 strong-window gate.

For a support-separated compact local collar:

```text
W_loc cap supp(transport, B-gradient, transition) = empty,
P_W support-respecting,
boundary flux through partial W_loc = 0,
```

4281 gives:

```text
R_transport_to_local[W_loc] = 0,
R_Bgrad_to_local[W_loc] = 0.
```

Therefore:

```text
A_J,eff_private[finite-margin collar] = 0.
```

That means the 4287 gate:

```text
A_J,eff_private <= {PI_B_COEFFICIENT} * Pi_B * (T_res/tau_L) / abs(c_Gamma)
```

is automatically satisfied inside that restricted domain.

## What Actually Remains

The unresolved object is no longer "all local cGamma/AJ". It is:

```text
transition-shell cGamma/AJ leakage.
```

For the current rough local `Pi_B={LOCAL_PIB}`, an order-one `A_J` and order-one `c_Gamma` would require:

```text
T_res/tau_L >= {local_required:.12f}.
```

For the rough transition-shell `Pi_B={TRANSITION_PIB}`, the same order-one branch would require:

```text
T_res/tau_L >= {transition_required:.12f}.
```

But the transition shell is not solved by those controls, because direct local projection already failed and closure credit is forbidden.

## Frontier

The next target is either:

1. derive a parent nonlocal owner/kernel theorem giving `P_metric,loc q_tr = 0`; or
2. fill real transition rows for `R_transport_to_local`, `R_Bgrad_to_local`, `T_res/tau_L`, `c_Gamma`, `Pi_B`, and `A_J,eff_private`.

No public local-GR claim is made.
"""


def checkpoint_doc() -> str:
    return f"""
# 4288 - finite-margin AJ zero domain split and transition frontier

Marker: `{MARKER}`

Decision: `{DECISION}`

4288 narrows the cGamma/AJ problem. In support-separated compact local collars, the 4281 theorem gives:

```text
R_transport_to_local=0,
R_Bgrad_to_local=0,
A_J,eff_private=0.
```

So the 4287 strong-window inequality is automatically passed in that restricted finite-margin domain.

The remaining live local-GR pressure is the transition shell. It needs a parent nonlocal owner/kernel theorem or real profile rows; closure no-leak sanity cannot be used as AJ evidence.
"""


def generated_nonclaim_rows(paths: Dict[str, Path]) -> Iterable[Dict[str, str]]:
    for path in paths.values():
        for row in csv_rows(path):
            yield row


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    domain = csv_rows(paths["domain_split"])
    aj_zero = csv_rows(paths["aj_zero_import"])
    pib = csv_rows(paths["pib_anchors"])
    window = csv_rows(paths["strong_window_recalc"])
    frontier = csv_rows(paths["transition_frontier"])
    all_generated = list(generated_nonclaim_rows(paths))
    validations = [
        ("VAL4288_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL4288_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all cited source needles found"),
        (
            "VAL4288_2_domain_split",
            {"support-separated compact local collar", "local collar intersects transition shell", "explicit no-leak closure branch"}.issubset({row["domain"] for row in domain}),
            "finite-margin, transition, and closure domains are separated",
        ),
        (
            "VAL4288_3_AJ_zero_imported",
            any(row["domain"] == "finite_margin_local_collar" and row["A_J_eff_private"] == "0.000000000000e+00" and row["score_ready"] == "True" for row in aj_zero),
            "finite-margin A_J zero imported from 4281",
        ),
        (
            "VAL4288_4_transition_AJ_unresolved",
            any(row["domain"] == "transition_shell" and row["A_J_eff_private"] == "MISSING" and row["score_ready"] == "False" for row in aj_zero),
            "transition AJ remains unresolved",
        ),
        (
            "VAL4288_5_pib_anchors",
            any(abs(float(row["Pi_B"]) - LOCAL_PIB) < 1e-15 for row in pib)
            and any(abs(float(row["Pi_B"]) - TRANSITION_PIB) < 1e-15 for row in pib),
            "local and transition Pi_B anchors emitted",
        ),
        (
            "VAL4288_6_window_split",
            any(row["window_id"] == "SWR4288_0_finite_margin_zero" and row["passes_window"] == "True" for row in window)
            and any(row["window_id"] == "SWR4288_3_transition_order_one" and row["passes_window"] == "False" for row in window)
            and any(row["window_id"] == "SWR4288_5_transition_AJ_missing" and row["score_ready"] == "False" for row in window),
            "window recalculation distinguishes zero collar from transition shell",
        ),
        (
            "VAL4288_7_frontier_routes",
            {"MISSING_PARENT_KERNEL_THEOREM", "MISSING_REAL_TRANSITION_PROFILE_ROWS", "FORBIDDEN"}.issubset({row["status"] for row in frontier}),
            "transition frontier routes and firewall present",
        ),
        ("VAL4288_8_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document written"),
        ("VAL4288_9_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "post-checkpoint document written"),
        ("VAL4288_10_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        (
            "VAL4288_11_no_claim_rows",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_generated),
            "all generated rows remain private nonclaim rows",
        ),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4288_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4288_SOURCE_REGISTER.csv",
        "domain_split": SOURCE_DIR / "P8_Y5_R2FR_4288_DOMAIN_SPLIT.csv",
        "aj_zero_import": SOURCE_DIR / "P8_Y5_R2FR_4288_AJ_ZERO_IMPORT.csv",
        "pib_anchors": SOURCE_DIR / "P8_Y5_R2FR_4288_PIB_ANCHORS.csv",
        "strong_window_recalc": SOURCE_DIR / "P8_Y5_R2FR_4288_STRONG_WINDOW_RECALCULATION.csv",
        "transition_frontier": SOURCE_DIR / "P8_Y5_R2FR_4288_TRANSITION_FRONTIER.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4288_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4288_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4288_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4288_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["domain_split"], domain_split_rows())
    write_csv(paths["aj_zero_import"], aj_zero_import_rows())
    write_csv(paths["pib_anchors"], pib_anchor_rows())
    write_csv(paths["strong_window_recalc"], strong_window_recalc_rows())
    write_csv(paths["transition_frontier"], transition_frontier_rows())
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
        "PPC4161 4288 finite-margin cGamma AJ domain split",
        "4288 imports the 4281 support-separated collar theorem into the 4287 strong-window gate. The cGamma/AJ branch is closed inside finite-margin compact local collars because `R_transport_to_local=R_Bgrad_to_local=0` gives `A_J,eff_private=0`. The remaining live local-GR pressure is specifically the transition shell, which needs a parent nonlocal owner/kernel theorem or real transition profile rows.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4288 packet finite-margin cGamma AJ split",
        "Packet update: cGamma/AJ is no longer treated as open across all local domains. Support-separated finite-margin collars inherit `A_J=0`; transition shells remain the frontier and cannot borrow closure credit.",
    )
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(VALIDATION_PATH))} failed={len(failed)}")
    print(f"{CHECKPOINT}: local order-one required T_res/tau_L={required_ratio(1.0, 1.0, LOCAL_PIB):.12f}")
    print(f"{CHECKPOINT}: transition order-one required T_res/tau_L={required_ratio(1.0, 1.0, TRANSITION_PIB):.12f}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
