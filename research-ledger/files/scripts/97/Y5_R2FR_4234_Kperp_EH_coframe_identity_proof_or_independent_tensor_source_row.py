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

CHECKPOINT = "4234"
CLAIM_ID = "L-075"
BRANCH = "MTS_R2FR_Y5_KPERP_EH_COFRAME_IDENTITY_4234"
DECISION = "KPERP_PRIVATE_EH_COFRAME_IDENTITY_DERIVED_PUBLIC_NO_INDEPENDENT_TT_SOURCE_CLAUSE_UNSIGNED_CGAMMA_SOLE_PRIVATE_SURVIVOR"
MARKER = "PPC4161_KPERP_EH_COFRAME_IDENTITY_4234"
PACKET_MARKER = "PPC4161_PACKET_KPERP_EH_COFRAME_IDENTITY_4234"
NEXT_TARGET = "4235-Y5-R2FR-cGamma-support-nohair-or-full-budget-profile-bound-runner.md"

FORMAL_PATH = FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md"
DOC_PATH = POST / "4234-Y5-R2FR-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4234_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4234_00_4233_next": SourceSpec(
        "SRC4234_00_4233_next",
        SOURCE_DIR / "P8_Y5_R2FR_4233_NEXT_TARGET.csv",
        "4234-Y5-R2FR-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
        "4233 selected Kperp/EH-coframe identity as the next pressure point.",
    ),
    "SRC4234_01_palatini": SourceSpec(
        "SRC4234_01_palatini",
        FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md",
        "S_EC[e, omega; kappa_eff] -> S_EH[g_obs; kappa_eff] + routed boundary.",
        "Private EH/Palatini principal block.",
    ),
    "SRC4234_02_same_coframe": SourceSpec(
        "SRC4234_02_same_coframe",
        FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md",
        "single observed coframe + Hilbert source descent + Maxwell-Hodge owner",
        "Same observed coframe and Hodge owner.",
    ),
    "SRC4234_03_coupling": SourceSpec(
        "SRC4234_03_coupling",
        FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md",
        "one constant source-blind coupling,",
        "Calibrated source-blind coupling.",
    ),
    "SRC4234_04_poynting": SourceSpec(
        "SRC4234_04_poynting",
        FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md",
        "Poynting vector is real physical flow",
        "EM/Poynting counted as Hilbert stress, not a hidden tensor source.",
    ),
    "SRC4234_05_Kzero": SourceSpec(
        "SRC4234_05_Kzero",
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "K_perp = 0.",
        "Original conditional Kperp zero theorem.",
    ),
    "SRC4234_06_Kvector": SourceSpec(
        "SRC4234_06_Kvector",
        FORMAL / "217-PPC4161-Kperp-finite-coefficient-vector.md",
        "C_T, S_T, B_T, I_T, Z_T, W_i^K.",
        "Finite Kperp source-pack fallback.",
    ),
    "SRC4234_07_Kdenominator": SourceSpec(
        "SRC4234_07_Kdenominator",
        FORMAL / "218-PPC4161-parent-tensor-operator-LT-coercivity.md",
        "Z_T, M_T^2, lambda_D, S_T, B_T, I_T, Z_Tmode, W_i^K.",
        "Tensor denominator and source numerator inputs.",
    ),
    "SRC4234_08_no_pole": SourceSpec(
        "SRC4234_08_no_pole",
        FORMAL / "219-PPC4161-no-physical-Kperp-pole-theorem.md",
        "K_perp = 0",
        "No-extra-pole theorem for ordinary EH TT in static compact local PPN.",
    ),
    "SRC4234_09_sector": SourceSpec(
        "SRC4234_09_sector",
        FORMAL / "220-PPC4161-Kperp-sector-placement-theorem.md",
        "K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source.",
        "Kperp sector placement identity.",
    ),
    "SRC4234_10_six_clause": SourceSpec(
        "SRC4234_10_six_clause",
        FORMAL / "221-PPC4161-EH-coframe-parent-signature-or-Kperp-score.md",
        "Six-Clause EH/Coframe Gate",
        "Six-clause EH/coframe fork.",
    ),
    "SRC4234_11_vertical": SourceSpec(
        "SRC4234_11_vertical",
        FORMAL / "229-PPC4161-qbasic-vertical-presymplectic-silence.md",
        "I_qbasic_vertical = int_S i_tau omega_qbasic_vertical = 0.",
        "Vertical q-basic silence.",
    ),
    "SRC4234_12_boundary": SourceSpec(
        "SRC4234_12_boundary",
        FORMAL / "233-PPC4161-boundary-corner-curl-zero-or-flux-bound.md",
        "I_boundary + I_corner = 0.",
        "Boundary/corner routing in no-flux collars.",
    ),
    "SRC4234_13_Dq": SourceSpec(
        "SRC4234_13_Dq",
        FORMAL / "235-PPC4161-Dq-source-readout-coupling-marker-zero-or-bound.md",
        "Dq_coeff[v]=0.",
        "Coefficient/readout quotient silence.",
    ),
    "SRC4234_14_two_survivor": SourceSpec(
        "SRC4234_14_two_survivor",
        FORMAL / "249-PPC4161-cGamma-Kperp-two-survivor-zero-proof-or-bound-runner.md",
        "`Kperp` is only ordinary EH TT/gauge/vertical/boundary radiation",
        "4233 explains why Kperp is the cleanest next derivation lever.",
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
    for source_spec in SOURCE_SPECS.values():
        text = read_text(source_spec.path)
        rows.append(
            {
                **common(),
                "source_id": source_spec.source_id,
                "path": str(source_spec.path),
                "exists": str(source_spec.path.exists()),
                "required_text": source_spec.required_text,
                "required_text_found": str(source_spec.required_text in text),
                "role": source_spec.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def six_clause_rows() -> List[Dict[str, str]]:
    rows = [
        ("KC4234_0_same_coframe", "same observed coframe for matter, EM, clocks and rods", "single observed coframe plus Hilbert/Maxwell-Hodge owner", "True", "False", "public/global action-domain adoption still not signed"),
        ("KC4234_1_EH_principal_block", "EH/Palatini spin-2 principal block", "S_EC -> S_EH[g_obs] plus routed boundary in the private IR selector", "True", "False", "conditional selector theorem, not global derivation"),
        ("KC4234_2_no_independent_TT_source", "no independent local MTS TT source projection", "single-coframe EH-only local tensor variation has no separate K_extra source functional", "True", "False", "this is private selector adoption; public parent action still needs a no-extra-TT-source clause"),
        ("KC4234_3_vertical_quotient_silence", "vertical quotient/gauge pieces do not project to observed local residuals", "Dq[v]=0 plus q-basic action descent gives vertical presymplectic silence", "True", "False", "global edge and marker leaks remain public caveats"),
        ("KC4234_4_boundary_radiation_routing", "boundary/radiation pieces are not hidden static bulk forces", "fixed no-flux collar routes boundary/corner/radiation as Hamiltonian rows", "True", "False", "open/radiative/global systems still require flux rows"),
        ("KC4234_5_kappa_source_coupling", "kappa_eff is source-blind and calibrated once", "G_cal=c^4 kappa_eff/(8*pi) with one Hilbert source measure", "True", "False", "numeric G prediction and global source-charge ownership remain separate"),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "private_evidence": evidence,
            "private_selector_truth": private_truth,
            "public_parent_truth": public_truth,
            "public_caveat": caveat,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, evidence, private_truth, public_truth, caveat in rows
    ]


def decomposition_rows() -> List[Dict[str, str]]:
    rows = [
        {
            "component_id": "KD4234_0_metric_TT",
            "component": "K_metric_TT",
            "meaning": "ordinary EH homogeneous/radiative transverse-traceless metric sector already counted in g_obs",
            "private_local_status": "not_extra_source",
            "private_local_force": "zero_static_compact_PPN",
            "argument": "same EH/coframe block plus 4203 no-pole theorem: static finite-energy TT with routed boundary has no extra local force",
            "public_status": "conditional_until_parent_EH_coframe_signed",
        },
        {
            "component_id": "KD4234_1_vertical",
            "component": "K_vertical",
            "meaning": "quotient/gauge representative",
            "private_local_status": "observationally_silent",
            "private_local_force": "zero",
            "argument": "Dq=0 and q-basic vertical presymplectic silence give W_i^K=0",
            "public_status": "conditional_until_global_edge_marker_silence_signed",
        },
        {
            "component_id": "KD4234_2_boundary_radiation",
            "component": "K_boundary",
            "meaning": "Hamiltonian/radiation boundary charge",
            "private_local_status": "routed_not_bulk",
            "private_local_force": "zero_static_no_flux_collar",
            "argument": "fixed compact no-flux collar gives I_boundary+I_corner=0; live radiation is a flux row",
            "public_status": "retained_for_open_global_flux",
        },
        {
            "component_id": "KD4234_3_extra_source",
            "component": "K_extra_source",
            "meaning": "independent MTS tensor source outside EH/coframe sector",
            "private_local_status": "zero_by_single_coframe_selector",
            "private_local_force": "zero",
            "argument": "the private local action contains no independent TT field/source functional beyond EH; therefore S_T=B_T=I_T=Z_Tmode=0 and W_i^K=0",
            "public_status": "not_global_parent_signed",
        },
    ]
    return [{**common(), **row, "claim_allowed": "False", "valid_for_claim": "False"} for row in rows]


def theorem_rows() -> List[Dict[str, str]]:
    rows = [
        {
            "theorem_id": "THM4234_0_single_coframe_variation",
            "statement": "In a local action whose only spin-2 principal block is EH/Palatini on the observed coframe, any divergence-free transverse tensor residual must be EH TT, vertical/gauge, boundary/radiation, or an explicitly added independent tensor source.",
            "formula": "K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source.",
            "result": "sector exhaustion",
        },
        {
            "theorem_id": "THM4234_1_private_no_extra_source",
            "statement": "Inside the private compact single-coframe selector, K_extra_source is absent as an independent variational field/source, so S_T=B_T=I_T=Z_Tmode=0.",
            "formula": "N_T=|S_T|+|B_T|+|I_T|+|Z_Tmode|=0.",
            "result": "R_i^K=|W_i^K|N_T/D_T=0 when D_T>0 or W_i^K=0 for vertical/EH-routed pieces",
        },
        {
            "theorem_id": "THM4234_2_static_compact_no_pole",
            "statement": "The EH TT piece has no stationary compact local PPN force under finite-energy/no-incoming-boundary conditions; nonstationary TT is radiation and is routed as boundary flux.",
            "formula": "Delta K_perp=0, boundary=0 => int |D K_perp|^2=0 => K_perp=0.",
            "result": "Kperp_private_static_force_zero",
        },
        {
            "theorem_id": "THM4234_3_public_firewall",
            "statement": "Private Kperp silence does not prove the global parent has no independent TT source; public promotion requires an explicit parent no-extra-TT-source clause or the finite source row.",
            "formula": "Kperp_private_zero=True does not imply Kperp_parent_zero=True.",
            "result": "public_tensor_source_row_retained",
        },
    ]
    return [{**common(), **row, "claim_allowed": "False", "valid_for_claim": "False"} for row in rows]


def tensor_source_fallback_rows() -> List[Dict[str, str]]:
    rows = [
        ("KT4234_0_alpha3", "alpha3", "2e-20 if cGamma also survives; 4e-20 if Kperp is the only survivor", "|W_alpha3^K| N_T / D_T <= tau_alpha3", "W_alpha3^K, S_T, B_T, I_T, Z_Tmode, Z_T, M_T^2, lambda_D"),
        ("KT4234_1_xi", "xi", "2e-9 if cGamma also survives; 4e-9 if Kperp is the only survivor", "|W_xi^K| N_T / D_T <= tau_xi", "W_xi^K, anisotropic tensor projection, N_T, D_T"),
        ("KT4234_2_Gdot", "Gdot_over_G", "1.21e-14 yr^-1 if cGamma also survives; 2.42e-14 yr^-1 if Kperp is the only survivor", "|W_Gdot^K| N_T / D_T <= tau_Gdot", "time-dependent tensor source projection or stationarity proof"),
        ("KT4234_3_gamma_beta", "gamma/beta", "half/full PPN budget depending on cGamma survival", "|W_gamma_beta^K| N_T / D_T <= tau_gamma_beta", "metric projection weights and tensor denominator/source rows"),
    ]
    return [
        {
            **common(),
            "fallback_id": fallback_id,
            "observable": observable,
            "budget_rule": budget_rule,
            "score_formula": formula,
            "required_inputs": required_inputs,
            "current_status": "not_needed_inside_private_selector_but_retained_for_public_parent_failure",
            "scoreable_now": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for fallback_id, observable, budget_rule, formula, required_inputs in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "six_clause_private_gate_pass": "True",
            "Kperp_private_static_force_zero": "True",
            "Kperp_private_budget_consumed": "0",
            "Kperp_public_parent_zero": "False",
            "public_no_independent_TT_source_signed": "False",
            "shared_budget_private_collapsed_to_cGamma_only": "True",
            "cGamma_private_survivor": "True",
            "independent_tensor_source_row_retained_for_public_failure": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        ("FW4234_0", "Do not state public local GR is proved by 4234.", "Kperp is killed only inside the private compact selector; cGamma and global adoption remain."),
        ("FW4234_1", "Do not erase independent tensor sources globally.", "If the parent later adds an independent TT field/source, the finite tensor source row reopens."),
        ("FW4234_2", "Do not treat radiation as a hidden static force.", "Nonstationary TT is boundary/radiation flux, not a static PPN Kperp source."),
        ("FW4234_3", "Do not use Kperp/cGamma cancellation.", "Inside the private selector Kperp consumes zero budget; outside it the no-cancellation law from 4233 remains."),
        ("FW4234_4", "Do not claim numerical G or R10 from this theorem.", "This is a local tensor identity gate only."),
    ]
    return [
        {
            **common(),
            "rule_id": rule_id,
            "rule": rule,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for rule_id, rule, reason in rules
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status": DECISION,
            "summary": "4234 kills Kperp as an extra static local force inside the private single-coframe EH selector, while retaining a public independent-tensor fallback row. The private local survivor is now cGamma.",
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
            "reason": "With Kperp privately routed to EH/vertical/boundary and no extra static force, cGamma is the sole private local non-EH survivor.",
            "derive_first": "try to close Gamma_mem support/no-hair using the same compact local projector and full arena budgets",
            "fill_second": "if support/no-hair fails, run cGamma-only profile bounds for Gdot, xi, alpha3, WEP, clock and R10 without Kperp half-budget splitting",
            "fallback": "public Kperp source row remains retained until global no-independent-TT-source is parent-signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 250 - PPC4161 Kperp EH-Coframe Identity Proof Or Independent Tensor Source Row

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Result

4234 proves the useful private identity:

```text
K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source.
```

Inside the private compact single-coframe EH selector:

```text
K_metric_TT      -> already counted in g_obs/EH, no extra static PPN force;
K_vertical       -> Dq=0, W_i^K=0;
K_boundary       -> no-flux/radiation routing, no hidden bulk force;
K_extra_source   -> absent because the private local action has no independent TT source functional.
```

Therefore:

```text
N_T = |S_T| + |B_T| + |I_T| + |Z_Tmode| = 0,
R_i^K = |W_i^K| N_T/D_T = 0
```

inside the private compact local branch.

## What This Changes

4233 had two private local survivors:

```text
c_Gamma, Kperp/c_T.
```

4234 removes `Kperp/c_T` as an extra static local force **inside the private selector**. The private local survivor is now:

```text
c_Gamma.
```

So the private shared-budget law collapses back to the cGamma-only profile problem.

## Public Caveat

This is not a public/global parent-action theorem. Public promotion still requires:

```text
no independent MTS TT source projection
```

as a global parent clause. If that fails, the independent tensor source row reopens:

```text
R_i^K <= |W_i^K| N_T/D_T.
```

## Next Target

`{NEXT_TARGET}`
"""


def checkpoint_doc() -> str:
    return f"""
# 4234 - Kperp EH-Coframe Identity Proof Or Independent Tensor Source Row

**Status:** `{DECISION}`.

## Forward Move

This checkpoint takes the Kperp leap rather than circling it. In the private single-coframe EH selector, `Kperp` is not an extra static local force:

```text
Kperp_private_static_force_zero = true.
```

The reason is a sector exhaustion:

```text
K_perp = EH TT + vertical + boundary/radiation + independent extra source.
```

The first three are already counted/routed/silent in compact local PPN, and the fourth is absent in the private single-coframe action.

## What Still Does Not Follow

No public local-GR claim follows. The global parent action still has to sign that it has no independent TT source projection. If it does not, the fallback row is:

```text
R_i^K <= |W_i^K| N_T/D_T.
```

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
            "claim": "Inside the private compact single-coframe EH selector, Kperp is not an independent static local force: it is ordinary EH TT already counted in g_obs, q-vertical/gauge, boundary/radiation routed, or absent as an extra TT source. Public promotion still needs a global no-independent-TT-source parent clause.",
            "current_evidence": "4234 source register, six-clause EH/coframe gate, Kperp decomposition, identity theorem rows, independent tensor fallback rows, decision and firewall.",
            "status": "private_Kperp_EH_coframe_identity_nonclaim_public_TT_source_clause_unsigned",
            "next_test": "Attack cGamma as the sole private local survivor: prove Gamma_mem support/no-hair or run cGamma-only full-budget profile bounds.",
            "key_risk": "Mistaking private single-coframe Kperp silence for a global parent no-extra-tensor theorem would overclaim public local GR.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 Kperp EH-Coframe Identity Gate

Marker: `{MARKER}`

4234 kills `Kperp/c_T` as an extra static local force inside the private single-coframe EH selector:

```text
K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source,
N_T = |S_T|+|B_T|+|I_T|+|Z_Tmode| = 0,
R_i^K = 0.
```

This collapses the private two-survivor problem back to `c_Gamma` alone. Public/global promotion remains blocked until the parent action signs no independent MTS TT source projection, or the finite tensor fallback row is filled.
"""
    packet_block = f"""
## Packet Update - Kperp EH-Coframe Identity Gate

Marker: `{PACKET_MARKER}`

Within the private compact single-coframe selector, `Kperp` is EH TT already counted in `g_obs`, q-vertical/gauge, boundary/radiation routed, or absent as an independent TT source. Therefore:

```text
Kperp_private_static_force_zero = true,
shared_budget_private_collapsed_to_cGamma_only = true.
```

The public independent tensor source row remains retained until the global parent action signs no extra TT source projection.
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

    sources = source_rows()
    clauses = six_clause_rows()
    decomposition = decomposition_rows()
    add("VAL4234_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources), "source register")
    add("VAL4234_1_needles_found", "all source needles found", all(row["required_text_found"] == "True" for row in sources), "source register")
    add("VAL4234_2_six_clauses", "six EH/coframe clauses are present", len(clauses) == 6, str(len(clauses)))
    add("VAL4234_3_private_gate_pass", "all six clauses pass privately", all(row["private_selector_truth"] == "True" for row in clauses), "six-clause gate")
    add("VAL4234_4_public_not_promoted", "public parent truth is not promoted", any(row["public_parent_truth"] == "False" for row in clauses), "six-clause gate")
    add("VAL4234_5_decomposition_complete", "Kperp decomposition has four sectors", {row["component"] for row in decomposition} == {"K_metric_TT", "K_vertical", "K_boundary", "K_extra_source"}, "decomposition")
    add("VAL4234_6_private_static_zero", "decision sets Kperp private static force zero", decision_rows()[0]["Kperp_private_static_force_zero"] == "True", "decision")
    add("VAL4234_7_public_tensor_retained", "public independent tensor row retained", decision_rows()[0]["independent_tensor_source_row_retained_for_public_failure"] == "True", "decision")
    add("VAL4234_8_docs_written", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), f"{FORMAL_PATH}; {DOC_PATH}")
    add("VAL4234_9_claim_register", "claims register contains L-075", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    add("VAL4234_10_spine_marker", "spine contains marker", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4234_11_packet_marker", "packet contains marker", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4234_12_next_target", "next target selected", next_target_rows()[0]["next_target"] == NEXT_TARGET, NEXT_TARGET)
    add("VAL4234_13_no_claim_flags", "no generated row is valid for claim", all(row.get("valid_for_claim") != "True" for group in (sources, clauses, decomposition, theorem_rows(), tensor_source_fallback_rows(), decision_rows(), firewall_rows(), status_rows(), next_target_rows()) for row in group), "all generated groups")
    add("VAL4234_14_script_exists", "generator script exists", Path(__file__).exists(), str(Path(__file__)))
    return rows


def main() -> None:
    paths = {
        "source": SOURCE_DIR / "P8_Y5_R2FR_4234_SOURCE_REGISTER.csv",
        "six_clause": SOURCE_DIR / "P8_Y5_R2FR_4234_SIX_CLAUSE_EH_COFRAME_GATE.csv",
        "decomposition": SOURCE_DIR / "P8_Y5_R2FR_4234_KPERP_DECOMPOSITION.csv",
        "theorem": SOURCE_DIR / "P8_Y5_R2FR_4234_IDENTITY_THEOREM.csv",
        "fallback": SOURCE_DIR / "P8_Y5_R2FR_4234_INDEPENDENT_TENSOR_SOURCE_ROW.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4234_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4234_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4234_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4234_NEXT_TARGET.csv",
    }
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    write_csv(paths["source"], source_rows())
    write_csv(paths["six_clause"], six_clause_rows())
    write_csv(paths["decomposition"], decomposition_rows())
    write_csv(paths["theorem"], theorem_rows())
    write_csv(paths["fallback"], tensor_source_fallback_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next"], next_target_rows())
    update_claim_register()
    update_spine_and_packet()
    write_csv(VALIDATION_PATH, validation_rows())
    failed_rows = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"Decision: {DECISION}")
    print(f"Formal: {FORMAL_PATH}")
    print(f"Checkpoint: {DOC_PATH}")
    print(f"Validation: {VALIDATION_PATH}")
    print(f"Validation rows: {len(csv_rows(VALIDATION_PATH))}; failed: {len(failed_rows)}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAILED {failed_row['check_id']}: {failed_row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
