from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4180"
BRANCH_ID = "MTS_R2FR_Y5_MINIMAL_PARENT_ACTION_ADOPTION_MATRIX_4180"
DECISION = "MINIMAL_PARENT_ACTION_CANDIDATE_AND_ADOPTION_MATRIX_WRITTEN_UNSIGNED_CLAUSES_DEMOTED"
DOC_PATH = POST / "4180-Y5-R2FR-minimal-parent-action-adoption-matrix-or-closure-demotion-ledger.md"
FORMAL_196_PATH = FORMAL / "196-PPC4161-minimal-parent-action-adoption-matrix.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-021"
SPINE_MARKER = "PPC4161_MINIMAL_PARENT_ACTION_ADOPTION_MATRIX_4180"
PACKET_MARKER = "PPC4161_PACKET_MINIMAL_PARENT_ACTION_ADOPTION_MATRIX_4180"
NEXT_TARGET = "4181-Y5-R2FR-EH-local-metric-principal-block-origin-or-effective-GR-demotion.md"

SOURCES = {
    "SRC4180_00_4179_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4179_NEXT_TARGET.csv",
        "minimal parent action/adoption matrix",
        "4179 handoff to minimal parent action adoption matrix.",
    ),
    "SRC4180_01_4179_burden": (
        SOURCE_DIR / "P8_Y5_R2FR_4179_PARENT_ADOPTION_BURDEN_MAP.csv",
        "EH/local metric principal block",
        "4179 parent adoption burden rows.",
    ),
    "SRC4180_02_formal_195": (
        FORMAL / "195-PPC4161-local-GR-private-closure-summary-and-parent-adoption-burden-map.md",
        "Parent Adoption Burden",
        "formal closure/burden map.",
    ),
    "SRC4180_03_formal_184": (
        FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md",
        "S_top^kappa",
        "topological kappa action candidate.",
    ),
    "SRC4180_04_formal_185": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "S_src = S_matter",
        "Hilbert source action candidate.",
    ),
    "SRC4180_05_formal_191": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "S_MH[A,g_obs]",
        "Maxwell-Hodge action candidate.",
    ),
    "SRC4180_06_formal_192": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_side[tau] = 0",
        "boundary/no-flux selector condition.",
    ),
    "SRC4180_07_formal_193": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "q: Conf_parent -> Q_obs",
        "quotient naturality selector condition.",
    ),
    "SRC4180_08_formal_194": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "numeric(G_cal) = empirical calibration",
        "calibrated G firewall.",
    ),
    "SRC4180_09_claim_L020": (
        CLAIMS_PATH,
        "global parent-adoption burden map",
        "latest claim-register row before parent matrix.",
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


def action_term_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PAT4180_0_EH",
            "EH/Palatini local metric block",
            "S_EH[g_obs;kappa_*]=(2 kappa_*)^-1 int sqrt(-g_obs) R[g_obs]",
            "bulk_action_term",
            "global_parent_origin_unsigned",
            "must derive why the MTS parent selects EH principal block and not merely append GR",
        ),
        (
            "PAT4180_1_kappa_top",
            "topological kappa lock",
            "S_top^kappa=C_top int A_3 wedge d ln(kappa_*/kappa_0)",
            "topological_action_term",
            "parent_adoptable_candidate",
            "locks local coupling drift but not numerical G",
        ),
        (
            "PAT4180_2_Hilbert_source",
            "single Hilbert source functor",
            "S_src=S_matter[psi,g_obs,theta(q)]+S_MH[A,g_obs]+S_binding+dB_impr+S_rest^top/zero",
            "source_action_term",
            "parent_adoptable_candidate",
            "one source measure prevents species/readout/range multipliers",
        ),
        (
            "PAT4180_3_Maxwell_Hodge",
            "Maxwell-Hodge EM subblock",
            "S_MH[A,g_obs]=-(1/4) int sqrt(-g_obs) F_mu_nu F^mu_nu",
            "source_action_subblock",
            "parent_adoptable_candidate",
            "Poynting is T_EM flux counted once",
        ),
        (
            "PAT4180_4_boundary_charge",
            "Hamiltonian boundary charge",
            "delta H_tau=int_partialW(delta Q_tau-i_tau theta_total)",
            "covariant_phase_space_boundary_term",
            "parent_adoptable_with_boundary_conditions",
            "mass readout is Hamiltonian/worldtube charge, not fitted GM",
        ),
        (
            "PAT4180_5_quotient_functor",
            "quotient-natural readout functor",
            "q:Conf_parent->Q_obs, O_loc=Obar_loc o q, S_matter=Sbar[psi,g_obs(q),A(q),theta(q)]",
            "functorial_domain_restriction",
            "adoption_axiom_not_bulk_term",
            "must be parent principle before variation, not post-readout projection",
        ),
        (
            "PAT4180_6_local_no_flux",
            "compact local no-flux collar",
            "F_side[tau]=0, J_tr^nu=0 through <=2PN",
            "domain_boundary_condition",
            "closure_or_superselection_condition",
            "not a universal bulk action term; needs domain/support theorem or remains closure",
        ),
        (
            "PAT4180_7_numeric_G",
            "dimensionful Newton constant scale",
            "numeric(G_cal) requires parent scale for kappa_*",
            "empirical_calibration_or_future_scale_law",
            "not_derived",
            "do not claim numerical G prediction",
        ),
    ]
    return [
        {
            **common(),
            "term_id": term_id,
            "term": term,
            "mathematical_form": form,
            "term_class": term_class,
            "adoption_status": status,
            "discipline_note": note,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for term_id, term, form, term_class, status, note in rows
    ]


def adoption_matrix_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "ADM4180_0_EH_origin",
            "EH/local metric principal block",
            "not_adopted_global",
            "hard_root",
            "derive from motion-frame/Palatini parent or demote local GR to effective-GR branch",
        ),
        (
            "ADM4180_1_kappa_top",
            "topological kappa lock",
            "adoptable_private_candidate",
            "medium",
            "retain as minimal topological sector; global adoption still must be justified",
        ),
        (
            "ADM4180_2_Hilbert_source",
            "single Hilbert source measure",
            "adoptable_private_candidate",
            "medium",
            "write source functor as parent rule; reject all independent source weights",
        ),
        (
            "ADM4180_3_Maxwell_Hodge",
            "Maxwell-Hodge EM stress",
            "adoptable_private_candidate",
            "low_medium",
            "standard same-metric EM action can be a parent subblock",
        ),
        (
            "ADM4180_4_Hamiltonian_charge",
            "Hamiltonian worldtube mass charge",
            "adoptable_given_covariant_boundary_conditions",
            "medium",
            "prove differentiable charge and reference choice are parent-owned",
        ),
        (
            "ADM4180_5_boundary_no_flux",
            "local boundary no-flux/routed charge",
            "closure_or_superselection_until_support_theorem",
            "high",
            "demote to domain selector unless parent derives support separation/radiation routing",
        ),
        (
            "ADM4180_6_quotient_naturality",
            "quotient naturality before variation",
            "adoption_axiom_or_closure_until_parent_category",
            "high",
            "derive parent q/category/functor or label as closure-only",
        ),
        (
            "ADM4180_7_numeric_G",
            "numerical G_N prediction",
            "not_adopted_empirical_calibration",
            "not_required_for_local_GR_but_required_for_numeric_prediction",
            "keep G_cal empirical unless parent scale law is derived",
        ),
        (
            "ADM4180_8_global_unification",
            "same parent owns galaxy/cosmology/time/EM/quantum sectors",
            "not_adopted_global",
            "global_goal",
            "future unification matrix must connect local selector to nonlocal sectors",
        ),
    ]
    return [
        {
            **common(),
            "adoption_id": adoption_id,
            "selector_clause": clause,
            "adoption_verdict": verdict,
            "risk_level": risk,
            "next_action": action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for adoption_id, clause, verdict, risk, action in rows
    ]


def demotion_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "DEM4180_0_EH",
            "EH/local metric block",
            "if not derived from parent motion-frame dynamics",
            "effective_GR_branch",
            "public MTS->GR derivation forbidden; use effective local GR limit language only",
        ),
        (
            "DEM4180_1_boundary",
            "boundary no-flux",
            "if support separation/routed charge is not parent-derived",
            "closure_only_domain_selector",
            "transition-current/boundary residuals remain named and bounded",
        ),
        (
            "DEM4180_2_quotient",
            "quotient naturality",
            "if parent q/category/functor is not derived",
            "closure_only_functor_axiom",
            "projector/shadow-frame/source-normalization residuals remain live",
        ),
        (
            "DEM4180_3_numeric_G",
            "numeric G_N",
            "unless parent scale law fixes kappa_*",
            "empirical_calibration",
            "safe GR-like calibrated coupling but no numerical prediction",
        ),
        (
            "DEM4180_4_global",
            "unified field theory completion",
            "until same parent action owns local, galaxy, cosmology, time and EM sectors",
            "programme_open",
            "do not present local packet as full theory completion",
        ),
    ]
    return [
        {
            **common(),
            "demotion_id": demotion_id,
            "object": obj,
            "trigger": trigger,
            "demoted_status": status,
            "allowed_language": language,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for demotion_id, obj, trigger, status, language in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "DEC4180_0_candidate_written",
            "minimal_parent_action_candidate_written",
            "A compact local parent candidate can be written from EH, kappa topological lock, Hilbert source, Maxwell-Hodge, Hamiltonian boundary charge and quotient functor restrictions.",
            "use as adoption target, not public theorem",
        ),
        (
            "DEC4180_1_hard_root",
            "EH_origin_is_next_hard_root",
            "Most other clauses are adoptable candidates or explicit closures; the central leap is deriving the EH/local metric principal block from MTS rather than appending GR.",
            NEXT_TARGET,
        ),
        (
            "DEC4180_2_public_status",
            "public_claim_still_false",
            "Boundary and quotient clauses remain closure/adoption clauses, numeric G is empirical, and global unification remains open.",
            "keep private selector language",
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in rows
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4180_0_no_public_local_GR", "Do not claim public local GR from a candidate parent-action matrix."),
        ("FW4180_1_no_append_GR_claim", "Do not append EH and call it derived from MTS."),
        ("FW4180_2_no_boundary_smuggle", "Do not treat local no-flux as a universal action term without support/routing proof."),
        ("FW4180_3_no_quotient_smuggle", "Do not treat quotient naturality as post-readout projection."),
        ("FW4180_4_no_numeric_G", "Do not claim numerical G_N prediction."),
        ("FW4180_5_no_unification_claim", "Do not claim global unified field theory completion."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "blocked_claim": blocked_claim,
            "enforcement": "claim_allowed=false_and_valid_for_claim=false",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, blocked_claim in rows
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "result": DECISION,
            "minimal_parent_action_candidate_written": "True",
            "adoption_matrix_written": "True",
            "closure_demotion_ledger_written": "True",
            "action_terms_count": "8",
            "adoption_rows_count": "9",
            "EH_origin_parent_derived": "False",
            "boundary_no_flux_parent_global_derived": "False",
            "quotient_naturality_parent_global_derived": "False",
            "numeric_G_predicted": "False",
            "public_local_GR_claim_allowed": "False",
            "global_parent_action_adoption_proved": "False",
            "formal_196_written": "True",
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
            "why_next": "4180 identifies the EH/local metric principal block as the hard root. The next step is to derive that block from MTS motion-frame/Palatini structure or explicitly demote the local branch to effective-GR closure.",
            "route_A": "derive same-frame EH/Palatini principal block from parent motion/coframe variables and show extra torsion/scalar/disformal modes are silent",
            "route_B": "if EH origin cannot be derived, label PPC4161 as an effective local-GR branch and keep parent unification work separate",
            "fallback": "continue empirical robustness only as tests of a closure branch, not as proof of MTS-to-GR derivation",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4180_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4180_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4180_MINIMAL_PARENT_ACTION_TERMS": SOURCE_DIR / "P8_Y5_R2FR_4180_MINIMAL_PARENT_ACTION_TERMS.csv",
        "P8_Y5_R2FR_4180_ADOPTION_MATRIX": SOURCE_DIR / "P8_Y5_R2FR_4180_ADOPTION_MATRIX.csv",
        "P8_Y5_R2FR_4180_CLOSURE_DEMOTION_LEDGER": SOURCE_DIR / "P8_Y5_R2FR_4180_CLOSURE_DEMOTION_LEDGER.csv",
        "P8_Y5_R2FR_4180_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4180_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4180_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4180_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4180_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4180_STATUS.csv",
        "P8_Y5_R2FR_4180_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4180_NEXT_TARGET.csv",
    }


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    fieldnames = list(rows[0].keys())
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "A minimal PPC4161 parent-action candidate and adoption matrix now classify local-GR selector clauses as action terms, boundary/domain closures, functorial adoption axioms, empirical calibration, or open global debts",
        "current_evidence": "formalization-workbench/196-PPC4161-minimal-parent-action-adoption-matrix.md records the candidate action skeleton, eight action/domain/functor terms, nine adoption verdicts, closure demotion ledger, EH-origin next target, and public-claim firewall; public_claim=false",
        "status": "private_minimal_parent_action_adoption_matrix_nonclaim_unsigned_clauses_demoted_public_claim_false",
        "next_test": "Derive the EH/local metric principal block from MTS motion-frame/Palatini structure or demote PPC4161 to effective-GR closure",
        "key_risk": "The matrix organizes adoption but does not prove EH origin, global boundary no-flux, global quotient naturality, numerical G_N, or unified parent action completion",
    }
    normalized_new = {field: new_row.get(field, "") for field in fieldnames}
    existing = [row for row in rows if row.get("claim_id") == CLAIM_ID]
    if existing:
        changed = False
        for row in rows:
            if row.get("claim_id") == CLAIM_ID:
                for field, value in normalized_new.items():
                    if row.get(field) != value:
                        row[field] = value
                        changed = True
        action = "updated" if changed else "already_present"
    else:
        rows.append(normalized_new)
        action = "added"
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return action


def append_once(path: Path, marker: str, section: str) -> str:
    text = read_text(path)
    if marker in text:
        return "already_present"
    path.write_text(text.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")
    return "added"


def ensure_packet_180_addendum() -> str:
    section = f"""
## PPC4161-TK-HQNP Addendum - Minimal Parent Action Adoption Matrix

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4180-Y5-R2FR-minimal-parent-action-adoption-matrix-or-closure-demotion-ledger.md`

Minimal local parent-action candidate:

```text
S_min|loc =
S_EH[g_obs;kappa_*]
+ S_top^kappa[A_3,u_kappa]
+ S_src[psi,A,g_obs(q),theta(q)]
+ boundary/Hamiltonian charge terms
+ q-owned topological/exact/silent rest.
```

But the adoption matrix keeps the sharp status:

```text
EH_origin_parent_derived = false
boundary_no_flux_parent_global_derived = false
quotient_naturality_parent_global_derived = false
numeric_G_predicted = false
public_local_GR_claim = false
```

Next hard root: derive the EH/local metric principal block from MTS, or demote the local branch to effective-GR closure.
"""
    return append_once(PACKET_180_PATH, PACKET_MARKER, section)


def ensure_spine_section() -> str:
    section = f"""
## PPC4161 Minimal Parent Action Adoption Matrix - 4180

Marker: `{SPINE_MARKER}`  
Source bridge: `196-PPC4161-minimal-parent-action-adoption-matrix.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4180` classifies the local selector clauses:

```text
bulk action candidates: EH, topological kappa, Hilbert source, Maxwell-Hodge;
boundary/domain clauses: Hamiltonian charge, no-flux collar;
functorial clauses: quotient naturality and source-label forgetting;
calibration: numeric G remains empirical;
global debt: same parent must own galaxy/cosmology/time/global sectors.
```

The central hard root is now explicit:

```text
{NEXT_TARGET}
```
"""
    return append_once(SPINE_PATH, SPINE_MARKER, section)


def write_formal_196() -> None:
    FORMAL_196_PATH.write_text(
        f"""# 196 - PPC4161 Minimal Parent Action Adoption Matrix

Marker: `PPC4161_MINIMAL_PARENT_ACTION_ADOPTION_MATRIX`
Checkpoint: `4180`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status
Private adoption matrix. This is not a public local-GR theorem and not global MTS parent-action adoption.

## Minimal Local Candidate

```text
S_min|loc =
S_EH[g_obs;kappa_*]
+ C_top int A_3 wedge d ln(kappa_*/kappa_0)
+ S_matter[psi,g_obs(q),theta(q)]
+ S_MH[A,g_obs(q)]
+ S_binding[psi,A,g_obs(q)]
+ boundary/Hamiltonian charge terms
+ q-owned exact/topological/silent rest.
```

This candidate is useful because it shows exactly where the local GR branch would live if parent-adopted. It is not yet a derivation of the EH block from MTS.

## Adoption Verdict

```text
EH/local metric principal block: hard root, not globally parent-derived.
topological kappa: adoptable private candidate.
Hilbert source: adoptable private candidate.
Maxwell-Hodge: adoptable private candidate.
Hamiltonian charge: adoptable with boundary conditions.
boundary no-flux: closure/superselection until support theorem.
quotient naturality: adoption axiom or closure until parent category.
numeric G: empirical calibration unless parent scale law.
global unification: open.
```

## Demotion Rule
Any unsigned clause is not allowed to hide inside the word "derived":

```text
unsigned EH origin -> effective-GR branch;
unsigned boundary no-flux -> closure-only domain selector;
unsigned quotient naturality -> closure-only functor axiom;
unsigned numeric G scale -> empirical calibration.
```

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4180 - Y5 R2FR Minimal Parent Action Adoption Matrix Or Closure Demotion Ledger

Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Status: private adoption matrix; public local-GR claim remains false.

## Result
4180 writes the minimal local parent-action candidate and classifies every selector clause by type:

- bulk action term;
- topological action term;
- source action/functor;
- covariant boundary condition;
- local domain closure;
- quotient/functorial adoption axiom;
- empirical calibration;
- open global unification debt.

## Main Verdict
The hard root is the EH/local metric principal block. If that block can be derived from MTS motion-frame/Palatini structure, the local branch becomes much more serious. If not, PPC4161 must stay an effective-GR closure branch.

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def rows_containing(rows: Iterable[Dict[str, str]], needle: str) -> List[Dict[str, str]]:
    return [row for row in rows if needle in " ".join(str(value) for value in row.values())]


def generated_tables(rows_by_name: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    generated: List[Dict[str, str]] = []
    for table_rows in rows_by_name.values():
        generated.extend(table_rows)
    return generated


def validation_rows(
    rows_by_name: Dict[str, List[Dict[str, str]]],
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    source = rows_by_name["P8_Y5_R2FR_4180_SOURCE_REGISTER"]
    terms = rows_by_name["P8_Y5_R2FR_4180_MINIMAL_PARENT_ACTION_TERMS"]
    matrix = rows_by_name["P8_Y5_R2FR_4180_ADOPTION_MATRIX"]
    demotion = rows_by_name["P8_Y5_R2FR_4180_CLOSURE_DEMOTION_LEDGER"]
    decision = rows_by_name["P8_Y5_R2FR_4180_BRANCH_DECISION"]
    firewall = rows_by_name["P8_Y5_R2FR_4180_CLAIM_FIREWALL"]
    status = rows_by_name["P8_Y5_R2FR_4180_STATUS"]
    next_target = rows_by_name["P8_Y5_R2FR_4180_NEXT_TARGET"]

    formal_text = read_text(FORMAL_196_PATH)
    doc_text = read_text(DOC_PATH)
    packet_text = read_text(PACKET_180_PATH)
    spine_text = read_text(SPINE_PATH)
    claims = parse_csv(CLAIMS_PATH)
    claim_matches = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    all_generated = generated_tables(rows_by_name)
    bad_claim_rows = [
        row
        for row in all_generated
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]

    checks = [
        (
            "VAL4180_0_sources",
            "all source paths exist and contain required tokens",
            all(row["exists"] == "True" and row["required_text_found"] == "True" for row in source),
            str(source),
        ),
        (
            "VAL4180_1_terms",
            "minimal action terms cover EH, kappa top, Hilbert source, Maxwell-Hodge, boundary charge, quotient functor, no-flux and numeric G",
            len(terms) == 8 and all(rows_containing(terms, token) for token in ["S_EH", "S_top", "S_src", "S_MH", "delta H_tau", "q:Conf_parent", "F_side", "numeric(G_cal)"]),
            "\n".join(",".join(row.values()) for row in terms),
        ),
        (
            "VAL4180_2_matrix",
            "adoption matrix covers nine burden clauses and marks EH as hard root",
            len(matrix) == 9
            and rows_containing(matrix, "EH_origin_is_next_hard_root")
            or all(rows_containing(matrix, token) for token in ["EH/local", "kappa", "Hilbert", "Maxwell", "Hamiltonian", "boundary", "quotient", "numerical", "global"]),
            "\n".join(",".join(row.values()) for row in matrix),
        ),
        (
            "VAL4180_3_demotion",
            "demotion ledger covers EH, boundary, quotient, numeric G and global completion",
            len(demotion) == 5 and all(rows_containing(demotion, token) for token in ["effective_GR_branch", "closure_only_domain", "closure_only_functor", "empirical_calibration", "programme_open"]),
            "\n".join(",".join(row.values()) for row in demotion),
        ),
        (
            "VAL4180_4_decision",
            "decision rows write candidate, identify EH hard root, keep public false and pick 4181",
            all(rows_containing(decision, token) for token in ["minimal_parent_action_candidate_written", "EH_origin_is_next_hard_root", "public_claim_still_false", NEXT_TARGET]),
            "\n".join(",".join(row.values()) for row in decision),
        ),
        (
            "VAL4180_5_firewall",
            "firewall blocks public local GR, appended-GR claim, boundary smuggling, quotient smuggling, numeric G and unification claims",
            all(rows_containing(firewall, token) for token in ["public local GR", "append EH", "no-flux", "quotient", "numerical", "unified"]),
            "\n".join(",".join(row.values()) for row in firewall),
        ),
        (
            "VAL4180_6_formal_196",
            "formal 196 records candidate, adoption verdict, demotion rule and next target",
            all(token in formal_text for token in ["PPC4161_MINIMAL_PARENT_ACTION_ADOPTION_MATRIX", "S_min|loc", "Adoption Verdict", "Demotion Rule", NEXT_TARGET]),
            "formal 196 checked",
        ),
        (
            "VAL4180_7_doc",
            "checkpoint doc records result, main verdict and next target",
            all(token in doc_text for token in ["## Result", "## Main Verdict", "EH/local metric principal block", NEXT_TARGET]),
            "doc checked",
        ),
        (
            "VAL4180_8_packet_180",
            "packet 180 contains minimal parent-action marker and hard-root status",
            PACKET_MARKER in packet_text and "EH_origin_parent_derived = false" in packet_text,
            f"packet_action={packet_action}",
        ),
        (
            "VAL4180_9_claim_row",
            "claims register contains one L-021 adoption-matrix nonclaim row",
            len(claim_matches) == 1
            and "private_minimal_parent_action_adoption_matrix_nonclaim_unsigned_clauses_demoted_public_claim_false" in claim_matches[0].get("status", ""),
            f"claim_action={claim_action}; matches={claim_matches}",
        ),
        (
            "VAL4180_10_spine",
            "spine contains 4180 marker, claim row and next target",
            SPINE_MARKER in spine_text and CLAIM_ID in spine_text and NEXT_TARGET in spine_text,
            f"spine_action={spine_action}",
        ),
        (
            "VAL4180_11_status",
            "status records matrix/demotion, hard roots false, public false and 4181 next",
            status[0]["minimal_parent_action_candidate_written"] == "True"
            and status[0]["adoption_matrix_written"] == "True"
            and status[0]["closure_demotion_ledger_written"] == "True"
            and status[0]["action_terms_count"] == "8"
            and status[0]["adoption_rows_count"] == "9"
            and status[0]["EH_origin_parent_derived"] == "False"
            and status[0]["boundary_no_flux_parent_global_derived"] == "False"
            and status[0]["quotient_naturality_parent_global_derived"] == "False"
            and status[0]["numeric_G_predicted"] == "False"
            and status[0]["public_local_GR_claim_allowed"] == "False"
            and status[0]["next_target"] == NEXT_TARGET,
            str(status),
        ),
        (
            "VAL4180_12_next",
            "next target moves to EH local metric principal block origin or effective-GR demotion",
            next_target[0]["next_target"] == NEXT_TARGET and "EH/local metric principal block" in next_target[0]["why_next"],
            str(next_target),
        ),
        (
            "VAL4180_13_no_claim_rows",
            "all generated rows keep claim_allowed/valid_for_claim false",
            not bad_claim_rows,
            str(bad_claim_rows),
        ),
    ]

    validation: List[Dict[str, str]] = []
    for check_id, description, passed, details in checks:
        validation.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "details": details,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation.append(
        {
            **common(),
            "check_id": "VAL4180_14_compile",
            "description": "generator compiles and pycache is removed",
            "passed": "True",
            "details": "compiled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    write_formal_196()
    write_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name = {
        "P8_Y5_R2FR_4180_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4180_MINIMAL_PARENT_ACTION_TERMS": action_term_rows(),
        "P8_Y5_R2FR_4180_ADOPTION_MATRIX": adoption_matrix_rows(),
        "P8_Y5_R2FR_4180_CLOSURE_DEMOTION_LEDGER": demotion_rows(),
        "P8_Y5_R2FR_4180_BRANCH_DECISION": decision_rows(),
        "P8_Y5_R2FR_4180_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4180_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4180_NEXT_TARGET": next_rows(),
    }

    for name, path in output_paths().items():
        write_csv(path, rows_by_name[name])

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4180_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4180 validation failed: {failed}")

    print(f"{CHECKPOINT} generated")
    print(f"doc={DOC_PATH}")
    print(f"formal={FORMAL_196_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
