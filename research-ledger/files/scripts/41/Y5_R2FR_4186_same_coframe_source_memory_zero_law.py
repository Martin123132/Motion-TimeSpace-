from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4186"
BRANCH_ID = "MTS_R2FR_Y5_SAME_COFRAME_SOURCE_MEMORY_ZERO_LAW_4186"
DECISION = (
    "JOINT_ZERO_LAW_CONDITIONAL_cD_AND_deltaKappa_PRIVATE_ZERO_"
    "cGamma_MEMORY_SUPPORT_OPEN_BOUND_RUNNER_STAGED_NONCLAIM"
)
DOC_PATH = POST / "4186-Y5-R2FR-same-coframe-source-memory-zero-law-for-cD-deltaKappa-cGamma-or-bound-runner.md"
FORMAL_202_PATH = FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-027"
SPINE_MARKER = "PPC4161_SAME_COFRAME_SOURCE_MEMORY_ZERO_LAW_4186"
PACKET_MARKER = "PPC4161_PACKET_SAME_COFRAME_SOURCE_MEMORY_ZERO_LAW_4186"
NEXT_TARGET = "4187-Y5-R2FR-local-memory-support-projector-zero-law-for-cGamma-or-PPN-clock-bound.md"

SOURCES = {
    "SRC4186_00_4185_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4185_NEXT_TARGET.csv",
        "derive parent functor/source-memory zero law",
        "4185 handoff to c_D/delta_kappa/c_Gamma zero law.",
    ),
    "SRC4186_01_formal_201": (
        FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md",
        "`c_D` because same-coframe failure",
        "4185 coefficient priority map.",
    ),
    "SRC4186_02_hilbert_source": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "All ordinary local source sectors use the same observed metric/coframe",
        "single coframe/source-measure descent clause.",
    ),
    "SRC4186_03_kappa_lock": (
        FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md",
        "D_A ln kappa_* = 0",
        "topological kappa-lock inside private packet.",
    ),
    "SRC4186_04_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "same-Hodge EM/Poynting source-owner theorem.",
    ),
    "SRC4186_05_quotient": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "Vertical Silence Proof",
        "quotient naturality and vertical representative silence.",
    ),
    "SRC4186_06_memory_redteam": (
        FORMAL / "06-consistency-red-team.md",
        "source_support_boundary_law_conditional_open",
        "memory support/screening warning: local memory silence remains open.",
    ),
    "SRC4186_07_palatini_selector": (
        FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md",
        "local memory couplings -> coefficient `c_Gamma`",
        "4184 residual classification.",
    ),
    "SRC4186_08_burden_map": (
        FORMAL / "195-PPC4161-local-GR-private-closure-summary-and-parent-adoption-burden-map.md",
        "Any unsigned clause stays closure-only",
        "public-claim policy for unsigned clauses.",
    ),
    "SRC4186_09_claim_L026": (
        CLAIMS_PATH,
        "residual_coefficient_map_nonclaim_parent_zero_or_numeric_bounds_missing_public_claim_false",
        "latest claim row before joint zero-law gate.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, required_text, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": required_text,
                "required_text_found": str(required_text in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def joint_zero_law_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "JZ4186_0_same_coframe",
            "single observed coframe/source functor",
            "S_matter, S_EM and binding terms use g_obs and the same Hilbert measure; no second Hodge/metric owner",
            "c_D=0",
            "private_selector_zero",
            "global parent adoption still open",
        ),
        (
            "JZ4186_1_poynting_owner",
            "Maxwell-Hodge owner",
            "Poynting flux is T_EM^0i of the Hilbert stress, not a separate background field",
            "c_D_EM_side_channel=0",
            "private_selector_zero",
            "depends on same coframe and boundary routing",
        ),
        (
            "JZ4186_2_kappa_lock",
            "topological kappa lock",
            "d ln(kappa_*)=0 in the private packet and the sector is source-blind",
            "D_A ln kappa_*=0",
            "private_selector_zero",
            "numeric value of G remains calibrated",
        ),
        (
            "JZ4186_3_source_measure",
            "Hilbert source-measure descent",
            "T_parent^H=Z_0 T_H, T_leak=0, delta_ZH=0, D_A delta_ZH=0",
            "delta_kappa=0",
            "private_selector_zero",
            "global ordinary-source functor adoption still open",
        ),
        (
            "JZ4186_4_quotient_silence",
            "quotient naturality",
            "ordinary matter, EM, clocks, rods, constants and source normalizations factor through q",
            "representative/source marker drift=0",
            "private_selector_zero",
            "requires q-owned local observable functor",
        ),
        (
            "JZ4186_5_memory_support",
            "local memory support/projector silence",
            "Gamma_mem contributes no compact-local bulk invariant except screened/routed/vertical pieces",
            "c_Gamma=0 if parent-signed",
            "conditional_not_currently_parent_derived",
            "memory support/locality theorem remains missing",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "zero_law_statement": statement,
            "coefficient_consequence": consequence,
            "status": status,
            "remaining_debt": debt,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, statement, consequence, status, debt in rows
    ]


def coefficient_verdict_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "CV4186_0_cD",
            "c_D",
            "same-coframe/disformal leak",
            "zero inside PPC4161 private selector",
            "closed_private_not_public",
            "global parent same-coframe functor",
            "WEP/clock/EM bound if same-coframe rejected",
        ),
        (
            "CV4186_1_deltaKappa",
            "delta_kappa",
            "source-coupling drift",
            "zero inside PPC4161-TK-H private selector",
            "closed_private_not_public_numeric_G_unpredicted",
            "global topological kappa plus Hilbert source-measure adoption",
            "LLR/orbital/clock measured-G envelope if finite",
        ),
        (
            "CV4186_2_cGamma",
            "c_Gamma",
            "local memory hair",
            "not zero from existing same-coframe/source laws",
            "open_parent_memory_support_debt",
            "local memory support/projector zero theorem",
            "PPN/clock/orbital/R10 bound rows if finite",
        ),
    ]
    return [
        {
            **common(),
            "verdict_id": verdict_id,
            "coefficient": coefficient,
            "residual": residual,
            "zero_law_verdict": verdict,
            "status": status,
            "next_derivation": next_derivation,
            "fallback_bound": fallback,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for verdict_id, coefficient, residual, verdict, status, next_derivation, fallback in rows
    ]


def memory_blocker_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "MB4186_0_not_source_weight",
            "c_Gamma is not a source-measure multiplier",
            "Hilbert source descent closes delta_ZH/source weights but does not automatically remove memory-curvature invariants",
            "open",
        ),
        (
            "MB4186_1_not_second_metric",
            "c_Gamma is not the same as c_D",
            "same-coframe forbids second metric/Hodge owners but memory can still multiply scalar/tensor invariants of the same metric",
            "open",
        ),
        (
            "MB4186_2_support",
            "local support law missing",
            "Need Gamma_mem compact-local support to vanish, become vertical, or be screened below local-test projection",
            "primary_blocker",
        ),
        (
            "MB4186_3_boundary",
            "memory boundary/routing law missing",
            "Need memory flux/radiative/transition pieces routed as boundary charges, not hidden bulk sources",
            "open",
        ),
        (
            "MB4186_4_projection",
            "observable projection missing",
            "Need J_PPN/J_clock/J_orbital/J_R10 projection for finite c_Gamma if zero theorem fails",
            "fallback_required",
        ),
    ]
    return [
        {
            **common(),
            "blocker_id": blocker_id,
            "blocker": blocker,
            "why_it_blocks_cGamma_zero": why,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for blocker_id, blocker, why, status in rows
    ]


def bound_runner_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "BR4186_0_cD_WEP_clock_EM",
            "c_D",
            "WEP;clock;EM_propagation;Poynting",
            "finite same-coframe leak coefficient and projection Jacobian",
            "only needed if same-coframe parent functor is rejected",
            "nonclaim_template_ready",
        ),
        (
            "BR4186_1_deltaKappa_orbital_clock",
            "delta_kappa",
            "orbital;LLR_Gdot;clock;local_G",
            "finite kappa/source-measure drift function and units",
            "only needed if kappa/source lock is rejected globally",
            "nonclaim_template_ready",
        ),
        (
            "BR4186_2_cGamma_PPN_clock",
            "c_Gamma",
            "PPN;clock;orbital;R10",
            "finite memory coupling, local profile/support law, projection Jacobians",
            "needed unless c_Gamma zero theorem closes",
            "active_next_bound_or_zero_target",
        ),
    ]
    return [
        {
            **common(),
            "runner_id": runner_id,
            "coefficient": coefficient,
            "arenas": arenas,
            "required_inputs": inputs,
            "when_to_use": when_to_use,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for runner_id, coefficient, arenas, inputs, when_to_use, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "joint_zero_law_written": "True",
            "c_D_private_zero": "True",
            "delta_kappa_private_zero": "True",
            "c_Gamma_parent_zero": "False",
            "c_Gamma_bound_runner_staged": "True",
            "global_parent_claim_allowed": "False",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "recommended_next_route": "cGamma_local_memory_support_projector_zero_or_bound",
            "meaning": (
                "The same-coframe and source-coupling pieces close inside the private selector. "
                "The remaining root residual is c_Gamma: local memory support/projector silence is still not parent-derived."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "FW4186_0_private",
            "c_D and delta_kappa are globally solved.",
            "They are zero only inside the private selector until global parent adoption closes.",
        ),
        (
            "FW4186_1_cGamma",
            "c_Gamma is zero because c_D and delta_kappa are zero.",
            "c_Gamma needs its own local memory support/projector theorem or finite bound.",
        ),
        (
            "FW4186_2_G",
            "The numerical value of G is predicted.",
            "The source-coupling law remains structural; numeric G remains calibrated.",
        ),
        (
            "FW4186_3_tests",
            "Bound-runner templates are empirical passes.",
            "They are nonclaim scaffolds until coefficients, units, source paths and projections are filled.",
        ),
        (
            "FW4186_4_public_GR",
            "MTS has public local GR.",
            "Public local-GR claim remains false until global adoption and c_Gamma/residual gates close.",
        ),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_language": forbidden,
            "safe_language": safe,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, safe in rows
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "result": DECISION,
            "source_sweep_complete": "True",
            "joint_zero_law_written": "True",
            "c_D_private_zero": "True",
            "delta_kappa_private_zero": "True",
            "c_Gamma_parent_zero": "False",
            "c_Gamma_bound_runner_staged": "True",
            "global_parent_claim_allowed": "False",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "formal_202_written": "True",
            "claim_register_action": claim_action,
            "packet_180_action": packet_action,
            "spine_action": spine_action,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": (
                "4186 closes the same-coframe/source-coupling roots privately but shows c_Gamma is not killed by those laws. "
                "The next gate must derive local memory support/projector zero directly or build finite PPN/clock/orbital/R10 bound rows."
            ),
            "route_A": "derive local memory support/projector zero: Gamma_mem has no compact-local bulk projection or is vertical/routed/screened",
            "route_B": "if finite c_Gamma remains, build PPN/clock/orbital/R10 projection rows with units, source paths and no-cancellation guards",
            "public_claim_policy": "no public local-GR claim while c_Gamma remains parent-open",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    names = [
        "P8_Y5_R2FR_4186_SOURCE_REGISTER",
        "P8_Y5_R2FR_4186_JOINT_ZERO_LAW_CLAUSES",
        "P8_Y5_R2FR_4186_COEFFICIENT_VERDICT_MAP",
        "P8_Y5_R2FR_4186_CGAMMA_MEMORY_BLOCKER_LEDGER",
        "P8_Y5_R2FR_4186_BOUND_RUNNER_INTERFACE",
        "P8_Y5_R2FR_4186_BRANCH_DECISION",
        "P8_Y5_R2FR_4186_CLAIM_FIREWALL",
        "P8_Y5_R2FR_4186_STATUS",
        "P8_Y5_R2FR_4186_NEXT_TARGET",
    ]
    return {name: SOURCE_DIR / f"{name}.csv" for name in names}


def write_formal_202() -> None:
    text = f"""# 202 - PPC4161 Same-Coframe Source-Memory Zero Law

Marker: `{SPINE_MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint fuses the same-coframe, Hilbert-source, kappa-lock, quotient, and memory-support clauses into a joint zero-law audit. It does not claim public local GR.

## Joint Zero Law

Inside the private PPC4161 selector:

```text
single observed coframe + Hilbert source descent + Maxwell-Hodge owner
=> c_D = 0.
```

Also:

```text
topological kappa lock + Hilbert source-measure descent
=> D_A ln kappa_* = 0, delta_ZH = 0, D_A delta_ZH = 0
=> delta_kappa = 0.
```

These are private-selector zeros, not global parent-action adoption.

## Memory Hair

The same laws do not automatically kill local memory couplings:

```text
c_Gamma * Gamma_mem * I_local[g_obs, R, T, source]
```

can still be same-coframe and source-normalized while changing local equations. Therefore:

```text
c_Gamma_parent_zero = false
```

unless a separate local memory support/projector theorem proves that `Gamma_mem` is vertical, absent, screened, compact-support silent, or boundary-routed in compact local collars.

## Verdict

```text
c_D_private_zero = true
delta_kappa_private_zero = true
c_Gamma_parent_zero = false
c_Gamma_bound_runner_staged = true
public_local_GR_claim_allowed = false
```

## Next Target

`{NEXT_TARGET}`
"""
    FORMAL_202_PATH.write_text(text, encoding="utf-8")


def write_doc() -> None:
    text = f"""# 4186 - Y5 R2FR Same-Coframe Source-Memory Zero Law For cD/deltaKappa/cGamma Or Bound Runner

Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Result

4186 gives a clean split:

```text
c_D = 0 inside the private same-coframe/Hilbert/Maxwell-Hodge selector.
delta_kappa = 0 inside the private topological-kappa plus Hilbert-source selector.
c_Gamma is not zero from those laws.
```

That means the next real blocker is narrower and sharper: local memory hair.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return "already_present"
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gravity",
            "claim": (
                "The private same-coframe/source-coupling zero law closes c_D and delta_kappa inside PPC4161, "
                "but c_Gamma remains open because local memory support/projector silence is not parent-derived"
            ),
            "current_evidence": (
                "formalization-workbench/202-PPC4161-same-coframe-source-memory-zero-law.md records the same-coframe/Hilbert/Maxwell-Hodge zero for c_D, "
                "topological-kappa plus Hilbert-source zero for delta_kappa, c_Gamma memory blocker ledger, bound-runner interface, and public-claim firewall"
            ),
            "status": "private_cD_deltaKappa_zero_law_nonclaim_cGamma_open_bound_runner_staged_public_claim_false",
            "next_test": "Derive local memory support/projector zero for c_Gamma or build PPN/clock/orbital/R10 bound rows with projection inputs",
            "key_risk": (
                "A same-coframe source-normalized memory coupling can still change local equations; "
                "c_Gamma needs its own zero theorem or finite bound"
            ),
        }
    )
    write_csv(CLAIMS_PATH, rows)
    return "added"


def ensure_packet_180_addendum() -> str:
    text = read_text(PACKET_180_PATH)
    if PACKET_MARKER in text:
        return "already_present"
    addendum = f"""

## Post-Checkpoint 4186 Same-Coframe Source-Memory Zero Law

Marker: `{PACKET_MARKER}`

`post-checkpoint-work/4186-Y5-R2FR-same-coframe-source-memory-zero-law-for-cD-deltaKappa-cGamma-or-bound-runner.md` closes two of the three root residuals inside the private selector:

```text
c_D_private_zero = true
delta_kappa_private_zero = true
c_Gamma_parent_zero = false
```

The remaining root residual is now specifically local memory support/projector silence.
"""
    PACKET_180_PATH.write_text(text.rstrip() + addendum, encoding="utf-8")
    return "added"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161 Same-Coframe Source-Memory Zero Law

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4186 shows that the private selector closes `c_D` and `delta_kappa`, but not `c_Gamma`. The remaining local-GR root blocker is now sharply localized: derive local memory support/projector silence, or build finite `c_Gamma` PPN/clock/orbital/R10 bound rows.

Next target:

`{NEXT_TARGET}`
"""
    SPINE_PATH.write_text(text.rstrip() + section, encoding="utf-8")
    return "added"


def validation_rows(
    rows_by_name: Dict[str, List[Dict[str, str]]],
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    paths = output_paths()
    source_ok = all(
        row["exists"] == "True" and row["required_text_found"] == "True"
        for row in rows_by_name["P8_Y5_R2FR_4186_SOURCE_REGISTER"]
    )
    decision = rows_by_name["P8_Y5_R2FR_4186_BRANCH_DECISION"][0]
    status = rows_by_name["P8_Y5_R2FR_4186_STATUS"][0]
    all_generated_rows = [
        row
        for rows in rows_by_name.values()
        for row in rows
    ]
    bad_claim_rows = [
        row
        for row in all_generated_rows
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]
    checks = [
        ("VAL4186_0_sources", "all cited sources exist and contain required text", source_ok, ""),
        ("VAL4186_1_joint_law", "joint zero-law clauses include memory support", any(row["clause_id"] == "JZ4186_5_memory_support" for row in rows_by_name["P8_Y5_R2FR_4186_JOINT_ZERO_LAW_CLAUSES"]), ""),
        ("VAL4186_2_cD", "c_D private zero is recorded", decision["c_D_private_zero"] == "True", str(decision)),
        ("VAL4186_3_deltaKappa", "delta_kappa private zero is recorded", decision["delta_kappa_private_zero"] == "True", str(decision)),
        ("VAL4186_4_cGamma_open", "c_Gamma remains parent-open", decision["c_Gamma_parent_zero"] == "False", str(decision)),
        ("VAL4186_5_bound_runner", "c_Gamma bound runner is staged", any(row["coefficient"] == "c_Gamma" and row["status"] == "active_next_bound_or_zero_target" for row in rows_by_name["P8_Y5_R2FR_4186_BOUND_RUNNER_INTERFACE"]), ""),
        ("VAL4186_6_memory_blocker", "memory blocker ledger marks primary blocker", any(row["status"] == "primary_blocker" for row in rows_by_name["P8_Y5_R2FR_4186_CGAMMA_MEMORY_BLOCKER_LEDGER"]), ""),
        ("VAL4186_7_public_claim", "public local-GR claim remains false", status["public_local_GR_claim_allowed"] == "False", str(status)),
        ("VAL4186_8_numeric_G", "numeric G remains unpredicted", status["numeric_G_predicted"] == "False", str(status)),
        ("VAL4186_9_formal_202", "formal 202 exists and has marker", FORMAL_202_PATH.exists() and SPINE_MARKER in read_text(FORMAL_202_PATH), str(FORMAL_202_PATH)),
        ("VAL4186_10_doc", "4186 doc exists and has decision", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4186_11_claim_row", "claim register contains L-027", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4186_12_packet_180", "packet 180 addendum marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4186_13_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4186_14_next", "next target recorded", rows_by_name["P8_Y5_R2FR_4186_NEXT_TARGET"][0]["next_target"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4186_15_output_paths", "all declared output CSVs exist", all(path.exists() for path in paths.values()), str(paths)),
        ("VAL4186_16_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
    ]
    validation = [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
            "details": details,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, description, passed, details in checks
    ]
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation.append(
        {
            **common(),
            "check_id": "VAL4186_17_compile",
            "description": "generator compiles and pycache is removed",
            "passed": "True",
            "details": "compiled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    write_formal_202()
    write_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name = {
        "P8_Y5_R2FR_4186_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4186_JOINT_ZERO_LAW_CLAUSES": joint_zero_law_rows(),
        "P8_Y5_R2FR_4186_COEFFICIENT_VERDICT_MAP": coefficient_verdict_rows(),
        "P8_Y5_R2FR_4186_CGAMMA_MEMORY_BLOCKER_LEDGER": memory_blocker_rows(),
        "P8_Y5_R2FR_4186_BOUND_RUNNER_INTERFACE": bound_runner_rows(),
        "P8_Y5_R2FR_4186_BRANCH_DECISION": decision_rows(),
        "P8_Y5_R2FR_4186_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4186_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4186_NEXT_TARGET": next_rows(),
    }

    for name, path in output_paths().items():
        write_csv(path, rows_by_name[name])

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4186_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4186 validation failed: {failed}")

    print(f"{CHECKPOINT} generated")
    print(f"doc={DOC_PATH}")
    print(f"formal={FORMAL_202_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
