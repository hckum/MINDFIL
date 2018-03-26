#! /usr/bin/python
# encoding=utf-8 

import os

if 'DYNO' in os.environ:
    ENV = 'production'
else:
    ENV = 'development'


SEQUENCE_MODE4 = [
    'show_introduction',    #0
    'show_introduction2',    #1
    'pre_survey',
    'tutorial.show_tutorial_rl_pdf',    #2
    'tutorial.show_tutorial_rl_id_1',    #3
    'tutorial.show_tutorial_rl_id_2',    #4
    'tutorial.show_tutorial_rl_id_3',    #5
    'tutorial.show_tutorial_rl_twin',    #6
    'tutorial.show_tutorial_rl_dup',    #7
    'tutorial.show_tutorial_rl_missing',    #8
    'tutorial.show_tutorial_rl_freq',    #9
    'tutorial.show_tutorial_privacy_pdf',    #10
    'tutorial.show_tutorial_privacy_practice',    #11
    'tutorial.show_tutorial_clickable_start',    #12
    'tutorial.show_tutorial_clickable_demo',  #13 DATA_CLICKABLE_DEMO
    'tutorial.show_tutorial_clickable_incremental1',    #14
    'tutorial.show_tutorial_clickable_incremental2',    #15
    'tutorial.show_tutorial_clickable_whatopen',    #16
    'tutorial.show_tutorial_clickable_decision_making_1',    #17
    'tutorial.show_tutorial_clickable_decision_making_2',    #18
    'tutorial.show_tutorial_clickable_decision_making_3',    #19
    'tutorial.show_tutorial_clickable_decision_making_4',    #20
    'tutorial.show_tutorial_clickable_decision_making_5',    #21
    'tutorial.show_tutorial_clickable_whatnotopen',    #22
    'tutorial.show_tutorial_clickable_whenidentical',    #23
    'tutorial.show_tutorial_clickable_decision_making_demo', #24 DATA_DM_DEMO
    'tutorial.show_tutorial_clickable_budgetmeter',    #25
    'tutorial.show_tutorial_clickable_budgetlimit',    #26
    'tutorial.show_tutorial_clickable_budgeting',    #27
    # 'show_tutorial_clickable_budgetmeter_vid',
    'tutorial.show_tutorial_clickable_prepractice',    #28
    'tutorial.show_tutorial_clickable_practice', #29 DATA_CLICKABLE_PRACTICE
    'main_section.show_section1_guide',    #30
    'main_section.show_record_linkage_task',    #31
    'main_section.show_section2_guide',    #32
    'main_section.show_section2_budget',
    'main_section.show_section2',    #33
    'post_survey',
    'show_thankyou'    #34
]

SEQUENCE_MODE1 =  [
    'show_introduction',    #0
    'show_introduction2',    #1
    'pre_survey',
    'tutorial.show_tutorial_rl_pdf',    #2
    'tutorial.show_tutorial_rl_id_1',    #3
    'tutorial.show_tutorial_rl_id_2',    #4
    'tutorial.show_tutorial_rl_id_3',    #5
    'tutorial.show_tutorial_rl_twin',    #6
    'tutorial.show_tutorial_rl_dup',    #7
    'tutorial.show_tutorial_rl_missing',    #8
    'tutorial.show_tutorial_rl_freq',    #9
    'tutorial.show_tutorial_privacy_pdf',    #10
    'tutorial.show_tutorial_privacy_practice',
    'main_section.show_section1_guide',    #30
    'main_section.show_record_linkage_task',    #31
    'main_section.show_section2_guide',    #32
    'main_section.show_section2',    #33
    'post_survey',
    'show_thankyou' 
]

SEQUENCE_MODE2 =  [
    'show_introduction',    #0
    'show_introduction2',    #1
    'pre_survey',
    'tutorial.show_tutorial_rl_pdf',    #2
    'tutorial.show_tutorial_rl_id_1',    #3
    'tutorial.show_tutorial_rl_id_2',    #4
    'tutorial.show_tutorial_rl_id_3',    #5
    'tutorial.show_tutorial_rl_twin',    #6
    'tutorial.show_tutorial_rl_dup',    #7
    'tutorial.show_tutorial_rl_missing',    #8
    'tutorial.show_tutorial_rl_freq',    #9
    'tutorial.show_tutorial_privacy_pdf',    #10
    'tutorial.show_tutorial_privacy_practice',    #11
    'tutorial.show_tutorial_clickable_start',    #12
    'tutorial.show_tutorial_clickable_demo',  #13 DATA_CLICKABLE_DEMO
    'tutorial.show_tutorial_clickable_incremental1',    #14
    'tutorial.show_tutorial_clickable_incremental2',    #15
    'tutorial.show_tutorial_clickable_whatopen',    #16
    'tutorial.show_tutorial_clickable_decision_making_1',    #17
    'tutorial.show_tutorial_clickable_decision_making_2',    #18
    'tutorial.show_tutorial_clickable_decision_making_3',    #19
    'tutorial.show_tutorial_clickable_decision_making_4',    #20
    'tutorial.show_tutorial_clickable_decision_making_5',    #21
    'tutorial.show_tutorial_clickable_whatnotopen',    #22
    'tutorial.show_tutorial_clickable_whenidentical',
    'tutorial.show_tutorial_clickable_prepractice',    #28
    'tutorial.show_tutorial_clickable_practice', #29 DATA_CLICKABLE_PRACTICE
    'main_section.show_section1_guide',    #30
    'main_section.show_record_linkage_task',    #31
    'main_section.show_section2_guide',    #32
    'main_section.show_section2',    #33
    'post_survey',
    'show_thankyou'    #34
]

SEQUENCE_MODE3 = [
   'show_introduction',    #0
   'show_introduction2',    #1
   'pre_survey',
   'tutorial.show_tutorial_rl_pdf',    #2
   'tutorial.show_tutorial_rl_id_1',    #3
   'tutorial.show_tutorial_rl_id_2',    #4
   'tutorial.show_tutorial_rl_id_3',    #5
   'tutorial.show_tutorial_rl_twin',    #6
   'tutorial.show_tutorial_rl_dup',    #7
   'tutorial.show_tutorial_rl_missing',    #8
   'tutorial.show_tutorial_rl_freq',    #9
   'tutorial.show_tutorial_privacy_pdf',    #10
   'tutorial.show_tutorial_privacy_practice',    #11
   'tutorial.show_tutorial_clickable_start',    #12
   'tutorial.show_tutorial_clickable_demo',  #13 DATA_CLICKABLE_DEMO
   'tutorial.show_tutorial_clickable_incremental1',    #14
   'tutorial.show_tutorial_clickable_incremental2',    #15
   'tutorial.show_tutorial_clickable_whatopen',    #16
   'tutorial.show_tutorial_clickable_decision_making_1',    #17
   'tutorial.show_tutorial_clickable_decision_making_2',    #18
   'tutorial.show_tutorial_clickable_decision_making_3',    #19
   'tutorial.show_tutorial_clickable_decision_making_4',    #20
   'tutorial.show_tutorial_clickable_decision_making_5',    #21
   'tutorial.show_tutorial_clickable_whatnotopen',    #22
   'tutorial.show_tutorial_clickable_whenidentical',    #23
   'tutorial.show_tutorial_clickable_decision_making_demo', #24 DATA_DM_DEMO
   'tutorial.show_tutorial_clickable_budgetmeter',
   'tutorial.show_tutorial_clickable_prepractice',    #28
   'tutorial.show_tutorial_clickable_practice', #29 DATA_CLICKABLE_PRACTICE
   'main_section.show_section1_guide',    #30
   'main_section.show_record_linkage_task',
   'main_section.show_section2_guide',    #32
   'main_section.show_section2',    #33
   'post_survey',
   'show_thankyou' 
]

SEQUENCE = {
    "Mode_1": SEQUENCE_MODE1,
    "Mode_2": SEQUENCE_MODE2,
    "Mode_3": SEQUENCE_MODE3,
    "Mode_4": SEQUENCE_MODE4
}


pre_survey_switch = True
post_survey_switch = False
section_2_switch = True

for mode in SEQUENCE.keys():
  values = SEQUENCE[mode]
  if not pre_survey_switch:
    values.remove("pre_survey")
  if not post_survey_switch:
    values.remove("post_survey")
  if not section_2_switch:
    values.remove("main_section.show_section2_guide")
    values.remove("main_section.show_section2")
    if 'main_section.show_section2_budget' in values:
      values.remove('main_section.show_section2_budget')
  SEQUENCE[mode] = values




DATA_PAIR_PER_PAGE = 6
'''
KAPR_LIMIT can take following parameters:
'moderate'
any number from 0 to 100
'''
KAPR_LIMIT = 'moderate'
#KAPR_LIMIT = 50.0

'''
    This factor will multiple the KAPR_LIMIT: KAPR_LIMIT_FACTOR * KAPR_LIMIT
    Valid value: 0 to 1 in decimal.
'''
KAPR_LIMIT_FACTOR = 1
#KAPR_LIMIT_FACTOR = 0.5

# email server
MAIL_SERVER = 'smtp.googlemail.com'

MAIL_PORT = 465

MAIL_USE_TLS = False

MAIL_USE_SSL = True

MAIL_USERNAME = 'ppirl.mindfil@gmail.com'

MAIL_PASSWORD = 'Abcd1234$'

MAIL_DEFAULT_SENDER = 'ppirl.mindfil@gmail.com'
