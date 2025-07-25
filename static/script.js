document.addEventListener('DOMContentLoaded', () => {
    const quizContainer = document.getElementById('quiz-container');
    const nextBtn = document.getElementById('next-btn');
    const resultContainer = document.createElement('div');
    quizContainer.after(resultContainer);

    let score = 0;
    let questionCount = 0;
    const totalQuestions = 5;
    let questionAnswered = false;

    async function getQuestion() {
        try {
            nextBtn.disabled = true;
            const response = await fetch('/get-question');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (data.error) {
                quizContainer.innerHTML = `<p style="color: red;">${data.error}</p>`;
                return null;
            }
            return data;
        } catch (error) {
            console.error('Error fetching question:', error);
            quizContainer.innerHTML = '<p style="color: red;">Could not fetch a new question. Please try refreshing the page.</p>';
            return null;
        } finally {
            nextBtn.disabled = false;
        }
    }

    function displayQuestion(questionData) {
        resultContainer.innerHTML = '';
        questionAnswered = false;
        quizContainer.innerHTML = `
            <div class="question">
                <p>${questionData.question}</p>
                <div class="options">
                    ${questionData.options.map(option => `
                        <label>
                            <input type="radio" name="option" value="${option}">
                            ${option}
                        </label>
                    `).join('')}
                </div>
            </div>
        `;
        nextBtn.textContent = 'Submit';
    }

    async function checkAnswer(selectedOption) {
        try {
            const response = await fetch('/check-answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ selected_option: selectedOption })
            });
            return await response.json();
        } catch (error) {
            console.error('Error checking answer:', error);
            return { correct: false, correct_answer: 'Error checking answer' };
        }
    }

    nextBtn.addEventListener('click', async () => {
        if (questionAnswered) {
            // Move to the next question
            if (questionCount < totalQuestions) {
                const questionData = await getQuestion();
                if (questionData) {
                    displayQuestion(questionData);
                }
            } else {
                window.location.href = `/score?score=${score}&total=${totalQuestions}`;
            }
            return;
        }

        const selectedOptionInput = document.querySelector('input[name="option"]:checked');
        if (selectedOptionInput) {
            nextBtn.disabled = true;
            questionAnswered = true;
            questionCount++;

            const selectedOption = selectedOptionInput.value;
            const result = await checkAnswer(selectedOption);
            
            if (result.correct) {
                score++;
                resultContainer.innerHTML = '<p style="color: green;">Correct!</p>';
            } else {
                resultContainer.innerHTML = `<p style="color: red;">Incorrect. The correct answer is: ${result.correct_answer}</p>`;
            }
            
            if (questionCount < totalQuestions) {
                nextBtn.textContent = 'Next Question';
            } else {
                nextBtn.textContent = 'See Score';
            }
            
            nextBtn.disabled = false;
        } else {
            alert('Please select an answer.');
        }
    });

    // Initial question load
    (async () => {
        const questionData = await getQuestion();
        if (questionData) {
            displayQuestion(questionData);
        }
    })();
}); 