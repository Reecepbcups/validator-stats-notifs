# validator-stats-notifs
### Built for Oni Validator

### Steps to Run
```bash
cp secrets.example.json secrets.json
# Update WEBHOOK_URL, and your OPERATOR_ADDRESSES (oni by default)

python -m pip install -r requirements/requirements.txt

python src/validator-stats.py
```