@echo off

set /p image_path="Enter the path to the image file: "
set /p width="Enter width of ascii art"

echo Running img2ascii.py...
python img2ascii.py "%image_path%" --invert --width "%width%"

echo.
pause