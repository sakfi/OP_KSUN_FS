$jobsUrl = 'https://api.github.com/repos/sakfi/OP_KSUN_FS/actions/runs/22692212457/jobs'
$response = Invoke-RestMethod -Uri $jobsUrl
foreach ($j in $response.jobs) {
    if ($j.conclusion -eq 'failure' -or ($j.status -eq 'completed' -and $j.conclusion -eq 'failure')) {
        Write-Host "Job Failed: $($j.name)"
        foreach ($s in $j.steps) {
            if ($s.conclusion -eq 'failure') {
                Write-Host "  Step Failed: $($s.name)"
            }
        }
        break
    }
}

Write-Host "---"

$commitsUrl = 'https://api.github.com/repos/WildKernels/OnePlus_KernelSU_SUSFS/commits?per_page=5'
$commits = Invoke-RestMethod -Uri $commitsUrl
foreach ($c in $commits) {
    Write-Host "- $($c.commit.message.Split("`n")[0])"
}
