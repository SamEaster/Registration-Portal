function menuToggle() {
  const toggleMenu = document.querySelector(".menu");
  toggleMenu.classList.toggle("active");
}

const scrollbtn = document.querySelector(".scrollbtn");
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth",
      block: "start",
      inline: "nearest",
    });
  });
});

// const faqs = document.querySelectorAll(".faq");
// // const question = document.querySelectorAll(".faq .question");
// faqs.forEach((faq) => {
//   faq.addEventListener("click", () => {
//     faq.children[1].classList.toggle("active");

//     const open = faq.querySelector(".open");
//     const close = faq.querySelector(".close");

//     if (faq.children[1].classList.contains("active")) {
//       open.classList.remove("active");
//       close.classList.add("active");
//     } else {
//       open.classList.add("active");
//       close.classList.remove("active");
//     }
//   });
// });

var temp;

// function selectModule(moduleNumber) {

//   var selectedCard = document.querySelector('.cards' + moduleNumber);
//   selectedCard.style.backgroundImage = 'url(module' + moduleNumber + '.png)';
//   selectedCard.style.border = '0.2vw solid #B5BC89';
//   if(temp != undefined){
//    var prevSelectedCard = document.querySelector('.cards'+ temp);
//    prevSelectedCard.style.backgroundImage = 'linear-gradient(black, black), url(module' +temp+ '.png)' ;
//    prevSelectedCard.style.border = 'none';
//   }

//   // Hide all competition details

//   var competitionDetails = document.querySelectorAll('.competition-details');

//   competitionDetails.forEach(function (detail) {
//       detail.style.display = 'none';
//   });

//   var selectedModule = document.querySelector('.module' + moduleNumber);
//   selectedModule.style.display = 'flex';

//   temp = moduleNumber;

// }

// ******************************************************************************************************

// JS for Modules Section :

// document.addEventListener('DOMContentLoaded', function () {
//   const modules = document.querySelectorAll('.module');
//   const competitions = document.querySelectorAll('.rectangle-group.module1');
//   let currentClickedModule = null;

//   function handleModuleClick(moduleId) {
//     competitions.forEach((competition) => {
//       const competitionModuleId = competition.getAttribute('data-module-id');

//       if (competitionModuleId === moduleId) {
//         competition.style.display = 'block';
//       } else {
//         competition.style.display = 'none';
//       }
//     });
//   }

//   function toggleGreyscale(module) {
//     const currentFilter = module.style.filter;

//     if (currentFilter.includes('0')) {
//       module.style.filter = 'grayscale(100%)';
//       module.style.border = '';
//     } else {
//       module.style.filter = 'grayscale(0)';
//       module.style.border = '2px solid white';
//     }
//   }

//   modules.forEach((module) => {
//     module.addEventListener('click', function () {
//       if (currentClickedModule && currentClickedModule !== this) {
//         currentClickedModule.classList.remove('clicked');
//         toggleGreyscale(currentClickedModule);
//       }

//       this.classList.toggle('clicked');

//       toggleGreyscale(this);

//       const moduleId = this.getAttribute('data-module-id');
//       handleModuleClick(moduleId);

//       currentClickedModule = this;
//     });
//   });
// });
let prev = null,
  active = true;
function filtermodule(id) {
  if (prev == id) {
    document.getElementById(id).classList.toggle("clicked");
    active = !active;
    prev = null;
    handleModuleClick(active ? id : null);
    document.getElementById("Competitions").scrollIntoView({
      behavior: "smooth",
      block: "start",
      inline: "nearest",
    });
    return;
  }
  active = true;
  handleModuleClick(id);
  if (prev != null) {
    document.getElementById(prev).classList.toggle("clicked");
  }
  document.getElementById(id).classList.toggle("clicked");
  prev = id;
  document.getElementById("Competitions").scrollIntoView({
    behavior: "smooth",
    block: "start",
    inline: "nearest",
  });
}
function handleModuleClick(moduleId) {
  const competitions = document.querySelectorAll(".rectangle-group.module1");

  competitions.forEach((competition) => {
    const competitionModuleId = competition.getAttribute("data-module-id");
    if (moduleId == null) {
      console.log("null");
      competition.style.display = "block";
    } else {
      if (competitionModuleId === moduleId) {
        competition.style.display = "block";
      } else {
        competition.style.display = "none";
      }
    }
  });
}
// ******************************************************************************************************

//FILTER COMPETITIONS:
// Add this script in your HTML or link to an external script

const searchInput = document.getElementById("searchInput");
const compContainer = document.getElementsByClassName(".compContainer");
const rectangleBox = document.querySelectorAll(".rectangle-group");
// const eventNameElements = document.querySelectorAll('.eventName');
// const competitions = Array.from(eventNameElements).map(element => element.innerText);
function performSearch() {
  const searchValue = searchInput.value.toLowerCase();
  for (let i = 0; i < rectangleBox.length; i++) {
    let competition = rectangleBox[i].getElementsByTagName("h6")[0];
    let competitionName = rectangleBox[i].getElementsByTagName("h3")[0];
    let competitiongroup = rectangleBox[i].getElementsByTagName("h5")[0];

    if (competition) {
      let competitiontag = competition.innerText;
      if (
        competitiontag.toLowerCase().indexOf(searchValue) > -1 ||
        competitionName.innerText.toLowerCase().indexOf(searchValue) > -1 ||
        competitiongroup.innerText.toLowerCase().indexOf(searchValue) > -1
      ) {
        rectangleBox[i].style.display = "";
      } else {
        rectangleBox[i].style.display = "none";
      }
    }
  }
}
// searchInput.addEventListener('onkeyup', performSearch);

// function updateTable(filteredCompetitions) {
//     const table = document.getElementById('resultsTable');

//     table.innerHTML = '';

//     filteredCompetitions.forEach(competition => {
//         const row = table.insertRow();
//         const cell = row.insertCell(0);
//         cell.textContent = competition.name;
//     });
// }
