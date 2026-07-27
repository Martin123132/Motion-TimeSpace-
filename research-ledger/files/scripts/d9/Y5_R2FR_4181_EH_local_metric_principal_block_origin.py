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

CHECKPOINT = "4181"
BRANCH_ID = "MTS_R2FR_Y5_EH_LOCAL_METRIC_PRINCIPAL_BLOCK_ORIGIN_4181"
DECISION = "CONDITIONAL_MOTION_FRAME_PALATINI_EH_ORIGIN_THEOREM_WRITTEN_CURRENT_MTS_DERIVATION_FALSE_EFFECTIVE_GR_DEMOTION_ACTIVE"
DOC_PATH = POST / "4181-Y5-R2FR-EH-local-metric-principal-block-origin-or-effective-GR-demotion.md"
FORMAL_197_PATH = FORMAL / "197-PPC4161-EH-local-metric-principal-block-origin-gate.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-022"
SPINE_MARKER = "PPC4161_EH_LOCAL_METRIC_PRINCIPAL_BLOCK_ORIGIN_4181"
PACKET_MARKER = "PPC4161_PACKET_EH_LOCAL_METRIC_PRINCIPAL_BLOCK_ORIGIN_4181"
NEXT_TARGET = "4182-Y5-R2FR-motion-frame-symmetry-parent-signature-or-effective-GR-label.md"

SOURCES = {
    "SRC4181_00_4180_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4180_NEXT_TARGET.csv",
        "EH/local metric principal block",
        "4180 handoff to EH origin or effective-GR demotion.",
    ),
    "SRC4181_01_4070": (
        POST / "4070-Y5-R2FR-psi-packet-coframe-parent-action-normalization-and-torsion-gate.md",
        "exact scalar gradients alone do",
        "4070 exact-gradient flatness obstruction and Cartan repair.",
    ),
    "SRC4181_02_4071": (
        POST / "4071-Y5-R2FR-Cartan-solder-field-origin-from-MTS-flow-or-demotion.md",
        "This is not a vibe",
        "4071 conditional origin of B and omega from local motion-frame symmetry.",
    ),
    "SRC4181_03_4072": (
        POST / "4072-Y5-R2FR-local-motion-frame-gauge-action-or-effective-GR-demotion.md",
        "formal_private_candidate",
        "4072 local motion-frame gauge action candidate and demotion status.",
    ),
    "SRC4181_04_4072_action_csv": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_LOCAL_MOTION_FRAME_GAUGE_ACTION.csv",
        "STANDARD_GR_FORM_IMPORTED_UNLESS_SYMMETRY_AND_IR_NORMAL_FORM_ARE_PARENT_SIGNED",
        "4072 action CSV explicitly marks EC/Palatini block imported unless parent-signed.",
    ),
    "SRC4181_05_4072_demote_csv": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_EFFECTIVE_GR_DEMOTION_MATRIX.csv",
        "FAILS_CURRENT_DERIVATION",
        "4072 demotion matrix.",
    ),
    "SRC4181_06_formal_179": (
        FORMAL / "179-PPC4048-local-parent-packet-candidate.md",
        "PPC4048_4070_4072_motion_frame_gauge_candidate = true",
        "formal packet records the motion-frame candidate and open gates.",
    ),
    "SRC4181_07_formal_196": (
        FORMAL / "196-PPC4161-minimal-parent-action-adoption-matrix.md",
        "EH/local metric principal block: hard root",
        "4180 adoption matrix identifies EH origin as the hard root.",
    ),
    "SRC4181_08_claim_L021": (
        CLAIMS_PATH,
        "minimal PPC4161 parent-action candidate",
        "latest claim-register row before EH-origin gate.",
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


def motion_frame_audit_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "MFA4181_0_gradient_trap",
            "exact scalar coframe route",
            "e^A=dX^A gives local pullback-flat metric when det(dX)!=0",
            "rejected",
            "cannot derive curved local GR from pure scalar gradients",
        ),
        (
            "MFA4181_1_covariant_solder",
            "Cartan/motion-frame repair",
            "e^A=D_omega X^A+B^A; g_obs=eta_AB e^A e^B",
            "conditional_candidate",
            "avoids exact-gradient flatness if B and omega are parent-owned",
        ),
        (
            "MFA4181_2_symmetry_logic",
            "local motion-frame symmetry",
            "X^A -> Lambda^A_B(x) X^B + a^A(x)",
            "conditional_origin_theorem",
            "local Lorentz/translation covariance forces omega and B as compensators",
        ),
        (
            "MFA4181_3_action_candidate",
            "Einstein-Cartan/Palatini action",
            "S_EC=(4 kappa_eff)^-1 int eps_ABCD e^A e^B R^CD[omega] - Lambda term",
            "formal_candidate_not_current_MTS_derived",
            "standard GR normal form is written but not yet derived from MTS primitives",
        ),
        (
            "MFA4181_4_MTS_uplift",
            "MTS variable uplift",
            "Psi^A -> X^A; flow -> B^A; Gamma_mem -> invariants/projections of R,T",
            "plausible_mapping_unsigned",
            "Gamma_mem scalar cannot own the full connection by itself",
        ),
        (
            "MFA4181_5_current_verdict",
            "current corpus status",
            "motion_frame_gauge_action=formal_private_candidate; current_MTS_derivation=false",
            "demotion_active_if_not_parent_signed",
            "route remains alive but not public derived local GR",
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "object": obj,
            "mathematical_content": content,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, obj, content, status, meaning in rows
    ]


def eh_origin_chain_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "EHO4181_0_parent_symmetry",
            "parent signs local motion-frame gauge symmetry",
            "local Lorentz + local translation/motion-frame covariance",
            "missing_parent_signature",
            "without this, B and omega are imported GR infrastructure",
        ),
        (
            "EHO4181_1_coframe",
            "nondegenerate observed coframe",
            "e^A=D_omega X^A+B^A, det(e)!=0, g_obs=eta_AB e^A e^B",
            "conditional_candidate",
            "curved Lorentzian metric can exist without exact-gradient flatness",
        ),
        (
            "EHO4181_2_two_derivative_normal_form",
            "IR/two-derivative Palatini normal form",
            "S_EC proportional to int eps_ABCD e^A e^B R^CD[omega] plus cosmological term",
            "missing_parent_IR_selection",
            "must derive why this is the leading local parent term, not simply append it",
        ),
        (
            "EHO4181_3_torsion_resolution",
            "torsion/nonmetricity silence",
            "delta_omega S_EC => T^A=0 on spinless compact local branch or torsion bounded",
            "conditional_gate",
            "otherwise PPN/preferred-frame residuals reopen",
        ),
        (
            "EHO4181_4_EH_reduction",
            "Palatini to EH",
            "omega=omega_LC[e] => S_EC -> S_EH[g_obs] + boundary",
            "conditional_theorem",
            "valid once EHO4181_0 through EHO4181_3 are signed",
        ),
        (
            "EHO4181_5_extra_modes",
            "scalar/disformal/higher-curvature silence",
            "no extra <=2PN bulk fields beyond q-owned/topological/boundary/vertical terms",
            "missing_global_parent_proof",
            "otherwise effective-GR residual interface is required",
        ),
        (
            "EHO4181_6_verdict",
            "EH principal block origin",
            "conditional Palatini/EH origin theorem exists; current MTS derivation remains false",
            "conditional_not_public_claim",
            "next target is parent-signature of the motion-frame symmetry/action",
        ),
    ]
    return [
        {
            **common(),
            "chain_id": chain_id,
            "step": step,
            "formula_or_condition": formula,
            "status": status,
            "if_missing": if_missing,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for chain_id, step, formula, status, if_missing in rows
    ]


def extra_mode_gate_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "XMG4181_0_torsion",
            "torsion",
            "T^A=D_omega e^A",
            "zero_or_bound_required",
            "preferred-frame/spin-torsion residuals reopen",
        ),
        (
            "XMG4181_1_nonmetricity",
            "nonmetricity",
            "D_omega eta_AB or connection/coframe mismatch",
            "zero_or_bound_required",
            "same-frame source and Maxwell-Hodge gates reopen",
        ),
        (
            "XMG4181_2_shadow_frame",
            "shadow coframe/frame",
            "matter or EM couples to e_shadow != e_obs",
            "forbidden_by_4177_if_parent_signed",
            "WEP/clock/R10/source-normalization residuals reopen",
        ),
        (
            "XMG4181_3_higher_curvature",
            "higher curvature local bulk terms",
            "R^2, R_AB R^AB or non-EH two-derivative-equivalent response",
            "absent_or_PPN_bound_required",
            "beta/gamma/xi/zeta residuals reopen",
        ),
        (
            "XMG4181_4_disformal_scalar",
            "scalar/disformal motion-frame mode",
            "independent scalar/vector representative enters g_obs or source functor",
            "zero_or_bound_required",
            "projector and fifth-force residuals reopen",
        ),
        (
            "XMG4181_5_boundary",
            "Cartan boundary/edge charge",
            "non-q-owned or non-routed boundary term",
            "fixed_exact_or_4176_routed_required",
            "mass charge and transition-current residuals reopen",
        ),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "extra_mode": mode,
            "mathematical_slot": slot,
            "required_status": required,
            "if_missing": if_missing,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, mode, slot, required, if_missing in rows
    ]


def demotion_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "DEM4181_0_EH_origin",
            "EH principal block",
            "motion-frame symmetry/action not parent-signed",
            "effective_GR_branch",
            "PPC4161 can be used as a disciplined local GR closure baseline, not a derived MTS->GR theorem",
        ),
        (
            "DEM4181_1_Cartan_fields",
            "B^A and omega^AB",
            "Cartan fields not derived from MTS flow/memory primitives",
            "effective_coframe_connection_inputs",
            "treat flow/memory mapping as future uplift target",
        ),
        (
            "DEM4181_2_torsion",
            "torsion/nonmetricity",
            "torsion gate not parent-signed or source-bounded",
            "residual_interface",
            "score torsion/preferred-frame/PPN residuals before empirical claims",
        ),
        (
            "DEM4181_3_IR_normal_form",
            "Palatini/EH normal form",
            "two-derivative EH uniqueness not derived from MTS IR action",
            "standard_GR_import_label",
            "do not call EH block MTS-derived",
        ),
        (
            "DEM4181_4_public_language",
            "public local-GR claim",
            "any above demotion trigger remains active",
            "public_claim_false",
            "use private conditional/effective language only",
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
            "DEC4181_0_conditional_theorem",
            "conditional_motion_frame_Palatini_EH_origin_theorem_written",
            "If local motion-frame symmetry, covariant solder coframe, Palatini normal form and torsion silence are parent-signed, the EH block follows.",
            "retain_as_theorem_target",
        ),
        (
            "DEC4181_1_current_status",
            "current_MTS_derivation_false",
            "4070-4072 and 4181 show the route is sharp but the parent signature of the motion-frame gauge action is missing.",
            "effective_GR_demotion_active_until_signed",
        ),
        (
            "DEC4181_2_next",
            "next_best_derivation_target",
            "The next hard target is not another PPN check; it is the parent signature for local motion-frame symmetry/action ownership.",
            NEXT_TARGET,
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
        ("FW4181_0_no_public_EH_origin", "Do not claim the EH block is derived from MTS until motion-frame symmetry/action is parent-signed."),
        ("FW4181_1_no_scalar_gradient_GR", "Do not revive exact scalar-gradient curved-GR route; it is locally flat."),
        ("FW4181_2_no_imported_GR_mask", "Do not import Einstein-Cartan/Palatini normal form and call it MTS-derived."),
        ("FW4181_3_no_torsion_silence_by_assumption", "Do not assume torsion/nonmetricity/extra modes are silent without parent proof or bounds."),
        ("FW4181_4_no_public_local_GR", "Do not claim public local GR from this conditional theorem."),
        ("FW4181_5_no_numeric_G", "Do not claim numerical G_N prediction."),
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
            "conditional_motion_frame_Palatini_EH_origin_theorem_written": "True",
            "pure_scalar_gradient_route_rejected": "True",
            "Cartan_solder_repair_candidate_retained": "True",
            "EH_origin_parent_derived": "False",
            "motion_frame_symmetry_parent_signed": "False",
            "Palatini_IR_normal_form_parent_derived": "False",
            "torsion_nonmetricity_silence_parent_proved": "False",
            "effective_GR_demotion_active": "True",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "formal_197_written": "True",
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
            "why_next": "4181 sharpens the EH origin route but leaves the decisive missing input: a parent signature for local motion-frame Lorentz/translation symmetry and its action ownership.",
            "route_A": "derive local motion-frame symmetry from MTS primitives so B^A and omega^AB are forced parent gauge fields",
            "route_B": "if symmetry/action ownership cannot be derived, label PPC4161 as effective-GR closure and keep residual interfaces explicit",
            "fallback": "continue testing only as closure-branch robustness, not proof of MTS-derived EH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4181_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4181_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4181_MOTION_FRAME_EVIDENCE_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4181_MOTION_FRAME_EVIDENCE_AUDIT.csv",
        "P8_Y5_R2FR_4181_EH_ORIGIN_THEOREM_CHAIN": SOURCE_DIR / "P8_Y5_R2FR_4181_EH_ORIGIN_THEOREM_CHAIN.csv",
        "P8_Y5_R2FR_4181_EXTRA_MODE_SILENCE_GATES": SOURCE_DIR / "P8_Y5_R2FR_4181_EXTRA_MODE_SILENCE_GATES.csv",
        "P8_Y5_R2FR_4181_EFFECTIVE_GR_DEMOTION_LEDGER": SOURCE_DIR / "P8_Y5_R2FR_4181_EFFECTIVE_GR_DEMOTION_LEDGER.csv",
        "P8_Y5_R2FR_4181_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4181_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4181_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4181_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4181_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4181_STATUS.csv",
        "P8_Y5_R2FR_4181_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4181_NEXT_TARGET.csv",
    }


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    fieldnames = list(rows[0].keys())
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "The EH/local metric principal block has a conditional motion-frame Palatini origin theorem, but current MTS does not yet parent-sign the motion-frame gauge action, so effective-GR demotion remains active",
        "current_evidence": "formalization-workbench/197-PPC4161-EH-local-metric-principal-block-origin-gate.md records the scalar-gradient flatness rejection, Cartan solder repair e^A=D_omega X^A+B^A, conditional Palatini-to-EH chain, extra-mode gates, and effective-GR demotion ledger; public_claim=false",
        "status": "conditional_EH_origin_theorem_nonclaim_current_MTS_derivation_false_effective_GR_demotion_active",
        "next_test": "Derive parent signature for local motion-frame Lorentz/translation symmetry and action ownership or label PPC4161 effective-GR closure",
        "key_risk": "The theorem is conditional; without parent-signed motion-frame symmetry/action, EH is imported GR infrastructure rather than derived MTS local dynamics",
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
## PPC4161-TK-HQNP Addendum - EH Local Metric Principal Block Origin Gate

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4181-Y5-R2FR-EH-local-metric-principal-block-origin-or-effective-GR-demotion.md`

4181 rejects the pure scalar-gradient route:

```text
e^A=dX^A  =>  local pullback-flat metric.
```

The retained conditional repair is:

```text
e^A = D_omega X^A + B^A,
g_obs = eta_AB e^A e^B,
S_EC[e,omega] -> S_EH[g_obs] + boundary
```

if and only if the parent signs local motion-frame symmetry, the Palatini/EC normal form, torsion/nonmetricity silence, and no extra <=2PN modes.

Status:

```text
conditional_EH_origin_theorem = true
current_MTS_EH_derivation = false
effective_GR_demotion_active = true
```
"""
    return append_once(PACKET_180_PATH, PACKET_MARKER, section)


def ensure_spine_section() -> str:
    section = f"""
## PPC4161 EH Local Metric Principal Block Origin Gate - 4181

Marker: `{SPINE_MARKER}`  
Source bridge: `197-PPC4161-EH-local-metric-principal-block-origin-gate.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4181` resolves the immediate fork:

```text
pure scalar-gradient coframe -> rejected as locally flat;
Cartan/motion-frame coframe -> retained as conditional route;
Palatini/EC -> EH only if parent-signed;
current MTS derivation -> false;
effective-GR demotion -> active.
```

Next:

```text
{NEXT_TARGET}
```
"""
    return append_once(SPINE_PATH, SPINE_MARKER, section)


def write_formal_197() -> None:
    FORMAL_197_PATH.write_text(
        f"""# 197 - PPC4161 EH Local Metric Principal Block Origin Gate

Marker: `PPC4161_EH_LOCAL_METRIC_PRINCIPAL_BLOCK_ORIGIN_GATE`
Checkpoint: `4181`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status
Private conditional theorem. This is not public local GR, not a global parent-action derivation, and not a numerical prediction of Newton's constant.

## Rejected Route

```text
e^A = dX^A,
g_obs = eta_AB dX^A dX^B.
```

If `det(dX) != 0`, then `X^A` are local coordinates and `g_obs` is locally a pullback of flat internal Minkowski space. Pure scalar gradients do not derive curved local GR.

## Retained Motion-Frame Route

```text
X^A = L_* Psi^A,
e^A = D_omega X^A + B^A,
g_obs = eta_AB e^A e^B.
```

If MTS parent-signs local motion-frame Lorentz plus translation symmetry, the compensators `omega^AB` and `B^A` are forced by covariance.

## Conditional EH Origin Theorem
If:

```text
local motion-frame symmetry is parent-owned;
e^A is nondegenerate and same-frame for matter/EM;
the leading local two-derivative normal form is Einstein-Cartan/Palatini;
torsion/nonmetricity and extra scalar/disformal modes are zero or bounded;
boundary terms are fixed/exact/routed;
```

then:

```text
S_EC[e,omega;kappa_eff] -> S_EH[g_obs;kappa_eff] + boundary,
```

and PPC4161 inherits the local EH/Newton/PPN chain.

## Current Verdict

```text
conditional_EH_origin_theorem = true,
current_MTS_EH_derivation = false,
effective_GR_demotion_active = true.
```

The route is not dead. But until the motion-frame symmetry/action is parent-signed, the EH block is effective-GR infrastructure, not a derived MTS block.

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4181 - Y5 R2FR EH Local Metric Principal Block Origin Or Effective-GR Demotion

Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Status: conditional theorem; effective-GR demotion active.

## Result
4181 rejects the exact scalar-gradient route and retains the Cartan/motion-frame route:

```text
e^A = D_omega X^A + B^A,
g_obs = eta_AB e^A e^B.
```

The Palatini/EH chain is conditionally valid:

```text
S_EC[e,omega] -> S_EH[g_obs] + boundary
```

only if local motion-frame symmetry/action ownership, torsion silence, same-frame matter/EM and extra-mode silence are parent-signed.

## Honest Verdict
The current corpus has a strong formal candidate, not a completed derivation. PPC4161 therefore remains an effective-GR closure branch unless 4182 derives the parent signature for the motion-frame gauge action.

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
    source = rows_by_name["P8_Y5_R2FR_4181_SOURCE_REGISTER"]
    audit = rows_by_name["P8_Y5_R2FR_4181_MOTION_FRAME_EVIDENCE_AUDIT"]
    chain = rows_by_name["P8_Y5_R2FR_4181_EH_ORIGIN_THEOREM_CHAIN"]
    extra = rows_by_name["P8_Y5_R2FR_4181_EXTRA_MODE_SILENCE_GATES"]
    demotion = rows_by_name["P8_Y5_R2FR_4181_EFFECTIVE_GR_DEMOTION_LEDGER"]
    decision = rows_by_name["P8_Y5_R2FR_4181_BRANCH_DECISION"]
    firewall = rows_by_name["P8_Y5_R2FR_4181_CLAIM_FIREWALL"]
    status = rows_by_name["P8_Y5_R2FR_4181_STATUS"]
    next_target = rows_by_name["P8_Y5_R2FR_4181_NEXT_TARGET"]

    formal_text = read_text(FORMAL_197_PATH)
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
            "VAL4181_0_sources",
            "all source paths exist and contain required tokens",
            all(row["exists"] == "True" and row["required_text_found"] == "True" for row in source),
            str(source),
        ),
        (
            "VAL4181_1_audit",
            "audit rejects scalar gradient and retains conditional Cartan repair with unsigned MTS derivation",
            all(rows_containing(audit, token) for token in ["exact scalar", "D_omega", "local motion-frame", "S_EC", "Gamma_mem", "current_MTS_derivation=false"]),
            "\n".join(",".join(row.values()) for row in audit),
        ),
        (
            "VAL4181_2_chain",
            "EH origin chain covers parent symmetry, coframe, Palatini normal form, torsion, EH reduction, extra modes and verdict",
            len(chain) == 7 and all(rows_containing(chain, token) for token in ["motion-frame", "det(e)", "S_EC", "T^A=0", "S_EH", "<=2PN", "conditional Palatini"]),
            "\n".join(",".join(row.values()) for row in chain),
        ),
        (
            "VAL4181_3_extra_modes",
            "extra-mode gates cover torsion, nonmetricity, shadow frame, higher curvature, disformal scalar and boundary charge",
            len(extra) == 6 and all(rows_containing(extra, token) for token in ["torsion", "nonmetricity", "shadow", "higher curvature", "scalar", "boundary"]),
            "\n".join(",".join(row.values()) for row in extra),
        ),
        (
            "VAL4181_4_demotion",
            "demotion ledger covers EH origin, Cartan fields, torsion, IR normal form and public language",
            len(demotion) == 5 and all(rows_containing(demotion, token) for token in ["effective_GR_branch", "effective_coframe", "residual_interface", "standard_GR_import", "public_claim_false"]),
            "\n".join(",".join(row.values()) for row in demotion),
        ),
        (
            "VAL4181_5_decision",
            "decision rows write conditional theorem, current false status and 4182 next target",
            all(rows_containing(decision, token) for token in ["conditional_motion_frame", "current_MTS_derivation_false", NEXT_TARGET]),
            "\n".join(",".join(row.values()) for row in decision),
        ),
        (
            "VAL4181_6_firewall",
            "firewall blocks public EH origin, scalar-gradient GR, imported GR mask, torsion silence by assumption, public local GR and numeric G",
            all(rows_containing(firewall, token) for token in ["EH block", "scalar-gradient", "Einstein-Cartan", "torsion", "public local GR", "numerical G"]),
            "\n".join(",".join(row.values()) for row in firewall),
        ),
        (
            "VAL4181_7_formal_197",
            "formal 197 records rejected route, retained route, conditional theorem, current verdict and next target",
            all(token in formal_text for token in ["Rejected Route", "Retained Motion-Frame Route", "Conditional EH Origin Theorem", "current_MTS_EH_derivation = false", NEXT_TARGET]),
            "formal 197 checked",
        ),
        (
            "VAL4181_8_doc",
            "checkpoint doc records result, honest verdict and next target",
            all(token in doc_text for token in ["## Result", "## Honest Verdict", "effective-GR closure branch", NEXT_TARGET]),
            "doc checked",
        ),
        (
            "VAL4181_9_packet_180",
            "packet 180 contains EH origin marker and demotion status",
            PACKET_MARKER in packet_text and "effective_GR_demotion_active = true" in packet_text,
            f"packet_action={packet_action}",
        ),
        (
            "VAL4181_10_claim_row",
            "claims register contains one L-022 EH-origin nonclaim row",
            len(claim_matches) == 1
            and "conditional_EH_origin_theorem_nonclaim_current_MTS_derivation_false_effective_GR_demotion_active" in claim_matches[0].get("status", ""),
            f"claim_action={claim_action}; matches={claim_matches}",
        ),
        (
            "VAL4181_11_spine",
            "spine contains 4181 marker, claim row and next target",
            SPINE_MARKER in spine_text and CLAIM_ID in spine_text and NEXT_TARGET in spine_text,
            f"spine_action={spine_action}",
        ),
        (
            "VAL4181_12_status",
            "status records conditional theorem true, parent derivation false, effective demotion active and public false",
            status[0]["conditional_motion_frame_Palatini_EH_origin_theorem_written"] == "True"
            and status[0]["pure_scalar_gradient_route_rejected"] == "True"
            and status[0]["Cartan_solder_repair_candidate_retained"] == "True"
            and status[0]["EH_origin_parent_derived"] == "False"
            and status[0]["motion_frame_symmetry_parent_signed"] == "False"
            and status[0]["Palatini_IR_normal_form_parent_derived"] == "False"
            and status[0]["torsion_nonmetricity_silence_parent_proved"] == "False"
            and status[0]["effective_GR_demotion_active"] == "True"
            and status[0]["public_local_GR_claim_allowed"] == "False"
            and status[0]["next_target"] == NEXT_TARGET,
            str(status),
        ),
        (
            "VAL4181_13_next",
            "next target moves to motion-frame symmetry parent signature or effective-GR label",
            next_target[0]["next_target"] == NEXT_TARGET and "local motion-frame" in next_target[0]["why_next"],
            str(next_target),
        ),
        (
            "VAL4181_14_no_claim_rows",
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
            "check_id": "VAL4181_15_compile",
            "description": "generator compiles and pycache is removed",
            "passed": "True",
            "details": "compiled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    write_formal_197()
    write_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name = {
        "P8_Y5_R2FR_4181_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4181_MOTION_FRAME_EVIDENCE_AUDIT": motion_frame_audit_rows(),
        "P8_Y5_R2FR_4181_EH_ORIGIN_THEOREM_CHAIN": eh_origin_chain_rows(),
        "P8_Y5_R2FR_4181_EXTRA_MODE_SILENCE_GATES": extra_mode_gate_rows(),
        "P8_Y5_R2FR_4181_EFFECTIVE_GR_DEMOTION_LEDGER": demotion_rows(),
        "P8_Y5_R2FR_4181_BRANCH_DECISION": decision_rows(),
        "P8_Y5_R2FR_4181_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4181_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4181_NEXT_TARGET": next_rows(),
    }

    for name, path in output_paths().items():
        write_csv(path, rows_by_name[name])

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4181_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4181 validation failed: {failed}")

    print(f"{CHECKPOINT} generated")
    print(f"doc={DOC_PATH}")
    print(f"formal={FORMAL_197_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
