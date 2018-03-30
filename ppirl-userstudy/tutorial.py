from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request
from flask_mail import Mail, Message
import os
import time
import math
import redis
import logging
import data_loader as dl
import data_display as dd
import data_model as dm
import user_data as ud
import re
import config
from util import state_machine
from global_data import r, DATASET_TUTORIAL, DATA_CLICKABLE_DEMO, DATA_TUTORIAL1, DATA_DM_DEMO, DATA_CLICKABLE_PRACTICE


tutorial = Blueprint('tutorial', __name__, template_folder='templates')


@tutorial.route('/tutorial/')
@tutorial.route('/tutorial/rl/')
@state_machine('show_tutorial_rl_pdf')
def show_tutorial_rl_pdf():
    return render_template('tutorial/rl/tutorial_pdf.html')


@tutorial.route('/tutorial/privacy')
@state_machine('show_tutorial_privacy_pdf')
def show_tutorial_privacy_pdf():
    return render_template('tutorial/privacy/tutorial_pdf.html')


@tutorial.route('/instructions/ppirl')
@state_machine('show_instruction_ppirl')
def show_instruction_ppirl():
    return render_template('instruction_ppirl.html')


@tutorial.route('/tutorial/rl/id')
@tutorial.route('/tutorial/rl/id_1')
@state_machine('show_tutorial_rl_id_1')
def show_tutorial_rl_id_1():
    pairs = dl.load_data_from_csv('data/tutorial/rl/id_1.csv')
    pairs_formatted = dd.format_data(pairs, 'full')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('tutorial/rl/id_1.html', data=data, icons=icons, title='Section 1: practice', thisurl='/tutorial/rl/id_1', page_number=5)

@tutorial.route('/tutorial/rl/id_2')
@state_machine('show_tutorial_rl_id_2')
def show_tutorial_rl_id_2():
    return render_template('tutorial/rl/id_2.html')

@tutorial.route('/tutorial/rl/id_3')
@state_machine('show_tutorial_rl_id_3')
def show_tutorial_rl_id_3():
    pairs = dl.load_data_from_csv('data/tutorial/rl/id_3.csv')
    pairs_formatted = dd.format_data(pairs, 'full')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('tutorial/rl/id_3.html', data=data, icons=icons, title='Section 1: practice', thisurl='/tutorial/rl/id_3',  page_number=5)

@tutorial.route('/tutorial/rl/twin')
@state_machine('show_tutorial_rl_twin')
def show_tutorial_rl_twin():
    pairs = dl.load_data_from_csv('data/tutorial/rl/twin.csv')
    pairs_formatted = dd.format_data(pairs, 'full')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('tutorial/rl/twin.html', data=data, icons=icons, title='Section 1: practice', thisurl='/tutorial/rl/twin',  page_number=5)

@tutorial.route('/tutorial/rl/dup')
@state_machine('show_tutorial_rl_dup')
def show_tutorial_rl_dup():
    pairs = dl.load_data_from_csv('data/tutorial/rl/dup.csv')
    pairs_formatted = dd.format_data(pairs, 'full')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('tutorial/rl/dup.html', data=data, icons=icons, title='Section 1: practice', thisurl='/tutorial/rl/dup',  page_number=5)

@tutorial.route('/tutorial/rl/missing')
@state_machine('show_tutorial_rl_missing')
def show_tutorial_rl_missing():
    pairs = dl.load_data_from_csv('data/tutorial/rl/missing.csv')
    pairs_formatted = dd.format_data(pairs, 'full')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('tutorial/rl/missing.html', data=data, icons=icons, title='Section 1: practice', thisurl='/tutorial/rl/missing',  page_number=5)

@tutorial.route('/tutorial/rl/freq')
@state_machine('show_tutorial_rl_freq')
def show_tutorial_rl_freq():
    pairs = dl.load_data_from_csv('data/tutorial/rl/freq.csv')
    pairs_formatted = dd.format_data(pairs, 'full')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('tutorial/rl/freq.html', data=data, icons=icons, title='Section 1: practice', thisurl='/tutorial/rl/freq',  page_number=5)

@tutorial.route('/tutorial/privacy/practice')
@state_machine('show_tutorial_privacy_practice')
def show_tutorial_privacy_practice():
    pairs = dl.load_data_from_csv('data/tutorial/privacy/practice.csv')
    pairs_formatted = dd.format_data(pairs, 'masked')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('tutorial/privacy/practice.html', data=data, icons=icons, title='Section 2: practice', thisurl='/tutorial/privacy/practice',  page_number=5)

@tutorial.route('/tutorial/<tutorial_section>/<page>/grading')
def grade_pratice_full_mode(tutorial_section, page):
    data_file = 'data/tutorial/' + str(tutorial_section) + "/" + str(page) + '.csv'
    pairs = dl.load_data_from_csv(data_file)
    feedback = ""
    responses = request.args.get('responses').split(',')
    all_correct = True
    wrong_ids = []
    right_ids = []



    ustudy_mode = int(r.get(session['user_id']+'_ustudy_mode'))
    data_mode = 'full'
    working_data = dm.DataPairList(data_pairs = pairs)
    # current_page = 1
    pairs_formatted = working_data.get_data_display(data_mode)[:]
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = working_data.get_icons()[:]
    ids_list = working_data.get_ids()[:]
    ids = zip(ids_list[0::2], ids_list[1::2])

    

    page_content = render_template('tutorial/table.html', 
        data=data, 
        icons=icons, 
        ids=ids, 
        ustudy_mode=ustudy_mode
    )

    custom_feedback = ""
  
    for i in range(0, len(pairs), 2):
        pair_id = pairs[i][0]
        q = "q" + pair_id
        answer = pairs[i][17]
        if answer == '1' and (q+'a4' in responses or q+'a5' in responses or q+'a6' in responses):
            right_ids.append(pair_id) 
        elif answer == '0' and (q+'a1' in responses or q+'a2' in responses or q+'a3' in responses):
            right_ids.append(pair_id)
        else:
            if tutorial_section == 'privacy':
                custom_feedback += ", ".join(pairs[i][18:]) + '<br>'
            wrong_ids.append(pair_id)
            all_correct = False
    if all_correct:
        feedback += 'Good job!<br> '
    else:
        feedback += 'Please review the questions you got wrong. <br>'

    if tutorial_section in ['clickable', 'privacy']:
        feedback += 'We have opened all the records for you to review. <br>'
    
    feedback += custom_feedback

    feedback += 'Please click the next button when you are done.'
    
    return jsonify(result=feedback, wrong_ids = wrong_ids, right_ids = right_ids, page_content = page_content)


@tutorial.route('/ppirl_tutorial1')
@state_machine('show_ppirl_tutorial1')
def show_ppirl_tutorial1():
    pairs_formatted = DATA_TUTORIAL1.get_data_display('masked')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = DATA_TUTORIAL1.get_icons()
    ids_list = DATA_TUTORIAL1.get_ids()
    ids = zip(ids_list[0::2], ids_list[1::2])

    # KAPR - K-Anonymity privacy risk
    KAPR_key = session['user_id'] + '_KAPR'
    r.set(KAPR_key, 0)

    # set the user-display-status as masked for all cell
    attribute_size = 6
    for id1 in ids_list:
        for i in range(attribute_size):
            key = session['user_id'] + '-' + id1[i]
            r.set(key, 'M')

    # get the delta information
    delta = list()
    for i in range(len(icons)):
        data_pair = DATA_TUTORIAL1.get_data_pair_by_index(i)
        delta += dm.KAPR_delta(DATASET, data_pair, ['M', 'M', 'M', 'M', 'M', 'M'], 2*DATA_TUTORIAL1.size())

    return render_template('tutorial1.html', data=data, icons=icons, ids=ids, title='Practice 2', thisurl='/ppirl_tutorial1', page_number=" ", delta=delta)


@tutorial.route('/tutorial/clickable')
@state_machine('show_tutorial_clickable_start')
def show_tutorial_clickable_start():
    return render_template('tutorial/clickable/start.html')


@tutorial.route('/tutorial/clickable/demo')
@state_machine('show_tutorial_clickable_demo')
def show_tutorial_clickable_demo():
    pairs_formatted = DATA_CLICKABLE_DEMO.get_data_display('masked')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = DATA_CLICKABLE_DEMO.get_icons()
    ids_list = DATA_CLICKABLE_DEMO.get_ids()
    ids = zip(ids_list[0::2], ids_list[1::2])

    # KAPR - K-Anonymity privacy risk
    KAPR_key = session['user_id'] + '_KAPR'
    r.set(KAPR_key, 0)

    # set the user-display-status as masked for all cell
    attribute_size = 6
    for id1 in ids_list:
        for i in range(attribute_size):
            key = session['user_id'] + '-' + id1[i]
            r.set(key, 'M')
    
    delta = list()
    for i in range(1):
        data_pair = DATA_CLICKABLE_DEMO.get_data_pair_by_index(i)
        delta += dm.KAPR_delta(DATASET_TUTORIAL, data_pair, ['M', 'M', 'M', 'M', 'M', 'M'], 2*DATA_CLICKABLE_DEMO.size())

    return render_template('tutorial/clickable/demo.html', data=data, icons=icons, ids=ids, title='Tutorial 3', thisurl='/tutorial/clickable/demo', page_number=" ", delta=delta, kapr_limit = 100)


@tutorial.route('/tutorial/clickable/incremental1')
@state_machine('show_tutorial_clickable_incremental1')
def show_tutorial_clickable_incremental1():
    return render_template('tutorial/clickable/incremental1.html')


@tutorial.route('/tutorial/clickable/incremental2')
@state_machine('show_tutorial_clickable_incremental2')
def show_tutorial_clickable_incremental2():
    return render_template('tutorial/clickable/incremental2.html')

@tutorial.route('/tutorial/clickable/whatopen')
@state_machine('show_tutorial_clickable_whatopen')
def show_tutorial_clickable_whatopen():
    return render_template('/tutorial/clickable/whatopen.html')

@tutorial.route('/tutorial/clickable/whenidentical')
@state_machine('show_tutorial_clickable_whenidentical')
def show_tutorial_clickable_whenidentical():
    return render_template('/tutorial/clickable/whenidentical.html')

@tutorial.route('/tutorial/clickable/whatnotopen')
@state_machine('show_tutorial_clickable_whatnotopen')
def show_tutorial_clickable_whatnotopen():
    return render_template('/tutorial/clickable/whatnotopen.html')

@tutorial.route('/tutorial/clickable/decision_making_1')
@state_machine('show_tutorial_clickable_decision_making_1')
def show_tutorial_clickable_decision_making_1():
    return render_template('tutorial/clickable/decision_making_1.html')

@tutorial.route('/tutorial/clickable/decision_making_2')
@state_machine('show_tutorial_clickable_decision_making_2')
def show_tutorial_clickable_decision_making_2():
    return render_template('tutorial/clickable/decision_making_2.html')

@tutorial.route('/tutorial/clickable/decision_making_3')
@state_machine('show_tutorial_clickable_decision_making_3')
def show_tutorial_clickable_decision_making_3():
    return render_template('tutorial/clickable/decision_making_3.html')

@tutorial.route('/tutorial/clickable/decision_making_4')
@state_machine('show_tutorial_clickable_decision_making_4')
def show_tutorial_clickable_decision_making_4():
    return render_template('tutorial/clickable/decision_making_4.html')

@tutorial.route('/tutorial/clickable/decision_making_5')
@state_machine('show_tutorial_clickable_decision_making_5')
def show_tutorial_clickable_decision_making_5():
    return render_template('tutorial/clickable/decision_making_5.html')

@tutorial.route('/tutorial/clickable/decision_making_demo')
@state_machine('show_tutorial_clickable_decision_making_demo')
def show_tutorial_clickable_decision_making_demo():
    pairs_formatted =  DATA_DM_DEMO.get_data_display('masked')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = DATA_DM_DEMO.get_icons()
    ids_list = DATA_DM_DEMO.get_ids()
    ids = zip(ids_list[0::2], ids_list[1::2])

    # KAPR - K-Anonymity privacy risk
    KAPR_key = session['user_id'] + '_KAPR'
    r.set(KAPR_key, 0)

    # set the user-display-status as masked for all cell
    attribute_size = 6
    for id1 in ids_list:
        for i in range(attribute_size):
            key = session['user_id'] + '-' + id1[i]
            r.set(key, 'M')

    # DATASET_T = dl.load_data_from_csv('data/tutorial1.csv')
    # print DATASET_T
    # get the delta information
    delta = list()
    for i in range(DATA_DM_DEMO.size()):
        data_pair = DATA_DM_DEMO.get_data_pair_by_index(i)
        delta += dm.KAPR_delta(DATASET_TUTORIAL, data_pair, ['M', 'M', 'M', 'M', 'M', 'M'], 2*DATA_DM_DEMO.size())

    # kapr_limit = dm.get_kaprlimit(DATASET_TUTORIAL, DATA_DM_DEMO, 'moderate')
    # r.set(session['user_id']+'tutorial_dmdemo_kapr_limit', kapr_limit)

    return render_template('tutorial/clickable/decision_making_demo.html', 
        data=data, 
        icons=icons, 
        ids=ids, 
        title='Tutorial 3', 
        thisurl='/tutorial/clickable/decision_making_demo', 
        page_number=" ", 
        delta=delta,
        kapr_limit=100)



@tutorial.route('/tutorial/clickable/budgetmeter')
@state_machine('show_tutorial_clickable_budgetmeter')
def show_tutorial_clickable_budgetmeter():
    return render_template('tutorial/clickable/budgetmeter.html')

@tutorial.route('/tutorial/clickable/budgetlimit')
@state_machine('show_tutorial_clickable_budgetlimit')
def show_tutorial_clickable_budgetlimit():
    return render_template('tutorial/clickable/budgetlimit.html')

@tutorial.route('/tutorial/clickable/budgeting')
@state_machine('show_tutorial_clickable_budgeting')
def show_tutorial_clickable_budgeting():
    return render_template('tutorial/clickable/budgeting.html')


@tutorial.route('/tutorial/clickable/budgetmeter_vid')
@state_machine('show_tutorial_clickable_budgetmeter_vid')
def show_tutorial_clickable_budgetmeter_vid():
    return render_template('tutorial/clickable/budgetmeter_vid.html')


@tutorial.route('/tutorial/clickable/prepractice')
@state_machine('show_tutorial_clickable_prepractice')
def show_tutorial_clickable_prepractice():
    return render_template('tutorial/clickable/prepractice.html')

    

@tutorial.route('/tutorial/clickable/practice')
@state_machine('show_tutorial_clickable_practice')
def show_tutorial_clickable_practice():
    pairs_formatted = DATA_CLICKABLE_PRACTICE.get_data_display('masked')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = DATA_CLICKABLE_PRACTICE.get_icons()
    ids_list = DATA_CLICKABLE_PRACTICE.get_ids()
    ids = zip(ids_list[0::2], ids_list[1::2])

    # KAPR - K-Anonymity privacy risk
    KAPR_key = session['user_id'] + '_KAPR'
    r.set(KAPR_key, 0)

    # set the user-display-status as masked for all cell
    attribute_size = 6
    for id1 in ids_list:
        for i in range(attribute_size):
            key = session['user_id'] + '-' + id1[i]
            r.set(key, 'M')

    # DATASET_T = dl.load_data_from_csv('data/tutorial1.csv')
    # print DATASET_T
    # get the delta information
    delta = list()
    for i in range(DATA_CLICKABLE_PRACTICE.size()):
        data_pair = DATA_CLICKABLE_PRACTICE.get_data_pair_by_index(i)
        delta += dm.KAPR_delta(DATASET_TUTORIAL, data_pair, ['M', 'M', 'M', 'M', 'M', 'M'], 2*DATA_CLICKABLE_PRACTICE.size())
    
    if session[session['user_id'] + '_mode'] == '4':
        kapr_limit = 20
    else:
        kapr_limit = 0

    # kapr_limit = dm.get_kaprlimit(DATASET_TUTORIAL, DATA_CLICKABLE_PRACTICE, 'moderate')
    # r.set(session['user_id']+'tutorial_practice_kapr_limit', kapr_limit)

    return render_template('tutorial/clickable/practice.html', 
        data=data, 
        icons=icons, 
        ids=ids, 
        title='Practice 3 ', 
        thisurl='/tutorial/clickable/practice', 
        page_number="1", 
        delta=delta, 
        kapr =0,
        kapr_limit = kapr_limit, 
        uid=str(session['user_id']),
        pair_num_base=6*0+1,
        ustudy_mode=r.get(str(session['user_id'])+'_ustudy_mode')
        )

     
   #      kapr = KAPR,
   # 