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
    data_num = int(uid)%10
    if data_num == 0:
        data_num = 10
    data_num -= 1

    if section == 1:
        return DATA_SECTION1[data_num]
    else:
        return DATA_SECTION2[data_num]

def get_sequence_for_mode():
    return config.SEQUENCE['Mode_'+r.get(str(session['user_id'])+'_ustudy_mode')]

def get_url_for_index(index):
    return get_sequence_for_mode()[int(index)]

@app.route('/')
@app.route('/index')
def index():
    user_id = 0
    if request.args.get("id") is None:
        user_id = str(r.incr('user_id_generator'))
        r.set('user_id_'+user_id, user_id)
        ustudy_mode = request.args.get('mode')
        ustudy_budget = request.args.get('budget')
        if ustudy_mode is None:
            ustudy_mode = '1'
        if ustudy_budget is None:
            ustudy_budget = '0'
        if ustudy_mode != '4':
            ustudy_budget = '0'
        if int(ustudy_mode) not in [1,2,3,4]:
            return page_not_found('page_not_found')
        if ustudy_budget not in ['moderate', 'minimum']:
            if float(ustudy_budget) < 0 or float(ustudy_budget) > 100:
                return page_not_found('page_not_found')
    else:
        user_id = str(request.args.get("id"))
        if r.get('user_id_' + user_id) is None:
            return render_template('user_not_found.html')
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
        session['state'] = index
    
    

    # saving user data
    data = {
        'uid': user_id,
        'type': 'session_start',
        'value': int(time.time()),
        'timestamp': int(time.time()),
        'source': 'server'
    }
    r.set(user_data_key, ud.format_user_data(data))

    r.set("session_"+str(user_id), session)

    r.set(str(session['user_id'])+'_ustudy_mode', ustudy_mode)
    r.set(str(session['user_id'])+'_ustudy_budget', ustudy_budget)

    return redirect(url_for(get_url_for_index(index)))

    

@app.route('/feedback_main_section')
def feedback_main_section():
    ids = request.args.get('ids').split(',')
    responses = request.args.get('responses').split(',')
    screen_ids = request.args.get('screen_ids').split(',')
    working_data = get_main_section_data(session['user_id'], 1)
    wrong_attempts = []
    feedback = ""
    for i in range(6):
        dp = working_data.get_data_pair(int(ids[i]))
        grade = dp.grade(int(responses[i]))
        # grades.append(grade)
        if not grade:
            wrong_attempts.append(screen_ids[i])

    if len(wrong_attempts) == 0:
        feedback = "You got all of the questions in this page right!"
    else:
        feedback += "Question(s) you got wrong: " + ", ".join(wrong_attempts) + "\n"
        # feedback += "You might want to consider opening more relevant information if it would help you get more questions right."

    return jsonify(result=feedback)

@app.route('/introduction')
@state_machine('show_introduction')
def show_introduction():
    return render_template('introduction.html', uid=str(session['user_id']))


@app.route('/introduction2')
@state_machine('show_introduction2')
def show_introduction2():
    return render_template('introduction2.html', uid=str(session['user_id']))


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
        if session["user_id"] + "_mode" == "4":
            kapr_limit = 20
        # float(r.get(session['user_id']+'tutorial_practice_kapr_limit'))
    elif get_url_for_index(session['state']) == 'main_section.show_record_linkage_task':
        working_data = get_main_section_data(session['user_id'], 1)
        full_data = DATASET
        kapr_limit = float(r.get(str(session['user_id'])+'section1_kapr_limit'))
    else:
        working_data = get_main_section_data(str(session['user_id']), 2)
        full_data = DATASET2

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
    if session['state'] == 13:
        working_data = DATA_CLICKABLE_DEMO
        full_data = DATASET_TUTORIAL
    elif session['state'] == 24:
        working_data = DATA_DM_DEMO
        full_data = DATASET_TUTORIAL
        # kapr_limit = float(r.get(session['user_id']+'tutorial_dmdemo_kapr_limit'))
    elif session['state'] == 29:
        working_data = DATA_CLICKABLE_PRACTICE
        full_data = DATASET_TUTORIAL
        kapr_limit = 20
        # float(r.get(session['user_id']+'tutorial_practice_kapr_limit'))
    elif session['state'] == 31:
        working_data = get_main_section_data(session['user_id'], 1)
        full_data = DATASET
        kapr_limit = float(r.get(session['user_id']+'section1_kapr_limit'))
    else:
        working_data = get_main_section_data(session['user_id'], 2)
        full_data = DATASET2

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
    user_id = session["user_id"]
    r.set("session_"+str(user_id)+"_state", str(session['state']))
    #timing info on next click 
    # timing_info = sequence[session['state']-1] + ": " + time.strftime("%a, %d %b %Y %H:%M:%S")
    # msg = Message(subject='user click: ' + session['user_id'], body=timing_info, recipients=['ppirl.mindfil@gmail.com'])
    # mail.send(msg)
 
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
        if 'type' in d and d['type'] == 'performance1':
            ret += ('section 1: ' + d['value'] + ';\n')
    for d in data:
        if 'type' in d and d['type'] == 'performance2':
            ret += ('section 2: ' + d['value'] + ';\n')
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

    # grading section 1
    user_data = r.get(user_data_key)
    data = ud.parse_user_data(user_data)
    result = ud.grade_final_answer(data, get_main_section_data(session['user_id'], 1))
    # saving user data
    performance1 = {
        'uid': session['user_id'],
        'type': 'performance1',
        'value': str(result[0]) + ' out of ' + str(result[1]),
        'timestamp': int(time.time()),
        'source': 'server'
    }
    r.append(user_data_key, ud.format_user_data(performance1))

    # grading section 2
    user_data_key = session['user_id'] + '_user_data'
    #r.append(user_data_key, 'type: session_end,timestamp: '+str(time.time())+';\n')
    user_data = r.get(user_data_key)
    data = ud.parse_user_data(user_data)
    # TODO! TODO! TODO! TODO! TODO! TODO! TODO! TODO! TODO! TODO! 
    # SECTION 2 pair num must be different from section 1! section 2 num be a factor of 6
    result = ud.grade_final_answer(data, get_main_section_data(session['user_id'], 2))
    performance2 = {
        'uid': session['user_id'],
        'type': 'performance2',
        'value': str(result[0]) + ' out of ' + str(result[1]),
        'timestamp': int(time.time()),
        'source': 'server'
    }
    r.append(user_data_key, ud.format_user_data(performance2))

    # get final KAPR
    KAPR_key = session['user_id'] + '_KAPR'
    final_KAPR = r.get(KAPR_key)
    kapr_limit = r.get(session['user_id']+'section1_kapr_limit')
    if final_KAPR is not None:
        kapr_info = 'type:final_KAPR_section1, value:' + str(final_KAPR) + ',total:' + kapr_limit + ';\n'
        kapr_info = {
            'uid': session['user_id'],
            'type': 'final_KAPR_section1',
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

    if r.get("data_choice_" + session['user_id']) != "collect":
        # print "discareded"
        r.delete(user_data_key)
        # print r.get(user_data_key)
        user_data = 'type:user_id,id:'+str(session['user_id'])+';\n'
        user_data = user_data + 'type:consent,value:NoDataCollection;\n'
        r.set(user_data_key, user_data)

    # send the data to email.
    msg = Message(subject='user data: ' + session['user_id'], body=extend_data, recipients=['mindfil.ppirl@gmail.com'])
    mail.send(msg)

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

