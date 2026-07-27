from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4233"
CLAIM_ID = "L-074"
BRANCH = "MTS_R2FR_Y5_CGAMMA_KPERP_TWO_SURVIVOR_4233"
DECISION = "TWO_SURVIVOR_SHARED_BUDGET_LAW_DERIVED_CGAMMA_KPERP_BOTH_UNSCORED_KPERP_IDENTITY_NEXT"
MARKER = "PPC4161_CGAMMA_KPERP_TWO_SURVIVOR_SHARED_BUDGET_4233"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_KPERP_TWO_SURVIVOR_SHARED_BUDGET_4233"
NEXT_TARGET = "4234-Y5-R2FR-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md"

FORMAL_PATH = FORMAL / "249-PPC4161-cGamma-Kperp-two-survivor-zero-proof-or-bound-runner.md"
DOC_PATH = POST / "4233-Y5-R2FR-cGamma-Kperp-two-survivor-zero-proof-or-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4233_VALIDATION.csv"
BOUND_TABLE = SOURCE_DIR / "P8_Y5_R2FR_4173_SOURCE_BACKED_BOUND_TABLE.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4233_00_4232_next": SourceSpec(
        "SRC4233_00_4232_next",
        SOURCE_DIR / "P8_Y5_R2FR_4232_NEXT_TARGET.csv",
        "4233-Y5-R2FR-cGamma-Kperp-two-survivor-zero-proof-or-bound-runner.md",
        "4232 selected the cGamma/Kperp two-survivor target.",
    ),
    "SRC4233_01_4232_vector": SourceSpec(
        "SRC4233_01_4232_vector",
        SOURCE_DIR / "P8_Y5_R2FR_4232_NON_EH_VECTOR.csv",
        "c_T / Kperp",
        "4232 non-EH vector rows identify the two local survivors.",
    ),
    "SRC4233_02_cgamma_bound": SourceSpec(
        "SRC4233_02_cgamma_bound",
        FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md",
        "|C_Gamma,a| <= B_a.",
        "Finite cGamma product-bound law.",
    ),
    "SRC4233_03_cgamma_profile": SourceSpec(
        "SRC4233_03_cgamma_profile",
        FORMAL / "205-PPC4161-cGamma-profile-projection-coefficient-gate.md",
        "C_Gamma_Gdot = c_Gamma D_t Xi_0",
        "cGamma profile split into Gdot/xi/channel rows.",
    ),
    "SRC4233_04_cgamma_stationarity": SourceSpec(
        "SRC4233_04_cgamma_stationarity",
        FORMAL / "206-PPC4161-local-memory-stationarity-gradient-zero-gate.md",
        "D_t Xi_0 = 0,",
        "Exact stationarity/homogeneity target for cGamma.",
    ),
    "SRC4233_05_cgamma_amplitude": SourceSpec(
        "SRC4233_05_cgamma_amplitude",
        FORMAL / "214-PPC4161-parent-amplitude-owner-for-Jres.md",
        "|c_Gamma| <= base_multiplier",
        "cGamma ceiling and amplitude-owner map.",
    ),
    "SRC4233_06_source_operator": SourceSpec(
        "SRC4233_06_source_operator",
        FORMAL / "215-PPC4161-source-operator-amplitude-AJ-bound.md",
        "K_perp=0 or PPN-bounded.",
        "Source-operator amplitude bound links the scalar route back to Kperp.",
    ),
    "SRC4233_07_Kperp_zero": SourceSpec(
        "SRC4233_07_Kperp_zero",
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "K_perp = 0.",
        "Kperp conditional zero theorem.",
    ),
    "SRC4233_08_Kperp_vector": SourceSpec(
        "SRC4233_08_Kperp_vector",
        FORMAL / "217-PPC4161-Kperp-finite-coefficient-vector.md",
        "|W_i^K| C_T (|S_T|+|B_T|+|I_T|+|Z_T|) <= bound_i.",
        "Finite Kperp coefficient vector.",
    ),
    "SRC4233_09_Kperp_denominator": SourceSpec(
        "SRC4233_09_Kperp_denominator",
        FORMAL / "218-PPC4161-parent-tensor-operator-LT-coercivity.md",
        "c_T = Z_T lambda_D + M_T^2",
        "Tensor denominator formula via packet shorthand.",
    ),
    "SRC4233_10_Kperp_no_pole": SourceSpec(
        "SRC4233_10_Kperp_no_pole",
        FORMAL / "219-PPC4161-no-physical-Kperp-pole-theorem.md",
        "K_perp = 0",
        "No-extra-pole theorem shape.",
    ),
    "SRC4233_11_Kperp_sector": SourceSpec(
        "SRC4233_11_Kperp_sector",
        FORMAL / "220-PPC4161-Kperp-sector-placement-theorem.md",
        "K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source.",
        "Kperp sector placement/no-double-count rule.",
    ),
    "SRC4233_12_EH_coframe": SourceSpec(
        "SRC4233_12_EH_coframe",
        FORMAL / "221-PPC4161-EH-coframe-parent-signature-or-Kperp-score.md",
        "R_i^K <= |W_i^K| N_T / D_T",
        "EH/coframe identity fork and Kperp score function.",
    ),
    "SRC4233_13_bounds": SourceSpec(
        "SRC4233_13_bounds",
        BOUND_TABLE,
        "alpha3",
        "Source-backed local empirical bound table from 4173.",
    ),
}


def common() -> Dict[str, str]:
    return {"timestamp_utc": STAMP, "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def bound_rows_for_runner() -> List[Dict[str, str]]:
    wanted = {
        "gamma_minus_1",
        "beta_minus_1",
        "xi",
        "alpha1",
        "alpha2",
        "alpha3",
        "zeta3",
        "Gdot_over_G",
        "alpha_Yukawa_at_lambda_38p6um",
        "eta_TiPt",
        "redshift_violation_alpha",
        "((2+2gamma-beta)/3)-1",
    }
    rows: List[Dict[str, str]] = []
    for row in csv_rows(BOUND_TABLE):
        if row["observable"] not in wanted:
            continue
        bound = row["allowed_abs_bound"]
        try:
            half_bound = f"{float(bound) / 2:.16g}"
            numeric = "True"
        except ValueError:
            half_bound = ""
            numeric = "False"
        full_curve = row["full_curve_available"]
        claim_grade = "False" if row["observable"] == "alpha_Yukawa_at_lambda_38p6um" else row["source_backed"]
        rows.append(
            {
                **common(),
                "arena_bound_id": f"TB4233_{row['bound_id']}",
                "arena": row["arena"],
                "observable": row["observable"],
                "source_allowed_abs_bound": bound,
                "units": row["units"],
                "split_budget_each_active_channel": half_bound,
                "split_rule": "if both cGamma and Kperp survive and no orthogonality theorem is parent-signed, each gets at most half the arena budget",
                "cGamma_condition": "|c_Gamma profile_Gamma,a| <= split_budget",
                "Kperp_condition": "|W_i^K| N_T / D_T <= split_budget",
                "scoreable_now": "False",
                "missing_cGamma_input": "profile_Gamma,a or zero theorem",
                "missing_Kperp_input": "W_i^K, N_T, D_T or EH/coframe no-extra-pole theorem",
                "numeric_bound_available": numeric,
                "full_curve_available": full_curve,
                "claim_allowed": "False",
                "valid_for_claim": "False" if claim_grade == "False" else "False",
            }
        )
    return rows


def zero_contract_rows() -> List[Dict[str, str]]:
    rows = [
        {
            "contract_id": "ZC4233_0_cGamma_zero",
            "channel": "cGamma",
            "zero_formula": "D_t Xi_0=0, grad_perp Xi_0=0 and no surviving Gamma_mem tensor/profile projection",
            "current_status": "not_parent_signed",
            "if_true": "cGamma consumes zero local empirical budget",
            "if_false": "cGamma must satisfy split-budget product rows",
        },
        {
            "contract_id": "ZC4233_1_Kperp_zero",
            "channel": "Kperp",
            "zero_formula": "Kperp is EH TT/gauge/vertical/boundary radiation only; no independent MTS tensor source projects onto local PPN",
            "current_status": "not_parent_signed",
            "if_true": "Kperp consumes zero local empirical budget and cGamma can be scored alone",
            "if_false": "Kperp must satisfy split-budget tensor rows",
        },
        {
            "contract_id": "ZC4233_2_orthogonality",
            "channel": "joint",
            "zero_formula": "parent action proves cGamma and Kperp project to orthogonal observables or one channel is identically zero before data",
            "current_status": "not_parent_signed",
            "if_true": "surviving channel may use the full arena budget",
            "if_false": "half-budget no-cancellation rule applies",
        },
    ]
    return [{**common(), **row, "claim_allowed": "False", "valid_for_claim": "False"} for row in rows]


def guard_rows() -> List[Dict[str, str]]:
    rows = [
        ("NC4233_0_no_cancellation", "Do not score C_Gamma,a + R_i^K by allowing opposite signs to cancel unless the parent action proves a sign/orthogonality identity before fitting."),
        ("NC4233_1_half_budget", "With both channels alive, use half-budget rows for each active channel in every shared arena."),
        ("NC4233_2_R10_anchor", "The R10 row remains anchor-only because alpha(lambda) is not a full curve; it can test schema but not claim a short-range pass."),
        ("NC4233_3_alpha3_pressure", "The alpha3 row is the harshest local guard: half-budget is 2e-20 dimensionless if both channels survive."),
        ("NC4233_4_Kperp_priority", "Kperp is the better next derivation target because killing it restores the full cGamma budget and removes the independent tensor source pack."),
    ]
    return [
        {
            **common(),
            "guard_id": guard_id,
            "guard": guard,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for guard_id, guard in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "cGamma_zero_parent_signed": "False",
            "Kperp_zero_parent_signed": "False",
            "orthogonality_parent_signed": "False",
            "shared_budget_law_active": "True",
            "strictest_shared_bound": "alpha3 half-budget = 2e-20 dimensionless",
            "scoreable_now": "False",
            "why_not_scoreable": "cGamma profiles and Kperp W_i/N_T/D_T coefficients are not parent-owned or sourced",
            "next_highest_pressure": "prove Kperp is EH/coframe TT/vertical/boundary rather than an independent MTS tensor source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4233_0", "No public local-GR claim follows from shared-budget rows."),
        ("FW4233_1", "No R10 pass follows from the anchor-only alpha(lambda) row."),
        ("FW4233_2", "No cancellation between cGamma and Kperp is allowed without a parent identity."),
        ("FW4233_3", "No Kperp score is allowed until W_i^K, N_T and D_T or a zero theorem is supplied."),
        ("FW4233_4", "No cGamma score is allowed until profile_Gamma,a or a zero theorem is supplied."),
    ]
    return [{**common(), "rule_id": rule_id, "rule": rule, "claim_allowed": "False", "valid_for_claim": "False"} for rule_id, rule in rows]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4233 derives the shared-budget law for the two live local survivors: cGamma and Kperp. With no parent orthogonality or zero theorem, each must fit within half of every shared local bound.",
            "public_local_GR_claim": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "Kperp is the cleanest lever: if it is proved to be ordinary EH TT/gauge/vertical/boundary, the two-survivor problem collapses back to the already-formulated cGamma profile problem.",
            "derive_first": "prove the EH/coframe identity/no-independent-TT-source clause for Kperp in compact local PPN",
            "fill_second": "if the proof fails, fill the first Kperp source row W_i^K, N_T and D_T against alpha3/xi/Gdot bounds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 249 - PPC4161 cGamma/Kperp Two-Survivor Zero-Proof Or Bound Runner

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

After 4232, the first local non-EH survivors are:

```text
c_Gamma,
Kperp/c_T.
```

4233 derives the joint rule:

```text
R_a = C_Gamma,a + R_a^K.
```

Unless the parent action proves one channel is zero or proves an orthogonality/sign identity before fitting, the safe scoring rule is not cancellation. It is a shared budget:

```text
|C_Gamma,a| <= B_a/2,
|R_a^K|     <= B_a/2.
```

If either channel is parent-zero, the surviving channel may use the full `B_a`.

## Current Verdict

Neither zero theorem is parent-signed yet:

```text
Z_Gamma = false,
Z_Kperp = false,
Z_orthogonality = false.
```

So the half-budget law is active. The strictest shared row is:

```text
alpha3 half-budget = 2e-20 dimensionless.
```

The branch is not scoreable yet because `c_Gamma` still needs arena profiles and `Kperp` still needs either the EH/coframe no-extra-pole proof or `W_i^K, N_T, D_T` source rows.

## Why Kperp Is Next

The cleanest improvement is to kill `Kperp` geometrically. If `Kperp` is only ordinary EH TT/gauge/vertical/boundary radiation in compact static local PPN, then `R_a^K=0` and the problem collapses back to the already-sharp `c_Gamma` profile bounds.

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4233 - cGamma/Kperp Two-Survivor Zero-Proof Or Bound Runner

**Status:** `{DECISION}`.

## Forward Move

4233 makes the two-survivor local test stricter:

```text
R_a = C_Gamma,a + R_a^K.
```

No cancellation is allowed. If both channels survive, each gets half of every local arena budget:

```text
|C_Gamma,a| <= B_a/2,
|R_a^K| <= B_a/2.
```

## Practical Read

This does not prove local GR. It says exactly how hard the surviving pair must fight if both stay alive. The alpha3 half-budget is only `2e-20`, so keeping both channels without a zero theorem is brutally expensive.

## Files Written

- `formalization-workbench\\249-PPC4161-cGamma-Kperp-two-survivor-zero-proof-or-bound-runner.md`
- `post-checkpoint-work\\source-intake\\mts_residuals\\P8_Y5_R2FR_4233_ARENA_BOUND_MATRIX.csv`
- `post-checkpoint-work\\source-intake\\mts_residuals\\P8_Y5_R2FR_4233_TWO_SURVIVOR_ZERO_CONTRACT.csv`
- `post-checkpoint-work\\source-intake\\mts_residuals\\P8_Y5_R2FR_4233_NO_CANCELLATION_GUARD.csv`
- `post-checkpoint-work\\source-intake\\mts_residuals\\P8_Y5_BRR545_4233_VALIDATION.csv`

## Next

`{NEXT_TARGET}`
"""


def update_claim_register() -> None:
    path = FORMAL / "02-claims-register.csv"
    rows = csv_rows(path)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": "The two surviving local non-EH channels, c_Gamma and Kperp/c_T, now obey a shared-budget law: without a parent zero or orthogonality theorem, each active channel must fit within half of every shared local bound before any aggregate residual is scored.",
            "current_evidence": "4233 source register, two-survivor zero contract, arena bound matrix, no-cancellation guard, decision and firewall.",
            "status": "private_two_survivor_shared_budget_nonclaim",
            "next_test": "Prove Kperp is ordinary EH/coframe TT/gauge/vertical/boundary radiation, or fill independent Kperp source rows W_i^K, N_T and D_T against alpha3/xi/Gdot bounds.",
            "key_risk": "Letting c_Gamma and Kperp cancel numerically would fake a local-GR pass unless the parent action proves the cancellation identity before testing.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 cGamma/Kperp Two-Survivor Shared-Budget Law

Marker: `{MARKER}`

4233 derives the no-cancellation rule for the first two live local non-EH survivors:

```text
R_a = C_Gamma,a + R_a^K.
```

If both channels survive and no parent orthogonality theorem is signed, each channel gets at most half of every local arena budget. The alpha3 shared row is therefore `2e-20` per channel. This makes `Kperp` the next best derivation target: kill it as EH/coframe TT/vertical/boundary, or fill an independent tensor source row.
"""
    packet_block = f"""
## Packet Update - cGamma/Kperp Two-Survivor Shared-Budget Law

Marker: `{PACKET_MARKER}`

The private packet now has a stricter local residual rule:

```text
|C_Gamma,a| <= B_a/2,
|R_a^K| <= B_a/2
```

whenever both `c_Gamma` and `Kperp/c_T` survive and no parent orthogonality identity exists. This blocks cancellation-based rescue and selects the next clean route: prove `Kperp` is not an independent MTS local tensor source.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validation_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    src = source_rows()
    matrix = bound_rows_for_runner()
    contracts = zero_contract_rows()
    add("VAL4233_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in src), "source register")
    add("VAL4233_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in src), "source register")
    add("VAL4233_2_bound_matrix_rows", "arena matrix includes source-backed local rows", len(matrix) >= 10, str(len(matrix)))
    add("VAL4233_3_half_budget_alpha3", "alpha3 half-budget is 2e-20", any(row["observable"] == "alpha3" and row["split_budget_each_active_channel"] == "2e-20" for row in matrix), "arena matrix")
    add("VAL4233_4_contracts", "zero contract covers cGamma, Kperp and orthogonality", {row["channel"] for row in contracts} == {"cGamma", "Kperp", "joint"}, "zero contract")
    add("VAL4233_5_no_score_now", "no arena row is scoreable now", all(row["scoreable_now"] == "False" for row in matrix), "arena matrix")
    add("VAL4233_6_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for group in (src, matrix, contracts, guard_rows(), decision_rows(), firewall_rows(), status_rows(), next_target_rows()) for row in group), "all groups")
    add("VAL4233_7_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4233_8_claim_register", "claims register contains L-074", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4233_9_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4233_10_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4233_11_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    add("VAL4233_12_decision_blocks_claim", "decision keeps scoreable_now false", decision_rows()[0]["scoreable_now"] == "False", DECISION)
    add("VAL4233_13_R10_anchor_retained", "R10 row remains nonclaim anchor", any(row["observable"] == "alpha_Yukawa_at_lambda_38p6um" and row["full_curve_available"] == "False" for row in matrix), "arena matrix")
    add("VAL4233_14_script_exists", "generator script exists", Path(__file__).exists(), str(Path(__file__)))
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4233_SOURCE_REGISTER.csv",
        "contract": SOURCE_DIR / "P8_Y5_R2FR_4233_TWO_SURVIVOR_ZERO_CONTRACT.csv",
        "matrix": SOURCE_DIR / "P8_Y5_R2FR_4233_ARENA_BOUND_MATRIX.csv",
        "guard": SOURCE_DIR / "P8_Y5_R2FR_4233_NO_CANCELLATION_GUARD.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4233_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4233_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4233_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4233_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["contract"], zero_contract_rows())
    write_csv(paths["matrix"], bound_rows_for_runner())
    write_csv(paths["guard"], guard_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next"], next_target_rows())
    update_claim_register()
    update_spine_and_packet()
    write_csv(VALIDATION_PATH, validation_rows())
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"Decision: {DECISION}")
    print(f"Formal: {FORMAL_PATH}")
    print(f"Checkpoint: {DOC_PATH}")
    print(f"Validation: {VALIDATION_PATH}")
    print(f"Validation rows: {len(csv_rows(VALIDATION_PATH))}; failed: {len(failed)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
