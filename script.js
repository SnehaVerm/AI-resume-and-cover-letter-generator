// Tab Switching
    document.getElementById('resumeBtn').onclick = () => {
      document.getElementById('resumeTab').classList.add('active');
      document.getElementById('coverTab').classList.remove('active');
      document.getElementById('resumeBtn').classList.add('active');
      document.getElementById('coverBtn').classList.remove('active');
    };

    document.getElementById('coverBtn').onclick = () => {
      document.getElementById('resumeTab').classList.remove('active');
      document.getElementById('coverTab').classList.add('active');
      document.getElementById('resumeBtn').classList.remove('active');
      document.getElementById('coverBtn').classList.add('active');
    };

    // Resume Submit
    document.getElementById("generateResumeBtn").addEventListener("click", async function (e) {
      e.preventDefault();

      const form = document.getElementById('resumeForm');
      const data = Object.fromEntries(new FormData(form).entries());

      const res = await fetch("http://localhost:5000/generate-resume", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await res.json();
      document.getElementById("resumePreview").innerText = result.resume;
    });

    // Set Today's Date
    function setToday() {
      const today = new Date();
      const formatted = today.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
      document.getElementById('date').value = formatted;
    }

    // Cover Letter Submit
    document.getElementById("coverForm").addEventListener("submit", async function (e) {
      e.preventDefault();

      const form = document.getElementById('coverForm');
      const data = Object.fromEntries(new FormData(form).entries());

      const res = await fetch("http://localhost:5000/generate-cover", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await res.json();
      document.getElementById("coverPreview").innerText = result.cover_letter;
    });