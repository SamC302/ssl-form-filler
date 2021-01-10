import json
from PDFNetPython3.PDFNetPython import PDFDoc, TextWidget, Field, Rect, Font, SDFDoc

with open('./config.json') as f:
    config = json.loads(f)

doc = PDFDoc(config['template_name'])
blank_page = doc.GetPage(1)

text_field = doc.FieldCreate("45", Field.e_text, "")
text = TextWidget.Create(doc, Rect(210, 97, 480, 106), text_field)
text.SetFont(Font.Create(doc.GetSDFDoc(), Font.e_times_bold))
text.RefreshAppearance()
blank_page.AnnotPushBack(text)
doc.Save('./'+config['template_name'].strip('.pdf')+'_New.pdf',SDFDoc.e_linearized)
