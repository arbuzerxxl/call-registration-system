let isLoading = false;
let isError = false;

const apiUrl = "http://localhost:82/appeal";

const redBored = "1px solid red";
const defaultBorder = "";
const emptyField = "";

window.onload = function () {
  const form = document.querySelector("#form");
  const dialog = document.querySelector("#dialog");
  const closeDialogBtn = document.querySelector("#dialog-btn");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (isLoading) return;

    isLoading = true;

    const name = event.target.elements.name;
    const secondName = event.target.elements.secondName;
    const patronymic = event.target.elements.patronymic;
    const phone = event.target.elements.phone;
    const appeal = event.target.elements.appeal;

    const formFields = [name, secondName, patronymic, phone, appeal];

    const data = {
      last_name: secondName.value,
      first_name: name.value,
      patronymic: patronymic.value,
      phone_number: phone.value,
      appeal: appeal.value,
    };

    formFields.forEach((field) => {
      if (field.value === emptyField) {
        field.style.border = redBored;
      } else {
        field.style.border = defaultBorder;
      }
    });

    const dataValues = Object.values(data);

    if (dataValues.some((v) => v === "")) {
      isError = true;
    } else {
      isError = false;
    }

    if (isError) {
      isLoading = false;
      return;
    }

    fetch(apiUrl, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
      crossDomain: true,
    })
      .then((res) => {
        if (res.status) {
          name.value = "";
          secondName.value = "";
          patronymic.value = "";
          phone.value = "";
          appeal.value = "";
          dialog.style.display = "block";
        }
      })
      .catch((e) => {
        console.log("Error", e);
      })
      .finally(() => (isLoading = false));
    return false;
  });

  closeDialogBtn.addEventListener("click", () => {
    dialog.style.display = "none";
  });
};
