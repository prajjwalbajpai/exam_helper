document.getElementById("qa-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = document.getElementById("qa-form");
  const formData = new FormData(form);

  const output = document.getElementById("output");
  const answerList = document.getElementById("answer-list");
  const summaryText = document.getElementById("summary-text");

  output.style.display = "block";
  answerList.innerHTML = "Loading answers...";
  summaryText.innerText = "Loading Important Topics...";

  try {
    const response = await fetch("/process", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    answerList.innerHTML = "";
    summaryText.innerText = "";

    if (data.error) {
      answerList.innerHTML = `<li style="color:red;">Error: ${data.error}</li>`;
    } else {
      data.answers.forEach(ans => {
        const li = document.createElement("li");
        li.innerHTML = marked.parse(ans);  
        answerList.appendChild(li);
        });

      summaryText.innerHTML = marked.parse(data.summary || "No summary available.");

    }

  } catch (err) {
    answerList.innerHTML = `<li style="color:red;">Request failed. Try again later.</li>`;
    summaryText.innerText = "";
  }
});
