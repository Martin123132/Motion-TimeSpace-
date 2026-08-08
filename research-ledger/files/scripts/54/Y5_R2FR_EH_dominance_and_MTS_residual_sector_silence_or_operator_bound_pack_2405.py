from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_EH_DOMINANCE_AND_MTS_RESIDUAL_SECTOR_SILENCE_OR_OPERATOR_BOUND_PACK_2405"
SCRIPT_PATH = Path(__file__).resolve()
POST_ROOT = SCRIPT_PATH.parents[1]
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
FORMALIZATION_ROOT = POST_ROOT.parent / "formalization-workbench"
DOC_PATH = POST_ROOT / "2405-Y5-R2FR-EH-dominance-and-MTS-residual-sector-silence-or-operator-bound-pack.md"


def post(path: str) -> Path:
    return POST_ROOT / path


SOURCES = [
    {
        "source_id": "SRC2405_2404_doc",
        "path": str(post("2404-Y5-R2FR-minimal-parent-action-first-variation-GR-Newton-gate-or-operator-residual-pack.md")),
        "needles": "NEXT2404_0_selected|DeltaE_MTS|OR2404_0_DeltaE_MTS|VAL2404_OVERALL",
        "role": "immediate parent: first variation and selected residual silence target",
    },
    {
        "source_id": "SRC2405_2404_variation",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2404_FIRST_VARIATION_LEDGER.csv")),
        "needles": "FV2404_3_silent_sector_variation|FV2404_5_field_equation|DeltaE_MTS",
        "role": "candidate variation source for DeltaE_MTS",
    },
    {
        "source_id": "SRC2405_2404_residuals",
        "path": str(post("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2404_OPERATOR_RESIDUAL_PACK.csv")),
        "needles": "OR2404_0_DeltaE_MTS|OR2404_1_DeltaE_boundary|OR2404_4_ppn_residual",
        "role": "operator residual pack",
    },
    {
        "source_id": "SRC2405_1770_doc",
        "path": str(post("1770-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md")),
        "needles": "EHD1770_0_target|RSS1770_6_verdict|OPC1770_0_total_DeltaE|VAL1770_OVERALL",
        "role": "earlier EH dominance theorem attempt",
    },
    {
        "source_id": "SRC2405_1840_doc",
        "path": str(post("1840-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md")),
        "needles": "EHD1840_0_target|RSS1840_6_verdict|OPC1840_0_total_DeltaE|VAL1840_OVERALL",
        "role": "consolidated EH dominance and operator coefficient pack",
    },
    {
        "source_id": "SRC2405_2235_doc",
        "path": str(post("2235-Y5-R2FR-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md")),
        "needles": "STR2235_1_multiplier_metric_stress|ROUTE2235_1_second_class_auxiliary|VAL2235_OVERALL",
        "role": "constraint/auxiliary zero-stress warning",
    },
    {
        "source_id": "SRC2405_2395_doc",
        "path": str(post("2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md")),
        "needles": "EHK2395_1_chain_rule_EH_silence|EHK2395_6_verdict|VAL2395_OVERALL",
        "role": "EH reference/kernel guardrail",
    },
    {
        "source_id": "SRC2405_2300_doc",
        "path": str(post("2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md")),
        "needles": "QSLOT2300_0_EH_GR|QEUL2300_3_residual_source_vector|QRES2300_8_total|VAL2300_OVERALL",
        "role": "q-sector source-vector residual precedent",
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


def dominance_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHD2405_0_target",
            "claim_piece": "EH dominance",
            "mathematical_form": "E_LHS^{mu nu}=G^{mu nu}+Lambda g^{mu nu}+DeltaE_MTS^{mu nu}+DeltaE_boundary^{mu nu}",
            "zero_condition": "DeltaE_MTS^{mu nu}=0 and DeltaE_boundary^{mu nu}=0 on the local branch",
            "current_result": "TARGET_EXACT",
            "remaining_gap": "must silence each retained MTS residual owner without EH-import laundering",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHD2405_1_sufficient_theorem",
            "claim_piece": "sector silence sufficient theorem",
            "mathematical_form": "If every S_i in S_silent is topological, first-class pure gauge with zero boundary charge, algebraic auxiliary zero-stress, or local higher-order bounded, then DeltaE_MTS=sum_i delta S_i/delta e=0/bounded",
            "zero_condition": "sector-by-sector certificates plus shared boundary/falloff class",
            "current_result": "CONDITIONAL_THEOREM",
            "remaining_gap": "certificates are not yet supplied for all retained sectors",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHD2405_2_lambda_warning",
            "claim_piece": "constraint multiplier stress warning",
            "mathematical_form": "delta_g int sqrt(-g) lambda C gives lambda delta_g C plus metric-volume terms; C=0 alone does not force zero stress",
            "zero_condition": "lambda=0 on branch, C metric-independent/topological, or second-class auxiliary elimination is stress-silent",
            "current_result": "SHORTCUT_REJECTED",
            "remaining_gap": "lambda_R/R_AB path previously failed parent-origin and zero-stress promotion",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHD2405_3_bianchi",
            "claim_piece": "Noether/Bianchi compatibility",
            "mathematical_form": "nabla_mu(G^{mu nu}+Lambda g^{mu nu})=0 requires nabla_mu(DeltaE_MTS+DeltaE_boundary-kappa J_shadow)^{mu nu}=0",
            "zero_condition": "residuals vanish, are separately conserved and bounded, or are parent-Noether paired",
            "current_result": "CONDITIONAL_FILTER",
            "remaining_gap": "not enough to prove zero; conserved nonzero residuals still affect PPN/Newton",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "EHD2405_4_current_verdict",
            "claim_piece": "current MTS EH dominance",
            "mathematical_form": "DeltaE_MTS=0 in the local branch",
            "zero_condition": "all sector rows in RSS2405 pass zero/silence or bound below local thresholds",
            "current_result": "NOT_PROVED_CURRENT_CORPUS",
            "remaining_gap": "operator coefficient pack remains live",
            "valid_for_claim": "false",
        },
    ]


def residual_sector_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS2405_0_higher_derivative",
            "sector": "higher-curvature / higher-derivative geometry",
            "operator_form": "c_R2 R^2 + c_Ricci2 R_munu R^munu + c_boxR R box R + ...",
            "silence_route": "derive no-higher-derivative parent grammar or show coefficients are below empirical bounds",
            "status": "NOT_ZEROED",
            "coefficient_row": "OPB2405_1_c_HD",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS2405_1_constraint_auxiliary",
            "sector": "constraint/auxiliary MTS residuals",
            "operator_form": "lambda_C C_MTS[q,Phi], lambda_R R_AB, q auxiliary blocks",
            "silence_route": "first-class zero-boundary generator or second-class auxiliary elimination with zero stress",
            "status": "UNSIGNED_ZERO_STRESS",
            "coefficient_row": "OPB2405_2_c_aux",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS2405_2_projector_domain",
            "sector": "projector/domain/readout operator",
            "operator_form": "E_projector(Pi_M), [d,Pi_M]J_H, q-domain tail",
            "silence_route": "variation-before-readout plus q/domain projector commutation theorem",
            "status": "NOT_ZEROED",
            "coefficient_row": "OPB2405_3_c_projector_operator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS2405_3_boundary_reference",
            "sector": "boundary/reference/improvement",
            "operator_form": "DeltaE_boundary, Q_boundary, reference counterterm stress",
            "silence_route": "compact support/falloff/reference fixed before readout",
            "status": "BOUNDARY_GATE_OPEN",
            "coefficient_row": "OPB2405_4_c_boundary_operator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS2405_4_memory_coframe",
            "sector": "memory/coframe/current-chain residual",
            "operator_form": "DeltaE_mem(theta,Q_tau,C_tau), hidden frame response, preferred-frame current",
            "silence_route": "terminal public coframe plus current-chain vertical silence",
            "status": "NOT_ZEROED",
            "coefficient_row": "OPB2405_5_c_memory_frame",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS2405_5_q_source_vector",
            "sector": "q / reciprocal source vector",
            "operator_form": "B_qW C_Weyl + B_qRic R_Ricci + C_qT T_H + Q_q[body] + Pi_q + tail_q",
            "silence_route": "first-class q removal, positive no-hair, or source-vector coefficient bounds",
            "status": "NOT_ZEROED",
            "coefficient_row": "OPB2405_6_c_q_source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS2405_6_verdict",
            "sector": "total MTS operator residual",
            "operator_form": "DeltaE_MTS=sum_i c_i O_i^{mu nu}",
            "silence_route": "all rows RSS2405_0..5 must pass",
            "status": "RESIDUAL_SECTORS_RETAINED_NONCLAIM",
            "coefficient_row": "OPB2405_0_total_DeltaE_MTS",
            "valid_for_claim": "false",
        },
    ]


def operator_bound_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPB2405_0_total_DeltaE_MTS",
            "quantity": "DeltaE_MTS",
            "definition": "total non-Einstein left-hand MTS residual",
            "symbolic_form": "DeltaE_MTS=sum_i c_i O_i^{mu nu}",
            "claim_condition": "all c_i=0/silent or source-backed bounds below local thresholds",
            "test_arenas": "PPN, Newton/Poisson, R10, orbital, clocks, cosmology separated by scale",
            "status": "NONCLAIM_ROOT_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPB2405_1_c_HD",
            "quantity": "c_HD",
            "definition": "higher-derivative curvature coefficient vector",
            "symbolic_form": "{c_R2,c_Ricci2,c_boxR,...}",
            "claim_condition": "parent grammar excludes local higher derivatives or coefficients are bounded",
            "test_arenas": "PPN, R10/Yukawa, gravitational waves",
            "status": "BOUND_OR_ZERO_NEEDED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPB2405_2_c_aux",
            "quantity": "c_aux",
            "definition": "constraint/auxiliary metric stress coefficient",
            "symbolic_form": "lambda_C delta C/delta g, lambda_R delta R_AB/delta g, auxiliary elimination tail",
            "claim_condition": "zero-stress first-class/second-class theorem",
            "test_arenas": "PPN, Newton exterior, q/RAB local branch",
            "status": "ZERO_STRESS_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPB2405_3_c_projector_operator",
            "quantity": "c_projector_operator",
            "definition": "operator residual from projectors/domain/readout",
            "symbolic_form": "E_projector(Pi_M), [d,Pi_M]J_H",
            "claim_condition": "projector commutes with local variation or is absent before readout",
            "test_arenas": "PPN, source normalization, local response",
            "status": "NOT_ZEROED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPB2405_4_c_boundary_operator",
            "quantity": "c_boundary_operator",
            "definition": "metric stress from boundary/reference/improvement terms",
            "symbolic_form": "DeltaE_boundary, delta Q_ref/delta g",
            "claim_condition": "fixed local boundary class and zero local support",
            "test_arenas": "orbits, source charge, local boundary leakage",
            "status": "BOUNDARY_GATE_OPEN",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPB2405_5_c_memory_frame",
            "quantity": "c_memory_frame",
            "definition": "memory/coframe/current-chain left-hand residual",
            "symbolic_form": "DeltaE_mem(theta,Q_tau,C_tau), preferred-frame operator",
            "claim_condition": "terminal public coframe and current-chain vertical silence",
            "test_arenas": "PPN preferred-frame, clocks, orbital secular drift",
            "status": "NOT_ZEROED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPB2405_6_c_q_source",
            "quantity": "c_q_source",
            "definition": "q-sector source-vector/operator residual",
            "symbolic_form": "B_qW,B_qRic,C_qT,Q_q_body,Pi_q,tail_q",
            "claim_condition": "q first-class removal, no-hair activation, or coefficient bounds",
            "test_arenas": "PPN, exterior vacuum, R10, source-profile tests",
            "status": "NOT_ZEROED",
            "valid_for_claim": "false",
        },
    ]


def empirical_map_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM2405_0_ppn_gamma_beta",
            "arena": "PPN gamma/beta",
            "sensitive_coefficients": "DeltaE_MTS,c_HD,c_projector_operator,c_memory_frame,c_q_source",
            "claim_condition": "derive gamma=1,beta=1 or bound residual vector below PPN limits",
            "status": "MAP_STAGED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM2405_1_newton_poisson",
            "arena": "Newton/Poisson",
            "sensitive_coefficients": "DeltaE_MTS,delta_G_source,c_boundary_operator,c_aux",
            "claim_condition": "Poisson equation follows without orbital-G laundering",
            "status": "MAP_STAGED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM2405_2_r10_yukawa",
            "arena": "short-range R10/Yukawa",
            "sensitive_coefficients": "c_HD,c_aux,c_q_source,c_nonminimal",
            "claim_condition": "operator residual projected to alpha(lambda) with real source-backed bounds",
            "status": "MAP_STAGED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM2405_3_orbits_clocks",
            "arena": "orbits and clocks",
            "sensitive_coefficients": "c_boundary_operator,c_memory_frame,c_projector_operator,delta_G_source",
            "claim_condition": "same-frame source normalization plus residual-bound map",
            "status": "MAP_STAGED_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2405_0_EH_dominance",
            "gate": "EH dominance parent-derived",
            "status": "BLOCKED",
            "why": "sector silence certificates are not supplied for all retained MTS residuals",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2405_1_residual_silence",
            "gate": "DeltaE_MTS=0",
            "status": "BLOCKED",
            "why": "constraint/auxiliary, q-source, projector, boundary, and memory/coframe sectors remain open",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2405_2_operator_bounds",
            "gate": "operator coefficients source-backed",
            "status": "BLOCKED",
            "why": "coefficient rows are symbolic; no numeric source-backed bounds are claimed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2405_3_poisson_ppn",
            "gate": "Poisson/PPN follows",
            "status": "BLOCKED",
            "why": "requires EH dominance plus source normalization and PPN residual map",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2405_4_local_GR_Newton",
            "gate": "local GR/Newton reduction",
            "status": "BLOCKED",
            "why": "2405 isolates the residual basis but does not zero it",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2405_0_EH_by_notation",
            "claim": "writing S_silent makes EH dominate",
            "allowed": "false",
            "reason": "silent sector must have zero metric variation or bounded operator residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2405_1_constraint_shortcut",
            "claim": "constraint equation C=0 implies zero stress",
            "allowed": "false",
            "reason": "lambda delta_g C and auxiliary elimination tails can survive",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2405_2_conservation_as_zero",
            "claim": "Bianchi conservation proves DeltaE_MTS=0",
            "allowed": "false",
            "reason": "conserved nonzero residuals still alter PPN/Newton/R10",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2405_3_local_GR",
            "claim": "local GR/Newton is derived",
            "allowed": "false",
            "reason": "operator residual rows remain live and unbounded",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2405_0_gain",
            "decision": "accept EH dominance theorem shape",
            "reason": "we now know exactly which sector certificates are sufficient",
            "consequence": "DeltaE_MTS becomes a finite residual owner problem",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2405_1_no_promotion",
            "decision": "do not promote local GR/Newton",
            "reason": "the residual basis is classified but not zeroed or bounded",
            "consequence": "keep PPN/Newton/R10/orbit claims blocked",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2405_2_next",
            "decision": "attack sector-by-sector variation and local scaling",
            "reason": "this is the least-handwavy way to prove or bound DeltaE_MTS",
            "consequence": "select 2406 sector variation/local scaling silence certificate",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2405_0_selected",
            "next_doc": "2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md",
            "why": "2405 reduces EH dominance to named sector certificates; 2406 must test each sector's variation and local scaling",
            "expected_output": "sector certificate table for c_HD,c_aux,c_projector,c_boundary,c_memory,c_q_source with zero/suppression/bound verdicts",
            "valid_for_claim": "false",
        }
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2405_SOURCE_REGISTER.csv": source_register_rows,
    "P8_Y5_PARENT_QLOC_2405_EH_DOMINANCE_THEOREM_ATTEMPT.csv": dominance_attempt_rows,
    "P8_Y5_PARENT_QLOC_2405_RESIDUAL_SECTOR_SILENCE_AUDIT.csv": residual_sector_rows,
    "P8_Y5_PARENT_QLOC_2405_OPERATOR_BOUND_PACK.csv": operator_bound_rows,
    "P8_Y5_PARENT_QLOC_2405_EMPIRICAL_BOUND_MAP.csv": empirical_map_rows,
    "P8_Y5_PARENT_QLOC_2405_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2405_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2405_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2405_NEXT_TARGET.csv": next_target_rows,
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
            *[str(row) for row in dominance_attempt_rows()],
            *[str(row) for row in residual_sector_rows()],
            *[str(row) for row in operator_bound_rows()],
            *[str(row) for row in empirical_map_rows()],
            *[str(row) for row in claim_gate_rows()],
            *[str(row) for row in refusal_rows()],
            *[str(row) for row in next_target_rows()],
        ]
    )
    checks = [
        {
            "row_id": "VAL2405_00_sources_exist",
            "status": "PASS" if sources_exist() else "FAIL",
            "detail": "all required source paths exist" if sources_exist() else "one or more source paths are missing",
        },
        {
            "row_id": "VAL2405_01_needles_found",
            "status": "PASS" if needles_found() else "FAIL",
            "detail": "all source needles found" if needles_found() else "one or more source needles are missing",
        },
        {
            "row_id": "VAL2405_02_EH_dominance_shape",
            "status": "PASS" if "EHD2405_0_target" in generated_text and "DeltaE_MTS" in generated_text else "FAIL",
            "detail": "EH dominance target and residual condition are recorded",
        },
        {
            "row_id": "VAL2405_03_shortcut_rejection",
            "status": "PASS" if "EHD2405_2_lambda_warning" in generated_text and "SHORTCUT_REJECTED" in generated_text else "FAIL",
            "detail": "constraint-implies-zero-stress shortcut is rejected",
        },
        {
            "row_id": "VAL2405_04_sector_audit",
            "status": "PASS" if "RSS2405_0_higher_derivative" in generated_text and "RSS2405_6_verdict" in generated_text else "FAIL",
            "detail": "residual sector silence audit is complete",
        },
        {
            "row_id": "VAL2405_05_operator_pack_nonclaim",
            "status": "PASS" if "OPB2405_0_total_DeltaE_MTS" in generated_text and "NONCLAIM_ROOT_RESIDUAL" in generated_text else "FAIL",
            "detail": "operator coefficient pack remains nonclaim",
        },
        {
            "row_id": "VAL2405_06_claims_blocked",
            "status": "PASS" if all(row["status"] == "BLOCKED" for row in claim_gate_rows()) else "FAIL",
            "detail": "EH dominance, residual silence, operator bounds, Poisson/PPN, and local GR remain blocked",
        },
        {
            "row_id": "VAL2405_07_csv_parse",
            "status": "PASS" if csvs_parse() else "FAIL",
            "detail": "generated CSVs parse and have rows",
        },
        {
            "row_id": "VAL2405_08_no_claim_flags",
            "status": "PASS" if no_claim_flags() else "FAIL",
            "detail": "no generated row has valid_for_claim=true",
        },
        {
            "row_id": "VAL2405_09_formalization_untouched_by_script",
            "status": "PASS" if formalization_untouched_by_script() else "FAIL",
            "detail": "script writes only post-checkpoint-work outputs",
        },
        {
            "row_id": "VAL2405_10_next_selected",
            "status": "PASS" if "2406-Y5-R2FR-sector-by-sector-MTS-residual-variation-and-local-scaling-silence-or-operator-bounds.md" in generated_text else "FAIL",
            "detail": "sector-by-sector residual variation route selected next",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "row_id": "VAL2405_OVERALL",
            "status": overall,
            "detail": "2405 reduces EH dominance to sector-by-sector residual silence certificates, rejects zero-stress shortcuts, retains operator bounds, and selects sector variation next",
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
    body = f"""# 2405 — EH Dominance And MTS Residual-Sector Silence Or Operator Bound Pack

## Result

This checkpoint gives the exact shape of the left-hand GR problem:

`E_LHS^{{mu nu}}=G^{{mu nu}}+Lambda g^{{mu nu}}+DeltaE_MTS^{{mu nu}}+DeltaE_boundary^{{mu nu}}`.

So EH dominance requires

`DeltaE_MTS^{{mu nu}}=0` and `DeltaE_boundary^{{mu nu}}=0`

or a source-backed proof that the remaining operator coefficients are below the relevant local thresholds.

The useful gain is that `DeltaE_MTS` is no longer one foggy object.  It is split into named owners:

- higher-derivative curvature terms;
- constraint/auxiliary metric stress;
- projector/domain/readout operators;
- boundary/reference/improvement terms;
- memory/coframe/current-chain residuals;
- q/reciprocal source-vector tails.

Shortcut rejected: a constraint equation like `C=0` does **not** by itself imply zero metric stress, because
`lambda delta_g C` or auxiliary elimination tails can survive.  That keeps the lambda/constraint route honest.

Current verdict: EH dominance is not parent-proved yet.  The next move is sector-by-sector variation and local scaling.

## Source Register

{markdown_table(source_register_rows(), ["source_id", "source_path", "exists", "role", "valid_for_claim"])}

## EH Dominance Theorem Attempt

{markdown_table(dominance_attempt_rows(), ["row_id", "claim_piece", "mathematical_form", "zero_condition", "current_result", "remaining_gap", "valid_for_claim"])}

## Residual Sector Silence Audit

{markdown_table(residual_sector_rows(), ["sector_id", "sector", "operator_form", "silence_route", "status", "coefficient_row", "valid_for_claim"])}

## Operator Bound Pack

{markdown_table(operator_bound_rows(), ["row_id", "quantity", "definition", "symbolic_form", "claim_condition", "test_arenas", "status", "valid_for_claim"])}

## Empirical Bound Map

{markdown_table(empirical_map_rows(), ["map_id", "arena", "sensitive_coefficients", "claim_condition", "status", "valid_for_claim"])}

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

This is a narrowing, not a victory lap.  But it is exactly the narrowing we needed.  The GR/Newton problem is now:
prove each named MTS residual sector is zero/silent, or stop pretending and carry its coefficient into PPN/Newton/R10
bounds.  That is a fair fight; no haymakers, no smoke machine.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2405_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2405_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
