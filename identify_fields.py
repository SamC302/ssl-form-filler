import json
from PDFNetPython3.PDFNetPython import PDFDoc, Field, SDFDoc


with open('./config.json') as f:
    config = json.loads(f.read())

def fill_pdf(name,save_location):
    doc = PDFDoc(name)
    itr = doc.GetFieldIterator()
    while itr.HasNext():
        field = itr.Current()
        field.SetValue(field.GetName())
        field.RefreshAppearance()
        itr.Next()

    doc_fields = doc.FDFExtract(PDFDoc.e_forms_only)
    doc.FDFMerge(doc_fields)

    doc.RefreshAnnotAppearances()

    doc.Save(save_location + "form-field-numbered.pdf", SDFDoc.e_linearized)


fill_pdf(config['form_template'],'./filled_forms/')
