# Check Claude Code prerequisites on Windows
Write-Output "Checking CLAUDE_CODE_GIT_BASH_PATH and Git/Bash availability..."

# Check CLAUDE_CODE_GIT_BASH_PATH (process/user/machine)
$proc = [Environment]::GetEnvironmentVariable('CLAUDE_CODE_GIT_BASH_PATH','Process')
$user = [Environment]::GetEnvironmentVariable('CLAUDE_CODE_GIT_BASH_PATH','User')
$machine = [Environment]::GetEnvironmentVariable('CLAUDE_CODE_GIT_BASH_PATH','Machine')

Write-Output "Process variable: $proc"
Write-Output "User variable:    $user"
Write-Output "Machine variable: $machine"

# Test path existence if any value is set
foreach ($val in @($proc,$user,$machine)) {
    if ([string]::IsNullOrWhiteSpace($val)) { continue }
    if (Test-Path $val) { Write-Output "Exists: $val" } else { Write-Output "Not found: $val" }
}

# Check for git in PATH
try {
    $git = (Get-Command git -ErrorAction Stop).Source
    Write-Output "git found: $git"
} catch {
    Write-Output "git not found in PATH"
}

# Search common Git for Windows locations
$common = @(
    'C:\Program Files\Git\bin\bash.exe',
    'C:\Program Files\Git\usr\bin\bash.exe',
    "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe"
)
foreach ($p in $common) {
    if (Test-Path $p) { Write-Output "Found Git Bash at: $p" }
}

Write-Output "To fix: Install Git for Windows (https://git-scm.com/downloads), or set CLAUDE_CODE_GIT_BASH_PATH to the full path to bash.exe and restart VS Code."