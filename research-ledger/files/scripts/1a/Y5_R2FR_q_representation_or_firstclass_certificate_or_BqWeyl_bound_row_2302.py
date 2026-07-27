from __future__ import annotations

import csv
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

BRANCH_ID = "MTS_R2FR_Q_REPRESENTATION_FIRSTCLASS_BQWEYL_2302"
DOC = ROOT / "2302-Y5-R2FR-q-representation-or-firstclass-certificate-or-BqWeyl-bound-row.md"

PATHS = {
    "2301_doc": ROOT / "2301-Y5-R2FR-q-firstclass-removal-or-Ricci-Weyl-source-vector-split.md",
    "2301_validation": OUT / "P8_Y5_BRR545_2301_VALIDATION.csv",
    "2301_next": OUT / "P8_Y5_PARENT_QLOC_2301_NEXT_TARGET.csv",
    "2301_rep_gate": OUT / "P8_Y5_PARENT_QLOC_2301_Q_REPRESENTATION_TYPE_GATE.csv",
    "2301_firstclass": OUT / "P8_Y5_PARENT_QLOC_2301_Q_FIRSTCLASS_REMOVAL_ATTEMPT.csv",
    "2301_split": OUT / "P8_Y5_PARENT_QLOC_2301_Q_RICCI_WEYL_SPLIT_ATTEMPT.csv",
    "2301_residuals": OUT / "P8_Y5_PARENT_QLOC_2301_Q_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv",
    "2254_doc": ROOT / "2254-Y5-R2FR-RAB-representation-certificate-or-BWeyl-bound-row.md",
    "2254_validation": OUT / "P8_Y5_BRR545_2254_VALIDATION.csv",
    "2254_weyl_index": OUT / "P8_Y5_PARENT_QLOC_2254_BWEYL_INDEX_ZERO_THEOREM_GATE.csv",
    "2254_certificate": OUT / "P8_Y5_PARENT_QLOC_2254_RAB_REPRESENTATION_CERTIFICATE_ATTEMPT.csv",
    "1022_quotient": ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
    "1156_functor": ROOT / "1156-Y5-R10-parent-quotient-matter-functor-signature-or-frame-leak-bound-fill.md",
    "1157_qmap": ROOT / "1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md",
    "1761_spurion": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
    "1768_normal_form": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
    "2297_body": ROOT / "2297-Y5-R2FR-Jq-source-zero-or-component-bound-pack.md",
    "2300_normal_form": ROOT / "2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md",
}

SOURCES = [
    ("SRC2302_00_2301_doc", "2301_handoff", PATHS["2301_doc"], ["DEC2301_4_next", "Q_REPRESENTATION_OR_FIRSTCLASS_CERTIFICATE_OR_BQWEYL_BOUND_NEXT"], "direct handoff selecting q representation/firstclass certificate or B_qWeyl bound"),
    ("SRC2302_01_2301_validation", "2301_validation", PATHS["2301_validation"], ["VAL2301_OVERALL", "PASS"], "confirms 2301 passed before 2302 starts"),
    ("SRC2302_02_2301_next", "2301_next", PATHS["2301_next"], ["2302-Y5-R2FR-q-representation-or-firstclass-certificate-or-BqWeyl-bound-row.md", "B_qWeyl"], "next-target contract"),
    ("SRC2302_03_2301_rep_gate", "2301_rep_gate", PATHS["2301_rep_gate"], ["QREP2301_5_verdict", "FAIL_CURRENT_CLAIM"], "incoming q representation gate blocks Weyl-zero claim"),
    ("SRC2302_04_2301_firstclass", "2301_firstclass", PATHS["2301_firstclass"], ["QFC2301_6_verdict", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED"], "incoming q first-class package remains unsigned"),
    ("SRC2302_05_2301_split", "2301_split", PATHS["2301_split"], ["QRWS2301_3_representation_escape", "EXACT_CONDITIONAL_INDEX_THEOREM"], "conditional q-Weyl index theorem from Ricci/Weyl split"),
    ("SRC2302_06_2301_residuals", "2301_residuals", PATHS["2301_residuals"], ["QCURV2301_0_BqWeyl", "MISSING_REPRESENTATION_OR_FIRSTCLASS_CERTIFICATE_OR_BOUND"], "B_qWeyl residual row to refine"),
    ("SRC2302_07_2254_doc", "2254_rab_precedent", PATHS["2254_doc"], ["WZ2254_0_conditional_theorem", "ZERO_THEOREM_NOT_ACTIVATED"], "R_AB Weyl-zero precedent and refusal standard"),
    ("SRC2302_08_2254_validation", "2254_validation", PATHS["2254_validation"], ["VAL2254_OVERALL", "PASS"], "confirms 2254 precedent passed"),
    ("SRC2302_09_2254_weyl_index", "2254_weyl_index", PATHS["2254_weyl_index"], ["WZ2254_0_conditional_theorem", "EXACT_CONDITIONAL_THEOREM"], "index-zero theorem shape"),
    ("SRC2302_10_2254_certificate", "2254_certificate", PATHS["2254_certificate"], ["CERT2254_5_verdict", "FAIL_CURRENT_CLAIM"], "representation certificate must be parent-signed, not inferred"),
    ("SRC2302_11_1022_quotient", "1022_quotient", PATHS["1022_quotient"], ["VQC1022_7_verdict", "fail_current_claim_but_best_next_target"], "older quotient/vertical no-pole route is conditional and unsigned"),
    ("SRC2302_12_1156_functor", "1156_functor", PATHS["1156_functor"], ["QMF1156_7_verdict", "QUOTIENT_MATTER_FUNCTOR_NOT_PARENT_SIGNED"], "q/matter functor route remains unsigned"),
    ("SRC2302_13_1157_qmap", "1157_qmap", PATHS["1157_qmap"], ["QMAP1157_8_verdict", "PARENT_Q_MAP_NULL_GENERATOR_NOT_DERIVED"], "parent q-map/null-generator proof explicitly fails current corpus"),
    ("SRC2302_14_1761_spurion", "1761_spurion", PATHS["1761_spurion"], ["SP1761_4_hidden_frame", "LIVE_UNLESS_DECLARED_EXTENSION"], "hidden conformal/disformal frame countermodel"),
    ("SRC2302_15_1768_normal_form", "1768_normal_form", PATHS["1768_normal_form"], ["SCL1768_2_nonminimal_coupling", "SCL1768_5_post_variation_projector"], "normal-form warning for hidden projectors/nonminimal couplings"),
    ("SRC2302_16_2297_body", "2297_body", PATHS["2297_body"], ["Q_q[body]", "EXTERIOR_ZERO_INSUFFICIENT_BODY_CHARGE_OPEN"], "body/worldtube charge remains a separate local source route"),
    ("SRC2302_17_2300_normal_form", "2300_normal_form", PATHS["2300_normal_form"], ["QRES2300_0_BqWeyl", "MISSING_Q_WEYL_COUPLING_ZERO_OR_BOUND"], "minimal q source-vector normal form already identifies B_qWeyl"),
]

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2302_SOURCE_REGISTER.csv",
    "evidence": OUT / "P8_Y5_PARENT_QLOC_2302_REPRESENTATION_EVIDENCE_LEDGER.csv",
    "representation_certificate": OUT / "P8_Y5_PARENT_QLOC_2302_Q_REPRESENTATION_CERTIFICATE_ATTEMPT.csv",
    "firstclass_certificate": OUT / "P8_Y5_PARENT_QLOC_2302_Q_FIRSTCLASS_CERTIFICATE_ATTEMPT.csv",
    "bqweyl_index": OUT / "P8_Y5_PARENT_QLOC_2302_BQWEYL_INDEX_ZERO_THEOREM_GATE.csv",
    "bqweyl_bound": OUT / "P8_Y5_PARENT_QLOC_2302_BQWEYL_BOUND_ROW_NONCLAIM.csv",
    "local_implications": OUT / "P8_Y5_PARENT_QLOC_2302_LOCAL_IMPLICATION_LEDGER.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2302_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2302_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2302_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2302_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2302_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2302_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_certificate": QUEUE / "JR2302_Q_REPRESENTATION_FIRSTCLASS_NONCLAIM.csv",
    "queue_bqweyl": QUEUE / "JR2302_BQWEYL_BOUND_ROW_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "q_BqWeyl_representation_nonclaim_2302.csv",
    "beta_docs": BETA_DOCS / "Q_BQWEYL_REPRESENTATION_2302_NONCLAIM.csv",
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


def evidence_rows() -> list[dict[str, Any]]:
    rows = [
        ("EVID2302_0_2301_type_gate", "2301 identifies scalar/quotient q and first-class absent q as the only clean B_qWeyl zero routes.", "supports exact route selection, not a current proof", "ZERO_ROUTE_IDENTIFIED_NOT_CERTIFIED", "QREP2301_5 still fails current claim", "2301_rep_gate;2301_handoff"),
        ("EVID2302_1_quotient_chain", "1022/1156/1157 contain a real quotient/null route: q map, vertical kernel, action/matter descent, and boundary silence.", "strong conditional spine exists", "CONDITIONAL_ROUTE_SHAPE_PRESENT", "1157 explicitly forbids q by declaration and says parent q-map/null generator is not derived", "1022_quotient;1156_functor;1157_qmap"),
        ("EVID2302_2_firstclass_package", "2301 first-class checklist demands Omega, momentum map, bracket closure, degree count, matter descent, and boundary/source neutrality.", "first-class would kill B_qWeyl if signed", "CLEANEST_ROUTE_BUT_UNSIGNED", "QFC2301_6 remains FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED", "2301_firstclass;2300_normal_form"),
        ("EVID2302_3_index_precedent", "2254 already established the right Weyl-zero discipline: index theorem plus parent representation/no-spurion certificate.", "q should be held to same standard as R_AB", "PRECEDENT_MATCHES_Q_GATE", "2254 refused activation without certificate", "2254_rab_precedent;2254_weyl_index;2254_certificate"),
        ("EVID2302_4_spurion_countermodels", "1761/1768 retain hidden frame, nonminimal coupling, and post-variation projector channels.", "scalar-looking q can still leak Weyl/source indices through hidden objects", "NO_SPURION_NOT_CERTIFIED", "must prove no Weyl-type projector/spurion in the same parent action", "1761_spurion;1768_normal_form"),
        ("EVID2302_5_body_charge", "2297 warns exterior source silence is insufficient because Q_q[body] can set exterior q data.", "first-class/no-spurion theorem must also neutralize body/boundary source data", "BOUNDARY_BODY_NEUTRALITY_REQUIRED", "Q_q[body] remains unsigned/bounded only as nonclaim", "2297_body;2300_normal_form"),
        ("EVID2302_6_verdict", "current evidence audit", "B_qWeyl zero is a sharp conditional theorem, but current corpus does not parent-sign q representation, first-class removal, or no-spurion silence.", "BQWEYL_ZERO_NOT_ACTIVATED", "stage B_qWeyl bound row and target parent q field-content/no-spurion source hunt", "2301_handoff;2254_rab_precedent;1157_qmap;1768_normal_form"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "evidence_id": evidence_id,
            "evidence": evidence,
            "interpretation": interpretation,
            "status": status,
            "limitation": limitation,
            "source_keys": source_keys,
            "source_paths": ";".join(src(key) for key in source_keys.split(";")),
            **false_flags(),
        }
        for evidence_id, evidence, interpretation, status, limitation, source_keys in rows
    ]


def representation_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        ("QRC2302_0_parent_q_object", "parent q object", "q: Phi_parent -> Q_obs is constructed before local fitting, with domain/equivalence relation declared", "CONDITIONAL_SUPPORT_NOT_PARENT_SIGNED", "MISSING_PARENT_Q_OBJECT_FOR_THIS_Q"),
        ("QRC2302_1_scalar_quotient_type", "scalar/quotient type", "q carries no Weyl/Riemann four-index structure and no hidden tensor/projector index", "NOT_PARENT_CERTIFIED", "MISSING_Q_SCALAR_QUOTIENT_TYPE_DECLARATION"),
        ("QRC2302_2_transform_law", "transformation law", "q transforms as scalar/density/quotient coordinate under diffeomorphism, local Lorentz, and internal vertical maps", "NOT_DECLARED_FOR_THIS_BRANCH", "MISSING_Q_TRANSFORMATION_LAW"),
        ("QRC2302_3_measure_density", "density/measure convention", "any density weight is absorbed by the action measure and does not supply Weyl indices", "NOT_CERTIFIED", "MISSING_Q_DENSITY_MEASURE_CERTIFICATE"),
        ("QRC2302_4_no_tensor_projector", "no hidden tensor/projector q", "no parent projector, frame, readout tensor, or history kernel carries Weyl-type indices into the q slot", "NOT_CERTIFIED", "MISSING_NO_Q_PROJECTOR_TENSOR_CERTIFICATE"),
        ("QRC2302_5_no_Weyl_spurion", "no Weyl-type spurion", "the parent action has no background/projector/spurion P^{munuab} that can form q P^{munuab} C_munuab", "NOT_CERTIFIED", "MISSING_NO_WEYL_SPURION_THEOREM"),
        ("QRC2302_6_boundary_readout_silence", "boundary/readout silence", "boundary/source/readout/projector operations do not reintroduce B_qWeyl after reduction", "NOT_CERTIFIED", "MISSING_BOUNDARY_READOUT_NO_REENTRY"),
        ("QRC2302_7_verdict", "q representation certificate", "QRC2302_0 through QRC2302_6 must close in one parent branch", "FAIL_CURRENT_CLAIM", "Q_REPRESENTATION_NO_SPURION_CERTIFICATE_NOT_PARENT_SIGNED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "certificate_id": certificate_id,
            "certificate_piece": piece,
            "required_statement": statement,
            "current_status": status,
            "missing_for_claim": missing,
            "source_paths": src("2301_rep_gate", "1022_quotient", "1156_functor", "1157_qmap", "1761_spurion", "1768_normal_form"),
            **false_flags(),
        }
        for certificate_id, piece, statement, status, missing in rows
    ]


def firstclass_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        ("QFCC2302_0_parent_Omega", "parent presymplectic form", "Omega_Y includes q, geometry, matter, boundary, and source/readout variables", "MISSING_PARENT_OMEGA", "cannot call q gauge without full phase-space form"),
        ("QFCC2302_1_generator", "momentum map/generator", "Omega_flat(v_q)=delta C_q plus differentiable boundary generator", "MISSING_MOMENTUM_MAP", "no first-class removal without parent-owned generator"),
        ("QFCC2302_2_brackets", "first-class algebra", "{G_q[epsilon],G_q[eta]} closes with zero/proper boundary term", "MISSING_BRACKET_CLOSURE", "anomaly or edge mode can leave q physical"),
        ("QFCC2302_3_degree_count", "reduced degree count", "constraints remove the q canonical pair and no residual q pole remains", "MISSING_DEGREE_COUNT", "absence of pole cannot be inferred from missing kinetic term"),
        ("QFCC2302_4_matter_descent", "matter/readout descent", "ordinary matter, constants, clocks, source support, and readout maps carry no q charge", "MISSING_MATTER_DESCENT", "source markers can survive bulk constraint"),
        ("QFCC2302_5_boundary_source", "boundary/source neutrality", "Q_q[body], Pi_q, boundary/reference q charges, and tail terms are zero/proper", "MISSING_BOUNDARY_SOURCE_NEUTRALITY", "worldtube/boundary data can source exterior q"),
        ("QFCC2302_6_verdict", "q first-class removal certificate", "QFCC2302_0 through QFCC2302_5 must close together", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED", "finite q residual vector remains live"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "certificate_id": certificate_id,
            "certificate_piece": piece,
            "required_statement": statement,
            "current_status": status,
            "if_missing": if_missing,
            "source_paths": src("2301_firstclass", "2300_normal_form", "2297_body", "1157_qmap"),
            **false_flags(),
        }
        for certificate_id, piece, statement, status, if_missing in rows
    ]


def bqweyl_index_rows() -> list[dict[str, Any]]:
    rows = [
        ("BQWZ2302_0_conditional_theorem", "If q is a scalar/quotient or pure density variable with no Weyl-type spurion/projector, a linear scalar action term q C_munuab is index-forbidden. If q is first-class absent, B_qWeyl is absent after reduction.", "B_qWeyl=0", "EXACT_CONDITIONAL_THEOREM", "premises unsigned"),
        ("BQWZ2302_1_scalar_quotient_case", "A scalar/quotient q cannot by itself contract the trace-free four-index Weyl tensor into a scalar density.", "linear Weyl mixing absent", "CONDITIONAL_ON_Q_TYPE", "q scalar/quotient type not certified"),
        ("BQWZ2302_2_density_case", "A scalar density q still needs only the measure; density weight does not supply four Weyl indices.", "linear q-Weyl term absent unless a projector/spurion is present", "CONDITIONAL_ON_MEASURE_CONVENTION", "density/measure convention not certified"),
        ("BQWZ2302_3_firstclass_case", "If q is removed as a first-class/constraint variable before reduction, all q source slots including B_qWeyl disappear, provided boundary/source charges vanish.", "B_qWeyl absent after reduction", "CONDITIONAL_ON_FIRSTCLASS_CERTIFICATE", "first-class/boundary/source package not signed"),
        ("BQWZ2302_4_spurion_countermodel", "A hidden four-index projector/background tensor/readout kernel can create a legal scalar q P^{munuab} C_munuab.", "B_qWeyl remains live", "COUNTERMODEL_SURVIVES", "no-spurion theorem missing"),
        ("BQWZ2302_5_boundary_readout_countermodel", "Boundary/source/readout or post-variation projector operations can regenerate an effective q-Weyl source even if the bulk term is absent.", "B_qWeyl-like residual remains live", "COUNTERMODEL_SURVIVES", "boundary/readout closure missing"),
        ("BQWZ2302_6_verdict", "B_qWeyl zero theorem", "conditional index theorem is ready, but not activated without q representation/no-spurion or first-class certificate", "ZERO_THEOREM_NOT_ACTIVATED", "MISSING_Q_REPRESENTATION_FIRSTCLASS_OR_NO_SPURION_CERTIFICATE"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "statement": statement,
            "effect": effect,
            "current_status": status,
            "blocker": blocker,
            "source_paths": src("2301_split", "2301_rep_gate", "2254_weyl_index", "1761_spurion", "1768_normal_form"),
            **false_flags(),
        }
        for theorem_id, statement, effect, status, blocker in rows
    ]


def bqweyl_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "BQB2302_0_BqWeyl",
            "symbol": "B_qWeyl",
            "definition": "linear q-Weyl/tidal curvature mixing coefficient in the q Euler source vector",
            "formula_or_bound": "|B_qWeyl| <= theorem_zero_from_BQWZ2302_or_source_backed_bound",
            "units_status": "MISSING_COMMON_Q_OPERATOR_NORMALIZATION",
            "required_sources": "q representation/no-spurion theorem; first-class removal certificate; or numeric/source-backed local curvature residual bound",
            "current_status": "MISSING_REPRESENTATION_FIRSTCLASS_OR_NUMERIC_BOUND",
            "observable_link": "PPN;orbital;local_GR;R10;alpha3",
            "source_paths": src("2301_residuals", "2300_normal_form", "2254_weyl_index"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "BQB2302_1_tau_BqWeyl_local",
            "symbol": "tau_BqWeyl_local",
            "definition": "projection from B_qWeyl C_Weyl to local PPN/orbital/R10/clock residual vector",
            "formula_or_bound": "residual_local <= tau_BqWeyl_local |B_qWeyl| |C_Weyl|",
            "units_status": "MISSING_ARENA_PROJECTION_KERNEL",
            "required_sources": "local curvature scale; source geometry; q Green function; PPN/orbital/R10 projection kernel; units",
            "current_status": "MISSING_ARENA_PROJECTION",
            "observable_link": "PPN;orbital;local_GR;R10",
            "source_paths": src("2301_residuals", "2297_body"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "BQB2302_2_profile_response",
            "symbol": "q_Weyl_profile",
            "definition": "exterior q profile sourced by Weyl/tidal curvature in local vacuum if B_qWeyl survives",
            "formula_or_bound": "q_Weyl <= ||G_q|| |B_qWeyl| |C_Weyl| plus boundary/source tails",
            "units_status": "MISSING_GQ_DOMAIN_AND_CURVATURE_UNITS",
            "required_sources": "q operator normalization; Green/domain choice; exterior Weyl scale; boundary/source tail envelope",
            "current_status": "MISSING_OPERATOR_AND_PROFILE_INPUTS",
            "observable_link": "local_GR;PPN;orbital",
            "source_paths": src("2297_body", "2300_normal_form", "2301_residuals"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "BQB2302_3_claim_status",
            "symbol": "B_qWeyl_claim_status",
            "definition": "claim status for q-Weyl/tidal branch",
            "formula_or_bound": "claim allowed only if BQWZ2302 activates or BQB2302_0/1/2 are numeric, sourced, unit-matched, and within arena bounds",
            "units_status": "status",
            "required_sources": "all above",
            "current_status": "NONCLAIM_BOUND_ROW_STAGED",
            "observable_link": "all_local_arenas",
            "source_paths": src("2301_validation", "2301_residuals"),
            **false_flags(),
        },
    ]
    return rows


def local_implication_rows() -> list[dict[str, Any]]:
    rows = [
        ("LIMP2302_0_exterior_Weyl", "Weyl/tidal curvature is generally nonzero in Schwarzschild/exterior vacuum.", "A surviving B_qWeyl sources q even when T_H and Ricci vanish.", "LOCAL_VACUUM_DANGER_RETAINED", "B_qWeyl zero or bound required"),
        ("LIMP2302_1_nohair_activation", "2296/2300 q no-hair branches cannot activate from exterior J_q=0 alone.", "B_qWeyl, Q_q[body], Pi_q, tails, and readout/source projectors must be zeroed or bounded.", "NOHAIR_NOT_ACTIVATED", "source/body/boundary/tail closures open"),
        ("LIMP2302_2_best_zero_route", "The least-scrutiny route remains structural: q scalar/quotient with no Weyl spurion, or q first-class absent.", "This removes the coupling before fitting rather than hiding a finite coefficient.", "DERIVATION_ROUTE_SELECTED", "parent certificate missing"),
        ("LIMP2302_3_bound_fallback", "If q representation/first-class/no-spurion certification fails, B_qWeyl becomes an ordinary finite residual.", "It must enter the same absolute no-cancellation envelope as C_qT, Q_q[body], boundary and tail rows.", "BOUND_ROUTE_STAGED", "numeric/source-backed rows absent"),
        ("LIMP2302_4_local_GR_claim", "Derived local GR/Newton recovery is not claimable from this checkpoint.", "The dangerous Weyl coupling is not killed and not bounded.", "LOCAL_GR_CLAIM_REFUSED", "B_qWeyl theorem-zero or bound missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "implication_id": implication_id,
            "statement": statement,
            "consequence": consequence,
            "status": status,
            "missing_for_claim": missing,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for implication_id, statement, consequence, status, missing in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2302_0_representation", "q representation/no-spurion certificate closes", "BLOCKED", "QRC2302_7_verdict=FAIL_CURRENT_CLAIM"),
        ("REF2302_1_firstclass", "q first-class removal closes", "BLOCKED", "QFCC2302_6_verdict=FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED"),
        ("REF2302_2_BqWeyl_zero", "B_qWeyl=0 by index theorem", "BLOCKED", "BQWZ2302_6_verdict=ZERO_THEOREM_NOT_ACTIVATED"),
        ("REF2302_3_BqWeyl_bound", "B_qWeyl finite bound is score-ready", "BLOCKED", "BQB2302 rows have missing representation/numeric/unit/projection inputs"),
        ("REF2302_4_local_vacuum", "local q source silence in exterior vacuum", "BLOCKED", "B_qWeyl plus body/boundary/tail/readout routes remain open"),
        ("REF2302_5_local_GR_Newton", "derived local GR/Newton recovery", "BLOCKED", "q representation/source/operator/boundary gates remain open"),
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
        ("CG2302_0_q_representation", "q scalar/quotient/no-spurion representation is parent-signed", "q object, field type, transform law, measure, no-spurion, and readout clauses missing"),
        ("CG2302_1_q_firstclass", "q is first-class/constraint removed", "Omega/DCq/bracket/degree/matter/boundary package missing"),
        ("CG2302_2_BqWeyl_zero", "B_qWeyl theorem-zero is activated", "conditional theorem premises unsigned"),
        ("CG2302_3_BqWeyl_bound", "B_qWeyl bound row is score-ready", "numeric bound, normalization, units, profile, and arena projection missing"),
        ("CG2302_4_local_vacuum", "local q source silence is derived", "Weyl/body/boundary/tail/readout gates open"),
        ("CG2302_5_local_GR_Newton", "local GR/Newton reduction is derived", "B_qWeyl/local q residual vector not closed"),
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
            "decision_id": "DEC2302_0_theorem",
            "decision": "BQWEYL_INDEX_ZERO_THEOREM_READY_CONDITIONAL",
            "rationale": "A scalar/quotient q cannot contract linearly with Weyl without a Weyl-type spurion, and first-class removal would delete q slots entirely.",
            "next_action": "do not activate until q representation/no-spurion or first-class package is parent-signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2302_1_current_corpus",
            "decision": "Q_REPRESENTATION_FIRSTCLASS_NOT_PARENT_SIGNED",
            "rationale": "1022/1156/1157 support the quotient route only conditionally; 2301 first-class checklist remains unsigned; 1761/1768 leave spurion/projector channels open.",
            "next_action": "keep B_qWeyl live; do not claim local vacuum source silence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2302_2_bound_fallback",
            "decision": "BQWEYL_BOUND_ROW_STAGED_NONCLAIM",
            "rationale": "If the structural certificate fails, B_qWeyl is a finite exterior-vacuum residual and must be bounded with normalization, profile, and arena projection.",
            "next_action": "stage B_qWeyl/tau/profile rows as nonclaim acquisition inputs",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2302_3_next",
            "decision": "Q_FIELD_CONTENT_NO_SPURION_OR_BQWEYL_BOUND_ACQUISITION_NEXT",
            "rationale": "The next useful move is not another broad audit: either source the q field-content/no-spurion certificate directly, or start source-backed B_qWeyl local bound acquisition.",
            "next_action": "2303-Y5-R2FR-q-field-content-no-spurion-certificate-or-BqWeyl-local-bound-acquisition.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2302_0_primary",
            "next_target": "2303-Y5-R2FR-q-field-content-no-spurion-certificate-or-BqWeyl-local-bound-acquisition.md",
            "script": "scripts/Y5_R2FR_q_field_content_no_spurion_certificate_or_BqWeyl_local_bound_acquisition_2303.py",
            "objective": "source the parent q field-content/type/transform/no-spurion certificate; if that fails, fill source-ready B_qWeyl, tau_BqWeyl_local, q_Weyl_profile, and arena projection rows without claims",
            "selection_status": "selected",
            "success_condition": "B_qWeyl theorem-zero activates from parent-signed q/no-spurion or first-class certificate, or a numeric/source-backed B_qWeyl local bound acquisition pack exists as nonclaim",
            "forbidden_shortcuts": "assuming scalar q from notation; q by declaration; absence-of-search-hit proof; ignoring hidden spurions/projectors; treating exterior vacuum as Weyl-silent; local-GR/R10/PPN claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2302_1_parallel",
            "next_target": "2302b-Y5-R2FR-BqRic-operator-domain-and-Schur-bound.md",
            "script": "scripts/Y5_R2FR_BqRic_operator_domain_and_Schur_bound_2302b.py",
            "objective": "separately test whether B_qRic is LHS-owned by a positive Schur/diagonalized operator block; do not use this to silence B_qWeyl",
            "selection_status": "parallel_held",
            "success_condition": "B_qRic is operator-owned or retained as finite residual, while B_qWeyl remains independently zeroed/bounded",
            "forbidden_shortcuts": "using Ricci silence to erase Weyl; Schur condition without operator domains; cancellation with B_qWeyl",
            "valid_for_claim": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    plan = [
        ("queue_certificate", OUTPUTS["representation_certificate"], COPY_TARGETS["queue_certificate"], "q representation/first-class certificate nonclaim queue"),
        ("queue_bqweyl", OUTPUTS["bqweyl_bound"], COPY_TARGETS["queue_bqweyl"], "B_qWeyl bound row nonclaim queue"),
        ("branch_wep", OUTPUTS["bqweyl_bound"], COPY_TARGETS["branch_wep"], "WEP/local branch locked q B_qWeyl residual copy"),
        ("beta_docs", OUTPUTS["bqweyl_index"], COPY_TARGETS["beta_docs"], "beta-source docs q B_qWeyl index theorem nonclaim copy"),
    ]
    rows = []
    for copy_key, source_path, target_path, reason in plan:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2302_{copy_key}",
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


def formalization_2302_output_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    markers = [
        "2302-Y5-R2FR-q-representation-or-firstclass-certificate-or-BqWeyl-bound-row",
        "P8_Y5_PARENT_QLOC_2302",
        "P8_Y5_BRR545_2302",
        "JR2302_",
        "q_BqWeyl_representation_nonclaim_2302",
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

    checks = [
        ("VAL2302_00_sources_exist", all(str(row["exists"]) == "True" for row in sections["source_register"]), "all cited source paths exist"),
        ("VAL2302_01_needles_present", all(str(row["needles_present"]) == "True" for row in sections["source_register"]), "all cited source needles are present"),
        ("VAL2302_02_prior_validation", all(str(row["validation_overall_pass"]) in ("", "True") for row in sections["source_register"]), "2301 and 2254 validation pass where checked"),
        ("VAL2302_03_evidence_verdict", any(row["evidence_id"] == "EVID2302_6_verdict" and row["status"] == "BQWEYL_ZERO_NOT_ACTIVATED" for row in sections["evidence"]), "evidence ledger refuses B_qWeyl zero activation"),
        ("VAL2302_04_rep_certificate_blocks", any(row["certificate_id"] == "QRC2302_7_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in sections["representation_certificate"]), "q representation certificate remains blocked"),
        ("VAL2302_05_firstclass_blocks", any(row["certificate_id"] == "QFCC2302_6_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED" for row in sections["firstclass_certificate"]), "q first-class certificate remains blocked"),
        ("VAL2302_06_index_theorem_conditional", any(row["theorem_id"] == "BQWZ2302_0_conditional_theorem" and row["current_status"] == "EXACT_CONDITIONAL_THEOREM" for row in sections["bqweyl_index"]), "conditional B_qWeyl index theorem is recorded"),
        ("VAL2302_07_zero_not_activated", any(row["theorem_id"] == "BQWZ2302_6_verdict" and row["current_status"] == "ZERO_THEOREM_NOT_ACTIVATED" for row in sections["bqweyl_index"]), "B_qWeyl zero theorem is not activated"),
        ("VAL2302_08_bound_row_nonclaim", any(row["bound_id"] == "BQB2302_0_BqWeyl" and row["current_status"] == "MISSING_REPRESENTATION_FIRSTCLASS_OR_NUMERIC_BOUND" for row in sections["bqweyl_bound"]), "B_qWeyl bound row remains nonclaim"),
        ("VAL2302_09_local_implication_refuses", any(row["implication_id"] == "LIMP2302_4_local_GR_claim" and row["status"] == "LOCAL_GR_CLAIM_REFUSED" for row in sections["local_implications"]), "local-GR claim is refused"),
        ("VAL2302_10_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in sections["runner_refusal"]), "refusal runner blocks all current claims"),
        ("VAL2302_11_claim_gates_blocked", all(str(row["gate_pass"]) == "False" for row in sections["claim_gates"]), "claim gates are blocked"),
        ("VAL2302_12_decision_next", any(row["decision_id"] == "DEC2302_3_next" and "BQWEYL" in row["decision"] for row in sections["decision"]), "decision selects q field-content/no-spurion or B_qWeyl bound acquisition next"),
        ("VAL2302_13_next_selected", any(row["route_id"] == "NEXT2302_0_primary" and row["selection_status"] == "selected" for row in sections["next_target"]), "next target selected"),
        ("VAL2302_14_csv_parse", csv_parse_ok, "all generated 2302 CSVs parse"),
        ("VAL2302_15_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" for row in all_rows), "no generated theorem/source/score/claim flags are true"),
        ("VAL2302_16_branch_copies", all(str(row["target_exists"]) == "True" and str(row["target_parses"]) == "True" for row in sections["branch_copies"]), "branch/queue copies exist and parse"),
        ("VAL2302_17_formalization_untouched", formalization_2302_output_count() == 0, "no 2302 checkpoint/output files were written under formalization-workbench"),
        ("VAL2302_18_no_pycache", not pycache_exists(), "scripts __pycache__ removed"),
    ]

    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2302_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2302 records the conditional B_qWeyl zero theorem, refuses current q representation/firstclass/no-spurion promotion, stages nonclaim B_qWeyl bound rows, and selects q field-content/no-spurion or local bound acquisition next",
        }
    )
    return rows


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 2302 - Y5/R2FR q Representation Or First-Class Certificate Or B_qWeyl Bound Row",
            "## Verdict\n\n2302 takes the cleanest derivation route first and does not get to claim it. The exact conditional theorem is now sharp: if `q` is parent-signed as a scalar/quotient or pure density variable with no Weyl-type spurion/projector, a linear `B_qWeyl C_Weyl` source is index-forbidden; if `q` is first-class absent, the slot disappears after reduction.\n\nCurrent corpus status: not signed. The older quotient/null route is useful but explicitly conditional, the first-class package lacks Omega/generator/brackets/degree/matter/boundary clauses, and hidden frame/projector/nonminimal channels remain open. Therefore `B_qWeyl=0` is not activated. `B_qWeyl` is staged as a nonclaim local-vacuum residual bound row, and the next target is a direct q field-content/no-spurion source hunt or local bound acquisition.",
            "## Source Register\n\n" + md_table(sections["source_register"]),
            "## Representation Evidence Ledger\n\n" + md_table(sections["evidence"]),
            "## q Representation Certificate Attempt\n\n" + md_table(sections["representation_certificate"]),
            "## q First-Class Certificate Attempt\n\n" + md_table(sections["firstclass_certificate"]),
            "## B_qWeyl Index-Zero Theorem Gate\n\n" + md_table(sections["bqweyl_index"]),
            "## B_qWeyl Bound Row\n\n" + md_table(sections["bqweyl_bound"]),
            "## Local Implication Ledger\n\n" + md_table(sections["local_implications"]),
            "## Refusal Runner\n\n" + md_table(sections["runner_refusal"]),
            "## Claim Gates\n\n" + md_table(sections["claim_gates"]),
            "## Decision Ledger\n\n" + md_table(sections["decision"]),
            "## Next Target\n\n" + md_table(sections["next_target"]),
            "## Branch Copies\n\n" + md_table(sections["branch_copies"]),
            "## Validation\n\n" + md_table(sections["validation"]),
            "## Working Interpretation\n\nThis is not a circle; it is the lock picking itself. The coupling can probably be killed cleanly, but only if the parent action says what `q` is and forbids the hidden Weyl-index carrier. Until then, `B_qWeyl` is the dragon tooth in local vacuum: small maybe, zero maybe, but not free.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    sections = {
        "source_register": source_register_rows(),
        "evidence": evidence_rows(),
        "representation_certificate": representation_certificate_rows(),
        "firstclass_certificate": firstclass_certificate_rows(),
        "bqweyl_index": bqweyl_index_rows(),
        "bqweyl_bound": bqweyl_bound_rows(),
        "local_implications": local_implication_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], sections["source_register"])
    write_csv(OUTPUTS["evidence"], sections["evidence"])
    write_csv(OUTPUTS["representation_certificate"], sections["representation_certificate"])
    write_csv(OUTPUTS["firstclass_certificate"], sections["firstclass_certificate"])
    write_csv(OUTPUTS["bqweyl_index"], sections["bqweyl_index"])
    write_csv(OUTPUTS["bqweyl_bound"], sections["bqweyl_bound"])
    write_csv(OUTPUTS["local_implications"], sections["local_implications"])
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
        raise SystemExit("2302 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
