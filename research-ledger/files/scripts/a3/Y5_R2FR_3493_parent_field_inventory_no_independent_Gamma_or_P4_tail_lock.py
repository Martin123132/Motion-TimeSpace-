from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3493-Y5-R2FR-parent-field-inventory-no-independent-Gamma-or-P4-tail-lock.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3493": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3492": {
        "path": ROOT / "3492-Y5-R2FR-parent-local-geometry-metric-only-or-spin-torsion-source-tail.md",
        "role": "3492 handoff",
    },
    "ogs_2047": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2047_OBSERVED_GEOMETRY_SLOT_AUDIT.csv",
        "role": "observed geometry slot audit",
    },
    "pas_2416": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2416_PARENT_ACTION_SIGNATURE_SPINE.csv",
        "role": "parent action signature spine",
    },
    "sga_2415": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2415_SECTOR_GAMMA_SLOT_AUDIT.csv",
        "role": "sector Gamma-slot audit",
    },
    "ngsa_2540": {
        "path": OUT / "P8_Y5_NO_SHADOW_2540_GAMMA_SLOT_SECTOR_AUDIT.csv",
        "role": "no-Gamma sector audit",
    },
    "gso_2043": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2043_GAMMA_SLOT_OWNER_THEOREM_ATTEMPT.csv",
        "role": "Gamma-slot owner theorem attempt",
    },
    "srz_2118": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_ZERO_THEOREM_ATTEMPT.csv",
        "role": "source/readout zero theorem attempt",
    },
    "sro_2122": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_LEMMA.csv",
        "role": "source/readout owner lemma",
    },
    "msrl_3037": {
        "path": OUT / "P8_Y5_R2FR_3037_MINIMUM_SOURCE_READOUT_LOCK_PARENT_CLAUSE.csv",
        "role": "minimum source-readout lock parent clause",
    },
    "tail_3492": {
        "path": OUT / "P8_Y5_R2FR_3492_P4_CONNECTION_TAIL_VECTOR.csv",
        "role": "P4 connection tail vector",
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


def parent_inventory_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "INV3493_0_total_object_language",
            "clause": "parent ordinary/local action argument list",
            "formal_statement": "Arg(S_ord^local) = {q(Phi), e_obs(q), g_obs(q), omega_LC[e_obs], Psi_A, A_owned, theta_A, fixed downstream readout/support maps}; Gamma_ind is not an argument.",
            "derivation": "If this object language is signed, every Gamma_ind derivative of matter/source/readout vanishes by variable absence.",
            "current_status": "CONTRACT_EXACT_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["ogs_2047"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "INV3493_1_metric_coframe_owner",
            "clause": "observed geometry owner",
            "formal_statement": "e_obs = E(q(Phi)); g_obs = eta_ab e_obs^a e_obs^b; omega_spin = omega_LC[e_obs] unless a P4 tail is retained.",
            "derivation": "The LC theorem from 3492 follows by construction once e/g are the only observed geometry variables.",
            "current_status": "PRIVATE_CANDIDATE_NOT_PUBLICLY_DERIVED",
            "source_path": str(SOURCES["pas_2416"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "INV3493_2_sector_sum_no_gamma",
            "clause": "sector-sum hypermomentum zero",
            "formal_statement": "Delta_Gamma^total = sum_i delta S_i/delta Gamma_ind = 0 over matter, spin, EM/light, source, clocks, orbit, projective and boundary sectors.",
            "derivation": "This is exact only if every sector either excludes Gamma_ind or has a signed silence theorem.",
            "current_status": "SECTOR_SUM_NOT_PUBLICLY_SIGNED",
            "source_path": str(SOURCES["sga_2415"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "INV3493_3_readout_support_owner",
            "clause": "source/readout/support maps are downstream q-natural maps",
            "formal_statement": "R_i(Phi)=Rbar_i(q(Phi), e_obs, A_owned, theta) and Pi_i are fixed before variation, so v in ker(Dq) gives delta_v(Pi_i J_i)=0.",
            "derivation": "The source/readout owner lemma is valid conditionally, but support/projector/worldtube descent is not yet sector-signed.",
            "current_status": "CONDITIONAL_THEOREM_BLOCKED_BY_SUPPORT_AND_COMMUTATOR",
            "source_path": str(SOURCES["sro_2122"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "INV3493_4_boundary_source_owner",
            "clause": "boundary and source Hamiltonian owner",
            "formal_statement": "theta_MTS, Q_tau, H_tau, H_ref, M_H_ref, support boundaries and improvement currents are parent-owned before readout.",
            "derivation": "Without this, a no-Gamma proof can be undone by boundary/projector/source-current leakage even if ordinary matter is clean.",
            "current_status": "MISSING_PRIMARY_LEAK_AND_SOURCE_OWNER",
            "source_path": str(SOURCES["pas_2416"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def sector_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector_id": "SEC3493_0_ordinary_matter",
            "sector": "ordinary_matter",
            "no_gamma_status": "CONDITIONAL_SUPPORTED_NOT_PUBLICLY_SIGNED",
            "best_evidence": "owned-coframe branch supports S_A[Psi_A,e_obs,omega_LC[e_obs],A_owned,theta_A]",
            "open_gap": "global Arg(S_ord) signature and direct representative/marker exclusion",
            "p4_tail_if_open": "epsilon_hypermomentum_source",
            "source_path": str(SOURCES["sga_2415"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "sector_id": "SEC3493_1_spin_connection",
            "sector": "spin_connection",
            "no_gamma_status": "EXACT_CONDITIONAL_COFAME_OWNED_NOT_PUBLIC",
            "best_evidence": "omega_spin=omega_LC[e_obs] kills independent spin/torsion only in owned-coframe branch",
            "open_gap": "independent torsion/metric-affine counterbranch not parent-excluded",
            "p4_tail_if_open": "epsilon_axial_torsion_spin",
            "source_path": str(SOURCES["sga_2415"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "sector_id": "SEC3493_2_em_light",
            "sector": "em_gauge_and_lightcone",
            "no_gamma_status": "PARTIAL_GAUGE_OWNER_NOT_FULL_READOUT",
            "best_evidence": "standard EM branch likely uses A_mu, F=dA, g_obs/Hodge rather than affine Gamma",
            "open_gap": "optical, Shapiro, ray and detector readout maps not all written as downstream Gamma-free functionals",
            "p4_tail_if_open": "epsilon_shear_nonmetricity",
            "source_path": str(SOURCES["sga_2415"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "sector_id": "SEC3493_3_source_worldtube",
            "sector": "source_worldtube",
            "no_gamma_status": "PRIVATE_SRNG_ZERO_ONLY",
            "best_evidence": "source support can be zero inside private SRNG/owned-coframe branch",
            "open_gap": "source support/worldtube selector not public parent theorem",
            "p4_tail_if_open": "epsilon_hypermomentum_source",
            "source_path": str(SOURCES["srz_2118"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "sector_id": "SEC3493_4_clocks_rods",
            "sector": "clocks_rods",
            "no_gamma_status": "PRIVATE_SRNG_ZERO_ONLY",
            "best_evidence": "clock/rod zero theorem works if readout uses only proper time/length from g_obs and fixed constants",
            "open_gap": "clock/readout action-argument certificate not public theorem",
            "p4_tail_if_open": "epsilon_weyl_nonmetricity",
            "source_path": str(SOURCES["srz_2118"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "sector_id": "SEC3493_5_orbital_readout",
            "sector": "orbital_readout",
            "no_gamma_status": "PRIVATE_SRNG_ZERO_ONLY",
            "best_evidence": "orbital zero route works if orbit/GM readout is downstream of source measure, Poisson/Gauss calibration and g_obs geodesic motion",
            "open_gap": "test-body/trajectory readout cannot import GR geodesics before parent proof",
            "p4_tail_if_open": "epsilon_projective_trace",
            "source_path": str(SOURCES["srz_2118"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "sector_id": "SEC3493_6_projective_trace",
            "sector": "projective_trace",
            "no_gamma_status": "PRIVATE_OWNED_COFRAME_ZERO_ONLY",
            "best_evidence": "projective trace absent in owned-coframe branch or harmless if all-sector invariant/fixed",
            "open_gap": "all-sector projective invariance/gauge fixation missing",
            "p4_tail_if_open": "epsilon_projective_trace",
            "source_path": str(SOURCES["sga_2415"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "sector_id": "SEC3493_7_boundary_improvement",
            "sector": "boundary_improvement",
            "no_gamma_status": "LIVE_PRIMARY_LEAK",
            "best_evidence": "not killed by private SRNG/spin/projective switches",
            "open_gap": "theta_MTS/Q_tau/H_tau/H_ref/M_H_ref and boundary object exhaustion missing",
            "p4_tail_if_open": "epsilon_axial_torsion_spin;epsilon_hypermomentum_source;epsilon_projective_trace",
            "source_path": str(SOURCES["sga_2415"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def no_gamma_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "NGT3493_0_variable_absence",
            "statement": "If Gamma_ind is absent from Arg(S_total^ord), then Delta_Gamma^total=0 by variable absence.",
            "proof": "For each sector S_i[q,e_obs,omega_LC[e_obs],Psi,A,theta,R_post], the partial functional derivative with respect to an independent Gamma_ind is zero. Summing sector derivatives preserves zero.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NGT3493_1_spin_not_hidden",
            "statement": "Spinors do not force independent torsion if omega is explicitly omega_LC[e_obs]; they do if omega_ind is admitted.",
            "proof": "The coframe-owned spin connection routes variation through e_obs/Hilbert stress. An independent first-order omega admits a spin/hypermomentum current and must be retained as P4.",
            "result": "FORK_EXACT",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NGT3493_2_readout_not_hidden",
            "statement": "Readout/source maps do not carry Gamma current only when they are downstream q/e_obs functors fixed before variation.",
            "proof": "If support, projector, clock, light, orbit, or GM maps are inserted before variation, their Gamma dependence creates an effective source current. If they are post-variation q-natural maps, the derivative is silent.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "NGT3493_3_public_verdict",
            "statement": "The current public parent field inventory does not sign no-independent-Gamma for the whole local branch.",
            "proof": "Sector evidence supports a private owned-coframe route, but source/readout, boundary, projective, and all-sector activation remain unsigned in current files.",
            "result": "ZERO_PROOF_NOT_CLOSED",
            "valid_for_claim": "False",
        },
    ]


def p4_official_lock_rows() -> list[dict[str, Any]]:
    tails = read_csv(SOURCES["tail_3492"]["path"])
    wep = read_csv(SOURCES["wep_3492"]["path"])
    ppn = read_csv(SOURCES["ppn_3492"]["path"])
    wep_counts: dict[str, int] = defaultdict(int)
    ppn_counts: dict[str, int] = defaultdict(int)
    for row in wep:
        wep_counts[row["coefficient_symbol"]] += 1
    for row in ppn:
        ppn_counts[row["coefficient_symbol"]] += 1

    rows: list[dict[str, Any]] = []
    for tail in tails:
        rows.append(
            {
                "lock_id": f"LOCK3493_{tail['tail_id']}",
                "tail_id": tail["tail_id"],
                "symbol": tail["symbol"],
                "geometry_object": tail["geometry_object"],
                "official_status": "OFFICIAL_LOCAL_GEOMETRY_FALLBACK_NONCLAIM",
                "why_locked": "parent field inventory/no-independent-Gamma proof is not public-signed across all local sectors",
                "wep_product_bound_rows": wep_counts[tail["symbol"]],
                "ppn_product_bound_rows": ppn_counts[tail["symbol"]],
                "zero_route": tail["zero_condition"],
                "next_action": "derive sector no-Gamma signature or fill kernel coefficient for this tail",
                "valid_for_claim": "False",
            }
        )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3493_0_variable_absence_theorem",
            "requirement": "variable-absence no-Gamma theorem is mathematically valid",
            "passed": "True",
            "evidence": "GSO2043_1 plus 3492 theorem ledger",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3493_1_parent_inventory_signed",
            "requirement": "parent action field inventory excludes independent Gamma in one public action object",
            "passed": "False",
            "evidence": "PAS2416_9 and OGS2047_7 fail current public activation",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3493_2_sector_sum_signed",
            "requirement": "matter, spin, EM/light, source, clock, orbit, projective and boundary sectors all exclude Gamma or prove silence",
            "passed": "False",
            "evidence": "SGA2415_10 says public no-Gamma not closed",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3493_3_source_readout_descent_signed",
            "requirement": "source/readout/support/projector maps descend through q/e_obs and are fixed before variation",
            "passed": "False",
            "evidence": "SRO2122_6 blocked by commutator and source support",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3493_4_p4_fallback_locked",
            "requirement": "P4 connection-tail vector is adopted as official finite local-geometry fallback",
            "passed": "True",
            "evidence": "3492 tail vector locked with WEP/PPN product-bound counts",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3493_0_no_lc_claim",
            "decision": "Do not promote local Levi-Civita/no-hypermomentum closure yet.",
            "rationale": "The theorem is exact but the public parent field inventory and sector-sum no-Gamma signature are not signed.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3493_1_p4_lock",
            "decision": "Lock the five-component P4 connection-tail vector as the official local-geometry fallback.",
            "rationale": "This prevents hidden GR assumptions while keeping the geometry problem test-facing and finite.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3493_2_best_next_attack",
            "decision": "Attack the ordinary matter/spin sub-branch first, because it is the nearest clean theorem-zero win.",
            "rationale": "Ordinary matter and coframe-owned spin are already conditionally strong; proving/adopting them would remove axial torsion and narrow P4 to source/readout/boundary.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3494-Y5-R2FR-ordinary-matter-coframe-owned-spin-proof-or-axial-torsion-tail.md",
            "next_script": "scripts/Y5_R2FR_3494_ordinary_matter_coframe_owned_spin_proof_or_axial_torsion_tail.py",
            "objective": "Try to prove ordinary matter and spin transport use omega_LC[e_obs] only; if not, keep epsilon_axial_torsion_spin as the first official P4 tail to source.",
            "success_gate": "ordinary matter + spin connection no-Gamma theorem-zero, or axial torsion tail gains a sharper spin/clock/WEP/PPN kernel interface",
            "forbidden_shortcuts": "assuming spin torsion is absent because GR usually sets it so; using private branch notation as public parent proof; treating P4 product bounds as isolated coefficients",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(outputs: dict[str, Path], locks: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "check_id": "VAL3493_0_sources_exist",
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
            "check_id": "VAL3493_1_csv_parse",
            "passed": parse_ok,
            "detail": "; ".join(details),
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3493_2_p4_lock_complete",
            "passed": len(locks) == 5 and all(int(row["wep_product_bound_rows"]) >= 2 and int(row["ppn_product_bound_rows"]) >= 2 for row in locks),
            "detail": f"locks={len(locks)}",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3493_3_parent_claim_blocked",
            "passed": any(row["passed"] == "False" and row["blocks_claim"] == "True" for row in gates),
            "detail": "parent inventory and sector-sum gates remain claim-blocking",
            "valid_for_claim": "False",
        }
    )
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append(
        {
            "check_id": "VAL3493_4_no_claim",
            "passed": all(row.get("valid_for_claim") == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3493_5_no_formalization_outputs",
            "passed": all(FORMALIZATION not in path.parents for path in outputs.values()),
            "detail": "outputs are under post-checkpoint-work/source-intake only",
            "valid_for_claim": "False",
        }
    )
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append(
        {
            "check_id": "VAL3493_SUMMARY",
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
    inventory: list[dict[str, Any]],
    sectors: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    locks: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3493: Parent Field Inventory No Independent Gamma Or P4 Tail Lock",
                "",
                "## Current Verdict",
                "- **Exact theorem:** if the parent local ordinary action has no independent `Gamma_ind` argument, then total observed hypermomentum vanishes by variable absence.",
                "- **No promotion:** the current corpus does not sign that field inventory across all matter, spin, EM/light, source, clock, orbit, projective and boundary sectors.",
                "- **Real narrowing:** ordinary matter and coframe-owned spin are the closest clean theorem-zero sub-branch; boundary/source/readout remain the heavy leaks.",
                "- **Fallback locked:** the five-component P4 connection-tail vector is now the official local-geometry fallback, with WEP/PPN product-bound interfaces inherited from 3492.",
                "- **No claim:** no local-GR or Levi-Civita pass is claimed.",
                "",
                "## Parent Inventory Contract",
                md_table(inventory, ["contract_id", "clause", "formal_statement", "current_status", "valid_for_claim"]),
                "",
                "## Sector Gamma Signature Matrix",
                md_table(sectors, ["sector_id", "sector", "no_gamma_status", "open_gap", "p4_tail_if_open", "valid_for_claim"]),
                "",
                "## No-Gamma Theorems",
                md_table(theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"]),
                "",
                "## Official P4 Lock",
                md_table(locks, ["lock_id", "symbol", "official_status", "wep_product_bound_rows", "ppn_product_bound_rows", "zero_route", "valid_for_claim"]),
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
    inventory = parent_inventory_contract_rows()
    sectors = sector_signature_rows()
    theorems = no_gamma_theorem_rows()
    locks = p4_official_lock_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3493_SOURCE_REGISTER.csv",
        "inventory_contract": OUT / "P8_Y5_R2FR_3493_PARENT_FIELD_INVENTORY_CONTRACT.csv",
        "sector_matrix": OUT / "P8_Y5_R2FR_3493_SECTOR_GAMMA_SIGNATURE_MATRIX.csv",
        "theorems": OUT / "P8_Y5_R2FR_3493_NO_GAMMA_THEOREM_LEDGER.csv",
        "p4_lock": OUT / "P8_Y5_R2FR_3493_OFFICIAL_P4_LOCAL_GEOMETRY_INTERFACE.csv",
        "gates": OUT / "P8_Y5_R2FR_3493_GATES.csv",
        "decisions": OUT / "P8_Y5_R2FR_3493_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3493_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["inventory_contract"], inventory, ["contract_id", "clause", "formal_statement", "derivation", "current_status", "source_path", "valid_for_claim"])
    write_csv(outputs["sector_matrix"], sectors, ["sector_id", "sector", "no_gamma_status", "best_evidence", "open_gap", "p4_tail_if_open", "source_path", "valid_for_claim"])
    write_csv(outputs["theorems"], theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"])
    write_csv(outputs["p4_lock"], locks, ["lock_id", "tail_id", "symbol", "geometry_object", "official_status", "why_locked", "wep_product_bound_rows", "ppn_product_bound_rows", "zero_route", "next_action", "valid_for_claim"])
    write_csv(outputs["gates"], gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"])
    write_csv(outputs["decisions"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, locks, gates)
    validation_path = OUT / "P8_Y5_BRR545_3493_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(inventory, sectors, theorems, locks, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
