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
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_1_sample_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_1_sample_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_1_sample_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_1_sample_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_1_sample_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_1_sample_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_1_sample_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_1_sample_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_1_sample_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_1_sample_10.csv'))
]
# this is the dataset used in section 2, NOTE: the question number has to be a factor of 6!
DATA_SECTION2 = [
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_2_sample_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_2_sample_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_2_sample_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_2_sample_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_2_sample_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_2_sample_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_2_sample_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_2_sample_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_2_sample_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_2_sample_10.csv'))
]


DATA_SECTION3 = [
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_10.csv'))
]

DATA_SECTION4 = [
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_4_sample_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_4_sample_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_4_sample_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_4_sample_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_4_sample_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_4_sample_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_4_sample_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_4_sample_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_4_sample_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_4_sample_10.csv'))
]

DATA_SECTION5 = [
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_5_sample_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_5_sample_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_5_sample_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_5_sample_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_5_sample_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_5_sample_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_5_sample_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_5_sample_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_5_sample_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_5_sample_10.csv'))
]

DATA_SECTION6 = [
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_6_sample_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_6_sample_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_6_sample_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_6_sample_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_6_sample_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_6_sample_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_6_sample_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_6_sample_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_6_sample_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_6_sample_10.csv'))
]

DATA_SECTION7 = [
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_7_sample_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_7_sample_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_7_sample_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_7_sample_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_7_sample_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_7_sample_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_7_sample_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_7_sample_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_7_sample_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_7_sample_10.csv'))
]

DATA_SECTION8 = [
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_8_sample_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_8_sample_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_8_sample_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_8_sample_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_8_sample_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_8_sample_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_8_sample_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_8_sample_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_8_sample_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_8_sample_10.csv'))
]

DATA_SECTION9 = [
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_9_sample_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_9_sample_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_9_sample_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_9_sample_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_9_sample_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_9_sample_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_9_sample_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_9_sample_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_9_sample_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_9_sample_10.csv'))
]

DATA_SECTION10 = [
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_10_sample_1.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_10_sample_2.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_10_sample_3.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_10_sample_4.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_10_sample_5.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_10_sample_6.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_10_sample_7.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_10_sample_8.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_10_sample_9.csv')),
    dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_10_sample_10.csv'))
]

# DATA_SECTION3 = [
#     dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_1.csv')),
#     dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_2.csv')),
#     dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_3.csv')),
#     dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_4.csv')),
#     dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_5.csv')),
#     dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_6.csv')),
#     dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_7.csv')),
#     dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_8.csv')),
#     dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_9.csv')),
#     dm.DataPairList(data_pairs = dl.load_data_from_csv('data/samples_sections_scrambling/section_3_sample_10.csv'))
# ]