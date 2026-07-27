from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3491-Y5-R2FR-nonHilbert-current-bypass-or-readout-order-silence.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3491": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3490": {
        "path": ROOT / "3490-Y5-R2FR-species-blind-measure-current-owner-or-product-bound-upgrade.md",
        "role": "3490 handoff",
    },
    "measure_1452": {
        "path": ROOT
        / "source-intake"
        / "microscope"
        / "branch_locked_wep"
        / "coefficients"
        / "common_measure_current_theorem_attempt_1452.csv",
        "role": "non-Hilbert bypass gate",
    },
    "owner_1687": {
        "path": ROOT
        / "source-intake"
        / "microscope"
        / "branch_locked_wep"
        / "residuals"
        / "R2FR_common_action_measure_current_owner_proof_attempt_1687.csv",
        "role": "Hilbert current conditional theorem",
    },
    "audit_1594": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1594_COMMON_MEASURE_CURRENT_AUDIT.csv",
        "role": "common measure/current audit with readout and non-Hilbert gates",
    },
    "nonhilbert_1958_attempt": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1958_CURRENT_OWNER_NONHILBERT_ATTEMPT.csv",
        "role": "non-Hilbert source-current channel split",
    },
    "nonhilbert_1958_bounds": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1958_NONHILBERT_CURRENT_BOUND_LEDGER.csv",
        "role": "non-Hilbert bound symbols",
    },
    "vbr_1816": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv",
        "role": "variation-before-readout conditional theorem",
    },
    "readout_2727": {
        "path": OUT / "P8_Y5_R2FR_2727_READOUT_REENTRY_COUNTERMODEL_LEDGER.csv",
        "role": "readout reentry countermodels",
    },
    "finite_3488": {
        "path": OUT / "P8_Y5_R2FR_3488_FINITE_JSPURION_COEFFICIENT_ROWS.csv",
        "role": "source reentry finite coefficient row",
    },
    "updates_3490": {
        "path": OUT / "P8_Y5_R2FR_3490_STATUS_UPDATES.csv",
        "role": "non-Hilbert current product-bound carry-forward",
    },
    "matrix_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "role": "WEP rows with empirical eta bounds",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(meta["path"]),
            "exists": str(Path(meta["path"]).exists()),
            "role": meta["role"],
            "valid_for_claim": "False",
        }
        for source_id, meta in SOURCES.items()
    ]


def hilbert_nonhilbert_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "NH3491_0_hilbert_uniqueness_conditional",
            "statement": "If one common S_matter is varied with respect to the observed metric/coframe before readout, the Hilbert source is unique.",
            "derivation": "T_H := (2/sqrt(-g)) delta S_matter/delta g_obs is fixed on the parent variational domain; downstream readout can report it but cannot redefine it.",
            "source_path": str(SOURCES["owner_1687"]["path"]),
            "result": "EXACT_CONDITIONAL_SUBTHEOREM",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "NH3491_1_nonhilbert_bypass_form",
            "statement": "The conditional Hilbert theorem does not by itself exclude J_src = kappa T_H + sum_i zeta_i J_NH,i.",
            "derivation": "A current not obtained from the same Hilbert variation is invisible to the uniqueness theorem unless the parent object language forbids it or its projection is zero.",
            "source_path": str(SOURCES["measure_1452"]["path"]),
            "result": "BYPASS_SURVIVES_AS_PARALLEL_GATE",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "NH3491_2_improvement_boundary_condition",
            "statement": "Canonical-to-Hilbert improvement currents are silent only when their projected boundary flux vanishes.",
            "derivation": "T_can - T_H = nabla_lambda B^(lambda mu nu); P_loc nabla B becomes a boundary/worldtube term, not zero by algebra alone.",
            "source_path": str(SOURCES["nonhilbert_1958_attempt"]["path"]),
            "result": "ZERO_IF_BOUNDARY_L2_FLUX_ZERO_OR_BOUNDED",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "NH3491_3_spin_torsion_condition",
            "statement": "Spin, torsion, hypermomentum, and nonmetricity channels are silent only in a Levi-Civita metric-only parent geometry or if projected exact.",
            "derivation": "Metric Hilbert variation does not own independent connection/coframe spin-current source channels unless the parent constrains them away.",
            "source_path": str(SOURCES["nonhilbert_1958_attempt"]["path"]),
            "result": "OPEN_CHANNEL_NOT_ZERO",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "NH3491_4_boundary_current_condition",
            "statement": "Boundary/source-worldtube source currents are silent only under a no-flux, neutral-boundary, or projector-orthogonality theorem.",
            "derivation": "A local arena projector can see l=2 boundary/current support even when the bulk Hilbert source is common.",
            "source_path": str(SOURCES["nonhilbert_1958_attempt"]["path"]),
            "result": "OPEN_CHANNEL_NOT_ZERO",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "NH3491_5_verdict",
            "statement": "A full non-Hilbert silence proof is not closed by the current corpus.",
            "derivation": "Hilbert uniqueness is useful but it needs parent-signed torsionless geometry, boundary flux silence, and readout no-reentry to become total-source uniqueness.",
            "source_path": str(SOURCES["audit_1594"]["path"]),
            "result": "FULL_ZERO_PROOF_FAILED_CLEANLY",
            "valid_for_claim": "False",
        },
    ]


def readout_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "RO3491_0_variation_before_readout",
            "statement": "Variation-before-readout kills post-current rescalings only if the readout is typed as downstream postprocessing.",
            "derivation": "For a parent action S[Phi], delta S/delta Phi is computed before R_post[Phi_sol]; then delta does not act on R_post.",
            "source_path": str(SOURCES["vbr_1816"]["path"]),
            "result": "EXACT_IF_PARENT_DOMAIN_TYPED",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "RO3491_1_commutator_formula",
            "statement": "The residual readout-current commutator is C_R := P_loc[(delta R/delta g) J + R(delta J/delta g) - R_H(delta J_H/delta g)].",
            "derivation": "C_R vanishes when R is post-variation, species-blind, source-label-free, and fixed before fitting; otherwise it is a genuine source/readout tail.",
            "source_path": str(SOURCES["vbr_1816"]["path"]),
            "result": "FORMULA_EXACT_STATUS_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "RO3491_2_preaction_limit",
            "statement": "Readout order cannot erase source weights already present inside S_matter.",
            "derivation": "If S_matter contains sum_A w_A S_A before variation, then T_H contains w_A T_A; downstream readout cannot divide it out without becoming a new source map.",
            "source_path": str(SOURCES["vbr_1816"]["path"]),
            "result": "LIMIT_THEOREM_COUNTERMODEL_SURVIVES",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "RO3491_3_marker_renamed_readout",
            "statement": "A material/domain/species marker renamed as readout data can reenter the source map unless a no-marker theorem is parent-signed.",
            "derivation": "The readout countermodel RCM2727_3 keeps a marker slot alive; this is not killed by Hilbert variation alone.",
            "source_path": str(SOURCES["readout_2727"]["path"]),
            "result": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "RO3491_4_source_worldtube_transfer",
            "statement": "Source-worldtube kernels are harmless only as fixed downstream kernels; if they select support or normalization before variation, they are transfer residuals.",
            "derivation": "A kernel K_arena placed before variation changes the effective source; a kernel after variation only reports the already-owned source.",
            "source_path": str(SOURCES["vbr_1816"]["path"]),
            "result": "TYPE_SPLIT_NOT_ZERO_PROOF",
            "valid_for_claim": "False",
        },
    ]


def residual_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RBR3491_0_spin_torsion",
            "symbol": "epsilon_NH_spin_torsion",
            "formula_piece": "P_loc[zeta_spin J_spin/torsion]",
            "source_channel": "spin/torsion/hypermomentum/nonmetricity current",
            "zero_condition": "parent geometry is Levi-Civita metric-only, or P_loc[J_spin/torsion] is exact/projected silent",
            "current_status": "OPEN_PRODUCT_BOUNDABLE",
            "source_path": str(SOURCES["nonhilbert_1958_bounds"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RBR3491_1_boundary_current",
            "symbol": "epsilon_NH_boundary_current",
            "formula_piece": "P_loc[zeta_boundary J_boundary]",
            "source_channel": "boundary/source-worldtube current",
            "zero_condition": "boundary no-flux, neutral worldtube, or projector-orthogonality theorem",
            "current_status": "OPEN_PRODUCT_BOUNDABLE",
            "source_path": str(SOURCES["nonhilbert_1958_bounds"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RBR3491_2_improvement_flux",
            "symbol": "epsilon_improvement_flux",
            "formula_piece": "P_loc[nabla_lambda B^(lambda mu nu)] = P_boundary[B]",
            "source_channel": "canonical-to-Hilbert improvement boundary flux",
            "zero_condition": "projected l=2 improvement flux vanishes on the local boundary/collar",
            "current_status": "OPEN_PRODUCT_BOUNDABLE",
            "source_path": str(SOURCES["nonhilbert_1958_attempt"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RBR3491_3_readout_reentry",
            "symbol": "epsilon_readout_reentry",
            "formula_piece": "P_loc[C_R]",
            "source_channel": "post-variation readout/domain/frame source-label reentry",
            "zero_condition": "readout is fixed downstream, species-blind, source-label-free, and cannot alter the variational source",
            "current_status": "OPEN_PRODUCT_BOUNDABLE",
            "source_path": str(SOURCES["finite_3488"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RBR3491_4_source_worldtube_kernel",
            "symbol": "epsilon_source_worldtube_kernel",
            "formula_piece": "P_loc[(K_arena^pre - K_arena^post) J_H]",
            "source_channel": "source-worldtube or arena-kernel transfer",
            "zero_condition": "K_arena is declared as post-variation reporting only, or its source-transfer norm is bounded",
            "current_status": "OPEN_PRODUCT_BOUNDABLE",
            "source_path": str(SOURCES["vbr_1816"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def product_bound_rows(residuals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matrix = read_csv(SOURCES["matrix_3475"]["path"])
    wep_rows = [row for row in matrix if row["row_type"] == "WEP_material_difference"]
    rows: list[dict[str, Any]] = []
    for residual in residuals:
        for index, wep in enumerate(wep_rows):
            rows.append(
                {
                    "product_bound_id": f"NHB3491_{residual['symbol']}_{index}_{wep['aug_row_id']}",
                    "coefficient_symbol": residual["symbol"],
                    "arena": wep["arena"],
                    "observable_row": wep["aug_row_id"],
                    "product_symbol": f"abs(S_E^q) * abs(Delta_{residual['symbol']}_AB)",
                    "bound_value": wep["bound"],
                    "bound_units": wep["bound_units"],
                    "bound_type": "one_at_a_time_or_no_cancellation_sufficient_envelope",
                    "derivation": "The WEP eta row bounds the observable total residual. This row is a safe nonclaim smoke interface for the named residual product, not an isolated measurement of the coefficient.",
                    "source_path": wep["source_path"],
                    "isolates_coefficient": "False",
                    "missing_for_isolation": "parent-owned lower bound on abs(S_E^q), no-cancellation allocation, or theorem-zero for all other residual channels",
                    "valid_for_claim": "False",
                }
            )
    return rows


def total_envelope_rows(residuals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matrix = read_csv(SOURCES["matrix_3475"]["path"])
    wep_rows = [row for row in matrix if row["row_type"] == "WEP_material_difference"]
    symbols = [row["symbol"] for row in residuals]
    rows: list[dict[str, Any]] = []
    for index, wep in enumerate(wep_rows):
        rows.append(
            {
                "envelope_id": f"NHT3491_{index}_{wep['aug_row_id']}",
                "arena": wep["arena"],
                "observable_row": wep["aug_row_id"],
                "sufficient_condition": " + ".join(f"abs(S_E^q)*abs(Delta_{symbol}_AB)" for symbol in symbols) + f" <= {wep['bound']}",
                "bound_value": wep["bound"],
                "bound_units": wep["bound_units"],
                "meaning": "If the absolute residual-product sum is kept below this eta row, the non-Hilbert/readout tail cannot exceed the measured WEP bound in that arena.",
                "source_path": wep["source_path"],
                "valid_for_claim": "False",
            }
        )
    return rows


def status_update_rows(residuals: list[dict[str, Any]], product_bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for residual in residuals:
        bounds = [row["product_bound_id"] for row in product_bounds if row["coefficient_symbol"] == residual["symbol"]]
        rows.append(
            {
                "coefficient_id": residual["residual_id"],
                "symbol": residual["symbol"],
                "old_status": residual["current_status"],
                "new_status": "PRODUCT_BOUNDED_NOT_ISOLATED" if bounds else "STILL_MISSING",
                "bound_source": ";".join(bounds),
                "meaning": "component has a finite WEP product-bound interface, but no isolated numeric coefficient and no source-coupling claim",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            "coefficient_id": "RBR3491_TOTAL_nonHilbert_readout_tail",
            "symbol": "epsilon_nonHilbert_readout_total",
            "old_status": "BYPASS_SURVIVES_AS_PARALLEL_GATE",
            "new_status": "DECOMPOSED_PRODUCT_BOUNDED_NOT_ISOLATED",
            "bound_source": ";".join(sorted({row["observable_row"] for row in product_bounds})),
            "meaning": "total tail is now decomposed into named product-boundable channels; local-GR claim remains blocked until theorem-zero or isolated source amplitudes exist",
            "valid_for_claim": "False",
        }
    )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM3491_0_total_source_uniqueness_contract",
            "statement": "Total local source uniqueness requires Hilbert variation plus silence of non-Hilbert, boundary/improvement, and readout-reentry channels.",
            "proof": "Hilbert variation fixes T_H only for the common action. Any independent projected current J_NH, projected boundary divergence, or post-variation readout commutator lies outside that proof unless separately forbidden or zero.",
            "result": "CONTRACT_EXACT_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3491_1_commutator_zero_condition",
            "statement": "The readout-current commutator vanishes if the readout is post-variation, source-label-free, species-blind, fixed before fitting, and has no arrow back into S_parent.",
            "proof": "Under those typing clauses delta acts only on S_parent; R_post is an observational map on the solved state, so it cannot alter the variational source.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3491_2_boundary_improvement_condition",
            "statement": "Improvement currents reduce to boundary/projector flux and require a local zero-flux or bound theorem.",
            "proof": "The divergence theorem turns P_loc nabla_lambda B^(lambda mu nu) into a projected boundary/collar term; it is zero only under flux/projector silence conditions.",
            "result": "CONDITIONAL_NOT_CLOSED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3491_3_product_bound_interface",
            "statement": "Unclosed non-Hilbert/readout channels can be made finite-product-boundable against WEP eta rows.",
            "proof": "Each residual source contrast enters composition tests multiplied by the common Earth source leg; eta rows bound the observable product/envelope but not the isolated coefficient.",
            "result": "FINITE_NONCLAIM_PROGRESS",
            "valid_for_claim": "False",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3491_0_hilbert_source_conditional",
            "requirement": "common Hilbert source subtheorem exists",
            "passed": "True",
            "evidence": "COM1687_1 and VBR1816 give conditional Hilbert/readout theorem",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3491_1_nonhilbert_silence",
            "requirement": "spin/torsion/non-Hilbert channels are absent, exact, or projected silent",
            "passed": "False",
            "evidence": "OWN1958_3 and CMT1452_5 keep the parallel gate open",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3491_2_boundary_improvement_silence",
            "requirement": "boundary and improvement flux l=2 projections are theorem-zero or source-bounded",
            "passed": "False",
            "evidence": "OWN1958_2/4 require boundary flux zero or envelope",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3491_3_readout_no_reentry",
            "requirement": "readout cannot retroactively redefine the source or reintroduce markers",
            "passed": "False",
            "evidence": "VBR1816 conditional only; RCM2727_3 marker-renamed-readout survives",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3491_4_residual_products_created",
            "requirement": "unclosed channels have finite product-bound/nonclaim rows",
            "passed": "True",
            "evidence": "WEP eta rows applied to all named non-Hilbert/readout residual channels",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3491_0_no_total_source_claim",
            "decision": "Do not claim total source uniqueness or local-GR closure.",
            "rationale": "Hilbert uniqueness is conditional; non-Hilbert, boundary/improvement, and readout reentry gates are not parent-signed.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3491_1_real_progress",
            "decision": "Keep the route alive by replacing vague non-Hilbert/readout debt with a finite residual vector and product-bound envelopes.",
            "rationale": "This is stronger than just saying missing: every open channel now has a formula, zero condition, and WEP-bound interface.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3491_2_best_next_attack",
            "decision": "Attack the parent local geometry/torsionless metric-only clause before another source sweep.",
            "rationale": "If Levi-Civita metric-only geometry is parent-signed, the spin/torsion non-Hilbert branch collapses and leaves boundary/readout as the next finite tails.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3492-Y5-R2FR-parent-local-geometry-metric-only-or-spin-torsion-source-tail.md",
            "next_script": "scripts/Y5_R2FR_3492_parent_local_geometry_metric_only_or_spin_torsion_source_tail.py",
            "objective": "Try to derive that the local parent geometry seen by ordinary matter is Levi-Civita metric-only; if not, keep spin/torsion/hypermomentum as a finite source-tail bound target.",
            "success_gate": "torsion/nonmetricity source channel theorem-zero, or source-backed spin/torsion product-envelope rows with explicit PPN/WEP projection",
            "forbidden_shortcuts": "assuming GR geometry before deriving the parent local geometry; deleting hypermomentum by naming it non-Hilbert; claiming isolated epsilon from product bounds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    outputs: dict[str, Path],
    product_bounds: list[dict[str, Any]],
    total_envelopes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "check_id": "VAL3491_0_sources_exist",
            "passed": all(Path(meta["path"]).exists() for meta in SOURCES.values()),
            "detail": "all cited local sources exist",
            "valid_for_claim": "False",
        }
    )
    parse_ok = True
    details: list[str] = []
    for name, path in outputs.items():
        try:
            parsed = read_csv(path)
            details.append(f"{name}:{len(parsed)}")
        except Exception as exc:
            parse_ok = False
            details.append(f"{name}:ERROR:{exc}")
    rows.append(
        {
            "check_id": "VAL3491_1_csv_parse",
            "passed": parse_ok,
            "detail": "; ".join(details),
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3491_2_product_bounds_created",
            "passed": len(product_bounds) >= 10,
            "detail": f"product_bounds={len(product_bounds)}",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3491_3_total_envelopes_created",
            "passed": len(total_envelopes) >= 2,
            "detail": f"total_envelopes={len(total_envelopes)}",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3491_4_parent_claim_blocked",
            "passed": any(row["passed"] == "False" and row["blocks_claim"] == "True" for row in gates),
            "detail": "non-Hilbert/boundary/readout gates remain claim-blocking",
            "valid_for_claim": "False",
        }
    )
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append(
        {
            "check_id": "VAL3491_5_no_claim",
            "passed": all(row.get("valid_for_claim") == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3491_6_no_formalization_outputs",
            "passed": all(FORMALIZATION not in path.parents for path in outputs.values()),
            "detail": "outputs are under post-checkpoint-work/source-intake only",
            "valid_for_claim": "False",
        }
    )
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append(
        {
            "check_id": "VAL3491_SUMMARY",
            "passed": passed,
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, sep] + body)


def write_doc(
    nonhilbert_attempts: list[dict[str, Any]],
    readout_attempts: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    product_bounds: list[dict[str, Any]],
    total_envelopes: list[dict[str, Any]],
    updates: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3491: Non-Hilbert Current Bypass Or Readout-Order Silence",
                "",
                "## Current Verdict",
                "- **Derivation result:** Hilbert-current uniqueness is a real conditional theorem, but it is not total source uniqueness.",
                "- **Failed zero proof:** non-Hilbert spin/torsion, boundary/improvement flux, and readout reentry are not parent-signed silent.",
                "- **Concrete progress:** the vague bypass has been decomposed into named residual channels with zero conditions and WEP product-bound interfaces.",
                "- **No claim:** no local-GR, WEP, or source-coupling pass is claimed.",
                "",
                "## Non-Hilbert Current Attempt",
                md_table(nonhilbert_attempts, ["attempt_id", "statement", "derivation", "result", "valid_for_claim"]),
                "",
                "## Readout-Order Attempt",
                md_table(readout_attempts, ["attempt_id", "statement", "derivation", "result", "valid_for_claim"]),
                "",
                "## R Bridge Residual Map",
                md_table(residuals, ["residual_id", "symbol", "formula_piece", "source_channel", "zero_condition", "current_status", "valid_for_claim"]),
                "",
                "## Product Bounds",
                md_table(product_bounds, ["product_bound_id", "coefficient_symbol", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "isolates_coefficient", "valid_for_claim"]),
                "",
                "## Total Sufficient Envelopes",
                md_table(total_envelopes, ["envelope_id", "arena", "sufficient_condition", "bound_value", "bound_units", "meaning", "valid_for_claim"]),
                "",
                "## Status Updates",
                md_table(updates, ["coefficient_id", "symbol", "old_status", "new_status", "bound_source", "meaning", "valid_for_claim"]),
                "",
                "## Theorems",
                md_table(theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"]),
                "",
                "## Gates",
                md_table(gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"]),
                "",
                "## Decisions",
                md_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"_Generated: {now()}_",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    nonhilbert_attempts = hilbert_nonhilbert_attempt_rows()
    readout_attempts = readout_attempt_rows()
    residuals = residual_map_rows()
    product_bounds = product_bound_rows(residuals)
    total_envelopes = total_envelope_rows(residuals)
    updates = status_update_rows(residuals, product_bounds)
    theorems = theorem_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3491_SOURCE_REGISTER.csv",
        "nonhilbert_attempts": OUT / "P8_Y5_R2FR_3491_NONHILBERT_SILENCE_ATTEMPTS.csv",
        "readout_attempts": OUT / "P8_Y5_R2FR_3491_READOUT_ORDER_ATTEMPTS.csv",
        "residual_map": OUT / "P8_Y5_R2FR_3491_RBRIDGE_RESIDUAL_MAP.csv",
        "product_bounds": OUT / "P8_Y5_R2FR_3491_PRODUCT_BOUND_ROWS.csv",
        "total_envelopes": OUT / "P8_Y5_R2FR_3491_TOTAL_ENVELOPES.csv",
        "updates": OUT / "P8_Y5_R2FR_3491_STATUS_UPDATES.csv",
        "theorems": OUT / "P8_Y5_R2FR_3491_THEOREM_LEDGER.csv",
        "gates": OUT / "P8_Y5_R2FR_3491_GATES.csv",
        "decisions": OUT / "P8_Y5_R2FR_3491_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3491_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["nonhilbert_attempts"], nonhilbert_attempts, ["attempt_id", "statement", "derivation", "source_path", "result", "valid_for_claim"])
    write_csv(outputs["readout_attempts"], readout_attempts, ["attempt_id", "statement", "derivation", "source_path", "result", "valid_for_claim"])
    write_csv(outputs["residual_map"], residuals, ["residual_id", "symbol", "formula_piece", "source_channel", "zero_condition", "current_status", "source_path", "valid_for_claim"])
    write_csv(outputs["product_bounds"], product_bounds, ["product_bound_id", "coefficient_symbol", "arena", "observable_row", "product_symbol", "bound_value", "bound_units", "bound_type", "derivation", "source_path", "isolates_coefficient", "missing_for_isolation", "valid_for_claim"])
    write_csv(outputs["total_envelopes"], total_envelopes, ["envelope_id", "arena", "observable_row", "sufficient_condition", "bound_value", "bound_units", "meaning", "source_path", "valid_for_claim"])
    write_csv(outputs["updates"], updates, ["coefficient_id", "symbol", "old_status", "new_status", "bound_source", "meaning", "valid_for_claim"])
    write_csv(outputs["theorems"], theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"])
    write_csv(outputs["gates"], gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"])
    write_csv(outputs["decisions"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, product_bounds, total_envelopes, gates)
    validation_path = OUT / "P8_Y5_BRR545_3491_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(nonhilbert_attempts, readout_attempts, residuals, product_bounds, total_envelopes, updates, theorems, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
