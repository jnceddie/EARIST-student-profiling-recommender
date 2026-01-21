// Questionnaire Form Handler
let currentSection = 1;
const totalSections = 5;

$(document).ready(function() {
    console.log('Questionnaire script loaded successfully');
    
    // Initialize
    updateProgress();
    updateButtons();
    
    // Career goal conditional display
    $('input[name="career_goal_specified"]').change(function() {
        if ($(this).val() === 'true') {
            $('#careerDescriptionDiv').slideDown();
        } else {
            $('#careerDescriptionDiv').slideUp();
            $('textarea[name="career_goal_description"]').val('');
        }
    });

    // Subject checkbox validation (max 3)
    $('.subject-checkbox').change(function() {
        const checked = $('.subject-checkbox:checked').length;
        if (checked > 3) {
            $(this).prop('checked', false);
            showInlineError($(this).closest('.form-group, .form-check-group'), 'Please select only up to 3 favorite subjects.');
        } else {
            clearInlineError($(this).closest('.form-group, .form-check-group'));
        }
    });
    
    // Next button
    $('#nextBtn').click(function() {
        console.log('Next button clicked - Current section:', currentSection);
        if (validateSection(currentSection)) {
            $(`#section${currentSection}`).removeClass('active');
            currentSection++;
            console.log('Moving to section:', currentSection);
            $(`#section${currentSection}`).addClass('active');
            updateProgress();
            updateButtons();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            console.log('Validation failed for section:', currentSection);
        }
    });
    
    // Previous button
    $('#prevBtn').click(function() {
        console.log('Previous button clicked - Current section:', currentSection);
        
        // Hide current section
        $(`#section${currentSection}`).removeClass('active');
        
        // Move to previous section
        currentSection--;
        console.log('Moving back to section:', currentSection);
        
        // Show previous section
        $(`#section${currentSection}`).addClass('active');
        
        // Update UI
        updateProgress();
        updateButtons();
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    // Form submission
    $('#questionnaireForm').submit(function(e) {
        e.preventDefault();
        clearAllInlineErrors();
        console.log('Form submitted');
        if (!validateSection(currentSection, true)) {
            return false;
        }
        // Prepare data matching backend expectations
        const formData = {
            name: $('input[name="student_name"]').val().trim(),
            grade_level: $('select[name="grade_level"]').val(),
            strand: $('select[name="strand"]').val(),
            email: $('input[name="email"]').val().trim() || null,
            favorite_subjects: [],
            skills: {
                analytical: parseInt($('input[name="skill_analytical"]:checked').val()) || 0,
                technical: parseInt($('input[name="skill_technical"]:checked').val()) || 0,
                communication: parseInt($('input[name="skill_communication"]:checked').val()) || 0,
                creativity: parseInt($('input[name="skill_creativity"]:checked').val()) || 0,
                numerical: parseInt($('input[name="skill_numerical"]:checked').val()) || 0,
                leadership: parseInt($('input[name="skill_leadership"]:checked').val()) || 0,
                attention_to_detail: parseInt($('input[name="skill_attention_to_detail"]:checked').val()) || 0,
                research: parseInt($('input[name="skill_research"]:checked').val()) || 0
            },
            interests: [],
            learning_style: $('select[name="learning_style"]').val(),
            career_goals: ''
        };
        // Collect favorite subjects
        $('input[name="favorite_subjects"]:checked').each(function() {
            formData.favorite_subjects.push($(this).val());
        });
        // Collect interests
        $('input[name="interests"]:checked').each(function() {
            formData.interests.push($(this).val());
        });
        // Add career goals if specified
        if ($('input[name="career_goal_specified"]:checked').val() === 'true') {
            formData.career_goals = $('textarea[name="career_goal_description"]').val().trim();
        }
        console.log('Submitting form data:', formData);
        // Show loading modal and disable submit
        $('#loadingModal').modal('show');
        $('#submitBtn').prop('disabled', true);
        // Submit to server
        $.ajax({
            url: '/api/submit-response',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                console.log('Server response:', response);
                $('#loadingModal').modal('hide');
                $('#submitBtn').prop('disabled', false);
                if (response.success) {
                    window.location.href = '/results';
                } else {
                    showGlobalError('Error generating recommendations. Please try again.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Submission error:', error, xhr);
                $('#loadingModal').modal('hide');
                $('#submitBtn').prop('disabled', false);
                let errorMsg = 'Error submitting questionnaire. Please try again.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                }
                showGlobalError(errorMsg);
            }
        });
    });
});

function showSection(sectionNum) {
    $('.questionnaire-section').removeClass('active');
    $(`#section${sectionNum}`).addClass('active');
}

function updateProgress() {
    $('.progress-step').each(function() {
        const stepNum = parseInt($(this).data('section'));
        
        if (stepNum < currentSection) {
            $(this).removeClass('active').addClass('completed');
        } else if (stepNum === currentSection) {
            $(this).addClass('active').removeClass('completed');
        } else {
            $(this).removeClass('active completed');
        }
    });
}

function updateButtons() {
    // Previous button
    if (currentSection === 1) {
        $('#prevBtn').prop('disabled', true);
    } else {
        $('#prevBtn').prop('disabled', false);
    }
    
    // Next/Submit button
    if (currentSection === totalSections) {
        $('#nextBtn').addClass('d-none');
        $('#submitBtn').removeClass('d-none');
    } else {
        $('#nextBtn').removeClass('d-none');
        $('#submitBtn').addClass('d-none');
    }
}

function validateSection(sectionNum, showInline = false) {
    let isValid = true;
    const section = $(`#section${sectionNum}`);
    // Remove previous validation errors
    section.find('.is-invalid').removeClass('is-invalid');
    section.find('.inline-error').remove();
    section.find('.section-error-summary').remove();

    let errorMessages = [];

    // Section 1: Personal Information
    if (sectionNum === 1) {
        const name = $('input[name="student_name"]').val().trim();
        if (!name) {
            $('input[name="student_name"]').addClass('is-invalid');
            if (showInline) showInlineError($('input[name="student_name"]'), 'Name is required.');
            errorMessages.push('Full Name is required.');
            isValid = false;
        }
        const email = $('input[name="email"]').val().trim();
        if (email && !validateEmail(email)) {
            $('input[name="email"]').addClass('is-invalid');
            if (showInline) showInlineError($('input[name="email"]'), 'Invalid email address.');
            errorMessages.push('Email address is invalid.');
            isValid = false;
        }
        if (!$('select[name="grade_level"]').val()) {
            $('select[name="grade_level"]').addClass('is-invalid');
            if (showInline) showInlineError($('select[name="grade_level"]'), 'Grade level is required.');
            errorMessages.push('Grade Level is required.');
            isValid = false;
        }
        if (!$('select[name="strand"]').val()) {
            $('select[name="strand"]').addClass('is-invalid');
            if (showInline) showInlineError($('select[name="strand"]'), 'Strand is required.');
            errorMessages.push('Strand is required.');
            isValid = false;
        }
    }
    // Section 2: Favorite Subjects
    if (sectionNum === 2) {
        const checkedSubjects = $('input[name="favorite_subjects"]:checked').length;
        if (checkedSubjects === 0) {
            if (showInline) showInlineError($('#section2 .subject-checkbox').last().closest('.form-group, .form-check-group'), 'Please select at least one favorite subject.');
            errorMessages.push('Please select at least one favorite subject.');
            isValid = false;
        } else if (checkedSubjects > 3) {
            if (showInline) showInlineError($('#section2 .subject-checkbox').last().closest('.form-group, .form-check-group'), 'Please select only up to 3 favorite subjects.');
            errorMessages.push('Please select only up to 3 favorite subjects.');
            isValid = false;
        }
    }
    // Section 3: Skills Rating
    if (sectionNum === 3) {
        const skillNames = [
            'analytical', 'technical', 'communication', 'creativity',
            'numerical', 'leadership', 'attention_to_detail', 'research'
        ];
        for (let skill of skillNames) {
            if (!$(`input[name="skill_${skill}"]:checked`).length) {
                if (showInline) showInlineError($(`#section3 .skill-rating input[name="skill_${skill}"]`).parent(), `Please rate your ${skill.replace('_', ' ')} skill level.`);
                errorMessages.push(`Please rate your ${skill.replace('_', ' ')} skill level.`);
                isValid = false;
            }
        }
    }
    // Section 4: Interests
    if (sectionNum === 4) {
        const checkedInterests = $('input[name="interests"]:checked').length;
        if (checkedInterests === 0) {
            if (showInline) showInlineError($('#section4 .interests-group'), 'Please select at least one interest area.');
            errorMessages.push('Please select at least one interest area.');
            isValid = false;
        }
    }
    // Section 5: Learning Style & Career Goals
    if (sectionNum === 5) {
        if (!$('select[name="learning_style"]').val()) {
            $('select[name="learning_style"]').addClass('is-invalid');
            if (showInline) showInlineError($('select[name="learning_style"]'), 'Please select your learning style preference.');
            errorMessages.push('Learning style preference is required.');
            isValid = false;
        }
    }
    if (!isValid && errorMessages.length > 0) {
        // Add error summary at the top of the section
        section.prepend(`<div class="section-error-summary alert alert-danger" style="font-weight:bold; font-size:1.1em;">${errorMessages.join('<br>')}</div>`);
        // Scroll to error summary
        const summary = section.find('.section-error-summary').first();
        if (summary.length) {
            $('html, body').animate({
                scrollTop: summary.offset().top - 120
            }, 300);
        } else {
            // Fallback: scroll to first invalid field
            const firstInvalid = section.find('.is-invalid').first();
            if (firstInvalid.length) {
                $('html, body').animate({
                    scrollTop: firstInvalid.offset().top - 100
                }, 300);
            }
        }
    }
    return isValid;
}

function showInlineError(element, message) {
    // Accepts a jQuery element
    if (!element || !element.length) return;
    if (element.hasClass('form-group') || element.hasClass('form-check-group')) {
        element.append(`<div class="inline-error text-danger small mt-1">${message}</div>`);
    } else {
        element.after(`<div class="inline-error text-danger small mt-1">${message}</div>`);
    }
}

function clearInlineError(element) {
    if (!element || !element.length) return;
    element.find('.inline-error').remove();
    element.removeClass('is-invalid');
}

function clearAllInlineErrors() {
    $('.inline-error').remove();
    $('.is-invalid').removeClass('is-invalid');
}

function showGlobalError(message) {
    // Show a global error message (could be a modal, toast, or alert)
    // For now, use alert, but can be replaced with a custom modal/toast
    alert(message);
}

function validateEmail(email) {
    // Simple email regex
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}