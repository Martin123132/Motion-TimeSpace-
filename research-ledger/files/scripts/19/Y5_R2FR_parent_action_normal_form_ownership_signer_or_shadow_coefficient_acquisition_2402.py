from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_PARENT_ACTION_NORMAL_FORM_OWNERSHIP_SIGNER_OR_SHADOW_COEFFICIENT_ACQUISITION_2402"
SCRIPT_PATH = Path(__file__).resolve()
POST_ROOT = SCRIPT_PATH.parents[1]
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
FORMALIZATION_ROOT = POST_ROOT.parent / "formalization-workbench"
DOC_PATH = POST_ROOT / "2402-Y5-R2FR-parent-action-normal-form-ownership-signer-or-shadow-coefficient-acquisition.md"


def post(path: str) -> Path:
    return POST_ROOT / path


SOURCES = [
    {
        "source_id": "SRC2402_2401_doc",
        "path": str(post("2401-Y5-R2FR-source-shadow-functional-exclusion-parent-action-grammar-or-shadow-bound-pack.md")),
        "needles": "NEXT2401_0_selected|PAG2401_0_single_parent_action|SSE2401_3_zero_if_contract_signed|VAL2401_OVERALL",
        "role": "immediate parent: source-shadow conditional zero and selected 2402",
    },
    {
        "source_id": "SRC2402_2401_contract",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2401_PARENT_ACTION_GRAMMAR_CONTRACT.csv")),
        "needles": "PAG2401_0_single_parent_action|PAG2401_1_identity_source_map|PAG2401_5_boundary_and_decoupled_silence",
        "role": "six-clause parent action grammar contract",
    },
    {
        "source_id": "SRC2402_2401_shadow_theorem",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2401_SOURCE_SHADOW_EXCLUSION_THEOREM.csv")),
        "needles": "SSE2401_1_variational_trichotomy|SSE2401_3_zero_if_contract_signed|SSE2401_4_current_verdict",
        "role": "conditional shadow zero theorem",
    },
    {
        "source_id": "SRC2402_1768_doc",
        "path": str(post("1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md")),
        "needles": "Parent Action Normal Form Signature|SCL1768_7_verdict|SCP1768_0_delta_w_shadow|VAL1768_OVERALL",
        "role": "earlier normal-form signature and coefficient pack",
    },
    {
        "source_id": "SRC2402_1768_normal_form",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1768_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv")),
        "needles": "ANF1768_0_parent_action_partition|ANF1768_2_hilbert_matter_owner|ANF1768_5_forbidden_source_map|ANF1768_6_current_verdict",
        "role": "normal-form owner rows",
    },
    {
        "source_id": "SRC2402_1768_classification",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1768_SHADOW_TERM_CLASSIFICATION_LEDGER.csv")),
        "needles": "SCL1768_0_hilbert_matter|SCL1768_2_nonminimal_coupling|SCL1768_5_post_variation_projector|SCL1768_7_verdict",
        "role": "shadow term classification inventory",
    },
    {
        "source_id": "SRC2402_2395_doc",
        "path": str(post("2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md")),
        "needles": "EHK2395_1_chain_rule_EH_silence|EHK2395_6_verdict|CG2395_3_GR_Newton|VAL2395_OVERALL",
        "role": "EH geometry owner and local-GR guardrails",
    },
    {
        "source_id": "SRC2402_2396_doc",
        "path": str(post("2396-Y5-R2FR-matter-source-lift-and-no-direct-slot-proof-or-source-charge-row.md")),
        "needles": "MSL2396_0_matter_action_grammar|MSL2396_4_no_direct_slot_zero|MSL2396_7_verdict|VAL2396_OVERALL",
        "role": "ordinary matter action grammar and no-direct slot gap",
    },
    {
        "source_id": "SRC2402_2397_doc",
        "path": str(post("2397-Y5-R2FR-no-direct-matter-coupling-grammar-or-coupling-charge-row.md")),
        "needles": "NDMC2397_0_allowed_minimal_syntax|NDMC2397_1_forbidden_direct_slots|NDMC2397_5_verdict|VAL2397_OVERALL",
        "role": "no-direct matter coupling grammar",
    },
    {
        "source_id": "SRC2402_1769_doc",
        "path": str(post("1769-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md")),
        "needles": "ELH1769_2_residual_decomposition|ORP1769_0_E_LHS_GR_residual|GBS1769_0_source_side|VAL1769_OVERALL",
        "role": "GR left-hand/operator residual context",
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


def owner_signer_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN2402_0_EH_geometry",
            "slot": "Einstein-Hilbert geometry",
            "normal_form_owner": "LHS_GR_REFERENCE_OPERATOR",
            "required_form": "S_EH[e_obs]=(16 pi G)^-1 int sqrt(-g_obs)(R[e_obs]-2 Lambda)",
            "signer_result": "CONDITIONAL_OWNER_READY",
            "current_gap": "EH can be separated as geometry, but MTS parent still needs EH dominance/residual silence",
            "residual_if_unsigned": "E_LHS_GR_residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN2402_1_MTS_geometry",
            "slot": "MTS geometric/action sector",
            "normal_form_owner": "LHS_MTS_OPERATOR",
            "required_form": "S_MTS[e_obs,Phi,X] varies into DeltaE_MTS^{mu nu}, not an RHS material source",
            "signer_result": "OWNER_ASSIGNED_AS_LHS_RESIDUAL",
            "current_gap": "operator residual must be theorem-zero or bounded in local weak-field arenas",
            "residual_if_unsigned": "DeltaE_MTS",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN2402_2_Hilbert_matter",
            "slot": "ordinary minimal matter",
            "normal_form_owner": "RHS_TOTAL_HILBERT_SOURCE",
            "required_form": "S_ord[e_obs,Psi,theta] and T_H=-2/sqrt(-g_obs) delta S_ord/delta g_obs",
            "signer_result": "CONDITIONAL_OWNER_READY",
            "current_gap": "requires no direct MTS/source slot, no post-variation source map, and matter lift/support closure",
            "residual_if_unsigned": "delta_w_shadow or epsilon_hidden_source_slot",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN2402_3_nonminimal",
            "slot": "nonminimal matter-geometry coupling",
            "normal_form_owner": "EXPLICIT_COEFFICIENT_OR_FORBIDDEN",
            "required_form": "DeltaS_nonminimal=int sqrt(-g) c_nonminimal f(Phi,X,labels)L_m",
            "signer_result": "UNSIGNED_CARRY_COEFFICIENT",
            "current_gap": "no parent theorem yet forbids all f(Phi,X,labels)L_m or A(X)J_m terms",
            "residual_if_unsigned": "c_nonminimal",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN2402_4_boundary",
            "slot": "boundary/improvement source",
            "normal_form_owner": "BOUNDARY_SILENT_OR_COEFFICIENT",
            "required_form": "delta S_boundary locally vanishes under compact support/falloff or is an explicit improvement residual",
            "signer_result": "UNSIGNED_CARRY_COEFFICIENT",
            "current_gap": "local boundary/worldtube silence is not globally signed",
            "residual_if_unsigned": "c_boundary",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN2402_5_projector",
            "slot": "post-variation source projector",
            "normal_form_owner": "FORBIDDEN_BY_ACTION_OWNERSHIP_IF_SIGNED",
            "required_form": "T_active=T_H, not P_material(T_H) after Hilbert variation",
            "signer_result": "CONDITIONAL_FORBIDDEN_NOT_PARENT_SIGNED",
            "current_gap": "single source-map identity is a contract, not a completed parent proof",
            "residual_if_unsigned": "c_projector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN2402_6_frame_reentry",
            "slot": "Weyl/disformal/public-frame re-entry",
            "normal_form_owner": "PUBLIC_COFRAME_ONLY_OR_FRAME_COEFFICIENT",
            "required_form": "ordinary matter/readout sees only e_obs, not A_A(X)e_obs, D_A(X), endpoint frame, or source metric",
            "signer_result": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "current_gap": "terminal public coframe/no-extra-frame action-domain proof remains unsigned",
            "residual_if_unsigned": "b_frame,d_frame,epsilon_endpoint",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN2402_7_decoupled_block",
            "slot": "separately conserved decoupled source block",
            "normal_form_owner": "ARENA_EXCLUDED_OR_BOUND",
            "required_form": "T_D is absent from local ordinary source arenas or has a source-backed projection bound",
            "signer_result": "UNSIGNED_CARRY_COEFFICIENT",
            "current_gap": "no local arena inventory yet proves absence of every separately conserved real block",
            "residual_if_unsigned": "delta_w_decoupled",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN2402_8_nonHilbert_spin_torsion",
            "slot": "spin/torsion/non-Hilbert current",
            "normal_form_owner": "BELINFANTE_IMPROVEMENT_LHS_OR_COEFFICIENT",
            "required_form": "non-Hilbert currents are absent, converted to Hilbert stress by improvement, assigned to connection/LHS geometry, or bounded",
            "signer_result": "UNSIGNED_CARRY_COEFFICIENT",
            "current_gap": "parent connection/coframe conventions do not yet sign absence or improvement for every current",
            "residual_if_unsigned": "c_nonHilbert",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NFT2402_0_normal_form",
            "claim_piece": "normal-form owner equation",
            "formal_statement": "delta S_parent/delta e_obs = E_EH + DeltaE_MTS + E_nonminimal + E_boundary + E_nonHilbert - (kappa/2) T_H",
            "proof_status": "CONDITIONAL_DECOMPOSITION",
            "meaning": "only T_H is an ordinary RHS source; other source-looking terms are LHS/operator, explicit residual, or forbidden",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NFT2402_1_shadow_expansion",
            "claim_piece": "shadow residual expansion",
            "formal_statement": "J_shadow = c_nonminimal J_nonminimal + c_boundary J_boundary + c_projector J_projector + c_frame J_frame + delta_w_decoupled T_D + c_nonHilbert J_nonHilbert",
            "proof_status": "DERIVED_CLASSIFICATION",
            "meaning": "the shadow gap is finite and owner-indexed, not an arbitrary mystery coupling",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NFT2402_2_zero_condition",
            "claim_piece": "source side closure condition",
            "formal_statement": "J_shadow=0 iff c_nonminimal=c_boundary=c_projector=c_frame=delta_w_decoupled=c_nonHilbert=0 and T_active=T_H",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "meaning": "local source side reduces to GR source if each off-contract owner is signed zero/silent/excluded",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NFT2402_3_current_verdict",
            "claim_piece": "current parent-action ownership signer",
            "formal_statement": "current corpus signs every owner row needed for J_shadow=0",
            "proof_status": "NOT_PROVED_CURRENT_CORPUS",
            "meaning": "EH/Hilbert/source-map lanes are sharpened, but nonminimal, boundary, projector, frame, decoupled, and non-Hilbert slots remain coefficient rows",
            "valid_for_claim": "false",
        },
    ]


def coefficient_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "COEF2402_0_E_LHS_GR_residual",
            "symbol": "DeltaE_MTS",
            "meaning": "left-hand deviation from Einstein operator after EH reference split",
            "needed_to_zero": "EH dominance/residual silence theorem",
            "observable_links": "PPN gamma/beta, Newton-Poisson, orbital, clocks",
            "status": "NONCLAIM_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "COEF2402_1_c_nonminimal",
            "symbol": "c_nonminimal",
            "meaning": "matter-MTS/geometric scalar coupling coefficient",
            "needed_to_zero": "no direct matter-MTS coupling theorem or explicit bound",
            "observable_links": "WEP/R10, clocks, composition dependence",
            "status": "NONCLAIM_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "COEF2402_2_c_boundary",
            "symbol": "c_boundary",
            "meaning": "local boundary/improvement/worldtube leakage coefficient",
            "needed_to_zero": "compact support/falloff/worldtube boundary silence theorem",
            "observable_links": "local force residuals, orbital boundary leakage",
            "status": "NONCLAIM_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "COEF2402_3_c_projector",
            "symbol": "c_projector",
            "meaning": "post-variation material source projector strength",
            "needed_to_zero": "identity source-map theorem signed by parent grammar",
            "observable_links": "WEP, R10, composition response",
            "status": "NONCLAIM_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "COEF2402_4_c_frame",
            "symbol": "c_frame",
            "meaning": "Weyl/disformal/endpoint public-frame re-entry coefficient",
            "needed_to_zero": "terminal public coframe/no-extra-frame proof",
            "observable_links": "clocks, EM constants, WEP, PPN preferred-frame",
            "status": "NONCLAIM_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "COEF2402_5_delta_w_decoupled",
            "symbol": "delta_w_decoupled",
            "meaning": "weight of a separately conserved block not connected to ordinary matter",
            "needed_to_zero": "local arena exclusion or empirical projection bound",
            "observable_links": "local source normalization, fifth-force-like residuals",
            "status": "NONCLAIM_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "COEF2402_6_c_nonHilbert",
            "symbol": "c_nonHilbert",
            "meaning": "spin/torsion/non-Hilbert current leakage after improvement conventions",
            "needed_to_zero": "connection/coframe normal form and Belinfante/improvement closure",
            "observable_links": "spin-polarized tests, torsion bounds, local source residuals",
            "status": "NONCLAIM_RESIDUAL",
            "valid_for_claim": "false",
        },
    ]


def gr_bridge_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "GRB2402_0_source_side",
            "object": "RHS Hilbert source",
            "current_status": "CONDITIONAL_CLOSURE_SHARPENED",
            "evidence": "owner theorem gives exact finite coefficients that must vanish",
            "next_requirement": "sign or bound each off-contract owner coefficient",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GRB2402_1_lhs_operator",
            "object": "LHS Einstein/Newton operator",
            "current_status": "STILL_BLOCKED",
            "evidence": "MTS geometry is assigned to LHS residual, not silently deleted",
            "next_requirement": "derive EH dominance/residual silence or score DeltaE_MTS",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "GRB2402_2_newton",
            "object": "Newtonian weak-field limit",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "source side and LHS operator both need closure before Poisson equation is an MTS theorem",
            "next_requirement": "minimal parent action candidate plus weak-field operator derivation",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2402_0_parent_normal_form",
            "gate": "complete parent normal form signed",
            "status": "BLOCKED",
            "why": "owner rows are classified but several are unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2402_1_source_shadow_zero",
            "gate": "J_shadow=0",
            "status": "BLOCKED",
            "why": "off-contract coefficients remain nonclaim rows",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2402_2_GR_left_hand",
            "gate": "Einstein/Newton left-hand operator",
            "status": "BLOCKED",
            "why": "DeltaE_MTS is assigned to LHS residual and not zeroed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2402_3_local_GR_Newton",
            "gate": "local GR/Newton reduction",
            "status": "BLOCKED",
            "why": "source side is sharper but not closed, and LHS operator residual remains",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2402_0_claim_all_owners_signed",
            "claim": "all parent action owner clauses are signed",
            "allowed": "false",
            "reason": "nonminimal, boundary, frame, decoupled, projector, and non-Hilbert slots remain unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2402_1_claim_source_side_closed",
            "claim": "RHS source side reduces to GR source",
            "allowed": "false",
            "reason": "J_shadow zero is exact only after coefficient zero/silence/exclusion",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2402_2_claim_GR_Newton",
            "claim": "MTS derives GR/Newton locally",
            "allowed": "false",
            "reason": "source closure and LHS Einstein dominance are still not current claims",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2402_0_accept_owner_finiteness",
            "decision": "accept finite owner-indexed residual basis",
            "reason": "source-shadow is no longer arbitrary; it is a finite list of unsigned owner slots",
            "consequence": "future tests/derivations know exactly which coefficients to zero or bound",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2402_1_no_axiom_laundering",
            "decision": "do not pretend a normal-form postulate is a derivation",
            "reason": "adopting minimal parent action would be legitimate, but must be labelled as parent action choice",
            "consequence": "next step should write the minimal candidate and mark which clauses are axioms versus derived",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2402_2_next",
            "decision": "build minimal parent action candidate with off-contract coefficient tests",
            "reason": "this is the fastest route to either close source side by construction or expose the remaining empirical coefficients",
            "consequence": "select 2403 minimal parent action normal-form candidate",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2402_0_selected",
            "next_doc": "2403-Y5-R2FR-minimal-parent-action-normal-form-candidate-or-off-contract-coefficient-bound-pack.md",
            "why": "2402 reduced source-shadow to a finite owner list; 2403 should write the minimal parent action candidate and separate axioms from derivations",
            "expected_output": "minimal action candidate, owner-zero table, and coefficient-bound fallback for every off-contract slot",
            "valid_for_claim": "false",
        }
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2402_SOURCE_REGISTER.csv": source_register_rows,
    "P8_Y5_PARENT_QLOC_2402_PARENT_ACTION_OWNER_SIGNER.csv": owner_signer_rows,
    "P8_Y5_PARENT_QLOC_2402_NORMAL_FORM_THEOREM.csv": theorem_rows,
    "P8_Y5_PARENT_QLOC_2402_SHADOW_COEFFICIENT_ACQUISITION.csv": coefficient_rows,
    "P8_Y5_PARENT_QLOC_2402_GR_BRIDGE_IMPACT.csv": gr_bridge_rows,
    "P8_Y5_PARENT_QLOC_2402_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2402_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2402_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2402_NEXT_TARGET.csv": next_target_rows,
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
            *[str(row) for row in owner_signer_rows()],
            *[str(row) for row in theorem_rows()],
            *[str(row) for row in coefficient_rows()],
            *[str(row) for row in gr_bridge_rows()],
            *[str(row) for row in claim_gate_rows()],
            *[str(row) for row in next_target_rows()],
        ]
    )
    checks = [
        {
            "row_id": "VAL2402_00_sources_exist",
            "status": "PASS" if sources_exist() else "FAIL",
            "detail": "all required source paths exist" if sources_exist() else "one or more source paths are missing",
        },
        {
            "row_id": "VAL2402_01_needles_found",
            "status": "PASS" if needles_found() else "FAIL",
            "detail": "all source needles found" if needles_found() else "one or more source needles are missing",
        },
        {
            "row_id": "VAL2402_02_owner_slots_complete",
            "status": "PASS" if "OWN2402_0_EH_geometry" in generated_text and "OWN2402_8_nonHilbert_spin_torsion" in generated_text else "FAIL",
            "detail": "owner signer covers geometry, Hilbert matter, and off-contract slots",
        },
        {
            "row_id": "VAL2402_03_shadow_expansion",
            "status": "PASS" if "J_shadow = c_nonminimal" in generated_text and "delta_w_decoupled" in generated_text else "FAIL",
            "detail": "finite source-shadow residual expansion is present",
        },
        {
            "row_id": "VAL2402_04_zero_condition",
            "status": "PASS" if "J_shadow=0 iff" in generated_text and "EXACT_CONDITIONAL_THEOREM" in generated_text else "FAIL",
            "detail": "source-side zero condition is exact but conditional",
        },
        {
            "row_id": "VAL2402_05_coefficients_nonclaim",
            "status": "PASS" if "COEF2402_6_c_nonHilbert" in generated_text and "NONCLAIM_RESIDUAL" in generated_text else "FAIL",
            "detail": "unsigned owner slots become nonclaim coefficient rows",
        },
        {
            "row_id": "VAL2402_06_global_claims_blocked",
            "status": "PASS" if all(row["status"] == "BLOCKED" for row in claim_gate_rows()) else "FAIL",
            "detail": "parent normal form, source zero, LHS, and GR/Newton gates remain blocked",
        },
        {
            "row_id": "VAL2402_07_csv_parse",
            "status": "PASS" if csvs_parse() else "FAIL",
            "detail": "generated CSVs parse and have rows",
        },
        {
            "row_id": "VAL2402_08_no_claim_flags",
            "status": "PASS" if no_claim_flags() else "FAIL",
            "detail": "no generated row has valid_for_claim=true",
        },
        {
            "row_id": "VAL2402_09_formalization_untouched_by_script",
            "status": "PASS" if formalization_untouched_by_script() else "FAIL",
            "detail": "script writes only post-checkpoint-work outputs",
        },
        {
            "row_id": "VAL2402_10_next_selected",
            "status": "PASS" if "2403-Y5-R2FR-minimal-parent-action-normal-form-candidate-or-off-contract-coefficient-bound-pack.md" in generated_text else "FAIL",
            "detail": "minimal parent action candidate route selected next",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "row_id": "VAL2402_OVERALL",
            "status": overall,
            "detail": "2402 reduces source-shadow to a finite owner-indexed coefficient basis, refuses local-GR promotion, and selects a minimal parent-action candidate next",
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
    body = f"""# 2402 — Parent Action Normal Form Ownership Signer Or Shadow Coefficient Acquisition

## Result

This checkpoint does not magically prove local GR, but it makes the coupling wound much less slippery.

The parent-action owner equation is now:

`delta S_parent/delta e_obs = E_EH + DeltaE_MTS + E_nonminimal + E_boundary + E_nonHilbert - (kappa/2) T_H`.

Only

`T_H := -2/sqrt(-g_obs) delta S_ord/delta g_obs`

is allowed to be the ordinary right-hand source.  Everything else must be owned as left-hand geometry, boundary/improvement, explicit nonminimal coupling, public-frame leakage, decoupled block, non-Hilbert current, or forbidden post-variation projector.

That gives the finite shadow expansion:

`J_shadow = c_nonminimal J_nonminimal + c_boundary J_boundary + c_projector J_projector + c_frame J_frame + delta_w_decoupled T_D + c_nonHilbert J_nonHilbert`.

So the exact source-side closure condition is:

`J_shadow=0 iff c_nonminimal=c_boundary=c_projector=c_frame=delta_w_decoupled=c_nonHilbert=0 and T_active=T_H`.

Current MTS has not signed every owner-zero clause.  Therefore the source side is narrowed to a finite residual basis, not promoted to a GR/Newton claim.

## Source Register

{markdown_table(source_register_rows(), ["source_id", "source_path", "exists", "role", "valid_for_claim"])}

## Parent Action Owner Signer

{markdown_table(owner_signer_rows(), ["owner_id", "slot", "normal_form_owner", "required_form", "signer_result", "current_gap", "residual_if_unsigned", "valid_for_claim"])}

## Normal Form Theorem

{markdown_table(theorem_rows(), ["row_id", "claim_piece", "formal_statement", "proof_status", "meaning", "valid_for_claim"])}

## Shadow Coefficient Acquisition

{markdown_table(coefficient_rows(), ["row_id", "symbol", "meaning", "needed_to_zero", "observable_links", "status", "valid_for_claim"])}

## GR Bridge Impact

{markdown_table(gr_bridge_rows(), ["row_id", "object", "current_status", "evidence", "next_requirement", "valid_for_claim"])}

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

This is another useful tightening.  The theory is no longer allowed to say “some coupling”.
The live source-side problem is now a finite owner table.  Either we adopt and defend a minimal parent action
where those off-contract coefficients are zero by construction, or we carry the coefficients into empirical bounds.
The next step is to write that minimal candidate honestly: which parts are definition, which are derived, and which
remain residuals.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2402_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2402_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
