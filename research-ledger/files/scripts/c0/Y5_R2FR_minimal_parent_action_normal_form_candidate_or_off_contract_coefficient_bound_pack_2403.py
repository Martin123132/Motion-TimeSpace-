from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_MINIMAL_PARENT_ACTION_NORMAL_FORM_CANDIDATE_OR_OFF_CONTRACT_COEFFICIENT_BOUND_PACK_2403"
SCRIPT_PATH = Path(__file__).resolve()
POST_ROOT = SCRIPT_PATH.parents[1]
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
FORMALIZATION_ROOT = POST_ROOT.parent / "formalization-workbench"
DOC_PATH = POST_ROOT / "2403-Y5-R2FR-minimal-parent-action-normal-form-candidate-or-off-contract-coefficient-bound-pack.md"


def post(path: str) -> Path:
    return POST_ROOT / path


SOURCES = [
    {
        "source_id": "SRC2403_2402_doc",
        "path": str(post("2402-Y5-R2FR-parent-action-normal-form-ownership-signer-or-shadow-coefficient-acquisition.md")),
        "needles": "NEXT2402_0_selected|J_shadow=0 iff|VAL2402_OVERALL",
        "role": "immediate parent: finite owner basis and selected minimal parent action candidate",
    },
    {
        "source_id": "SRC2403_2402_owner",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2402_PARENT_ACTION_OWNER_SIGNER.csv")),
        "needles": "OWN2402_0_EH_geometry|OWN2402_2_Hilbert_matter|OWN2402_8_nonHilbert_spin_torsion",
        "role": "owner-by-owner signer rows",
    },
    {
        "source_id": "SRC2403_2402_coefficients",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2402_SHADOW_COEFFICIENT_ACQUISITION.csv")),
        "needles": "COEF2402_0_E_LHS_GR_residual|COEF2402_3_c_projector|COEF2402_6_c_nonHilbert",
        "role": "off-contract coefficient basis",
    },
    {
        "source_id": "SRC2403_2330_doc",
        "path": str(post("2330-Y5-R2FR-parent-action-adoption-vs-deeper-quotient-derivation-decision.md")),
        "needles": "Minimal Universal Matter Coupling|private provisional parent-action restriction|VAL2330_OVERALL",
        "role": "adoption-vs-deeper-derivation fork control",
    },
    {
        "source_id": "SRC2403_2372_doc",
        "path": str(post("2372-Y5-R2FR-parent-action-source-blind-functor-signature-or-source-profile-vector.md")),
        "needles": "Minimal Universal Matter Coupling|No local-GR/Newton claim|CG2372_4_local_GR_Newton",
        "role": "private minimal universal matter coupling branch",
    },
    {
        "source_id": "SRC2403_2357_doc",
        "path": str(post("2357-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md")),
        "needles": "MCA2357_0_parent_split|MCA2357_7_current_corpus_verdict|VAL2357_OVERALL",
        "role": "minimal parent matter coupling action candidate",
    },
    {
        "source_id": "SRC2403_2300_doc",
        "path": str(post("2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md")),
        "needles": "QSLOT2300_0_EH_GR|QRES2300_8_total|VAL2300_OVERALL",
        "role": "q-sector minimal parent slot and residual vector precedent",
    },
    {
        "source_id": "SRC2403_2234_doc",
        "path": str(post("2234-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md")),
        "needles": "ANS2234_A_EH_lambdaR_silent|ADOPT2234_6_verdict|VAL2234_OVERALL",
        "role": "weak-field minimal action ansatz and adoption guardrail",
    },
    {
        "source_id": "SRC2403_1769_doc",
        "path": str(post("1769-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md")),
        "needles": "ELH1769_0_target|NWF1769_1_poisson_conditional|VAL1769_OVERALL",
        "role": "GR/Newton conditional bridge and operator residual context",
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


def candidate_action_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "MPA2403_0_field_domain",
            "action_piece": "field/domain declaration",
            "candidate_form": "Fields={Phi_MTS,q(Phi),e_obs=E(q),Psi_A,theta_A,A_obs(optional),lambda_C}; no arena-added source/readout slots",
            "status": "CANDIDATE_AXIOM_NOT_DERIVED",
            "role": "fixes the parent object language before local tests",
            "derived_if": "future quotient-constructor theorem derives this domain from motion/time/space primitives",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MPA2403_1_EH_reference_core",
            "action_piece": "EH/local metric core",
            "candidate_form": "S_EH[e_obs]=(2 kappa0)^-1 int sqrt(-g_obs)(R[e_obs]-2 Lambda0)",
            "status": "WORKING_BRANCH_AXIOM_NOT_MTS_DERIVATION",
            "role": "gives the GR reference operator if adopted and if MTS residuals are silent",
            "derived_if": "future parent-reduction theorem shows the local MTS operator has EH as its leading quotient image",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MPA2403_2_silent_MTS_sector",
            "action_piece": "MTS residual/quotient sector",
            "candidate_form": "S_silent[q,Phi,lambda_C]=int sqrt(-g_obs) lambda_C C_MTS[q,Phi] + S_top[q,Phi] + O(residual coefficients)",
            "status": "CANDIDATE_CLOSURE_SLOT",
            "role": "keeps MTS content visible instead of deleting it by EH import",
            "derived_if": "constraints are first-class/topological or stress-silent on the local branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MPA2403_3_universal_matter",
            "action_piece": "minimal universal matter coupling",
            "candidate_form": "S_ord=sum_A int mu_obs(e_obs) L_A(Psi_A,D_obs Psi_A;theta_A,A_obs)",
            "status": "PRIVATE_RESTRICTION_READY_NOT_DERIVED",
            "role": "one Hilbert source before readout; no species/source weights",
            "derived_if": "source-blind functor or Noether/source-charge identity is derived from parent primitives",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MPA2403_4_boundary_policy",
            "action_piece": "boundary and reference policy",
            "candidate_form": "S_boundary[e_obs,q] allowed only when compact/falloff/local support makes delta S_boundary source-silent or explicitly coefficient-owned",
            "status": "BOUNDARY_AXIOM_OR_RESIDUAL",
            "role": "prevents boundary/worldtube terms from hiding as local source",
            "derived_if": "local boundary silence and reference normalization are proved for the chosen branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MPA2403_5_forbidden_terms",
            "action_piece": "off-contract term exclusion",
            "candidate_form": "Set c_nonminimal=c_projector=c_frame=delta_w_decoupled=c_nonHilbert=0 by candidate restriction; keep c_boundary only if silent",
            "status": "AXIOM_IF_ADOPTED_NOT_PROOF",
            "role": "turns 2402 residual basis into explicit candidate-zero clauses",
            "derived_if": "each forbidden slot is excluded by a parent constructor theorem, not by preference",
            "valid_for_claim": "false",
        },
    ]


def axiom_derived_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADS2403_0_definition",
            "clause": "one parent variational object",
            "classification": "candidate_definition",
            "reason": "needed for Euler ownership and no post-variation source map",
            "may_be_used_for": "private branch bookkeeping and first-variation tests",
            "may_not_be_used_for": "public claim that MTS has derived the action",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADS2403_1_EH_core",
            "clause": "EH leading local operator",
            "classification": "candidate_axiom_until_derived",
            "reason": "EH core gives GR/Newton if adopted, but EH-only import is not an MTS derivation",
            "may_be_used_for": "conditional GR bridge calculation",
            "may_not_be_used_for": "claiming MTS reduces to GR without residual silence theorem",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADS2403_2_Hilbert_source",
            "clause": "ordinary source is total Hilbert source",
            "classification": "derived_conditional_inside_candidate",
            "reason": "once S_ord is the only ordinary matter action and variation precedes readout, T_active=T_H follows",
            "may_be_used_for": "source-side conditional theorem",
            "may_not_be_used_for": "skipping proof of S_ord descent and source-map identity",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADS2403_3_no_shadow",
            "clause": "J_shadow=0",
            "classification": "derived_conditional_from_axiom_set",
            "reason": "2401/2402 show exact zero iff every off-contract coefficient is zero/silent/excluded",
            "may_be_used_for": "conditional source-side closure under MPA2403",
            "may_not_be_used_for": "declaring the off-contract coefficients physically impossible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADS2403_4_Newton",
            "clause": "Poisson/Newton limit",
            "classification": "not_derived_currently",
            "reason": "needs first variation, weak-field expansion, source normalization, and MTS residual silence",
            "may_be_used_for": "next checkpoint target",
            "may_not_be_used_for": "local-GR/Newton claim",
            "valid_for_claim": "false",
        },
    ]


def off_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFF2403_0_DeltaE_MTS",
            "coefficient": "DeltaE_MTS",
            "candidate_value": "0 on local GR branch",
            "status": "AXIOM_OR_RESIDUAL_NOT_DERIVED",
            "bound_if_not_zero": "PPN/Newton/operator-residual bound pack",
            "observable_link": "gamma,beta,preferred-frame,Poisson,orbital",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFF2403_1_c_nonminimal",
            "coefficient": "c_nonminimal",
            "candidate_value": "0",
            "status": "FORBIDDEN_BY_CANDIDATE_NOT_PARENT_PROVED",
            "bound_if_not_zero": "WEP/R10/clock composition-coupling bounds",
            "observable_link": "composition dependence and fifth-force lanes",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFF2403_2_c_boundary",
            "coefficient": "c_boundary",
            "candidate_value": "0 or locally silent",
            "status": "BOUNDARY_SILENCE_NOT_GLOBAL",
            "bound_if_not_zero": "worldtube/boundary leakage pack",
            "observable_link": "local source charge and orbital boundary terms",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFF2403_3_c_projector",
            "coefficient": "c_projector",
            "candidate_value": "0",
            "status": "FORBIDDEN_BY_VARIATION_BEFORE_READOUT_IF_ADOPTED",
            "bound_if_not_zero": "post-readout/source-selector coefficient pack",
            "observable_link": "WEP/R10/readout composition residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFF2403_4_c_frame",
            "coefficient": "c_frame",
            "candidate_value": "0",
            "status": "PUBLIC_COFRAME_AXIOM_NOT_DEEP_DERIVATION",
            "bound_if_not_zero": "clock/alpha/mass/frame-leak bound pack",
            "observable_link": "clock comparisons, alpha_EM, PPN preferred-frame",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFF2403_5_delta_w_decoupled",
            "coefficient": "delta_w_decoupled",
            "candidate_value": "0 in local ordinary arenas",
            "status": "ARENA_EXCLUSION_NOT_COMPLETE",
            "bound_if_not_zero": "separately conserved block/source-profile vector bounds",
            "observable_link": "source normalization and fifth-force-like residuals",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFF2403_6_c_nonHilbert",
            "coefficient": "c_nonHilbert",
            "candidate_value": "0 or Belinfante/LHS-owned",
            "status": "CONNECTION_CONVENTION_NOT_SIGNED",
            "bound_if_not_zero": "spin/torsion/non-Hilbert source-current bounds",
            "observable_link": "spin-polarized and torsion-sensitive tests",
            "valid_for_claim": "false",
        },
    ]


def conditional_derivation_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CDR2403_0_first_variation",
            "derivation": "candidate first variation",
            "formal_step": "delta S_min/delta e_obs gives G_munu+Lambda g_munu+DeltaE_MTS = kappa0 T_H + J_shadow terms",
            "condition": "all candidate clauses are adopted and variations are performed before readout",
            "result": "ordinary RHS is total Hilbert source plus explicit residual coefficients",
            "status": "TO_BE_VERIFIED_IN_2404",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CDR2403_1_source_closure",
            "derivation": "source side closes inside candidate",
            "formal_step": "if OFF2403_1..6 vanish/silent/excluded, then J_shadow=0 and T_active=T_H",
            "condition": "off-contract coefficients are zero by adopted branch or derived constructor theorem",
            "result": "source side is GR-like up to one common G calibration",
            "status": "EXACT_CONDITIONAL_NOT_PUBLIC",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CDR2403_2_operator_closure",
            "derivation": "left-hand operator closes",
            "formal_step": "if DeltaE_MTS=0 or higher-order bounded below local thresholds, E_LHS -> G_munu+Lambda g_munu",
            "condition": "EH dominance/residual silence theorem",
            "result": "Einstein equation follows under candidate",
            "status": "BLOCKED_PENDING_2404",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CDR2403_3_Newton_lane",
            "derivation": "Newton/Poisson limit",
            "formal_step": "weak-field 00 equation yields nabla^2 Phi=4 pi G rho_H if source and operator closures pass",
            "condition": "CDR2403_1 and CDR2403_2 plus source normalization",
            "result": "Newton inverse-square law becomes reachable, not yet claimed",
            "status": "TARGET_CONDITIONAL",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2403_0_candidate_written",
            "gate": "minimal parent action candidate written",
            "status": "PASS_PRIVATE_NONCLAIM",
            "why": "MPA2403 rows define the candidate branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2403_1_candidate_derived",
            "gate": "candidate derived from MTS primitives",
            "status": "BLOCKED",
            "why": "field domain, EH leading operator, and zero-coefficient restrictions remain candidate axioms",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2403_2_source_side",
            "gate": "source side GR-like",
            "status": "CONDITIONAL_BLOCKED",
            "why": "holds inside candidate only if off-contract coefficients vanish/silent/excluded",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2403_3_operator_side",
            "gate": "Einstein/Newton LHS operator",
            "status": "BLOCKED",
            "why": "DeltaE_MTS and weak-field first variation still require proof",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2403_4_local_GR_Newton",
            "gate": "local GR/Newton reduction",
            "status": "BLOCKED",
            "why": "candidate existence is not derivation; source and LHS gates remain conditional",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2403_0_candidate_as_proof",
            "claim": "the minimal parent action candidate proves MTS",
            "allowed": "false",
            "reason": "candidate axioms are labelled and not derived from deeper primitives",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2403_1_EH_import",
            "claim": "EH core alone is the MTS local theory",
            "allowed": "false",
            "reason": "EH-only import is forbidden unless MTS residual silence and quotient origin are signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2403_2_delete_coefficients",
            "claim": "off-contract coefficients can be deleted",
            "allowed": "false",
            "reason": "until derived zero, they remain explicit nonclaim bound rows",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2403_3_local_GR",
            "claim": "local GR/Newton is now derived",
            "allowed": "false",
            "reason": "2403 writes the candidate; 2404 must vary it and residual gates still remain",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2403_0_progress",
            "decision": "use minimal parent action as private candidate branch",
            "reason": "it is the cleanest low-scrutiny route to a GR/Newton derivation if its axioms are later derived or defended",
            "consequence": "future derivations can be precise instead of circling vague coupling language",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2403_1_no_laundering",
            "decision": "keep candidate axioms separate from derived theorems",
            "reason": "the project goal requires derivability, not just a tidy imposed action",
            "consequence": "all public/local claims remain blocked",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2403_2_next",
            "decision": "vary the candidate and test the GR/Newton bridge",
            "reason": "we must prove the candidate actually yields Einstein/Poisson under its own assumptions before spending more effort defending it",
            "consequence": "select 2404 first-variation GR/Newton gate",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2403_0_selected",
            "next_doc": "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md",
            "why": "2403 writes the candidate; 2404 must vary it and check the exact GR/Newton bridge without public promotion",
            "expected_output": "first-variation ledger, source closure theorem, weak-field Poisson conditions, and residual coefficient pack",
            "valid_for_claim": "false",
        }
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2403_SOURCE_REGISTER.csv": source_register_rows,
    "P8_Y5_PARENT_QLOC_2403_MINIMAL_PARENT_ACTION_CANDIDATE.csv": candidate_action_rows,
    "P8_Y5_PARENT_QLOC_2403_AXIOM_DERIVED_STATUS.csv": axiom_derived_rows,
    "P8_Y5_PARENT_QLOC_2403_OFF_CONTRACT_COEFFICIENTS.csv": off_contract_rows,
    "P8_Y5_PARENT_QLOC_2403_CONDITIONAL_DERIVATION_LEDGER.csv": conditional_derivation_rows,
    "P8_Y5_PARENT_QLOC_2403_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2403_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2403_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2403_NEXT_TARGET.csv": next_target_rows,
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
            *[str(row) for row in candidate_action_rows()],
            *[str(row) for row in axiom_derived_rows()],
            *[str(row) for row in off_contract_rows()],
            *[str(row) for row in conditional_derivation_rows()],
            *[str(row) for row in claim_gate_rows()],
            *[str(row) for row in refusal_rows()],
            *[str(row) for row in next_target_rows()],
        ]
    )
    checks = [
        {
            "row_id": "VAL2403_00_sources_exist",
            "status": "PASS" if sources_exist() else "FAIL",
            "detail": "all required source paths exist" if sources_exist() else "one or more source paths are missing",
        },
        {
            "row_id": "VAL2403_01_needles_found",
            "status": "PASS" if needles_found() else "FAIL",
            "detail": "all source needles found" if needles_found() else "one or more source needles are missing",
        },
        {
            "row_id": "VAL2403_02_candidate_written",
            "status": "PASS" if "MPA2403_0_field_domain" in generated_text and "MPA2403_5_forbidden_terms" in generated_text else "FAIL",
            "detail": "minimal parent action candidate rows are present",
        },
        {
            "row_id": "VAL2403_03_axiom_derived_split",
            "status": "PASS" if "candidate_axiom_until_derived" in generated_text and "derived_conditional_inside_candidate" in generated_text else "FAIL",
            "detail": "candidate axioms are separated from conditional derivations",
        },
        {
            "row_id": "VAL2403_04_off_contract_pack",
            "status": "PASS" if "OFF2403_6_c_nonHilbert" in generated_text and "AXIOM_OR_RESIDUAL_NOT_DERIVED" in generated_text else "FAIL",
            "detail": "off-contract coefficient pack is retained",
        },
        {
            "row_id": "VAL2403_05_no_EH_import_laundering",
            "status": "PASS" if "EH-only import is forbidden" in generated_text else "FAIL",
            "detail": "EH import refusal is explicit",
        },
        {
            "row_id": "VAL2403_06_local_claims_blocked",
            "status": "PASS" if all(row["status"] in {"BLOCKED", "CONDITIONAL_BLOCKED", "PASS_PRIVATE_NONCLAIM"} for row in claim_gate_rows()) else "FAIL",
            "detail": "candidate, source, operator, and GR/Newton gates remain nonclaim",
        },
        {
            "row_id": "VAL2403_07_csv_parse",
            "status": "PASS" if csvs_parse() else "FAIL",
            "detail": "generated CSVs parse and have rows",
        },
        {
            "row_id": "VAL2403_08_no_claim_flags",
            "status": "PASS" if no_claim_flags() else "FAIL",
            "detail": "no generated row has valid_for_claim=true",
        },
        {
            "row_id": "VAL2403_09_formalization_untouched_by_script",
            "status": "PASS" if formalization_untouched_by_script() else "FAIL",
            "detail": "script writes only post-checkpoint-work outputs",
        },
        {
            "row_id": "VAL2403_10_next_selected",
            "status": "PASS" if "2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md" in generated_text else "FAIL",
            "detail": "first-variation GR/Newton gate selected next",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "row_id": "VAL2403_OVERALL",
            "status": overall,
            "detail": "2403 writes the minimal parent-action candidate, labels axioms versus derived conditionals, retains off-contract coefficient rows, and selects first variation next",
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
    body = f"""# 2403 — Minimal Parent Action Normal Form Candidate Or Off-Contract Coefficient Bound Pack

## Result

This checkpoint writes the private minimal parent-action candidate without pretending it has already been derived.

Candidate branch:

`S_min = S_EH[e_obs] + S_silent[q,Phi,lambda_C] + S_ord[e_obs(q),Psi,theta,A_obs] + S_boundary_silent`.

The intended local equation after first variation is:

`G_munu + Lambda g_munu + DeltaE_MTS = kappa0 T_H + kappa0 J_shadow`,

with

`T_H := -2/sqrt(-g_obs) delta S_ord/delta g_obs`.

Inside this candidate, the source side closes only if the off-contract coefficients vanish/silent/excluded:

`J_shadow=0 iff c_nonminimal=c_boundary=c_projector=c_frame=delta_w_decoupled=c_nonHilbert=0 and T_active=T_H`.

That is useful.  It is not yet a proof that MTS derives GR.  The EH core, source-blind matter restriction, public coframe,
and zero off-contract coefficients are private candidate clauses until derived from deeper motion/time/space primitives.

## Source Register

{markdown_table(source_register_rows(), ["source_id", "source_path", "exists", "role", "valid_for_claim"])}

## Minimal Parent Action Candidate

{markdown_table(candidate_action_rows(), ["row_id", "action_piece", "candidate_form", "status", "role", "derived_if", "valid_for_claim"])}

## Axiom Derived Status

{markdown_table(axiom_derived_rows(), ["row_id", "clause", "classification", "reason", "may_be_used_for", "may_not_be_used_for", "valid_for_claim"])}

## Off-Contract Coefficient Pack

{markdown_table(off_contract_rows(), ["row_id", "coefficient", "candidate_value", "status", "bound_if_not_zero", "observable_link", "valid_for_claim"])}

## Conditional Derivation Ledger

{markdown_table(conditional_derivation_rows(), ["row_id", "derivation", "formal_step", "condition", "result", "status", "valid_for_claim"])}

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

This is the useful kind of leap: not a public leap, a controlled private branch.  The candidate gives us something
real to vary.  If its first variation does not cleanly yield the Einstein/Poisson chain under the stated clauses,
the route fails early.  If it does, the next fight becomes deeper derivation of the candidate clauses from MTS
primitives rather than guessing at couplings in the fog.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2403_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2403_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
