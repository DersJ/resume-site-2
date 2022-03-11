function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function initTooltips() {
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

document.querySelectorAll(".copy-link-button").forEach((el) => {
  el.addEventListener("click", function (e) {
    e.preventDefault();
    // do the copy logic ....
    var inputc = document.body.appendChild(document.createElement("input"));
    inputc.value = window.location.href;
    inputc.focus();
    inputc.select();
    document.execCommand("copy");
    inputc.parentNode.removeChild(inputc);
    // change title for tooltip
    el.setAttribute("data-bs-original-title", "Link copied to clipboard!");

    // show the tooltip with the new title
    bootstrap.Tooltip.getInstance(el).show();
  });
  el.addEventListener("mouseout", (e) => {
    e.preventDefault();
    el.setAttribute("data-bs-original-title", "Click to copy link");
  });
});


function defer(method) {
    if (window.$ && window.bootstrap) {
        method();
    } else {
        setTimeout(function() { defer(method) }, 50);
    }
}

defer(initTooltips);