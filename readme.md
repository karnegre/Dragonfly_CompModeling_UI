## Multi-Composite Modeling UI
Updated: 2021.18.11

Beta 1.0 now available for testing: [Multi-Composite Spectra Modeling UI](https://share.streamlit.io/karnegre/dragonfly_compmodeling_ui/main/app.py).

The user-interface (UI) was developed using Streamlit. The UI is intended for [Dragonfly](https://dragonfly.jhuapl.edu/) team use as a modeling aid for determining the surface composition of Saturn's moon, Titan. 

Models used include an intimate mixing model using the [Shkuratov model](https://www.sciencedirect.com/science/article/pii/S0019103598960353) and a linear mixing model using compound reflectance spectra.

## Installation

**Note: You only need to install Dragonfly_CompModeling_UI if you want to contribute or run it 
locally. If you just want to use it, go [here](https://share.streamlit.io/karnegre/dragonfly_compmodeling_ui/main/app.py).**

```bash
git clone https://github.com/karnegre/Dragonfly_CompModeling_UI.git
cd Dragonfly_CompModeling_UI
pip install -r requirements.txt
```
## Running locally

```bash
streamlit run app.py
```
## Using the Models
tbd

## Instructions for Uploading Data
There are two sets of instructions for prepping the data; one for uploading optical constant data and the other for reflectance spectra data
### Data Preparation
1. Prepping your Optical Constant Data
    - Copy and paste data into Notepad
    - Data must be in the following format:
   
     ![This is an image](Format.JPG)
   
        - wave column contains the wavelength domain (micron)
        - n column contains the refractive indexes
        - k column contains the extinction coefficients
       
    - Save the file as the name of the compound and as a .txt file
2. Prepping your Reflectance Data
    - Copy and paste data into Notepad
    - Data must be in the following format:
   
     ![This is an image](Format2.JPG)
   
        - wave column contains the wavelength domain (micron)
        - r column contains the albedo 
       
    - Save the file as the name of the compound and as a .txt file
### Data Upload
Head to the app [Multi-Composite Spectra Modeling UI](https://share.streamlit.io/karnegre/dragonfly_compmodeling_ui/main/app.py) and complete the form under the Upload Data tab