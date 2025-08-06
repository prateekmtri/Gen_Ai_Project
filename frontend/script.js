// Helper functions to show/hide the loader
const showLoader = () => {
  document.getElementById("loader").style.display = 'block';
};
const hideLoader = () => {
  document.getElementById("loader").style.display = 'none';
};

// Function to update the file name display
const updateFileName = () => {
    const fileInput = document.getElementById("fileInput");
    const fileNameSpan = document.getElementById("fileName");
    if (fileInput.files.length > 0) {
      fileNameSpan.textContent = fileInput.files[0].name;
      fileNameSpan.style.fontStyle = 'normal';
    } else {
      fileNameSpan.textContent = "No file selected";
      fileNameSpan.style.fontStyle = 'italic';
    }
};

// Original uploadFile function, now with loader
const uploadFile = async () => {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file first!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  showLoader();
  try {
    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    alert(data.message || "Uploaded successfully!");
  } catch (error) {
    alert("Upload failed: " + error.message);
  } finally {
    hideLoader();
  }
};

// Original askQuestion function, now with loader and better UI feedback
const askQuestion = async () => {
  const questionInput = document.getElementById("questionInput");
  const answerOutput = document.getElementById("answerOutput");
  const question = questionInput.value;

  if (!question.trim()) {
    alert("Please type a question!");
    return;
  }

  const formData = new FormData();
  formData.append("question", question);

  showLoader();
  answerOutput.innerHTML = '<p>Thinking...</p>';

  try {
    const response = await fetch("http://localhost:8000/search", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    const answers = data.results;

    if (answers && answers.length > 0) {
      answerOutput.innerText = answers[0].content;
    } else {
      answerOutput.innerText = "Sorry, no relevant answer was found in the document.";
    }

  } catch (error) {
    answerOutput.innerText = "Error: " + error.message;
  } finally {
    hideLoader();
  }
};

// Helper function to ask question on pressing Enter key
const handleEnter = (event) => {
    if (event.key === 'Enter') {
        askQuestion();
    }
}