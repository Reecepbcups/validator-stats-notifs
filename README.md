# validator-stats-notifs
### Built for Oni Validator

### Steps to Run
```bash
cp secrets.example.json secrets.json
# Update WEBHOOK_URL, and your OPERATOR_ADDRESSES (oni by default)
python -m pip install -r requirements/requirements.txt
python src/validator-stats.py

OR

bash run.sh
# auto git pull latest, git intall requirements, and run
```


### If you want graphs
```
# Arch
sudo pacman -S docker
systemctl start docker
systemctl enable docker

cd validator-stats-notifs
bash run_docker.sh
```