# Local replay

Use retained Windows Python 3.13 with NumPy, SciPy, SymPy and psutil, one numerical thread. Verification only: `python -B verify.py`. It reads previous and current packets, recalculates initial integrals/estimates and diagnostic scores, checks the reported failure, and verifies the receipt without starting an evolution. The seven technical notes distinguish analytic assumptions and numerical controls. No telescope input or external solver is needed. The local existence argument and source attribution are in LIFESPAN.md; the cited paper is not evidence for the numerical MTS amplitude.

For a complete numerical replay, create an empty sibling of this stage, copy only its Python scripts, Markdown and the original closeout.json into it, and keep the signed preceding stage intact. Below, each line is a separate invocation of the retained Python with `-B`; run serially. Files are exclusively created; never replay into the signed directory.
```
bootstrap.py
initial_polynomial.py
massive_budget.py
concentration.py
probe.py 960 0.000014
probe.py 1920 0.000014
test_response.py
shell_check.py 960 dust
shell_check.py 960 both
shell_check.py 1920 dust
shell_check.py 1920 both
shell_check.py score
energy_check.py 960 0.00625
energy_check.py 1920 0.00625
energy_check.py 1920 1
energy_check.py score
verify.py
```

Ordinary and full-strength shell checks share radial grids, proper-time targets and tolerance; the endpoint-slope stencil is independent of the evolution stencil. The 1/160 bound uses the continuum initial polynomial, not the new numerical energy histories. Point probes cannot certify a global continuum box: the analytic inequalities do that work. Do not use -O or --seal in a verification run. Creation of a receipt is exclusive and followed by an independent read-only invocation. No continuing job, GitHub action or change to the prior calculation is part of replay.

