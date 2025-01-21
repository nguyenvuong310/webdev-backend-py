import pandas as pd
from sqlalchemy import create_engine
import os

path = os.path.dirname(os.path.abspath(__file__))



df = pd.read_csv(path + "/dataset/diem_thi_thpt_2024.csv")

db_url = 'db_url' # Replace 'db_url' with your database URL
engine = create_engine(db_url)

connection = engine.connect()
print("Kết nối thành công!")

# Batch size
batch_size = 100000

student_df = pd.DataFrame()
student_df['id'] = df['sbd']


def insert_chunk(df, table_name, engine, batch_size=100000):
    try:
        for start in range(0, len(df), batch_size):
            end = start + batch_size
            batch_df = df[start:end]  
            batch_df.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"Inserted batch {start // batch_size + 1} successfully.")
    except Exception as e:
        print(f"Lỗi khi thực hiện thao tác cơ sở dữ liệu: {e}")


subject_df = pd.DataFrame({
    'math': df['toan'],
    'literature': df['ngu_van'],
    'language': df['ngoai_ngu'],
    'physics': df['vat_li'],
    'chemistry': df['hoa_hoc'],
    'biology': df['sinh_hoc'],
    'history': df['lich_su'],
    'geography': df['dia_li'],
    'civics': df['gdcd'],
    'foreign_language_code': df['ma_ngoai_ngu'],
    'student_id': df['sbd']
})

print("Inserting data into database in chunks...")
print("Inserting student data...")
insert_chunk(student_df, 'students', engine)
print("Inserting subject data...")
insert_chunk(subject_df, 'scores', engine)

print("Bulk insert data into database completed in chunks!")


