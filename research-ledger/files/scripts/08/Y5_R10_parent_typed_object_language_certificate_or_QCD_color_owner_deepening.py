from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1236"
TITLE = "1236-Y5-R10-parent-typed-object-language-certificate-or-QCD-color-owner-deepening"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
CERTIFICATE_PATH = OUT_DIR / f"{PACK_ID}_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv"
META_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_NO_HIDDEN_VISIBLE_COEFFICIENT_META_THEOREM.csv"
UNIQUE_F2_STATUS_PATH = OUT_DIR / f"{PACK_ID}_UNIQUE_F2_STATUS_AFTER_CERTIFICATE.csv"
QCD_DEEPENING_PATH = OUT_DIR / f"{PACK_ID}_QCD_COLOR_OWNER_DEEPENING.csv"
FINITE_RESIDUAL_PATH = OUT_DIR / f"{PACK_ID}_FINITE_EM_QCD_RESIDUAL_BACKSTOP.csv"
EDGE_STATUS_PATH = OUT_DIR / f"{PACK_ID}_GRAPH_EDGE_STATUS_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1236_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1236_0_1235_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1235_NEXT_TARGET.csv",
            "needle": "NEXT1235_0_1236",
            "purpose": "1235 handoff to typed certificate or QCD owner deepening",
        },
        {
            "source_id": "SRC1236_1_1235_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv",
            "needle": "TREQ1235_1_visible_coeff_domain",
            "purpose": "exact certificate requirements",
        },
        {
            "source_id": "SRC1236_2_1235_unique_F2",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1235_UNIQUE_F2_TYPED_COEFFICIENT_DOMAIN_PROOF_ATTEMPT.csv",
            "needle": "UF21235_7_verdict",
            "purpose": "unique-F2 remains unclosed",
        },
        {
            "source_id": "SRC1236_3_1235_blockers",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1235_UNIQUE_F2_BLOCKER_LEDGER.csv",
            "needle": "UBLOCK1235_0_unique_F2",
            "purpose": "active unique-F2 blocker ledger",
        },
        {
            "source_id": "SRC1236_4_1235_QCD",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1235_QCD_COLOR_EDGE_OWNER_PROOF_ATTEMPT.csv",
            "needle": "QCD1235_1_color_edge_conditional",
            "purpose": "QCD color conditional theorem",
        },
        {
            "source_id": "SRC1236_5_1055_parent_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_6_single_parent_action",
            "purpose": "single parent action contract candidate",
        },
        {
            "source_id": "SRC1236_6_1055_no_mixed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_3_no_mixed_coefficients",
            "purpose": "no hidden-visible coefficient contract",
        },
        {
            "source_id": "SRC1236_7_1220_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            "needle": "PTOL1220_1_visible_coefficient_domain",
            "purpose": "visible coefficient domain still not derived",
        },
        {
            "source_id": "SRC1236_8_1219_typed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv",
            "needle": "TVC1219_1_typed_domain_theorem",
            "purpose": "typed functor conditional theorem",
        },
        {
            "source_id": "SRC1236_9_1219_counterexample",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK.csv",
            "needle": "HSC1219_1_alpha",
            "purpose": "hidden scalar alpha/F2 counterexample",
        },
        {
            "source_id": "SRC1236_10_1114_no_hidden_visible",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "NHV1114_6_verdict",
            "purpose": "no-hidden-visible theorem remains unsigned",
        },
        {
            "source_id": "SRC1236_11_1115_invariant",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
            "needle": "LIA1115_6_verdict",
            "purpose": "local invariant algebra triviality not derived",
        },
        {
            "source_id": "SRC1236_12_988_em_lock",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv",
            "needle": "EMLOCK988_5_theorem_verdict",
            "purpose": "EM lock theorem gate remains conditional",
        },
        {
            "source_id": "SRC1236_13_989_em_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
            "needle": "ELA989_5_total",
            "purpose": "EM signature audit blocks promotion",
        },
        {
            "source_id": "SRC1236_14_1065_charge_norm",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv",
            "needle": "CIN1065_4_verdict",
            "purpose": "current/source normalization remains conditional",
        },
        {
            "source_id": "SRC1236_15_1232_edges",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv",
            "needle": "EDGE1232_2_quark_gluon",
            "purpose": "quark-gluon edge target",
        },
        {
            "source_id": "SRC1236_16_1232_fractions",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv",
            "needle": "FSP1232_4_QCD_gluon_fraction",
            "purpose": "QCD component fraction source gap",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    certificate = [
        {
            "clause_id": "CERT1236_0_parent_sorts",
            "certificate_clause": "Declare disjoint parent sorts before fitting: Q_obs, C_hid, Theta_rep, Top_level, Conn_vis, Coeff_vis[O], Readout.",
            "formal_effect": "Visible coefficient terms can only be formed from their declared argument sorts.",
            "proof_status": "GRAMMAR_CERTIFICATE_WRITTEN",
            "missing_for_derivation": "MTS primitive derivation of these sorts and their disjointness, not just a private discipline contract",
            "effect_if_parent_signed": "blocks arbitrary hidden scalar arguments by syntax",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_6_single_parent_action"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CERT1236_1_visible_coefficient_domain",
            "certificate_clause": "For every visible operator O_vis, Arg(Coeff_vis[O_vis]) subset Q_obs x Theta_rep x Top_level and contains no C_hid slot.",
            "formal_effect": "Terms c(I_hid)O_vis and f(I_hid)F_Q^2 are ill-typed, not dynamically tuned.",
            "proof_status": "EXACT_IF_PARENT_SIGNED_NOT_DERIVED",
            "missing_for_derivation": "parent object-language certificate that visible coefficients really use this restricted domain",
            "effect_if_parent_signed": "closes hidden-scalar part of unique-F2 blocker",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv", "PTOL1220_1_visible_coefficient_domain"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CERT1236_2_unique_EM_curvature_norm",
            "certificate_clause": "F_Q^2 descends only as the T_Q subblock of one parent curvature norm; no independent lambda_A F_Q^2 constructor exists.",
            "formal_effect": "Removes the independent visible Maxwell counterterm, not only hidden scalar dependence.",
            "proof_status": "REQUIRED_NOT_DERIVED",
            "missing_for_derivation": "parent-owned T_Q, fixed norm, and no-counterterm theorem",
            "effect_if_parent_signed": "closes independent lambda_A branch of unique-F2 blocker",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_1_unique_F2"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CERT1236_3_no_extension_marker",
            "certificate_clause": "No hidden marker, branch label, or domain selector may be retyped as Theta_rep or Top_level unless it is discrete, fixed, and parent-owned.",
            "formal_effect": "Prevents hidden scalar data from being smuggled back as a constant-like visible label.",
            "proof_status": "REQUIRED_NOT_DERIVED",
            "missing_for_derivation": "no-extension/no-marker theorem covering the surviving scalar obstruction list",
            "effect_if_parent_signed": "protects the typed-domain theorem against relabelled hidden arguments",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv", "TREQ1235_2_no_extension_marker"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CERT1236_4_radiative_readout_closure",
            "certificate_clause": "Renormalized/effective/readout maps preserve the same sorted domains and do not generate C_hid -> Coeff_vis morphisms.",
            "formal_effect": "Tree-level typed exclusion survives loop matching, clocks, spectroscopy, Hodge/coframe, and readout transfer.",
            "proof_status": "REQUIRED_NOT_DERIVED",
            "missing_for_derivation": "radiative/readout closure theorem or retained finite transfer priors",
            "effect_if_parent_signed": "prevents alpha drift from reappearing after EM-lock",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_5_radiative_readout_closure"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CERT1236_5_source_label_forgetting",
            "certificate_clause": "The gravitational source functor returns total Hilbert stress-energy, not per-species source weights or source-only labels.",
            "formal_effect": "Connects the typed coefficient certificate to WEP/R10/local-GR source-side reduction.",
            "proof_status": "CONDITIONAL_LEMMA_NOT_PARENT_DERIVED",
            "missing_for_derivation": "parent matter category that forgets species labels before source coupling selection",
            "effect_if_parent_signed": "would attack beta_source_alpha and relative source-weight residuals",
            "source": source_ref("source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_4_source_label_forgetting"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "CERT1236_6_current_verdict",
            "certificate_clause": "The exact certificate can be written, but the present corpus does not derive it from MTS primitives.",
            "formal_effect": "Useful private closure contract, not a theorem or public claim.",
            "proof_status": "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED",
            "missing_for_derivation": "derive the sorted action grammar from motion/time/space primitives or demote it explicitly to closure",
            "effect_if_parent_signed": "would reopen EM-lock and local source-coupling closure",
            "source": "CERT1236_0 through CERT1236_5",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    meta_theorem = [
        {
            "theorem_id": "META1236_0_statement",
            "statement": "If CERT1236_0 through CERT1236_4 are parent-signed, then Hom(C_hid,Coeff_vis[O_vis]) is absent for visible EM/matter/readout operators.",
            "proof_sketch": "A term can only be formed by a constructor with matching argument sorts; Coeff_vis constructors have no C_hid slot, and no extension marker can retype C_hid as representation/topological data.",
            "result": "EXACT_CONDITIONAL_META_THEOREM",
            "gap": "premises are not derived from MTS primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "META1236_1_unique_F2_consequence",
            "statement": "If the meta-theorem plus unique parent EM curvature norm are signed, then Lie_v g_EM^{-2}=0 and f(I_hid)F_Q^2/lambda_A F_Q^2 are unavailable.",
            "proof_sketch": "Hidden vertical vectors have no coefficient argument to act on, while the visible Maxwell normalization is fixed by the single parent curvature norm.",
            "result": "EXACT_CONDITIONAL_COROLLARY",
            "gap": "unique curvature norm and EM generator/current owner remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "META1236_2_local_GR_consequence",
            "statement": "If source label forgetting and matter pullback are also signed, local source coupling reduces to the total Hilbert stress source rather than composition weights.",
            "proof_sketch": "The variation of a single descended matter action with respect to g_obs(q) returns T_total; no species/source-only coefficient constructor exists.",
            "result": "EXACT_CONDITIONAL_COROLLARY",
            "gap": "matter category/source functor descent remains conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "META1236_3_public_status",
            "statement": "The certificate is not evidence unless MTS derives the premises; adopting it now is a private closure route only.",
            "proof_sketch": "A grammar restriction that is not derived from the theory can discipline future work, but cannot be scored as a prediction or theorem-zero.",
            "result": "NO_CLAIM_PROMOTION",
            "gap": "derivation source missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    unique_f2_status = [
        {
            "status_id": "UF2S1236_0_hidden_scalar_branch",
            "branch": "f(I_hid)F_Q^2",
            "after_certificate_attempt": "WOULD_CLOSE_IF_CERT_PARENT_SIGNED",
            "actual_status": "OPEN",
            "reason": "certificate written as exact grammar but not derived from MTS primitives",
            "next_required": "derive sorted coefficient domain from parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "UF2S1236_1_visible_counterterm_branch",
            "branch": "lambda_A F_Q^2",
            "after_certificate_attempt": "NOT_CLOSED_BY_HIDDEN_DOMAIN_ALONE",
            "actual_status": "OPEN",
            "reason": "unique curvature norm/no-independent-F2 theorem remains unsigned",
            "next_required": "parent EM curvature norm owner with no counterterm constructor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "UF2S1236_2_readout_branch",
            "branch": "measured alpha readout/radiative leakage",
            "after_certificate_attempt": "NOT_CLOSED_BY_TREE_GRAMMAR_ALONE",
            "actual_status": "OPEN",
            "reason": "readout and effective maps may reintroduce hidden dependence unless separately closed",
            "next_required": "radiative/readout closure theorem or finite transfer priors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "UF2S1236_3_verdict",
            "branch": "unique F_Q^2 total",
            "after_certificate_attempt": "SHARPENED_NOT_CLOSED",
            "actual_status": "UNIQUE_F2_REMAINS_BLOCKED",
            "reason": "certificate is schema-valid but not parent-derived; independent F2 and readout branches remain open",
            "next_required": "derive the certificate or keep finite EM residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    qcd_deepening = [
        {
            "qcd_id": "QCD1236_0_strong_sector_sorts",
            "object": "color gauge sector",
            "candidate_parent_form": "Conn_color, F_color, Rep_color[q], g_s level/norm, and a parent-owned gauge kinetic term",
            "would_prove": "strong-sector interaction is part of the same parent action rather than imported phenomenology",
            "current_status": "OWNER_CANDIDATE_WRITTEN_NOT_DERIVED",
            "gap": "no source row yet identifies the MTS parent color connection/norm owner",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "qcd_id": "QCD1236_1_color_current",
            "object": "quark-gluon interaction edge",
            "candidate_parent_form": "D_mu q = partial_mu q + i g_s A_mu^a T_a q and delta S/delta A_mu^a = J_a^mu",
            "would_prove": "a nonzero parent-owned color current connects quark and gluon/binding components",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "gap": "requires QCD1236_0 strong-sector owner",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "qcd_id": "QCD1236_2_bound_state_transfer",
            "object": "hadronization/material response",
            "candidate_parent_form": "map from quark/gluon Hamiltonian components to material energy fractions F_B,q and F_B,g",
            "would_prove": "color interaction edge becomes relevant to source-weight/WEP/R10 component response",
            "current_status": "TRANSFER_MAP_MISSING",
            "gap": "FSP1232_3/FSP1232_4 remain missing claim-grade component fractions",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "qcd_id": "QCD1236_3_no_QCD_source_prefactor",
            "object": "source coupling for QCD energy",
            "candidate_parent_form": "total Hilbert stress tensor from the same descended matter action, with no w_q or w_g source-only labels",
            "would_prove": "QCD sector does not introduce composition-dependent gravitational source weights",
            "current_status": "CONDITIONAL_SOURCE_LABEL_FORGETTING",
            "gap": "PAC1055_4 source-label forgetting is not parent-derived",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "qcd_id": "QCD1236_4_verdict",
            "object": "QCD color edge owner",
            "candidate_parent_form": "strong-sector owner + color current + bound-state transfer + total Hilbert source",
            "would_prove": "quark-gluon edge could count toward connected source graph",
            "current_status": "DEEPENED_BUT_NOT_SIGNED",
            "gap": "strong-sector owner and source-weight transfer are both missing",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_residuals = [
        {
            "residual_id": "FEMQCD1236_0_EM_alpha",
            "quantity": "b_alpha or c_alpha_DD",
            "source_of_residual": "typed certificate not parent-derived and unique-F2 remains blocked",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "parent-derived certificate or source-backed coefficient prior",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEMQCD1236_1_beta_source_alpha",
            "quantity": "beta_source_alpha",
            "source_of_residual": "source-label forgetting/current owner not parent-derived",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "single current/source owner or numeric beta prior with source path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEMQCD1236_2_readout_alpha",
            "quantity": "tau_clock/tau_WEP/readout alpha transfer",
            "source_of_residual": "radiative/readout closure not parent-derived",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "readout closure theorem or official transfer kernels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEMQCD1236_3_QCD_quark_fraction",
            "quantity": "F_B,q",
            "source_of_residual": "QCD bound-state transfer and component fractions missing",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "claim-grade quark energy fraction source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEMQCD1236_4_QCD_gluon_fraction",
            "quantity": "F_B,g",
            "source_of_residual": "gluon/binding energy fraction source missing",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "claim-grade gluon/binding fraction source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "FEMQCD1236_5_delta_w_qg",
            "quantity": "delta w_q and delta w_g",
            "source_of_residual": "QCD source prefactor zero theorem not parent-derived",
            "status": "FINITE_RESIDUAL_ACTIVE_NONCLAIM",
            "required_to_score": "source-label forgetting theorem or finite priors with sourced units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    edge_status = [
        {
            "edge_id": "EDGE1232_0_electron_photon",
            "prior_status": "BLOCKED_BY_UNIQUE_F2",
            "new_status": "BLOCKED_BY_CERTIFICATE_NOT_DERIVED",
            "reason": "typed certificate would close hidden branch but is not parent-derived; independent F2/readout branches remain open",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_1_quark_photon",
            "prior_status": "PENDING",
            "new_status": "PENDING",
            "reason": "not attempted in 1236",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_2_quark_gluon",
            "prior_status": "QCD_COLOR_EDGE_STAGED_NOT_SIGNED",
            "new_status": "DEEPENED_BUT_NOT_SIGNED",
            "reason": "strong-sector owner, bound-state transfer, and source-label forgetting remain missing",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1236_0_certificate_useful_not_claim",
            "decision": "keep typed certificate as private exact closure contract only",
            "because": "it cleanly kills hidden-visible coefficients if signed, but current MTS corpus does not derive the sorted grammar",
            "next_action": "try deriving the sorted action grammar from MTS primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1236_1_unique_F2_still_blocked",
            "decision": "do not close unique F_Q^2",
            "because": "hidden branch, independent F2 branch, and readout branch are not all parent-signed",
            "next_action": "retain finite EM residuals until certificate plus curvature norm plus readout closure exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1236_2_QCD_deepened_not_counted",
            "decision": "do not count QCD color edge for graph connectedness",
            "because": "color-current proof is conditional and material/source transfer is missing",
            "next_action": "derive strong-sector parent owner or source component-fraction rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1236_3_GR_route_requires_source_functor",
            "decision": "local GR/Newton reduction still hinges on total Hilbert source functor",
            "because": "source-label forgetting is the bridge from typed field theory to WEP/R10/PPN source universality",
            "next_action": "make source-label forgetting a derivation target, not a postulate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1236_0_parent_certificate",
            "claim": "parent typed object-language certificate is derived",
            "status": "BLOCKED",
            "reason": "CERT1236_6 verdict=CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1236_1_no_hidden_visible_coefficients",
            "claim": "Hom(C_hid,Coeff_vis)=absent as MTS theorem",
            "status": "BLOCKED",
            "reason": "meta-theorem premises are not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1236_2_unique_F2",
            "claim": "unique F_Q^2 closes",
            "status": "BLOCKED",
            "reason": "UF2S1236_3 verdict=UNIQUE_F2_REMAINS_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1236_3_QCD_color_edge",
            "claim": "quark-gluon edge parent-signed",
            "status": "BLOCKED",
            "reason": "QCD1236_4 verdict=DEEPENED_BUT_NOT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1236_4_graph_connectedness",
            "claim": "ordinary matter graph connected by signed parent edges",
            "status": "BLOCKED",
            "reason": "no edge counts for connected graph",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1236_5_Delta_w_zero",
            "claim": "Delta_w=0 theorem",
            "status": "BLOCKED",
            "reason": "finite EM/QCD residuals remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1236_6_WEP_R10_PPN_clock",
            "claim": "R10/WEP/PPN/clock local tests pass",
            "status": "BLOCKED",
            "reason": "source functor and coefficient/readout transfer not closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1236_7_local_GR",
            "claim": "local GR/Newton source-side reduction",
            "status": "BLOCKED",
            "reason": "total Hilbert source functor not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1236_0_1237",
            "target_file": "1237-Y5-R10-MTS-primitives-to-sorted-parent-action-derivation-or-closure-demotion.md",
            "target_script": "scripts/Y5_R10_MTS_primitives_to_sorted_parent_action_derivation_or_closure_demotion.py",
            "task": "attempt to derive the sorted parent action grammar from MTS primitives; if it cannot be derived, demote the typed certificate to an explicit closure assumption and keep finite EM/QCD source residuals for testing",
            "success_condition": "either a parent-derived grammar signs visible coefficient domains, unique curvature norm, readout closure, and source-label forgetting; or the closure assumption is clearly separated from derivable MTS content",
            "do_not_do": "do not claim EM lock, QCD edge, graph connectedness, Delta_w=0, WEP, PPN, clock, R10, local GR, or public victory from a private grammar contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        CERTIFICATE_PATH,
        META_THEOREM_PATH,
        UNIQUE_F2_STATUS_PATH,
        QCD_DEEPENING_PATH,
        FINITE_RESIDUAL_PATH,
        EDGE_STATUS_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(CERTIFICATE_PATH, certificate)
    write_csv(META_THEOREM_PATH, meta_theorem)
    write_csv(UNIQUE_F2_STATUS_PATH, unique_f2_status)
    write_csv(QCD_DEEPENING_PATH, qcd_deepening)
    write_csv(FINITE_RESIDUAL_PATH, finite_residuals)
    write_csv(EDGE_STATUS_PATH, edge_status)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            certificate,
            meta_theorem,
            unique_f2_status,
            qcd_deepening,
            finite_residuals,
            edge_status,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    certificate_written = any(row["clause_id"] == "CERT1236_0_parent_sorts" for row in certificate)
    certificate_not_derived = any(
        row["clause_id"] == "CERT1236_6_current_verdict"
        and row["proof_status"] == "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"
        for row in certificate
    )
    meta_conditional = all(row["result"] in {"EXACT_CONDITIONAL_META_THEOREM", "EXACT_CONDITIONAL_COROLLARY", "NO_CLAIM_PROMOTION"} for row in meta_theorem)
    unique_f2_blocked = any(
        row["status_id"] == "UF2S1236_3_verdict" and row["actual_status"] == "UNIQUE_F2_REMAINS_BLOCKED"
        for row in unique_f2_status
    )
    qcd_deepened_not_signed = any(
        row["qcd_id"] == "QCD1236_4_verdict" and row["current_status"] == "DEEPENED_BUT_NOT_SIGNED"
        for row in qcd_deepening
    )
    finite_backstop_active = len(finite_residuals) == 6 and all(
        row["status"] == "FINITE_RESIDUAL_ACTIVE_NONCLAIM" for row in finite_residuals
    )
    no_edges_signed = all(parse_bool(row["counts_for_connected_graph"]) is False for row in edge_status)
    gates_blocked = all(row["status"] == "BLOCKED" and is_false(row, "claim_allowed") for row in claim_gates)
    next_is_1237 = next_target[0]["target_file"].startswith("1237-Y5-R10-MTS-primitives")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1236_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1236_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1236_2_certificate_written",
            "typed certificate clauses are written",
            certificate_written,
            "CERT1236_0 through CERT1236_6 generated",
        ),
        validation_row(
            "VAL1236_3_certificate_not_derived",
            "certificate is not promoted as parent-derived",
            certificate_not_derived,
            "CERT1236_6 status=CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED",
        ),
        validation_row(
            "VAL1236_4_meta_theorem_conditional",
            "no-hidden-visible theorem remains conditional",
            meta_conditional,
            "meta theorem rows do not permit claim promotion",
        ),
        validation_row(
            "VAL1236_5_unique_F2_blocked",
            "unique-F2 remains blocked",
            unique_f2_blocked,
            "UF2S1236_3 status=UNIQUE_F2_REMAINS_BLOCKED",
        ),
        validation_row(
            "VAL1236_6_QCD_deepened_not_signed",
            "QCD route is deepened but not signed",
            qcd_deepened_not_signed,
            "QCD1236_4 status=DEEPENED_BUT_NOT_SIGNED",
        ),
        validation_row(
            "VAL1236_7_finite_backstop",
            "finite EM/QCD residuals remain active",
            finite_backstop_active,
            f"finite_residual_rows={len(finite_residuals)}",
        ),
        validation_row(
            "VAL1236_8_no_edges_signed",
            "no graph edge is counted as parent-signed",
            no_edges_signed,
            "counts_for_connected_graph=false for all updated edges",
        ),
        validation_row(
            "VAL1236_9_claim_gates_blocked",
            "all claim gates remain blocked",
            gates_blocked,
            f"blocked_gates={sum(row['status'] == 'BLOCKED' for row in claim_gates)}/{len(claim_gates)}",
        ),
        validation_row(
            "VAL1236_10_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1236_11_next_target_1237",
            "next target derives grammar from MTS primitives or demotes closure",
            next_is_1237,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1236_12_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1236_13_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1236_14_overall",
            "overall 1236 validation",
            all(row["status"] == "PASS" for row in validation),
            "1236 writes the exact typed certificate, refuses to promote it without derivation, deepens QCD owner requirements, and keeps local-GR gates blocked",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1236 writes the exact parent typed object-language certificate, but it does **not** derive it from MTS primitives. So it is a strong private closure contract, not yet a theorem.",
        "",
        "**Main progress:** the missing object is now brutally explicit: sorted parent action grammar, visible coefficient domains, unique EM curvature norm, no-extension marker, radiative/readout closure, and source-label forgetting. QCD is deepened into a strong-sector owner route, but still not signed.",
        "",
        "**No-claim guard:** no EM lock, QCD edge, graph connectedness, `Delta_w=0`, R10, WEP, PPN, clock, orbital, local-GR, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Parent Typed Object-Language Certificate Attempt",
        markdown_table(certificate, list(certificate[0].keys())),
        "",
        "## No Hidden-Visible Coefficient Meta-Theorem",
        markdown_table(meta_theorem, list(meta_theorem[0].keys())),
        "",
        "## Unique F2 Status After Certificate",
        markdown_table(unique_f2_status, list(unique_f2_status[0].keys())),
        "",
        "## QCD Color Owner Deepening",
        markdown_table(qcd_deepening, list(qcd_deepening[0].keys())),
        "",
        "## Finite EM/QCD Residual Backstop",
        markdown_table(finite_residuals, list(finite_residuals[0].keys())),
        "",
        "## Graph Edge Status Update",
        markdown_table(edge_status, list(edge_status[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
