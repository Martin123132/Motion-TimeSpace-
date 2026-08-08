from __future__ import annotations

import csv
import re
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_Q_FIELD_CONTENT_NO_SPURION_OR_BQWEYL_BOUND_2303"
DOC = ROOT / "2303-Y5-R2FR-q-field-content-no-spurion-certificate-or-BqWeyl-local-bound-acquisition.md"

PATHS = {
    "2302_doc": ROOT / "2302-Y5-R2FR-q-representation-or-firstclass-certificate-or-BqWeyl-bound-row.md",
    "2302_validation": OUT / "P8_Y5_BRR545_2302_VALIDATION.csv",
    "2302_next": OUT / "P8_Y5_PARENT_QLOC_2302_NEXT_TARGET.csv",
    "2302_rep_cert": OUT / "P8_Y5_PARENT_QLOC_2302_Q_REPRESENTATION_CERTIFICATE_ATTEMPT.csv",
    "2302_index": OUT / "P8_Y5_PARENT_QLOC_2302_BQWEYL_INDEX_ZERO_THEOREM_GATE.csv",
    "2302_bound": OUT / "P8_Y5_PARENT_QLOC_2302_BQWEYL_BOUND_ROW_NONCLAIM.csv",
    "581_chain": OUT / "P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
    "594_contract": OUT / "P8_Y5_R10_594_QUOTIENT_MAP_CONSTRUCTION_CONTRACT.csv",
    "637_qmap": OUT / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
    "619_doc": ROOT / "619-Y5-R10-no-marker-minimal-quotient-theorem-or-qbarXT-residual-fill.md",
    "619_no_marker": OUT / "P8_Y5_R10_619_NO_MARKER_THEOREM_ATTEMPT.csv",
    "619_minimal": OUT / "P8_Y5_R10_619_MINIMAL_QUOTIENT_GATE.csv",
    "623_doc": ROOT / "623-Y5-R10-unique-observed-coframe-functor-or-bg-prior-fill.md",
    "623_functor": OUT / "P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv",
    "624_doc": ROOT / "624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md",
    "624_signature": OUT / "P8_Y5_R10_624_PARENT_SIGNATURE_AUDIT.csv",
    "624_bg_rows": OUT / "P8_Y5_R10_624_BG_SMOKE_ROWS.csv",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
    "1157_doc": ROOT / "1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md",
    "1761_doc": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
    "1768_doc": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
    "2297_doc": ROOT / "2297-Y5-R2FR-Jq-source-zero-or-component-bound-pack.md",
    "2300_doc": ROOT / "2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md",
    "2301_residuals": OUT / "P8_Y5_PARENT_QLOC_2301_Q_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv",
}

SOURCES = [
    ("SRC2303_00_2302_doc", "2302_handoff", PATHS["2302_doc"], ["DEC2302_3_next", "Q_FIELD_CONTENT_NO_SPURION_OR_BQWEYL_BOUND_ACQUISITION_NEXT"], "direct handoff selecting q field-content/no-spurion source hunt or B_qWeyl local bound acquisition"),
    ("SRC2303_01_2302_validation", "2302_validation", PATHS["2302_validation"], ["VAL2302_OVERALL", "PASS"], "confirms 2302 passed before 2303 starts"),
    ("SRC2303_02_2302_next", "2302_next", PATHS["2302_next"], ["2303-Y5-R2FR-q-field-content-no-spurion-certificate-or-BqWeyl-local-bound-acquisition.md", "B_qWeyl"], "next-target contract"),
    ("SRC2303_03_2302_rep_cert", "2302_rep_cert", PATHS["2302_rep_cert"], ["QRC2302_7_verdict", "FAIL_CURRENT_CLAIM"], "incoming q representation certificate is blocked"),
    ("SRC2303_04_2302_index", "2302_index", PATHS["2302_index"], ["BQWZ2302_0_conditional_theorem", "EXACT_CONDITIONAL_THEOREM"], "incoming conditional B_qWeyl theorem"),
    ("SRC2303_05_2302_bound", "2302_bound", PATHS["2302_bound"], ["BQB2302_0_BqWeyl", "MISSING_REPRESENTATION_FIRSTCLASS_OR_NUMERIC_BOUND"], "incoming B_qWeyl nonclaim bound row"),
    ("SRC2303_06_581_chain", "581_chain", PATHS["581_chain"], ["QVT581_7_alpha_result", "conditional_theorem_proved_but_premises"], "older quotient/vertical theorem chain"),
    ("SRC2303_07_594_contract", "594_contract", PATHS["594_contract"], ["QMC594_4_no_hidden_marker", "not_proved"], "quotient-map construction contract and no-hidden-marker blocker"),
    ("SRC2303_08_637_qmap", "637_qmap", PATHS["637_qmap"], ["QM637_2_vertical_kernel", "Dq[v_X]=0"], "candidate q-map derivation with vertical kernel conditional"),
    ("SRC2303_09_619_doc", "619_doc", PATHS["619_doc"], ["NMT619_5_no_marker_theorem_verdict", "qbar_XT=0"], "no-marker/minimal quotient checkpoint doc"),
    ("SRC2303_10_619_no_marker", "619_no_marker", PATHS["619_no_marker"], ["NMT619_5_no_marker_theorem_verdict", "not_closed"], "no-marker theorem fails to close"),
    ("SRC2303_11_619_minimal", "619_minimal", PATHS["619_minimal"], ["MQ619_6_gate_verdict", "no_marker_theorem_not_closed"], "minimal quotient gate keeps countermodels live"),
    ("SRC2303_12_623_doc", "623_doc", PATHS["623_doc"], ["OCF623_4_bg_verdict", "factorization"], "coframe factorization checkpoint doc"),
    ("SRC2303_13_623_functor", "623_functor", PATHS["623_functor"], ["OCF623_4_bg_verdict", "not_closed"], "coframe factorization lemma remains conditional"),
    ("SRC2303_14_624_doc", "624_doc", PATHS["624_doc"], ["SIG624_7_signature_verdict", "not_signed"], "observed coframe factorization checkpoint doc"),
    ("SRC2303_15_624_signature", "624_signature", PATHS["624_signature"], ["SIG624_7_signature_verdict", "not_signed"], "observed coframe factorization parent signature fails"),
    ("SRC2303_16_624_bg_rows", "624_bg_rows", PATHS["624_bg_rows"], ["BGR624_0_conformal_common", "MISSING_PARENT_INPUT"], "common-frame runner rows remain missing"),
    ("SRC2303_17_1023_doc", "1023_doc", PATHS["1023_doc"], ["QVC1023_8_verdict", "fail_current_claim_demote_current_branch"], "single q/vX/action certificate fails current claim"),
    ("SRC2303_18_1157_doc", "1157_doc", PATHS["1157_doc"], ["QMAP1157_8_verdict", "PARENT_Q_MAP_NULL_GENERATOR_NOT_DERIVED"], "parent q-map/null-generator proof fails current corpus"),
    ("SRC2303_19_1761_doc", "1761_spurion", PATHS["1761_doc"], ["SP1761_4_hidden_frame", "LIVE_UNLESS_DECLARED_EXTENSION"], "hidden frame countermodel"),
    ("SRC2303_20_1768_doc", "1768_normal_form", PATHS["1768_doc"], ["SCL1768_2_nonminimal_coupling", "SCL1768_5_post_variation_projector"], "nonminimal/projector normal-form warning"),
    ("SRC2303_21_2297_doc", "2297_body", PATHS["2297_doc"], ["Q_q[body]", "EXTERIOR_ZERO_INSUFFICIENT_BODY_CHARGE_OPEN"], "body/source-worldtube charge warning"),
    ("SRC2303_22_2300_doc", "2300_normal_form", PATHS["2300_doc"], ["QRES2300_0_BqWeyl", "MISSING_Q_WEYL_COUPLING_ZERO_OR_BOUND"], "minimal q source-vector normal form"),
    ("SRC2303_23_2301_residuals", "2301_residuals", PATHS["2301_residuals"], ["QCURV2301_0_BqWeyl", "MISSING_REPRESENTATION_OR_FIRSTCLASS_CERTIFICATE_OR_BOUND"], "latest q curvature residual acquisition row"),
]

SCAN_KEYS = [
    "581_chain",
    "594_contract",
    "637_qmap",
    "619_doc",
    "619_no_marker",
    "623_doc",
    "623_functor",
    "624_doc",
    "624_signature",
    "1023_doc",
    "1157_doc",
    "1761_spurion",
    "1768_normal_form",
    "2302_handoff",
]

SCAN_PATTERNS = [
    ("q_map", re.compile(r"\bq\s*:\s*Phi_parent|Q_obs|Q_MTS|quotient map|parent quotient", re.IGNORECASE)),
    ("vertical_kernel", re.compile(r"Dq\[v_X\]|dq\(v_X\)|vertical kernel|v_X is vertical|presymplectic-null", re.IGNORECASE)),
    ("action_factorization", re.compile(r"S_parent|S_bulk|S_matter|factorization|factors through|action descent", re.IGNORECASE)),
    ("no_marker_spurion", re.compile(r"no-marker|no hidden|no-spurion|hidden frame|Weyl/disformal|representative Weyl", re.IGNORECASE)),
    ("failure_status", re.compile(r"not_signed|not_closed|not_parent|NOT_PARENT|MISSING|FAIL|blocked|conditional", re.IGNORECASE)),
    ("bqweyl", re.compile(r"B_qWeyl|BqWeyl|C_Weyl|Weyl/tidal|Weyl-type", re.IGNORECASE)),
]

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2303_SOURCE_REGISTER.csv",
    "source_scan": OUT / "P8_Y5_PARENT_QLOC_2303_FOCUSED_Q_SOURCE_SCAN.csv",
    "q_certificate": OUT / "P8_Y5_PARENT_QLOC_2303_Q_FIELD_CONTENT_CERTIFICATE_SOURCE_HUNT.csv",
    "no_spurion": OUT / "P8_Y5_PARENT_QLOC_2303_Q_NO_SPURION_CERTIFICATE_SOURCE_HUNT.csv",
    "bqweyl_acquisition": OUT / "P8_Y5_PARENT_QLOC_2303_BQWEYL_LOCAL_BOUND_ACQUISITION_REQUIREMENTS.csv",
    "arena_projection": OUT / "P8_Y5_PARENT_QLOC_2303_BQWEYL_ARENA_PROJECTION_ROWS.csv",
    "candidate_parent_clause": OUT / "P8_Y5_PARENT_QLOC_2303_CANDIDATE_PARENT_Q_CLAUSE_NONCLAIM.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2303_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2303_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2303_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2303_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2303_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2303_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_certificate": QUEUE / "JR2303_Q_FIELD_CONTENT_NO_SPURION_SOURCE_HUNT_NONCLAIM.csv",
    "queue_bqweyl": QUEUE / "JR2303_BQWEYL_LOCAL_BOUND_ACQUISITION_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "q_BqWeyl_local_bound_acquisition_nonclaim_2303.csv",
    "beta_docs": BETA_DOCS / "Q_FIELD_CONTENT_BQWEYL_2303_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def false_flags() -> dict[str, bool]:
    return {
        "theorem_zero": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def src(*keys: str) -> str:
    by_key = {source_key: path for _, source_key, path, _, _ in SOURCES}
    return ";".join(rel(by_key[key]) for key in keys)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_id, source_key, path, needles, role in SOURCES:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_key": source_key,
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "validation_overall_pass": validation_pass(path) if "validation" in source_key else "",
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def focused_source_scan_rows() -> list[dict[str, Any]]:
    by_key = {source_key: path for _, source_key, path, _, _ in SOURCES}
    rows: list[dict[str, Any]] = []
    hit_count: dict[str, int] = {pattern_id: 0 for pattern_id, _ in SCAN_PATTERNS}
    max_per_pattern = 16
    for source_key in SCAN_KEYS:
        path = by_key[source_key]
        if not path.exists():
            continue
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            clean_line = " ".join(line.strip().split())
            if not clean_line:
                continue
            for pattern_id, pattern in SCAN_PATTERNS:
                if hit_count[pattern_id] >= max_per_pattern:
                    continue
                if pattern.search(clean_line):
                    hit_count[pattern_id] += 1
                    rows.append(
                        {
                            "branch_id": BRANCH_ID,
                            "scan_id": f"SCAN2303_{len(rows):03d}",
                            "pattern_id": pattern_id,
                            "source_key": source_key,
                            "source_path": rel(path),
                            "line_number": line_number,
                            "excerpt": clean_line[:360],
                            "interpretation": scan_interpretation(pattern_id, clean_line),
                            "valid_for_claim": False,
                            "claim_allowed": False,
                        }
                    )
    if not rows:
        raise ValueError("focused scan produced no rows")
    return rows


def scan_interpretation(pattern_id: str, line: str) -> str:
    if pattern_id == "q_map":
        return "candidate q-map/quotient language located; source must still sign parent construction"
    if pattern_id == "vertical_kernel":
        return "vertical-kernel condition located; source must still identify actual local direction"
    if pattern_id == "action_factorization":
        return "action or matter factorization language located; source must still sign all parent clauses"
    if pattern_id == "no_marker_spurion":
        return "no-spurion or hidden-spurion channel located; countermodels remain important"
    if pattern_id == "failure_status":
        return "source explicitly marks a premise conditional, missing, blocked, or unsigned"
    if pattern_id == "bqweyl":
        return "B_qWeyl/Weyl local-vacuum pressure point located"
    return "focused source hit"


def q_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        ("QFCH2303_0_parent_q_object", "construct parent q object", "Conf_parent -> Q_obs/Q_MTS is defined before variation with domain and equivalence relation", "CONTRACT_LANGUAGE_FOUND_NOT_PARENT_SIGNED", "581/594/637/1156/1157 repeatedly state q as conditional quotient/projection", "MISSING_EXPLICIT_PARENT_CONFIGURATION_AND_EQUIVALENCE_RELATION", "581_chain;594_contract;637_qmap;1157_doc"),
        ("QFCH2303_1_actual_vertical_direction", "identify actual local q/Weyl-sensitive direction", "the direction sourcing q is tangent to the kernel of Dq on the compact local branch", "CONDITIONAL_ONLY", "637 gives Dq[v_X]=0 only if v_X is tangent to the null orbit; 1157 says actual Xhat identification is not signed", "MISSING_LOCAL_DIRECTION_EQUALS_NULL_GENERATOR_PROOF", "637_qmap;1157_doc;1023_doc"),
        ("QFCH2303_2_field_type", "declare q field type", "q is scalar/quotient/pure density and not a Weyl/Riemann four-index tensor or hidden tensor-projector carrier", "NOT_DECLARED_FOR_THIS_Q_BRANCH", "2302 needs this exact clause; older files speak of quotient variables but not this R2FR q field-content certificate", "MISSING_Q_FIELD_BUNDLE_RANK_TRANSFORM_LAW", "2302_rep_cert;1023_doc;1157_doc"),
        ("QFCH2303_3_action_descent", "bulk action descent", "S_parent[Phi]=S_red[q(Phi)] plus owned exact/topological terms before variation", "CONDITIONAL_TEMPLATE_ONLY", "581/594/1023 state the descent conditionally; no full parent Lagrangian signs it", "MISSING_PARENT_ACTION_DESCENT_FOR_Q", "581_chain;594_contract;1023_doc"),
        ("QFCH2303_4_matter_geometry_descent", "matter/coframe factorization", "ordinary matter-visible geometry and constants factor through q/Q_MTS with no representative-frame dependence", "NOT_PARENT_SIGNED", "619/623/624 give exact lemmas but retain common Weyl/disformal and marker channels", "MISSING_ALL_SPECIES_MATTER_FACTORISATION_AND_CONSTANT_TRIVIALITY", "619_no_marker;623_functor;624_signature"),
        ("QFCH2303_5_boundary_source_neutrality", "boundary/source neutrality", "q quotient or first-class direction carries no Q_q[body], Pi_q, edge, readout, or tail source", "NOT_SIGNED", "2297/2300 keep body and boundary source terms live", "MISSING_Q_BODY_BOUNDARY_TAIL_ZERO", "2297_body;2300_normal_form;2301_residuals"),
        ("QFCH2303_6_verdict", "q field-content certificate", "QFCH2303_0 through QFCH2303_5 all close in one parent branch", "FAIL_CURRENT_CLAIM_SOURCE_HUNT_NEGATIVE", "source hunt found conditional building blocks but no parent-signed certificate", "BQWEYL_ZERO_NOT_ACTIVATED", "2302_handoff;581_chain;637_qmap;619_no_marker;624_signature;1157_doc"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "certificate_id": certificate_id,
            "target_clause": target,
            "required_statement": required,
            "hunt_result": result,
            "evidence_summary": evidence,
            "missing_for_claim": missing,
            "source_paths": ";".join(src(key) for key in keys.split(";")),
            **false_flags(),
        }
        for certificate_id, target, required, result, evidence, missing, keys in rows
    ]


def no_spurion_rows() -> list[dict[str, Any]]:
    rows = [
        ("NSH2303_0_no_Weyl_projector", "forbid Weyl-index carrier", "no P^{munuab}, hidden tensor, readout kernel, or background projector can contract q with C_munuab", "NOT_PARENT_SIGNED", "2302 names this as the exact B_qWeyl kill clause; 1768 leaves projector/nonminimal channels open", "MISSING_NO_WEYL_PROJECTOR_THEOREM", "2302_index;1768_normal_form"),
        ("NSH2303_1_no_common_frame", "forbid representative Weyl/disformal matter frame", "ordinary matter cannot see A_g(q_rep)^2 g_obs or disformal q-dependent frame before quotient", "NOT_PARENT_SIGNED", "623/624 retain common-frame c_g/B_g rows; 1761 calls hidden frame live unless declared extension", "MISSING_NO_REPRESENTATIVE_FRAME_THEOREM", "623_functor;624_signature;624_bg_rows;1761_spurion"),
        ("NSH2303_2_no_marker_constants", "forbid material marker/constant return", "constants, charges, material labels, and source weights are representation data or q-blind", "NOT_PARENT_SIGNED", "619 keeps constants, markers, and source-current variants legal", "MISSING_CONSTANT_TRIVIALITY_AND_NO_MARKER_PROOF", "619_no_marker;619_minimal"),
        ("NSH2303_3_no_post_variation_projector", "forbid post-variation source/readout projector", "no projector/readout/source mask reintroduces q-Weyl or q-source dependence after Euler variation", "NOT_PARENT_SIGNED", "1768 keeps post-variation projector as forbidden by contract but not parent-signed; 2302 keeps readout countermodel live", "MISSING_READOUT_PROJECTOR_NO_REENTRY_THEOREM", "1768_normal_form;2302_index"),
        ("NSH2303_4_no_boundary_spurion", "forbid boundary/source Weyl-like edge data", "boundary/source terms do not supply q-sensitive Weyl/tidal effective source", "NOT_PARENT_SIGNED", "2297/2300 retain Q_q[body], Pi_q, and tails", "MISSING_BOUNDARY_SOURCE_SPURION_SILENCE", "2297_body;2300_normal_form"),
        ("NSH2303_5_verdict", "no-spurion certificate", "NSH2303_0 through NSH2303_4 close together", "FAIL_CURRENT_CLAIM_NO_SPURION_NOT_SIGNED", "countermodel channels remain live across source files", "B_QWEYL_BOUND_ACQUISITION_REQUIRED_IF_NO_NEW_PARENT_CLAUSE", "1761_spurion;1768_normal_form;619_no_marker;624_signature;2302_index"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "no_spurion_id": no_spurion_id,
            "target_clause": clause,
            "required_statement": required,
            "hunt_result": result,
            "evidence_summary": evidence,
            "missing_for_claim": missing,
            "source_paths": ";".join(src(key) for key in keys.split(";")),
            **false_flags(),
        }
        for no_spurion_id, clause, required, result, evidence, missing, keys in rows
    ]


def bqweyl_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("BQA2303_0_zero_switch", "Z_BqWeyl", "boolean theorem-zero switch for B_qWeyl", "true iff q field-content and no-spurion/first-class certificate is parent-signed", "boolean", "2302 theorem plus 2303 certificate rows", "ZERO_SWITCH_FALSE_CURRENTLY", "MISSING_Q_FIELD_CONTENT_NO_SPURION_OR_FIRSTCLASS_CERTIFICATE", "local_GR;PPN;R10;orbital"),
        ("BQA2303_1_parent_coefficient", "B_qWeyl", "linear q-Weyl/tidal curvature source coefficient", "|B_qWeyl| in common q operator normalization", "operator_dependent", "parent Hessian/source-vector normalization or theorem-zero", "MISSING_PARENT_COEFFICIENT", "MISSING_PARENT_SOURCE_AND_UNITS", "local_GR;PPN;R10;orbital;alpha3"),
        ("BQA2303_2_q_operator", "L_q_or_G_q", "q local operator or Green norm used to convert Weyl source to profile", "||G_q|| or coercive inverse/domain bound", "operator_norm", "q Hessian/domain/self-adjoint boundary source", "MISSING_OPERATOR_DOMAIN", "MISSING_GQ_SOURCE", "local_GR;PPN;orbital"),
        ("BQA2303_3_weyl_scale", "C_Weyl_local", "exterior Weyl/tidal curvature scale in selected local arena/domain", "sup_D |C_Weyl| with domain and units", "1/length^2", "local geometry profile or conservative GR/MTS exterior curvature bound", "MISSING_CURVATURE_PROFILE", "MISSING_CWEYL_SOURCE", "local_GR;PPN;orbital"),
        ("BQA2303_4_tau_projection", "tau_BqWeyl_local", "projection from q_Weyl profile to arena observable vector", "residual <= tau |B_qWeyl| ||G_q|| |C_Weyl| plus tails", "arena_dependent", "R10/PPN/clock/orbital response kernels", "MISSING_ARENA_PROJECTION", "MISSING_TAU_SOURCE", "R10;PPN;clock;orbital"),
        ("BQA2303_5_body_boundary_tail", "epsilon_q_body_boundary_tail", "absolute envelope for Q_q[body], Pi_q, readout, projector, and history tails", "sum_abs(body,boundary,readout,projector,history) in same q profile units", "q_profile_units", "2297/2300 source-body and tail rows or zero theorem", "MISSING_TAIL_ENVELOPE", "MISSING_BODY_BOUNDARY_TAIL_SOURCES", "all_local_arenas"),
        ("BQA2303_6_acceptance_rule", "B_qWeyl_claim_status", "claim gate for B_qWeyl local bound", "claim only if Z_BqWeyl=true or all numeric rows are source-backed, unit-matched, and abs-summed below arena limits", "status", "all above", "NONCLAIM_ACQUISITION_SCHEMA_READY", "VALID_FOR_CLAIM_FALSE_UNTIL_INPUTS_EXIST", "all_local_arenas"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "symbol": symbol,
            "definition": definition,
            "required_value_or_formula": formula,
            "units": units,
            "required_source": required_source,
            "current_status": status,
            "missing_for_claim": missing,
            "observable_link": observable,
            "source_paths": src("2302_bound", "2301_residuals", "2297_body", "2300_normal_form"),
            **false_flags(),
        }
        for acquisition_id, symbol, definition, formula, units, required_source, status, missing, observable in rows
    ]


def arena_projection_rows() -> list[dict[str, Any]]:
    rows = [
        ("AP2303_0_R10", "R10 inverse-square", "alpha_R10_qWeyl <= tau_R10 |B_qWeyl| ||G_q|| |C_Weyl| + tails", "tau_R10;lambda_q;source/test material map;normalization;bound curve", "MISSING_R10_PROJECTION", "do not use R10 claim while B_qWeyl rows missing"),
        ("AP2303_1_PPN", "PPN/local metric", "PPN_vec_qWeyl <= tau_PPN |B_qWeyl| ||G_q|| |C_Weyl| + tails", "tau_PPN;gauge convention;metric projection;solar-system domain", "MISSING_PPN_PROJECTION", "do not claim local-GR/PPN recovery"),
        ("AP2303_2_orbital", "orbital dynamics", "delta_a_or_GM <= tau_orbital |B_qWeyl| ||G_q|| |C_Weyl| + tails", "tau_orbital;source mass normalization;domain;curvature profile", "MISSING_ORBITAL_PROJECTION", "no orbital/Newton pass"),
        ("AP2303_3_clock_alpha", "clock/EM/fine structure", "delta_clock_or_alpha <= tau_clock |B_qWeyl| ||G_q|| |C_Weyl| + representative-frame tails", "tau_clock;tau_alpha;clock/EM readout map", "MISSING_CLOCK_ALPHA_PROJECTION", "no clock/EM pass"),
        ("AP2303_4_total", "all local arenas", "residual_total_abs = sum_abs(B_qWeyl profile, body, boundary, readout, projector, history)", "all components numeric/sourced or theorem-zero", "MISSING_ABSOLUTE_ENVELOPE_INPUTS", "no cancellation between unknown components"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "arena": arena,
            "projection_formula": formula,
            "required_inputs": inputs,
            "current_status": status,
            "guard": guard,
            "source_paths": src("2302_bound", "2301_residuals", "2297_body"),
            **false_flags(),
        }
        for projection_id, arena, formula, inputs, status, guard in rows
    ]


def candidate_parent_clause_rows() -> list[dict[str, Any]]:
    rows = [
        ("PQC2303_0_clause_shape", "candidate parent q clause", "Declare a parent configuration quotient q:Conf_parent->Q_obs with q scalar/quotient/pure-density field content, Dq[v_q]=0 for the local representative direction, S_bulk and S_matter factor through q up to owned exact/topological terms, and no Weyl-type spurion/projector/readout kernel exists.", "WOULD_ACTIVATE_BQWEYL_INDEX_THEOREM_IF_PARENT_SIGNED", "not a current proof; a future parent action contract"),
        ("PQC2303_1_required_signature", "signature burden", "Must be signed by field list, transformation law, action terms, measure/coframe descent, matter/constants descent, boundary/source neutrality, and radiative/readout closure.", "FULL_PARENT_SIGNATURE_REQUIRED", "prevents a pretty axiom from becoming a hidden closure"),
        ("PQC2303_2_current_status", "current status", "Existing files contain this as conditional route fragments only.", "CONTRACT_FRAGMENT_READY_NOT_DERIVED", "cannot be used for local-GR/Newton/R10/PPN claim"),
        ("PQC2303_3_next_use", "next use", "Use this clause as a checklist for a future parent action section; otherwise proceed to B_qWeyl numeric/source bound acquisition.", "ROUTE_SELECTOR", "keeps derivation-first and testing-first branches separated"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "clause_name": name,
            "statement": statement,
            "status": status,
            "limitation": limitation,
            "source_paths": src("2302_index", "581_chain", "594_contract", "637_qmap", "619_no_marker", "624_signature", "1157_doc"),
            **false_flags(),
        }
        for clause_id, name, statement, status, limitation in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2303_0_q_field_content", "q field-content certificate source-found", "BLOCKED", "QFCH2303_6 verdict=FAIL_CURRENT_CLAIM_SOURCE_HUNT_NEGATIVE"),
        ("REF2303_1_no_spurion", "q no-spurion certificate closes", "BLOCKED", "NSH2303_5 verdict=FAIL_CURRENT_CLAIM_NO_SPURION_NOT_SIGNED"),
        ("REF2303_2_BqWeyl_zero", "B_qWeyl=0 activated", "BLOCKED", "zero switch false; q/no-spurion/first-class certificate not parent signed"),
        ("REF2303_3_BqWeyl_bound", "B_qWeyl local bound score-ready", "BLOCKED", "BQA2303 rows missing parent coefficient, operator, Weyl scale, projection, and tail envelope"),
        ("REF2303_4_local_GR_Newton", "derived local GR/Newton recovery", "BLOCKED", "B_qWeyl plus body/boundary/tail/readout residual vector open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for refusal_id, claim, result, blocked_by in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2303_0_q_field_content", "parent q field-content/type/transform certificate signed", "source hunt found conditional fragments only"),
        ("CG2303_1_no_spurion", "no Weyl/projector/frame/marker/readout spurion theorem signed", "countermodel channels remain live"),
        ("CG2303_2_BqWeyl_zero", "B_qWeyl theorem-zero activated", "zero switch false"),
        ("CG2303_3_BqWeyl_bound", "B_qWeyl numeric/source local bound score-ready", "coefficient/operator/Weyl/projection/tail inputs missing"),
        ("CG2303_4_local_GR_Newton", "local GR/Newton derivable branch closed", "q local residual vector remains open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "gate_pass": False,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2303_0_source_hunt",
            "decision": "Q_FIELD_CONTENT_SOURCE_HUNT_NEGATIVE_FOR_CURRENT_CORPUS",
            "rationale": "The current corpus contains conditional quotient-map and coframe-factorization lemmas, but no parent-signed q field-content/transform/no-spurion certificate.",
            "next_action": "do not activate B_qWeyl zero theorem from existing sources",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2303_1_contract_gain",
            "decision": "PARENT_Q_CLAUSE_NOW_EXACT",
            "rationale": "The future parent action now has a concrete contract: q quotient object, vertical kernel, scalar/density type, action/matter descent, no Weyl spurion, and boundary/source silence.",
            "next_action": "use candidate parent clause as derivation checklist, not as claim evidence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2303_2_bound_gain",
            "decision": "BQWEYL_LOCAL_BOUND_ACQUISITION_INTERFACE_WRITTEN",
            "rationale": "If no new parent clause is supplied, B_qWeyl must be bounded with parent coefficient, q operator/Green norm, Weyl scale, arena projection, and absolute tail envelope.",
            "next_action": "target first concrete B_qWeyl bound input or derive one missing parent q clause",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2303_3_next",
            "decision": "BQWEYL_FIRST_SOURCE_INPUT_OR_PARENT_Q_CLAUSE_DERIVATION_NEXT",
            "rationale": "The next useful step is either derive one hard parent clause, preferably no Weyl-spurion from object language, or fill the first local B_qWeyl source input.",
            "next_action": "2304-Y5-R2FR-no-Weyl-spurion-parent-object-language-or-BqWeyl-first-local-source-input.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2303_0_primary",
            "next_target": "2304-Y5-R2FR-no-Weyl-spurion-parent-object-language-or-BqWeyl-first-local-source-input.md",
            "script": "scripts/Y5_R2FR_no_Weyl_spurion_parent_object_language_or_BqWeyl_first_local_source_input_2304.py",
            "objective": "try to derive the no-Weyl-spurion object-language clause for q from the parent action grammar; if it fails, fill the first source-backed B_qWeyl local input row without claims",
            "selection_status": "selected",
            "success_condition": "one hard parent q/no-spurion clause becomes source-backed, or B_qWeyl acquisition advances from schema to first real sourced input while claims remain blocked",
            "forbidden_shortcuts": "q by declaration; no-spurion by taste; treating absence of source hits as proof; treating common-frame WEP safety as local-GR safety; numeric placeholder bounds; local-GR/R10/PPN claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        }
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    plan = [
        ("queue_certificate", OUTPUTS["q_certificate"], COPY_TARGETS["queue_certificate"], "q field-content/no-spurion source hunt nonclaim queue"),
        ("queue_bqweyl", OUTPUTS["bqweyl_acquisition"], COPY_TARGETS["queue_bqweyl"], "B_qWeyl local bound acquisition nonclaim queue"),
        ("branch_wep", OUTPUTS["arena_projection"], COPY_TARGETS["branch_wep"], "WEP/local branch q B_qWeyl arena projection nonclaim copy"),
        ("beta_docs", OUTPUTS["candidate_parent_clause"], COPY_TARGETS["beta_docs"], "beta-source docs q parent clause nonclaim copy"),
    ]
    rows = []
    for copy_key, source_path, target_path, reason in plan:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2303_{copy_key}",
                "source_path": rel(source_path),
                "target_path": rel(target_path),
                "target_exists": target_path.exists(),
                "target_parses": parse_csv(target_path),
                "reason": reason,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    columns = list(rows[0].keys())
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def formalization_2303_output_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    markers = [
        "2303-Y5-R2FR-q-field-content-no-spurion-certificate-or-BqWeyl-local-bound-acquisition",
        "P8_Y5_PARENT_QLOC_2303",
        "P8_Y5_BRR545_2303",
        "JR2303_",
        "q_BqWeyl_local_bound_acquisition_nonclaim_2303",
    ]
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers))


def pycache_exists() -> bool:
    return any(path.name == "__pycache__" for path in (ROOT / "scripts").rglob("__pycache__"))


def remove_pycache() -> None:
    for path in (ROOT / "scripts").rglob("__pycache__"):
        shutil.rmtree(path)


def validation_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    for path in generated:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    all_rows: list[dict[str, Any]] = []
    for path in generated:
        all_rows.extend(read_csv(path))

    pattern_ids = {row["pattern_id"] for row in sections["source_scan"]}
    checks = [
        ("VAL2303_00_sources_exist", all(str(row["exists"]) == "True" for row in sections["source_register"]), "all cited source paths exist"),
        ("VAL2303_01_needles_present", all(str(row["needles_present"]) == "True" for row in sections["source_register"]), "all cited source needles are present"),
        ("VAL2303_02_prior_validation", all(str(row["validation_overall_pass"]) in ("", "True") for row in sections["source_register"]), "2302 validation passes where checked"),
        ("VAL2303_03_scan_has_q_map", "q_map" in pattern_ids, "focused scan found q-map/quotient language"),
        ("VAL2303_04_scan_has_spurion", "no_marker_spurion" in pattern_ids, "focused scan found no-spurion/countermodel language"),
        ("VAL2303_05_scan_has_bqweyl", "bqweyl" in pattern_ids, "focused scan found B_qWeyl/Weyl pressure language"),
        ("VAL2303_06_q_certificate_blocks", any(row["certificate_id"] == "QFCH2303_6_verdict" and row["hunt_result"] == "FAIL_CURRENT_CLAIM_SOURCE_HUNT_NEGATIVE" for row in sections["q_certificate"]), "q field-content source hunt refuses current claim"),
        ("VAL2303_07_no_spurion_blocks", any(row["no_spurion_id"] == "NSH2303_5_verdict" and row["hunt_result"] == "FAIL_CURRENT_CLAIM_NO_SPURION_NOT_SIGNED" for row in sections["no_spurion"]), "no-spurion source hunt refuses current claim"),
        ("VAL2303_08_bqweyl_requirements_complete", any(row["acquisition_id"] == "BQA2303_6_acceptance_rule" and row["current_status"] == "NONCLAIM_ACQUISITION_SCHEMA_READY" for row in sections["bqweyl_acquisition"]), "B_qWeyl local acquisition interface is complete"),
        ("VAL2303_09_arena_rows_complete", len(sections["arena_projection"]) >= 5 and all(str(row["valid_for_claim"]) == "False" for row in sections["arena_projection"]), "arena projection rows remain nonclaim"),
        ("VAL2303_10_candidate_clause_nonclaim", any(row["clause_id"] == "PQC2303_0_clause_shape" and row["status"] == "WOULD_ACTIVATE_BQWEYL_INDEX_THEOREM_IF_PARENT_SIGNED" for row in sections["candidate_parent_clause"]), "candidate parent q clause is explicit and nonclaim"),
        ("VAL2303_11_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in sections["runner_refusal"]), "refusal runner blocks all current claims"),
        ("VAL2303_12_claim_gates_blocked", all(str(row["gate_pass"]) == "False" for row in sections["claim_gates"]), "claim gates are blocked"),
        ("VAL2303_13_decision_next", any(row["decision_id"] == "DEC2303_3_next" and "BQWEYL_FIRST_SOURCE_INPUT" in row["decision"] for row in sections["decision"]), "decision selects no-Weyl-spurion derivation or first B_qWeyl source input next"),
        ("VAL2303_14_next_selected", any(row["route_id"] == "NEXT2303_0_primary" and row["selection_status"] == "selected" for row in sections["next_target"]), "next target selected"),
        ("VAL2303_15_csv_parse", csv_parse_ok, "all generated 2303 CSVs parse"),
        ("VAL2303_16_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" for row in all_rows), "no generated theorem/source/score/claim flags are true"),
        ("VAL2303_17_branch_copies", all(str(row["target_exists"]) == "True" and str(row["target_parses"]) == "True" for row in sections["branch_copies"]), "branch/queue copies exist and parse"),
        ("VAL2303_18_formalization_untouched", formalization_2303_output_count() == 0, "no 2303 checkpoint/output files were written under formalization-workbench"),
        ("VAL2303_19_no_pycache", not pycache_exists(), "scripts __pycache__ removed"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2303_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2303 performs a focused q field-content/no-spurion source hunt, keeps B_qWeyl zero unactivated, writes a nonclaim local bound acquisition interface, and selects no-Weyl-spurion derivation or first source input next",
        }
    )
    return rows


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 2303 - Y5/R2FR q Field-Content No-Spurion Certificate Or B_qWeyl Local Bound Acquisition",
            "## Verdict\n\n2303 looked where the q certificate would actually be if the corpus already had it: the quotient-map chain, coframe/matter factorization chain, no-marker/no-spurion chain, q/vX action-descent chain, and the 2302 B_qWeyl gate. Result: the route is real, but not source-closed. Existing files give conditional q-map and factorization lemmas; they do not parent-sign q field-content, transform law, actual vertical direction, action descent, no Weyl-type spurion/projector, or boundary/source neutrality.\n\nSo the clean theorem remains: `B_qWeyl=0` if the parent action signs scalar/quotient q plus no Weyl-index carrier, or if q is first-class absent. But current MTS cannot spend that theorem yet. The useful gain is that the future parent q clause is now exact, and the fallback `B_qWeyl` acquisition interface now names the first real inputs needed: parent coefficient, q operator/Green norm, Weyl scale, arena projection, and absolute body/boundary/tail envelope.",
            "## Source Register\n\n" + md_table(sections["source_register"]),
            "## Focused q Source Scan\n\n" + md_table(sections["source_scan"]),
            "## q Field-Content Certificate Source Hunt\n\n" + md_table(sections["q_certificate"]),
            "## q No-Spurion Certificate Source Hunt\n\n" + md_table(sections["no_spurion"]),
            "## B_qWeyl Local Bound Acquisition Requirements\n\n" + md_table(sections["bqweyl_acquisition"]),
            "## B_qWeyl Arena Projection Rows\n\n" + md_table(sections["arena_projection"]),
            "## Candidate Parent q Clause Nonclaim\n\n" + md_table(sections["candidate_parent_clause"]),
            "## Refusal Runner\n\n" + md_table(sections["runner_refusal"]),
            "## Claim Gates\n\n" + md_table(sections["claim_gates"]),
            "## Decision Ledger\n\n" + md_table(sections["decision"]),
            "## Next Target\n\n" + md_table(sections["next_target"]),
            "## Branch Copies\n\n" + md_table(sections["branch_copies"]),
            "## Validation\n\n" + md_table(sections["validation"]),
            "## Working Interpretation\n\nThis is the coupling fight getting cleaner. We did not knock the dragon out, but we found the throat: no Weyl-index carrier in the parent object language. If we can derive that, `B_qWeyl` dies structurally. If not, it becomes a normal coefficient with normal evidence rules, not a ghost in the walls.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    sections = {
        "source_register": source_register_rows(),
        "source_scan": focused_source_scan_rows(),
        "q_certificate": q_certificate_rows(),
        "no_spurion": no_spurion_rows(),
        "bqweyl_acquisition": bqweyl_acquisition_rows(),
        "arena_projection": arena_projection_rows(),
        "candidate_parent_clause": candidate_parent_clause_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], sections["source_register"])
    write_csv(OUTPUTS["source_scan"], sections["source_scan"])
    write_csv(OUTPUTS["q_certificate"], sections["q_certificate"])
    write_csv(OUTPUTS["no_spurion"], sections["no_spurion"])
    write_csv(OUTPUTS["bqweyl_acquisition"], sections["bqweyl_acquisition"])
    write_csv(OUTPUTS["arena_projection"], sections["arena_projection"])
    write_csv(OUTPUTS["candidate_parent_clause"], sections["candidate_parent_clause"])
    write_csv(OUTPUTS["runner_refusal"], sections["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], sections["claim_gates"])
    write_csv(OUTPUTS["decision"], sections["decision"])
    write_csv(OUTPUTS["next_target"], sections["next_target"])

    sections["branch_copies"] = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], sections["branch_copies"])

    remove_pycache()
    sections["validation"] = validation_rows(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    remove_pycache()
    sections["validation"] = validation_rows(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])

    DOC.write_text(build_doc(sections), encoding="utf-8")

    if not all(row["result"] == "PASS" for row in sections["validation"]):
        raise SystemExit("2303 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
