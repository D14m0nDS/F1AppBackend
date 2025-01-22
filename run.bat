@echo off

REM Clear previous HOST_IP and SUBNET_MASK entries in the .env file
findstr /v "HOST_IP=" .env > temp.env
findstr /v "SUBNET_MASK=" temp.env > temp2.env
move /y temp2.env .env

REM Variables to store IP and Subnet Mask
set HOST_IP=
set SUBNET_MASK=

REM Loop through IP addresses and their subnet masks
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr "IPv4 Address" ^| findstr "192."') do set "HOST_IP=%%A"
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr "Subnet Mask"') do (
    if not defined SUBNET_MASK set "SUBNET_MASK=%%A"
)

REM Remove leading spaces
set HOST_IP=%HOST_IP: =%
set SUBNET_MASK=%SUBNET_MASK: =%

REM Add HOST_IP and SUBNET_MASK to the .env file
echo HOST_IP=%HOST_IP% >> .env
echo SUBNET_MASK=%SUBNET_MASK% >> .env

REM Display the detected IP and Subnet Mask
echo Detected Local IP: %HOST_IP%
echo Detected Subnet Mask: %SUBNET_MASK%

REM Start Docker Compose
docker-compose up --build
