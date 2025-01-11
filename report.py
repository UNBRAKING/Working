import sys
from pyrogram import Client, filters
import asyncio
import json
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import *


def get_reason(text):
    if text == "Report for child abuse":
        return InputReportReasonChildAbuse()
    elif text == "Report for impersonation":
        return InputReportReasonFake()
    elif text == "Report for copyrighted content":
        return InputReportReasonCopyright()
    elif text == "Report an irrelevant geogroup":
        return InputReportReasonGeoIrrelevant()
    elif text == "Reason for Pornography":
        return InputReportReasonPornography()
    elif text == "Report an illegal drug":
        return InputReportReasonIllegalDrugs()
    elif text == "Report for offensive person detail":
        return InputReportReasonPersonalDetails()
    elif text == "Report for spam":
        return InputReportReasonSpam()
    elif text == "Report for Violence":
        return InputReportReasonViolence()
    else:
        return None


async def main(message):
    config = json.load(open("config.json"))
    report_reason_text = message
    report_reason = get_reason(report_reason_text)
    
    if not report_reason:
        print("Invalid report reason provided.")
        return
    
    target = config['Target']
    
    for account in config["accounts"]:
        session_string = account["Session_String"]
        owner_name = account['OwnerName']
        
        async with Client(name="Session", session_string=session_string) as app:
            try:
                if target.startswith("https://"):
                    peer = await app.resolve_peer(target)
                    resolved_peer = InputPeerChannel(channel_id=peer.channel_id, access_hash=peer.access_hash)
                else:
                    peer = await app.resolve_peer(target)
                    resolved_peer = InputPeerUser(user_id=peer.user_id, access_hash=peer.access_hash)
                
                report_peer = ReportPeer(
                    peer=resolved_peer, 
                    reason=report_reason, 
                    message=report_reason_text
                )

                result = await app.invoke(report_peer)
                print(result, 'Reported by Account', owner_name)
            
            except Exception as e:
                print(f"Failed to report from {owner_name}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <reason>")
        sys.exit(1)

    input_string = sys.argv[1]
    asyncio.run(main(message=input_string))