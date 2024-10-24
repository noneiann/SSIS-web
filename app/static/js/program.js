document
	.getElementById("submitAddProgram")
	.addEventListener("click", function () {
		const programCode = document.getElementById("courseCode").value;
		const programName = document.getElementById("name").value;
		const college = document.getElementById("college").value;
		const errorDiv = document.querySelector(".error");
		const csrfToken = document.querySelector(
			'#addProgramForm input[name="csrf_token"]'
		).value;

		errorDiv.classList.add("d-none");
		errorDiv.innerText = "";

		if (programCode === "") {
			errorDiv.innerText = "Program Code is required.";
			errorDiv.classList.remove("d-none");
			return;
		}

		if (programName === "") {
			errorDiv.innerText = "Program Name is required.";
			errorDiv.classList.remove("d-none");
			return;
		}

		fetch("/add_program", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrfToken,
			},
			body: JSON.stringify({
				courseCode: programCode,
				name: programName,
				college: college,
			}),
		})
			.then((response) => {
				if (!response.ok) {
					return response.json().then((errorData) => {
						throw errorData;
					});
				}
				return response.json();
			})
			.then((result) => {
				alert(result.message);
				location.reload();
			})
			.catch((error) => {
				errorDiv.innerText =
					error.message || "An error occurred. Please try again.";
				errorDiv.classList.remove("d-none");
				console.error("Error:", error);
			});
	});
