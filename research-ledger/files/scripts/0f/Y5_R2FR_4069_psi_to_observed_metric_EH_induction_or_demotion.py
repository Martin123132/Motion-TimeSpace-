from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4069-Y5-R2FR-psi-to-observed-metric-EH-induction-or-demotion.md"

DECISION = "SINGLE_SCALAR_COVARIANCE_REJECTED_PSI_PACKET_COFRAME_EH_ROUTE_CONSTRUCTED_CONDITIONALLY"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4069_00_4068_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4068_NEXT_TARGET.csv",
        "psi/q_parent induces g_obs plus EH normal form",
        "4068 selected psi-to-metric/EH induction as the next derivation target.",
    ),
    "SRC4069_01_4068_gap": (
        SOURCE_DIR / "P8_Y5_R2FR_4068_CORE_OPEN_GAPS.csv",
        "GAP4068_0_metric_EH_induction",
        "4068 identified metric/EH induction as the P0 bottleneck.",
    ),
    "SRC4069_02_variable_psi": (
        FORMALIZATION / "04-variable-audit.csv",
        "d_mu_psi_covariance",
        "variable audit records the psi-gradient covariance metric route and its warning.",
    ),
    "SRC4069_03_equation_register": (
        FORMALIZATION / "05-equation-register.md",
        "smoothed gradient covariance becomes a Lorentzian metric",
        "equation register records the assumption that must be repaired.",
    ),
    "SRC4069_04_known_limits": (
        FORMALIZATION / "11-known-limits-targets.md",
        "If the Einstein-Hilbert term is simply assumed",
        "known-limits document states the EH-assumption demotion risk.",
    ),
    "SRC4069_05_core_action": (
        PROJECT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
        "Constructing the emergent metric",
        "core action document claims emergent metric construction from psi gradients.",
    ),
    "SRC4069_06_fundamental_action": (
        PROJECT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "The emergent metric relation",
        "fundamental action draft gives the metric relation as a central step.",
    ),
    "SRC4069_07_effective_field": (
        PROJECT / "core-mts-framework" / "field-theory" / "the-effective-field-theory-of-motion-timespace.md",
        "Coarse-graining the ψ-covariance defines the emergent metric",
        "effective field draft states the covariance-to-metric route.",
    ),
    "SRC4069_08_local_eh_requirements": (
        SOURCE_DIR / "P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv",
        "EH505_0_operator_reduction",
        "older local EH reduction gate lists the operator requirement.",
    ),
    "SRC4069_09_local_eh_theorem": (
        SOURCE_DIR / "P8_LOCAL_EH_REDUCTION_THEOREM_ATTEMPT.csv",
        "T506_EH_plus_silent_reduction",
        "older theorem attempt gives EH-plus-silent-sector condition.",
    ),
    "SRC4069_10_min_parent_blocks": (
        SOURCE_DIR / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "A511_0_EH_core",
        "minimal parent local GR action block records the EH core.",
    ),
    "SRC4069_11_symbol_map": (
        SOURCE_DIR / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "g_obs / g_readout",
        "symbol map records observed metric/readout placement and its limits.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4069_SOURCE_REGISTER.csv",
    "scalar_rank_test": SOURCE_DIR / "P8_Y5_R2FR_4069_SCALAR_COVARIANCE_RANK_TEST.csv",
    "coframe_repair": SOURCE_DIR / "P8_Y5_R2FR_4069_PSI_PACKET_COFRAME_REPAIR_THEOREM.csv",
    "eh_normal_form": SOURCE_DIR / "P8_Y5_R2FR_4069_EH_NORMAL_FORM_GATE.csv",
    "parent_requirements": SOURCE_DIR / "P8_Y5_R2FR_4069_PARENT_REQUIREMENTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4069_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4069_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4069_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4069_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4069_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, source_tuple in SOURCES.items():
        path, needle, role = source_tuple
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def scalar_rank_test_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "test_id": "RANK4069_0_single_scalar",
            "object_tested": "C_mn = <partial_m psi partial_n psi> for one deterministic real scalar",
            "result": "FAILS_AS_METRIC",
            "reason": "At each point partial_m psi partial_n psi is an outer product, so rank(C) <= 1 before any ensemble repair; a 4D metric must be nondegenerate rank 4.",
            "consequence": "the old single-scalar wording cannot derive g_obs",
            "repair": "replace single scalar by a rank-four psi packet/coframe or stochastic multiplet with an invertible covariance frame",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "RANK4069_1_positive_covariance",
            "object_tested": "C_mn = <partial_m psi^A partial_n psi^A> with Euclidean internal sum",
            "result": "FAILS_LORENTZIAN_SIGNATURE",
            "reason": "A Euclidean covariance is positive semidefinite; it can describe a spatial/Riemannian metric but not a Lorentzian metric without an internal time direction or background subtraction.",
            "consequence": "smoothing alone does not produce the GR metric signature",
            "repair": "introduce an internal Lorentz metric eta_AB or a distinguished clock phase in the psi packet",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "RANK4069_2_eta_plus_covariance",
            "object_tested": "g_mn = eta_mn + L_*^2 <partial_m psi partial_n psi>",
            "result": "WORKS_ONLY_AS_PERTURBATIVE_ANSATZ",
            "reason": "Adding eta_mn can preserve Lorentzian signature for small covariance, but eta then supplies the causal structure rather than deriving it.",
            "consequence": "good weak-field ansatz; not a background-independent metric emergence proof",
            "repair": "treat eta as local tangent-space internal metric eta_AB in a coframe formula, not as a fixed spacetime background",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "test_id": "RANK4069_3_dimension",
            "object_tested": "metric normalization",
            "result": "REQUIRES_SCALE_OR_FRAME_NORMALIZATION",
            "reason": "partial psi partial psi has psi-units squared over length squared; g_mn is dimensionless.",
            "consequence": "L_* or equivalent normalization must be parent-owned or explicitly calibrated",
            "repair": "define e^A_m = L_A <partial_m Psi^A> or normalize covariance eigenframes before forming g_mn",
            "valid_for_public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def coframe_repair_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "COF4069_0_metric_induction",
            "statement": "Let Psi^A be a rank-four local motion packet with A=0..3 and define e^A_m = L_A <D_m Psi^A>_loc. If det(e) != 0 and the internal packet metric eta_AB has Lorentzian signature, then g_obs_mn = eta_AB e^A_m e^B_n is a nondegenerate Lorentzian observed metric.",
            "proof_sketch": "An invertible coframe pulls the fixed internal Lorentz form eta_AB to the tangent space; congruence by an invertible matrix preserves signature by Sylvester inertia.",
            "status": "PROVED_CONDITIONAL_ON_RANK_FOUR_PACKET",
            "what_closed": "metric nondegeneracy and Lorentzian signature can be derived from a psi packet/coframe rather than assumed from one scalar covariance",
            "remaining_parent_input": "parent action must own Psi^A, eta_AB/internal clock direction, L_A normalization, and rank-four regularity",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "COF4069_1_background_repair",
            "statement": "The old eta_mn background can be reinterpreted as eta_AB, an internal tangent-space metric used only after the coframe descends.",
            "proof_sketch": "The spacetime metric is g_obs=e^T eta e; eta_AB is not a fixed spacetime metric and does not by itself define distances between manifold points.",
            "status": "REPAIR_ROUTE_CONSTRUCTED",
            "what_closed": "avoids the strongest background-independence objection to g=eta+covariance",
            "remaining_parent_input": "local Lorentz/internal-frame gauge story must be written",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "COF4069_2_quotient_readout",
            "statement": "If public observables depend on the psi packet only through e^A_m and g_obs_mn, then vertical packet rotations/noise directions lie in ker(Dq_parent).",
            "proof_sketch": "For q_parent(Phi)=(e,g_obs,...), variations that leave e and g_obs fixed have Dq_parent[v]=0, so the 2570 quotient chain rule kills their matter/readout effect.",
            "status": "EXACT_CONDITIONAL_QUOTIENT_APPLICATION",
            "what_closed": "connects psi-packet induction to the existing quotient machinery",
            "remaining_parent_input": "complete q_parent and vertical generators must be parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "COF4069_3_single_scalar_demotion",
            "statement": "The phrase 'a scalar psi defines the metric by gradient covariance' must be demoted unless psi is explicitly a packet/ensemble whose covariance has four independent directions and a Lorentzian internal form.",
            "proof_sketch": "RANK4069_0 and RANK4069_1 rule out the literal single-scalar reading.",
            "status": "DEMOTION_OF_OLD_WORDING",
            "what_closed": "removes a mathematically weak claim from the GR bridge",
            "remaining_parent_input": "canonical notation must say psi-packet or coframe-generating motion field, not lone scalar, if this route is retained",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def eh_normal_form_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "EHNF4069_0_two_derivative_universality",
            "gate": "local diffeomorphism-invariant two-derivative metric normal form",
            "conditional_result": "A local, four-dimensional, two-derivative, diffeomorphism-invariant metric action with second-order metric equations has the Einstein-Hilbert plus cosmological-constant form, up to boundary/topological terms.",
            "status": "STANDARD_NORMAL_FORM_CONDITIONAL",
            "MTS_requirement": "show the psi-packet/coframe parent action flows in the IR to only the massless spin-2 metric mode with extra torsion/scalar/vector modes silent or heavy",
            "if_fails": "EH remains an adopted effective branch rather than derived",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "EHNF4069_1_extra_mode_silence",
            "gate": "torsion, nonmetricity, scalar, vector, and higher-curvature leakage",
            "conditional_result": "If extra coframe/connection modes are constrained, massive above the local scale, topological, or no-flux silent, they do not alter the local <=2PN EH branch.",
            "status": "CONDITIONAL_ON_EXISTING_SILENCE_GATES",
            "MTS_requirement": "supply actual operator inventory, signs, gaps, and boundary conditions for the psi-packet parent action",
            "if_fails": "retain PPN/R10/orbital residual coefficient rows",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "EHNF4069_2_coupling",
            "gate": "coefficient of EH term",
            "conditional_result": "The form of EH can be induced without predicting the numerical value of kappa_eff; G_N remains calibrated unless parent normalization supplies the coefficient.",
            "status": "FORM_DERIVATION_ONLY_NOT_G_NUMERIC",
            "MTS_requirement": "derive or explicitly calibrate L_A, kappa_eff, and any induced Planck scale",
            "if_fails": "safe GR-reduction branch still possible, but no Newton-G prediction",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "EHNF4069_3_matter_same_metric",
            "gate": "universal matter/EM coupling to induced g_obs",
            "conditional_result": "The induced metric route only supports local GR if the same g_obs couples to matter, EM, clocks, and PPN readouts.",
            "status": "CARRIES_FORWARD_4068_MATTER_GATE",
            "MTS_requirement": "prove no shadow matter frame or hidden source-only prefactor",
            "if_fails": "WEP/source-coupling residuals stay live",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def parent_requirement_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "requirement_id": "REQ4069_0_packet",
            "requirement": "psi must be a rank-four packet/coframe generator, not a literal lone scalar, for metric emergence",
            "current_status": "NOT_CANONICALIZED",
            "acceptance_test": "write parent variables Psi^A or equivalent packet and show det(e^A_m) != 0 on the local branch",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "requirement_id": "REQ4069_1_internal_lorentz_form",
            "requirement": "internal Lorentzian form eta_AB or clock/space split must be parent-owned",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "acceptance_test": "eta_AB is an internal tangent-space structure and observables are invariant under the relevant internal frame symmetry",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "requirement_id": "REQ4069_2_normalization",
            "requirement": "L_A or covariance normalization must make e^A_m and g_obs dimensionally valid",
            "current_status": "MISSING_SCALE_OWNER",
            "acceptance_test": "normalization is derived, measured, or topological/integration-constant with no hidden source dependence",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "requirement_id": "REQ4069_3_IR_spin2",
            "requirement": "IR action must contain only the massless spin-2 metric mode at leading local order",
            "current_status": "CONDITIONAL_NORMAL_FORM_ONLY",
            "acceptance_test": "extra modes are gauge, massive, topological, boundary-silent, or scored as residuals below empirical locks",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
        {
            "requirement_id": "REQ4069_4_EH_coefficient",
            "requirement": "EH coefficient must be derived or explicitly calibrated",
            "current_status": "CALIBRATED_NOT_PREDICTED",
            "acceptance_test": "state G_N is measured unless a parent normalization theorem supplies kappa_eff",
            "priority": "P2",
            "timestamp_utc": current_timestamp,
        },
    ]


def static_rows(current_timestamp: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "decision_gate": [
            {
                "decision_id": "DEC4069_0",
                "decision": DECISION,
                "summary": "The literal single-scalar covariance route is mathematically rejected, but a stronger psi-packet/coframe route proves Lorentzian metric induction conditionally and gives a conditional EH normal-form path.",
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            },
            {
                "decision_id": "DEC4069_1",
                "decision": "DO_NOT_DEMOTE_WHOLE_GR_BRIDGE_YET",
                "summary": "Demote the old wording, not the whole route: the next work should formalize the psi-packet parent action and see whether the coframe/EH gates can be signed.",
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            },
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4069_0",
                "claim": "a literal single scalar psi derives the spacetime metric by gradient covariance",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "rank and Lorentzian-signature tests fail without packet/internal-metric repair",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4069_1",
                "claim": "a rank-four psi packet/coframe can induce a Lorentzian observed metric",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "conditional theorem closes metric signature/nondegeneracy if packet, eta_AB, normalization, and rank are parent-owned",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4069_2",
                "claim": "MTS derives the EH action and local GR as a completed theorem",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "EH normal form is conditional on IR spin-2 universality, extra-mode silence, and coefficient ownership",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4069_3",
                "claim": "MTS predicts the numerical value of Newton G",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "4069 only preserves calibrated kappa_eff/G_N unless a future parent normalization theorem closes",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4069_0",
                "next_doc": "4070-Y5-R2FR-psi-packet-coframe-parent-action-normalization-and-torsion-gate.md",
                "next_script": "scripts/Y5_R2FR_4070_psi_packet_coframe_parent_action_normalization_and_torsion_gate.py",
                "reason": "formalize the psi-packet/coframe parent action, normalization scale, internal Lorentz symmetry, and torsion/extra-mode silence; this is the route that could turn 4069 from conditional repair into a real GR-reduction derivation",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4069",
                "status": DECISION,
                "formalization_modified": False,
                "public_claim": False,
                "github_action": False,
                "timestamp_utc": current_timestamp,
            }
        ],
    }


def validate_sources(source_table: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in source_table if not row["exists"]]
    absent_needles = [row["source_id"] for row in source_table if not row["needle_found"]]
    if missing or absent_needles:
        return False, f"missing={missing}; absent_needles={absent_needles}"
    return True, "all cited source paths exist and needles are present"


def validate_csv_parse(paths: Iterable[Path]) -> Tuple[bool, str]:
    details: List[str] = []
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as input_file:
                parsed_rows = list(csv.DictReader(input_file))
            details.append(f"{path.name}:rows={len(parsed_rows)}")
    except Exception as exc:  # pragma: no cover
        return False, repr(exc)
    return True, "; ".join(details)


def validate_no_public_claim(row_groups: Iterable[List[Dict[str, object]]]) -> Tuple[bool, str]:
    offenders: List[str] = []
    for rows in row_groups:
        for row in rows:
            for key in ("valid_for_claim", "valid_for_public_claim", "allowed_public", "public_claim", "github_action"):
                if key in row and str(row[key]).lower() == "true":
                    offenders.append(str(row))
    if offenders:
        return False, f"public/github claim flags found: {offenders}"
    return True, "all claim-bearing rows preserve public/github false"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    claims_ok, claims_detail = validate_no_public_claim(row_groups)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4069_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4069_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4069_02_no_public_or_github_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4069_03_single_scalar_rejected",
            "passed": "FAILS_AS_METRIC" in joined and "FAILS_LORENTZIAN_SIGNATURE" in joined,
            "detail": "literal single-scalar covariance route is rejected by rank/signature gates",
        },
        {
            "check_id": "VAL4069_04_coframe_repair_constructed",
            "passed": "PROVED_CONDITIONAL_ON_RANK_FOUR_PACKET" in joined and "g_obs_mn = eta_AB e^A_m e^B_n" in joined,
            "detail": "psi-packet/coframe Lorentzian metric theorem is constructed conditionally",
        },
        {
            "check_id": "VAL4069_05_EH_normal_form_conditional",
            "passed": "STANDARD_NORMAL_FORM_CONDITIONAL" in joined and "FORM_DERIVATION_ONLY_NOT_G_NUMERIC" in joined,
            "detail": "EH normal form is conditional and Newton G remains unpredicted",
        },
        {
            "check_id": "VAL4069_06_next_target",
            "passed": "4070-Y5-R2FR-psi-packet-coframe-parent-action-normalization-and-torsion-gate.md" in joined,
            "detail": "next target attacks packet parent action and extra-mode gates",
        },
        {"check_id": "VAL4069_07_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4069 - Psi To Observed Metric/EH Induction Or Demotion

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## The Important Result

4069 rejects the weak version:

```text
one real scalar psi -> <d psi d psi> -> full spacetime metric
```

That route fails as a derivation because a single scalar gradient outer product is rank `<=1`, and a Euclidean covariance cannot by itself produce Lorentzian signature.

But 4069 does **not** kill the GR bridge. It upgrades the viable route:

```text
rank-four psi packet / motion coframe
e^A_mu = L_A <D_mu Psi^A>_loc
g_obs_mu_nu = eta_AB e^A_mu e^B_nu
```

If `det(e) != 0` and `eta_AB` is an internal Lorentzian metric, then `g_obs` is a genuine nondegenerate Lorentzian metric. That part is a clean conditional proof, not handwaving.

## EH Normal Form

The EH step is still conditional but now sharply stated:

```text
psi packet -> induced coframe/metric
local diffeomorphism + internal Lorentz symmetry
only massless spin-2 survives at leading two-derivative order
extra torsion/scalar/vector/higher-curvature modes silent or residualized
=> EH + Lambda + boundary/topological terms
```

So the win is: the metric-signature problem has a plausible derived route. The remaining work is parent-action ownership of the packet, normalization, internal Lorentz form, and extra-mode silence.

## What Must Be Demoted

The old phrase "a scalar field psi defines the metric by gradient covariance" should not be used literally anymore. The safe version is:

```text
an MTS motion packet, whose rank-four local coframe/covariance descends through q_parent,
induces the observed metric.
```

## Next

`4070` should build the psi-packet/coframe parent action gate: field content, normalization, internal Lorentz symmetry, torsion/extra-mode silence, and the route to EH normal form.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    scalar_rank = scalar_rank_test_rows(current_timestamp)
    coframe_repair = coframe_repair_rows(current_timestamp)
    eh_normal_form = eh_normal_form_rows(current_timestamp)
    parent_requirements = parent_requirement_rows(current_timestamp)
    static = static_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["scalar_rank_test"], scalar_rank)
    write_csv(OUTPUTS["coframe_repair"], coframe_repair)
    write_csv(OUTPUTS["eh_normal_form"], eh_normal_form)
    write_csv(OUTPUTS["parent_requirements"], parent_requirements)
    write_csv(OUTPUTS["decision_gate"], static["decision_gate"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["scalar_rank_test"],
        OUTPUTS["coframe_repair"],
        OUTPUTS["eh_normal_form"],
        OUTPUTS["parent_requirements"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        scalar_rank,
        coframe_repair,
        eh_normal_form,
        parent_requirements,
        static["decision_gate"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, row_groups)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
