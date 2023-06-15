# Selenium_gitlab_automation
An project use Selenium to auto generate gitlab test case 



### WHAT THIS PROJECT FOR


1. Help QA to create testcase for IPTP's Gitlab issues automatic
3. Help QA update test issues and original issues automatic


# How to run it

## Setup

- Install virtualenv (optional)
```bash
python3 -m virtualenv .   
```
- Init venvironment
```bash
virtualenv venvironment 
```
- If error on use file .ps1, then run:
```bash
set-executionpolicy remotesigned
```
- Activate environment
```bash
Scripts\activate
```
- Install from [requirements.txt](requirements.txt)
```bash
pip install -r requirements.txt
```

## Run
- Run pytest on file [rpa_gitlab_qa.py](rpa_gitlab_qa.py)
```bash
pytest .\rpa_gitlab_qa.py
```


### What is included on this template?

- 🖼️ Libraries:
  * **Selenium**, Selenium with Python [link](https://selenium-python.readthedocs.io/index.html)
  * **PyAutoGUI**, PyAutoGUI’s documentation! [link](https://pyautogui.readthedocs.io/en/latest/)
  * **python-dotenv** python-dotenv [link](https://pypi.org/project/python-dotenv/)
  * **pytest** pytest [link](https://docs.pytest.org/en/7.3.x/)
  * **openpyxl** A Python library to read/write Excel 2010 xlsx/xlsm files [link](https://openpyxl.readthedocs.io/en/stable/)