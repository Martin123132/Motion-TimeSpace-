from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4100-Y5-R2FR-nonHilbert-source-bypass-improvement-zero-or-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "EXACT_DMU_IMPROVEMENT_ZERO_ACCEPTED_AS_PARTIAL_THEOREM_TOTAL_NONHILBERT_BYPASS_RETAINS_OFFICIAL_ABSOLUTE_SUM_FALLBACK"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4100_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4099_NEXT_TARGET.csv",
        "4100-Y5-R2FR-nonHilbert-source-bypass-improvement-zero-or-bound.md",
        "4099 selects non-Hilbert source bypass as next live density/source-current gate.",
    ),
    "SRC4100_01_weight_residual": (
        SOURCE_DIR / "P8_Y5_R2FR_4099_SOURCE_WEIGHT_RESIDUALS.csv",
        "SWR4099_7_nonHilbert_bypass",
        "4099 source-weight residuals leave non-Hilbert bypass as outside-Hom next gate.",
    ),
    "SRC4100_02_density_impact": (
        SOURCE_DIR / "P8_Y5_R2FR_4099_DENSITY_IMPACT.csv",
        "NEXT_GATE_NONHILBERT_BYPASS",
        "4099 density impact sends work to non-Hilbert bypass.",
    ),
    "SRC4100_03_bound_vector": (
        SOURCE_DIR / "P8_Y5_R2FR_4099_BOUND_VECTOR.csv",
        "BH4099_7_nonHilbert_bypass",
        "4099 bound vector includes non-Hilbert source bypass row.",
    ),
    "SRC4100_04_bypass_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3564_NONHILBERT_BYPASS_THEOREM.csv",
        "NHB3564_1_exact_improvement_cancellation",
        "3564 exact-improvement cancellation lemma.",
    ),
    "SRC4100_05_bypass_decomposition": (
        SOURCE_DIR / "P8_Y5_R2FR_3564_NONHILBERT_BYPASS_THEOREM.csv",
        "NHB3564_0_decomposition",
        "3564 decomposes active source into Hilbert plus non-Hilbert channels.",
    ),
    "SRC4100_06_component_gates": (
        SOURCE_DIR / "P8_Y5_R2FR_3564_COMPONENT_GATES.csv",
        "NHC3564_0_spin_torsion",
        "3564 component gates show spin/torsion is the leading live bypass channel.",
    ),
    "SRC4100_07_official_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_3564_OFFICIAL_NONHILBERT_FALLBACK_ROWS.csv",
        "FNH3564_0_total",
        "3564 official absolute non-Hilbert fallback rows.",
    ),
    "SRC4100_08_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_3564_DECISION_LEDGER.csv",
        "DEC3564_2",
        "3564 decision selecting official non-Hilbert fallback.",
    ),
    "SRC4100_09_spin_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3565_SPIN_TORSION_THEOREM_STACK.csv",
        "STH3565_0_connection_fork",
        "3565 spin/torsion next gate: no independent connection or P4 residual.",
    ),
    "SRC4100_10_spin_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3565_P4_SPIN_HYPERMOMENTUM_BOUND_ROWS.csv",
        "P4H3565_0_total",
        "3565 official P4 spin/hypermomentum fallback rows.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
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


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4100_11_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4100 non-Hilbert source bypass gate.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def nonhilbert_bypass_theorem_rows() -> List[dict]:
    return [
        {
            "theorem_id": "NHB4100_0_decomposition",
            "claim_piece": "Hilbert/non-Hilbert source split",
            "statement": "After the Hilbert source is extracted, every remaining active source-current contribution is a non-Hilbert bypass channel.",
            "formula": "J_active = J_H + J_NH; J_NH=J_spin/torsion+J_boundary/worldtube+J_readout+J_improvement+J_shadow/projector+J_decoupled",
            "if_signed": "source-current leakage has a finite channel basis",
            "current_status": "DECOMPOSITION_ADOPTED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "NHB4100_1_exact_dmu_improvement_zero",
            "claim_piece": "exact improvement cancellation",
            "statement": "A classified exact improvement cancels from the Hamiltonian surface one-form only under fixed bundle, tau, surface, no-corner and no-readout-dependence clauses.",
            "formula": "L' = L + dmu; delta(i_tau mu)-i_tau(delta mu)=0",
            "if_signed": "classified exact dmu improvements do not feed source mass",
            "current_status": "PARTIAL_EXACT_THEOREM_ACCEPTED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "NHB4100_2_total_zero_conditions",
            "claim_piece": "total non-Hilbert silence",
            "statement": "Total non-Hilbert bypass silence requires every component gate to vanish or be bounded; exact improvements alone are not enough.",
            "formula": "P_source[J_NH]=0 iff E_spin=E_boundary=E_improvement=E_readout=E_shadow_projector=E_decoupled=0",
            "if_signed": "non-Hilbert bypass no longer blocks density/source-current closure",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "NHB4100_3_live_failure",
            "claim_piece": "live bypass failure",
            "statement": "Spin/torsion, boundary/worldtube flux, readout reentry, shadow/projector support and decoupled blocks remain open or unsigned.",
            "formula": "epsilon_current_owner_NH_abs=sum_abs(E_i) until component theorems/numeric bounds exist",
            "if_signed": "not_applicable",
            "current_status": "OFFICIAL_FALLBACK_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "NHB4100_4_next_gate",
            "claim_piece": "best next structural route",
            "statement": "The closest GR-like structural route is spin/torsion/hypermomentum silence: either no independent connection in the local source/readout action, or P4 residuals are retained.",
            "formula": "Arg(S_local) excludes Gamma_ind/omega_ind OR retain E_spin/P4",
            "if_signed": "connection recovery branch becomes sharply decidable",
            "current_status": "NEXT_TARGET",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def component_gate_rows() -> List[dict]:
    return [
        {
            "component_id": "CG4100_0_spin_torsion",
            "symbol": "E_spin",
            "definition": "spin/torsion/nonmetricity/hypermomentum source projection",
            "status": "LIVE_UNSIGNED",
            "zero_condition": "metric-only Levi-Civita branch or Palatini EH with no hypermomentum/projective source",
            "fallback": "P4 spin/torsion/hypermomentum residual",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "CG4100_1_boundary_worldtube",
            "symbol": "E_boundary",
            "definition": "boundary/worldtube/source-current projection",
            "status": "LIVE_UNSIGNED",
            "zero_condition": "zero compact boundary/source-worldtube projection with fixed reference and support",
            "fallback": "boundary/source flux bound",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "CG4100_2_improvement_flux",
            "symbol": "E_improvement",
            "definition": "canonical/Hilbert improvement or superpotential flux",
            "status": "PARTIAL_EXACT_ZERO_FOR_CLASSIFIED_DMU_ONLY",
            "zero_condition": "exact dmu improvement with fixed tau/surface and no corner/readout residue",
            "fallback": "unclassified improvement/superpotential flux bound",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "CG4100_3_readout_reentry",
            "symbol": "E_readout",
            "definition": "post-variation readout/domain/frame current reentry",
            "status": "LIVE_UNSIGNED",
            "zero_condition": "readout maps downstream and cannot create source-labelled current terms",
            "fallback": "readout leakage value",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "CG4100_4_shadow_projector",
            "symbol": "E_shadow_projector",
            "definition": "shadow connection/projector/domain/support source tail",
            "status": "LIVE_UNSIGNED",
            "zero_condition": "single observed coframe/projector theorem or explicit coefficient bound",
            "fallback": "shadow/projector support bound",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "CG4100_5_decoupled_block",
            "symbol": "E_decoupled",
            "definition": "separately conserved non-Hilbert source block",
            "status": "LIVE_INVENTORY",
            "zero_condition": "arena exclusion or finite bound",
            "fallback": "decoupled conserved block bound",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "CG4100_6_total",
            "symbol": "epsilon_current_owner_NH_abs",
            "definition": "absolute non-Hilbert source-current owner envelope",
            "status": "OFFICIAL_NONCLAIM_FALLBACK",
            "zero_condition": "all components zero or sourced numeric values",
            "fallback": "absolute-sum non-Hilbert envelope",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def official_fallback_rows() -> List[dict]:
    return [
        {
            "fallback_id": "FNH4100_0_total",
            "channel": "nonHilbert_total",
            "symbol": "epsilon_current_owner_NH_abs",
            "definition": "total projected non-Hilbert source-current envelope",
            "status": "OFFICIAL_NONCLAIM_TOTAL_ENVELOPE",
            "units": "dimensionless_after_source_normalization",
            "observable_links": "local_GR;Newton_GM;PPN;WEP;R10;orbital;clock",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "fallback_id": "FNH4100_1_spin",
            "channel": "spin_torsion",
            "symbol": "E_spin",
            "definition": "spin/torsion/nonmetricity/hypermomentum source projection",
            "status": "MISSING_NO_GAMMA_CERTIFICATE_OR_P4_VALUE",
            "units": "dimensionless",
            "observable_links": "PPN;clock;spin_transport;local_GR;R10",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "fallback_id": "FNH4100_2_boundary",
            "channel": "boundary_worldtube",
            "symbol": "E_boundary",
            "definition": "boundary/worldtube source projection",
            "status": "MISSING_B_ZERO_FLUX_OR_SOURCE_BOUND",
            "units": "dimensionless_or_declared_GM_flux",
            "observable_links": "Newton_GM;orbital;PPN;local_GR",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "fallback_id": "FNH4100_3_improvement",
            "channel": "improvement_flux",
            "symbol": "E_improvement",
            "definition": "unclassified or non-exact improvement/superpotential flux",
            "status": "PARTIAL_EXACT_DMU_ZERO_ELSE_BOUND_REQUIRED",
            "units": "source_current_or_dimensionless",
            "observable_links": "Newton_GM;PPN;local_GR",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "fallback_id": "FNH4100_4_readout",
            "channel": "readout_reentry",
            "symbol": "E_readout",
            "definition": "post-variation readout/domain/frame source-current reentry",
            "status": "MISSING_READOUT_REENTRY_ZERO_OR_LEAKAGE_VALUE",
            "units": "dimensionless",
            "observable_links": "WEP;R10;clock;PPN;orbital",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "fallback_id": "FNH4100_5_shadow_projector",
            "channel": "shadow_projector_support",
            "symbol": "E_shadow_projector",
            "definition": "shadow connection/projector/domain/support source tail",
            "status": "MISSING_SHADOW_PROJECTOR_SUPPORT_VALUE",
            "units": "dimensionless",
            "observable_links": "R10;PPN;clock;local_GR;source_normalization",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "fallback_id": "FNH4100_6_decoupled",
            "channel": "decoupled_conserved_block",
            "symbol": "E_decoupled",
            "definition": "separately conserved real block outside Hilbert source",
            "status": "MISSING_ARENA_EXCLUSION_OR_BOUND",
            "units": "dimensionless_or_declared",
            "observable_links": "PPN;WEP;R10;orbital",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "fallback_id": "FNH4100_7_no_cancellation",
            "channel": "absolute_sum_policy",
            "symbol": "sum_abs_components",
            "definition": "total envelope uses absolute sum unless parent signs cancellation",
            "status": "ACTIVE_GUARD",
            "units": "policy",
            "observable_links": "all_local_source_arenas",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def density_impact_rows() -> List[dict]:
    return [
        {
            "impact_id": "NHI4100_0_partial_gain",
            "condition": "classified exact dmu improvement with fixed tau/surface/no-corner/no-readout dependence",
            "impact": "that component can be treated as theorem-zero in the Hamiltonian surface one-form",
            "source_coupling_effect": "reduces E_improvement only",
            "status": "PARTIAL_THEOREM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "impact_id": "NHI4100_1_current_state",
            "condition": "spin/torsion, boundary, readout, shadow/projector and decoupled blocks remain unsigned",
            "impact": "total non-Hilbert bypass remains active",
            "source_coupling_effect": "E_rho_qbasic and Hamiltonian/Gauss source-mass identity remain nonclaim",
            "status": "OFFICIAL_FALLBACK_ACTIVE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "impact_id": "NHI4100_2_no_cancellation",
            "condition": "multiple non-Hilbert channels are unsigned",
            "impact": "use absolute envelope rather than signed cancellation",
            "source_coupling_effect": "epsilon_current_owner_NH_abs=sum_abs(E_i)",
            "status": "NO_CANCELLATION_GUARD",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "impact_id": "NHI4100_3_next_gate",
            "condition": "non-Hilbert bypass fallback is official",
            "impact": "spin/torsion/hypermomentum is the closest GR-like structural gate",
            "source_coupling_effect": "move to no-Gamma-or-P4 fork",
            "status": "NEXT_GATE_SPIN_TORSION",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_gate_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4100_0_partial",
            "decision": "accept exact dmu improvement cancellation as a partial theorem",
            "meaning": "Classified exact improvements can be silent, but only under fixed tau/surface/no-corner/no-readout clauses.",
            "result": "E_improvement has a theorem-zero subcase",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4100_1_total",
            "decision": "do not claim total non-Hilbert bypass silence",
            "meaning": "Spin/torsion, boundary/worldtube, readout reentry, shadow/projector and decoupled blocks remain live.",
            "result": "epsilon_current_owner_NH_abs remains official fallback",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4100_2_policy",
            "decision": "use absolute-sum fallback unless parent signs a cancellation identity",
            "meaning": "No cancellation between unsigned bypass channels is allowed as evidence.",
            "result": "no-cancellation guard active",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4100_3_next",
            "decision": "attack spin/torsion/hypermomentum silence next",
            "meaning": "The closest route back to GR is no independent connection in source/readout action, or a sourced P4 residual branch.",
            "result": "4101 spin/torsion target selected",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4100_0_exact_improvement",
            "claim": "classified exact dmu improvements can be silent under fixed-surface clauses",
            "allowed": "True",
            "reason": "the Hamiltonian surface one-form contribution cancels for genuine exact improvements with no corner/readout residue",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4100_1_total_nonHilbert_zero",
            "claim": "all non-Hilbert source bypass is zero",
            "allowed": "False",
            "reason": "spin/torsion, boundary/worldtube, readout reentry, shadow/projector and decoupled channels remain unsigned",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4100_2_density_qbasic",
            "claim": "Hilbert density q-basicness is proved",
            "allowed": "False",
            "reason": "non-Hilbert bypass remains official fallback, and source-weight/support/EM gates remain active",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4100_3_Newton",
            "claim": "source-normalized Newtonian mechanics is publicly derived",
            "allowed": "False",
            "reason": "source-current non-Hilbert bypass still blocks public Hamiltonian/Gauss source-mass identity",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4100_4_local_GR",
            "claim": "local GR/PPN is derived",
            "allowed": "False",
            "reason": "connection, PPN, R11, EM and source-current closure gates remain downstream",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4100_0",
            "next_target": "4101-Y5-R2FR-spin-torsion-hypermomentum-silence-or-P4-bound.md",
            "script": "scripts/Y5_R2FR_4101_spin_torsion_hypermomentum_silence_or_P4_bound.py",
            "why": "4100 leaves E_spin as the leading live non-Hilbert bypass channel. The GR-like fork is exact: no independent Gamma/omega in local source/readout action, or retain official P4 coefficients.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4100_1",
            "next_target": "4102-Y5-R2FR-common-coupling-owner-or-Gdot-bound.md",
            "script": "defer_until_spin_torsion_gate",
            "why": "Common calibration remains allowed only if derivative-free and parent-owned; otherwise it becomes Gdot/source drift.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4100",
            "decision": DECISION,
            "exact_dmu_partial_zero": "True",
            "total_nonHilbert_zero_public": "False",
            "nonHilbert_fallback": "official_absolute_sum",
            "density_qbasic_public": "False",
            "Newton_source_public": "False",
            "next_required_gate": "spin_torsion_hypermomentum_silence_or_P4_bound",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def write_doc() -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 4100 - Non-Hilbert Source Bypass Improvement Zero Or Bound",
                "",
                "## Purpose",
                "",
                "4099 made source-weight rows an official fallback and exposed the next density/source-current gate: non-Hilbert source bypass. 4100 separates the narrow exact-improvement zero from the live bypass channels.",
                "",
                f"- Decision: `{DECISION}`",
                "- Public density/source-current claim: `false`",
                "- Public Newton/local-GR claim: `false`",
                "",
                "## Partial Theorem",
                "",
                "A genuine exact improvement can be silent only in the classified case:",
                "",
                "```text",
                "L' = L + dmu",
                "fixed tau, fixed surface, no corner/topological remainder, no readout dependence",
                "delta(i_tau mu) - i_tau(delta mu) = 0",
                "```",
                "",
                "This is useful, but narrow. It only handles `E_improvement` subcases.",
                "",
                "## Live Non-Hilbert Channels",
                "",
                "```text",
                "J_active = J_H + J_NH",
                "J_NH = J_spin/torsion + J_boundary/worldtube + J_readout",
                "     + J_improvement + J_shadow/projector + J_decoupled",
                "```",
                "",
                "Total silence requires every component to vanish or be bounded. Until then:",
                "",
                "```text",
                "epsilon_current_owner_NH_abs = sum_abs(E_i)",
                "```",
                "",
                "with no cancellation between unsigned channels.",
                "",
                "## Next Target",
                "",
                "`4101-Y5-R2FR-spin-torsion-hypermomentum-silence-or-P4-bound.md` should take the clean GR-like fork: either no independent `Gamma_ind/omega_ind` appears in the local source/readout action, or the theory carries official P4 spin/torsion/hypermomentum residual coefficients.",
                "",
                "## Outputs",
                "",
                "- `P8_Y5_R2FR_4100_SOURCE_REGISTER.csv`",
                "- `P8_Y5_R2FR_4100_NONHILBERT_BYPASS_THEOREM.csv`",
                "- `P8_Y5_R2FR_4100_COMPONENT_GATES.csv`",
                "- `P8_Y5_R2FR_4100_OFFICIAL_FALLBACK_ROWS.csv`",
                "- `P8_Y5_R2FR_4100_DENSITY_IMPACT.csv`",
                "- `P8_Y5_R2FR_4100_DECISION_GATE.csv`",
                "- `P8_Y5_R2FR_4100_CLAIM_GATE.csv`",
                "- `P8_Y5_R2FR_4100_NEXT_TARGET.csv`",
                "- `P8_Y5_R2FR_4100_STATUS.csv`",
                "- `P8_Y5_BRR545_4100_VALIDATION.csv`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4100_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4100_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4100_NONHILBERT_BYPASS_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4100_NONHILBERT_BYPASS_THEOREM.csv",
        "P8_Y5_R2FR_4100_COMPONENT_GATES": SOURCE_DIR / "P8_Y5_R2FR_4100_COMPONENT_GATES.csv",
        "P8_Y5_R2FR_4100_OFFICIAL_FALLBACK_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4100_OFFICIAL_FALLBACK_ROWS.csv",
        "P8_Y5_R2FR_4100_DENSITY_IMPACT": SOURCE_DIR / "P8_Y5_R2FR_4100_DENSITY_IMPACT.csv",
        "P8_Y5_R2FR_4100_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4100_DECISION_GATE.csv",
        "P8_Y5_R2FR_4100_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4100_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4100_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4100_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4100_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4100_STATUS.csv",
    }


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4100_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4100_NONHILBERT_BYPASS_THEOREM"], nonhilbert_bypass_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4100_COMPONENT_GATES"], component_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4100_OFFICIAL_FALLBACK_ROWS"], official_fallback_rows())
    write_csv(outputs["P8_Y5_R2FR_4100_DENSITY_IMPACT"], density_impact_rows())
    write_csv(outputs["P8_Y5_R2FR_4100_DECISION_GATE"], decision_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4100_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4100_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4100_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        rows.append(
            {
                "check_id": f"VAL4100_SRC_{source_id}",
                "check": "local source exists and contains needle",
                "passed": bool_string(contains),
                "detail": f"{path} | needle={needle} | role={role}",
                "timestamp_utc": TIMESTAMP,
            }
        )

    for name, path in outputs.items():
        try:
            parsed = parse_csv(path)
            ok = len(parsed) > 0
            detail = f"{path} rows={len(parsed)}"
        except Exception as exc:
            ok = False
            detail = f"{path} parse_error={exc}"
        rows.append(
            {
                "check_id": f"VAL4100_CSV_{name}",
                "check": "generated CSV parses and is non-empty",
                "passed": bool_string(ok),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    theorem = parse_csv(outputs["P8_Y5_R2FR_4100_NONHILBERT_BYPASS_THEOREM"])
    theorem_text = "\n".join(str(row) for row in theorem)
    theorem_ok = all(
        needle in theorem_text
        for needle in ["J_active", "L' = L + dmu", "P_source[J_NH]=0", "epsilon_current_owner_NH_abs", "NEXT_TARGET"]
    )
    rows.append(
        {
            "check_id": "VAL4100_THEOREM",
            "check": "non-Hilbert theorem records decomposition, exact-improvement subcase, total zero conditions, fallback and next target",
            "passed": bool_string(theorem_ok),
            "detail": "requires active split, dmu, total condition, envelope and next target",
            "timestamp_utc": TIMESTAMP,
        }
    )

    components = parse_csv(outputs["P8_Y5_R2FR_4100_COMPONENT_GATES"])
    component_text = "\n".join(str(row) for row in components)
    component_ok = all(
        needle in component_text
        for needle in ["E_spin", "E_boundary", "E_improvement", "E_readout", "E_shadow_projector", "E_decoupled", "epsilon_current_owner_NH_abs"]
    )
    rows.append(
        {
            "check_id": "VAL4100_COMPONENT_GATES",
            "check": "component gates cover spin, boundary, improvement, readout, shadow/projector, decoupled and total channels",
            "passed": bool_string(component_ok),
            "detail": f"component_rows={len(components)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    fallback = parse_csv(outputs["P8_Y5_R2FR_4100_OFFICIAL_FALLBACK_ROWS"])
    fallback_text = "\n".join(str(row) for row in fallback)
    fallback_ok = all(
        needle in fallback_text
        for needle in ["OFFICIAL_NONCLAIM_TOTAL_ENVELOPE", "MISSING_NO_GAMMA_CERTIFICATE_OR_P4_VALUE", "PARTIAL_EXACT_DMU_ZERO_ELSE_BOUND_REQUIRED", "ACTIVE_GUARD"]
    )
    rows.append(
        {
            "check_id": "VAL4100_FALLBACK",
            "check": "official fallback rows preserve total envelope, spin/P4, partial improvement and no-cancellation guard",
            "passed": bool_string(fallback_ok),
            "detail": f"fallback_rows={len(fallback)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    impact = parse_csv(outputs["P8_Y5_R2FR_4100_DENSITY_IMPACT"])
    impact_text = "\n".join(str(row) for row in impact)
    impact_ok = all(needle in impact_text for needle in ["PARTIAL_THEOREM", "OFFICIAL_FALLBACK_ACTIVE", "NO_CANCELLATION_GUARD", "NEXT_GATE_SPIN_TORSION"])
    rows.append(
        {
            "check_id": "VAL4100_DENSITY_IMPACT",
            "check": "density impact separates partial gain, active fallback, no-cancellation and spin/torsion next gate",
            "passed": bool_string(impact_ok),
            "detail": f"impact_rows={len(impact)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    claims = parse_csv(outputs["P8_Y5_R2FR_4100_CLAIM_GATE"])
    no_public = all(row.get("public_claim") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    rows.append(
        {
            "check_id": "VAL4100_NO_PUBLIC_CLAIM",
            "check": "4100 does not promote total non-Hilbert zero, density q-basicness, Newton or local-GR claims",
            "passed": bool_string(no_public),
            "detail": "all claim rows remain private/nonclaim",
            "timestamp_utc": TIMESTAMP,
        }
    )

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4100_NEXT_TARGET"])
    next_text = "\n".join(str(row) for row in next_rows)
    next_ok = "4101-Y5-R2FR-spin-torsion-hypermomentum-silence-or-P4-bound.md" in next_text
    rows.append(
        {
            "check_id": "VAL4100_NEXT_TARGET",
            "check": "next target moves to spin/torsion/hypermomentum no-Gamma-or-P4 fork",
            "passed": bool_string(next_ok),
            "detail": "requires 4101 spin/torsion target",
            "timestamp_utc": TIMESTAMP,
        }
    )

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    rows.append(
        {
            "check_id": "VAL4100_SCOPE",
            "check": "outputs stay in post-checkpoint-work and not formalization-workbench",
            "passed": bool_string(in_scope and not formalization_touched),
            "detail": f"doc={DOC_PATH}; csv_count={len(outputs)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = f"py_compile failed: {exc}"
    rows.append(
        {
            "check_id": "VAL4100_SCRIPT_COMPILES",
            "check": "generator script compiles",
            "passed": bool_string(compile_ok),
            "detail": compile_detail,
            "timestamp_utc": TIMESTAMP,
        }
    )

    return rows


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4100_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(f"4100 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()
