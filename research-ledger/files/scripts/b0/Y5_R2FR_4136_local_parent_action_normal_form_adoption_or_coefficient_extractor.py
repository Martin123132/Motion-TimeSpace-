from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4136-Y5-R2FR-local-parent-action-normal-form-adoption-or-coefficient-extractor.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_PARENT_ACTION_NORMAL_FORM_ADOPTION_OR_COEFFICIENT_EXTRACTOR_4136"
CHECKPOINT_ID = "4136"
DECISION = "LOCAL_NORMAL_FORM_COMPATIBLE_BUT_NOT_PARENT_ADOPTED_COEFFICIENT_EXTRACTOR_EMITTED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4136_00_4135_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4135_NEXT_TARGET.csv",
        "4136-Y5-R2FR-local-parent-action-normal-form-adoption-or-coefficient-extractor.md",
        "4135 selected local parent-action normal-form adoption or coefficient extractor.",
    ),
    "SRC4136_01_4135_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4135_STATUS.csv",
        "SURVIVOR_OPERATORS_REDUCED_TO_LOCAL_NORMAL_FORM_OR_COEFFICIENT_EXTRACTOR",
        "4135 survivor-operator fork status.",
    ),
    "SRC4136_02_4135_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4135_NORMAL_FORM_THEOREM.csv",
        "R_survivor_ops=0",
        "Normal-form theorem from 4135.",
    ),
    "SRC4136_03_4135_operator_map": (
        SOURCE_DIR / "P8_Y5_R2FR_4135_OPERATOR_EXCISION_MAP.csv",
        "Gamma_Khat_q_loc",
        "Survivor operator excision map.",
    ),
    "SRC4136_04_4135_extractors": (
        SOURCE_DIR / "P8_Y5_R2FR_4135_COEFFICIENT_EXTRACTOR_ROWS.csv",
        "CER4135_7_GK",
        "Coefficient extractor templates from 4135.",
    ),
    "SRC4136_05_4021_witness": (
        SOURCE_DIR / "P8_Y5_R2FR_4021_PARENT_LOCAL_ACTION_WITNESS.csv",
        "WIT4021_7_claim_guard",
        "Local parent action witness and claim guard.",
    ),
    "SRC4136_06_4021_lemmas": (
        SOURCE_DIR / "P8_Y5_R2FR_4021_DERIVED_ZERO_LEMMAS.csv",
        "LEM4021_6_PPN_zero_vector_under_witness",
        "Derived zero lemmas under witness.",
    ),
    "SRC4136_07_3576_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_3576_CANDIDATE_PARENT_BRANCH_ADOPTION_PACKET.csv",
        "ADOPT3576_6_no_extra_mass",
        "Candidate branch adoption packet.",
    ),
    "SRC4136_08_3400_clauses": (
        SOURCE_DIR / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
        "PC3400_4_no_boundary_extra_mass",
        "Parent signature clauses.",
    ),
    "SRC4136_09_3424_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_3424_PC3400_ADOPTION_AUDIT.csv",
        "FAIL_RETAINED_DEBT",
        "Adoption audit showing retained debts.",
    ),
    "SRC4136_10_4013_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4013_STATUS.csv",
        "Maxwell/Poynting stress accounting",
        "Maxwell/Poynting once-only stress theorem status.",
    ),
    "SRC4136_11_4014_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4014_STATUS.csv",
        "observed Hodge/Maxwell normalization",
        "Observed-Hodge Maxwell normalization owner status.",
    ),
    "SRC4136_12_4027_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4027_STATUS.csv",
        "Khat components split",
        "Latest Gamma/Khat component split status.",
    ),
    "SRC4136_13_gk_decision": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_DECISION.csv",
        "D513_1",
        "Gamma/Khat/q_loc variational-stress route.",
    ),
    "SRC4136_14_gk_residual": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
        "QR513_0_nonvariational_stress",
        "Gamma/Khat/q_loc residual fallback.",
    ),
    "SRC4136_15_source_norm": (
        SOURCE_DIR / "P8_R11_SOURCE_NORMALIZATION_DECISION.csv",
        "D0_minimum_fill",
        "Source-normalization operator minimum fill.",
    ),
    "SRC4136_16_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4136_local_parent_action_normal_form_adoption_or_coefficient_extractor.py",
        "Reproducible generator for this 4136 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def normal_form_target_rows() -> List[dict]:
    data = [
        (
            "NFT4136_0_configuration",
            "local configuration split",
            "Q_parent^loc = Q_dyn^loc x K_G x Q_aux; q:Q_dyn^loc -> Met_obs; V=ker(Dq); T_local K_G=0",
            "local G/kappa drift silence, observed/vertical split",
        ),
        (
            "NFT4136_1_EH_metric",
            "EH observed metric operator",
            "(2 kappa_*)^-1 int R[g_obs(q(Phi))] eps_obs",
            "Newton/PPN GR-like metric field equations through 2PN",
        ),
        (
            "NFT4136_2_source",
            "same-source matter EM binding",
            "S_matter[psi,g_obs,theta] + S_EM[A,g_obs,mu0,J] + S_binding",
            "single Hilbert/coframe source current, EM/Poynting once-only, beta source lock",
        ),
        (
            "NFT4136_3_silent_terms",
            "silent non-EH terms",
            "dB + S_top + S_aux^double-zero + S_vert[Phi]",
            "boundary/topological/vertical/auxiliary terms carry no observed 2PN stress if premises hold",
        ),
        (
            "NFT4136_4_exclusion",
            "forbidden observed non-EH operators",
            "exclude f(Phi)R, R^2, R_abR^ab, Weyl^2, vector-aether, disformal matter, finite-range bulk_X, nonlocal memory, source prefactors unless scored",
            "prevents local GR from being obtained by post-hoc tuning",
        ),
        (
            "NFT4136_5_special",
            "Gamma/Khat/q_loc special slot",
            "T_GK=Gamma_eff g-Khat must be Hilbert stress/vertical/boundary-silent or retained as q_loc profile",
            "special residual that cannot be hidden under generic operator exclusion",
        ),
    ]
    rows: List[dict] = []
    for target_id, slot, mathematical_form, closes in data:
        row = row_base()
        row.update(
            {
                "target_id": target_id,
                "slot": slot,
                "mathematical_form": mathematical_form,
                "closes_if_adopted": closes,
                "status": "TARGET_NORMAL_FORM_SLOT",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def adoption_audit_rows() -> List[dict]:
    data = [
        (
            "AUD4136_0_configuration",
            "local configuration split",
            "3576/4021 give an internally consistent candidate branch with fixed g_obs/e_obs, q(Phi), tau, Pi_M and K_G",
            "PARTIAL_CANDIDATE_COMPATIBLE",
            "not corpus-adopted; cannot publish as local-GR proof",
            "keep Z_local_normal_form=false",
        ),
        (
            "AUD4136_1_kappa",
            "constant K_G/kappa",
            "PC3400/3576 allow kappa as a GR-style measured universal constant; 4021 proves no local drift if K_G factor is fixed",
            "CAN_SIGN_IN_CANDIDATE_BRANCH_NOT_PUBLIC_CLAIM",
            "SI value of G is calibration, but source/range/time/species drift still needs parent adoption",
            "retain Gdot/WEP/PPN derivative guard",
        ),
        (
            "AUD4136_2_EH",
            "EH observed metric operator",
            "WIT4021 writes EH operator and LEM4021 gives EH zero theorem for non-EH R11 stress under witness",
            "COMPATIBLE_WITNESS_ONLY",
            "actual corpus has not adopted EH-only observed metric operator through 2PN",
            "emit survivor coefficient extractor if not adopted",
        ),
        (
            "AUD4136_3_matter_EM",
            "same-source matter/EM/binding",
            "3576 signs public matter/EM in candidate branch; 4013/4014 derive conditional once-only Maxwell/Hodge/Poynting ownership",
            "PARTIAL_CANDIDATE_STRONG",
            "hidden constitutive sectors, binding, apparatus and source normalization remain possible leaks",
            "keep source-normalization extractor active",
        ),
        (
            "AUD4136_4_boundary_topological",
            "dB and S_top",
            "exact wrong-object boundary piece can vanish in candidate branch; topological/exact terms are allowed by normal form",
            "PARTIAL_EXACT_ZERO_ONLY",
            "harmonic/corner/worldtube/reference remainders are not killed by the exact piece",
            "retain R_boundary_harmonic",
        ),
        (
            "AUD4136_5_vertical",
            "vertical-only sectors",
            "vertical sectors with Dq=0 do not vary g_obs and therefore do not enter observed 2PN metric equations",
            "LOGICAL_ZERO_ROUTE_NOT_SECTOR_CLASSIFIED",
            "actual retained sectors are not all classified as vertical/source-silent",
            "operator classification remains required",
        ),
        (
            "AUD4136_6_double_zero",
            "auxiliary double-zero sectors",
            "double-zero mechanism can silence auxiliary/memory/R11 couplings at fixed point",
            "CONDITIONAL_MECHANISM_NOT_PARENT_DERIVED",
            "double-zero shape is requirement/candidate, not yet owned by parent action",
            "retain double-zero or coefficient fork",
        ),
        (
            "AUD4136_7_no_extra_ops",
            "no survivor observed operators",
            "4135 lists all survivor families and the normal-form exclusion route",
            "FAILS_PUBLIC_ADOPTION_NOW",
            "R2/fR, Ricci/Weyl, scalar, vector, torsion/nonmetricity, bulk_X, memory and source-normalization are not parent-excised",
            "emit coefficient extractor rows",
        ),
        (
            "AUD4136_8_GK",
            "Gamma/Khat/q_loc",
            "4023-4027 construct routes but current Khat/Gamma component match fails for claim",
            "SPECIAL_FAILS_ADOPTION_NOW",
            "T_GK Hilbert-stress/action match, verticality, projector ownership and boundary silence are not signed",
            "make GK/q_loc the next special target",
        ),
    ]
    rows: List[dict] = []
    for audit_id, slot, evidence, adoption_status, live_gap, action in data:
        row = row_base()
        row.update(
            {
                "audit_id": audit_id,
                "slot": slot,
                "evidence": evidence,
                "adoption_status": adoption_status,
                "live_gap": live_gap,
                "action_taken": action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def coefficient_fallback_rows() -> List[dict]:
    rows: List[dict] = []
    extractor_path = SOURCE_DIR / "P8_Y5_R2FR_4135_COEFFICIENT_EXTRACTOR_ROWS.csv"
    for source_row in parse_csv(extractor_path):
        row = row_base()
        row.update(
            {
                "fallback_id": source_row["extractor_id"].replace("CER4135", "CF4136"),
                "operator_family": source_row["operator_family"],
                "extraction_task": source_row["extraction_task"],
                "required_fields": source_row["required_fields"],
                "target_score_rows": source_row["target_score_rows"],
                "trigger": "Z_local_normal_form is not parent-signed",
                "status": "EMITTED_FROM_4135_EXTRACTOR_NONCLAIM",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def refusal_terms_rows() -> List[dict]:
    data = [
        (
            "REF4136_0_parent_adoption",
            "R_parent_adoption",
            "actual MTS parent corpus has not adopted WIT4021 local normal form",
            "boolean guard",
            "blocks all local-GR promotion",
        ),
        (
            "REF4136_1_survivor_ops",
            "R_survivor_ops",
            "observed non-EH survivor operators not yet excised or sourced",
            "dimensionless master residual",
            "PPN/R10/WEP/clocks/Newton source denominator",
        ),
        (
            "REF4136_2_boundary",
            "R_boundary_harmonic",
            "exact boundary zero does not remove harmonic/corner/worldtube/reference remainders",
            "dimensionless boundary charge",
            "alpha3/xi/beta/Gdot/source hair",
        ),
        (
            "REF4136_3_domain",
            "R_undescended_support",
            "binding/apparatus/hidden/source-normalization support may be outside the descended total source action",
            "dimensionless source support integral",
            "WEP/Newton/R10/beta",
        ),
        (
            "REF4136_4_flux",
            "R_unstationary_flux",
            "stationary no-flux branch is not a universal parent theorem",
            "dimensionless flux ratio",
            "clock/orbit flux/Gdot/source hair",
        ),
        (
            "REF4136_5_GK",
            "R_GK_q_loc",
            "Gamma/Khat/q_loc special residual has no signed S_GK or profile bound yet",
            "q_loc force/source-exchange or compact-shell proxy",
            "delta_beta_q_loc/R10/local force",
        ),
    ]
    rows: List[dict] = []
    for refusal_id, symbol, reason, units, arena in data:
        row = row_base()
        row.update(
            {
                "refusal_id": refusal_id,
                "symbol": symbol,
                "reason": reason,
                "units": units,
                "arena_projection": arena,
                "status": "LIVE_REFUSAL_TERM",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DG4136_0_attempted_adoption",
            "NORMAL_FORM_ADOPTION_ATTEMPTED",
            "The WIT4021 normal form was compared slot-by-slot against the current corpus evidence.",
            "use adoption audit rather than repeating broad survivor lists",
        ),
        (
            "DG4136_1_result",
            "COMPATIBLE_BUT_NOT_PARENT_ADOPTED",
            "Several slots are strong candidate-compatible, especially K_G, same public matter/EM and once-only Poynting, but the full parent action has not adopted EH-only plus silent terms through 2PN.",
            "Z_local_normal_form remains false",
        ),
        (
            "DG4136_2_fallback",
            "COEFFICIENT_EXTRACTOR_EMITTED",
            "Because adoption is unsigned, the 4135 coefficient extractor has been emitted as the official fallback.",
            "do not claim local GR; use coefficients if normal form fails",
        ),
        (
            "DG4136_3_special",
            "GK_QLOC_SELECTED_AS_NEXT_SPECIAL_TARGET",
            "Gamma/Khat/q_loc is the most specific refusal term: it has a known variational-stress route and a q_loc-profile bound route.",
            "4137-Y5-R2FR-GK-q-loc-special-action-or-profile-bound.md",
        ),
        (
            "DG4136_4_claim_ceiling",
            "NO_LOCAL_GR_CLAIM",
            "Normal-form compatibility is not adoption; all local GR/Newton/PPN/R10 claims remain blocked.",
            "keep private nonclaim status",
        ),
    ]
    rows: List[dict] = []
    for gate_id, decision, rationale, action in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "decision": decision,
                "rationale": rationale,
                "next_action": action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4136_0",
            "result": DECISION,
            "summary": (
                "4136 attempts the actual WIT4021 local normal-form adoption. The result is compatible but not "
                "parent-adopted: K_G/kappa, public matter/EM, observed Hodge/Poynting and EH witness pieces are "
                "strong candidate slots, but survivor operators, boundary/domain/flux remainders, source-normalization "
                "and Gamma/Khat/q_loc prevent Z_local_normal_form=true. The official fallback is now the 4135 "
                "coefficient extractor, emitted in 4136."
            ),
            "normal_form_adoption_attempted": "True",
            "Z_local_normal_form": "False",
            "coefficient_extractor_emitted": "True",
            "GK_q_loc_special_refusal": "True",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM prediction, Maxwell derivation, alpha derivation, or source-normalization pass",
            "next_target": "4137 GK/q_loc special action or profile bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4136_0",
            "target_doc": "4137-Y5-R2FR-GK-q-loc-special-action-or-profile-bound.md",
            "target_script": "scripts/Y5_R2FR_4137_GK_q_loc_special_action_or_profile_bound.py",
            "objective": (
                "attack the Gamma/Khat/q_loc special refusal term: either sign T_GK as Hilbert stress from a "
                "diffeomorphism-invariant local sector with Euler/projector/boundary silence, or emit a q_loc profile "
                "bound with D_GK components, P_loc ownership, units, PPN/R10 projection and source path"
            ),
            "success_gate": "S_GK/T_GK/q_loc zero parent-signed, or q_loc bound rows are source-backed with units and arena projections",
            "reason": "4136 shows the broad normal form is compatible but blocked; GK/q_loc is the sharpest special refusal term with a known derivation-or-bound fork.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4136_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4136_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4136_NORMAL_FORM_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4136_NORMAL_FORM_TARGET.csv",
        "P8_Y5_R2FR_4136_ADOPTION_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4136_ADOPTION_AUDIT.csv",
        "P8_Y5_R2FR_4136_COEFFICIENT_FALLBACK_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4136_COEFFICIENT_FALLBACK_ROWS.csv",
        "P8_Y5_R2FR_4136_REFUSAL_TERMS": SOURCE_DIR / "P8_Y5_R2FR_4136_REFUSAL_TERMS.csv",
        "P8_Y5_R2FR_4136_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4136_DECISION_GATES.csv",
        "P8_Y5_R2FR_4136_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4136_STATUS.csv",
        "P8_Y5_R2FR_4136_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4136_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4136 - Local Parent-Action Normal-Form Adoption or Coefficient Extractor",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- The normal form is compatible with the best private branch, but not parent-adopted.",
        "- Because adoption fails, the coefficient extractor is now emitted as fallback instead of being merely proposed.",
        "- No Newton/local-GR/PPN/R10 pass is claimed.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Target Normal Form", "", "| slot | status | form |", "|---|---|---|"])
    for row in normal_form_target_rows():
        sections.append(f"| {row['slot']} | {row['status']} | {row['mathematical_form']} |")
    sections.extend(["", "## Adoption Audit", "", "| slot | adoption status | live gap |", "|---|---|---|"])
    for row in adoption_audit_rows():
        sections.append(f"| {row['slot']} | {row['adoption_status']} | {row['live_gap']} |")
    sections.extend(["", "## Fallback Extractor", "", "| operator | required fields | target rows |", "|---|---|---|"])
    for row in coefficient_fallback_rows():
        sections.append(f"| {row['operator_family']} | {row['required_fields']} | {row['target_score_rows']} |")
    sections.extend(
        [
            "",
            "## Current Meaning",
            "",
            "- This is not failure-in-the-bad-sense: the normal-form route is coherent and compatible with several prior candidate clauses.",
            "- It is still not a theorem of the actual corpus, so `Z_local_normal_form=false`.",
            "- The next efficient move is the special `Gamma/Khat/q_loc` refusal term, because it has a concrete action-or-profile fork.",
            "",
            "## Claim Ceiling",
            "",
            f"- {status['claim_state']}.",
            "- Compatibility is not adoption, and adoption is not empirical robustness.",
            "",
            "## Next Target",
            "",
            "- `4137-Y5-R2FR-GK-q-loc-special-action-or-profile-bound.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4136_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4136_NORMAL_FORM_TARGET": normal_form_target_rows,
        "P8_Y5_R2FR_4136_ADOPTION_AUDIT": adoption_audit_rows,
        "P8_Y5_R2FR_4136_COEFFICIENT_FALLBACK_ROWS": coefficient_fallback_rows,
        "P8_Y5_R2FR_4136_REFUSAL_TERMS": refusal_terms_rows,
        "P8_Y5_R2FR_4136_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4136_STATUS": status_rows,
        "P8_Y5_R2FR_4136_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4136_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4136_1_doc",
        "checkpoint markdown exists and names decision",
        DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"),
        str(DOC_PATH),
    )

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4136_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    target_text = flatten_rows([outputs["P8_Y5_R2FR_4136_NORMAL_FORM_TARGET"]])
    target_ok = all(
        token in target_text
        for token in [
            "Q_parent^loc",
            "EH observed metric operator",
            "same-source matter EM binding",
            "dB + S_top + S_aux^double-zero",
            "forbidden observed non-EH operators",
            "Gamma/Khat/q_loc",
        ]
    )
    add("VAL4136_3_target", "target normal form contains configuration, EH, source, silent terms, exclusions and GK slot", target_ok, "target tokens checked")

    audit_text = flatten_rows([outputs["P8_Y5_R2FR_4136_ADOPTION_AUDIT"]])
    audit_ok = all(
        token in audit_text
        for token in [
            "PARTIAL_CANDIDATE_COMPATIBLE",
            "CAN_SIGN_IN_CANDIDATE_BRANCH_NOT_PUBLIC_CLAIM",
            "COMPATIBLE_WITNESS_ONLY",
            "PARTIAL_CANDIDATE_STRONG",
            "FAILS_PUBLIC_ADOPTION_NOW",
            "SPECIAL_FAILS_ADOPTION_NOW",
        ]
    )
    add("VAL4136_4_adoption_audit", "adoption audit records compatibility, partial signatures and failed public adoption", audit_ok, "audit tokens checked")

    fallback = parse_csv(outputs["P8_Y5_R2FR_4136_COEFFICIENT_FALLBACK_ROWS"])
    fallback_text = flatten_rows([outputs["P8_Y5_R2FR_4136_COEFFICIENT_FALLBACK_ROWS"]])
    fallback_ok = len(fallback) == 9 and all(
        token in fallback_text
        for token in ["R2_fR_scalar_mode", "Gamma_Khat_q_loc", "source_normalization_operator", "Z_local_normal_form is not parent-signed"]
    )
    add("VAL4136_5_fallback", "coefficient fallback emits all 4135 extractor rows under normal-form failure", fallback_ok, f"fallback_rows={len(fallback)}")

    refusal_text = flatten_rows([outputs["P8_Y5_R2FR_4136_REFUSAL_TERMS"]])
    refusal_ok = all(
        token in refusal_text
        for token in ["R_parent_adoption", "R_survivor_ops", "R_boundary_harmonic", "R_undescended_support", "R_unstationary_flux", "R_GK_q_loc"]
    )
    add("VAL4136_6_refusals", "refusal terms preserve parent, survivor, boundary, domain, flux and GK blockers", refusal_ok, "refusal tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4136_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in [
            "NORMAL_FORM_ADOPTION_ATTEMPTED",
            "COMPATIBLE_BUT_NOT_PARENT_ADOPTED",
            "COEFFICIENT_EXTRACTOR_EMITTED",
            "GK_QLOC_SELECTED_AS_NEXT_SPECIAL_TARGET",
            "NO_LOCAL_GR_CLAIM",
        ]
    )
    add("VAL4136_7_decisions", "decision gates record attempted adoption, fallback, GK next target and no-claim", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4136_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("normal_form_adoption_attempted") == "True"
        and status[0].get("Z_local_normal_form") == "False"
        and status[0].get("coefficient_extractor_emitted") == "True"
        and status[0].get("GK_q_loc_special_refusal") == "True"
    )
    add("VAL4136_8_status", "status records attempted adoption, false normal form, emitted extractor and GK refusal", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4136_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4137-Y5-R2FR-GK-q-loc-special-action-or-profile-bound.md"
    add("VAL4136_9_next_target", "next target is GK/q_loc special action or profile bound", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4136_10_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4136*")) or any(FORMALIZATION.rglob("4136-Y5-R2FR*"))
    add(
        "VAL4136_11_scope",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        in_scope and not formalization_output and not formalization_touched,
        f"doc={DOC_PATH}; csv_count={len(outputs)}",
    )

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4136_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4136_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
