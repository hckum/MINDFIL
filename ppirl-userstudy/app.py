from flask import Flask, render_template, redirect, url_for, session, jsonify, request, g
from functools import wraps
import time
from random import *
import data_loader as dl
import data_display as dd
import json


app = Flask(__name__)


CONFIG = {
    'sequence': [
        'show_introduction',
        'show_introduction2',
        'show_RL_tutorial',
        'show_instruction_base_mode',
        'show_pratice_base_mode',
        'show_instruction_full_mode',
        'show_pratice_full_mode',
        'show_privacy_in_RL',
        'show_instruction_masked_mode',
        'show_pratice_masked_mode',
        'show_instruction_minimum_mode',
        'show_pratice_minimum_mode',
        'show_instruction_moderate_mode',
        'show_pratice_moderate_mode',
        'show_instruction_ppirl',
        'show_record_linkage_task',
        'show_thankyou'
    ]
}


def state_machine(function_name):
    def wrapper(f):
        @wraps(f)
        def inner_wrapper(*args, **kwargs):
            sequence = CONFIG['sequence']
            for i in range(len(sequence)):
                if sequence[i] == function_name:
                    session['state'] = i
                    break
            return f(*args, **kwargs)
        return inner_wrapper
    return wrapper


@app.route('/')
def show_record_linkages():
    session['user'] = str(time.time()) + '.' + str(randint(1,10000))
    session['data'] = dict()
    session['data']['practice'] = ''
    session['data']['start_time'] = time.time()
    return redirect(url_for('show_introduction'))
    #return render_template('record_linkage.html')


@app.route('/introduction')
@state_machine('show_introduction')
def show_introduction():
    return render_template('introduction.html')


@app.route('/introduction2')
@state_machine('show_introduction2')
def show_introduction2():
    return render_template('introduction2.html')


@app.route('/RL_tutorial')
@state_machine('show_RL_tutorial')
def show_RL_tutorial():
    return render_template('RL_tutorial.html')


@app.route('/privacy_in_RL')
@state_machine('show_privacy_in_RL')
def show_privacy_in_RL():
    return render_template('privacy.html')


@app.route('/instructions/base_mode')
@state_machine('show_instruction_base_mode')
def show_instruction_base_mode():
    return render_template('instruction_base_mode.html')


@app.route('/instructions/full_mode')
@state_machine('show_instruction_full_mode')
def show_instruction_full_mode():
    return render_template('instruction_full_mode.html')


@app.route('/instructions/masked_mode')
@state_machine('show_instruction_masked_mode')
def show_instruction_masked_mode():
    return render_template('instruction_masked_mode.html')


@app.route('/instructions/minimum_mode')
@state_machine('show_instruction_minimum_mode')
def show_instruction_minimum_mode():
    return render_template('instruction_minimum_mode.html')


@app.route('/instructions/moderate_mode')
@state_machine('show_instruction_moderate_mode')
def show_instruction_moderate_mode():
    return render_template('instruction_moderate_mode.html')


@app.route('/instructions/encrypted_mode')
@state_machine('show_instruction_encrypted_mode')
def show_instruction_encrypted_mode():
    return render_template('instruction_encrypted_mode.html')


@app.route('/instructions/ppirl')
@state_machine('show_instruction_ppirl')
def show_instruction_ppirl():
    return render_template('instruction_ppirl.html')


@app.route('/practice/base_mode')
@state_machine('show_pratice_base_mode')
def show_pratice_base_mode():
    pairs = dl.load_data_from_csv('data/practice_base_mode.csv')
    pairs_formatted = dd.format_data(pairs, 'base')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = (len(pairs)/2)*[7*['']]
    return render_template('record_linkage_d.html', data=data, icons=icons, title='Base mode', thisurl='/practice/base_mode')


@app.route('/practice/full_mode')
@state_machine('show_pratice_full_mode')
def show_pratice_full_mode():
    pairs = dl.load_data_from_csv('data/practice_full_mode.csv')
    pairs_formatted = dd.format_data(pairs, 'full')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('record_linkage_d.html', data=data, icons=icons, title='Full mode', thisurl='/practice/full_mode')


@app.route('/practice/masked_mode')
@state_machine('show_pratice_masked_mode')
def show_pratice_masked_mode():
    pairs = dl.load_data_from_csv('data/practice_masked_mode.csv')
    pairs_formatted = dd.format_data(pairs, 'masked')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('record_linkage_d.html', data=data, icons=icons, title='Masked mode', thisurl='/practice/masked_mode')


@app.route('/practice/minimum_mode')
@state_machine('show_pratice_minimum_mode')
def show_pratice_minimum_mode():
    pairs = dl.load_data_from_csv('data/practice_minimum_mode.csv')
    pairs_formatted = dd.format_data(pairs, 'minimum')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('record_linkage_d.html', data=data, icons=icons, title='Minimum mode', thisurl='/practice/minimum_mode')


@app.route('/practice/moderate_mode')
@state_machine('show_pratice_moderate_mode')
def show_pratice_moderate_mode():
    pairs = dl.load_data_from_csv('data/practice_moderate_mode.csv')
    pairs_formatted = dd.format_data(pairs, 'moderate')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('record_linkage_d.html', data=data, icons=icons, title='Moderate mode', thisurl='/practice/moderate_mode')


@app.route('/practice/<table_mode>/grading')
def grade_pratice_full_mode(table_mode):
    data_file = 'practice_' + str(table_mode) + '.csv'
    ret = list()
    print(session['data'])
    session['data']['practice'] = session['data']['practice'] +  request.args.get('response') + '\n'
    print(session['data'])
    responses = request.args.get('response').split(',')
    pairs = dl.load_data_from_csv('data/' + data_file)
    j = 0
    all_correct = True
    for i in range(0, len(pairs), 2):
        result = False
        j += 1
        q = 'q' + str(j)
        answer = pairs[i][17]
        if answer == '1' and (q+'a4' in responses or q+'a5' in responses or q+'a6' in responses):
            result = True
        if answer == '0' and (q+'a1' in responses or q+'a2' in responses or q+'a3' in responses):
            result = True
        if not result:
            ret.append('<div>' + pairs[i][18] + '</div>')
            all_correct = False
    if all_correct:
        ret.append('<div>Good job!</div>')
    return jsonify(result=ret)


@app.route('/record_linkage')
@state_machine('show_record_linkage_task')
def show_record_linkage_task():
    pairs = dl.load_data_from_csv('data/ppirl.csv')
    pairs_formatted = dd.format_data(pairs, 'masked')
    data = zip(pairs_formatted[0::2], pairs_formatted[1::2])
    icons = dd.generate_icon(pairs)
    return render_template('record_linkage_d.html', data=data, icons=icons, title='PPIRL Framework')


@app.route('/thankyou')
@state_machine('show_thankyou')
def show_thankyou():
    session['data']['end_time'] = time.time()
    print(session['data'])
    dl.save_data_to_json('data/saved/'+str(session['user'])+'.json', session['data'])
    return render_template('thankyou.html')


@app.route('/select')
def select_panel():
    return render_template('select_panel2.html')


@app.route('/test')
def test():
    return render_template('bootstrap_test.html')


@app.route('/next')
def next():
    sequence = CONFIG['sequence']
    state = session['state'] + 1
    session['state'] += 1

    return redirect(url_for(sequence[state]))


app.secret_key = 'a9%z$/`9h8FMnh893;*g783'