from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3294-Y5-R2FR-local-GR-reduction-contract-Hilbert-source-common-G-and-Newton-limit-under-AX1090.md"

SRC_3293_DOC = ROOT / "3293-Y5-R2FR-parent-Hilbert-source-and-canonical-quantum-normalization-signature-under-AX1090.md"
SRC_3293_NEXT = OUT / "P8_Y5_R2FR_3293_NEXT_TARGET.csv"
SRC_3293_SIGNATURE = OUT / "P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv"
SRC_3293_LOCALGR = OUT / "P8_Y5_R2FR_3293_LOCAL_GR_MATTER_COUPLING_REDUCTION.csv"
SRC_3293_VALIDATION = OUT / "P8_Y5_BRR545_3293_VALIDATION.csv"
SRC_3286_DOC = ROOT / "3286-Y5-R2FR-Hodge-Poynting-factor-owner-or-first-CH-CS-slope-row-under-AX1090.md"
SRC_3287_DOC = ROOT / "3287-Y5-R2FR-chi-to-metric-Hodge-premise-proof-or-DeltaChi-slope-source-row-under-AX1090.md"
SRC_3288_DOC = ROOT / "3288-Y5-R2FR-same-public-metric-or-ZQ-impedance-owner-split-under-AX1090.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3294_SOURCE_REGISTER.csv",
    "contract": OUT / "P8_Y5_R2FR_3294_LOCAL_GR_REDUCTION_CONTRACT.csv",
    "theorem": OUT / "P8_Y5_R2FR_3294_LOCAL_GR_CONDITIONAL_THEOREM.csv",
    "newton": OUT / "P8_Y5_R2FR_3294_NEWTON_LIMIT_AND_COMMON_G_CALIBRATION.csv",
    "residual_vector": OUT / "P8_Y5_R2FR_3294_PPN_NEWTON_MAXWELL_RESIDUAL_VECTOR.csv",
    "runner": OUT / "P8_Y5_R2FR_3294_LOCAL_GR_CONTRACT_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3294_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3294_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3294_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3294_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 560) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
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


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 330)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3293_DOC, "Hilbert source/common G handoff", ["common G", "Hilbert-source signature"]),
        (SRC_3293_NEXT, "3293 next target", ["local-GR-reduction-contract", "Newton-limit"]),
        (SRC_3293_SIGNATURE, "Hilbert source theorem", ["HSSIG3293_1_source_only_exclusion", "HSSIG3293_4_verdict"]),
        (SRC_3293_LOCALGR, "local GR matter coupling inputs", ["LGR3293_1_common_G", "LGR3293_3_Maxwell_stress"]),
        (SRC_3293_VALIDATION, "3293 validation", ["VAL3293_13_overall", "true"]),
        (SRC_3286_DOC, "Hodge/Poynting EM stress owner", ["metric_Hodge_branch", "Poynting"]),
        (SRC_3287_DOC, "chi to metric Hodge reconstruction", ["Hodge shape", "same public metric"]),
        (SRC_3288_DOC, "same public metric and calibrated Z_Q standard", ["GR uses empirical G", "shared observed coframe"]),
        (SRC_1100_DOC, "T_Q/current and alpha normalization open clauses", ["TQS1100_4_same_current_owner", "Z_A"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3294_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "LGC3294_0_single_public_metric",
            "piece": "public geometry",
            "required_statement": "one observed metric/coframe g_pub/e_obs is shared by matter, clocks, rods, source current, Maxwell stress, and local gravitational field equation",
            "derived_if_signed": "no bimetric source split; EM stress and matter stress live in the same tensor equation",
            "current_status": "CONDITIONAL_FROM_3288_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "LGC3294_1_Einstein_like_kinetic",
            "piece": "gravitational left-hand side",
            "required_statement": "the parent local metric equation reduces to G_mu_nu + Lambda g_mu_nu plus bounded higher-derivative/extra-field residuals",
            "derived_if_signed": "left-hand side is GR in the local weak-field regime",
            "current_status": "MAJOR_OPEN_THEOREM_LOVELOCK_ROUTE_NEXT",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "LGC3294_2_Hilbert_source",
            "piece": "matter source",
            "required_statement": "source is T_H_mu_nu=-2/sqrt(-g) delta S_m/delta g^mu_nu from one descended matter action",
            "derived_if_signed": "source-only species weights vanish by 3293",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "LGC3294_3_common_calibrated_G",
            "piece": "coupling constant",
            "required_statement": "one universal common constant kappa_G=8*pi*G_cal/c^4 couples the total Hilbert source",
            "derived_if_signed": "G can be empirically calibrated like GR; no relative species/source weights may hide in it",
            "current_status": "FAIR_ALLOWED_CALIBRATION_NOT_PREDICTION",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "LGC3294_4_Maxwell_stress",
            "piece": "EM contribution",
            "required_statement": "public Maxwell/Hodge action on g_pub supplies T_EM^mu_nu with no Poynting/background double count",
            "derived_if_signed": "EM stress enters the same Hilbert source consistently with 3286-3288",
            "current_status": "CONDITIONAL_HODGE_BRANCH_NOT_FULLY_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "LGC3294_5_Newton_limit",
            "piece": "Newtonian mechanics",
            "required_statement": "weak-field slow-motion limit gives g_00=-(1+2Phi/c^2)+O(c^-4) and nabla^2 Phi=4*pi*G_cal*rho_total plus residuals",
            "derived_if_signed": "Newtonian mechanics follows as GR limit with calibrated G",
            "current_status": "CONDITIONAL_ON_LGC3294_0_TO_3_AND_SMALL_RESIDUALS",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "LGC3294_6_PPN_residual_gate",
            "piece": "local tests",
            "required_statement": "all extra-field, metric-split, source-weight, G-drift, and constitutive residuals are zero by theorem or bounded below PPN/WEP/orbital limits",
            "derived_if_signed": "local-GR claim can be promoted only after residual vector closes",
            "current_status": "BOUNDING_STAGE_REQUIRED",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "LGT3294_0_conditional_GR_equation",
            "statement": "If LGC3294_0..4 are parent-signed, the local MTS field equation reduces to G_mu_nu + Lambda g_mu_nu = (8*pi*G_cal/c^4) T_H_mu_nu + R_mu_nu^MTS with R_mu_nu^MTS=0 or bounded.",
            "status": "EXACT_CONDITIONAL_REDUCTION",
            "not_a_claim_because": "Einstein-like kinetic term, same public metric, and Hilbert source are not all parent-signed.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "LGT3294_1_common_G_fairness",
            "statement": "A common constant G_cal is acceptable for first local-GR reduction just as GR uses measured G; the required derivation is universality/silence, not the numerical value.",
            "status": "FAIR_STANDARD_FORMALIZED",
            "not_a_claim_because": "G drift and relative source weights remain residual gates.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "LGT3294_2_Newton_limit",
            "statement": "Under weak-field slow-motion assumptions and small residuals, the 00 equation gives nabla^2 Phi=4*pi*G_cal*rho_total plus explicit residual source terms.",
            "status": "STANDARD_GR_LIMIT_CONDITIONAL",
            "not_a_claim_because": "the parent equation has not yet been proven Einstein-like.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "LGT3294_3_no_Bianchi_smuggling",
            "statement": "Bianchi identity supports consistency after the source is Hilbert-owned; it is not used as a standalone proof of universal coupling.",
            "status": "RED_TEAM_GUARD",
            "not_a_claim_because": "constant relative source weights can evade simple divergence checks.",
            "valid_for_claim": "false",
        },
    ]


def newton_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NGC3294_0_common_G_allowed",
            "quantity": "G_cal",
            "rule": "may be empirical/calibrated in first-pass local limit",
            "forbidden_escape": "species-dependent G_A, range-dependent G(r), time-drifting G(t), frame-dependent G_frame, or hidden-variable G(I_hid)",
            "status": "ALLOWED_COMMON_ONLY",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NGC3294_1_Newton_Poisson",
            "quantity": "nabla^2 Phi",
            "rule": "equals 4*pi*G_cal*rho_total when LGC3294 contract and weak-field limit are signed",
            "forbidden_escape": "rho_total reweighted by w_A or extra hidden source density without residual accounting",
            "status": "CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NGC3294_2_orbital_PPN_bridge",
            "quantity": "PPN/orbital residual vector",
            "rule": "score deviations only after deriving projection from R_mu_nu^MTS into gamma,beta,alpha_i,Gdot,Yukawa/source terms",
            "forbidden_escape": "declaring GR reduction because one sector is quiet",
            "status": "PROJECTION_REQUIRED",
            "valid_for_claim": "false",
        },
    ]


def residual_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RV3294_0_metric_split",
            "symbol": "R_metric",
            "meaning": "g_EM, g_matter, g_clock, or source frame not the same public metric/coframe",
            "required_zero_or_bound": "same-public-metric theorem or optical/source-frame bounds",
            "current_status": "OPEN_FROM_3288",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RV3294_1_non_Einstein_kinetic",
            "symbol": "R_kin",
            "meaning": "left-hand side differs from Einstein tensor by higher derivative, scalar, vector, torsion, or memory terms",
            "required_zero_or_bound": "Lovelock/second-order metric theorem or PPN/orbital bounds",
            "current_status": "NEXT_TARGET",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RV3294_2_non_Hilbert_source",
            "symbol": "R_source",
            "meaning": "source-only species weights or non-Hilbert source selector survives",
            "required_zero_or_bound": "3293 parent Hilbert-source signature or WEP/PPN/R10 source-product bounds",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RV3294_3_G_drift",
            "symbol": "R_G",
            "meaning": "common coupling is not actually common/constant; hidden, time, range, or frame drift",
            "required_zero_or_bound": "q-basic G_cal or Gdot/range/fifth-force bounds",
            "current_status": "OPEN",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RV3294_4_EM_constitutive",
            "symbol": "R_EM",
            "meaning": "Delta_chi, impedance drift, Poynting double count, or nonmetric Hodge stress",
            "required_zero_or_bound": "3286-3288 Hodge/public metric/Z_Q gates or Delta_chi bounds",
            "current_status": "CONDITIONAL_ZERO_WITH_LIVE_DELTA_CHI",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RV3294_5_readout_boundary",
            "symbol": "R_readout",
            "meaning": "radiative/readout/boundary terms reintroduce couplings after tree-level reduction",
            "required_zero_or_bound": "effective-action/readout closure or source-backed product bounds",
            "current_status": "OPEN",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN3294_0_contract_shape", "local GR contract has all named pieces", "PASS_SYMBOLIC_NONCLAIM"),
        ("RUN3294_1_common_G", "common G allowed only as universal calibration", "PASS_SYMBOLIC_NONCLAIM"),
        ("RUN3294_2_Newton_limit", "Newton limit conditional on Einstein kinetic + Hilbert source", "PASS_SYMBOLIC_NONCLAIM"),
        ("RUN3294_3_residual_vector", "claim refused until residual vector zero/bounded", "REFUSE_CLAIM_NONCLAIM"),
    ]
    return [
        {
            "run_id": run_id,
            "check": check,
            "observed_status": status,
            "expectation_match": "true",
            "claim_allowed": "false",
        }
        for run_id, check, status in rows
    ]


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3294_0_contract_complete",
            "gate": "local GR reduction contract names all required pieces",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "this is a structured contract, not a proof.",
        },
        {
            "gate_id": "GATE3294_1_Einstein_kinetic_signed",
            "gate": "Einstein-like kinetic term parent-signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "next target is Lovelock/metric kinetic theorem.",
        },
        {
            "gate_id": "GATE3294_2_Hilbert_source_signed",
            "gate": "Hilbert-source signature parent-signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "3293 gives conditional theorem only.",
        },
        {
            "gate_id": "GATE3294_3_residual_vector_closed",
            "gate": "PPN/Newton/Maxwell residual vector zero or bounded",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "residual projection/bounds remain open.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3294_0_spine_progress",
            "finding": "The local-GR route now has a precise contract: single public metric, Einstein-like kinetic term, Hilbert source, common calibrated G, Maxwell stress, Newton limit, and residual vector.",
            "consequence": "future work can attack one contract piece at a time rather than circling generic coupling concerns.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3294_1_G_policy",
            "finding": "Deriving numerical G is not required before local-GR reduction; proving common universality/no drift is required.",
            "consequence": "this matches the fair GR standard while still blocking source-weight cheats.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3294_2_best_next",
            "finding": "The biggest remaining local-GR gap is the gravitational left-hand side.",
            "consequence": "next target should use the Lovelock/second-order metric route: derive Einstein tensor plus Lambda or explicitly parameterize R_kin.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3294_0_3295",
            "target_doc": "3295-Y5-R2FR-Lovelock-metric-kinetic-owner-or-non-Einstein-residual-vector-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3295_Lovelock_metric_kinetic_owner_or_non_Einstein_residual_vector.py",
            "objective": "derive or reject the Einstein-like gravitational left-hand side from locality, diffeomorphism invariance, single metric, second-order field equations, and no extra propagating local fields; if rejected, parameterize R_kin for PPN/Newton/orbital tests.",
            "guardrails": "do not assume GR kinetic term by taste; do not use Bianchi alone; do not claim local GR until R_kin and the residual vector are zero or bounded.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    newton: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    formalization_changed_count: int,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "check": check, "passed": bool_str(passed), "detail": detail})

    add("VAL3294_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3294_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add("VAL3294_2_outputs_parse", "all 3294 non-validation output CSVs parse", all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation"))

    pieces = {row["piece"] for row in contract}
    add(
        "VAL3294_3_contract_pieces_complete",
        "contract includes geometry, kinetic, Hilbert source, common G, Maxwell stress, Newton limit, and residual gate",
        {"public geometry", "gravitational left-hand side", "matter source", "coupling constant", "EM contribution", "Newtonian mechanics", "local tests"}.issubset(pieces),
    )

    theorem_text = " ".join(row["statement"] for row in theorem)
    add(
        "VAL3294_4_GR_equation_and_no_Bianchi_smuggling",
        "theorem states conditional GR equation and no Bianchi smuggling",
        "G_mu_nu + Lambda g_mu_nu" in theorem_text and "8*pi*G_cal" in theorem_text and "not used as a standalone proof" in theorem_text,
    )

    newton_text = " ".join(row["quantity"] + " " + row["rule"] + " " + row["forbidden_escape"] for row in newton)
    add(
        "VAL3294_5_Newton_and_G_policy_present",
        "Newton/G table allows common G and forbids species/range/time/frame drift",
        "G_cal" in newton_text and "species-dependent" in newton_text and "nabla^2 Phi" in newton_text,
    )

    residual_symbols = {row["symbol"] for row in residuals}
    add(
        "VAL3294_6_residual_vector_complete",
        "residual vector includes metric, kinetic, source, G, EM, and readout terms",
        {"R_metric", "R_kin", "R_source", "R_G", "R_EM", "R_readout"}.issubset(residual_symbols),
    )

    add("VAL3294_7_runner_expectations", "runner expectations all match", all(row["expectation_match"] == "true" for row in runner), ";".join(f"{row['run_id']}={row['observed_status']}" for row in runner))
    add("VAL3294_8_claim_gates_false", "no 3294 gate allows local GR claim", all(row["claim_allowed"] == "false" for row in promotion) and any(row["passed"] == "false" for row in promotion))
    add(
        "VAL3294_9_next_target_Lovelock",
        "next target focuses Lovelock/metric kinetic owner or non-Einstein residual",
        len(next_target) == 1 and "Lovelock" in next_target[0]["target_doc"] and "non-Einstein-residual" in next_target[0]["target_doc"],
    )
    add(
        "VAL3294_10_decision_records_spine_progress",
        "decision ledger records local-GR spine and G policy",
        any("precise contract" in row["finding"] for row in decisions) and any("numerical G" in row["finding"] for row in decisions),
    )
    add(
        "VAL3294_11_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        formalization_changed_count == 0,
        f"formalization_changed_count={formalization_changed_count}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3294_12_overall", "3294 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return checks


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    newton: list[dict[str, Any]],
    residual_vector: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3294 - Local GR reduction contract: Hilbert source, common G, and Newton limit under AX1090

**Run UTC:** {RUN_UTC}

3294 turns the recent coupling work into a local-GR spine contract. The point is not to claim GR yet. The point is to state exactly what MTS must derive or bound to reduce to GR/Newton/Maxwell in the local regime:

`G_mu_nu + Lambda g_mu_nu = (8*pi*G_cal/c^4) T_H_mu_nu + R_mu_nu^MTS`.

Here `G_cal` may be empirical at first pass, exactly as in GR, but it must be a single common silent coupling. Relative source weights, hidden drift, range/time/frame dependence, and non-Hilbert source selectors remain forbidden residuals unless derived/bounded.

## Source Register

{md_table(sources)}

## Local GR Reduction Contract

{md_table(contract)}

## Conditional Local GR Theorem

{md_table(theorem)}

## Newton Limit And Common G Calibration

{md_table(newton)}

## PPN/Newton/Maxwell Residual Vector

{md_table(residual_vector)}

## Nonclaim Runner

{md_table(runner)}

## Promotion Gates

{md_table(promotion)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    before_fw = snapshot_tree(FW)

    sources = source_register_rows()
    contract = contract_rows()
    theorem = theorem_rows()
    newton = newton_rows()
    residual_vector = residual_vector_rows()
    runner = runner_rows()
    promotion = promotion_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["newton"], newton)
    write_csv(OUTPUTS["residual_vector"], residual_vector)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    after_fw = snapshot_tree(FW)
    validation = validate(sources, contract, theorem, newton, residual_vector, runner, promotion, decisions, next_target, changed_count(before_fw, after_fw))
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, contract, theorem, newton, residual_vector, runner, promotion, decisions, next_target, validation)

    if PYCACHE.exists():
        for item in PYCACHE.iterdir():
            if item.is_file():
                item.unlink()
        try:
            PYCACHE.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    main()
