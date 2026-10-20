# Voting Systems Alpha

This repository contains the `Voting_Systems_alpha.ipynb` notebook and the
local Python module, data files, and images it uses. Keep the notebook and the
`voting_functions.py`, `CVR files/`, and `SP images/` paths together as shown;
the notebook reads these files using relative paths.

## Open in Google Colab

[Open the notebook in Google Colab](https://colab.research.google.com/github/gmorre/Voting-Systems-alpha/blob/main/Voting_Systems_alpha.ipynb).
Sign in to Google if asked, select **Connect**, then choose **Runtime → Run
all**. The first cell downloads the supporting files and installs the required
packages. Some activities pause to ask for input; type an answer in the prompt
and press Enter. If you start a new Colab runtime later, run all cells again.

Colab runs a temporary copy. Changes students make there do not change this
GitHub repository. They can use **File → Save a copy in Drive** if they want
their own copy to keep working in.

## Run the notebook locally

1. Install Python 3.11 through 3.13 and JupyterLab.
2. From this repository folder, install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Start JupyterLab from this folder:

   ```bash
   jupyter lab
   ```

4. Open `Voting_Systems_alpha.ipynb` and run its cells. Some cells ask for
   input while running.

The notebook hides and locks code cells in compatible Jupyter interfaces.
This is only a display/editing convenience; the notebook source is still
available to anyone who downloads the file.
