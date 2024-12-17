import os
import zipfile
import requests
import shutil

# Base URL Structure
base_url = "https://lazyfoo.net/tutorials/SDL/"
# test_zip_url = [
#     "https://lazyfoo.net/tutorials/SDL/02_getting_an_image_on_the_screen/02_getting_an_image_on_the_screen.zip",
#     "https://lazyfoo.net/tutorials/SDL/17_mouse_events/17_mouse_events.zip"]


code_folder="src"
resources_folder="resources" # Images, sounds, etc, anything that is not a .cpp file
output_folder="output" 

# Get all zip files in the output folder
zip_files = [os.path.join(output_folder, file) for file in os.listdir(output_folder) if file.endswith(".zip")]

# Get all zip files to download
response = requests.get(base_url)
html = response.text
# zip_files = [base_url + line.split('"')[1] for line in html.split("\n") if ".zip" in line]

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Download all zip files
def download_zip_files(url,output_path):
    '''Download zip files from the given URL'''
    path = os.path.join(output_path,url.split("/")[-1])
    downloaded_successfully = False
    try:
        print("Downloading: ", url)
        response = requests.get(url)
        response.raise_for_status()
        with open(path ,"wb") as file:
            file.write(response.content)
        downloaded_successfully = True
        print("Downloaded: ", url)
    except requests.exceptions.RequestException as e:
        print(f"Error in downloading the url {url}: {e}")
    return path,downloaded_successfully

def unzip_files(zip_file_path,output_folder):
    '''Unzip the zip files'''
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
        print(f"Unzipped the file {zip_file_path}")
    except Exception as e:
        print(f"Error in unzipping the file {zip_file_path}: {e}")
        
def clean_unzipped_files(unzip_folder_path):
    '''
    Copy *.cpp files source folder.
    Delete readme.txt file, and copy other files into to source folder
    Copy other files to resources folder
    '''
    src_path = os.path.join(output_folder,code_folder)
    if not os.path.exists(src_path):
        os.mkdir(src_path)
        
    resources_path = os.path.join(output_folder,resources_folder)
    if not os.path.exists(resources_path):
        os.mkdir(resources_path)
    
    for root, _, files in os.walk(unzip_folder_path):
        for file in files:
            # handle .cpp files
            if file.endswith(".cpp"):
                # copy .cpp files to source folder
                src_cpp_file = os.path.join(root,file)
                dest_file = os.path.join(src_path,file)
                if not os.path.exists(dest_file):
                    os.rename(src_cpp_file,dest_file)
                # shutil.copy(src_file,dest_file)
            elif file.endswith(".txt"):
                os.remove(os.path.join(root,file))
            else:
                src_resource_file = os.path.join(root,file)
                dest_file = os.path.join(resources_path,file)
                if not os.path.exists(dest_file):
                    os.rename(src_resource_file,dest_file)

    # Remove the unzipped folder/and zip file
    #os.remove(unzip_folder_path)
    # os.removedirs(unzip_folder_path)
    shutil.rmtree(unzip_folder_path)
    os.remove(unzip_folder_path+".zip")

def main():
    '''Main function to download all zip files'''
    for url in zip_files:
        # uncomment for downloading zip files with url
        # result = download_zip_files(url,output_folder)
        result = url,True
        if (result[1]):
            unzip_files(result[0],output_folder)
            clean_unzipped_files(os.path.splitext(result[0])[0])
    print("All zip files downloaded successfully")
    
if __name__ == "__main__":
    main()





