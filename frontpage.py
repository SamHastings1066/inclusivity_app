import streamlit as st
import pandas as pd
import os
import openai
import json
import regex as re

#st.set_page_config(layout="wide")

st.markdown(
  """
  <style>
  .css-qrbaxs {
    font-size: 18px;
    color: rgb(25 52 213);
}
.css-jhf39w {
    font-size: 18px;
    color: rgb(25 52 213);
}
.st-fs {
    background: rgb(51 216 24 / 25%);
}
.css-15yebgu {
    color: rgb(57 167 12);
}
.css-jv3mmh {
    background-color: rgb(57, 167, 12);
}
.st-bp {
    font-size: 18px;
}
  </style>
  """,
  unsafe_allow_html = True
)

def my_widget():
  col1, col2, col3 = st.columns(3)
  racist = col1.checkbox('Racism', value = 0)
  sexist = col2.checkbox('Sexism', value = 0)
  transphobic = col3.checkbox('Transphobia', value = 0)
  return racist, sexist, transphobic

my_expander = st.expander("Scan settings", expanded=True)
with my_expander:
    racist, sexist, transphobic = my_widget()

chappelle = '''What… what is a woman? What is that, in this day and time? Is there even such a thing as a woman or a man or anything? Hmm. Hmm? Seems to be a question nowadays. Now listen, women get mad at me gay people get mad at me, lesbians get mad at me, but I’m gonna tell you right now, and this is true… these transgenders… the n*ggas want me dead.'''

user_query = st.text_area(label = 'Enter the text you would like scanned:',
#value = chappelle,
placeholder = 'Enter text here',
help = '''Analysis is completed using the GPT3 Davinci model.''')

prompt_general = '''Give this paragraph a score from 0-10 based on how {} it is and \
explain the score: "{}". Give your response in the format of a python dictionary, \
using double quotes, with a score" key corresponding to the score and a "reason" \
key corresponding to the reason'''


# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")


# --- Initialising SessionState ---
if "racist_response" not in st.session_state:
  st.session_state.racist_response = ""
if "sexist_response" not in st.session_state:
  st.session_state.sexist_response = ""
if "transphobic_response" not in st.session_state:
  st.session_state.transphobic_response = ""

def progess_decorator(func):
  def wrapper(ism):
    with st.spinner('Calculating {} score...'.format(ism)):
      return func(ism)
  return wrapper

@progess_decorator
def response(ism):
  prompt = prompt_general.format(ism, user_query)
  response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, temperature=0.3, max_tokens=1000)
  text = response.choices[0].text
  #st.write(text)
  dictionary_reg = re.compile(r'(?<={)[^}]*(?=})')
  dict_string = "{" + dictionary_reg.search(text).group() + "}"
  #dict_string = dict_string.replace("'", '"')
  result = json.loads(dict_string)
  score = result['score']
  reason = result['reason']
  return score, reason


def write_response(score, reason, ism):
  st.slider(label = "{} score: {}".format(ism, score) , min_value=0, max_value=10, value=score,
  disabled = True)
  st.write("Reason for score: " + reason)



col1, col2 = st.columns(2)
scan_button = col1.button('Scan text', on_click=None)
reset_button = col2.button('Reset results', on_click=None)

# reset the responses
if reset_button == True:
  st.session_state.racist_response = st.session_state.sexist_response = \
  st.session_state.transphobic_response = ""

# only if scan button clicked AND response is empty, then query gpt3
if scan_button == True:
  if st.session_state.racist_response == "" and racist:
    racist_score, racist_reason = response('racist')
    st.session_state.racist_response = {'score': racist_score,
    'reason': racist_reason}
  if st.session_state.sexist_response == "" and sexist:
    sexist_score, sexist_reason = response('sexist')
    st.session_state.sexist_response = {'score': sexist_score,
    'reason': sexist_reason}
  if st.session_state.transphobic_response == "" and transphobic:
    transphobic_score, transphobic_reason = response('transphobic')
    st.session_state.transphobic_response = {'score': transphobic_score,
    'reason': transphobic_reason}


# if check boxes are cliked on and off this will not wipe the response result
if st.session_state.racist_response != "" and racist:
  write_response(st.session_state.racist_response['score'],
  st.session_state.racist_response['reason'], 'racism')
if st.session_state.sexist_response != "" and sexist:
  write_response(st.session_state.sexist_response['score'],
  st.session_state.sexist_response['reason'], 'sexism')
if st.session_state.transphobic_response != "" and transphobic:
  write_response(st.session_state.transphobic_response['score'],
  st.session_state.transphobic_response['reason'], 'transphobia')



#max_tokens:
#  sets an upper bound on how many tokens the API will return
#  defaults to 16
#  range [0, 2048] for davinci, although it is [0, 4096] for some newer models 1 800 829 1040

