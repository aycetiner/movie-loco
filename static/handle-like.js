// handles like/unlike of a post

async function processForm(evt) {
  evt.preventDefault();
  let postID = $(this).attr("data-id");

  const resp = await axios({
    method: "POST",
    url: `/users/add_like/${postID}`,
  });
  if ($(this).children("button").hasClass("btn-primary")) {
    $(this).children("button").removeClass("btn-primary");
    $(this).children("button").addClass("btn-secondary");
  } else {
    $(this).children("button").removeClass("btn-secondary");
    $(this).children("button").addClass("btn-primary");
  }
}

$(".messages-form").on("submit", processForm);

// reloads the page when using browser back button

window.addEventListener("pageshow", function (event) {
  var historyTraversal =
    event.persisted ||
    (typeof window.performance != "undefined" &&
      window.performance.navigation.type === 2);
  if (historyTraversal) {
    // Handle page restore.
    window.location.reload();
  }
});
