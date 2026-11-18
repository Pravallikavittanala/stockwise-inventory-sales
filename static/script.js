document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-confirm]").forEach(form => {
    form.addEventListener("submit", event => {
      if (!confirm(form.dataset.confirm)) event.preventDefault();
    });
  });
  document.querySelectorAll(".close").forEach(button => {
    button.addEventListener("click", () => button.parentElement.remove());
  });
});
