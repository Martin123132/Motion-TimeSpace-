from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4285"
CLAIM_ID = "L-126"
BRANCH = "MTS_R2FR_Y5_TRANSITION_NONLOCAL_OWNER_KERNEL_OR_EXPLICIT_CLOSURE_LOCK_4285"
DECISION = "PARENT_NONLOCAL_OWNER_KERNEL_NOT_DERIVED_TRANSITION_LOCAL_SAFETY_LOCKED_AS_EXPLICIT_NOLEAK_CLOSURE_NONCLAIM"
MARKER = "PPC4161_TRANSITION_NONLOCAL_OWNER_KERNEL_OR_EXPLICIT_CLOSURE_LOCK_4285"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_NONLOCAL_OWNER_KERNEL_OR_EXPLICIT_CLOSURE_LOCK_4285"
NEXT_TARGET = "4286-Y5-R2FR-transition-closure-local-sanity-and-cGamma-AJ-interface-runner.md"

FORMAL_PATH = FORMAL / "301-PPC4161-transition-nonlocal-owner-kernel-or-explicit-local-closure-lock.md"
DOC_PATH = POST / "4285-Y5-R2FR-transition-nonlocal-owner-kernel-or-explicit-local-closure-lock.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4285_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
SHELL_FAIL_RATIO = "2.37379306246213e+16"
LOCAL_PROJECTOR_REQUIRED = "0"
PHENO_TOLERANCE = "1e-12"
AJ_REQUIREMENT = "0.1678939074330212*(mu_Xi T_res)/|c_Gamma|"

SOURCES = {
    "SRC4285_00_4284_result": (
        FORMAL / "300-PPC4161-real-transition-shell-profile-calculator.md",
        "derive P_metric,loc q_tr = 0 from a parent nonlocal owner/kernel law",
        "4284 selects parent nonlocal owner/kernel or explicit closure after direct shell projection fails.",
    ),
    "SRC4285_01_94_kernel_required": (
        FORMAL / "94-routed-transition-equations-v1.md",
        "quarantine_nonlocal_kernel_required",
        "94 writes the routed-current skeleton and identifies the missing nonlocal kernel.",
    ),
    "SRC4285_02_95_pheno_kernel": (
        FORMAL / "95-transition-owner-equations-v2.md",
        "a normalized nonlocal kernel as an explicitly phenomenological closure.",
        "95 says the normalized kernel is closure-only, not parent-derived.",
    ),
    "SRC4285_03_96_contract": (
        FORMAL / "96-transition-closure-contract.md",
        "The closure kernel remains:",
        "96 locks the closure contract: no leak, conservation normalization, shared parameters and demotion.",
    ),
    "SRC4285_04_97_priors": (
        FORMAL / "97-transition-closure-observable-priors.md",
        "theta_closure = {P_Q, P_gal, P_cos, xi_Q}.",
        "97 defines the shared closure parameter vector.",
    ),
    "SRC4285_05_98_falsification": (
        FORMAL / "98-transition-closure-falsification-pack.md",
        "The transition closure now has a concrete falsification pack:",
        "98 makes the closure killable before empirical use.",
    ),
    "SRC4285_06_102_thresholds": (
        FORMAL / "102-transition-closure-observable-threshold-spec.md",
        "P_metric_loc_abs_max = 0",
        "102 gives executable local no-leak observables and thresholds.",
    ),
    "SRC4285_07_136_kernel_theorem": (
        FORMAL / "136-metric-response-kernel-theorem.md",
        "metric_response_kernel_formal_only_source_lift_missing_parent_theorem_not_derived",
        "136 rejects the metric-response kernel as parent-derived while preserving theorem shape.",
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
        f'"4285 locks the transition-shell local safety route as explicit no-leak closure unless a future parent nonlocal owner/kernel theorem is derived. The current corpus has a clean normalized kernel contract, shared theta_closure, falsification and threshold package, but the parent kernel/source-lift theorem is not derived. Therefore transition safety is usable only as labelled phenomenological closure and not as evidence of derived local GR.",'
        f'"4285 source register, parent-kernel derivation audit, explicit closure lock, falsification-contract import, local-GR status rows, cGamma/AJ open rows, decision and firewall.",'
        f'private_transition_local_safety_explicit_no_leak_closure_parent_kernel_not_derived_nonclaim,'
        f'"Run local no-leak sanity plus cGamma AJ interface checks, or derive a genuine parent nonlocal owner/kernel law that supersedes the closure.",'
        f'"Calling the closure parent-derived, letting P_metric_loc become nonzero, using sector-specific closure parameters, or hiding unresolved cGamma/AJ profiles."\n'
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


def parent_kernel_audit_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "PKD4285_0_target",
            "q_Q^nu(x)=int K_Q^nu{}_rho(x,y) q_tr^rho(y) dSigma_y",
            "Correct nonlocal owner kernel shape.",
            "KERNEL_SHAPE_DEFINED",
        ),
        (
            "PKD4285_1_normalization",
            "int K_Q^nu{}_rho(x,y) dSigma_y = P_Q delta^nu{}_rho",
            "Required conservation/accounting normalization.",
            "NORMALIZATION_CONTRACT_DEFINED",
        ),
        (
            "PKD4285_2_parent_gap",
            "K_Q is not derived from parent dynamics/action/source-lift.",
            "95 and 136 leave parent nonlocal kernel/source-lift theorem open.",
            "PARENT_KERNEL_NOT_DERIVED",
        ),
        (
            "PKD4285_3_response_gap",
            "R_loc[q_tr]=0 is formal until Sigma_metric[q_tr] is parent-fixed.",
            "136 says vector-current equations alone do not determine local PPN metric response.",
            "METRIC_RESPONSE_KERNEL_NOT_DERIVED",
        ),
        (
            "PKD4285_4_result",
            "P_metric,loc q_tr=0 cannot be called derived.",
            "The current branch must be closure-locked.",
            "DERIVED_LOCAL_GR_THROUGH_SHELL_FALSE",
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "mathematical_clause": clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, clause, meaning, status in raw
    ]


def closure_lock_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "CL4285_0_no_leak",
            "P_metric,loc = 0 for failed Solar transition closure",
            LOCAL_PROJECTOR_REQUIRED,
            "mandatory",
            "LOCAL_NO_LEAK_LOCKED",
        ),
        (
            "CL4285_1_normalization",
            "P_Q + P_gal + P_cos + P_metric,loc = 1",
            "1",
            "mandatory",
            "CONSERVATION_NORMALIZATION_LOCKED",
        ),
        (
            "CL4285_2_shared_theta",
            "theta_closure = {P_Q, P_gal, P_cos, xi_Q}",
            "shared across local, galaxy, cosmology",
            "mandatory",
            "SHARED_CLOSURE_VECTOR_LOCKED",
        ),
        (
            "CL4285_3_label",
            "closure use must be labelled phenomenological closure",
            "not parent-derived",
            "mandatory",
            "PUBLIC_DERIVATION_CLAIM_FORBIDDEN",
        ),
        (
            "CL4285_4_local_tolerance",
            "P_metric_loc_abs_max <= tolerance only for numerical implementation sanity; theorem target is exactly zero",
            PHENO_TOLERANCE,
            "sanity threshold",
            "LOCAL_NUMERIC_SANITY_THRESHOLD_IMPORTED",
        ),
    ]
    return [
        {
            **common(),
            "lock_id": lock_id,
            "clause": clause,
            "value_or_rule": value,
            "requirement_level": level,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for lock_id, clause, value, level, status in raw
    ]


def falsification_import_rows() -> List[Dict[str, str]]:
    raw = [
        ("FI4285_0_local_no_leak", "P_metric_loc_abs_max = 0; implementation sanity <= 1e-12", "102", "IMPORTED"),
        ("FI4285_1_current_leak", "local_current_leak_norm <= 1e-12 for implementation sanity", "102", "IMPORTED"),
        ("FI4285_2_normalization", "P_Q + P_gal + P_cos + P_metric,loc = 1", "96/98", "IMPORTED"),
        ("FI4285_3_shared_simplex", "one theta_closure across local/galaxy/cosmology", "97/98", "IMPORTED"),
        ("FI4285_4_holdouts", "galaxy and cosmology labelled holdout falsifiers before any empirical support language", "98/100/102", "IMPORTED"),
    ]
    return [
        {
            **common(),
            "import_id": import_id,
            "contract": contract,
            "source_label": source_label,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for import_id, contract, source_label, status in raw
    ]


def local_gr_status_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "LGS4285_0_far_local",
            "support-separated compact local collars",
            "conditionally repaired by finite-margin/no-flux selector",
            "PRIVATE_CONDITIONAL_BRANCH",
        ),
        (
            "LGS4285_1_shell_direct",
            "direct transition shell as local metric source",
            f"fails by ratio ~{SHELL_FAIL_RATIO}",
            "DIRECT_LOCAL_METRIC_ROUTE_REJECTED",
        ),
        (
            "LGS4285_2_shell_closure",
            "transition-shell local safety",
            "explicit no-leak phenomenological closure unless parent kernel theorem appears",
            "EXPLICIT_CLOSURE_LOCKED",
        ),
        (
            "LGS4285_3_public_claim",
            "derived local GR through transition shells",
            "not proved",
            "PUBLIC_LOCAL_GR_CLAIM_FORBIDDEN",
        ),
    ]
    return [
        {
            **common(),
            "status_id": status_id,
            "branch_scope": scope,
            "result": result,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for status_id, scope, result, status in raw
    ]


def cgamma_aj_rows() -> List[Dict[str, str]]:
    raw = [
        ("AJ4285_0_Rtransport", "R_transport_to_local", "MISSING_REAL_CGAMMA_AJ_PROFILE", AJ_REQUIREMENT, "OPEN_PROFILE_ROW"),
        ("AJ4285_1_RBgrad", "R_Bgrad_to_local", "MISSING_REAL_CGAMMA_AJ_PROFILE", AJ_REQUIREMENT, "OPEN_PROFILE_ROW"),
        ("AJ4285_2_Tres_tau", "T_res/tau_L", "MISSING_PARENT_NORMALIZATION", "needed for AJ conversion", "OPEN_PROFILE_ROW"),
        ("AJ4285_3_cGamma", "c_Gamma", "MISSING_PARENT_COEFFICIENT", "needed for AJ conversion", "OPEN_PROFILE_ROW"),
    ]
    return [
        {
            **common(),
            "row_id": row_id,
            "quantity": quantity,
            "value": value,
            "requirement": requirement,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, quantity, value, requirement, status in raw
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4285_0",
            "selected_route": "EXPLICIT_NOLEAK_CLOSURE_LOCK_WITH_PARENT_KERNEL_OPEN",
            "meaning": "No parent nonlocal owner/kernel theorem is currently derived. Transition safety is locked as no-leak labelled closure; a future parent kernel can supersede it.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4285_0", "Do not call the normalized nonlocal closure parent-derived."),
        ("FW4285_1", "Do not allow P_metric,loc to become nonzero for the failed Solar transition branch."),
        ("FW4285_2", "Do not use different theta_closure values by sector."),
        ("FW4285_3", "Do not use closure-backed galaxy/cosmology fits as evidence of derived local GR."),
        ("FW4285_4", "Do not hide unresolved cGamma/AJ profile rows behind the closure lock."),
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
            "status_id": "STATUS4285_0",
            "status": "TRANSITION_LOCAL_SAFETY_EXPLICIT_CLOSURE_LOCKED_PARENT_KERNEL_OPEN",
            "summary": "4285 prevents further theorem-circling on the transition shell: use explicit no-leak closure or derive a real parent nonlocal owner/kernel.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NEXT4285_0",
            "target_file": NEXT_TARGET,
            "task": "Run the local no-leak sanity and cGamma AJ interface checks under the closure lock, while keeping parent-kernel derivation as a separate future theorem route.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 301 Transition Nonlocal Owner Kernel Or Explicit Local Closure Lock

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4285 tests the only remaining local-transition survival route after 4284.

The correct nonlocal owner shape is:

```text
q_Q^nu(x) = int_{{Sigma_x}} K_Q^nu{{}}_rho(x,y) q_tr^rho(y) dSigma_y.
```

with normalization:

```text
int_{{Sigma_x}} K_Q^nu{{}}_rho(x,y) dSigma_y = P_Q delta^nu{{}}_rho.
```

and closure accounting:

```text
P_Q + P_gal + P_cos + P_metric,loc = 1.
```

For the failed Solar transition branch:

```text
P_metric,loc = 0.
```

The current corpus does **not** derive `K_Q` from a parent action, source-lift, or metric-response kernel theorem. Therefore the kernel remains a phenomenological no-leak closure, not derived local GR.

## Closure Lock

The transition branch is locked as:

```text
explicit no-leak closure,
shared theta_closure = {{P_Q, P_gal, P_cos, xi_Q}},
no sector-specific closure parameters,
labelled phenomenological use only,
local no-leak falsifier active.
```

Executable local sanity targets are:

```text
P_metric_loc_abs_max = 0
local_current_leak_norm = 0
```

with numerical implementation sanity tolerance:

```text
<= {PHENO_TOLERANCE}.
```

## Local-GR Status

```text
far-local/support-separated collars: conditionally repaired;
direct transition shell: scored failure;
transition local safety: explicit closure unless parent kernel theorem appears;
derived local GR through transition shell: false.
```

## Still Open

The closure lock does not fill the cGamma AJ rows:

```text
R_transport_to_local,
R_Bgrad_to_local,
T_res/tau_L,
c_Gamma.
```

Those remain explicit profile/coefficient obligations.

## No-Claim Guard

No public local-GR claim is made.

## Next Target

`{NEXT_TARGET}` should run the local no-leak sanity and cGamma AJ interface checks under this closure lock.
"""


def checkpoint_doc() -> str:
    return f"""
# 4285 - transition nonlocal owner kernel or explicit local closure lock

Marker: `{MARKER}`

Decision: `{DECISION}`

4285 locks the failed transition-shell local safety route as explicit no-leak closure:

```text
P_metric,loc = 0,
P_Q + P_gal + P_cos + P_metric,loc = 1,
theta_closure = {{P_Q, P_gal, P_cos, xi_Q}},
```

because the parent nonlocal owner/kernel theorem is not derived.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    parent = csv_rows(paths["parent"])
    closure = csv_rows(paths["closure"])
    falsification = csv_rows(paths["falsification"])
    local_status = csv_rows(paths["local_status"])
    aj = csv_rows(paths["aj"])
    generated_rows: Iterable[Dict[str, str]] = (
        sources
        + parent
        + closure
        + falsification
        + local_status
        + aj
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4285_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4285_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4285_2_parent_kernel_not_derived",
            any(row["status"] == "PARENT_KERNEL_NOT_DERIVED" for row in parent)
            and any(row["status"] == "METRIC_RESPONSE_KERNEL_NOT_DERIVED" for row in parent),
            "parent kernel and metric response theorem remain unsigned",
        ),
        (
            "VAL4285_3_closure_lock",
            any(row["status"] == "LOCAL_NO_LEAK_LOCKED" for row in closure)
            and any(row["status"] == "CONSERVATION_NORMALIZATION_LOCKED" for row in closure)
            and any(row["status"] == "SHARED_CLOSURE_VECTOR_LOCKED" for row in closure),
            "closure lock clauses emitted",
        ),
        (
            "VAL4285_4_falsification_import",
            {"FI4285_0_local_no_leak", "FI4285_2_normalization", "FI4285_3_shared_simplex"}.issubset(
                {row["import_id"] for row in falsification}
            ),
            "falsification contracts imported",
        ),
        (
            "VAL4285_5_local_gr_status",
            any(row["status"] == "EXPLICIT_CLOSURE_LOCKED" for row in local_status)
            and any(row["status"] == "PUBLIC_LOCAL_GR_CLAIM_FORBIDDEN" for row in local_status),
            "local GR status remains nonclaim",
        ),
        (
            "VAL4285_6_aj_open",
            {"R_transport_to_local", "R_Bgrad_to_local", "T_res/tau_L", "c_Gamma"}.issubset({row["quantity"] for row in aj}),
            "cGamma AJ obligations remain explicit",
        ),
        ("VAL4285_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4285_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4285_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        (
            "VAL4285_10_no_claim_rows",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in generated_rows),
            "all generated rows remain nonclaim",
        ),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4285_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4285_SOURCE_REGISTER.csv",
        "parent": SOURCE_DIR / "P8_Y5_R2FR_4285_PARENT_KERNEL_DERIVATION_AUDIT.csv",
        "closure": SOURCE_DIR / "P8_Y5_R2FR_4285_EXPLICIT_CLOSURE_LOCK.csv",
        "falsification": SOURCE_DIR / "P8_Y5_R2FR_4285_FALSIFICATION_CONTRACT_IMPORT.csv",
        "local_status": SOURCE_DIR / "P8_Y5_R2FR_4285_LOCAL_GR_STATUS.csv",
        "aj": SOURCE_DIR / "P8_Y5_R2FR_4285_CGAMMA_AJ_OPEN_ROWS.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4285_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4285_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4285_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4285_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["parent"], parent_kernel_audit_rows())
    write_csv(paths["closure"], closure_lock_rows())
    write_csv(paths["falsification"], falsification_import_rows())
    write_csv(paths["local_status"], local_gr_status_rows())
    write_csv(paths["aj"], cgamma_aj_rows())
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
        "PPC4161 4285 transition closure lock",
        "4285 locks transition-shell local safety as explicit no-leak phenomenological closure unless a future parent nonlocal owner/kernel theorem is derived. The closure has normalized accounting, shared theta_closure, imported falsifiers, and public-claim demotion; it does not fill cGamma AJ profiles or prove derived local GR through the shell.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4285 packet transition no-leak closure",
        "Packet update: transition shell direct local projection has failed and parent kernel is unsigned, so the transition branch is locked as explicit no-leak closure. Far-local/support-separated collars remain conditional; cGamma AJ rows remain open.",
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
