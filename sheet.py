import gspread

string = "test"
gc = gspread.service_account()

# Open a sheet from a spreadsheet in one go
wks = gc.open("Global Database").sheet1

# Update a range of cells using the top left corner address
wks.insert_row(values=None, index=1)
wks.update('A1', [[1, string, 3], [4, 5, 6]])

# Or update a single cell
wks.update('B42', "it's down there somewhere, let me take another look.")

# Format the header
wks.format('A1:B1', {'textFormat': {'bold': True}})