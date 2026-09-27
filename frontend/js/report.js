const reportForm = document.getElementById("reportForm");

const successMessage =
    document.getElementById("successMessage");


reportForm.addEventListener("submit", function(event) {

    event.preventDefault();

    const location =
        document.getElementById("location").value;

    const problem =
        document.getElementById("problem").value;

    const description =
        document.getElementById("description").value;

    console.log("Location:", location);
    console.log("Problem:", problem);
    console.log("Description:", description);

    successMessage.style.display = "block";

    reportForm.reset();

});