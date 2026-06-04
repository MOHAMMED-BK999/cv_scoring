import zipfile
import os

z = zipfile.ZipFile('backend_small_2mb.zip', 'w', zipfile.ZIP_DEFLATED)
total_data_size = 0
MAX_DATA_SIZE = 2.5 * 1024 * 1024  # 2.5 MB

def add_dir(dir_name):
    global total_data_size
    for r, d, files in os.walk(dir_name):
        r_norm = r.replace('\\', '/')
        
        if '.venv' in r_norm or '__pycache__' in r_norm or '.git' in r_norm or 'node_modules' in r_norm:
            continue
            
        is_data_dir = 'data/dataset' in r_norm or 'tests/data' in r_norm

        for f in files:
            if f.endswith('.zip') or f.endswith('.db') or f == 'backend_small_2mb.zip': 
                continue
            
            file_path = os.path.join(r, f)
            
            if is_data_dir:
                if total_data_size > MAX_DATA_SIZE:
                    continue
                total_data_size += os.path.getsize(file_path)

            arcname = os.path.relpath(file_path, '.').replace('\\', '/')
            z.write(file_path, arcname)

add_dir('backend')

z.close()
print("Size:", os.path.getsize('backend_small_2mb.zip'))
