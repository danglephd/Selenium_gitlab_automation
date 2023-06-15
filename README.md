# Selenium_gitlab_automation
An project use Selenium to auto generate gitlab test case 



### WHAT THIS PROJECT FOR


1. Help QA to create testcase for IPTP's Gitlab issues automatic
3. Help QA update test issues and original issues automatic


# How to run it

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

### What is included on this template?

- 🖼️ Templates for starting multiple application types:
  * **Basic low dependency** Python program (default) [use this template](https://github.com/rochacbruno/python-project-template/generate)
  * **Flask** with database, admin interface, restapi and authentication [use this template](https://github.com/rochacbruno/flask-project-template/generate).