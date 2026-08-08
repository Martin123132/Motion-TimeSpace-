from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "753-Y5-R10-Palpha3-source-pack-or-parent-zero-theorem.md"
NEXT_TARGET = "754-Y5-R10-q_loc-parent-kernel-signature-or-preferred-frame-source-fill.md"
STATUS = "Y5_R10_753_parent_zero_theorem_written_not_signed_external_PPN_source_pack_recorded_nonclaim"
CLAIM_CEILING = "conditional_parent_zero_theorem_and_external_PPN_source_pack_only_no_fqV_no_Wqalpha3_no_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_753_SOURCE_REGISTER.csv"
EXTERNAL_SOURCE_PACK_PATH = RESIDUALS / "P8_Y5_R10_753_EXTERNAL_PPN_SOURCE_PACK.csv"
ZERO_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_753_PARENT_ZERO_THEOREM_ATTEMPT.csv"
CLAUSE_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_753_ZERO_CLAUSE_SIGNATURE_MATRIX.csv"
GAP_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_753_SOURCE_PACK_GAP_LEDGER.csv"
PRODUCT_DECISION_PATH = RESIDUALS / "P8_Y5_R10_753_QLOC_ALPHA3_PRODUCT_DECISION.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_753_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_753_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_753_VALIDATION.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "752_doc": {
        "path": POST_CHECKPOINT / "752-Y5-R10-Palpha3-operator-source-hunt-or-q_loc-template-dryrun.md",
        "needles": [
            "local source hunt does not find an executable `P_alpha3` chain",
            "P_flux, G_PPN, Pi_alpha3^PPN, and q_loc component input remain missing",
            "753-Y5-R10-Palpha3-source-pack-or-parent-zero-theorem.md",
        ],
        "role": "immediate 753 handoff",
    },
    "752_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_752_VALIDATION.csv",
        "needles": ["V752_16_validation_rows_ready", "V752_13_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "752_operator_hunt": {
        "path": RESIDUALS / "P8_Y5_R10_752_PALPHA3_OPERATOR_SOURCE_HUNT.csv",
        "needles": ["OSH752_5_verdict", "P_flux, G_PPN, Pi_alpha3^PPN, and q_loc component input remain missing"],
        "role": "operator source hunt failure",
    },
    "752_piece_status": {
        "path": RESIDUALS / "P8_Y5_R10_752_OPERATOR_PIECE_STATUS.csv",
        "needles": ["OPS752_4_W_q_alpha3", "not_computed"],
        "role": "operator piece status",
    },
    "752_requirements": {
        "path": RESIDUALS / "P8_Y5_R10_752_SOURCE_REQUIREMENTS_QUEUE.csv",
        "needles": ["REQ752_2_green_operator", "REQ752_3_ppn_projection"],
        "role": "missing source requirement queue",
    },
    "752_product": {
        "path": RESIDUALS / "P8_Y5_R10_752_QLOC_ALPHA3_PRODUCT_STATUS.csv",
        "needles": ["QAP752_3_gate", "not_scoreable"],
        "role": "alpha3 product blocker",
    },
    "748_doc": {
        "path": POST_CHECKPOINT / "748-Y5-R10-q_loc-vector-parity-zero-theorem-or-Wqalpha3-source-row.md",
        "needles": [
            "vector parity zero theorem has a clean conditional form",
            "valid_for_claim",
            "parity_zero_failed_current_corpus",
        ],
        "role": "prior parity zero attempt",
    },
    "747_zero_audit": {
        "path": RESIDUALS / "P8_Y5_R10_747_ALPHA3_QLOC_ZERO_THEOREM_AUDIT.csv",
        "needles": ["AZ747_2_momentum_map", "zero_theorem_failed_current_corpus"],
        "role": "prior q_loc alpha3 zero audit",
    },
    "751_operator_contract": {
        "path": RESIDUALS / "P8_Y5_R10_751_MINIMAL_PALPHA3_OPERATOR_CONTRACT.csv",
        "needles": ["PA3751_4_minimal_composition", "P_alpha3_min"],
        "role": "minimal Palpha3 composition",
    },
    "momentum_map_theorem": {
        "path": RESIDUALS / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv",
        "needles": ["MMT582_4_no_pole_result", "conditional_theorem_only"],
        "role": "vertical momentum-map closure attempt",
    },
    "momentum_map_contract": {
        "path": RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
        "needles": ["NMC583_1_vertical_generator", "NMC583_5_boundary_zero"],
        "role": "Noether momentum-map required objects",
    },
    "momentum_owner_test": {
        "path": RESIDUALS / "P8_Y5_R10_586_MOMENTUM_MAP_OWNER_TEST.csv",
        "needles": ["MMT586_4_matter_factorization", "blocked"],
        "role": "momentum-map owner blocker",
    },
    "ppn_metric_contract": {
        "path": RESIDUALS / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv",
        "needles": ["MEX524_3_gravitomagnetic_preferred_frame", "alpha1=alpha2=alpha3=0"],
        "role": "local PPN alpha_i metric gate",
    },
    "ppn_source_gates": {
        "path": RESIDUALS / "P8_Y5_PPN_SOURCE_STABILITY_GATES.csv",
        "needles": ["PSG524_6_preferred_frame_location_zero", "not_derived_not_scored"],
        "role": "PPN preferred-frame gate",
    },
    "r11_vector_status": {
        "path": RESIDUALS / "R11_EXECUTABLE_VECTOR_STATUS.csv",
        "needles": ["vector_preferred_frame", "template_only"],
        "role": "R11 vector/preferred-frame blocker",
    },
}


EXTERNAL_SOURCES = [
    {
        "external_id": "EXT753_0_Will_2014_LRR",
        "source_title": "The Confrontation between General Relativity and Experiment",
        "authors": "Clifford M. Will",
        "year": "2014",
        "url": "https://arxiv.org/abs/1403.7377",
        "doi_or_record": "10.12942/lrr-2014-4",
        "use_in_753": "modern review source for PPN framework, preferred-frame parameters, and experimental context",
        "what_it_does_not_provide": "does not by itself derive MTS q_loc -> alpha3 response coefficient",
        "source_confidence": "high",
        "valid_for_claim": "false",
    },
    {
        "external_id": "EXT753_1_Will_2006_LRR",
        "source_title": "The Confrontation between General Relativity and Experiment",
        "authors": "Clifford M. Will",
        "year": "2006",
        "url": "https://arxiv.org/abs/gr-qc/0510072",
        "doi_or_record": "10.12942/lrr-2006-3",
        "use_in_753": "stable PPN review anchor and published Living Reviews reference",
        "what_it_does_not_provide": "does not fill P_flux, G_PPN, or Pi_alpha3 for the MTS parent action",
        "source_confidence": "high",
        "valid_for_claim": "false",
    },
    {
        "external_id": "EXT753_2_Will_Nordtvedt_1972_PPN_I",
        "source_title": "Conservation Laws and Preferred Frames in Relativistic Gravity. I. Preferred-frame theories and an extended PPN formalism",
        "authors": "Clifford M. Will; Kenneth Nordtvedt Jr.",
        "year": "1972",
        "url": "https://adsabs.harvard.edu/full/1972ApJ...177..757W",
        "doi_or_record": "Astrophys. J. 177, 757",
        "use_in_753": "original extended PPN/preferred-frame formalism anchor",
        "what_it_does_not_provide": "does not provide an MTS-specific response operator",
        "source_confidence": "high",
        "valid_for_claim": "false",
    },
    {
        "external_id": "EXT753_3_Nordtvedt_Will_1972_PPN_II",
        "source_title": "Conservation laws and preferred frames in relativistic gravity. II - Experimental evidence to rule out preferred-frame theories of gravity",
        "authors": "Kenneth Nordtvedt Jr.; Clifford M. Will",
        "year": "1972",
        "url": "https://ntrs.nasa.gov/citations/19730042524",
        "doi_or_record": "NASA NTRS 19730042524 / Astrophys. J. 177, 775-792",
        "use_in_753": "original preferred-frame experimental-effects source; useful for alpha_i source-pack provenance",
        "what_it_does_not_provide": "does not prove q_loc is absent/gauge/even in MTS",
        "source_confidence": "high",
        "valid_for_claim": "false",
    },
    {
        "external_id": "EXT753_4_Damour_Schaefer_alpha3",
        "source_title": "A new test of conservation laws and Lorentz invariance in relativistic gravity",
        "authors": "Thibault Damour; Gerhard Schaefer",
        "year": "1990s",
        "url": "https://repo-archives.ihes.fr/FONDS_IHES/I_Prepublications/DAMOUR/1994-1998/P_96_36/P_96_36.pdf",
        "doi_or_record": "IHES preprint PDF",
        "use_in_753": "alpha3-specific pulsar/preferred-frame motivation source",
        "what_it_does_not_provide": "does not substitute for parent MTS weak-field derivation",
        "source_confidence": "medium",
        "valid_for_claim": "false",
    },
]


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def external_source_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [{**row, "generated_utc": generated_utc} for row in EXTERNAL_SOURCES]


def zero_theorem_rows(generated_utc: str) -> list[dict[str, Any]]:
    theorem_statement = (
        "If the parent action has no non-dynamical preferred-frame datum, matter descends to a single observed metric/coframe, "
        "q_loc is either scalar/even or a vertical first-class constraint with zero boundary charge, and the weak-field PPN map is "
        "linear in the q_loc vector-flux source, then P_alpha3(q_loc)=0."
    )
    proof_chain = "P_Hodge q_loc has no transverse/harmonic momentum-flux component => P_flux=0 => G_PPN(0)=0 => Pi_alpha3^PPN(0)=0"
    return [
        {
            "theorem_id": "PZT753_0_best_shot_statement",
            "route": "parent_zero_theorem",
            "mathematical_form": theorem_statement,
            "proof_obligation": "sign all ZCS753 clauses from parent action and matter coupling",
            "current_status": "conditional_theorem_written_not_parent_signed",
            "claim_effect_if_signed": "alpha3_q_loc=0 without tuning W_q_alpha3 or f_qV",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "PZT753_1_kernel_factorization",
            "route": "operator_kernel_route",
            "mathematical_form": proof_chain,
            "proof_obligation": "prove q_loc enters ker(P_flux o P_Hodge) or prove P_flux annihilates q_loc by Noether/constraint identity",
            "current_status": "blocked_by_missing_q_loc_component_and_vertical_owner",
            "claim_effect_if_signed": "f_qV=0 and alpha3 product is theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "PZT753_2_no_prior_frame_route",
            "route": "no_preferred_frame_parent_route",
            "mathematical_form": "S_parent[Y] and S_matter[Psi, q(Y)] contain no fixed u^mu, foliation, domain vector, projector stress, or asymptotic preferred-frame datum through PPN order",
            "proof_obligation": "audit parent and observed matter action for every vector/domain/projector/readout term",
            "current_status": "blocked_by_R11_vector_template_and_PPN_source_gate",
            "claim_effect_if_signed": "alpha1=alpha2=alpha3=xi preferred-frame/location slots are absent rather than numerically suppressed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "PZT753_3_external_source_pack_result",
            "route": "PPN_source_pack",
            "mathematical_form": "external PPN sources identify what alpha3 means and why preferred-frame channels are dangerous",
            "proof_obligation": "derive the MTS-specific map from q_loc/source terms into the cited PPN alpha3 slot",
            "current_status": "source_pack_recorded_not_operator_derivation",
            "claim_effect_if_signed": "can normalize future W_q_alpha3 derivation against standard PPN conventions",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "PZT753_4_verdict",
            "route": "claim_alpha3_q_loc_zero_now",
            "mathematical_form": "P_alpha3(q_loc)=0",
            "proof_obligation": "all theorem clauses signed or numeric product below 5.38167370680806e-15",
            "current_status": "zero_theorem_not_claimed_current_corpus",
            "claim_effect_if_signed": "local alpha3 pressure removed; beta/gamma/R10 still separate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def clause_matrix_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "ZCS753_0_no_fixed_preferred_datum",
            "needed_clause": "no non-dynamical preferred vector/foliation/domain stress in the parent or readout action",
            "mathematical_form": "delta S / delta u_fixed = absent; fields transform covariantly; no prior frame in boundary conditions",
            "local_evidence": str(RESIDUALS / "R11_EXECUTABLE_VECTOR_STATUS.csv"),
            "current_signature": "not_signed_R11_vector_template_only",
            "blocks": "no_prior_frame_route; Pi_alpha3_zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZCS753_1_metric_matter_descent",
            "needed_clause": "matter descends to one observed metric/coframe and does not couple to q_loc vector representatives",
            "mathematical_form": "S_matter = Sbar[Psi, g_obs(q(Y))] and delta_{ker Dq} S_matter=0 through PPN order",
            "local_evidence": str(RESIDUALS / "P8_Y5_R10_586_MOMENTUM_MAP_OWNER_TEST.csv"),
            "current_signature": "not_derived_blocked",
            "blocks": "matter_evenness; WEP local-GR branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZCS753_2_q_loc_kernel_or_scalar_even",
            "needed_clause": "q_loc has no physical vector/momentum flux component in compact local branch",
            "mathematical_form": "P_flux P_Hodge q_loc=0, equivalently f_qV=0, from parent equations not from q_proxy",
            "local_evidence": str(RESIDUALS / "P8_Y5_R10_752_SOURCE_REQUIREMENTS_QUEUE.csv"),
            "current_signature": "missing_component_input_and_flux_projector",
            "blocks": "f_qV; product theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZCS753_3_vertical_first_class_owner",
            "needed_clause": "q_loc vector branch is a vertical gauge/constraint direction with no local charge",
            "mathematical_form": "i_v Omega = delta G, G=int epsilon C_q + Q_boundary, {G,G}=G+K_boundary, Q_boundary=K_boundary=0",
            "local_evidence": str(RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv"),
            "current_signature": "missing_symplectic_potential_vertical_generator_boundary_zero",
            "blocks": "kernel route; local odd charge zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZCS753_4_boundary_and_harmonic_silence",
            "needed_clause": "compact local boundary and harmonic pieces cannot leak into preferred-frame flux",
            "mathematical_form": "Q_boundary=0 and q_H=0 or Pi_alpha3(q_H)=0 under allowed boundary conditions",
            "local_evidence": str(RESIDUALS / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv"),
            "current_signature": "boundary_not_silenced",
            "blocks": "P_flux; alpha3 no-flux route",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZCS753_5_ppn_projection_normalization",
            "needed_clause": "standard PPN alpha3 extraction is sourced and MTS weak-field map lands in its zero slot",
            "mathematical_form": "delta g_0i[q_loc] has no alpha3 basis coefficient after observed-frame gauge fixing",
            "local_evidence": str(RESIDUALS / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv"),
            "current_signature": "metric_contract_written_not_computed",
            "blocks": "W_q_alpha3; Pi_alpha3^PPN",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZCS753_6_conservation_self_acceleration_silence",
            "needed_clause": "no anomalous self-acceleration/conservation-law-violating q_loc source survives",
            "mathematical_form": "nabla_mu T^{mu nu}=0 in observed frame and no alpha3 self-acceleration source term from q_loc",
            "local_evidence": str(RESIDUALS / "P8_Y5_PPN_SOURCE_STABILITY_GATES.csv"),
            "current_signature": "not_derived_not_scored",
            "blocks": "alpha3 physical interpretation and local-GR branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ZCS753_7_verdict",
            "needed_clause": "all zero theorem clauses are parent signed",
            "mathematical_form": "ZCS753_0..ZCS753_6 all true => alpha3_q_loc=0",
            "local_evidence": "this audit",
            "current_signature": "failed_current_corpus",
            "blocks": "alpha3/PPN/R10/Newton/local-GR claim promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gap_ledger_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gap_id": "GAP753_0_PPN_convention_source",
            "missing_object": "PPN alpha3 convention/extraction source",
            "current_progress": "external review/original PPN sources recorded",
            "minimum_fill": "specific equation/section mapped to Pi_alpha3^PPN in local notation",
            "safe_action": "source exact formula before computing W_q_alpha3",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gap_id": "GAP753_1_MTS_weak_field_equations",
            "missing_object": "G_PPN for MTS q_loc",
            "current_progress": "no gauge-fixed weak-field Green operator found",
            "minimum_fill": "linearized field equations in observed frame with q_loc source term and boundary conditions",
            "safe_action": "derive from parent action, not fit to alpha3 bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gap_id": "GAP753_2_flux_projector",
            "missing_object": "P_flux and f_qV",
            "current_progress": "operator skeleton exists; no q_loc component input or projector source",
            "minimum_fill": "component-resolved q_loc field/profile or theorem P_flux P_Hodge q_loc=0",
            "safe_action": "prove kernel first; otherwise keep numeric branch blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gap_id": "GAP753_3_parent_kernel_signature",
            "missing_object": "ker(Dq) / vertical owner / matter descent signature",
            "current_progress": "momentum-map and quotient clauses remain templates or blocked",
            "minimum_fill": "parent variation showing q_loc vector branch is gauge or absent from matter readout",
            "safe_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def product_decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "QAP753_0_product_gate_retained",
            "quantity": "abs(W_q_alpha3*f_qV)",
            "value": f"must_be <= {WF_LIMIT:.15g}",
            "status_after_753": "retained_not_scoreable",
            "reason": "zero theorem is conditional and numeric source pack does not fill MTS operator",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "QAP753_1_external_sources_nonclaim",
            "quantity": "external PPN source pack",
            "value": "recorded",
            "status_after_753": "useful_for_convention_not_for_MTS_coefficient",
            "reason": "external sources define alpha3 context; they do not derive q_loc projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "QAP753_2_zero_theorem_nonclaim",
            "quantity": "P_alpha3(q_loc)",
            "value": "conditional_zero_only",
            "status_after_753": "not_parent_signed",
            "reason": "kernel/no-prior-frame/matter-descent/boundary/PPN clauses remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU753_0_allowed",
            "allowed_after_753": "say best-shot parent zero theorem has been written as a conditional sufficient theorem",
            "forbidden_after_753": "say alpha3, PPN, R10, Newton, or local-GR passes",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU753_1_allowed",
            "allowed_after_753": "use external PPN sources as convention/provenance anchors",
            "forbidden_after_753": "treat external PPN reviews as an MTS W_q_alpha3 calculation",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU753_2_allowed",
            "allowed_after_753": "attack q_loc parent-kernel signature next",
            "forbidden_after_753": "run product evaluator with missing W_q_alpha3 or f_qV",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "conditional parent zero theorem written; external PPN source pack recorded; no claim promoted",
            "hard_blocker": "no parent-signed proof that q_loc lies in the alpha3 kernel and no MTS weak-field alpha3 operator",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    external: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    product: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V753_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V753_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_752 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_752_VALIDATION.csv")
    validation.append({"check_id": "V753_2_prior_752_clean", "result": "pass" if prior_752 and all(row.get("result") == "pass" for row in prior_752) else "fail", "detail": "752 validation has no failures"})
    validation.append({"check_id": "V753_3_external_source_pack_recorded", "result": "pass" if len(external) >= 4 and all(row["url"].startswith("https://") for row in external) else "fail", "detail": "PPN/preferred-frame external URLs recorded"})
    validation.append({"check_id": "V753_4_zero_theorem_written_not_promoted", "result": "pass" if any(row["theorem_id"] == "PZT753_0_best_shot_statement" and row["valid_for_claim"] == "false" for row in theorem) else "fail", "detail": "conditional theorem row exists and is nonclaim"})
    validation.append({"check_id": "V753_5_claim_zero_blocked", "result": "pass" if any(row["theorem_id"] == "PZT753_4_verdict" and row["current_status"] == "zero_theorem_not_claimed_current_corpus" for row in theorem) else "fail", "detail": "Palpha3 q_loc zero not claimed"})
    validation.append({"check_id": "V753_6_clause_matrix_complete", "result": "pass" if len(clauses) == 8 and all(row["current_signature"] != "signed" for row in clauses) else "fail", "detail": "zero theorem clauses remain unsigned"})
    validation.append({"check_id": "V753_7_gap_ledger_written", "result": "pass" if len(gaps) == 4 and all(row["valid_for_claim"] == "false" for row in gaps) else "fail", "detail": "four source/derivation gaps queued"})
    validation.append({"check_id": "V753_8_product_gate_retained", "result": "pass" if any(row["decision_id"] == "QAP753_0_product_gate_retained" and row["status_after_753"] == "retained_not_scoreable" for row in product) else "fail", "detail": f"WF_limit={WF_LIMIT:.15g}"})
    all_generated = external + theorem + clauses + gaps + product + routes + summary
    validation.append({"check_id": "V753_9_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V753_10_no_local_arena_claim", "result": "pass" if "no_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "alpha3/PPN/R10/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V753_11_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) else "fail", "detail": NEXT_TARGET})
    output_paths = [OUTPUT_DOC, SOURCE_REGISTER_PATH, EXTERNAL_SOURCE_PACK_PATH, ZERO_THEOREM_PATH, CLAUSE_MATRIX_PATH, GAP_LEDGER_PATH, PRODUCT_DECISION_PATH, ROUTE_PATH, SUMMARY_PATH, VALIDATION_PATH]
    validation.append({"check_id": "V753_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V753_13_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V753_14_external_not_treated_as_operator", "result": "pass" if all(row["valid_for_claim"] == "false" and "does not" in row["what_it_does_not_provide"] for row in external) else "fail", "detail": "external sources are provenance only"})
    validation.append({"check_id": "V753_15_route_forbids_missing_product_eval", "result": "pass" if any("run product evaluator with missing W_q_alpha3 or f_qV" in row["forbidden_after_753"] for row in routes) else "fail", "detail": "do not run evaluator with missing products"})
    validation.append({"check_id": "V753_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    external: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    product: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 753 - Y5 R10 Palpha3 Source Pack Or Parent Zero Theorem

Start point: 752 showed that the local corpus does not contain an executable

```text
P_alpha3_min := Pi_alpha3^PPN o G_PPN o P_flux o P_Hodge
```

Current result: **best shot taken, but no claim promoted**. The clean theorem route is now explicit:

```text
P_Hodge q_loc has no physical vector/flux component
=> P_flux = 0
=> G_PPN(0) = 0
=> Pi_alpha3^PPN(0) = 0
=> alpha3_q_loc = 0
```

That would be a serious kill-switch for the alpha3 branch, but the current corpus does not yet sign the clauses that make the first arrow true. The external PPN source pack is useful for convention/provenance, not enough to compute `W_q_alpha3` for MTS.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Parent Zero Theorem Attempt

{markdown_table(theorem, ["theorem_id", "route", "mathematical_form", "proof_obligation", "current_status", "claim_effect_if_signed", "valid_for_claim"])}

## Zero Clause Signature Matrix

{markdown_table(clauses, ["clause_id", "needed_clause", "mathematical_form", "current_signature", "blocks", "valid_for_claim"])}

## External PPN Source Pack

{markdown_table(external, ["external_id", "source_title", "authors", "year", "url", "doi_or_record", "use_in_753", "what_it_does_not_provide", "valid_for_claim"])}

## Source Pack Gap Ledger

{markdown_table(gaps, ["gap_id", "missing_object", "current_progress", "minimum_fill", "safe_action", "valid_for_claim"])}

## q_loc Alpha3 Product Decision

{markdown_table(product, ["decision_id", "quantity", "value", "status_after_753", "reason", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_753", "forbidden_after_753", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This was the right punch to throw: if we can prove `q_loc` is in the parent kernel of the preferred-frame projector, alpha3 stops being a numerical panic and becomes an exact zero. But 753 does not let us claim that yet. The real next bite is smaller and sharper: prove `P_flux P_Hodge q_loc = 0` from the parent kernel / matter descent / boundary silence, or accept that the preferred-frame source has to be filled numerically.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    external = external_source_rows(generated_utc)
    theorem = zero_theorem_rows(generated_utc)
    clauses = clause_matrix_rows(generated_utc)
    gaps = gap_ledger_rows(generated_utc)
    product = product_decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, external, theorem, clauses, gaps, product, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(EXTERNAL_SOURCE_PACK_PATH, external, ["external_id", "source_title", "authors", "year", "url", "doi_or_record", "use_in_753", "what_it_does_not_provide", "source_confidence", "valid_for_claim", "generated_utc"])
    write_csv(ZERO_THEOREM_PATH, theorem, ["theorem_id", "route", "mathematical_form", "proof_obligation", "current_status", "claim_effect_if_signed", "valid_for_claim", "generated_utc"])
    write_csv(CLAUSE_MATRIX_PATH, clauses, ["clause_id", "needed_clause", "mathematical_form", "local_evidence", "current_signature", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(GAP_LEDGER_PATH, gaps, ["gap_id", "missing_object", "current_progress", "minimum_fill", "safe_action", "valid_for_claim", "generated_utc"])
    write_csv(PRODUCT_DECISION_PATH, product, ["decision_id", "quantity", "value", "status_after_753", "reason", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_753", "forbidden_after_753", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, external, theorem, clauses, gaps, product, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        print(f"wrote {OUTPUT_DOC}")
        print(f"wrote {VALIDATION_PATH}")
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
