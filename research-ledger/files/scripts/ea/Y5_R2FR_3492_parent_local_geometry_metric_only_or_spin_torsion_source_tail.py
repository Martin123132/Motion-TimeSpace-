from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3492-Y5-R2FR-parent-local-geometry-metric-only-or-spin-torsion-source-tail.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3492": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3491": {
        "path": ROOT / "3491-Y5-R2FR-nonHilbert-current-bypass-or-readout-order-silence.md",
        "role": "3491 handoff",
    },
    "nh_2539": {
        "path": OUT / "P8_Y5_NO_SHADOW_2539_NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT.csv",
        "role": "no-hypermomentum/Levi-Civita audit",
    },
    "moc_1829": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1829_METRIC_ONLY_CONNECTION_THEOREM_ATTEMPT.csv",
        "role": "metric-only connection theorem attempt",
    },
    "nhm_1834": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1834_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv",
        "role": "no-hypermomentum theorem attempt",
    },
    "nh_2042": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2042_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv",
        "role": "observed hypermomentum definition and conditional theorem",
    },
    "lc_1960": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1960_LC_NO_HYPERMOMENTUM_ATTEMPT.csv",
        "role": "Levi-Civita/no-hypermomentum route split",
    },
    "mvs_1961": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1961_METRIC_ONLY_SIGNATURE_ATTEMPT.csv",
        "role": "metric-only signature audit",
    },
    "p4_interface_2042": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2042_P4_CONNECTION_INTERFACE.csv",
        "role": "P4 connection residual channel interface",
    },
    "spin_projective_2043": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2043_SPIN_PROJECTIVE_GUARD.csv",
        "role": "spin/projective/nonmetricity guard map",
    },
    "rbridge_3491": {
        "path": OUT / "P8_Y5_R2FR_3491_RBRIDGE_RESIDUAL_MAP.csv",
        "role": "3491 non-Hilbert residual map",
    },
    "matrix_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "role": "WEP rows with empirical eta bounds",
    },
    "ppn_2489": {
        "path": OUT / "P8_Y5_NO_SHADOW_2489_PPN_BOUND_LEDGER.csv",
        "role": "source-backed PPN comparator bounds",
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


def metric_only_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "LC3492_0_target",
            "route": "total local geometry reduction",
            "statement": "Derive Gamma_obs = Gamma_LC[g_obs] and Delta_Gamma = 0 for ordinary local tests.",
            "derivation": "This closes the spin/torsion/nonmetricity bypass only if the parent branch signs metric/coframe-only geometry or a Palatini no-hypermomentum equation.",
            "result": "TARGET_EXACT",
            "source_path": str(SOURCES["lc_1960"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "LC3492_1_metric_only_lemma",
            "route": "kinematic metric-only route",
            "statement": "If the parent variable list contains g/e but no independent Gamma/omega, then Gamma_obs is definitionally Levi-Civita.",
            "derivation": "On that configuration space Gamma_obs := Gamma_LC[g_obs], so T^lambda_{mu nu}=2 Gamma^lambda_[mu nu]=0 and Q_{lambda mu nu}=nabla^LC_lambda g_mu nu=0 by construction.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "source_path": str(SOURCES["moc_1829"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "LC3492_2_no_gamma_slot_lemma",
            "route": "matter/source no-hypermomentum route",
            "statement": "If S_ord has no independent Gamma argument, Delta_lambda^{mu nu}:= -2/sqrt(-g) delta S_ord/delta Gamma^lambda_{mu nu}=0.",
            "derivation": "The functional derivative with respect to an absent independent variable vanishes. Coframe-owned omega_LC[e_obs] contributes only through the metric/coframe Hilbert variation already counted.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "source_path": str(SOURCES["nh_2042"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "LC3492_3_parent_signature_test",
            "route": "current MTS corpus",
            "statement": "The current corpus does not parent-sign the metric-only/no-Gamma branch across matter, source, clock, light, orbit, and readout sectors.",
            "derivation": "1961 blocks parent variable list, metric ownership rank, q-stack descent, matter blindness, and no-Gamma readout reentry in one branch.",
            "result": "PARENT_SIGNATURE_MISSING",
            "source_path": str(SOURCES["mvs_1961"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def palatini_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "PAL3492_0_palatini_route",
            "statement": "If Gamma is independent but appears only in the EH/Palatini block and Delta_Gamma=0, the connection equation reduces to Levi-Civita up to projective gauge.",
            "derivation": "The Gamma Euler equation gives metric compatibility and zero torsion modulo the projective trace; fixing/projecting the trace yields Gamma=Gamma_LC[g].",
            "result": "STANDARD_CONDITIONAL_ROUTE",
            "source_path": str(SOURCES["lc_1960"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "PAL3492_1_projective_caveat",
            "statement": "Projective freedom is harmless only if all matter/source/readout sectors are projectively invariant or the projective trace is fixed.",
            "derivation": "Gamma -> Gamma + delta^lambda_mu A_nu can survive Palatini variation; it is observable if clocks, spin transport, source charge, or orbit readout couple to the trace.",
            "result": "UNSIGNED_CAVEAT",
            "source_path": str(SOURCES["spin_projective_2043"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "PAL3492_2_spin_torsion_counterbranch",
            "statement": "A first-order spin-connection branch with spinor matter does not generically give torsion zero.",
            "derivation": "If omega is independent, delta_omega S can give T^a proportional to a spin/hypermomentum current; zero requires an explicit coframe-owned spin connection or a source-tail bound.",
            "result": "COUNTERBRANCH_EXPLICIT",
            "source_path": str(SOURCES["lc_1960"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "PAL3492_3_current_verdict",
            "statement": "The Palatini route is not claimable in the current corpus.",
            "derivation": "EH-only operator, no Gamma matter/source/readout coupling, projective silence, and spin-connection ownership are all unsigned in one parent branch.",
            "result": "PALATINI_ZERO_PROOF_NOT_CLOSED",
            "source_path": str(SOURCES["nh_2539"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def connection_tail_rows() -> list[dict[str, Any]]:
    return [
        {
            "tail_id": "P4T3492_0_axial_torsion",
            "symbol": "epsilon_axial_torsion_spin",
            "geometry_object": "S_mu or axial contorsion K_[abc]",
            "definition": "normalized projected spin/axial-torsion source tail",
            "weak_field_projection": "delta_PPN_alpha3 += K_alpha3_axial * epsilon_axial_torsion_spin; eta_AB += S_E^q Delta_epsilon_axial_torsion_spin_AB",
            "zero_condition": "omega_spin = omega_LC[e_obs] and no independent contorsion couples to spin current",
            "source_channel": "spin transport; fermion matter; clock/WEP source coupling",
            "source_path": str(SOURCES["spin_projective_2043"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "tail_id": "P4T3492_1_projective_trace",
            "symbol": "epsilon_projective_trace",
            "geometry_object": "Gamma projective trace A_mu",
            "definition": "normalized projected projective-trace connection tail",
            "weak_field_projection": "delta_PPN_alpha1/alpha2 += K_projective * epsilon_projective_trace; clock/orbit/source readout tails if not invariant",
            "zero_condition": "projective trace is gauge, fixed, or unobservable in matter/source/readout",
            "source_channel": "clock; source charge; orbital readout; preferred-frame PPN",
            "source_path": str(SOURCES["spin_projective_2043"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "tail_id": "P4T3492_2_weyl_nonmetricity",
            "symbol": "epsilon_weyl_nonmetricity",
            "geometry_object": "Q_mu = Q_mu^lambda_lambda",
            "definition": "normalized Weyl-trace nonmetricity tail affecting rods, clocks, masses, and source normalization",
            "weak_field_projection": "delta_PPN_gamma/beta += K_weyl * epsilon_weyl_nonmetricity; eta_AB += S_E^q Delta_epsilon_weyl_nonmetricity_AB",
            "zero_condition": "metric compatibility for rods/clocks/source normalization or a sourced Weyl-trace bound",
            "source_channel": "clock; rods; WEP; source normalization",
            "source_path": str(SOURCES["spin_projective_2043"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "tail_id": "P4T3492_3_shear_nonmetricity",
            "symbol": "epsilon_shear_nonmetricity",
            "geometry_object": "traceless Q_tilde_lambda_mu_nu",
            "definition": "normalized shear nonmetricity tail affecting light cones and anisotropic readout",
            "weak_field_projection": "delta_PPN_gamma/Shapiro += K_shear * epsilon_shear_nonmetricity; lightcone readout tail retained",
            "zero_condition": "null cones and optical readout are metric g_obs readouts, not shear-nonmetric connection readouts",
            "source_channel": "lightcone; Shapiro; clock; WEP",
            "source_path": str(SOURCES["spin_projective_2043"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "tail_id": "P4T3492_4_hypermomentum",
            "symbol": "epsilon_hypermomentum_source",
            "geometry_object": "Delta_lambda^{mu nu}",
            "definition": "normalized matter/source/readout independent-connection current",
            "weak_field_projection": "delta_PPN_alpha3/source-current += K_Delta * epsilon_hypermomentum_source; eta_AB += S_E^q Delta_epsilon_hypermomentum_source_AB",
            "zero_condition": "delta S_ord/delta Gamma=0 across matter, source, clock, light and orbital readout",
            "source_channel": "matter source current; readout reentry; WEP; PPN source-current",
            "source_path": str(SOURCES["p4_interface_2042"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def wep_product_rows(tails: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matrix = read_csv(SOURCES["matrix_3475"]["path"])
    wep_rows = [row for row in matrix if row["row_type"] == "WEP_material_difference"]
    rows: list[dict[str, Any]] = []
    for tail in tails:
        for index, wep in enumerate(wep_rows):
            rows.append(
                {
                    "bound_id": f"LCW3492_{tail['symbol']}_{index}_{wep['aug_row_id']}",
                    "coefficient_symbol": tail["symbol"],
                    "arena": wep["arena"],
                    "observable_row": wep["aug_row_id"],
                    "product_symbol": f"abs(S_E^q) * abs(Delta_{tail['symbol']}_AB)",
                    "bound_value": wep["bound"],
                    "bound_units": wep["bound_units"],
                    "projection": tail["weak_field_projection"],
                    "source_path": wep["source_path"],
                    "isolates_coefficient": "False",
                    "valid_for_claim": "False",
                }
            )
    return rows


def ppn_product_rows(tails: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ppn_rows = read_csv(SOURCES["ppn_2489"]["path"])
    rows: list[dict[str, Any]] = []
    preferred: dict[str, list[str]] = {
        "epsilon_axial_torsion_spin": ["alpha3", "alpha1", "alpha2"],
        "epsilon_projective_trace": ["alpha1", "alpha2", "xi"],
        "epsilon_weyl_nonmetricity": ["gamma_minus_1", "beta_minus_1"],
        "epsilon_shear_nonmetricity": ["gamma_minus_1", "xi"],
        "epsilon_hypermomentum_source": ["alpha3", "gamma_minus_1", "beta_minus_1"],
    }
    for tail in tails:
        observables = preferred[tail["symbol"]]
        for ppn in ppn_rows:
            if ppn["observable"] not in observables:
                continue
            rows.append(
                {
                    "bound_id": f"LCP3492_{tail['symbol']}_{ppn['observable']}",
                    "coefficient_symbol": tail["symbol"],
                    "observable": ppn["observable"],
                    "dataset_id": ppn["dataset_id"],
                    "product_symbol": f"abs(K_{ppn['observable']}_{tail['symbol']} * {tail['symbol']})",
                    "bound_value": ppn["upper_bound"],
                    "bound_units": ppn["units"],
                    "projection_status": "SYMBOLIC_KERNEL_REQUIRED",
                    "missing_for_score": f"K_{ppn['observable']}_{tail['symbol']} weak-field projection coefficient",
                    "source_reference": ppn["reference"],
                    "valid_for_claim": "False",
                }
            )
    return rows


def status_update_rows(tails: list[dict[str, Any]], wep_bounds: list[dict[str, Any]], ppn_bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for tail in tails:
        wep_ids = [row["bound_id"] for row in wep_bounds if row["coefficient_symbol"] == tail["symbol"]]
        ppn_ids = [row["bound_id"] for row in ppn_bounds if row["coefficient_symbol"] == tail["symbol"]]
        rows.append(
            {
                "tail_id": tail["tail_id"],
                "symbol": tail["symbol"],
                "old_status": "OPEN_PRODUCT_BOUNDABLE",
                "new_status": "WEP_AND_PPN_PRODUCT_BOUNDED_NOT_ISOLATED",
                "wep_bound_sources": ";".join(wep_ids),
                "ppn_bound_sources": ";".join(ppn_ids),
                "meaning": "tail has explicit WEP and PPN product-bound interfaces but no isolated coefficient and no local-GR claim",
                "valid_for_claim": "False",
            }
        )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3492_0_metric_only_conditional_theorem",
            "requirement": "metric/coframe-only configuration implies Levi-Civita connection",
            "passed": "True",
            "evidence": "MOC1829_1 and NH2042_1/2 are exact conditional lemmas",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3492_1_parent_variable_list",
            "requirement": "parent action/object language excludes independent observed Gamma/omega",
            "passed": "False",
            "evidence": "MVS1961_1 not parent-signed",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3492_2_matter_source_readout_no_gamma",
            "requirement": "matter, source, clock, light, orbit, and readout sectors carry no independent Gamma charge",
            "passed": "False",
            "evidence": "NH2042_4 and SPG2043_4 unsigned",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3492_3_spin_projective_nonmetricity_silence",
            "requirement": "spin/torsion, projective trace, Weyl trace, and shear nonmetricity are silent or bounded",
            "passed": "False",
            "evidence": "SPG2043 guard rows unsigned",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3492_4_tail_bounds_created",
            "requirement": "fallback P4 connection tails have explicit WEP and PPN product-bound interfaces",
            "passed": "True",
            "evidence": "generated WEP and PPN product-bound rows for all five connection tails",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM3492_0_metric_only_LC",
            "statement": "Metric/coframe-only parent geometry implies Levi-Civita local geometry.",
            "proof": "If the independent variables do not include Gamma, the only connection available to matter/readout is Gamma_LC[g_obs] or omega_LC[e_obs]; torsion/nonmetricity are not independent degrees of freedom.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3492_1_no_gamma_no_hypermomentum",
            "statement": "No independent Gamma slot implies zero observed hypermomentum.",
            "proof": "Delta_lambda^{mu nu} is the functional derivative of S_ord with respect to independent Gamma. If S_ord is a functional only of e_obs, omega_LC[e_obs], matter, gauge fields, and constants, that derivative vanishes.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3492_2_spin_counterbranch",
            "statement": "Independent spin connection plus spinor matter is a real counterbranch to torsion zero.",
            "proof": "In first-order language, varying an independent spin connection can produce torsion sourced by spin/hypermomentum. This is not erased by calling the current non-Hilbert.",
            "result": "COUNTERBRANCH_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3492_3_tail_bound_progress",
            "statement": "If the LC/no-hypermomentum theorem is unsigned, the correct fallback is a decomposed connection-tail vector with WEP and PPN product bounds.",
            "proof": "Each torsion/nonmetricity/hypermomentum channel maps to an observable product against WEP eta or to a symbolic PPN projection coefficient constrained by source-backed PPN comparators.",
            "result": "FINITE_NONCLAIM_PROGRESS",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3492_0_lc_status",
            "decision": "Do not claim local Levi-Civita reduction.",
            "rationale": "The exact theorem exists, but its parent variable-list and no-Gamma matter/source/readout premises are unsigned.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3492_1_tail_status",
            "decision": "Upgrade the spin/torsion/hypermomentum loophole into a five-component P4 connection tail vector.",
            "rationale": "This turns the coupling worry into test-facing quantities instead of a vague obstruction.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3492_2_best_next_attack",
            "decision": "Attack parent field inventory/no-independent-Gamma signature next.",
            "rationale": "Signing that one clause would collapse the clean LC route much faster than trying to numerically source every tail.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3493-Y5-R2FR-parent-field-inventory-no-independent-Gamma-or-P4-tail-lock.md",
            "next_script": "scripts/Y5_R2FR_3493_parent_field_inventory_no_independent_Gamma_or_P4_tail_lock.py",
            "objective": "Try to sign the parent field inventory/object-language clause that excludes independent observed Gamma; if it fails, lock the P4 connection-tail vector as the official local-geometry fallback.",
            "success_gate": "parent variable list and matter/source/readout functor prove no independent Gamma, or P4 tail vector becomes the official finite local-geometry residual interface",
            "forbidden_shortcuts": "assuming GR geometry before parent field inventory is signed; hiding spin torsion inside Hilbert stress; treating PPN product bounds as isolated coefficients",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    outputs: dict[str, Path],
    tails: list[dict[str, Any]],
    wep_bounds: list[dict[str, Any]],
    ppn_bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "check_id": "VAL3492_0_sources_exist",
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
            "check_id": "VAL3492_1_csv_parse",
            "passed": parse_ok,
            "detail": "; ".join(details),
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3492_2_tail_vector_complete",
            "passed": len(tails) == 5,
            "detail": f"tails={len(tails)}",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3492_3_wep_bounds_created",
            "passed": len(wep_bounds) >= 10,
            "detail": f"wep_bounds={len(wep_bounds)}",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3492_4_ppn_bounds_created",
            "passed": len(ppn_bounds) >= 12,
            "detail": f"ppn_bounds={len(ppn_bounds)}",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3492_5_parent_claim_blocked",
            "passed": any(row["passed"] == "False" and row["blocks_claim"] == "True" for row in gates),
            "detail": "LC/no-hypermomentum claim remains blocked by parent signature gates",
            "valid_for_claim": "False",
        }
    )
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append(
        {
            "check_id": "VAL3492_6_no_claim",
            "passed": all(row.get("valid_for_claim") == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3492_7_no_formalization_outputs",
            "passed": all(FORMALIZATION not in path.parents for path in outputs.values()),
            "detail": "outputs are under post-checkpoint-work/source-intake only",
            "valid_for_claim": "False",
        }
    )
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append(
        {
            "check_id": "VAL3492_SUMMARY",
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
    metric_rows: list[dict[str, Any]],
    palatini_rows: list[dict[str, Any]],
    tails: list[dict[str, Any]],
    wep_bounds: list[dict[str, Any]],
    ppn_bounds: list[dict[str, Any]],
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
                "# 3492: Parent Local Geometry Metric-Only Or Spin-Torsion Source Tail",
                "",
                "## Current Verdict",
                "- **Derivation win:** the metric/coframe-only route is an exact conditional theorem: no independent `Gamma` means Levi-Civita geometry and zero observed hypermomentum.",
                "- **Claim block:** the current corpus still does not parent-sign the no-independent-`Gamma` variable list across matter, source, clocks, light, orbit, and readout.",
                "- **Counterbranch retained:** independent spin connection plus spinor/hypermomentum current can source torsion; this cannot be deleted by calling it non-Hilbert.",
                "- **Concrete progress:** the local-geometry loophole is now a five-component P4 connection-tail vector with WEP and PPN product-bound interfaces.",
                "- **No claim:** no local-GR, Levi-Civita, WEP, or PPN pass is claimed.",
                "",
                "## Metric-Only Derivation",
                md_table(metric_rows, ["attempt_id", "route", "statement", "derivation", "result", "valid_for_claim"]),
                "",
                "## Palatini And Spin Counterbranch",
                md_table(palatini_rows, ["attempt_id", "statement", "derivation", "result", "valid_for_claim"]),
                "",
                "## P4 Connection Tail Vector",
                md_table(tails, ["tail_id", "symbol", "geometry_object", "definition", "weak_field_projection", "zero_condition", "valid_for_claim"]),
                "",
                "## WEP Product Bounds",
                md_table(wep_bounds, ["bound_id", "coefficient_symbol", "arena", "product_symbol", "bound_value", "bound_units", "isolates_coefficient", "valid_for_claim"]),
                "",
                "## PPN Product Bounds",
                md_table(ppn_bounds, ["bound_id", "coefficient_symbol", "observable", "product_symbol", "bound_value", "bound_units", "projection_status", "valid_for_claim"]),
                "",
                "## Status Updates",
                md_table(updates, ["tail_id", "symbol", "old_status", "new_status", "meaning", "valid_for_claim"]),
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
    metric_rows = metric_only_derivation_rows()
    palatini_rows = palatini_derivation_rows()
    tails = connection_tail_rows()
    wep_bounds = wep_product_rows(tails)
    ppn_bounds = ppn_product_rows(tails)
    updates = status_update_rows(tails, wep_bounds, ppn_bounds)
    theorems = theorem_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3492_SOURCE_REGISTER.csv",
        "metric_derivation": OUT / "P8_Y5_R2FR_3492_METRIC_ONLY_DERIVATION.csv",
        "palatini_derivation": OUT / "P8_Y5_R2FR_3492_PALATINI_AND_SPIN_COUNTERBRANCH.csv",
        "tail_vector": OUT / "P8_Y5_R2FR_3492_P4_CONNECTION_TAIL_VECTOR.csv",
        "wep_bounds": OUT / "P8_Y5_R2FR_3492_WEP_PRODUCT_BOUNDS.csv",
        "ppn_bounds": OUT / "P8_Y5_R2FR_3492_PPN_PRODUCT_BOUNDS.csv",
        "updates": OUT / "P8_Y5_R2FR_3492_STATUS_UPDATES.csv",
        "theorems": OUT / "P8_Y5_R2FR_3492_THEOREM_LEDGER.csv",
        "gates": OUT / "P8_Y5_R2FR_3492_GATES.csv",
        "decisions": OUT / "P8_Y5_R2FR_3492_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3492_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["metric_derivation"], metric_rows, ["attempt_id", "route", "statement", "derivation", "result", "source_path", "valid_for_claim"])
    write_csv(outputs["palatini_derivation"], palatini_rows, ["attempt_id", "statement", "derivation", "result", "source_path", "valid_for_claim"])
    write_csv(outputs["tail_vector"], tails, ["tail_id", "symbol", "geometry_object", "definition", "weak_field_projection", "zero_condition", "source_channel", "source_path", "valid_for_claim"])
    write_csv(outputs["wep_bounds"], wep_bounds, ["bound_id", "coefficient_symbol", "arena", "observable_row", "product_symbol", "bound_value", "bound_units", "projection", "source_path", "isolates_coefficient", "valid_for_claim"])
    write_csv(outputs["ppn_bounds"], ppn_bounds, ["bound_id", "coefficient_symbol", "observable", "dataset_id", "product_symbol", "bound_value", "bound_units", "projection_status", "missing_for_score", "source_reference", "valid_for_claim"])
    write_csv(outputs["updates"], updates, ["tail_id", "symbol", "old_status", "new_status", "wep_bound_sources", "ppn_bound_sources", "meaning", "valid_for_claim"])
    write_csv(outputs["theorems"], theorems, ["theorem_id", "statement", "proof", "result", "valid_for_claim"])
    write_csv(outputs["gates"], gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"])
    write_csv(outputs["decisions"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, tails, wep_bounds, ppn_bounds, gates)
    validation_path = OUT / "P8_Y5_BRR545_3492_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(metric_rows, palatini_rows, tails, wep_bounds, ppn_bounds, updates, theorems, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
