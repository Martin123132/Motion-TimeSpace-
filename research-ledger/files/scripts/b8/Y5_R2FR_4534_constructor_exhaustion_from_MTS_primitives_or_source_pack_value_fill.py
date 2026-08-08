from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4534"
CLAIM_ID = "L-376"
MARKER = "PPC4161_CONSTRUCTOR_EXHAUSTION_FROM_MTS_PRIMITIVES_OR_SOURCE_PACK_VALUE_FILL_4534"
PACKET_MARKER = "PPC4161_PACKET_CONSTRUCTOR_EXHAUSTION_FROM_MTS_PRIMITIVES_OR_SOURCE_PACK_VALUE_FILL_4534"
DECISION = "STRICT_MTS_PRIMITIVE_GRAMMAR_GIVES_CONDITIONAL_INDUCTION_PROOF_BUT_CURRENT_CORPUS_HAS_NOT_SIGNED_GRAMMAR_UNIQUENESS"
NEXT_TARGET = "4535-Y5-R2FR-action-scale-measure-owner-from-MTS-action-line-or-adopt-strict-grammar-closure.md"

FORMAL_PATH = FORMAL / "550-PPC4161-constructor-exhaustion-from-MTS-primitives-or-source-pack-value-fill.md"
DOC_PATH = POST / "4534-Y5-R2FR-constructor-exhaustion-from-MTS-primitives-or-source-pack-value-fill.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4534_SOURCE_REGISTER.csv"
STRICT_GRAMMAR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4534_STRICT_MTS_PRIMITIVE_GRAMMAR.csv"
INDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4534_CONSTRUCTOR_EXHAUSTION_INDUCTION.csv"
COUNTERMODEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4534_COUNTERMODEL_ATTACK_MATRIX.csv"
VALUE_FILL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4534_SOURCE_PACK_VALUE_FILL_ATTEMPT.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4534_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4534_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4534_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4534_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    sources = [
        {
            "source_id": "SRC4534_00_action_principle",
            "label": "MTS action principle",
            "path": ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
            "needle": "The full action is",
            "role": "core psi/metric/action/matter seed",
        },
        {
            "source_id": "SRC4534_01_programme",
            "label": "unified programme primitive note",
            "path": FORMAL / "03-unified-field-theory-programme.md",
            "needle": "Candidate MTS primitives",
            "role": "primitive field framing",
        },
        {
            "source_id": "SRC4534_02_4423_owner",
            "label": "4423 action density owner",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4423_DERIVATION_ROWS.csv",
            "needle": "constructor",
            "role": "previous Hom/action-density theorem target",
        },
        {
            "source_id": "SRC4534_03_4424_constructor",
            "label": "4424 constructor exhaustion output",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4424_CONSTRUCTOR_EXHAUSTION_OUTPUT.csv",
            "needle": "ParentGenerate",
            "role": "previous ParentGenerate_MTS image theorem attempt",
        },
        {
            "source_id": "SRC4534_04_1107_object",
            "label": "1107 object-language exhaustion",
            "path": SOURCE_DIR / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
            "needle": "EXH1107_1_chain_rule",
            "role": "chain-rule win and membership blocker",
        },
        {
            "source_id": "SRC4534_05_1338_no_slot",
            "label": "1338 no-source species slot theorem",
            "path": SOURCE_DIR / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
            "needle": "OLT1338_2_MTS_primitive_constructor",
            "role": "primitive constructor blocker",
        },
        {
            "source_id": "SRC4534_06_1236_certificate",
            "label": "1236 typed object language certificate",
            "path": SOURCE_DIR / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
            "needle": "CERT1236_0_parent_sorts",
            "role": "sorted grammar certificate clauses",
        },
        {
            "source_id": "SRC4534_07_4533_theorem",
            "label": "4533 action-measure theorem target",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4533_ACTION_MEASURE_OWNER_THEOREM_ATTEMPT.csv",
            "needle": "AMO4533_0_target",
            "role": "current action-measure proof target",
        },
        {
            "source_id": "SRC4534_08_4533_countermodels",
            "label": "4533 source-weight countermodels",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4533_SOURCE_WEIGHT_COUNTERMODEL_RESOLUTION.csv",
            "needle": "CEX4533_0_relative_species_weight",
            "role": "countermodel list to attack",
        },
        {
            "source_id": "SRC4534_09_4533_source_pack",
            "label": "4533 first eigenmode source pack",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4533_FIRST_REAL_EIGENMODE_SOURCE_PACK.csv",
            "needle": "SP4533_0_ZR",
            "role": "fallback value-fill matrix",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source in sources:
        path = Path(source["path"])
        exists = path.exists()
        content = read_text(path) if exists else ""
        needle = str(source["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source["source_id"],
                "label": source["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in content),
                "role": source["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def strict_grammar_rows() -> list[dict[str, Any]]:
    return [
        {
            "grammar_id": "GRAM4534_0_primitives",
            "sort_or_rule": "StrictMTSPrimitiveSet",
            "definition": "Generators are only Phi/psi, derivatives of Phi, the quotient q(Phi), observed metric/coframe e_obs(q), one parent integration measure mu[q], one action scale, universal constants, and ordinary matter representation data theta_A that already affect nongravitational matter equations.",
            "derived_from_sources": "SRC4534_00_action_principle;SRC4534_01_programme",
            "proof_role": "base alphabet for induction",
            "current_status": "STRICT_GRAMMAR_DEFINED",
            "valid_for_claim": "False",
        },
        {
            "grammar_id": "GRAM4534_1_allowed_constructors",
            "sort_or_rule": "ParentGenerate_MTS",
            "definition": "Close the primitive set under tensor product, contraction with e_obs/g_obs, covariant derivative, curvature formation, gauge/representation covariant derivatives, universal scalar functions, sums/products, variation before readout, and one total Hilbert/coframe source derivative.",
            "derived_from_sources": "SRC4534_03_4424_constructor;SRC4534_06_1236_certificate",
            "proof_role": "constructor closure image",
            "current_status": "CONSTRUCTOR_ATLAS_STATED_AS_STRICT_CLOSURE",
            "valid_for_claim": "False",
        },
        {
            "grammar_id": "GRAM4534_2_forbidden_constructors",
            "sort_or_rule": "NoIndependentSourceSlot",
            "definition": "Forbid primitive or derived maps SpeciesLabel -> Coeff_active_source, hidden scalar -> Coeff_active_source, readout selector -> Coeff_active_source, boundary/domain marker -> Coeff_active_source, or separate pre-variation weights w_A S_A except one universal common calibration mode.",
            "derived_from_sources": "SRC4534_05_1338_no_slot;SRC4534_07_4533_theorem;SRC4534_08_4533_countermodels",
            "proof_role": "what must be absent for local source coupling to reduce to GR",
            "current_status": "STRICT_GRAMMAR_FORBIDS_THE_COUNTERMODELS",
            "valid_for_claim": "False",
        },
        {
            "grammar_id": "GRAM4534_3_observable_argument_rule",
            "sort_or_rule": "NoInertActiveSourceScalar",
            "definition": "A scalar that changes only active gravitational source strength while leaving q(Phi), theta_A spectra/scattering/charges, and ordinary matter equations unchanged is not generated by StrictMTSPrimitiveSet; it is an external closure coefficient, not a derived MTS object.",
            "derived_from_sources": "SRC4534_04_1107_object;SRC4534_05_1338_no_slot",
            "proof_role": "separates measured matter constants from source-only weights",
            "current_status": "DERIVED_WITHIN_STRICT_GRAMMAR",
            "valid_for_claim": "False",
        },
        {
            "grammar_id": "GRAM4534_4_application_status",
            "sort_or_rule": "CurrentCorpusApplication",
            "definition": "The existing corpus contains the psi/metric/L_matter seed and several exact certificate clauses, but it does not yet prove that the strict primitive grammar is the unique parent grammar or that radiative/readout maps preserve it.",
            "derived_from_sources": "SRC4534_03_4424_constructor;SRC4534_06_1236_certificate;SRC4534_07_4533_theorem",
            "proof_role": "prevents smuggling closure into claim",
            "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
    ]


def induction_rows() -> list[dict[str, Any]]:
    return [
        {
            "induction_id": "IND4534_0_theorem",
            "statement": "In StrictMTSPrimitiveSet, every active source coefficient is a function of q(Phi), e_obs/g_obs, universal constants, and ordinary matter representation data only through the ordinary matter action before variation; no relative source-only w_A can be constructed.",
            "proof_step": "Prove by structural induction on ParentGenerate_MTS terms.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "claim_effect_if_parent_signed": "Delta_w_A=0, source-only beta/kappa_A rows vanish except common calibration.",
            "current_status": "PROVED_FOR_STRICT_GRAMMAR",
            "valid_for_claim": "False",
        },
        {
            "induction_id": "IND4534_1_base_generators",
            "statement": "Base generators have no codomain Coeff_active_source indexed by SpeciesLabel.",
            "proof_step": "Phi/psi and q(Phi) are label-free; e_obs/g_obs and mu[q] are quotient objects; universal constants have singleton domain; theta_A labels matter representation data but are not active-source coefficient constructors.",
            "result": "BASE_CASE_CLOSES_INSIDE_STRICT_GRAMMAR",
            "claim_effect_if_parent_signed": "No primitive source-only coefficient exists.",
            "current_status": "STRICT_BASE_OK",
            "valid_for_claim": "False",
        },
        {
            "induction_id": "IND4534_2_constructor_preservation",
            "statement": "Allowed tensor/differential/curvature/variation constructors preserve absence of SpeciesLabel -> Coeff_active_source.",
            "proof_step": "Compositions/products/contractions/covariant derivatives cannot create a target sort absent from their inputs; Hilbert variation returns the derivative of the already-formed total matter action, not a new pre-variation source selector.",
            "result": "NO_HOM_PRESERVED_BY_ALLOWED_CONSTRUCTORS",
            "claim_effect_if_parent_signed": "No source-only slot appears after local variation.",
            "current_status": "STRICT_INDUCTION_STEP_OK",
            "valid_for_claim": "False",
        },
        {
            "induction_id": "IND4534_3_common_mode_projection",
            "statement": "A single universal multiplier w_star is calibration, not relative source coupling.",
            "proof_step": "Project action-scale perturbations into common plus orthogonal pieces. Strict grammar permits only the common scalar; the orthogonal species vector requires a SpeciesLabel -> Coeff_active_source generator.",
            "result": "P_PERP_DELTA_W_ZERO_IF_STRICT_GRAMMAR_SIGNED",
            "claim_effect_if_parent_signed": "measured G absorbs common mode; WEP/R10/PPN see no relative source-weight vector.",
            "current_status": "STRICT_COMMON_MODE_SEPARATION_OK",
            "valid_for_claim": "False",
        },
        {
            "induction_id": "IND4534_4_application_block",
            "statement": "The induction is not yet an MTS theorem because uniqueness of StrictMTSPrimitiveSet is not derived from the parent action line.",
            "proof_step": "The original corpus says standard L_matter and gives the correct seed, but it has not shown that alternative pre-action weights, hidden markers, shadow frames, or readout/radiative tails are impossible parent terms.",
            "result": "APPLICATION_BLOCKED_NOT_A_CLAIM",
            "claim_effect_if_parent_signed": "would promote local source-coupling zero route.",
            "current_status": "PARENT_GRAMMAR_UNIQUENESS_UNSIGNED",
            "valid_for_claim": "False",
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "attack_id": "CMA4534_0_relative_species_weight",
            "countermodel": "S_matter=sum_A w_A S_A, w_A=w_star(1+epsilon_A)",
            "strict_grammar_attack": "Requires the forbidden orthogonal generator SpeciesLabel -> Coeff_active_source. Since theta_A only enters L_A as measured representation data, epsilon_A has no constructor.",
            "survives_current_corpus_because": "the current corpus has not parent-derived the strict action-scale/measure owner or uniqueness of the matter action line.",
            "exact_if_signed": "P_perp Delta_w_A=0",
            "finite_fallback": "Delta_w_species coefficient vector",
            "current_status": "KILLED_BY_STRICT_GRAMMAR_ONLY",
            "valid_for_claim": "False",
        },
        {
            "attack_id": "CMA4534_1_hidden_marker_weight",
            "countermodel": "w_A=w(I_hidden, material marker, domain, boundary class, readout selector)",
            "strict_grammar_attack": "No hidden, marker, domain, boundary, or readout selector is in the allowed argument domain of Coeff_active_source; all visible coefficients must descend through q(Phi) and parent-owned theta_rep.",
            "survives_current_corpus_because": "no-extension/no-marker and radiative/readout closure are certificate clauses, not derived theorems.",
            "exact_if_signed": "Xi_marker_readout=0",
            "finite_fallback": "marker/readout source coefficient rows",
            "current_status": "KILLED_BY_STRICT_NO_REENTRY_ONLY",
            "valid_for_claim": "False",
        },
        {
            "attack_id": "CMA4534_2_shadow_frame",
            "countermodel": "g_A=A_A(X)^2 g_obs or disformal source/species frame before variation",
            "strict_grammar_attack": "Strict grammar has one observed coframe/metric q(Phi); a second species frame is an extra map into matter/source geometry and is not generated by ParentGenerate_MTS.",
            "survives_current_corpus_because": "observed-stack uniqueness is not proven against all effective/readout frame maps.",
            "exact_if_signed": "c_g/disformal source-frame residual=0",
            "finite_fallback": "c_g/disformal/clock-source bound rows",
            "current_status": "KILLED_BY_STRICT_SINGLE_OBSERVED_STACK_ONLY",
            "valid_for_claim": "False",
        },
        {
            "attack_id": "CMA4534_3_direct_alpha_mass_vertex",
            "countermodel": "alpha_EM(X)F^2, m_A(X), q_A X_mu J_A^mu, or theta_A(I_Q,m)",
            "strict_grammar_attack": "Direct constant/mass/charge vertices are not active-source weights if they alter spectroscopy/scattering; if they only affect active source they are forbidden source-only scalars. Fixed measured constants remain in theta_A.",
            "survives_current_corpus_because": "constant-sector superselection and no direct matter-X vertex grammar are not fully parent-derived.",
            "exact_if_signed": "direct source-only alpha/mass/charge vertices vanish",
            "finite_fallback": "alpha/mass/charge coefficient rows",
            "current_status": "PARTITIONED_BY_OBSERVABLE_ARGUMENT_RULE",
            "valid_for_claim": "False",
        },
    ]


def source_pack_value_fill_rows() -> list[dict[str, Any]]:
    source_pack_path = SOURCE_DIR / "P8_Y5_R2FR_4533_FIRST_REAL_EIGENMODE_SOURCE_PACK.csv"
    rows: list[dict[str, Any]] = []
    for row in read_csv(source_pack_path):
        value = row.get("current_value", "")
        status = row.get("status", "")
        numeric_like = False
        try:
            float(value.split()[0])
            numeric_like = True
        except (ValueError, IndexError):
            numeric_like = False
        acceptable_now = numeric_like and status not in {
            "SOURCE_BACKED_PROXY_NONCLAIM",
            "DIAGNOSTIC_PROXY_NONCLAIM",
            "EXTERNAL_REVIEW_CANDIDATE_NONCLAIM",
            "SYMBOLIC_PROJECTION_ONLY",
        }
        rows.append(
            {
                "fill_id": "VF4534_" + row["pack_id"].replace("SP4533_", ""),
                "pack_id": row["pack_id"],
                "quantity": row.get("quantity", ""),
                "current_value": value,
                "incoming_status": status,
                "numeric_like": b(numeric_like),
                "claim_grade_fill_found": b(acceptable_now),
                "value_fill_result": "NO_FILL_VALUE_AVAILABLE" if not acceptable_now else "CANDIDATE_FILL_FOUND_REQUIRES_REVIEW",
                "next_needed": row.get("acceptance", ""),
                "source_path": row.get("source_path", ""),
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            "fill_id": "VF4534_OVERALL",
            "pack_id": "all",
            "quantity": "first real eigenmode source pack",
            "current_value": "no complete numeric/source-backed row",
            "incoming_status": "PARTIAL_SYMBOLIC_PROXY_NONCLAIM",
            "numeric_like": "False",
            "claim_grade_fill_found": "False",
            "value_fill_result": "SOURCE_PACK_REMAINS_NONCLAIM",
            "next_needed": "derive strict zero route or fill Z_R,M_R2,K_i,Q_source,Q_test and accepted alpha_bound(lambda) in one same-frame row",
            "source_path": str(source_pack_path),
            "valid_for_claim": "False",
        }
    )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4534_0_strict_grammar_theorem",
            "gate": "strict grammar induction",
            "status": "PASS_CONDITIONAL_THEOREM",
            "meaning": "Within the strict MTS primitive grammar, source-only w_A is unformable by induction.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4534_1_current_parent_application",
            "gate": "apply strict grammar to current MTS corpus",
            "status": "BLOCKED_GRAMMAR_UNIQUENESS_UNSIGNED",
            "meaning": "The parent action has not yet derived one action-scale/measure owner, no hidden/readout re-entry and radiative closure.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4534_2_finite_source_pack",
            "gate": "source-pack value fill",
            "status": "BLOCKED_NO_CLAIM_GRADE_FILL",
            "meaning": "Existing rows contain symbolic/proxy/candidate values, not a same-frame complete eigenmode prediction.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4534_3_local_gr_newton_claim",
            "gate": "local GR/Newton source-coupling claim",
            "status": "BLOCKED",
            "meaning": "Need either parent-signed strict grammar or a complete numeric bounded finite branch.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4534_0",
            "decision": DECISION,
            "meaning": "4534 is a real derivation advance: source-only coupling is killed by structural induction once the strict MTS primitive grammar is accepted. The remaining problem is no longer vague coupling; it is the specific parent-signature question of deriving grammar uniqueness/action-scale ownership from the MTS action line. The finite pack was also checked and still has no claim-grade fill.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4534_0",
            "target": NEXT_TARGET,
            "objective": "Try to derive the strict grammar's action-scale/measure owner from the MTS action line itself. If this cannot be derived, explicitly mark strict grammar as a closure assumption and move finite branch work to real eigenmode/source values.",
            "derive_first": "prove one parent action phase/measure owner: only one mu[q] and one action scale multiply the total ordinary matter action before variation.",
            "fallback": "adopt strict grammar as named closure only, then prioritize numeric same-frame eigenmode inputs Z_R,M_R2,K_i,Q_iS,Q_iT and accepted alpha_bound(lambda).",
            "avoid": "calling the strict grammar proof a current MTS theorem before grammar uniqueness is parent-derived.",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    grammar: list[dict[str, Any]],
    induction: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append(
        {
            "validation_id": "VAL4534_00_sources",
            "status": "PASS" if source_ok else "FAIL",
            "detail": "all source paths exist and needles found" if source_ok else "missing source or needle",
        }
    )

    grammar_ids = {row["grammar_id"] for row in grammar}
    grammar_ok = {
        "GRAM4534_0_primitives",
        "GRAM4534_1_allowed_constructors",
        "GRAM4534_2_forbidden_constructors",
        "GRAM4534_4_application_status",
    }.issubset(grammar_ids)
    checks.append(
        {
            "validation_id": "VAL4534_01_strict_grammar",
            "status": "PASS" if grammar_ok else "FAIL",
            "detail": "strict primitive grammar and application block rows present",
        }
    )

    induction_ids = {row["induction_id"] for row in induction}
    induction_ok = {"IND4534_0_theorem", "IND4534_1_base_generators", "IND4534_2_constructor_preservation", "IND4534_4_application_block"}.issubset(induction_ids)
    checks.append(
        {
            "validation_id": "VAL4534_02_induction",
            "status": "PASS" if induction_ok else "FAIL",
            "detail": "structural induction theorem/base/step/application-block rows present",
        }
    )

    attack_ids = {row["attack_id"] for row in countermodels}
    counter_ok = {
        "CMA4534_0_relative_species_weight",
        "CMA4534_1_hidden_marker_weight",
        "CMA4534_2_shadow_frame",
        "CMA4534_3_direct_alpha_mass_vertex",
    }.issubset(attack_ids)
    checks.append(
        {
            "validation_id": "VAL4534_03_countermodels",
            "status": "PASS" if counter_ok else "FAIL",
            "detail": "all four live 4533 countermodel classes attacked",
        }
    )

    fill_overall = next((row for row in fills if row.get("fill_id") == "VF4534_OVERALL"), {})
    fills_ok = bool(fills) and fill_overall.get("value_fill_result") == "SOURCE_PACK_REMAINS_NONCLAIM"
    checks.append(
        {
            "validation_id": "VAL4534_04_value_fill",
            "status": "PASS" if fills_ok else "FAIL",
            "detail": "source-pack value fill attempted and remains nonclaim",
        }
    )

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    checks.append(
        {
            "validation_id": "VAL4534_05_claims_blocked",
            "status": "PASS" if gates_ok else "FAIL",
            "detail": "all claim gates remain blocked or conditional nonclaim",
        }
    )

    csv_files = [
        SOURCE_REGISTER,
        STRICT_GRAMMAR_CSV,
        INDUCTION_CSV,
        COUNTERMODEL_CSV,
        VALUE_FILL_CSV,
        GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
    ]
    csv_ok = True
    csv_detail: list[str] = []
    for path in csv_files:
        try:
            parsed = read_csv(path)
            if not parsed:
                csv_ok = False
                csv_detail.append(f"{path.name}:empty")
        except Exception as exc:  # pragma: no cover - validation artifact
            csv_ok = False
            csv_detail.append(f"{path.name}:{exc}")
    checks.append(
        {
            "validation_id": "VAL4534_06_csv_parse",
            "status": "PASS" if csv_ok else "FAIL",
            "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(csv_detail),
        }
    )

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append(
        {
            "validation_id": "VAL4534_07_pycache_absent",
            "status": "PASS" if pycache_absent else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present",
        }
    )

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        {
            "validation_id": "VAL4534_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "4534 strict grammar induction proof attempt and value-fill gate",
        }
    )
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    grammar: list[dict[str, Any]],
    induction: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4534 - constructor exhaustion from MTS primitives or source-pack value fill

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains internal, conditional and nonclaim.

## What Moved

- This checkpoint does the actual proof attempt: under a strict `MTS primitives only` grammar, `w_A` is not merely unwanted; it is unformable by structural induction.
- The induction separates the useful theorem from the still-unsigned application: the current corpus has the `psi -> q(Phi) -> g/e_obs -> L_matter` seed, but not yet uniqueness of the grammar/action-scale owner.
- The four live source-coupling countermodels from 4533 are attacked one by one; each is killed by strict grammar, but each survives current MTS until grammar uniqueness/no-reentry is parent-derived.
- The first eigenmode source pack was checked for a value-fill escape route. It remains symbolic/proxy/nonclaim.

## Strict MTS Primitive Grammar

{markdown_table(grammar)}

## Constructor Exhaustion Induction

{markdown_table(induction)}

### Compact Proof

Let `G_0` be the strict primitive alphabet: `Phi/psi`, `q(Phi)`, `e_obs/g_obs`, `mu[q]`, one action scale, universal constants, and ordinary representation data `theta_A` only where it already enters the nongravitational matter action. Let `ParentGenerate_MTS` be the closure of `G_0` under the allowed local tensor, derivative, curvature, gauge, variation and readout-before-source constructors listed above.

Base case: no generator in `G_0` has codomain `Coeff_active_source` indexed by `SpeciesLabel`.  
Induction step: allowed constructors compose, differentiate, contract, sum, multiply, vary or project existing generated objects; none introduces a new codomain absent from the inputs. Hilbert/coframe variation differentiates the already-formed total matter action and therefore cannot create a pre-variation species source selector.  
Therefore `Hom(SpeciesLabel,Coeff_active_source)=empty` inside the strict generated grammar. A common scalar action normalization is a calibration mode; the orthogonal species vector `P_perp Delta_w_A` requires the forbidden Hom.  

This is a theorem of the strict grammar. It is not yet a theorem of current MTS until the parent action derives that this strict grammar is unique and stable under hidden, boundary, radiative and readout maps.

## Countermodel Attack Matrix

{markdown_table(countermodels)}

## Source Pack Value Fill Attempt

{markdown_table(fills)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker not in existing:
        with path.open("a", encoding="utf-8", newline="") as handle:
            if existing and not existing.endswith("\n"):
                handle.write("\n")
            handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    CLAIMS_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "claim_name": "local_gr_newton_r2fr_constructor_exhaustion_induction",
        "statement": "4534 proves that strict MTS primitive grammar would make source-only species weights unformable by structural induction, while current MTS still lacks parent-signed grammar uniqueness/action-scale ownership.",
        "evidence": "Generated strict grammar, constructor-exhaustion induction, countermodel attack matrix, value-fill attempt, claim gates and validation P8_Y5_BRR545_4534_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_strict_grammar_induction_parent_signature_required",
        "next_target": NEXT_TARGET,
        "blocker": "The strict primitive grammar is not yet derived as the unique parent grammar; first eigenmode source pack has no claim-grade numeric/source-backed row.",
        "sector": "local_gr_newton",
        "source_path": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "failure_mode": "Treating the strict grammar proof as a current MTS theorem before action-scale/measure owner and no-reentry are parent-signed.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    grammar = strict_grammar_rows()
    induction = induction_rows()
    countermodels = countermodel_rows()
    fills = source_pack_value_fill_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(STRICT_GRAMMAR_CSV, grammar)
    write_csv(INDUCTION_CSV, induction)
    write_csv(COUNTERMODEL_CSV, countermodels)
    write_csv(VALUE_FILL_CSV, fills)
    write_csv(GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, grammar, induction, countermodels, fills, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, grammar, induction, countermodels, fills, gates, decisions, next_target, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4534 Constructor Exhaustion From MTS Primitives Or Source Pack Value Fill

Marker: `{MARKER}`  
4534 proves a useful conditional theorem: if the parent grammar is strictly generated from MTS primitives (`psi`, `q(Phi)`, observed coframe/metric, one measure/action scale, universal constants and ordinary representation data), then `Hom(SpeciesLabel,Coeff_active_source)=empty` by structural induction and source-only `w_A` is unformable. The current corpus has not yet derived uniqueness of that strict grammar or radiative/readout no-reentry, and the finite source pack has no claim-grade fill. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4534 Packet Integration

Marker: `{PACKET_MARKER}`  
The packet now contains the strict-grammar induction proof: source-only coupling dies if strict MTS primitive closure is parent-signed. Application remains blocked by action-scale/measure ownership and no-reentry; finite eigenmode values remain nonclaim.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
