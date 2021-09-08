$scriptpath = $MyInvocation.MyCommand.Path
$dir = Split-Path $scriptpath
Push-Location $dir

Write-Host "Setting up container" -ForegroundColor Green
docker container stop containertcc
docker container rm containertcc
docker image rm local-db

docker pull microsoft/mssql-server-linux:2017-latest

Write-Host "Waiting for container to start up..." -ForegroundColor Green
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=dti@1406" --name "containertcc" -p 9000:1433 -d microsoft/mssql-server-linux:2017-latest
   
$jb = Start-Job { docker logs -f containertcc }
while ($jb.HasMoreData) { 
	Receive-Job $jb -OutVariable output | ForEach-Object { if ($_ -match "Microsoft Corporation") { break } }
}
Stop-Job $jb
Remove-Job $jb

write-host "moving scripts into container" -foregroundcolor green
docker exec -t containertcc mkdir /var/opt/mssql/scripts/
docker cp ./00_cria.sql containertcc:/var/opt/mssql/scripts/

write-host "runing scripts" -foregroundcolor green
docker exec -t containertcc /opt/mssql-tools/bin/sqlcmd -s localhost -U SA -P "dti@1406" -i /var/opt/mssql/scripts/00_cria.sql 