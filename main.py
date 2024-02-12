from flask import Flask, render_template, request, send_file
import os
import shutil
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/molst_form", methods=["POST", "GET"])
def molst_form():
    if request.method == "POST":
        print(request.form)
        # Create a BytesIO object to store the PDF content
        packet = io.BytesIO()

        # First page
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(40, 700, request.form["name"])
        can.drawString(300, 700, request.form["dob"])
        if request.form["gender"] == "male":
            can.drawString(463, 705, "X")
        else:
            can.drawString(513, 705, "X")
        dims = [575, 561, 547, 533, 519, 490, 476, 440]
        can.drawString(60, dims[int(request.form["1"]) - 1], "X")
        dims = [357, 207, 187, 143]
        can.drawString(85, dims[int(request.form["3"]) - 1], "X")
        can.drawString(120, 59, request.form["psign"])
        can.drawString(380, 59, request.form["pname"])
        can.drawString(120, 35, request.form["license"])
        can.drawString(350, 35, request.form["phone"])
        can.drawString(482, 35, request.form["date"])
        can.save()
        packet.seek(0)

        # Create a new BytesIO object for the second page
        packet_second_page = io.BytesIO()

        # Second page
        can_second_page = canvas.Canvas(packet_second_page, pagesize=letter)
        can_second_page.drawString(40, 740, request.form["name"])
        can_second_page.drawString(300, 740, request.form["dob"])
        if request.form["gender"] == "male":
            can_second_page.drawString(463, 736, "X")
        else:
            can_second_page.drawString(513, 736, "X")
        dims = [677,664,637,609]
        can_second_page.drawString(100, dims[int(request.form["5"]) - 1], "X")
        can_second_page.drawString(175, 650, request.form["timelimit1"])
        can_second_page.drawString(175, 623, request.form["timelimit2"])
        dims = [100,350]
        can_second_page.drawString(dims[int(request.form["6"]) - 1], 580, "X")
        dims = [(100,510),(345,539),(345,497)]
        can_second_page.drawString(dims[int(request.form["7"]) - 1][0],
                                   dims[int(request.form["7"]) - 1][1], "X")
        dims = [(100,442),(345,465),(345,425)]
        can_second_page.drawString(dims[int(request.form["8"]) - 1][0],
                                   dims[int(request.form["8"]) - 1][1], "X")
        dims = [(100,380),(100,352),(345,373),(345,345)]
        can_second_page.drawString(dims[int(request.form["9"]) - 1][0],
                                   dims[int(request.form["9"]) - 1][1], "X")
        dims = [(100,290),(100,248),(345,290),(345,235)]
        can_second_page.drawString(dims[int(request.form["10"]) - 1][0],
                                   dims[int(request.form["10"]) - 1][1], "X")
        can_second_page.drawString(175, 220, request.form["timelimit3"])
        can_second_page.drawString(425, 248, request.form["timelimit4"])
        dims = [(100,193),(345,206),(345,178)]
        can_second_page.drawString(dims[int(request.form["11"]) - 1][0],
                                   dims[int(request.form["11"]) - 1][1], "X")
        can_second_page.drawString(80, 150, request.form["otherorders"])
        can_second_page.drawString(425, 193, request.form["timelimit5"])
        can_second_page.drawString(120, 59, request.form["psign"])
        can_second_page.drawString(380, 59, request.form["pname"])
        can_second_page.drawString(120, 35, request.form["license"])
        can_second_page.drawString(350, 35, request.form["phone"])
        can_second_page.drawString(482, 35, request.form["date"])
        can_second_page.save()
        packet_second_page.seek(0)

        # Create a new BytesIO object for the third page
        # packet_third_page = io.BytesIO()

        # # Third page
        # can_third_page = canvas.Canvas(packet_third_page, pagesize=letter)
        # dims = [259,365,507]
        # can_third_page.setFontSize(10)
        # can_third_page.drawString(dims[int(request.form["12"]) - 1], 100, "X")
        # can_third_page.drawString(305, 78, request.form["name"])
        # can_third_page.drawString(345, 54, request.form["psign"])
        # can_third_page.drawString(330, 66, request.form["pname"])
        # can_third_page.drawString(500, 78, request.form["dob"])
        # can_third_page.drawString(500, 66, request.form["date"])
        # can_third_page.drawString(500, 54, request.form["phone"])
        # can_third_page.save()
        # packet_third_page.seek(0)

        # Merge the first, second, and third pages
        new_pdf = PdfFileReader(packet)
        new_pdf_second_page = PdfFileReader(packet_second_page)
        # new_pdf_third_page = PdfFileReader(packet_third_page)
        #/home/AmmarKhawaja/mysite/forms/molst_form.pdf for PythonAnywhere
        existing_pdf = PdfFileReader(open("./forms/molst_form.pdf", "rb"))

        output = PdfFileWriter()
        output.addPage(existing_pdf.pages[0])
        output.getPage(0).mergePage(new_pdf.getPage(0))
        output.addPage(existing_pdf.pages[1])
        output.getPage(1).mergePage(new_pdf_second_page.getPage(0))
        # output.addPage(existing_pdf.pages[2])
        # output.getPage(2).mergePage(new_pdf_third_page.getPage(0))

        #/home/AmmarKhawaja/mysite/forms/molst_form_M.pdf for PythonAnywhere
        with open("./forms/molst_form_M.pdf", "wb") as output_stream:
            output.write(output_stream)
        #/home/AmmarKhawaja/mysite/forms for PythonAnywhere
        return send_file(os.path.join("./forms", "molst_form_M.pdf"), as_attachment=True, download_name="molst_form.pdf")
    else:
        return render_template("molst_form.html")

if __name__ == "__main__":
    app.run(debug= True)
