import os
import re
from sqlalchemy import Boolean, Date, Integer, Numeric
from decimal import Decimal
from datetime import date
import model

def db_import_file(engine, table_class, fname, col_order):
    with open(fname) as f:
        rows = []
        for line in f:
            values = line.split('^')
            row = {}
            for ind in range(len(col_order)):
                col_name = col_order[ind]
                col_value = None
                wrapped_value = values[ind].strip().decode('windows-1252')
                match = re.match('[~]{0,1}([^~]*)[~]{0,1}', wrapped_value)
                if match:
                    col_value = match.group(1)
                else:
                    if len(wrapped_value):
                        raise ValueError(
                            "Unexpected value, '{}'; regular expression did not match line:\n{}.".format(
                                wrapped_value, line))

                if type(table_class.__dict__[col_name].type) is Integer:
                    if col_value == '':
                        col_value = None
                    else:
                        col_value = int(col_value)

                if type(table_class.__dict__[col_name].type) is Numeric:
                    if col_value == '':
                        col_value = None
                    else:
                        col_value = Decimal(col_value)

                if type(table_class.__dict__[col_name].type) is Date:
                    match_date = re.match('([\d]{2})/([\d]{4})', col_value)
                    if match_date:
                        month = match_date.group(1)
                        year = match_date.group(2)
                        col_value = date(int(year), int(month), 1)
                    else:
                        col_value = None

                if type(table_class.__dict__[col_name].type) is Boolean:
                    if (col_value.upper() == 'N'
                            or col_value == '0'
                            or not col_value):
                        col_value = False
                    else:
                        col_value = True

                row[col_name] = col_value
            rows.append(row)

        engine.execute(table_class.__table__.insert(), rows)

def db_import(engine, data_dir):
    model.Base.metadata.drop_all(engine)
    model.Base.metadata.create_all(engine)

    fnames = os.listdir(data_dir)
    for fname in fnames:
        table_class = None
        col_order = []
        full_fname = os.path.join(data_dir, fname)

        if fname == 'DATA_SRC.txt':
            table_class = model.DataSource
            col_order = ['id', 'authors', 'title', 'year', 'journal', 'volume_city',
                         'issue_state', 'start_page', 'end_page']
        elif fname == 'DATSRCLN.txt':
            table_class = model.FoodNutrientDataSourceMap
            col_order = ['food_id', 'nutrient_id', 'data_source_id']
        elif fname == 'DERIV_CD.txt':
            table_class = model.DerivationCode
            col_order = ['id', 'desc']
        elif fname == 'FD_GROUP.txt':
            table_class = model.FoodGroup
            col_order = ['id', 'name']
        elif fname == 'FOOD_DES.txt':
            table_class = model.Food
            col_order = ['id', 'group_id', 'long_desc', 'short_desc', 'common_name',
                         'manufacturer', 'has_fndds_profile', 'refuse_desc', 'refuse_pct',
                         'sci_name', 'nitrogen_protein_factor', 'protein_calories_factor',
                         'fat_calories_factor', 'carb_calories_factor']
        elif fname == 'FOOTNOTE.txt':
            table_class = model.Footnote
            col_order = ['food_id', 'orig_id', 'type', 'nutrient_id', 'desc']
        elif fname == 'LANGDESC.txt':
            table_class = model.Langual
            col_order = ['id', 'desc']
        elif fname == 'LANGUAL.txt':
            table_class = model.FoodLangualMap
            col_order = ['food_id', 'langual_id']
        elif fname == 'NUT_DATA.txt':
            table_class = model.FoodNutrientData
            col_order = ['food_id', 'nutrient_id', 'value', 'num_data_points', 'std_error',
                         'source_code_id', 'derivation_code_id', 'missing_food_id',
                         'is_fortified', 'num_studies', 'min_value', 'max_value',
                         'degrees_freedom', 'lower_95_error_bound', 'upper_95_error_bound',
                         'stat_comments', 'last_modified', 'confidence_code']
        elif fname == 'NUTR_DEF.txt':
            table_class = model.Nutrient
            col_order = ['id', 'units', 'infoods_tag', 'name', 'num_decimals', 'sr_order']
        elif fname == 'SRC_CD.txt':
            table_class = model.SourceCode
            col_order = ['id', 'desc']
        elif fname == 'WEIGHT.txt':
            table_class = model.Weight
            col_order = ['food_id', 'sequence', 'amount', 'measurement_desc',
                         'grams', 'num_data_points', 'std_dev']
        else:
            print("No handler for file {}".format(full_fname))

        if col_order:
            print("Processing file '{}' with class '{}'".format(full_fname, table_class.__name__))
            db_import_file(engine, table_class, full_fname, col_order)
