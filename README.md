# simu_it_aging
Simulate the carbon impact of IT depending on the speed of replacement

## To install it
```
python3 -m venv venv
source venv/bin/activate

pip install -r requierements.txt
```

## To run it
```
python app.py
```

Then connect to 127.0.0.1:8050 using your favorite web browser

## To do list
- [ ] Add other parameters than only carbon (aka water + adp)
- [ ] link to boavista or resilio to simulate actual system or compute embedded footprint from hardware configuration
- [ ] Explain how efficiency is computed from the notebook
- [ ] insure that we are actually computing the SCI
