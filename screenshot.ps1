#! /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -File
###! /home/bruno/scripts/pshellwrap

param(
    [Parameter(Mandatory=$true)][string]$output,
    [int]$top = -1,
    [int]$left = -1,
    [int]$width = -1,
    [int]$height = -1
)

Add-Type -AssemblyName System.Windows.Forms,System.Drawing

$screens = [Windows.Forms.Screen]::AllScreens

if ($top -lt 0) { $top = ($screens.Bounds.Top | Measure-Object -Minimum).Minimum }
if ($left -lt 0) { $left = ($screens.Bounds.Left | Measure-Object -Minimum).Minimum }
if ($width -lt 0) { $width = ($screens.Bounds.Right | Measure-Object -Maximum).Maximum }
if ($height -lt 0) { $height = ($screens.Bounds.Bottom | Measure-Object -Maximum).Maximum }

$bounds = [Drawing.Rectangle]::FromLTRB($left, $top, $width, $height)
$bmp = New-Object System.Drawing.Bitmap ([int]$bounds.width), ([int]$bounds.height)
$graphics = [Drawing.Graphics]::FromImage($bmp)

$graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size)
$bmp.Save($output)

$graphics.Dispose()
$bmp.Dispose()

