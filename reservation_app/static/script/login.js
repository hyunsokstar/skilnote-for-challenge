const tabItems = document.querySelectorAll(".tab-menu-subject-item");
const tabContents = document.querySelectorAll(".tab-menu-content-item");

tabItems.forEach((item) => {
  item.addEventListener("click", tabHandler);
});

function tabHandler(item) {
  const tabTarget = item.currentTarget;
  const target = tabTarget.dataset.tab;
  // alert("target : "+ target);
  tabItems.forEach((title) => {
    title.classList.remove("active");
  });
  tabContents.forEach((target) => {
    target.classList.remove("target");
  });
  tabTarget.classList.add("active");
  document.querySelector("#" + target).classList.add("target");
}

