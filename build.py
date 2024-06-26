import os
import shutil

# Where to output zip file
out_dir = "dist"

# Folder which contains add-on code
src_dir = "dcgenerator"


# Create "./dist" directory
os.makedirs(out_dir, exist_ok=True)

# Create zip file
shutil.make_archive(f"{out_dir}/{src_dir}", 'zip', src_dir)
