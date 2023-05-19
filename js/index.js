// SORT

function sortTable() {
  const table = document.getElementById("table");
  const tbody = table.querySelector("tbody");
  const sortSelect = document.getElementById("sort-select");
  const sortValue = sortSelect.value;

  // Sort table based on selected option
  switch (sortValue) {
    case "title-asc":
      sortRowsByColumn(tbody, 0, "asc");
      break;
    case "title-desc":
      sortRowsByColumn(tbody, 0, "desc");
      break;
    case "price-asc":
      sortRowsByColumn(tbody, 1, "asc");
      break;
    case "price-desc":
      sortRowsByColumn(tbody, 1, "desc");
      break;
    default:
      break;
  }
}

function sortRowsByColumn(tbody, columnIndex, sortOrder) {
  const rows = Array.from(tbody.querySelectorAll("tr"));
  const sortMultiplier = sortOrder === "asc" ? 1 : -1;
  rows.sort((a, b) => {
    let aValue = a.cells[columnIndex].textContent.trim().toLowerCase();
    let bValue = b.cells[columnIndex].textContent.trim().toLowerCase();

    if (columnIndex === 1) {
      aValue = parseInt(aValue.replace(/\./g, ""));
      bValue = parseInt(bValue.replace(/\./g, ""));
    }

    if (aValue < bValue) {
      return -1 * sortMultiplier;
    } else if (aValue > bValue) {
      return 1 * sortMultiplier;
    } else {
      return 0;
    }
  });
  rows.forEach((row) => tbody.appendChild(row));
}


const Button = document.getElementById("Button");
const Input = document.getElementById("name");
const ClearButton = document.getElementById("clear-button");
const DataOutput = document.querySelector("#data-output");


// Hide ClearButton initially
ClearButton.style.display = "none";

// Show/hide ClearButton on scroll
window.addEventListener("scroll", () => {
  if (DataOutput.getBoundingClientRect().top < window.innerHeight) {
    ClearButton.style.display = "block";
  } else {
    ClearButton.style.display = "none";
  }
});

ClearButton.addEventListener("click", () => {
  // Find the element that displays the search results and clear its contents
  const placeholder = document.querySelector("#data-output");
  placeholder.innerHTML = "";
});

ClearButton.addEventListener("click", () => {
  // Find the element that displays the search results and clear its contents
  const placeholder = document.querySelector("#data-output");
  placeholder.innerHTML = "";
});

function performSearch() {
  const inputValue = Input.value;
  const searchText = inputValue.trim().toLowerCase().split(/\s+/);

  const urls = ["./js/phongvu.json", "./js/anphat.json", "./js/gearvn.json"];
  const requests = urls.map((url) => fetch(url));

  Promise.all(requests)
    .then((responses) => Promise.all(responses.map((r) => r.json())))
    .then((products) => {
      let allProducts = [].concat(...products);
      let filteredProducts = allProducts.filter((product) => {
        const title = product.title.toLowerCase();
        return searchText.every((word) => title.includes(word));
      });

      const placeholder = document.querySelector("#data-output");
      let output = "";
      filteredProducts.forEach((product) => {
        const title = product.title.toLowerCase();
        if (!searchText.every((word) => title.includes(word))) {
          return;
        }
        const formattedPrice = product.price.toLocaleString();
        output += `
          <tr>
            <td>${product.title}</td>
            <td>${formattedPrice}</td>
            <td><a href="${product.product_url}">Go to store</a></td>
            <td><img src="${product.img_url}"></td>
            <td>${product.shop_name}</td>
          </tr>
        `;
      });
      placeholder.innerHTML = output;
    })
    .catch((error) => console.error(error));
}

Button.addEventListener("click", performSearch);

Input.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    performSearch();
  }
});
