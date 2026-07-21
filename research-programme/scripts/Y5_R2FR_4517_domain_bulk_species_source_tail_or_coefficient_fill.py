from __future__ import annotations

import csv
import io
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4517"
CLAIM_ID = "L-359"
MARKER = "PPC4161_DOMAIN_BULK_SPECIES_SOURCE_TAIL_OR_COEFFICIENT_FILL_4517"
PACKET_MARKER = "PPC4161_PACKET_DOMAIN_BULK_SPECIES_SOURCE_TAIL_OR_COEFFICIENT_FILL_4517"
DECISION = "DOMAIN_PROJECTOR_DOUBLE_ZERO_NOFLUX_THEOREM_DERIVED_CONDITIONALLY_BULK_SPECIES_ROWS_STAGED_NONCLAIM"
NEXT_TARGET = "4518-Y5-R2FR-domain-R11-silence-or-bulk-range-alpha-curve.md"

FORMAL_PATH = FORMAL / "533-PPC4161-domain-bulk-species-source-tail-or-coefficient-fill.md"
DOC_PATH = POST / "4517-Y5-R2FR-domain-bulk-species-source-tail-or-coefficient-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4517_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4517_SOURCE_REGISTER.csv"
DOMAIN_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4517_DOMAIN_PROJECTOR_DOUBLE_ZERO_NOFLUX_THEOREM.csv"
Y5_CLOSURE_MAP = SOURCE_DIR / "P8_Y5_R2FR_4517_Y5_UPDATED_CLOSURE_MAP.csv"
DOMAIN_COEFF_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4517_DOMAIN_PROJECTOR_COEFFICIENT_VECTOR.csv"
BULK_SPECIES_LEDGER = SOURCE_DIR / "P8_Y5_R2FR_4517_BULK_SPECIES_CALIBRATION_LEDGER.csv"
R11_GATE = SOURCE_DIR / "P8_Y5_R2FR_4517_R11_DOMAIN_SILENCE_GATE.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4517_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4517_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4517_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4517_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4517_DECISION.csv"

FORMAL_532 = FORMAL / "532-PPC4161-source-functor-parent-signature-or-first-Y5-coefficient-fill.md"
POST_4516 = POST / "4516-Y5-R2FR-source-functor-parent-signature-or-first-Y5-coefficient-fill.md"
THEOREM_4516 = SOURCE_DIR / "P8_Y5_R2FR_4516_STATIONARY_HILBERT_SOURCE_SUBTHEOREM.csv"
Y5_4516 = SOURCE_DIR / "P8_Y5_R2FR_4516_Y5_PARTIAL_CLOSURE_MAP.csv"
DEBT_4516 = SOURCE_DIR / "P8_Y5_R2FR_4516_REMAINING_SOURCE_DEBT.csv"
JZ_1354 = SOURCE_DIR / "P8_Y5_R10_1354_Y5Y6_JZ_COEFFICIENT_FILL.csv"
DOMAIN_CLAUSE = SOURCE_DIR / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv"
DOMAIN_VARIATION = SOURCE_DIR / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv"
DOMAIN_GATE = SOURCE_DIR / "P8_DOMAIN_SELECTOR_PARENT_ACTION_GATE.csv"
DOMAIN_VECTOR = SOURCE_DIR / "P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv"
DOMAIN_NOVECTOR = SOURCE_DIR / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv"
DOMAIN_ALPHA3 = SOURCE_DIR / "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv"
DOUBLE_ZERO_R11 = SOURCE_DIR / "P8_DOUBLE_ZERO_R11_VARIATION_PROOF.csv"
SN_AUDIT = SOURCE_DIR / "P8_SOURCE_NORMALIZATION_CHANNEL_AUDIT.csv"
SN_FILL = SOURCE_DIR / "P8_SOURCE_NORMALIZATION_COEFFICIENT_FILL.csv"
BULK_FILL = SOURCE_DIR / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_YUKAWA_FILL_ROW.csv"
BULK_POSITIVE = SOURCE_DIR / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_POSITIVE_OPERATOR_ATTEMPT.csv"
BULK_MARKER = SOURCE_DIR / "P8_Y5_R2FR_4475_MARKER_BULK_COUPLING_ZERO_THEOREM.csv"
SPECIES = SOURCE_DIR / "P8_Y5_R2FR_3637_SPECIES_BLIND_THEOREM.csv"
SPECIES_BOUND = SOURCE_DIR / "P8_species_source_charge_residual_or_zero.csv"
CALIBRATION = SOURCE_DIR / "P8_Y5_R2FR_4206_CALIBRATION_THEOREM.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def csv_line(values: Sequence[object]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(values)
    return buffer.getvalue().strip("\r\n")


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4517_00_formal532", "4516 formal handoff", FORMAL_532, "PPC4161_SOURCE_FUNCTOR_PARENT_SIGNATURE_OR_FIRST_Y5_COEFFICIENT_FILL_4516", "stationary source subset handoff"),
        ("SRC4517_01_post4516", "4516 post handoff", POST_4516, "NT4516_0", "declares domain/bulk/species target"),
        ("SRC4517_02_theorem4516", "4516 stationary theorem", THEOREM_4516, "SHS4516_3_mass_flux_surface_lock", "no-flux mass flux lock"),
        ("SRC4517_03_y5_4516", "4516 Y5 closure map", Y5_4516, "JZ1354_Y5_2_domain_projector_mass", "domain row live before 4517"),
        ("SRC4517_04_debt4516", "4516 remaining source debt", DEBT_4516, "RSD4516_0_domain_projector", "domain source debt"),
        ("SRC4517_05_jz1354", "1354 raw Y5 rows", JZ_1354, "JZ1354_Y5_2_domain_projector_mass", "domain source-normalization row"),
        ("SRC4517_06_domain_clause", "domain parent action clause", DOMAIN_CLAUSE, "C3_double_zero_memory", "double-zero selector clause"),
        ("SRC4517_07_domain_variation", "domain variation chain", DOMAIN_VARIATION, "V3_Ward_force", "on-shell domain force identity"),
        ("SRC4517_08_domain_gate", "domain parent action gate", DOMAIN_GATE, "G4_R11_silence", "R11 silence remains blocker"),
        ("SRC4517_09_domain_vector", "domain coefficient vector", DOMAIN_VECTOR, "R11_EH_operator_ledger", "domain R5/R6/R7/R8/R11 vector"),
        ("SRC4517_10_domain_novector", "domain no-vector theorem", DOMAIN_NOVECTOR, "T6_no_vector_verdict", "no-vector verdict"),
        ("SRC4517_11_domain_alpha3", "domain alpha3 no-leak", DOMAIN_ALPHA3, "N7_no_leak_verdict", "alpha3 no-leak verdict"),
        ("SRC4517_12_double_zero_r11", "double-zero R11 variation proof", DOUBLE_ZERO_R11, "V2_R11_variation", "R11 double-zero silence if factorized"),
        ("SRC4517_13_sn_audit", "source normalization audit", SN_AUDIT, "C1_domain_projector", "domain source-normalization channel"),
        ("SRC4517_14_sn_fill", "source normalization fill", SN_FILL, "F0_c_domain_source_normalization_operator", "F0 domain coefficient fill"),
        ("SRC4517_15_bulk_fill", "bulk/range fill row", BULK_FILL, "FB557_0_bulk_memory_range_zero_or_Yukawa_bound", "bulk/range fill route"),
        ("SRC4517_16_bulk_positive", "bulk positive operator attempt", BULK_POSITIVE, "BMR557_7_verdict", "bulk no-hair current verdict"),
        ("SRC4517_17_bulk_marker", "bulk marker theorem", BULK_MARKER, "LMB4475_7_verdict", "marker coupling zero theorem"),
        ("SRC4517_18_species", "species blind theorem", SPECIES, "SBT3637_4_live_verdict", "species theorem live verdict"),
        ("SRC4517_19_species_bound", "species source charge bound", SPECIES_BOUND, "SSC2675_1_conditional_zero", "species residual/bound row"),
        ("SRC4517_20_calibration", "calibration theorem", CALIBRATION, "GT4206_3_numeric_G_firewall", "calibration firewall"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def domain_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "DPN4517_0_variation_split",
            "object": "domain/projector source tail",
            "statement": "The domain/projector contribution to source-normalization splits into selector bulk stress, domain flux, projector operator and boundary/reference pieces.",
            "formula": "j_Z_domain = j_chi + j_flux + j_P + j_boundary + j_R11",
            "zero_route": "chi=lambda_D=0; F_domain=0; delta_g P_D=0; boundary source charge=0; c_domain_R11=0",
            "fallback_bound": "|j_Z_domain| <= |j_chi|+|j_flux|+|j_P|+|j_boundary|+|j_R11|",
            "status": "DECOMPOSITION_DERIVED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DPN4517_1_double_zero_selector",
            "object": "selector bulk stress",
            "statement": "A parent-owned quadratic selector/memory activation gives a double zero: if the local branch has Y_loc=0 or chi_D=0, then both the selector value and its first variation vanish.",
            "formula": "Sigma_loc=G_AB Y^A Y^B; Y_loc=0 => Sigma_loc=delta Sigma_loc=0; S_mem,D=chi_D^2 L_mem,D => delta S_mem,D=0 at chi_D=0",
            "zero_route": "parent owns the quadratic factorization and local zero branch",
            "fallback_bound": "retain |j_chi| if selector is linear, kinetic, external, or not parent-owned",
            "status": "EXACT_CONDITIONAL_DOUBLE_ZERO",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DPN4517_2_no_flux_domain",
            "object": "domain flux",
            "statement": "4516's stationary Hilbert collar kills domain mass flux only when the domain representative is comoving/q-basic and no wall flux crosses the same worldtube.",
            "formula": "D Pi_D=0 and nabla.(Pi_D J_M)=0 and int_wall n.Pi_D J_M=0 => j_flux=0",
            "zero_route": "q-basic fixed domain projector plus stationary no-flux local collar",
            "fallback_bound": "retain |j_flux| as alpha3/preferred-frame/source-normalization channel",
            "status": "EXACT_CONDITIONAL_LOCAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DPN4517_3_topological_projector",
            "object": "projector metric stress",
            "statement": "A metric-independent topological/relative-chain projector has no local bulk metric variation, so it cannot supply a local source-normalization operator by itself.",
            "formula": "delta_g P_D|bulk=0 => j_P=0",
            "zero_route": "P_D is parent-owned, diffeomorphic and metric-free, not an after-solve Hodge/orthogonal filter",
            "fallback_bound": "retain |j_P| and R5/R6/R7/R8 coefficient products if P_D is metric/readout dependent",
            "status": "EXACT_CONDITIONAL_PROJECTOR_THEOREM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DPN4517_4_R11_silence",
            "object": "domain R11 source-normalization",
            "statement": "Double-zero also silences retained R11 domain operators only if every local operator is multiplied by the same parent-owned Sigma_loc factor.",
            "formula": "delta[Sigma_loc O_A]=Sigma_loc delta O_A + O_A delta Sigma_loc = 0 on Y_loc=0",
            "zero_route": "all domain R11 operators are Sigma_loc-factorized or an executable R11 vector scores them",
            "fallback_bound": "c_domain_source_normalization_operator remains live",
            "status": "CONDITIONAL_R11_ZERO_NOT_LIVE_SIGNED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DPN4517_5_domain_row_verdict",
            "object": "JZ1354_Y5_2_domain_projector_mass",
            "statement": "The domain/projector Y5 row is conditionally closed only in the combined double-zero/no-flux/topological/R11-silent branch.",
            "formula": "DPN4517_1+DPN4517_2+DPN4517_3+DPN4517_4 and boundary source charge=0 => j_Z_domain_projector=0",
            "zero_route": "same-branch parent signatures for all clauses",
            "fallback_bound": "|j_Z_domain_projector| <= |j_chi|+|j_flux|+|j_P|+|j_boundary|+|j_R11|",
            "status": "CONDITIONAL_LOCAL_ZERO_VECTOR_READY",
            "valid_for_claim": False,
        },
    ]


def y5_updated_rows() -> List[Dict[str, object]]:
    status_map = {
        "JZ1354_Y5_0_radial_Meff_hair": ("CONDITIONAL_LOCAL_STATIONARY_ZERO", "4516 Hilbert stationary collar"),
        "JZ1354_Y5_2_domain_projector_mass": ("CONDITIONAL_DOMAIN_DOUBLE_ZERO_NOFLUX_ZERO", "4517 DPN4517_1-4 combined branch"),
        "JZ1354_Y5_6_time_drift": ("CONDITIONAL_LOCAL_STATIONARY_ZERO", "4516 Hilbert stationary collar"),
    }
    rows: List[Dict[str, object]] = []
    for source in read_csv(JZ_1354):
        if source.get("sector") != "Y5_source_normalization":
            continue
        new_status, route = status_map.get(
            source["coefficient_id"],
            ("REMAINS_LIVE", "not closed by 4516 stationary or 4517 domain theorem"),
        )
        rows.append(
            {
                "coefficient_id": source["coefficient_id"],
                "symbol": source["symbol"],
                "meaning": source["meaning"],
                "updated_status": new_status,
                "route_or_reason": route,
                "finite_fallback": source["source_requirement"],
                "observable_link": source["observable_link"],
                "accepted_for_scoring": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def domain_coeff_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source in read_csv(DOMAIN_VECTOR):
        rows.append(
            {
                "target_row": source.get("target_row"),
                "observable": source.get("observable"),
                "coefficient_symbol": source.get("coefficient_symbol"),
                "map": source.get("map"),
                "4517_zero_condition": "domain double-zero + no-flux + topological projector + R11 silence in same parent branch",
                "fallback": source.get("value_or_theorem"),
                "target_bound": source.get("target_bound"),
                "score_status": "conditional_not_scoreable",
                "valid_for_claim": False,
            }
        )
    return rows


def bulk_species_rows() -> List[Dict[str, object]]:
    return [
        {
            "ledger_id": "BSL4517_0_bulk_range",
            "component": "Y5_3 bulk X/Yukawa",
            "current_theorem": "positive operator/no-source/no-boundary-flux route exists only as a conditional template",
            "why_not_closed": "mass gap alone gives lambda_X, not alpha_X; source/test charge and measured-G normalization still set the force amplitude",
            "finite_route": "R10_alpha_lambda_curve_MTS_source_normalization.csv or sourced theorem-zero certificate",
            "next_action": "either prove Q_X=q_test=boundary_flux=0 or build executable alpha(lambda) curve",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "BSL4517_1_nonEH",
            "component": "Y5_4 non-EH source operator",
            "current_theorem": "marker/nonEH operator zero if absent from parent action grammar and no auxiliary/boundary route exists",
            "why_not_closed": "full action inventory and hidden auxiliary/boundary firewall are not parent-signed",
            "finite_route": "R11_nonEH_operator_vector_executable.csv with units/maps or action-grammar absence theorem",
            "next_action": "use the R11 gate before any local-GR promotion",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "BSL4517_2_species",
            "component": "Y5_5 species/material source charge",
            "current_theorem": "species-blind source functor implies Delta beta_X_AB=0 and eta_source_AB=0",
            "why_not_closed": "species labels/source prefactors are not yet excluded from parent source grammar; common-mode charge can still source R10/source normalization",
            "finite_route": "P8_species_source_charge_residual_or_zero.csv / epsilon_A vector with no bound inversion",
            "next_action": "derive source-label forgetting or fill species charge vector",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "BSL4517_3_boundary",
            "component": "Y5_1 boundary/source-reference shift",
            "current_theorem": "no local wall flux helps but does not equal boundary source-reference neutrality",
            "why_not_closed": "source-functional boundary charge/reference shift can survive as calibration data",
            "finite_route": "same-branch boundary source-charge theorem or finite boundary coefficient",
            "next_action": "tie boundary charge to topological/no-flux class or keep coefficient row",
            "valid_for_claim": False,
        },
        {
            "ledger_id": "BSL4517_4_calibration",
            "component": "Y5_7 absolute calibration",
            "current_theorem": "GR-equivalent structural calibration needs one constant universal kappa/G_N",
            "why_not_closed": "numeric G_N is not derived and absolute source calibration must be fixed before orbital readout",
            "finite_route": "parent-selected kappa/G calibration or explicit calibration offset row",
            "next_action": "use calibration theorem without demanding MTS derive numeric G_N",
            "valid_for_claim": False,
        },
    ]


def r11_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "R11D4517_0_factorized_operator_zero",
            "condition": "every domain source-normalization R11 operator is multiplied by Sigma_loc=G_AB Y^A Y^B",
            "mathematical_test": "delta[Sigma_loc O_A]=0 on Y_loc=0 for all retained O_A",
            "status": "CONDITIONAL_NOT_INVENTORIED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "R11D4517_1_executable_vector",
            "condition": "if any retained operator is not factorized, it has coefficient, units, map and source path",
            "mathematical_test": "R11_nonEH_operator_vector_executable.csv has claim-valid rows for domain_projector_mass",
            "status": "MISSING_EXECUTABLE_VECTOR",
            "valid_for_claim": False,
        },
        {
            "gate_id": "R11D4517_2_no_absorption",
            "condition": "domain R11 operator cannot be absorbed into fitted G or cancelled against another source tail",
            "mathematical_test": "componentwise absolute bound or parent Ward identity only",
            "status": "NO_CANCELLATION_GUARD",
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {"audit_id": "PA4517_0_domain_decomposition", "clause": "domain/source tail split", "status": "DERIVED", "reason": "selector, flux, projector, boundary and R11 pieces are separated", "valid_for_claim": False},
        {"audit_id": "PA4517_1_domain_zero", "clause": "domain/projector Y5 zero", "status": "CONDITIONAL_LOCAL_THEOREM", "reason": "requires same-branch double-zero, no-flux, topological projector and R11 silence", "valid_for_claim": False},
        {"audit_id": "PA4517_2_R11", "clause": "domain R11 silence", "status": "NOT_LIVE_SIGNED", "reason": "factorized inventory or executable vector missing", "valid_for_claim": False},
        {"audit_id": "PA4517_3_bulk_species", "clause": "bulk/range and species rows", "status": "STAGED_NOT_CLOSED", "reason": "both have conditional theorem routes but require alpha curve/source charges or parent source grammar", "valid_for_claim": False},
        {"audit_id": "PA4517_4_claim", "clause": "local GR/Newton/PPN/R10", "status": "NOT_CLAIMED", "reason": "conditional rows remain nonclaim and unscored", "valid_for_claim": False},
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {"gate_id": "CG4517_0_domain", "claim": "Y5_2 domain/projector source tail live-zero", "passed": False, "blocker": "R11 factorized inventory/executable vector and parent-owned projector signatures missing", "valid_for_claim": False},
        {"gate_id": "CG4517_1_all_Y5", "claim": "all Y5 rows vanish", "passed": False, "blocker": "boundary, bulk/range, nonEH, species and calibration rows remain live", "valid_for_claim": False},
        {"gate_id": "CG4517_2_R10", "claim": "R10/fifth-force source-normalization silence", "passed": False, "blocker": "bulk/range alpha(lambda) curve or theorem-zero certificate missing", "valid_for_claim": False},
        {"gate_id": "CG4517_3_local_GR", "claim": "local GR/Newton/PPN pass", "passed": False, "blocker": "source-normalization rows are conditional/nonclaim and R11 not silent", "valid_for_claim": False},
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "domain/projector source tail decomposition; double-zero/no-flux/topological/R11 conditional zero theorem; updated Y5 map with radial, time and domain rows conditionally closed",
            "not_derived": "live parent signatures for R11 silence, boundary source charge, bulk/range alpha curve, species label forgetting and absolute calibration",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": STAMP,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4517_0",
            "decision": DECISION,
            "because": "the domain projector row has enough existing variation machinery to become a conditional zero theorem, while bulk/range/species need source-backed rows or stronger parent grammar",
            "effect": "Y5 source-normalization is now narrowed to three conditional local closures plus five live rows, with R11/domain silence as the next hard gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4517_0",
            "target_file": NEXT_TARGET,
            "task": "try to close domain R11 silence by factorized operator inventory; if that fails, build the bulk/range alpha(lambda) source-normalization curve",
            "success_condition": "domain c_domain_source_normalization_operator is theorem-zero/executable, or bulk/range has a source-backed alpha(lambda) row",
            "avoid": "declaring the domain row closed without R11 silence or using mass gap alone as fifth-force zero",
            "valid_for_claim": False,
        }
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    csv_paths = [
        SOURCE_REGISTER,
        DOMAIN_THEOREM,
        Y5_CLOSURE_MAP,
        DOMAIN_COEFF_VECTOR,
        BULK_SPECIES_LEDGER,
        R11_GATE,
        PARENT_AUDIT,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    details = []
    parsed_ok = True
    for path in csv_paths:
        try:
            details.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:  # pragma: no cover
            parsed_ok = False
            details.append(f"{path.name}:FAIL:{exc}")
    sources_ok = all(row["exists"] and row["needle_found"] for row in all_rows["sources"])
    theorem_ok = any(row["theorem_id"] == "DPN4517_5_domain_row_verdict" for row in all_rows["theorem"])
    y5_domain_ok = any(row["coefficient_id"] == "JZ1354_Y5_2_domain_projector_mass" and row["updated_status"] == "CONDITIONAL_DOMAIN_DOUBLE_ZERO_NOFLUX_ZERO" for row in all_rows["y5"])
    domain_vector_ok = len(all_rows["domain_coeff"]) >= 5
    bulk_species_ok = len(all_rows["bulk_species"]) == 5
    r11_ok = any(row["gate_id"] == "R11D4517_1_executable_vector" for row in all_rows["r11"])
    gates_blocked = all(str(row.get("passed")) == "False" for row in all_rows["gates"])
    flags_false = True
    for rows in all_rows.values():
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "accepted_for_scoring"):
                if key in row and str(row[key]).lower() != "false":
                    flags_false = False
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks = [
        ("VAL4517_00_sources", sources_ok, "all source paths exist and source needles are found"),
        ("VAL4517_01_theorem", theorem_ok, "domain projector row verdict exists"),
        ("VAL4517_02_y5_domain", y5_domain_ok, "Y5 domain/projector row conditionally closed"),
        ("VAL4517_03_domain_vector", domain_vector_ok, "domain coefficient vector imported"),
        ("VAL4517_04_bulk_species", bulk_species_ok, "bulk/species/calibration ledger has five rows"),
        ("VAL4517_05_R11", r11_ok, "R11 domain silence gate recorded"),
        ("VAL4517_06_claims_blocked", gates_blocked, "all claim gates remain blocked"),
        ("VAL4517_07_nonclaim_flags", flags_false, "all claim/scoring flags remain false"),
        ("VAL4517_08_csv_parse", parsed_ok, ";".join(details)),
        ("VAL4517_09_next_target", all_rows["next"][0]["target_file"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4517_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
    ]
    rows = [
        {"validation_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL4517_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4517 domain/bulk/species source tail or coefficient fill",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    existing = text(CLAIMS_PATH)
    if CLAIM_ID in existing or MARKER in existing:
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr_newton_r2fr_domain_source_subset",
            "4517 derives the domain/projector source-tail decomposition and the combined conditional zero theorem: the Y5 domain/projector row vanishes only when the selector is parent-owned double-zero, the domain mass projector is q-basic/no-flux in the 4516 stationary collar, the projector is metric-free/topological, and all domain R11 source-normalization operators are Sigma_loc-factorized or executable. This conditionally closes the domain row in the local branch but keeps R11, boundary, bulk/range, species and calibration rows nonclaim.",
            "4517 source register, domain projector theorem, updated Y5 closure map, domain coefficient vector, bulk/species/calibration ledger, R11 gate, parent audit, claim gates, status and validation.",
            "private_domain_projector_conditional_zero_nonclaim",
            NEXT_TARGET,
            "claiming domain/source-normalization silence without R11 factorization, using mass gap alone as fifth-force zero, or upgrading conditional local closure to local GR.",
            "local_gr_newton_r2fr_domain_source_subset",
            str(FORMAL_PATH),
            NEXT_TARGET,
            "close domain R11 silence or build the bulk/range alpha(lambda) source-normalization curve.",
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    theorem: Sequence[Mapping[str, object]],
    y5: Sequence[Mapping[str, object]],
    domain_coeff: Sequence[Mapping[str, object]],
    bulk_species: Sequence[Mapping[str, object]],
    r11: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4517 - Domain/Bulk/Species Source Tail Or Coefficient Fill

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4517 makes the next real reduction in the source-normalization problem.

The domain/projector source tail is no longer a foggy row:

`j_Z_domain = j_chi + j_flux + j_P + j_boundary + j_R11`.

The exact conditional zero route is:

`chi=lambda_D=0; F_domain=0; delta_g P_D=0; boundary source charge=0; c_domain_R11=0 => j_Z_domain_projector=0`.

The new ingredient is the combined branch:

- double-zero selector: `Sigma_loc=G_AB Y^A Y^B; Y_loc=0 => Sigma_loc=delta Sigma_loc=0`;
- 4516 no-flux collar: `D Pi_D=0` and `nabla.(Pi_D J_M)=0` with no wall flux;
- topological projector: `delta_g P_D|bulk=0`;
- R11 silence: every retained domain operator is `Sigma_loc`-factorized or executable.

So `JZ1354_Y5_2_domain_projector_mass` is conditionally closed in the same local branch as the radial/time source closures. It is **not** claim-live because R11 factorization/executable rows and boundary source charge are still unsigned.

Bulk/range and species do not get fake wins here: mass gap alone is not fifth-force zero, and species-blind WEP only kills differential species charge, not common-mode source charge.

## Source Register

{table(sources)}

## Domain Projector Double-Zero No-Flux Theorem

{table(theorem)}

## Updated Y5 Closure Map

{table(y5)}

## Domain Projector Coefficient Vector

{table(domain_coeff)}

## Bulk / Species / Calibration Ledger

{table(bulk_species)}

## R11 Domain Silence Gate

{table(r11)}

## Parent Signature Audit

{table(parent)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Decision

{table(decisions)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def main() -> None:
    sources = source_rows()
    theorem = domain_theorem_rows()
    y5 = y5_updated_rows()
    domain_coeff = domain_coeff_rows()
    bulk_species = bulk_species_rows()
    r11 = r11_gate_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    decisions = decision_rows()
    next_target = next_rows()

    all_rows = {
        "sources": sources,
        "theorem": theorem,
        "y5": y5,
        "domain_coeff": domain_coeff,
        "bulk_species": bulk_species,
        "r11": r11,
        "parent": parent,
        "gates": gates,
        "status": status,
        "decisions": decisions,
        "next": next_target,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DOMAIN_THEOREM, theorem)
    write_csv(Y5_CLOSURE_MAP, y5)
    write_csv(DOMAIN_COEFF_VECTOR, domain_coeff)
    write_csv(BULK_SPECIES_LEDGER, bulk_species)
    write_csv(R11_GATE, r11)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, theorem, y5, domain_coeff, bulk_species, r11, parent, gates, status, decisions, next_target, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4517 Domain/Bulk/Species Source Tail Or Coefficient Fill

Marker: `{MARKER}`  
4517 derives the domain/projector source-tail decomposition `j_Z_domain=j_chi+j_flux+j_P+j_boundary+j_R11` and the exact conditional local zero route. With parent-owned double-zero selector, 4516 no-flux Hilbert collar, topological metric-free projector and factorized/executable R11 domain operators, the Y5 domain/projector source-normalization row is conditionally zero. The row is not promoted because R11 silence and boundary source charge are unsigned. Bulk/range, species and calibration remain staged with finite routes.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4517 Packet Integration

Marker: `{PACKET_MARKER}`  
The private packet now has three conditional Y5 source closures: radial hair, time drift and domain/projector mass. The next hard local gate is domain R11 silence, otherwise the work should pivot to a source-backed bulk/range `alpha(lambda)` curve.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
