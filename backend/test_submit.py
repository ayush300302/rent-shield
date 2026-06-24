"""Test script for the /submit endpoint with PDF file upload."""
import urllib.request
import json

pdf_path = r"c:\Users\siddp\Downloads\rent-shieldd\backend\test_offer.pdf"

boundary = "----BOUNDARY123456"
crlf = b"\r\n"

body = b""
# Add document_type field
body += b"------BOUNDARY123456" + crlf
body += b'Content-Disposition: form-data; name="document_type"' + crlf + crlf
body += b"offer_letter" + crlf

# Add file field
body += b"------BOUNDARY123456" + crlf
body += b'Content-Disposition: form-data; name="file"; filename="test_offer.pdf"' + crlf
body += b"Content-Type: application/pdf" + crlf + crlf
with open(pdf_path, "rb") as f:
    body += f.read()
body += crlf
body += b"------BOUNDARY123456--" + crlf

req = urllib.request.Request(
    "http://127.0.0.1:8000/submit",
    data=body,
    headers={"Content-Type": "multipart/form-data; boundary=----BOUNDARY123456"},
)

try:
    r = urllib.request.urlopen(req)
    result = json.loads(r.read().decode())
    print("=== /submit PDF Upload Test ===")
    print(json.dumps(result, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()}")
