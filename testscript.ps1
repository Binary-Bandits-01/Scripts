# URL of the image you want to set as the wallpaper
$imageUrl = "https://drive.google.com/file/d/14Wrj8flgCS0E5DhXyS8WiwFIK6-qyF2e/view?usp=sharing"

# Destination path for the downloaded image
$downloadPath = "$env:USERPROFILE\Downloads\wallpaper.jpg"

# Download the image
Invoke-WebRequest -Uri $imageUrl -OutFile $downloadPath

# Set the downloaded image as the wallpaper
$regKeyPath = "HKCU:\Control Panel\Desktop"
Set-ItemProperty -Path $regKeyPath -Name Wallpaper -Value $downloadPath
RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters
