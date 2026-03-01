function goToComputer() {
  window.location.href = "computer.html";
}

/* Fake AI evaluation (replace with real AI later) */
function evaluate() {
  const text = document.getElementById("promptInput").value;

  localStorage.setItem("answer", text);

  if (Math.random() > 0.5) {
    window.location.href = "guilty.html";
  } else {
    window.location.href = "innocent.html";
  }
}

/* Load answer on verdict pages */
window.onload = () => {
  const box = document.getElementById("answerBox");
  if (box) {
    box.textContent = localStorage.getItem("answer") || "No prompt";
  }
};

/* Star rating */
function rate(num) {
  alert("Rated: " + num);
}