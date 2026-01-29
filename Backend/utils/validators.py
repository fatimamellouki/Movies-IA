# backend/utils/validators.py
import re
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email: str) -> tuple:
    """Valider une adresse email"""
    try:
        # Valider et normaliser l'email
        valid = validate_email(email)
        return True, valid.email
    except EmailNotValidError as e:
        return False, str(e)

def validate_password_strength(password: str) -> tuple:
    """Valider la force d'un mot de passe"""
    errors = []
    
    if len(password) < 8:
        errors.append("Le mot de passe doit contenir au moins 8 caractères")
    
    if not re.search(r"[A-Z]", password):
        errors.append("Le mot de passe doit contenir au moins une majuscule")
    
    if not re.search(r"[a-z]", password):
        errors.append("Le mot de passe doit contenir au moins une minuscule")
    
    if not re.search(r"\d", password):
        errors.append("Le mot de passe doit contenir au moins un chiffre")
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Le mot de passe doit contenir au moins un caractère spécial")
    
    if errors:
        return False, errors
    return True, "Mot de passe valide"

def validate_user_data(user_data: dict) -> tuple:
    """Valider les données utilisateur"""
    errors = {}
    
    # Valider l'email
    if 'email' in user_data:
        is_valid, message = validate_email_address(user_data['email'])
        if not is_valid:
            errors['email'] = message
    
    # Valider le mot de passe
    if 'password' in user_data:
        is_valid, message = validate_password_strength(user_data['password'])
        if not is_valid:
            errors['password'] = message
    
    # Valider l'âge
    if 'age' in user_data:
        try:
            age = int(user_data['age'])
            if age < 1 or age > 120:
                errors['age'] = "L'âge doit être entre 1 et 120"
        except ValueError:
            errors['age'] = "L'âge doit être un nombre valide"
    
    # Valider le genre
    if 'gender' in user_data:
        gender = user_data['gender'].upper()
        if gender not in ['M', 'F', 'O']:
            errors['gender'] = "Le genre doit être M, F ou O"
    
    # Valider l'occupation
    valid_occupations = [
        'administrator', 'artist', 'doctor', 'educator', 'engineer',
        'entertainment', 'executive', 'healthcare', 'homemaker', 'lawyer',
        'librarian', 'marketing', 'none', 'other', 'programmer',
        'retired', 'salesman', 'scientist', 'student', 'technician', 'writer'
    ]
    
    if 'occupation' in user_data:
        if user_data['occupation'] not in valid_occupations:
            errors['occupation'] = f"Occupation doit être l'une des suivantes: {', '.join(valid_occupations)}"
    
    if errors:
        return False, errors
    return True, "Données utilisateur valides"

def validate_rating(rating: float) -> bool:
    """Valider une note de film"""
    try:
        rating_float = float(rating)
        return 1.0 <= rating_float <= 5.0
    except ValueError:
        return False

def validate_date(date_string: str, format: str = "%Y-%m-%d") -> bool:
    """Valider une date"""
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False

def sanitize_input(input_string: str) -> str:
    """Nettoyer une chaîne de caractères pour éviter les injections"""
    if not input_string:
        return ""
    
    # Supprimer les caractères dangereux
    dangerous_chars = ['<', '>', ';', '"', "'", '\\', '/', '|']
    for char in dangerous_chars:
        input_string = input_string.replace(char, '')
    
    # Limiter la longueur
    if len(input_string) > 1000:
        input_string = input_string[:1000]
    
    return input_string.strip()