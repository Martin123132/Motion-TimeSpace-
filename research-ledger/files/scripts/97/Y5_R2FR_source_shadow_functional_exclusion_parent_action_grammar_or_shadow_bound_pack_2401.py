from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_SOURCE_SHADOW_FUNCTIONAL_EXCLUSION_PARENT_ACTION_GRAMMAR_OR_SHADOW_BOUND_PACK_2401"
SCRIPT_PATH = Path(__file__).resolve()
POST_ROOT = SCRIPT_PATH.parents[1]
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
FORMALIZATION_ROOT = POST_ROOT.parent / "formalization-workbench"
DOC_PATH = POST_ROOT / "2401-Y5-R2FR-source-shadow-functional-exclusion-parent-action-grammar-or-shadow-bound-pack.md"


def post(path: str) -> Path:
    return POST_ROOT / path


SOURCES = [
    {
        "source_id": "SRC2401_2400_doc",
        "path": str(post("2400-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md")),
        "needles": "NEXT2400_0_selected|source-shadow|delta_w_block + delta_w_shadow|VAL2400_OVERALL",
        "role": "immediate parent selecting source-shadow grammar",
    },
    {
        "source_id": "SRC2401_2400_shadow_audit",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2400_SOURCE_SHADOW_BAN_AUDIT.csv")),
        "needles": "SSB2400_0_forbidden_shape|SSB2400_1_total_hilbert_owner|SSB2400_3_current_verdict",
        "role": "2400 source-shadow loophole audit",
    },
    {
        "source_id": "SRC2401_1767_doc",
        "path": str(post("1767-Y5-R2FR-single-source-map-grammar-and-source-shadow-ban-or-shadow-bound.md")),
        "needles": "Single Source-Map Identity Theorem|source-shadow classification|`delta_w_shadow` remains a nonclaim residual|VAL1767_OVERALL",
        "role": "single-source-map identity and shadow trichotomy",
    },
    {
        "source_id": "SRC2401_1767_zero",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1767_SOURCE_SHADOW_ZERO_ATTEMPT.csv")),
        "needles": "SSZ1767_1_shadow_as_action_term|SSZ1767_2_shadow_as_nonvariational|SSZ1767_3_shadow_as_projector|SSZ1767_4_current_verdict",
        "role": "source-shadow zero attempt and surviving gaps",
    },
    {
        "source_id": "SRC2401_1768_doc",
        "path": str(post("1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md")),
        "needles": "Parent Action Normal Form Signature|Shadow Term Classification Ledger|SCL1768_7_verdict|VAL1768_OVERALL",
        "role": "parent normal-form and term-owner ledger",
    },
    {
        "source_id": "SRC2401_1768_classification",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1768_SHADOW_TERM_CLASSIFICATION_LEDGER.csv")),
        "needles": "SCL1768_2_nonminimal_coupling|SCL1768_3_boundary_improvement|SCL1768_4_nonhilbert_spin_torsion|SCL1768_5_post_variation_projector|SCL1768_7_verdict",
        "role": "shadow term classification ledger",
    },
    {
        "source_id": "SRC2401_1803_doc",
        "path": str(post("1803-Y5-R2FR-no-shadow-constant-marker-or-qbar-coefficient-pack.md")),
        "needles": "SCT1803_5_source_prefactor|SCT1803_6_action_normal_form|QCP1803_6_delta_w_shadow|VAL1803_OVERALL",
        "role": "hidden-coupling and coefficient-pack gate",
    },
    {
        "source_id": "SRC2401_1839_doc",
        "path": str(post("1839-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row.md")),
        "needles": "SSB1839_0_identity_source_map|SSB1839_1_shadow_trichotomy|SSB1839_3_current_verdict|VAL1839_OVERALL",
        "role": "consolidated source-shadow ban attempt",
    },
    {
        "source_id": "SRC2401_1880_zero",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1880_NO_SHADOW_ZERO_THEOREM_ATTEMPT.csv")),
        "needles": "ZTH1880_0_exact_conditional|ZTH1880_1_shortcut_rejection|ZTH1880_2_current_verdict|ZTH1880_3_fallback",
        "role": "terminal coframe no-shadow conditional theorem and shortcut rejection",
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


def grammar_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PAG2401_0_single_parent_action",
            "clause": "single parent action",
            "mathematical_requirement": "S_parent[e_obs,Phi,Psi,theta]=S_EH[e_obs]+S_MTS[e_obs,Phi]+S_ord[e_obs,Psi,theta]+S_boundary",
            "why_needed": "prevents field equations from being written with an extra post-variation source map",
            "current_status": "CONTRACT_REQUIRED_NOT_PARENT_SIGNED",
            "if_signed": "all source-looking terms must be variationally owned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PAG2401_1_identity_source_map",
            "clause": "identity Hilbert source map",
            "mathematical_requirement": "T_active := T_H := -2/sqrt(-g_obs) delta S_ord/delta g_obs, with no independent F_shadow(T_H,labels)",
            "why_needed": "kills post-Hilbert source projectors and material-labelled source maps",
            "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "if_signed": "post-variation source-shadow maps are forbidden by grammar",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PAG2401_2_owner_exhaustion",
            "clause": "source-looking owner exhaustion",
            "mathematical_requirement": "each tensor contribution belongs exactly to RHS Hilbert matter, LHS geometry/MTS, boundary/improvement, explicit nonminimal term, or decoupled real sector",
            "why_needed": "no unowned tensor can be smuggled into q_loc^nu or the local field equation",
            "current_status": "CLASSIFICATION_READY_NOT_EXHAUSTED",
            "if_signed": "J_shadow has no independent owner left",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PAG2401_3_no_source_only_prefactor",
            "clause": "no source-only prefactor",
            "mathematical_requirement": "partial S_ord/partial w_A=0 and no kappa_A, w_A, eta_A multiplies the active source except one common calibration",
            "why_needed": "prevents a source-only coupling from bypassing the matter action and exchange-graph collapse",
            "current_status": "PARTIAL_FROM_2397_2400_NOT_PARENT_SIGNED",
            "if_signed": "delta_w_block is the only possible disconnected-block residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PAG2401_4_public_coframe_only",
            "clause": "terminal public coframe only",
            "mathematical_requirement": "ordinary matter/readout couples to e_obs only; no A_A(X)e_obs, D_A(X), endpoint frame, or source-only metric slot",
            "why_needed": "prevents representative-dependent Weyl/disformal re-entry after the source map is cleaned",
            "current_status": "EXACT_CONDITIONAL_FROM_1880_NOT_PARENT_SIGNED",
            "if_signed": "frame-shadow terms are zero rather than source residuals",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PAG2401_5_boundary_and_decoupled_silence",
            "clause": "boundary and decoupled silence",
            "mathematical_requirement": "boundary/improvement terms are locally silent under the chosen falloff, and separately conserved decoupled blocks are absent from local test sources or explicitly bounded",
            "why_needed": "separately conserved tensors can survive Bianchi without being Hilbert matter",
            "current_status": "BOUND_OR_EXCLUSION_REQUIRED",
            "if_signed": "remaining source-shadow coefficient is zero in local arenas",
            "valid_for_claim": "false",
        },
    ]


def exclusion_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSE2401_0_define_shadow",
            "claim_piece": "source-shadow definition",
            "formal_statement": "J_shadow is any contribution such that E_LHS^{mu nu}=kappa(T_H^{mu nu}+J_shadow^{mu nu}) while J_shadow is not the Hilbert/coframe variation of ordinary matter in the declared source sector",
            "proof_step": "definition isolates hidden RHS material, post-variation projectors, source-only prefactors, and unowned conserved tensors",
            "result": "well-defined residual target",
            "status": "DEFINITION",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSE2401_1_variational_trichotomy",
            "claim_piece": "action-derived source-shadow trichotomy",
            "formal_statement": "If field equations come from delta S_parent=0, then a source-looking tensor is either delta S_ord/delta e_obs, delta S_geom/delta e_obs, delta S_boundary/delta e_obs, delta S_nonminimal/delta e_obs, or not action-derived",
            "proof_step": "split the Euler variation by the parent action partition",
            "result": "hidden source terms are reclassified as matter, geometry, boundary/nonminimal, or forbidden nonvariational insertions",
            "status": "CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSE2401_2_nonvariational_rejection",
            "claim_piece": "nonvariational source-shadow rejection",
            "formal_statement": "A post-variation J_shadow with no DeltaS is not admitted by a parent action; Bianchi further requires nabla_mu J_shadow^{mu nu}=0 if inserted anyway",
            "proof_step": "Euler-Lagrange ownership plus nabla_mu E_LHS^{mu nu}=0",
            "result": "nonvariational shadows are forbidden or become real separately conserved residual blocks",
            "status": "DERIVED_FILTER",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSE2401_3_zero_if_contract_signed",
            "claim_piece": "source-shadow zero theorem",
            "formal_statement": "If PAG2401_0..5 are signed, then J_shadow^{mu nu}=0 in local ordinary-source arenas and delta_w_shadow=0",
            "proof_step": "all shadow slots are either identity Hilbert source, LHS geometry, boundary-silent, explicitly absent, or excluded from the arena",
            "result": "exact local source-shadow zero, conditional on full parent grammar",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SSE2401_4_current_verdict",
            "claim_piece": "current MTS source-shadow exclusion",
            "formal_statement": "current corpus proves PAG2401_0..5",
            "proof_step": "existing checkpoints state the clauses but do not sign the complete parent action inventory",
            "result": "source-shadow is narrowed to a parent-action grammar contract or an empirical shadow coefficient pack",
            "status": "NOT_PROVED_CURRENT_CORPUS",
            "valid_for_claim": "false",
        },
    ]


def shadow_bound_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBP2401_0_delta_w_shadow",
            "quantity": "delta_w_shadow",
            "meaning": "coefficient multiplying any unexcluded non-Hilbert/post-Hilbert source-shadow current",
            "mathematical_form": "T_active=T_H+delta_w_shadow J_shadow",
            "units": "dimensionless if J_shadow is normalized to T_H",
            "status": "RETAINED_NONCLAIM",
            "required_before_claim": "parent grammar proof or source-backed projection coefficients and arena bounds",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBP2401_1_nonminimal_coefficient",
            "quantity": "c_nonminimal",
            "meaning": "coefficient for explicit matter-MTS/geometric scalar coupling",
            "mathematical_form": "DeltaS_nonminimal=int sqrt(-g) c_nonminimal f(Phi,X,labels)L_m",
            "units": "model-dependent",
            "status": "BOUND_OR_FORBID",
            "required_before_claim": "normal-form owner decision and matter EOM impact",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBP2401_2_boundary_coefficient",
            "quantity": "c_boundary",
            "meaning": "local leakage from boundary/improvement terms",
            "mathematical_form": "J_boundary^{mu nu}=nabla_alpha U^{alpha mu nu}",
            "units": "source-density units after normalization",
            "status": "SILENCE_OR_BOUND",
            "required_before_claim": "falloff/local support theorem or finite boundary residual bound",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBP2401_3_projector_coefficient",
            "quantity": "c_projector",
            "meaning": "post-variation material/source projector strength",
            "mathematical_form": "T_active=T_H+c_projector(P_material(T_H)-T_H)",
            "units": "dimensionless",
            "status": "FORBIDDEN_IF_IDENTITY_SOURCE_MAP_SIGNED",
            "required_before_claim": "identity source-map theorem signed by parent grammar",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBP2401_4_decoupled_block",
            "quantity": "delta_w_decoupled",
            "meaning": "weight of separately conserved source block not exchange-connected to ordinary test matter",
            "mathematical_form": "nabla_mu T_D^{mu nu}=0 and T_active=T_H+delta_w_decoupled T_D",
            "units": "dimensionless after normalization",
            "status": "ARENA_EXCLUDE_OR_BOUND",
            "required_before_claim": "local arena inventory proving absence or a finite empirical projection",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2401_0_parent_action_normal_form",
            "gate": "complete parent action normal form",
            "status": "BLOCKED",
            "why": "PAG2401 clauses are a contract; current corpus does not sign the full action inventory",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2401_1_identity_source_map",
            "gate": "T_active equals total Hilbert source",
            "status": "BLOCKED",
            "why": "identity source map is conditional and post-variation/projector exclusion is not yet parent-signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2401_2_delta_w_shadow_zero",
            "gate": "delta_w_shadow=0",
            "status": "BLOCKED",
            "why": "nonminimal, boundary, projector, frame, and decoupled-block slots still need signed zero/exclusion",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2401_3_local_GR_Newton",
            "gate": "local GR/Newton source side",
            "status": "BLOCKED",
            "why": "source-shadow zero is an exact conditional theorem, not a current corpus theorem",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2401_0_claim_shadow_zero",
            "claim": "MTS proves J_shadow=0",
            "allowed": "false",
            "reason": "PAG2401_0..5 are not all parent-signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2401_1_claim_identity_source",
            "claim": "active source is exactly total Hilbert source",
            "allowed": "false",
            "reason": "identity source-map theorem remains conditional",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2401_2_claim_local_GR",
            "claim": "local GR/Newton follows from source-side cleanup",
            "allowed": "false",
            "reason": "shadow/source side is narrowed but not fully closed, and LHS/operator gates still matter",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2401_0_real_gain",
            "decision": "accept exact conditional source-shadow zero theorem",
            "reason": "if the parent action grammar is signed, J_shadow has no independent slot",
            "consequence": "we have a precise contract rather than a vague coupling gap",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2401_1_no_promotion",
            "decision": "do not claim local GR/Newton",
            "reason": "the contract is not yet signed by a complete parent action inventory",
            "consequence": "keep all local claims blocked",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2401_2_next",
            "decision": "attack the parent action normal-form signer next",
            "reason": "this is now the shortest route from conditional theorem to actual source-side closure",
            "consequence": "select 2402 parent action normal-form ownership signer",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2401_0_selected",
            "next_doc": "2402-Y5-R2FR-parent-action-normal-form-ownership-signer-or-shadow-coefficient-acquisition.md",
            "why": "2401 proves the exact conditional zero theorem; 2402 must either sign each parent owner clause or turn unsigned clauses into coefficient rows",
            "expected_output": "owner-by-owner signer for Hilbert matter, MTS geometry, nonminimal, boundary, projector, frame, and decoupled-block terms",
            "valid_for_claim": "false",
        }
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2401_SOURCE_REGISTER.csv": source_register_rows,
    "P8_Y5_PARENT_QLOC_2401_PARENT_ACTION_GRAMMAR_CONTRACT.csv": grammar_contract_rows,
    "P8_Y5_PARENT_QLOC_2401_SOURCE_SHADOW_EXCLUSION_THEOREM.csv": exclusion_theorem_rows,
    "P8_Y5_PARENT_QLOC_2401_SHADOW_BOUND_PACK.csv": shadow_bound_rows,
    "P8_Y5_PARENT_QLOC_2401_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2401_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2401_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2401_NEXT_TARGET.csv": next_target_rows,
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
            *[str(row) for row in grammar_contract_rows()],
            *[str(row) for row in exclusion_theorem_rows()],
            *[str(row) for row in shadow_bound_rows()],
            *[str(row) for row in claim_gate_rows()],
            *[str(row) for row in decision_rows()],
            *[str(row) for row in next_target_rows()],
        ]
    )
    checks = [
        {
            "row_id": "VAL2401_00_sources_exist",
            "status": "PASS" if sources_exist() else "FAIL",
            "detail": "all required source paths exist" if sources_exist() else "one or more source paths are missing",
        },
        {
            "row_id": "VAL2401_01_needles_found",
            "status": "PASS" if needles_found() else "FAIL",
            "detail": "all source needles found" if needles_found() else "one or more source needles are missing",
        },
        {
            "row_id": "VAL2401_02_contract_written",
            "status": "PASS" if "PAG2401_0_single_parent_action" in generated_text and "PAG2401_5_boundary_and_decoupled_silence" in generated_text else "FAIL",
            "detail": "parent action grammar contract is explicit",
        },
        {
            "row_id": "VAL2401_03_trichotomy_present",
            "status": "PASS" if "SSE2401_1_variational_trichotomy" in generated_text else "FAIL",
            "detail": "action-derived source-shadow trichotomy recorded",
        },
        {
            "row_id": "VAL2401_04_conditional_zero_theorem",
            "status": "PASS" if "J_shadow^{mu nu}=0" in generated_text and "EXACT_CONDITIONAL_THEOREM" in generated_text else "FAIL",
            "detail": "exact conditional source-shadow zero theorem recorded",
        },
        {
            "row_id": "VAL2401_05_shadow_pack_nonclaim",
            "status": "PASS" if "SBP2401_0_delta_w_shadow" in generated_text and "RETAINED_NONCLAIM" in generated_text else "FAIL",
            "detail": "fallback shadow coefficient pack remains nonclaim",
        },
        {
            "row_id": "VAL2401_06_global_claims_blocked",
            "status": "PASS" if all(row["status"] == "BLOCKED" for row in claim_gate_rows()) else "FAIL",
            "detail": "parent normal form, identity source, shadow zero, and local GR gates remain blocked",
        },
        {
            "row_id": "VAL2401_07_csv_parse",
            "status": "PASS" if csvs_parse() else "FAIL",
            "detail": "generated CSVs parse and have rows",
        },
        {
            "row_id": "VAL2401_08_no_claim_flags",
            "status": "PASS" if no_claim_flags() else "FAIL",
            "detail": "no generated row has valid_for_claim=true",
        },
        {
            "row_id": "VAL2401_09_formalization_untouched_by_script",
            "status": "PASS" if formalization_untouched_by_script() else "FAIL",
            "detail": "script writes only post-checkpoint-work outputs",
        },
        {
            "row_id": "VAL2401_10_next_selected",
            "status": "PASS" if "2402-Y5-R2FR-parent-action-normal-form-ownership-signer-or-shadow-coefficient-acquisition.md" in generated_text else "FAIL",
            "detail": "parent action ownership signer selected next",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "row_id": "VAL2401_OVERALL",
            "status": overall,
            "detail": "2401 records the exact conditional source-shadow zero theorem, refuses promotion, stages the shadow-bound pack, and selects parent-action ownership signing next",
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
    body = f"""# 2401 — Source-Shadow Functional Exclusion Parent-Action Grammar Or Shadow Bound Pack

## Result

This is the cleanest source-shadow statement we can honestly write right now.

Define `J_shadow` by

`E_LHS^{{mu nu}} = kappa (T_H^{{mu nu}} + J_shadow^{{mu nu}})`,

where `T_H := -2/sqrt(-g_obs) delta S_ord/delta g_obs` is the total ordinary Hilbert/coframe source.

If the parent action grammar signs the six clauses `PAG2401_0..5`, then every source-looking contribution has an owner:

- ordinary matter source: `T_H`;
- MTS/EH geometry: left-hand operator;
- boundary/improvement: locally silent or bounded;
- nonminimal matter-geometry term: explicit coefficient, not hidden source;
- projector/nonvariational term: forbidden;
- decoupled conserved block: arena-excluded or bounded.

Under those clauses,

`J_shadow^{{mu nu}}=0`

and therefore `delta_w_shadow=0` in local ordinary-source arenas.

But those clauses are not all parent-signed in the current corpus.  So this is an exact conditional theorem, not a local-GR/Newton claim.

## Source Register

{markdown_table(source_register_rows(), ["source_id", "source_path", "exists", "role", "valid_for_claim"])}

## Parent Action Grammar Contract

{markdown_table(grammar_contract_rows(), ["clause_id", "clause", "mathematical_requirement", "why_needed", "current_status", "if_signed", "valid_for_claim"])}

## Source-Shadow Exclusion Theorem

{markdown_table(exclusion_theorem_rows(), ["row_id", "claim_piece", "formal_statement", "proof_step", "result", "status", "valid_for_claim"])}

## Shadow Bound Pack

{markdown_table(shadow_bound_rows(), ["row_id", "quantity", "meaning", "mathematical_form", "units", "status", "required_before_claim", "valid_for_claim"])}

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

This is a proper forward step.  The coupling gap is no longer “maybe some mystery source term”.
It is now a finite parent-action signing problem: sign the owner clauses, or carry `delta_w_shadow`,
`c_nonminimal`, `c_boundary`, `c_projector`, and `delta_w_decoupled` as explicit nonclaim coefficients.
That is exactly the kind of discipline needed before the local GR/Newton bridge can be taken seriously.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2401_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2401_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
