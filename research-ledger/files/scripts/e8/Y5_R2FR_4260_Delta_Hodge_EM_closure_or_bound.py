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

CHECKPOINT = "4260"
CLAIM_ID = "L-101"
BRANCH = "MTS_R2FR_Y5_DELTA_HODGE_EM_CLOSURE_OR_BOUND_4260"
DECISION = "DELTA_HODGE_EM_UNIQUENESS_LEMMA_SIGNED_ACTION_DOMAIN_AND_CONSTITUTIVE_ABSENCE_UNSIGNED_BOUND_TEMPLATE_WRITTEN_NONCLAIM"
MARKER = "PPC4161_DELTA_HODGE_EM_CLOSURE_OR_BOUND_4260"
PACKET_MARKER = "PPC4161_PACKET_DELTA_HODGE_EM_CLOSURE_OR_BOUND_4260"
NEXT_TARGET = "4261-Y5-R2FR-sign-visible-EM-action-domain-or-fill-constitutive-bound-row.md"

FORMAL_PATH = FORMAL / "276-PPC4161-Delta-Hodge-EM-closure-or-bound.md"
DOC_PATH = POST / "4260-Y5-R2FR-Delta-Hodge-EM-closure-or-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4260_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4260_00_224_doc": SourceSpec(
        "SRC4260_00_224_doc",
        FORMAL / "224-PPC4161-Hodge-deformation-zero-or-constitutive-bound.md",
        "The no-cancellation envelope is:",
        "4208 Hodge zero and constitutive bound statement.",
    ),
    "SRC4260_01_4208_contract": SourceSpec(
        "SRC4260_01_4208_contract",
        SOURCE_DIR / "P8_Y5_R2FR_4208_HODGE_ZERO_CONTRACT.csv",
        "HZ4208_2_visible_EM_action_domain",
        "Clause-level Hodge zero contract.",
    ),
    "SRC4260_02_4208_decomposition": SourceSpec(
        "SRC4260_02_4208_decomposition",
        SOURCE_DIR / "P8_Y5_R2FR_4208_CONSTITUTIVE_DECOMPOSITION.csv",
        "Delta_chi_principal",
        "Constitutive subcomponent vector.",
    ),
    "SRC4260_03_4259_vector": SourceSpec(
        "SRC4260_03_4259_vector",
        SOURCE_DIR / "P8_Y5_R2FR_4259_EM_VISIBLE_RESIDUAL_VECTOR.csv",
        "PRIORITY_ZERO_OR_BOUND_SUBTARGET",
        "4259 made Delta_Hodge_EM the priority EM subgate.",
    ),
    "SRC4260_04_198_AMF": SourceSpec(
        "SRC4260_04_198_AMF",
        FORMAL / "198-PPC4161-motion-frame-symmetry-parent-signature-gate.md",
        "A_MF_PARENT_SIGNATURE_NOT_FOUND",
        "Current observed-coframe ownership remains nonclaim globally.",
    ),
    "SRC4260_05_202_same_coframe": SourceSpec(
        "SRC4260_05_202_same_coframe",
        FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md",
        "single observed coframe + Hilbert source descent + Maxwell-Hodge owner",
        "Private same-coframe zero law compatibility.",
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
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if CLAIM_ID in text:
        return
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = next(csv.reader(handle))
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": (
            "4260 attacks Delta_Hodge_EM. It signs only the mathematical Hodge uniqueness lemma once g_obs, "
            "orientation, and observed coframe are fixed, while leaving the parent-visible Maxwell action domain "
            "and absence of independent chi_EM/constitutive channels unsigned. A no-cancellation bound template "
            "is written; no Hodge-zero claim is made."
        ),
        "current_evidence": (
            "4260 source register, Hodge closure audit, Hodge theorem rows, constitutive subvector, bound template, "
            "decision and firewall."
        ),
        "status": "private_Delta_Hodge_uniqueness_signed_action_domain_unsigned_nonclaim",
        "next_test": "Sign visible EM action domain or fill constitutive bound rows.",
        "key_risk": "Using mathematical Hodge uniqueness as if it also proved the parent EM action has no chi_EM side-channel.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


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
                "valid_for_claim": "False",
            }
        )
    return rows


def hodge_closure_audit_rows() -> List[Dict[str, str]]:
    source_contract = csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4208_HODGE_ZERO_CONTRACT.csv")
    status_by_contract = {row.get("contract_id", ""): row.get("status", "") for row in source_contract}
    clauses = [
        (
            "HC4260_0_observed_coframe",
            "e_obs, g_obs, vol_obs, orientation descend through q before EM variation",
            status_by_contract.get("HZ4208_0_observed_coframe", "MISSING_CONTRACT"),
            "needed for observed Hodge star",
        ),
        (
            "HC4260_1_Hodge_uniqueness",
            "observed metric plus orientation uniquely determine *_obs on two-forms",
            status_by_contract.get("HZ4208_1_Hodge_uniqueness", "MISSING_CONTRACT"),
            "mathematical lemma is signed",
        ),
        (
            "HC4260_2_visible_action_domain",
            "parent-visible EM action uses only F wedge *_obs F before variation",
            status_by_contract.get("HZ4208_2_visible_EM_action_domain", "MISSING_CONTRACT"),
            "needed to remove independent chi_EM",
        ),
        (
            "HC4260_3_constitutive_absence",
            "no independent principal/skewon/hidden/readout constitutive tensor",
            status_by_contract.get("HZ4208_3_constitutive_absence", "MISSING_CONTRACT"),
            "needed for Delta_Hodge_EM=0",
        ),
        (
            "HC4260_4_axion_gradient",
            "active axion/topological gradients are absent or boundary-routed",
            status_by_contract.get("HZ4208_4_axion_guard", "MISSING_CONTRACT"),
            "prevents F wedge F shortcut",
        ),
        (
            "HC4260_5_readout_guard",
            "post-solution readout does not regenerate Hodge/alpha dependence",
            status_by_contract.get("HZ4208_6_readout_before_variation", "MISSING_CONTRACT"),
            "protects spectroscopy/clock side-channel",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "source_status": status,
            "role": role,
            "closure_effect": "Delta_Hodge_EM_zero_if_all_zero_clauses_signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, status, role in clauses
    ]


def theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DH4260_0_unique_hodge",
            "Hodge uniqueness lemma",
            "Given g_obs, orientation, and volume form, alpha wedge *_obs beta = <alpha,beta>_g_obs vol_obs uniquely fixes *_obs.",
            "SIGNED_MATHEMATICAL_LEMMA",
            "Does not by itself prove parent-visible EM action uses *_obs.",
        ),
        (
            "DH4260_1_zero_theorem",
            "Delta_Hodge zero theorem",
            "If the parent-visible EM action contains only F wedge *_obs F and forbids independent chi_EM, hidden/disformal EM metrics, skewon/dissipative pieces, active axion gradients, and readout-regenerated Hodge maps, then Delta_Hodge_EM=0.",
            "DERIVED_CONDITIONAL",
            "Blocked by unsigned action-domain and constitutive-absence clauses.",
        ),
        (
            "DH4260_2_bound_law",
            "Delta_Hodge bound law",
            "||Delta_Hodge_EM|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||d theta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|.",
            "SOURCE_BACKED_BOUND_FORM",
            "No cancellation between constitutive subpieces.",
        ),
        (
            "DH4260_3_scale_guard",
            "conformal/scale guard",
            "In four dimensions the Hodge star on two-forms is conformally invariant, so Hodge closure does not fix Z_Q, mu0, alpha_EM, charge normalization, source mass, or G_N.",
            "NO_SMUGGLE_GUARD",
            "Prevents fake EM unification claims.",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "name": name,
            "statement": statement,
            "status": status,
            "guard": guard,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, name, statement, status, guard in raw
    ]


def constitutive_subvector_rows() -> List[Dict[str, str]]:
    source_rows_4208 = csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4208_CONSTITUTIVE_DECOMPOSITION.csv")
    output: List[Dict[str, str]] = []
    for row in source_rows_4208:
        coefficient = row.get("coefficient", "")
        if coefficient in {"Delta_Hodge_EM", "Delta_conformal_scale"}:
            continue
        output.append(
            {
                **common(),
                "component_id": row.get("component_id", ""),
                "coefficient": coefficient,
                "definition": row.get("definition", ""),
                "physical_effect": row.get("physical_effect", ""),
                "status": "RETAINED_HODGE_SUBCOMPONENT",
                "feeds": "Delta_Hodge_EM",
                "numeric_value": "MISSING",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return output


def bound_template_rows(subvector: List[Dict[str, str]]) -> List[Dict[str, str]]:
    rows = []
    for subrow in subvector:
        rows.append(
            {
                **common(),
                "candidate_id": "TEMPLATE_ONLY",
                "coefficient": subrow["coefficient"],
                "required_value": "MISSING_SOURCE_BACKED_NONNEGATIVE_BOUND_OR_THEOREM_ZERO",
                "units": "dimensionless_Hodge_operator_norm_or_normalized_component",
                "source_path": "MISSING_SOURCE_PATH",
                "zero_proof_path": "MISSING_ZERO_PROOF_PATH_IF_ZERO",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            **common(),
            "candidate_id": "TEMPLATE_ONLY",
            "coefficient": "Delta_Hodge_EM_total",
            "required_value": "SUM_ABS_OF_SUBCOMPONENTS",
            "units": "dimensionless_Hodge_operator_norm",
            "source_path": str(FORMAL_PATH),
            "zero_proof_path": "ALL_SUBCOMPONENTS_ZERO_OR_BOUNDED",
            "valid_for_claim": "False",
        }
    )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4260_0_lemma_signed",
            "The mathematical Hodge uniqueness lemma is signed.",
            "Once g_obs and orientation are fixed, *_obs is not an extra freedom.",
            "Do not confuse this with parent EM action ownership.",
        ),
        (
            "DEC4260_1_real_blocker",
            "The real blocker is visible EM action-domain ownership plus absence of independent chi_EM/constitutive tensors.",
            "This is exactly the gap between geometry and EM material law.",
            NEXT_TARGET,
        ),
        (
            "DEC4260_2_bound_ready",
            "A no-cancellation Delta_Hodge_EM bound template now exists.",
            "This gives an empirical fallback if action-domain closure fails.",
            "Fill component bounds or prove zeros one coefficient at a time.",
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4260_0_uniqueness_overclaim", "using Hodge uniqueness to assert the parent action has no independent chi_EM", "VISIBLE_EM_ACTION_DOMAIN_REQUIRED"),
        ("FW4260_1_gauge_overclaim", "using gauge covariance to kill skewon/principal/hidden/readout constitutive pieces", "CONSTITUTIVE_ABSENCE_REQUIRED"),
        ("FW4260_2_axion", "ignoring active axion-gradient or orientation flux terms", "AXION_ORIENTATION_BOUNDARY_ROUTE_REQUIRED"),
        ("FW4260_3_scale", "claiming alpha_EM/source normalization from Hodge closure", "SCALE_OWNER_GATE_SEPARATE"),
        ("FW4260_4_cancellation", "letting Hodge subcomponents cancel", "SUM_ABS_BOUND_REQUIRED"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden,
            "required_gate": gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, gate in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4260_0",
            "summary": (
                "4260 signs Hodge uniqueness as mathematics, but keeps Delta_Hodge_EM open until the parent-visible "
                "EM action domain and constitutive absence are signed or bounded."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": (
                "Sign that visible EM uses only F wedge *_obs F with no independent chi_EM, or fill the "
                "Delta_Hodge_EM subcomponent bound template."
            ),
            "avoid": "Do not infer EM action-domain ownership from Hodge uniqueness alone.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 276 - PPC4161 Delta-Hodge-EM closure or bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4260 does not prove `Delta_Hodge_EM=0`, `Dq_EM[Hperp]=0`, Maxwell derivation, alpha prediction, local GR, PPN, R10, or clock safety. It separates the signed mathematical lemma from the unsigned parent-action clauses.

## Signed mathematical lemma

Once `g_obs`, orientation, and volume form are fixed:

```text
alpha wedge *_obs beta = <alpha,beta>_g_obs vol_obs.
```

So the observed Hodge star `*_obs` is unique. This part is mathematics, not speculation.

## Unsigned parent-action clauses

The zero:

```text
Delta_Hodge_EM = 0
```

requires more than Hodge uniqueness. It requires:

```text
S_EM = -(4 mu0)^-1 int F wedge *_obs F,
no independent chi_EM,
no hidden/disformal EM metric,
no skewon/dissipative constitutive piece,
no active axion-gradient bulk term,
no readout-regenerated Hodge map.
```

Current source status keeps those action-domain/constitutive clauses unsigned.

## Bound route

If closure fails, retain:

```text
||Delta_Hodge_EM||
<= ||Delta_chi_principal||
 + ||Delta_chi_skewon||
 + L||d theta_EM||
 + |C_Hodge_hidden|
 + |C_Hodge_readout|
 + |Delta_orientation_flux|.
```

No cancellation between terms is allowed.

## Scale guard

In four dimensions the Hodge star on two-forms is conformally invariant. Therefore Hodge closure does not derive:

```text
Z_Q, mu0, alpha_EM, charge/current normalization, source mass, G_N.
```

Those remain separate source-scale gates.

## Next target

`{NEXT_TARGET}` should either sign the visible EM action-domain clause or fill the constitutive subcomponent bound rows.
"""


def checkpoint_doc() -> str:
    return f"""
# 4260 - Y5 R2FR Delta-Hodge-EM closure or bound

Packet marker: `{PACKET_MARKER}`

## Result

4260 attacks `Delta_Hodge_EM`.

What is genuinely signed:

```text
g_obs + orientation => unique *_obs.
```

What remains unsigned:

```text
parent-visible EM action domain,
absence of independent chi_EM / constitutive tensor,
readout/Hodge regeneration,
active axion-gradient and orientation flux.
```

## Claim status

Private nonclaim. The branch now has a sharper Hodge bound template, not a Hodge-zero pass.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    audit = csv_rows(paths["audit"])
    theorems = csv_rows(paths["theorems"])
    subvector = csv_rows(paths["subvector"])
    template = csv_rows(paths["template"])
    rows = [
        ("VAL4260_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4260_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        ("VAL4260_2_uniqueness_signed", any(row["status"] == "SIGNED_MATHEMATICAL_LEMMA" for row in theorems), "Hodge uniqueness lemma emitted"),
        ("VAL4260_3_unsigned_clauses", any("unsigned" in row["source_status"] for row in audit), "unsigned action-domain clauses remain explicit"),
        ("VAL4260_4_bound_law", any(row["theorem_id"] == "DH4260_2_bound_law" for row in theorems), "bound law emitted"),
        ("VAL4260_5_subvector_rows", len(subvector) >= 5, "constitutive subvector emitted"),
        ("VAL4260_6_template_nonclaim", bool(template) and all(row["valid_for_claim"] == "False" for row in template), "bound template stays nonclaim"),
        ("VAL4260_7_no_fake_zero", all(row["required_value"] != "0" for row in template), "no Hodge zero fabricated"),
        ("VAL4260_8_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4260_9_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4260_10_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in rows
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4260_SOURCE_REGISTER.csv"
    audit_path = SOURCE_DIR / "P8_Y5_R2FR_4260_HODGE_CLOSURE_AUDIT.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4260_HODGE_THEOREMS.csv"
    subvector_path = SOURCE_DIR / "P8_Y5_R2FR_4260_DELTA_HODGE_SUBVECTOR.csv"
    template_path = SOURCE_DIR / "P8_Y5_R2FR_4260_DELTA_HODGE_BOUND_TEMPLATE.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4260_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4260_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4260_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4260_NEXT_TARGET.csv"

    subvector = constitutive_subvector_rows()
    write_csv(source_path, source_rows())
    write_csv(audit_path, hodge_closure_audit_rows())
    write_csv(theorem_path, theorem_rows())
    write_csv(subvector_path, subvector)
    write_csv(template_path, bound_template_rows(subvector))
    write_csv(decision_path, decision_rows())
    write_csv(firewall_path, firewall_rows())
    write_csv(status_path, status_rows())
    write_csv(next_path, next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()

    paths = {
        "sources": source_path,
        "audit": audit_path,
        "theorems": theorem_path,
        "subvector": subvector_path,
        "template": template_path,
    }
    validation = validation_rows(paths)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 10 csv artifacts")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()
