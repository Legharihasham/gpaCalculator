from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

GRADE_POINTS = {
    'A': 4.00,
    'A-': 3.75,
    'B+': 3.50,
    'B': 3.00,
    'C+': 2.50,
    'C': 2.00,
    'D+': 1.50,
    'D': 1.00,
    'F': 0.00,
    'W': None
}

@app.route('/')
def index():
    return render_template('index.html', grade_points=GRADE_POINTS)

@app.route('/calculate_gpa', methods=['POST'])
def calculate_gpa():
    try:
        data = request.get_json()
        courses = data.get('courses', [])
        
        if not courses:
            return jsonify({'error': 'No courses provided'}), 400

        total_points = 0
        total_credits = 0

        for course in courses:
            grade = course.get('grade')
            credits = float(course.get('credits', 0))
            
            if grade not in GRADE_POINTS or GRADE_POINTS[grade] is None:
                continue
                
            total_points += GRADE_POINTS[grade] * credits
            total_credits += credits

        if total_credits == 0:
            return jsonify({'error': 'No valid courses to calculate GPA'}), 400

        gpa = total_points / total_credits
        return jsonify({
            'gpa': round(gpa, 2),
            'total_credits': total_credits
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate_cgpa', methods=['POST'])
def calculate_cgpa():
    try:
        data = request.get_json()
        semesters = data.get('semesters', [])
        
        if not semesters:
            return jsonify({'error': 'No semesters provided'}), 400

        total_points = 0
        total_credits = 0

        for semester in semesters:
            credits = float(semester.get('credits', 0))
            gpa = float(semester.get('gpa', 0))
            
            total_points += gpa * credits
            total_credits += credits

        if total_credits == 0:
            return jsonify({'error': 'No valid semesters to calculate CGPA'}), 400

        cgpa = total_points / total_credits
        return jsonify({
            'cgpa': round(cgpa, 2),
            'total_credits': total_credits
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 