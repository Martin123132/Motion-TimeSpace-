from common import *
import ast

modest()
check_parent()
records = []
for path in STAGE.glob("*.py"):
    ast.parse(path.read_text(encoding="utf-8"))
    records.append(dict(path=str(path), sha256=digest(path)))
write(ROOT / "syntax-result.json", dict(passed=True, records=records, family=LABEL))
print("syntax and retained-source integrity passed", LABEL, flush=True)
