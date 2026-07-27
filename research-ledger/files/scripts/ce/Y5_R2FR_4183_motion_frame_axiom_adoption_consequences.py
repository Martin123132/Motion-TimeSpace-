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

CHECKPOINT = "4183"
BRANCH_ID = "MTS_R2FR_Y5_A_MF_ADOPTION_CONSEQUENCES_4183"
DECISION = (
    "A_MF_ADOPTION_CONTRACT_WRITTEN_NOETHER_IDENTITIES_DERIVED_"
    "PALATINI_NOT_FORCED_EFFECTIVE_GR_TEST_CONTRACT_READY"
)
DOC_PATH = POST / "4183-Y5-R2FR-motion-frame-axiom-adoption-consequences-or-effective-GR-test-contract.md"
FORMAL_199_PATH = FORMAL / "199-PPC4161-motion-frame-axiom-adoption-consequences-and-test-contract.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-024"
SPINE_MARKER = "PPC4161_A_MF_ADOPTION_CONSEQUENCES_4183"
PACKET_MARKER = "PPC4161_PACKET_A_MF_ADOPTION_CONSEQUENCES_4183"
NEXT_TARGET = "4184-Y5-R2FR-Palatini-IR-normal-form-selector-under-AMF-or-residual-EFT-bound.md"

SOURCES = {
    "SRC4183_00_4182_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4182_NEXT_TARGET.csv",
        "adopt A_MF as a parent axiom",
        "4182 handoff naming the adoption-consequence fork.",
    ),
    "SRC4183_01_formal_198": (
        FORMAL / "198-PPC4161-motion-frame-symmetry-parent-signature-gate.md",
        "Compensator Forcing Theorem",
        "formal 198 gives the A_MF axiom candidate and compensator theorem.",
    ),
    "SRC4183_02_4182_derivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4182_COMPENSATOR_FORCING_DERIVATION.csv",
        "compensator_forcing_theorem_proved",
        "4182 CSV evidence for B and omega forcing under A_MF.",
    ),
    "SRC4183_03_4182_countermodels": (
        SOURCE_DIR / "P8_Y5_R2FR_4182_COUNTERMODEL_LEDGER.csv",
        "effective_GR_only",
        "countermodel showing inserted fixed coframe is only effective GR.",
    ),
    "SRC4183_04_selector": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "Maxwell-Hodge/Poynting stress ownership",
        "local selector clauses that must be owned by the parent action.",
    ),
    "SRC4183_05_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "downstream EM/Poynting owner theorem inside the private selector.",
    ),
    "SRC4183_06_source_coupling": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi)",
        "calibrated Newton coupling firewall.",
    ),
    "SRC4183_07_action_matrix": (
        FORMAL / "196-PPC4161-minimal-parent-action-adoption-matrix.md",
        "EH/local metric principal block: hard root",
        "action matrix says the EH block is the hard root not globally parent-derived.",
    ),
    "SRC4183_08_claim_L023": (
        CLAIMS_PATH,
        "conditional_compensator_theorem_nonclaim_A_MF_not_parent_signed",
        "latest claim row before A_MF adoption-consequence gate.",
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


def adoption_consequence_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "AC4183_0_A_MF_adoption",
            "adopt A_MF as explicit parent axiom candidate",
            "local motion-frame affine/Lorentz relabelings are gauge redundancies of X^A=L_*Psi^A",
            "new_parent_axiom_candidate_not_older_derived",
            "removes ambiguity about whether B and omega are imported",
        ),
        (
            "AC4183_1_forced_fields",
            "compensator fields",
            "omega^AB and B^A are required for local covariance; e^A=D_omega X^A+B^A",
            "forced_if_A_MF",
            "g_obs can be parent-owned if A_MF is adopted",
        ),
        (
            "AC4183_2_building_blocks",
            "covariant invariants",
            "allowed local terms must be built from e^A, R^AB[omega], T^A, parent scalars, matter fields, and exterior/covariant derivatives",
            "derived_selection_rule",
            "scalar Gamma_mem can enter as invariant/readout, not as full connection",
        ),
        (
            "AC4183_3_same_coframe",
            "universal matter/EM metric owner",
            "matter and Maxwell-Hodge sectors must use g_obs=eta_AB e^A e^B or explicitly carry a residual",
            "required_for_WEP_EM_closure",
            "protects Maxwell/Poynting Hilbert stress channel",
        ),
        (
            "AC4183_4_noether",
            "Noether identities",
            "local Lorentz and translation redundancy imply spin-stress balance and covariant source conservation identities",
            "derived_conditional_on_action_invariance",
            "needed for Bianchi/conservation closure",
        ),
        (
            "AC4183_5_limit",
            "what A_MF does not force",
            "A_MF allows many invariant actions; it does not by itself select the Einstein-Cartan/Palatini term",
            "Palatini_EH_not_forced_by_A_MF_alone",
            "next gate must select or bound extra invariant terms",
        ),
        (
            "AC4183_6_effective_contract",
            "if A_MF is not adopted",
            "treat PPC4161 as effective-GR closure and test residuals instead of calling it derived MTS local GR",
            "test_contract_ready",
            "keeps work empirical without smuggling derivation",
        ),
    ]
    return [
        {
            **common(),
            "consequence_id": consequence_id,
            "clause": clause,
            "content": content,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for consequence_id, clause, content, status, meaning in rows
    ]


def noether_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "NI4183_0_action_variation",
            "first-order variables",
            "delta S = E_A wedge delta e^A + E_AB wedge delta omega^AB + E_XA delta X^A + matter equations plus boundary",
            "setup",
            "defines the Euler forms whose gauge identities must vanish off shell",
        ),
        (
            "NI4183_1_lorentz_variation",
            "local Lorentz parameter lambda^AB",
            "delta_lambda e^A=lambda^A_B e^B, delta_lambda omega^AB=-D_omega lambda^AB, delta_lambda X^A=lambda^A_B X^B",
            "A_MF_transformation",
            "variation by arbitrary lambda gives the Lorentz Noether identity",
        ),
        (
            "NI4183_2_lorentz_identity",
            "spin-stress balance",
            "D_omega E_AB + e_[A wedge E_B] + X_[A E_B]^X plus matter spin terms = 0",
            "derived_identity",
            "in spinless torsion-free local branch this enforces symmetric Hilbert stress",
        ),
        (
            "NI4183_3_translation_variation",
            "local translation parameter a^A",
            "delta_a X^A=a^A, delta_a B^A=-D_omega a^A, delta_a e^A=0 when e^A=D_omega X^A+B^A",
            "A_MF_transformation",
            "translation redundancy removes X^A as a direct observable",
        ),
        (
            "NI4183_4_translation_identity",
            "source conservation",
            "E_XA - D_omega E_BA plus matter source pullback terms = 0; after field equations this reduces to covariant stress conservation in the local branch",
            "derived_identity",
            "connects parent gauge redundancy to Bianchi-compatible source conservation",
        ),
        (
            "NI4183_5_diffeomorphism_identity",
            "spacetime covariance",
            "diffeomorphism invariance gives D_omega E_A contracted with e plus curvature/torsion terms; on shell it becomes nabla_mu T_total^{mu nu}=0",
            "derived_conditional_on_covariant_action",
            "needed for Newton/PPN conservation consistency",
        ),
        (
            "NI4183_6_limit",
            "normal-form warning",
            "Noether identities constrain allowed equations but do not uniquely choose the EC/Palatini Lagrangian coefficient",
            "not_EH_selection",
            "prevents pretending conservation alone derives GR",
        ),
    ]
    return [
        {
            **common(),
            "identity_id": identity_id,
            "object": obj,
            "statement": statement,
            "status": status,
            "consequence": consequence,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for identity_id, obj, statement, status, consequence in rows
    ]


def normal_form_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "NF4183_0_EC_Palatini",
            "epsilon_ABCD e^A wedge e^B wedge R^CD",
            "allowed",
            "desired EH/Palatini principal block",
            "coefficient still calibrated by kappa_eff",
        ),
        (
            "NF4183_1_cosmological",
            "epsilon_ABCD e^A wedge e^B wedge e^C wedge e^D",
            "allowed",
            "cosmological constant / vacuum term",
            "must match cosmology branch, not local tests alone",
        ),
        (
            "NF4183_2_torsion_squared",
            "T^A wedge star T_A and irreducible torsion squares",
            "allowed_unless_suppressed",
            "can create PPN/preferred-frame/contact residuals",
            "needs coefficient zero, heavy mass, or source-backed bound",
        ),
        (
            "NF4183_3_curvature_squared",
            "R^AB wedge star R_AB and scalar curvature squares",
            "allowed_unless_IR_suppressed",
            "higher-derivative local deviations",
            "needs EFT scale/bound; A_MF alone does not erase it",
        ),
        (
            "NF4183_4_disformal_second_metric",
            "matter Hodge/measure using metric not equal to g_obs",
            "forbidden_or_residual",
            "WEP/EM/Poynting side channel",
            "same-coframe axiom or residual test required",
        ),
        (
            "NF4183_5_memory_invariants",
            "Gamma_mem times curvature/torsion/source invariants",
            "allowed_if_covariant",
            "local memory hair can reopen local tests",
            "must screen, vanish, or be bounded in compact local collars",
        ),
        (
            "NF4183_6_boundary_topological",
            "Nieh-Yan, Euler, Pontryagin, GHY/Hamiltonian boundary terms",
            "allowed_if_routed",
            "affects charges/boundaries not bulk PPN if properly routed",
            "boundary no-flux and charge routing remain required",
        ),
    ]
    return [
        {
            **common(),
            "normal_form_id": normal_form_id,
            "term_family": term_family,
            "A_MF_status": status,
            "physical_role": role,
            "gate_or_bound": gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for normal_form_id, term_family, status, role, gate in rows
    ]


def effective_test_contract_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "ETC4183_0_torsion",
            "torsion / spin-connection residual",
            "PPN preferred-frame, spin couplings, short-range gravity",
            "coefficient zero/heavy/bounded",
            "open",
        ),
        (
            "ETC4183_1_second_metric",
            "matter/EM metric not equal to g_obs",
            "WEP, clocks, Maxwell propagation, Poynting stress mismatch",
            "same-coframe proof or Eotvos/clock/EM bound",
            "open",
        ),
        (
            "ETC4183_2_source_coupling",
            "kappa_eff or source charge drift",
            "Newton coefficient, orbital GM, clock/local G variation",
            "calibration lock or measured-G envelope",
            "open_numeric_G_not_predicted",
        ),
        (
            "ETC4183_3_memory_hair",
            "Gamma_mem local invariant couplings",
            "PPN, R10, clock, orbital residuals",
            "local screening or source-backed bound",
            "open",
        ),
        (
            "ETC4183_4_EM_Hodge",
            "Maxwell-Hodge owner mismatch",
            "Poynting side channel and EM stress double-counting",
            "single Hodge owner or residual flux ledger",
            "private_selector_closed_global_open",
        ),
        (
            "ETC4183_5_boundary",
            "radiative/transition boundary leakage",
            "local conservation and orbital/clock leakage",
            "Hamiltonian routing/no-flux/support separation",
            "private_selector_closed_global_open",
        ),
        (
            "ETC4183_6_empirical_dashboard",
            "combined effective-GR closure residual vector",
            "R10, WEP, PPN, clock, orbital, EM propagation",
            "score only as closure robustness, not derivation proof",
            "ready_to_build",
        ),
    ]
    return [
        {
            **common(),
            "test_id": test_id,
            "residual": residual,
            "arena": arena,
            "acceptance_requirement": requirement,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for test_id, residual, arena, requirement, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "A_MF_adoption_contract_written": "True",
            "A_MF_older_MTS_derivation_found": "False",
            "Noether_identities_derived": "True",
            "B_omega_forced_if_A_MF": "True",
            "same_coframe_matter_EM_required": "True",
            "Palatini_EH_forced_by_A_MF_alone": "False",
            "IR_normal_form_selector_needed": "True",
            "effective_GR_test_contract_ready": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "meaning": (
                "A_MF is now an explicit adoption-ready parent axiom with derived Noether consequences. "
                "It forces the geometry variables but not the EH action by itself."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "FW4183_0_A_MF",
            "A_MF is derived from older MTS primitives.",
            "A_MF is an explicit adoption-ready parent axiom candidate unless a later derivation closes it.",
        ),
        (
            "FW4183_1_EH",
            "A_MF alone derives Einstein-Hilbert/Palatini dynamics.",
            "A_MF derives covariant variables and Noether identities; an IR normal-form selector is still required.",
        ),
        (
            "FW4183_2_GR",
            "MTS now publicly derives local GR.",
            "The local-GR branch remains private/nonclaim until A_MF plus Palatini normal form plus residual gates close.",
        ),
        (
            "FW4183_3_G",
            "MTS predicts the numerical value of G.",
            "The structural relation G_cal=c^4 kappa_eff/(8*pi) remains calibrated unless kappa_eff is parent-predicted.",
        ),
        (
            "FW4183_4_tests",
            "Effective-GR closure tests prove derivation.",
            "Tests can support robustness of the closure branch; derivation requires parent ownership of the action clauses.",
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
            "A_MF_adoption_contract_written": "True",
            "A_MF_older_MTS_derivation_found": "False",
            "Noether_identities_derived": "True",
            "B_omega_forced_if_A_MF": "True",
            "Palatini_EH_forced_by_A_MF_alone": "False",
            "IR_normal_form_selector_needed": "True",
            "effective_GR_test_contract_ready": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "formal_199_written": "True",
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
                "A_MF now gives the variables and identities, but it does not select Einstein-Cartan/Palatini over other A_MF-invariant terms. "
                "The next gate must derive or bound the IR normal form."
            ),
            "route_A": "derive an IR selector under A_MF: locality, parity, two-derivative order, no extra light modes, same-coframe matter, and boundary routing select EC/Palatini",
            "route_B": "if selector fails, treat extra invariant terms as EFT residuals and build bounds for torsion, curvature-squared, disformal, memory, and boundary terms",
            "public_claim_policy": "no public local-GR derivation claim until the Palatini normal form and residual gates close",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    names = [
        "P8_Y5_R2FR_4183_SOURCE_REGISTER",
        "P8_Y5_R2FR_4183_A_MF_ADOPTION_CONSEQUENCE_MATRIX",
        "P8_Y5_R2FR_4183_NOETHER_IDENTITY_DERIVATION",
        "P8_Y5_R2FR_4183_IR_NORMAL_FORM_GATE",
        "P8_Y5_R2FR_4183_EFFECTIVE_GR_TEST_CONTRACT",
        "P8_Y5_R2FR_4183_FORK_DECISION",
        "P8_Y5_R2FR_4183_CLAIM_FIREWALL",
        "P8_Y5_R2FR_4183_STATUS",
        "P8_Y5_R2FR_4183_NEXT_TARGET",
    ]
    return {name: SOURCE_DIR / f"{name}.csv" for name in names}


def write_formal_199() -> None:
    text = f"""# 199 - PPC4161 Motion-Frame Axiom Adoption Consequences And Test Contract

Marker: `{SPINE_MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not say MTS has already derived local GR. It writes the exact adoption contract for `A_MF`, derives the Noether/action consequences, and identifies the next missing step: the IR normal-form selector for the Einstein-Cartan/Palatini block.

## If A_MF Is Adopted

`A_MF` says the internal motion-frame labels of `X^A=L_*Psi^A` are local gauge redundancies. The previous checkpoint proved:

```text
e^A = D_omega X^A + B^A
g_obs = eta_AB e^A e^B
```

4183 adds the action-level consequences. Any parent action using this branch must be built from covariant objects:

```text
e^A, R^AB[omega], T^A, parent scalar invariants, matter/EM fields,
and covariant exterior derivatives.
```

Matter and Maxwell-Hodge terms must use the same `g_obs` unless a residual side channel is explicitly kept.

## Noether Consequences

For a first-order local action:

```text
delta S = E_A wedge delta e^A + E_AB wedge delta omega^AB + E_XA delta X^A + matter equations + boundary.
```

Local Lorentz redundancy gives a spin-stress balance identity:

```text
D_omega E_AB + e_[A wedge E_B] + X_[A E_B]^X + spin/matter terms = 0.
```

Local translation redundancy gives the source/conservation identity:

```text
E_XA - D_omega E_BA + matter source pullback terms = 0.
```

Together with diffeomorphism invariance and the field equations, the compact local branch must reduce to the usual covariant conservation condition for the total Hilbert source:

```text
nabla_mu T_total^(mu nu) = 0.
```

This is useful: it explains why Bianchi-compatible conservation is not an extra magic patch if `A_MF` is adopted.

## The Limit

`A_MF` does not uniquely select the Einstein-Cartan/Palatini action. It allows:

- the desired `epsilon_ABCD e^A wedge e^B wedge R^CD`;
- cosmological/vacuum terms;
- torsion-squared terms;
- curvature-squared terms;
- covariant memory couplings;
- boundary/topological terms;
- possible disformal/second-metric side channels unless forbidden.

Therefore:

```text
A_MF_adoption_contract_written = true
Noether_identities_derived = true
Palatini_EH_forced_by_A_MF_alone = false
IR_normal_form_selector_needed = true
public_local_GR_claim_allowed = false
```

## Effective-GR Test Contract

If `A_MF` is not adopted, or if the IR normal form cannot be selected, PPC4161 remains an effective-GR closure branch. Its residual vector must include torsion, second metric/disformal coupling, source-coupling drift, local memory hair, EM-Hodge owner mismatch, and boundary leakage.

## Next Target

`{NEXT_TARGET}`
"""
    FORMAL_199_PATH.write_text(text, encoding="utf-8")


def write_doc() -> None:
    text = f"""# 4183 - Y5 R2FR Motion-Frame Axiom Adoption Consequences Or Effective-GR Test Contract

Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Result

4183 adopts `A_MF` only as an explicit parent-axiom candidate and derives what follows.

It gives a real advance:

- `A_MF` forces covariant variables `e^A`, `omega^AB`, `B^A`;
- local Lorentz redundancy gives a spin-stress balance identity;
- local translation redundancy gives a source/conservation identity;
- same-coframe matter/EM coupling becomes a required clause, not an optional aesthetic.

## Honest Limit

`A_MF` does not by itself derive the Einstein-Cartan/Palatini action. It permits other invariant terms, including torsion-squared, curvature-squared, memory couplings, and boundary/topological structures.

So the next target is not another loop around the same missing axiom. It is the sharper question:

```text
Can A_MF plus locality/two-derivative/low-energy/no-extra-light-mode assumptions select the Palatini IR normal form?
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
                "If adopted as an explicit parent axiom candidate, A_MF forces the Cartan variables and Noether identities needed for local conservation, "
                "but it does not by itself select the Palatini/EH action"
            ),
            "current_evidence": (
                "formalization-workbench/199-PPC4161-motion-frame-axiom-adoption-consequences-and-test-contract.md records "
                "the A_MF adoption contract, covariant building blocks, Lorentz spin-stress identity, translation source-conservation identity, "
                "IR normal-form gate, effective-GR residual test contract, and public-claim firewall"
            ),
            "status": "A_MF_adoption_consequences_nonclaim_Noether_identities_derived_Palatini_not_forced_public_claim_false",
            "next_test": "Derive the Palatini IR normal-form selector under A_MF or bound all extra A_MF-invariant residual terms as EFT corrections",
            "key_risk": (
                "A_MF can make the geometry variables natural while still allowing non-GR invariant terms; "
                "without an IR selector the branch remains effective-GR closure"
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

## Post-Checkpoint 4183 A_MF Adoption Consequences

Marker: `{PACKET_MARKER}`

`post-checkpoint-work/4183-Y5-R2FR-motion-frame-axiom-adoption-consequences-or-effective-GR-test-contract.md` treats `A_MF` as an explicit adoption-ready parent axiom candidate and derives the action-level consequences.

The useful gain is:

```text
A_MF -> e^A, omega^AB, B^A as parent-covariant variables
A_MF + local action invariance -> spin-stress and source-conservation Noether identities
same-coframe matter/EM owner required
```

The honest limit is:

```text
Palatini_EH_forced_by_A_MF_alone = false
IR_normal_form_selector_needed = true
effective_GR_test_contract_ready = true
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

## PPC4161 A_MF Adoption Consequences

Marker: `{SPINE_MARKER}`

Claim register row: `{CLAIM_ID}`

4183 turns `A_MF` from a vague missing ingredient into an explicit adoption contract. If adopted, it forces the Cartan variables and the Noether identities needed for local conservation. It does not by itself force the Palatini/EH action, because other A_MF-invariant torsion, curvature, memory, boundary, and disformal terms remain allowed unless selected out or bounded.

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
        for row in rows_by_name["P8_Y5_R2FR_4183_SOURCE_REGISTER"]
    )
    decision = rows_by_name["P8_Y5_R2FR_4183_FORK_DECISION"][0]
    status = rows_by_name["P8_Y5_R2FR_4183_STATUS"][0]
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
        ("VAL4183_0_sources", "all cited sources exist and contain required text", source_ok, ""),
        ("VAL4183_1_adoption", "A_MF adoption contract row exists", any(row["consequence_id"] == "AC4183_0_A_MF_adoption" for row in rows_by_name["P8_Y5_R2FR_4183_A_MF_ADOPTION_CONSEQUENCE_MATRIX"]), ""),
        ("VAL4183_2_noether", "Noether identities derived rows exist", any(row["status"] == "derived_identity" for row in rows_by_name["P8_Y5_R2FR_4183_NOETHER_IDENTITY_DERIVATION"]), ""),
        ("VAL4183_3_normal_form", "Palatini not forced by A_MF alone is recorded", any(row["status"] == "Palatini_EH_not_forced_by_A_MF_alone" for row in rows_by_name["P8_Y5_R2FR_4183_A_MF_ADOPTION_CONSEQUENCE_MATRIX"]), ""),
        ("VAL4183_4_effective_tests", "effective-GR residual dashboard row exists", any(row["test_id"] == "ETC4183_6_empirical_dashboard" for row in rows_by_name["P8_Y5_R2FR_4183_EFFECTIVE_GR_TEST_CONTRACT"]), ""),
        ("VAL4183_5_decision", "decision keeps Palatini forced false", decision["Palatini_EH_forced_by_A_MF_alone"] == "False", str(decision)),
        ("VAL4183_6_selector_needed", "IR normal-form selector is required", decision["IR_normal_form_selector_needed"] == "True", str(decision)),
        ("VAL4183_7_public_claim", "public local-GR claim remains false", status["public_local_GR_claim_allowed"] == "False", str(status)),
        ("VAL4183_8_formal_199", "formal 199 exists and has marker", FORMAL_199_PATH.exists() and SPINE_MARKER in read_text(FORMAL_199_PATH), str(FORMAL_199_PATH)),
        ("VAL4183_9_doc", "4183 doc exists and has decision", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), str(DOC_PATH)),
        ("VAL4183_10_claim_row", "claim register contains L-024", any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)), claim_action),
        ("VAL4183_11_packet_180", "packet 180 addendum marker present", PACKET_MARKER in read_text(PACKET_180_PATH), packet_action),
        ("VAL4183_12_spine", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH), spine_action),
        ("VAL4183_13_next", "next target recorded", rows_by_name["P8_Y5_R2FR_4183_NEXT_TARGET"][0]["next_target"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4183_14_output_paths", "all declared output CSVs exist", all(path.exists() for path in paths.values()), str(paths)),
        ("VAL4183_15_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not bad_claim_rows, str(bad_claim_rows)),
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
            "check_id": "VAL4183_16_compile",
            "description": "generator compiles and pycache is removed",
            "passed": "True",
            "details": "compiled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    write_formal_199()
    write_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name = {
        "P8_Y5_R2FR_4183_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4183_A_MF_ADOPTION_CONSEQUENCE_MATRIX": adoption_consequence_rows(),
        "P8_Y5_R2FR_4183_NOETHER_IDENTITY_DERIVATION": noether_rows(),
        "P8_Y5_R2FR_4183_IR_NORMAL_FORM_GATE": normal_form_rows(),
        "P8_Y5_R2FR_4183_EFFECTIVE_GR_TEST_CONTRACT": effective_test_contract_rows(),
        "P8_Y5_R2FR_4183_FORK_DECISION": decision_rows(),
        "P8_Y5_R2FR_4183_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4183_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4183_NEXT_TARGET": next_rows(),
    }

    for name, path in output_paths().items():
        write_csv(path, rows_by_name[name])

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4183_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4183 validation failed: {failed}")

    print(f"{CHECKPOINT} generated")
    print(f"doc={DOC_PATH}")
    print(f"formal={FORMAL_199_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
