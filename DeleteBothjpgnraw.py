import os
from tqdm import tqdm

# Define the folder path
folder_path = input("Please enter the folder path: ")

# Get the user's selected camera brand
camera_brand = input("Please enter the camera brand (e.g., Canon, Nikon, Sony, Fujifilm, Olympus, Panasonic, Pentax): ")

# Determine the raw format suffix based on the camera brand
raw_formats = {
    "Canon": [".CR2", ".CR3"],
    "Nikon": [".NEF"],
    "Sony": [".ARW"],
    "Fujifilm": [".RAF"],
    "Olympus": [".ORF"],
    "Panasonic": [".RW2"],
    "Pentax": [".PEF"]
}

# Get input for any other raw format suffixes the user wants to handle
other_raw_formats_input = input("Are there any other raw format suffixes that need to be handled? (Y/N): ").upper()
if other_raw_formats_input == "Y":
    other_raw_formats = input("Please enter other raw format suffixes, separated by commas: ").split(",")
    # Check if the camera brand exists; if not, create a new list
    if camera_brand in raw_formats:
        raw_formats[camera_brand].extend(other_raw_formats)
    else:
        raw_formats[camera_brand] = other_raw_formats

# Initialize dictionaries to store jpg and raw format files
jpg_files = {}
raw_files = {}

# Traverse through the files in the folder
for filename in os.listdir(folder_path):
    # Get the full path of the file
    file_path = os.path.join(folder_path, filename)

    # Check if the file is a regular file
    if os.path.isfile(file_path):
        # Split the file name and file format
        name, extension = os.path.splitext(filename)

        # Add the file to the respective dictionary
        if extension.lower() == ".jpg":
            jpg_files[name] = True
        elif extension.upper() in raw_formats[camera_brand]:
            raw_files[name] = True

# Let the user choose whether to keep .jpg or raw format files from the camera
keep_jpg = input("Do you want to keep .jpg files? (Y/N): ").upper() == "Y"

# Delete .jpg files or raw format files
if not keep_jpg:
    print("Deleting .jpg files...")
    for filename in tqdm(jpg_files.keys()):
        jpg_file_path = os.path.join(folder_path, filename + ".jpg")
        if os.path.exists(jpg_file_path):
            os.remove(jpg_file_path)
else:
    print("Deleting raw format files...")
    for filename in tqdm(raw_files.keys()):
        for ext in raw_formats[camera_brand]:
            raw_file_path = os.path.join(folder_path, filename + ext)
            if os.path.exists(raw_file_path):
                os.remove(raw_file_path)

# Output the results
if not keep_jpg:
    print("The folder retains raw format files:")
    for filename in raw_files:
        for ext in raw_formats[camera_brand]:
            print(filename + ext)
else:
    print("The folder retains .jpg files:")
    for filename in jpg_files:
        print(filename + ".jpg")

# Count the number of kept files
num_kept_files = len(raw_files) if not keep_jpg else len(jpg_files)
print("\nThe number of files kept: ", num_kept_files)
