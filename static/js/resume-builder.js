// resume-builder.js
// This file contains JavaScript functionality for the resume builder

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality when the DOM is loaded
    
    // Function to handle form submissions with AJAX
    function handleFormSubmission(formId, successCallback) {
        const form = document.getElementById(formId);
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formData = new FormData(form);
                
                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        successCallback(data);
                    } else {
                        // Handle validation errors
                        if (data.errors) {
                            alert('Validation errors:\n' + data.errors.join('\n'));
                        } else {
                            console.error('Error:', data);
                            alert('An error occurred. Please try again.');
                        }
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
            });
        }
    }
    
    // Function to handle delete buttons
    function handleDeleteButtons(className, deleteUrl) {
        document.querySelectorAll(className).forEach(button => {
            button.addEventListener('click', function() {
                const itemId = this.dataset.id;
                if (confirm('Are you sure you want to delete this item?')) {
                    fetch(deleteUrl.replace('0', itemId), {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Remove the item from the DOM
                            // Find the closest parent container and remove it
                            if (className.includes('experience')) {
                                this.closest('.experience-item').remove();
                            } else if (className.includes('education')) {
                                this.closest('.education-item').remove();
                            } else if (className.includes('skill')) {
                                this.closest('.skill-item').remove();
                            } else if (className.includes('project')) {
                                this.closest('.project-item').remove();
                            } else {
                                // Fallback: try to remove the closest container
                                this.closest('[class*="-item"]').remove();
                            }
                            alert('Item deleted successfully!');
                        } else {
                            alert('Error deleting item.');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Error deleting item.');
                    });
                }
            });
        });
    }
    
    // Initialize form handlers
    handleFormSubmission('personal-info-form', function(data) {
        alert('Personal information saved successfully!');
    });
    
    // Initialize delete button handlers
    handleDeleteButtons('.delete-experience-btn', '/resumes/delete-experience/0/');
    handleDeleteButtons('.delete-education-btn', '/resumes/delete-education/0/');
    handleDeleteButtons('.delete-skill-btn', '/resumes/delete-skill/0/');
    handleDeleteButtons('.delete-project-btn', '/resumes/delete-project/0/');
    
    // Print resume functionality
    const printButton = document.getElementById('print-resume-btn');
    if (printButton) {
        printButton.addEventListener('click', function() {
            window.print();
        });
    }
    
    // AI suggestions functionality
    const aiAnalyzeButton = document.getElementById('ai-analyze-btn');
    if (aiAnalyzeButton) {
        aiAnalyzeButton.addEventListener('click', function() {
            // Get the resume ID from the URL
            const urlParts = window.location.pathname.split('/');
            const resumeId = urlParts[urlParts.length - 2];
            
            // Show loading indicator
            const suggestionsContainer = document.getElementById('ai-suggestions-content');
            suggestionsContainer.innerHTML = '<p>Analyzing your resume... This may take a moment.</p>';
            
            // Send request to AI analysis endpoint
            fetch(`/resumes/${resumeId}/ai-analyze/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    section: 'full'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    suggestionsContainer.innerHTML = `<div class="prose prose-sm"><h4 class="text-lg font-semibold text-gray-800 mb-2">AI Suggestions:</h4><div class="bg-blue-50 p-4 rounded-md">${data.suggestions.replace(/\n/g, '<br>')}</div></div>`;
                } else {
                    suggestionsContainer.innerHTML = `<p class="text-red-600">Error: ${data.error || 'Failed to get AI suggestions'}</p>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                suggestionsContainer.innerHTML = '<p class="text-red-600">Error: Failed to connect to AI service</p>';
            });
        });
    }
    
    // AI generate summary functionality
    const aiGenerateSummaryButton = document.getElementById('ai-generate-summary-btn');
    if (aiGenerateSummaryButton) {
        aiGenerateSummaryButton.addEventListener('click', function() {
            // Get the resume ID from the URL
            const urlParts = window.location.pathname.split('/');
            const resumeId = urlParts[urlParts.length - 2];
            
            // Show loading indicator
            const summaryContainer = document.getElementById('summary-suggestions');
            if (summaryContainer) {
                summaryContainer.innerHTML = '<p>Generating professional summary...</p>';
                
                // Send request to AI summary generation endpoint
                fetch(`/resumes/${resumeId}/ai-generate-summary/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        summaryContainer.innerHTML = `<div class="bg-green-50 p-4 rounded-md">${data.summary}</div><button id="use-summary-btn" class="mt-2 inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Use This Summary</button>`;
                        
                        // Add event listener to the "Use This Summary" button
                        document.getElementById('use-summary-btn').addEventListener('click', function() {
                            const summaryTextarea = document.getElementById('summary-textarea');
                            if (summaryTextarea) {
                                summaryTextarea.value = data.summary;
                            }
                        });
                    } else {
                        summaryContainer.innerHTML = `<p class="text-red-600">Error: ${data.error || 'Failed to generate summary'}</p>`;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    summaryContainer.innerHTML = '<p class="text-red-600">Error: Failed to connect to AI service</p>';
                });
            }
        });
    }
    
    // Save summary functionality
    const saveSummaryButton = document.getElementById('save-summary-btn');
    if (saveSummaryButton) {
        saveSummaryButton.addEventListener('click', function() {
            const summaryText = document.getElementById('summary-textarea').value;
            // Get the resume ID from the URL
            const urlParts = window.location.pathname.split('/');
            const resumeId = urlParts[urlParts.length - 2];
            
            // Send request to save summary endpoint
            fetch(`/resumes/${resumeId}/save-summary/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    summary: summaryText
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Summary saved successfully!');
                } else {
                    // Handle validation errors
                    if (data.errors) {
                        alert('Validation errors:\n' + data.errors.join('\n'));
                    } else {
                        alert('Error saving summary.');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving summary.');
            });
        });
    }
    
    // Layout customization functionality
    const customizeLayoutBtn = document.getElementById('customize-layout-btn');
    const layoutModal = document.getElementById('layout-customization-modal');
    const saveLayoutBtn = document.getElementById('save-layout-btn');
    const cancelLayoutBtn = document.getElementById('cancel-layout-btn');
    
    // Show modal when customize layout button is clicked
    if (customizeLayoutBtn) {
        customizeLayoutBtn.addEventListener('click', function() {
            if (layoutModal) layoutModal.classList.remove('hidden');
        });
    }
    
    // Hide modal when cancel button is clicked
    if (cancelLayoutBtn) {
        cancelLayoutBtn.addEventListener('click', function() {
            if (layoutModal) layoutModal.classList.add('hidden');
        });
    }
    
    // Save layout when save button is clicked
    if (saveLayoutBtn) {
        saveLayoutBtn.addEventListener('click', function() {
            const layoutStyle = document.getElementById('layout-style') ? document.getElementById('layout-style').value : '';
            
            // Get the resume ID from the URL
            const urlParts = window.location.pathname.split('/');
            const resumeId = urlParts[urlParts.length - 2];
            
            // Send AJAX request to save layout
            fetch(`/resumes/${resumeId}/customize-layout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new URLSearchParams({
                    'layout': layoutStyle
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Close modal
                    if (layoutModal) layoutModal.classList.add('hidden');
                    
                    // Show success message
                    alert('Layout saved successfully!');
                } else {
                    alert('Error saving layout.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving layout.');
            });
        });
    }
    
    // Typography customization functionality
    const customizeTypographyBtn = document.getElementById('customize-typography-btn');
    const typographyModal = document.getElementById('typography-customization-modal');
    const saveTypographyBtn = document.getElementById('save-typography-btn');
    const cancelTypographyBtn = document.getElementById('cancel-typography-btn');
    
    // Show modal when customize typography button is clicked
    if (customizeTypographyBtn) {
        customizeTypographyBtn.addEventListener('click', function() {
            if (typographyModal) typographyModal.classList.remove('hidden');
        });
    }
    
    // Hide modal when cancel button is clicked
    if (cancelTypographyBtn) {
        cancelTypographyBtn.addEventListener('click', function() {
            if (typographyModal) typographyModal.classList.add('hidden');
        });
    }
    
    // Save typography when save button is clicked
    if (saveTypographyBtn) {
        saveTypographyBtn.addEventListener('click', function() {
            const headingFont = document.getElementById('heading-font') ? document.getElementById('heading-font').value : '';
            const bodyFont = document.getElementById('body-font') ? document.getElementById('body-font').value : '';
            const headingFontSize = document.getElementById('heading-font-size') ? document.getElementById('heading-font-size').value : '';
            const bodyFontSize = document.getElementById('body-font-size') ? document.getElementById('body-font-size').value : '';
            
            // Get the resume ID from the URL
            const urlParts = window.location.pathname.split('/');
            const resumeId = urlParts[urlParts.length - 2];
            
            // Send AJAX request to save typography
            fetch(`/resumes/${resumeId}/customize-typography/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new URLSearchParams({
                    'heading_font': headingFont,
                    'body_font': bodyFont,
                    'heading_font_size': headingFontSize,
                    'body_font_size': bodyFontSize
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Close modal
                    if (typographyModal) typographyModal.classList.add('hidden');
                    
                    // Show success message
                    alert('Typography saved successfully!');
                } else {
                    alert('Error saving typography.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving typography.');
            });
        });
    }
    
    // Color customization functionality
    const customizeColorsBtn = document.getElementById('customize-colors-btn');
    const colorModal = document.getElementById('color-customization-modal');
    const saveColorsBtn = document.getElementById('save-colors-btn');
    const cancelColorsBtn = document.getElementById('cancel-colors-btn');
    
    // Show modal when customize colors button is clicked
    if (customizeColorsBtn) {
        customizeColorsBtn.addEventListener('click', function() {
            if (colorModal) colorModal.classList.remove('hidden');
        });
    }
    
    // Hide modal when cancel button is clicked
    if (cancelColorsBtn) {
        cancelColorsBtn.addEventListener('click', function() {
            if (colorModal) colorModal.classList.add('hidden');
        });
    }
    
    // Save colors when save button is clicked
    if (saveColorsBtn) {
        saveColorsBtn.addEventListener('click', function() {
            const primaryColor = document.getElementById('primary-color') ? document.getElementById('primary-color').value : '';
            const secondaryColor = document.getElementById('secondary-color') ? document.getElementById('secondary-color').value : '';
            const accentColor = document.getElementById('accent-color') ? document.getElementById('accent-color').value : '';
            const textColor = document.getElementById('text-color') ? document.getElementById('text-color').value : '';
            const backgroundColor = document.getElementById('background-color') ? document.getElementById('background-color').value : '';
            
            // Get the resume ID from the URL
            const urlParts = window.location.pathname.split('/');
            const resumeId = urlParts[urlParts.length - 2];
            
            // Send AJAX request to save colors
            fetch(`/resumes/${resumeId}/customize-colors/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new URLSearchParams({
                    'primary_color': primaryColor,
                    'secondary_color': secondaryColor,
                    'accent_color': accentColor,
                    'text_color': textColor,
                    'background_color': backgroundColor
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Close modal
                    if (colorModal) colorModal.classList.add('hidden');
                    
                    // Show success message
                    alert('Colors saved successfully!');
                } else {
                    alert('Error saving colors.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving colors.');
            });
        });
    }
});