from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in the environment.")
TABLE_NAME = "Messages"
REQUIRED_AMOUNT = 100  

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def verify_payment(txid, required_amount=REQUIRED_AMOUNT):
    # Look up the transaction by TxID
    db_result = supabase.table(TABLE_NAME).select('*').eq('txid', txid).execute()
    if not db_result.data or len(db_result.data) == 0:
        return {"status": "not_approved", "message": "Payment is not approved."}
    
    transaction = db_result.data[0]
    # Extract amount (assume format like '7000 RWF')
    amount_str = transaction.get('amount', '').replace(' RWF', '').replace(',', '').strip()
    try:
        paid_amount = int(amount_str)
    except Exception:
        return {"status": "not_approved", "message": "Payment is not approved (invalid amount format)."}
    
    if paid_amount == required_amount:
        return {"status": "approved", "message": "Payment is approved."}
    elif paid_amount < required_amount:
        shortage = required_amount - paid_amount
        return {"status": "not_approved", "message": f"Payment is not approved. You are short by {shortage} RWF."}
    else:
        return {"status": "approved", "message": "Payment is approved."}
