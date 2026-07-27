from __future__ import annotations

import csv
import shutil
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1467"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1467-Y5-R10-RAB-unique-EM-owner-no-hidden-F2-proof-or-CMSM-browser-session-run.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1466_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1466_VALIDATION.csv"
PREV_EM_EDGE = OUT / "P8_Y5_R10_1466_EM_CURRENT_EDGE_OWNER_PROOF_ATTEMPT.csv"
PREV_REQUIREMENTS = OUT / "P8_Y5_R10_1466_EM_OWNER_REQUIREMENT_MATRIX.csv"
PREV_COUNTERMODELS = OUT / "P8_Y5_R10_1466_EM_EDGE_COUNTERMODEL_LEDGER.csv"
PREV_CAPTURE = OUT / "P8_Y5_R10_1466_CMSM_BROWSER_SESSION_CAPTURE_WORKFLOW.csv"
PREV_CAPTURE_RESULT = OUT / "P8_Y5_R10_1466_CMSM_SESSION_CAPTURE_RESULT_NONCLAIM.csv"
PREV_GATES = OUT / "P8_Y5_R10_1466_REDUCTION_GATES.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1466_PARENT_SIGNING_DECISION.csv"

PARENT_990 = OUT / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv"
PARENT_1055 = OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
CONSTANT_SECTOR = OUT / "P8_constant_sector_universality_CONTRACT.csv"
GLOBAL_COUPLING = OUT / "P8_global_coupling_superselection_CONTRACT.csv"
NO_SPECIES_SOURCE = OUT / "P8_no_species_source_charge_CONTRACT.csv"
DOMAIN_NOVECTOR = OUT / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv"
DOMAIN_VECTOR_GATE = OUT / "P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENT_GATE.csv"
DOMAIN_ALPHA3 = OUT / "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv"
LOCAL_ZERO_CLAUSE = OUT / "P8_PARENT_LOCAL_ZERO_ACTION_CLAUSE.csv"
LOCAL_ZERO_IDENTITIES = OUT / "P8_PARENT_LOCAL_ZERO_REQUIRED_IDENTITIES.csv"
CURRENT_1453 = OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv"
SELECTOR_1453 = OUT / "P8_Y5_R10_1453_CURRENT_RESCALING_SELECTOR_MATRIX.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_CMSM_FILELIST = MICROSCOPE / "official_filelists" / "CMSM_MICROSCOPE_filelist_checksummed.csv"
LIVE_EM_EDGE_IMPORT = COEFF / "EM_current_edge_parent_signed_import.csv"
LIVE_VISIBLE_ALGEBRA_IMPORT = COEFF / "visible_coefficient_algebra_parent_signed_import.csv"

CMSM_MODULE_7 = "https://cmsm-ds.onera.fr/user/microscope/modules/7"
CMSM_PORTAL = "https://cmsm-ds.onera.fr/user/microscope"
CMSM_COMPLEX_SEARCH = "https://cmsm-ds.onera.fr/user/microscope/api/v1/rs-catalog/complex/search"
CMSM_DATAOBJECT_SEARCH = "https://cmsm-ds.onera.fr/user/microscope/api/v1/rs-access-project/dataobjects/search"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1467_SOURCE_REGISTER.csv"
VISIBLE_ALGEBRA = OUT / "P8_Y5_R10_1467_VISIBLE_COEFFICIENT_ALGEBRA_THEOREM_ATTEMPT.csv"
UNIQUE_EM_OWNER = OUT / "P8_Y5_R10_1467_UNIQUE_EM_OWNER_NO_HIDDEN_F2_PROOF_ATTEMPT.csv"
NO_HIDDEN_F2 = OUT / "P8_Y5_R10_1467_NO_HIDDEN_F2_OPERATOR_CLASSIFICATION.csv"
SOURCE_LABEL_IMPACT = OUT / "P8_Y5_R10_1467_SOURCE_LABEL_FORGETTING_IMPACT.csv"
COUNTERMODELS = OUT / "P8_Y5_R10_1467_COUNTERMODEL_LEDGER.csv"
CMSM_SESSION_RUN = OUT / "P8_Y5_R10_1467_CMSM_BROWSER_SESSION_RUN_LEDGER.csv"
CMSM_ENDPOINT_PROBE = OUT / "P8_Y5_R10_1467_CMSM_ENDPOINT_PROBE_NONCLAIM.csv"
CAPTURE_EVIDENCE = OUT / "P8_Y5_R10_1467_CMSM_CAPTURE_EVIDENCE_REQUIREMENTS.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1467_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1467_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1467_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1467_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1467_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1467_VALIDATION.csv"

QUAR_SESSION_RUN = QUARANTINE / "CMSM_BROWSER_SESSION_RUN_LEDGER_NONCLAIM.csv"
QUAR_ENDPOINT_PROBE = QUARANTINE / "CMSM_ENDPOINT_PROBE_NONCLAIM.csv"
QUAR_CAPTURE_REQUIREMENTS = QUARANTINE / "CMSM_CAPTURE_EVIDENCE_REQUIREMENTS.csv"

BRANCH_VISIBLE_ALGEBRA = COEFF / "visible_coefficient_algebra_theorem_attempt_1467.csv"
BRANCH_EM_OWNER = COEFF / "unique_EM_owner_no_hidden_F2_attempt_1467.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_unique_EM_owner_signing_decision_1467.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def copy_branch(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= START_TS:
            count += 1
    return count


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1467_0_1466_next", PREV_NEXT, "1466 handoff to unique EM owner/no-hidden-F2 theorem"),
        ("SRC1467_1_1466_validation", PREV_VALIDATION, "1466 validation baseline"),
        ("SRC1467_2_1466_em_edge", PREV_EM_EDGE, "exact conditional EM current edge theorem"),
        ("SRC1467_3_1466_requirements", PREV_REQUIREMENTS, "missing parent EM owner requirements"),
        ("SRC1467_4_1466_countermodels", PREV_COUNTERMODELS, "hidden F2/source/readout countermodels"),
        ("SRC1467_5_1466_capture", PREV_CAPTURE, "CMSM browser-session workflow"),
        ("SRC1467_6_1466_capture_result", PREV_CAPTURE_RESULT, "CMSM session not executed in 1466"),
        ("SRC1467_7_1466_gates", PREV_GATES, "1466 gate pattern"),
        ("SRC1467_8_1466_signing", PREV_SIGNING, "1466 signing refusal"),
        ("SRC1467_9_parent_990", PARENT_990, "parent action contract EM lock"),
        ("SRC1467_10_parent_1055", PARENT_1055, "no mixed coefficients and EM owner contract candidate"),
        ("SRC1467_11_constant_sector", CONSTANT_SECTOR, "constant-sector universality contract"),
        ("SRC1467_12_global_coupling", GLOBAL_COUPLING, "global coupling superselection analogy"),
        ("SRC1467_13_no_species_source", NO_SPECIES_SOURCE, "source label/species charge contract"),
        ("SRC1467_14_domain_novector", DOMAIN_NOVECTOR, "example of covariance not proving no-vector/no-leak"),
        ("SRC1467_15_domain_vector_gate", DOMAIN_VECTOR_GATE, "coefficient gate pattern for retained residuals"),
        ("SRC1467_16_domain_alpha3", DOMAIN_ALPHA3, "no-leak theorem attempt template"),
        ("SRC1467_17_local_zero_clause", LOCAL_ZERO_CLAUSE, "parent local zero action clause analogy"),
        ("SRC1467_18_local_zero_identities", LOCAL_ZERO_IDENTITIES, "required identities for local zero"),
        ("SRC1467_19_current_1453", CURRENT_1453, "current/source normalization owner theorem attempt"),
        ("SRC1467_20_selector_1453", SELECTOR_1453, "source/current rescaling selector matrix"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, usage in local_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": str(path.relative_to(ROOT)),
                "exists": path.exists(),
                "usage": usage,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    for source_id, url, usage in [
        ("SRC1467_21_CMSM_module_7", CMSM_MODULE_7, "authenticated CMSM module target"),
        ("SRC1467_22_CMSM_portal", CMSM_PORTAL, "CMSM portal target"),
        ("SRC1467_23_CMSM_complex_search", CMSM_COMPLEX_SEARCH, "candidate REGARDS catalog endpoint"),
        ("SRC1467_24_CMSM_dataobjects", CMSM_DATAOBJECT_SEARCH, "candidate REGARDS dataobject endpoint"),
    ]:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "web_url_string",
                "path_or_url": url,
                "exists": "probe_recorded_separately",
                "usage": usage,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def visible_algebra_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "VCA1467_0_target",
            "claim": "no hidden visible-coefficient maps",
            "mathematical_form": "Allowed[Coeff(O_vis)] subset q_loc^* C^infty(Q_obs) tensor pi_const^* C^infty(K_const); Hom(C_hid,Coeff(O_vis)) = 0",
            "result": "TARGET_EQUIVALENCE_SHARPENED",
            "what_it_proves_if_signed": "any visible coefficient is a quotient/constant object, so vertical hidden motion cannot alter it",
            "current_gap": "PAC1055_3 is a contract candidate, not a derived parent operator-classification theorem",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "VCA1467_1_vertical_derivative",
            "claim": "visible coefficient silence follows from coefficient-algebra descent",
            "mathematical_form": "for v in ker(Dq_loc) cap ker(Dpi_const), c_vis=q_loc^*c_Q*pi_const^*c_K implies L_v c_vis=0",
            "result": "EXACT_SUBTHEOREM",
            "what_it_proves_if_signed": "hidden representative directions cannot source alpha_EM, masses, clocks, or other visible coefficients",
            "current_gap": "the inclusion of all visible coefficients in the descended algebra remains unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "VCA1467_2_necessity",
            "claim": "a hidden coefficient is exactly the obstruction",
            "mathematical_form": "if exists Xhat with v(Xhat) != 0 and c_vis=c0+epsilon f(Xhat), then L_v c_vis=epsilon f'(Xhat)v(Xhat) != 0 generically",
            "result": "EXACT_OBSTRUCTION",
            "what_it_proves_if_signed": "any allowed hidden map into visible coefficients reopens the EM/clock/WEP source residual branch",
            "current_gap": "diffeomorphism and gauge covariance alone allow scalar Xhat coefficient maps",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "VCA1467_3_countermodel",
            "claim": "covariance/gauge invariance do not forbid hidden visible coefficients",
            "mathematical_form": "S_EM=-1/4 int sqrt(-g) [g_*^-2 + epsilon f(Xhat)] F_Q^2 with Xhat a parent scalar and A_Q a proper U(1) connection",
            "result": "COUNTERMODEL_SURVIVES",
            "what_it_proves_if_signed": "nothing; it shows why the parent algebra theorem is required",
            "current_gap": "must exclude hidden coefficient maps by parent grammar, not by covariance rhetoric",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "VCA1467_4_verdict",
            "claim": "visible coefficient algebra closes no-hidden-F2",
            "mathematical_form": "NoHiddenF2 <=> Z_EM in q_loc^*C^infty(Q_obs) tensor pi_const^*C^infty(K_const) for the EM kinetic coefficient, with unique A_Q owner separately required",
            "result": "EXACT_EQUIVALENCE_NOT_PARENT_SIGNED",
            "what_it_proves_if_signed": "the no-hidden-F2 branch would close structurally if the parent visible coefficient algebra is derived",
            "current_gap": "visible coefficient algebra triviality is not derived from deeper MTS primitives in the current corpus",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def unique_em_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "UEO1467_0_AQ_descent",
            "target": "unique observed EM connection",
            "required_statement": "A_Q is a connection on a single observed U(1) bundle over Q_obs with parent gauge lifts preserving the same quotient object",
            "result": "CONDITIONAL_DESCENT_FORM_READY",
            "if_signed": "duplicate_AQ countermodel is killed",
            "remaining_gap": "no parent proof that all EM readout/coupling branches use this same quotient connection",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "UEO1467_1_F2_coefficient",
            "target": "unique Maxwell kinetic coefficient",
            "required_statement": "Z_EM(Phi) multiplying F_Q^2 is a constant-sector/topological-level object, not a hidden-field functional",
            "result": "REDUCED_TO_VISIBLE_COEFFICIENT_ALGEBRA",
            "if_signed": "hidden f(Xhat)F_Q^2 is forbidden",
            "remaining_gap": "visible coefficient algebra is exact conditional but not parent-signed",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "UEO1467_2_current_normalization",
            "target": "charge-current normalization",
            "required_statement": "J_Q is obtained by variation with respect to the same A_Q before readout and cannot be independently rescaled downstream",
            "result": "PARTIAL_FROM_1453_AND_1466",
            "if_signed": "post-current EM rescaling is killed",
            "remaining_gap": "pre-action source weights and non-Hilbert currents remain outside pure EM current algebra",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "UEO1467_3_rep_charge",
            "target": "fixed representation charge",
            "required_statement": "q_e and charge generator T_Q are fixed representation/topological data under vertical MTS flow",
            "result": "CONDITIONAL_FROM_CONSTANT_SECTOR_CONTRACT",
            "if_signed": "charge cannot become a hidden local source knob",
            "remaining_gap": "constant-sector superselection is not parent-derived",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "UEO1467_4_verdict",
            "target": "unique EM owner/no-hidden-F2 proof",
            "required_statement": "A_Q descent + visible coefficient algebra + fixed charge/current extraction + readout closure",
            "result": "PROMISING_REDUCTION_NOT_CLOSED",
            "if_signed": "EM alpha/Coulomb hidden coefficient branch would close structurally",
            "remaining_gap": "the parent grammar that forbids hidden visible coefficients is still the missing theorem",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def no_hidden_f2_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "NHF1467_0_allowed",
            "operator": "Z_EM(K_const) F_Q^2",
            "classification": "ALLOWED_IF_CONSTANT_SECTOR_OWNER_SIGNED",
            "reason": "coefficient is fixed by representation/topological/constant sector and is vertically silent",
            "Lie_v_coefficient_zero": "conditional_true",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "NHF1467_1_forbidden_if_algebra_signed",
            "operator": "f(Xhat) F_Q^2",
            "classification": "FORBIDDEN_ONLY_IF_VISIBLE_ALGEBRA_SIGNED",
            "reason": "hidden representative scalar maps into visible EM kinetic coefficient",
            "Lie_v_coefficient_zero": "false_generically",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "NHF1467_2_duplicate_connection",
            "operator": "F_Q[A_1]^2 + F_Q[A_2]^2 or mixed readout A_Q^obs != A_Q^source",
            "classification": "FORBIDDEN_ONLY_IF_UNIQUE_AQ_DESCENT_SIGNED",
            "reason": "connection uniqueness is separate from coefficient silence",
            "Lie_v_coefficient_zero": "not_applicable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "NHF1467_3_radiative_reentry",
            "operator": "Z_EM^eff(q,K,Xhat;mu) F_Q^2 after EFT/readout",
            "classification": "RETAINED_UNTIL_RADIATIVE_READOUT_CLOSURE",
            "reason": "even a tree-level algebra theorem needs stability under effective/readout maps",
            "Lie_v_coefficient_zero": "not_proved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def source_label_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "impact_id": "SLI1467_0_alpha_branch",
            "if_visible_algebra_signed": "hidden local alpha_EM/F2 coefficient branch closes at tree level",
            "still_not_closed": "WEP/local source universality",
            "why": "no-hidden-F2 controls EM kinetic coefficient, not pre-variation Hilbert source weights",
            "claim_effect": "alpha drift/fifth-force branch improves, but no local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "impact_id": "SLI1467_1_source_weights",
            "if_visible_algebra_signed": "charge/current cannot hide an EM coefficient source marker",
            "still_not_closed": "w_A S_A or kappa_A T_A before gravitational/source variation",
            "why": "source-label forgetting is a separate parent matter/source functor theorem",
            "claim_effect": "connected-graph edge remains nonclaim until source functor is signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "impact_id": "SLI1467_2_local_GR",
            "if_visible_algebra_signed": "one EM-sector leak is removed from the local residual vector",
            "still_not_closed": "EH operator, measured GM/source charge, PPN readout, R11 silence",
            "why": "GR reduction requires gravity/source/readout identities, not only EM coupling hygiene",
            "claim_effect": "project moves forward but remains pre-claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1467_0_covariant_hidden_F2",
            "countermodel": "S_EM includes [g_*^-2+epsilon f(Xhat)]F_Q^2 where Xhat is a scalar parent hidden invariant",
            "survives_why": "gauge and diffeomorphism covariance are preserved",
            "killed_by_1467": False,
            "needed_to_kill": "parent visible coefficient algebra theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1467_1_duplicate_AQ",
            "countermodel": "two quotient-adjacent EM connections share charges but differ in source/readout branches",
            "survives_why": "coefficient algebra silence does not itself prove unique connection descent",
            "killed_by_1467": False,
            "needed_to_kill": "unique A_Q descent theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1467_2_pre_source_weight",
            "countermodel": "S_matter=sum_A w_A S_A with ordinary EM action still clean",
            "survives_why": "visible EM coefficient silence does not remove species source prefactors",
            "killed_by_1467": False,
            "needed_to_kill": "source-label forgetting/common matter source functor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1467_3_EFT_reentry",
            "countermodel": "renormalized/readout map generates Z_EM^eff(Xhat) even if bare Z_EM is fixed",
            "survives_why": "radiative/readout closure is a separate theorem",
            "killed_by_1467": False,
            "needed_to_kill": "radiative/readout quotient-preservation theorem or explicit residual bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def cmsm_session_run_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "session_id": "CMSM1467_0_auth_requirement",
            "route": "authenticated browser session",
            "status": "NO_AUTHENTICATED_USER_BROWSER_STATE_AVAILABLE_TO_SCRIPT",
            "what_was_done": "1467 performs non-auth endpoint probes only and records the evidence requirement for a future user/browser capture",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "session_id": "CMSM1467_1_capture_contract",
            "route": "future DevTools/HAR or authenticated browser export",
            "status": "CAPTURE_CONTRACT_READY",
            "what_was_done": "required evidence rows are written in CAPTURE_EVIDENCE and quarantine copies",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def probe_url(url: str, method: str) -> dict[str, Any]:
    request = urllib.request.Request(url, method=method, headers={"User-Agent": "MTS-private-audit/1467"})
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            body = response.read(2048)
            text = body.decode("utf-8", errors="ignore").lower()
            contains_filelist = any(token in text for token in ["checksum", "downloadurl", "download_url", "dataobject", "dataset"])
            return {
                "http_status": response.status,
                "final_url": response.geturl(),
                "content_type": response.headers.get("content-type", ""),
                "sample_bytes": len(body),
                "result": "HTTP_RESPONSE_NO_CLAIM",
                "filelist_like_tokens_seen": contains_filelist,
                "error": "",
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(2048)
        text = body.decode("utf-8", errors="ignore").lower()
        contains_filelist = any(token in text for token in ["checksum", "downloadurl", "download_url", "dataobject", "dataset"])
        return {
            "http_status": exc.code,
            "final_url": url,
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "sample_bytes": len(body),
            "result": "HTTP_ERROR_NO_CLAIM",
            "filelist_like_tokens_seen": contains_filelist,
            "error": str(exc.reason),
        }
    except Exception as exc:
        return {
            "http_status": "",
            "final_url": url,
            "content_type": "",
            "sample_bytes": 0,
            "result": "NETWORK_ERROR_NO_CLAIM",
            "filelist_like_tokens_seen": False,
            "error": f"{type(exc).__name__}: {exc}",
        }


def cmsm_endpoint_probe_rows() -> list[dict[str, Any]]:
    probes = [
        ("PROBE1467_0_module7_get", "GET", CMSM_MODULE_7),
        ("PROBE1467_1_portal_get", "GET", CMSM_PORTAL),
        ("PROBE1467_2_complex_options", "OPTIONS", CMSM_COMPLEX_SEARCH),
        ("PROBE1467_3_dataobjects_options", "OPTIONS", CMSM_DATAOBJECT_SEARCH),
    ]
    rows: list[dict[str, Any]] = []
    for probe_id, method, url in probes:
        result = probe_url(url, method)
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "probe_id": probe_id,
                "method": method,
                "url": url,
                "http_status": result["http_status"],
                "final_url": result["final_url"],
                "content_type": result["content_type"],
                "sample_bytes": result["sample_bytes"],
                "result": result["result"],
                "filelist_like_tokens_seen": result["filelist_like_tokens_seen"],
                "filelist_acquired": False,
                "checksums_acquired": False,
                "download_urls_acquired": False,
                "error": result["error"],
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def capture_evidence_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "evidence_id": "EV1467_0_auth_context",
            "required_evidence": "authenticated browser/session context or official unauthenticated API response",
            "current_status": "MISSING",
            "promotion_rule": "no source pack without authenticated/official response provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "evidence_id": "EV1467_1_filelist_rows",
            "required_evidence": "dataset_id, product_id, file_name, file_role, byte_count, row_count, download_url",
            "current_status": "MISSING",
            "promotion_rule": "all fields must be machine-readable and source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "evidence_id": "EV1467_2_checksums",
            "required_evidence": "official checksum or locally computed checksum after official download URL",
            "current_status": "MISSING",
            "promotion_rule": "no live coefficient/readout import without checksum ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "evidence_id": "EV1467_3_schema",
            "required_evidence": "metadata schema or column dictionary for downloaded files",
            "current_status": "MISSING",
            "promotion_rule": "no parser-based source map without schema or reviewed columns",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    guarded_paths = [
        ("LG1467_0_official_readout", LIVE_OFFICIAL_READOUT, "official MICROSCOPE readout kernel"),
        ("LG1467_1_source_worldtube", LIVE_SOURCE_WORLD, "source worldtube/projection table"),
        ("LG1467_2_material_tensor", LIVE_MATERIAL_TENSOR, "material tensor from official data"),
        ("LG1467_3_Cparent", LIVE_CPARENT, "live C_parent WEP coefficient import"),
        ("LG1467_4_CMSM_filelist", LIVE_CMSM_FILELIST, "live CMSM official file-list import"),
        ("LG1467_5_EM_edge_import", LIVE_EM_EDGE_IMPORT, "live parent-signed EM edge import"),
        ("LG1467_6_visible_algebra_import", LIVE_VISIBLE_ALGEBRA_IMPORT, "live parent-signed visible coefficient algebra import"),
    ]
    return [
        {
            "guard_id": guard_id,
            "path": str(path.relative_to(ROOT)),
            "meaning": meaning,
            "exists_now": path.exists(),
            "would_write_in_1467": False,
            "status": "ABSENT_EXPECTED" if not path.exists() else "PRESENT_PREEXISTING_REVIEW_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, meaning in guarded_paths
    ]


def reduction_gate_rows(
    visible: list[dict[str, Any]],
    unique: list[dict[str, Any]],
    probes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    equivalence_written = any(row["result"] == "EXACT_EQUIVALENCE_NOT_PARENT_SIGNED" for row in visible)
    reduction_written = any(row["result"] == "PROMISING_REDUCTION_NOT_CLOSED" for row in unique)
    probes_recorded = len(probes) >= 4
    return [
        {
            "gate_id": "GATE1467_0_visible_algebra_equivalence",
            "gate": "no-hidden-F2 reduced to visible coefficient algebra theorem",
            "gate_pass": equivalence_written,
            "claim_effect": "derivation sharpened only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1467_1_parent_visible_algebra_signed",
            "gate": "parent visible coefficient algebra is signed",
            "gate_pass": False,
            "claim_effect": "no-hidden-F2 cannot be promoted without this",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1467_2_unique_AQ_signed",
            "gate": "unique A_Q quotient descent is signed",
            "gate_pass": False,
            "claim_effect": "duplicate EM branch remains possible",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1467_3_source_label_forgetting_signed",
            "gate": "source-label forgetting/common source functor is signed",
            "gate_pass": False,
            "claim_effect": "WEP/local source universality remains blocked",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1467_4_unique_EM_reduction_written",
            "gate": "unique EM owner proof is reduced to concrete parent clauses",
            "gate_pass": reduction_written,
            "claim_effect": "next proof target is now precise",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1467_5_CMSM_probes_recorded",
            "gate": "CMSM non-auth endpoint probes/session requirement recorded",
            "gate_pass": probes_recorded,
            "claim_effect": "data capture remains quarantine-only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1467_6_CMSM_filelist_acquired",
            "gate": "official CMSM file list and checksums acquired",
            "gate_pass": False,
            "claim_effect": "official data source pack remains missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1467_7_local_claim",
            "gate": "local GR/WEP/R10 claim allowed",
            "gate_pass": False,
            "claim_effect": "explicitly forbidden in 1467",
            "valid_for_claim": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1467_0_unique_EM_owner",
            "target": "unique EM owner/no-hidden-F2 theorem",
            "visible_algebra_equivalence_written": True,
            "parent_visible_algebra_signed": False,
            "unique_AQ_descent_signed": False,
            "source_label_forgetting_signed": False,
            "radiative_readout_closure_signed": False,
            "CMSM_filelist_imported": False,
            "no_hidden_F2_import_allowed": False,
            "edge_counts_for_connected_graph": False,
            "Delta_w_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "tau_WEP_numeric_allowed": False,
            "local_claim_allowed": False,
            "decision": "REDUCE_NO_HIDDEN_F2_TO_VISIBLE_COEFFICIENT_ALGEBRA_KEEP_NONCLAIM",
            "reason": "no-hidden-F2 is mathematically controlled by a parent coefficient-algebra theorem, but that theorem is not yet parent-derived",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1467_0_derivation",
            "decision": "no-hidden-F2 is not solved directly; it is reduced to parent visible-coefficient algebra",
            "why": "covariant hidden scalar coefficients are legal unless the parent grammar forbids hidden-to-visible coefficient maps",
            "consequence": "next derivation target is the parent algebra theorem, not more QED algebra",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1467_1_claim_guard",
            "decision": "do not promote the EM edge or local branch",
            "why": "unique A_Q descent, source-label forgetting, and radiative/readout closure remain unsigned",
            "consequence": "WEP/R10/PPN/local-GR claims remain blocked",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1467_2_CMSM",
            "decision": "record endpoint probes and authenticated evidence requirements only",
            "why": "a script cannot supply the user's authenticated browser state or official file-list/checksum rows",
            "consequence": "CMSM remains useful for future data plumbing, not for this derivation claim",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1467_0_1468",
            "next_target": "1468-Y5-R10-RAB-parent-visible-coefficient-algebra-triviality-or-retained-alpha-bound.md",
            "script": "scripts/Y5_R10_RAB_parent_visible_coefficient_algebra_triviality_or_retained_alpha_bound.py",
            "objective": "try to parent-derive the visible coefficient algebra theorem that forbids hidden maps into EM/mass/clock coefficients; if it fails, keep alpha/constant channels as retained bound rows",
            "include": "quotient algebra; constant-sector superselection; hidden invariant map exclusion; f(Xhat)F_Q^2 countermodel; retained alpha/clock/WEP residuals",
            "exclude": "local-GR pass; WEP/R10 claim; C_parent promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        VISIBLE_ALGEBRA,
        UNIQUE_EM_OWNER,
        NO_HIDDEN_F2,
        SOURCE_LABEL_IMPACT,
        COUNTERMODELS,
        CMSM_SESSION_RUN,
        CMSM_ENDPOINT_PROBE,
        CAPTURE_EVIDENCE,
        QUAR_SESSION_RUN,
        QUAR_ENDPOINT_PROBE,
        QUAR_CAPTURE_REQUIREMENTS,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def csv_parse_clean(paths: list[Path]) -> bool:
    try:
        for path in paths:
            rows = read_csv_rows(path)
            if not rows:
                return False
        return True
    except Exception:
        return False


def branch_copies_exist() -> bool:
    return BRANCH_VISIBLE_ALGEBRA.exists() and BRANCH_EM_OWNER.exists() and BRANCH_SIGNING.exists()


def validation_rows(
    sources: list[dict[str, Any]],
    visible: list[dict[str, Any]],
    unique: list[dict[str, Any]],
    hidden_f2: list[dict[str, Any]],
    source_impact: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    session_run: list[dict[str, Any]],
    probes: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    equivalence_written = any(row["result"] == "EXACT_EQUIVALENCE_NOT_PARENT_SIGNED" for row in visible)
    exact_obstruction_written = any(row["result"] == "EXACT_OBSTRUCTION" for row in visible)
    unique_reduction_written = any(row["result"] == "PROMISING_REDUCTION_NOT_CLOSED" for row in unique)
    hidden_classifier_ok = any(row["classification"] == "FORBIDDEN_ONLY_IF_VISIBLE_ALGEBRA_SIGNED" for row in hidden_f2)
    source_impact_nonclaim = all(not truth(row["claim_allowed"]) for row in source_impact)
    countermodels_retained = all(not truth(row["killed_by_1467"]) for row in countermodels)
    session_nonclaim = all(not truth(row["claim_allowed"]) for row in session_run + probes + evidence)
    no_filelist_import = all(
        not truth(row.get("filelist_acquired", False))
        and not truth(row.get("checksums_acquired", False))
        and not truth(row.get("download_urls_acquired", False))
        for row in session_run + probes
    )
    evidence_missing = all(row["current_status"] == "MISSING" for row in evidence)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1467"]) for row in live_guard)
    safe_gate_pattern = truth(gates[0]["gate_pass"]) and truth(gates[4]["gate_pass"]) and truth(gates[5]["gate_pass"]) and all(
        not truth(row["gate_pass"]) for row in gates[1:4] + gates[6:]
    )
    signing_refuses = all(
        truth(row["visible_algebra_equivalence_written"])
        and not truth(row["parent_visible_algebra_signed"])
        and not truth(row["no_hidden_F2_import_allowed"])
        and not truth(row["edge_counts_for_connected_graph"])
        and not truth(row["Delta_w_zero_import_allowed"])
        and not truth(row["C_parent_WEP_import_allowed"])
        and not truth(row["tau_WEP_numeric_allowed"])
        and not truth(row["local_claim_allowed"])
        for row in signing
    )
    generated_parse = csv_parse_clean(generated_csvs())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = formalization_modified_count() == 0

    checks = [
        ("VAL1467_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1467_1_equivalence", equivalence_written, "no-hidden-F2 equivalence to visible coefficient algebra written"),
        ("VAL1467_2_obstruction", exact_obstruction_written, "hidden scalar coefficient obstruction written"),
        ("VAL1467_3_unique_reduction", unique_reduction_written, "unique EM owner reduction written"),
        ("VAL1467_4_hidden_classifier", hidden_classifier_ok, "f(Xhat)F_Q^2 classified as forbidden only if algebra theorem is signed"),
        ("VAL1467_5_source_impact", source_impact_nonclaim, "source-label impacts remain nonclaim"),
        ("VAL1467_6_countermodels", countermodels_retained, "all countermodels retained"),
        ("VAL1467_7_session_nonclaim", session_nonclaim, "CMSM session/probe/evidence rows remain nonclaim"),
        ("VAL1467_8_no_filelist", no_filelist_import, "no CMSM file list/checksum/download URL imported"),
        ("VAL1467_9_evidence_missing", evidence_missing, "required official CMSM capture evidence remains explicitly missing"),
        ("VAL1467_10_live_paths", live_paths_untouched, "critical live official/source/material/Cparent/EM/algebra files remain absent"),
        ("VAL1467_11_gate_pattern", safe_gate_pattern, "only derivation-sharpening and probe-recording gates pass; claim gates false"),
        ("VAL1467_12_signing_refuses", signing_refuses, "parent signing refuses no-hidden-F2 import and local claims"),
        ("VAL1467_13_generated_csv_parse", generated_parse, "all generated 1467 CSVs parse cleanly"),
        ("VAL1467_14_branch_copies", branch_copies_exist(), "nonclaim branch copies written"),
        ("VAL1467_15_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1467_16_formalization_untouched", formalization_untouched, f"formalization modified-file count since start={formalization_modified_count()}"),
    ]
    overall = all(result for _, result, _ in checks)
    checks.append(
        (
            "VAL1467_17_overall",
            overall,
            "1467 reduces no-hidden-F2 to parent visible coefficient algebra but refuses promotion",
        )
    )
    generated = now()
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, result, detail in checks
    ]


def write_doc(
    sources: list[dict[str, Any]],
    visible: list[dict[str, Any]],
    unique: list[dict[str, Any]],
    hidden_f2: list[dict[str, Any]],
    source_impact: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    session_run: list[dict[str, Any]],
    probes: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1467 - Y5 R10 RAB Unique EM Owner No Hidden F2 Proof Or CMSM Browser Session Run")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- No-hidden-`F_Q^2` did not close as a standalone theorem.")
    lines.append("- It reduced cleanly to a parent visible-coefficient algebra theorem: visible coefficients must descend only from quotient observables plus fixed constant/topological sectors.")
    lines.append("- If that algebra theorem is parent-signed, `f(Xhat)F_Q^2` dies. If it is not signed, the covariant hidden-scalar countermodel survives.")
    lines.append("- This improves the derivation map, but does not permit EM-edge, WEP, R10, PPN, clock, orbital, local-GR, or `C_parent` promotion.")
    lines.append("- CMSM access remains quarantine-only: unauthenticated endpoint probes/session requirements are recorded, but no official file list or checksums are imported.")
    lines.append("")
    lines.append("## Exact Algebra Reduction")
    lines.append("Let `v in ker(Dq_loc) cap ker(Dpi_const)` be an allowed hidden/vertical direction. If")
    lines.append("")
    lines.append("`Allowed[Coeff(O_vis)] subset q_loc^* C^infty(Q_obs) tensor pi_const^* C^infty(K_const)`,")
    lines.append("")
    lines.append("then every visible coefficient `c_vis` obeys `L_v c_vis = 0`. Hence a Maxwell coefficient `Z_EM` in that algebra cannot contain `f(Xhat)` with `v(Xhat) != 0`.")
    lines.append("")
    lines.append("Conversely, if the parent grammar allows `Z_EM = g_*^-2 + epsilon f(Xhat)`, then `L_v Z_EM = epsilon f'(Xhat)v(Xhat)` generically, and hidden EM/fine-structure leakage remains alive.")
    lines.append("")
    lines.append("## Source Register")
    lines.append("| source_id | type | exists | path_or_url | usage |")
    lines.append("|---|---:|---:|---|---|")
    for row in sources:
        lines.append(f"| {row['source_id']} | {row['source_type']} | {row['exists']} | `{row['path_or_url']}` | {row['usage']} |")
    lines.append("")
    lines.append("## Visible Coefficient Algebra Attempt")
    lines.append("| step_id | result | current_gap | parent_signed |")
    lines.append("|---|---|---|---:|")
    for row in visible:
        lines.append(f"| {row['step_id']} | {row['result']} | {row['current_gap']} | {row['parent_signed']} |")
    lines.append("")
    lines.append("## Unique EM Owner Attempt")
    lines.append("| proof_id | target | result | remaining_gap |")
    lines.append("|---|---|---|---|")
    for row in unique:
        lines.append(f"| {row['proof_id']} | {row['target']} | {row['result']} | {row['remaining_gap']} |")
    lines.append("")
    lines.append("## No-Hidden-F2 Operator Classification")
    lines.append("| row_id | classification | reason |")
    lines.append("|---|---|---|")
    for row in hidden_f2:
        lines.append(f"| {row['row_id']} | {row['classification']} | {row['reason']} |")
    lines.append("")
    lines.append("## Source-Label Impact")
    lines.append("| impact_id | still_not_closed | claim_effect |")
    lines.append("|---|---|---|")
    for row in source_impact:
        lines.append(f"| {row['impact_id']} | {row['still_not_closed']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Countermodels Retained")
    lines.append("| countermodel_id | killed_by_1467 | needed_to_kill |")
    lines.append("|---|---:|---|")
    for row in countermodels:
        lines.append(f"| {row['countermodel_id']} | {row['killed_by_1467']} | {row['needed_to_kill']} |")
    lines.append("")
    lines.append("## CMSM Session/Probe Ledger")
    lines.append("| session_id | status | filelist_acquired |")
    lines.append("|---|---|---:|")
    for row in session_run:
        lines.append(f"| {row['session_id']} | {row['status']} | {row['filelist_acquired']} |")
    lines.append("")
    lines.append("| probe_id | method | http_status | result | filelist_acquired |")
    lines.append("|---|---|---:|---|---:|")
    for row in probes:
        lines.append(f"| {row['probe_id']} | {row['method']} | {row['http_status']} | {row['result']} | {row['filelist_acquired']} |")
    lines.append("")
    lines.append("## Capture Evidence Requirements")
    lines.append("| evidence_id | current_status | required_evidence |")
    lines.append("|---|---|---|")
    for row in evidence:
        lines.append(f"| {row['evidence_id']} | {row['current_status']} | {row['required_evidence']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Parent Signing Decision")
    for row in signing:
        lines.append(f"- `{row['decision_id']}`: `{row['decision']}` because {row['reason']}.")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
    lines.append("")
    lines.append("## Validation")
    lines.append("| check_id | result | detail |")
    lines.append("|---|---|---|")
    for row in validation:
        lines.append(f"| {row['check_id']} | {row['result']} | {row['detail']} |")
    lines.append("")
    lines.append("## Next Target")
    for row in next_target:
        lines.append(f"- `{row['next_target']}` via `{row['script']}`: {row['objective']}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_rows()
    visible = visible_algebra_rows()
    unique = unique_em_owner_rows()
    hidden_f2 = no_hidden_f2_rows()
    source_impact = source_label_impact_rows()
    countermodels = countermodel_rows()
    session_run = cmsm_session_run_rows()
    probes = cmsm_endpoint_probe_rows()
    evidence = capture_evidence_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows(visible, unique, probes)
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(VISIBLE_ALGEBRA, visible)
    write_csv(UNIQUE_EM_OWNER, unique)
    write_csv(NO_HIDDEN_F2, hidden_f2)
    write_csv(SOURCE_LABEL_IMPACT, source_impact)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(CMSM_SESSION_RUN, session_run)
    write_csv(CMSM_ENDPOINT_PROBE, probes)
    write_csv(CAPTURE_EVIDENCE, evidence)
    write_csv(QUAR_SESSION_RUN, session_run)
    write_csv(QUAR_ENDPOINT_PROBE, probes)
    write_csv(QUAR_CAPTURE_REQUIREMENTS, evidence)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(VISIBLE_ALGEBRA, BRANCH_VISIBLE_ALGEBRA)
    copy_branch(UNIQUE_EM_OWNER, BRANCH_EM_OWNER)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(
        sources,
        visible,
        unique,
        hidden_f2,
        source_impact,
        countermodels,
        session_run,
        probes,
        evidence,
        live_guard,
        gates,
        signing,
    )
    write_csv(VALIDATION, validation)
    write_doc(
        sources,
        visible,
        unique,
        hidden_f2,
        source_impact,
        countermodels,
        session_run,
        probes,
        evidence,
        gates,
        signing,
        decisions,
        validation,
        next_target,
    )
    print("Y5_R10_1467_no_hidden_F2_reduced_to_visible_coefficient_algebra_nonclaim")


if __name__ == "__main__":
    main()
