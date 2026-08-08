from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4271"
CLAIM_ID = "L-112"
BRANCH = "MTS_R2FR_Y5_CORE_COFRAME_SHADOW_ZERO_OR_FIRST_SOURCE_BACKED_EPSILON_ROW_4271"
DECISION = "CORE_COFRAME_SHADOW_ACTION_DOMAIN_THEOREM_DERIVED_CURRENT_ZERO_UNSIGNED_FRAME_COMPONENT_BOUND_FORK_READY_NONCLAIM"
MARKER = "PPC4161_CORE_COFRAME_SHADOW_ZERO_OR_FIRST_SOURCE_BACKED_EPSILON_ROW_4271"
PACKET_MARKER = "PPC4161_PACKET_CORE_COFRAME_SHADOW_ZERO_OR_FIRST_SOURCE_BACKED_EPSILON_ROW_4271"
NEXT_TARGET = "4272-Y5-R2FR-parent-no-extra-frame-signature-or-cg-bdis-first-bound-runner.md"

FORMAL_PATH = FORMAL / "287-PPC4161-core-coframe-shadow-zero-or-first-source-backed-epsilon-row.md"
DOC_PATH = POST / "4271-Y5-R2FR-core-coframe-shadow-zero-or-first-source-backed-epsilon-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4271_VALIDATION.csv"

LIVE_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4254_DQ_COMPONENT_VALUES_CANDIDATE.csv"
LOCAL_COMPONENT_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4271_DQ_COMPONENT_VALUES_CANDIDATE.csv"
CORE_CANDIDATE_PATH = SOURCE_DIR / "P8_Y5_R2FR_4271_DQ_GEOM_CORE_FRAME_CANDIDATE.csv"
BOUND_GEOM_4272_PATH = SOURCE_DIR / "P8_Y5_R2FR_4272_DQ_GEOM_BOUND_RUNNER_CANDIDATE.csv"
FORMAL_4272_PATH = FORMAL / "288-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-first-bound-runner.md"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
PROBE_ORDER = (
    "Dq_geom",
    "Dq_tau",
    "Dq_matter",
    "Dq_source_readout",
    "Dq_theta_marker",
    "Dq_boundary_projector",
    "Dq_EM",
    "Dq_coeff",
)


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4271_00_4270_formal_core": SourceSpec(
        "SRC4271_00_4270_formal_core",
        FORMAL / "286-PPC4161-Dq-geom-core-coframe-shadow-or-reduced-epsilon-bound.md",
        "MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW",
        "4270 reduced Dq_geom to the core observed-readout/coframe-shadow residual.",
    ),
    "SRC4271_01_3860_basicness": SourceSpec(
        "SRC4271_01_3860_basicness",
        SOURCE_DIR / "P8_Y5_R2FR_3860_COFRAME_BASICNESS_THEOREM.csv",
        "EXACT_CONDITIONAL_COFRAME_BASICNESS",
        "Exact q-basic coframe chain-rule theorem.",
    ),
    "SRC4271_02_3861_no_shadow": SourceSpec(
        "SRC4271_02_3861_no_shadow",
        SOURCE_DIR / "P8_Y5_R2FR_3861_NO_SHADOW_COFRAME_THEOREM.csv",
        "FINITE_SHADOW_IS_SOURCE_COUPLING",
        "Finite shadow frame variation is a real source coupling, not notation.",
    ),
    "SRC4271_03_same_coframe_clause": SourceSpec(
        "SRC4271_03_same_coframe_clause",
        SOURCE_DIR / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "UOC519_5_no_conformal_disformal_shadow_frame",
        "Same observed coframe/no conformal-disformal shadow clause.",
    ),
    "SRC4271_04_single_frame_gate": SourceSpec(
        "SRC4271_04_single_frame_gate",
        SOURCE_DIR / "P8_Y5_R2FR_2959_SINGLE_OBSERVED_FRAME_PARENT_ACTION_GATE.csv",
        "SFRAME2959_0_target_clause",
        "Single observed frame parent action gate.",
    ),
    "SRC4271_05_closure_warning": SourceSpec(
        "SRC4271_05_closure_warning",
        SOURCE_DIR / "P8_Y5_R2FR_2960_SINGLE_FRAME_CLOSURE_DECLARATION_NONCLAIM.csv",
        "CLOSE2960_0_statement",
        "Closure branch exists but has no theorem-zero credit.",
    ),
    "SRC4271_06_no_marker_theorem": SourceSpec(
        "SRC4271_06_no_marker_theorem",
        SOURCE_DIR / "P8_Y5_R2FR_3370_NO_SHADOW_NO_MARKER_THEOREM.csv",
        "NSM3370_0_matter_functor_domain",
        "No-shadow/no-marker conditional action-domain theorem.",
    ),
    "SRC4271_07_shadow_source_formula": SourceSpec(
        "SRC4271_07_shadow_source_formula",
        SOURCE_DIR / "P8_Y5_R2FR_3647_NO_SHADOW_THEOREM_ATTEMPT.csv",
        "NSF3647_3_trace_source",
        "Trace-source formula for finite conformal shadow frame.",
    ),
    "SRC4271_08_shadow_coefficients": SourceSpec(
        "SRC4271_08_shadow_coefficients",
        SOURCE_DIR / "P8_Y5_R2FR_3769_SHADOW_FRAME_RESIDUAL_COEFFICIENTS.csv",
        "SFC3769_0_h_matter",
        "Sector shadow-frame coefficient vector.",
    ),
    "SRC4271_09_shadow_budget": SourceSpec(
        "SRC4271_09_shadow_budget",
        SOURCE_DIR / "P8_Y5_R2FR_3769_SHADOW_FRAME_BOUND_BUDGET.csv",
        "SBB3769_1_gamma_shadow",
        "Existing PPN/clock/orbit frame-bound budget rows.",
    ),
    "SRC4271_10_cg_ppn_projection": SourceSpec(
        "SRC4271_10_cg_ppn_projection",
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2104_CG_PPN_PROJECTION.csv",
        "PRJ2104_4_Cassini_projection_bound",
        "Source-backed diagnostic PPN gamma projection for conformal frame coupling.",
    ),
    "SRC4271_11_private_selector": SourceSpec(
        "SRC4271_11_private_selector",
        SOURCE_DIR / "P8_Y5_R2FR_4234_SIX_CLAUSE_EH_COFRAME_GATE.csv",
        "KC4234_0_same_coframe",
        "Private selector has same-coframe truth but public parent truth remains false.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = list(rows[0].keys())
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def dq_geom_4272_bound_row() -> Dict[str, str]:
    for row in csv_rows(BOUND_GEOM_4272_PATH):
        if (
            row.get("probe_id") == "Dq_geom"
            and row.get("new_epsilon") == "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
        ):
            return row
    return {}


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if CLAIM_ID in text:
        return
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = next(csv.reader(handle))
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": (
            "4271 derives the exact action-domain fork for the remaining Dq_geom core: if ordinary matter, EM, clocks, rods, source charge and readouts use "
            "only one quotient-owned observed coframe and no independent Weyl/disformal/source-frame slots, the core coframe-shadow variation is absent by "
            "variable-domain plus q-chain-rule reasoning. If those slots are allowed, their conformal/disformal derivatives couple to matter trace and "
            "preferred-frame channels and must be bounded as c_g/b_dis/shadow-frame residuals. The current corpus has the theorem route but not the public "
            "parent signature, so the live Dq_geom row remains nonnumeric and nonclaim."
        ),
        "current_evidence": (
            "4271 source register, action-domain theorem rows, core residual decomposition, frame-component bridge, diagnostic PPN bound row, "
            "updated Dq_geom candidate, decision and firewall."
        ),
        "status": "private_core_coframe_shadow_action_domain_theorem_derived_current_zero_unsigned_nonclaim",
        "next_test": "Either parent-sign the no-extra-frame action-domain clause, or run a first finite c_g/b_dis frame-component bound with sourced projection coefficients.",
        "key_risk": "Treating a private same-frame selector or closure declaration as a public derivation of local GR.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "CST4271_0_core_model",
            "sector frame split",
            "For each ordinary sector, write g_s=A_s(Phi)^2 g_obs+B_s(Phi) U_mu U_nu+h_s^perp modulo Lorentz/diffeomorphism/q-gauge.",
            "DEFINITION",
            "A_s, B_s and h_s^perp are physical only when they are independent parent/readout arguments rather than q-owned notation.",
        ),
        (
            "CST4271_1_vertical_variation",
            "finite shadow source formula",
            "D_v S_s=(1/2) int sqrt(-g_s) T_s^{mu nu} D_v g^s_{mu nu}; with D_v g_s=2 c_s g_obs+b_s U_mu U_nu+D_v h_s^perp, finite c_s hits T_s and finite b_s hits T_s^{mu nu}U_mu U_nu.",
            "DERIVED_SOURCE_FORMULA",
            "This proves a shadow frame is observable unless removed by the parent action domain or bounded.",
        ),
        (
            "CST4271_2_no_extra_frame_zero",
            "action-domain zero",
            "If S_s and readouts depend on parent fields only through e_obs(q), omega[e_obs], fixed/q-basic theta and q-sector fields, with no independent A_s, B_s, h_s^perp or source-frame slot, then c_s=b_s=D_v h_s^perp=0 for v in ker(Dq).",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            "The zero follows from variable absence plus D(e_bar(q))[v]=D e_bar[Dq(v)]=0.",
        ),
        (
            "CST4271_3_closure_not_derivation",
            "private selector limit",
            "4234/2960 allow a private same-frame closure branch, but public_parent_truth=false means it cannot be used as a derived local-GR claim.",
            "PRIVATE_SELECTOR_ONLY",
            "The live main branch must keep a finite/nonclaim residual until the parent action signs the clause.",
        ),
        (
            "CST4271_4_core_bound",
            "core residual bound",
            "epsilon_core_geom <= C_cg sum_s|c_s| + C_dis sum_s|b_dis_s| + C_shadow sum_s||h_s^perp|| + C_readout epsilon_readout_frame + C_terminal epsilon_terminal.",
            "DERIVED_ABSOLUTE_BOUND_FORK",
            "No cancellation between conformal, disformal, sector-shadow, readout and terminal-coframe tails is allowed.",
        ),
        (
            "CST4271_5_current_verdict",
            "current corpus status",
            "The theorem is exact, but the parent no-extra-frame/action-domain certificate is unsigned; finite c_g/b_dis/shadow-frame rows remain live.",
            "CURRENT_ZERO_UNSIGNED_BOUND_FORK_ACTIVE",
            "Do not promote Dq_geom=0 yet.",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "name": name,
            "statement": statement,
            "status": status,
            "guard": guard,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, name, statement, status, guard in raw
    ]


def residual_decomposition_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "CRD4271_0_cg",
            "c_g",
            "common conformal/Weyl frame derivative D_v ln A_g",
            "matter trace T and source-normalization/PPN gamma channels",
            "zero if A_g is absent or q-owned; otherwise finite component",
            "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv and 2104 projection",
        ),
        (
            "CRD4271_1_bdis",
            "b_dis",
            "representative disformal derivative D_v B_g",
            "preferred-frame, clocks, light cones, orbital/PPN channels",
            "zero if B_g is absent or q-owned; otherwise finite component",
            "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
        ),
        (
            "CRD4271_2_sector_shadow",
            "epsilon_shadow_matter/light/clock/EM/source",
            "non-gauge sector metric/coframe shadow norm",
            "WEP, PPN, clock, EM stress, Newtonian GM/source calibration",
            "zero only under same public coframe for all sectors",
            "P8_Y5_R2FR_3769_SHADOW_FRAME_RESIDUAL_COEFFICIENTS.csv",
        ),
        (
            "CRD4271_3_readout_terminal",
            "epsilon_readout_frame + epsilon_terminal",
            "readout or terminal public coframe selected after variation or with hidden endpoint slot",
            "clock/source/orbit/readout mismatch and endpoint leakage",
            "zero only if readout is fixed q-basic before variation",
            "3860/3861 and 2887/2888 audits",
        ),
        (
            "CRD4271_4_reduced_core",
            "epsilon_core_geom",
            "C_cg|c_g|+C_dis|b_dis|+C_shadow epsilon_shadow+C_readout epsilon_readout+C_terminal epsilon_terminal",
            "the live nonclaim Dq_geom core",
            "needs parent zero or sourced finite coefficients",
            "4271 live candidate",
        ),
    ]
    return [
        {
            **common(),
            "decomposition_id": decomposition_id,
            "component": component,
            "definition": definition,
            "observable_link": observable_link,
            "zero_or_bound_rule": zero_or_bound_rule,
            "source_or_next_gate": source_or_next_gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for decomposition_id, component, definition, observable_link, zero_or_bound_rule, source_or_next_gate in raw
    ]


def frame_bridge_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "FBR4271_0_parent_zero_route",
            "parent_no_extra_frame_signature",
            "If the parent action grammar excludes A_g, B_dis, h_s^perp and source-frame slots for ordinary sectors, Dq_geom core zero follows.",
            "MISSING_PUBLIC_PARENT_SIGNATURE",
            "not_scoreable",
        ),
        (
            "FBR4271_1_private_selector_route",
            "same_frame_private_selector",
            "4234 has private_selector_truth=true for same coframe, EH block, vertical silence, boundary routing and kappa source coupling.",
            "PRIVATE_CLOSURE_DEBT_TRUE",
            "allowed only as labelled private branch, not as derivation evidence",
        ),
        (
            "FBR4271_2_finite_bound_route",
            "c_g_bdis_shadow_vector",
            "If parent zero is unsigned, score the absolute vector of c_g, b_dis, sector shadows, readout and terminal tails.",
            "MISSING_COMPONENT_VALUES_AND_PROJECTIONS",
            "4272 runner target",
        ),
        (
            "FBR4271_3_ppn_anchor",
            "Cassini_gamma_diagnostic",
            "Existing 2104 row gives alpha_eff<=0.00578792 only if Y_gamma=1 and every non-cg tail is theorem-zero.",
            "SOURCE_BACKED_DIAGNOSTIC_NOT_MTS_SCORE",
            "do not compare raw c_g without N_X and range/profile response",
        ),
    ]
    return [
        {
            **common(),
            "bridge_id": bridge_id,
            "route": route,
            "statement": statement,
            "status": status,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bridge_id, route, statement, status, next_action in raw
    ]


def diagnostic_bound_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "bound_id": "DBG4271_0_Cassini_alpha_eff_diagnostic",
            "quantity": "alpha_eff",
            "formula": "|Delta_gamma|<=6.7e-05 and Delta_gamma=-2 alpha_eff^2 with Y_gamma=1 gives alpha_eff<=sqrt(3.35e-05)",
            "numeric_value": "0.00578792",
            "units": "dimensionless",
            "source_path": str(SOURCE_DIR / "P8_Y5_PARENT_QLOC_2104_CG_PPN_PROJECTION.csv"),
            "source_row": "PRJ2104_4_Cassini_projection_bound",
            "why_not_claim": "N_X, Y_gamma, source profile, range response and non-cg tails are not MTS-derived or zeroed.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def core_candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "candidate_id": "DQ_GEOM_CORE_FRAME_COUPLING_4271",
            "probe_id": "Dq_geom",
            "old_epsilon": "MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW",
            "new_epsilon": "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND",
            "new_epsilon_C1": "MISSING_C1_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND",
            "source_path": str(FORMAL_PATH),
            "status": "ACTION_DOMAIN_THEOREM_DERIVED_PARENT_ZERO_UNSIGNED_FINITE_BOUND_FORK",
            "conditions_to_zero": (
                "public parent action excludes independent Weyl/disformal/source-frame/sector-shadow slots; all ordinary sectors use e_obs(q), "
                "omega[e_obs], fixed/q-basic constants and fixed readouts before variation"
            ),
            "finite_bound_route": "c_g;b_dis;epsilon_shadow_sector;epsilon_readout_frame;epsilon_terminal with absolute no-cancellation envelope",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def component_candidate_rows() -> List[Dict[str, str]]:
    previous = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    bound_geom_4272 = dq_geom_4272_bound_row()
    if not previous:
        previous = [
            {
                **common(),
                "candidate_id": "DQ_COORDINATE_SEMINORM_SMOKE_4255",
                "probe_id": probe,
                "weight": "1.0",
                "epsilon": f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                "epsilon_C1": f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                "source_path": str(FORMAL_PATH),
                "valid_for_claim": "False",
            }
            for probe in PROBE_ORDER
        ]
    output: List[Dict[str, str]] = []
    seen = set()
    for row in previous:
        probe = row.get("probe_id", "")
        if not probe:
            continue
        updated = dict(row)
        updated.update(common())
        if probe == "Dq_geom":
            updated["epsilon"] = "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND"
            updated["epsilon_C1"] = "MISSING_C1_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND"
            updated["source_path"] = str(FORMAL_PATH)
            updated["valid_for_claim"] = "False"
        output.append(updated)
        seen.add(probe)
    for probe in PROBE_ORDER:
        if probe not in seen:
            output.append(
                {
                    **common(),
                    "candidate_id": "DQ_COORDINATE_SEMINORM_SMOKE_4255",
                    "probe_id": probe,
                    "weight": "1.0",
                    "epsilon": "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND"
                    if probe == "Dq_geom"
                    else f"MISSING_ZERO_PROOF_OR_PROFILE_{probe}",
                    "epsilon_C1": "MISSING_C1_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND"
                    if probe == "Dq_geom"
                    else f"MISSING_C1_ZERO_PROOF_OR_PROFILE_{probe}",
                    "source_path": str(FORMAL_PATH),
                    "valid_for_claim": "False",
                }
            )
    if bound_geom_4272:
        for row in output:
            if row.get("probe_id") == "Dq_geom":
                row["epsilon"] = bound_geom_4272.get("new_epsilon", "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS")
                row["epsilon_C1"] = bound_geom_4272.get("new_epsilon_C1", "MISSING_C1_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS")
                row["source_path"] = str(FORMAL_4272_PATH)
                row["valid_for_claim"] = "False"
    return output


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4271_0_theorem_result",
            "The core coframe-shadow route is now an exact action-domain theorem, not a vague missing item.",
            "No-extra-frame/no-Weyl/no-disformal action-domain ownership implies zero by variable absence and q-chain rule.",
            NEXT_TARGET,
        ),
        (
            "DEC4271_1_current_status",
            "Do not adopt Dq_geom=0 in the public/current branch.",
            "The parent signature is still unsigned; 4234/2960 are private selector/closure routes only.",
            "keep live Dq_geom nonnumeric and nonclaim",
        ),
        (
            "DEC4271_2_finite_route",
            "If the parent signature cannot be closed next, score the finite c_g/b_dis/shadow-frame vector.",
            "This connects the remaining geometry blocker to PPN/R10/WEP/clock/orbital tests without pretending a theorem-zero.",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4271_0_no_closure_as_derivation", "Do not treat 4234 or 2960 private same-frame selector truth as public parent derivation.", "parent_no_extra_frame_signature"),
        ("FW4271_1_no_covariance_shortcut", "Do not infer no shadow frame from diffeomorphism covariance, WEP silence, or Ward conservation alone.", "action-domain exclusion or finite c_g/b_dis bound"),
        ("FW4271_2_no_raw_cg_score", "Do not compare raw c_g directly to Cassini/R10/clock bounds.", "canonical normalization, range/profile response and tail guards"),
        ("FW4271_3_no_trace_erasure", "Do not call finite conformal frame derivative a unit convention if D_v ln A_g is nonzero.", "trace-source row retained"),
        ("FW4271_4_no_local_gr_claim", "Do not claim local GR while Dq_geom, C_perp, eta_domain, nabla_S_norm and eta_C1 remain open.", "4254 stays blocked"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden,
            "required_gate": gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, gate in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4271_0",
            "summary": (
                "4271 converts the remaining Dq_geom core into a sharp theorem/fork: parent-sign no-extra-frame and get zero, "
                "or retain a finite c_g/b_dis/sector-shadow vector tied to local tests. The current live row remains nonclaim."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": "Try to parent-sign the no-extra-frame action-domain clause; if it fails, build the first finite c_g/b_dis bound runner with real projection requirements.",
            "avoid": "Do not loop through generic coframe language, private selector closure, or raw c_g-to-bound comparisons.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 287 - PPC4161 core coframe-shadow zero or first source-backed epsilon row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4271 does not prove public local GR, PPN safety, R10 safety, WEP safety, clock safety, orbital safety, or:

```text
Dq_geom = 0.
```

It proves the exact fork for the remaining geometry core.

## Core frame split

For each ordinary sector `s`, modulo Lorentz/diffeomorphism/q-gauge:

```text
g_s = A_s(Phi)^2 g_obs + B_s(Phi) U_mu U_nu + h_s^perp.
```

For a hidden vertical variation `v in ker(Dq)`:

```text
D_v g_s = 2 c_s g_obs + b_s U_mu U_nu + D_v h_s^perp,
c_s := D_v ln A_s,
b_s := D_v B_s.
```

The matter/action variation is:

```text
D_v S_s
= 1/2 int sqrt(-g_s) T_s^{{mu nu}} D_v g^s_{{mu nu}}
~ int sqrt(-g_s) [c_s T_s + 1/2 b_s T_s^{{mu nu}} U_mu U_nu + ...].
```

So a finite shadow frame is a physical source/readout coupling, not harmless notation.

## Exact zero fork

If the parent action and readouts use only:

```text
e_obs(q),
omega[e_obs],
fixed or q-basic visible constants theta,
q-sector ordinary fields,
```

and exclude independent:

```text
A_s(Phi), B_s(Phi), h_s^perp,
source-only frame slots,
post-readout frame slots,
hidden Hodge/constitutive frame slots,
```

then:

```text
c_s = b_s = D_v h_s^perp = 0,
epsilon_core_observed_readout = 0,
epsilon_core_coframe_shadow = 0.
```

This is a real theorem: variable absence plus the q-chain rule.

## Current result

The current corpus has this theorem route, and the private same-frame selector exists, but the public parent action has not signed the no-extra-frame/action-domain clause.

Therefore the live main branch keeps:

```text
Dq_geom = MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND.
```

## Finite bound fork

Until the parent zero is signed:

```text
epsilon_core_geom
<= C_cg sum_s |c_s|
 + C_dis sum_s |b_dis_s|
 + C_shadow sum_s ||h_s^perp||
 + C_readout epsilon_readout_frame
 + C_terminal epsilon_terminal.
```

The existing Cassini/PPN gamma projection gives only a diagnostic:

```text
alpha_eff <= 0.00578792
```

under the special assumptions `Y_gamma=1` and all non-cg tails theorem-zero. This is not a raw `c_g` score because `N_X`, range/profile response and tail guards are missing.

## 4254 feed

The live `Dq_geom` candidate is sharpened from:

```text
MISSING_REDUCED_EPSILON_GEOM_CORE_COFRAME_SHADOW
```

to:

```text
MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND.
```

## Next target

`{NEXT_TARGET}` should either parent-sign the no-extra-frame clause or build the finite `c_g/b_dis` runner.
"""


def checkpoint_doc() -> str:
    return f"""
# 4271 - Y5 R2FR core coframe-shadow zero or first source-backed epsilon row

Packet marker: `{PACKET_MARKER}`

## Result

The core geometry blocker is now an exact fork:

```text
parent no-extra-frame action-domain signature -> Dq_geom core zero
unsigned parent signature -> finite c_g/b_dis/shadow-frame bound vector
```

## Human translation

If ordinary matter has no hidden frame knob to turn, there is nothing for hidden vertical geometry to push on. If it does have a hidden frame knob, that knob couples to matter trace, light cones, clocks, source normalization and PPN channels.

That is a real derivation target, not a vibes gap.

## Claim firewall

No local-GR claim is made. The live route still needs either parent action signature or finite sourced component bounds.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorems = csv_rows(paths["theorems"])
    residuals = csv_rows(paths["residuals"])
    bridges = csv_rows(paths["bridges"])
    diagnostics = csv_rows(paths["diagnostics"])
    core_candidate = csv_rows(paths["core_candidate"])
    local_candidate = csv_rows(paths["local_candidate"])
    live_candidate = csv_rows(LIVE_COMPONENT_CANDIDATE_PATH)
    live_geom = [row for row in live_candidate if row.get("probe_id") == "Dq_geom"]
    live_geom_is_4271 = (
        bool(live_geom)
        and live_geom[0].get("epsilon") == "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND"
        and live_geom[0].get("epsilon_C1") == "MISSING_C1_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND"
        and live_geom[0].get("source_path") == str(FORMAL_PATH)
    )
    live_geom_is_later_4272 = (
        bool(live_geom)
        and live_geom[0].get("epsilon") == "MISSING_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
        and live_geom[0].get("epsilon_C1") == "MISSING_C1_SCOREABLE_CG_BDIS_FRAME_VECTOR_INPUTS"
        and live_geom[0].get("source_path") == str(FORMAL_4272_PATH)
    )
    prior_zero_components = {
        "Dq_tau": "285-PPC4161-Dq-tau-reference-time-lock-or-tau-residual-bound.md",
        "Dq_matter": "281-PPC4161-Dq-matter-action-domain-zero-or-source-prefactor-bound.md",
        "Dq_source_readout": "282-PPC4161-Dq-source-readout-Hilbert-charge-zero-or-coefficient-remainder.md",
        "Dq_theta_marker": "280-PPC4161-Dq-theta-marker-component-zero-or-marker-bound.md",
        "Dq_boundary_projector": "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
        "Dq_EM": "279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md",
        "Dq_coeff": "283-PPC4161-Dq-coeff-fixed-parent-constant-or-Newton-calibration-bound.md",
    }
    prior_zeros_preserved = True
    for probe, source_file in prior_zero_components.items():
        rows = [row for row in live_candidate if row.get("probe_id") == probe]
        if not rows or rows[0].get("epsilon") != "0.0" or source_file not in rows[0].get("source_path", ""):
            prior_zeros_preserved = False
    residual_components = {row.get("component") for row in residuals}
    rows = [
        ("VAL4271_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4271_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4271_2_source_formula",
            any(row["status"] == "DERIVED_SOURCE_FORMULA" for row in theorems),
            "finite shadow frame source formula emitted",
        ),
        (
            "VAL4271_3_exact_zero_fork",
            any(row["status"] == "EXACT_CONDITIONAL_ZERO_THEOREM" for row in theorems),
            "parent no-extra-frame zero theorem emitted",
        ),
        (
            "VAL4271_4_current_zero_unsigned",
            any(row["status"] == "CURRENT_ZERO_UNSIGNED_BOUND_FORK_ACTIVE" for row in theorems),
            "current no-claim verdict retained",
        ),
        (
            "VAL4271_5_core_components_mapped",
            {"c_g", "b_dis", "epsilon_shadow_matter/light/clock/EM/source", "epsilon_readout_frame + epsilon_terminal"}.issubset(residual_components),
            "core frame components mapped",
        ),
        (
            "VAL4271_6_bridge_routes",
            any(row["status"] == "MISSING_PUBLIC_PARENT_SIGNATURE" for row in bridges)
            and any(row["status"] == "MISSING_COMPONENT_VALUES_AND_PROJECTIONS" for row in bridges),
            "parent-zero and finite-bound routes both represented",
        ),
        (
            "VAL4271_7_diagnostic_nonclaim",
            bool(diagnostics)
            and diagnostics[0].get("numeric_value") == "0.00578792"
            and diagnostics[0].get("valid_for_claim") == "False",
            "Cassini alpha_eff diagnostic carried as nonclaim",
        ),
        (
            "VAL4271_8_core_candidate_nonclaim",
            bool(core_candidate)
            and core_candidate[0]["new_epsilon"] == "MISSING_CORE_FRAME_COUPLING_ZERO_OR_NUMERIC_CG_BDIS_BOUND"
            and core_candidate[0]["valid_for_claim"] == "False",
            "core Dq_geom candidate is nonclaim",
        ),
        (
            "VAL4271_9_live_4254_updated_nonzero",
            live_geom_is_4271 or live_geom_is_later_4272,
            "live 4254 candidate Dq_geom updated to 4271 core row or later 4272 refinement",
        ),
        (
            "VAL4271_10_local_candidate_matches_live",
            (
                any(row.get("probe_id") == "Dq_geom" and row.get("source_path") == str(FORMAL_PATH) for row in local_candidate)
                and live_geom_is_4271
            )
            or (
                any(row.get("probe_id") == "Dq_geom" and row.get("source_path") == str(FORMAL_4272_PATH) for row in local_candidate)
                and live_geom_is_later_4272
            ),
            "local and live candidates carry 4271 source or later 4272 source",
        ),
        (
            "VAL4271_11_prior_zero_adoptions_preserved",
            prior_zeros_preserved,
            "prior tau/matter/source/theta/boundary/EM/coefficient zero rows preserved",
        ),
        (
            "VAL4271_12_no_fake_claim",
            bool(live_geom) and live_geom[0].get("epsilon") != "0.0" and all(row.get("valid_for_claim") == "False" for row in sources + theorems + residuals + bridges + diagnostics),
            "geometry remains nonzero/nonclaim",
        ),
        ("VAL4271_13_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4271_14_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4271_15_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in rows
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4271_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4271_CORE_SHADOW_ACTION_DOMAIN_THEOREM.csv"
    residual_path = SOURCE_DIR / "P8_Y5_R2FR_4271_CORE_RESIDUAL_DECOMPOSITION.csv"
    bridge_path = SOURCE_DIR / "P8_Y5_R2FR_4271_FRAME_COMPONENT_BRIDGE.csv"
    diagnostic_path = SOURCE_DIR / "P8_Y5_R2FR_4271_FIRST_DIAGNOSTIC_BOUND_ROW.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4271_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4271_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4271_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4271_NEXT_TARGET.csv"

    component_candidate = component_candidate_rows()
    write_csv(source_path, source_rows())
    write_csv(theorem_path, theorem_rows())
    write_csv(residual_path, residual_decomposition_rows())
    write_csv(bridge_path, frame_bridge_rows())
    write_csv(diagnostic_path, diagnostic_bound_rows())
    write_csv(CORE_CANDIDATE_PATH, core_candidate_rows())
    write_csv(LOCAL_COMPONENT_CANDIDATE_PATH, component_candidate)
    write_csv(LIVE_COMPONENT_CANDIDATE_PATH, component_candidate)
    write_csv(decision_path, decision_rows())
    write_csv(firewall_path, firewall_rows())
    write_csv(status_path, status_rows())
    write_csv(next_path, next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()

    paths = {
        "sources": source_path,
        "theorems": theorem_path,
        "residuals": residual_path,
        "bridges": bridge_path,
        "diagnostics": diagnostic_path,
        "core_candidate": CORE_CANDIDATE_PATH,
        "local_candidate": LOCAL_COMPONENT_CANDIDATE_PATH,
    }
    validation = validation_rows(paths)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 11 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()
