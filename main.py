import json
import pandas
from PDFNetPython3.PDFNetPython import PDFDoc, Field, SDFDoc
from math import floor

with open('./config.json') as f:
    config = json.loads(f.read())


def myround(x, prec=2, base=.5):
    return round(base * round(float(x) / base), prec)


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

        if {i for i in list(str(data[config['phone_number_column']][row_num]))} - {*[str(i) for i in range(10)], '-'} != set():
            print(f"There can only be dashes and numbers in the phone number. Row {row_num+1} violates this. It will be skipped.")
            return
        dash_count = sum([1 if i == '-' else 0 for i in str(data[config['phone_number_column']][row_num])])
        if dash_count != 2 and dash_count != 0:
            print(f"The phone number entered for row {row_num+1} has an inconsistent amount of dashes. It either needs 2 or none. This row is being skipped.")
            return
        if dash_count == 0 and len(str(data[config['phone_number_column']][row_num])) != 10:
            print(f"The phone number entered for row {row_num+1} is in the numbers-only format but does not have 10 digits. It will be skipped.")
            return
        if field.GetName() == '8':
            try:
                field.SetValue(str(data[config['phone_number_column']][row_num]).split('-')[0])
            except IndexError:
                field.SetValue(str(data[config['phone_number_column']][row_num])[:3])
        if field.GetName() == '9':
            try:
                field.SetValue(str(data[config['phone_number_column']][row_num]).split('-')[1])
            except IndexError:
                field.SetValue(str(data[config['phone_number_column']][row_num])[3:7])
        if field.GetName() == '10':
            try:
                field.SetValue(str(data[config['phone_number_column']][row_num]).split('-')[2])
            except IndexError:
                field.SetValue(str(data[config['phone_number_column']][row_num])[7:])
        if field.GetName() == 'ALL SCHOOLS EXCEPT ELEMENTARY 9/2018':
            field.SetValue(config['school'])
        if field.GetName() == '30':
            field.SetValue(config['date_start'])
        if field.GetName() == '31':
            field.SetValue(config['date_end'])
        if field.GetName() == '32':
            field.SetValue(str(floor(int(data[config['total_hours_column']][row_num]) / 8) + 1))
        if field.GetName() == '33':
            total_days = floor(int(data[config['total_hours_column']][row_num]) / 8) + 1
            if total_days == 1:
                field.SetValue(str(data[config['total_hours_column']][row_num]))
            else:
                field.SetValue(str(myround(data[config['total_hours_column']][row_num]/total_days)))

        field.RefreshAppearance()
        itr.Next()

    doc_fields = doc.FDFExtract(PDFDoc.e_forms_only)
    doc.FDFMerge(doc_fields)

    doc.RefreshAnnotAppearances()
    # doc.FlattenAnnotations(True)

    doc.Save(save_location + data["FULL Name"][row_num].strip().replace(" ", "-") + "-SSL.pdf", SDFDoc.e_linearized)


sheets_data = pandas.read_csv(config['csv_data'])

for i in sheets_data.index:
    fill_pdf(config['template_name'].rstrip(".pdf") + "_New" + ".pdf", sheets_data, i, './filled_forms/')
