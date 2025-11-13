<#
Auto reclass PowerShell helper (safe, idempotent)

Usage (run from project root, venv activated):
  .\scripts\auto_reclass.ps1

What it does:
- Creates a timestamped backup of `sentiments.db` (if present).
- Creates/overwrites `sentiments.db.bak` as an additional backup.
- Runs Python script `scripts\force_reclass.py` to re-evaluate and update DB rows.
- Runs `scripts\eval_db.py --limit 50` to print the updated distribution and a sample of recent rows.

This script is defensive and prints helpful messages. It returns a non-zero exit
code when an underlying Python step fails.
#>

try {
	$ErrorActionPreference = 'Stop'

	Write-Host "Auto reclass helper starting..." -ForegroundColor Cyan

	$root = (Get-Location).Path
	$dbPath = Join-Path $root 'sentiments.db'
	$bakPath = Join-Path $root 'sentiments.db.bak'

	if (Test-Path $dbPath) {
		$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
		$manualBak = Join-Path $root ("sentiments.db.manual.{0}.bak" -f $timestamp)
		Copy-Item -Path $dbPath -Destination $manualBak -Force
		Write-Host "Created manual DB backup: $manualBak" -ForegroundColor Green

		# Also update the generic backup
		Copy-Item -Path $dbPath -Destination $bakPath -Force
		Write-Host "Updated default backup: $bakPath" -ForegroundColor Green
	}
	else {
		Write-Host "No database file found at $dbPath. The reclass script will likely fail." -ForegroundColor Yellow
	}

	# Run the force reclass script
	Write-Host "Running python .\scripts\force_reclass2.py ..." -ForegroundColor Cyan
	& python .\scripts\force_reclass2.py
	$rc = $LASTEXITCODE
	if ($rc -ne 0) {
		Write-Host "force_reclass.py exited with code $rc" -ForegroundColor Red
		exit $rc
	}

	# Run evaluator to show result
	Write-Host "\nRunning python .\scripts\eval_db.py --limit 50 ..." -ForegroundColor Cyan
	& python .\scripts\eval_db.py --limit 50
	$rc2 = $LASTEXITCODE
	if ($rc2 -ne 0) {
		Write-Host "eval_db.py exited with code $rc2" -ForegroundColor Red
		exit $rc2
	}

	Write-Host "\nAuto reclass finished. If using Streamlit, restart it so the UI reloads DB:" -ForegroundColor Green
	Write-Host "  streamlit run app.py" -ForegroundColor Green
}
catch {
	Write-Host "An error occurred: $_" -ForegroundColor Red
	exit 1
}

