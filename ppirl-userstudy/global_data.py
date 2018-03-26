import os
import redis
import config
import data_loader as dl
import data_display as dd
import data_model as dm
import user_data as ud


if config.ENV == 'production':
    r = redis.from_url(os.environ.get("REDIS_URL"))
elif config.ENV == 'development':
    r = redis.Redis(host='localhost', port=6379, db=0)

# global data, this should be common across all users, not affected by multiple process
# this is the full database for tutorial
DATASET_TUTORIAL =  dl.load_data_from_csv('data/tutorial/all_tutorial_questions.csv')

DATA_CLICKABLE_DEMO = dm.DataPairList(data_pairs = dl.load_data_from_csv('data/tutorial/clickable/demo.csv'))

DATA_TUTORIAL1 = dm.DataPairList(data_pairs = dl.load_data_from_csv('data/tutorial1.csv'))

DATA_DM_DEMO = dm.DataPairList(data_pairs = dl.load_data_from_csv('data/tutorial/clickable/decision_making_demo.csv'))
# DATA_TUTORIAL1 = dm.DataPairList(data_pairs = dl.load_data_from_csv('data/tutorial1.csv'))

DATA_CLICKABLE_PRACTICE = dm.DataPairList(data_pairs = dl.load_data_from_csv('data/tutorial/clickable/practice.csv'))


# this is the full database for section 1
DATASET = dl.load_data_from_csv('data/main_section_full.csv')
# this is the full database for section 2
DATASET2 = dl.load_data_from_csv('data/main_section_full.csv')

# this is the dataset used in section 1
DATA_SECTION1 = [
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section1_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section1_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section1_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section1_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section1_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section1_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section1_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section1_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section1_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section1_10.csv'))
]
# this is the dataset used in section 2, NOTE: the question number has to be a factor of 6!
DATA_SECTION2 = [
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section2_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section2_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section2_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section2_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section2_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section2_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section2_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section2_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section2_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/main_section/section2_10.csv'))
]