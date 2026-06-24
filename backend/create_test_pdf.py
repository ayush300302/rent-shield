"""Create a simple test PDF with text content for testing the /submit endpoint."""
from reportlab_alternative import create_test_pdf
import os

# Simple approach: write raw PDF bytes
pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_offer.pdf")

# Minimal valid PDF with text
pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj

2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj

3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]
   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj

4 0 obj
<< /Length 187 >>
stream
BT
/F1 12 Tf
72 700 Td
(Google India Private Limited) Tj
0 -20 Td
(Offer of Employment - Software Engineer) Tj
0 -20 Td
(Annual CTC: INR 15,00,000 - Fifteen Lakhs Per Annum) Tj
0 -20 Td
(Salary: 15 LPA) Tj
ET
endstream
endobj

5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj

xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000266 00000 n 
0000000505 00000 n 

trailer
<< /Size 6 /Root 1 0 R >>
startxref
574
%%EOF
"""

with open(pdf_path, "wb") as f:
    f.write(pdf_content)

print(f"Test PDF created at: {pdf_path}")
