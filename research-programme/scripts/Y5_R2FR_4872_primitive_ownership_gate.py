from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from Y5_R2FR_4872_covariance_flow_ownership import ownership_result


CHECKPOINT = "4872"
TIMESTAMP = "2026-07-10T19:05:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = (
    "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-"
    "kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def stamp(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["timestamp_utc"] = TIMESTAMP
    return rows


def source_rows() -> list[dict[str, Any]]:
    sources = [
        (
            "SRC4872_00_core_action",
            ROOT / "core-mts-framework" / "action-principle"
            / "the-fundamental-action-of-motion-timespace-field-theory.md",
            "A_MTS",
            "printed primitive action",
        ),
        (
            "SRC4872_01_core_eft",
            ROOT / "core-mts-framework" / "field-theory"
            / "the-effective-field-theory-of-motion-timespace.md",
            "A_eff[g]",
            "printed coarse-graining claim",
        ),
        (
            "SRC4872_02_AMF",
            POST / "4562-Y5-R2FR-A-MF-parent-origin-from-motion-time-space-or-effective-axiom-freeze.md",
            "CURRENT_CORPUS_FAILS_PARENT_ORIGIN_FREEZE_AS_AXIOM",
            "prior frame-origin gate",
        ),
        (
            "SRC4872_03_flow",
            POST / "4857-Y5-R2FR-parent-time-coframe-kinetic-owner-or-PPN-safe-coefficient-surface-and-mode-stability-gate.md",
            "PARENT_TIME_FLOW_KINETIC_STABILITY_4857",
            "unit-flow action",
        ),
        (
            "SRC4872_04_public",
            POST / "4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md",
            "PUBLIC_FRAME_VARIATION_SELECTION_4861",
            "public metric and source chain",
        ),
        (
            "SRC4872_05_prior",
            POST / "4871-Y5-R2FR-v3-l1-asymptotic-kappa4-crosscheck-and-full-first-order-C3-arbitration.md",
            "V3_L1_SURFACE_KAPPA4_AND_C3_ARBITRATION_4871",
            "prior checkpoint",
        ),
        (
            "SRC4872_06_checkpoint",
            POST / "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md",
            "PRIMITIVE_COVARIANCE_SIGN_AND_FLOW_RANK_THEOREM_4872",
            "human derivation",
        ),
        (
            "SRC4872_07_formal",
            FORMAL / "888-PPC4161-primitive-covariance-metric-and-composite-flow-ownership.md",
            "PPC4161_PRIMITIVE_COVARIANCE_FLOW_OWNERSHIP_4872",
            "formal integration",
        ),
        ("SRC4872_08_claim", FORMAL / "02-claims-register.csv", "L-714", "claim register"),
        (
            "SRC4872_09_variable",
            FORMAL / "04-variable-audit.csv",
            "constructed_sign_corrected_public_metric_candidate_measure_open",
            "variable audit",
        ),
        (
            "SRC4872_10_equation",
            FORMAL / "05-equation-register.md",
            "1.165 Primitive covariance sign",
            "equation register",
        ),
        (
            "SRC4872_11_redteam",
            FORMAL / "06-consistency-red-team.md",
            "116. Primitive covariance and flow-ownership red team",
            "red-team register",
        ),
        (
            "SRC4872_12_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4872",
            "unification spine",
        ),
        (
            "SRC4872_13_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "Last checkpoint: " + chr(96) + "4872-",
            "resume marker",
        ),
        (
            "SRC4872_14_math",
            POST / "scripts" / "Y5_R2FR_4872_covariance_flow_ownership.py",
            "def ownership_result",
            "symbolic derivation",
        ),
        (
            "SRC4872_15_generator",
            Path(__file__).resolve(),
            'CHECKPOINT = "4872"',
            "generator",
        ),
        (
            "SRC4872_16_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4871_VALIDATION.csv",
            "VAL4871_OVERALL",
            "historical validation",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in sources:
        content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_locator": str(path),
                "needle": needle,
                "source_exists": path.exists(),
                "needle_found": needle in content,
                "role": role,
                "source_validated": path.exists() and needle in content,
            }
        )
    return stamp(rows)


def primitive_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    damping = data["sections"]["damping"]
    metric = data["sections"]["metric_maps"]
    return stamp(
        [
            {
                "audit_id": "PA4872_0",
                "object": "printed gamma psi partial_t psi",
                "status": "REJECT_BULK_PARENT",
                "derived_result": damping["boundary_form"],
                "issue": "Euler derivative=" + damping["euler_derivative"],
                "next_action": "construct doubled/open parent",
            },
            {
                "audit_id": "PA4872_1",
                "object": "signed real potential",
                "status": "CORRECT_SIGN_BRANCH",
                "derived_result": "lambda sgn(psi)|psi|^(n-1)",
                "issue": "core expression omits sign for negative psi",
                "next_action": "choose ontology and domain",
            },
            {
                "audit_id": "PA4872_2",
                "object": "legacy covariant rank-one metric",
                "status": "REJECT_SELECTED_P_POSITIVE",
                "derived_result": metric["core_covariant_rank_one_p"],
                "issue": metric["core_branch_sign_for_0_le_q_lt_1"],
                "next_action": "use inverse connected covariance",
            },
            {
                "audit_id": "PA4872_3",
                "object": "fixed eta and explicit partial_t",
                "status": "OPEN_BACKGROUND_DESCENT",
                "derived_result": "background remains separately present",
                "issue": "not a primitive diffeomorphism theorem",
                "next_action": "derive eta-decoupling quotient",
            },
        ]
    )


def metric_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    metric = data["sections"]["metric_maps"]
    coframe = data["sections"]["coframe"]
    return stamp(
        [
            {
                "map_id": "CM4872_0",
                "map_or_clause": "connected normalized C^munu",
                "status": "CONSTRUCTED_CANDIDATE",
                "result": "centering and ell_star explicit",
                "remaining_gate": "state and W_ell open",
            },
            {
                "map_id": "CM4872_1",
                "map_or_clause": metric["inverse_covariance_branch"],
                "status": "PASS_EXACT",
                "result": "p=q>=0",
                "remaining_gate": "full covariance spectrum",
            },
            {
                "map_id": "CM4872_2",
                "map_or_clause": "inverse and determinant",
                "status": "PASS_EXACT",
                "result": metric["public_determinant_ratio"],
                "remaining_gate": metric["lorentzian_gate"],
            },
            {
                "map_id": "CM4872_3",
                "map_or_clause": coframe["metric_factorization"],
                "status": "PASS_LOCAL_LORENTZ_REDUNDANCY",
                "result": coframe["redundancy"],
                "remaining_gate": "no translation theorem claimed",
            },
            {
                "map_id": "CM4872_4",
                "map_or_clause": "Gamma_IR has no separate eta or W_ell",
                "status": "OPEN_DYNAMICAL_GATE",
                "result": "required for public diffeomorphism invariance",
                "remaining_gate": "not in printed scalar action",
            },
        ]
    )


def flow_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    rank_one = data["sections"]["rank_one"]
    multimode = data["sections"]["multimode"]
    return stamp(
        [
            {
                "flow_id": "FR4872_0",
                "construction": "timelike Landau eigenflow",
                "status": "CONSTRUCTED_CONDITIONAL",
                "derived_result": "covariant composite unit vector",
                "gate": "simple eigenvalue and spectral gap",
            },
            {
                "flow_id": "FR4872_1",
                "construction": rank_one["flow"],
                "status": "NO_GO_SPIN1",
                "derived_result": "u wedge du=" + rank_one["frobenius_component"],
                "gate": "vorticity identically zero",
            },
            {
                "flow_id": "FR4872_2",
                "construction": multimode["realizations"],
                "status": "EXISTENCE_PASS",
                "derived_result": multimode["vorticity_Oepsilon"],
                "gate": "actual MTS ensemble open",
            },
            {
                "flow_id": "FR4872_3",
                "construction": "selected c_omega=D>0",
                "status": "REQUIRES_MULTIMODE",
                "derived_result": "incompatible with u=N dpsi",
                "gate": "derive covariance response",
            },
        ]
    )


def matching_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    surface = data["sections"]["public_surface"]
    ratios = "; ".join(
        f"{key}={value}" for key, value in surface["small_p_ratios"].items()
    )
    return stamp(
        [
            {
                "matching_id": "EM4872_0",
                "statement": "EH plus four two-derivative unit-flow operators",
                "status": "DERIVED_CONDITIONAL",
                "premise_or_evidence": "gHat,u,locality,diffeomorphism,parity",
                "remaining_gate": "coefficients not fixed",
            },
            {
                "matching_id": "EM4872_1",
                "statement": "cI=-Mstar^-2 d2 Gamma_micro[B_I]/d epsilon2",
                "status": "DEFINITION_DERIVED",
                "premise_or_evidence": "four projected calibration backgrounds",
                "remaining_gate": "Gamma_micro unevaluated",
            },
            {
                "matching_id": "EM4872_2",
                "statement": "c_i=p cbar_i+O(p2)",
                "status": "DERIVED_ANALYTIC_DECOUPLING",
                "premise_or_evidence": "V=sqrt(p)u regular",
                "remaining_gate": "analyticity premise",
            },
            {
                "matching_id": "EM4872_3",
                "statement": ratios,
                "status": "CORRESPONDENCE_EFT_MATCH",
                "premise_or_evidence": "selected public safe surface",
                "remaining_gate": "r not primitive",
            },
            {
                "matching_id": "EM4872_4",
                "statement": f"alpha1={surface['alpha1']}; alpha2={surface['alpha2']}",
                "status": "PASS_IDENTITY",
                "premise_or_evidence": "checkpoint-4861 surface",
                "remaining_gate": "absolute p empirical",
            },
            {
                "matching_id": "EM4872_5",
                "statement": "Gcos/GN=" + surface["Gcos_over_GN"],
                "status": "PASS_IDENTITY",
                "premise_or_evidence": "checkpoint-4861 surface",
                "remaining_gate": "Mstar open",
            },
        ]
    )


def source_descent_rows() -> list[dict[str, Any]]:
    return stamp(
        [
            {
                "descent_id": "SD4872_0",
                "statement": "S_int[psi,Psi,A]=S_matter[gHat(psi),Psi,A]",
                "status": "CONDITIONAL_PREMISE_UNSIGNED",
                "meaning": "one public metric and no direct species u charge",
            },
            {
                "descent_id": "SD4872_1",
                "statement": "one public Hilbert variation",
                "status": "DERIVED_FROM_PREMISE",
                "meaning": "one source tensor for all matter",
            },
            {
                "descent_id": "SD4872_2",
                "statement": "nablaHat_mu THat^munu=0",
                "status": "DERIVED_WARD_IDENTITY",
                "meaning": "on matter shell",
            },
            {
                "descent_id": "SD4872_3",
                "statement": "J_u_perp=p h THat u/sqrt(1-p)",
                "status": "DERIVED_CHAIN_RULE",
                "meaning": "universal momentum-flux source",
            },
            {
                "descent_id": "SD4872_4",
                "statement": "EM flow source is Poynting projection",
                "status": "DERIVED_EM_COMPONENT",
                "meaning": "not an independent coupling",
            },
        ]
    )


def limit_rows() -> list[dict[str, Any]]:
    return stamp(
        [
            {
                "limit_id": "LG4872_0",
                "premise": "p->0; c_i->0; finite gap; universal descent",
                "status": "CONDITIONAL_GR_LIMIT",
                "derived_limit": "EH plus common matter action",
                "remaining_gate": "Mstar, gap and descent",
            },
            {
                "limit_id": "LG4872_1",
                "premise": "weak static public metric",
                "status": "CONDITIONAL_NEWTON_LIMIT",
                "derived_limit": "GN=[8pi Mstar2(1-c14/2)]^-1",
                "remaining_gate": "core gamma and lambda already contain G",
            },
            {
                "limit_id": "LG4872_2",
                "premise": "local parity-even U1 action on gHat",
                "status": "CONDITIONAL_MAXWELL_LIMIT",
                "derived_limit": "F_mn F^mn plus current",
                "remaining_gate": "charge and A_mu origin",
            },
            {
                "limit_id": "LG4872_3",
                "premise": "primitive unified local limit",
                "status": "BLOCKED",
                "derived_limit": "correspondence EFT retained",
                "remaining_gate": "open parent, Kubo and source quotient",
            },
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "printed damping action", "REJECT_BULK_PARENT", "Euler derivative zero"),
        (2, "legacy covariant metric", "REJECT_SELECTED_BRANCH", "positive q maps to p<=0"),
        (3, "inverse connected covariance", "SELECT_CANDIDATE", "q maps to p>=0"),
        (4, "single-gradient flow", "REJECT_SPIN1_OWNER", "Frobenius zero"),
        (5, "multimode eigenflow", "SELECT_ROUTE", "explicit nonzero curl"),
        (6, "unit-flow basis", "RETAIN_DERIVED_CONDITIONAL", "complete IR basis"),
        (7, "exact coefficient ratios", "DEMOTE_EFT_MATCHING", "Kubo open"),
        (8, "universal source", "CONDITIONAL_QUOTIENT", "premise unsigned"),
        (9, "4857-4871", "RETAIN_CORRESPONDENCE_TESTS", "internal math survives"),
        (10, "next target", "OPEN_PARENT_AND_KUBO", NEXT_TARGET),
    ]
    return stamp(
        [
            {
                "priority": priority,
                "target": target,
                "decision": decision,
                "reason": reason,
            }
            for priority, target, decision, reason in entries
        ]
    )


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "R_open_parent", "OPEN_ROOT", "construct covariant variational damping"),
        (2, "R_smoothing", "OPEN_ROOT", "define W_ell, state and ell_star"),
        (3, "R_eta_descent", "OPEN_ROOT", "remove observable background"),
        (4, "R_flow_gap", "OPEN_ROOT", "derive timelike spectral gap"),
        (5, "R_Mstar", "OPEN_ROOT", "calculate EH response without input G"),
        (6, "R_cI", "OPEN_ROOT", "evaluate four Kubo coefficients"),
        (7, "R_ratio", "OPEN_DECISION", "compare with p,r surface"),
        (8, "R_source", "OPEN_ROOT", "derive universal matter quotient"),
        (9, "R_correspondence", "RETAIN_EFFECTIVE", "use prior regressions"),
        (10, "R_local_GR", "BLOCKED", "no primitive claim"),
    ]
    return stamp(
        [
            {
                "priority": priority,
                "residual": residual,
                "status": status,
                "next_action": action,
            }
            for priority, residual, status, action in entries
        ]
    )


def validation_rows(
    sources: list[dict[str, Any]],
    groups: list[list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    data = ownership_result()
    sections = data["sections"]
    claims = [
        row for row in read_csv(FORMAL / "02-claims-register.csv")
        if row.get("claim_id") == "L-714"
    ]
    variables = {
        row.get("symbol"): row
        for row in read_csv(FORMAL / "04-variable-audit.csv")
        if row.get("symbol") in {
            "C_connected_inverse_MTS",
            "u_Landau_MTS",
            "c1_c2_c3_c4_parent",
        }
    }
    checkpoint = (
        POST / "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md"
    ).read_text(encoding="utf-8")
    formal = (
        FORMAL / "888-PPC4161-primitive-covariance-metric-and-composite-flow-ownership.md"
    ).read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior = read_csv(OUTPUT / "P8_Y5_BRR545_4871_VALIDATION.csv")
    output_paths = [
        OUTPUT / name
        for name in (
            "P8_Y5_R2FR_4872_SOURCE_REGISTER.csv",
            "P8_Y5_R2FR_4872_PRIMITIVE_ACTION_AUDIT.csv",
            "P8_Y5_R2FR_4872_COVARIANCE_METRIC_MAP.csv",
            "P8_Y5_R2FR_4872_FLOW_RANK_GATE.csv",
            "P8_Y5_R2FR_4872_EFT_MATCHING.csv",
            "P8_Y5_R2FR_4872_SOURCE_DESCENT.csv",
            "P8_Y5_R2FR_4872_LIMIT_GATE.csv",
            "P8_Y5_R2FR_4872_BRANCH_DECISION.csv",
            "P8_Y5_R2FR_4872_RESIDUAL_REBASE.csv",
        )
    ]

    def check(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    checks = [
        check("VAL4872_00_symbolic", data["all_symbolic_checks_pass"], "six symbolic groups"),
        check("VAL4872_01_damping", sections["damping"]["euler_derivative"] == "0", "boundary term"),
        check("VAL4872_02_metric", sections["metric_maps"]["passed"], "inverse and determinant"),
        check("VAL4872_03_coframe", sections["coframe"]["passed"], "local Lorentz"),
        check("VAL4872_04_rank", sections["rank_one"]["passed"] and not sections["rank_one"]["spin1_mode_owned"], "single-gradient no-go"),
        check("VAL4872_05_multimode", sections["multimode"]["passed"], "nonzero curl example"),
        check("VAL4872_06_surface", sections["public_surface"]["passed"], "PPN and G ratios"),
        check("VAL4872_07_sources", len(sources) == 17 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        check("VAL4872_08_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows private"),
        check("VAL4872_09_csv", all(path.exists() and all(None not in row for row in read_csv(path)) for path in output_paths), "nine CSVs parse"),
        check("VAL4872_10_claim", len(claims) == 1 and claims[0].get("status") == "primitive_scalar_damping_and_rank_one_sign_no_gos_derived_inverse_covariance_multimode_flow_candidate_constructed_correspondence_demoted_private_nonclaim", "L-714"),
        check("VAL4872_11_variables", variables.get("C_connected_inverse_MTS", {}).get("status") == "constructed_sign_corrected_public_metric_candidate_measure_open" and variables.get("u_Landau_MTS", {}).get("status") == "composite_flow_candidate_rank_one_no_go_multimode_existence_derived" and variables.get("c1_c2_c3_c4_parent", {}).get("status") == "operator_basis_and_O_p_scaling_derived_exact_ratios_EFT_matched_primitive_Kubo_open", "variable statuses"),
        check("VAL4872_12_documents", "PRIMITIVE_COVARIANCE_SIGN_AND_FLOW_RANK_THEOREM_4872" in checkpoint and "PPC4161_PRIMITIVE_COVARIANCE_FLOW_OWNERSHIP_4872" in formal, "document markers"),
        check("VAL4872_13_registers", "1.165 Primitive covariance sign" in (FORMAL / "05-equation-register.md").read_text(encoding="utf-8") and "116. Primitive covariance and flow-ownership red team" in (FORMAL / "06-consistency-red-team.md").read_text(encoding="utf-8") and "PPC4161 checkpoint 4872" in (FORMAL / "07-unification-spine.md").read_text(encoding="utf-8"), "formal registers"),
        check("VAL4872_14_resume", ("Last checkpoint: " + chr(96) + "4872-") in resume and NEXT_TARGET in resume, "resume handoff"),
        check("VAL4872_15_prior", prior[-1].get("status") == "PASS", "4871 green"),
        check("VAL4872_16_scripts", compiles(Path(__file__).resolve()) and compiles(POST / "scripts" / "Y5_R2FR_4872_covariance_flow_ownership.py"), "scripts compile"),
        check("VAL4872_17_pycache", not (POST / "scripts" / "__pycache__").exists(), "no pycache"),
    ]
    checks.append(
        check(
            "VAL4872_OVERALL",
            all(row["status"] == "PASS" for row in checks),
            "PRIMITIVE_COVARIANCE_FLOW_OWNERSHIP_4872_VALIDATED",
        )
    )
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    data = ownership_result()
    sources = source_rows()
    tables = [
        (OUTPUT / "P8_Y5_R2FR_4872_SOURCE_REGISTER.csv", sources),
        (OUTPUT / "P8_Y5_R2FR_4872_PRIMITIVE_ACTION_AUDIT.csv", primitive_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4872_COVARIANCE_METRIC_MAP.csv", metric_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4872_FLOW_RANK_GATE.csv", flow_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4872_EFT_MATCHING.csv", matching_rows(data)),
        (OUTPUT / "P8_Y5_R2FR_4872_SOURCE_DESCENT.csv", source_descent_rows()),
        (OUTPUT / "P8_Y5_R2FR_4872_LIMIT_GATE.csv", limit_rows()),
        (OUTPUT / "P8_Y5_R2FR_4872_BRANCH_DECISION.csv", decision_rows()),
        (OUTPUT / "P8_Y5_R2FR_4872_RESIDUAL_REBASE.csv", residual_rows()),
    ]
    for path, rows in tables:
        write_csv(path, rows)
    groups = [rows for _, rows in tables]
    validation = validation_rows(sources, groups)
    write_csv(OUTPUT / "P8_Y5_BRR545_4872_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print(
        "P8_Y5_BRR545_4872_VALIDATION_PASS"
        if passed
        else "P8_Y5_BRR545_4872_VALIDATION_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

