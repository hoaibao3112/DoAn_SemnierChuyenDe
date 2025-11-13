<#
Run the whole QA pipeline: reset DB, reclass, eval, run tests.

Usage (from project root, venv activated):
  .\scripts\run_all.ps1

This script will:
- create ./logs
- run reset_and_seed_db.py (recreate DB and seed tests)
- run force_reclass2.py (ensure DB matches current logic)
- run test_runner.py --debug --extra and save log
- run pytest -q and save log
- run eval_db.py --limit 200 and save log
- print a short summary (accuracy, pytest summary, DB distribution)

It does NOT modify your code other than the DB and writes logs to ./logs.
#>

Set-StrictMode -Version Latest

$root = (Get-Location).Path
$logs = Join-Path $root 'logs'
New-Item -ItemType Directory -Path $logs -Force | Out-Null

function Run-Python($args, $outfile){
    Write-Host "\n==> Running: python $args" -ForegroundColor Cyan
    $file = Join-Path $logs $outfile
    # Run and tee output
    & python $args 2>&1 | Tee-Object -FilePath $file
    $rc = $LASTEXITCODE
    if ($rc -ne 0) { Write-Host "Command returned exit code $rc" -ForegroundColor Red }
    return @{ rc = $rc; file = $file }
}

Write-Host "Starting full run at $(Get-Date -Format s)" -ForegroundColor Green

# 1) Reset & seed DB
$r1 = Run-Python '.\scripts\reset_and_seed_db.py' 'reset_seed.txt'
if ($r1.rc -ne 0) { Write-Host "Reset & seed failed; aborting." -ForegroundColor Red; exit $r1.rc }

# 2) Force reclass (ensure DB updated with current logic)
$r2 = Run-Python '.\scripts\force_reclass2.py' 'force_reclass.txt'
if ($r2.rc -ne 0) { Write-Host "Force reclass failed; continuing to gather logs." -ForegroundColor Yellow }

# 3) Run test runner (detailed)
$r3 = Run-Python '.\test_runner.py --debug --extra' 'test_runner.txt'

# 4) Run pytest
Write-Host "\n==> Running: pytest -q" -ForegroundColor Cyan
$pytestFile = Join-Path $logs 'pytest.txt'
pytest -q 2>&1 | Tee-Object -FilePath $pytestFile
$pytestRc = $LASTEXITCODE
if ($pytestRc -ne 0) { Write-Host "pytest returned exit code $pytestRc" -ForegroundColor Red }

# 5) Eval DB distribution
$r5 = Run-Python '.\scripts\eval_db.py --limit 200' 'eval_db.txt'

Write-Host "\n=== Summary ===" -ForegroundColor Green

# Extract ACCURACY line from test_runner
try {
    $accLine = Select-String -Path (Join-Path $logs 'test_runner.txt') -Pattern 'ACCURACY:' -SimpleMatch | Select-Object -First 1
    if ($accLine) { Write-Host "Test runner: $($accLine.Line)" -ForegroundColor Green }
    else { Write-Host "Test runner: ACCURACY line not found in log." -ForegroundColor Yellow }
} catch { Write-Host "Could not read test_runner log." -ForegroundColor Yellow }

# Pytest summary (last non-empty line)
try {
    $pyLines = Get-Content (Join-Path $logs 'pytest.txt') | Where-Object { $_ -ne '' }
    if ($pyLines.Count -gt 0) { Write-Host "Pytest last line: $($pyLines[-1])" -ForegroundColor Green }
    else { Write-Host "Pytest produced no output." -ForegroundColor Yellow }
} catch { Write-Host "Could not read pytest log." -ForegroundColor Yellow }

# Eval DB distribution (first 10 lines)
try {
    Write-Host "\nDB eval (first 12 lines):" -ForegroundColor Green
    Get-Content (Join-Path $logs 'eval_db.txt') | Select-Object -First 12 | ForEach-Object { Write-Host $_ }
} catch { Write-Host "Could not read eval_db log." -ForegroundColor Yellow }

Write-Host "\nLogs saved under: $logs" -ForegroundColor Cyan
Write-Host "Full run complete at $(Get-Date -Format s)" -ForegroundColor Green

if ($pytestRc -ne 0 -or $r3.rc -ne 0) { exit 1 } else { exit 0 }
