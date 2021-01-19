# ssl-form-filler

This will automatically fill ssl forms from a google form.

Make sure you run ```pip install -r requirements.txt``` to have the required packages.

To start, download the google sheets form responses as a csv and place it in the sheets_data folder.

Next, place the SSL Template with the supervisor section (except for the hours part) filled out into the filled forms folder.

Make a file called config.json and place it in this folder. It should look this:

```json
{
  "sheets_mapping": {
    "[Field ID]": "[CSV Column Name]"
  },
  "template_name" : "./template_forms/[Name of initial supervisor form]",
  "csv_data" : "./sheets_data/[Name of Spreadsheet]",
  "school" : "[School as found in the dropdown in the ssl form",
  "date_start" : "[Start Date]",
  "date_end" : "[End Date]",
  "phone_number_column": "[Name of column in csv containing the phone number]",
  "total_hours_column": "[Name of column in csv containing the total hours completed]"

}
```

Fill in the values for the brackets. For the sheets_mapping, for every Field you want auto filled, use the pdf form field id and the column name in the csv.

To get the pdf form field id, run identify_fields.py. This will make a pdf called form-filled-numbered.pdf in the filled_forms folder. This pdf has the field filled with their id.

Run add_sign_field.py to add the signature box.

If you are configuring this for your own use (you want to change how this works), modify the logic in main.py.

If you want to flatten the pdf (make it no longer changeable), uncomment line 64 in main.py which is also shown below.
```python
# doc.FlattenAnnotations(True)
```

