# Author: Alex Ksikes

import web
from config import db

def add(ids, score, user_id):
    if not 0 <= score <= 5 or not user_id or not ids: return
    for id in ids:
        db.query(
            'insert votes (user_id, applicant_id, score)' +
            ' values ($user_id, $applicant_id, $score)' + 
            ' on duplicate key update' + 
            ' user_id = $user_id, applicant_id = $applicant_id, score = $score',
            vars = dict(user_id=user_id, applicant_id=id, score=score))
        update_calculated_votes(id)
        
def update_calculated_votes(applicant_id):
    calculated = \
    db.select('votes', 
        vars = dict(applicant_id=applicant_id),
        what = 'sum(score) / count(score) as vote, count(score) as vote_counts',       
        where = 'applicant_id = $applicant_id')[0]
    
    db.update('applicants', 
        vars = dict(id=applicant_id),
        where = 'id = $id',
        calculated_vote = calculated.vote, calculated_vote_counts = calculated.vote_counts)

def get_votes(applicant_id):
    return db.select('votes as v, users as u',
        vars = dict(id=applicant_id),       
        what = 'v.*, nickname',
        where = 'applicant_id = $id and v.user_id = u.id',
        order = 'creation_ts')