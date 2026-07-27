from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3495-Y5-R2FR-source-readout-boundary-gamma-current-zero-or-P4-tail-priority.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3495": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3494": {
        "path": ROOT / "3494-Y5-R2FR-ordinary-matter-coframe-owned-spin-proof-or-axial-torsion-tail.md",
        "role": "3494 handoff",
    },
    "next_3494": {
        "path": OUT / "P8_Y5_R2FR_3494_NEXT_TARGET.csv",
        "role": "3494 next target",
    },
    "p4_lock_3493": {
        "path": OUT / "P8_Y5_R2FR_3493_OFFICIAL_P4_LOCAL_GEOMETRY_INTERFACE.csv",
        "role": "official P4 local-geometry fallback",
    },
    "axial_3494": {
        "path": OUT / "P8_Y5_R2FR_3494_AXIAL_TORSION_KERNEL_INTERFACE.csv",
        "role": "sharpened axial torsion kernel",
    },
    "srz_2118": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_ZERO_THEOREM_ATTEMPT.csv",
        "role": "source/readout Gamma-current zero attempt",
    },
    "sro_2122": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_LEMMA.csv",
        "role": "source/readout owner lemma",
    },
    "exceptions_2117": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2117_SECTOR_EXCEPTION_LEDGER.csv",
        "role": "sector exception ledger",
    },
    "commutator_1898": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
        "role": "readout variation commutator attempt",
    },
    "targets_1900": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
        "role": "official readout data target status",
    },
    "sector_3493": {
        "path": OUT / "P8_Y5_R2FR_3493_SECTOR_GAMMA_SIGNATURE_MATRIX.csv",
        "role": "3493 sector Gamma signature matrix",
    },
    "wep_3492": {
        "path": OUT / "P8_Y5_R2FR_3492_WEP_PRODUCT_BOUNDS.csv",
        "role": "3492 WEP product bounds",
    },
    "ppn_3492": {
        "path": OUT / "P8_Y5_R2FR_3492_PPN_PRODUCT_BOUNDS.csv",
        "role": "3492 PPN product bounds",
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


def zero_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "ZSRB3495_0_master_descent",
            "target": "total source/readout/boundary Gamma-current",
            "statement": "If every source, readout, support, projector and boundary map descends through q/e_obs and is fixed before variation, then Delta_Gamma[source+readout+boundary]=0.",
            "proof": "For R_i(Phi)=Rbar_i(q(Phi),e_obs,A_owned,theta) and Pi_i=Pi_i(q,e_obs), any vertical v in ker(Dq) gives delta_v R_i=0 and delta_v(Pi_i J_i)=0; no independent Gamma-current is produced.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "source_path": str(SOURCES["sro_2122"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZSRB3495_1_support_projector_commutator",
            "target": "projector/support commutator",
            "statement": "If support/projector maps depend on fields, source labels or boundary/domain motion before variation, delta(Pi J)=Pi delta J + (delta Pi)J can source a residual.",
            "proof": "The pure postprocessing lemma does not apply to pre-variation projectors, source-worldtube supports, material tensors, domain selectors or calibration feedback.",
            "current_status": "COUNTERMODEL_ACTIVE",
            "source_path": str(SOURCES["commutator_1898"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZSRB3495_2_source_worldtube",
            "target": "source/worldtube current",
            "statement": "Source-worldtube Gamma-current vanishes only if source stress/profile, composition convention, support tube and GM normalization are owned coframe data.",
            "proof": "Without those objects, source support can re-enter as an effective connection/source current even when matter spin is clean.",
            "current_status": "CONDITIONAL_ZERO_NOT_SIGNED",
            "source_path": str(SOURCES["srz_2118"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZSRB3495_3_clock_light_orbit",
            "target": "clock/light/orbit readout currents",
            "statement": "Clock, lightcone and orbital Gamma-currents vanish only if readout operators are downstream metric/gauge functors, not independent Gamma probes or imported GR geodesics.",
            "proof": "Clock/rod proper-time, photon null-cone and orbit/GM readout must be derived from g_obs plus owned gauge/source maps; otherwise Weyl, shear and projective tails remain live.",
            "current_status": "RESPONSE_OPERATORS_UNSIGNED",
            "source_path": str(SOURCES["srz_2118"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZSRB3495_4_boundary_domain",
            "target": "boundary/domain/projector current",
            "statement": "Boundary/domain/projector currents vanish only if domain, support, central worldline, boundary transport and projector stress are fixed by the same parent readout map.",
            "proof": "Boundary and domain motion are the primary leak that survives private spin and owned-coframe branch switches.",
            "current_status": "PROJECTOR_DESCENT_UNSIGNED",
            "source_path": str(SOURCES["sro_2122"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def gamma_current_decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "GC3495_0_source_worldtube",
            "component": "Delta_source",
            "formula": "Delta_source ~ delta_Gamma S_source[support, profile, composition, GM]",
            "zero_condition": "source stress/profile/support/GM are q/e_obs-owned downstream data",
            "mapped_tail": "epsilon_hypermomentum_source",
            "status": "OPEN_HIGHEST_PRIORITY",
            "source_path": str(SOURCES["srz_2118"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "GC3495_1_boundary_projector",
            "component": "Delta_boundary + K_comm",
            "formula": "delta(Pi_boundary J)=Pi_boundary delta J + (delta Pi_boundary)J",
            "zero_condition": "domain/support/projector/boundary transport fixed by q/e_obs before variation",
            "mapped_tail": "epsilon_hypermomentum_source;epsilon_projective_trace",
            "status": "OPEN_PRIMARY_LEAK",
            "source_path": str(SOURCES["commutator_1898"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "GC3495_2_projective_trace",
            "component": "Delta_projective",
            "formula": "Gamma -> Gamma + delta^lambda_mu A_nu trace-mode readout/source coupling",
            "zero_condition": "all sectors projectively invariant or trace fixed before matter/readout coupling",
            "mapped_tail": "epsilon_projective_trace",
            "status": "OPEN_GLOBAL_CERTIFICATE",
            "source_path": str(SOURCES["srz_2118"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "GC3495_3_clock_rod",
            "component": "Delta_clock + Q_trace",
            "formula": "clock/rod response to Weyl trace nonmetricity",
            "zero_condition": "clocks and rods read only proper time/length from g_obs and fixed theta",
            "mapped_tail": "epsilon_weyl_nonmetricity",
            "status": "OPEN_RESPONSE_OPERATOR",
            "source_path": str(SOURCES["srz_2118"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "GC3495_4_lightcone",
            "component": "Delta_light + Q_shear",
            "formula": "lightcone/ray/Shapiro response to trace-free nonmetricity",
            "zero_condition": "photon/light propagation is null cone of g_obs plus owned EM gauge data",
            "mapped_tail": "epsilon_shear_nonmetricity",
            "status": "OPEN_RESPONSE_OPERATOR",
            "source_path": str(SOURCES["srz_2118"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "GC3495_5_orbital_GM",
            "component": "Delta_orbit + Delta_GM",
            "formula": "orbit/GM/autoparallel/geodesic transfer convention",
            "zero_condition": "orbit/GM readout is downstream of source measure, Poisson/Gauss calibration and g_obs geodesic limit",
            "mapped_tail": "epsilon_projective_trace;epsilon_hypermomentum_source",
            "status": "OPEN_GM_TRANSFER",
            "source_path": str(SOURCES["sro_2122"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def inherited_count(symbol: str, source_key: str) -> int:
    return sum(1 for row in read_csv(SOURCES[source_key]["path"]) if row.get("coefficient_symbol") == symbol)


def p4_priority_rows() -> list[dict[str, Any]]:
    priorities = [
        {
            "rank": 1,
            "symbol": "epsilon_hypermomentum_source",
            "tail": "independent Gamma current / source-worldtube / boundary support",
            "why_now": "directly controls calibrated source coupling and Newton/local-GR source normalization; appears in source_worldtube, boundary and orbit components",
            "next_kernel": "K_source_worldtube + K_boundary_projector + K_Delta_PPN_alpha3",
            "zero_route": "delta S_source/readout/boundary / delta Gamma = 0 by q/e_obs support descent",
        },
        {
            "rank": 2,
            "symbol": "epsilon_projective_trace",
            "tail": "projective trace connection mode",
            "why_now": "blocks Palatini/LC promotion and contaminates orbit/source/clock readout unless all-sector invariant or fixed",
            "next_kernel": "K_projective_trace for orbit/clock/source and PPN alpha1/alpha2/xi",
            "zero_route": "all-sector projective invariance or parent gauge-fixing before readout",
        },
        {
            "rank": 3,
            "symbol": "epsilon_weyl_nonmetricity",
            "tail": "Weyl trace nonmetricity",
            "why_now": "tests clock/rod/source-normalization metricity and links to clock/WEP/product constraints",
            "next_kernel": "K_clock_redshift + K_rod_scale + K_source_norm",
            "zero_route": "clock/rod readout as proper time/length from g_obs only",
        },
        {
            "rank": 4,
            "symbol": "epsilon_shear_nonmetricity",
            "tail": "trace-free/shear nonmetricity",
            "why_now": "tests lightcone/Shapiro/optical readout and EM stress metricity",
            "next_kernel": "K_lightcone_shear + K_Shapiro_gamma",
            "zero_route": "photon/light readout from g_obs null cone plus owned EM gauge data",
        },
        {
            "rank": 5,
            "symbol": "epsilon_axial_torsion_spin",
            "tail": "axial torsion spin coupling",
            "why_now": "already sharpened in 3494; stays live only if owned-coframe spin branch is rejected globally or boundary spin-current leakage reopens",
            "next_kernel": "KRT component table / xi_A / frame map if spin zero branch rejected",
            "zero_route": "omega_spin=omega_LC[e_obs] and no independent contorsion",
        },
    ]
    rows: list[dict[str, Any]] = []
    for item in priorities:
        rows.append(
            {
                "priority_rank": item["rank"],
                "coefficient_symbol": item["symbol"],
                "tail": item["tail"],
                "why_now": item["why_now"],
                "wep_product_bound_rows": inherited_count(item["symbol"], "wep_3492"),
                "ppn_product_bound_rows": inherited_count(item["symbol"], "ppn_3492"),
                "next_kernel": item["next_kernel"],
                "zero_route": item["zero_route"],
                "status": "NEXT_ATTACK" if item["rank"] == 1 else ("WATCH_ALREADY_SHARPENED" if item["rank"] == 5 else "QUEUED"),
                "valid_for_claim": "False",
            }
        )
    return rows


def data_target_rows() -> list[dict[str, Any]]:
    targets = read_csv(SOURCES["targets_1900"]["path"])
    rows: list[dict[str, Any]] = []
    for row in targets:
        if row.get("target_id") in {"cmsm_ds_onera_root", "cmsm_ds_onera_segment_22", "local_suep_segments_1071", "local_surrogate_design_1075"}:
            rows.append(
                {
                    "target_id": row["target_id"],
                    "expected_artifact": row["expected_artifact"],
                    "current_status": row["current_status"],
                    "usable_for_claim": row["usable_for_claim"],
                    "role_in_3495": "source/readout support evidence; cannot close zero theorem unless official arrays or parent descent theorem exists",
                    "valid_for_claim": "False",
                }
            )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3495_0_descent_theorem_valid",
            "requirement": "q/e_obs descent theorem for source/readout/projector Gamma-current is mathematically valid",
            "passed": "True",
            "evidence": "SRO2122_0 exact conditional theorem",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3495_1_source_worldtube_signed",
            "requirement": "source profile/support/composition/GM are q/e_obs-owned and fixed before variation",
            "passed": "False",
            "evidence": "SRZ2118_0 and SEC2117_4 not closed",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3495_2_projector_commutator_zero",
            "requirement": "support/projector/boundary commutator delta(Pi)J is theorem-zero",
            "passed": "False",
            "evidence": "RVC1898_2 projector/source-worldtube obstruction survives",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3495_3_readout_operators_signed",
            "requirement": "clock, lightcone and orbit readout operators are downstream metric/gauge functors",
            "passed": "False",
            "evidence": "SRZ2118_1/2/3 and SRO2122_2/3 remain unsigned",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3495_4_p4_priority_queue_created",
            "requirement": "remaining P4 tails are ranked by local-GR/source-coupling risk with inherited bounds",
            "passed": "True",
            "evidence": "priority queue ranks hypermomentum/source-worldtube first",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3495_0_no_zero_claim",
            "decision": "Do not claim source/readout/boundary Gamma-current zero.",
            "rationale": "The descent theorem is exact, but source support, projector commutator, readout operators and boundary/domain maps are not signed.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3495_1_priority",
            "decision": "Prioritize epsilon_hypermomentum_source next.",
            "rationale": "It is the broadest remaining obstruction to calibrated source coupling, Newtonian source normalization and local-GR reduction.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3495_2_method",
            "decision": "Attack source-worldtube/support q/e_obs descent before trying to numerically fit every P4 tail.",
            "rationale": "A theorem-zero for source support would collapse the largest leak; if it fails, the same checkpoint supplies the kernel requirements for bounds.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3496-Y5-R2FR-source-worldtube-hypermomentum-zero-or-kernel-fill.md",
            "next_script": "scripts/Y5_R2FR_3496_source_worldtube_hypermomentum_zero_or_kernel_fill.py",
            "objective": "Try to prove source stress/profile/support/GM are q/e_obs-owned downstream data so epsilon_hypermomentum_source vanishes; if not, fill the first source-worldtube hypermomentum kernel interface.",
            "success_gate": "source-worldtube q/e_obs descent theorem-zero, or executable K_source_worldtube/K_boundary_projector/K_Delta_PPN_alpha3 nonclaim kernel rows",
            "forbidden_shortcuts": "using point-source GR import as proof; treating surrogate MICROSCOPE data as official arrays; hiding support/projector commutators inside calibration",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    outputs: dict[str, Path],
    decomposition: list[dict[str, Any]],
    priority: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "check_id": "VAL3495_0_sources_exist",
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
            "check_id": "VAL3495_1_csv_parse",
            "passed": parse_ok,
            "detail": "; ".join(details),
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3495_2_decomposition_complete",
            "passed": len(decomposition) >= 6,
            "detail": f"components={len(decomposition)}",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3495_3_priority_queue_complete",
            "passed": len(priority) == 5 and priority[0]["coefficient_symbol"] == "epsilon_hypermomentum_source",
            "detail": f"priority_rows={len(priority)}; top={priority[0]['coefficient_symbol'] if priority else 'none'}",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3495_4_parent_claim_blocked",
            "passed": any(row["passed"] == "False" and row["blocks_claim"] == "True" for row in gates),
            "detail": "source/readout/boundary Gamma-current claim remains blocked",
            "valid_for_claim": "False",
        }
    )
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append(
        {
            "check_id": "VAL3495_5_no_claim",
            "passed": all(row.get("valid_for_claim") == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3495_6_no_formalization_outputs",
            "passed": all(FORMALIZATION not in path.parents for path in outputs.values()),
            "detail": "outputs are under post-checkpoint-work/source-intake only",
            "valid_for_claim": "False",
        }
    )
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append(
        {
            "check_id": "VAL3495_SUMMARY",
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
    theorems: list[dict[str, Any]],
    decomposition: list[dict[str, Any]],
    priority: list[dict[str, Any]],
    data_targets: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3495: Source Readout Boundary Gamma-Current Zero Or P4 Tail Priority",
                "",
                "## Current Verdict",
                "- **Exact theorem:** q/e_obs descent plus post-variation readout kills source/readout/boundary Gamma-currents.",
                "- **No claim:** source-worldtube support, projector commutators, clock/light/orbit readout and boundary/domain maps are not parent-signed.",
                "- **Main obstruction:** `epsilon_hypermomentum_source` is now the highest-priority P4 tail because it controls source coupling and Newton/local-GR normalization.",
                "- **Queue:** projective trace, Weyl nonmetricity, shear nonmetricity follow; axial torsion is already sharpened from 3494.",
                "",
                "## Zero Theorem Attempts",
                md_table(theorems, ["theorem_id", "target", "statement", "current_status", "valid_for_claim"]),
                "",
                "## Gamma-Current Decomposition",
                md_table(decomposition, ["component_id", "component", "formula", "zero_condition", "mapped_tail", "status", "valid_for_claim"]),
                "",
                "## P4 Tail Priority Queue",
                md_table(priority, ["priority_rank", "coefficient_symbol", "tail", "why_now", "wep_product_bound_rows", "ppn_product_bound_rows", "status", "valid_for_claim"]),
                "",
                "## Readout Data Status",
                md_table(data_targets, ["target_id", "expected_artifact", "current_status", "usable_for_claim", "role_in_3495", "valid_for_claim"]),
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
    theorems = zero_theorem_rows()
    decomposition = gamma_current_decomposition_rows()
    priority = p4_priority_rows()
    data_targets = data_target_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3495_SOURCE_REGISTER.csv",
        "theorems": OUT / "P8_Y5_R2FR_3495_SOURCE_READOUT_BOUNDARY_ZERO_THEOREMS.csv",
        "decomposition": OUT / "P8_Y5_R2FR_3495_GAMMA_CURRENT_DECOMPOSITION.csv",
        "priority": OUT / "P8_Y5_R2FR_3495_P4_TAIL_PRIORITY_QUEUE.csv",
        "data_targets": OUT / "P8_Y5_R2FR_3495_READOUT_DATA_STATUS.csv",
        "gates": OUT / "P8_Y5_R2FR_3495_GATES.csv",
        "decisions": OUT / "P8_Y5_R2FR_3495_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3495_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["theorems"], theorems, ["theorem_id", "target", "statement", "proof", "current_status", "source_path", "valid_for_claim"])
    write_csv(outputs["decomposition"], decomposition, ["component_id", "component", "formula", "zero_condition", "mapped_tail", "status", "source_path", "valid_for_claim"])
    write_csv(outputs["priority"], priority, ["priority_rank", "coefficient_symbol", "tail", "why_now", "wep_product_bound_rows", "ppn_product_bound_rows", "next_kernel", "zero_route", "status", "valid_for_claim"])
    write_csv(outputs["data_targets"], data_targets, ["target_id", "expected_artifact", "current_status", "usable_for_claim", "role_in_3495", "valid_for_claim"])
    write_csv(outputs["gates"], gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"])
    write_csv(outputs["decisions"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, decomposition, priority, gates)
    validation_path = OUT / "P8_Y5_BRR545_3495_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(theorems, decomposition, priority, data_targets, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
