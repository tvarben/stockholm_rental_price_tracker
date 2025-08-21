python3 -m venv venv
source venv/bin/activate #on windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install-deps #only for linux
playwright install
