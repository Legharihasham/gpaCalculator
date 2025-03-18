document.addEventListener('DOMContentLoaded', function() {
    // Add Course Button
    document.getElementById('addCourse').addEventListener('click', function() {
        const template = document.querySelector('.course-entry').cloneNode(true);
        template.querySelectorAll('input, select').forEach(input => input.value = '');
        document.getElementById('courseList').appendChild(template);
    });

    // Add Semester Button
    document.getElementById('addSemester').addEventListener('click', function() {
        const template = document.querySelector('.semester-entry').cloneNode(true);
        template.querySelectorAll('input').forEach(input => input.value = '');
        document.getElementById('semesterList').appendChild(template);
    });

    // Remove Course/Semester Button Delegation
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-course')) {
            const courseEntries = document.querySelectorAll('.course-entry');
            if (courseEntries.length > 1) {
                e.target.closest('.course-entry').remove();
            }
        }
        if (e.target.classList.contains('remove-semester')) {
            const semesterEntries = document.querySelectorAll('.semester-entry');
            if (semesterEntries.length > 1) {
                e.target.closest('.semester-entry').remove();
            }
        }
    });

    // GPA Form Submission
    document.getElementById('gpaForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const courses = [];
        let semesterCredits = 0;
        
        document.querySelectorAll('.course-entry').forEach(entry => {
            const credits = parseFloat(entry.querySelector('.credits').value);
            const grade = entry.querySelector('.grade').value;
            
            if (credits && grade) {
                courses.push({
                    credits: credits,
                    grade: grade
                });
                semesterCredits += credits;
            }
        });

        // Get current CGPA and total credits
        const currentCGPA = parseFloat(document.getElementById('currentCGPA').value) || 0;
        const totalCreditsCompleted = parseFloat(document.getElementById('totalCreditsCompleted').value) || 0;

        fetch('/calculate_gpa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                courses: courses,
                currentCGPA: currentCGPA,
                totalCreditsCompleted: totalCreditsCompleted
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            document.getElementById('gpaResult').textContent = data.gpa.toFixed(2);
            document.getElementById('semesterCredits').textContent = semesterCredits;
            document.getElementById('newCGPAResult').textContent = data.newCGPA.toFixed(2);
            document.getElementById('totalCredits').textContent = data.total_credits;
            document.querySelector('.result-section').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while calculating GPA');
        });
    });

    // CGPA Form Submission
    document.getElementById('cgpaForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const semesters = [];
        document.querySelectorAll('.semester-entry').forEach(entry => {
            const credits = parseFloat(entry.querySelector('.credits').value);
            const gpa = parseFloat(entry.querySelector('.gpa').value);
            
            if (credits && gpa) {
                semesters.push({
                    credits: credits,
                    gpa: gpa
                });
            }
        });

        fetch('/calculate_cgpa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ semesters: semesters })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            document.getElementById('cgpaResult').textContent = data.cgpa.toFixed(2);
            document.getElementById('cgpaTotalCredits').textContent = data.total_credits;
            document.querySelector('.cgpa-result-section').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while calculating CGPA');
        });
    });
}); 