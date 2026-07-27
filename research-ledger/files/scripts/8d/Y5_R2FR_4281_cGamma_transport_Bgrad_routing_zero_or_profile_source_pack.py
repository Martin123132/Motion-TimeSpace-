from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4281"
CLAIM_ID = "L-122"
BRANCH = "MTS_R2FR_Y5_CGAMMA_TRANSPORT_BGRAD_ROUTING_ZERO_OR_PROFILE_SOURCE_PACK_4281"
DECISION = "FINITE_MARGIN_LOCAL_COLLAR_ZERO_DERIVED_TRANSITION_SHELL_REMAINS_PROFILE_OR_QUARANTINE_NONCLAIM"
MARKER = "PPC4161_CGAMMA_TRANSPORT_BGRAD_ROUTING_ZERO_OR_PROFILE_SOURCE_PACK_4281"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_TRANSPORT_BGRAD_ROUTING_ZERO_OR_PROFILE_SOURCE_PACK_4281"
NEXT_TARGET = "4282-Y5-R2FR-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md"

FORMAL_PATH = FORMAL / "297-PPC4161-cGamma-transport-Bgrad-routing-zero-or-profile-source-pack.md"
DOC_PATH = POST / "4281-Y5-R2FR-cGamma-transport-Bgrad-routing-zero-or-profile-source-pack.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4281_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
AJ_STRONG_WINDOW = "0.1678939074330212*(mu_Xi T_res)/|c_Gamma|"
AJ_PIB_WINDOW = "0.167893843691*Pi_B*(T_res/tau_L)/|c_Gamma|"

SOURCES = {
    "SRC4281_00_4280_AJ_gate": (
        FORMAL / "296-PPC4161-cGamma-parent-memory-equation-AJ-source-coefficient-or-profile-fill.md",
        "A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|.",
        "4280 leaves only transport/B-gradient leakage in the private cGamma AJ budget.",
    ),
    "SRC4281_01_4242_M2_pruning": (
        FORMAL / "258-PPC4161-M2-defect-source-map-pruning-or-real-profile-input-pack.md",
        "Bgrad transition support needs boundary/quarantine treatment",
        "4242 routes M2 transport/Bgrad terms into explicit residuals and marks routing as conditional.",
    ),
    "SRC4281_02_transition_quarantine": (
        FORMAL / "132-transition-shell-bound-or-quarantine.md",
        "The current must either:",
        "132 forbids hiding transition current and allows only exact cancellation, theorem projection, or explicit conservation ownership.",
    ),
    "SRC4281_03_solar_transition_gate": (
        FORMAL / "92-solar-transition-current-ppn-gate.md",
        "an unsuppressed transition shell is ruled out as a local metric source in this proxy.",
        "92 supplies the countercase: transition shell cannot be accepted as a local metric source by direct projection.",
    ),
    "SRC4281_04_XB_gradient_invariants": (
        FORMAL / "85-coarse-graining-invariants-XB.md",
        "smooth vacuum transition shells should not route to chi.",
        "85 separates structured galaxy transport from smooth vacuum transition shells and defines B-gradient warning invariants.",
    ),
    "SRC4281_05_projector_red_team": (
        FORMAL / "06-consistency-red-team.md",
        "P_loc = Pi_B + (1 - Pi_B)(1 - C_cos)(1 - T_gal)",
        "06 records the universal projector algebra and shows Solar transition shells remain in the local branch, not galaxy/cosmology.",
    ),
    "SRC4281_06_product_budgets": (
        FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md",
        "C_Gamma_Gdot",
        "Product-bound target table retained for finite profile fallback.",
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
        f'"4281 proves a restricted but useful cGamma routing result: on compact local collars with finite margin away from transport support and B-gradient/transition support, support-respecting local projection gives R_transport_to_local=R_Bgrad_to_local=0. The same checkpoint rejects global transition-shell closure because the Solar/vacuum transition remains P_loc=1 and fails as a direct local metric source unless an exact cancellation/projector theorem or explicit conserved quarantine is supplied.",'
        f'"4281 source register, finite-margin zero theorem, transition-shell countercase, profile source schema, AJ profile bound rows, decision and firewall.",'
        f'private_finite_margin_local_cGamma_routing_zero_transition_shell_nonclaim,'
        f'"Either derive exact transition-shell cancellation/projector/conservation ownership or fill real finite profile rows for R_transport/R_Bgrad and cGamma arena projections.",'
        f'"Claiming global local-GR closure from the finite-margin collar theorem, routing Solar transition shells into galaxy/cosmology, or treating missing profile rows as zeros."\n'
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


def zero_theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "TZ4281_0_definitions",
            "R_transport_to_local[W]=||P_W P_loc T_transport||; R_Bgrad_to_local[W]=||P_W P_loc C_B grad(B_env,Pi_B,L_cg)||",
            "4280/4242 residual definitions plus XB gradient invariants",
            "DEFINITIONS_IMPORTED",
        ),
        (
            "TZ4281_1_support_separation",
            "If W_loc cap supp(T_transport)=empty and W_loc cap supp(grad B_env,grad Pi_B,grad L_cg,I_Bgrad)=empty, then both projected residuals vanish on W_loc.",
            "standard support theorem for local projector acting on distributions/functions",
            "FINITE_MARGIN_LOCAL_COLLAR_ZERO_DERIVED",
        ),
        (
            "TZ4281_2_boundary_no_flux",
            "Boundary leakage is zero only if P_W is support-respecting and no flux enters the compact collar through partial W_loc.",
            "132 forbids unowned transition current; 258 says Bgrad needs boundary/quarantine treatment",
            "BOUNDARY_CLAUSE_REQUIRED",
        ),
        (
            "TZ4281_3_transport_not_chi",
            "Smooth vacuum transition shells have T_gal=0 and must not route to chi/galaxy transport; structured matter gradients are required for transport ownership.",
            "85 and 06 projector algebra",
            "TRANSPORT_ZERO_FOR_SMOOTH_VACUUM_COLLAR_CONDITIONALLY_DERIVED",
        ),
        (
            "TZ4281_4_AJ_consequence",
            "On finite-margin collars satisfying TZ4281_1 through TZ4281_3: A_J,eff_private=0 after the 4280 A_src=0 import.",
            "4280 plus finite-margin support zero",
            "AJ_ZERO_ON_RESTRICTED_LOCAL_COLLAR",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "mathematical_form": mathematical_form,
            "source_basis": source_basis,
            "status": status,
            "claim_scope": "private_restricted_local_collar",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, mathematical_form, source_basis, status in raw
    ]


def countercase_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "TC4281_0_solar_transition_projector",
            "Solar/vacuum transition has Pi_B~=1/2, T_gal=0, P_loc=1, P_gal=0, P_cos=0.",
            "06 red-team lines and 92 transition row",
            "NOT_ROUTABLE_TO_GALAXY_OR_COSMOLOGY",
        ),
        (
            "TC4281_1_direct_metric_fail",
            "Bare transition shell fails as a direct local metric source; U_B^2 suppression also fails.",
            "92 solar transition PPN gate",
            "BLOCKS_GLOBAL_ZERO_CLAIM",
        ),
        (
            "TC4281_2_smooth_switch_counterexample",
            "A smooth Pi_B/B_env switch has nonzero gradient on its transition shell, so finite-margin zero cannot be extended across the shell.",
            "85 transition-gradient invariant and 132 quarantine gate",
            "SMOOTH_TRANSITION_REQUIRES_PROFILE_OR_THEOREM",
        ),
        (
            "TC4281_3_allowed_escape_hatches",
            "Only exact cancellation, theorem-level projection, or explicit conserved nonlocal quarantine can remove the shell residual.",
            "132 transition shell route classification",
            "EXACT_THEOREM_OR_PROFILE_REQUIRED",
        ),
    ]
    return [
        {
            **common(),
            "countercase_id": countercase_id,
            "countercase": countercase,
            "source_basis": source_basis,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for countercase_id, countercase, source_basis, status in raw
    ]


def profile_schema_rows() -> List[Dict[str, str]]:
    raw = [
        ("PS4281_0_Rtransport", "R_transport_to_local", "dimensionless_or_AJ_units", "P_W P_loc transport profile over compact local collar", "MISSING_REAL_PROFILE"),
        ("PS4281_1_RBgrad", "R_Bgrad_to_local", "dimensionless_or_AJ_units", "P_W P_loc B-gradient/transition profile over compact local collar", "MISSING_REAL_PROFILE"),
        ("PS4281_2_Tres_tauL", "T_res/tau_L", "s^-1 or normalized private units", "relaxation-time conversion for AJ budget", "MISSING_PARENT_NORMALIZATION"),
        ("PS4281_3_cGamma", "c_Gamma", "model coefficient", "finite product-bound coefficient, not inferred from bound alone", "MISSING_PARENT_COEFFICIENT"),
        ("PS4281_4_transition_profile", "transition_shell_profile", "arena response units", "Solar/vacuum transition-shell source projection if not exactly canceled", "MISSING_ARENA_PROJECTION"),
    ]
    return [
        {
            **common(),
            "schema_id": schema_id,
            "quantity": quantity,
            "required_units": units,
            "required_source_row": source_row,
            "status": status,
            "source_path": "MISSING_SOURCE_PATH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for schema_id, quantity, units, source_row, status in raw
    ]


def aj_profile_bound_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "AJB4281_0_zero_collar",
            "finite_margin_local_collar",
            "R_transport_to_local=0 and R_Bgrad_to_local=0",
            "A_J,eff_private=0",
            "passes only inside support-separated compact local collar",
            "CONDITIONAL_ZERO_BRANCH",
        ),
        (
            "AJB4281_1_transition_shell",
            "transition_shell",
            "R_transport_to_local or R_Bgrad_to_local may be nonzero",
            f"|R_transport_to_local|+|R_Bgrad_to_local| <= {AJ_STRONG_WINDOW}",
            "not scoreable until real profile rows exist",
            "PROFILE_REQUIRED",
        ),
        (
            "AJB4281_2_PiB_budget",
            "transition_or_partial_PiB_branch",
            "nonzero B-gradient support",
            f"|R_transport_to_local|+|R_Bgrad_to_local| <= {AJ_PIB_WINDOW}",
            "not scoreable until c_Gamma, T_res/tau_L and profile units are sourced",
            "PROFILE_REQUIRED",
        ),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "arena": arena,
            "residual_condition": residual_condition,
            "bound_or_consequence": bound,
            "meaning": meaning,
            "status": status,
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, arena, residual_condition, bound, meaning, status in raw
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4281_0",
            "selected_route": "FINITE_MARGIN_LOCAL_ZERO_PLUS_TRANSITION_PROFILE_OR_THEOREM",
            "meaning": "Local compact collars away from transition support get exact residual zero; transition shells remain live and must be canceled/quarantined by theorem or profiled numerically.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4281_0", "Do not extend finite-margin collar zero across transition shell."),
        ("FW4281_1", "Do not route Solar/vacuum transition shells into galaxy or cosmology when P_loc=1."),
        ("FW4281_2", "Do not treat MISSING_REAL_PROFILE or MISSING_PARENT_COEFFICIENT rows as zero."),
        ("FW4281_3", "Do not claim local GR globally until transition-shell cancellation/projector/conservation ownership closes."),
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
            "status_id": "STATUS4281_0",
            "status": "LOCAL_COLLAR_BRANCH_IMPROVED_TRANSITION_SHELL_STILL_OPEN",
            "summary": "4281 closes transport/Bgrad residuals only where support separation is true; transition shell is the remaining local danger.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NEXT4281_0",
            "target_file": NEXT_TARGET,
            "task": "Derive exact transition-shell cancellation/projector/conservation ownership, or fill real profile source rows for finite transition residual bounds.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 297 cGamma Transport/Bgrad Routing Zero Or Profile Source Pack

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4281 gives a real but restricted zero theorem.

From 4280 the live private cGamma AJ gate is:

```text
A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|.
```

Define a compact local test collar `W_loc` and write schematically:

```text
R_transport_to_local[W_loc] =
  || P_W P_loc T_transport ||

R_Bgrad_to_local[W_loc] =
  || P_W P_loc C_B grad(B_env, Pi_B, L_cg) ||.
```

If:

```text
W_loc cap supp(T_transport) = empty,
W_loc cap supp(grad B_env, grad Pi_B, grad L_cg, I_Bgrad) = empty,
P_W is support-respecting,
boundary flux through partial W_loc is zero,
```

then:

```text
R_transport_to_local[W_loc] = 0,
R_Bgrad_to_local[W_loc] = 0,
```

and, using the 4280 import `A_src=0`:

```text
A_J,eff_private[W_loc] = 0.
```

This is the finite-margin local-collar branch. It is an honest support theorem, not a fitted switch.

## Why This Does Not Close The Transition Shell

The Solar/vacuum transition countercase remains live:

```text
Pi_B ~= 1/2,
T_gal = 0,
P_loc = 1,
P_gal = 0,
P_cos = 0.
```

So a Solar transition shell cannot be hidden in the galaxy or cosmology branch.

The old transition-shell gates also say:

```text
bare direct local projection fails,
U_B^2 transition suppression fails,
coefficient tuning is forbidden.
```

Therefore the finite-margin zero theorem cannot be extended through the transition shell unless a new parent theorem supplies exact cancellation, projector silence, or explicit conserved nonlocal quarantine.

## Live Profile Route

If a local collar intersects transition support, use:

```text
|R_transport_to_local| + |R_Bgrad_to_local|
<= {AJ_STRONG_WINDOW}
```

or:

```text
|R_transport_to_local| + |R_Bgrad_to_local|
<= {AJ_PIB_WINDOW}.
```

But those rows are not scoreable until real values and source paths exist for:

```text
R_transport_to_local,
R_Bgrad_to_local,
T_res/tau_L,
c_Gamma,
transition_shell_profile.
```

## Interpretation

This improves the local-GR route:

```text
ordinary compact local tests away from transition support can use exact residual zero;
transition shells remain the real enemy.
```

No public local-GR claim is made.

## Next Target

`{NEXT_TARGET}` must either derive exact transition-shell cancellation/projector/conservation ownership, or fill real source-backed profile rows.
"""


def checkpoint_doc() -> str:
    return f"""
# 4281 - cGamma transport/Bgrad routing zero or profile source pack

Marker: `{MARKER}`

Decision: `{DECISION}`

4281 proves a restricted support-zero branch:

```text
finite-margin W_loc away from transport/B-gradient support
=> R_transport_to_local = R_Bgrad_to_local = 0
=> A_J,eff_private = 0.
```

It also blocks the overclaim:

```text
transition shell has P_loc=1 and fails direct local projection,
so transition support still needs exact cancellation/quarantine or real profile rows.
```
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorem = csv_rows(paths["zero_theorem"])
    countercases = csv_rows(paths["countercases"])
    profile_schema = csv_rows(paths["profile_schema"])
    aj_bounds = csv_rows(paths["aj_bounds"])
    generated_rows: Iterable[Dict[str, str]] = (
        sources
        + theorem
        + countercases
        + profile_schema
        + aj_bounds
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4281_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4281_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4281_2_finite_margin_zero",
            any(row["status"] == "FINITE_MARGIN_LOCAL_COLLAR_ZERO_DERIVED" for row in theorem),
            "finite-margin local collar zero theorem emitted",
        ),
        (
            "VAL4281_3_AJ_zero_consequence",
            any(row["status"] == "AJ_ZERO_ON_RESTRICTED_LOCAL_COLLAR" for row in theorem),
            "AJ zero consequence emitted for restricted collar",
        ),
        (
            "VAL4281_4_transition_countercase",
            any(row["status"] == "BLOCKS_GLOBAL_ZERO_CLAIM" for row in countercases),
            "transition shell countercase blocks global zero",
        ),
        (
            "VAL4281_5_profile_schema",
            {"R_transport_to_local", "R_Bgrad_to_local", "T_res/tau_L", "c_Gamma"}.issubset({row["quantity"] for row in profile_schema}),
            "profile source schema includes required live quantities",
        ),
        (
            "VAL4281_6_bound_rows",
            any(row["status"] == "CONDITIONAL_ZERO_BRANCH" for row in aj_bounds)
            and any(row["status"] == "PROFILE_REQUIRED" for row in aj_bounds),
            "AJ zero and finite profile branches represented",
        ),
        ("VAL4281_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4281_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4281_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        (
            "VAL4281_10_no_claim_rows",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in generated_rows),
            "all generated rows remain nonclaim",
        ),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4281_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4281_SOURCE_REGISTER.csv",
        "zero_theorem": SOURCE_DIR / "P8_Y5_R2FR_4281_ROUTING_ZERO_THEOREM.csv",
        "countercases": SOURCE_DIR / "P8_Y5_R2FR_4281_TRANSITION_SHELL_COUNTERCASE.csv",
        "profile_schema": SOURCE_DIR / "P8_Y5_R2FR_4281_PROFILE_SOURCE_SCHEMA.csv",
        "aj_bounds": SOURCE_DIR / "P8_Y5_R2FR_4281_AJ_PROFILE_BOUND_ROWS.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4281_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4281_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4281_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4281_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["zero_theorem"], zero_theorem_rows())
    write_csv(paths["countercases"], countercase_rows())
    write_csv(paths["profile_schema"], profile_schema_rows())
    write_csv(paths["aj_bounds"], aj_profile_bound_rows())
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
        "PPC4161 4281 finite-margin local cGamma zero",
        "4281 proves a restricted support-zero branch for cGamma transport/B-gradient residuals on compact local collars away from transition support. It also blocks the dangerous global overclaim: Solar/vacuum transition shells have `P_loc=1` and still require exact cancellation, theorem-level projection, explicit conserved quarantine, or real profile rows.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4281 packet cGamma transport/Bgrad gate",
        "Packet update: finite-margin local collars can set `R_transport_to_local=R_Bgrad_to_local=0` by support separation, but transition shells remain live profile/theorem obligations. No public local-GR claim is made.",
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
