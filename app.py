from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "im_so_awesome"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def survey_start():
    """Start a survey."""

    return render_template('survey_start.html', survey=survey)

@app.route('/begin', methods=['POST'])
def begin_survey():
    """Begin a survey."""
    session[RESPONSES_KEY] = []
    
    return redirect("/questions/0")
    
@app.route('/answer', methods=['POST'])
def handle_answer():
    """Save answer and redirect to next question."""
    choice = request.form['answer']

     # add current response to session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        #  all questions answered! Congratulate them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # accessing question page too early
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "questions.html", question_num=qid, question=question)

@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("complete.html")
