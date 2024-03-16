from flask import Flask, render_template, request, flash, redirect, url_for
import math

app = Flask(__name__)

app.config['SECRET_KEY'] = 'vzc qe432'

# Define a mapping between ranks and their corresponding Elo numbers
rank_to_elo = {
    "Iron": 1,
    "Bronze": 401,
    "Silver": 801,
    "Gold": 1201,
    "Platinum": 1601,
    "Emerald": 2001,
    "Diamond": 2401,
    "Apex": 2800,
}
tier_to_elo = {
    "4": 0,
    "3": 100,
    "2": 200,
    "1": 300,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get the form data
    current_rank = request.form['currentRank']
    goal_rank = request.form['goalRank']
    current_tier = request.form['currentTier']
    goal_tier = request.form['goalTier']
    current_lp = int(request.form['currentLP'])
    goal_lp = int(request.form['goalLP'])
    winrate = int(request.form['Winrate'])
    gains = int(request.form['LPgains'])
    losses = int(request.form['LPloss'])


    if current_lp < 0 or current_lp >= 100: #check that it's greater than 0 and less than 100
        flash('Error: current LP has to be at least 0 and below 100', category='error')
        return redirect(url_for('index'))
    
    if goal_lp < 0 or goal_lp >= 100: #check that it's greater than 0 and less than 100
        flash('Error: target LP has to be at least 0 and below 100', category='error')
        return redirect(url_for('index'))

    if winrate < 1 or winrate >= 100: #check that it's greater than 0 and less than 100
        flash('Error: Winrate has to be at least 0 and below 100', category='error')
        return redirect(url_for('index'))
    
    if gains < 1 or gains >= 100: #check that it's greater than 0 and less than 100
        flash('Error: LP gains has to be at least 0 and below 100', category='error')
        return redirect(url_for('index'))
    
    if losses < 1 or losses >= 100: #check that it's greater than 0 and less than 100
        flash('Error: LP losses has to be at least 0 and below 100', category='error')
        return redirect(url_for('index'))

    # Convert ranks to Elo numbers
    current_elo = rank_to_elo.get(current_rank, 0) + tier_to_elo.get(current_tier, 0) + current_lp
    goal_elo = rank_to_elo.get(goal_rank, 0) + tier_to_elo.get(goal_tier, 0) + goal_lp

    if current_elo >= goal_elo:
        flash('Error: you will climb!', category='error')
        return redirect(url_for('index'))
    
    # Perform calculations based on Elo numbers
    # For example, you can calculate the LP needed to reach the goal rank
    lp_needed = goal_elo-current_elo
    lp_ratio = winrate/100*gains - (100-winrate)/100*losses
    if lp_ratio == 0:
        return render_template('result.html', numGames="infinity", lp_needed=lp_needed)

    numGames = math.ceil( lp_needed/ lp_ratio)
    return render_template('result.html', numGames=numGames, lp_needed=lp_needed)

if __name__ == '__main__':
    app.run(debug=True)
