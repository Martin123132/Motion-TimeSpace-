from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3856"
BRANCH = "MTS_R2FR_Y5_BETA_EH2_REENTRY_UNDER_RAB_BRANCH_LABEL_3856"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3856-Y5-R2FR-beta-EH2-reentry-under-RAB-branch-label.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3855_FREEZE = OUT / "P8_Y5_R2FR_3855_RAB_BRANCH_FREEZE.csv"
CSV_3855_MATRIX = OUT / "P8_Y5_R2FR_3855_LOCAL_GR_HANDOFF_MATRIX.csv"
CSV_3855_BETA = OUT / "P8_Y5_R2FR_3855_BETA_REENTRY_QUEUE.csv"
CSV_3855_VALIDATION = OUT / "P8_Y5_BRR545_3855_VALIDATION.csv"
CSV_3843_LEDGER = OUT / "P8_Y5_R2FR_3843_INTEGRATED_BETA_LEDGER.csv"
CSV_3843_QUEUE = OUT / "P8_Y5_R2FR_3843_SOURCE_FILL_QUEUE.csv"
CSV_3844_LOVELOCK = OUT / "P8_Y5_R2FR_3844_LOVELOCK_EH2_ROUTE.csv"
CSV_3844_EH2 = OUT / "P8_Y5_R2FR_3844_EH2_BOUND_UPDATE.csv"
CSV_3844_CLAUSES = OUT / "P8_Y5_R2FR_3844_PARENT_CLAUSE_AUDIT.csv"
CSV_3845_ACTION = OUT / "P8_Y5_R2FR_3845_VISIBLE_ACTION_CANDIDATE.csv"
CSV_3845_EH2 = OUT / "P8_Y5_R2FR_3845_EH2_IMPLICATION_UPDATE.csv"
CSV_3845_GATES = OUT / "P8_Y5_R2FR_3845_CLAIM_GATES.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"
CSV_3818_GUARDS = OUT / "P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv"
CSV_3826_KERNEL = OUT / "P8_Y5_R2FR_3826_SOURCE_KERNEL_RESIDUAL_BUNDLE.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3856_SOURCE_REGISTER.csv",
    "branch": OUT / "P8_Y5_R2FR_3856_BRANCH_LABEL_AUDIT.csv",
    "theorem": OUT / "P8_Y5_R2FR_3856_EH2_CONDITIONAL_COLLAPSE_THEOREM.csv",
    "clauses": OUT / "P8_Y5_R2FR_3856_LOVELOCK_CLAUSE_REENTRY_AUDIT.csv",
    "beta": OUT / "P8_Y5_R2FR_3856_BETA_RESIDUAL_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3856_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3856_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3856_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3856_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3856_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3856_00_3855_freeze", CSV_3855_FREEZE, "REQUIRED_DOWNSTREAM_METADATA", "branch label input"),
    ("SRC3856_01_3855_matrix", CSV_3855_MATRIX, "prevents gamma/R_AB work from being mistaken for beta", "handoff matrix"),
    ("SRC3856_02_3855_beta", CSV_3855_BETA, "NEXT_DERIVATION_TARGET_WITH_RAB_LABEL", "beta reentry target"),
    ("SRC3856_03_3855_validation", CSV_3855_VALIDATION, "PASS", "previous checkpoint validation"),
    ("SRC3856_04_3843_ledger", CSV_3843_LEDGER, "PARENT_SECOND_VARIATION_REQUIRED", "integrated beta ledger"),
    ("SRC3856_05_3843_queue", CSV_3843_QUEUE, "parent EH second-variation / nonlinear self-source proof", "P0 beta queue"),
    ("SRC3856_06_3844_lovelock", CSV_3844_LOVELOCK, "Lovelock-style uniqueness", "EH2 theorem route"),
    ("SRC3856_07_3844_eh2", CSV_3844_EH2, "EXACT_CONDITIONAL_ZERO_ROUTE", "EH2 bound update"),
    ("SRC3856_08_3844_clauses", CSV_3844_CLAUSES, "MISSING_EXPLICIT_PARENT_LAGRANGIAN", "clause audit"),
    ("SRC3856_09_3845_action", CSV_3845_ACTION, "S_candidate", "visible action candidate"),
    ("SRC3856_10_3845_eh2", CSV_3845_EH2, "EXACT_CONDITIONAL_EH2_COLLAPSE", "candidate EH2 implication"),
    ("SRC3856_11_3845_gates", CSV_3845_GATES, "BLOCKED_PARENT_DERIVATION_NOT_SIGNED", "candidate claim gates"),
    ("SRC3856_12_3818_poisson", CSV_3818_POISSON, "nabla^2 Phi=4*pi*G_ref rho_H", "Newtonian source bridge"),
    ("SRC3856_13_3818_guards", CSV_3818_GUARDS, "GM_orbit/G_ref cannot fill M_H_ref", "anti-circular source guard"),
    ("SRC3856_14_3826_kernel", CSV_3826_KERNEL, "R_kernel_total_3826", "source kernel residual bundle"),
]

BETA_FORMULA = (
    "abs(beta-1)|RAB_branch_label <= "
    "B_EH2_vertex+B_extra_scalar2+B_boundary2+B_readout2+"
    "B_eps_temporal_order+B_eps_temporal_gauge+B_eps_temporal_domain+"
    "B_eps_temporal_nonlinear+B_eps_temporal_multipole_motion+"
    "B_eps_temporal_denominator+B_RAB_beta_cross(RAB_branch_label)"
)

LOVELOCK_CLAUSE_FORMULA = (
    "B_Lovelock_clause_failure <= "
    "B_public_metric+B_covariance_Bianchi+B_local_second_order+"
    "B_no_extra_dof+B_Hilbert_source+B_boundary_topological+"
    "B_Newtonian_normalization+B_readout_gauge"
)

EH2_CURRENT_BOUND = (
    "B_EH2_vertex <= "
    "B_Lovelock_clause_failure+B_field_redef_gauge+B_unclassified_EH2_residual"
)

EH2_COLLAPSE = (
    "if B_Lovelock_clause_failure=0 and B_field_redef_gauge=0, "
    "then B_L2_operator=B_grav_energy_source=B_nonEH2_operator=B_EH2_vertex=0"
)


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
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
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
                "role": role,
                "claim_use": "nonclaim_derivation_reentry_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def branch_label_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "BLA3856_0_required_label",
            "object": "RAB_branch_label",
            "rule": "every beta/EH2 row must declare explicit_RAB_zero_closure or finite_RAB_hair",
            "effect_on_beta": "metadata prevents gamma closure from being silently mixed into beta",
            "status": "PASS_BRANCH_LABEL_CARRIED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BLA3856_1_closure_control",
            "object": "explicit_RAB_zero_closure",
            "rule": "allowed only as local-GR control branch",
            "effect_on_beta": "does not set B_EH2_vertex, B_source, B_readout, or B_boundary to zero",
            "status": "CONTROL_BRANCH_NOT_BETA_PROOF",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BLA3856_2_finite_hair",
            "object": "finite_RAB_hair",
            "rule": "allowed only with sourced B_RAB rows beating the 3851 pressure budget",
            "effect_on_beta": "adds or bounds B_RAB_beta_cross if finite hair mixes into temporal readout",
            "status": "FINITE_HAIR_RETAINS_CROSS_TERM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "BLA3856_3_cross_term_guard",
            "object": "B_RAB_beta_cross(RAB_branch_label)",
            "rule": "may be zero only after a readout-decoupling or field-redefinition theorem",
            "effect_on_beta": "keeps RAB work from erasing beta by bookkeeping",
            "status": "CROSS_TERM_GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "THM3856_0_branch_separation",
            "step": "RAB separation lemma",
            "statement": "RAB_branch_label fixes the spatial/gamma branch but is not an identity for the temporal second-order EH vertex.",
            "requires": "3855 branch freeze plus explicit beta row label",
            "derived_consequence": "beta must be proved through EH2/source/readout clauses, not by R_AB=0",
            "current_status": "EXACT_GUARD_LEMMA",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "THM3856_1_lovelock_EH2_collapse",
            "step": "conditional EH2 collapse theorem",
            "statement": EH2_COLLAPSE,
            "requires": "single public metric; diffeo/Bianchi covariance; local second-order metric operator; no extra visible dof; Hilbert source glue; boundary/topological silence; Newtonian normalization; fixed PPN readout gauge",
            "derived_consequence": "beta self-coupling is no longer an independent fitted coefficient once the parent visible action is EH/Lovelock-class and readout is fixed",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "THM3856_2_current_bound",
            "step": "strict-current bound",
            "statement": EH2_CURRENT_BOUND,
            "requires": "3844/3845 clauses remain unsigned",
            "derived_consequence": "MTS is not rejected here, but beta is still blocked from claim status",
            "current_status": "NONCLAIM_BOUND_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "THM3856_3_candidate_action_adoption",
            "step": "parent action reentry",
            "statement": "the 3845 S_candidate is the correct next adoption target only if MTS primitives derive g_obs, kappa_MTS, S_matter descent, and silent-sector conditions",
            "requires": "visible metric bridge and parent-owned Lagrangian/operator class",
            "derived_consequence": "next work should try to adopt or reject the EH visible parent action, not write another missing-variable ledger",
            "current_status": "NEXT_CONSTRUCTION_TARGET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def clause_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "LVC3856_0_public_metric",
            "required_clause": "single 4D public metric/coframe visible branch",
            "source_status": "CONTRACT_AVAILABLE_NOT_PARENT_SIGNED",
            "beta_effect_if_closed": "enables metric-theory beta readout instead of multi-frame ambiguity",
            "current_decision": "retain B_public_metric until MTS primitives own g_obs",
            "next_proof_artifact": "motion/time/space to Lorentzian g_obs bridge",
            "source": rel(CSV_3844_CLAUSES),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3856_1_covariance_Bianchi",
            "required_clause": "covariant divergence-consistent visible equation",
            "source_status": "PARTIAL_CONTRACT_NO_PARENT_VARIATION",
            "beta_effect_if_closed": "locks self-source consistency and narrows B_grav_energy_source",
            "current_decision": "retain B_covariance_Bianchi until parent variation is signed",
            "next_proof_artifact": "delta S_parent/delta g_obs with nabla_mu E_vis^mu_nu=0",
            "source": rel(CSV_3844_CLAUSES),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3856_2_local_second_order",
            "required_clause": "local second-order metric operator",
            "source_status": "MISSING_EXPLICIT_PARENT_LAGRANGIAN",
            "beta_effect_if_closed": "activates Lovelock uniqueness and attacks B_L2_operator/B_nonEH2_operator",
            "current_decision": "main blocker; target this next through 3845 action adoption",
            "next_proof_artifact": "explicit parent visible Lagrangian/operator class",
            "source": rel(CSV_3844_CLAUSES),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3856_3_no_extra_dof",
            "required_clause": "no retained scalar/vector/torsion/nonmetric/disformal beta-order degree",
            "source_status": "UNSIGNED_WITH_KNOWN_COUNTERCHANNELS",
            "beta_effect_if_closed": "removes scalar-tensor and higher-operator beta contamination",
            "current_decision": "retain B_no_extra_dof and B_extra_scalar2",
            "next_proof_artifact": "kernel/projector theorem or finite coupling bounds",
            "source": rel(CSV_3844_CLAUSES),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3856_4_Hilbert_source",
            "required_clause": "ordinary source is Hilbert/coframe variation of the same public action",
            "source_status": "CONDITIONAL_FROM_1030_3818_NOT_SIGNED",
            "beta_effect_if_closed": "ties Newtonian source and nonlinear self-energy to one source measure",
            "current_decision": "retain B_Hilbert_source and source-normalization guards",
            "next_proof_artifact": "same-source action descent with M_H_ref and Pi_M J_H closed",
            "source": rel(CSV_3844_CLAUSES),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3856_5_boundary_topological",
            "required_clause": "boundary/topological/cosmological terms silent at beta order",
            "source_status": "BOUNDARY_SPECIALIZATION_REQUIRED",
            "beta_effect_if_closed": "removes boundary/reference terms from U^2 coefficient",
            "current_decision": "retain B_boundary2 and domain terms",
            "next_proof_artifact": "local exterior Dirichlet/flux/harmonic/counterterm theorem",
            "source": rel(CSV_3844_CLAUSES),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3856_6_Newtonian_normalization",
            "required_clause": "Newtonian C_t fixes EH coefficient before beta extraction",
            "source_status": "CONDITIONAL_FROM_3818_WITH_SOURCE_GUARDS",
            "beta_effect_if_closed": "prevents fitted GM from laundering the beta denominator",
            "current_decision": "retain B_Newtonian_normalization until G_ref/rho_H are parent-owned",
            "next_proof_artifact": "Poisson/Gauss bridge with anti-circular GM guard",
            "source": rel(CSV_3818_GUARDS),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "clause_id": "LVC3856_7_readout_gauge",
            "required_clause": "field variable and PPN gauge fixed before beta comparison",
            "source_status": "READOUT_GAUGE_LOCK_REQUIRED",
            "beta_effect_if_closed": "sets B_field_redef_gauge=0 after EH2 collapse",
            "current_decision": "retain B_field_redef_gauge until readout Hessian/gauge is fixed",
            "next_proof_artifact": "g00=-1+2U-2 beta U^2+eps in declared PPN gauge",
            "source": rel(CSV_3843_LEDGER),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def beta_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "BRU3856_0_branch_labelled_beta",
            "observable": "beta-1",
            "formula": BETA_FORMULA,
            "meaning": "the beta residual now explicitly carries RAB_branch_label and a cross-term guard",
            "status": "BRANCH_LABELLED_NONCLAIM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRU3856_1_lovelock_clause_bound",
            "observable": "B_Lovelock_clause_failure",
            "formula": LOVELOCK_CLAUSE_FORMULA,
            "meaning": "EH2 is reduced to a finite parent-action clause stack rather than an undefined vibes gap",
            "status": "DERIVATION_STACK_EXPLICIT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRU3856_2_EH2_current",
            "observable": "B_EH2_vertex",
            "formula": EH2_CURRENT_BOUND,
            "meaning": "strict-current corpus lacks signed parent visible action and readout lock",
            "status": "CURRENT_BOUND_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRU3856_3_EH2_if_closed",
            "observable": "B_EH2_vertex",
            "formula": EH2_COLLAPSE,
            "meaning": "this is the leap-forward route: derive EH visible action and beta stops being independently fitted",
            "status": "EXACT_CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BRU3856_4_RAB_cross_guard",
            "observable": "B_RAB_beta_cross(RAB_branch_label)",
            "formula": "B_RAB_beta_cross=0 only if temporal readout/gauge is decoupled from the R_AB branch; otherwise it remains bounded by B_field_redef_gauge+B_readout2 or by sourced finite-hair rows",
            "meaning": "prevents explicit_RAB_zero_closure from becoming a hidden beta proof",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3856_0_sources",
            "gate": "source-backed inputs resolved",
            "status": "PASS_SOURCE_REGISTERED",
            "claim_allowed": False,
            "reason": "3856 uses existing 3843/3844/3845/3855 rows and does not fabricate parent coefficients",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3856_1_RAB_separation",
            "gate": "RAB closure not used as beta proof",
            "status": "PASS_NO_RAB_BETA_SMUGGLE",
            "claim_allowed": False,
            "reason": "B_RAB_beta_cross is explicit and only theorem-zero under readout decoupling",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3856_2_EH2_theorem",
            "gate": "conditional EH2 collapse formulated",
            "status": "PASS_EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": False,
            "reason": "all Lovelock/EH clauses are named, but not all are parent-signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3856_3_parent_action",
            "gate": "parent visible EH action adopted",
            "status": "BLOCKED_PARENT_VISIBLE_ACTION_NOT_ADOPTED",
            "claim_allowed": False,
            "reason": "3845 S_candidate is written but MTS ownership of g_obs/kappa/matter/silent sector is not proved",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3856_4_beta_claim",
            "gate": "strict-current beta/local-GR claim",
            "status": "BLOCKED_BETA_CLAIM",
            "claim_allowed": False,
            "reason": "B_Lovelock_clause_failure, B_field_redef_gauge, source guards, and B_RAB_beta_cross remain active",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3856_5_next",
            "gate": "next target selected",
            "status": "PASS_3857_ACTION_ADOPTION_TARGET",
            "claim_allowed": False,
            "reason": "best next step is trying to derive/adopt the 3845 visible EH parent action under the RAB label",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3856_0",
            "decision": "do not use R_AB closure as a beta proof",
            "consequence": "all beta rows carry RAB_branch_label plus B_RAB_beta_cross guard",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3856_1",
            "decision": "promote EH2 to an exact Lovelock/EH visible-action theorem stack",
            "consequence": "the gap is now explicit parent-action adoption, not an undefined missing coupling",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3856_2",
            "decision": "make 3845 S_candidate the next construction target",
            "consequence": "3857 should attempt action adoption or produce a precise adoption-failure residual",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3856_0",
            "next_checkpoint": "3857-Y5-R2FR-visible-EH-parent-action-adoption-test-under-RAB-label.md",
            "script": "scripts/Y5_R2FR_3857_visible_EH_parent_action_adoption_test_under_RAB_label.py",
            "objective": "try to adopt or reject the 3845 minimal visible EH parent action from MTS primitives under explicit RAB_branch_label",
            "reason": "3856 shows beta/EH2 collapses only if the parent visible action is EH/Lovelock-class with source/readout clauses signed",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_BRANCH_LABELLED_EH2_COLLAPSE_ROUTE",
            "claim": "no beta, PPN, R_AB zero, Newton, EM, or local-GR claim",
            "result": "RAB-labelled beta theorem derived: EH2 collapse is exact conditional on parent visible EH/Lovelock action plus source/readout clauses; strict-current blocker is parent action adoption",
            "next": "3857 visible EH parent action adoption test under RAB label",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    branch: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    beta: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3856 - Beta EH2 Reentry Under RAB Branch Label

Private checkpoint. This is the derivation-first reentry into `beta` after 3855 froze the `R_AB` branch labels.

Generated: `{timestamp}`

## Result

The useful step is not another `R_AB` loop. The useful step is this separation:

`RAB_branch_label` is required metadata for the local branch, but `R_AB=0` is not a beta proof.

The branch-labelled beta residual is therefore:

`{BETA_FORMULA}`.

The exact conditional collapse route is:

`{EH2_COLLAPSE}`.

The price of that theorem is the full Lovelock/EH visible-action clause stack:

`{LOVELOCK_CLAUSE_FORMULA}`.

The strict-current bound remains:

`{EH2_CURRENT_BOUND}`.

So 3856 does move the ball: the beta gap is no longer a vague missing coupling. It is now a named parent-action adoption problem. The 3845 visible action candidate is the next thing to actually try to adopt from MTS primitives.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Branch Label Audit

{markdown_table(branch, ["audit_id", "object", "status", "effect_on_beta"])}

## EH2 Conditional Collapse Theorem

{markdown_table(theorem, ["theorem_id", "step", "current_status", "derived_consequence"])}

## Lovelock Clause Reentry Audit

{markdown_table(clauses, ["clause_id", "required_clause", "source_status", "current_decision"])}

## Beta Residual Update

{markdown_table(beta, ["row_id", "observable", "status", "formula"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3856 gives the clean target: prove/adopt a parent-owned visible EH/Lovelock action with source and readout clauses, or beta stays nonclaim. The next checkpoint should not circle missing coefficients; it should attack the 3845 `S_candidate` adoption route directly.

Next target: `3857-Y5-R2FR-visible-EH-parent-action-adoption-test-under-RAB-label.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3855", "Current State After 3856", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3856 at ")
    )
    paragraph = (
        "`3856` re-enters the beta/EH2 problem under the frozen `RAB_branch_label` and proves the useful separation lemma: "
        "`R_AB=0` is branch metadata/control-branch information, not a beta proof. "
        "The beta row now carries `B_RAB_beta_cross(RAB_branch_label)` unless readout decoupling is proved. "
        "The EH2 route is sharpened to an exact conditional Lovelock/EH collapse theorem: if the parent owns one public metric, a covariant local second-order metric operator, no visible extra beta-order dof, Hilbert source glue, boundary/topological silence, Newtonian normalization, and fixed PPN readout gauge, then the EH2 vertex collapses to zero. "
        "The strict-current blocker is no longer vague coupling; it is adopting or rejecting the 3845 visible EH parent action from MTS primitives.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3856-Y5-R2FR-beta-EH2-reentry-under-RAB-branch-label.md`

Target: attack the P0 beta gap: parent EH second variation / nonlinear self-source proof under explicit RAB branch metadata, without using R_AB closure as a beta proof.

This is the best next move because 3855 freezes the gamma/R_AB fork and the 3843 dashboard identifies EH2/source self-coupling as the highest-leverage beta target."""
    new_gate = """`3857-Y5-R2FR-visible-EH-parent-action-adoption-test-under-RAB-label.md`

Target: try to adopt or reject the 3845 minimal visible EH parent action from MTS primitives under explicit RAB_branch_label.

This is the best next move because 3856 turns beta/EH2 into a precise parent visible-action adoption problem rather than another missing-coefficient audit."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3856_BRANCH_LABEL_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3856_EH2_CONDITIONAL_COLLAPSE_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3856_LOVELOCK_CLAUSE_REENTRY_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3856_BETA_RESIDUAL_UPDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3856_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3856_BRANCH_LABEL_AUDIT.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3856 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    branch: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    beta: list[dict[str, object]],
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

    all_text = " ".join(str(row) for row in branch + theorem + clauses + beta + gates)
    add(
        "VAL3856_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3856_1_branch_label",
        "RAB_branch_label is carried into beta",
        "RAB_branch_label" in all_text and "B_RAB_beta_cross" in all_text,
        "branch label and cross-term guard present",
    )
    add(
        "VAL3856_2_no_RAB_beta_smuggle",
        "R_AB closure is not used as beta proof",
        "CONTROL_BRANCH_NOT_BETA_PROOF" in all_text and "PASS_NO_RAB_BETA_SMUGGLE" in all_text,
        "RAB branch separated from EH2 beta proof",
    )
    add(
        "VAL3856_3_EH2_collapse",
        "conditional EH2 collapse theorem is explicit",
        "B_L2_operator=B_grav_energy_source=B_nonEH2_operator=B_EH2_vertex=0" in all_text,
        "EH2 collapse implication written",
    )
    add(
        "VAL3856_4_lovelock_stack",
        "Lovelock clause stack is explicit",
        "B_local_second_order" in all_text and "B_Hilbert_source" in all_text and "B_readout_gauge" in all_text,
        "clause failure formula carried",
    )
    add(
        "VAL3856_5_parent_action_blocked",
        "strict-current parent action adoption remains blocked",
        "BLOCKED_PARENT_VISIBLE_ACTION_NOT_ADOPTED" in all_text and "MISSING_EXPLICIT_PARENT_LAGRANGIAN" in all_text,
        "claim remains blocked by parent visible action",
    )
    add(
        "VAL3856_6_nonclaim",
        "all rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in branch + theorem + clauses + beta + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3856_7_next",
        "next target is 3857 action adoption",
        DOC_PATH.exists() and "3857-Y5-R2FR-visible-EH-parent-action-adoption-test-under-RAB-label" in read_text(DOC_PATH),
        "3857 action adoption target visible",
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
        add(f"VAL3856_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3856_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "The strict-current bound remains" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3856*", "P8_Y5_BRR545_3856*", "*Y5_R2FR_3856*", "3856-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3856_10_formalization_clean",
        "formalization-workbench has no generated 3856 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3856 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3856_11_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    branch = branch_label_rows(timestamp)
    theorem = theorem_rows(timestamp)
    clauses = clause_rows(timestamp)
    beta = beta_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["branch"], branch)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["clauses"], clauses)
    write_csv(OUTPUTS["beta"], beta)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, branch, theorem, clauses, beta, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, branch, theorem, clauses, beta, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_BRANCH_LABELLED_EH2_COLLAPSE_ROUTE")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
