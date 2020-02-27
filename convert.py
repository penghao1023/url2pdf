from xlrd import open_workbook
from json import dump


if __name__ == '__main__':
    workbook = open_workbook('work-final.xlsx')
    sheet = workbook.sheet_by_index(0)
    dump({str(name.value): ' '.join(sheet.col_values(index, 1)).split() for index, name in enumerate(sheet.row(0))},
         open('source.json', 'w'), ensure_ascii=False)

