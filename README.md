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

# ensure you allow the firewall to port 722
# (to change port, edit run_docker.sh & default.conf)

cd validator-stats-notifs
bash run_docker.sh
```

### Missing a chain you want?
make a PR to the following module
```
https://github.com/Reecepbcups/python-ibc
src -> pyibc_api -> chain_apis -> CHAIN_APIS dict

Will move to cosmos.directory in the future, hardcoded for now
```