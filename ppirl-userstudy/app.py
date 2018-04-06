from flask import Flask, render_template, redirect, url_for, session, jsonify, request, g
from flask_mail import Mail, Message
import time
from random import *
import json
import hashlib
import collections
import os
import redis
import logging
import math
import copy
import re
import data_loader as dl
import data_display as dd
import data_model as dm
import user_data as ud
import config
from main_section import main_section
from tutorial import tutorial
from util import state_machine
from global_data import *


app = Flask(__name__)
app.debug = False
app.secret_key = 'a9%z$/`9h8FMnh893;*g783'

app.register_blueprint(tutorial)
app.register_blueprint(main_section)

app.config.from_pyfile('email_config.py')
mail = Mail(app)


if not r.exists('user_id_generator'):
    r.set('user_id_generator', 0)


def get_main_section_data(uid, section):
    sample = int(uid)%10
    if sample == 0:
        sample = 10
    sample -= 1

    if section == 1:
        return DATA_SECTION1[sample]
    elif section == 2:
        return DATA_SECTION2[sample]
    elif section == 3:
        return DATA_SECTION3[sample]
    elif section == 4:
        return DATA_SECTION4[sample]    
    elif section == 5:
        return DATA_SECTION5[sample]
    elif section == 6:
        return DATA_SECTION6[sample]
    elif section == 7:
        return DATA_SECTION7[sample]    
    elif section == 8:
        return DATA_SECTION8[sample]
    elif section == 9:
        return DATA_SECTION9[sample]
    elif section == 10:
        return DATA_SECTION10[sample]    


def get_sequence_for_mode():
    return config.SEQUENCE['Mode_'+r.get(str(session['user_id'])+'_ustudy_mode')]

def get_url_for_index(index):
    return get_sequence_for_mode()[int(index)]

@app.route('/')
@app.route('/index')
def index():
    user_id = 0
    # new user
    if request.args.get("id") is None:
        user_id = str(r.incr('user_id_generator'))
        r.set('user_id_'+user_id, user_id)
        ustudy_mode = request.args.get('mode')
        ustudy_budget = request.args.get('budget')
        # print '>>>>>>>>>>>>>>>>>>>>>'
        # print ustudy_mode, ustudy_budget
        if ustudy_mode is None:
            ustudy_mode = '1'
        if ustudy_mode == '4' and ustudy_budget is None:
            ustudy_budget = 'moderate'
        if ustudy_mode == '5' and ustudy_budget is None:
            ustudy_mode = '4'
            ustudy_budget = 'minimum'        
        if ustudy_budget is None:
            ustudy_budget = '0'
        if not ustudy_mode in ['4', '5']:
            ustudy_budget = '0'
        if int(ustudy_mode) not in [1,2,3,4]:
            return page_not_found('page_not_found')
        if ustudy_budget not in ['moderate', 'minimum']:
            if float(ustudy_budget) < 0 or float(ustudy_budget) > 100:
                return page_not_found('page_not_found')
    else:
        user_id = str(request.args.get("id"))
        if r.get('user_id_' + user_id) is None:
            # new user come with id
            #return render_template('user_not_found.html')
            r.set('user_id_'+user_id, user_id)
            ustudy_mode = request.args.get('mode')
            ustudy_budget = request.args.get('budget')
            if ustudy_mode is None:
                ustudy_mode = '1'
            if ustudy_mode == '4' and ustudy_budget is None:
                ustudy_budget = 'moderate'
            if ustudy_mode == '5' and ustudy_budget is None:
                ustudy_mode = '4'
                ustudy_budget = 'minimum'        
            if ustudy_budget is None:
                ustudy_budget = '0'
            if not ustudy_mode in ['4', '5']:
                ustudy_budget = '0'
            if int(ustudy_mode) not in [1,2,3,4]:
                return page_not_found('page_not_found')
            if ustudy_budget not in ['moderate', 'minimum']:
                if float(ustudy_budget) < 0 or float(ustudy_budget) > 100:
                    return page_not_found('page_not_found')
        else:
            # come back user
            ustudy_mode = r.get(user_id+'_ustudy_mode')
            ustudy_budget = r.get(user_id+'_ustudy_budget')

    session['user_id'] = str(user_id)
    session[session['user_id'] + '_mode'] = str(ustudy_mode)
    user_data_key = str(session['user_id']) + '_user_data'

    index = r.get("session_"+str(user_id)+"_state")
    if index is None:
        index = 0
        r.set("session_"+str(user_id)+"_state", 0)
        session['state'] = 0
    else:
        session['state'] = int(index)

    # saving user data
    data = {
        'uid': user_id,
        'type': 'session_start',
        'value': int(time.time()),
        'timestamp': int(time.time()),
        'source': 'server',
        'ustudy_mode': ustudy_mode,
        'ustudy_budget': ustudy_budget
    }
    previous_user_data = r.get(user_data_key)
    if not previous_user_data:
        r.set(user_data_key, ud.format_user_data(data))
    else:
        r.append(user_data_key, ud.format_user_data(data))
    #r.set(user_data_key, ud.format_user_data(data))

    r.set("session_"+str(user_id), session)

    r.set(str(session['user_id'])+'_ustudy_mode', ustudy_mode)
    r.set(str(session['user_id'])+'_ustudy_budget', ustudy_budget)

    return redirect(url_for(get_url_for_index(index)))

    

@app.route('/feedback_main_section')
def feedback_main_section():
    # open all cells
    ustudy_mode = int(r.get(session['user_id']+'_ustudy_mode'))
    data_mode = 'full'
    working_data = get_main_section_data(session['user_id'], 1)
    current_page = int(r.get(str(session['user_id'])+'_current_page'))
    pairs_formatted = working_data.get_data_display(data_mode)[2*config.DATA_PAIR_PER_PAGE*current_page:2*config.DATA_PAIR_PER_PAGE*(current_page+1)]
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = working_data.get_icons()[config.DATA_PAIR_PER_PAGE*current_page:config.DATA_PAIR_PER_PAGE*(current_page+1)]
    ids_list = working_data.get_ids()[2*config.DATA_PAIR_PER_PAGE*current_page:2*config.DATA_PAIR_PER_PAGE*(current_page+1)]
    ids = zip(ids_list[0::2], ids_list[1::2])

    page_content = render_template('record_linkage_next.html', 
        data=data, 
        icons=icons, 
        ids=ids, 
        pair_num_base=6*current_page+1, 
        ustudy_mode=ustudy_mode
    )

    # generating the feedback
    ids = request.args.get('ids').split(',')
    responses = request.args.get('responses').split(',')
    screen_ids = request.args.get('screen_ids').split(',')
    working_data = get_main_section_data(session['user_id'], 1)
    wrong_attempts = []
    wrong_ids = []
    right_ids = []
    feedback = ""
    for i in range(6):
        dp = working_data.get_data_pair(int(ids[i]))
        grade = dp.grade(int(responses[i]))
        # grades.append(grade)
        if not grade:
            wrong_attempts.append(screen_ids[i])
            wrong_ids.append(ids[i])
        else:
            right_ids.append(ids[i])


    # if len(wrong_attempts) == 0:
    #     feedback = "You got all of the questions in this page right! "
    #     if not session[session['user_id'] + '_mode'] == '1':
    #         feedback += "We have opened all the records for you to review. "
    # else:
    #     feedback += "The question(s) you got wrong are " + ", ".join(wrong_attempts) + "\n"
    #     if not session[session['user_id'] + '_mode'] == '1':
    #         feedback += ". All the records have been opened so that you can review!"

    if len(wrong_attempts) == 0:
        feedback = "You got all of the questions in this page right! "
    else:
        feedback += "Please review the questions you got wrong. "
    
    if not session[session['user_id'] + '_mode'] == '1':
            feedback += "All the records have been opened so that you can review! "    

    feedback += 'Click on the next button to continue.'

    return jsonify(result=feedback, wrong_ids=wrong_ids, right_ids=right_ids, page_content=page_content)

@app.route('/introduction')
@state_machine('show_introduction')
def show_introduction():
    return render_template('introduction.html', uid=str(session['user_id']))


@app.route('/introduction2')
@state_machine('show_introduction2')
def show_introduction2():
    return render_template('introduction2.html', uid=str(session['user_id']))

@app.route('/pre_survey', methods=['GET', 'POST'])
@state_machine('pre_survey')
def pre_survey():
    if request.method == 'POST':
        user_data_key = str(session['user_id']) + '_user_data'
        formatted_data = "uid:" + session['user_id'] + "," + "type: pre_survey_data, value: "
        f = request.form
        for key in f:
            formatted_data += key + ":" + f[key] + "|" 
        formatted_data += ";"    
        r.append(user_data_key, formatted_data)
        return redirect('/next')
    if request.method == 'GET':
        return render_template('pre_survey.html', uid=str(session['user_id']))



@app.route('/post_survey', methods=['GET', 'POST'])
@state_machine('post_survey')
def post_survey():
    if request.method == 'POST':
        user_data_key = str(session['user_id']) + '_user_data'
        formatted_data = "uid:" + session['user_id'] + "," + "type: post_survey_data, value: '"
        f = request.form
        for key in f:
           formatted_data += key + ":" + f[key] + "|" 
        formatted_data += "';"    
        r.append(user_data_key, formatted_data)
        print(r.get(user_data_key))
        return redirect('/next')
    if request.method == 'GET':
        return render_template('post_survey.html', uid=str(session['user_id']), umode=session[session['user_id'] + '_mode'], ubudget=r.get(str(session['user_id'])+'_ustudy_budget'))

@app.route('/post_survey_scenario3', methods=['GET', 'POST'])
@state_machine('post_survey_scenario3')
def post_survey_scenario3():
    if request.method == 'POST':
        user_data_key = str(session['user_id']) + '_user_data'
        formatted_data = "uid:" + session['user_id'] + "," + "type: post_survey_data, value: '"
        f = request.form
        for key in f:
           formatted_data += key + ":" + f[key] + "|" 
        formatted_data += "';"    
        r.append(user_data_key, formatted_data)
        print(r.get(user_data_key))
        return redirect('/next')
    if request.method == 'GET':
        return render_template('post_survey_scenario3.html', uid=str(session['user_id']), umode=session[session['user_id'] + '_mode'], ubudget=r.get(str(session['user_id'])+'_ustudy_budget'))


@app.route('/save_data', methods=['GET', 'POST'])
def save_data():
    user_data = request.form['user_data']
    data_list = user_data.split(';')
    formatted_data = ''
    for line in data_list:
        if line:
            formatted_data += ('uid:'+str(session['user_id'])+','+line+';')
    user_data_key = str(session['user_id']) + '_user_data'
    r.append(user_data_key, formatted_data)
    return 'data_saved.'


@app.route('/get_cell', methods=['GET', 'POST'])
def open_cell():
    ret = dict()
    kapr_limit = 0
    
    if get_url_for_index(session['state']) == 'tutorial.show_tutorial_clickable_demo':
        working_data = DATA_CLICKABLE_DEMO
        full_data = DATASET_TUTORIAL
    elif get_url_for_index(session['state']) == 'tutorial.show_tutorial_clickable_decision_making_demo':
        working_data = DATA_DM_DEMO
        full_data = DATASET_TUTORIAL
        # kapr_limit = 100
        # float(r.get(session['user_id']+'tutorial_dmdemo_kapr_limit'))
    elif get_url_for_index(session['state']) == 'tutorial.show_tutorial_clickable_practice':
        working_data = DATA_CLICKABLE_PRACTICE
        full_data = DATASET_TUTORIAL
        if r.get(session['user_id']+'_ustudy_mode') == "4":
            kapr_limit = 20
    elif get_url_for_index(session['state']) == 'tutorial.show_tutorial_clickable_practice_post':
        working_data = DATA_CLICKABLE_PRACTICE
        full_data = DATASET_TUTORIAL
        # if r.get(session['user_id']+'_ustudy_mode') == "4":
        kapr_limit = 20
        # float(r.get(session['user_id']+'tutorial_practice_kapr_limit'))
    elif get_url_for_index(session['state']) == 'main_section.show_record_linkage_task':
        working_data = get_main_section_data(session['user_id'], 1)
        full_data = DATASET
        kapr_limit = float(r.get(str(session['user_id'])+'section1_kapr_limit'))
    # elif 'show_section' in get_url_for_index(session['state']):
    else:
        section = int(r.get(session['user_id']+'_main_section_num'))
        working_data = get_main_section_data(str(session['user_id']), section)
        working_data.set_kapr_size(6*6)
        full_data = DATASET2
        kapr_limit = float(r.get(str(session['user_id'])+'section'+str(section)+'_kapr_limit'))

    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    mode = request.args.get('mode')
    pair_num = str(id1.split('-')[0])
    attr_num = str(id1.split('-')[2])
    user_key = str(session['user_id'])
    ret = dm.open_cell(user_key, full_data, working_data, pair_num, attr_num, mode, r, kapr_limit)
    return jsonify(ret)


@app.route('/get_big_cell', methods=['GET', 'POST'])
def open_big_cell():
    ret = dict()

    kapr_limit = 0
    if get_url_for_index(session['state']) == 'tutorial.show_tutorial_clickable_demo':
        working_data = DATA_CLICKABLE_DEMO
        full_data = DATASET_TUTORIAL
    elif get_url_for_index(session['state']) == 'tutorial.show_tutorial_clickable_decision_making_demo':
        working_data = DATA_DM_DEMO
        full_data = DATASET_TUTORIAL
        # kapr_limit = float(r.get(session['user_id']+'tutorial_dmdemo_kapr_limit'))
    elif get_url_for_index(session['state']) == 'tutorial.show_tutorial_clickable_practice':
        working_data = DATA_CLICKABLE_PRACTICE
        full_data = DATASET_TUTORIAL
        if session["user_id"] + "_mode" == "4":
          kapr_limit = 20
        # float(r.get(session['user_id']+'tutorial_practice_kapr_limit'))
    elif get_url_for_index(session['state']) == 'tutorial.show_tutorial_clickable_practice_post':
        working_data = DATA_CLICKABLE_PRACTICE
        full_data = DATASET_TUTORIAL
        # if r.get(session['user_id']+'_ustudy_mode') == "4":
        kapr_limit = 20
    elif get_url_for_index(session['state']) == 'main_section.show_record_linkage_task':
        working_data = get_main_section_data(session['user_id'], 1)
        full_data = DATASET
        kapr_limit = float(r.get(session['user_id']+'section1_kapr_limit'))
    else:
        section = int(r.get(session['user_id']+'_main_section_num'))
        working_data = get_main_section_data(str(session['user_id']), section)
        working_data.set_kapr_size(6*6)
        full_data = DATASET2
        kapr_limit = float(r.get(str(session['user_id'])+'section'+str(section)+'_kapr_limit'))

    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    id3 = request.args.get('id3')
    id4 = request.args.get('id4')
    mode = request.args.get('mode')
    user_key = session['user_id']

    pair_num1 = str(id1.split('-')[0])
    attr_num1 = str(id1.split('-')[2])
    ret1 = dm.open_cell(user_key, full_data, working_data, pair_num1, attr_num1, mode, r, kapr_limit)
    pair_num2 = str(id3.split('-')[0])
    attr_num2 = str(id3.split('-')[2])
    ret2 = dm.open_cell(user_key, full_data, working_data, pair_num2, attr_num2, mode, r, kapr_limit)

    if ret2['result'] == 'fail':
        return jsonify(ret2)

    ret = {
        'value1': ret1['value1'],
        'value2': ret1['value2'],
        'value3': ret2['value1'],
        'value4': ret2['value2'],
        'id': ret1['id'],
        'mode': ret2['mode'],
        'KAPR': ret2['KAPR'],
        'result': ret2['result'],
        'new_delta': ret2['new_delta']
    }

    return jsonify(ret)


@app.route('/next', methods=['GET', 'POST'])
def next():
    sequence = config.SEQUENCE
    state = session['state'] + 1
    session['state'] += 1
    #user_id = session["user_id"]
    #r.set("session_"+str(user_id)+"_state", str(session['state']))
    return redirect(url_for(get_url_for_index(session['state'])))


@app.route('/pull_data')
def pull_data():
    user_data_key = session['user_id'] + '_user_data'
    user_data = r.get(user_data_key)
    if not user_data:
        return render_template('show_data.html', data='No data is collected for this user.', uid=str(session['user_id']))

    data = ud.parse_user_data(user_data)

    ret = ''
    for d in data:
        if 'type' in d and 'performance' in d['type']:
            section = re.findall(r'\d+', d['type'])[0]
            ret += ('section ' + section + ': ' + d['value'] + ';\n')
    #     if 'type' in d and d['type'] == 'performance1':
    #         ret += ('section 1: ' + d['value'] + ';\n')
    # for d in data:
    #     if 'type' in d and d['type'] == 'performance2':
    #         ret += ('section 2: ' + d['value'] + ';\n')
    for d in data:
        if 'type' in d and d['type'] == 'final_KAPR_section1':
            ret += ('Final privacy budget used in section 1: ' + str(round(100*float(d['value']), 2)) + '% out of ' + d['total'] + '%;\n')
    
    ret = ret + '\n' + user_data
    ret = ret.replace('\n', '<br />')

    return render_template('show_data.html', data=ret, uid=str(session['user_id']))


@app.route('/pull_data_all')
def pull_data_all():
    ret = ''
    for key in r.scan_iter("*_user_data"):
        user_data = r.get(key)
        ret = ret + user_data + '<br/><br/><br/>'
    return ret


@app.route('/thankyou')
@state_machine('show_thankyou')
def show_thankyou():
    
    user_data_key = session['user_id'] + '_user_data'
    
    session_end = {
        'uid': session['user_id'],
        'type': 'session_end',
        'value': int(time.time()),
        'timestamp': int(time.time()),
        'source': 'server'
    }
    r.append(user_data_key, ud.format_user_data(session_end))

    # grading section 2
    user_data_key = session['user_id'] + '_user_data'
    #r.append(user_data_key, 'type: session_end,timestamp: '+str(time.time())+';\n')
    user_data = r.get(user_data_key)
    data = ud.parse_user_data(user_data)
    result = ud.grade_final_answer(data, get_main_section_data(session['user_id'], 10))
    performance2 = {
        'uid': session['user_id'],
        'type': 'performance10',
        'value': str(result[0]) + ' out of ' + str(result[1]),
        'timestamp': int(time.time()),
        'source': 'server'
    }
    r.append(user_data_key, ud.format_user_data(performance2))

    # get final KAPR
    KAPR_key = session['user_id'] + '_KAPR'
    final_KAPR = r.get(KAPR_key)
    kapr_limit = r.get(session['user_id']+'section10_kapr_limit')
    if final_KAPR is not None and kapr_limit is not None:
        kapr_info = 'type:final_KAPR_section1, value:' + str(final_KAPR) + ',total:' + kapr_limit + ';\n'
        kapr_info = {
            'uid': session['user_id'],
            'type': 'final_KAPR_section10',
            'value': str(final_KAPR),
            'timestamp': int(time.time()),
            'source': 'server',
            'total': kapr_limit
        }
        r.append(user_data_key, ud.format_user_data(kapr_info))

    data = ud.parse_user_data(r.get(user_data_key))
    # dl.save_data_to_json('data/saved/'+str(session['user_id'])+'.json', user_data)
    extend_data = ''
    for d in data:
        if 'type' in d and d['type'] == 'performance1':
            extend_data += ('section 1: ' + d['value'] + ';\n')
    for d in data:
        if 'type' in d and d['type'] == 'performance2':
            extend_data += ('section 2: ' + d['value'] + ';\n')
    for d in data:
        if 'type' in d and d['type'] == 'final_KAPR_section1':
            extend_data += ('Final privacy budget used in section 1: ' + str(round(100*float(d['value']), 2)) + '% out of ' + d['total'] + '%;\n')
    extend_data = extend_data + r.get(user_data_key)

    # if r.get("data_choice_" + session['user_id']) != "collect":
    #     # print "discareded"
    #     r.delete(user_data_key)
    #     # print r.get(user_data_key)
    #     user_data = 'type:user_id,id:'+str(session['user_id'])+';\n'
    #     user_data = user_data + 'type:consent,value:NoDataCollection;\n'
    #     r.set(user_data_key, user_data)

    # send the data to email.
    #msg = Message(subject='user data: ' + session['user_id'], body=extend_data, recipients=['mindfil.ppirl@gmail.com'])
    #mail.send(msg)

    # clear user data in redis
    #for key in r.scan_iter("prefix:"+session['user_id']):
    #    r.delete(key)

    return render_template('thankyou.html', uid=str(session['user_id']))


'''
@app.route('/section1_start')
@state_machine('show_section1_startpage')
def show_section1_startpage():
    return render_template('section1_start.html')
'''

@app.route('/id')
def get_id():
    if session['user_id']:
        return str(session['user_id'])
    return 'Null'


@app.route('/flushdb')
def flush_redis():
    r.flushdb()
    return 'redis flushed.'

    admin_key = request.args.get("key")
    if r.get('admin_key' + admin_key) is not None:
        r.flushdb()
        return 'redis flushed.'
    else:
        return 'Failed: premission denied.'


@app.route('/save_data_choice', methods=['POST'])
def save_data_choice():
    data_choice = request.form.get('data_choice')
    r.set("data_choice_" + session['user_id'], data_choice)
    print r.get("data_choice_" + session['user_id'])
    return redirect(url_for('next'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.route('/get_ustudy_setting')
def get_ustudy_setting():
    user_id = session['user_id']
    ustudy_mode = r.get(user_id+'_ustudy_mode')
    ustudy_budget = r.get(user_id+'_ustudy_budget')
    result = 'mode:'+ustudy_mode
    ret = {
        'result': result,
    }
    return jsonify(ret)


