## Multi-Composite Modeling UI
Beta 0.1 now available for testing: [Multi-Composite Spectra Modeling UI](https://share.streamlit.io/karnegre/dragonfly_compmodeling_ui/main/app.py).

The user-interface (UI) was developed using Streamlit. The UI is intended for [Dragonfly](https://dragonfly.jhuapl.edu/) team use as a modeling aid for determining the surface composition of Saturn's moon, Titan. 

Models used include an intimate mixing using the [Shkuratov model](https://www.sciencedirect.com/science/article/pii/S0019103598960353) and a linear mixing model using compound reflectance spectra.

## Installation

**Note: You only need to install Traingenerator if you want to contribute or run it 
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


