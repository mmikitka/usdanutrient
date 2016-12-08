from sqlalchemy import (Table, Column, Boolean, Date, Integer, Numeric, String, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class FoodGroup(Base):
    __tablename__ = 'food_group'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(60), nullable=False)

    def __repr__(self):
        return "<FoodGroup(id='{}', name='{}')>".format(
                    self.id, self.name)

class Food(Base):
    __tablename__ = 'food'

    id = Column(Integer, nullable=False, primary_key=True)
    group_id = Column(Integer, ForeignKey('food_group.id'), nullable=False)
    long_desc = Column(String(200), nullable=False)
    short_desc = Column(String(60), nullable=False)
    common_name = Column(String(100))
    sci_name = Column(String(65))
    manufacturer = Column(String(65))
    has_fndds_profile = Column(Boolean)
    refuse_desc = Column(String(135))
    refuse_pct = Column(Integer)
    nitrogen_protein_factor = Column(Numeric)
    protein_calories_factor = Column(Numeric)
    fat_calories_factor = Column(Numeric)
    carb_calories_factor = Column(Numeric)

    group = relationship("FoodGroup")
    nutrient_data = relationship("FoodNutrientData")
    weights = relationship("Weight")
    languals = relationship("FoodLangualMap")

    def __repr__(self):
        return "<Food(id='{}', long_desc='{}', short_desc='{}')>".format(
                    self.id, self.long_desc, self.short_desc)

class NutrientCategory(Base):
    __tablename__ = 'nutrient_category'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(60), nullable=False)

    def __repr__(self):
        return "<NutrientCategory(id='{}', name='{}')>".format(
                    self.id, self.name)

class Nutrient(Base):
    __tablename__ = 'nutrient'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(60), nullable=False)
    units = Column(String(7), nullable=False)
    num_decimals = Column(Integer, nullable=False)
    sr_order = Column(Integer, nullable=False)
    infoods_tag = Column(String(20))

    # Custom field
    category_id = Column(Integer, ForeignKey('nutrient_category.id'))

    category = relationship("NutrientCategory")

    def __repr__(self):
        return "<Nutrient(id='{}', name='{}', units='{}')>".format(
                    self.id, self.name, self.units)

class FoodNutrientData(Base):
    __tablename__ = 'food_nutrient_data'

    food_id = Column(Integer, ForeignKey('food.id'), primary_key=True, nullable=False)
    nutrient_id = Column(Integer, ForeignKey('nutrient.id'), primary_key=True, nullable=False)
    source_code_id = Column(Integer, ForeignKey('source_code.id'), nullable=False)
    derivation_code_id = Column(String(4), ForeignKey('derivation_code.id'))
    missing_food_id = Column(Integer)
    value = Column(Numeric, nullable=False)
    num_data_points = Column(Integer, nullable=False)
    std_error = Column(Numeric)
    is_fortified = Column(Boolean)
    num_studies = Column(Integer)
    min_value = Column(Numeric)
    max_value = Column(Numeric)
    degrees_freedom = Column(Integer)
    lower_95_error_bound = Column(Numeric)
    upper_95_error_bound = Column(Numeric)
    stat_comments = Column(String(10))
    last_modified = Column(Date)
    confidence_code = Column(String(1))

    food = relationship("Food")
    nutrient = relationship("Nutrient")
    source_code = relationship("SourceCode")
    derivation_code = relationship("DerivationCode")

    def __repr__(self):
        return "<FoodNutrientData(food_id='{}', nutrient_id='{}', value='{}'>".format(
                    self.id, self.nutrient_id, self.value)

class Langual(Base):
    __tablename__ = 'langual'

    id = Column(String(5), primary_key=True, nullable=False)
    desc = Column(String(140), nullable=False)

    def __repr__(self):
        return "<Langual(id='{}', desc='{}')>".format(
                    self.id, self.desc)

class FoodLangualMap(Base):
    __tablename__ = 'food_langual_map'

    food_id = Column(Integer, ForeignKey('food.id'), primary_key=True, nullable=False)
    langual_id = Column(String(5), ForeignKey('langual.id'), primary_key=True, nullable=False)
    langual = relationship("Langual")

    def __repr__(self):
        return "<FoodLangualMap(food_id='{}', langual_id='{}')>".format(
                    self.food_id, self.langual_id)

class SourceCode(Base):
    __tablename__ = 'source_code'

    id = Column(Integer, primary_key=True, nullable=False)
    desc = Column(String(60), nullable=False)

    def __repr__(self):
        return "<SourceCode(id='{}', desc='{}')>".format(
                    self.id, self.desc)

class DerivationCode(Base):
    __tablename__ = 'derivation_code'

    id = Column(String(4), primary_key=True, nullable=False)
    desc = Column(String(120), nullable=False)

    def __repr__(self):
        return "<DerivationCode(id='{}', desc='{}')>".format(
                    self.id, self.desc)

class Weight(Base):
    __tablename__ = 'weight'

    food_id = Column(Integer, ForeignKey('food.id'), primary_key=True, nullable=False)
    sequence = Column(Integer, primary_key=True, nullable=False)
    amount = Column(Numeric, nullable=False)
    measurement_desc = Column(String(84), nullable=False)
    grams = Column(Numeric, nullable=False)
    num_data_points = Column(Integer)
    std_dev = Column(Numeric)

    food = relationship("Food")

    def __repr__(self):
        return "<Weight(food_id='{}', sequence='{}', amount='{}', measurement_desc='{}', grams='{}')>".format(
                    self.food_id, self.sequence, self.amount, self.measurement_desc, self.grams)

class Footnote(Base):
    __tablename__ = 'footnote'

    # There is no primary key on this table (see the SR PDF document), so
    # I created an artificial primary key.
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    orig_id = Column(Integer, nullable=False)
    food_id = Column(Integer, ForeignKey('food.id'), nullable=False)
    type = Column(String(1), nullable=False)
    nutrient_id = Column(Integer, ForeignKey('nutrient.id'))
    desc = Column(String(200), nullable=False)

    def __repr__(self):
        return "<Footnote(food_id='{}', id='{}', type='{}', nutrient_id='{}', desc='{}')>".format(
                    self.food_id, self.id, self.type, self.nutrient_id, self.desc)

class DataSource(Base):
    __tablename__ = 'data_source'

    id = Column(String(6), primary_key=True, nullable=False)
    authors = Column(String(255))
    title = Column(String(255), nullable=False)
    year = Column(String(4))
    journal = Column(String(135))
    volume_city = Column(String(16))
    issue_state = Column(String(5))
    start_page = Column(String(5))
    end_page = Column(String(5))

    def __repr__(self):
        return "<DataSource(id='{}', authors='{}', title='{}', year='{}', journal='{}')>".format(
                    self.id, self.authors, self.title, self.year, self.journal)

class FoodNutrientDataSourceMap(Base):
    __tablename__ = 'food_nutrient_data_source_map'

    food_id = Column(Integer, ForeignKey('food.id'), primary_key=True, nullable=False)
    nutrient_id = Column(Integer, ForeignKey('nutrient.id'), primary_key=True, nullable=False)
    data_source_id = Column(String(6), ForeignKey('data_source.id'), primary_key=True, nullable=False)
    data_source = relationship("DataSource")

    def __repr__(self):
        return "<FoodNutrientDataSourceMap(food_id='{}', nutrient_id='{}', data_source_id='{}')>".format(
            self.food_id, self.data_source_id, self.data_source)
