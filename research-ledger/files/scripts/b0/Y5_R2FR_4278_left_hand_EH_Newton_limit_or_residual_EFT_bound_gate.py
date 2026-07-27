from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4278"
CLAIM_ID = "L-119"
BRANCH = "MTS_R2FR_Y5_LEFT_HAND_EH_NEWTON_LIMIT_OR_RESIDUAL_EFT_BOUND_GATE_4278"
DECISION = "LEFT_HAND_EH_NEWTON_CHAIN_ASSEMBLED_CONDITIONAL_PALATINI_SELECTOR_RESIDUAL_EFT_FORKS_REMAIN_NONCLAIM"
MARKER = "PPC4161_LEFT_HAND_EH_NEWTON_LIMIT_OR_RESIDUAL_EFT_BOUND_GATE_4278"
PACKET_MARKER = "PPC4161_PACKET_LEFT_HAND_EH_NEWTON_LIMIT_OR_RESIDUAL_EFT_BOUND_GATE_4278"
NEXT_TARGET = "4279-Y5-R2FR-residual-EFT-coefficient-zero-or-local-test-bound-pack.md"

FORMAL_PATH = FORMAL / "294-PPC4161-left-hand-EH-Newton-limit-or-residual-EFT-bound-gate.md"
DOC_PATH = POST / "4278-Y5-R2FR-left-hand-EH-Newton-limit-or-residual-EFT-bound-gate.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4278_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES = {
    "SRC4278_00_4277_action_domain": (
        FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md",
        "new 4277 standard-branch row: Dq_geom = 0.0",
        "4277 closes the right-hand coupling leak in the standard branch.",
    ),
    "SRC4278_01_4181_EH_origin_gate": (
        FORMAL / "197-PPC4161-EH-local-metric-principal-block-origin-gate.md",
        "S_EC[e,omega;kappa_eff] -> S_EH[g_obs;kappa_eff] + boundary",
        "4181 writes the conditional motion-frame Palatini-to-EH theorem.",
    ),
    "SRC4278_02_4183_AMF": (
        FORMAL / "199-PPC4161-motion-frame-axiom-adoption-consequences-and-test-contract.md",
        "A_MF_adoption_contract_written = true",
        "4183 derives the Noether/conservation consequences of adopting A_MF.",
    ),
    "SRC4278_03_4184_IR_selector": (
        FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md",
        "S_EC = (4 kappa_eff)^-1",
        "4184 selects the EC/Palatini principal block conditionally and names residual EFT terms.",
    ),
    "SRC4278_04_4178_kappa": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi)",
        "4178 supplies the calibrated structural source-coupling law.",
    ),
    "SRC4278_05_4171_newton": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "nabla^2 Phi_N = 4*pi G_N rho_H",
        "4171 supplies the weak-field Poisson/Gauss/Newton readout.",
    ),
    "SRC4278_06_4172_ppn": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "R_PPN =",
        "4172 supplies the private full PPN readout inside the EH branch.",
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
    fieldnames = list(rows[0].keys())
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


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def selector_clause_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "SEL4278_0_motion_frame_variables",
            "A_MF identifies X^A=L_*Psi^A labels as local motion-frame gauge data with e^A=D_omega X^A+B^A.",
            "motion-frame variables are natural left-hand fields",
            "CONDITIONAL_FROM_4183",
        ),
        (
            "SEL4278_1_local_covariant_action",
            "The local action is a covariant 4-form built from e^A, omega^AB, R^AB, T^A and q-basic scalars.",
            "forbids arbitrary noncovariant left-hand operators",
            "CONDITIONAL_SELECTOR_CLAUSE",
        ),
        (
            "SEL4278_2_IR_two_derivative_order",
            "At leading low-energy/two-derivative parity-even order, the EC/Palatini term is the selected principal block.",
            "selects EH principal operator",
            "CONDITIONAL_FROM_4184",
        ),
        (
            "SEL4278_3_same_observed_coframe",
            "Matter and Maxwell-Hodge use the same g_obs/coframe already protected by 4277.",
            "prevents second-metric/disformal left-hand leak",
            "CONDITIONAL_FROM_4277",
        ),
        (
            "SEL4278_4_torsion_nonmetricity_resolution",
            "Torsion/nonmetricity are algebraic and zero in the compact spinless branch, or retained as explicit coefficients.",
            "lets EC reduce to EH or reopens c_T/c_Q residuals",
            "CONDITIONAL_OR_RETAINED",
        ),
        (
            "SEL4278_5_fixed_coupling",
            "kappa_eff is fixed before local vertical variation and maps structurally to G_cal=c^4 kappa_eff/(8*pi).",
            "couples EH operator to the Hamiltonian/Hilbert source without orbital GM",
            "CONDITIONAL_FROM_4178",
        ),
    ]
    return [
        {
            **common(),
            "selector_id": selector_id,
            "clause": clause,
            "would_prove": would_prove,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for selector_id, clause, would_prove, status in raw
    ]


def left_hand_derivation_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "LHD4278_0_EC_block",
            "S_left -> S_EC = (4 kappa_eff)^-1 int eps_ABCD e^A wedge e^B wedge R^CD[omega] - Lambda term",
            "motion-frame Palatini selector supplies the leading local geometry operator",
            "CONDITIONAL_SELECTOR_THEOREM",
        ),
        (
            "LHD4278_1_connection_equation",
            "delta_omega S_EC = 0 gives algebraic torsion/spin equation; compact spinless branch gives T^A=0 up to retained c_T source",
            "Palatini variables collapse to Levi-Civita EH if torsion residual is zero/bounded",
            "CONDITIONAL_TORSION_RESOLUTION",
        ),
        (
            "LHD4278_2_metric_equation",
            "delta_e S_EC + delta_e S_matter = 0 gives G_mu_nu + Lambda_eff g_mu_nu = kappa_eff T_H_mu_nu + E_res_mu_nu",
            "left-hand EH equation with explicit residual tensor",
            "CONDITIONAL_EH_EQUATION_WITH_RESIDUALS",
        ),
        (
            "LHD4278_3_local_source_coupling",
            "G_cal = c^4 kappa_eff/(8*pi), D_v ln kappa_eff = 0",
            "calibrated structural Newton coupling with no local hidden drift",
            "CONDITIONAL_FROM_4178_4267",
        ),
        (
            "LHD4278_4_Poisson_readout",
            "G_00^lin=2 nabla^2 Phi_N/c^2 and T_00=rho_H c^2 imply nabla^2 Phi_N=4*pi G_cal rho_H plus residuals",
            "Newtonian mechanics follows from the left-hand EH operator and Hamiltonian/Hilbert source",
            "CONDITIONAL_NEWTON_LIMIT_DERIVED",
        ),
        (
            "LHD4278_5_PPN_readout",
            "EH <=2PN readout with 4277 no shadow slots gives gamma=1, beta=1, alpha_i=zeta_i=xi=0, Gdot/G=0 plus residual vector",
            "PPN target vector is zero only when residual EFT rows are closed",
            "CONDITIONAL_PPN_VECTOR_WITH_RESIDUAL_FORKS",
        ),
    ]
    return [
        {
            **common(),
            "derivation_id": derivation_id,
            "mathematical_form": mathematical_form,
            "result": result,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for derivation_id, mathematical_form, result, status in raw
    ]


def residual_eft_rows() -> List[Dict[str, str]]:
    raw = [
        ("RES4278_0_torsion", "c_T", "torsion-squared/algebraic torsion source", "PPN preferred-frame/spin-torsion; clock/orbital residual", "parent zero, spinless algebraic elimination, heavy mass, or sourced bound"),
        ("RES4278_1_curvature_squared", "c_R2_or_M_R", "R^2/R_mu_nu^2/Weyl^2 corrections", "short-range/R10, PPN beta/gamma, orbital precession", "parent zero, topological reduction, M_R large, or sourced EFT bound"),
        ("RES4278_2_second_metric", "c_D", "second metric/disformal ordinary matter owner", "fifth-force, WEP, PPN gamma, clocks", "4277 zero theorem or finite canonical coupling source row"),
        ("RES4278_3_memory", "c_Gamma", "local memory/Gamma/Khat coupling in left-hand operator", "range-dependent local force, cosmology-local leakage", "parent double-zero/no-flux theorem or local bound"),
        ("RES4278_4_boundary", "c_bdy", "unrouted boundary/edge charge in compact collar", "source normalization, clock/orbital residual", "fixed exact boundary or source-backed flux bound"),
        ("RES4278_5_coupling_drift", "delta_kappa", "local source-coupling drift", "Gdot/G, WEP/source-mass calibration", "4267 fixed coefficient branch or numeric drift bound"),
        ("RES4278_6_lambda", "Lambda_eff_local", "cosmological/vacuum term in local weak field", "constant acceleration/tidal residual", "local negligible bound or cosmology-calibrated row"),
    ]
    return [
        {
            **common(),
            "residual_id": residual_id,
            "coefficient": coefficient,
            "meaning": meaning,
            "test_arena": test_arena,
            "closure_requirement": closure_requirement,
            "status": "RESIDUAL_RETAINED_UNTIL_PARENT_ZERO_OR_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for residual_id, coefficient, meaning, test_arena, closure_requirement in raw
    ]


def operator_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "gate_id": "OPG4278_0_conditional_EH_Newton_pass",
            "left_hand_operator": "G_mu_nu[g_obs]+Lambda_eff g_mu_nu",
            "right_hand_source": "kappa_eff T_H_mu_nu",
            "residual_tensor": "E_res_mu_nu=0 only if all residual EFT rows are closed",
            "newton_limit": "nabla^2 Phi_N=4*pi G_cal rho_H",
            "ppn_vector": "R_PPN=0",
            "status": "CONDITIONAL_BRANCH_PASS_NONCLAIM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "OPG4278_1_effective_GR_residual_fork",
            "left_hand_operator": "EH plus residual EFT corrections",
            "right_hand_source": "same Hilbert source plus retained residual source terms",
            "residual_tensor": "E_res_mu_nu != 0 until coefficient rows are parent-zero, heavy/screened, or bounded",
            "newton_limit": "Poisson law gains Delta_Phi_res",
            "ppn_vector": "R_PPN gains residual components",
            "status": "RESIDUAL_BOUND_ROUTE_OPEN",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4278_0_chain_assembled",
            "Assemble the left-hand chain instead of treating EH/Newton as scattered private notes.",
            "4277 closes the right-hand local coupling leak; 197/199/200 supply the conditional Palatini/EH selector; 187/188/194 supply Newton/PPN/source-coupling readout.",
            "use this as the local left-hand gate",
        ),
        (
            "DEC4278_1_no_public_claim",
            "Keep the route private/nonclaim because the selector is conditional.",
            "A_MF/IR selector and residual coefficient closures are not globally parent-derived.",
            NEXT_TARGET,
        ),
        (
            "DEC4278_2_testable_fork",
            "Any failure of the selector becomes named EFT residual coefficients, not vague missing magic.",
            "torsion, curvature-squared, second metric, memory, boundary, kappa drift and Lambda rows map to PPN/R10/clock/orbital/EM tests.",
            "source or bound residual coefficients",
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4278_0_no_EH_import", "EH equations are allowed only after the motion-frame/Palatini selector clauses are explicitly adopted or derived."),
        ("FW4278_1_no_residual_erasure", "Residual EFT terms cannot be called zero unless parent-forbidden, heavy/screened, topological, boundary-exact, or source-bounded."),
        ("FW4278_2_no_numeric_G_claim", "G_cal is structurally derived from kappa_eff, but its numerical SI value remains empirical unless a parent scale law fixes kappa_eff."),
        ("FW4278_3_no_public_local_GR_claim", "Newton/PPN readout is conditional branch evidence, not a public local-GR pass or empirical validation."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4278",
            "current_status": "left-hand EH/Newton chain assembled as conditional Palatini-selector route with explicit residual EFT forks",
            "local_gr_claim": "False",
            "newton_claim": "False",
            "ppn_claim": "False",
            "numeric_G_prediction": "False",
            "next_best_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "the branch now has conditional right-hand coupling zero and conditional left-hand EH/Newton chain; the remaining route to tests is closing or bounding residual EFT coefficients.",
            "success_condition": "derive parent zeros/heavy scales for residual coefficients or create source-backed local test bounds for PPN, R10, clocks, WEP, orbital and EM arenas.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


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
            "4278 assembles the left-hand local EH/Newton route as a single conditional gate: A_MF plus a Palatini IR selector gives the EC principal block, torsion resolution gives EH, "
            "the calibrated source law gives G_cal=c^4 kappa_eff/(8*pi), and the weak-field 00 equation gives Poisson/Newton/PPN readout when residual EFT rows vanish or are bounded."
        ),
        "current_evidence": (
            "4278 source register, selector clauses, left-hand derivation rows, residual EFT map, operator gate rows, decision and firewall."
        ),
        "status": "private_conditional_left_hand_EH_Newton_chain_assembled_residual_EFT_forks_nonclaim",
        "next_test": "Close or bound torsion, curvature-squared, second-metric/disformal, memory, boundary, kappa-drift and Lambda residual coefficients against local arenas.",
        "key_risk": "Treating conditional Palatini/EH selector as a public MTS derivation, erasing residual EFT terms, or claiming a numerical prediction of G.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def append_unique_block(path: Path, marker: str, title: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + f"\n\n## {title}\n\nMarker: `{marker}`\n\n{body.strip()}\n", encoding="utf-8")


def formal_doc() -> str:
    return f"""
# 294 - PPC4161 left-hand EH/Newton limit or residual EFT bound gate

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4278 does not claim public local GR, empirical PPN/R10 safety, orbital validation, or a numerical prediction of Newton's constant.

It does assemble the local left-hand route as one conditional theorem chain:

```text
4277 matter-interface descent
+ A_MF motion-frame adoption
+ Palatini IR normal-form selector
+ torsion/nonmetricity zero-or-bound
+ fixed calibrated kappa_eff
=> EH/Newton/PPN left-hand operator, up to explicit residual EFT rows.
```

## Left-hand derivation

The selected local geometry block is:

```text
S_EC = (4 kappa_eff)^-1 int epsilon_ABCD e^A wedge e^B wedge R^CD[omega]
       - (Lambda_eff/12 kappa_eff) int epsilon_ABCD e^A wedge e^B wedge e^C wedge e^D.
```

In the compact spinless branch, the connection equation is algebraic:

```text
delta_omega S_EC = 0
=> T^A = 0
```

unless a torsion residual coefficient is retained.

Substitution gives:

```text
S_EC[e,omega;kappa_eff] -> S_EH[g_obs;kappa_eff] + boundary.
```

Variation gives:

```text
G_mu_nu[g_obs] + Lambda_eff g_mu_nu
= kappa_eff T_H_mu_nu + E_res_mu_nu.
```

Here `E_res_mu_nu` is not hand-waved away. It is the sum of retained torsion, curvature-squared, second-metric, memory, boundary, kappa-drift and local-Lambda residuals.

## Newton readout

With:

```text
G_cal = c^4 kappa_eff/(8*pi),
G_00^lin = 2 nabla^2 Phi_N/c^2,
T_00 = rho_H c^2,
```

the zero-residual branch gives:

```text
nabla^2 Phi_N = 4*pi G_cal rho_H.
```

The Hamiltonian/Hilbert source charge then gives:

```text
Phi_N = -G_cal M_H^dress/r,
a_r = -G_cal M_H^dress/r^2.
```

This is a structural Newtonian reduction. It still does not predict the numerical SI value of `G`.

## PPN readout

When the residual tensor is zero or below local-test bounds, the EH `<=2PN` readout gives:

```text
gamma = 1,
beta = 1,
alpha_i = 0,
zeta_i = 0,
xi = 0,
dot(G_eff)/G_eff = 0.
```

If any selector clause fails, the failure becomes a named residual coefficient, not a silent closure assumption.

## Residual EFT fork

The active residual map is:

```text
c_T             torsion/nonmetricity residual,
c_R2 or M_R     curvature-squared correction,
c_D             second metric/disformal owner,
c_Gamma         memory/Gamma/Khat local coupling,
c_bdy           boundary/edge charge,
delta_kappa     coupling drift,
Lambda_eff      local vacuum/tidal residual.
```

Each must be parent-zero, symmetry-forbidden, heavy/screened, topological/boundary-exact, or source-backed bounded.

## Next target

`{NEXT_TARGET}` should close or bound the residual EFT coefficient map against PPN, R10, clocks, WEP, orbital, and EM arenas.
"""


def checkpoint_doc() -> str:
    return f"""
# 4278 - left-hand EH/Newton limit or residual EFT bound gate

Marker: `{MARKER}`

Decision: `{DECISION}`

4278 assembles the left-hand chain:

```text
A_MF + Palatini IR selector
=> S_EC
=> S_EH + boundary
=> G_mu_nu = kappa_eff T_H_mu_nu + residuals
=> nabla^2 Phi_N = 4*pi G_cal rho_H + residuals.
```

The route is live but conditional. The next target is not another vague missing ledger; it is the residual coefficient map:

```text
c_T, c_R2/M_R, c_D, c_Gamma, c_bdy, delta_kappa, Lambda_eff.
```
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    selectors = csv_rows(paths["selector"])
    derivations = csv_rows(paths["derivation"])
    residuals = csv_rows(paths["residuals"])
    gates = csv_rows(paths["operator_gate"])
    all_rows: Iterable[Dict[str, str]] = (
        sources
        + selectors
        + derivations
        + residuals
        + gates
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4278_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4278_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4278_2_selector_present",
            any(row["selector_id"] == "SEL4278_2_IR_two_derivative_order" and row["status"] == "CONDITIONAL_FROM_4184" for row in selectors),
            "Palatini IR selector clause represented",
        ),
        (
            "VAL4278_3_EH_equation",
            any(row["derivation_id"] == "LHD4278_2_metric_equation" and row["status"] == "CONDITIONAL_EH_EQUATION_WITH_RESIDUALS" for row in derivations),
            "EH metric equation with residual tensor written",
        ),
        (
            "VAL4278_4_Newton_limit",
            any(row["derivation_id"] == "LHD4278_4_Poisson_readout" and row["status"] == "CONDITIONAL_NEWTON_LIMIT_DERIVED" for row in derivations),
            "Poisson/Newton readout linked to kappa_eff",
        ),
        (
            "VAL4278_5_residual_map",
            {"c_T", "c_R2_or_M_R", "c_D", "c_Gamma", "c_bdy", "delta_kappa", "Lambda_eff_local"}.issubset({row.get("coefficient") for row in residuals}),
            "all named residual EFT coefficients mapped",
        ),
        (
            "VAL4278_6_operator_gate_nonclaim",
            any(row["gate_id"] == "OPG4278_0_conditional_EH_Newton_pass" and row["valid_for_claim"] == "False" for row in gates),
            "operator gate remains conditional nonclaim",
        ),
        ("VAL4278_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4278_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4278_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4278_10_no_claim_rows", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows), "all rows remain nonclaim"),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4278_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4278_SOURCE_REGISTER.csv",
        "selector": SOURCE_DIR / "P8_Y5_R2FR_4278_PALATINI_SELECTOR_CLAUSES.csv",
        "derivation": SOURCE_DIR / "P8_Y5_R2FR_4278_LEFT_HAND_EH_NEWTON_DERIVATION.csv",
        "residuals": SOURCE_DIR / "P8_Y5_R2FR_4278_RESIDUAL_EFT_COEFFICIENT_MAP.csv",
        "operator_gate": SOURCE_DIR / "P8_Y5_R2FR_4278_LEFT_HAND_OPERATOR_GATE.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4278_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4278_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4278_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4278_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["selector"], selector_clause_rows())
    write_csv(paths["derivation"], left_hand_derivation_rows())
    write_csv(paths["residuals"], residual_eft_rows())
    write_csv(paths["operator_gate"], operator_gate_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4278 left-hand EH/Newton gate",
        "4278 assembles the conditional left-hand chain: `A_MF + Palatini IR selector -> S_EC -> S_EH -> G_mu_nu=kappa_eff T_H_mu_nu + residuals -> Poisson/Newton/PPN readout`. It keeps public claims false and turns any selector failure into explicit residual EFT coefficients: `c_T`, `c_R2/M_R`, `c_D`, `c_Gamma`, `c_bdy`, `delta_kappa`, and `Lambda_eff`.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4278 packet left-hand EH/Newton gate",
        "Packet update: after 4277 closes the standard-branch matter-interface leak, 4278 binds the left-hand Palatini/EH/Newton chain into one gate. The next pressure point is residual EFT coefficient closure or source-backed bounds.",
    )
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(VALIDATION_PATH))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
