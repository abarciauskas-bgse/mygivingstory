from openpyxl import load_workbook
import numpy as np

wb = load_workbook('data/MyGivingStory_Data_for_DataKind_Merged.xlsx')
print wb.get_sheet_names()

ws = wb.get_sheet_by_name('CLEAN DATA')
A = np.array([[i.value for i in j] for j in ws.rows])

columns = A[0,:]
story_text_column_idx = np.argwhere(columns == 'Story_Text')[0]
data = np.array(A[range(1,A.shape[0]),:])
documents = [data.item((i,story_text_column_idx)) for i in range(data.shape[0])]
