# Author: Alex Ksikes

import web
from config import db

def add_comment(user_id, applicant_id, comment):
    db.insert('comments', 
        user_id=user_id, applicant_id=applicant_id, comment=comment)

def delete_comment(user_id, id):
    db.delete('comments',
        vars = dict(user_id=user_id, id=id),
        where = 'user_id = $user_id and id = $id')
    
def get_comments(applicant_id):
    return db.query(
        '''select c.*, nickname, score \
        from comments as c 
        left join users as u on c.user_id = u.id 
        left join votes as v on u.id = v.user_id and v.applicant_id = $id
        where c.applicant_id = $id
        order by c.creation_ts desc''',
        vars = dict(id=applicant_id))