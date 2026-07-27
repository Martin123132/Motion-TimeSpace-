from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from hidden_invariant_no_extension_gate import evaluate_import_rows, evaluate_no_extension_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
COEFF_DIR = POST / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"

CHECKPOINT = "4425"
CLAIM_ID = "L-266"
MARKER = "PPC4161_HIDDEN_INVARIANT_NO_EXTENSION_OR_LIVE_CPARENT_WEP_IMPORT_ROW_4425"
PACKET_MARKER = "PPC4161_PACKET_HIDDEN_INVARIANT_NO_EXTENSION_OR_LIVE_CPARENT_WEP_IMPORT_ROW_4425"
DECISION = "HIDDEN_INVARIANT_NO_EXTENSION_THEOREM_SHARPENED_CURRENTLY_BLOCKED_BY_SCALAR_MARKER_READOUT_REENTRY_NO_CPWEP_IMPORT"
NEXT_TARGET = "4426-Y5-R2FR-hidden-invariant-triviality-transitive-fibre-proof-or-first-finite-Csource-vector.md"

FORMAL_PATH = FORMAL / "441-PPC4161-hidden-invariant-no-extension-or-live-Cparent-WEP-import-row.md"
DOC_PATH = POST / "4425-Y5-R2FR-hidden-invariant-no-extension-or-live-Cparent-WEP-import-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4425_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4425_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4425_DERIVATION_ROWS.csv"
NO_EXTENSION_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4425_NO_EXTENSION_INPUT.csv"
NO_EXTENSION_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4425_NO_EXTENSION_OUTPUT.csv"
CPARENT_IMPORT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4425_CPARENT_WEP_IMPORT_INPUT.csv"
CPARENT_IMPORT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4425_CPARENT_WEP_IMPORT_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4425_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4425_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4425_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4425_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "hidden_invariant_no_extension_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4425_hidden_invariant_no_extension_or_live_Cparent_WEP_import_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4424 = SOURCE_DIR / "P8_Y5_R2FR_4424_NEXT_TARGET.csv"
FORMAL_440 = FORMAL / "440-PPC4161-parent-constructor-exhaustion-or-first-numeric-Pwep-coefficient.md"
DOC_1050 = POST / "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md"
DOC_1051 = POST / "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md"
DOC_1055 = POST / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md"
DOC_1058 = POST / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md"
DOC_980 = POST / "980-Y5-R10-no-marker-sector-functor-theorem-or-first-qbar-source-acquisition.md"
DOC_1220 = POST / "1220-Y5-R10-parent-typed-object-language-signature-or-finite-coupling-closure.md"
DOC_1235 = POST / "1235-Y5-R10-unique-F2-typed-coefficient-domain-or-QCD-color-edge-owner.md"

CSV_1051_NMM = SOURCE_DIR / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv"
CSV_1051_ISO = SOURCE_DIR / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv"
CSV_1055_PAC = SOURCE_DIR / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
CSV_1058_OP = SOURCE_DIR / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"
CSV_1058_READOUT = SOURCE_DIR / "P8_Y5_R10_1058_RADIATIVE_READOUT_CLOSURE_GATE.csv"
CSV_980_NMF = SOURCE_DIR / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv"
CSV_1220_PTOL = SOURCE_DIR / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv"
CSV_1235_TREQ = SOURCE_DIR / "P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv"
CDH_1480 = COEFF_DIR / "coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv"
ACTION_LINE_AUDIT = COEFF_DIR / "action_density_line_owner_audit_nonclaim_2679.csv"
C_SCHEMA = COEFF_DIR / "C_parent_import_schema.csv"
C_SLOT_TEMPLATE = COEFF_DIR / "C_parent_WEP_slot_import_TEMPLATE.csv"
C_SLOT_REFUSED = COEFF_DIR / "C_parent_WEP_slot_import_REFUSED_1447.csv"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4425_00_4424_next", "path": NEXT_4424, "needle": "4425-Y5-R2FR-hidden-invariant-no-extension-or-live-Cparent-WEP-import-row.md", "role": "4424 handoff."},
        {"source_id": "SRC4425_01_440_formal", "path": FORMAL_440, "needle": "hidden invariant scalars", "role": "current constructor-exhaustion obstruction."},
        {"source_id": "SRC4425_02_1050_doc", "path": DOC_1050, "needle": "Current verdict", "role": "visible-hidden product functor summary."},
        {"source_id": "SRC4425_03_1051_doc", "path": DOC_1051, "needle": "no-mixed-hidden-visible morphism", "role": "older no-mixed morphism checkpoint."},
        {"source_id": "SRC4425_04_1051_no_mixed", "path": CSV_1051_NMM, "needle": "NMM1051_2_scalar_counterexample", "role": "scalar invariant counterexample."},
        {"source_id": "SRC4425_05_1051_invariant_audit", "path": CSV_1051_ISO, "needle": "ISO1051", "role": "invariant scalar obstruction audit."},
        {"source_id": "SRC4425_06_980_no_marker", "path": CSV_980_NMF, "needle": "NMF980_2_scalar_obstruction_lemma", "role": "no-marker functor obstruction."},
        {"source_id": "SRC4425_07_1055_contract", "path": CSV_1055_PAC, "needle": "PAC1055_3_no_mixed_coefficients", "role": "parent action no-mixed coefficient contract."},
        {"source_id": "SRC4425_08_1058_operator", "path": CSV_1058_OP, "needle": "operator", "role": "visible operator-domain exhaustion attempt."},
        {"source_id": "SRC4425_09_1058_readout", "path": CSV_1058_READOUT, "needle": "readout", "role": "radiative/readout closure gate."},
        {"source_id": "SRC4425_10_1220_typed", "path": CSV_1220_PTOL, "needle": "PTOL1220_6_no_extension_no_marker", "role": "typed object-language signature attempt."},
        {"source_id": "SRC4425_11_1235_requirements", "path": CSV_1235_TREQ, "needle": "TREQ1235_2_no_extension_marker", "role": "no-extension marker requirement."},
        {"source_id": "SRC4425_12_1480_hom", "path": CDH_1480, "needle": "CDH1480_3_scalar_counterexample", "role": "coefficient-domain Hom exclusion obstruction."},
        {"source_id": "SRC4425_13_2679_action_line", "path": ACTION_LINE_AUDIT, "needle": "ADO2679_6_source_label_readout", "role": "source-label readout re-entry."},
        {"source_id": "SRC4425_14_import_schema", "path": C_SCHEMA, "needle": "value,float_or_DERIVED_ZERO", "role": "C_parent import schema."},
        {"source_id": "SRC4425_15_slot_template", "path": C_SLOT_TEMPLATE, "needle": "MISSING_DERIVED_ZERO_OR_NUMERIC_VALUE", "role": "live C_parent WEP template."},
        {"source_id": "SRC4425_16_slot_refused", "path": C_SLOT_REFUSED, "needle": "REFUSED_NO_SOURCE_SIGNED_FUNCTIONAL_DERIVATIVE", "role": "prior C_parent WEP import refusal."},
        {"source_id": "SRC4425_17_gate", "path": GATE_PATH, "needle": "def evaluate_no_extension_row", "role": "4425 hidden-invariant gate."},
        {"source_id": "SRC4425_18_generator", "path": GENERATOR_PATH, "needle": "HIDDEN_INVARIANT_NO_EXTENSION", "role": "4425 generator."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        content = text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": True if not needle else needle in content,
                "line_number": line_of(path, needle),
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {"derivation_id": "HNE4425_0_exact_target", "claim": "Hidden/readout re-entry can be reduced to a no-extension theorem.", "derivation": "For active source coefficients, require either O(C_hid)^inv = R or a parent typed-domain proof that hidden/material/readout markers have no argument slot in Coeff_active_source. Then Hom(C_hid, Coeff_active_source) is constant/absent.", "consequence": "This is the exact route from ParentGenerate_MTS to no source-only coupling.", "status": "TARGET_EXACT", "valid_for_claim": False},
        {"derivation_id": "HNE4425_1_trivial_invariant_route", "claim": "If O(C_hid)^inv = R, hidden scalar coefficient maps collapse to constants.", "derivation": "Any natural scalar c:C_hid -> R_+ factors through invariant scalars. If the invariant algebra is only constants, dc=0 and the relative source coefficient is common-mode.", "consequence": "This would kill hidden-to-source coefficient drift without fitting.", "status": "EXACT_CONDITIONAL_THEOREM", "valid_for_claim": False},
        {"derivation_id": "HNE4425_2_typed_no_extension_route", "claim": "If visible coefficient domains exclude hidden/readout markers, the scalar obstruction is typed out.", "derivation": "Even with a nonconstant hidden invariant I, c(I) O_source is illegal if Coeff_active_source has argument domain only in q_obs, fixed representation/topological data and universal constants.", "consequence": "This is the best fallback proof if invariant triviality is too strong.", "status": "EXACT_IF_PARENT_TYPED_DOMAIN_SIGNED", "valid_for_claim": False},
        {"derivation_id": "HNE4425_3_readout_survival", "claim": "Tree-level no-extension must survive EFT and physical readout.", "derivation": "S_bare factorization is insufficient unless S_eff, clocks, WEP projection, R10 projection and source normalization preserve the same coefficient domain.", "consequence": "No public zero claim can fire without radiative/readout closure.", "status": "REQUIRED_CLOSURE_THEOREM", "valid_for_claim": False},
        {"derivation_id": "HNE4425_4_current_failure", "claim": "Current corpus does not prove no-extension.", "derivation": "The scalar obstruction ledger still admits I_hid with dI != 0; typed domains and no-marker requirements exist as contracts; radiative/readout closure remains unsigned.", "consequence": "C_parent_WEP remains a live finite residual slot.", "status": "CURRENT_PROOF_BLOCKED_BY_SCALAR_MARKER_READOUT_REENTRY", "valid_for_claim": False},
        {"derivation_id": "HNE4425_5_import_rule", "claim": "A C_parent_WEP row can only move the finite branch if it is numeric or DERIVED_ZERO with a parent source.", "derivation": "Sensitivity components, comparator bounds and templates are not parent coefficients. The row needs value, units, sign, parent basis, functional derivative or zero certificate, and independence from the MICROSCOPE bound.", "consequence": "The finite route is kept honest and nonclaim unless a real parent coefficient appears.", "status": "STRICT_IMPORT_CONTRACT", "valid_for_claim": False},
    ]


def no_extension_input_rows() -> List[Dict[str, object]]:
    return [
        {"row_id": "HNE4425_0_chain_rule_baseline", "clause": "q-kernel verticality alone", "quotient_verticality_declared": True, "hidden_invariant_algebra_trivial": False, "no_extension_marker": False, "visible_coefficient_domain_excludes_hidden": False, "parent_action_domain_signed": False, "radiative_readout_closure": False, "source_label_forgetting": False, "source_path": str(FORMAL_440), "input_valid": False, "valid_for_claim": False, "notes": "Dq[v]=0 kills q-observables, not hidden coefficient maps by itself."},
        {"row_id": "HNE4425_1_trivial_hidden_algebra_route", "clause": "O(C_hid)^inv=R route", "quotient_verticality_declared": True, "hidden_invariant_algebra_trivial": True, "no_extension_marker": False, "visible_coefficient_domain_excludes_hidden": False, "parent_action_domain_signed": False, "radiative_readout_closure": False, "source_label_forgetting": True, "source_path": str(CSV_1051_NMM), "input_valid": False, "valid_for_claim": False, "notes": "Exact theorem if invariant triviality is parent-signed; readout closure still needed."},
        {"row_id": "HNE4425_2_scalar_counterexample_current", "clause": "surviving scalar obstruction", "quotient_verticality_declared": True, "hidden_invariant_algebra_trivial": False, "no_extension_marker": False, "visible_coefficient_domain_excludes_hidden": False, "parent_action_domain_signed": False, "radiative_readout_closure": False, "source_label_forgetting": False, "source_path": str(CSV_980_NMF), "input_valid": False, "valid_for_claim": False, "notes": "A nonconstant invariant scalar can feed c(I) O_source unless target is forbidden."},
        {"row_id": "HNE4425_3_typed_domain_route", "clause": "typed no-extension marker route", "quotient_verticality_declared": True, "hidden_invariant_algebra_trivial": False, "no_extension_marker": True, "visible_coefficient_domain_excludes_hidden": True, "parent_action_domain_signed": False, "radiative_readout_closure": False, "source_label_forgetting": True, "source_path": str(CSV_1220_PTOL), "input_valid": False, "valid_for_claim": False, "notes": "Typed-domain contract blocks hidden arguments only after parent action domain is signed."},
        {"row_id": "HNE4425_4_readout_reentry_guard", "clause": "tree-level no-extension readout survival", "quotient_verticality_declared": True, "hidden_invariant_algebra_trivial": False, "no_extension_marker": True, "visible_coefficient_domain_excludes_hidden": True, "parent_action_domain_signed": True, "radiative_readout_closure": False, "source_label_forgetting": True, "source_path": str(CSV_1058_READOUT), "input_valid": False, "valid_for_claim": False, "notes": "Even a signed tree-level typed domain must survive effective/readout transfer."},
        {"row_id": "HNE4425_5_future_no_extension_contract", "clause": "full future theorem contract", "quotient_verticality_declared": True, "hidden_invariant_algebra_trivial": True, "no_extension_marker": True, "visible_coefficient_domain_excludes_hidden": True, "parent_action_domain_signed": True, "radiative_readout_closure": True, "source_label_forgetting": True, "source_path": str(CSV_1235_TREQ), "input_valid": False, "valid_for_claim": False, "notes": "Executable target only; input_valid=false prevents a claim."},
    ]


def import_input_rows() -> List[Dict[str, object]]:
    return [
        {"row_id": "CPIMP4425_0_live_template", "coefficient": "C_parent_WEP_TiPt", "value": "MISSING_DERIVED_ZERO_OR_NUMERIC_VALUE", "units": "MISSING_PARENT_BASIS_UNITS", "parent_basis": "MISSING_PARENT_BASIS", "sign_convention": "MISSING_SIGN_CONVENTION", "source_path": str(C_SLOT_TEMPLATE), "zero_certificate_source": "MISSING_PARENT_ZERO_CERTIFICATE", "independent_of_bound": False, "input_valid": False, "valid_for_claim": False, "notes": "Template exists but no parent value."},
        {"row_id": "CPIMP4425_1_prior_refusal", "coefficient": "C_parent_WEP_TiPt", "value": "MISSING_REFUSED_NO_SOURCE_SIGNED_FUNCTIONAL_DERIVATIVE", "units": "MISSING_PARENT_BASIS_UNITS", "parent_basis": "MISSING_PARENT_BASIS", "sign_convention": "MISSING_SIGN_CONVENTION", "source_path": str(C_SLOT_REFUSED), "zero_certificate_source": "MISSING_PARENT_ZERO_CERTIFICATE", "independent_of_bound": False, "input_valid": False, "valid_for_claim": False, "notes": "Prior import correctly refused: no source-signed functional derivative."},
        {"row_id": "CPIMP4425_2_schema_only", "coefficient": "C_parent_WEP_TiPt", "value": "MISSING_VALUE_PER_SCHEMA", "units": "dimensionless_parent_WEP_basis_or_declared", "parent_basis": "MISSING_PARENT_BASIS", "sign_convention": "MISSING_SIGN_CONVENTION", "source_path": str(C_SCHEMA), "zero_certificate_source": "MISSING_PARENT_ZERO_CERTIFICATE", "independent_of_bound": False, "input_valid": False, "valid_for_claim": False, "notes": "Schema is useful but not evidence."},
        {"row_id": "CPIMP4425_3_live_import_contract", "coefficient": "C_parent_WEP_TiPt_or_C_i", "value": "MISSING_NUMERIC_OR_DERIVED_ZERO_PARENT_FUNCTIONAL_DERIVATIVE", "units": "explicit_parent_basis_required", "parent_basis": "MISSING_VARIATION_BASIS", "sign_convention": "MISSING_DELTA_ETA_SIGN", "source_path": str(ACTION_LINE_AUDIT), "zero_certificate_source": "MISSING_NO_EXTENSION_OR_FUNCTIONAL_ZERO_CERTIFICATE", "independent_of_bound": False, "input_valid": False, "valid_for_claim": False, "notes": "The only acceptable next finite row shape is now explicit."},
    ]


def claim_gate_rows(no_ext: Sequence[Mapping[str, str]], imports: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    rows = {row["row_id"]: row for row in no_ext}
    imp = {row["row_id"]: row for row in imports}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in no_ext) and not any(row.get("valid_for_claim") == "True" for row in imports)
    return [
        {"gate_id": "CG4425_0_trivial_route_exact", "claim": "O(C_hid)^inv=R would close hidden coefficient maps", "passed": rows["HNE4425_1_trivial_hidden_algebra_route"].get("current_status") == "TREE_LEVEL_SCALAR_ROUTE_READY_READOUT_REENTRY_OPEN", "valid_for_claim": False, "detail": "exact tree-level conditional; not parent-signed and readout is open."},
        {"gate_id": "CG4425_1_scalar_counterexample_live", "claim": "current hidden scalar counterexample remains live", "passed": rows["HNE4425_2_scalar_counterexample_current"].get("current_status") == "SCALAR_INVARIANT_EXTENSION_COUNTERMODEL_LIVE", "valid_for_claim": False, "detail": "one nonconstant invariant scalar can still feed a source coefficient."},
        {"gate_id": "CG4425_2_typed_route_unsigned", "claim": "typed no-extension route is conditional only", "passed": rows["HNE4425_3_typed_domain_route"].get("current_status") == "TYPED_DOMAIN_CONDITIONAL_NOT_PARENT_SIGNED", "valid_for_claim": False, "detail": "domain-exclusion contract exists but parent action domain is unsigned."},
        {"gate_id": "CG4425_3_full_contract_nonclaim", "claim": "future no-extension contract is executable but nonclaim", "passed": rows["HNE4425_5_future_no_extension_contract"].get("current_status") == "NO_EXTENSION_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "full theorem row is deliberately input_valid=false until parent-signed."},
        {"gate_id": "CG4425_4_no_cparent_import", "claim": "a real C_parent_WEP value or DERIVED_ZERO certificate is present", "passed": False, "valid_for_claim": False, "detail": "all import rows are template/refused/schema/contract only."},
        {"gate_id": "CG4425_5_imports_blocked", "claim": "C_parent import rows stay blocked", "passed": all(row.get("score_ready") == "False" for row in imp.values()), "valid_for_claim": False, "detail": "no numeric or DERIVED_ZERO parent coefficient is score-ready."},
        {"gate_id": "CG4425_6_no_claim_outputs", "claim": "4425 generated no claim-ready row", "passed": no_claims, "valid_for_claim": False, "detail": "checkpoint advances theorem contract and finite import rules only."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4425_0",
            "decision": DECISION,
            "summary": "4425 tries the no-extension proof directly. The mathematical route is now exact: hidden re-entry dies if either the hidden invariant algebra is trivial, or a parent typed-domain/no-marker theorem forbids hidden/material/readout arguments in active source coefficients, and the result survives EFT/readout. Current MTS has not signed those premises. The scalar-invariant counterexample, no-extension marker requirement, source-label/readout re-entry and radiative closure remain live, so C_parent_WEP is retained as an explicit finite slot. No numeric or DERIVED_ZERO parent import row is present.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4425_0_best_result", "status": "NO_EXTENSION_THEOREM_CONTRACT_EXACT", "detail": "The proof target is now one of two exact routes: invariant triviality or typed no-extension.", "valid_for_claim": False},
        {"status_id": "STAT4425_1_open_proof", "status": "SCALAR_MARKER_READOUT_REENTRY_LIVE", "detail": "Current corpus still permits a nonconstant hidden invariant or a marker/readout extension.", "valid_for_claim": False},
        {"status_id": "STAT4425_2_finite_branch", "status": "CPARENT_WEP_IMPORT_CONTRACT_READY_NO_VALUE", "detail": "Finite branch accepts only numeric or DERIVED_ZERO parent coefficients; none are present.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4425_0",
            "target": NEXT_TARGET,
            "objective": "Try to prove hidden invariant triviality from the local quotient/vertical fibre geometry; if that fails, assemble a first finite source-coupling vector row rather than repeating template imports.",
            "derive_first": "show the hidden fibre is a transitive gauge/representative fibre with no nonconstant local invariant scalar, or prove the parent typed-domain no-extension theorem from MTS primitives.",
            "fallback": "fill one finite C_source/C_parent_WEP component with value, units, sign, parent variation basis, source path and independence from comparator bounds.",
            "avoid": "reusing sensitivity components as parent coefficients; counting no-extension as an axiom; claiming tree-level closure without EFT/readout survival.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], no_ext: Sequence[Mapping[str, str]], imports: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 441 PPC4161 hidden invariant no-extension or live C_parent WEP import row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4425 makes the hidden-coupling route sharper rather than circling it:

- The exact no-extension theorem is now written: kill hidden/source coefficient maps by proving `O(C_hid)^inv = R`, or by deriving a parent typed-domain/no-marker rule for `Coeff_active_source`.
- The scalar-invariant counterexample is also kept explicit: if any nonconstant `I_hid` survives, `c(I_hid) O_source` remains legal unless the coefficient target is typed out.
- Tree-level no-extension is not enough; radiative/effective/readout maps must preserve the same coefficient domain.
- No `C_parent_WEP` numeric or `DERIVED_ZERO` row exists, so the finite branch stays live but nonclaim.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Hidden No-Extension Gate

{table(no_ext)}

## C_parent WEP Import Gate

{table(imports)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4425 - hidden invariant no-extension or live C_parent WEP import row

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Wrote the exact no-extension theorem as two routes: invariant-triviality or typed-domain/no-marker exclusion.
- Preserved the scalar-invariant counterexample instead of pretending quotient verticality alone kills it.
- Added a readout/EFT survival clause so a tree-level no-extension cannot be overclaimed.
- Rebuilt the `C_parent_WEP` import route as a strict nonclaim contract: real numeric value or `DERIVED_ZERO` certificate only.

## Decision

{table(decision_rows())}

## Next target

{table(next_rows())}
"""


def upsert_marked_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    block = f"{start}\n{section.rstrip()}\n{end}\n"
    if start in existing and end in existing:
        before = existing.split(start)[0]
        after = existing.split(end, 1)[1].lstrip("\n")
        write_text(path, before + block + after)
    else:
        sep = "" if existing.endswith("\n") or not existing else "\n"
        write_text(path, existing + sep + block)


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    rows = [row for row in rows if row.get("claim_id") != CLAIM_ID]
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "4425 sharpens the hidden/readout no-extension theorem for source coupling. Hidden re-entry is killed only if O(C_hid)^inv=R or a parent typed-domain/no-marker rule excludes hidden/material/readout arguments from active source coefficients, and EFT/readout closure preserves that rule. Current MTS has not signed these clauses, and no numeric or DERIVED_ZERO C_parent_WEP import row exists.",
        "current_evidence": "4425 source register, derivation rows, no-extension output, C_parent WEP import output, claim gates, decision, status, next target and validation CSV.",
        "status": "hidden_no_extension_theorem_exact_scalar_marker_readout_reentry_live_no_cparent_import",
        "next_test": "Prove hidden invariant triviality from vertical fibre geometry, or fill a first finite source-coupling coefficient vector with real parent provenance.",
        "key_risk": "Counting quotient verticality as invariant triviality; treating typed no-extension as an axiom; claiming tree-level closure without readout/EFT survival.",
        "sector": "local_gr",
        "evidence": "4425 source register, derivation rows, no-extension output, C_parent WEP import output, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Prove hidden invariant triviality from vertical fibre geometry, or fill a first finite source-coupling coefficient vector with real parent provenance.",
        "risk": "Counting quotient verticality as invariant triviality; treating typed no-extension as an axiom; claiming tree-level closure without readout/EFT survival.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4425 local spine update: no-extension has two honest proof routes

4425 stops treating hidden re-entry as vague fog. The route is now exact: either prove the hidden fibre has trivial invariant algebra, `O(C_hid)^inv = R`, or prove a parent typed-domain/no-marker theorem saying hidden/material/readout markers are not arguments of active source coefficients. The scalar counterexample remains live, and tree-level syntax must survive EFT/readout. So no local-GR/Newton source-coupling claim fires yet, but the next leap is clearer: prove hidden-fibre transitivity/no scalar invariants, or fill a real finite source-coupling coefficient row.
"""
    packet_section = f"""## 4425 packet update: hidden re-entry door narrowed

`{PACKET_MARKER}`

Private packet result: the source-coupling loophole is now a precise door, not a hallway. If the hidden fibre has no nonconstant invariant scalar, or if parent typing forbids all hidden/readout extensions into source coefficients, `C_parent_WEP` can go to zero. If not, it must be carried as a finite coefficient with real provenance.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    no_ext = {row["row_id"]: row for row in rows_from(NO_EXTENSION_OUTPUT)}
    imports = {row["row_id"]: row for row in rows_from(CPARENT_IMPORT_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in no_ext.values()) and not any(row.get("valid_for_claim") == "True" for row in imports.values())
    checks = [
        ("VAL4425_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4425_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every source needle is present"),
        ("VAL4425_2_trivial_route_exact", no_ext["HNE4425_1_trivial_hidden_algebra_route"].get("current_status") == "TREE_LEVEL_SCALAR_ROUTE_READY_READOUT_REENTRY_OPEN", "trivial invariant algebra route is exact but readout-open"),
        ("VAL4425_3_scalar_counterexample_live", no_ext["HNE4425_2_scalar_counterexample_current"].get("current_status") == "SCALAR_INVARIANT_EXTENSION_COUNTERMODEL_LIVE", "scalar counterexample remains live"),
        ("VAL4425_4_typed_route_unsigned", no_ext["HNE4425_3_typed_domain_route"].get("current_status") == "TYPED_DOMAIN_CONDITIONAL_NOT_PARENT_SIGNED", "typed-domain route is unsigned"),
        ("VAL4425_5_future_contract_nonclaim", no_ext["HNE4425_5_future_no_extension_contract"].get("current_status") == "NO_EXTENSION_CONTRACT_READY_NONCLAIM", "future no-extension contract is executable nonclaim"),
        ("VAL4425_6_imports_not_score_ready", all(row.get("score_ready") == "False" for row in imports.values()), "no C_parent import row is score-ready"),
        ("VAL4425_7_no_claim_outputs", no_claims, "no generated row is claim-ready"),
        ("VAL4425_8_claim_gates_block", any(row["gate_id"] == "CG4425_6_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gates explicitly block public claim"),
        ("VAL4425_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-266"),
        ("VAL4425_10_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4425_11_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4425_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4425_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4425_14_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4425_15_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(NO_EXTENSION_INPUT, no_extension_input_rows())
    write_csv(CPARENT_IMPORT_INPUT, import_input_rows())
    write_csv(NO_EXTENSION_OUTPUT, evaluate_no_extension_rows(NO_EXTENSION_INPUT))
    write_csv(CPARENT_IMPORT_OUTPUT, evaluate_import_rows(CPARENT_IMPORT_INPUT))
    no_ext = rows_from(NO_EXTENSION_OUTPUT)
    imports = rows_from(CPARENT_IMPORT_OUTPUT)
    gates = claim_gate_rows(no_ext, imports)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), no_ext, imports, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
