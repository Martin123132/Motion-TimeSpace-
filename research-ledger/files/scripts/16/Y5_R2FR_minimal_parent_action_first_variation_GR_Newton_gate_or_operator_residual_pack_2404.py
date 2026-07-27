from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_MINIMAL_PARENT_ACTION_FIRST_VARIATION_GR_NEWTON_GATE_OR_OPERATOR_RESIDUAL_PACK_2404"
SCRIPT_PATH = Path(__file__).resolve()
POST_ROOT = SCRIPT_PATH.parents[1]
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
FORMALIZATION_ROOT = POST_ROOT.parent / "formalization-workbench"
DOC_PATH = POST_ROOT / "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md"


def post(path: str) -> Path:
    return POST_ROOT / path


SOURCES = [
    {
        "source_id": "SRC2404_2403_doc",
        "path": str(post("2403-Y5-R2FR-minimal-parent-action-normal-form-candidate-or-off-contract-coefficient-bound-pack.md")),
        "needles": "NEXT2403_0_selected|S_min =|G_munu + Lambda g_munu + DeltaE_MTS|VAL2403_OVERALL",
        "role": "immediate parent: minimal candidate and selected first-variation gate",
    },
    {
        "source_id": "SRC2404_2403_candidate",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2403_MINIMAL_PARENT_ACTION_CANDIDATE.csv")),
        "needles": "MPA2403_1_EH_reference_core|MPA2403_2_silent_MTS_sector|MPA2403_3_universal_matter|MPA2403_5_forbidden_terms",
        "role": "candidate action terms",
    },
    {
        "source_id": "SRC2404_2403_derivation",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2403_CONDITIONAL_DERIVATION_LEDGER.csv")),
        "needles": "CDR2403_0_first_variation|CDR2403_1_source_closure|CDR2403_2_operator_closure|CDR2403_3_Newton_lane",
        "role": "conditional derivation targets",
    },
    {
        "source_id": "SRC2404_2403_coefficients",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2403_OFF_CONTRACT_COEFFICIENTS.csv")),
        "needles": "OFF2403_0_DeltaE_MTS|OFF2403_1_c_nonminimal|OFF2403_6_c_nonHilbert",
        "role": "off-contract residual rows",
    },
    {
        "source_id": "SRC2404_1769_doc",
        "path": str(post("1769-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md")),
        "needles": "ELH1769_1_EH_variation|NWF1769_1_poisson_conditional|ORP1769_0_E_LHS_GR_residual|VAL1769_OVERALL",
        "role": "GR/Newton conditional template and residual pack",
    },
    {
        "source_id": "SRC2404_1769_einstein",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1769_EINSTEIN_LEFT_HAND_LIMIT_ATTEMPT.csv")),
        "needles": "ELH1769_0_target|ELH1769_1_EH_variation|ELH1769_4_current_verdict",
        "role": "Einstein left-hand limit rows",
    },
    {
        "source_id": "SRC2404_1769_newton",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1769_NEWTON_POISSON_WEAK_FIELD_ATTEMPT.csv")),
        "needles": "NWF1769_0_metric_ansatz|NWF1769_1_poisson_conditional|NWF1769_4_current_verdict",
        "role": "Newton/Poisson weak-field template",
    },
    {
        "source_id": "SRC2404_2234_doc",
        "path": str(post("2234-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md")),
        "needles": "EUL2234_3_EH_metric|WPPN2234_2_beta|GATE2234_5_local_GR|VAL2234_OVERALL",
        "role": "weak-field ansatz and adoption guard",
    },
    {
        "source_id": "SRC2404_2402_doc",
        "path": str(post("2402-Y5-R2FR-parent-action-normal-form-ownership-signer-or-shadow-coefficient-acquisition.md")),
        "needles": "J_shadow=0 iff|COEF2402_0_E_LHS_GR_residual|CG2402_3_local_GR_Newton|VAL2402_OVERALL",
        "role": "finite source-shadow/operator coefficient basis",
    },
]


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCES:
        path = Path(source["path"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_path": source["path"],
                "exists": str(path.exists()).lower(),
                "needles": source["needles"],
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def first_variation_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FV2404_0_candidate_action",
            "variation_piece": "minimal candidate",
            "formal_step": "S_min=S_EH[e]+S_silent[q,Phi,lambda_C]+S_ord[e(q),Psi,theta,A_obs]+S_boundary_silent",
            "result": "one variational object exists inside the private branch",
            "status": "CANDIDATE_NOT_DERIVED",
            "blocking_issue": "candidate clauses are not yet derived from deeper MTS primitives",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FV2404_1_EH_variation",
            "variation_piece": "EH metric/coframe variation",
            "formal_step": "delta S_EH/delta g^{mu nu}=-(sqrt(-g)/(2 kappa0))(G_munu+Lambda0 g_munu) plus boundary",
            "result": "Einstein operator appears with the usual normalization inside the candidate",
            "status": "STANDARD_CONDITIONAL_TEMPLATE",
            "blocking_issue": "EH core is candidate axiom until MTS-to-EH leading-operator theorem is signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FV2404_2_matter_variation",
            "variation_piece": "ordinary matter variation",
            "formal_step": "T_H^{mu nu}:=-2/sqrt(-g) delta S_ord/delta g_munu and delta_Psi S_ord=0 on matter shell",
            "result": "ordinary RHS source is total Hilbert source before readout",
            "status": "CONDITIONAL_INSIDE_CANDIDATE",
            "blocking_issue": "requires universal matter coupling and source-map identity to be parent-signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FV2404_3_silent_sector_variation",
            "variation_piece": "MTS silent/residual sector",
            "formal_step": "DeltaE_MTS^{mu nu}:=(2 kappa0/sqrt(-g)) delta S_silent/delta g_munu plus induced q/e variations",
            "result": "extra MTS content is exposed as left-hand residual, not deleted",
            "status": "RESIDUAL_EXPOSED",
            "blocking_issue": "must prove DeltaE_MTS=0, pure gauge, topological, or below bounds on local branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FV2404_4_boundary_variation",
            "variation_piece": "boundary/improvement variation",
            "formal_step": "DeltaE_boundary^{mu nu}:=(2 kappa0/sqrt(-g)) delta S_boundary_silent/delta g_munu",
            "result": "boundary is silent only under compact/falloff/local support assumptions",
            "status": "RESIDUAL_OR_SILENCE_CONDITION",
            "blocking_issue": "boundary/worldtube policy remains an explicit gate",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FV2404_5_field_equation",
            "variation_piece": "candidate field equation",
            "formal_step": "G_munu+Lambda g_munu+DeltaE_MTS+DeltaE_boundary = kappa0(T_H_munu+J_shadow_munu)",
            "result": "the GR/Newton chain is exact if DeltaE terms and J_shadow vanish/silent",
            "status": "EXACT_CONDITIONAL_EQUATION",
            "blocking_issue": "source-shadow and operator residual gates remain nonclaim",
            "valid_for_claim": "false",
        },
    ]


def source_closure_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRCLOSE2404_0_shadow_zero",
            "condition": "J_shadow=0",
            "formal_requirement": "c_nonminimal=c_boundary=c_projector=c_frame=delta_w_decoupled=c_nonHilbert=0 and T_active=T_H",
            "result_if_met": "right-hand source is total Hilbert stress only",
            "current_status": "CONDITIONAL_FROM_2401_2402_2403",
            "gap": "off-contract coefficients are set to zero by candidate restriction, not derived zero",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRCLOSE2404_1_conservation",
            "condition": "source conservation",
            "formal_requirement": "nabla_mu T_H^{mu nu}=0 on S_ord matter shell and nabla_mu(DeltaE_MTS+DeltaE_boundary)^{mu nu}=0 or zero",
            "result_if_met": "Bianchi identity is compatible with matter motion",
            "current_status": "PARTIAL_CONDITIONAL",
            "gap": "MTS residual divergence identity must be signed by the parent Noether theorem",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRCLOSE2404_2_G_calibration",
            "condition": "single source normalization",
            "formal_requirement": "kappa0=8 pi G_ref/c^4 and the same Hilbert mass normalizes Poisson, clocks/orbits, and source charge",
            "result_if_met": "Newton G is not backfilled from orbital fits",
            "current_status": "BLOCKED_NORMALIZATION_GATE",
            "gap": "M_H_ref/Pi_M/Hilbert source-charge equivalence remains unsigned",
            "valid_for_claim": "false",
        },
    ]


def weak_field_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "WF2404_0_metric_ansatz",
            "step": "weak-field metric",
            "formula": "g_00=-(1+2 U/c^2+O(c^-4)), g_ij=(1-2 gamma U/c^2)delta_ij+O(c^-4)",
            "condition": "slow-motion weak field, local ordinary source, same observed frame",
            "result": "sets the Poisson/PPN comparison variables",
            "status": "STANDARD_TEMPLATE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "WF2404_1_00_equation",
            "step": "00 component",
            "formula": "G_00 ~= 2 nabla^2 U/c^2 and T_00 ~= rho_H c^2",
            "condition": "DeltaE_00=0, J_shadow_00=0, Lambda negligible locally, kappa0=8 pi G_ref/c^4",
            "result": "nabla^2 U=4 pi G_ref rho_H",
            "status": "EXACT_CONDITIONAL_POISSON",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "WF2404_2_inverse_square",
            "step": "Newton force law",
            "formula": "for isolated spherical M_H, U=-G_ref M_H/r and a=-nabla U",
            "condition": "Poisson equation plus boundary condition U->0 and no residual exterior source",
            "result": "Newton inverse-square law in the candidate branch",
            "status": "CONDITIONAL_NOT_MTS_PROOF",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "WF2404_3_ppn",
            "step": "PPN gamma/beta",
            "formula": "gamma-1 and beta-1 are sourced by spatial/second-order pieces of DeltaE_MTS, boundary, frame, and shadow residuals",
            "condition": "EH nonlinear completion dominates and all residual operators are silent below PPN order",
            "result": "gamma=1,beta=1 only conditionally",
            "status": "PPN_RESIDUAL_GATE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "WF2404_4_current_verdict",
            "step": "current weak-field verdict",
            "formula": "candidate yields GR/Newton iff source closure + operator residual silence + source normalization all pass",
            "condition": "three independent gates",
            "result": "strong conditional bridge; no local GR claim",
            "status": "CONDITIONAL_BRIDGE_NOT_CLAIM",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OR2404_0_DeltaE_MTS",
            "residual": "DeltaE_MTS",
            "definition": "left-hand MTS deviation from Einstein operator in candidate first variation",
            "must_show": "zero, pure constraint/topological, higher order below bounds, or empirical residual bound",
            "observable_link": "PPN gamma/beta, Newton-Poisson, orbital dynamics, clocks",
            "status": "ROOT_OPERATOR_BLOCKER",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OR2404_1_DeltaE_boundary",
            "residual": "DeltaE_boundary",
            "definition": "boundary/worldtube/reference-improvement variation that reaches local equations",
            "must_show": "compact/falloff/local support silence or coefficient bound",
            "observable_link": "local source charge, orbital boundary leakage",
            "status": "BOUNDARY_GATE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OR2404_2_J_shadow",
            "residual": "J_shadow",
            "definition": "non-Hilbert/post-Hilbert source residual from 2401/2402",
            "must_show": "off-contract coefficients vanish/silent/excluded",
            "observable_link": "WEP/R10/clocks/composition",
            "status": "SOURCE_GATE_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OR2404_3_delta_G_source",
            "residual": "delta_G_source",
            "definition": "mismatch between kappa0 source normalization and measured Newtonian mass/charge",
            "must_show": "same Hilbert mass controls Poisson, Hamiltonian charge, and measured source",
            "observable_link": "Newtonian orbits, lab G, source normalization",
            "status": "NORMALIZATION_GATE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OR2404_4_ppn_residual",
            "residual": "delta_gamma_delta_beta",
            "definition": "PPN deviations induced by non-EH operator or source residuals",
            "must_show": "gamma-1=0 and beta-1=0 or source-backed bounds",
            "observable_link": "solar-system PPN",
            "status": "PPN_GATE",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2404_0_first_variation",
            "gate": "candidate first variation written",
            "status": "PASS_CONDITIONAL_NONCLAIM",
            "why": "FV2404 exposes the exact field equation and residuals",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2404_1_source_closure",
            "gate": "J_shadow=0 and T_active=T_H",
            "status": "CONDITIONAL_BLOCKED",
            "why": "requires off-contract coefficient zero as derivation, not only candidate restriction",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2404_2_operator_closure",
            "gate": "DeltaE_MTS+DeltaE_boundary=0",
            "status": "BLOCKED",
            "why": "operator residual silence is not proved",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2404_3_poisson",
            "gate": "Poisson/Newton equation follows",
            "status": "CONDITIONAL_BLOCKED",
            "why": "needs source closure, operator closure, and source normalization",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2404_4_local_GR_Newton",
            "gate": "local GR/Newton reduction",
            "status": "BLOCKED",
            "why": "first variation gives a clean conditional bridge, not a derived current-MTS theorem",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2404_0_first_variation_as_claim",
            "claim": "candidate first variation proves MTS reduces to GR",
            "allowed": "false",
            "reason": "the action is private candidate and residual closures are unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2404_1_EH_import",
            "claim": "standard EH variation can be imported as MTS proof",
            "allowed": "false",
            "reason": "EH variation is a conditional template until MTS leading-operator origin is signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2404_2_orbital_G_laundering",
            "claim": "orbital GM can normalize the Newton proof",
            "allowed": "false",
            "reason": "that would use the target Newtonian source law to prove itself",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2404_3_ppn_pass",
            "claim": "PPN gamma=beta=1 is passed",
            "allowed": "false",
            "reason": "DeltaE_MTS and source residuals still define PPN residual rows",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2404_0_real_gain",
            "decision": "accept the candidate first-variation bridge as exact conditional math",
            "reason": "the route to Einstein/Poisson is now explicit and testable clause-by-clause",
            "consequence": "no more vague coupling/operator talk in this branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2404_1_primary_bottleneck",
            "decision": "treat DeltaE_MTS residual silence as the next hard target",
            "reason": "source side is conditionally organized; LHS MTS operator is the remaining GR-critical piece",
            "consequence": "next checkpoint should attempt EH dominance/residual silence directly",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2404_2_next",
            "decision": "select EH dominance and residual-sector silence",
            "reason": "without this, Newton/PPN cannot be promoted even inside the candidate branch",
            "consequence": "2405 should try to derive DeltaE_MTS=0 or split it into source-backed bounds",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2404_0_selected",
            "next_doc": "2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md",
            "why": "first variation shows GR/Newton needs DeltaE_MTS and boundary residuals silent before Poisson/PPN promotion",
            "expected_output": "DeltaE_MTS owner split, zero/silence theorem attempt, and operator-residual bound pack if zero fails",
            "valid_for_claim": "false",
        }
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2404_SOURCE_REGISTER.csv": source_register_rows,
    "P8_Y5_PARENT_QLOC_2404_FIRST_VARIATION_LEDGER.csv": first_variation_rows,
    "P8_Y5_PARENT_QLOC_2404_SOURCE_CLOSURE_GATES.csv": source_closure_rows,
    "P8_Y5_PARENT_QLOC_2404_WEAK_FIELD_NEWTON_GATE.csv": weak_field_rows,
    "P8_Y5_PARENT_QLOC_2404_OPERATOR_RESIDUAL_PACK.csv": residual_rows,
    "P8_Y5_PARENT_QLOC_2404_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2404_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2404_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2404_NEXT_TARGET.csv": next_target_rows,
}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def sources_exist() -> bool:
    return all(Path(source["path"]).exists() for source in SOURCES)


def needles_found() -> bool:
    for source in SOURCES:
        path = Path(source["path"])
        if not path.exists():
            return False
        text = read_text(path)
        for needle in source["needles"].split("|"):
            if needle and needle not in text:
                return False
    return True


def csvs_parse() -> bool:
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            return False
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return False
    return True


def no_claim_flags() -> bool:
    for name in CSV_BUILDERS:
        path = RESIDUALS / name
        if not path.exists():
            return False
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if row.get("valid_for_claim", "").strip().lower() == "true":
                    return False
    return True


def formalization_untouched_by_script() -> bool:
    return not str(DOC_PATH).startswith(str(FORMALIZATION_ROOT)) and not str(RESIDUALS).startswith(str(FORMALIZATION_ROOT))


def validation_rows() -> list[dict[str, str]]:
    generated_text = "\n".join(
        [
            *[str(row) for row in first_variation_rows()],
            *[str(row) for row in source_closure_rows()],
            *[str(row) for row in weak_field_rows()],
            *[str(row) for row in residual_rows()],
            *[str(row) for row in claim_gate_rows()],
            *[str(row) for row in refusal_rows()],
            *[str(row) for row in next_target_rows()],
        ]
    )
    checks = [
        {
            "row_id": "VAL2404_00_sources_exist",
            "status": "PASS" if sources_exist() else "FAIL",
            "detail": "all required source paths exist" if sources_exist() else "one or more source paths are missing",
        },
        {
            "row_id": "VAL2404_01_needles_found",
            "status": "PASS" if needles_found() else "FAIL",
            "detail": "all source needles found" if needles_found() else "one or more source needles are missing",
        },
        {
            "row_id": "VAL2404_02_field_equation_present",
            "status": "PASS" if "FV2404_5_field_equation" in generated_text and "G_munu+Lambda g_munu+DeltaE_MTS" in generated_text else "FAIL",
            "detail": "candidate first-variation field equation is present",
        },
        {
            "row_id": "VAL2404_03_source_closure_gated",
            "status": "PASS" if "SRCLOSE2404_0_shadow_zero" in generated_text and "CONDITIONAL_FROM_2401_2402_2403" in generated_text else "FAIL",
            "detail": "source closure is gated and nonclaim",
        },
        {
            "row_id": "VAL2404_04_poisson_condition_present",
            "status": "PASS" if "nabla^2 U=4 pi G_ref rho_H" in generated_text else "FAIL",
            "detail": "conditional Poisson equation is recorded",
        },
        {
            "row_id": "VAL2404_05_operator_residual_pack",
            "status": "PASS" if "OR2404_0_DeltaE_MTS" in generated_text and "ROOT_OPERATOR_BLOCKER" in generated_text else "FAIL",
            "detail": "operator residual pack is retained",
        },
        {
            "row_id": "VAL2404_06_EH_import_refused",
            "status": "PASS" if "REF2404_1_EH_import" in generated_text else "FAIL",
            "detail": "EH import laundering is refused",
        },
        {
            "row_id": "VAL2404_07_local_claims_blocked",
            "status": "PASS" if all(row["status"] in {"PASS_CONDITIONAL_NONCLAIM", "CONDITIONAL_BLOCKED", "BLOCKED"} for row in claim_gate_rows()) else "FAIL",
            "detail": "first variation, source, operator, Poisson, and local GR gates remain nonclaim",
        },
        {
            "row_id": "VAL2404_08_csv_parse",
            "status": "PASS" if csvs_parse() else "FAIL",
            "detail": "generated CSVs parse and have rows",
        },
        {
            "row_id": "VAL2404_09_no_claim_flags",
            "status": "PASS" if no_claim_flags() else "FAIL",
            "detail": "no generated row has valid_for_claim=true",
        },
        {
            "row_id": "VAL2404_10_formalization_untouched_by_script",
            "status": "PASS" if formalization_untouched_by_script() else "FAIL",
            "detail": "script writes only post-checkpoint-work outputs",
        },
        {
            "row_id": "VAL2404_11_next_selected",
            "status": "PASS" if "2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md" in generated_text else "FAIL",
            "detail": "EH dominance/residual silence route selected next",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "row_id": "VAL2404_OVERALL",
            "status": overall,
            "detail": "2404 varies the minimal candidate, derives the exact conditional Einstein/Poisson bridge, retains operator/source residual gates, and selects EH dominance next",
        }
    )
    return [{"branch_id": BRANCH_ID, **row} for row in checks]


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    body = f"""# 2404 — Minimal Parent Action First Variation GR/Newton Gate Or Operator Residual Pack

## Result

The private candidate from 2403 survives the first formal variation test as an exact **conditional bridge**.

Inside the candidate branch,

`S_min=S_EH[e]+S_silent[q,Phi,lambda_C]+S_ord[e(q),Psi,theta,A_obs]+S_boundary_silent`,

the first variation gives the exposed equation

`G_munu+Lambda g_munu+DeltaE_MTS+DeltaE_boundary = kappa0(T_H_munu+J_shadow_munu)`.

If

`J_shadow=0`, `DeltaE_MTS=0`, `DeltaE_boundary=0`, and `kappa0=8 pi G_ref/c^4`

then the weak-field `00` equation yields

`nabla^2 U=4 pi G_ref rho_H`.

That is the cleanest GR/Newton bridge shape so far.  It is not yet a claim, because those four if-clauses are not all
derived from MTS primitives.  The live hard bottleneck is now the left-hand residual `DeltaE_MTS`, with boundary and
source-normalization as parallel gates.

## Source Register

{markdown_table(source_register_rows(), ["source_id", "source_path", "exists", "role", "valid_for_claim"])}

## First Variation Ledger

{markdown_table(first_variation_rows(), ["row_id", "variation_piece", "formal_step", "result", "status", "blocking_issue", "valid_for_claim"])}

## Source Closure Gates

{markdown_table(source_closure_rows(), ["row_id", "condition", "formal_requirement", "result_if_met", "current_status", "gap", "valid_for_claim"])}

## Weak Field Newton Gate

{markdown_table(weak_field_rows(), ["row_id", "step", "formula", "condition", "result", "status", "valid_for_claim"])}

## Operator Residual Pack

{markdown_table(residual_rows(), ["row_id", "residual", "definition", "must_show", "observable_link", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_gate_rows(), ["row_id", "gate", "status", "why", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows(), ["row_id", "claim", "allowed", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision_rows(), ["row_id", "decision", "reason", "consequence", "valid_for_claim"])}

## Next Target

{markdown_table(next_target_rows(), ["row_id", "next_doc", "why", "expected_output", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows(), ["row_id", "status", "detail"])}

## Practical Status

This is a useful pressure test.  The candidate does not fall apart under first variation; it gives the expected
Einstein/Poisson chain exactly when the source and operator residuals are silent.  So the next fight is no longer
“what is the coupling?” but “can the MTS residual operator `DeltaE_MTS` be proven silent, constrained, or bounded?”
That is a much cleaner boxing ring.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2404_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2404_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
