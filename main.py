import json
import pandas
from PDFNetPython3.PDFNetPython import PDFDoc, Field, SDFDoc


with open('./config.json') as f:
    config = json.loads(f)

def fill_pdf(name, data, row_num, save_location):
    doc = PDFDoc(name)
    itr = doc.GetFieldIterator()
    while itr.HasNext():
        field = itr.Current()
        if (col := config['sheets_mapping'].get(field.GetName())) is not None:
            field.SetValue(str(data[col][row_num]))
        if field.GetName() == '42':
            field.SetValue(str(data['Timestamp'][row_num].split(' ')[0].split('/')[0]))
        if field.GetName() == '43':
            field.SetValue(str(data['Timestamp'][row_num].split(' ')[0].split('/')[1]))
        if field.GetName() == '44':
            field.SetValue(str(data['Timestamp'][row_num].split(' ')[0].split('/')[2]))
        if field.GetName() == '8':
            try:
                field.SetValue(str(data['Phone Number'][row_num]).split('-')[0])
            except IndexError:
                pass
        if field.GetName() == '9':
            try:
                field.SetValue(str(data['Phone Number'][row_num]).split('-')[1])
            except IndexError:
                pass
        if field.GetName() == '10':
            try:
                field.SetValue(str(data['Phone Number'][row_num]).split('-')[2])
            except IndexError:
                pass
        if field.GetName() == 'ALL SCHOOLS EXCEPT ELEMENTARY 9/2018':
            field.SetValue(config['school'])
        if field.GetName() == '30':
            field.SetValue(config['date_start'])
        if field.GetName() == '31':
            field.SetValue(config['date_end'])
        field.RefreshAppearance()
        itr.Next()

    doc_fields = doc.FDFExtract(PDFDoc.e_forms_only)
    doc.FDFMerge(doc_fields)

    doc.RefreshAnnotAppearances()
    #doc.FlattenAnnotations(True)

    doc.Save(save_location + data["FULL Name"][row_num].strip().replace(" ", "-") + "-SSL.pdf", SDFDoc.e_linearized)


sheets_data = pandas.read_csv(config['csv_data'])

for i in sheets_data.index:
    fill_pdf(config['form_template'], sheets_data, i, './filled_forms/')
