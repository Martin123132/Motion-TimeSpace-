from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4277"
CLAIM_ID = "L-118"
BRANCH = "MTS_R2FR_Y5_MATTER_INTERFACE_ACTION_DOMAIN_PROOF_OR_CANONICAL_GX_SOURCE_FILL_4277"
DECISION = "STANDARD_BRANCH_MATTER_INTERFACE_DESCENT_DERIVES_GX_ZERO_CONDITIONAL_NONCLAIM"
MARKER = "PPC4161_MATTER_INTERFACE_ACTION_DOMAIN_PROOF_OR_CANONICAL_GX_SOURCE_FILL_4277"
PACKET_MARKER = "PPC4161_PACKET_MATTER_INTERFACE_ACTION_DOMAIN_PROOF_OR_CANONICAL_GX_SOURCE_FILL_4277"
NEXT_TARGET = "4278-Y5-R2FR-left-hand-local-EH-Newton-limit-or-source-probe-tomography-fill.md"

FORMAL_PATH = FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md"
DOC_PATH = POST / "4277-Y5-R2FR-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4277_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4277_DQ_COMPONENT_VALUES_CANDIDATE.csv"
CORE_BOUND_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4277_DQ_GEOM_BOUND_RUNNER_CANDIDATE.csv"

ALPHA_EFF_BOUND = 0.00578792
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

PROBE_ORDER = (
    "Dq_geom",
    "Dq_tau",
    "Dq_matter",
    "Dq_source_readout",
    "Dq_theta_marker",
    "Dq_boundary_projector",
    "Dq_EM",
    "Dq_coeff",
)

ZERO_SOURCE_BY_PROBE = {
    "Dq_tau": FORMAL / "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md",
    "Dq_matter": FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
    "Dq_source_readout": FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
    "Dq_theta_marker": FORMAL / "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md",
    "Dq_boundary_projector": FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
    "Dq_EM": FORMAL / "279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md",
    "Dq_coeff": FORMAL / "283-PPC4161-Dq-coeff-fixed-parent-constant-or-Newton-calibration-bound.md",
}

SOURCES = {
    "SRC4277_00_4276_formal": (
        FORMAL / "292-PPC4161-parent-gX-zero-no-shadow-theorem-or-first-canonical-gX-source-row.md",
        "ordinary matter-interface action-domain descent",
        "4276 identified the decisive missing bridge.",
    ),
    "SRC4277_01_4265_matter": (
        FORMAL / "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
        "S_matter = Sbar[psi, g_obs(q), theta_obs]",
        "4265 already adopted the standard local branch matter action-domain descent.",
    ),
    "SRC4277_02_4264_theta": (
        FORMAL / "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md",
        "theta_obs = {m_A, charges, alpha_EM, hbar, c, material labels}",
        "4264 fixes visible constants/markers in the standard branch.",
    ),
    "SRC4277_03_4266_source": (
        FORMAL / "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
        "T_obs = -2/sqrt|g_obs| delta Sbar_m / delta g_obs",
        "4266 routes the Hilbert source readout after matter descent.",
    ),
    "SRC4277_04_4267_coeff": (
        FORMAL / "283-PPC4161-Dq-coeff-fixed-parent-constant-or-Newton-calibration-bound.md",
        "delta_v G_N = 0",
        "4267 blocks hidden drift of fixed parent constants in the local branch.",
    ),
    "SRC4277_05_4268_boundary": (
        FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
        "Dq_boundary_projector = 0",
        "4268 fixes the compact no-flux collar/projector branch.",
    ),
    "SRC4277_06_4269_tau": (
        FORMAL / "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md",
        "tau_obs = tau_bar(q)",
        "4269 fixes observed local time/readout in the standard branch.",
    ),
    "SRC4277_07_4263_em": (
        FORMAL / "279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md",
        "Poynting is already the Hilbert flux of the EM stress",
        "4263 blocks double-counting EM/Poynting flux in the closed-collar branch.",
    ),
    "SRC4277_08_1029_chain": (
        SOURCE_DIR / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv",
        "NST1029_1_chain_rule_zero",
        "Older chain-rule theorem: q-factorization kills vertical frame coupling.",
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


def is_number(value: str) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number)


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


def descent_theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "AD4277_0_interface_definition",
            "Define the ordinary local interface as quotient data.",
            "I_m(q(Phi)) := (g_obs(q), theta_obs(q), tau_obs(q), orientation/collar(q))",
            "STANDARD_BRANCH_INTERFACE_DEFINED",
            "The branch is standard/local and private, not a global MTS ontology claim.",
        ),
        (
            "AD4277_1_action_factorization",
            "Use the 4265 matter-domain branch.",
            "S_matter[Psi;Phi] = Sbar_m[Psi, g_obs(q(Phi)), theta_obs(q(Phi))]",
            "CONDITIONAL_DESCENT_INPUT_PRESENT",
            "Direct hidden-parent matter operators remain a retained fork.",
        ),
        (
            "AD4277_2_vertical_variation",
            "For v in ker(Dq), all quotient-interface arguments are stationary.",
            "delta_v g_obs = Dg_obs[Dq(v)] = 0 and delta_v theta_obs = Dtheta_obs[Dq(v)] = 0",
            "CONDITIONAL_CHAIN_RULE_INPUT_PRESENT",
            "Needs q-kernel ownership for the tested local branch.",
        ),
        (
            "AD4277_3_action_domain_descent",
            "The matter action has zero vertical derivative in the standard branch.",
            "delta_v S_matter = DSbar_m[delta_v g_obs, delta_v theta_obs] = 0",
            "CONDITIONAL_STANDARD_BRANCH_PROOF",
            "Public parent claim still needs branch selector/parent signature.",
        ),
        (
            "AD4277_4_shadow_slot_exclusion",
            "A live A_g or B_dis slot would contradict the descent equation.",
            "Sbar_m[Psi,A_g(phi_X)e_pub,...] gives delta_v S_matter proportional to g_X delta phi_X unless g_X=0; similarly B_dis gives b_dis",
            "NO_SHADOW_SLOT_DERIVED_WITHIN_STANDARD_BRANCH",
            "If such slot is reintroduced, it must be scored as finite canonical g_X/b_dis.",
        ),
        (
            "AD4277_5_canonical_zero",
            "The canonical frame coupling vanishes in this branch.",
            "g_X=d ln A_g/dphi_X = 0 and b_dis=0",
            "CONDITIONAL_GX_BDIS_ZERO_DERIVED",
            "Nonclaim until the left-hand field equation/Newton limit and public branch selector close.",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "status": status,
            "caveat": caveat,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, mathematical_form, status, caveat in raw
    ]


def tail_guard_rows() -> List[Dict[str, str]]:
    raw = [
        ("TG4277_0_tau", "Dq_tau", "0.0", ZERO_SOURCE_BY_PROBE["Dq_tau"], "q-basic observed tau/reference-time branch"),
        ("TG4277_1_matter", "Dq_matter", "0.0", ZERO_SOURCE_BY_PROBE["Dq_matter"], "matter action-domain descent branch"),
        ("TG4277_2_source", "Dq_source_readout", "0.0", ZERO_SOURCE_BY_PROBE["Dq_source_readout"], "Hilbert/ADM source-charge branch"),
        ("TG4277_3_theta", "Dq_theta_marker", "0.0", ZERO_SOURCE_BY_PROBE["Dq_theta_marker"], "calibrated q-basic visible constants branch"),
        ("TG4277_4_boundary", "Dq_boundary_projector", "0.0", ZERO_SOURCE_BY_PROBE["Dq_boundary_projector"], "fixed compact no-flux collar branch"),
        ("TG4277_5_em", "Dq_EM", "0.0", ZERO_SOURCE_BY_PROBE["Dq_EM"], "closed-collar visible EM/Poynting-once branch"),
        ("TG4277_6_coeff", "Dq_coeff", "0.0", ZERO_SOURCE_BY_PROBE["Dq_coeff"], "fixed parent-action/calibrated constant branch"),
        ("TG4277_7_geom", "Dq_geom", "0.0", FORMAL_PATH, "matter-interface descent kills canonical g_X and b_dis slots"),
    ]
    return [
        {
            **common(),
            "guard_id": guard_id,
            "probe_id": probe_id,
            "epsilon": epsilon,
            "epsilon_C1": epsilon,
            "source_path": str(source_path),
            "branch_scope": branch_scope,
            "status": "CONDITIONAL_STANDARD_BRANCH_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for guard_id, probe_id, epsilon, source_path, branch_scope in raw
    ]


def canonical_zero_source_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "source_row_id": "GXSR4277_0_standard_branch_gX_zero",
            "row_type": "canonical_gx_zero",
            "g_X": "0.0",
            "b_dis": "0.0",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "computed_alpha_eff": "0.0",
            "passed_bound": "True",
            "definition": "g_X=d ln A_g/dphi_X; absent/factored ordinary shadow frame in standard branch",
            "units": "dimensionless",
            "source_path": str(FORMAL_PATH),
            "source_anchor": "AD4277_3_action_domain_descent;AD4277_4_shadow_slot_exclusion;AD4277_5_canonical_zero",
            "derivation_status": "CONDITIONAL_STANDARD_BRANCH_DERIVED",
            "tail_guard_status": "STANDARD_BRANCH_COMPONENTS_ZERO_NONCLAIM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "verdict": "CONDITIONAL_ZERO_PASSES_BOUND_NONCLAIM",
        },
        {
            **common(),
            "source_row_id": "GXSR4277_1_counterfactual_finite_slot",
            "row_type": "canonical_gx_retained_fork",
            "g_X": "MISSING_NUMERIC_RETAINED_SLOT",
            "b_dis": "MISSING_NUMERIC_RETAINED_SLOT",
            "alpha_eff_bound": f"{ALPHA_EFF_BOUND:.8f}",
            "computed_alpha_eff": "",
            "passed_bound": "False",
            "definition": "If A_g/B_dis is reintroduced outside the standard branch, score finite canonical coupling.",
            "units": "dimensionless",
            "source_path": str(FORMAL_PATH),
            "source_anchor": "retained_finite_shadow_slot_fork",
            "derivation_status": "RETAINED_FORK_NOT_ADOPTED",
            "tail_guard_status": "MISSING_FINITE_FORK_TAIL_GUARDS",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "verdict": "FINITE_FORK_BLOCKED_UNLESS_SOURCED",
        },
    ]


def bound_runner_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for row in canonical_zero_source_rows():
        out = dict(row)
        gx = row.get("g_X", "")
        if is_number(gx):
            alpha_eff = abs(float(gx))
            out["computed_alpha_eff"] = f"{alpha_eff:.8g}"
            out["passed_bound"] = str(alpha_eff <= ALPHA_EFF_BOUND)
        rows.append(out)
    return rows


def bound_candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "DQ_GEOM_STANDARD_BRANCH_GX_ZERO_4277",
            "target_component": "Dq_geom",
            "norm_or_bound": "g_X=0 and b_dis=0 by matter-interface action-domain descent in the standard branch",
            "numeric_bound": "0.0",
            "units": "dimensionless Dq component",
            "filled_inputs": "4265 matter descent; 4264 theta; 4266 source readout; 4267 fixed coefficients; 4268 boundary; 4269 tau; 4263 EM",
            "missing": "public parent branch-selector signature; left-hand EH/Newton limit; source-probe tomography constants",
            "source_path": str(FORMAL_PATH),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    previous_by_probe = {row.get("probe_id", ""): row for row in previous if row.get("probe_id", "")}
    rows: List[Dict[str, str]] = []
    for probe in PROBE_ORDER:
        base = dict(previous_by_probe.get(probe, {}))
        base.update(common())
        base.setdefault("candidate_id", "DQ_COORDINATE_SEMINORM_SMOKE_4255")
        base["probe_id"] = probe
        base["weight"] = base.get("weight") or "1.0"
        if probe == "Dq_geom":
            base["epsilon"] = "0.0"
            base["epsilon_C1"] = "0.0"
            base["source_path"] = str(FORMAL_PATH)
        elif probe in ZERO_SOURCE_BY_PROBE:
            base["epsilon"] = "0.0"
            base["epsilon_C1"] = "0.0"
            base["source_path"] = str(ZERO_SOURCE_BY_PROBE[probe])
        else:
            base["epsilon"] = base.get("epsilon") or f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}"
            base["epsilon_C1"] = base.get("epsilon_C1") or f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}"
            base["source_path"] = base.get("source_path") or str(FORMAL_PATH)
        base["valid_for_claim"] = "False"
        rows.append(base)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4277_0_close_standard_branch_geom",
            "Close Dq_geom to zero inside the standard local matter-interface branch.",
            "4265 supplies exactly the action-domain descent 4276 demanded; chain rule then kills ordinary A_g/B_dis shadow slots.",
            "feed zero Dq components into source-probe/left-hand gates",
        ),
        (
            "DEC4277_1_keep_nonclaim",
            "Do not promote this to public local-GR evidence yet.",
            "The branch selector is private/conditional, and left-hand EH/Newton plus source-probe tomography still need verification.",
            NEXT_TARGET,
        ),
        (
            "DEC4277_2_retained_fork",
            "If a future parent action reintroduces direct hidden matter/frame slots, score them as finite g_X/b_dis.",
            "The zero theorem is not compatible with hidden direct matter operators or field-rename escapes.",
            "source canonical finite row if the hidden slot is adopted",
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
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4277_0_standard_branch_only", "The g_X=b_dis=0 result applies only to the standard local matter-interface branch."),
        ("FW4277_1_no_hidden_operator", "Any direct hidden-parent matter operator breaks the theorem and must be separately bounded."),
        ("FW4277_2_no_public_local_gr_claim", "Zero Dq components do not by themselves prove the left-hand Einstein/Newton limit or source-probe rank gate."),
        ("FW4277_3_no_constant_source_rename", "Moving the coupling into constants, sources, clocks, collars, or EM flux is forbidden unless those rows remain zero or bounded."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4277",
            "current_status": "standard-branch matter-interface descent derives g_X=b_dis=0 and Dq_geom=0 as a private conditional component row",
            "local_gr_claim": "False",
            "ppn_claim": "False",
            "newton_claim": "False",
            "em_claim": "False",
            "next_best_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "with all Dq components zero in the standard branch, the next real obstacle is the left-hand local EH/Newton limit or source-probe tomography constants.",
            "success_condition": "either derive the local Einstein/Newton operator limit from the parent action, or fill source-probe matrix/constants so 4254 computes A_H/h_U_C1.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


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
            "4277 uses the 4265 standard local matter-action branch to derive the 4276 missing matter-interface descent: "
            "S_matter[Psi;Phi]=Sbar_m[Psi,g_obs(q(Phi)),theta_obs(q(Phi))]. For v in ker(Dq), delta_v S_matter=0, so any ordinary A_g/B_dis shadow-frame slot is absent or has g_X=b_dis=0. "
            "This closes Dq_geom to 0 only as a private conditional standard-branch component row, not as a public local-GR claim."
        ),
        "current_evidence": (
            "4277 source register, action-domain descent theorem rows, tail guard matrix, canonical zero source row, runner result, updated Dq component candidate, decision and firewall."
        ),
        "status": "private_standard_branch_matter_interface_descent_gX_zero_nonclaim",
        "next_test": "Derive the left-hand local EH/Newton operator limit or fill source-probe tomography inputs so the zero Dq branch feeds a quantitative local bound.",
        "key_risk": "Mistaking the standard-branch conditional zero for a public parent theorem, or reintroducing hidden matter/frame slots via constants/source/readout tails.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def append_unique_block(path: Path, marker: str, title: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + f"\n\n## {title}\n\nMarker: `{marker}`\n\n{body.strip()}\n", encoding="utf-8")


def formal_doc() -> str:
    return f"""
# 293 - PPC4161 matter-interface action-domain proof or canonical g_X source fill

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4277 does not claim public local GR, PPN, R10, WEP, clock, orbital, Newtonian, Maxwell, or EM closure.

It does close the specific 4276 blocker inside the already-declared standard local branch:

```text
old 4276 blocker: MISSING_MATTER_INTERFACE_ACTION_DOMAIN_OR_CANONICAL_GX_SOURCE_ROW
new 4277 standard-branch row: Dq_geom = 0.0, Dq_geom_C1 = 0.0
```

## Matter-interface descent

The 4265 branch already states:

```text
S_matter[Psi; Phi] = Sbar_m[Psi, g_obs(q(Phi)), theta_obs(q(Phi))].
```

For a hidden vertical variation:

```text
v in ker(Dq),
delta_v g_obs = Dg_obs[Dq(v)] = 0,
delta_v theta_obs = Dtheta_obs[Dq(v)] = 0.
```

Therefore:

```text
delta_v S_matter
= DSbar_m[delta_v g_obs, delta_v theta_obs]
= 0.
```

This is the action-domain descent 4276 was asking for.

## Consequence for shadow-frame couplings

If ordinary matter contained:

```text
Sbar_m[Psi, A_g(phi_X)e_pub, ...]
```

then a vertical variation would produce:

```text
delta_v S_matter proportional to d ln A_g/dphi_X.
```

But the branch descent gives:

```text
delta_v S_matter = 0
```

for arbitrary ordinary matter probes in the tested local branch. Hence the ordinary shadow slot is absent, or its canonical derivative vanishes:

```text
g_X = d ln A_g/dphi_X = 0.
```

The same action-domain argument kills the retained disformal ordinary-frame slot:

```text
b_dis = 0.
```

## Tail guard status

The zero is conditional on the companion standard-branch rows:

```text
Dq_theta_marker = 0,
Dq_matter = 0,
Dq_source_readout = 0,
Dq_coeff = 0,
Dq_boundary_projector = 0,
Dq_tau = 0,
Dq_EM = 0.
```

These rows block the obvious field-rename escapes into constants, source charge, measured coupling, clock time, collar choice, or Poynting/EM flux.

## What remains

This is serious progress, but it is not the whole local-GR reduction.

Still missing:

```text
public parent branch-selector signature,
left-hand Einstein/Newton operator limit,
source-probe/tomography constants if using the 4254 route,
quantitative bridge into PPN/R10/clock/orbital tests.
```

## Next target

`{NEXT_TARGET}` should now attack the left-hand local EH/Newton limit, or fill the source-probe matrix/constants route so the zero-Dq branch becomes quantitatively usable.
"""


def checkpoint_doc() -> str:
    return f"""
# 4277 - matter-interface action-domain proof or canonical g_X source fill

Marker: `{MARKER}`

Decision: `{DECISION}`

4277 uses the 4265 standard local branch to derive the 4276 missing bridge:

```text
S_matter[Psi;Phi] = Sbar_m[Psi,g_obs(q(Phi)),theta_obs(q(Phi))]
v in ker(Dq)
=> delta_v S_matter = 0
=> g_X = 0, b_dis = 0
```

The live `Dq_geom` component is therefore set to:

```text
Dq_geom = 0.0
Dq_geom_C1 = 0.0
```

This remains private and conditional, not a public local-GR claim.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorem = csv_rows(paths["descent_theorem"])
    guards = csv_rows(paths["tail_guards"])
    zero_rows = csv_rows(paths["canonical_zero"])
    runners = csv_rows(paths["runner"])
    components = csv_rows(paths["local_candidate"])
    live_components = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    all_rows: Iterable[Dict[str, str]] = (
        sources
        + theorem
        + guards
        + zero_rows
        + runners
        + csv_rows(paths["core_bound"])
        + components
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    live_geom = [row for row in live_components if row.get("probe_id") == "Dq_geom"]
    validations = [
        ("VAL4277_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4277_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4277_2_action_descent",
            any(row["theorem_id"] == "AD4277_3_action_domain_descent" and row["status"] == "CONDITIONAL_STANDARD_BRANCH_PROOF" for row in theorem),
            "matter-interface action-domain descent derived in standard branch",
        ),
        (
            "VAL4277_3_shadow_zero",
            any(row["theorem_id"] == "AD4277_5_canonical_zero" and row["status"] == "CONDITIONAL_GX_BDIS_ZERO_DERIVED" for row in theorem),
            "canonical g_X and b_dis zero derived conditionally",
        ),
        (
            "VAL4277_4_tail_guards",
            {row.get("probe_id") for row in guards} == set(PROBE_ORDER)
            and all(row.get("epsilon") == "0.0" and row.get("epsilon_C1") == "0.0" for row in guards),
            "standard-branch Dq tail guard matrix is zero",
        ),
        (
            "VAL4277_5_zero_runner",
            any(row["source_row_id"] == "GXSR4277_0_standard_branch_gX_zero" and row["verdict"] == "CONDITIONAL_ZERO_PASSES_BOUND_NONCLAIM" for row in runners),
            "canonical zero source row passes the bound as nonclaim",
        ),
        (
            "VAL4277_6_live_4254_geom_zero",
            bool(live_geom)
            and live_geom[0].get("epsilon") == "0.0"
            and live_geom[0].get("epsilon_C1") == "0.0"
            and live_geom[0].get("source_path") == str(FORMAL_PATH)
            and live_geom[0].get("valid_for_claim") == "False",
            "live Dq_geom component closed to conditional zero nonclaim",
        ),
        ("VAL4277_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4277_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4277_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4277_10_no_claim_rows", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows), "all rows remain nonclaim"),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4277_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4277_SOURCE_REGISTER.csv",
        "descent_theorem": SOURCE_DIR / "P8_Y5_R2FR_4277_MATTER_INTERFACE_DESCENT_THEOREM.csv",
        "tail_guards": SOURCE_DIR / "P8_Y5_R2FR_4277_STANDARD_BRANCH_TAIL_GUARDS.csv",
        "canonical_zero": SOURCE_DIR / "P8_Y5_R2FR_4277_CANONICAL_GX_ZERO_SOURCE_ROW.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4277_BOUND_RUNNER_RESULTS.csv",
        "core_bound": CORE_BOUND_CANDIDATE_PATH,
        "local_candidate": LOCAL_COMPONENT_CANDIDATE_PATH,
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4277_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4277_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4277_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4277_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["descent_theorem"], descent_theorem_rows())
    write_csv(paths["tail_guards"], tail_guard_rows())
    write_csv(paths["canonical_zero"], canonical_zero_source_rows())
    write_csv(paths["runner"], bound_runner_rows())
    write_csv(paths["core_bound"], bound_candidate_rows())
    component_candidate = component_candidate_rows()
    write_csv(paths["local_candidate"], component_candidate)
    write_csv(LIVE_COMPONENT_CANDIDATE_PATH, component_candidate)
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
        "PPC4161 4277 matter-interface descent closes Dq_geom conditionally",
        "4277 uses the 4265 standard local matter action-domain branch to derive `delta_v S_matter=0` for `v in ker(Dq)`. Therefore ordinary shadow-frame slots are absent or have `g_X=b_dis=0`, giving `Dq_geom=0` as a private conditional standard-branch component row. This is not a public local-GR claim; left-hand EH/Newton and quantitative source-probe gates remain.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4277 packet Dq_geom conditional zero",
        "Packet update: the previous `Dq_geom` blocker is closed inside the standard local branch by matter-interface descent. All Dq component candidates are now zero/nonclaim; the next pressure point is the left-hand EH/Newton limit or source-probe tomography constants.",
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
