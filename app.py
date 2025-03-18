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
        current_cgpa = float(data.get('currentCGPA', 0))
        total_credits_completed = float(data.get('totalCreditsCompleted', 0))
        
        if not courses:
            return jsonify({'error': 'No courses provided'}), 400

        # Calculate semester GPA
        semester_points = 0
        semester_credits = 0

        for course in courses:
            grade = course.get('grade')
            credits = float(course.get('credits', 0))
            
            if grade not in GRADE_POINTS or GRADE_POINTS[grade] is None:
                continue
                
            semester_points += GRADE_POINTS[grade] * credits
            semester_credits += credits

        if semester_credits == 0:
            return jsonify({'error': 'No valid courses to calculate GPA'}), 400

        semester_gpa = semester_points / semester_credits

        # Calculate new CGPA if current CGPA is provided
        new_cgpa = semester_gpa
        total_credits = semester_credits

        if current_cgpa > 0 and total_credits_completed > 0:
            previous_points = current_cgpa * total_credits_completed
            new_total_credits = total_credits_completed + semester_credits
            new_cgpa = (previous_points + semester_points) / new_total_credits
            total_credits = new_total_credits

        return jsonify({
            'gpa': round(semester_gpa, 2),
            'newCGPA': round(new_cgpa, 2),
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