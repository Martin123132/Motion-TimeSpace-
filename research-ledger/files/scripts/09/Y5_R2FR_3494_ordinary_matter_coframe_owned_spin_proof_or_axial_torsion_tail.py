from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3494-Y5-R2FR-ordinary-matter-coframe-owned-spin-proof-or-axial-torsion-tail.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3494": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3493": {
        "path": ROOT / "3493-Y5-R2FR-parent-field-inventory-no-independent-Gamma-or-P4-tail-lock.md",
        "role": "3493 handoff",
    },
    "sector_3493": {
        "path": OUT / "P8_Y5_R2FR_3493_SECTOR_GAMMA_SIGNATURE_MATRIX.csv",
        "role": "3493 sector signature matrix",
    },
    "p4_lock_3493": {
        "path": OUT / "P8_Y5_R2FR_3493_OFFICIAL_P4_LOCAL_GEOMETRY_INTERFACE.csv",
        "role": "3493 official P4 fallback lock",
    },
    "spin_2115": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2115_SPIN_GUARD_GATE.csv",
        "role": "spin guard gate",
    },
    "spin_sig_2116": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2116_PARENT_SPIN_SIGNATURE_AUDIT.csv",
        "role": "parent spin signature audit",
    },
    "axial_map_2115": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2115_AXIAL_CMTS_KRT_MAP.csv",
        "role": "C_MTS to KRT axial map",
    },
    "axial_values_2116": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2116_AXIAL_COMPONENT_SOURCE_VALUES.csv",
        "role": "candidate branch axial values",
    },
    "spin_2348": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2348_SPIN_CONNECTION_COFRAME_OWNED_AUDIT.csv",
        "role": "coframe-owned spin connection audit",
    },
    "p4_axial_2348": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2348_AXIAL_TORSION_P4_COMPONENT_ROW.csv",
        "role": "axial torsion P4 component rows",
    },
    "ordinary_2647": {
        "path": OUT / "P8_Y5_ORDINARY_MATTER_SIGNATURE_2647_CLAUSE_MATRIX.csv",
        "role": "ordinary matter signature clause matrix",
    },
    "ordinary_3084": {
        "path": OUT / "P8_Y5_R2FR_3084_ORDINARY_MATTER_SIGNATURE_AUDIT.csv",
        "role": "ordinary matter signature audit",
    },
    "functor_1412": {
        "path": OUT / "P8_Y5_R10_1412_ORDINARY_MATTER_FUNCTOR_EXHAUSTION_AUDIT.csv",
        "role": "ordinary matter functor exhaustion audit",
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


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "SPIN3494_0_owned_coframe_action",
            "statement": "On an owned-coframe ordinary branch, S_ord + S_spin uses e_obs, omega_LC[e_obs], owned gauge fields and fixed theta, with no Gamma_ind or K_abc slot.",
            "derivation": "The parent action candidate in 2116 and the spin audit in 2348 give the exact action form needed for variable-absence hypermomentum zero.",
            "result": "CANDIDATE_BRANCH_EXACT_NOT_GLOBAL",
            "source_path": str(SOURCES["spin_sig_2116"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "SPIN3494_1_delta_gamma_zero",
            "statement": "If S_spin = Sbar[psi,e_obs,omega_LC[e_obs],A_owned,theta], then delta S_spin/delta Gamma_ind = 0.",
            "derivation": "Gamma_ind is not an independent argument. The omega_LC[e_obs] variation is a dependent coframe variation and belongs to Hilbert/coframe stress, not a separate torsion equation.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "source_path": str(SOURCES["spin_2348"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "SPIN3494_2_axial_zero_inside_branch",
            "statement": "Inside the signed owned-coframe branch, axial torsion A_MTS^mu and spin coupling xi_A are zero by variable absence, not by fitting.",
            "derivation": "LC geometry is torsion-free, so T_MTS=0 and A_MTS=0. The independent axial coupling xi_A multiplies a term absent from the owned-coframe action.",
            "result": "DERIVED_ZERO_ONLY_INSIDE_CANDIDATE_BRANCH",
            "source_path": str(SOURCES["axial_values_2116"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "SPIN3494_3_ordinary_matter_global_gap",
            "statement": "Ordinary matter action exhaustion is still not globally parent-signed.",
            "derivation": "2647/3084/1412 retain matter bundle, constant superselection, source-only weight, readout and shadow-domain gaps.",
            "result": "ORDINARY_MATTER_SIGNATURE_NOT_GLOBAL",
            "source_path": str(SOURCES["ordinary_3084"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "SPIN3494_4_counterbranch",
            "statement": "If an independent torsionful spin connection is admitted, axial torsion generically couples to spin and must remain as P4.",
            "derivation": "Einstein-Cartan/metric-affine alternatives introduce independent contorsion or axial vector slots; these are not killed by Hilbert stress language.",
            "result": "COUNTERBRANCH_RETAINS_AXIAL_TAIL",
            "source_path": str(SOURCES["spin_2115"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def fork_rows() -> list[dict[str, Any]]:
    return [
        {
            "fork_id": "FORK3494_0_owned_coframe_private_branch",
            "branch": "owned_coframe_spin",
            "premises": "Arg(S_spin) excludes Gamma_ind/K_abc; omega_spin=omega_LC[e_obs]; theta fixed; no axial torsion current term",
            "result": "Delta_spin=0, xi_A=0, A_MTS=0 inside the branch",
            "claim_status": "PRIVATE_CANDIDATE_NOT_PUBLIC_PARENT_SIGNATURE",
            "fallback_needed": "False inside branch; True globally",
            "valid_for_claim": "False",
        },
        {
            "fork_id": "FORK3494_1_metric_affine_counterbranch",
            "branch": "independent_spin_connection",
            "premises": "Arg(S_spin) includes omega_ind/Gamma_ind or contorsion K_abc and spin current",
            "result": "Delta_spin and axial torsion can be nonzero",
            "claim_status": "COUNTERBRANCH_NOT_EXCLUDED",
            "fallback_needed": "True",
            "valid_for_claim": "False",
        },
        {
            "fork_id": "FORK3494_2_global_parent_branch",
            "branch": "public_local_geometry",
            "premises": "all ordinary matter, spin transport, readout, source and boundary sectors share the owned-coframe object language",
            "result": "would retire epsilon_axial_torsion_spin and part of epsilon_hypermomentum_source",
            "claim_status": "NOT_SIGNED_BY_CURRENT_CORPUS",
            "fallback_needed": "True",
            "valid_for_claim": "False",
        },
    ]


def axial_kernel_rows() -> list[dict[str, Any]]:
    return [
        {
            "kernel_id": "AXK3494_0_connection_residual",
            "quantity": "C_MTS^lambda_{mu nu}",
            "formula": "C_MTS^lambda_{mu nu} := Gamma_MTS^lambda_{mu nu} - Gamma_LC^lambda_{mu nu}[g_obs]",
            "units": "m^-1",
            "status": "DEFINED_FALLBACK_NOT_NUMERIC",
            "missing_for_score": "parent choice LC-zero or independent affine branch plus C_MTS component values",
            "source_path": str(SOURCES["axial_map_2115"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "AXK3494_1_torsion_projection",
            "quantity": "T_MTS^lambda_{mu nu}",
            "formula": "T_MTS^lambda_{mu nu} = 2 C_MTS^lambda_{[mu nu]}",
            "units": "m^-1",
            "status": "EXACT_COMPONENT_FORMULA_IF_C_EXISTS",
            "missing_for_score": "antisymmetric C_MTS components and sign convention",
            "source_path": str(SOURCES["axial_map_2115"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "AXK3494_2_axial_projection",
            "quantity": "A_MTS^mu",
            "formula": "A_MTS^mu := (1/6) epsilon^{alpha beta gamma mu} T_MTS_{alpha beta gamma}",
            "units": "m^-1",
            "status": "EXACT_COMPONENT_FORMULA_WITH_ORIENTATION",
            "missing_for_score": "orientation, signature, index placement and local frame/component label",
            "source_path": str(SOURCES["axial_map_2115"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "AXK3494_3_unit_conversion",
            "quantity": "A_MTS_component_GeV",
            "formula": "A_MTS_component_GeV = 1.973269804e-16 * A_MTS_component_m^-1",
            "units": "GeV",
            "status": "UNIT_FACTOR_STAGED_NOT_SCOREABLE",
            "missing_for_score": "actual A_MTS value, xi_A, basis and KRT component convention",
            "source_path": str(SOURCES["axial_map_2115"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "AXK3494_4_spin_coupling",
            "quantity": "b_eff^I",
            "formula": "b_eff^I = xi_A R^I_mu A_MTS^mu + retained vector/tensor torsion mixing",
            "units": "GeV or declared KRT convention units",
            "status": "MISSING_XI_A_BASIS_FRAME_COMPONENT_BOUND",
            "missing_for_score": "xi_A, R^I_mu, mixing matrix, frame convention and component-specific bound",
            "source_path": str(SOURCES["axial_map_2115"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "AXK3494_5_no_cancellation_rule",
            "quantity": "epsilon_axial_torsion_spin",
            "formula": "abs(b_eff^I) plus absolute retained unmapped pieces <= B_KRT^I; no fitted cancellation",
            "units": "dimensionless after declared normalization or GeV in KRT comparison",
            "status": "OFFICIAL_FIRST_P4_TAIL_SHARPENED",
            "missing_for_score": "numeric components or public owned-coframe zero theorem",
            "source_path": str(SOURCES["p4_axial_2348"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def inherited_bound_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCES["wep_3492"]["path"]):
        if row["coefficient_symbol"] != "epsilon_axial_torsion_spin":
            continue
        rows.append(
            {
                "inherit_id": f"AXB3494_WEP_{row['bound_id']}",
                "bound_family": "WEP_product",
                "coefficient_symbol": row["coefficient_symbol"],
                "observable": row["arena"],
                "product_symbol": row["product_symbol"],
                "bound_value": row["bound_value"],
                "bound_units": row["bound_units"],
                "source": row["source_path"],
                "score_status": "PRODUCT_BOUND_NOT_ISOLATED",
                "valid_for_claim": "False",
            }
        )
    for row in read_csv(SOURCES["ppn_3492"]["path"]):
        if row["coefficient_symbol"] != "epsilon_axial_torsion_spin":
            continue
        rows.append(
            {
                "inherit_id": f"AXB3494_PPN_{row['bound_id']}",
                "bound_family": "PPN_product",
                "coefficient_symbol": row["coefficient_symbol"],
                "observable": row["observable"],
                "product_symbol": row["product_symbol"],
                "bound_value": row["bound_value"],
                "bound_units": row["bound_units"],
                "source": row["source_reference"],
                "score_status": "SYMBOLIC_KERNEL_REQUIRED",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            "inherit_id": "AXB3494_KRT_component_anchor",
            "bound_family": "spin_torsion_component_anchor",
            "coefficient_symbol": "epsilon_axial_torsion_spin",
            "observable": "KRT2008_axial_torsion_component",
            "product_symbol": "abs(b_eff^I)",
            "bound_value": "source_anchor_present_but_component_table_missing",
            "bound_units": "GeV",
            "source": str(SOURCES["axial_values_2116"]["path"]),
            "score_status": "ANCHOR_RETAINED_NOT_SCORE",
            "valid_for_claim": "False",
        }
    )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3494_0_spin_conditional_zero",
            "requirement": "coframe-owned spin connection gives Delta_spin=0 by variable absence",
            "passed": "True",
            "evidence": "SPIN2348_1/2 and SOG2115_3 exact conditional theorem",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3494_1_candidate_branch_exists",
            "requirement": "owned-coframe spin branch has explicit candidate variable list and zero values",
            "passed": "True",
            "evidence": "PSS2116 candidate action and ACV2116 zero rows",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3494_2_global_parent_signature",
            "requirement": "ordinary matter + spin object language is parent-signed for all local sectors",
            "passed": "False",
            "evidence": "ordinary matter signature audits 2647/3084/1412 remain unsigned",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3494_3_counterbranch_excluded",
            "requirement": "independent torsionful spin connection / Einstein-Cartan branch is forbidden by parent ontology",
            "passed": "False",
            "evidence": "SPIN2348_4 and SOG2115_5 retain counterbranch",
            "blocks_claim": "True",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3494_4_axial_kernel_sharpened",
            "requirement": "epsilon_axial_torsion_spin has an explicit component/kernel chain and inherited bounds",
            "passed": "True",
            "evidence": "AXK3494 rows plus inherited WEP/PPN/KRT anchor rows",
            "blocks_claim": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3494_0_branch_result",
            "decision": "Treat owned-coframe spin as a real conditional theorem-zero branch, not a claim.",
            "rationale": "The math is exact once the action arguments are signed, but the public parent signature is still missing.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3494_1_global_result",
            "decision": "Do not retire epsilon_axial_torsion_spin globally.",
            "rationale": "Independent torsionful spin connection remains a legal counterbranch until explicitly forbidden or bounded.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3494_2_progress",
            "decision": "Promote epsilon_axial_torsion_spin to the first sharpened P4 tail.",
            "rationale": "It now has a component chain from C_MTS to torsion to axial projection to KRT/PPN/WEP comparators.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3495-Y5-R2FR-source-readout-boundary-gamma-current-zero-or-P4-tail-priority.md",
            "next_script": "scripts/Y5_R2FR_3495_source_readout_boundary_gamma_current_zero_or_P4_tail_priority.py",
            "objective": "Attack the remaining source/readout/boundary Gamma-current leaks after the owned-coframe spin fork; either derive q/e_obs descent or prioritize the next P4 tail to source.",
            "success_gate": "source/readout/boundary connection-current theorem-zero, or prioritized P4 tail queue with sharpened kernels for hypermomentum/projective/Weyl/shear",
            "forbidden_shortcuts": "using the private spin zero branch to claim all-sector LC; ignoring boundary/source support commutators; replacing source/readout proof with GR geodesic assumptions",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    outputs: dict[str, Path],
    kernels: list[dict[str, Any]],
    inherited_bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "check_id": "VAL3494_0_sources_exist",
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
            "check_id": "VAL3494_1_csv_parse",
            "passed": parse_ok,
            "detail": "; ".join(details),
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3494_2_kernel_chain_complete",
            "passed": len(kernels) >= 6,
            "detail": f"kernels={len(kernels)}",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3494_3_inherited_bounds_present",
            "passed": len(inherited_bounds) >= 6,
            "detail": f"inherited_bounds={len(inherited_bounds)}",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3494_4_parent_claim_blocked",
            "passed": any(row["passed"] == "False" and row["blocks_claim"] == "True" for row in gates),
            "detail": "global spin/ordinary matter claim remains blocked",
            "valid_for_claim": "False",
        }
    )
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append(
        {
            "check_id": "VAL3494_5_no_claim",
            "passed": all(row.get("valid_for_claim") == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3494_6_no_formalization_outputs",
            "passed": all(FORMALIZATION not in path.parents for path in outputs.values()),
            "detail": "outputs are under post-checkpoint-work/source-intake only",
            "valid_for_claim": "False",
        }
    )
    passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append(
        {
            "check_id": "VAL3494_SUMMARY",
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
    attempts: list[dict[str, Any]],
    forks: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3494: Ordinary Matter Coframe-Owned Spin Proof Or Axial Torsion Tail",
                "",
                "## Current Verdict",
                "- **Real theorem:** if ordinary spin uses only `omega_LC[e_obs]`, then independent spin hypermomentum is zero by variable absence.",
                "- **Branch status:** the owned-coframe candidate branch gives `xi_A=0` and `A_MTS=0`, but this is not globally parent-signed.",
                "- **Counterbranch retained:** an independent torsionful spin connection can source axial torsion, so `epsilon_axial_torsion_spin` cannot be retired globally.",
                "- **Concrete progress:** the axial tail now has a sharper kernel chain from `C_MTS` to torsion to axial projection to KRT/PPN/WEP interfaces.",
                "- **No claim:** no local-GR, LC, WEP, PPN, or spin-torsion pass is claimed.",
                "",
                "## Theorem Attempt",
                md_table(attempts, ["attempt_id", "statement", "derivation", "result", "valid_for_claim"]),
                "",
                "## Fork Ledger",
                md_table(forks, ["fork_id", "branch", "premises", "result", "claim_status", "fallback_needed", "valid_for_claim"]),
                "",
                "## Axial Kernel Interface",
                md_table(kernels, ["kernel_id", "quantity", "formula", "units", "status", "missing_for_score", "valid_for_claim"]),
                "",
                "## Inherited Bounds",
                md_table(bounds, ["inherit_id", "bound_family", "observable", "product_symbol", "bound_value", "bound_units", "score_status", "valid_for_claim"]),
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
    attempts = theorem_attempt_rows()
    forks = fork_rows()
    kernels = axial_kernel_rows()
    bounds = inherited_bound_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3494_SOURCE_REGISTER.csv",
        "theorem_attempts": OUT / "P8_Y5_R2FR_3494_COFRAME_SPIN_THEOREM_ATTEMPT.csv",
        "forks": OUT / "P8_Y5_R2FR_3494_SPIN_FORK_LEDGER.csv",
        "kernels": OUT / "P8_Y5_R2FR_3494_AXIAL_TORSION_KERNEL_INTERFACE.csv",
        "bounds": OUT / "P8_Y5_R2FR_3494_AXIAL_BOUND_INHERITANCE.csv",
        "gates": OUT / "P8_Y5_R2FR_3494_GATES.csv",
        "decisions": OUT / "P8_Y5_R2FR_3494_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3494_NEXT_TARGET.csv",
    }
    write_csv(outputs["source_register"], source_register(), ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["theorem_attempts"], attempts, ["attempt_id", "statement", "derivation", "result", "source_path", "valid_for_claim"])
    write_csv(outputs["forks"], forks, ["fork_id", "branch", "premises", "result", "claim_status", "fallback_needed", "valid_for_claim"])
    write_csv(outputs["kernels"], kernels, ["kernel_id", "quantity", "formula", "units", "status", "missing_for_score", "source_path", "valid_for_claim"])
    write_csv(outputs["bounds"], bounds, ["inherit_id", "bound_family", "coefficient_symbol", "observable", "product_symbol", "bound_value", "bound_units", "source", "score_status", "valid_for_claim"])
    write_csv(outputs["gates"], gates, ["gate_id", "requirement", "passed", "evidence", "blocks_claim", "valid_for_claim"])
    write_csv(outputs["decisions"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, kernels, bounds, gates)
    validation_path = OUT / "P8_Y5_BRR545_3494_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(attempts, forks, kernels, bounds, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
