
import zipfile
import os
import tempfile
import shutil

def safe_extract(zip_ref, member, temp_dir):
    target_path = os.path.join(temp_dir, member.filename)
    target_folder = os.path.dirname(target_path)
    
    # Shorten each part of the directory path if it is too long
    parts = target_folder.split('/')
    for i in range(len(parts)):
        if len(parts[i]) > 100:
            parts[i] = parts[i][:100]
    new_folder = '/'.join(parts)
    
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    # Shorten the file name if it is too long
    file_name = os.path.basename(target_path)
    if len(file_name) > 100:
        file_name = file_name[:100]
        
    new_target_path = os.path.join(new_folder, file_name)
    
    with open(new_target_path, 'wb') as f:
        f.write(zip_ref.read(member))
    
    return new_target_path

def count_md_files_in_zip(zip_path, temp_dir):
    md_count = 0
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.infolist():
                if member.filename.endswith('/'):
                    continue  # skip directories
                try:
                    file_path = safe_extract(zip_ref, member, temp_dir)
                    print(f'Debug: File extracted to {file_path}')
                    if file_path.lower().endswith('.md'):
                        md_count += 1
                        print(f'Debug: .md file found ({file_path})')
                    elif file_path.lower().endswith('.zip'):
                        print(f'Debug: Nested ZIP file found ({file_path}), extracting...')
                        nested_temp_dir = tempfile.mkdtemp()
                        md_count += count_md_files_in_zip(file_path, nested_temp_dir)
                        shutil.rmtree(nested_temp_dir)
                        print(f'Debug: Removed temporary directory {nested_temp_dir}')
                except Exception as e:
                    print(f'Debug: An error occurred while processing {member.filename}: {e}')
    except Exception as e:
        print(f'Debug: An error occurred while opening the ZIP file: {e}')
    return md_count

def main(zip_path):
    # Create a temporary directory for extraction
    temp_dir = tempfile.mkdtemp()
    print(f'Debug: Temporary directory created at {temp_dir}')
    
    try:
        md_count = count_md_files_in_zip(zip_path, temp_dir)
        print(f'Number of .md files: {md_count}')
    finally:
        # Clean up by removing the temporary directory
        shutil.rmtree(temp_dir)
        print(f'Debug: Temporary directory {temp_dir} removed')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python count_md_files_nested_v4.py <path_to_zip_file>')
    else:
        main(sys.argv[1])
