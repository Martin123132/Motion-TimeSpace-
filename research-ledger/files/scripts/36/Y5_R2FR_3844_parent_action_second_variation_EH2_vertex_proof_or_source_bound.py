from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3844"
BRANCH = "MTS_R2FR_Y5_PARENT_ACTION_SECOND_VARIATION_EH2_LOVELOCK_ROUTE_3844"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3844-Y5-R2FR-parent-action-second-variation-EH2-vertex-proof-or-source-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3843 = PCW / "3843-Y5-R2FR-integrated-beta-ledger-threshold-dashboard-and-source-fill-queue.md"
P_3838 = PCW / "3838-Y5-R2FR-EH2-parent-second-variation-vertex-match-or-beta-bound.md"
P_1008 = PCW / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md"
P_1030 = PCW / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md"
P_1029 = PCW / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md"
P_1025 = PCW / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md"

CSV_3843_LEDGER = OUT / "P8_Y5_R2FR_3843_INTEGRATED_BETA_LEDGER.csv"
CSV_3843_QUEUE = OUT / "P8_Y5_R2FR_3843_SOURCE_FILL_QUEUE.csv"
CSV_3843_VALIDATION = OUT / "P8_Y5_BRR545_3843_VALIDATION.csv"
CSV_3838_EH2 = OUT / "P8_Y5_R2FR_3838_EH2_MISMATCH_DECOMPOSITION.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"
CSV_3828_ZERO = OUT / "P8_Y5_R2FR_3828_ZERO_CONDITION_THEOREM.csv"
CSV_637_PARENT = OUT / "P8_Y5_R10_637_PARENT_ACTION_DERIVATION_ATTEMPT.csv"
CSV_1008_PARENT = OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv"
CSV_1030_PUBLIC = OUT / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv"
CSV_1029_SHADOW = OUT / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv"
CSV_1025_SECOND = OUT / "P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3844_SOURCE_REGISTER.csv",
    "theorem_route": OUT / "P8_Y5_R2FR_3844_LOVELOCK_EH2_ROUTE.csv",
    "clause_audit": OUT / "P8_Y5_R2FR_3844_PARENT_CLAUSE_AUDIT.csv",
    "eh2_update": OUT / "P8_Y5_R2FR_3844_EH2_BOUND_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3844_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3844_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3844_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3844_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3844_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3844_0_3843_doc", P_3843, "anti-circling checkpoint"),
    ("SRC3844_1_3843_ledger", CSV_3843_LEDGER, "B_L2_operator"),
    ("SRC3844_2_3843_queue", CSV_3843_QUEUE, "SFQ3843_0"),
    ("SRC3844_3_3843_validation", CSV_3843_VALIDATION, "PASS"),
    ("SRC3844_4_3838_doc", P_3838, "core beta question"),
    ("SRC3844_5_3838_eh2", CSV_3838_EH2, "EH2M3838_0_L2_operator"),
    ("SRC3844_6_3818_poisson", CSV_3818_POISSON, "POI3818_0_linearized_00"),
    ("SRC3844_7_3828_zero", CSV_3828_ZERO, "ZPPN3828_2_beta_lock"),
    ("SRC3844_8_637_parent_action", CSV_637_PARENT, "PA637_3_action_descent"),
    ("SRC3844_9_1008_parent_doc", P_1008, "missing_explicit_current_chain"),
    ("SRC3844_10_1008_parent_audit", CSV_1008_PARENT, "PVA1008_0_parent_action"),
    ("SRC3844_11_1030_public_doc", P_1030, "single-public-metric parent action"),
    ("SRC3844_12_1030_public_contract", CSV_1030_PUBLIC, "SPM1030_6_contract_verdict"),
    ("SRC3844_13_1029_shadow_doc", P_1029, "no-shadow-frame theorem"),
    ("SRC3844_14_1029_shadow_audit", CSV_1029_SHADOW, "NST1029_6_verdict"),
    ("SRC3844_15_1025_second_doc", P_1025, "exact local second-variation contract"),
    ("SRC3844_16_1025_second_derivation", CSV_1025_SECOND, "SV1025_6_verdict"),
]

LOVELOCK_AIP_URL = "https://pubs.aip.org/aip/jmp/article/12/3/498/223441/The-Einstein-Tensor-and-Its-Generalizations"
LOVELOCK_INSPIRE_URL = "https://inspirehep.net/literature/67644"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "input_for_parent_second_variation_EH2_lovelock_route",
                "claim_use": "nonclaim_derivation_route_and_clause_audit_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_route_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "LV3844_0_reference",
            "step": "external theorem route",
            "mathematical_statement": "Lovelock-style uniqueness: in 4D, a local metric-only, diffeomorphism-covariant, divergence-free, second-order gravitational field equation has the Einstein tensor plus cosmological metric term as the unique visible tensor structure.",
            "derived_consequence_for_MTS": "if the MTS local visible branch satisfies the clauses, the visible metric operator is EH/GR through second order up to cosmological/boundary terms",
            "status": "REFERENCE_ROUTE_VALID_NOT_MTS_SIGNED",
            "source": f"Lovelock 1971 DOI 10.1063/1.1665613; {LOVELOCK_AIP_URL}; {LOVELOCK_INSPIRE_URL}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "route_id": "LV3844_1_visible_branch",
            "step": "visible metric branch assumption",
            "mathematical_statement": "q(Phi) supplies a single 4D public metric/coframe g_obs for rods, clocks, free fall, photons, and source readout before PPN fitting",
            "derived_consequence_for_MTS": "the parent action can be tested as a metric theory rather than a multi-frame or scalar-tensor theory",
            "status": "CONDITIONAL_FROM_1030_NOT_PARENT_SIGNED",
            "source": rel(CSV_1030_PUBLIC),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "route_id": "LV3844_2_parent_operator",
            "step": "second-order parent operator restriction",
            "mathematical_statement": "delta S_parent/delta g_obs is local and contains at most second derivatives of g_obs on the compact exterior local branch",
            "derived_consequence_for_MTS": "higher-derivative, nonlocal, scalar, torsion, nonmetricity, and disformal operators cannot shift the beta-order vertex",
            "status": "MISSING_EXPLICIT_PARENT_LAGRANGIAN_AND_OPERATOR_CLASS",
            "source": rel(P_1008),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "route_id": "LV3844_3_eh2_zero_if_clauses_pass",
            "step": "EH2 collapse theorem",
            "mathematical_statement": "Lovelock clauses + Newtonian normalization + Hilbert source glue imply B_L2_operator=0, B_grav_energy_source=0, and B_nonEH2_operator=0",
            "derived_consequence_for_MTS": "B_EH2_vertex reduces to the remaining field-redefinition/gauge/readout residual rather than an independent beta self-coupling gap",
            "status": "EXACT_CONDITIONAL_EH2_ROUTE",
            "source": f"{rel(CSV_3838_EH2)}; {rel(CSV_3818_POISSON)}; {rel(CSV_3828_ZERO)}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "route_id": "LV3844_4_current_verdict",
            "step": "current MTS proof status",
            "mathematical_statement": "current corpus has contracts for quotient/public metric/action descent/source glue, but not a signed parent visible Lagrangian satisfying all Lovelock clauses",
            "derived_consequence_for_MTS": "EH2 is not rejected, but not proven; the route is now a precise parent-action construction problem",
            "status": "EH2_ZERO_NOT_CLAIMED_ROUTE_SHARPENED",
            "source": f"{rel(CSV_637_PARENT)}; {rel(CSV_1008_PARENT)}; {rel(CSV_1030_PUBLIC)}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def clause_audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "LVC3844_0_4d_visible_metric",
            "required_clause": "single 4D public metric/coframe visible branch",
            "mathematical_form": "q(Phi) -> g_obs on a 4D local exterior arena; ordinary observables factor through g_obs",
            "would_close": "lets Lovelock theorem apply to the local visible branch",
            "current_status": "CONTRACT_AVAILABLE_NOT_PARENT_SIGNED",
            "blocking_source": rel(CSV_1030_PUBLIC),
            "if_unsigned": "multi-frame/shadow-frame or scalar-tensor countermodels remain legal",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3844_1_diffeomorphism_covariance",
            "required_clause": "parent visible equation is covariant and divergence-consistent",
            "mathematical_form": "nabla_mu E_vis^{mu nu}=0 with matter/source descent on the same q-owned branch",
            "would_close": "forces Bianchi/self-source consistency instead of arbitrary beta coefficient fitting",
            "current_status": "PARTIAL_CONTRACT_NO_PARENT_VARIATION",
            "blocking_source": rel(CSV_1008_PARENT),
            "if_unsigned": "B_grav_energy_source remains active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3844_2_local_second_order",
            "required_clause": "local second-order metric operator",
            "mathematical_form": "E_vis[g_obs] depends on g_obs, partial g_obs, partial^2 g_obs only, with no nonlocal inverse operators",
            "would_close": "activates the Lovelock uniqueness route for the visible operator",
            "current_status": "MISSING_EXPLICIT_PARENT_LAGRANGIAN",
            "blocking_source": rel(P_1008),
            "if_unsigned": "B_L2_operator and B_nonEH2_operator remain active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3844_3_metric_only_no_extra_dof",
            "required_clause": "no retained scalar/vector/torsion/nonmetricity/disformal visible beta-order degree",
            "mathematical_form": "kernel/projector removes representative fields or gives theorem-zero residuals before beta extraction",
            "would_close": "removes scalar-tensor and higher-operator beta contamination",
            "current_status": "UNSIGNED_WITH_KNOWN_COUNTERCHANNELS",
            "blocking_source": f"{rel(CSV_1029_SHADOW)}; {rel(CSV_1025_SECOND)}",
            "if_unsigned": "B_nonEH2_operator and B_extra_scalar2 remain active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3844_4_hilbert_source_glue",
            "required_clause": "ordinary matter source is the Hilbert/coframe variation of the same public metric action",
            "mathematical_form": "T_total := delta S_matter / delta g_obs and E_vis = kappa T_total with no source-only weights",
            "would_close": "locks Newtonian source normalization to gravitational self-energy at second order",
            "current_status": "CONDITIONAL_FROM_1030_3818_NOT_SIGNED",
            "blocking_source": f"{rel(CSV_1030_PUBLIC)}; {rel(CSV_3818_POISSON)}",
            "if_unsigned": "B_grav_energy_source and source-spurion rows remain active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3844_5_boundary_topological_silence",
            "required_clause": "boundary/topological/cosmological terms do not shift beta-order local exterior self-coupling",
            "mathematical_form": "GHY/topological/reference terms are fixed before variation or vanish in local beta projection; Lambda term not used to fit beta",
            "would_close": "prevents boundary/reference terms from mimicking EH2 success",
            "current_status": "BOUNDARY_SPECIALIZATION_REQUIRED",
            "blocking_source": rel(CSV_3843_LEDGER),
            "if_unsigned": "B_boundary2 and B_eps_temporal_domain remain active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3844_6_newtonian_normalization",
            "required_clause": "Newtonian C_t fixes the EH coefficient before beta extraction",
            "mathematical_form": "G_ref/kappa_0 is calibrated from the same Hilbert source and not from fitted orbital mu",
            "would_close": "converts Lovelock proportionality constant into the observed Newtonian coupling without beta smuggling",
            "current_status": "CONDITIONAL_FROM_3818_WITH_SOURCE_GUARDS",
            "blocking_source": rel(CSV_3818_POISSON),
            "if_unsigned": "the EH shape could be right while G/source normalization remains circular",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3844_7_readout_gauge",
            "required_clause": "field variable and PPN gauge are fixed before comparing beta",
            "mathematical_form": "g00 = -1 + 2U - 2 beta U^2 + eps in a declared PPN gauge/readout",
            "would_close": "prevents nonlinear field redefinition from changing beta after EH2 is matched",
            "current_status": "READOUT_GAUGE_LOCK_REQUIRED",
            "blocking_source": rel(CSV_3843_LEDGER),
            "if_unsigned": "B_field_redef_gauge remains active even if Lovelock clauses close",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3844_8_verdict",
            "required_clause": "all Lovelock/EH2 clauses pass simultaneously",
            "mathematical_form": "LVC3844_0 through LVC3844_7 all parent-signed or source-bounded on the same branch",
            "would_close": "B_EH2_vertex has an exact theorem-zero route modulo readout/gauge residual",
            "current_status": "FAIL_CURRENT_CLAIM_EXACT_ROUTE_AVAILABLE",
            "blocking_source": "this audit",
            "if_unsigned": "retain EH2 nonclaim bound and construct parent visible Lagrangian candidate next",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def eh2_update_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "EH2U3844_0_lovelock_clause_failure",
            "observable": "B_Lovelock_clause_failure",
            "formula": "B_Lovelock_clause_failure <= B_public_metric + B_covariance_Bianchi + B_local_second_order + B_no_extra_dof + B_Hilbert_source + B_boundary_topological + B_Newtonian_normalization",
            "new_detail": "Lovelock route turns EH2 from a free second-order mismatch into a finite list of parent-action clauses",
            "status": "DERIVATION_ROUTE_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EH2U3844_1_if_clauses_pass",
            "observable": "B_EH2_vertex",
            "formula": "if B_Lovelock_clause_failure=0 then B_L2_operator=0, B_grav_energy_source=0, B_nonEH2_operator=0 and B_EH2_vertex <= B_field_redef_gauge",
            "new_detail": "the beta self-coupling gap collapses to readout/gauge after parent EH uniqueness is signed",
            "status": "EXACT_CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EH2U3844_2_current_bound",
            "observable": "B_EH2_vertex",
            "formula": "B_EH2_vertex <= B_Lovelock_clause_failure + B_field_redef_gauge + B_unclassified_EH2_residual",
            "new_detail": "current corpus has no signed parent visible action, so the residual remains nonclaim rather than zero",
            "status": "CURRENT_NONCLAIM_BOUND_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3844_0_lovelock_route",
            "gate": "Lovelock/EH2 route is mathematically coherent",
            "status": "PASS_CONDITIONAL_ROUTE",
            "claim_allowed": False,
            "reason": "4D metric-only local second-order covariance would force EH/GR visible operator up to Lambda/boundary",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3844_1_parent_action",
            "gate": "explicit parent visible Lagrangian exists",
            "status": "BLOCKED_MISSING_EXPLICIT_PARENT_VISIBLE_LAGRANGIAN",
            "claim_allowed": False,
            "reason": "1008/637 provide contracts and descent attempts, not a signed visible action satisfying Lovelock clauses",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3844_2_extra_dof",
            "gate": "metric-only/no-extra-dof clause",
            "status": "BLOCKED_SCALAR_FRAME_OPERATOR_CHANNELS_RETAINED",
            "claim_allowed": False,
            "reason": "1029/1030/1025 keep shadow-frame and scalar/Hessian channels nonclaim",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3844_3_eh2_zero",
            "gate": "EH2 vertex theorem-zero",
            "status": "BLOCKED_LOVELOCK_CLAUSES_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "reason": "conditional route exists, but all clauses are not signed on the same parent branch",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3844_4_no_fake_claim",
            "gate": "no EH2/local-GR claim is promoted",
            "status": "PASS_NO_CLAIM_PROMOTED",
            "claim_allowed": False,
            "reason": "all theorem/closure rows remain nonclaim",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3844_5_next_action",
            "gate": "next target is constructive parent action candidate",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "the proof path now demands a visible MTS parent Lagrangian candidate, not another generic missing-row sweep",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3844_0",
            "decision": "EH2 is not dead; it has a clean theorem route",
            "consequence": "use Lovelock conditions as the parent-action target rather than trying to tune beta directly",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3844_1",
            "decision": "current corpus does not yet prove EH2 zero",
            "consequence": "no local-GR or beta claim; retain B_EH2_vertex nonclaim bound",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3844_2",
            "decision": "next step must be constructive",
            "consequence": "write the minimal visible parent action candidate in MTS variables and test every Lovelock clause against it",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3844_0",
            "next_checkpoint": "3845-Y5-R2FR-visible-metric-parent-action-candidate-from-MTS-or-Lovelock-failure.md",
            "script": "scripts/Y5_R2FR_3845_visible_metric_parent_action_candidate_from_MTS_or_Lovelock_failure.py",
            "objective": "construct the minimal visible parent action candidate from MTS motion/time/space objects and test whether it satisfies the 3844 Lovelock/EH2 clauses",
            "reason": "3844 turns EH2 into a constructive parent-action problem; the next move should build or reject that candidate, not just repeat missing-source language",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_EH2_LOVELOCK_ROUTE_SHARPENED",
            "claim": "no EH2, beta, local-GR, or Newtonian-source claim",
            "next": "3845 visible metric parent action candidate from MTS or Lovelock failure",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        vals = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, object]],
    theorem_route: list[dict[str, object]],
    clause_audit: list[dict[str, object]],
    eh2_update: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3844 - Parent Action Second Variation EH2 Vertex Proof Or Source Bound

Private checkpoint. This is a derivation-first attempt on the highest-leverage beta obstruction from 3843: the parent EH second variation. It does not claim `B_EH2_vertex=0`, `beta=1`, local GR, or a PPN pass.

Generated: `{timestamp}`

## Result

The best route is a Lovelock/EH uniqueness lock:

`4D public metric + diffeomorphism covariance + local second-order metric equations + no extra visible degrees + Hilbert source glue => EH/GR visible operator`.

If those clauses are parent-signed on the same compact local branch, then the EH2 gap collapses:

`B_L2_operator=0`, `B_grav_energy_source=0`, `B_nonEH2_operator=0`, so `B_EH2_vertex <= B_field_redef_gauge`.

That is real forward movement: the target is no longer "find the missing coupling somehow"; it is "construct the parent visible action and test these clauses."

## External Theorem Anchor

- Lovelock 1971, DOI `10.1063/1.1665613`: {LOVELOCK_AIP_URL}
- Inspire record: {LOVELOCK_INSPIRE_URL}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Lovelock/EH2 Route

{markdown_table(theorem_route, ["route_id", "step", "status", "derived_consequence_for_MTS", "source"])}

## Parent Clause Audit

{markdown_table(clause_audit, ["clause_id", "required_clause", "current_status", "would_close", "if_unsigned"])}

## EH2 Bound Update

{markdown_table(eh2_update, ["row_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This does not prove local GR yet, but it changes the shape of the work. The EH2/beta question now has a respectable theorem route: make MTS satisfy the Lovelock clauses, and the GR quadratic vertex follows. If MTS cannot supply a visible parent action satisfying those clauses, this route should fail explicitly rather than being patched by beta-fitting.

Next target: `3845-Y5-R2FR-visible-metric-parent-action-candidate-from-MTS-or-Lovelock-failure.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3843", "Current State After 3844", 1)
    paragraph = (
        "`3844` attacks the highest-leverage beta obstruction directly. "
        "The derived route is Lovelock/EH uniqueness: a 4D single-public-metric, diffeomorphism-covariant, local second-order, metric-only visible branch with Hilbert source glue must reduce to the EH/GR visible operator up to cosmological/boundary terms. "
        "If those clauses are parent-signed, then `B_L2_operator=0`, `B_grav_energy_source=0`, and `B_nonEH2_operator=0`, so `B_EH2_vertex <= B_field_redef_gauge`. "
        "Current MTS does not yet claim this because the explicit parent visible Lagrangian, no-extra-dof clause, source glue, and boundary/readout clauses are not all signed on one branch. "
        "The next step is constructive: build the minimal visible MTS parent action candidate or record the Lovelock route as a clean failure.\n\n"
    )
    anchor = "`3843` integrates"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3844-Y5-R2FR-parent-action-second-variation-EH2-vertex-proof-or-source-bound.md`

Target: try to prove the parent visible second variation matches the EH/GR quadratic vertex and gravitational self-source, or emit explicit residual source-bound rows.

This is the best next move because 3843 shows EH2 is the highest-leverage route from symbolic beta ledger to derived local GR."""
    new_gate = """`3845-Y5-R2FR-visible-metric-parent-action-candidate-from-MTS-or-Lovelock-failure.md`

Target: construct the minimal visible parent action candidate from MTS motion/time/space objects and test every Lovelock/EH2 clause.

This is the best next move because 3844 turns EH2 into a constructive parent-action problem rather than another missing-row sweep."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3844_LOVELOCK_EH2_ROUTE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3844_PARENT_CLAUSE_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3844_EH2_BOUND_UPDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3844_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3844_LOVELOCK_EH2_ROUTE.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3844 at ")
    )
    if f"Generated by 3844 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3844 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem_route: list[dict[str, object]],
    clause_audit: list[dict[str, object]],
    eh2_update: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in theorem_route + clause_audit + eh2_update + gates)
    add(
        "VAL3844_0_sources",
        "all cited local source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3844_1_lovelock_route",
        "Lovelock/EH route is recorded",
        "Lovelock" in all_text and "10.1063/1.1665613" in all_text,
        "external theorem anchor and route row present",
    )
    add(
        "VAL3844_2_eh2_collapse_formula",
        "conditional EH2 collapse formula is present",
        all(token in all_text for token in ["B_L2_operator=0", "B_grav_energy_source=0", "B_nonEH2_operator=0", "B_EH2_vertex <= B_field_redef_gauge"]),
        "EH2 collapse tokens present",
    )
    add(
        "VAL3844_3_clause_audit",
        "all required Lovelock clauses are audited",
        all(
            token in all_text
            for token in [
                "single 4D public metric/coframe",
                "diffeomorphism",
                "local second-order",
                "no retained scalar",
                "Hilbert/coframe",
                "boundary/topological",
                "Newtonian C_t",
                "PPN gauge",
            ]
        ),
        "clause tokens present",
    )
    add(
        "VAL3844_4_nonclaim",
        "all 3844 rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem_route + clause_audit + eh2_update + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3844_5_parent_blocked",
        "parent action failure remains explicit",
        any(row["gate_id"] == "GATE3844_1_parent_action" and row["status"].startswith("BLOCKED") for row in gates),
        "explicit parent visible Lagrangian gate blocked",
    )
    add(
        "VAL3844_6_next_constructive",
        "next target is constructive parent action candidate",
        "3845-Y5-R2FR-visible-metric-parent-action-candidate-from-MTS-or-Lovelock-failure" in all_text
        or (DOC_PATH.exists() and "3845-Y5-R2FR-visible-metric-parent-action-candidate-from-MTS-or-Lovelock-failure" in read_text(DOC_PATH)),
        "3845 constructive target visible",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3844_7_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3844_8_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "Lovelock/EH uniqueness lock" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3844*", "P8_Y5_BRR545_3844*", "*Y5_R2FR_3844*", "3844-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3844_9_formalization_clean",
        "formalization-workbench has no 3844 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3844 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3844_10_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    theorem_route = theorem_route_rows(timestamp)
    clause_audit = clause_audit_rows(timestamp)
    eh2_update = eh2_update_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem_route"], theorem_route)
    write_csv(OUTPUTS["clause_audit"], clause_audit)
    write_csv(OUTPUTS["eh2_update"], eh2_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem_route, clause_audit, eh2_update, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem_route, clause_audit, eh2_update, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_EH2_LOVELOCK_ROUTE_SHARPENED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
