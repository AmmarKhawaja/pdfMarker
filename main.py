from flask import Flask, render_template, request, send_file, session
import os
import shutil
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from secret import SECRET_KEY
import base64
from datetime import datetime

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = 'signatures'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

@app.route("/", methods=["POST", "GET"])
def home():
    if not session.get("P_NAME"):
        session["P_NAME"] = " "
    if not session.get("P_PHONE"):
        session["P_PHONE"] = " "
    if not session.get("P_LICENSE"):
        session["P_LICENSE"] = " "
    if not session.get("P_SIGN"):
        session["P_SIGN"] = " "
    if session.get("P_NAME"):
            # /home/AmmarKhawaja/mysite/signatures/
            matching_files = [file for file in os.listdir("./signatures/") if file.startswith(session.get("P_NAME"))]
            if len(matching_files) > 0:
                session["P_SIGN"] = matching_files[0]

    if request.method == "POST":
        print(request.form)
        session["P_NAME"] = (request.form["P_name"])
        session["P_PHONE"] = (request.form["P_phone"])
        session["P_LICENSE"] = (request.form["P_license"])
        file = request.files['P_sign']
        if file:
            if len(session.get("P_NAME")) > 5:
                filename = session.get("P_NAME") + "|" + file.filename.replace("|", "")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                session['P_SIGN'] = filename

    return render_template("index.html")

@app.route("/molst_form", methods=["POST", "GET"])
def molst_form():
    if request.method == "POST":
        
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
        # can.drawString(120, 59, request.form["psign"])
        # /home/AmmarKhawaja/mysite/signatures/
        can.drawImage("signatures/" + session.get("P_SIGN"), 120, 59, 50, 15)
        can.drawString(380, 59, request.form["pname"])
        can.drawString(120, 35, request.form["license"])
        can.drawString(350, 35, request.form["phone"])
        can.drawString(482, 35, request.form["date"])
        can.save()
        packet.seek(0)

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
        # can_second_page.drawString(120, 59, request.form["psign"])
        # /home/AmmarKhawaja/mysite/signatures/
        can_second_page.drawImage("signatures/" + session.get("P_SIGN"), 120, 59, 50, 15)
        can_second_page.drawString(380, 59, request.form["pname"])
        can_second_page.drawString(120, 35, request.form["license"])
        can_second_page.drawString(350, 35, request.form["phone"])
        can_second_page.drawString(482, 35, request.form["date"])
        can_second_page.save()
        packet_second_page.seek(0)

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
        return render_template("molst_form.html", 
                               P_NAME=session.get("P_NAME"), 
                               P_PHONE=session.get("P_PHONE"), 
                               P_LICENSE=session.get("P_LICENSE"), 
                               DATE=datetime.now().strftime("%m/%d/%Y"))
    
@app.route("/certification_form", methods=["POST", "GET"])
def certification_form():
    if request.method == "POST":
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        if "1" in request.form:
            can.drawString(95, 755, request.form.get("1",""))
            can.drawString(270, 645, request.form.get("1",""))
        if "0" in request.form:
            can.drawString(415, 750, request.form["0"])
        can.drawString(425, 50, request.form["25"])
        role_status = [(274,630),(396,630),(137,620)]
        if "practitionerRole" in request.form:
            role = role_status[int(request.form["practitionerRole"]) - 1]
            can.drawString(role[0], role[1], "X")
        if "2" in request.form:
            can.drawString(108, 595, "X")
        dims_general_status = [515, 445, 363]
        if "3" in request.form:
            can.drawString(48, dims_general_status[int(request.form["3"]) - 1], "X")
        if "4" in request.form:
            can.drawString(84, 295, "X")
        if "5" in request.form:
            can.drawString(65, 252, "X")
        if "6" in request.form:
            can.drawString(112, 252, "X")
        if "7" in request.form:
            can.drawString(307, 252, "X")
        if "8" in request.form:
            can.drawString(402, 250, "X")
        if "9" in request.form:
            can.drawString(480, 248, "X")
        if "10" in request.form:
            can.drawString(65, 238, "X")
        if "11" in request.form:
            can.drawString(154, 238, "X")
        if "12" in request.form:
            can.drawString(266, 238, "X")
        if "13" in request.form:
            can.drawString(370, 238, "X")
            can.drawString(420, 237, "Dialysis")
        if "14" in request.form and len(request.form["14"]):
            can.drawString(370, 238, "X")
            can.drawString(420, 237, request.form.get("14",""))
        if "15" in request.form:
            can.drawString(126, 198, "X")
        if "16" in request.form:
            can.drawString(254, 198, "X")
        dims_decision = [142, 127]
        valid = True
        if "17" in request.form:
            can.drawString(80, dims_decision[int(request.form["17"]) - 1], "X")
            valid = False
        if "19" in request.form:
            can.drawString(245, 105, "X")
            valid = True
        if "20" in request.form:
            can.drawString(316, 105, "X")
            valid = True
        if "21" in request.form:
            can.drawString(399, 102, "X")
            valid = True
        if "22" in request.form:
            can.drawString(478, 99, "X")
            valid = True
        if "23" in request.form and len(request.form["23"]):
            can.drawString(80, 87, "X")
            can.drawString(130, 87, request.form.get("23",""))
            if request.form.get("23","") != "":
                valid = True
        if not valid:
            return "Did not fill in Diagnosis of reason for incapacity."
        can.drawImage("signatures/" + session.get("P_SIGN"), 120, 45, 50, 15)
        can.save()
        packet.seek(0)
        existing_pdf = PdfFileReader(open("./forms/certification_form.pdf", "rb"))
        new_pdf = PdfFileReader(packet)
        output = PdfFileWriter()
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        with open("./forms/certification_form_M.pdf", "wb") as out:
            output.write(out)
        return send_file("./forms/certification_form_M.pdf", as_attachment=True, download_name="certification_form.pdf")
    else:
        return render_template("certification_form.html", DATE=datetime.now().strftime("%m/%d/%Y"))

if __name__ == "__main__":
    app.run(debug= True)
