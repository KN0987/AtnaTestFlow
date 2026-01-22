# How to build and run

cd /Users/youruser/Document/AtnaTestFlow  # adjust path if different  
python3 -m pip install -r requirements.txt  
python3 -m PyInstaller --onefile --windowed --name AtnaTestFlow main.py

# How to rebuild

cd /Users/khangnguyen/Document/AtnaTestFlow  
For Mac/Linux: rm -rf build dist AtnaTestFlow.spec  
For Window: Remove-Item -Recurse -Force build, dist, *.spec  
python3 -m PyInstaller --onefile --windowed --name AtnaTestFlow main.py
