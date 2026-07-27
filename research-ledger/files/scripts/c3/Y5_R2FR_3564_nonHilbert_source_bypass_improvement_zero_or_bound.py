from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3564-Y5-R2FR-nonHilbert-source-bypass-improvement-zero-or-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_NONHILBERT_BYPASS_3564"
CHECKPOINT_ID = "3564"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def sources() -> dict[str, Path]:
    return {
        "handoff_3563": RESIDUALS / "P8_Y5_R2FR_3563_NEXT_TARGET.csv",
        "fallback_3563": RESIDUALS / "P8_Y5_R2FR_3563_OFFICIAL_DENSITY_FALLBACK_ROWS.csv",
        "current_owner_1958": RESIDUALS / "P8_Y5_PARENT_QLOC_1958_CURRENT_OWNER_NONHILBERT_ATTEMPT.csv",
        "bound_1958": RESIDUALS / "P8_Y5_PARENT_QLOC_1958_NONHILBERT_CURRENT_BOUND_LEDGER.csv",
        "trident_2332": RESIDUALS / "P8_Y5_PARENT_QLOC_2332_NONHILBERT_TRIDENT_SILENCE_AUDIT.csv",
        "envelopes_2332": RESIDUALS / "P8_Y5_PARENT_QLOC_2332_NONHILBERT_RESIDUAL_ENVELOPES.csv",
        "projection_2346": RESIDUALS / "P8_Y5_PARENT_QLOC_2346_NONHILBERT_SOURCE_PROJECTION_ZERO_AUDIT.csv",
        "bound_pack_2346": RESIDUALS / "P8_Y5_PARENT_QLOC_2346_NONHILBERT_COMPONENT_BOUND_PACK.csv",
        "residual_2373": RESIDUALS / "P8_Y5_PARENT_QLOC_2373_NONHILBERT_RESIDUAL_ROW.csv",
        "trident_update_2373": RESIDUALS / "P8_Y5_PARENT_QLOC_2373_NONHILBERT_TRIDENT_UPDATE.csv",
        "improvement_2380": RESIDUALS / "P8_Y5_PARENT_QLOC_2380_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv",
        "boundary_2350": RESIDUALS / "P8_Y5_PARENT_QLOC_2350_BOUNDARY_IMPROVEMENT_ZERO_AUDIT.csv",
        "silence_3491": RESIDUALS / "P8_Y5_R2FR_3491_NONHILBERT_SILENCE_ATTEMPTS.csv",
        "inventory_2617": RESIDUALS / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_NONHILBERT_BOUNDARY_PROJECTOR_AUDIT.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3563": "declares 3564 target",
        "fallback_3563": "imports nonHilbert_source_bypass official fallback from density branch",
        "current_owner_1958": "current-owner/non-Hilbert theorem attempt",
        "bound_1958": "first non-Hilbert bound ledger",
        "trident_2332": "spin/boundary/readout trident silence audit",
        "envelopes_2332": "absolute residual envelopes for trident heads",
        "projection_2346": "source-projection zero audit for non-Hilbert channels",
        "bound_pack_2346": "dimensionless component bound pack",
        "residual_2373": "Noether source-charge identity residual rows",
        "trident_update_2373": "trident route update selecting spin/torsion next gate",
        "improvement_2380": "exact boundary improvement cancellation derivation",
        "boundary_2350": "boundary/improvement zero audit",
        "silence_3491": "recent non-Hilbert silence attempts",
        "inventory_2617": "single-source map non-Hilbert inventory",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NHB3564_0_decomposition",
            "name": "non-Hilbert bypass decomposition",
            "statement": "After the Hilbert source is extracted, write J_active = J_H + J_NH with J_NH = J_spin/torsion + J_boundary/worldtube + J_readout + J_improvement + J_shadow/projector + J_decoupled.",
            "derivation": "This is the inventory of all active source channels not owned by the same Hilbert variation; it unifies the 1958, 2332, 2346 and 2617 ledgers.",
            "required_premises": "Hilbert baseline fixed; no cancellation between unsigned channels",
            "current_status": "EXACT_DECOMPOSITION_NONCLAIM",
            "effect": "defines what must be zeroed or bounded",
            "source_path": str(source_paths["projection_2346"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NHB3564_1_exact_improvement_cancellation",
            "name": "exact improvement cancellation lemma",
            "statement": "If a non-Hilbert contribution is a genuine exact improvement L' = L + dmu on the same field bundle, with fixed tau, fixed surface embedding, no corner/topological remainder and no readout dependence, then its Hamiltonian surface one-form contribution cancels: delta(i_tau mu)-i_tau(delta mu)=0.",
            "derivation": "theta' = theta + delta mu and Q_tau' = Q_tau + i_tau mu. Therefore k_tau' = delta Q_tau' - i_tau theta' = k_tau when [delta,i_tau]=0.",
            "required_premises": "exact improvement classification; fixed tau/surface; no corner/cohomology/readout terms",
            "current_status": "EXACT_CONDITIONAL_PARTIAL_ZERO",
            "effect": "kills only classified exact-improvement flux, not total J_NH",
            "source_path": str(source_paths["improvement_2380"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NHB3564_2_total_zero_conditions",
            "name": "total non-Hilbert zero theorem conditions",
            "statement": "P_source[J_NH]=0 follows only if spin/torsion is absent/projected-silent, boundary/worldtube/improvement flux has zero compact local projection, readout/domain/frame reentry is forbidden, shadow/projector/support tails are zero, and decoupled conserved blocks are excluded or bounded.",
            "derivation": "Apply the projection to each component and use an absolute no-cancellation envelope. Total zero requires every component zero on the same parent branch.",
            "required_premises": "all component zero theorems signed together",
            "current_status": "EXACT_CONDITIONAL_TOTAL_THEOREM_NOT_LIVE",
            "effect": "sets the full non-Hilbert bypass success gate",
            "source_path": str(source_paths["trident_2332"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NHB3564_3_live_failure",
            "name": "live failure of total bypass proof",
            "statement": "Current MTS does not sign total non-Hilbert silence: spin/torsion/nonmetricity, boundary/worldtube flux, readout reentry, shadow/projector support and nonminimal/decoupled blocks remain open or unsigned.",
            "derivation": "Every inspected source marks the total zero theorem as conditional, not parent-signed, with component envelopes required.",
            "required_premises": "none; this is the current verdict",
            "current_status": "TOTAL_ZERO_NOT_DERIVED",
            "effect": "promote non-Hilbert fallback rows",
            "source_path": str(source_paths["silence_3491"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NHB3564_4_official_fallback",
            "name": "official non-Hilbert source-current fallback",
            "statement": "Because total P_source[J_NH]=0 is not signed, epsilon_current_owner_NH_abs is now the official nonclaim fallback for the density/source-current branch, using absolute component envelopes and no cancellation.",
            "derivation": "2346 and 2373 already provide component rows; 3564 promotes them to the active fallback so future work does not keep restating non-Hilbert silence.",
            "required_premises": "failed total zero proof; component rows exist",
            "current_status": "OFFICIAL_NONCLAIM_FALLBACK_SELECTED",
            "effect": "future local source work uses this vector unless a component theorem closes",
            "source_path": str(source_paths["bound_pack_2346"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NHB3564_5_next_gate",
            "name": "next gate selection",
            "statement": "The best next derivation target is spin/torsion/nonmetricity/hypermomentum silence, because it is the closest GR-like structural route: metric-only Levi-Civita source geometry or Palatini EH plus no hypermomentum.",
            "derivation": "2373 explicitly selects spin/torsion as the primary next gate; boundary/readout remain parallel gates but are less likely to close without the charge/reference stack.",
            "required_premises": "3564 fallback active",
            "current_status": "NEXT_GATE_SELECTED",
            "effect": "sets 3565",
            "source_path": str(source_paths["trident_update_2373"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def component_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("NHC3564_0_spin_torsion", "E_spin", "spin/torsion/nonmetricity/hypermomentum source projection", "LIVE_UNSIGNED", "metric-only Levi-Civita branch or Palatini EH with no hypermomentum/projective source", "spin/torsion gate", "bound_pack_2346"),
        ("NHC3564_1_boundary_worldtube", "E_boundary", "boundary/worldtube/source-current projection", "LIVE_UNSIGNED", "zero compact boundary/source-worldtube projection with fixed reference and support", "boundary gate", "boundary_2350"),
        ("NHC3564_2_improvement_flux", "E_improvement", "canonical/Hilbert improvement or superpotential flux", "PARTIAL_EXACT_ZERO_FOR_CLASSIFIED_DMU_ONLY", "exact dmu improvement with fixed tau/surface and no corner/readout residue", "improvement gate", "improvement_2380"),
        ("NHC3564_3_readout_reentry", "E_readout", "post-variation readout/domain/frame current reentry", "LIVE_UNSIGNED", "readout maps downstream and cannot create source-labelled current terms", "readout gate", "trident_2332"),
        ("NHC3564_4_shadow_projector", "E_shadow_projector", "shadow connection/projector/domain/support tail", "LIVE_UNSIGNED", "single observed coframe/projector theorem or explicit coefficient bound", "shadow/projector gate", "projection_2346"),
        ("NHC3564_5_decoupled_block", "E_decoupled", "separately conserved non-Hilbert source block", "LIVE_INVENTORY", "arena exclusion or finite bound", "decoupled block gate", "inventory_2617"),
        ("NHC3564_6_total", "epsilon_current_owner_NH_abs", "absolute non-Hilbert source-current owner envelope", "OFFICIAL_NONCLAIM_FALLBACK", "all components zero or sourced numeric values", "total envelope", "bound_pack_2346"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "component_id": component_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "zero_condition": zero_condition,
            "gate": gate,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for component_id, symbol, definition, status, zero_condition, gate, source_key in rows
    ]


def fallback_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("FNH3564_0_total", "nonHilbert_total", "epsilon_current_owner_NH_abs", "total projected non-Hilbert source-current envelope", "OFFICIAL_NONCLAIM_TOTAL_ENVELOPE", "dimensionless after source normalization", "local_GR;Newton_GM;PPN;WEP;R10;orbital;clock", "P8_nonHilbert_source_current_total_bound.csv", "bound_pack_2346"),
        ("FNH3564_1_spin", "spin_torsion", "E_spin", "spin/torsion/nonmetricity/hypermomentum source projection", "MISSING_NO_GAMMA_CERTIFICATE_OR_P4_VALUE", "dimensionless", "PPN;clock;spin_transport;local_GR;R10", "P8_spin_torsion_source_projection_bound.csv", "bound_pack_2346"),
        ("FNH3564_2_boundary", "boundary_worldtube", "E_boundary", "boundary/worldtube source projection", "MISSING_B_ZERO_FLUX_OR_SOURCE_BOUND", "dimensionless_or_declared_GM_flux", "Newton_GM;orbital;PPN;local_GR", "P8_boundary_worldtube_source_projection_bound.csv", "bound_pack_2346"),
        ("FNH3564_3_improvement", "improvement_flux", "E_improvement", "unclassified or non-exact improvement/superpotential flux", "PARTIAL_EXACT_DMU_ZERO_ELSE_BOUND_REQUIRED", "source-current_or_dimensionless", "Newton_GM;PPN;local_GR", "P8_improvement_flux_exact_or_bound.csv", "envelopes_2332"),
        ("FNH3564_4_readout", "readout_reentry", "E_readout", "post-variation readout/domain/frame source-current reentry", "MISSING_READOUT_REENTRY_ZERO_OR_LEAKAGE_VALUE", "dimensionless", "WEP;R10;clock;PPN;orbital", "P8_readout_reentry_current_bound.csv", "bound_pack_2346"),
        ("FNH3564_5_shadow_projector", "shadow_projector_support", "E_shadow_projector", "shadow connection/projector/domain/support source tail", "MISSING_SHADOW_PROJECTOR_SUPPORT_VALUE", "dimensionless", "R10;PPN;clock;local_GR;source_normalization", "P8_shadow_projector_support_bound.csv", "bound_pack_2346"),
        ("FNH3564_6_decoupled", "decoupled_conserved_block", "E_decoupled", "separately conserved real block outside Hilbert source", "MISSING_ARENA_EXCLUSION_OR_BOUND", "dimensionless_or_declared", "PPN;WEP;R10;orbital", "P8_decoupled_conserved_block_bound.csv", "inventory_2617"),
        ("FNH3564_7_no_cancellation", "absolute_sum_policy", "sum_abs_components", "total envelope uses absolute sum unless parent signs cancellation", "ACTIVE_GUARD", "policy", "all local source arenas", "P8_nonHilbert_no_cancellation_policy.csv", "bound_pack_2346"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "fallback_id": fallback_id,
            "channel": channel,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "units": units,
            "observable_links": observable_links,
            "required_artifact": required_artifact,
            "source_path": str(source_paths[source_key]),
            "official_nonHilbert_fallback": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for fallback_id, channel, symbol, definition, status, units, observable_links, required_artifact, source_key in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3564_0",
            "decision": "Exact improvement cancellation is a partial theorem.",
            "meaning": "Classified exact dmu improvements cancel from the Hamiltonian surface one-form under fixed tau/surface/no-corner clauses.",
            "claim_effect": "partial reduction only",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3564_1",
            "decision": "Total non-Hilbert bypass is not zeroed.",
            "meaning": "Spin/torsion, boundary/worldtube, readout reentry, shadow/projector and decoupled blocks remain live.",
            "claim_effect": "no density/source-current closure claim",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3564_2",
            "decision": "Official non-Hilbert fallback selected.",
            "meaning": "Future local-GR source-current work uses the absolute non-Hilbert envelope unless a component theorem closes.",
            "claim_effect": "nonHilbert_source_bypass becomes canonical nonclaim vector",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3564_3",
            "decision": "Next target is spin/torsion silence.",
            "meaning": "The closest GR-like route is proving the local source branch is metric-only Levi-Civita or Palatini EH with no hypermomentum.",
            "claim_effect": "sets up 3565",
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STAT3564_0",
            "status": "NONHILBERT_TOTAL_ZERO_NOT_DERIVED_OFFICIAL_FALLBACK_SELECTED",
            "summary": "Exact dmu improvements are conditionally silent, but total non-Hilbert source bypass is not zeroed. The official nonclaim fallback is epsilon_current_owner_NH_abs with absolute component envelopes.",
            "strongest_result": "exact-improvement partial zero plus official non-Hilbert fallback",
            "still_missing": "spin/torsion silence, boundary/worldtube no-flux, readout no-reentry, shadow/projector support silence, decoupled-block exclusion",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3564_0",
            "target_doc": "3565-Y5-R2FR-spin-torsion-hypermomentum-silence-or-P4-bound.md",
            "target_script": "scripts/Y5_R2FR_3565_spin_torsion_hypermomentum_silence_or_P4_bound.py",
            "objective": "try to prove the local source branch is metric-only Levi-Civita, or Palatini EH with no matter/source/readout hypermomentum and projective silence; if not, promote E_spin/P4 torsion-nonmetricity bound rows",
            "success_gate": "spin/torsion/hypermomentum channel theorem-zero, or E_spin becomes source-ready nonclaim P4 bound row",
            "reason": "3564 makes non-Hilbert bypass official fallback and identifies spin/torsion as the closest GR-like structural gate",
            "valid_for_claim": False,
        }
    ]


def validation(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    theorem: list[dict[str, object]],
    components: list[dict[str, object]],
    fallback: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [str(path) for path in source_paths.values() if not path.exists()]
    parse_failures: list[str] = []
    for path in outputs.values():
        if path.suffix.lower() == ".csv":
            try:
                read_csv(path)
            except Exception as exc:
                parse_failures.append(f"{path}: {exc}")
    theorem_ids = {str(row["theorem_id"]) for row in theorem}
    component_ids = {str(row["component_id"]) for row in components}
    fallback_ids = {str(row["fallback_id"]) for row in fallback}
    unsafe_claims = [
        str(row["fallback_id"])
        for row in fallback
        if str(row.get("valid_for_claim", "")).lower() == "true"
        or str(row.get("score_ready", "")).lower() == "true"
        or str(row.get("claim_allowed", "")).lower() == "true"
    ]
    formalization_touched = any(path == FORMALIZATION or FORMALIZATION in path.parents for path in outputs.values())
    rows = [
        ("VAL3564_0_sources_exist", not missing_sources, f"{len(source_paths)-len(missing_sources)}/{len(source_paths)} cited source paths exist" if not missing_sources else "; ".join(missing_sources)),
        ("VAL3564_1_generated_csvs_parse", not parse_failures, f"{sum(1 for path in outputs.values() if path.suffix.lower()=='.csv')} generated CSV files parse" if not parse_failures else "; ".join(parse_failures)),
        ("VAL3564_2_theorem_rows_present", {"NHB3564_1_exact_improvement_cancellation","NHB3564_2_total_zero_conditions","NHB3564_4_official_fallback"}.issubset(theorem_ids), "improvement, total-zero and fallback theorem rows present"),
        ("VAL3564_3_component_rows_present", {"NHC3564_0_spin_torsion","NHC3564_1_boundary_worldtube","NHC3564_3_readout_reentry","NHC3564_4_shadow_projector","NHC3564_6_total"}.issubset(component_ids), "component gate rows present"),
        ("VAL3564_4_fallback_rows_present", {"FNH3564_0_total","FNH3564_1_spin","FNH3564_2_boundary","FNH3564_3_improvement","FNH3564_4_readout","FNH3564_5_shadow_projector","FNH3564_7_no_cancellation"}.issubset(fallback_ids), "official non-Hilbert fallback rows present"),
        ("VAL3564_5_fallback_nonclaim", not unsafe_claims, "all fallback rows remain nonclaim" if not unsafe_claims else "; ".join(unsafe_claims)),
        ("VAL3564_6_official_fallback_marked", all(str(row.get("official_nonHilbert_fallback", "")).lower() == "true" for row in fallback), "every fallback row marked official_nonHilbert_fallback"),
        ("VAL3564_7_formalization_workbench_untouched", not formalization_touched, "3564 generated outputs only inside post-checkpoint-work"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
        }
        for validation_id, passes, detail in rows
    ]


def write_doc(
    output_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    components: list[dict[str, object]],
    fallback: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    lines = [
        "# 3564 - Non-Hilbert source bypass improvement zero or bound",
        "",
        "## Verdict",
        "3564 closes only the clean subpiece: exact `dmu` improvements are conditionally silent in the Hamiltonian surface one-form when `tau`, the surface and corner class are fixed. But total non-Hilbert source bypass is not zeroed.",
        "",
        "So `nonHilbert_source_bypass` is now an official nonclaim fallback vector: spin/torsion, boundary/worldtube, readout reentry, shadow/projector/support and decoupled blocks are absolute-summed until individually zeroed or bounded.",
        "",
        "## Exact improvement lemma",
        "`L' = L + dmu` gives `theta' = theta + delta mu` and `Q_tau' = Q_tau + i_tau mu`; therefore `k_tau' = delta Q_tau' - i_tau theta' = k_tau` when `[delta,i_tau]=0` and no corner/topological/readout residue exists.",
        "",
        "This is useful but narrow. It does not silence spin/torsion, boundary/worldtube charges, readout reentry or projector/support tails.",
        "",
        "## What moved",
        "- Exact improvements are separated from unclassified boundary/current flux.",
        "- Total `J_NH` is decomposed into named component gates.",
        "- The non-Hilbert bypass vector is promoted to official nonclaim fallback.",
        "- Next target is the closest GR-like structural gate: spin/torsion/hypermomentum silence.",
        "",
        "## Generated outputs",
    ]
    for name, path in output_paths.items():
        lines.append(f"- `{name}`: `{path}`")
    lines.extend(["", "## Theorem rows"])
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['statement']}")
    lines.extend(["", "## Component gates"])
    for row in components:
        lines.append(f"- `{row['component_id']}` `{row['symbol']}`: {row['status']} ({row['definition']})")
    lines.extend(["", "## Official fallback rows"])
    for row in fallback:
        lines.append(f"- `{row['fallback_id']}` `{row['symbol']}`: {row['status']}")
    lines.extend(["", "## Decision ledger"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} {row['meaning']}")
    lines.extend(["", "## Next target", f"- `{next_rows[0]['target_doc']}`", f"- Objective: {next_rows[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    source_rows = source_register(source_paths)
    theorem = theorem_rows(source_paths)
    components = component_rows(source_paths)
    fallback = fallback_rows(source_paths)
    decisions = decision_rows()
    statuses = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3564_SOURCE_REGISTER.csv",
        "bypass_theorem": RESIDUALS / "P8_Y5_R2FR_3564_NONHILBERT_BYPASS_THEOREM.csv",
        "component_gates": RESIDUALS / "P8_Y5_R2FR_3564_COMPONENT_GATES.csv",
        "official_fallback": RESIDUALS / "P8_Y5_R2FR_3564_OFFICIAL_NONHILBERT_FALLBACK_ROWS.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3564_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3564_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3564_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_nonHilbert_bypass_official_fallback_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3564_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["bypass_theorem"], theorem)
    write_csv(outputs["component_gates"], components)
    write_csv(outputs["official_fallback"], fallback)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], statuses)
    write_csv(outputs["next_target"], next_rows)
    write_csv(outputs["canonical_status"], [{
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "canonical_status": statuses[0]["status"],
        "strongest_result": statuses[0]["strongest_result"],
        "still_missing": statuses[0]["still_missing"],
        "next_target": next_rows[0]["target_doc"],
        "claim_allowed": False,
        "valid_for_claim": False,
    }])
    validation_rows = validation(source_paths, {key: path for key, path in outputs.items() if key != "validation"}, theorem, components, fallback)
    write_csv(outputs["validation"], validation_rows)
    write_doc(outputs, theorem, components, fallback, decisions, next_rows)
    for path in [DOC, *outputs.values()]:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
