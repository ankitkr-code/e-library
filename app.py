import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='template')
app.secret_key = 'replace-with-a-safe-secret'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

students = []

programs = []

books = []

locations = []

library_cards = []

issued_books = []

transactions = []

users = {}

syllabus_items = []

notices = []

class_notes = []

academic_tasks = []

pending_registrations = []

def load_data():
    global students, programs, books, locations, library_cards, issued_books, transactions, users, syllabus_items, notices, class_notes, academic_tasks, pending_registrations
    try:
        with open('data/students.json', 'r') as f:
            students = json.load(f)
    except FileNotFoundError:
        students = []
    try:
        with open('data/programs.json', 'r') as f:
            programs = json.load(f)
    except FileNotFoundError:
        programs = []
    try:
        with open('data/books.json', 'r') as f:
            books = json.load(f)
    except FileNotFoundError:
        books = []
    try:
        with open('data/locations.json', 'r') as f:
            locations = json.load(f)
    except FileNotFoundError:
        locations = []
    try:
        with open('data/library_cards.json', 'r') as f:
            library_cards = json.load(f)
    except FileNotFoundError:
        library_cards = []
    try:
        with open('data/issued_books.json', 'r') as f:
            issued_books = json.load(f)
    except FileNotFoundError:
        issued_books = []
    try:
        with open('data/transactions.json', 'r') as f:
            transactions = json.load(f)
    except FileNotFoundError:
        transactions = []
    try:
        with open('data/users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    try:
        with open('data/syllabus.json', 'r') as f:
            syllabus_items = json.load(f)
    except FileNotFoundError:
        syllabus_items = []
    try:
        with open('data/notices.json', 'r') as f:
            notices = json.load(f)
    except FileNotFoundError:
        notices = []
    try:
        with open('data/class_notes.json', 'r') as f:
            class_notes = json.load(f)
    except FileNotFoundError:
        class_notes = []
    try:
        with open('data/academic_tasks.json', 'r') as f:
            academic_tasks = json.load(f)
    except FileNotFoundError:
        academic_tasks = []
    try:
        with open('data/pending_registrations.json', 'r') as f:
            pending_registrations = json.load(f)
    except FileNotFoundError:
        pending_registrations = []

def save_students():
    with open('data/students.json', 'w') as f:
        json.dump(students, f, indent=4)

def save_programs():
    with open('data/programs.json', 'w') as f:
        json.dump(programs, f, indent=4)

def save_books():
    with open('data/books.json', 'w') as f:
        json.dump(books, f, indent=4)

def save_locations():
    with open('data/locations.json', 'w') as f:
        json.dump(locations, f, indent=4)

def save_library_cards():
    with open('data/library_cards.json', 'w') as f:
        json.dump(library_cards, f, indent=4)

def save_issued_books():
    with open('data/issued_books.json', 'w') as f:
        json.dump(issued_books, f, indent=4)

def save_transactions():
    with open('data/transactions.json', 'w') as f:
        json.dump(transactions, f, indent=4)

def save_users():
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=4)

def save_syllabus():
    with open('data/syllabus.json', 'w') as f:
        json.dump(syllabus_items, f, indent=4)

def save_notices():
    with open('data/notices.json', 'w') as f:
        json.dump(notices, f, indent=4)

def save_class_notes():
    with open('data/class_notes.json', 'w') as f:
        json.dump(class_notes, f, indent=4)

def save_academic_tasks():
    with open('data/academic_tasks.json', 'w') as f:
        json.dump(academic_tasks, f, indent=4)

def save_pending_registrations():
    with open('data/pending_registrations.json', 'w') as f:
        json.dump(pending_registrations, f, indent=4)

def department_options():
    values = set()
    for program in programs:
        if program.get('department'):
            values.add(program['department'])
    for student in students:
        if student.get('program'):
            values.add(student['program'])
    for item in syllabus_items:
        if item.get('department'):
            values.add(item['department'])
    return sorted(values)

def filter_by_department(items, department):
    if not department:
        return items
    return [item for item in items if item.get('department') == department]

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Admin access only.', 'danger')
            return redirect(url_for('dashboard'))
        return view(*args, **kwargs)
    return wrapped

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def book_recommendations(keyword, username, history=None):
    keyword = (keyword or '').strip().lower()
    history = history or []
    recommended = []
    user_books = [t['book'] for t in transactions if t['student'] == username and t['type'] == 'Issue']
    history_categories = {book['category'] for book in books if book['title'] in user_books}
    keywords = keyword.split()
    category_map = {
        'python': 'Coding', 'flask': 'Coding', 'algorithm': 'Coding', 'data': 'Coding',
        'math': 'Mathematics', 'calculus': 'Mathematics', 'algebra': 'Mathematics', 'discrete': 'Mathematics',
    }

    for book in books:
        book_text = ' '.join([book['title'], book['author'], book['category'], book.get('isbn', ''), book.get('location', '')]).lower()
        score = 0
        if keyword and keyword in book_text:
            score += 3
        for term in keywords:
            if term in book_text:
                score += 2
            if category_map.get(term) == book['category']:
                score += 2
        if book['category'] in history_categories:
            score += 1
        if any(term in book['title'].lower() for term in keywords):
            score += 1
        if score > 0:
            recommended.append((score, book))

    if not recommended and history_categories:
        for book in books:
            if book['category'] in history_categories:
                recommended.append((1, book))

    if not recommended:
        recommended = [(0, book) for book in books]

    recommended.sort(key=lambda item: (-item[0], item[1]['title']))
    recommended_books = [item[1] for item in recommended]

    if keyword:
        response = f"Here are books related to '{keyword}':"
    elif history:
        response = 'Based on your recent activity, these books may interest you:'
    else:
        response = 'Here are some popular book suggestions for you:'

    return recommended_books[:6], response

# ===================== CHATBOT SEARCH FUNCTIONS =====================
def search_tokens(value):
    return [token for token in ''.join(ch.lower() if ch.isalnum() else ' ' for ch in value or '').split() if len(token) >= 2]

def exact_word_match(query, values):
    query_terms = search_tokens(query)
    if not query_terms:
        return False

    text_terms = set()
    for value in values:
        text_terms.update(search_tokens(str(value or '')))

    return all(any(token_matches(term, text_term) for text_term in text_terms) for term in query_terms)

def token_matches(query_term, text_term):
    if query_term == text_term:
        return True
    if len(query_term) >= 4 and text_term.startswith(query_term):
        return True
    return False

def contains_phrase(query, values):
    query = (query or '').strip().lower()
    if len(query) < 3:
        return False
    return any(query in str(value or '').lower() for value in values)

def matches_query(query, values, aliases=None):
    aliases = aliases or []
    values = list(values) + aliases
    return exact_word_match(query, values) or contains_phrase(query, values)

def search_books(query):
    """Search books by title, author, category, ISBN, or location."""
    results = []
    for book in books:
        if matches_query(query, [
            book.get('title', ''),
            book.get('author', ''),
            book.get('category', ''),
            book.get('isbn', ''),
            book.get('location', ''),
        ], aliases=['book', 'books']):
            results.append({
                'type': 'Book',
                'title': book.get('title', 'N/A'),
                'author': book.get('author', 'N/A'),
                'category': book.get('category', 'N/A'),
                'detail': f"by {book.get('author', 'Unknown')} - {book.get('category', 'General')}"
            })
    return results

def search_programs(query):
    """Search programs by name, department, or description."""
    results = []
    for program in programs:
        if matches_query(query, [
            program.get('name', ''),
            program.get('department', ''),
            program.get('description', ''),
            program.get('incharge', ''),
        ], aliases=['program', 'programs', 'department']):
            results.append({
                'type': 'Program',
                'title': program.get('name', 'N/A'),
                'department': program.get('department', 'N/A'),
                'detail': f"Department: {program.get('department', 'N/A')}"
            })
    return results

def search_notices(query):
    """Search notices by title, content, department, or notice keyword."""
    results = []
    for notice in notices:
        if matches_query(query, [
            notice.get('title', ''),
            notice.get('content', ''),
            notice.get('department', ''),
            notice.get('created_date', ''),
        ], aliases=['notice', 'notices']):
            results.append({
                'type': 'Notice',
                'title': notice.get('title', 'N/A'),
                'content': notice.get('content', 'N/A')[:100] + '...',
                'detail': f"Posted on {notice.get('created_date', 'N/A')}"
            })
    return results

def search_syllabus(query):
    """Search syllabus by department, semester, file, or syllabus keyword."""
    results = []
    for item in syllabus_items:
        if matches_query(query, [
            item.get('subject', ''),
            item.get('content', ''),
            item.get('department', ''),
            item.get('semester', ''),
            item.get('file', ''),
        ], aliases=['syllabus', 'semester']):
            results.append({
                'type': 'Syllabus',
                'title': item.get('subject') or f"{item.get('department', 'N/A')} Semester {item.get('semester', 'N/A')}",
                'department': item.get('department', 'N/A'),
                'detail': f"Department: {item.get('department', 'N/A')} - Semester {item.get('semester', 'N/A')}"
            })
    return results

def search_class_notes(query):
    """Search class notes by subject, topic, or content."""
    results = []
    for note in class_notes:
        if matches_query(query, [
            note.get('subject', ''),
            note.get('topic', ''),
            note.get('content', ''),
            note.get('department', ''),
        ], aliases=['class', 'notes', 'class notes']):
            results.append({
                'type': 'Class Notes',
                'title': note.get('topic', 'N/A'),
                'subject': note.get('subject', 'N/A'),
                'detail': f"Subject: {note.get('subject', 'N/A')} - Posted on {note.get('date', 'N/A')}"
            })
    return results

def search_academic_tasks(query):
    """Search academic tasks by title, description, or subject."""
    results = []
    for task in academic_tasks:
        if matches_query(query, [
            task.get('title', ''),
            task.get('description', ''),
            task.get('subject', ''),
            task.get('department', ''),
        ], aliases=['assignment', 'assignments', 'quiz', 'task', 'tasks']):
            results.append({
                'type': 'Academic Task',
                'title': task.get('title', 'N/A'),
                'subject': task.get('subject', 'N/A'),
                'detail': f"Due: {task.get('due_date', 'N/A')} - Subject: {task.get('subject', 'N/A')}"
            })
    return results

def search_all_data(query):
    """Search all college data"""
    if not query or len(query) < 2:
        return {'results': [], 'message': 'Please enter at least 2 characters to search'}
    
    normalized_query = query.strip().lower()
    if normalized_query in {'notice', 'notices'}:
        all_results = search_notices(query)
    elif normalized_query in {'syllabus', 'syllabi'}:
        all_results = search_syllabus(query)
    elif normalized_query in {'book', 'books'}:
        all_results = search_books(query)
    elif normalized_query in {'program', 'programs', 'department', 'departments'}:
        all_results = search_programs(query)
    elif normalized_query in {'assignment', 'assignments', 'quiz', 'task', 'tasks'}:
        all_results = search_academic_tasks(query)
    else:
        all_results = []
        all_results.extend(search_books(query))
        all_results.extend(search_programs(query))
        all_results.extend(search_notices(query))
        all_results.extend(search_syllabus(query))
        all_results.extend(search_class_notes(query))
        all_results.extend(search_academic_tasks(query))
    
    if all_results:
        message = f"Found {len(all_results)} result(s) for '{query}'"
    else:
        message = f"No results found for '{query}'. Try searching for keywords like: python, calculus, notice, syllabus, or assignment"
    
    return {
        'results': all_results,
        'message': message,
        'query': query
    }

@app.route('/')
def home():
    # Public home page - shows dashboard without requiring login
    if session.get('username'):
        # If already logged in, redirect to dashboard
        return redirect(url_for('dashboard'))
    
    department_names = ', '.join([p.get('department', '') for p in programs if p.get('department')])

    # Show public dashboard with real library counts
    return render_template('dashboard.html',
                         title='DEC Smart Scholar Hub',
                         subtitle='Library Management System',
                         students=len(students),
                         programs=len(programs),
                         books=len(books),
                         issued_books=0,
                         locations=len(locations),
                         cards=len(library_cards),
                         transactions=0,
                         department_names=department_names,
                         recent_notices=notices[:2],
                         notices_count=len(notices),
                         role='guest')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Check if user is pending approval
        pending_user = next((p for p in pending_registrations if p['username'] == username), None)
        if pending_user:
            error = '⏳ Your account is pending admin approval. Please check back later.'
        else:
            user = users.get(username)
            if user and user['password'] == password:
                session['username'] = username
                session['role'] = user['role']
                return redirect(url_for('dashboard'))
            error = 'Invalid Username or Password'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        name = request.form.get('name', '').strip()
        registration_no = request.form.get('registration_no', '').strip()
        department = request.form.get('department', '').strip()
        email = request.form.get('email', '').strip()
        
        if not all([username, password, name, registration_no, department, email]):
            error = 'All fields are required.'
        elif username in users or any(p['username'] == username for p in pending_registrations):
            error = 'Username already exists.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        else:
            # Save to pending registrations
            pending_registrations.append({
                'username': username,
                'password': password,
                'name': name,
                'registration_no': registration_no,
                'department': department,
                'email': email,
                'registered_at': __import__('datetime').datetime.now().isoformat()
            })
            save_pending_registrations()
            flash('Registration successful! Your account is pending admin approval. Please check back later.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    role = session.get('role')
    if role == 'user':
        return render_template(
            'dashboard.html',
            title='User Dashboard',
            subtitle='Welcome to your e-library',
            role='user',
            books=len(books),
            issued=len([i for i in issued_books if i['student'] == session.get('username')]),
            issued_books=len([i for i in issued_books if i['student'] == session.get('username')]),
            transactions=len([t for t in transactions if t['student'] == session.get('username')]),
            students=len(students),
            programs=len(programs),
            locations=len(locations),
            department_names=', '.join([p.get('department', '') for p in programs if p.get('department')]),
            recent_notices=notices[:2],
            notices_count=len(notices),
            suggested_books=book_recommendations('', session.get('username')),
        )

    return render_template(
        'dashboard.html',
        title='Admin Dashboard',
        subtitle='Overview of e-library activity',
        role='admin',
        students=len(students),
        programs=len(programs),
        books=len(books),
        issued=len(issued_books),
        issued_books=len(issued_books),
        locations=len(locations),
        cards=len(library_cards),
        transactions=len(transactions),
        department_names=', '.join([p.get('department', '') for p in programs if p.get('department')]),
        recent_notices=notices[:2],
        notices_count=len(notices),
    )

@app.route('/students', methods=['GET', 'POST'])
@login_required
@admin_required
def student_master():
    if request.method == 'POST':
        next_id = max([s['id'] for s in students]) + 1 if students else 1
        students.append({
            'id': next_id,
            'name': request.form.get('name', '').strip(),
            'program': request.form.get('program', '').strip(),
            'registration_no': request.form.get('registration_no', '').strip(),
            'email': request.form.get('email', '').strip(),
        })
        save_students()
        flash('Student added successfully.', 'success')
        return redirect(url_for('student_master'))

    query = request.args.get('q', '').strip()
    filtered = [s for s in students if query.lower() in s['name'].lower()] if query else students
    return render_template('student_master.html', title='Student Master', subtitle='Manage student records', students=filtered, query=query)

@app.route('/programs', methods=['GET', 'POST'])
@login_required
def program_master():
    if request.method == 'POST':
        next_id = max([p['id'] for p in programs]) + 1 if programs else 1
        programs.append({
            'id': next_id,
            'name': request.form.get('name', '').strip(),
            'department': request.form.get('department', '').strip(),
            'incharge': request.form.get('incharge', '').strip(),
        })
        save_programs()
        flash('Program added successfully.', 'success')
        return redirect(url_for('program_master'))
    return render_template('program_master.html', title='Program Master', subtitle='Create and view programs', programs=programs)

@app.route('/books', methods=['GET', 'POST'])
@login_required
def book_master():
    if request.method == 'POST':
        next_id = max([b['id'] for b in books]) + 1 if books else 1
        books.append({
            'id': next_id,
            'title': request.form.get('title', '').strip(),
            'author': request.form.get('author', '').strip(),
            'isbn': request.form.get('isbn', '').strip(),
            'location': request.form.get('location', '').strip(),
            'category': request.form.get('category', '').strip() or 'General',
            'pdf': None,
        })
        save_books()
        flash('Book added successfully.', 'success')
        return redirect(url_for('book_master'))
    return render_template('book_master.html', title='Book Master', subtitle='Manage book inventory', books=books)

@app.route('/books/<int:book_id>/update-pdf', methods=['GET', 'POST'])
@login_required
@admin_required
def update_book_pdf(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        flash('Book not found.', 'warning')
        return redirect(url_for('book_master'))
    if request.method == 'POST':
        file = request.files.get('pdf_file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            book['pdf'] = os.path.join('uploads', filename).replace('\\', '/')
            save_books()
            flash('Book PDF updated successfully.', 'success')
            return redirect(url_for('book_master'))
        flash('Please upload a valid PDF file.', 'danger')
    return render_template('update_book_pdf.html', book=book)

@app.route('/syllabus', methods=['GET', 'POST'])
@login_required
def syllabus():
    if request.method == 'POST':
        if session.get('role') != 'admin':
            flash('Admin access required to add syllabus items.', 'danger')
            return redirect(url_for('syllabus'))

        department = request.form.get('department', '').strip()
        semester = request.form.get('semester', '').strip()
        file = request.files.get('file')
        if not department or not semester:
            flash('Department and semester are required.', 'danger')
            return redirect(url_for('syllabus'))
        if not file or not allowed_file(file.filename):
            flash('A valid PDF file is required for the syllabus item.', 'danger')
            return redirect(url_for('syllabus'))

        filename = secure_filename(file.filename)
        syllabus_folder = os.path.join('static', 'syllabus')
        os.makedirs(syllabus_folder, exist_ok=True)
        save_path = os.path.join(syllabus_folder, filename)
        file.save(save_path)
        file_path = os.path.join('syllabus', filename).replace('\\', '/')

        next_id = max([item['id'] for item in syllabus_items]) + 1 if syllabus_items else 1
        syllabus_items.append({
            'id': next_id,
            'department': department,
            'semester': semester,
            'file': file_path,
        })
        save_syllabus()
        flash('Syllabus item added successfully.', 'success')
        return redirect(url_for('syllabus'))

    return render_template('syllabus.html', title='Syllabus', subtitle='College syllabus resources', syllabus_items=syllabus_items)

@app.route('/syllabus/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_syllabus(item_id):
    item = next((s for s in syllabus_items if s['id'] == item_id), None)
    if not item:
        flash('Syllabus item not found.', 'warning')
        return redirect(url_for('syllabus'))
    if request.method == 'POST':
        item['department'] = request.form.get('department', '').strip()
        item['semester'] = request.form.get('semester', '').strip()
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            syllabus_folder = os.path.join('static', 'syllabus')
            os.makedirs(syllabus_folder, exist_ok=True)
            save_path = os.path.join(syllabus_folder, filename)
            file.save(save_path)
            item['file'] = os.path.join('syllabus', filename).replace('\\', '/')
        save_syllabus()
        flash('Syllabus updated successfully.', 'success')
        return redirect(url_for('syllabus'))
    return render_template('edit_syllabus.html', item=item)

@app.route('/upload-book', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_book():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        category = request.form.get('category', '').strip()
        isbn = request.form.get('isbn', '').strip()
        location = request.form.get('location', '').strip()
        file = request.files.get('pdf_file')
        pdf_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            pdf_path = os.path.join('uploads', filename).replace('\\', '/')
        elif file:
            flash('Only PDF uploads are allowed.', 'danger')
            return redirect(url_for('upload_book'))

        next_id = max([b['id'] for b in books]) + 1 if books else 1
        books.append({
            'id': next_id,
            'title': title,
            'author': author,
            'isbn': isbn,
            'location': location,
            'category': category,
            'pdf': pdf_path,
        })
        save_books()
        flash('Book uploaded successfully.', 'success')
        return redirect(url_for('upload_book'))
    return render_template('upload_book.html', title='Upload Book', subtitle='Admin book upload')

@app.route('/chatbot')
@login_required
def chatbot():
    query = request.args.get('q', '').strip()
    history = session.get('search_history', [])
    if query:
        if query not in history:
            history.insert(0, query)
        session['search_history'] = history[:10]

    search_results = search_all_data(query)
    return jsonify({
        'message': search_results['message'],
        'results': search_results['results'],
        'history': session.get('search_history', []),
    })

@app.route('/locations', methods=['GET', 'POST'])
@login_required
def manage_location():
    if request.method == 'POST':
        if session.get('role') != 'admin':
            flash('Admin access only.', 'danger')
            return redirect(url_for('manage_location'))
        next_id = max([l['id'] for l in locations]) + 1 if locations else 1
        locations.append({
            'id': next_id,
            'name': request.form.get('name', '').strip(),
            'description': request.form.get('description', '').strip(),
        })
        save_locations()
        flash('Location added successfully.', 'success')
        return redirect(url_for('manage_location'))
    is_admin = session.get('role') == 'admin'
    return render_template(
        'manage_location.html',
        title='Manage Location' if is_admin else 'Library Locations',
        subtitle='Add or update library locations' if is_admin else 'View book storage locations',
        locations=locations,
        can_edit=is_admin,
    )

@app.route('/library-cards', methods=['GET', 'POST'])
@login_required
def manage_library_card():
    if request.method == 'POST':
        next_id = max([c['id'] for c in library_cards]) + 1 if library_cards else 1
        library_cards.append({
            'id': next_id,
            'student': request.form.get('student', '').strip(),
            'card_number': request.form.get('card_number', '').strip(),
            'status': request.form.get('status', 'Active'),
        })
        save_library_cards()
        flash('Library card created.', 'success')
        return redirect(url_for('manage_library_card'))
    return render_template('manage_library_card.html', title='Manage Library Card', subtitle='Issue and track cards', cards=library_cards)

@app.route('/issue-book', methods=['GET', 'POST'])
@login_required
def issue_book():
    if request.method == 'POST':
        next_id = max([i['id'] for i in issued_books]) + 1 if issued_books else 1
        issue_record = {
            'id': next_id,
            'student': request.form.get('student', '').strip(),
            'book': request.form.get('book', '').strip(),
            'issue_date': request.form.get('issue_date', '').strip(),
            'due_date': request.form.get('due_date', '').strip(),
        }
        issued_books.append(issue_record)
        transactions.append({'id': len(transactions) + 1, 'student': issue_record['student'], 'book': issue_record['book'], 'type': 'Issue', 'date': issue_record['issue_date']})
        save_issued_books()
        save_transactions()
        flash('Book issued successfully.', 'success')
        return redirect(url_for('issue_book'))
    
    # Filter issued books based on user role
    role = session.get('role')
    if role == 'admin':
        filtered_issued_books = issued_books
    else:
        # Regular user can only see their own issued books
        username = session.get('username')
        filtered_issued_books = [i for i in issued_books if i['student'] == username]
    
    return render_template('issue_book.html', title='Issue Book', subtitle='Record book issues', students=students, books=books, issued_books=filtered_issued_books, role=role)

@app.route('/return-book', methods=['GET', 'POST'])
@login_required
def return_book():
    if request.method == 'POST':
        issue_id = int(request.form.get('issue_id', '0'))
        returned = next((item for item in issued_books if item['id'] == issue_id), None)
        if returned:
            issued_books.remove(returned)
            transactions.append({'id': len(transactions) + 1, 'student': returned['student'], 'book': returned['book'], 'type': 'Return', 'date': request.form.get('return_date', '').strip()})
            save_issued_books()
            save_transactions()
            flash('Book returned successfully.', 'success')
        else:
            flash('Issued book record not found.', 'warning')
        return redirect(url_for('return_book'))
    return render_template('return_book.html', title='Return Book', subtitle='Process returned books', issued_books=issued_books, students=students)

@app.route('/transactions')
@login_required
def transaction_report():
    return render_template('transaction_report.html', title='Transaction Report', subtitle='View issue and return history', transactions=transactions)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm = request.form.get('confirm_password', '').strip()
        username = session.get('username')
        user = users.get(username)
        if not user or user.get('password') != current:
            flash('Current password is incorrect.', 'danger')
        elif new_password != confirm:
            flash('New password and confirmation do not match.', 'danger')
        else:
            user['password'] = new_password
            save_users()
            flash('Password updated successfully.', 'success')
            return redirect(url_for('dashboard'))
    return render_template('change_password.html', title='Change Password', subtitle='Update your password')

# ===================== ADMIN MANAGEMENT ROUTES =====================
@app.route('/admin-management', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_management():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        new_role = request.form.get('role', '').strip()
        
        if username in users:
            users[username]['role'] = new_role
            save_users()
            flash(f'{username} role updated to {new_role}.', 'success')
            return redirect(url_for('admin_management'))
        else:
            flash('User not found.', 'danger')
    
    return render_template('admin_management.html', title='Admin Management', subtitle='Manage user roles and permissions', users=users)

# ===================== STUDENT REGISTRATION APPROVAL ROUTES =====================
@app.route('/approve-registrations', methods=['GET'])
@login_required
@admin_required
def approve_registrations_page():
    return render_template('approve_registrations.html', title='Approve Student Registrations', subtitle='Review pending student registrations', pending_registrations=pending_registrations)

@app.route('/approve-registration/<username>', methods=['POST'])
@login_required
@admin_required
def approve_registration(username):
    global pending_registrations
    pending_user = next((p for p in pending_registrations if p['username'] == username), None)
    
    if pending_user:
        # Create user account
        users[username] = {
            'password': pending_user['password'],
            'role': 'user'
        }
        save_users()
        
        # Create student record
        next_id = max([s['id'] for s in students]) + 1 if students else 1
        students.append({
            'id': next_id,
            'name': pending_user['name'],
            'program': pending_user['department'],
            'email': pending_user['email'],
            'registration_no': pending_user['registration_no']
        })
        save_students()
        
        # Remove from pending
        pending_registrations = [p for p in pending_registrations if p['username'] != username]
        save_pending_registrations()
        
        flash(f'✓ {username} approved! Account created and added to student records.', 'success')
    else:
        flash('Registration not found.', 'danger')
    
    return redirect(url_for('approve_registrations_page'))

@app.route('/reject-registration/<username>', methods=['POST'])
@login_required
@admin_required
def reject_registration(username):
    global pending_registrations
    pending_user = next((p for p in pending_registrations if p['username'] == username), None)
    
    if pending_user:
        # Remove from pending
        pending_registrations = [p for p in pending_registrations if p['username'] != username]
        save_pending_registrations()
        
        flash(f'✕ {username} rejected.', 'info')
    else:
        flash('Registration not found.', 'danger')
    
    return redirect(url_for('approve_registrations_page'))

# ===================== NOTICES ROUTES =====================
@app.route('/notices', methods=['GET', 'POST'])
@login_required
def notices():
    if request.method == 'POST':
        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('notices'))
        
        next_id = max([n['id'] for n in notices]) + 1 if notices else 1
        pdf_path = None
        file = request.files.get('pdf_file')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            pdf_path = os.path.join('uploads', filename).replace('\\', '/')
        elif file:
            flash('Only PDF uploads are allowed.', 'danger')
            return redirect(url_for('notices'))
        
        notice = {
            'id': next_id,
            'title': request.form.get('title', '').strip(),
            'content': request.form.get('content', '').strip(),
            'department': request.form.get('department', '').strip(),
            'created_by': session.get('username'),
            'created_date': request.form.get('created_date', '').strip(),
            'pdf': pdf_path,
        }
        notices.append(notice)
        save_notices()
        flash('Notice posted successfully.', 'success')
        return redirect(url_for('notices'))
    
    # Filter notices by department for users
    department_filter = request.args.get('department', '')
    user_role = session.get('role')
    
    if user_role == 'admin':
        filtered_notices = notices
    else:
        # Users see notices for their department (if they have a program)
        filtered_notices = notices
    
    return render_template('notices.html', title='Notices', subtitle='Department Notices', 
                         notices=filtered_notices, departments=department_options(), 
                         selected_department=department_filter, user_role=user_role)

@app.route('/notices/<int:notice_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_notice(notice_id):
    notice = next((n for n in notices if n['id'] == notice_id), None)
    if not notice:
        flash('Notice not found.', 'warning')
        return redirect(url_for('notices'))
    
    if request.method == 'POST':
        notice['title'] = request.form.get('title', '').strip()
        notice['content'] = request.form.get('content', '').strip()
        notice['department'] = request.form.get('department', '').strip()
        file = request.files.get('pdf_file')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            notice['pdf'] = os.path.join('uploads', filename).replace('\\', '/')
        elif file:
            flash('Only PDF uploads are allowed.', 'danger')
            return redirect(url_for('edit_notice', notice_id=notice_id))
        
        save_notices()
        flash('Notice updated successfully.', 'success')
        return redirect(url_for('notices'))
    
    return render_template('edit_notice.html', notice=notice, departments=department_options())

@app.route('/notices/<int:notice_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_notice(notice_id):
    global notices
    notices = [n for n in notices if n['id'] != notice_id]
    save_notices()
    flash('Notice deleted successfully.', 'success')
    return redirect(url_for('notices'))

# ===================== CLASS NOTES ROUTES =====================
@app.route('/class-notes', methods=['GET', 'POST'])
@login_required
def class_notes_view():
    if request.method == 'POST':
        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('class_notes_view'))
        
        department = request.form.get('department', '').strip()
        subject = request.form.get('subject', '').strip()
        file = request.files.get('file')
        
        if not department or not subject:
            flash('Department and subject are required.', 'danger')
            return redirect(url_for('class_notes_view'))
        
        if not file or not allowed_file(file.filename):
            flash('A valid PDF file is required.', 'danger')
            return redirect(url_for('class_notes_view'))
        
        filename = secure_filename(file.filename)
        notes_folder = os.path.join('static', 'uploads')
        os.makedirs(notes_folder, exist_ok=True)
        save_path = os.path.join(notes_folder, filename)
        file.save(save_path)
        file_path = os.path.join('uploads', filename).replace('\\', '/')
        
        next_id = max([n['id'] for n in class_notes]) + 1 if class_notes else 1
        class_notes.append({
            'id': next_id,
            'department': department,
            'subject': subject,
            'file': file_path,
            'uploaded_by': session.get('username'),
            'uploaded_date': request.form.get('uploaded_date', '').strip(),
        })
        save_class_notes()
        flash('Class notes uploaded successfully.', 'success')
        return redirect(url_for('class_notes_view'))
    
    department_filter = request.args.get('department', '')
    user_role = session.get('role')
    
    if department_filter:
        filtered_notes = filter_by_department(class_notes, department_filter)
    else:
        filtered_notes = class_notes
    
    return render_template('class_notes.html', title='Class Notes', subtitle='Educational Materials',
                         class_notes=filtered_notes, departments=department_options(),
                         selected_department=department_filter, user_role=user_role)

@app.route('/class-notes/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_class_note(note_id):
    note = next((n for n in class_notes if n['id'] == note_id), None)
    if not note:
        flash('Class note not found.', 'warning')
        return redirect(url_for('class_notes_view'))
    
    if request.method == 'POST':
        note['department'] = request.form.get('department', '').strip()
        note['subject'] = request.form.get('subject', '').strip()
        file = request.files.get('file')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            notes_folder = os.path.join('static', 'uploads')
            os.makedirs(notes_folder, exist_ok=True)
            save_path = os.path.join(notes_folder, filename)
            file.save(save_path)
            note['file'] = os.path.join('uploads', filename).replace('\\', '/')
        
        save_class_notes()
        flash('Class note updated successfully.', 'success')
        return redirect(url_for('class_notes_view'))
    
    return render_template('edit_class_note.html', note=note, departments=department_options())

@app.route('/class-notes/<int:note_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_class_note(note_id):
    global class_notes
    class_notes = [n for n in class_notes if n['id'] != note_id]
    save_class_notes()
    flash('Class note deleted successfully.', 'success')
    return redirect(url_for('class_notes_view'))

# ===================== ACADEMIC TASKS ROUTES =====================
@app.route('/academic-tasks', methods=['GET', 'POST'])
@login_required
def academic_tasks_view():
    if request.method == 'POST':
        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('academic_tasks_view'))
        
        next_id = max([t['id'] for t in academic_tasks]) + 1 if academic_tasks else 1
        task = {
            'id': next_id,
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'task_type': request.form.get('task_type', '').strip(),  # 'assignment' or 'quiz'
            'department': request.form.get('department', '').strip(),
            'due_date': request.form.get('due_date', '').strip(),
            'created_by': session.get('username'),
            'created_date': request.form.get('created_date', '').strip(),
        }
        academic_tasks.append(task)
        save_academic_tasks()
        flash('Task created successfully.', 'success')
        return redirect(url_for('academic_tasks_view'))
    
    department_filter = request.args.get('department', '')
    task_type_filter = request.args.get('type', '')
    user_role = session.get('role')
    
    filtered_tasks = academic_tasks
    if department_filter:
        filtered_tasks = filter_by_department(filtered_tasks, department_filter)
    if task_type_filter:
        filtered_tasks = [t for t in filtered_tasks if t['task_type'] == task_type_filter]
    
    return render_template('academic_tasks.html', title='Assignments & Quizzes',
                         subtitle='Course Assessments', academic_tasks=filtered_tasks,
                         departments=department_options(), selected_department=department_filter,
                         selected_type=task_type_filter, user_role=user_role)

@app.route('/academic-tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_academic_task(task_id):
    task = next((t for t in academic_tasks if t['id'] == task_id), None)
    if not task:
        flash('Task not found.', 'warning')
        return redirect(url_for('academic_tasks_view'))
    
    if request.method == 'POST':
        task['title'] = request.form.get('title', '').strip()
        task['description'] = request.form.get('description', '').strip()
        task['task_type'] = request.form.get('task_type', '').strip()
        task['department'] = request.form.get('department', '').strip()
        task['due_date'] = request.form.get('due_date', '').strip()
        save_academic_tasks()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('academic_tasks_view'))
    
    return render_template('edit_academic_task.html', task=task, departments=department_options())

@app.route('/academic-tasks/<int:task_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_academic_task(task_id):
    global academic_tasks
    academic_tasks = [t for t in academic_tasks if t['id'] != task_id]
    save_academic_tasks()
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('academic_tasks_view'))

# ===================== QUESTIONS MANAGEMENT ROUTES =====================
@app.route('/academic-tasks/<int:task_id>/questions', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_questions(task_id):
    task = next((t for t in academic_tasks if t['id'] == task_id), None)
    if not task:
        flash('Task not found.', 'warning')
        return redirect(url_for('academic_tasks_view'))
    
    if 'questions' not in task:
        task['questions'] = []
    
    if request.method == 'POST':
        question_id = max([q['id'] for q in task['questions']]) + 1 if task['questions'] else 1
        question = {
            'id': question_id,
            'question_text': request.form.get('question_text', '').strip(),
            'question_type': request.form.get('question_type', 'multiple_choice'),  # multiple_choice, short_answer, essay
            'marks': int(request.form.get('marks', '1')),
        }
        
        if question['question_type'] == 'multiple_choice':
            question['options'] = [
                request.form.get('option_1', '').strip(),
                request.form.get('option_2', '').strip(),
                request.form.get('option_3', '').strip(),
                request.form.get('option_4', '').strip(),
            ]
            question['correct_answer'] = int(request.form.get('correct_answer', '0'))
        else:
            question['options'] = []
            question['correct_answer'] = None
        
        task['questions'].append(question)
        save_academic_tasks()
        flash('Question added successfully.', 'success')
        return redirect(url_for('manage_questions', task_id=task_id))
    
    return render_template('manage_questions.html', task=task, title=f"Questions for {task['title']}")

@app.route('/academic-tasks/<int:task_id>/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_question(task_id, question_id):
    task = next((t for t in academic_tasks if t['id'] == task_id), None)
    if not task:
        flash('Task not found.', 'warning')
        return redirect(url_for('academic_tasks_view'))
    
    if 'questions' not in task:
        task['questions'] = []
    
    question = next((q for q in task['questions'] if q['id'] == question_id), None)
    if not question:
        flash('Question not found.', 'warning')
        return redirect(url_for('manage_questions', task_id=task_id))
    
    if request.method == 'POST':
        question['question_text'] = request.form.get('question_text', '').strip()
        question['question_type'] = request.form.get('question_type', 'multiple_choice')
        question['marks'] = int(request.form.get('marks', '1'))
        
        if question['question_type'] == 'multiple_choice':
            question['options'] = [
                request.form.get('option_1', '').strip(),
                request.form.get('option_2', '').strip(),
                request.form.get('option_3', '').strip(),
                request.form.get('option_4', '').strip(),
            ]
            question['correct_answer'] = int(request.form.get('correct_answer', '0'))
        else:
            question['options'] = []
            question['correct_answer'] = None
        
        save_academic_tasks()
        flash('Question updated successfully.', 'success')
        return redirect(url_for('manage_questions', task_id=task_id))
    
    return render_template('edit_question.html', task=task, question=question)

@app.route('/academic-tasks/<int:task_id>/questions/<int:question_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_question(task_id, question_id):
    task = next((t for t in academic_tasks if t['id'] == task_id), None)
    if not task:
        flash('Task not found.', 'warning')
        return redirect(url_for('academic_tasks_view'))
    
    if 'questions' in task:
        task['questions'] = [q for q in task['questions'] if q['id'] != question_id]
        save_academic_tasks()
        flash('Question deleted successfully.', 'success')
    
    return redirect(url_for('manage_questions', task_id=task_id))

load_data()

if __name__ == '__main__':
    app.run(debug=True)
