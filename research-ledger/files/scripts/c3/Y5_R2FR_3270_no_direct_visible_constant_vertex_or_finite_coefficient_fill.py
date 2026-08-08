from __future__ import annotations

import csv
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3270-Y5-R2FR-no-direct-visible-constant-vertex-or-finite-coefficient-fill-under-AX1090.md"

SRC_3269_DOC = ROOT / "3269-Y5-R2FR-fixed-local-constants-superselection-for-DD-zero-or-coefficient-runner-under-AX1090.md"
SRC_3269_CLAUSES = OUT / "P8_Y5_R2FR_3269_FIXED_CONSTANTS_SUPERSELECTION_CLAUSES.csv"
SRC_3269_RUNNER = OUT / "P8_Y5_R2FR_3269_COEFFICIENT_RUNNER_RESULTS_NONCLAIM.csv"
SRC_3265_DELTA = OUT / "P8_Y5_R2FR_3265_TWO_ARENA_DELTA_MATRIX_NONCLAIM.csv"
SRC_3266_THEOREM = OUT / "P8_Y5_R2FR_3266_RESIDUAL_INCLUSIVE_INVERSION_THEOREM.csv"
SRC_CONST = OUT / "P8_constant_sector_universality_CONTRACT.csv"
SRC_GUARDS_3008 = OUT / "P8_Y5_R2FR_3008_COUPLING_GUARD_ROWS.csv"
SRC_MATTER_955 = OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv"
SRC_FV_1098 = OUT / "P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv"
SRC_THM_1098 = OUT / "P8_Y5_R10_1098_ACTION_SIGNATURE_THEOREM.csv"
SRC_MHM_1105 = OUT / "P8_Y5_R10_1105_MASTER_MORPHISM_THEOREM_ATTEMPT.csv"
SRC_SUB_1105 = OUT / "P8_Y5_R10_1105_MASTER_MORPHISM_SUBCASE_MAP.csv"
SRC_FIN_1105 = OUT / "P8_Y5_R10_1105_FINITE_SOURCE_REQUIREMENTS.csv"
SRC_F2_1057 = OUT / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv"
SRC_CT_1057 = OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"
SRC_GRAMMAR_1065 = OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv"
SRC_WA_1065 = OUT / "P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv"
SRC_SIG_1104 = ROOT / "1104-Y5-R10-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md"
SRC_MOMS_1090 = ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3270_SOURCE_REGISTER.csv",
    "sweep_summary": OUT / "P8_Y5_R2FR_3270_VISIBLE_VERTEX_CORPUS_SWEEP_SUMMARY.csv",
    "sweep_hits": OUT / "P8_Y5_R2FR_3270_VISIBLE_VERTEX_CORPUS_SWEEP_HITS.csv",
    "theorem": OUT / "P8_Y5_R2FR_3270_NO_DIRECT_VERTEX_THEOREM_OR_NO_GO.csv",
    "vertex_classes": OUT / "P8_Y5_R2FR_3270_VISIBLE_VERTEX_CLASSIFICATION.csv",
    "finite_schema": OUT / "P8_Y5_R2FR_3270_FINITE_VERTEX_COEFFICIENT_SCHEMA.csv",
    "finite_rows": OUT / "P8_Y5_R2FR_3270_FINITE_VERTEX_COEFFICIENT_ROWS_NONCLAIM.csv",
    "candidate_inputs": OUT / "P8_Y5_R2FR_3270_VERTEX_CANDIDATE_INPUTS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3270_VERTEX_DD_RUNNER_RESULTS_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3270_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3270_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3270_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3270_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def source_parse_ok(path: Path) -> bool:
    if path.suffix.lower() == ".csv":
        return csv_parse_ok(path)
    return text_parse_ok(path)


def compact_text(value: str, limit: int = 420) -> str:
    text = re.sub(r"\s+", " ", value).strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


def evidence_hits(path: Path, patterns: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as exc:
        return f"READ_ERROR:{exc}"
    hits: list[str] = []
    lowered_patterns = [pattern.lower() for pattern in patterns]
    for idx, line in enumerate(lines, start=1):
        low = line.lower()
        if any(pattern in low for pattern in lowered_patterns):
            hits.append(f"L{idx}:{compact_text(line, 260)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def source_register() -> list[dict[str, Any]]:
    sources = [
        (SRC_3269_DOC, "3269 handoff: fixed constants zero route and 3270 target", ["NEXT3269", "no direct", "C_g=C_hatm=C_e"]),
        (SRC_3269_CLAUSES, "3269 fixed-constants clauses", ["FC3269_2", "no direct", "CONDITIONAL"]),
        (SRC_3269_RUNNER, "3269 DD coefficient runner", ["CASE3269", "D_hatm", "D_e"]),
        (SRC_3265_DELTA, "rank-two MICROSCOPE/Eot-Wash DD matrix", ["MICROSCOPE", "EOTWASH", "Delta_Q"]),
        (SRC_3266_THEOREM, "residual-inclusive inversion theorem", ["residual", "inverse", "D_hatm"]),
        (SRC_CONST, "constant-sector universality contract", ["C2_no_direct", "C4_no_constant", "C7_empirical"]),
        (SRC_GUARDS_3008, "coupling guard rows", ["CG3008_1", "source-only", "hidden frame"]),
        (SRC_MATTER_955, "minimal matter action source-coupling lemma", ["MMA955_5", "relative", "source-only"]),
        (SRC_FV_1098, "forbidden visible vertex audit", ["scalar_F2", "mass_X", "source_weight"]),
        (SRC_THM_1098, "ordinary constant owner theorem and counterexample", ["chain_rule", "counterexample", "verdict"]),
        (SRC_MHM_1105, "master hidden-visible morphism theorem attempt", ["MHM1105_3", "symmetry", "verdict"]),
        (SRC_SUB_1105, "master morphism subcase map", ["SUB1105", "RETAINED_RESIDUAL", "source"]),
        (SRC_FIN_1105, "finite source requirements", ["FIN1105", "needed_row", "missing"]),
        (SRC_F2_1057, "unique Maxwell subblock theorem attempt", ["UMS1057", "F_Q^2", "counterterm"]),
        (SRC_CT_1057, "F2 counterterm ledger", ["hidden scalar", "LEGAL", "radiative"]),
        (SRC_GRAMMAR_1065, "parent no-source-only grammar audit", ["PGG1065", "w_A", "source"]),
        (SRC_WA_1065, "w_A theorem-zero clauses", ["WTZ1065", "Delta_w", "verdict"]),
        (SRC_SIG_1104, "ordinary-sector action signature ledger", ["SIG1104", "THM1104", "hidden-visible"]),
        (SRC_MOMS_1090, "MOMS synthesis and missing axiom ledger", ["AX1090_1", "operator-domain", "hidden"]),
    ]
    rows = []
    for idx, (path, role, patterns) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3270_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(source_parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, patterns),
                "valid_for_claim": "false",
            }
        )
    return rows


SWEEP_PATTERNS = [
    ("alpha_EM_X", "alpha_EM(X)"),
    ("mass_X", "m_A(X)"),
    ("fX_F2", "f_X(Xhat)F_Q^2"),
    ("hidden_F2", "f(I_hid)F^2"),
    ("source_only", "source-only"),
    ("wA_X", "w_A(Xhat)"),
    ("kappaA_X", "kappa_A(Xhat)"),
    ("hidden_visible_hom", "hidden-visible"),
    ("shadow_frame", "shadow frame"),
    ("disformal", "disformal"),
    ("no_direct_vertex", "no direct"),
]

_CORPUS_FILES_CACHE: list[Path] | None = None
_SWEEP_SUMMARY_CACHE: list[dict[str, Any]] | None = None
_SWEEP_HITS_CACHE: list[dict[str, Any]] | None = None


def corpus_files() -> list[Path]:
    global _CORPUS_FILES_CACHE
    if _CORPUS_FILES_CACHE is not None:
        return _CORPUS_FILES_CACHE
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        parts = {part.lower() for part in rel.parts}
        if ".venv-score" in parts or "__pycache__" in parts or "runs" in parts:
            continue
        if path.suffix.lower() not in {".md", ".csv"}:
            continue
        if path.name.startswith("3270-") or path.name.startswith("P8_Y5_R2FR_3270") or path.name.startswith("P8_Y5_BRR545_3270"):
            continue
        files.append(path)
    _CORPUS_FILES_CACHE = sorted(files)
    return _CORPUS_FILES_CACHE


def classify_hit(line: str) -> str:
    up = line.upper()
    if "EXACT_CONDITIONAL" in up or "CONDITIONAL" in up:
        return "conditional_theorem_or_clause"
    if "COUNTEREXAMPLE" in up or "LEGAL" in up or "LIVE" in up or "RETAINED" in up:
        return "retained_countermodel_or_residual"
    if "NOT_PARENT" in up or "UNSIGNED" in up or "NOT_DERIVED" in up:
        return "unsigned_blocker"
    if "POLICY" in up or "FORBIDDEN" in up:
        return "policy_or_required_forbidden_vertex"
    if "CLAIM_ALLOWED" in up or "VALID_FOR_CLAIM" in up:
        return "claim_gate_context"
    return "context_hit"


def build_corpus_sweep(max_hits_per_pattern: int = 35) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    global _SWEEP_SUMMARY_CACHE, _SWEEP_HITS_CACHE
    if _SWEEP_SUMMARY_CACHE is not None and _SWEEP_HITS_CACHE is not None:
        return _SWEEP_SUMMARY_CACHE, _SWEEP_HITS_CACHE
    files = corpus_files()
    summary_state: dict[str, dict[str, Any]] = {}
    lowered_patterns = [(name, pattern, pattern.lower()) for name, pattern in SWEEP_PATTERNS]
    for name, pattern, _ in lowered_patterns:
        summary_state[name] = {
            "pattern_id": name,
            "pattern": pattern,
            "hit_count": 0,
            "file_set": set(),
            "role_counts": {},
            "newest_relevant_path": "",
            "newest_relevant_hit": "",
            "newest_mtime": -1.0,
        }
    hit_rows: list[dict[str, Any]] = []
    per_pattern: dict[str, int] = {name: 0 for name, _ in SWEEP_PATTERNS}
    hit_id = 0
    for path in files:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        rel = str(path.relative_to(ROOT))
        mtime = path.stat().st_mtime
        matched_patterns_in_file: set[str] = set()
        for line_no, line in enumerate(lines, start=1):
            low = line.lower()
            for name, pattern, pattern_low in lowered_patterns:
                if pattern_low not in low:
                    continue
                state = summary_state[name]
                state["hit_count"] += 1
                matched_patterns_in_file.add(name)
                role = classify_hit(line)
                role_counts = state["role_counts"]
                role_counts[role] = role_counts.get(role, 0) + 1
                if mtime > state["newest_mtime"]:
                    state["newest_mtime"] = mtime
                    state["newest_relevant_path"] = str(path)
                    state["newest_relevant_hit"] = f"L{line_no}:{compact_text(line, 220)}"
                if per_pattern[name] >= max_hits_per_pattern:
                    continue
                per_pattern[name] += 1
                hit_id += 1
                hit_rows.append(
                    {
                        "hit_id": f"HIT3270_{hit_id:04d}",
                        "pattern_id": name,
                        "pattern": pattern,
                        "source_path": str(path),
                        "relative_path": rel,
                        "line": line_no,
                        "hit_role": role,
                        "snippet": compact_text(line, 500),
                        "valid_for_claim": "false",
                    }
                )
        for name in matched_patterns_in_file:
            summary_state[name]["file_set"].add(str(path))
    summary_rows: list[dict[str, Any]] = []
    for name, _, _ in lowered_patterns:
        state = summary_state[name]
        roles = state["role_counts"]
        summary_rows.append(
            {
                "pattern_id": name,
                "pattern": state["pattern"],
                "hit_count": state["hit_count"],
                "file_count": len(state["file_set"]),
                "role_counts": ";".join(f"{key}={value}" for key, value in sorted(roles.items())),
                "newest_relevant_path": state["newest_relevant_path"],
                "newest_relevant_hit": state["newest_relevant_hit"],
                "sweep_scope": "all post-checkpoint-work md/csv except 3270 outputs, runs, venv, pycache",
                "valid_for_claim": "false",
            }
        )
    _SWEEP_SUMMARY_CACHE = summary_rows
    _SWEEP_HITS_CACHE = hit_rows
    return summary_rows, hit_rows


def corpus_sweep_hits(max_hits_per_pattern: int = 35) -> list[dict[str, Any]]:
    _, hit_rows = build_corpus_sweep(max_hits_per_pattern=max_hits_per_pattern)
    return hit_rows


def corpus_sweep_summary() -> list[dict[str, Any]]:
    summary_rows, _ = build_corpus_sweep()
    return summary_rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "NVT3270_0_chain_rule_zero",
            "claim_piece": "exact vertical silence criterion",
            "formal_statement": "If c_vis(Phi)=c_bar(q(Phi),theta_rep) and v is vertical with Dq[v]=0 and L_v theta_rep=0, then L_v c_vis=0.",
            "proof": "Apply the chain rule: L_v c_vis=(partial_q c_bar)Dq[v]+(partial_theta c_bar)L_v theta_rep=0.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_buys": "alpha, mass, binding, clock and source coefficients are zero only after the parent visible coefficient algebra is signed.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NVT3270_1_no_direct_vertex_equivalence",
            "claim_piece": "no direct visible constant vertex is an operator-domain statement",
            "formal_statement": "No alpha_EM(X), m_A(X), f(I_hid)F^2, w_A(X)S_A, clock_X or hidden-frame slot is equivalent to Coeff(O_vis) receiving only q-pullback or fixed representation data.",
            "proof": "Every direct vertex is a hidden-to-visible coefficient morphism; removing all such morphisms leaves only q-owned or fixed data, where NVT3270_0 applies.",
            "status": "EXACT_REDUCTION_TO_OPERATOR_DOMAIN",
            "what_it_buys": "This collapses many coupling debts into one beam: Hom(A_hid,Coeff_vis)=Const/0.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NVT3270_2_symmetry_no_go",
            "claim_piece": "covariance and gauge symmetry alone do not ban the vertices",
            "formal_statement": "If a nonconstant hidden scalar/invariant I_hid survives, then f(I_hid)F^2, m_A(I_hid) psi_bar psi, nu_i(I_hid), and w_A(I_hid)S_A are scalar/gauge-compatible counterterms unless parent typing forbids their target slot.",
            "proof": "Each term is an observed-frame scalar density and respects ordinary diffeomorphism/U(1) symmetry after I_hid is a scalar; its vertical derivative is generically f'(I_hid)L_v I_hid.",
            "status": "COUNTEREXAMPLE_THEOREM",
            "what_it_buys": "It rules out a fake proof route: metric/coframe descent plus covariance is not enough.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NVT3270_3_current_MTS_verdict",
            "claim_piece": "current no-direct-vertex promotion",
            "formal_statement": "The current corpus contains conditional chains and counterexample ledgers, but not a parent-signed hidden-visible hom ban or trivial invariant algebra theorem.",
            "proof": "1098, 1105, 1057, 1065, 1104 and 3269 all keep at least one direct-vertex or source-weight clause unsigned.",
            "status": "NOT_PROMOTED_RETAIN_FINITE_BRANCH",
            "what_it_buys": "The finite coupling runner is required; no local-GR/WEP/clock/R10/Maxwell claim is made from 3270.",
            "valid_for_claim": "false",
        },
    ]


def vertex_class_rows() -> list[dict[str, Any]]:
    return [
        {
            "vertex_id": "VTX3270_0_alpha_F2",
            "visible_slot": "EM kinetic / alpha_EM",
            "forbidden_or_owned_form": "forbid f(I_hid)F_Q^2, f_X(Xhat)F_Q^2, lambda_A F_Q^2 unless generated by a unique parent gauge norm",
            "coefficient_symbol": "b_alpha or C_e",
            "DD_mapping": "D_e=C_e receives alpha/EM drift contribution after sign convention is fixed",
            "current_status": "RETAINED_RESIDUAL_OPERATOR_DOMAIN_UNSIGNED",
            "proof_needed": "unique Maxwell subblock plus no independent F2 plus no hidden-visible hom plus radiative/readout closure",
            "valid_for_claim": "false",
        },
        {
            "vertex_id": "VTX3270_1_mass_spectrum",
            "visible_slot": "hatm, mass ratios, Yukawa/QCD/binding",
            "forbidden_or_owned_form": "forbid m_A(I_hid), y_A(I_hid), Lambda_QCD(I_hid), B_A(I_hid)",
            "coefficient_symbol": "b_hatm, b_mu, b_mA, b_nuc",
            "DD_mapping": "D_hatm=C_hatm-C_g receives common light-quark/nuclear response after material sensitivity ownership is fixed",
            "current_status": "RETAINED_RESIDUAL_MATTER_SPECTRUM_UNSIGNED",
            "proof_needed": "parent matter spectrum owner and binding response descent",
            "valid_for_claim": "false",
        },
        {
            "vertex_id": "VTX3270_2_source_weight",
            "visible_slot": "Hilbert/source coupling",
            "forbidden_or_owned_form": "forbid w_A(I_hid)S_A, kappa_A(I_hid)T_A, source-only material multipliers before variation",
            "coefficient_symbol": "Delta_w_AB or qbar_source",
            "DD_mapping": "not a DD C_parent coordinate; enters epsilon_k/source-normalization residual unless source functor kills it",
            "current_status": "RETAINED_SOURCE_COUNTERMODEL",
            "proof_needed": "no-source-only-slot grammar plus common action measure/current owner",
            "valid_for_claim": "false",
        },
        {
            "vertex_id": "VTX3270_3_hidden_frame",
            "visible_slot": "matter frame/readout metric",
            "forbidden_or_owned_form": "forbid A_A(I_hid)^2 g_obs, disformal B_A(I_hid), hidden Hodge/readout slots",
            "coefficient_symbol": "b_conf, b_dis, b_clock",
            "DD_mapping": "outside the two-channel DD basis; routes to PPN/clock/orbital residual vector",
            "current_status": "RETAINED_FRAME_READOUT_COUNTERMODEL",
            "proof_needed": "single observed coframe descent plus no-shadow frame and readout-before/after closure",
            "valid_for_claim": "false",
        },
        {
            "vertex_id": "VTX3270_4_marker_binding",
            "visible_slot": "material marker / binding response",
            "forbidden_or_owned_form": "forbid material_A(I_hid), preparation_A(I_hid), source mask or binding response after readout",
            "coefficient_symbol": "b_marker, c_surface, epsilon_k",
            "DD_mapping": "only maps into DD after material charge owner and source/test projection are parent-signed",
            "current_status": "RETAINED_MATERIAL_MARKER_COUNTERMODEL",
            "proof_needed": "matter category label-forgetting plus material response descent",
            "valid_for_claim": "false",
        },
    ]


def finite_schema_rows() -> list[dict[str, Any]]:
    return [
        {"field": "coefficient_id", "type": "string", "required": "true", "meaning": "stable coefficient row id", "valid_for_claim": "false"},
        {"field": "vertex_id", "type": "string", "required": "true", "meaning": "visible vertex class from P8_Y5_R2FR_3270_VISIBLE_VERTEX_CLASSIFICATION.csv", "valid_for_claim": "false"},
        {"field": "coefficient_symbol", "type": "string", "required": "true", "meaning": "local derivative or source-weight coefficient", "valid_for_claim": "false"},
        {"field": "maps_to_C_g", "type": "float_or_MISSING", "required": "if DD projected", "meaning": "contribution to C_g=L_X ln Lambda_3", "valid_for_claim": "false"},
        {"field": "maps_to_C_hatm", "type": "float_or_MISSING", "required": "if DD projected", "meaning": "contribution to C_hatm=L_X ln hatm", "valid_for_claim": "false"},
        {"field": "maps_to_C_e", "type": "float_or_MISSING", "required": "if DD projected", "meaning": "contribution to C_e=L_X ln alpha_EM", "valid_for_claim": "false"},
        {"field": "epsilon_MICROSCOPE", "type": "float_or_MISSING", "required": "if source/readout residual", "meaning": "absolute residual eta budget in MICROSCOPE row", "valid_for_claim": "false"},
        {"field": "epsilon_EOTWASH", "type": "float_or_MISSING", "required": "if source/readout residual", "meaning": "absolute residual eta budget in Eot-Wash row", "valid_for_claim": "false"},
        {"field": "source_path", "type": "path_or_MISSING", "required": "true for claim", "meaning": "parent theorem or coefficient source path", "valid_for_claim": "false"},
        {"field": "claim_status", "type": "enum", "required": "true", "meaning": "NONCLAIM unless parent theorem and numeric/source rows are real", "valid_for_claim": "false"},
    ]


def finite_coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient_id": "COEF3270_0_b_alpha",
            "vertex_id": "VTX3270_0_alpha_F2",
            "coefficient_symbol": "b_alpha_as_C_e",
            "maps_to_C_g": "0",
            "maps_to_C_hatm": "0",
            "maps_to_C_e": "MISSING_PARENT_VALUE",
            "epsilon_MICROSCOPE": "0",
            "epsilon_EOTWASH": "0",
            "source_path": str(SRC_F2_1057),
            "current_status": "MISSING_PARENT_COEFFICIENT_OR_ZERO_THEOREM",
            "claim_status": "NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "COEF3270_1_b_hatm",
            "vertex_id": "VTX3270_1_mass_spectrum",
            "coefficient_symbol": "b_hatm_as_C_hatm_minus_C_g",
            "maps_to_C_g": "0",
            "maps_to_C_hatm": "MISSING_PARENT_VALUE",
            "maps_to_C_e": "0",
            "epsilon_MICROSCOPE": "0",
            "epsilon_EOTWASH": "0",
            "source_path": str(SRC_FV_1098),
            "current_status": "MISSING_MATTER_SPECTRUM_OWNER_OR_COEFFICIENT",
            "claim_status": "NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "COEF3270_2_source_weight",
            "vertex_id": "VTX3270_2_source_weight",
            "coefficient_symbol": "Delta_w_AB_times_tau_k",
            "maps_to_C_g": "NOT_A_DD_C_COORDINATE",
            "maps_to_C_hatm": "NOT_A_DD_C_COORDINATE",
            "maps_to_C_e": "NOT_A_DD_C_COORDINATE",
            "epsilon_MICROSCOPE": "MISSING_SOURCE_WEIGHT_PRODUCT",
            "epsilon_EOTWASH": "MISSING_SOURCE_WEIGHT_PRODUCT",
            "source_path": str(SRC_GRAMMAR_1065),
            "current_status": "SOURCE_ONLY_SLOT_UNSIGNED",
            "claim_status": "NONCLAIM_REFUSE_TO_HIDE_IN_C_PARENT",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "COEF3270_3_hidden_frame",
            "vertex_id": "VTX3270_3_hidden_frame",
            "coefficient_symbol": "b_conf_b_dis",
            "maps_to_C_g": "OUTSIDE_DD_BASIS",
            "maps_to_C_hatm": "OUTSIDE_DD_BASIS",
            "maps_to_C_e": "OUTSIDE_DD_BASIS",
            "epsilon_MICROSCOPE": "MISSING_PPN_CLOCK_PROJECTION",
            "epsilon_EOTWASH": "MISSING_PPN_CLOCK_PROJECTION",
            "source_path": str(SRC_SIG_1104),
            "current_status": "FRAME_READOUT_RESIDUAL_RETAINED",
            "claim_status": "NONCLAIM_ROUTE_TO_PPN_CLOCK_VECTOR",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "COEF3270_4_marker_binding",
            "vertex_id": "VTX3270_4_marker_binding",
            "coefficient_symbol": "b_marker_or_c_surface",
            "maps_to_C_g": "0",
            "maps_to_C_hatm": "MISSING_MATERIAL_RESPONSE_MAP",
            "maps_to_C_e": "MISSING_MATERIAL_RESPONSE_MAP",
            "epsilon_MICROSCOPE": "MISSING_MATERIAL_PROJECTION",
            "epsilon_EOTWASH": "MISSING_MATERIAL_PROJECTION",
            "source_path": str(SRC_SUB_1105),
            "current_status": "MATERIAL_RESPONSE_OWNER_UNSIGNED",
            "claim_status": "NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def delta_rows() -> list[dict[str, str]]:
    rows = read_csv(SRC_3265_DELTA)
    if len(rows) < 2:
        raise ValueError("expected two DD matrix rows")
    return rows


def candidate_input_rows() -> list[dict[str, Any]]:
    micro_bound = float(delta_rows()[0]["eta_abs_bound"])
    return [
        {
            "case_id": "VCASE3270_0_no_vertex_zero",
            "description": "signed no-direct-vertex branch smoke: all DD visible coefficients and source residuals zero",
            "C_g": "0",
            "C_hatm": "0",
            "C_e": "0",
            "epsilon_MICROSCOPE": "0",
            "epsilon_EOTWASH": "0",
            "dd_projection_status": "DD_PROJECTED",
            "input_status": "CONDITIONAL_ZERO_SMOKE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "case_id": "VCASE3270_1_tiny_alpha_vertex",
            "description": "small hidden EM vertex smoke with C_e=b_alpha=1e-13",
            "C_g": "0",
            "C_hatm": "0",
            "C_e": "1e-13",
            "epsilon_MICROSCOPE": "0",
            "epsilon_EOTWASH": "0",
            "dd_projection_status": "DD_PROJECTED",
            "input_status": "NUMERIC_SMOKE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "case_id": "VCASE3270_2_tiny_mass_vertex",
            "description": "small hidden mass-spectrum vertex smoke with C_hatm-C_g=1e-13",
            "C_g": "0",
            "C_hatm": "1e-13",
            "C_e": "0",
            "epsilon_MICROSCOPE": "0",
            "epsilon_EOTWASH": "0",
            "dd_projection_status": "DD_PROJECTED",
            "input_status": "NUMERIC_SMOKE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "case_id": "VCASE3270_3_large_alpha_vertex_fail",
            "description": "large hidden EM vertex smoke proving the runner catches an over-bound alpha leak",
            "C_g": "0",
            "C_hatm": "0",
            "C_e": "1e-9",
            "epsilon_MICROSCOPE": "0",
            "epsilon_EOTWASH": "0",
            "dd_projection_status": "DD_PROJECTED",
            "input_status": "FAILURE_SMOKE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "case_id": "VCASE3270_4_source_weight_epsilon",
            "description": "source-only weight is not hidden in C_parent; it is an explicit epsilon residual",
            "C_g": "0",
            "C_hatm": "0",
            "C_e": "0",
            "epsilon_MICROSCOPE": fmt(1.1 * micro_bound),
            "epsilon_EOTWASH": "0",
            "dd_projection_status": "DD_PROJECTED_WITH_EXPLICIT_EPSILON",
            "input_status": "SOURCE_WEIGHT_EPSILON_SMOKE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "case_id": "VCASE3270_5_hidden_frame_refusal",
            "description": "hidden conformal/disformal frame is outside the two-channel DD basis and must route to PPN/clock vector",
            "C_g": "0",
            "C_hatm": "0",
            "C_e": "0",
            "epsilon_MICROSCOPE": "0",
            "epsilon_EOTWASH": "0",
            "dd_projection_status": "REFUSE_OUTSIDE_DD_BASIS",
            "input_status": "REFUSAL_CASE_FRAME_NOT_DD",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    deltas = delta_rows()
    rows: list[dict[str, Any]] = []
    for case in candidate_input_rows():
        cg = float(case["C_g"])
        chatm = float(case["C_hatm"])
        ce = float(case["C_e"])
        eps_micro = float(case["epsilon_MICROSCOPE"])
        eps_eot = float(case["epsilon_EOTWASH"])
        d_hatm = chatm - cg
        d_e = ce
        predictions: dict[str, tuple[float, float, float, str]] = {}
        for delta_row in deltas:
            arena = delta_row["arena"]
            label = "MICROSCOPE" if "MICROSCOPE" in arena else "EOTWASH"
            eps = eps_micro if label == "MICROSCOPE" else eps_eot
            dqhat = float(delta_row["Delta_Qhatm_prime"])
            dqe = float(delta_row["Delta_Qe_prime"])
            bound = float(delta_row["eta_abs_bound"])
            eta_core = dqhat * d_hatm + dqe * d_e
            eta_abs_plus_eps = abs(eta_core) + eps
            status = "pass_bound" if eta_abs_plus_eps <= bound else "fail_bound"
            predictions[label] = (eta_core, eta_abs_plus_eps, bound, status)
        row_projectable = case["dd_projection_status"] != "REFUSE_OUTSIDE_DD_BASIS"
        passes_numeric_bounds = row_projectable and all(item[3] == "pass_bound" for item in predictions.values())
        if not row_projectable:
            claim_status = "REFUSE_OR_FAIL"
        elif passes_numeric_bounds and case["input_status"].startswith("CONDITIONAL_ZERO"):
            claim_status = "CONDITIONAL_ZERO_NONCLAIM"
        elif passes_numeric_bounds:
            claim_status = "PASSES_NUMERIC_SMOKE_NONCLAIM"
        else:
            claim_status = "FAILS_NUMERIC_SMOKE"
        rows.append(
            {
                "case_id": case["case_id"],
                "input_status": case["input_status"],
                "dd_projection_status": case["dd_projection_status"],
                "D_hatm": fmt(d_hatm),
                "D_e": fmt(d_e),
                "eta_MICROSCOPE_core": fmt(predictions["MICROSCOPE"][0]),
                "eta_MICROSCOPE_abs_plus_epsilon": fmt(predictions["MICROSCOPE"][1]),
                "eta_MICROSCOPE_bound": fmt(predictions["MICROSCOPE"][2]),
                "eta_MICROSCOPE_status": predictions["MICROSCOPE"][3],
                "eta_EOTWASH_core": fmt(predictions["EOTWASH"][0]),
                "eta_EOTWASH_abs_plus_epsilon": fmt(predictions["EOTWASH"][1]),
                "eta_EOTWASH_bound": fmt(predictions["EOTWASH"][2]),
                "eta_EOTWASH_status": predictions["EOTWASH"][3],
                "row_projectable": bool_str(row_projectable),
                "passes_numeric_bounds": bool_str(passes_numeric_bounds),
                "claim_status": claim_status,
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_gate_rows() -> list[dict[str, Any]]:
    runners = {row["case_id"]: row for row in runner_rows()}
    sweep = corpus_sweep_summary()
    direct_hits = sum(int(row["hit_count"]) for row in sweep if row["pattern_id"] in {"alpha_EM_X", "mass_X", "fX_F2", "source_only", "wA_X", "hidden_visible_hom"})
    return [
        {
            "gate_id": "VG3270_0_chain_rule_theorem",
            "gate": "visible coefficients vanish if q-pullback/fixed-representation typing is signed",
            "passed": "true",
            "reason": "NVT3270_0 is an exact chain-rule theorem",
            "claim_allowed": "false",
        },
        {
            "gate_id": "VG3270_1_no_direct_vertex_parent_signed",
            "gate": "no direct alpha/mass/source/clock/frame vertex is parent-signed in current MTS",
            "passed": "false",
            "reason": "1098/1105/1057/1065/1104 keep operator-domain, no-F2, no-source-only and readout closure unsigned",
            "claim_allowed": "false",
        },
        {
            "gate_id": "VG3270_2_sweep_not_one_look",
            "gate": "corpus sweep covered repeated direct-vertex mentions rather than a one-file vibe check",
            "passed": bool_str(direct_hits > 20),
            "reason": f"direct_vertex_related_hits={direct_hits}",
            "claim_allowed": "false",
        },
        {
            "gate_id": "VG3270_3_large_alpha_caught",
            "gate": "runner catches over-bound alpha/EM coefficient leaks",
            "passed": bool_str(runners["VCASE3270_3_large_alpha_vertex_fail"]["passes_numeric_bounds"] == "false"),
            "reason": runners["VCASE3270_3_large_alpha_vertex_fail"]["claim_status"],
            "claim_allowed": "false",
        },
        {
            "gate_id": "VG3270_4_source_weight_not_hidden_in_C",
            "gate": "source-only weights are explicit epsilon/source residuals, not silently absorbed into C_parent",
            "passed": bool_str(runners["VCASE3270_4_source_weight_epsilon"]["passes_numeric_bounds"] == "false"),
            "reason": "source-weight smoke exceeds MICROSCOPE epsilon budget and remains a separate residual branch",
            "claim_allowed": "false",
        },
        {
            "gate_id": "VG3270_5_hidden_frame_refused",
            "gate": "hidden frame/disformal case is refused by DD runner instead of mislabeled as alpha/mass",
            "passed": bool_str(runners["VCASE3270_5_hidden_frame_refusal"]["row_projectable"] == "false"),
            "reason": runners["VCASE3270_5_hidden_frame_refusal"]["dd_projection_status"],
            "claim_allowed": "false",
        },
        {
            "gate_id": "VG3270_6_local_GR",
            "gate": "local GR/Newton/Maxwell/PPN promotion",
            "passed": "false",
            "reason": "3270 attacks visible coupling leakage only; EH/source/Bianchi/PPN/readout gates remain separate",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3270_0_real_progress",
            "verdict": "NO_DIRECT_VERTEX_REDUCED_TO_ONE_OPERATOR_DOMAIN_BEAM",
            "what_moved": "3270 proves the exact chain-rule zero route, proves covariance/gauge symmetry cannot ban hidden-visible coefficient maps, sweeps the corpus, and routes visible vertices into a DD/residual runner.",
            "best_next": "derive the typed visible coefficient algebra Hom(A_hid,Coeff_vis)=Const/0 from the quotient/category object language, not from covariance alone",
            "fallback_next": "fill source-backed b_alpha, b_hatm/b_nuc, Delta_w_AB, b_frame/b_dis, and clock/readout coefficient rows",
            "claim_status": "NO_LOCAL_GR_OR_WEP_PROMOTION",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3270_1_physics_read",
            "verdict": "THE_COUPLING_IS_THE_THROAT",
            "what_moved": "If this beam closes, the alpha/mass/source-weight debts collapse together; if it does not, MTS remains testable but becomes a finite-coupling model rather than a derived local-GR branch.",
            "best_next": "try the no-hidden-visible-hom typing proof before spending effort on many coefficient priors",
            "fallback_next": "prioritize alpha/EM and source-weight rows because they hit WEP, clocks, R10 and Newtonian source calibration simultaneously",
            "claim_status": "PRIVATE_DISCIPLINE_TOOL",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3270_0_3271",
            "selected": "primary",
            "target_doc": "3271-Y5-R2FR-hidden-visible-hom-typing-proof-or-coupling-coefficient-bound-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3271_hidden_visible_hom_typing_proof_or_coupling_coefficient_bound_pack.py",
            "objective": "Try to derive Hom(A_hid,Coeff_vis)=Const/0 from the parent quotient/category typing: visible coefficients must be q-pullbacks or fixed representation data. If this fails, emit source-ready coefficient rows for b_alpha, b_hatm, Delta_w_AB, b_frame/b_dis, and clock/readout projections.",
            "guardrail": "Do not claim no-direct-vertex from covariance, gauge invariance, or absence of examples; one hidden scalar coefficient map is a live countermodel.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def output_csvs_parse() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not csv_parse_ok(path):
            return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    sources = source_register()
    runners = runner_rows()
    gates = promotion_gate_rows()
    finite_rows = finite_coefficient_rows()
    validations = [
        {
            "check_id": "VAL3270_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3270_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3270_2_outputs_parse",
            "check": "all 3270 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3270_3_sweep_has_hits",
            "check": "corpus sweep found direct-vertex/coupling evidence across multiple files",
            "passed": bool_str(sum(int(row["hit_count"]) for row in corpus_sweep_summary()) > 50),
            "detail": f"patterns={len(SWEEP_PATTERNS)};files={len(corpus_files())}",
        },
        {
            "check_id": "VAL3270_4_no_valid_claim_rows",
            "check": "finite coefficient rows remain nonclaim",
            "passed": bool_str(all(row["valid_for_claim"] == "false" and "NONCLAIM" in row["claim_status"] for row in finite_rows)),
            "detail": "all finite rows carry missing theorem/value/source status",
        },
        {
            "check_id": "VAL3270_5_zero_case_passes",
            "check": "zero no-direct-vertex smoke predicts zero/passing eta in both DD arenas",
            "passed": bool_str(next(row for row in runners if row["case_id"] == "VCASE3270_0_no_vertex_zero")["passes_numeric_bounds"] == "true"),
            "detail": next(row for row in runners if row["case_id"] == "VCASE3270_0_no_vertex_zero")["claim_status"],
        },
        {
            "check_id": "VAL3270_6_large_alpha_fails",
            "check": "large alpha leak fails the DD smoke bound",
            "passed": bool_str(next(row for row in runners if row["case_id"] == "VCASE3270_3_large_alpha_vertex_fail")["passes_numeric_bounds"] == "false"),
            "detail": next(row for row in runners if row["case_id"] == "VCASE3270_3_large_alpha_vertex_fail")["claim_status"],
        },
        {
            "check_id": "VAL3270_7_hidden_frame_refused",
            "check": "hidden frame/disformal candidate is refused outside DD basis",
            "passed": bool_str(next(row for row in runners if row["case_id"] == "VCASE3270_5_hidden_frame_refusal")["row_projectable"] == "false"),
            "detail": next(row for row in runners if row["case_id"] == "VCASE3270_5_hidden_frame_refusal")["dd_projection_status"],
        },
        {
            "check_id": "VAL3270_8_claim_gates_false",
            "check": "no 3270 promotion gate allows a WEP/local-GR claim",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in gates)),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3270_9_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3270_10_overall",
            "check": "3270 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3270_10_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        vals = [str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    sources = read_csv(OUTPUTS["sources"])
    sweep_summary = read_csv(OUTPUTS["sweep_summary"])
    theorem = read_csv(OUTPUTS["theorem"])
    vertex_classes = read_csv(OUTPUTS["vertex_classes"])
    finite_rows = read_csv(OUTPUTS["finite_rows"])
    runners = read_csv(OUTPUTS["runner"])
    gates = read_csv(OUTPUTS["promotion"])
    decisions = read_csv(OUTPUTS["decision"])
    next_targets = read_csv(OUTPUTS["next"])
    validations = read_csv(OUTPUTS["validation"])
    content = f"""# 3270 - No direct visible constant vertex or finite coefficient fill under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3270` makes the coupling bottleneck sharper: visible coefficients vanish by chain rule only if they are `q`-pullbacks or fixed representation data.
- It also proves the warning theorem: ordinary covariance/gauge symmetry alone does **not** ban `f(I_hid)F^2`, `m_A(I_hid)`, `w_A(I_hid)S_A`, clock/readout, or hidden-frame coefficient maps.
- The live missing beam is now precise: `Hom(A_hid,Coeff_vis)=Const/0`, or equivalently a parent-typed visible coefficient algebra.
- The fallback is executable: alpha/mass DD leaks run through the two-arena matrix, while source-only and hidden-frame terms are refused as hidden `C_parent` shortcuts and kept as residual branches.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## Corpus Sweep Summary
{md_table(sweep_summary, ["pattern_id", "pattern", "hit_count", "file_count", "role_counts", "newest_relevant_path", "valid_for_claim"])}

## No-Direct-Vertex Theorem / No-Go
{md_table(theorem, ["theorem_id", "claim_piece", "formal_statement", "proof", "status", "what_it_buys", "valid_for_claim"])}

## Visible Vertex Classes
{md_table(vertex_classes, ["vertex_id", "visible_slot", "forbidden_or_owned_form", "coefficient_symbol", "DD_mapping", "current_status", "proof_needed", "valid_for_claim"])}

## Finite Coefficient Rows
{md_table(finite_rows, ["coefficient_id", "vertex_id", "coefficient_symbol", "maps_to_C_g", "maps_to_C_hatm", "maps_to_C_e", "epsilon_MICROSCOPE", "epsilon_EOTWASH", "current_status", "claim_status", "valid_for_claim"])}

## DD / Residual Runner
{md_table(runners, ["case_id", "input_status", "dd_projection_status", "D_hatm", "D_e", "eta_MICROSCOPE_abs_plus_epsilon", "eta_MICROSCOPE_bound", "eta_EOTWASH_abs_plus_epsilon", "eta_EOTWASH_bound", "row_projectable", "passes_numeric_bounds", "claim_status", "valid_for_claim"])}

## Promotion Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "best_next", "fallback_next", "claim_status", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    rows_by_key = {
        "sources": source_register(),
        "sweep_summary": corpus_sweep_summary(),
        "sweep_hits": corpus_sweep_hits(),
        "theorem": theorem_rows(),
        "vertex_classes": vertex_class_rows(),
        "finite_schema": finite_schema_rows(),
        "finite_rows": finite_coefficient_rows(),
        "candidate_inputs": candidate_input_rows(),
        "runner": runner_rows(),
        "promotion": promotion_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
