from app import db
from datetime import datetime

# 회원
class Users(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False) # unique 추가해야 함.
    password = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(50)) # 회원 프로필 사진
    postings = db.relationship("Postings", backref="writer", lazy=True)
    comments = db.relationship("Comments", backref="writer", lazy=True) # 이걸로 사용자가 작성한 모든 댓글 조회 가능

    def __repr__(self) :
        return f'User: {self.email}'

# 게시글
class Postings(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", onupdate="CASCADE"), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self) :
        return f'Postings: {self.title}({self.created})'

# 댓글
class Comments(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", onupdate="CASCADE"), nullable=False)
    posting_id = db.Column(db.Integer, db.ForeignKey("postings.id", onupdate="CASCADE"), nullable=False) # 댓글 달린 게시글 번호
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self) :
        return f'Comments: posted on {self.posting_id}({self.created})'