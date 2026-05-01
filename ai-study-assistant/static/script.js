let extractedText = "";

// Function for Option 1: Uploading a PDF
async function uploadPDF() {
    const fileInput = document.getElementById('pdf-upload');
    const file = fileInput.files[0];
    
    if (!file) {
        alert("Please select a PDF document first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    document.getElementById('loading').style.display = 'block';
    document.getElementById('result-box').innerHTML = "";

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            extractedText = data.text;
            document.getElementById('action-buttons').style.display = 'flex';
            document.getElementById('result-box').innerHTML = "<em>PDF processed successfully! Choose an option above.</em>";
            document.getElementById('text-input').value = ""; // Clear text box
        } else {
            alert("Error: " + data.error);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to upload the document.");
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

// Function for Option 2: Using Pasted Text
function usePastedText() {
    const textArea = document.getElementById('text-input');
    
    if (!textArea.value.trim()) {
        alert("Please paste some text into the box first!");
        return;
    }
    
    // Save the text from the box
    extractedText = textArea.value;
    
    // Show the AI action buttons
    document.getElementById('action-buttons').style.display = 'flex';
    document.getElementById('result-box').innerHTML = "<em>Text loaded! Choose an option above.</em>";
    document.getElementById('pdf-upload').value = ""; // Clear file input
}

// Function to send text to Gemini AI
async function processText(action) {
    if (!extractedText) {
        alert("No document content found. Please upload a file or paste text first.");
        return;
    }

    document.getElementById('loading').style.display = 'block';
    document.getElementById('result-box').innerHTML = "";

    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: extractedText, action: action })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('result-box').innerHTML = data.result;
        } else {
            alert("Error: " + data.error);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to generate AI response.");
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}