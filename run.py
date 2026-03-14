from putninalozi import app, db
import sys
sys.stdout.reconfigure(encoding='utf-8')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True)
