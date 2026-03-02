import pandas as pd

def gst_mismatch(gst_3b_path, gst_2a_path):
    gst_3b=pd.read_csv(gst_3b_path)
    gst_2a=pd.read_csv(gst_2a_path)

    total_3b=gst_3b["taxable_value"].sum()
    total_2a=gst_2a["taxable_value"].sum()

    mismatch_percent = abs(total_3b - total_2a) / total_3b * 100

    return {
        "gst_3b": total_3b,
        "gst_2a": total_2a,
        "mismatch_percent": mismatch_percent,
        "risk": mismatch_percent > 15
    }


def bank_vs_gst(bank_path, gst_3b_total):
    bank=pd.read_csv(bank_path)
    total_credit = bank[bank["type"]=="credit"]["amount"].sum()

    return {
        "bank_credit": total_credit,
        "gst_sales": gst_3b_total,
        "risk": total_credit<gst_3b_total
    }