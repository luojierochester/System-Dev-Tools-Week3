param(
    [string]$TorchPython = $env:TORCH_PYTHON
)

$ErrorActionPreference = 'Stop'
$Repo = Split-Path $PSScriptRoot -Parent
$ToolsPython = Join-Path $Repo 'q09\.venv\Scripts\python.exe'
$SystemPython = 'C:\Users\25651\AppData\Local\Programs\Python\Python312\python.exe'

function Section([string]$Title) {
    Write-Output ""
    Write-Output "===== $Title ====="
}

function Run([string]$Label, [scriptblock]$Action) {
    Section $Label
    & $Action
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

Set-Location $Repo
if (-not (Test-Path -LiteralPath $ToolsPython)) {
    if (-not (Test-Path -LiteralPath $SystemPython)) {
        throw 'Python 3.12 was not found; install Python or create q09/.venv.'
    }
    & $SystemPython -m venv (Join-Path $Repo 'q09\.venv')
}

$missingTools = & $ToolsPython -c "import importlib.util; print(any(importlib.util.find_spec(x) is None for x in ('build','pytest','ruff')))"
if ($missingTools -eq 'True') {
    & $ToolsPython -m pip install --disable-pip-version-check build pytest ruff
}

if (-not $TorchPython) {
    $candidates = @(
        $ToolsPython,
        'C:\Users\25651\Desktop\机器视觉\课程结课设计\.venv\Scripts\python.exe',
        $SystemPython
    )
    foreach ($candidate in $candidates) {
        if ((Test-Path -LiteralPath $candidate) -and
            ((& $candidate -c "import importlib.util; print(importlib.util.find_spec('torch') is not None)") -eq 'True')) {
            $TorchPython = $candidate
            break
        }
    }
}
if (-not $TorchPython) {
    throw 'PyTorch interpreter not found. Set TORCH_PYTHON to a Python executable containing torch.'
}

Write-Output "Week 3 verification | student=24020007086"
Write-Output "tools_python=$ToolsPython"
Write-Output "torch_python=$TorchPython"

Run 'Static checks: Ruff' {
    & $ToolsPython -m ruff check q09 q10 q12 exercises scripts
}

Run 'q09: build wheel' {
    & $ToolsPython -m build --wheel q09
}
$Wheel = Get-ChildItem -LiteralPath (Join-Path $Repo 'q09\dist') -Filter '*.whl' |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Wheel) { throw 'q09 did not produce a wheel' }

Run 'q09: inspect wheel metadata' {
    & $ToolsPython exercises/q13_ext/wheel_inspector.py $Wheel.FullName
}
Run 'q09: isolated install outside source tree' {
    & $ToolsPython exercises/q14_ext/verify_wheel.py $Wheel.FullName
}

Run 'q10: repaired CLI tests' {
    $previous = $env:PYTHONPATH
    try {
        $env:PYTHONPATH = (Join-Path $Repo 'q10\src')
        & $ToolsPython -m pytest -q q10/tests
    } finally {
        $env:PYTHONPATH = $previous
    }
}

Run 'q11: communication checks' {
    & $ToolsPython exercises/q19_ext/issue_linter.py q11/communication.md
    if ($LASTEXITCODE -ne 0) { return }
    & $ToolsPython exercises/q20_ext/review_linter.py q11/communication.md
}

Run 'q12: deterministic CPU training' {
    Push-Location q12
    try { & $TorchPython train.py; & $TorchPython -m unittest -v test_train.py }
    finally { Pop-Location }
}

foreach ($number in 13..20) {
    $directory = "exercises/q${number}_ext"
    $tests = Get-ChildItem -LiteralPath $directory -Filter 'test_*.py' -ErrorAction SilentlyContinue
    if ($tests) {
        Run "extension q${number}_ext tests" {
            & $ToolsPython -m unittest discover -s $directory -p 'test_*.py' -v
        }
    }
}

Run 'Ex05: prompt contract' {
    & $ToolsPython exercises/q17_ext/prompt_contract.py exercises/q17_ext/example_contract.json
}
Run 'Ex06: bounded verification command' {
    & $ToolsPython exercises/q18_ext/verified_loop.py --attempts 2 -- $ToolsPython -c "print('verified')"
}

foreach ($number in 21..23) {
    $directory = "exercises/q${number}_ext"
    Run "extension q${number}_ext tests" {
        & $TorchPython -m unittest discover -s $directory -p 'test_*.py' -v
    }
}

Run 'Ex09: reproducibility audit' {
    & $TorchPython exercises/q21_ext/reproducibility_audit.py
}
Run 'Ex10: gradient diagnostics' {
    & $TorchPython exercises/q22_ext/gradient_diagnostics.py
}
Run 'Ex11: checkpoint roundtrip' {
    & $TorchPython exercises/q23_ext/checkpoint_roundtrip.py
}

Section 'RESULT'
Write-Output 'ALL WEEK 3 CHECKS PASSED'
