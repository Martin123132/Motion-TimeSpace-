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

CHECKPOINT = "4182"
BRANCH_ID = "MTS_R2FR_Y5_MOTION_FRAME_SYMMETRY_PARENT_SIGNATURE_4182"
DECISION = (
    "A_MF_PARENT_SIGNATURE_NOT_FOUND_COMPENSATOR_FORCING_THEOREM_CONDITIONAL_"
    "EFFECTIVE_GR_CLOSURE_LABEL_ACTIVE"
)
DOC_PATH = POST / "4182-Y5-R2FR-motion-frame-symmetry-parent-signature-or-effective-GR-label.md"
FORMAL_198_PATH = FORMAL / "198-PPC4161-motion-frame-symmetry-parent-signature-gate.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-023"
SPINE_MARKER = "PPC4161_MOTION_FRAME_SYMMETRY_PARENT_SIGNATURE_4182"
PACKET_MARKER = "PPC4161_PACKET_MOTION_FRAME_SYMMETRY_PARENT_SIGNATURE_4182"
NEXT_TARGET = "4183-Y5-R2FR-motion-frame-axiom-adoption-consequences-or-effective-GR-test-contract.md"

SOURCES = {
    "SRC4182_00_4181_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4181_NEXT_TARGET.csv",
        "derive local motion-frame symmetry from MTS primitives",
        "4181 handoff naming motion-frame symmetry as the decisive missing input.",
    ),
    "SRC4182_01_formal_197": (
        FORMAL / "197-PPC4161-EH-local-metric-principal-block-origin-gate.md",
        "If MTS parent-signs local motion-frame Lorentz plus translation symmetry",
        "4181 conditional EH-origin theorem.",
    ),
    "SRC4182_02_4071": (
        POST / "4071-Y5-R2FR-Cartan-solder-field-origin-from-MTS-flow-or-demotion.md",
        "This is not a vibe",
        "4071 compensator logic for B and omega.",
    ),
    "SRC4182_03_4072": (
        POST / "4072-Y5-R2FR-local-motion-frame-gauge-action-or-effective-GR-demotion.md",
        "does **not** yet derive this action",
        "4072 demotion warning for the local motion-frame gauge action.",
    ),
    "SRC4182_04_formal_179": (
        FORMAL / "179-PPC4048-local-parent-packet-candidate.md",
        "parent-sign local motion-frame Lorentz plus translation gauge symmetry",
        "PPC4048 packet records motion-frame gauge branch as a candidate, not a derivation.",
    ),
    "SRC4182_05_redteam_solder": (
        FORMAL / "06-consistency-red-team.md",
        "no owner-spacetime solder map is parent-derived",
        "Red-team record: owner-spacetime solder map remained unproved.",
    ),
    "SRC4182_06_observer_coframe": (
        POST / "10-observer-map-symplectic-contract.md",
        "all matter sectors couple to the same observer coframe",
        "Earlier contract requiring a single observed coframe before local PPN claims.",
    ),
    "SRC4182_07_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "EM side-channel closure inside the private selector uses the same metric/Hodge owner.",
    ),
    "SRC4182_08_claim_L022": (
        CLAIMS_PATH,
        "conditional motion-frame Palatini origin theorem",
        "Latest claim-register row before the motion-frame parent-signature gate.",
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


def evidence_sweep_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "EV4182_0_named_handoff",
            "4181 next target",
            "explicitly asks for local motion-frame Lorentz/translation parent signature",
            "strong_problem_statement",
            "does not itself prove the signature",
        ),
        (
            "EV4182_1_compensator_logic",
            "4071",
            "local affine motion-frame covariance forces omega and B if the symmetry is real",
            "conditional_derivation_available",
            "the conditional theorem can be written exactly",
        ),
        (
            "EV4182_2_action_candidate",
            "4072",
            "motion-frame Palatini action exists as a formal private candidate",
            "candidate_not_parent_owned",
            "candidate action is not yet an MTS derivation",
        ),
        (
            "EV4182_3_packet_record",
            "formal 179",
            "packet asks to parent-sign local motion-frame Lorentz plus translation gauge symmetry",
            "open_parent_burden",
            "same missing clause is already recorded",
        ),
        (
            "EV4182_4_redteam_solder",
            "red-team section 77",
            "owner-spacetime solder map is not parent-derived",
            "direct_counterevidence",
            "prevents claiming derived local metric ownership",
        ),
        (
            "EV4182_5_observer_coframe",
            "observer-map contract",
            "all matter sectors must couple to one observer coframe",
            "necessary_condition_found",
            "supports the target contract but does not generate the symmetry",
        ),
        (
            "EV4182_6_em_hodge",
            "Maxwell-Hodge/Poynting theorem",
            "Poynting flux is owned by the Maxwell-Hodge Hilbert stress inside the selector",
            "compatible_downstream_closure",
            "helps if coframe/metric ownership is parent-signed",
        ),
        (
            "EV4182_7_current_verdict",
            "whole sweep",
            "no source supplies the parent axiom A_MF as an owned MTS principle",
            "parent_signature_not_found",
            "effective-GR closure label must remain active",
        ),
    ]
    return [
        {
            **common(),
            "evidence_id": evidence_id,
            "source_scope": source_scope,
            "finding": finding,
            "status": status,
            "consequence": consequence,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for evidence_id, source_scope, finding, status, consequence in rows
    ]


def forcing_derivation_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "FD4182_0_axiom",
            "A_MF",
            "Local internal motion-frame relabelings are gauge redundancies: X^A -> Lambda^A_B(x) X^B + a^A(x).",
            "adoption_ready_axiom_not_currently_parent_signed",
        ),
        (
            "FD4182_1_failure_of_dX",
            "dX obstruction",
            "dX'^A contains dLambda^A_B X^B + da^A, so dX^A is not covariant under local affine frame relabeling.",
            "proved_conditional_on_A_MF",
        ),
        (
            "FD4182_2_spin_connection",
            "omega compensation",
            "Choose omega' = Lambda omega Lambda^-1 - dLambda Lambda^-1 so D_omega X transforms without the dLambda contamination.",
            "proved_conditional_on_A_MF",
        ),
        (
            "FD4182_3_solder_connection",
            "B compensation",
            "With X' = Lambda X + a, D_{omega'}X' = Lambda D_omega X + D_{omega'}a; choose B' = Lambda B - D_{omega'}a.",
            "proved_conditional_on_A_MF",
        ),
        (
            "FD4182_4_covariant_coframe",
            "e covariance",
            "e'^A = D_{omega'}X'^A + B'^A = Lambda^A_B e^B for e^A = D_omega X^A + B^A.",
            "compensator_forcing_theorem_proved",
        ),
        (
            "FD4182_5_metric_invariance",
            "g_obs",
            "g_obs = eta_AB e^A e^B is invariant under local Lorentz motion-frame rotations and is not pure pullback-flat when B^A is independent.",
            "conditional_local_metric_origin",
        ),
        (
            "FD4182_6_limit",
            "what is still not derived",
            "This proves B and omega are forced by A_MF, not that current MTS already derives A_MF or the Palatini normal form.",
            "public_claim_blocked",
        ),
    ]
    return [
        {
            **common(),
            "derivation_id": derivation_id,
            "clause": clause,
            "statement": statement,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for derivation_id, clause, statement, status in rows
    ]


def countermodel_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "CM4182_0_global_only",
            "Only global Lorentz/translation symmetry is owned.",
            "dLambda=0 and da=0, so no local connection is forced.",
            "does_not_derive_B_or_omega",
        ),
        (
            "CM4182_1_scalar_memory_only",
            "Gamma_mem is a scalar memory/readout variable only.",
            "A scalar cannot encode the full local Lorentz connection or translational solder form.",
            "connection_ownership_fails",
        ),
        (
            "CM4182_2_exact_gradient",
            "e^A=dX^A without B^A.",
            "Nondegenerate scalar gradients give a local pullback-flat metric.",
            "curved_local_GR_fails",
        ),
        (
            "CM4182_3_fixed_background_coframe",
            "A fixed coframe is inserted externally.",
            "The local metric works as a background structure but is not parent-derived MTS geometry.",
            "effective_GR_only",
        ),
        (
            "CM4182_4_second_metric_or_EM_owner",
            "Matter/EM couples to a different metric or Hodge owner.",
            "Poynting/Maxwell stress no longer closes the same Hilbert source channel.",
            "local_selector_reopens",
        ),
    ]
    return [
        {
            **common(),
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "failure_mode": failure_mode,
            "verdict": verdict,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for countermodel_id, countermodel, failure_mode, verdict in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "compensator_forcing_theorem_proved": "True",
            "A_MF_parent_signature_found": "False",
            "B_omega_forced_if_A_MF": "True",
            "current_MTS_local_GR_derivation": "False",
            "effective_GR_closure_label_active": "True",
            "public_local_GR_claim_allowed": "False",
            "meaning": (
                "4182 advances the math by proving the exact compensator forcing law, "
                "but labels the PPC4161 local-GR branch as effective-GR closure until A_MF is parent-signed."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "FW4182_0_no_public_local_GR",
            "Do not say MTS derives local GR.",
            "Use: conditional motion-frame compensator theorem plus effective-GR closure label.",
        ),
        (
            "FW4182_1_no_numeric_G",
            "Do not say MTS predicts the numerical value of Newton's constant.",
            "Use: calibrated-source relation remains internal/empirical unless parent coefficient is derived.",
        ),
        (
            "FW4182_2_no_parent_symmetry_claim",
            "Do not say A_MF is already in the parent corpus.",
            "Use: A_MF is an adoption-ready axiom/contract not found in the current sweep.",
        ),
        (
            "FW4182_3_no_gamma_connection",
            "Do not equate scalar Gamma_mem with the full connection.",
            "Use: Gamma_mem may be an invariant/projection/readout of Cartan field strengths.",
        ),
        (
            "FW4182_4_tests_as_closure",
            "Do not use local tests as proof of parent derivation.",
            "Use: local tests score the effective-GR closure branch and residual interfaces.",
        ),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_language": forbidden_language,
            "safe_language": safe_language,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_language, safe_language in rows
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "result": DECISION,
            "source_sweep_complete": "True",
            "compensator_forcing_theorem_proved": "True",
            "A_MF_parent_signature_found": "False",
            "local_motion_frame_symmetry_parent_signed": "False",
            "B_omega_forced_if_A_MF": "True",
            "same_observer_coframe_necessary_condition_found": "True",
            "Poynting_Hodge_downstream_compatible": "True",
            "effective_GR_closure_label_active": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "formal_198_written": "True",
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
                "4182 proves the compensator law but does not find A_MF in the parent corpus. "
                "The next gate must either adopt A_MF explicitly and derive its Noether/action consequences, "
                "or write the effective-GR closure test contract."
            ),
            "route_A": "adopt A_MF as a parent axiom and derive the Palatini normal-form/noether identities it forces",
            "route_B": "keep PPC4161 as an effective-GR closure branch and build residual tests around torsion, second metric, EM-Hodge, and source coupling",
            "public_claim_policy": "no public local-GR derivation claim until A_MF and the Palatini normal form are parent-signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    names = [
        "P8_Y5_R2FR_4182_SOURCE_REGISTER",
        "P8_Y5_R2FR_4182_PARENT_SYMMETRY_EVIDENCE_SWEEP",
        "P8_Y5_R2FR_4182_COMPENSATOR_FORCING_DERIVATION",
        "P8_Y5_R2FR_4182_COUNTERMODEL_LEDGER",
        "P8_Y5_R2FR_4182_EFFECTIVE_GR_LABEL_DECISION",
        "P8_Y5_R2FR_4182_CLAIM_FIREWALL",
        "P8_Y5_R2FR_4182_STATUS",
        "P8_Y5_R2FR_4182_NEXT_TARGET",
    ]
    return {name: SOURCE_DIR / f"{name}.csv" for name in names}


def write_formal_198() -> None:
    text = f"""# 198 - PPC4161 Motion-Frame Symmetry Parent-Signature Gate

Marker: `{SPINE_MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint proves the exact compensator forcing theorem for a local motion-frame symmetry, but it does not find that symmetry as a parent-owned MTS axiom in the current corpus.

## Adoption-Ready Axiom

Call the missing parent axiom `A_MF`:

```text
The internal motion-frame labels of X^A=L_* Psi^A are local gauge redundancies,
X^A -> Lambda^A_B(x) X^B + a^A(x),
with observables depending only on covariant coframe combinations and scalar contractions.
```

This is the narrowest axiom that would turn the Cartan branch from imported GR infrastructure into an MTS-owned local geometry route.

## Compensator Forcing Theorem

If `A_MF` is parent-signed, then the naive scalar-gradient coframe fails because:

```text
dX'^A = d(Lambda^A_B X^B + a^A)
      = Lambda^A_B dX^B + dLambda^A_B X^B + da^A.
```

The `dLambda` and `da` terms are not covariant. To restore local covariance one must introduce:

```text
omega_prime = Lambda omega Lambda^-1 - dLambda Lambda^-1,
B_prime = Lambda B - D_omega_prime a,
e^A = D_omega X^A + B^A.
```

Then:

```text
e_prime^A = D_omega_prime X_prime^A + B_prime^A = Lambda^A_B e^B,
g_obs = eta_AB e^A e^B.
```

So `omega^AB` and `B^A` are not decorative if `A_MF` is real: they are forced compensators.

## Source-Sweep Verdict

The present corpus supports all of the following:

- the exact-gradient route is rejected;
- the Cartan solder repair is mathematically coherent;
- same-observer-coframe and Maxwell-Hodge/Poynting downstream closures are compatible with it;
- the local selector branch can use the resulting `g_obs` as an effective local metric.

But the sweep did not find a parent-owned MTS statement that internal motion-frame labels are locally affine/Lorentz gauge redundancies. It also found an earlier red-team warning that no owner-spacetime solder map is parent-derived.

## Effective-GR Label

Until `A_MF` is adopted or derived from earlier MTS primitives:

```text
PPC4161_local_GR_branch = effective_GR_closure_branch,
current_MTS_local_GR_derivation = false,
effective_GR_closure_label_active = true,
public_local_GR_claim_allowed = false.
```

This is not a failure of the compensator theorem. It is the correct label for the present state of ownership.

## Next Target

`{NEXT_TARGET}`

Either adopt `A_MF` explicitly and derive its Noether/action consequences, or keep the branch labelled as effective-GR closure and test the residual interfaces without calling it a derived MTS local-GR theorem.
"""
    FORMAL_198_PATH.write_text(text, encoding="utf-8")


def write_doc() -> None:
    text = f"""# 4182 - Y5 R2FR Motion-Frame Symmetry Parent Signature Or Effective-GR Label

Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Result

4182 makes one real mathematical move and one honesty move.

The mathematical move is the exact compensator forcing theorem:

```text
If X^A -> Lambda^A_B(x)X^B + a^A(x),
then e^A = D_omega X^A + B^A is forced by covariance,
with B_prime = Lambda B - D_omega_prime a and omega_prime = Lambda omega Lambda^-1 - dLambda Lambda^-1.
```

That proves the route is not arbitrary: if local motion-frame redundancy is parent-owned, `B^A` and `omega^AB` are mandatory.

## Honest Verdict

The current corpus does not yet parent-sign the axiom `A_MF`. Existing files show a candidate, a conditional theorem, same-coframe requirements, and downstream EM/Poynting compatibility, but not parent ownership of the local affine/Lorentz motion-frame symmetry.

Therefore the local branch is labelled:

```text
effective_GR_closure_label_active = true
public_local_GR_claim_allowed = false
```

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
                "The local motion-frame compensator theorem is proved conditionally: "
                "if A_MF is parent-signed, omega^AB and B^A are forced, but A_MF is not found in the current MTS corpus"
            ),
            "current_evidence": (
                "formalization-workbench/198-PPC4161-motion-frame-symmetry-parent-signature-gate.md records "
                "the affine-frame transformation, dX obstruction, omega/B compensator transformations, "
                "covariant coframe e^A=D_omega X^A+B^A, source sweep, countermodels, and active effective-GR closure label; public_claim=false"
            ),
            "status": "conditional_compensator_theorem_nonclaim_A_MF_not_parent_signed_effective_GR_closure_label_active",
            "next_test": "Either adopt A_MF as a parent axiom and derive Noether/action consequences, or build the effective-GR closure residual test contract",
            "key_risk": (
                "The theorem proves what follows from A_MF, not that MTS already owns A_MF; "
                "without that axiom the local-GR branch remains imported effective-GR infrastructure"
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

## Post-Checkpoint 4182 Motion-Frame Symmetry Parent-Signature Gate

Marker: `{PACKET_MARKER}`

`post-checkpoint-work/4182-Y5-R2FR-motion-frame-symmetry-parent-signature-or-effective-GR-label.md` proves the exact compensator forcing theorem:

```text
X^A -> Lambda^A_B(x)X^B + a^A(x)
e^A = D_omega X^A + B^A
e'^A = Lambda^A_B e^B
```

This proves `omega^AB` and `B^A` are forced if local motion-frame affine/Lorentz redundancy is parent-owned. The source sweep does not find that parent-owned axiom in the present MTS corpus, so the PPC4161 local-GR branch remains labelled as effective-GR closure until `A_MF` is adopted or derived.

```text
A_MF_parent_signature_found = false
compensator_forcing_theorem_proved = true
effective_GR_closure_label_active = true
public_local_GR_claim_allowed = false
```
"""
    PACKET_180_PATH.write_text(text.rstrip() + addendum, encoding="utf-8")
    return "added"


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161 Motion-Frame Symmetry Parent-Signature Gate

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4182 proves the conditional compensator theorem needed by the local-GR route. If MTS parent-signs the local affine/Lorentz motion-frame redundancy `A_MF`, the noncovariant terms in `dX'^A` force a spin/motion-frame connection `omega^AB` and a translational solder form `B^A`, with:

```text
e^A = D_omega X^A + B^A,
g_obs = eta_AB e^A e^B.
```

The theorem is useful because it shows the Cartan fields are not arbitrary add-ons under `A_MF`. The present corpus still does not prove `A_MF`, so the local-GR branch is an effective-GR closure branch until the parent axiom or an equivalent derivation is adopted.

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
        for row in rows_by_name["P8_Y5_R2FR_4182_SOURCE_REGISTER"]
    )
    decision = rows_by_name["P8_Y5_R2FR_4182_EFFECTIVE_GR_LABEL_DECISION"][0]
    status = rows_by_name["P8_Y5_R2FR_4182_STATUS"][0]
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
        ("VAL4182_0_sources", "all cited sources exist and contain required text", source_ok, ""),
        ("VAL4182_1_evidence", "evidence sweep has direct parent-signature verdict", any(row["status"] == "parent_signature_not_found" for row in rows_by_name["P8_Y5_R2FR_4182_PARENT_SYMMETRY_EVIDENCE_SWEEP"]), ""),
        ("VAL4182_2_derivation", "compensator forcing theorem row exists", any(row["status"] == "compensator_forcing_theorem_proved" for row in rows_by_name["P8_Y5_R2FR_4182_COMPENSATOR_FORCING_DERIVATION"]), ""),
        ("VAL4182_3_countermodels", "countermodels include scalar-memory failure", any(row["countermodel_id"] == "CM4182_1_scalar_memory_only" for row in rows_by_name["P8_Y5_R2FR_4182_COUNTERMODEL_LEDGER"]), ""),
        ("VAL4182_4_decision", "decision keeps A_MF parent signature false", decision["A_MF_parent_signature_found"] == "False", str(decision)),
        ("VAL4182_5_effective_label", "effective-GR closure label is active", decision["effective_GR_closure_label_active"] == "True", str(decision)),
        ("VAL4182_6_public_claim", "public local-GR claim remains false", status["public_local_GR_claim_allowed"] == "False", str(status)),
        ("VAL4182_7_formal_198", "formal 198 exists and has marker", FORMAL_198_PATH.exists() and SPINE_MARKER in read_text(FORMAL_198_PATH), str(FORMAL_198_PATH)),
        ("VAL4182_8_doc", "4182 doc exists and has decision", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4182_9_claim_row", "claim register contains L-023", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4182_10_packet_180", "packet 180 addendum marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4182_11_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4182_12_next", "next target recorded", rows_by_name["P8_Y5_R2FR_4182_NEXT_TARGET"][0]["next_target"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4182_13_output_paths", "all declared output CSVs exist", all(path.exists() for path in paths.values()), str(paths)),
        ("VAL4182_14_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
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
            "check_id": "VAL4182_15_compile",
            "description": "generator compiles and pycache is removed",
            "passed": "True",
            "details": "compiled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    write_formal_198()
    write_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name = {
        "P8_Y5_R2FR_4182_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4182_PARENT_SYMMETRY_EVIDENCE_SWEEP": evidence_sweep_rows(),
        "P8_Y5_R2FR_4182_COMPENSATOR_FORCING_DERIVATION": forcing_derivation_rows(),
        "P8_Y5_R2FR_4182_COUNTERMODEL_LEDGER": countermodel_rows(),
        "P8_Y5_R2FR_4182_EFFECTIVE_GR_LABEL_DECISION": decision_rows(),
        "P8_Y5_R2FR_4182_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4182_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4182_NEXT_TARGET": next_rows(),
    }

    for name, path in output_paths().items():
        write_csv(path, rows_by_name[name])

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4182_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4182 validation failed: {failed}")

    print(f"{CHECKPOINT} generated")
    print(f"doc={DOC_PATH}")
    print(f"formal={FORMAL_198_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
