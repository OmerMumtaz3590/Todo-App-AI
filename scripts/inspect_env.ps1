$v=(Get-Item Env:CLAUDE_CODE_GIT_BASH_PATH).Value
Write-Output "Raw: '$v'"
Write-Output ('Escaped: ' + $v.Replace("`r","\\r").Replace("`n","\\n"))
$bytes=[System.Text.Encoding]::UTF8.GetBytes($v)
for ($i=0; $i -lt $bytes.Length; $i++) {
    Write-Output ("{0}: '{1}' 0x{2:X2}" -f $i, [char]$bytes[$i], $bytes[$i])
}