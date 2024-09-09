
# ![logo1](https://github.com/user-attachments/assets/4fad5aaa-ca9e-4abb-8c0a-c3406a1fd790)

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-239120?style=for-the-badge&logoColor=white)](https://github.com/AlexRequiemd/CrimsonSimpleImageConverter?tab=MIT-1-ov-file)
![Status](https://img.shields.io/badge/Status-Developing-F38020?style=for-the-badge&logoColor=white)
[![MIT License](https://img.shields.io/badge/By-Alex_S._A._Rocha_Filho-D70A53?style=for-the-badge&logoColor=white)](https://github.com/AlexRequiemd)

***Crimson Simple Image Converter is an application for extracting images from PDF documents and converting them into various formats. It supports multiple languages and themes and allows for customization of the conversion process. This project uses Python and several libraries, including Pillow and customtkinter.***

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Files and Folders](#files-and-folders)
- [Libraries](#libraries)
- [Supported Formats](#supported-formats)
- [Setup](#setup)
  - [Install Dependencies](#install-dependencies)
  - [Folder Structure](#folder-structure)
  - [Installer](#installer)
- [Usage](#usage)
  - [User Interface](#user-interface)
  - [Change Language](#change-language)
  - [Conversion Settings](#conversion-settings)
- [Features by Tab](#features-by-tab)
- [Demonstration](#demonstration)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Releases](#releases)

## Features

- Extraction of images from PDF documents.
- Conversion of images into various formats.
- Support for multiple languages: English, Portuguese, and Spanish.
- Light and dark themes.
- Adjustable settings, including options for handling existing files.
- Graphical user interface using customtkinter.

## Architecture

### Files and Folders

- `data/`: Contains configuration and translation files.
  - `data.json`: General application settings.
  - `lang_eng.json`: Translations for English.
  - `lang_pt-br.json`: Translations for Portuguese.
  - `lang_spa.json`: Translations for Spanish.
- `language/`: Library responsible for managing languages and translations.
  - `__init__.py`: Initializes the language library.
- `app.py`: Main application file.

### Libraries

- **Pillow**: Used for image manipulation and conversion.
- **customtkinter**: Provides custom widgets for the graphical interface.
- **PikePDF**: Used for manipulating PDF documents.
- **json**: Standard library for handling JSON files.

## Supported Formats

### Input Formats

- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.ico`, `.webp`, `.tiff`, `.tif`, `.jp2`, `.j2k`, `.jfif`
- **PDF**: `.pdf`

### Output Formats

- **Images**: `.jpg`, `.png`, `.gif`, `.bmp`, `.webp`, `.ico`, `.tiff`, `.jp2`, `.pdf`, `.eps`

## Setup

### Install Dependencies

#### Make sure you have the following libraries installed:
+ **Pillow:** A library for image processing in Python, supporting various formats and basic manipulations.
+ **CustomTkinter:** An extension of Tkinter with modern, customizable widgets for graphical interfaces.
+ **PikePDF:** A tool for PDF manipulation, such as editing and encryption, based on QPDF.
+ **JSON:** A lightweight data exchange format; the json module converts between Python objects and JSON strings.

```bash
pip install pillow customtkinter pikepdf
```

## Installer
+ You can also install the application using the installer provided in the [Releases](https://github.com/AlexRequiemd/CrimsonSimpleImageConverter/releases) section of the repository. Download the installer from the latest release and follow the on-screen instructions to complete the installation.

## Folder Structure
### The project should have the following folder structure:

```plaintext
CrimsonSimpleImageConverter/
├── data/
│   ├── data.json
│   ├── lang_eng.json
│   ├── lang_pt-br.json
│   └── lang_spa.json
├── language/
│   └── __init__.py
└── app.py
```



## Usage
### Start the Application
Run the main file to start the application:

```bash
python app.py
```

## User Interface
### Input:
+ Add files or folders for extraction.
### Output: 
+ Set output options and select the output directory.
### Log: 
+ View the extraction and conversion log.
### Settings: 
+ Adjust application settings such as language and theme.
### About: 
+ Information about the application.

## Change Language
The language of the interface can be changed by modifying the data.json file to reflect the desired setting:

```json
"language": "pt-br"  // or "en" for English, "spa" for Spanish
```

## Conversion Settings
### Configure conversion options in the data.json file:

```json
"del_original": 0,  // 0: No, 1: Yes
"open_output": 0,   // 0: No, 1: Yes
"clean_input": 0,   // 0: No, 1: Yes
"finish_beep": 1,   // 0: No, 1: Yes
"finish_close": 0,  // 0: No, 1: Yes
"output_mode": 1,   // 1: Standard mode, 2: Alternative mode
"output_path": "",  // Output path
"replace_option": 0,  // 0: Ask, 1: Replace, 2: Ignore, 3: Rename
"format_option": 2   // 0: Standard format, 1: Alternative format, 2: Other format
```
## Features by Tab
### Input Tab
#### Add Files/Folder: 
+ Load images or PDFs for extraction.
#### Clear: 
+ Remove selected files or folders from the list.
#### Start: 
+ Begin the extraction and conversion process.
### Output Tab
#### Output Directory: 
+ Select where to save the converted images.
### Options: 
+ Configure settings for handling output, such as whether to ask, replace, ignore, or rename existing files.
### Log Tab
#### View Log: 
+ Access detailed logs of the extraction and conversion process.
### Settings Tab
#### Language: 
+ Change the language of the application.
#### Theme: 
+ Switch between light and dark themes.
### About Tab
#### Information: 
+ View details about the application, including version and author information.
## Demonstration
### Check out the demonstration video of the application:

<a href="https://youtu.be/gGpC1T5b-9w?si=u5Ohcwx7SsjfnIbz" target="_blank" rel="noopener noreferrer"> 
<img src="https://github.com/user-attachments/assets/497e94d9-79ee-4382-92bd-9c4327c5c784" style="height: 338px; width:603px;"/>
</a>


### Screenshots
+ Here are some screenshots of the application:

<img src="https://github.com/user-attachments/assets/aaac4fd4-2dc7-4ec7-8f99-91d831005a9d" style="height: 250px; width:427px;"/>

<img src="https://github.com/user-attachments/assets/65a2720d-7c60-410d-bf40-1c277ad467d2" style="height: 250px; width:427px;"/>

<img src="https://github.com/user-attachments/assets/4423cbe7-36b0-4183-a4fa-9bb2faae80fe" style="height: 250px; width:427px;"/>

<img src="https://github.com/user-attachments/assets/fc135143-c1e1-4066-a2d2-8f2b12a40169" style="height: 250px; width:427px;"/>

<img src="https://github.com/user-attachments/assets/e32ff39f-8790-422f-9194-019d08e34316" style="height: 250px; width:427px;"/>

####

<img src="https://github.com/user-attachments/assets/d55bc7de-8975-4d2a-add5-0daeae2c6684" style="height: 216px; width:384px;"/>

####

<img src="https://github.com/user-attachments/assets/ac91f822-a9ae-48da-b33a-c1239e7f4c69" style="height: 216px; width:384px;"/>


## Contributing
### Contributions are welcome! If you would like to contribute to the project, please follow these steps:

+ Fork the repository.
+ Create a branch for your feature or fix: git checkout -b my-new-feature.
+ Commit your changes: git commit -am 'Add new feature'.
+ Push your branch to the remote repository: git push origin my-new-feature.
+ Open a Pull Request for review.

## License
#### This project is licensed under the [*MIT License*](https://github.com/AlexRequiemd/CrimsonSimpleImageConverter?tab=MIT-1-ov-file).

## Releases
#### *You can download the installer from the [*Releases*](https://github.com/AlexRequiemd/CrimsonSimpleImageConverter/releases) section of the repository.*