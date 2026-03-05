$url = "https://api.github.com/repos/sakfi/OP_KSUN_FS/actions/runs/22692212457/logs"
$zipFile = "logs.zip"
$extractPath = "logs_extracted"

Write-Host "Downloading logs..."
Invoke-WebRequest -Uri $url -OutFile $zipFile

if (Test-Path $zipFile) {
    Write-Host "Extracting logs..."
    if (Test-Path $extractPath) { Remove-Item -Force -Recurse $extractPath }
    Expand-Archive -Path $zipFile -DestinationPath $extractPath
    
    # We are looking for "Build Kernel.txt" inside the specific job folder
    $logFiles = Get-ChildItem -Path $extractPath -Recurse -Filter "*Build Kernel.txt"
    foreach ($file in $logFiles) {
        $content = Get-Content $file.FullName
        # Simple heuristic to find errors
        $errors = $content | Select-String -Pattern "error:" -Context 2,2
        if ($errors) {
            Write-Host "Errors found in $($file.FullName):"
            $errors | Select-Object -First 10 | ForEach-Object { Write-Host $_ }
            break
        }
    }
}
