$archivePath = "all.zip"
$excludedItems = @("venv", "config.txt", ".gitattributes")
$pscpPath = "C:\Program Files\PuTTY\pscp.exe"
$pscpArgs = "all.zip root@192.168.1.130:/root"

if (Test-Path $archivePath) {
    Remove-Item $archivePath -Force
}

$itemsToArchive = Get-ChildItem | Where-Object { $_.Name -notin $excludedItems }
Compress-Archive -Path $itemsToArchive -DestinationPath $archivePath

Start-Process -FilePath $pscpPath -ArgumentList $pscpArgs