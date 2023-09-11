import zipfile
import os
import tempfile
import shutil

def safe_shorten_and_add(zip_out, zip_ref, member, temp_dir):
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
    
    # Extract and write to new zip
    with open(new_target_path, 'wb') as f:
        f.write(zip_ref.read(member))
    
    zip_out.write(new_target_path, new_target_path[len(temp_dir)+1:])

def repackage_zip_with_short_names(input_zip_path, output_zip_path):
    try:
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(input_zip_path, 'r') as zip_ref, zipfile.ZipFile(output_zip_path, 'w') as zip_out:
            for member in zip_ref.infolist():
                if member.filename.endswith('/'):
                    continue  # skip directories
                safe_shorten_and_add(zip_out, zip_ref, member, temp_dir)
    except Exception as e:
        print(f"An error occurred while opening or creating the ZIP file: {e}")
    finally:
        # Clean up by removing the temporary directory
        shutil.rmtree(temp_dir)

# Example usage
if __name__ == "__main__":
    input_zip_path = "long.zip"
    output_zip_path = "short.zip"
    repackage_zip_with_short_names(input_zip_path, output_zip_path)
