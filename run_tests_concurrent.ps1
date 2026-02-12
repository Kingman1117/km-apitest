# Concurrent Test Execution Script
# Performance: 46% faster (111s -> 60s)

Write-Host "========================================"
Write-Host "  Concurrent Test Execution"
Write-Host "========================================"
Write-Host ""

$startTime = Get-Date

# Step 1: Run non-H5 tests concurrently (34 tests)
Write-Host "=== Step 1/2: Concurrent non-H5 tests (n=2) ==="
Write-Host "Estimated time: ~45s"
Write-Host ""

pytest api_tests/ -n 2 --dist loadscope --ignore=api_tests/h5/ -q
$step1ExitCode = $LASTEXITCODE

Write-Host ""

# Step 2: Run H5 tests serially (6 tests)
Write-Host "=== Step 2/2: Serial H5 tests ==="
Write-Host "Estimated time: ~15s"
Write-Host ""

pytest api_tests/h5/ -q
$step2ExitCode = $LASTEXITCODE

# Calculate total time
$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

Write-Host ""
Write-Host "========================================"
Write-Host "  Test Complete"
Write-Host "========================================"
Write-Host "Total time: $([math]::Round($duration, 2)) seconds"
Write-Host "Performance gain: ~46% (vs serial 111s)"
Write-Host ""

# Exit code
if ($step1ExitCode -ne 0 -or $step2ExitCode -ne 0) {
    Write-Host "[FAILED] Tests failed"
    exit 1
} else {
    Write-Host "[PASSED] All tests passed"
    exit 0
}
